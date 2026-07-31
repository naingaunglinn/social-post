#!/usr/bin/env python3
"""Night Ace v5 slide builder — one renderer per slide type (A/B/C/D/E/G/I),
plus dedicated landscape hero compositions.

Deck content is data, not code: each post is a JSON spec in posts/, and output
goes to out/<slug>/ so decks never overwrite each other.

    python3 build.py                 # newest spec in posts/
    python3 build.py <slug>          # posts/<slug>.json
    python3 build.py posts/x.json    # explicit path

In spec strings, [[x]] wraps x in the electric-blue accent span."""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(ROOT, "fonts")
POSTS = os.path.join(ROOT, "posts")

PAPER, INK, BLUE, GRAPHITE, TRACK = "#F5F5F5", "#141419", "#2E6BFF", "#55555C", "#DFDFE4"

# out/<slug>/*.html sits two levels below fonts/ — relative keeps emitted HTML
# portable across machines (absolute file:// paths baked in the builder's cwd).
FONT_URL = "../../fonts"

CSS_BASE = f"""
@font-face {{ font-family:'Archivo VF'; src:url('{FONT_URL}/Archivo.ttf'); font-weight:100 1000; }}
@font-face {{ font-family:'Plex VF'; src:url('{FONT_URL}/IBMPlexSans.ttf'); font-weight:100 1000; }}
@font-face {{ font-family:'Plex Mono'; src:url('{FONT_URL}/IBMPlexMono-Regular.ttf'); font-weight:400; }}
@font-face {{ font-family:'Plex Mono'; src:url('{FONT_URL}/IBMPlexMono-Medium.ttf'); font-weight:500; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:100%; height:100%; }}
body {{ font-family:'Plex VF',sans-serif; -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility; }}
.slide {{ display:flex; flex-direction:column; overflow:hidden; }}
.slide.spread {{ justify-content:space-between; }}
.slide.paper {{ background:{PAPER}; color:{INK}; }}
.slide.ink {{ background:{INK}; color:{PAPER}; }}
.hdr {{ display:flex; justify-content:space-between; align-items:baseline; }}
.mono {{ font-family:'Plex Mono',monospace; font-weight:500; letter-spacing:.14em; }}
.paper .wordmark {{ color:{INK}; }} .ink .wordmark {{ color:{PAPER}; }}
.pageno {{ color:{GRAPHITE}; }} .ink .pageno {{ color:{TRACK}; }}
.blue {{ color:{BLUE}; }}
.hero {{ font-family:'Archivo VF'; font-weight:900; letter-spacing:-0.025em; line-height:.94; white-space:nowrap; }}
.statement {{ font-family:'Archivo VF'; font-weight:800; letter-spacing:-0.02em; line-height:1.04; }}
.title {{ font-family:'Archivo VF'; font-weight:750; letter-spacing:-0.015em; line-height:1.1; }}
.bar {{ height:6px; border-radius:3px; background:{TRACK}; position:relative; flex:none; }}
.ink .bar {{ background:{GRAPHITE}; }}
.bar i {{ position:absolute; left:0; top:0; bottom:0; border-radius:3px; background:{BLUE}; }}
.body {{ color:{GRAPHITE}; line-height:1.5; font-weight:420; }}
.ink .body {{ color:{TRACK}; }}
.cta {{ line-height:1.45; font-weight:560; }}
.paper .cta {{ color:{INK}; }} .ink .cta {{ color:{PAPER}; }}
.row {{ display:flex; align-items:baseline; }}
.num {{ font-family:'Plex Mono',monospace; font-weight:500; letter-spacing:.14em; color:{GRAPHITE}; flex:none; }}
.item {{ font-weight:520; }}
.cols {{ display:flex; }}
.coltitle {{ font-family:'Archivo VF'; font-weight:750; letter-spacing:-0.01em; }}
.colitems {{ color:{GRAPHITE}; line-height:1.75; font-weight:450; }}
.mlabel {{ font-family:'Plex Mono',monospace; font-weight:500; letter-spacing:.1em; flex:none; }}
.mdesc {{ font-family:'Plex Mono',monospace; font-weight:400; letter-spacing:.02em; color:{GRAPHITE}; }}
.quote {{ font-weight:500; line-height:1.32; letter-spacing:-0.005em; }}
"""

