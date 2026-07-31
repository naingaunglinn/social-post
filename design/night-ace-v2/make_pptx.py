#!/usr/bin/env python3
"""Hand-rolled OOXML PPTX of the Night Ace carousel (no external deps).
v5: fully generic — consumes render.js's metrics/<slug>.json dump (text runs,
fonts, colors, shapes, page ground), so every slide type renders without bespoke
code. Writes the Canva twin next to the deck it came from.
Font names map to Canva's library (Archivo Black / Archivo / IBM Plex Sans / IBM Plex Mono).

    python3 make_pptx.py             # newest metrics/ dump
    python3 make_pptx.py <slug>
"""
import glob, json, os, sys, zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
METRICS_DIR = os.path.join(ROOT, "metrics")

def resolve_slug(arg=None):
    if arg:
        return arg[:-5] if arg.endswith(".json") else arg
    found = sorted(glob.glob(os.path.join(METRICS_DIR, "*.json")))
    if not found:
        sys.exit(f"no metrics in {METRICS_DIR}/ — run render.js first")
    slug = os.path.basename(found[-1])[:-5]
    print("no slug given — using newest metrics:", slug)
    return slug

SLUG = resolve_slug(sys.argv[1] if len(sys.argv) > 1 else None)
MPATH = os.path.join(METRICS_DIR, SLUG + ".json")
if not os.path.exists(MPATH):
    avail = ", ".join(sorted(os.path.basename(p)[:-5]
                             for p in glob.glob(os.path.join(METRICS_DIR, "*.json"))))
    sys.exit(f"no metrics at {MPATH}\navailable: {avail or '(none)'}")
M = json.load(open(MPATH, encoding="utf-8"))
SLIDE_KEYS = sorted(k for k in M if k.startswith("slide-"))
N = len(SLIDE_KEYS)
W, H = 1080, 1350
EMU = lambda px: int(round(px * 9525))
SZ = lambda px: int(round(px * 72))  # px -> hundredths of a point (0.72 pt/px)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def font_map(family, weight):
    fam = family.lower()
    if "archivo" in fam:
        return ("Archivo Black", 0) if weight >= 850 else ("Archivo", 1)
    if "mono" in fam:
        return ("IBM Plex Mono", 1 if weight >= 450 else 0)
    return ("IBM Plex Sans", 1 if weight >= 500 else 0)

def text_sp(sid, t):
    typeface, bold = font_map(t["family"], t["weight"])
    sz = SZ(t["fs"])
    spc = int(round(t["ls"] * 72))
    ln = int(round(t["lh"] / t["fs"] * 100000))
    algn = {"right": "r", "end": "r", "center": "ctr"}.get(t["align"], "l")
    paras, cur = [], []
    for r in t["runs"]:
        if r.get("br"):
            paras.append(cur); cur = []
        else:
            cur.append(r)
    paras.append(cur)
    pxml = ""
    for para in paras:
        rs = "".join(
            f'<a:r><a:rPr lang="en-US" sz="{sz}" b="{bold}" spc="{spc}" dirty="0">'
            f'<a:solidFill><a:srgbClr val="{r["c"].lstrip("#").upper()}"/></a:solidFill>'
            f'<a:latin typeface="{typeface}"/><a:cs typeface="{typeface}"/></a:rPr>'
            f'<a:t>{esc(r["t"])}</a:t></a:r>'
            for r in para if r.get("t"))
        pxml += f'<a:p><a:pPr algn="{algn}"><a:lnSpc><a:spcPct val="{ln}"/></a:lnSpc></a:pPr>{rs}</a:p>'
    x, y = EMU(t["x"]), EMU(t["y"])
    w, h = EMU(t["w"] + 48), EMU(t["h"] + 8)
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="text{sid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:noAutofit/></a:bodyPr>'
            f'<a:lstStyle/>{pxml}</p:txBody></p:sp>')

