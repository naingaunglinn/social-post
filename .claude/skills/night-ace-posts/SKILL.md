---
name: night-ace-posts
description: Generates on-brand Night Ace social content packages (Facebook, Instagram, LinkedIn, X) and renders the matching carousel and hero images from the local design pipeline. Use when asked for Night Ace social posts, a content batch, or a post package.
argument-hint: "[count] [topic]"
disable-model-invocation: true
---

# Night Ace — Social Content Generator

Night Ace is a web design, development, and AI automation studio. Alternate between two audiences:

- **Craft lane** — developers, designers, technical founders. Builds authority.
- **Service lane** — business owners and non-technical founders. Generates inquiries.

---

## Step 0 — Preflight

**0a.** Read `night-ace-content-calendar.md`. Note the last 10 topics and hooks, and the
`LAYOUT LOG` — which cover treatment and which slide types the recent posts used. Don't repeat.

**0b.** Confirm `design/night-ace-v2/` has `build.py`, `render.js`, `make_pptx.py`, `fonts/`.

**0c.** Canva is optional — storage and the editable twin only, not layout.

---

## Step 1 — Arguments

First token, if a number → post count (**default 3**, warn above 4). Rest → topic. Otherwise rotate
pillars: 1) web design tips · 2) tech trend commentary · 3) AI in practice · 4) process /
behind-the-scenes · 5) engagement question. Never two adjacent posts in the same pillar or lane.

---

## Step 2 — Write the copy deck

Per post, all 13 sections:

1. **Topic** — angle + lane + pillar.
2. **Carousel script** — 8 slides, ~250 words. **Assign a slide type to each slide** from the
   library below, and check the composition rules before finalising.
3. **Hook** — cover line.
4. **LinkedIn caption** — short paragraphs, 3–5 hashtags inline.
5. **Facebook caption** — 2–4 sentences, one CTA.
6. **Instagram caption** — hook in line one.
7. **X post** — under 280 characters.
8. **Instagram hashtags** — 8–15, ending `#nightace`. **Mandatory.**
9. **Cover treatment** — which of the four cover types, and why this one isn't the last one used.
10. **Alt text** — one per asset.
11. **Filename slug** — kebab-case.
12. **Keywords** — 10–14, ending "Night Ace".
13. **Scheduling** — table: platform · asset · day · time, in both ET and MMT. **Mandatory.**

### Step 2b — Persist before designing

**On approval, write all 13 sections to `content/YYYY-MM-DD-<slug>.md` immediately.** Design work
reads from that file and never rewrites it. When the deck lives only in chat, §8 and §13 get lost in
long render runs.

---

## BRAND SYSTEM v4

### The invariants — these never change

Ground is either paper `#F5F5F5` or ink `#141419`. Type is Archivo and IBM Plex, nothing else. The
mono header row — `NIGHT ACE` left, `0N — 08` right — appears on every slide. One blue accent
moment per slide, never two. 96px margins on 1080×1350.

That is the whole brand. Six rules. Everything else is free to move, and should.

### The variables — vary these deliberately

Vertical anchoring · type scale · presence of a hero word · number of columns · ground inversion ·
real imagery · rule weight. A system with one layout isn't a system, it's a template, and a feed of
templates reads as wallpaper by the third post.

### Palette

| Role | Hex | Use |
|---|---|---|
| Paper | `#F5F5F5` | primary ground |
| Ink | `#141419` | display type; also an inverted ground |
| Electric blue | `#2E6BFF` | the single accent |
| Graphite | `#55555C` | body |
| Hairline | `#DFDFE4` | bar track, rules |

### Typography

- **Hero word:** Archivo Black, enormous, tight. Only here.
- **Titles:** Archivo variable 700–800 — not Black, which clots at title size.
- **Body:** IBM Plex Sans 400/500, line-height 1.5, measure ≤780px.
- **Micro-labels and code:** IBM Plex Mono Medium, uppercase, +14% tracking.

---

## SLIDE TYPE LIBRARY

Nine types, same DNA. Compose a sequence; don't repeat one type eight times.

**A · Hero word** — giant lowercase word, blue punctuation, title below, bar, body.
```
NIGHT ACE                 0N — 08
        (void)
  cached■
  You've seen it before.
  ▬▬▬▬▬▬────────────────
  body body body
```

**B · Full-bleed statement** — no hero word. The title *is* the giant type, edge to edge, 3–4 lines.
```
NIGHT ACE                 0N — 08
  Speed is
  part of the
  design.■
  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
```

**C · Numbered stack** — 3–5 short items, mono numerals hung in the left margin, real hierarchy.
```
NIGHT ACE                 0N — 08
  What passes the filter
  ▬▬▬▬▬────────────────
  01  Same steps every time
  02  Rules, not judgment
  03  Daily or weekly
  04  Cheap to fix
```