B = lambda s: f'<span class="blue">{s}</span>'

# ---- composition primitives -------------------------------------------------

ANCHORS = ("top", "center", "bottom", "spread")

def layout(s, default, group, tail=""):
    """Place a slide's content. `group` is the main block, kept tight together;
    `tail` is an optional element that wants the bottom edge.

    anchor=spread emits group and tail as separate flex children, so with the
    header they become three zones — top / middle / bottom — and the tile reads
    full at thumbnail size. Other anchors pool the free space at one end."""
    a = s.get("anchor", default)
    if a not in ANCHORS:
        sys.exit(f"anchor must be one of {'/'.join(ANCHORS)}, got {a!r}")
    if a == "spread":
        return f"<div>{group}</div>{tail}"
    if a == "top":
        return group + tail + '<div style="margin-bottom:auto"></div>'
    if a == "center":
        return ('<div style="margin-top:auto"></div>' + group + tail
                + '<div style="margin-bottom:auto"></div>')
    return '<div style="margin-top:auto"></div>' + group + tail

def eyebrow(s, mb=28):
    """Small mono label above the main block. Fills the top of the tile and gives
    the accent somewhere to land other than a terminal period."""
    if not s.get("eyebrow"):
        return ""
    return (f'<div class="mono" style="font-size:26px;letter-spacing:.14em;'
            f'margin-bottom:{mb}px">{s["eyebrow"]}</div>')

# ---- spec loading ----------------------------------------------------------

def expand(v):
    """Recursively turn [[x]] into a blue accent span."""
    if isinstance(v, str):
        return re.sub(r"\[\[(.+?)\]\]", lambda m: B(m.group(1)), v)
    if isinstance(v, list):
        return [expand(x) for x in v]
    if isinstance(v, dict):
        return {k: expand(x) for k, x in v.items()}
    return v

def load_spec(arg=None):
    if arg and os.path.sep in arg:
        path = arg
    elif arg:
        path = os.path.join(POSTS, arg if arg.endswith(".json") else arg + ".json")
    else:
        found = sorted(glob.glob(os.path.join(POSTS, "*.json")))
        if not found:
            sys.exit(f"no deck specs in {POSTS}/")
        path = found[-1]
        print("no slug given — using newest spec:", os.path.basename(path))
    if not os.path.exists(path):
        avail = "\n  ".join(sorted(os.path.basename(p)[:-5]
                                  for p in glob.glob(os.path.join(POSTS, "*.json"))))
        sys.exit(f"no spec at {path}\navailable:\n  {avail}")
    spec = json.load(open(path, encoding="utf-8"))
    spec.setdefault("slug", os.path.basename(path)[:-5])
    for key in ("hero", "slides"):
        if key not in spec:
            sys.exit(f"{path}: missing required key '{key}'")
    return expand(spec)

SPEC = load_spec(sys.argv[1] if len(sys.argv) > 1 else None)
SLUG = SPEC["slug"]
SLIDES = SPEC["slides"]
OUT = os.path.join(ROOT, "out", SLUG)
os.makedirs(OUT, exist_ok=True)

