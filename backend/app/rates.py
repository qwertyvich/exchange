"""One shared, persistent market cache. Clients never call market providers."""
import asyncio
import json
import logging
import os
import time
import secrets
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_DOWN
from datetime import datetime, timezone, timedelta
import httpx
from jose import jwt, JWTError
from sqlalchemy import text
from .auth import JWT_SECRET, JWT_ALG
from .db import engine
from .documents import read_document, write_document

log = logging.getLogger(__name__)
CRYPTO = {
    1: ("bitcoin", "BTC", "XBTUSD"), 2: ("ethereum", "ETH", "ETHUSD"),
    3: ("tether", "USDT", "USDTUSD"), 4: ("tether", "USDT", "USDTUSD"),
    5: ("tether", "USDT", "USDTUSD"), 6: ("tether", "USDT", "USDTUSD"),
    7: ("dai", "DAI", "DAIUSD"), 8: ("usd-coin", "USDC", "USDCUSD"),
    9: ("solana", "SOL", "SOLUSD"), 10: ("litecoin", "LTC", "LTCUSD"),
    11: ("tron", "TRX", "TRXUSD"), 12: ("dogecoin", "DOGE", "XDGUSD"),
}
RUB_OUT = {2001: "СБП", 2011: "Сбер QR", 2002: "Сбер", 2003: "Альфа-банк", 2010: "Наличные RUB"}
INTERVAL = max(300, int(os.getenv("RATES_REFRESH_SECONDS", "300")))
MAX_AGE = int(os.getenv("RATES_MAX_AGE_SECONDS", "900"))


def positive(value):
    try:
        v = float(value)
        return v if 0 < v < 1e20 else 0
    except (TypeError, ValueError):
        return 0


async def refresh_market():
    # Advisory lock and next_attempt apply across workers, restarts and users.
    with engine.connect() as conn:
        postgres = engine.dialect.name == "postgresql"
        if postgres and not conn.execute(text("SELECT pg_try_advisory_lock(708182)" )).scalar():
            return
        try:
            old = read_document("market", {})
            now = time.time()
            if now < old.get("next_attempt", 0):
                return
            state = {**old, "next_attempt": now + INTERVAL}
            write_document("market", state)
            async with httpx.AsyncClient(timeout=12, follow_redirects=True) as client:
                if now - state.get("fiat_fetched_at", 0) > 3600:
                    try:
                        response = await client.get("https://www.cbr.ru/scripts/XML_daily.asp")
                        response.raise_for_status()
                        root = ET.fromstring(response.content)
                        rub = {"RUB": 1.0}
                        for row in root.findall("Valute"):
                            rub[row.findtext("CharCode")] = float(row.findtext("Value").replace(",", ".")) / int(row.findtext("Nominal"))
                        if positive(rub.get("USD")):
                            state.update(fiat_rub=rub, fiat_date=root.attrib.get("Date"), fiat_fetched_at=now)
                    except (httpx.HTTPError, ET.ParseError, ValueError, TypeError):
                        log.warning("CBR rates unavailable; keeping the previous snapshot")
                prices = None
                try:
                    key = os.getenv("COINGECKO_API_KEY", "")
                    response = await client.get("https://api.coingecko.com/api/v3/simple/price",
                        params={"ids": ",".join(sorted({r[0] for r in CRYPTO.values()})), "vs_currencies": "usd", "include_last_updated_at": "true"},
                        headers={"x-cg-demo-api-key": key} if key else {})
                    response.raise_for_status()
                    data = response.json()
                    prices = {coin: float(data[coin]["usd"]) for coin in {r[0] for r in CRYPTO.values()}
                              if positive(data.get(coin, {}).get("usd")) and now - data[coin].get("last_updated_at", 0) <= MAX_AGE}
                    if len(prices) < len({r[0] for r in CRYPTO.values()}):
                        raise ValueError("Incomplete/stale provider snapshot")
                    state["source"] = "CoinGecko"
                except (httpx.HTTPError, ValueError, KeyError, TypeError):
                    try:
                        # Kraken's last USD trades are an independent fallback, not invented prices.
                        response = await client.get("https://api.kraken.com/0/public/Ticker",
                            params={"pair": ",".join(sorted({r[2] for r in CRYPTO.values()}))})
                        response.raise_for_status()
                        data = response.json()
                        if data.get("error"):
                            raise ValueError("Kraken provider error")
                        aliases = {"XBTUSD": "XXBTZUSD", "ETHUSD": "XETHZUSD", "LTCUSD": "XLTCZUSD", "XDGUSD": "XXDGZUSD"}
                        prices = {}
                        for coin, _, pair in CRYPTO.values():
                            row = data["result"].get(pair) or data["result"].get(aliases.get(pair, pair))
                            if not row or not positive(row["c"][0]):
                                raise ValueError("Incomplete Kraken snapshot")
                            prices[coin] = float(row["c"][0])
                        state["source"] = "Kraken"
                    except (httpx.HTTPError, ValueError, KeyError, TypeError):
                        prices = None
                        log.warning("Crypto providers unavailable; keeping previous rates")
                if prices:
                    state.update(usd=prices, fetched_at=now, failures=0)
                else:
                    failures = old.get("failures", 0) + 1
                    state.update(failures=failures, next_attempt=now + min(INTERVAL * 2 ** min(failures, 4), 3600))
                write_document("market", state)
        finally:
            if postgres:
                conn.execute(text("SELECT pg_advisory_unlock(708182)"))


