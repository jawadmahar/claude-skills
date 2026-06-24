#!/usr/bin/env python3
"""Estimate food cost % from a bank statement export.

Reads a CSV/TSV bank statement, classifies each transaction by counterparty,
sums food and packaging spend, reconstructs net sales from delivery payouts
(plus optional in-store/own-app credits), and reports food cost as a % of sales.

Numerator  = food/ingredient suppliers + packaging/consumables.
Denominator= delivery payouts grossed up to net sales (default /0.49) + in-store
             sweeps + own-app credits.

Caveats the output repeats: a statement shows PURCHASES not consumption (stock
timing), supplier deliveries are lumpy, and the gross-up ratio is approximate.
For an exact %, pass the real net sales with --sales.

The KEYWORD lists below are sensible defaults for UFO Food Ltd; edit them for
other businesses. Standard library only.
"""

import argparse
import csv
import json
import sys
from collections import defaultdict

# --- Classification keyword groups (counterparty / reference, case-insensitive) ---
FOOD = ["BRAKE BROS", "3663", "DANBURY OILS", "KOREAFOODS", "ITAEWON",
        "TUK TUK MART", "EOE COOP FOOD", "TESCO STORES", "ICELAND", "BIDFOOD", "BOOKER"]
# WRAPSWINGS.STORE = nominated-supplier portal: branded packaging + nominated
# food lines, so it is cost of goods (food + packaging mix).
PACKAGING = ["AMAZON", "AMZN", "POUNDLAND", "WRAPSWINGS.STORE"]   # consumables / COGS
UNCERTAIN = []                                         # none currently
DELIVERY_SALES = ["UBER", "DELIVEROO", "JET "]         # platform payouts (credits)
OWNAPP_SALES = ["APP4"]                                # own-app order payouts
INSTORE_IN = ["UFO FOOD LTD"]                          # internal sweep of in-store/kiosk takings
EXCLUDE = ["WAGE", "B PAYMENT", "STEM CENTRE", "MAHAR COFFEE", "GOCARDLESS",
           "ANNA SUBSCRIPTION", "HISCOX", "COMPANIESHOUSE", "OTTER UK",
           "SYNE GRAPHICS", "PARKING", "NOTEMACHINE", "NORFOLK AND NORWIC",
           "KONOBA", "CAFE NEGRO", "THE FEED", "ARGOS", "HMT",
           "ROOP ZAHRA & MUHAMMAD"]


def classify(text):
    t = text.upper()
    # Order matters: sales and exclusions take precedence over cost keywords.
    for grp, name in [(DELIVERY_SALES, "delivery_sales"), (OWNAPP_SALES, "ownapp_sales"),
                      (EXCLUDE, "excluded"), (UNCERTAIN, "uncertain"),
                      (FOOD, "food"), (PACKAGING, "packaging"), (INSTORE_IN, "instore_in")]:
        if any(k in t for k in grp):
            return name
    return "unclassified"


def load(path):
    # Sniff delimiter (tab or comma).
    with open(path, newline="") as f:
        sample = f.read(2048)
        f.seek(0)
        delim = "\t" if sample.count("\t") >= sample.count(",") else ","
        rows = list(csv.DictReader(f, delimiter=delim))
    out = []
    for r in rows:
        keys = {k.lower(): v for k, v in r.items()}
        try:
            amt = float(str(keys.get("amount", "0")).replace(",", "").replace("£", "") or 0)
        except ValueError:
            amt = 0.0
        text = " ".join(str(keys.get(k, "")) for k in ("description", "reference", "name"))
        out.append({"date": keys.get("date", ""), "amount": amt,
                    "description": keys.get("description", "").strip(), "text": text})
    return out


def main():
    p = argparse.ArgumentParser(description="Estimate food cost % from a bank statement CSV/TSV.")
    p.add_argument("statement", nargs="?", help="CSV/TSV with date, description, reference, amount columns")
    p.add_argument("--grossup", type=float, default=0.49, help="Payout as fraction of net sales (default 0.49)")
    p.add_argument("--sales", type=float, default=None, help="Known net sales for the period (overrides derivation)")
    p.add_argument("--include-uncertain", action="store_true", help="Count UNCERTAIN spend (e.g. WrapsWings) as packaging")
    p.add_argument("--format", choices=["text", "json"], default="text")
    args = p.parse_args()
    if not args.statement:
        p.print_help()
        return

    rows = load(args.statement)
    cats = defaultdict(list)
    for r in rows:
        cats[classify(r["text"])].append(r)

    out_spend = lambda items: -sum(x["amount"] for x in items if x["amount"] < 0)
    in_credit = lambda items: sum(x["amount"] for x in items if x["amount"] > 0)

    food = out_spend(cats["food"])
    packaging = out_spend(cats["packaging"])
    uncertain = out_spend(cats["uncertain"])
    numerator = food + packaging + (uncertain if args.include_uncertain else 0)

    delivery_payout = in_credit(cats["delivery_sales"])
    instore = in_credit(cats["instore_in"])
    ownapp = in_credit(cats["ownapp_sales"])
    if args.sales is not None:
        net_sales = args.sales
        sales_basis = "supplied via --sales"
    else:
        net_sales = delivery_payout / args.grossup + instore + ownapp
        sales_basis = f"delivery payout /{args.grossup} + in-store sweeps + own-app"

    food_cost_pct = (numerator / net_sales * 100) if net_sales else 0.0

    # Per-supplier rollup for the cost categories.
    suppliers = {}
    for cat in ("food", "packaging", "uncertain"):
        agg = defaultdict(float)
        for x in cats[cat]:
            if x["amount"] < 0:
                agg[x["description"]] += -x["amount"]
        suppliers[cat] = dict(sorted(agg.items(), key=lambda kv: -kv[1]))

    result = {
        "transactions": len(rows),
        "food_spend": round(food, 2),
        "packaging_spend": round(packaging, 2),
        "uncertain_spend": round(uncertain, 2),
        "numerator": round(numerator, 2),
        "delivery_payout": round(delivery_payout, 2),
        "instore_sweeps": round(instore, 2),
        "ownapp_credits": round(ownapp, 2),
        "net_sales": round(net_sales, 2),
        "sales_basis": sales_basis,
        "food_cost_pct": round(food_cost_pct, 1),
        "unclassified": [f"{x['date']} {x['amount']} {x['description']}" for x in cats["unclassified"]],
        "suppliers": suppliers,
    }

    if args.format == "json":
        print(json.dumps(result, indent=2))
        return

    print(f"Transactions: {result['transactions']}")
    print(f"Food/ingredient spend:   £{food:,.2f}")
    print(f"Packaging/consumables:   £{packaging:,.2f}")
    print(f"Uncertain spend:         £{uncertain:,.2f}  ({'included' if args.include_uncertain else 'excluded'})")
    print(f"Numerator (cost):        £{numerator:,.2f}")
    print(f"Net sales ({sales_basis}): £{net_sales:,.2f}")
    print(f"=> FOOD COST: {food_cost_pct:.1f}% of net sales")
    if result["unclassified"]:
        print("\nUnclassified (review):")
        for u in result["unclassified"]:
            print(f"  {u}")


if __name__ == "__main__":
    main()