def page(idx, total, ground, inner, W, H, PAD, mono_px, extra=""):
    css = CSS_BASE + f".slide {{ width:{W}px; height:{H}px; padding:{PAD}px; }}"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body><div class="slide {ground}{(' ' + extra) if extra else ''}">
  <div class="hdr">
    <span class="mono wordmark" style="font-size:{mono_px}px">NIGHT&nbsp;ACE</span>
    <span class="mono pageno" style="font-size:{mono_px}px">{idx:02d} — {total:02d}</span>
  </div>
{inner}</div></body></html>"""

def bar(idx, total, mt):
    fill = round(idx / max(total, 1) * 100, 2)
    return f'<div class="bar" style="margin-top:{mt}px"><i style="width:{fill}%"></i></div>'

# ---- slide type renderers (portrait 1080×1350, PAD 96) ---------------------

def type_A(idx, total, s):  # hero word; anchor default bottom
    group = (eyebrow(s)
             + f'<div class="hero" style="font-size:{s["gpx"]}px">{s["giant"]}</div>'
             f'<div class="title" style="font-size:{s.get("tpx",66)}px;max-width:860px;margin-top:52px">{s["title"]}</div>'
             + bar(idx, total, 44))
    tail = f'<div class="body" style="font-size:32px;max-width:780px;margin-top:44px">{s["body"]}</div>'
    return "paper", layout(s, "bottom", group, tail)

def type_B(idx, total, s):  # full-bleed statement; anchor default top
    mt = 0 if s.get("eyebrow") or s.get("anchor") != "top" else 120
    group = (eyebrow(s, mb=32)
             + f'<div class="statement" style="font-size:{s.get("spx",100)}px;margin-top:{mt}px">{s["statement"]}</div>'
             + bar(idx, total, 48))
    tail = (f'<div class="body" style="font-size:32px;max-width:780px;margin-top:40px">{s["tail"]}</div>'
            if s.get("tail") else "")
    return "paper", layout(s, "top", group, tail)

def type_C(idx, total, s):  # numbered stack
    rows = "".join(
        f'<div class="row" style="margin-top:{0 if i == 0 else 44}px">'
        f'<div class="num" style="font-size:26px;width:110px">{i + 1:02d}</div>'
        f'<div class="item" style="font-size:40px">{it}</div></div>'
        for i, it in enumerate(s["items"]))
    mt = 0 if s.get("eyebrow") or s.get("anchor") != "top" else 120
    group = (eyebrow(s)
             + f'<div class="title" style="font-size:66px;max-width:860px;margin-top:{mt}px">{s["title"]}</div>'
             + bar(idx, total, 40))
    return "paper", layout(s, "top", group, f'<div style="margin-top:64px">{rows}</div>')

def type_D(idx, total, s):  # comparison split, columns centered, bar bottom-anchored
    def col(title, items, blue=False, pad="padding-right:56px", rule=""):
        t = B(title) if blue else title
        its = "<br>".join(items)
        return (f'<div style="width:50%;{pad};{rule}">'
                f'<div class="coltitle" style="font-size:52px">{t}</div>'
                f'<div class="colitems" style="font-size:34px;line-height:1.9;margin-top:36px">{its}</div></div>')
    inner = (
        f'<div class="cols" style="margin-top:auto">'
        + col(s["titleL"], s["itemsL"], blue=True)
        + col(s["titleR"], s["itemsR"], pad="padding-left:56px", rule=f"border-left:1px solid {TRACK}")
        + '</div>'
        + bar(idx, total, 0).replace('margin-top:0px', 'margin-top:auto'))
    return "paper", inner

def type_E(idx, total, s):  # inverted statement (cover / CTA), centered
    sub = ""
    if s.get("sub"):
        sub = f'<div class="body" style="font-size:32px;max-width:780px;margin-top:40px">{s["sub"]}</div>'
    if s.get("cta"):
        sub = f'<div class="cta" style="font-size:34px;max-width:820px;margin-top:40px">{s["cta"]}</div>'
    inner = (
        f'<div style="margin-top:auto"></div>'
        f'<div class="statement" style="font-size:{s.get("spx",100)}px">{s["statement"]}</div>'
        + bar(idx, total, 44) + sub
        + f'<div style="margin-bottom:auto"></div><div style="height:64px"></div>')
    return "ink", inner

def type_G(idx, total, s):  # mono block
    rows = "".join(
        f'<div class="row" style="margin-top:{0 if i == 0 else 40}px">'
        f'<div class="mlabel" style="font-size:30px;width:330px;{ "color:" + BLUE if i == len(s["rows"]) - 1 else ""}">{lab}</div>'
        f'<div class="mdesc" style="font-size:30px">{desc}</div></div>'
        for i, (lab, desc) in enumerate(s["rows"]))
    mt = 0 if s.get("eyebrow") or s.get("anchor") != "top" else 120
    group = (eyebrow(s)
             + f'<div class="title" style="font-size:66px;max-width:860px;margin-top:{mt}px">{s["title"]}</div>'
             + bar(idx, total, 40))
    return "paper", layout(s, "top", group, f'<div style="margin-top:72px">{rows}</div>')

def type_I(idx, total, s):  # pull quote, centered; bar at bottom
    inner = (
        f'<div class="quote" style="font-size:60px;max-width:840px;margin-top:auto">{s["quote"]}</div>'
        + bar(idx, total, 0).replace('margin-top:0px', 'margin-top:auto'))
    return "paper", inner

RENDERERS = {"A": type_A, "B": type_B, "C": type_C, "D": type_D, "E": type_E, "G": type_G, "I": type_I}

# ---- render the deck from the spec -----------------------------------------

def render_slide(i, s):
    """Returns (ground, inner, extra_class). An explicit spec `ground` overrides
    the type's default, so inversion is a per-slide variable on any slide type."""
    if s["type"] not in RENDERERS:
        sys.exit(f"slide {i}: unknown type {s['type']!r} (have {'/'.join(sorted(RENDERERS))})")
    ground, inner = RENDERERS[s["type"]](i, len(SLIDES), s)
    override = s.get("ground")
    if override not in (None, "paper", "ink"):
        sys.exit(f"slide {i}: ground must be 'paper' or 'ink', got {override!r}")
    extra = "spread" if s.get("anchor") == "spread" else ""
    return (override or ground), inner, extra