**D · Comparison split** — vertical hairline, two columns. This / not this.
```
NIGHT ACE                 0N — 08
  Automate      │  Keep human
  ─────────     │  ─────────
  Data entry    │  Pricing
  Routing       │  Negotiation
  Reports       │  Bad news
```

**E · Inverted** — ink ground, paper type, blue accent. Identical structure, opposite value. **At
least one per deck.** This is the cheapest, strongest variety move you have.

**F · Big number** — one huge numeral, small mono label. Only with a real, sourced figure.

**G · Mono block** — IBM Plex Mono on paper, terminal or code texture. Very on-brand for a dev
studio and completely different in feel from every other type.

**H · Artifact** — a real screenshot: PageSpeed report, DevTools waterfall, before/after, a diff.
Mono caption underneath. This is evidence, not decoration, and it's the ingredient the feed is
missing most.

**I · Pull quote** — one sentence set large in IBM Plex Sans, not Archivo. The texture change alone
makes the slide read differently.

### Composition rules

- **Max two consecutive slides of the same type.**
- **Type A max twice per deck.** It was eight-for-eight in the first two posts; that's the monotony.
- **At least one type E (inverted)** per deck — put it on the turn or the CTA.
- **At least one of G, H, or I** per deck when the topic allows.
- Vary vertical anchoring: don't bottom-anchor every slide.

### Cover rotation

Instagram is browsed as a 3-wide grid of covers. If every cover is a lowercase word with blue
punctuation, the profile reads as wallpaper — `fast?` and `taste?` were already near-identical two
posts in. Rotate covers, and **never use the same treatment as the previous post:**

1. **Word mark** — hero word + blue punctuation (type A).
2. **Statement** — the hook itself as full-bleed giant type (type B).
3. **Inverted** — ink ground, paper type (type E). Punches hardest in a grid of light tiles.
4. **Numeral** — a big figure or count when the post is genuinely a list of N.

**Alternate the cover's ground with the previous post.** Paper, then ink, then paper. This is the
grid's main variety mechanism — a feed of light tiles reads as wallpaper no matter how the type is
set, and the checkerboard is what makes a locked palette look varied across nine tiles. `build.py`
compares each build against the previous post's `deck.json` and prints a `! grid:` warning when
either the ground or the treatment repeats. Don't ship past that warning without a reason.

Record which one was used in the calendar's `LAYOUT LOG`.

### Contact-sheet check

Before publishing, tile the last nine covers into a 3×3 and look at it:

```bash
montage exports/*/[!0]*-01.png -tile 3x3 -geometry +8+8 /tmp/grid.png
```

If it reads as one repeated image, change the cover before posting. This is the check the audience
performs automatically when they land on the profile.

### Imagery

No AI-generated renders, ever — that was v1's failure. But **real artifacts are encouraged**:
screenshots, terminal output, before/after captures, photographs of actual work. A web studio that
never shows a screen is hiding its evidence.

### Anti-patterns

- Dark ground + one bright accent as the *whole system* (v1). Inverted slides are punctuation, not
  the default.
- Warm cream + serif display + terracotta accent.
- The broadsheet stack: hairlines everywhere, dense columns, zero radius. Keep hairlines to the bar
  track, the split rule in type D, and nothing else.
- `01 / 02 / 03` on content that isn't a sequence. The page counter is fine; carousel order is real.
- Gradients, glows, glassmorphism, ambient particles.
- Two accent moments on one slide — the final slide currently has both a blue hero period and
  "Night Ace" in blue. Pick one.

---

## Voice

Confident, modern, plain language. AI is a tool Night Ace uses well, never a "replaces the humans"
pitch. Every caption's first line works with zero context.

**Never invent** stats, clients, results, or testimonials. Write `[ADD REAL STAT]`.

---

## Step 3 — Render

Deck content is **data, not code**. Write a spec at `design/night-ace-v2/posts/<slug>.json`, then:

```bash
cd design/night-ace-v2
python3 build.py    <slug>   # posts/<slug>.json  → out/<slug>/*.html + deck.json
node   render.js    <slug>   # Playwright         → shots/<slug>/ + metrics/<slug>.json
python3 make_pptx.py <slug>  # Canva twin         → out/<slug>/<slug>.pptx
```

Each stage defaults to the newest post if the slug is omitted, and prints which one it picked.
Nothing overwrites a previous deck — every post owns its `out/`, `shots/`, and `metrics/` entry.

**Spec format.** Top level: `slug`, `title`, `cover` (the treatment name, for the LAYOUT LOG),
`hero` (`statement` + `sub` for the landscape compositions), and `slides` — a list whose entries
each declare a `type` plus that renderer's fields. `[[x]]` in any string wraps `x` in the electric-blue
accent span. Never hand-edit `build.py` to change copy; the renderers are the engine, the spec is
the content.