async def rates_worker():
    while True:
        try:
            await refresh_market()
        except asyncio.CancelledError:
            raise
        except Exception:
            log.exception("Rate refresh failed")
        await asyncio.sleep(15)


def currency_catalog(settings):
    rows = {i: {"id": i, "symbol": symbol, "coin": coin, "name": settings.get("deposit_wallets", {}).get(str(i), {}).get("name", symbol)}
            for i, (coin, symbol, _) in CRYPTO.items()}
    rows.update({i: {"id": i, "symbol": "RUB", "name": name} for i, name in RUB_OUT.items()})
    rows[2101] = {"id": 2101, "symbol": "RUB", "name": "Перевод на карту"}
    for key, row in settings.get("deposit_wallets", {}).items():
        if key.isdigit() and int(key) >= 2102 and row.get("symbol"):
            rows[int(key)] = {"id": int(key), "symbol": str(row["symbol"]).upper(), "name": row.get("name", row["symbol"])}
    return rows


def allowed_pair(give, get, mode):
    if give == get:
        return False
    if mode == "0":
        return give in CRYPTO and (get in CRYPTO or get in RUB_OUT)
    if mode == "1":
        return (give in CRYPTO and (get in CRYPTO or get in RUB_OUT)) or (give == 2101 and get in CRYPTO)
    return give in {3, 4, 5, 6, 2101} and get >= 2102


def rate_table(settings, market=None):
    market = read_document("market", {}) if market is None else market
    now = time.time()
    fresh = now - market.get("fetched_at", 0) <= MAX_AGE
    fiat_fresh = now - market.get("fiat_fetched_at", 0) <= 4 * 24 * 3600
    catalog = currency_catalog(settings)
    fiat_rub = market.get("fiat_rub", {}) if fiat_fresh else {}
    usd_rub = positive(fiat_rub.get("USD"))
    def price(row):
        if row.get("coin"):
            return positive(market.get("usd", {}).get(row["coin"])) if fresh else 0
        return positive(fiat_rub.get(row["symbol"])) / usd_rub if usd_rub else 0
    output = {}
    for give in catalog:
        for get in catalog:
            if not allowed_pair(give, get, str(settings.get("mode", "0"))):
                continue
            a, b = catalog[give], catalog[get]
            p, q = price(a), price(b)
            rule = settings.get("direction_rates", {}).get(f"{give}:{get}", {})
            fee = float(rule.get("fee_percent", settings.get("percent", 0)))
            manual = positive(rule.get("rate"))
            tiers = []
            rate, source = 0, "unavailable"
            numerator, denominator = Decimal(0), Decimal(1)
            if manual:
                rate, source = manual, "manual"
                numerator = Decimal(str(rule["rate"]))
                fee = 0  # Manual rates already include the operator's margin.
            elif str(settings.get("mode")) == "2":
                legacy = settings.get("deposit_wallets", {}).get(str(get), {})
                course = positive(legacy.get("course_rub" if give == 2101 else "course_usdt"))
                if course:
                    rate, source, fee = 1 / course, "manual_legacy", 0
                    numerator, denominator = Decimal(1), Decimal(str(course))
            elif give == 2101 and q:
                for tier in settings.get("fiat_in", {}).values():
                    cost = positive(tier.get("rate"))
                    if cost:
                        denom = Decimal(str(cost)) * Decimal(str(q))
                        tiers.append({"from": float(tier["from"]), "to": float(tier["to"]), "rate": float(Decimal(1) / denom), "numerator": "1", "denominator": str(denom)})
                tiers.sort(key=lambda t: t["from"])
                if tiers:
                    rate, source, fee = tiers[0]["rate"], "manual_tiers", 0
                    numerator, denominator = Decimal(1), Decimal(tiers[0]["denominator"])
            if not rate and p and q:
                rate, source = p / q * (1 - fee / 100), "market"
                numerator = Decimal(str(p)) * (Decimal(1) - Decimal(str(fee)) / 100)
                denominator = Decimal(str(q))
            min_give = float(settings.get("giveMin", 0)) / p if p else 0
            max_give = float(settings.get("giveMax", 0)) / p if p else 0
            if give == 2101 and settings.get("fiat_in"):
                min_give = min(float(t["from"]) for t in settings["fiat_in"].values())
                max_give = max(float(t["to"]) for t in settings["fiat_in"].values())
            # Legacy mode 2 specifies USD/USDT limits even for entirely manual directions.
            if str(settings.get("mode")) == "2" and give in {3, 4, 5, 6}:
                min_give, max_give = float(settings.get("giveMin", 0)), float(settings.get("giveMax", 0))
            if positive(rule.get("min_amount")):
                min_give = float(rule["min_amount"])
            if positive(rule.get("max_amount")):
                max_give = float(rule["max_amount"])
            output[f"{give}:{get}"] = {"rate": rate, "source": source, "fee_percent": fee, "tiers": tiers,
                "numerator": str(numerator), "denominator": str(denominator),
                "funding_ranges": [{"from": float(t["from"]), "to": float(t["to"])} for t in settings.get("fiat_in", {}).values()] if give == 2101 else [],
                "min_give": min_give, "max_give": max_give,
                "min_get": float(settings.get("getMin", 0)) / q if q and str(settings.get("mode")) != "2" else 0,
                "max_get": float(settings.get("getMax", 0)) / q if q and str(settings.get("mode")) != "2" else 0}
    return {"directions": output, "currencies": list(catalog.values()), "updated_at": market.get("fetched_at"),
            "source": market.get("source"), "fiat_date": market.get("fiat_date"), "stale": not fresh,
            "refresh_seconds": INTERVAL}


