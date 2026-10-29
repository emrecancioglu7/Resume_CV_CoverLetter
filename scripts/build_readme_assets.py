#!/usr/bin/env python3
"""Generates the README's animated SVG artwork into assets/ (a dark and a light variant of each).

Run from the repo root after changing any text below:  python3 scripts/build_readme_assets.py
Same approach as the GitHub profile and AWS-Cloud-Resume READMEs: self-contained SVG (no external
fonts, images or services), CSS animations inside the SVG that switch off for viewers with
"reduce motion" enabled, and the same palette as emrecancioglu.com.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
MONO_CLASS = 'class="mono"'
SPACED = 'letter-spacing="3"'

PALETTES = {
    "dark": dict(bg1="#0a0d12", bg2="#0e1a18", card="#11161d", card_border="#1f2a33", grid="#1a2430",
                 text="#ececea", muted="#9aa3ab", accent="#34d399", accent2="#38bdf8", accent_soft="#34d39922",
                 paper="#f4f5f2", ink="#2a2f35", ink_soft="#c5cbc8"),
    "light": dict(bg1="#ffffff", bg2="#ecfdf5", card="#ffffff", card_border="#d7e3dd", grid="#e3ece8",
                  text="#17181a", muted="#5b6168", accent="#059669", accent2="#0284c7", accent_soft="#05966914",
                  paper="#ffffff", ink="#2a2f35", ink_soft="#d4dbd7"),
}

# Numbers come straight from the résumé (resume/*.tex); update them here when the CV changes.
STATS = [("9+", "YEARS EXPERIENCE", "YIL DENEYİM"), ("3", "MANUFACTURING PLANTS", "ÜRETİM TESİSİ"),
         ("4", "PUBLICATIONS", "YAYIN"), ("6", "AWARDS", "ÖDÜL")]
SECTIONS = ["summary", "skills", "experience", "honors", "presentation", "certification", "education"]

BASE_STYLE = """
    .fade { opacity: 0; animation: fade .7s ease-out forwards; }
    @keyframes fade { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
    .pulse { stroke-dasharray: 16 600; stroke-dashoffset: 616; animation: flow 2.4s linear infinite; }
    @keyframes flow { to { stroke-dashoffset: 0; } }
"""
REDUCED_MOTION = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } .fade { opacity: 1; } }"


def svg(width, height, body, style, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
            f'<style>text {{ font-family: {FONT}; }} .mono {{ font-family: {MONO}; }} {BASE_STYLE} {style} {REDUCED_MOTION}</style>'
            f'{body}</svg>')


def t(x, y, s, size, fill, weight=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'


def backdrop(p, w, h, glow_cx=0.8):
    return f'''
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p["bg1"]}"/><stop offset="1" stop-color="{p["bg2"]}"/></linearGradient>
      <radialGradient id="glow" cx="{glow_cx}" cy="0.5" r="0.5"><stop offset="0" stop-color="{p["accent"]}" stop-opacity="0.18"/><stop offset="1" stop-color="{p["accent"]}" stop-opacity="0"/></radialGradient>
      <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{p["grid"]}" stroke-width="1"/></pattern>
    </defs>
    <rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>
    <rect width="{w}" height="{h}" rx="18" fill="url(#grid)" opacity="0.5"/>
    <rect width="{w}" height="{h}" rx="18" fill="url(#glow)"/>
    <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" fill="none" stroke="{p["card_border"]}"/>'''


# ---------------------------------------------------------------- hero banner
def page(p, x, y, w, h, heading_w, lines, delay0, cls_extra=""):
    """A sheet of paper whose text lines 'write themselves' one after another."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{p["paper"]}" stroke="{p["card_border"]}" {cls_extra}/>',
           f'<rect x="{x + 22}" y="{y + 24}" width="{heading_w}" height="12" rx="3" fill="{p["ink"]}"/>',
           f'<rect x="{x + 22}" y="{y + 44}" width="{heading_w * 0.6:.0f}" height="6" rx="3" fill="{p["accent"]}"/>']
    for i, lw in enumerate(lines):
        ly = y + 72 + i * 16
        if lw == 0:  # section heading
            out.append(f'<rect x="{x + 22}" y="{ly - 3}" width="50" height="7" rx="2" fill="{p["accent"]}" opacity=".8"/>')
            continue
        out.append(f'<path d="M{x + 22} {ly}h{lw}" stroke="{p["ink_soft"]}" stroke-width="5" stroke-linecap="round" '
                   f'class="write" style="--len:{lw}px;stroke-dasharray:{lw} {lw};stroke-dashoffset:{lw};animation-delay:{delay0 + i * 0.18:.2f}s"/>')
    return "".join(out)


