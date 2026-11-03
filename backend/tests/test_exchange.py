import os
import time
import unittest
from copy import deepcopy
from decimal import Decimal
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.db import Base
from app import main
from app.rates import rate_table, make_quote, decode_quote
from app.models import User
from app.auth import create_access_token
from app.settings_validation import validated_settings


SETTINGS = {"mode": "0", "percent": 2, "giveMin": 10, "giveMax": 100000, "getMin": 0, "getMax": 100000,
    "deposit_wallets": {"2102": {"name": "Турция", "symbol": "TRY", "course_rub": "3.2", "course_usdt": "0.0356"}},
    "fiat_in": {"1": {"from": 1000, "to": 10000, "rate": 100}, "2": {"from": 10001, "to": 50000, "rate": 110}}}


def market():
    return {"fetched_at": time.time(), "fiat_fetched_at": time.time(), "usd": {"bitcoin": 50000, "ethereum": 2500, "tether": 1},
            "fiat_rub": {"USD": 100, "RUB": 1, "TRY": 2.5}, "source": "fixture"}


class RatesTests(unittest.TestCase):
    def test_automatic_rate_includes_fee_once(self):
        row = rate_table(SETTINGS, market())["directions"]["1:2"]
        self.assertAlmostEqual(row["rate"], 19.6)
        self.assertAlmostEqual(rate_table(SETTINGS, market())["directions"]["1:2001"]["rate"], 4900000)

    def test_manual_rate_has_priority_and_is_directional(self):
        settings = {**SETTINGS, "direction_rates": {"1:2": {"rate": 22}}}
        rows = rate_table(settings, market())["directions"]
        self.assertEqual(rows["1:2"]["rate"], 22)
        self.assertEqual(rows["1:2"]["fee_percent"], 0)
        self.assertAlmostEqual(rows["2:1"]["rate"], 0.049)

    def test_stale_automatic_quotes_are_disabled_manual_survives(self):
        snapshot = market(); snapshot["fetched_at"] = 0
        settings = {**SETTINGS, "direction_rates": {"1:2": {"rate": 22, "min_amount": 1, "max_amount": 10}}}
        rows = rate_table(settings, snapshot)["directions"]
        self.assertEqual(rows["1:2001"]["rate"], 0)
        self.assertEqual(rows["1:2"]["rate"], 22)
        self.assertEqual(rows["1:2"]["max_give"], 10)

    def test_all_modes_and_legacy_course_convention(self):
        self.assertNotIn("2101:1", rate_table(SETTINGS, market())["directions"])
        rows = rate_table({**SETTINGS, "mode": "1"}, market())["directions"]
        self.assertEqual(len(rows["2101:1"]["tiers"]), 2)
        rows = rate_table({**SETTINGS, "mode": "2"}, market())["directions"]
        self.assertAlmostEqual(rows["2101:2102"]["rate"], 0.3125)
        self.assertAlmostEqual(rows["3:2102"]["rate"], 1 / 0.0356)
        self.assertNotIn("1:2", rows)

    def test_cbr_automatic_fiat_cross_rate(self):
        settings = deepcopy(SETTINGS); settings["mode"] = "2"; settings["deposit_wallets"]["2102"] = {"symbol": "TRY"}
        self.assertAlmostEqual(rate_table(settings, market())["directions"]["3:2102"]["rate"], 39.2)

    def test_tiers_rounding_limits_and_signature(self):
        with patch("app.rates.read_document", return_value=market()):
            q = make_quote({**SETTINGS, "mode": "1"}, 2101, 1, "11000")
            self.assertEqual(Decimal(q["get_amount"]), Decimal("0.00200000"))
            self.assertEqual(decode_quote(q["quote_token"])["get_id"], 1)
            with self.assertRaises(ValueError):
                make_quote(SETTINGS, 1, 2, "0")
            with self.assertRaises(ValueError):
                make_quote(SETTINGS, 1, 2, "999999999")
            with self.assertRaises(ValueError):
                decode_quote(q["quote_token"] + "bad")
            with self.assertRaises(ValueError):
                make_quote({**SETTINGS, "mode": "2"}, 2101, 2102, "10000.5")

    def test_settings_validation_preserves_unknown_fields(self):
        old = {**SETTINGS, "fiat_in_methods": {"keep": 1}}
        self.assertEqual(validated_settings(old, {"mode": "2"})["fiat_in_methods"], {"keep": 1})
        for change in ({"percent": -1}, {"percent": "NaN"}, {"mode": "9"}, {"direction_rates": {"1:2": {"rate": -2}}}):
            with self.assertRaises(ValueError): validated_settings(old, change)


class TicketApiTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)
        def get_db():
            with self.session() as db: yield db
        main.app.dependency_overrides[main.get_db] = get_db
        self.client = TestClient(main.app)
        self.config = patch("app.main.load_settings", return_value=deepcopy(SETTINGS)); self.config.start()
        self.snapshot = patch("app.rates.read_document", return_value=market()); self.snapshot.start()
        self.telegram = patch.dict(os.environ, {"TELEGRAM_ENABLED": "false"}); self.telegram.start()

    def tearDown(self):
        self.telegram.stop(); self.snapshot.stop(); self.config.stop()
        self.client.close(); main.app.dependency_overrides.clear(); self.engine.dispose()

    def payload(self):
        q = self.client.post("/api/quote", json={"give_id": 1, "get_id": 2, "amount": "1"}).json()
        return {"give": {"currency_backend_id": 1, "symbol": "FAKE", "amount": 999},
            "get": {"currency_backend_id": 2, "symbol": "FAKE", "amount": 999999}, "fee_percent": 0,
            "client": {"telegram": "@example_user", "payout_details": "test wallet"}, "rates_snapshot": {},
            "created_at": "2000-01-01", "quote_token": q["quote_token"]}

    def test_browser_cannot_override_signed_amounts_and_ticket_is_private(self):
        response = self.client.post("/api/tickets", json=self.payload())
        self.assertEqual(response.status_code, 200, response.text)
        ticket_id = response.json()["ticket_id"]
        ticket = self.client.get(f"/api/tickets/{ticket_id}").json()
        self.assertEqual(float(ticket["give"]["amount"]), 1)
        self.assertEqual(float(ticket["get"]["amount"]), 19.6)
        self.assertEqual(ticket["give"]["symbol"], "BTC")
        self.client.cookies.clear()
        for method, url in (("get", f"/api/tickets/{ticket_id}"), ("patch", f"/api/tickets/{ticket_id}/cancel"), ("patch", f"/api/tickets/{ticket_id}/confirm")):
            self.assertEqual(getattr(self.client, method)(url).status_code, 404)

    def test_missing_forged_or_wrong_direction_quote_is_rejected(self):
        payload = self.payload(); payload["quote_token"] = "forged"
        self.assertEqual(self.client.post("/api/tickets", json=payload).status_code, 409)
        payload = self.payload(); payload["get"]["currency_backend_id"] = 3
        self.assertEqual(self.client.post("/api/tickets", json=payload).status_code, 400)

    def test_repeated_submit_returns_the_same_ticket(self):
        payload = self.payload()
        a = self.client.post("/api/tickets", json=payload)
        b = self.client.post("/api/tickets", json=payload)
        self.assertEqual(a.status_code, 200)
        self.assertEqual(b.status_code, 200)
        self.assertEqual(a.json()["ticket_id"], b.json()["ticket_id"])

    def test_member_ticket_requires_its_owner_token_for_read_and_actions(self):
        with self.session() as db:
            db.add(User(id="owner", name="Owner", email="owner@example.com", password_hash="unused", role="user", is_superuser=False))
            db.commit()
        headers = {"Authorization": f"Bearer {create_access_token('owner')}"}
        for action in ("cancel", "confirm"):
            created = self.client.post("/api/tickets", json=self.payload(), headers=headers)
            self.assertEqual(created.status_code, 200, created.text)
            ticket_id = created.json()["ticket_id"]
            url = f"/api/tickets/{ticket_id}"
            self.assertEqual(self.client.get(url).status_code, 404)
            self.assertEqual(self.client.get(url, headers=headers).status_code, 200)
            self.assertEqual(self.client.patch(f"{url}/{action}").status_code, 404)
            changed = self.client.patch(f"{url}/{action}", headers=headers)
            self.assertEqual(changed.status_code, 200, changed.text)
            self.assertEqual(changed.json()["status"], "cancelled" if action == "cancel" else "not_confirmed")


if __name__ == "__main__": unittest.main()
