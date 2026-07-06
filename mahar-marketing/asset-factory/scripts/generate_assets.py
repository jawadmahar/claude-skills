#!/usr/bin/env python3
"""Asset factory: batch-generate marketing images via Gemini (Nano Banana) or OpenAI.

Standard library only. Keys come from environment variables (GEMINI_API_KEY or
OPENAI_API_KEY) - never hardcode keys.

Usage:
  generate_assets.py batch.json --out ./assets-out
  generate_assets.py batch.json --provider openai
  generate_assets.py batch.json --dry-run          # print prompts, no API calls
  generate_assets.py batch.json --limit 10         # cap total images (test run)
  generate_assets.py batch.json --reference-dir ./raw-assets
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

GEMINI_MODEL = "gemini-2.5-flash-image"
GEMINI_URL = ("https://generativelanguage.googleapis.com/v1beta/models/"
              f"{GEMINI_MODEL}:generateContent")
OPENAI_URL = "https://api.openai.com/v1/images/generations"
MAX_RETRIES = 3


def load_brand_kit(brand):
    kits = json.loads(
        (Path(__file__).parent.parent / "assets" / "brand-kits.json").read_text(encoding="utf-8"))
    if brand not in kits:
        sys.exit(f"Unknown brand '{brand}'. Available: {', '.join(sorted(kits))}")
    return kits[brand]


def build_prompt(kit, concept, size, variant_idx):
    w, h = size.split("x")
    orientation = "square" if w == h else "vertical 9:16 story/reel"
    angles = kit.get("variant_angles", ["straight-on product shot"])
    angle = angles[variant_idx % len(angles)]
    return (
        f"Advertising image for {kit['display_name']}, {kit['descriptor']}. "
        f"Concept: {concept['visual']}. "
        f"Overlay headline text: \"{concept['hook']}\" in a bold, readable typeface. "
        f"Style: {kit['style']}. Colour palette: {', '.join(kit['palette'])}. "
        f"Composition variant: {angle}. "
        f"Format: {orientation}, {w}x{h} pixels, edge-to-edge, no borders or watermarks. "
        f"Constraints: {kit['constraints']} UK English spelling in any text."
    )


def _post_json(url, payload, headers):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def gen_gemini(prompt, size, api_key, reference_images):
    parts = [{"text": prompt}]
    for ref in reference_images[:3]:
        parts.append({"inline_data": {
            "mime_type": "image/png" if ref.suffix.lower() == ".png" else "image/jpeg",
            "data": base64.b64encode(ref.read_bytes()).decode("ascii")}})
    body = _post_json(GEMINI_URL, {"contents": [{"parts": parts}]},
                      {"x-goog-api-key": api_key})
    for cand in body.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            data = part.get("inlineData") or part.get("inline_data")
            if data and data.get("data"):
                return base64.b64decode(data["data"])
    raise RuntimeError("Gemini returned no image data (possibly safety-filtered)")


def gen_openai(prompt, size, api_key, _reference_images):
    # gpt-image-1 sizes: 1024x1024, 1024x1536, 1536x1024
    api_size = "1024x1536" if size == "1080x1920" else "1024x1024"
    body = _post_json(OPENAI_URL,
                      {"model": "gpt-image-1", "prompt": prompt, "size": api_size, "n": 1},
                      {"Authorization": f"Bearer {api_key}"})
    return base64.b64decode(body["data"][0]["b64_json"])


PROVIDERS = {
    "gemini": ("GEMINI_API_KEY", gen_gemini),
    "openai": ("OPENAI_API_KEY", gen_openai),
}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("spec", help="batch spec JSON (see SKILL.md)")
    p.add_argument("--provider", choices=PROVIDERS, default="gemini")
    p.add_argument("--out", default="./assets-out")
    p.add_argument("--limit", type=int, default=0, help="cap total images (0 = no cap)")
    p.add_argument("--dry-run", action="store_true", help="print prompts without calling the API")
    p.add_argument("--reference-dir", help="folder of raw reference photos (gemini only)")
    p.add_argument("--pace", type=float, default=2.0, help="seconds between requests (default 2)")
    args = p.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    kit = load_brand_kit(spec["brand"])
    env_var, generate = PROVIDERS[args.provider]
    api_key = os.environ.get(env_var, "")
    if not api_key and not args.dry_run:
        sys.exit(f"{env_var} is not set. Export it or use --dry-run.")

    refs = []
    if args.reference_dir:
        refs = sorted(q for q in Path(args.reference_dir).iterdir()
                      if q.suffix.lower() in (".png", ".jpg", ".jpeg"))

    out_dir = Path(args.out) / spec["campaign"]
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest, made, failed = [], 0, 0

    jobs = [(ci, c, v, s)
            for ci, c in enumerate(spec["concepts"])
            for v in range(int(spec.get("variants_per_concept", 3)))
            for s in spec.get("sizes", ["1080x1080"])]
    if args.limit:
        jobs = jobs[:args.limit]
    print(f"{len(jobs)} images queued ({args.provider}, brand={spec['brand']})", file=sys.stderr)

    for ci, concept, v, size in jobs:
        prompt = build_prompt(kit, concept, size, v)
        fname = f"c{ci + 1}_v{v + 1}_{size}.png"
        if args.dry_run:
            print(f"--- {fname}\n{prompt}\n")
            continue
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                png = generate(prompt, size, api_key, refs)
                (out_dir / fname).write_bytes(png)
                manifest.append({"file": fname, "prompt": prompt, "size": size,
                                 "provider": args.provider,
                                 "concept": concept["hook"],
                                 "generated_at": datetime.now(timezone.utc).isoformat()})
                made += 1
                print(f"[{made}/{len(jobs)}] {fname}", file=sys.stderr)
                break
            except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError, KeyError) as e:
                detail = getattr(e, "code", "") or str(e)
                if attempt == MAX_RETRIES:
                    failed += 1
                    print(f"FAILED {fname}: {detail}", file=sys.stderr)
                else:
                    time.sleep(args.pace * (2 ** attempt))
        time.sleep(args.pace)

    if not args.dry_run:
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"Done: {made} generated, {failed} failed -> {out_dir}", file=sys.stderr)
        if failed and not made:
            sys.exit(1)


if __name__ == "__main__":
    main()
