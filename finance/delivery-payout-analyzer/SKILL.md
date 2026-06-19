---
name: delivery-payout-analyzer
description: Food delivery payout and promotion profitability analyzer. Use when a user shares Uber Eats / Deliveroo / Just Eat gross and net sales, mentions promotional discounts, payouts, royalties or commission, or asks whether running promotions is worth it.
license: MIT
metadata:
  version: 1.0.0
  author: Mahar Group Operations
  category: finance
  updated: 2026-06-18
---

# Delivery Payout Analyzer

Turn food delivery platform sales figures into the cash the business actually
receives, and test whether heavier promotions leave the business better or
worse off. Built for Mahar Group food businesses (UFO Food / Wraps and Wings,
Cafe UFO, Mahar Coffee), UK VAT at 20%.

## Metric definitions

See [references/sales-metrics-definitions.md](references/sales-metrics-definitions.md)
for the full set. In short:

- **Gross sales** = order value INCLUDING promotional discounts.
- **Net sales** = order value EXCLUDING promotional discounts (what customers paid).
- **Payout** = `Net - (royalty 30% + VAT) - (ads + VAT)`.
- **Contribution** = `Payout - food cost` (food cost defaults to 33% of net).

## Step 1 - Collect inputs

For each trading period, gather:

- Gross sales and Net sales (from the platform "Business performance" screen).
- Ad spend (ex VAT) if known. If not, supply the **actual bank payout** and the
  tool will reverse-engineer ad spend.
- Optional: `in_store_inc_vat` (EPOS sales, inc VAT after discount) and labour
  (`labour_hours` + `labour_rate`, or a direct `labour_cost`) to extend the
  model to a full-business contribution after labour.
- Optional overrides: royalty rate (default 30%), VAT (20%), food cost (33%).

To compare promotion levels, collect **two** periods: a lighter-promo baseline
and a heavier-promo test period.

## Step 2 - Run the calculator

```bash
python3 scripts/payout_calculator.py assets/example_input.json
python3 scripts/payout_calculator.py my_data.json --format json
python3 scripts/payout_calculator.py my_data.json --food-cost-rate 0.28
```

Input JSON shape (see `assets/example_input.json`):

```json
{
  "royalty_rate": 0.30,
  "vat_rate": 0.20,
  "food_cost_rate": 0.33,
  "periods": [
    { "name": "light promo", "gross": 5589.92, "net": 4885.03, "actual_payout": 2357.39 },
    { "name": "heavy promo", "gross": 7955.43, "net": 6394.03, "actual_payout": 3131.13 }
  ]
}
```

## Step 3 - Read the verdict

The tool reports, per period: promo discount, royalty, ads, payout (and payout
as a % of net), food cost and contribution. With two periods it adds a
comparison and a **verdict** based on the change in **contribution**.

Key principle: a promotion only pays if the **extra net sales it drives** cover
the extra discount, commission and food cost. A deeper discount on orders that
would have happened anyway is pure margin loss, so always cross-check that
**order counts** actually rose. Two weeks is a directional signal, not proof -
track several cycles before fixing strategy.

## Files

- `scripts/payout_calculator.py` - payout + promotion comparison (stdlib only, `--help`, `--format json`).
- `scripts/food_cost_from_statement.py` - estimate food cost % from a bank statement CSV/TSV by classifying suppliers (`--sales`, `--grossup`, `--include-uncertain`, `--format json`).
- `references/sales-metrics-definitions.md` - metric definitions and worked example.
- `assets/example_input.json` - UFO Food June 2026 two-week comparison.
