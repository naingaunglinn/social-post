# Night Ace — Content Calendar

## DESIGN SYSTEM v2 (2026-07-27) — current

The generated-3D dark look below (v1) was **rejected by the user as "cheap and noticeably AI"**
and replaced the same day with an editorial typographic system: `#F5F5F5` paper background,
Archivo Black display + IBM Plex Sans/Mono, giant type heroes, blue loading-bar signature.
Full spec lives in the skill's BRAND SYSTEM v2 block; the deterministic build pipeline lives in
`design/night-ace-v2/` (`build.py` → `render.js` → PNGs; `make_pptx.py` → Canva-importable PPTX).

- **Post-ready v2 exports:** `exports/2026-07-27-website-speed-first-time-visitors-v2/`
  (8 carousel PNGs 1080×1350, Facebook hero 1200×630, X hero 1920×1080)
- **Canva master v2:** import `night-ace-carousel-v2.pptx` (same folder) via Canva → *Import
  file*. Archivo Black / IBM Plex Sans / IBM Plex Mono are all in Canva's font library, so text
  arrives editable and on-font. After import, tokenize a copy (same `{{TOKEN}}` flow as v1) —
  or run the pipeline per post and skip Canva editing entirely.
- LinkedIn PDF for v2: assemble from the PNGs (`img2pdf`/ImageMagick) or export from Canva after
  the PPTX import.

## MASTER TEMPLATE (v1 — SUPERSEDED by Design System v2 above; kept for reference)