def hero(p):
    w, h = 1200, 380
    body = [backdrop(p, w, h),
            f'<g class="fade">{t(64, 100, "RÉSUMÉ & COVER LETTER · LaTeX", 15, p["accent"], 700, extra=SPACED)}</g>',
            f'<g class="fade" style="animation-delay:.15s">{t(62, 166, "Emre Çancıoğlu", 62, p["text"], 700)}</g>',
            f'<g class="fade" style="animation-delay:.3s">{t(64, 208, "Digitalization & AI Supervisor · Industrial Automation", 21, p["muted"])}</g>',
            f'<g class="fade" style="animation-delay:.45s">{t(64, 240, "Awesome-CV · XeLaTeX · one file per section", 18, p["muted"])}</g>']
    # EN / TR chip: the active language flips back and forth.
    body.append(f'''<g class="fade" style="animation-delay:.6s">
      <rect x="64" y="272" width="148" height="42" rx="21" fill="{p["accent_soft"]}" stroke="{p["accent"]}" stroke-opacity="0.5"/>
      <rect x="68" y="276" width="70" height="34" rx="17" fill="{p["accent"]}" class="knob"/>
      {t(103, 299, "EN", 15, p["text"], 700, "middle")}
      {t(173, 299, "TR", 15, p["text"], 700, "middle")}
    </g>''')
    body.append(f'''<g class="fade" style="animation-delay:.7s">
      <rect x="228" y="272" width="200" height="42" rx="21" fill="none" stroke="{p["card_border"]}"/>
      {t(328, 299, "résumé + cover letter", 15, p["muted"], 600, "middle")}
    </g>''')
    # Two sheets: the cover letter behind, the résumé in front writing itself.
    body.append(f'<g class="fade" style="animation-delay:.3s"><g class="float2">'
                f'{page(p, 790, 58, 230, 290, 110, [170, 180, 160, 0, 175, 150, 180, 120, 0, 170, 140], 0.6)}</g></g>')
    body.append(f'<g class="fade" style="animation-delay:.5s"><g class="float">'
                f'{page(p, 900, 40, 240, 300, 120, [190, 150, 0, 180, 196, 140, 0, 170, 186, 120, 160], 1.0)}'
                f'<rect x="1088" y="300" width="40" height="22" rx="5" fill="#dc2626"/>{t(1108, 315, "PDF", 11, "#ffffff", 800, "middle")}'
                f'</g></g>')
    style = """
    .write { animation: write .5s ease-out forwards; }
    @keyframes write { to { stroke-dashoffset: 0; } }
    .float { animation: float 5s ease-in-out infinite; }
    .float2 { animation: float 6s ease-in-out -2s infinite; }
    @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    .knob { animation: knob 6s ease-in-out infinite; }
    @keyframes knob { 0%,40% { transform: translateX(0); } 50%,90% { transform: translateX(70px); } 100% { transform: translateX(0); } }
    """
    return svg(w, h, "".join(body), style,
               "Emre Çancıoğlu: Digitalization & AI Supervisor. Bilingual (EN/TR) résumé and cover letter built with LaTeX and Awesome-CV")


