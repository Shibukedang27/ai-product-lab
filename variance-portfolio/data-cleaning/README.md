# Data cleaning demo — Variance

Synthetic, anonymized customer/orders CSV with common real-world mess: inconsistent casing, currency symbols, bad emails/phones, mixed date formats, blanks, and duplicate order IDs.

## Before → after

| Issue in `sample_messy.csv` | Fix in `clean.py` / `sample_clean.csv` |
|-----------------------------|----------------------------------------|
| Mixed city casing / aliases (`HYDERABAD`, `bengaluru`) | Normalized city names |
| Emails with spaces / bad values | Lowercased, validated, empties cleared |
| Phones as `N/A`, leading 0, `91-…` | E.164-ish `+91 XXXXXXXXXX` or blank |
| Amounts with `₹`, `Rs.`, commas | Numeric `0.00` strings; negatives dropped |
| Dates as `D/M/Y`, `Y/M/D`, invalid | ISO `YYYY-MM-DD` or blank |
| Duplicate `order_id` | Keep last occurrence |
| Empty names + emails | Row dropped |

## How to run

```bash
cd /workspace/freelance-setup/portfolio/data-cleaning
python3 clean.py
```

Optional flags:

```bash
python3 clean.py --input sample_messy.csv --output sample_clean.csv
```

No pip installs required (stdlib only).

## Files

| File | Role |
|------|------|
| `sample_messy.csv` | Generated messy input (40 rows) |
| `clean.py` | Cleaning script |
| `sample_clean.csv` | Cleaned output (regenerate with `python3 clean.py`) |

## Notes

All data is fictional. Safe for portfolios — no secrets or API keys.
