# EXPLORAZONE - Science Discovery Lab

A 15,000 sq ft interactive children's science centre at Unit 5-6, Francis Way, Bowthorpe Park, Norwich, NR5 9JA. Operated by **Coreaxis2 Ltd** (Company No. 16929722). The venue carries 80+ hands-on exhibits, a VR zone, live workshops, birthday parties, school trips, and **Cafe UFO** on-site.

The brand is mid-rebrand from **"Exploring Science"** to **"EXPLORAZONE"**, with full switch targeted for **22 June 2026**. Every public surface produced before that date should carry "**formerly Exploring Science**" as a continuity cue.

This folder is the design system for that brand. Anything Claude Design generates for Explorazone (web pages, social, signage mock-ups, decks) should pull tokens and components from here.

## Sources

| Source | Where to find it |
|---|---|
| Brand vocabulary - colours, type, lockup rules, voice | `brand-system-starter/` (local mount, read-only) |
| Brand mark SVGs and brand fonts                       | `uploads/` (project filesystem) |
| Colour-spec PDFs                                      | `uploads/EXPLORAZONE COLOUR CODES (1).pdf`, `uploads/EXPLORAZONE ONLY.pdf` |
| Rendered lockup PNGs                                  | `uploads/EXPLORAZONE-ORANGE.png`, `uploads/EXPLORAZONE-WHITE.png` |

No existing production website was supplied. The marketing-site UI kit in `ui_kits/marketing-site/` is therefore built directly from the documented brand rules - it does not recreate a live site.

## Index

| Path | Purpose |
|---|---|
| `README.md`              | This file. |
| `SKILL.md`               | Agent Skill manifest - load this folder as a Claude Code skill. |
| `colors_and_type.css`    | Single source of truth for colour + type + spacing + radii + shadow tokens. Import at the top of any HTML output. |
| `assets/fonts/`          | Astrii (wordmark) and FF Clan Pro Black (display) TTFs. |
| `assets/logos/`          | Approved lockups (SVG + PNG) and emblems. |
| `preview/`               | Small HTML cards that populate the Design System tab (colours, type, spacing, components, brand). |
| `ui_kits/marketing-site/`| Click-thru recreation of explorazone.co.uk - homepage + tickets + schools. |

## Content fundamentals

**Voice.** Warm, direct, confident. Speaks to families and schools. British English. Professional but never corporate. Sentences are short, active, and honest about what the day is like (the floor is loud, the cafe is on-site, the VR is bookable on the day). The brand sells experience, not credentials.

**Casing.** Body copy is sentence case. Headlines and buttons are **ALL CAPS** because FF Clan Pro Black is always set in caps; never set caps on Inter body copy. Eyebrows, tags, and labels are caps tracked +0.08em.

**The brand name.** "Explorazone" in body copy (single word, capital E). "EXPLORAZONE" only as the wordmark - and always as the supplied SVG, never re-typed. The descriptor is "Science Discovery Lab", always set in FF Clan Pro Black, all caps.

**Person.** Mostly "you" to the visitor; "we" sparingly for the venue. School-facing copy switches to "your pupils" / "your trip lead".

**Hero phrases approved by Khalil.**
- "Same team. New name. Bigger adventure."
- "New management. New experience. Same amazing science."
- "Norwich's biggest interactive science centre."
- "15,000 sq ft of hands-on adventure."

**Continuity cue.** During the dual-branding window (April-June 2026), every public surface should carry "**formerly Exploring Science**" - top of page, footer, or a continuity banner. Patterns are documented in `preview/components-continuity.html`.

**Punctuation, hard rules.**
- **No em dashes.** Use hyphens, commas, or full stops.
- Spaced en-dashes in body copy are fine (" - "). The brand-system-starter README models this.
- Ampersands `&` are allowed in headings, navigation, and tabular labels; full word "and" in body.
- No exclamation marks in body copy. Headlines may use one full stop per sentence, including short ones ("Bigger Adventure.").

**Numbers and money.** Always £ with no space (£18, £4.50). Use commas for thousands ("15,000 sq ft"). Don't mix decimals and whole-pound prices in the same row.

**Pricing rules supplied by Khalil.**
- School trip standard rate £18 pp - never mention a cafe meal in that bundle.
- Birthday parties from £18 pp; max 20% discount cap.
- No VAT on customer-facing documents.

**Emoji and unicode.** Avoid emoji in marketing copy. The brand does not use emoji as a visual system - the green X-arrows in the wordmark are the brand's "icon" mood. Unicode `★`, `→`, `·` (middot), and `✓` are acceptable as small inline glyphs.

**SEND-friendly copywriting.** Avoid metaphor-only sentences; pair every figurative line with a literal one. State quietly important practical info (calm room, drop-off bay, sensory advisory) in plain language, never in italics or asides.

**Avoid.** "Guided sessions" language in standard school comms (it implies a paid extra); "magical" and "amazing" overuse (the brand prefers concrete superlatives like "loud", "big", "hands-on", "noisy"); any blending of Cafe UFO and Explorazone marks on the same surface.

