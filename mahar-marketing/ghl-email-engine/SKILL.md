---
name: ghl-email-engine
description: Build and send evergreen and retargeting email campaigns directly through GoHighLevel (LeadConnector API v2) to pipeline-segmented contacts. Use when sending email campaigns, nurture sequences, win-back or retargeting emails for STEMEX, Muffin Break, Cafe UFO, or Explorazone. Sends through GHL's own sending domain (dedicated IP) - no Mailchimp or third-party ESP.
---

# GHL Email Engine

Prompt-driven email campaigns that go out through your own GoHighLevel sub-accounts. Deliverability rides on your dedicated GHL sending IP and authenticated domains, which beats routing through a shared third-party ESP.

**Setup required once per entity:** a Private Integration Token and Location ID. See `references/ghl-setup.md`. Nothing here stores credentials; the scripts read `GHL_API_KEY` and `GHL_LOCATION_ID` from the environment.

## What you can say to Claude once this skill is installed

- "Send the evergreen welcome sequence to new Explorazone leads"
- "Build a win-back email for Muffin Break customers inactive 60+ days and show me the draft first"
- "How many contacts are in the STEMEX 'Short Breaks enquiry' stage?"

Claude uses the scripts below; every send happens inside your GHL account, so replies, unsubscribes and history stay in GHL where the team already works.

## Workflow

### 1. Segment - who gets it

```bash
python3 scripts/ghl_client.py contacts --tag "meta-lead" --pipeline-stage "New Enquiry"
python3 scripts/ghl_client.py contacts --inactive-days 60          # lapsed customers
python3 scripts/ghl_client.py contacts --tag "short-breaks" --count-only
```

### 2. Draft - what they get

Sequences are JSON files in `assets/sequences/`. Two production-ready starters ship with the skill:

- `evergreen-welcome.json` - 4-email nurture for brand-new leads (day 0, 2, 5, 10)
- `retargeting-lapsed.json` - 3-email win-back for contacts inactive 45+ days

Each email supports GHL merge fields (`{{contact.first_name}}` etc.) and per-entity token blocks so one sequence serves all four brands. Claude can draft new sequences from these templates on request - always review copy before the first live send.

### 3. Send

```bash
# One-off campaign email to a segment (dry run first - prints recipients and rendered email)
python3 scripts/send_campaign.py assets/sequences/retargeting-lapsed.json \
    --email 1 --tag "lapsed-60d" --entity muffin_break --dry-run

# Live send (asks for confirmation unless --yes)
python3 scripts/send_campaign.py assets/sequences/retargeting-lapsed.json \
    --email 1 --tag "lapsed-60d" --entity muffin_break --yes
```

For **evergreen automation** (every new lead gets the sequence forever), do not cron this script - instead install the sequence as a GHL Workflow once and let GHL handle timing natively (steps in `references/ghl-setup.md`). The script can enrol contacts into an existing workflow:

```bash
python3 scripts/ghl_client.py enroll --workflow-id <id> --tag "meta-lead"
```

### 4. Measure

GHL tracks opens/clicks/replies natively (Marketing > Emails > Statistics). Pair with the Meta CAPI connection so email-driven conversions feed back into ad optimisation - that closes the loop this whole suite is built around.

## Safety rails (enforced by the scripts)

- `--dry-run` renders everything and sends nothing; live sends require `--yes` or an interactive confirm.
- Hard cap of 500 recipients per invocation (`--max-recipients` to lower it); larger sends should be GHL Workflows.
- Contacts with `dnd` (do not disturb) or missing email are always skipped and reported.
- Every send is logged to `send-log.jsonl` next to the sequence file (who, what, when).

## Files

- `scripts/ghl_client.py` - GHL/LeadConnector API v2 client and CLI (stdlib only)
- `scripts/send_campaign.py` - segment + render + send with safety rails
- `assets/sequences/evergreen-welcome.json` - 4-email nurture sequence
- `assets/sequences/retargeting-lapsed.json` - 3-email win-back sequence
- `references/ghl-setup.md` - PIT token creation, scopes, deliverability checklist, workflow install
