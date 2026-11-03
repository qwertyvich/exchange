import math
from copy import deepcopy


def validated_settings(previous, incoming):
    if not isinstance(incoming, dict):
        raise ValueError("Ожидается объект настроек")
    result = {**deepcopy(previous), **deepcopy(incoming)}
    if str(result.get("mode")) not in {"0", "1", "2"}:
        raise ValueError("Выберите один из трёх режимов")
    result["mode"] = str(result["mode"])
    def number(value, label, minimum=0, maximum=1e15):
        try:
            n = float(value)
        except (ValueError, TypeError):
            raise ValueError(f"{label}: укажите число")
        if not math.isfinite(n) or not minimum <= n <= maximum:
            raise ValueError(f"{label}: число вне допустимого диапазона")
        return n
    result["percent"] = number(result.get("percent", 0), "Комиссия", maximum=99.99)
    for key in ("giveMin", "giveMax", "getMin", "getMax"):
        result[key] = number(result.get(key, 0), key)
    if result["giveMin"] > result["giveMax"] or result["getMin"] > result["getMax"]:
        raise ValueError("Минимальный лимит не может превышать максимальный")
    for key, rule in result.get("direction_rates", {}).items():
        parts = key.split(":")
        if len(parts) != 2 or not all(p.isdigit() for p in parts) or parts[0] == parts[1] or not isinstance(rule, dict):
            raise ValueError("Неверное направление обмена")
        if rule.get("rate") not in (None, "", 0):
            rule["rate"] = number(rule["rate"], "Ручной курс", minimum=1e-15)
        else:
            rule.pop("rate", None)
        if "fee_percent" in rule:
            rule["fee_percent"] = number(rule["fee_percent"], "Комиссия направления", maximum=99.99)
        for field in ("min_amount", "max_amount"):
            if rule.get(field) not in (None, ""):
                rule[field] = number(rule[field], "Лимит направления")
            else:
                rule.pop(field, None)
        if rule.get("max_amount") and rule.get("min_amount", 0) > rule["max_amount"]:
            raise ValueError("Лимиты направления заданы неверно")
    for row in result.get("fiat_in", {}).values():
        lo, hi = number(row.get("from"), "От"), number(row.get("to"), "До")
        if lo > hi:
            raise ValueError("Неверный диапазон ввода рублей")
        number(row.get("rate"), "Курс ввода рублей", minimum=1e-15)
    for row in result.get("deposit_wallets", {}).values():
        for field in ("course_rub", "course_usdt"):
            if row.get(field) not in (None, ""):
                number(row[field], "Ручной курс валюты")
    return result