## Visual foundations

**Palette.** Six values, no more. The brand explicitly forbids introducing new palette colours without sign-off.

| Token | Hex | When |
|---|---|---|
| Primary orange   | `#ED4724` | Hero surfaces, buttons, brand fields. The most-used colour. |
| Surface white    | `#FFFFFF` | Page and card background. |
| Maroon on orange | `#491211` | Body, descriptor, dim text on the orange field. |
| Maroon on white  | `#561F1C` | Default body text on white. |
| Green on orange  | `#99CC67` | X-arrow accent on the orange lockup. |
| Green on white   | `#A7CF38` | Default digital accent. Success states. |

The two maroons and the two greens are *not* light/dark variants - they are context-paired. Pick by surface. There is no neutral grey scale; use `rgba(73,18,17,0.12)` for keylines, `rgba(73,18,17,0.06)` for shadows. Tints of orange (`rgba(237,71,36,0.08)`) are the only acceptable tinted neutrals.

**Backgrounds.** Two main surfaces - the orange brand field and white. A subtle off-white `#FAF7F3` is acceptable for sectioned page heroes inside the marketing site (pulled from the maroon at low saturation). **No gradients between brand colours**, except inside placeholder image slots where the gradient is monochrome inside one brand colour. No patterns, no textures, no grain, no photographic overlays.

**Type.** Three families, strictly role-locked.
- **Astrii** - the pixel-grid wordmark face. Reserved for the EXPLORAZONE wordmark. The wordmark is *always* placed as the supplied SVG, never re-typed.
- **FF Clan Pro Black** - display. Headlines, signage call-outs, buttons, eyebrows, labels. Always all caps, tracking -0.02em on large sizes, +0.06 to +0.10em on small sizes.
- **Inter** (placeholder, pending Khalil) - body. 16px floor on digital, line-height 1.5.

**Type hierarchy.** Display sits on top of body with a deliberate size jump (40-56px vs 14-16px). Avoid mid-weight 24-32px headlines - they read as web-template default and dilute the chunky display voice.

**Spacing.** 4px base grid. Tokens 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 80 / 96. Sections sit on 80px vertical rhythm on desktop, 56px on smaller surfaces. The brand uses generous white space - SEND visitors specifically benefit from low visual clutter, so prefer one big idea per section.

**Corner radii.** `md` (8px) for buttons and inputs. `lg` (16px) for cards, surfaces, panels. `pill` (999px) is reserved for status pills and tags only - never on buttons. `none` (0) on full-bleed banners. No mixed radii within one card.

**Borders / keylines.**
- Default keyline: 1px `rgba(73,18,17,0.12)`.
- Brand keyline (the official one for the white-field lockup): 2px solid `#ED4724`. This is the rectangle frame around the white-field wordmark - reproduce it carefully when building any white-field mark.

**Cards.** White background, 1px keyline, `lg` radius (16px), padding 24px, shadow-1 (low maroon tint). On hover, lift -2px and graduate to shadow-3. No coloured left borders, no top accents - the brand keyline is reserved.

**Shadows / elevation.** Four steps, all maroon-tinted. Never blue or pure black. See `preview/shadows.html`. Use shadow-2 on cards, shadow-3 on hover and popovers, shadow-4 only on modals.

**Animation.** Brisk and friendly, never bouncy or theatrical. Durations 120 / 200 / 360ms. Easing `cubic-bezier(0.2, 0.7, 0.2, 1)`. Hover states use a 6% brightness lift (`filter: brightness(1.06)`); press states translate `+1px`. Cards lift `-2px` on hover. Avoid scale transforms above 1.02; the brand reads young, not jumpy.

**Hover and press states.**
- Buttons: hover `filter: brightness(1.06)`; press `translateY(+1px)`.
- Cards: hover `translateY(-2px)` + shadow lift.
- Links: orange brand colour with no underline; underline on hover.
- Inputs: 2px orange border on focus + 3px orange-at-18% glow ring.

**Transparency and blur.** Used sparingly. Card tags on top of photos use `rgba(255,255,255,0.92)` with `backdrop-filter: blur(4px)`. The decorative hero emblem sits at 18% opacity. Never use transparency on body copy.

**Imagery vibe.** Warm, primary, slightly loud. Children mid-activity, not posed. Avoid moody / blue-toned photography; reach for daylight, bright primaries, and shallow depth where possible. When real photography is missing, ship a **labelled placeholder** (brand-tinted gradient + caps caption) rather than an AI-generated or stock image.

**Layout rules.**
- Headers are sticky at 60-72px. The continuity bar (orange) sits *above* the white header during the dual-branding window.
- Footers are dark maroon (`#2a1110`) - the only dark surface in the system.
- Page content max-width 1200px, centred. Side gutters 32px desktop, 16px mobile.
- Hero copy is always left-aligned. Body sections may centre headings; never centre body paragraphs longer than two lines.

