#!/usr/bin/env python3
"""Delivery payout and promotion profitability calculator.

Computes the payout from a food delivery platform (Uber Eats, Deliveroo, etc.)
from gross sales, net sales and ad spend, then compares two trading periods to
test whether running heavier promotions leaves the business better or worse off.

Metric definitions (as used across Mahar Group food businesses):
  - Gross sales      : total order value INCLUDING promotional discounts.
  - Net sales        : gross sales EXCLUDING promotional discounts
                       (i.e. what customers actually paid, gross minus promo).
  - Promo discount   : gross - net.
  - Royalty          : platform commission, charged on NET sales (default 30%).
  - Payout           : net - (royalty + VAT on royalty) - (ads + VAT on ads).
  - Contribution     : payout - food cost (food cost defaults to 25% of net).
                       This is profit after platform, ads and ingredients,
                       but BEFORE labour, rent and other fixed costs.

Standard library only. UK VAT defaults to 20%.
"""

import argparse
import json
import sys


def _money(x):
    return round(float(x) + 0.0, 2)


def compute_period(period, royalty_rate, vat_rate, food_cost_rate):
    """Compute the full payout breakdown for a single trading period.

    period keys:
      name          (str)            label for the period
      gross         (float)          gross sales incl. promo discount
      net           (float)          net sales excl. promo discount
      ads           (float, opt)     ad spend EXCLUDING VAT
      actual_payout (float, opt)     payout actually received (reverse-engineers ads)
    """
    name = period.get("name", "period")
    gross = float(period["gross"])
    net = float(period["net"])

    promo_discount = gross - net
    promo_pct = (promo_discount / gross) if gross else 0.0

    royalty = net * royalty_rate
    royalty_vat = royalty * vat_rate
    royalty_incl_vat = royalty + royalty_vat

    # Ads: either supplied (ex VAT) or reverse-engineered from the actual payout.
    actual_payout = period.get("actual_payout")
    if period.get("ads") is not None:
        ads = float(period["ads"])
        ads_incl_vat = ads * (1 + vat_rate)
        ads_source = "input"
    elif actual_payout is not None:
        # payout = net - royalty_incl_vat - ads_incl_vat  ->  solve for ads
        ads_incl_vat = net - royalty_incl_vat - float(actual_payout)
        ads = ads_incl_vat / (1 + vat_rate)
        ads_source = "implied from actual payout"
    else:
        ads = 0.0
        ads_incl_vat = 0.0
        ads_source = "assumed zero"

    payout = net - royalty_incl_vat - ads_incl_vat
    if actual_payout is not None and ads_source == "input":
        payout = float(actual_payout)  # trust the bank figure when both given

    food_cost = net * food_cost_rate
    contribution = payout - food_cost

    payout_pct_of_net = (payout / net) if net else 0.0

    return {
        "name": name,
        "gross_sales": _money(gross),
        "net_sales": _money(net),
        "promo_discount": _money(promo_discount),
        "promo_discount_pct_of_gross": round(promo_pct * 100, 1),
        "royalty": _money(royalty),
        "royalty_vat": _money(royalty_vat),
        "royalty_incl_vat": _money(royalty_incl_vat),
        "ads_ex_vat": _money(ads),
        "ads_incl_vat": _money(ads_incl_vat),
        "ads_source": ads_source,
        "payout": _money(payout),
        "payout_pct_of_net": round(payout_pct_of_net * 100, 1),
        "food_cost": _money(food_cost),
        "contribution": _money(contribution),
    }


def compare_periods(base, test, food_cost_rate):
    """Compare a baseline (lighter promo) period against a test (heavier promo) period."""
    d_gross = test["gross_sales"] - base["gross_sales"]
    d_net = test["net_sales"] - base["net_sales"]
    d_promo = test["promo_discount"] - base["promo_discount"]
    d_payout = test["payout"] - base["payout"]
    d_contribution = test["contribution"] - base["contribution"]

    # Payout generated per extra £1 of net sales the promotion brought in.
    payout_per_extra_net = (d_payout / d_net) if d_net else 0.0

    if d_contribution > 0:
        verdict = "BETTER OFF with the heavier promotion"
    elif d_contribution < 0:
        verdict = "WORSE OFF with the heavier promotion"
    else:
        verdict = "NEUTRAL"

    return {
        "baseline": base["name"],
        "test": test["name"],
        "delta_gross": _money(d_gross),
        "delta_net": _money(d_net),
        "delta_promo_discount": _money(d_promo),
        "delta_payout": _money(d_payout),
        "delta_contribution": _money(d_contribution),
        "payout_per_extra_pound_of_net": round(payout_per_extra_net, 3),
        "food_cost_rate_used": food_cost_rate,
        "verdict": verdict,
    }


