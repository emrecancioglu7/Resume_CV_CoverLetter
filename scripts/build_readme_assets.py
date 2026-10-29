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
REDUCED_MOTION = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } .fade { opacity: 1; } .write { stroke-dashoffset: 0 !important; } .stamp { opacity: 1; } }"


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



# ---------------------------------------------------------------- badges
# Badges are generated here too instead of linking img.shields.io: GitHub's image proxy (camo)
# regularly times out on shields.io (HTTP 504), which shows up as broken images in the README.
# Brand icon paths are from Simple Icons (CC0, simpleicons.org), 24x24 viewBox.
BADGE_FONT = "Verdana, 'DejaVu Sans', Geneva, sans-serif"


def text_width(s, size=11):
    """Rough Verdana advance widths; the text is then forced to this width with textLength."""
    w = 0.0
    for ch in s:
        if ch in "il.,:;|!'·":
            w += 0.33
        elif ch == " ":
            w += 0.35
        elif ch in "mwMW":
            w += 0.95
        elif ch.isupper() or ch.isdigit():
            w += 0.72
        else:
            w += 0.6
    return w * size


def badge(label, value, color, icon=None, label_color="#24292f"):
    h, pad, size = 28, 10, 11
    icon_w = 20 if icon else 0
    segs = []  # (x, width, fill, text)
    x = 0
    if label:
        lw = pad + icon_w + text_width(label) + pad
        segs.append((x, lw, label_color, label))
        x += lw
    vw = (0 if label else icon_w) + pad + text_width(value) + pad
    segs.append((x, vw, color, value))
    w = x + vw
    parts = []
    for i, (sx, sw, fill, text) in enumerate(segs):
        parts.append(f'<rect x="{sx:.1f}" width="{sw:.1f}" height="{h}" fill="{fill}"/>')
        tx = sx + pad + (icon_w if i == 0 else 0)
        tw = text_width(text)
        parts.append(f'<text x="{tx:.1f}" y="18.5" font-size="{size}" font-weight="600" fill="#ffffff" '
                     f'textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{escape(text)}</text>')
    if icon:
        parts.append(f'<svg x="{pad}" y="7" width="14" height="14" viewBox="0 0 24 24"><path fill="#ffffff" d="{ICONS[icon]}"/></svg>')
    alt = f"{label}: {value}" if label else value
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h}" viewBox="0 0 {w:.1f} {h}" role="img" aria-label="{escape(alt)}">'
            f'<title>{escape(alt)}</title><style>text {{ font-family: {BADGE_FONT}; letter-spacing: .2px; }}</style>'
            f'<clipPath id="r"><rect width="{w:.1f}" height="{h}" rx="6"/></clipPath><g clip-path="url(#r)">{"".join(parts)}</g></svg>')