**Protection.** The official wordmark needs clear space equal to the height of one capital "E" on all sides. Never crop the wordmark; if space is tight, drop to the emblem instead.

## Iconography

The brand does not ship an icon set. The only visual marks supplied are:

- Two **wordmark lockups** (`Logo_Logo_01.svg` orange field, `Logo_Logo_02.svg` white keyline) - copied into `assets/logos/` as `lockup-orange-field.svg` and `lockup-white-keyline.svg`, plus PNG copies. Always reach for the SVG first; the PNGs are a fallback for environments that won't load SVG.
- Four **emblems**:
  - `emblem-orange-square.svg` - pixel emblem on a filled orange square.
  - `emblem-pattern-only.svg` - just the pattern, transparent background. Use this when placing on photos or other brand surfaces.
  - `emblem-orange-circle.svg` - app icon / favicon, filled orange circle.
  - `emblem-white-circle.svg` - app icon / favicon, white circle with orange pattern.

**Approach.** The brand reads as a pixel-grid system. Treat ANY iconography you add to a surface as if it were drawn on the same 12-square grid as the wordmark. Prefer:
1. The supplied emblem as a quiet brand stamp.
2. Unicode glyphs (`✓`, `→`, `★`, `·`) for inline cues.
3. **Lucide** icons (`lucide.dev`, CDN: `https://cdn.jsdelivr.net/npm/lucide-static@latest/icons/`) as a substitute set when a real icon is required - **flag any use of Lucide as a substitution pending Khalil's official icon system.** Lucide is the closest match: 1.5px stroke, square caps, plain geometry, no flourishes.

**Do not.**
- Do not draw new icons inline with hand-rolled SVG paths.
- Do not import Heroicons, Phosphor, Tabler, Font Awesome, or any rounded / duotone icon family - they fight the pixel-grid vocabulary.
- Do not use emoji as a substitute for icons.
- Do not use coloured icons; if an icon is added, use `currentColor` so it picks up the brand orange or maroon from context.

## Quick contract for Claude Design

When generating any Explorazone surface, do all of the following:

1. Link `colors_and_type.css` (or vendor its tokens) - do not invent colour or type values.
2. Place a supplied SVG/PNG lockup, never re-type EXPLORAZONE.
3. Carry "formerly Exploring Science" until 22 June 2026.
4. Use FF Clan Pro Black for headings (all caps), Inter for body (16px+).
5. No em dashes. No new palette colours. No mixed Cafe UFO branding on the same surface.

## Operating context

- **Entity:** Coreaxis2 Ltd, Company No. 16929722.
- **Address:** Unit 5-6, Francis Way, Bowthorpe Park, Norwich, NR5 9JA.
- **Phone:** 01603 927900.
- **Web:** explorazone.co.uk (single canonical domain; old domain 301-redirects).
- **Rebrand window:** April 2026 - 22 June 2026 (transition from "Exploring Science").

---

*Built 15 May 2026 against the brand-system-starter v1 and Khalil's brand pack. Body face Inter is a placeholder; flag any work that depends on the final body face for confirmation.*

## CAVEATS / install state

This skill was installed from the Claude Design handoff bundle on 22 May 2026. The following items are **referenced by SKILL.md and README.md but were not present in the bundle**, and need to be dropped in before the skill is fully usable:

| Missing path | What it is | Where to source from |
|---|---|---|
| `assets/fonts/Astrii.ttf` | Wordmark face (logotype only) | `uploads/ASTRII_.TTF` in the original project |
| `assets/fonts/FFClanProBlk.ttf` | Display face (headlines, buttons, eyebrows) | `uploads/FFClanProBlk.TTF` in the original project |
| `assets/logos/lockup-orange-field.svg` (+ `.png`) | Reversed wordmark on orange field | `uploads/Logo_Logo_01.svg`, `uploads/EXPLORAZONE-ORANGE.png` |
| `assets/logos/lockup-white-keyline.svg` (+ `.png`) | Orange wordmark on white field with 2px orange keyline | `uploads/Logo_Logo_02.svg`, `uploads/EXPLORAZONE-WHITE.png` |
| `assets/logos/emblem-orange-square.svg` | Pixel emblem on filled orange square | `uploads/Logo_Emblem_01.svg` |
| `assets/logos/emblem-pattern-only.svg` | Emblem pattern, transparent background | `uploads/Logo_Emblem_02.svg` |
| `assets/logos/emblem-orange-circle.svg` | App icon / favicon, orange circle | `uploads/Logo_ Rounded Emblem_01.svg` |
| `assets/logos/emblem-white-circle.svg` | App icon / favicon, white circle | `uploads/Logo_Rounded Emblem_02.svg` |
| `ui_kits/marketing-site/` | Click-thru recreation (home + tickets + schools) | Not in bundle; rebuild against the rules above when needed |

Until the fonts land, preview cards fall back to the stack defined in `colors_and_type.css` (`Helvetica Neue` / `Arial Black` for display, `Inter` from Google Fonts for body). The wordmark must still be placed as the supplied SVG once available - never re-typed.
