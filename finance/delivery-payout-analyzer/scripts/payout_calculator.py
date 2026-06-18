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
  - Contribution     : payout - food cost (food cost defaults to 33% of net).
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

    # ----- In-store (EPOS) + kiosk sales: no platform commission or ads -----
    in_store = float(period.get("in_store_inc_vat", 0) or 0)
    in_store_food = in_store * food_cost_rate
    in_store_contribution = in_store - in_store_food

    kiosk = float(period.get("kiosk_inc_vat", 0) or 0)
    kiosk_contribution = kiosk * (1 - food_cost_rate)

    total_sales = net + in_store + kiosk

    # ----- Labour: cost serves both delivery and in-store -----
    if period.get("labour_cost") is not None:
        labour_cost = float(period["labour_cost"])
        labour_hours = period.get("labour_hours")
    elif period.get("labour_hours") is not None and period.get("labour_rate") is not None:
        labour_hours = float(period["labour_hours"])
        labour_cost = labour_hours * float(period["labour_rate"])
    else:
        labour_hours = None
        labour_cost = 0.0

    labour_pct_of_sales = (labour_cost / total_sales) if total_sales else 0.0

    contribution_before_labour = contribution + in_store_contribution + kiosk_contribution
    contribution_after_labour = contribution_before_labour - labour_cost

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
        "in_store_sales": _money(in_store),
        "in_store_contribution": _money(in_store_contribution),
        "kiosk_sales": _money(kiosk),
        "kiosk_contribution": _money(kiosk_contribution),
        "total_sales": _money(total_sales),
        "labour_hours": labour_hours,
        "labour_cost": _money(labour_cost),
        "labour_pct_of_sales": round(labour_pct_of_sales * 100, 1),
        "contribution_before_labour": _money(contribution_before_labour),
        "contribution_after_labour": _money(contribution_after_labour),
    }


def compare_periods(base, test, food_cost_rate):
    """Compare a baseline (lighter promo) period against a test (heavier promo) period."""
    d_gross = test["gross_sales"] - base["gross_sales"]
    d_net = test["net_sales"] - base["net_sales"]
    d_promo = test["promo_discount"] - base["promo_discount"]
    d_payout = test["payout"] - base["payout"]
    d_contribution = test["contribution"] - base["contribution"]
    d_total_sales = test["total_sales"] - base["total_sales"]
    d_labour = test["labour_cost"] - base["labour_cost"]
    d_contribution_after_labour = test["contribution_after_labour"] - base["contribution_after_labour"]

    # Payout generated per extra £1 of net sales the promotion brought in.
    payout_per_extra_net = (d_payout / d_net) if d_net else 0.0

    # When labour is supplied, judge on the bottom line after labour.
    has_labour = base["labour_cost"] or test["labour_cost"]
    decisive = d_contribution_after_labour if has_labour else d_contribution
    basis = "contribution after labour" if has_labour else "contribution"

    if decisive > 0:
        verdict = f"BETTER OFF with the heavier promotion (on {basis})"
    elif decisive < 0:
        verdict = f"WORSE OFF with the heavier promotion (on {basis})"
    else:
        verdict = "NEUTRAL"

    return {
        "baseline": base["name"],
        "test": test["name"],
        "delta_gross": _money(d_gross),
        "delta_net": _money(d_net),
        "delta_total_sales": _money(d_total_sales),
        "delta_promo_discount": _money(d_promo),
        "delta_payout": _money(d_payout),
        "delta_contribution": _money(d_contribution),
        "delta_labour_cost": _money(d_labour),
        "delta_contribution_after_labour": _money(d_contribution_after_labour),
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
        lines.append(f"  PAYOUT (delivery)           £{p['payout']:,.2f}  ({p['payout_pct_of_net']}% of net)")
        lines.append(f"  Food cost on delivery      £{p['food_cost']:,.2f}")
        lines.append(f"  Delivery contribution      £{p['contribution']:,.2f}")
        if p["in_store_sales"]:
            lines.append(f"  In-store sales (inc VAT)   £{p['in_store_sales']:,.2f}")
            lines.append(f"  In-store contribution      £{p['in_store_contribution']:,.2f}")
        if p["kiosk_sales"]:
            lines.append(f"  Kiosk sales (inc VAT)      £{p['kiosk_sales']:,.2f}")
            lines.append(f"  Kiosk contribution         £{p['kiosk_contribution']:,.2f}")
        if p["in_store_sales"] or p["kiosk_sales"]:
            lines.append(f"  Total sales (inc VAT)      £{p['total_sales']:,.2f}")
        if p["labour_cost"]:
            hrs = f"{p['labour_hours']:g} hrs" if p["labour_hours"] is not None else "n/a"
            lines.append(f"  Contribution pre-labour    £{p['contribution_before_labour']:,.2f}")
            lines.append(f"  Labour ({hrs})         £{p['labour_cost']:,.2f}  ({p['labour_pct_of_sales']}% of total sales)")
            lines.append(f"  CONTRIBUTION after labour  £{p['contribution_after_labour']:,.2f}")

    if comparison:
        lines.append("")
        lines.append("PROMOTION COMPARISON")
        lines.append("=" * 60)
        lines.append(f"  {comparison['baseline']}  ->  {comparison['test']}")
        lines.append(f"  Change in gross sales      £{comparison['delta_gross']:,.2f}")
        lines.append(f"  Change in net sales        £{comparison['delta_net']:,.2f}")
        lines.append(f"  Change in total sales      £{comparison['delta_total_sales']:,.2f}")
        lines.append(f"  Change in promo discount   £{comparison['delta_promo_discount']:,.2f}")
        lines.append(f"  Change in payout           £{comparison['delta_payout']:,.2f}")
        lines.append(f"  Change in delivery contrib £{comparison['delta_contribution']:,.2f}")
        lines.append(f"  Change in labour cost      £{comparison['delta_labour_cost']:,.2f}")
        lines.append(f"  Change in contrib aft lab  £{comparison['delta_contribution_after_labour']:,.2f}")
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
    parser.add_argument("--food-cost-rate", type=float, default=0.33, help="Food cost as a fraction of net sales (default 0.33)")
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