# ---------------------------------------------------------------- stats
def stats(p):
    w, h = 1200, 150
    cw, gap = 286, 16
    out = []
    for i, (num, en, tr) in enumerate(STATS):
        x = i * (cw + gap) + 4
        out.append(f'''<g class="fade" style="animation-delay:{i * 0.15:.2f}s">
      <rect x="{x}" y="4" width="{cw}" height="{h - 8}" rx="14" fill="{p["card"]}" stroke="{p["card_border"]}" stroke-width="1.5"/>
      {t(x + cw / 2, 68, num, 44, p["accent"], 800, "middle")}
      <path d="M{x + cw / 2 - 30} 84h60" stroke="{p["accent"]}" stroke-width="3" stroke-linecap="round" class="under" style="animation-delay:{0.4 + i * 0.15:.2f}s"/>
      {t(x + cw / 2, 110, en, 13, p["text"], 700, "middle", 'letter-spacing="1.5"')}
      {t(x + cw / 2, 130, tr, 12, p["muted"], 500, "middle", 'letter-spacing="1.5"')}
    </g>''')
    style = """
    .under { stroke-dasharray: 60; stroke-dashoffset: 60; animation: under .8s ease-out forwards; }
    @keyframes under { to { stroke-dashoffset: 0; } }
    """
    return svg(w, h, "".join(out), style, " · ".join(f"{n} {en.lower()}" for n, en, _ in STATS))


# ---------------------------------------------------------------- build flow
def build(p):
    w, h = 1200, 400
    out = [backdrop(p, w, h, 0.6), t(48, 50, "HOW A PDF IS BUILT", 14, p["accent"], 700, extra=SPACED)]
    fx, fw, fh = 48, 220, 36
    top = 76
    hub_x, hub_y, hub_w, hub_h = 410, 168, 190, 72
    tex_x, pdf_x = 720, 990
    hub_mid = hub_y + hub_h / 2
    for i, name in enumerate(SECTIONS):
        y = top + i * 44
        mid = y + fh / 2
        d = f"M{fx + fw} {mid} C{fx + fw + 80} {mid}, {hub_x - 80} {hub_mid}, {hub_x} {hub_mid}"
        out.append(f'<path d="{d}" fill="none" stroke="{p["grid"]}" stroke-width="2"/>')
        out.append(f'<path d="{d}" fill="none" stroke="{p["accent"]}" stroke-width="2.5" stroke-linecap="round" class="pulse" style="animation-delay:{i * 0.3:.2f}s"/>')
        out.append(f'''<g class="fade" style="animation-delay:{i * 0.08:.2f}s">
      <rect x="{fx}" y="{y}" width="{fw}" height="{fh}" rx="8" fill="{p["card"]}" stroke="{p["card_border"]}"/>
      {t(fx + 16, y + 23, f"resume/{name}.tex", 13, p["text"], 500, extra=MONO_CLASS)}
    </g>''')

    def box(x, title, sub, color, delay, extra=""):
        return f'''<g class="fade" style="animation-delay:{delay:.2f}s">
      <rect x="{x}" y="{hub_y}" width="{hub_w}" height="{hub_h}" rx="12" fill="{p["card"]}" stroke="{color}" stroke-width="1.5"/>
      {extra}
      {t(x + hub_w / 2, hub_mid - 2, title, 17, p["text"], 700, "middle", MONO_CLASS)}
      {t(x + hub_w / 2, hub_mid + 20, sub, 12, p["muted"], 400, "middle")}
    </g>'''

    for x0, x1, d in [(hub_x + hub_w, tex_x, 0.6), (tex_x + hub_w, pdf_x, 1.2)]:
        path = f"M{x0} {hub_mid} H{x1}"
        out.append(f'<path d="{path}" fill="none" stroke="{p["grid"]}" stroke-width="2"/>'
                   f'<path d="{path}" fill="none" stroke="{p["accent2"]}" stroke-width="3" stroke-linecap="round" class="pulse" style="animation-delay:{d}s"/>')
    spinner = (f'<circle cx="{tex_x + hub_w - 22}" cy="{hub_y + 20}" r="8" fill="none" stroke="{p["accent2"]}" '
               f'stroke-width="2.5" stroke-dasharray="30 20" class="spin"/>')
    out.append(box(hub_x, "resume.tex", "entry point · EN / TR", p["accent"], .3))
    out.append(box(tex_x, "xelatex ×2", "custom fonts · references", p["accent2"], .5, spinner))
    out.append(box(pdf_x, "resume.pdf", "3 pages · ready to send", "#dc2626", .7,
                   f'<circle cx="{pdf_x + hub_w - 22}" cy="{hub_y + 20}" r="5" fill="#dc2626" class="blink"/>'))
    out.append(f'<g class="fade" style="animation-delay:.9s">{t(tex_x + hub_w / 2, hub_y + hub_h + 70, "Same flow for the cover letter: coverletter.tex → coverletter.pdf", 14, p["muted"], 500, "middle")}</g>')
    style = f"""
    .spin {{ transform-origin: {tex_x + hub_w - 22}px {hub_y + 20}px; animation: spin 1.2s linear infinite; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    .blink {{ animation: blink 1.6s ease-in-out infinite; }}
    @keyframes blink {{ 50% {{ fill-opacity: .2; }} }}
    """
    return svg(w, h, "".join(out), style,
               "Build: one .tex file per section (" + ", ".join(SECTIONS) + ") → resume.tex → xelatex twice → resume.pdf")


