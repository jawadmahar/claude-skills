# EXPLORAZONE - Marketing site UI kit

The public-facing surface at **explorazone.co.uk**. Three click-thru pages built on the brand foundations defined in `/colors_and_type.css` and the components in `components.jsx`.

## What's in here

| File | Purpose |
|---|---|
| `index.html`     | Homepage - hero, stats, six exhibit zones, parties promo, schools strip. |
| `tickets.html`   | Tickets & opening times - three ticket cards, opening table, enquiry form. |
| `schools.html`   | School trips landing page - checklist, quote, enquiry form. |
| `components.jsx` | All React components for the kit. Each one is small and reusable. |
| `styles.css`     | Kit-specific layout CSS on top of `/colors_and_type.css`. |

## Components

- `ContinuityBar`  - orange top strip carrying "Formerly Exploring Science" + open hours + phone.
- `Header`        - sticky header with logo, primary nav, primary CTA.
- `Hero`          - orange hero, headline, lede, two CTAs. The decorative emblem is set at 18% opacity.
- `Stats`         - four-up stats strip that overlaps the hero.
- `SectionHead`   - eyebrow + display heading + lede paragraph.
- `AttractionCard`- image placeholder + tag + title + description. Hovers lift the card.
- `Attractions`   - the six-zone grid.
- `PartiesPromo`  - orange strip + an included-with feature card.
- `SchoolsPromo`  - split layout: copy + quote on the left, checklist on the right.
- `Footer`        - dark maroon footer with four columns and a legal strip.
- `PageShell`     - wraps ContinuityBar + Header + children + Footer.
- `TicketCard` / `TicketsPage` / `SchoolsPage` - inner-page compositions.

## How to use

Load any page in a browser. Each one bootstraps React + Babel, imports `components.jsx`, and renders the relevant composition. Click between pages from the header nav.

## Source-of-truth note

The brief did not supply an existing website codebase. The kit is therefore built directly from the brand-system-starter rules (`/brand-system-starter/`) and the brand vocabulary in `/README.md`. Every visual choice is traceable to a documented token, lockup, or rule - nothing is invented.

## Image policy

All photo slots are intentional placeholders (`mk-img-placeholder` + a brand-tinted gradient). When real photography arrives, swap the `mk-card-img` background to the new image URL. Do not draw photo content with SVG or generate it with AI.

## Accessibility / SEND

- Body copy never drops below 16px.
- Buttons keep a 44px minimum hit area.
- Continuity bar uses maroon-on-orange (`#491211` on `#ED4724`) - the approved on-orange pairing.
- Focus rings are 3px brand-orange at 18% opacity, on top of a 2px orange border.
