#!/usr/bin/env python3
"""Variance portfolio demo — clean a messy customer/orders CSV.

Usage:
    python3 clean.py
    python3 clean.py --input sample_messy.csv --output sample_clean.csv

No third-party deps.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

CITY_MAP = {
    "hyderabad": "Hyderabad",
    "secunderabad": "Secunderabad",
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "mumbai": "Mumbai",
}

STATUS_MAP = {
    "active": "active",
    "inactive": "inactive",
    "churned": "churned",
}


def clean_text(value: str | None) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def clean_email(value: str) -> str:
    email = clean_text(value).lower()
    email = re.sub(r"\.{2,}", ".", email)
    if not email or "@" not in email or email.startswith("@") or email.endswith("@"):
        return ""
    local, _, domain = email.partition("@")
    if not local or "." not in domain:
        return ""
    return email


def clean_phone(value: str) -> str:
    raw = clean_text(value)
    if not raw or raw.upper() in {"N/A", "NA", "NONE", "-"}:
        return ""
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("91") and len(digits) >= 12:
        digits = digits[-10:]
    elif digits.startswith("0") and len(digits) == 11:
        digits = digits[1:]
    if len(digits) != 10:
        return ""
    return f"+91 {digits}"


def clean_city(value: str) -> str:
    city = clean_text(value).lower()
    if not city:
        return ""
    return CITY_MAP.get(city, clean_text(value).title())


def clean_status(value: str) -> str:
    status = clean_text(value).lower()
    return STATUS_MAP.get(status, "")


def clean_amount(value: str) -> str:
    raw = clean_text(value)
    if not raw:
        return ""
    raw = raw.replace("₹", "").replace("Rs.", "").replace("rs.", "").replace(",", "")
    raw = re.sub(r"[^0-9.\-]", "", raw)
    if not raw or raw in {".", "-", "-."}:
        return ""
    try:
        amount = float(raw)
    except ValueError:
        return ""
    if amount < 0:
        return ""
    return f"{amount:.2f}"


def clean_date(value: str) -> str:
    raw = clean_text(value)
    if not raw:
        return ""
    formats = ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%m/%d/%Y")
    for fmt in formats:
        try:
            dt = datetime.strptime(raw, fmt)
            if dt.year < 2000 or dt.year > 2100:
                return ""
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return ""


def clean_name(value: str) -> str:
    name = clean_text(value)
    if not name:
        return ""
    return " ".join(part.capitalize() for part in name.split(" "))


def clean_row(row: dict[str, str]) -> dict[str, str]:
    return {
        "order_id": clean_text(row.get("order_id", "")).upper(),
        "customer_name": clean_name(row.get("customer_name", "")),
        "email": clean_email(row.get("email", "")),
        "phone": clean_phone(row.get("phone", "")),
        "city": clean_city(row.get("city", "")),
        "status": clean_status(row.get("status", "")),
        "amount": clean_amount(row.get("amount", "")),
        "order_date": clean_date(row.get("order_date", "")),
        "notes": clean_text(row.get("notes", "")).lower(),
    }


def is_usable(row: dict[str, str]) -> bool:
    if not row["order_id"]:
        return False
    if not row["customer_name"] and not row["email"]:
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean messy CSV for Variance portfolio demo")
    parser.add_argument("--input", default="sample_messy.csv")
    parser.add_argument("--output", default="sample_clean.csv")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    in_path = root / args.input if not Path(args.input).is_absolute() else Path(args.input)
    out_path = root / args.output if not Path(args.output).is_absolute() else Path(args.output)

    with in_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw_rows = list(reader)

    cleaned: list[dict[str, str]] = []
    dropped = 0
    for row in raw_rows:
        c = clean_row(row)
        if is_usable(c):
            cleaned.append(c)
        else:
            dropped += 1

    deduped: dict[str, dict[str, str]] = {}
    for row in cleaned:
        deduped[row["order_id"]] = row
    final_rows = list(deduped.values())
    dupes_removed = len(cleaned) - len(final_rows)

    fieldnames = [
        "order_id",
        "customer_name",
        "email",
        "phone",
        "city",
        "status",
        "amount",
        "order_date",
        "notes",
    ]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_rows)

    cities = Counter(r["city"] for r in final_rows if r["city"])
    print("Variance data-cleaning demo")
    print(f"  input:          {in_path.name} ({len(raw_rows)} rows)")
    print(f"  output:         {out_path.name} ({len(final_rows)} rows)")
    print(f"  dropped:        {dropped} unusable rows")
    print(f"  deduped:        {dupes_removed} duplicate order_id(s)")
    top = ", ".join(f"{c} ({n})" for c, n in cities.most_common(3)) or "n/a"
    print(f"  top cities:     {top}")
    print("Done.")


if __name__ == "__main__":
    main()