def make_quote(settings, give_id, get_id, amount):
    table = rate_table(settings)
    row = table["directions"].get(f"{give_id}:{get_id}")
    amount = Decimal(str(amount))
    if not amount.is_finite() or amount <= 0:
        raise ValueError("Укажите положительную сумму")
    if not row or not row["rate"]:
        raise ValueError("Курс направления временно недоступен")
    rate = row["rate"]
    numerator, denominator = row["numerator"], row["denominator"]
    if row["tiers"]:
        tier = next((t for t in row["tiers"] if t["from"] <= amount <= t["to"]), None)
        if not tier:
            raise ValueError("Сумма вне доступных диапазонов")
        rate = tier["rate"]
        numerator, denominator = tier["numerator"], tier["denominator"]
    if row["funding_ranges"] and not any(Decimal(str(t["from"])) <= amount <= Decimal(str(t["to"])) for t in row["funding_ranges"]):
        raise ValueError("Сумма вне доступных диапазонов приёма рублей")
    if not row["max_give"]:
        raise ValueError("Нет актуального курса для проверки лимитов; задайте лимиты направления")
    if not Decimal(str(row["min_give"])) <= amount <= Decimal(str(row["max_give"])):
        raise ValueError(f"Сумма должна быть от {row['min_give']:.8g} до {row['max_give']:.8g}")
    catalog = {r["id"]: r for r in table["currencies"]}
    step = Decimal("0.00000001") if get_id in CRYPTO else Decimal("0.01")
    result = (amount * Decimal(numerator) / Decimal(denominator)).quantize(step, rounding=ROUND_DOWN)
    if result <= 0:
        raise ValueError("Сумма слишком мала")
    if row["min_get"] and result < Decimal(str(row["min_get"])) or row["max_get"] and result > Decimal(str(row["max_get"])):
        raise ValueError("Сумма получения вне лимитов направления")
    now = datetime.now(timezone.utc)
    quote = {"kind": "quote", "jti": secrets.token_hex(16), "give_id": give_id, "get_id": get_id, "give_amount": str(amount), "get_amount": str(result),
             "give_symbol": catalog[give_id]["symbol"], "get_symbol": catalog[get_id]["symbol"],
             "rate": rate, "fee_percent": row["fee_percent"], "source": row["source"],
             "exp": int((now + timedelta(seconds=60)).timestamp())}
    return {**quote, "quote_token": jwt.encode(quote, JWT_SECRET, algorithm=JWT_ALG)}


def decode_quote(token):
    try:
        result = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        if result.get("kind") != "quote" or not result.get("jti"):
            raise ValueError()
        return result
    except (JWTError, ValueError):
        raise ValueError("Курс обновился. Пересчитайте обмен и повторите отправку")