def render_text(periods, comparison):
    lines = []
    lines.append("DELIVERY PAYOUT ANALYSIS")
    lines.append("=" * 60)
    for p in periods:
        lines.append("")
        lines.append(p["name"])
        lines.append("-" * len(p["name"]))
        lines.append(f"  Gross sales (incl promo)   £{p['gross_sales']:,.2f}")
        lines.append(f"  Net sales (excl promo)     £{p['net_sales']:,.2f}")
        lines.append(f"  Promo discount             £{p['promo_discount']:,.2f}  ({p['promo_discount_pct_of_gross']}% of gross)")
        lines.append(f"  Royalty incl VAT           £{p['royalty_incl_vat']:,.2f}")
        lines.append(f"  Ads incl VAT               £{p['ads_incl_vat']:,.2f}  ({p['ads_source']})")
        lines.append(f"  PAYOUT                      £{p['payout']:,.2f}  ({p['payout_pct_of_net']}% of net)")
        lines.append(f"  Food cost (est)            £{p['food_cost']:,.2f}")
        lines.append(f"  Contribution               £{p['contribution']:,.2f}")

    if comparison:
        lines.append("")
        lines.append("PROMOTION COMPARISON")
        lines.append("=" * 60)
        lines.append(f"  {comparison['baseline']}  ->  {comparison['test']}")
        lines.append(f"  Change in gross sales      £{comparison['delta_gross']:,.2f}")
        lines.append(f"  Change in net sales        £{comparison['delta_net']:,.2f}")
        lines.append(f"  Change in promo discount   £{comparison['delta_promo_discount']:,.2f}")
        lines.append(f"  Change in payout           £{comparison['delta_payout']:,.2f}")
        lines.append(f"  Change in contribution     £{comparison['delta_contribution']:,.2f}")
        lines.append(f"  Payout per extra £1 net    £{comparison['payout_per_extra_pound_of_net']:,.3f}")
        lines.append("")
        lines.append(f"  VERDICT: {comparison['verdict']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate delivery platform payout and test promotion profitability."
    )
    parser.add_argument("data", nargs="?", help="JSON file with one or two periods (see assets/example_input.json)")
    parser.add_argument("--royalty-rate", type=float, default=0.30, help="Platform royalty/commission rate on net sales (default 0.30)")
    parser.add_argument("--vat-rate", type=float, default=0.20, help="VAT rate (default 0.20)")
    parser.add_argument("--food-cost-rate", type=float, default=0.25, help="Food cost as a fraction of net sales (default 0.25)")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    if not args.data:
        parser.print_help()
        sys.exit(0)

    try:
        with open(args.data) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    raw_periods = data.get("periods", data if isinstance(data, list) else [data])
    if not raw_periods:
        print("Error: no periods found in input.", file=sys.stderr)
        sys.exit(1)

    royalty_rate = data.get("royalty_rate", args.royalty_rate)
    vat_rate = data.get("vat_rate", args.vat_rate)
    food_cost_rate = data.get("food_cost_rate", args.food_cost_rate)

    try:
        periods = [compute_period(p, royalty_rate, vat_rate, food_cost_rate) for p in raw_periods]
    except (KeyError, TypeError, ValueError) as e:
        print(f"Error: invalid period data ({e}).", file=sys.stderr)
        sys.exit(1)

    comparison = None
    if len(periods) >= 2:
        comparison = compare_periods(periods[0], periods[1], food_cost_rate)

    if args.format == "json":
        print(json.dumps({"periods": periods, "comparison": comparison}, indent=2))
    else:
        print(render_text(periods, comparison))


if __name__ == "__main__":
    main()