- **Carousel master (1080×1350, 8 pages):** design ID `DAHQkAjrvRg` — [edit](https://www.canva.com/d/HI0bivMtDkw9uRG)
  - Title in Canva: "MASTER — Night Ace carousel 1080×1350 (do not post)"
  - Lives in folder [Night Ace / Social / 2026-07](https://www.canva.com/folder/FAHQkIZqDtI) — move it up to `Night Ace / Social` if you prefer it month-agnostic.
- **Workflow per post (Path A):** `copy-design` the master → `start-editing-transaction` on the copy → one `perform-editing-operations` call with `find_and_replace_text` for every token below → `commit` → `resize-design` the filled copy to 1200×630 (Facebook) and 1920×1080 (X) → export.
  - **Heroes need no separate masters:** `resize-design` is confirmed working on this account (tested 2026-07-27), and resizing the *filled* carousel carries the finished copy into both hero sizes automatically.
- **Token map** (extends the skill's default table — this master has eyebrow/card/column slots):

| Token | Content |
|---|---|
| `{{HOOK}}` | Cover hook (page 1 title) |
| `{{SUB}}` | Cover subtitle |
| `{{S2_TITLE}}` / `{{S2_TITLE_B}}` | Slide 2 title, first + second line (second line renders electric blue) |
| `{{S2_BODY}}` | Slide 2 body |
| `{{S3_EYEBROW}}` / `{{S3_TITLE}}` / `{{S3_BODY}}` | Slide 3 blue eyebrow label, title, body |
| `{{S4_EYEBROW}}` / `{{S4_TITLE}}` / `{{S4_BODY}}` | Slide 4 blue eyebrow label, title, body |
| `{{S5_TITLE}}` / `{{S5_BODY}}` | Slide 5 title, body |
| `{{S6_TITLE}}` | Slide 6 title |
| `{{S6_CARD1_TITLE}}` / `{{S6_CARD1_BODY}}` | Slide 6 left card |
| `{{S6_CARD2_TITLE}}` / `{{S6_CARD2_BODY}}` | Slide 6 right card |
| `{{S7_TITLE}}` | Slide 7 title |
| `{{S7_COL1_TITLE}}` / `{{S7_COL1_BODY}}` | Slide 7 left column label + bullet |
| `{{S7_COL2_TITLE}}` / `{{S7_COL2_BODY}}` | Slide 7 right column label + bullet |
| `{{S8_TITLE}}` | Final slide big statement |
| `{{CTA}}` | Final slide CTA line |

- **Known master quirks** (fix manually in Canva once if desired; API cannot change these):
  - Font family is the generator's grotesque sans, not literal Space Grotesk — swap via Canva UI on the master once and every future post inherits it.
  - Slide 3 has a large saturated blue panel behind the phone image (shape fills aren't editable via MCP).
  - "Night Ace" wordmark exists on pages 1, 2, 5, 7 only (text elements can't be inserted via MCP; add to 3, 4, 6, 8 by hand if wanted).
  - Page 1/2/5/7 imagery is fixed obsidian-orb renders; replace per-post via `update_fill` with a new asset if variety is needed.

---

## 2026-07-27 — Website speed: "Your website feels fast to you. That's the problem."

- **Lane / pillar:** Service lane · Pillar 1 (web design tips)
- **Designs:**
  - Carousel (post this one): `DAHQkNQeZaM` — [edit](https://www.canva.com/d/XimC_nsnC8_bekU) · [view](https://www.canva.com/d/2NvPwXZwB7xBZNl)
  - Facebook hero 1200×630: `DAHQkDZUW-I` — [edit](https://www.canva.com/d/bieG67eObN_kODj)
  - X hero 1920×1080: `DAHQkPvyyqo` — [edit](https://www.canva.com/d/pTiS28nefIu8eln)
- **Exports:** `exports/2026-07-27-website-speed-first-time-visitors/`
  - `website-speed-first-time-visitors-01.png` … `-08.png` (Instagram, post pages 1–8 in order)
  - `website-speed-first-time-visitors-linkedin.pdf` (LinkedIn document carousel)
  - `website-speed-first-time-visitors-facebook-1200x630.png`
  - `website-speed-first-time-visitors-x-1920x1080.png`
- **Hook:** Your website feels fast to you. That's the problem.
- **Alt text:** Abstract 3D render of a glossy black orb speeding across a dark background, trailing frosted-glass fragments lit by electric blue light.

### LinkedIn caption

The owner of a slow website is usually the last person to know.

Your browser keeps saved copies of your own site, so every visit you make loads instantly. Your customers don't get that version. They get the cold load — every image, every script, every widget, usually over mobile data.

Three culprits cause most of it:

— Images uploaded straight from a camera, heavier than the rest of the page combined
— Add-on overload: chat widgets, trackers, and sliders all ship code visitors must download
— No caching or CDN, so the server rebuilds the page for every single visit

The honest test takes thirty seconds: open your site in a private window, on your phone, on mobile data. That's the version first-time visitors judge you on — and the one Google factors into rankings.

If you don't like what you see, that's fixable — and it's one of the highest-leverage improvements a business site can make.

#WebsiteSpeed #WebPerformance #WebDesign #SmallBusiness #Startups

### Facebook caption

Your website loads quickly on your computer because your browser has saved copies of it — your customers get the slow, from-scratch version, usually on a phone. Want to see what they see? Open your site in a private window on mobile data. If you don't like the result, send us the link — Night Ace will tell you exactly what's dragging it down, in plain language.

### Instagram caption

Your website feels fast to you. That's the problem.

Your browser has seen your site before — it loads saved copies. First-time visitors download everything cold, usually on a phone, on mobile data.

Most slowdowns trace back to three things: oversized images, too many add-on scripts, and no caching. All three are fixable without redesigning anything.

The honest test: open your site in a private window on your phone. If it drags, your customers already noticed.

Want a plain-language read on what's slowing yours down? Send Night Ace the link.

**Hashtags:** #websitespeed #pagespeed #webperformance #corewebvitals #websitedesign #webdevelopment #smallbusinesswebsite #startupwebsite #seotips #uxdesign #webdesigner #digitalstudio #businessgrowth #nightace

### X post

Your website feels fast to you because your browser has seen it before. First-time visitors load it cold, on a phone. Open it in a private window on mobile data — that's the speed your customers get. #WebPerformance #WebsiteSpeed

### Scheduling (audience US/EU; poster is in Myanmar, MMT included)

| Platform | Asset | Day | Time |
|---|---|---|---|
| LinkedIn | PDF carousel | Tue 2026-07-29 | 9:00 AM ET / 7:30 PM MMT |
| X | 16:9 hero PNG | Tue 2026-07-29 | 10:00 AM ET / 8:30 PM MMT |
| Facebook | 1200×630 hero PNG | Tue 2026-07-29 | 1:00 PM ET / 11:30 PM MMT |
| Instagram | PNG pages 1–8 | Wed 2026-07-30 | 11:00 AM ET / 9:30 PM MMT |

**SEO keywords:** website speed optimization, page speed, slow website fix, core web vitals, website performance, image optimization, website caching, CDN, small business website, site speed test, website audit, web design studio, web development agency, Night Ace

---

## LAYOUT LOG

| Post | Cover treatment | Slide-type sequence |
|---|---|---|
| 2026-07-27 website-speed (v2 light) | word mark `fast?` | A-A-A-A-A-A-A-A |
| 2026-07-27 design-principles | word mark `taste?` | A-A-A-A-A-A-A-A |
| 2026-07-27 ai-automation | **inverted** | E-B-C-D-I-G-A-E |
| 2026-07-28 claude-code-orchestration | statement | B-A-G-C-D-E-I-B |

Grid note (2026-07-27): the two word-mark covers read near-identical side by side — flagged for a
possible cover swap on design-principles before its Jul 31 slot; next post must not use inverted.
Grid note (2026-07-28): contact sheet re-checked with the statement cover added — four treatments
now in rotation, reads varied. Next post must not use a statement cover.

## 2026-07-28 — Claude Code orchestration: "Stop prompting. Start orchestrating."

- **Lane / pillar:** Craft lane · Pillar 3 (AI in practice, process/behind-the-scenes lens)
- **Deck (source of truth for all captions/hashtags/scheduling):** `content/2026-07-28-claude-code-orchestration-step.md`
- **Exports:** `exports/2026-07-28-claude-code-orchestration-step/` — 8 carousel PNGs 1080×1350,
  `-linkedin.pdf` (8 pages, ImageMagick), Facebook hero 1200×630 (own landscape composition, ink
  ground), X hero 1920×1080, `claude-code-orchestration-step.pptx` (Canva twin, generic v4 exporter)
- **Scheduled:** LinkedIn/X/Facebook Thu Aug 6, Instagram Fri Aug 7 (deck §13)
- **Lead magnet (comment gate):** every caption and slide 8 ask readers to comment "ACE" to
  receive the **Night Ace AI Orchestra** package — `giveaways/claude-code-ai-orchestra.zip`
  (README, PLAYBOOK, MIT license, 4 `ace-*` subagents, `/orchestra` + `/orchestra-audit`
  commands). Fulfil by DM: attach the zip, or upload it somewhere durable and send the link.
  Watch comments on all four platforms for "ACE" from Aug 6 onward.
- Canva upload: skipped (optional) — import the PPTX any time

## 2026-07-27 — AI automation for local businesses: "Your business doesn't need AI."

- **Lane / pillar:** Service lane · Pillar 3 (AI in practice)
- **Deck:** `content/2026-07-27-ai-automation-local-businesses.md`
- **Exports:** `exports/2026-07-27-ai-automation-local-businesses/` — 8 PNGs 1080×1350,
  `-linkedin.pdf` (8 pages), Facebook hero 1200×630 (own landscape composition per v4),
  X hero 1920×1080, `ai-automation-local-businesses.pptx` (Canva twin, generic v4 exporter)
- **Scheduled:** Facebook/LinkedIn/X Tue Aug 4, Instagram Wed Aug 5 (deck §13)

## 2026-07-27 — Design principles: "Taste starts arguments. Principles end them."

- **Lane / pillar:** Craft lane · Pillar 4 (process / behind-the-scenes)
- **Deck (source of truth for all captions/hashtags/scheduling):** `content/2026-07-27-design-principles-over-taste.md`
- **Exports:** `exports/2026-07-27-design-principles-over-taste/` — 8 carousel PNGs 1080×1350,
  `-linkedin.pdf` (8 pages), Facebook hero 1200×630, X hero 1920×1080,
  `design-principles-over-taste.pptx` (Canva-importable twin, titles in Archivo 700 per v3)
- **Design system:** v3 editorial typographic; giant heroes `taste? decide. one. space. type. again. less. purpose.` — words only, no numerals (principles aren't a sequence)
- **Scheduled:** LinkedIn/X/Facebook Thu Jul 31, Instagram Fri Aug 1 (details in deck §13)
- Canva upload: skipped (optional under v3) — import the PPTX any time

---

### Scratch designs from the website-speed v1 run (safe to delete in Canva)

- `DAHQkOpz5AM` — first-generation single-page collage (rejected)
- `DAHQkNy0ku0` — 1200×630 resize test of the collage
- `DAHQkBmY4hg` — 16:9 presentation original (source of the final carousel)
- Unpicked candidate batches: [batch 1](https://www.canva.com/d/HFkZrHTdOT10vw0) · [batch 2 c1](https://www.canva.com/d/izMfKuj7GaDbBb3) / [c2](https://www.canva.com/d/dVwYD3uGGZbbMHh) / [c3](https://www.canva.com/d/fGjEOSsRDvgMHTE)
