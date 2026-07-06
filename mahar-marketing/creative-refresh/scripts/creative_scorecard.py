#!/usr/bin/env python3
"""Creative scorecard: classify Meta ads as SCALE / KEEP / WATCH / KILL / REACTIVATE.

Input: JSON (list of ad objects, or {"ad_entities": "..."} as returned by the
Meta MCP) or CSV exported from Ads Manager. Recognised fields per ad:
name, spend/amount_spent, lead(s), ctr, cpm, frequency, effective_status.

Usage:
  creative_scorecard.py ads.json
  creative_scorecard.py ads.csv --min-spend 15 --json
  creative_scorecard.py ads.json --brief > refresh-brief.md
"""
import argparse
import csv
import json
import re
import statistics
import sys
from pathlib import Path


def _num(value):
    """Parse '£56.30 GBP', '3.31%', '54,257', 20 -> float. None if not parseable."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = re.sub(r"[^0-9.\-]", "", str(value))
    try:
        return float(cleaned)
    except ValueError:
        return None


def load_ads(path):
    text = Path(path).read_text(encoding="utf-8")
    if path.lower().endswith(".csv"):
        rows = list(csv.DictReader(text.splitlines()))
    else:
        data = json.loads(text)
        if isinstance(data, dict) and "ad_entities" in data:
            inner = data["ad_entities"]
            data = json.loads(inner) if isinstance(inner, str) else inner
        rows = data if isinstance(data, list) else [data]

    ads = []
    for row in rows:
        low = {k.lower().replace(" ", "_"): v for k, v in row.items()}
        spend = _num(low.get("spend") or low.get("amount_spent") or low.get("amount_spent_(gbp)"))
        leads = _num(low.get("lead") or low.get("leads") or low.get("results"))
        ads.append({
            "id": str(low.get("id", "")),
            "name": str(low.get("name") or low.get("ad_name") or "unnamed"),
            "status": str(low.get("effective_status") or low.get("status") or "UNKNOWN").upper(),
            "spend": spend or 0.0,
            "leads": int(leads) if leads else 0,
            "ctr": _num(low.get("ctr") or low.get("ctr_(all)")),
            "cpm": _num(low.get("cpm")),
            "frequency": _num(low.get("frequency")),
        })
    return [a for a in ads if a["spend"] > 0]


def classify(ads, min_spend, scale_ratio=0.75, kill_ratio=2.0,
             fatigue_freq=3.5, weak_ctr=1.5, weak_ctr_freq=2.5):
    scored = [a for a in ads if a["leads"] > 0]
    for a in ads:
        a["cpl"] = round(a["spend"] / a["leads"], 2) if a["leads"] else None

    cpls = [a["cpl"] for a in scored if a["spend"] >= min_spend]
    median_cpl = statistics.median(cpls) if cpls else None
    total_spend = sum(a["spend"] for a in ads) or 1.0

    for a in ads:
        a["spend_share"] = round(a["spend"] / total_spend * 100, 1)
        verdict, reasons = "KEEP", []
        if a["spend"] < min_spend:
            verdict = "WATCH"
            reasons.append(f"below min spend GBP {min_spend:.0f}, too early to judge")
        elif a["cpl"] is None:
            verdict = "KILL"
            reasons.append("spend with zero leads")
        elif median_cpl:
            ratio = a["cpl"] / median_cpl
            if ratio <= scale_ratio:
                verdict = "SCALE"
                reasons.append(f"CPL {ratio:.2f}x median")
            elif ratio > kill_ratio:
                verdict = "KILL"
                reasons.append(f"CPL {ratio:.2f}x median (kill threshold {kill_ratio}x)")
            elif ratio > 1.25:
                verdict = "WATCH"
                reasons.append(f"CPL {ratio:.2f}x median")
        if a["ctr"] is not None and a["frequency"] is not None:
            if a["ctr"] < weak_ctr and a["frequency"] > weak_ctr_freq and verdict != "SCALE":
                verdict = "KILL"
                reasons.append(f"CTR {a['ctr']}% with frequency {a['frequency']} - creative not landing")
        if a["frequency"] is not None and a["frequency"] > fatigue_freq and verdict in ("KEEP", "SCALE"):
            verdict = "WATCH"
            reasons.append(f"frequency {a['frequency']} > {fatigue_freq} - fatigue risk")
        if "PAUSED" in a["status"] and a["cpl"] and median_cpl and a["cpl"] / median_cpl <= scale_ratio:
            verdict = "REACTIVATE"
            reasons.append("paused ad with winner-level CPL - review why it was paused")
        a["verdict"], a["reasons"] = verdict, reasons

    return median_cpl


def render_text(ads, median_cpl):
    order = {"REACTIVATE": 0, "KILL": 1, "SCALE": 2, "WATCH": 3, "KEEP": 4}
    lines = [f"Median CPL (qualifying ads): GBP {median_cpl:.2f}" if median_cpl
             else "Median CPL: not computable (no ads with leads)"]
    lines.append("")
    for a in sorted(ads, key=lambda x: (order[x["verdict"]], -(x["spend"]))):
        cpl = f"GBP {a['cpl']:.2f}" if a["cpl"] else "n/a"
        lines.append(f"[{a['verdict']:<10}] {a['name'][:52]:<52} "
                     f"spend GBP {a['spend']:>8.2f}  leads {a['leads']:>4}  CPL {cpl}")
        for r in a["reasons"]:
            lines.append(f"             - {r}")
    return "\n".join(lines)


def render_brief(ads, median_cpl):
    template_path = Path(__file__).parent.parent / "assets" / "refresh-brief-template.md"
    winners = [a for a in ads if a["verdict"] in ("SCALE", "REACTIVATE")]
    kills = [a for a in ads if a["verdict"] == "KILL"]

    def bullet(items, extra=""):
        return "\n".join(
            f"- **{a['name']}** - CPL GBP {a['cpl'] or 0:.2f}, CTR {a['ctr'] or 0}%, "
            f"{a['spend_share']}% of spend{extra}" for a in items) or "- none identified"

    body = template_path.read_text(encoding="utf-8")
    return (body
            .replace("{{MEDIAN_CPL}}", f"{median_cpl:.2f}" if median_cpl else "n/a")
            .replace("{{WINNERS}}", bullet(winners))
            .replace("{{KILL_LIST}}", bullet(kills))
            .replace("{{N_ADS}}", str(len(ads))))


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("input", help="ads.json or ads.csv")
    p.add_argument("--min-spend", type=float, default=10.0,
                   help="ignore ads below this spend for median/kill decisions (default 10)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--brief", action="store_true", help="emit a refresh brief in Markdown")
    args = p.parse_args()

    ads = load_ads(args.input)
    if not ads:
        sys.exit("No ads with spend found in input.")
    median_cpl = classify(ads, args.min_spend)

    if args.brief:
        print(render_brief(ads, median_cpl))
    elif args.json:
        print(json.dumps({"median_cpl": median_cpl, "ads": ads}, indent=2))
    else:
        print(render_text(ads, median_cpl))


if __name__ == "__main__":
    main()
