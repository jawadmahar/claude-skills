---
name: explorazone-design
description: Use this skill to generate well-branded interfaces and assets for EXPLORAZONE, the Norwich interactive science centre (operated by Coreaxis2 Ltd, mid-rebrand from "Exploring Science"). Use for production work or throwaway prototypes, mocks, decks, web pages, signage call-outs, school comms, and birthday-party collateral. Contains brand guidelines, colour and type tokens, and 20 preview specimens covering colour, type, spacing, components, and brand. Font TTFs, logo SVG/PNG assets, and the marketing-site UI kit are referenced but not yet bundled - see CAVEATS in README.md.
user-invocable: true
---

# EXPLORAZONE design skill

Read `README.md` first - it contains the full brand context, content fundamentals, and visual foundations. Then explore the other files as needed.

## Quick-start

- **Tokens & type:** `colors_and_type.css` - import at the top of any HTML you output.
- **Logos:** `assets/logos/` - prefer the SVGs (`lockup-orange-field.svg`, `lockup-white-keyline.svg`, emblems). PNG copies live alongside for environments that won't load SVG.
- **Fonts:** `assets/fonts/Astrii.ttf` (wordmark, reserved) and `assets/fonts/FFClanProBlk.ttf` (display).
- **Reference UI:** `ui_kits/marketing-site/index.html` shows the brand applied to a working homepage; `components.jsx` factors it into reusable pieces.
- **Card specimens:** `preview/` - one HTML file per token cluster.

## Hard rules (do not break)

1. The wordmark "EXPLORAZONE" is always the supplied SVG/PNG. Never re-type it in any font.
2. "Explorazone" in body copy. Capital E, single word. Never "Xplorazone", "Explora Zone", "Explorzone".
3. Every public surface carries "**formerly Exploring Science**" until 22 June 2026.
4. **No em dashes anywhere.** Use hyphens, commas, or full stops.
5. Only the six brand colours - no additions without sign-off.
6. Body face minimum 16px on digital, line-height 1.5 (SEND accessibility).
7. Do not blend Cafe UFO branding with Explorazone marks on the same surface.

## How to work

When asked to produce visual artefacts (slides, mocks, throwaway prototypes), write static HTML files that link `colors_and_type.css` and place real logo assets (copy them out, never inline base64 stand-ins). When working on production code, vendor the tokens in the host stack's idiom (CSS vars, design tokens, Tailwind config) and read the rules here as the source of truth.

If the user invokes this skill with no other guidance, ask:
- What surface are you producing - web, social, signage, deck, schools comms, birthday pack?
- Orange brand field or white field?
- Audience - families, schools, or partners?
- Any photography to work with, or should imagery placeholders be used?

Then act as an expert designer who outputs HTML artefacts or production code, depending on the need. Default to HTML mocks unless the user names a framework.