def shape_sp(sid, s):
    x, y, w, h = EMU(s["x"]), EMU(s["y"]), EMU(max(s["w"], 0.5)), EMU(max(s["h"], 0.5))
    color = s["color"].lstrip("#").upper()
    geom = ('<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 50000"/></a:avLst></a:prstGeom>'
            if s.get("radius", 0) > 0 else '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="shape{sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>{geom}'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>')

def slide_xml(key):
    m = M[key]
    bg = m["bg"].lstrip("#").upper()
    sid = 2
    shapes = []
    for s in m["shapes"]:
        sid += 1
        shapes.append(shape_sp(sid, s))
    for t in m["texts"]:
        sid += 1
        shapes.append(text_sp(sid, t))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            f'<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="{bg}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>'
            '<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
            '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            + "".join(shapes) + '</p:spTree></p:cSld><p:clrMapOvr><a:overrideClrMapping bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" '
            'accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" '
            'hlink="hlink" folHlink="folHlink"/></p:clrMapOvr></p:sld>')

INK, BLUE, GRAPHITE, TRACK, PAPER = "141419", "2E6BFF", "55555C", "DFDFE4", "F5F5F5"

THEME = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
 '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="NightAce">'
 '<a:themeElements><a:clrScheme name="NightAce">'
 f'<a:dk1><a:srgbClr val="{INK}"/></a:dk1><a:lt1><a:srgbClr val="{PAPER}"/></a:lt1>'
 f'<a:dk2><a:srgbClr val="{GRAPHITE}"/></a:dk2><a:lt2><a:srgbClr val="{TRACK}"/></a:lt2>'
 f'<a:accent1><a:srgbClr val="{BLUE}"/></a:accent1><a:accent2><a:srgbClr val="{BLUE}"/></a:accent2>'
 f'<a:accent3><a:srgbClr val="{BLUE}"/></a:accent3><a:accent4><a:srgbClr val="{BLUE}"/></a:accent4>'
 f'<a:accent5><a:srgbClr val="{BLUE}"/></a:accent5><a:accent6><a:srgbClr val="{BLUE}"/></a:accent6>'
 f'<a:hlink><a:srgbClr val="{BLUE}"/></a:hlink><a:folHlink><a:srgbClr val="7C5CFF"/></a:folHlink></a:clrScheme>'
 '<a:fontScheme name="NightAce"><a:majorFont><a:latin typeface="Archivo Black"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
 '<a:minorFont><a:latin typeface="IBM Plex Sans"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>'
 '<a:fmtScheme name="Office"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
 '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
 '<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
 '<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
 '<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
 '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle>'
 '<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
 '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
 '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>')

MASTER = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
 '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
 f'<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="{PAPER}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>'
 '<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
 '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
 '</p:spTree></p:cSld>'
 '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" '
 'accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
 '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>')

LAYOUT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
 '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank">'
 '<p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
 '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
 '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')

def build(path):
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
          '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
          '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
          '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          + "".join(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' for i in range(1, N + 1))
          + '</Types>')
    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
                 '</Relationships>')
    pres = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
            '<p:sldIdLst>' + "".join(f'<p:sldId id="{255 + i}" r:id="rId{i + 1}"/>' for i in range(1, N + 1)) + '</p:sldIdLst>'
            f'<p:sldSz cx="{EMU(W)}" cy="{EMU(H)}"/><p:notesSz cx="{EMU(W)}" cy="{EMU(H)}"/></p:presentation>')
    pres_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
                 + "".join(f'<Relationship Id="rId{i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>' for i in range(1, N + 1))
                 + '</Relationships>')
    master_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
                   '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>'
                   '</Relationships>')
    layout_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
                   '</Relationships>')
    slide_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
                  '</Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("ppt/presentation.xml", pres)
        z.writestr("ppt/_rels/presentation.xml.rels", pres_rels)
        z.writestr("ppt/slideMasters/slideMaster1.xml", MASTER)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", master_rels)
        z.writestr("ppt/slideLayouts/slideLayout1.xml", LAYOUT)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", layout_rels)
        z.writestr("ppt/theme/theme1.xml", THEME)
        for i, key in enumerate(SLIDE_KEYS, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xml(key))
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels)
    print("wrote", path, os.path.getsize(path), "bytes,", N, "slides")

build(os.path.join(ROOT, "out", SLUG, SLUG + ".pptx"))
