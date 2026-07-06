---
name: asset-factory
description: Batch-generate hundreds of on-brand marketing image assets from prompt templates and raw asset descriptions, using Google Gemini image generation (Nano Banana) or OpenAI images as the backend (BYOK). Use when a campaign needs new creative variants, when refreshing ad creatives at scale, or when building an asset library for STEMEX, Muffin Break, Cafe UFO, or Explorazone.
---

# Asset Factory

Turns one brief into hundreds of ready-to-use ad images. Prompts are assembled from a brand kit (colours, tone, subjects) plus a campaign brief, then sent in batches to an image API. Output is a folder of PNGs with a manifest so every asset is traceable back to its prompt.

**Providers (bring your own key, set one):**

| Provider | Env var | Model | Notes |
|---|---|---|---|
| Google Gemini | `GEMINI_API_KEY` | `gemini-2.5-flash-image` (Nano Banana) | Preferred - fast, cheap, strong text rendering. Key from Google AI Studio. |
| OpenAI | `OPENAI_API_KEY` | `gpt-image-1` | Fallback - available through the ChatGPT Team account. |

No key is ever stored in this repo. The script reads environment variables only.

## Workflow

### 1. Pick the brand kit and write the batch spec

Brand kits for all four entities live in `assets/brand-kits.json`. A batch spec is a small JSON file:

```json
{
  "brand": "explorazone",
  "campaign": "summer-holidays-b2g3",
  "sizes": ["1080x1080", "1080x1920"],
  "concepts": [
    {"hook": "Two tickets, one price", "visual": "family exploring a giant bubble exhibit"},
    {"hook": "Beat the heat, feed their brains", "visual": "kids doing experiments in a cool lab"}
  ],
  "variants_per_concept": 5
}
```

### 2. Generate

```bash
python3 scripts/generate_assets.py batch.json --out ./assets-out
python3 scripts/generate_assets.py batch.json --provider openai --dry-run   # print prompts only
python3 scripts/generate_assets.py batch.json --limit 10                    # test run
```

`concepts x variants x sizes` = total images (2 concepts x 5 variants x 2 sizes = 20). For "hundreds", raise `variants_per_concept` or add concepts - the script paces requests and retries transient failures, so large batches can run unattended.

### 3. Review and file

Every run writes `manifest.json` (file, prompt, provider, brand, campaign, timestamp). Cull the misses, keep the rest in your asset library. Feed winners' prompt patterns back into the next batch spec.

### Using raw assets as references

Gemini supports image+text prompts. Put reference photos (your real shopfront, real products, real exhibits) in a folder and pass `--reference-dir ./raw-assets`: the script attaches up to 3 references per request so generated images stay anchored to reality. Recommended for food photography (Muffin Break, Cafe UFO) where invented food looks fake.

## Guardrails

- Never generate images of identifiable real children; brand kits for STEMEX and Explorazone specify illustrated or back-view children only.
- All prices/offers in generated text must be checked by a human before publishing (models mangle small print).
- UK spelling in all overlay text; Explorazone is one word, capital E.

## Files

- `scripts/generate_assets.py` - batch generator (stdlib only; BYOK)
- `assets/brand-kits.json` - palette, tone, subjects per entity
- `assets/prompt-templates.md` - proven prompt patterns per format
- `assets/example-batch.json` - working example spec
