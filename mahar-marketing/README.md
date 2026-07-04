# Mahar Marketing Skills

Internal skill suite for Mahar Group Operations (STEMEX, Muffin Break Norwich, Cafe UFO / Wraps and Wings, Explorazone). Built so anyone on the team (Musa, Eman, or Claude itself) can run the marketing engine without starting from scratch.

## Skills

| Skill | Purpose | Trigger from Claude |
|---|---|---|
| [creative-refresh](creative-refresh/) | Score every ad against CPL/CTR/frequency thresholds, find winners and fatigued ads, and generate a refresh brief for the next campaign | "refresh creatives for [entity]" or run on a `/loop` |
| [asset-factory](asset-factory/) | Batch-generate hundreds of on-brand image assets from raw asset descriptions using Gemini (Nano Banana) or OpenAI image APIs (BYOK) | "generate assets for [campaign]" |
| [ghl-email-engine](ghl-email-engine/) | Evergreen and retargeting email campaigns sent directly through GoHighLevel (own IP, no Mailchimp) against pipeline-segmented contacts | "send [sequence] to [segment]" |

## How the loop works

```
Meta MCP (ad performance)          GHL (leads -> pipeline stages)
        |                                   |
        v                                   v
creative-refresh scorecard  ->  refresh brief (winning hooks, kill list)
        |
        v
asset-factory  ->  100s of on-brand variants from raw assets
        |
        v
new Meta campaign (via Meta MCP)    ghl-email-engine (nurture the leads)
        |                                   |
        +--------- repeat monthly ----------+
```

## House rules

- All entities are UK businesses. GBP, UK spelling, VAT at 20% where money is user-facing.
- The Bowthorpe science centre is **Explorazone** (capital E, single word) after the 2026 rebrand.
- Known baseline (30d to 1 Jul 2026): blended CPL ~GBP 1.44; Muffin Break ~GBP 0.51; kill threshold CPL > 2x account median for 7+ days.
- Scripts use Python standard library only, except where an external image/email API is the whole point (BYOK via environment variables, never hardcoded keys).

## Environment variables

| Variable | Used by | Where to get it |
|---|---|---|
| `GEMINI_API_KEY` | asset-factory | Google AI Studio (Nano Banana image model) |
| `OPENAI_API_KEY` | asset-factory (fallback) | OpenAI / ChatGPT Team account |
| `GHL_API_KEY` | ghl-email-engine | GHL > Settings > Private Integrations |
| `GHL_LOCATION_ID` | ghl-email-engine | GHL sub-account (one per entity) |