# ---------------------------------------------------------------- divider + footer
def divider(p):
    w, h = 1200, 24
    body = f'''<defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="{p["accent"]}" stop-opacity="0"/><stop offset=".5" stop-color="{p["accent"]}"/><stop offset="1" stop-color="{p["accent"]}" stop-opacity="0"/></linearGradient></defs>
    <rect x="0" y="11" width="{w}" height="2" fill="url(#d)" opacity=".5"/>
    <rect x="0" y="10" width="120" height="4" rx="2" fill="{p["accent2"]}" class="glint"/>'''
    style = """.glint { opacity: .8; animation: glint 4s ease-in-out infinite; }
    @keyframes glint { from { transform: translateX(-120px); } to { transform: translateX(1200px); } }"""
    return svg(w, h, body, style, "")


def footer(p):
    w, h = 1200, 120
    body = f'''<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{p["accent"]}"/><stop offset="1" stop-color="{p["accent2"]}"/></linearGradient></defs>
    <path class="wave" d="M0,60 C200,10 400,110 600,60 C800,10 1000,110 1200,60 L1240,120 L-40,120Z" fill="url(#g)" opacity="0.18"/>
    <path class="wave2" d="M0,80 C200,40 400,120 600,80 C800,40 1000,120 1200,80 L1240,120 L-40,120Z" fill="url(#g)" opacity="0.12"/>
    {t(600, 52, "Typeset with XeLaTeX · Awesome-CV · emrecancioglu.com", 15, p["muted"], 500, "middle")}'''
    style = """.wave { animation: sway 6s ease-in-out infinite alternate; }
    .wave2 { animation: sway 8s ease-in-out infinite alternate-reverse; }
    @keyframes sway { to { transform: translateX(-40px); } }"""
    return svg(w, h, body, style, "Typeset with XeLaTeX and Awesome-CV — emrecancioglu.com")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("hero", hero), ("stats", stats), ("build", build), ("divider", divider), ("footer", footer)]:
        for mode, p in PALETTES.items():
            (OUT / f"{name}-{mode}.svg").write_text(fn(p), encoding="utf-8")
    print(f"wrote {len(PALETTES) * 5} files to {OUT}")


if __name__ == "__main__":
    main()
