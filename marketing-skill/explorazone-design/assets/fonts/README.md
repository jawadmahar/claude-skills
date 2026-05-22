# Fonts (drop-in placeholder)

Two TTF files belong here. They were not included in the design handoff bundle, so until they land the preview cards and any generated HTML will fall back to system stacks.

| Filename | Used as | Notes |
|---|---|---|
| `Astrii.ttf` | `--ez-font-logotype` | Reserved for the EXPLORAZONE wordmark. Never set body or headings in Astrii. The wordmark is *always* placed as the supplied SVG; this TTF exists only so the wordmark renders correctly inside design tools that re-set it. |
| `FFClanProBlk.ttf` | `--ez-font-display` | Display face. Headlines, signage call-outs, buttons, eyebrows. Always all caps. |

Source in the original Claude Design project: `uploads/ASTRII_.TTF`, `uploads/FFClanProBlk.TTF`.

The body face (`--ez-font-body`) is Inter, loaded via Google Fonts in `colors_and_type.css`. No file needed here.
