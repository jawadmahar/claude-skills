# Prompt patterns that work

Assembled from Mahar campaign history. The generator builds prompts automatically from the brand kit; use these patterns when writing new `concepts` in a batch spec.

## The formula

```
[format] advertising image for [brand descriptor].
Concept: [one concrete visual scene - not a list].
Overlay headline: "[hook - 6 words or fewer]".
Style: [brand kit style]. Palette: [brand kit palette].
Constraints: [brand kit constraints].
```

## Hooks: what the data says

- **Convenience beats discounts for food.** "Skip the rush" (6.33% CTR) outperformed every buy-one-get-one ad on the Muffin Break account. Lead with time saved, queue skipped, sorted-for-you.
- **Value bundles beat percentages for attractions.** "Two tickets one price" (4.11% CTR, GBP 0.65 CPL) beat percentage-off framing on Explorazone. Concrete beats abstract.
- **Audience-named offers work but need volume.** "Grandparents 65+" pulled 3.41% CTR on a small budget; "Teachers Go Free" failed (GBP 13+ CPL). Test audience-specific hooks small before scaling.
- **First three words carry the hook.** Meta truncates aggressively on some placements.

## Visual scene tips per format

- **1080x1080 (feed):** one hero subject, headline in top third, no fine print.
- **1080x1920 (stories/reels):** vertical energy - full-height subjects, headline centre-top, CTA space bottom (platform UI covers the very bottom 250px).
- Ask for "edge-to-edge, no borders, no watermark" every time - models love adding frames.
- For text-heavy offers, generate the background image only and add text in Canva; model-rendered small print is unreliable.

## Reference images

For food (Muffin Break, Cafe UFO), always pass `--reference-dir` with 2-3 real product photos. Generated-from-nothing food is uncanny; anchored food is appetising.