for i, s in enumerate(SLIDES, 1):
    ground, inner, extra = render_slide(i, s)
    open(os.path.join(OUT, f"slide-{i:02d}.html"), "w", encoding="utf-8").write(
        page(i, len(SLIDES), ground, inner, 1080, 1350, 96, 22, extra))

# ---- landscape heroes: own composition, full width, type scales up ---------

def hero(name, W, H, PAD, spx, sub_px, mono_px, bar_mt, sub_mt):
    n = len(SLIDES)
    inner = (
        f'<div style="margin-top:auto"></div>'
        f'<div class="statement" style="font-size:{spx}px">{SPEC["hero"]["statement"]}</div>'
        + bar(1, n, bar_mt)
        + f'<div class="body" style="font-size:{sub_px}px;margin-top:{sub_mt}px">{SPEC["hero"]["sub"]}</div>'
        + f'<div style="margin-bottom:auto"></div>')
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(
        page(1, n, "ink", inner, W, H, PAD, mono_px))

hero("hero-fb.html", 1200, 630, 64, 66, 24, 16, 32, 24)
hero("hero-x.html", 1920, 1080, 96, 104, 32, 22, 44, 32)

# ---- manifest: the LAYOUT LOG line, derived rather than transcribed ---------

sequence = "-".join(s["type"] for s in SLIDES)
grounds = [render_slide(i, s)[0] for i, s in enumerate(SLIDES, 1)]
manifest = {
    "slug": SLUG,
    "title": SPEC.get("title", SLUG),
    "cover": SPEC.get("cover", "?"),
    "cover_ground": grounds[0],
    "sequence": sequence,
    "distinct_types": len(set(s["type"] for s in SLIDES)),
    "inverted_slides": [i for i, g in enumerate(grounds, 1) if g == "ink"],
    "accent_uses": sum(len(re.findall(r"\[\[.+?\]\]", json.dumps(v, ensure_ascii=False)))
                       for v in [SPEC["slides"]]),
    "layout_log_line": f'| {SLUG} | {SPEC.get("cover", "?")} | {sequence} |',
}
json.dump(manifest, open(os.path.join(OUT, "deck.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

print(f"built {len([f for f in os.listdir(OUT) if f.endswith('.html')])} html files in {OUT}")
print(f"  cover {manifest['cover']} on {grounds[0]} · sequence {sequence} · "
      f"{manifest['distinct_types']} distinct types · inverted {manifest['inverted_slides']}")
print("  LAYOUT LOG:", manifest["layout_log_line"])

# ---- grid check: the cover is what shows in the Instagram grid ---------------

prev = None
for p in sorted(glob.glob(os.path.join(ROOT, "out", "*", "deck.json"))):
    try:
        d = json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        continue
    if d.get("slug") and d["slug"] < SLUG:
        prev = d
if prev:
    if prev.get("cover_ground") == grounds[0]:
        print(f"  ! grid: cover ground '{grounds[0]}' repeats {prev['slug']} — "
              f"alternate paper/ink so the grid doesn't read flat")
    if prev.get("cover") == manifest["cover"]:
        print(f"  ! grid: cover treatment '{manifest['cover']}' repeats {prev['slug']}")
