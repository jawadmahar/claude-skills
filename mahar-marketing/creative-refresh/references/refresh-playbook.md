# Refresh Playbook - thresholds, cadence, escalation

## Why these thresholds

| Rule | Value | Rationale (from Mahar account history) |
|---|---|---|
| KILL at CPL > 2x median | 2.0x | Teachers Go Free v2 (Explorazone) ran at 4-6x sibling CPL for weeks (GBP 10.93-13.80 vs ~GBP 2 account norm) before being paused manually in June 2026. A 2x tripwire catches this in days. |
| SCALE at CPL <= 0.75x median | 0.75x | Muffin Break "skip the rush" sat at ~GBP 0.40 CPL (best in group) with under 10% of spend. Winners tend to be starved because budgets follow habit, not data. |
| REACTIVATE check on paused ads | always | Explorazone "two tickets one price": 280 leads at GBP 0.65 CPL, 4.11% CTR - the account's best ad - found PAUSED while weaker ads spent. Always ask why a winner was paused. |
| Fatigue watch at frequency > 3.5 | 3.5 | Explorazone Birthday campaign hit frequency 4.19 in May 2026; its CPL then rose 34% the following month (GBP 2.02 -> 2.71). |
| Weak-creative kill: CTR < 1.5% and frequency > 2.5 | - | If people have seen it twice and still do not click, more budget will not fix the creative. |
| Min spend to judge: GBP 10 | 10 | Below this, lead counts are noise. |

## Cadence

- **Weekly** (loop): scorecard per entity; act only on new KILL / REACTIVATE verdicts.
- **Monthly**: full refresh - scorecard, brief, new asset batch, launch, pause the kill list.
- **Quarterly**: re-derive thresholds from the trailing 90 days per account (medians drift seasonally - school holidays move STEMEX and Explorazone hard).

## Escalation

- Any account whose blended CPL rises >25% month-on-month: flag to the director before adding budget.
- Any single ad passing GBP 150 spend without at least (spend / median CPL / 2) leads: pause first, discuss after.
- New campaigns get a 7-day grace period before verdicts apply (learning phase).

## Seasonal notes

- STEMEX and Explorazone: demand spikes in school holidays (half terms, Easter, summer). Never judge a term-time month against a holiday month.
- Muffin Break and Cafe UFO: weather-sensitive; hot spells favour iced-drink creatives (Cold Iced Matcha launched 30 Jun 2026 - judge after its first full fortnight).
- Explorazone rebrand (Apr-Jun 2026): creatives referencing "Exploring Sciences" or "Science Museum" must be retired; everything new says Explorazone.
