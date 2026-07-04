---
name: creative-refresh
description: Score Meta ad creatives against CPL/CTR/frequency thresholds, identify winners and fatigued ads, and generate a data-backed refresh brief for the next campaign. Use when refreshing creatives for a new campaign, reviewing ad performance, or running a recurring creative health check for STEMEX, Muffin Break, Cafe UFO, or Explorazone.
---

# Creative Refresh

Turns raw Meta ad-level performance data into a decision sheet: which creatives to scale, which to kill, and a ready-to-use brief for the replacements. Designed to be run monthly per entity, or on demand before any new campaign.

## Workflow

### 1. Export ad-level data

From a Claude session with the Meta MCP connected, pull ad-level data (last 30 days) for the target account and save it as JSON:

```
Pull ad-level data for [account] last 30 days: id, name, spend, lead, ctr, cpm,
frequency, effective_status. Save the raw JSON to ads.json.
```

Account IDs: STEMEX `889449515877118`, Explorazone `1929079174665224`, Muffin Break `3083829301898602`.

Without MCP access, export the same columns from Ads Manager as CSV (the script accepts both).

### 2. Run the scorecard

```bash
python3 scripts/creative_scorecard.py ads.json                # human-readable
python3 scripts/creative_scorecard.py ads.json --json         # machine-readable
python3 scripts/creative_scorecard.py ads.csv --min-spend 15  # ignore low-spend tests
```

The script classifies every ad:

| Verdict | Rule (defaults, override with flags) |
|---|---|
| SCALE | CPL <= 0.75x account median AND spend share < 40% |
| KEEP | CPL within 0.75-1.25x median |
| WATCH | CPL 1.25-2x median, or frequency > 3.5 |
| KILL | CPL > 2x median with spend >= min-spend, or CTR < 1.5% with frequency > 2.5 |
| REACTIVATE | paused ad whose CPL was <= 0.75x median (the "paused star" trap) |

### 3. Generate the refresh brief

```bash
python3 scripts/creative_scorecard.py ads.json --brief > refresh-brief.md
```

This fills `assets/refresh-brief-template.md` with the winning hooks, kill list, and format gaps (e.g. no 9:16 video among winners). Hand the brief to asset-factory to produce the new variants.

### 4. Run it as a loop (optional)

From Claude: `/loop 7d refresh creatives check for <entity>` - Claude re-pulls the data weekly, re-runs the scorecard, and reports only when a verdict changes (new KILL or new SCALE candidate).

## Known lessons baked into the thresholds

- Muffin Break's "skip the rush" convenience hook (6.3% CTR) beat every discount hook. Test convenience angles first for food entities.
- Explorazone's "two tickets one price" was the account's best ad while sitting paused. The REACTIVATE check exists because of this.
- Teachers Go Free ran to GBP 13+ CPL before anyone noticed. The KILL rule (2x median) would have caught it three weeks earlier.

## Files

- `scripts/creative_scorecard.py` - scorer and brief generator (stdlib only)
- `assets/refresh-brief-template.md` - brief skeleton
- `references/refresh-playbook.md` - thresholds rationale, cadence, escalation