ICONS = {
    "latex": "M2.176 2.814c.233.42.476.78.73 1.09.247-.013 1.132.456 1.312.523.508.282 1.063.63 1.567.966.505.337.96.662 1.272.9.156.12.278.218.352.286a.483.483 0 01.078.082.08.08 0 01.01.021.06.06 0 01-.004.047.057.057 0 01-.04.03.077.077 0 01-.028 0c-.057 0-.203-.163-.497-.415a23.474 23.474 0 00-2.759-1.827c-.504-.28-.956-.542-1.264-.613a2.322 2.322 0 00-.36-.025 2.706 2.706 0 00-.788.133c.494.414.91.716 1.28.949-.57-.182-1.182-.21-1.902.133.526.329.967.567 1.354.745 1.103.156 2.258.696 3.224 1.309.483.307.904.615 1.219.867.157.125.29.237.39.328.098.091.174.154.197.21.03.073-.019.104-.084.058-.032-.022-.088-.102-.184-.191a7.35 7.35 0 00-.384-.327c-.312-.25-.729-.552-1.209-.857-.893-.562-2.232-1.013-3.173-1.397-.602-.11-1.225-.06-1.906.39.449.2.837.349 1.182.463.812 0 1.892.365 2.935.922 1.042.556 2.04 1.214 2.523 1.774.066.077-.016.126-.074.07-.52-.495-1.463-1.204-2.498-1.756-.639-.337-2.153-1.01-2.886-1.01l.004.002c-.567.02-1.13.195-1.679.716.477.118.885.196 1.244.249-.44.088-.87.3-1.289.722.324.07.616.122.882.162-.328.159-.639.404-.923.78.373.03.703.042 1 .044-.36.166-.696.43-.996.85.533.027.98.025 1.364.003-.422.172-.812.464-1.145.968.662.01 1.188-.022 1.628-.076l-.006.002c.99-.073 2.297.127 2.962.847.052.057-.024.118-.072.074-.648-.58-1.493-.827-2.89-.921h-.002c-.543.149-1.046.446-1.46 1.074.536.008.982-.013 1.366-.05-.469.257-.873.644-1.139 1.306.483-.092.888-.19 1.237-.292-.363.265-.668.636-.873 1.194.324-.072.612-.146.871-.221a2.519 2.519 0 00-.513 1.095c.352-.13.655-.254.926-.377-.257.3-.453.681-.55 1.19.495-.199.899-.388 1.238-.568-.31.333-.543.76-.635 1.356a11.816 11.816 0 001.442-.744c-.433.362-.764.843-.879 1.587.788-.348 1.339-.663 1.767-.955-.184.372-.282.806-.235 1.348.762-.584 1.243-1.056 1.602-1.473-.024.269-.003.56.077.884.546-.939 1.089-1.212 1.65-1.526-.895.451-.762.79-.762 1.184.683-.72 1.635-1.482 1.927-1.96-.39.585-.547 1.14-.65 1.63-1.993 1.054-3.207 1.329-4.568 1.75.528.194 1.093.383.859.652l-.624.622c.399-.124.805-.3 1.158-.059-.035.327-.447.492-.8.683.621-.224.756-.172.92-.12.081.393-.203.603-.388.862 1.565-1.19 3.606-2.13 5.044-2.522 2.022-.681 4.63-1.389 5.339-3.115l.712-2.847-.004.004c-.111-.034-.246-.063-.35-.133a.651.651 0 01-.235-.297c-.252.065-.44.03-.56-.088-.117-.117-.167-.296-.203-.491-.203.041-.362.016-.467-.077-.116-.101-.17-.26-.198-.444l-.008-.039.037-.015a.842.842 0 00.302-.194.257.257 0 00.07-.225l-.006-.037.03-.016c.163-.093.345-.169.428-.28a.274.274 0 00.053-.21.88.88 0 00-.155-.357l-.027-.04.04-.027c.118-.09.244-.179.308-.26.032-.04.048-.076.047-.11 0-.033-.015-.07-.064-.117l-.098-.094.135.006c.213.01.395-.007.538-.053a.504.504 0 00.274-.197c-.007-.033-.02-.063-.02-.098a.484.484 0 01.967 0c0 .044-.015.084-.026.125.177.014.347.01.507-.06l.002.001.035-.013c.236-.085.334.045.72-.456-1.69-2.19-4.157-.635-4.977 1.622-.21.576-1.405.578-1.751 0-1.37-2.95-5.53-6.068-9.07-7.218zm.86 2.145c.906.293 1.913.782 2.77 1.328.43.273.813.543 1.114.779.301.236.566.473.62.575.054.102 0 .14-.082.06-.081-.078-.303-.32-.6-.553-.298-.234-.68-.505-1.106-.777-.775-.49-1.982-.958-2.716-1.412zm-1.7 2.7c1.116.014 2.35.447 3.434.997.541.275 1.023.567 1.395.83.372.263.672.524.734.657.061.134-.02.13-.087.055a4.401 4.401 0 00-.704-.626 11.47 11.47 0 00-1.385-.826C3.76 8.264 2.439 7.82 1.336 7.66zm14.916.772a.381.381 0 100 .762.381.381 0 000-.762zM1.7 8.478c.822.072 1.72.368 2.534.75 1.086.509 2.035 1.158 2.434 1.667.035.045-.014.131-.08.062-.428-.44-1.322-1.131-2.397-1.635-.913-.421-2.282-.87-3.262-.78.251-.03.497-.088.771-.064zm16.339.01c-.366.475-.53.423-.703.464.094.43.35.586.585.77l-.06.012c2.315-.447 4.186-.286 6.139-.236l-5.961-1.01zm-.178 1.246h-.002l-.004.016.006-.016zm-.625-.757c-.183.074-.373.076-.563.059a.477.477 0 01-.42.26.483.483 0 01-.435-.278.609.609 0 01-.274.188c-.139.045-.308.057-.493.055.02.035.054.068.055.104a.273.273 0 01-.069.174c-.073.092-.189.17-.295.248.087.141.137.26.149.362a.39.39 0 01-.07.284c-.106.14-.288.21-.439.293a.374.374 0 01-.09.268.89.89 0 01-.297.198c.027.156.074.283.154.354.086.076.211.103.425.047l.055-.014.01.055c.033.207.088.385.187.483.1.099.244.135.503.055l.049-.015.016.048c.05.142.12.223.209.282.087.06.247.112.358.147.798-.869 1.525-1.772 1.884-2.86-.225-.177-.506-.338-.609-.797zm-16.23.386c1.165-.08 2.283.196 3.202.626.92.43 1.658.939 1.974 1.307.075.087-.019.12-.072.072a8.187 8.187 0 00-1.947-1.29c-.904-.414-2.193-.644-3.157-.715zm.864.802c.61.02 1.24.155 1.806.352.756.262 1.421.614 1.747.98.045.05-.007.127-.074.069-.349-.304-.961-.693-1.706-.951-.574-.195-1.613-.369-2.268-.397.197-.022.292-.06.495-.053zm1.05 1.788c.423.034.886.133 1.341.407.043.026.049.136-.049.09-.856-.402-1.326-.49-2.457-.31.386-.128.74-.221 1.164-.187zm-.04.788c.4-.035.784-.002 1.297.204.044.018.08.126-.033.094-.857-.243-1.167-.328-2.287.104.28-.229.622-.366 1.023-.402zm1.285.687c.317-.023.635-.026.934.006.052.006.055.105-.006.102a7.87 7.87 0 00-1.837.115c-.243.046-.423.043-1.405.458.287-.233.794-.452 1.385-.56a8.91 8.91 0 01.93-.12zm1.28.49c.099.003.062.104.006.103-.728-.01-1.304.132-1.875.295a9.78 9.78 0 00-1.318.525c.283-.23.713-.457 1.291-.622.579-.166 1.248-.326 1.896-.302zm.528.398c.036-.005.105.084.018.1-.73.137-1.244.267-1.794.454-.216.074-.58.207-1.243.587.26-.269.656-.492 1.213-.68.558-.19 1.196-.37 1.806-.46zm.311.507c.075-.012.097.087.02.102-1.217.241-1.76.556-2.54 1.144.504-.523 1.297-1.051 2.52-1.246zm.595.448c.087-.013.11.087.021.1-.872.13-1.477.553-2.255 1.33.295-.493 1.004-1.24 2.234-1.43zm.372.39c.046-.006.114.073.023.1a2.634 2.634 0 00-.669.3c-.182.118-.3.2-.597.507.111-.245.296-.434.542-.59.247-.157.509-.293.7-.317z",
    "pdf": "M6 2h8l6 6v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm7 1.5V9h5.5zM8 13h8v1.6H8zm0 3.4h8V18H8z",
}

BADGES = [  # file name, label, value, color, icon
    ("resume-pdf", "Resume", "PDF", "#dc2626", "pdf"),
    ("ozgecmis-pdf", "Özgeçmiş", "PDF", "#dc2626", "pdf"),
    ("website", None, "emrecancioglu.com", "#059669", None),
    ("latex", "LaTeX", "XeTeX", "#008080", "latex"),
    ("template", "template", "Awesome-CV", "#0395de", None),
    ("languages", "languages", "EN | TR", "#059669", None),
    ("license", "license", "MIT", "#0284c7", None),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("hero", hero), ("stats", stats), ("build", build), ("divider", divider), ("footer", footer)]:
        for mode, p in PALETTES.items():
            (OUT / f"{name}-{mode}.svg").write_text(fn(p), encoding="utf-8")
    badge_dir = OUT / "badges"
    badge_dir.mkdir(exist_ok=True)
    for name, label, value, color, icon in BADGES:
        (badge_dir / f"{name}.svg").write_text(badge(label, value, color, icon), encoding="utf-8")
    print(f"wrote {len(PALETTES) * 5} files to {OUT} and {len(BADGES)} badges to {badge_dir}")


if __name__ == "__main__":
    main()
