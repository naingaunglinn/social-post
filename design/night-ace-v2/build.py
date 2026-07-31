#!/usr/bin/env python3
"""Night Ace v4 slide builder — one renderer per slide type (A/B/C/D/E/G/I),
plus dedicated landscape hero compositions. Emits standalone HTML into out/."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "out")
os.makedirs(OUT, exist_ok=True)

PAPER, INK, BLUE, GRAPHITE, TRACK = "#F5F5F5", "#141419", "#2E6BFF", "#55555C", "#DFDFE4"

CSS_BASE = f"""
@font-face {{ font-family:'Archivo VF'; src:url('file://{FONTS}/Archivo.ttf'); font-weight:100 1000; }}
@font-face {{ font-family:'Plex VF'; src:url('file://{FONTS}/IBMPlexSans.ttf'); font-weight:100 1000; }}
@font-face {{ font-family:'Plex Mono'; src:url('file://{FONTS}/IBMPlexMono-Regular.ttf'); font-weight:400; }}
@font-face {{ font-family:'Plex Mono'; src:url('file://{FONTS}/IBMPlexMono-Medium.ttf'); font-weight:500; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:100%; height:100%; }}
body {{ font-family:'Plex VF',sans-serif; -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility; }}
.slide {{ display:flex; flex-direction:column; overflow:hidden; }}
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

def page(idx, total, ground, inner, W, H, PAD, mono_px):
    css = CSS_BASE + f".slide {{ width:{W}px; height:{H}px; padding:{PAD}px; }}"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body><div class="slide {ground}">
  <div class="hdr">
    <span class="mono wordmark" style="font-size:{mono_px}px">NIGHT&nbsp;ACE</span>
    <span class="mono pageno" style="font-size:{mono_px}px">{idx:02d} — {total:02d}</span>
  </div>
{inner}</div></body></html>"""

def bar(idx, total, mt):
    fill = round(idx / max(total, 1) * 100, 2)
    return f'<div class="bar" style="margin-top:{mt}px"><i style="width:{fill}%"></i></div>'

# ---- slide type renderers (portrait 1080×1350, PAD 96) ---------------------

def type_A(idx, total, s):  # hero word, bottom-anchored
    inner = (
        f'<div class="hero" style="font-size:{s["gpx"]}px;margin-top:auto">{s["giant"]}</div>'
        f'<div class="title" style="font-size:{s.get("tpx",66)}px;max-width:860px;margin-top:52px">{s["title"]}</div>'
        + bar(idx, total, 44)
        + f'<div class="body" style="font-size:32px;max-width:780px;margin-top:44px">{s["body"]}</div>')
    return "paper", inner

def type_B(idx, total, s):  # full-bleed statement, top-anchored
    inner = (
        f'<div class="statement" style="font-size:{s.get("spx",100)}px;margin-top:120px">{s["statement"]}</div>'
        + bar(idx, total, 48)
        + (f'<div class="body" style="font-size:32px;max-width:780px;margin-top:40px">{s["tail"]}</div>' if s.get("tail") else ""))
    return "paper", inner

def type_C(idx, total, s):  # numbered stack
    rows = "".join(
        f'<div class="row" style="margin-top:{0 if i == 0 else 44}px">'
        f'<div class="num" style="font-size:26px;width:110px">{i + 1:02d}</div>'
        f'<div class="item" style="font-size:40px">{it}</div></div>'
        for i, it in enumerate(s["items"]))
    inner = (
        f'<div class="title" style="font-size:66px;max-width:860px;margin-top:120px">{s["title"]}</div>'
        + bar(idx, total, 40)
        + f'<div style="margin-top:64px">{rows}</div>')
    return "paper", inner

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
    inner = (
        f'<div class="title" style="font-size:66px;max-width:860px;margin-top:120px">{s["title"]}</div>'
        + bar(idx, total, 40)
        + f'<div style="margin-top:72px">{rows}</div>')
    return "paper", inner

def type_I(idx, total, s):  # pull quote, centered; bar at bottom
    inner = (
        f'<div class="quote" style="font-size:60px;max-width:840px;margin-top:auto">{s["quote"]}</div>'
        + bar(idx, total, 0).replace('margin-top:0px', 'margin-top:auto'))
    return "paper", inner

RENDERERS = {"A": type_A, "B": type_B, "C": type_C, "D": type_D, "E": type_E, "G": type_G, "I": type_I}

# ---- deck: Claude Code orchestration step (seq B-A-G-C-D-E-I-B) ------------

SLIDES = [
    dict(type="B", spx=112,
         statement=f'Stop<br>prompting.<br>Start<br>orchestrating{B(".")}',
         tail="The step that turns Claude Code from a fast assistant into an engineering process."),
    dict(type="A", giant=f"solo{B('.')}", gpx=260,
         title="One context is<br>one opinion",
         body="A single agent writes the code, then grades its own work. It defends its first idea to the end of the context window — the same trap that makes authors bad reviewers of their own code."),
    dict(type="G", title="What the orchestration<br>step looks like",
         rows=[("SCOUT", "→  map the codebase in parallel"),
               ("FAN OUT", "→  one agent per concern"),
               ("VERIFY", "→  skeptics refute each finding"),
               ("MERGE", "→  one ranked synthesis")]),
    dict(type="C", title="When to reach for it",
         items=["The work outgrows one context", "Findings need independent checks",
                "The task splits along clean seams", "Being wrong is expensive"]),
    dict(type="D", titleL="Orchestrate", titleR="Stay solo",
         itemsL=["Codebase audits", "Wide migrations", "Adversarial review", "Research sweeps"],
         itemsR=["One-file fixes", "Quick questions", "Exploration", "Anything cheap to redo"]),
    dict(type="E", spx=100,
         statement=f'Orchestration<br>isn\'t speed.<br>It\'s doubt{B(".")}',
         sub="Parallel agents don't just finish sooner. They disagree — and the disagreement is the signal."),
    dict(type="I", quote="“An agent reviewing its own work is one opinion counted twice.”"),
    dict(type="B", spx=100,
         statement=f'Ship the process,<br>not the prompt{B(".")}',
         tail="Want the full Night Ace orchestra for Claude Code — agents, commands, and the playbook? Comment “ACE” and we'll send you the package."),
]

for i, s in enumerate(SLIDES, 1):
    ground, inner = RENDERERS[s["type"]](i, len(SLIDES), s)
    open(os.path.join(OUT, f"slide-{i:02d}.html"), "w").write(
        page(i, len(SLIDES), ground, inner, 1080, 1350, 96, 22))

# ---- landscape heroes: own composition, full width, type scales up ---------

def hero(name, W, H, PAD, spx, sub_px, mono_px, bar_mt, sub_mt):
    statement = f'Stop prompting.<br>Start orchestrating{B(".")}'
    inner = (
        f'<div style="margin-top:auto"></div>'
        f'<div class="statement" style="font-size:{spx}px">{statement}</div>'
        + bar(1, 8, bar_mt)
        + f'<div class="body" style="font-size:{sub_px}px;margin-top:{sub_mt}px">The orchestration step that turns Claude Code into an engineering process</div>'
        + f'<div style="margin-bottom:auto"></div>')
    open(os.path.join(OUT, name), "w").write(page(1, 8, "ink", inner, W, H, PAD, mono_px))

hero("hero-fb.html", 1200, 630, 64, 66, 24, 16, 32, 24)
hero("hero-x.html", 1920, 1080, 96, 104, 32, 22, 44, 32)
print("built", len([f for f in os.listdir(OUT) if f.endswith('.html')]), "html files in", OUT)
