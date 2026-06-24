#!/usr/bin/env python3
"""Per-channel contribution and a keep/drop test for delivery.

For each sales channel computes contribution before labour, then allocates
labour by sales share to show contribution after fully-allocated labour. For a
keep/drop decision it reports the avoidable-labour breakeven: the fraction of a
channel's allocated labour that must disappear on closure for dropping it to
improve profit.

  contribution_before_labour = net x (payout_rate - food_cost_rate)
    payout_rate = share of net sales kept after platform commission + ads
                  (delivery ~0.49; in-store/kiosk 1.0; own-app ~0.90)
  labour allocated by share of total net sales
  drop improves profit only if avoidable labour > contribution_before_labour

Figures are BEFORE rent, utilities, VAT remittance and card fees. Standard library only.
"""

import argparse
import json
import sys


def analyse(data):
    labour = float(data["labour_per_week"])
    channels = data["channels"]
    total_net = sum(float(c["net_per_week"]) for c in channels) or 1.0

    rows = []
    for c in channels:
        net = float(c["net_per_week"])
        payout_rate = float(c.get("payout_rate", 1.0))
        fc = float(c.get("food_cost_rate", 0.33))
        cbl = net * (payout_rate - fc)
        share = net / total_net
        alloc_labour = labour * share
        caf = cbl - alloc_labour
        # Breakeven: drop helps only if avoidable labour exceeds cbl.
        breakeven_frac = (cbl / alloc_labour) if alloc_labour else 0.0
        rows.append({
            "name": c["name"],
            "net_per_week": round(net, 2),
            "sales_share_pct": round(share * 100, 1),
            "contribution_before_labour": round(cbl, 2),
            "allocated_labour": round(alloc_labour, 2),
            "contribution_after_labour": round(caf, 2),
            "drop_breakeven_avoidable_labour_pct": round(breakeven_frac * 100, 1),
        })

    totals = {
        "total_net_per_week": round(total_net, 2),
        "labour_per_week": round(labour, 2),
        "contribution_before_labour": round(sum(r["contribution_before_labour"] for r in rows), 2),
        "contribution_after_labour": round(sum(r["contribution_before_labour"] for r in rows) - labour, 2),
    }
    return {"channels": rows, "totals": totals}


def render(res):
    out = ["CHANNEL ECONOMICS (per week, before rent/utilities/VAT)", "=" * 64]
    for r in res["channels"]:
        out.append("")
        out.append(f"{r['name']}  (net £{r['net_per_week']:,.0f}/wk, {r['sales_share_pct']}% of sales)")
        out.append(f"  Contribution before labour   £{r['contribution_before_labour']:,.2f}")
        out.append(f"  Allocated labour (by sales)   £{r['allocated_labour']:,.2f}")
        out.append(f"  Contribution AFTER labour     £{r['contribution_after_labour']:,.2f}")
        out.append(f"  Drop helps only if >{r['drop_breakeven_avoidable_labour_pct']:.0f}% of its labour is avoidable")
    t = res["totals"]
    out.append("")
    out.append("-" * 64)
    out.append(f"  TOTAL net sales/wk            £{t['total_net_per_week']:,.2f}")
    out.append(f"  Labour/wk                     £{t['labour_per_week']:,.2f}")
    out.append(f"  Total contribution pre-labour £{t['contribution_before_labour']:,.2f}")
    out.append(f"  TOTAL after labour            £{t['contribution_after_labour']:,.2f}")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Per-channel contribution and delivery keep/drop test.")
    p.add_argument("data", nargs="?", help="JSON with labour_per_week and channels[]")
    p.add_argument("--format", choices=["text", "json"], default="text")
    args = p.parse_args()
    if not args.data:
        p.print_help()
        return
    try:
        with open(args.data) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)
    res = analyse(data)
    print(json.dumps(res, indent=2) if args.format == "json" else render(res))


if __name__ == "__main__":
    main()