Any slide may set `"ground": "ink"` to invert regardless of its type. Ground inversion is a
**variable**, so a single-type deck can still carry punctuation — reach for this before reaching for
a new slide type.

**`anchor`** decides where a slide's free space goes: `top`, `center`, `bottom`, or `spread`.
`spread` splits the content into three zones — header, main group, tail — pinned to the top, middle
and bottom edges, so the tile reads full at thumbnail size. Every type A slide left at its default
pools 26–38% of the tile as blank ground at one end, which is what makes a light cover read as an
empty white square in the Instagram grid. Use `spread` on anything that will be a cover.

**`eyebrow`** is a small mono label above the main block. It anchors the top of the tile and gives
the accent a second home. Wrap any part in `[[…]]` to make it blue: `"eyebrow": "PRINCIPLE [[03]]"`.

**Blue budget: one accent moment per slide, and it must not be the terminal period every time.**
The old rule — bar fill plus the hero's period only — is why 14 of 14 accent uses across the first
four decks were a full stop. That is the single biggest source of the "every post looks the same"
feeling. Rotate where it lands: an eyebrow numeral, one word inside a title, the whole hero on an
inverted ground, a mono label. `[[…]]` works in any string in the spec, not just the giant word. `build.py` prints the cover, sequence, distinct-type count, and which slides
inverted, and writes the same into `out/<slug>/deck.json` with a ready-to-paste `layout_log_line`.
Copy that line into the LAYOUT LOG rather than retyping the sequence from memory.

**Sizing giant type is measurable, not guesswork.** `.hero` is `white-space:nowrap` inside
`overflow:hidden`, so an oversized word is **clipped silently** — it will not look wrong in the HTML,
only in the PNG. Portrait measure is 888px (1080 − 2×96 pad). Check a `gpx` before trusting it:

```bash
python3 -c "
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
f=instantiateVariableFont(TTFont('fonts/Archivo.ttf'),{'wght':900,'wdth':100},inplace=False)
u=f['head'].unitsPerEm; c=f.getBestCmap(); h=f['hmtx']
w=lambda t,s: sum(h[c[ord(x)]][0] for x in t)/u*s - len(t)*0.025*s
print(w('purpose.',172))   # must be <= 888
"
```

Sizing every giant word to the *same optical width* (~778px) rather than the same point size is the
intended look — a word-mark series fills the measure.

**Landscape heroes get their own composition.** The current 1200×630 is the portrait layout
reflowed, which leaves the right half empty and the type undersized. Re-set it: type scales up,
content spans the width, header row stays.

Assets: 8 carousel PNGs at 1080×1350, an 8-page PDF, a 1200×630 Facebook hero, a 1920×1080 X hero.

**Look at every page before declaring done.** A render that compiles is not a render that reads.

### If the design system itself changes

Load `frontend-design` first and follow its two-pass process — plan the tokens, critique the plan
against the anti-patterns, then build. Update this block; the spec lives here.

A design change **never re-runs Step 2 and never touches the deck file.** Rebuild assets, then
re-print §8 and §13 in the summary.

---

## Step 4 — Export, file, log

1. `exports/YYYY-MM-DD-<slug>/`: numbered PNGs, `-linkedin.pdf`, both heroes, the PPTX.
2. Optional: Canva, filed under `Night Ace / Social / YYYY-MM`.
3. Append to `night-ace-content-calendar.md`: deck file link, export path, and the `LAYOUT LOG`
   line — copy `layout_log_line` from `out/<slug>/deck.json`, don't retype it. A hand-typed
   sequence can drift from what actually rendered; the manifest can't.

## Step 5 — Definition of done

```
Deck file      content/YYYY-MM-DD-<slug>.md         [ ]
  §8 hashtags present                               [ ]
  §13 scheduling table present                      [ ]
Slide types    ≥4 distinct, ≥1 inverted             [ ]
Cover          differs from previous post           [ ]
Contact sheet  checked, not wallpaper               [ ]
Carousel       8 PNGs @ 1080×1350, viewed           [ ]
LinkedIn PDF   8 pages                              [ ]
FB hero        1200×630, own composition            [ ]
X hero         1920×1080                            [ ]
Calendar + LAYOUT LOG updated                       [ ]
```

Paste the hashtag block and scheduling table into chat directly — not a link. Those get copied into
a phone at posting time.

---

## Guardrails

- No invented numbers, clients, or outcomes.
- No hook, topic, or cover treatment repeated from recent entries.
- Off-brand output means fixing this file, not patching one post.
- Report tool failures plainly. Never substitute a description for an asset.

---

**Usage**
- `/night-ace-posts` → 3 posts, alternating lanes
- `/night-ace-posts 2 website speed` → 2 posts on that topic
- `/night-ace-posts 1 AI automation for local businesses` → single service-lane post
