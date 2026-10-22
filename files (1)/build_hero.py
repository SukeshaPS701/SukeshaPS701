"""
Builds assets/profile-hero-dark.svg (animated terminal-style profile hero).

Usage:
    python build_hero.py                 # placeholder portrait
    python build_hero.py --photo me.jpg  # your photo, auto-converted to a dithered portrait
Needs Pillow only when --photo is used:  pip install pillow
Edit the LINES list below to change the text.
"""
import argparse, base64, io, os

W, H = 1200, 500
ACCENT, ACCENT2 = "#2dd4bf", "#8b5cf6"
CHAR_W = 9.0          # approx width of one monospace char at 15px
TYPE_SPEED = 0.028    # seconds per character

# (text, style)   style: cmd | title | tag | item | dim
LINES = [
    ("> identity.loaded", "cmd"),
    ("$ whoami", "dim"),
    ("@SukeshaPS701 // AI & ML STUDENT", "title"),
    ("[ PROFILE ]", "tag"),
    ("+ location  : puttur, karnataka, india", "item"),
    ("+ education : bca - artificial intelligence & machine learning", "item"),
    ("+ focus     : machine learning + ai agents", "item"),
    ("+ github    : github.com/SukeshaPS701", "item"),
    ("[ STACK ]", "tag"),
    ("{ Python | Jupyter Notebook | Machine Learning }", "item"),
    ("[ BUILDING ]", "tag"),
    ("{ churn analysis | spam detection | music recommender | face detection }", "item"),
]

STYLE = {
    "cmd":   ('#e6edf3', 'font-weight="700"'),
    "dim":   ('#7d8590', ''),
    "title": ('#ffffff', 'font-weight="700" font-size="16"'),
    "tag":   (ACCENT,    ''),
    "item":  ('#e6edf3', ''),
}

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def portrait_image(path):
    from PIL import Image, ImageOps
    w, h = 300, 300
    img = ImageOps.fit(Image.open(path).convert("L"), (w, h), Image.LANCZOS, centering=(0.5, 0.35))
    img = ImageOps.autocontrast(img, cutoff=2)
    img = img.convert("1")                       # Floyd-Steinberg dither
    img = ImageOps.invert(img.convert("L")).convert("1")
    # white dots on transparent background
    rgba = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px, src = rgba.load(), img.load()
    for y in range(h):
        for x in range(w):
            if src[x, y]:
                px[x, y] = (230, 237, 243, 255)
    buf = io.BytesIO(); rgba.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()

def build(photo=None):
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Sukesha PS - AI and ML student, animated profile banner">')
    a(f'''<defs>
  <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT2}"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0" r="1">
    <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.10"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="#ffffff" stroke-opacity="0.035"/>
  </pattern>
  <clipPath id="imgclip"><rect x="62" y="150" width="268" height="268" rx="10"/></clipPath>''')
    # typing clip rects
    t = 1.0
    y0, dy = 150, 24
    clips, texts = [], []
    for i, (txt, st) in enumerate(LINES):
        n = len(txt)
        dur = max(0.25, n * TYPE_SPEED)
        steps = n + 1
        vals = ";".join(str(round(k * CHAR_W)) for k in range(steps)) + ";820"
        y = y0 + i * dy
        clips.append(
            f'<clipPath id="c{i}"><rect x="412" y="{y-18}" width="0" height="26">'
            f'<animate attributeName="width" values="{vals}" dur="{dur:.2f}s" begin="{t:.2f}s" calcMode="discrete" fill="freeze"/>'
            f'</rect></clipPath>')
        color, extra = STYLE[st]
        texts.append(f'<text x="412" y="{y}" fill="{color}" {extra} clip-path="url(#c{i})">{esc(txt)}</text>')
        if st == "title":
            ul = (f'<rect x="412" y="{y+8}" width="0" height="2" fill="{ACCENT}">'
                  f'<animate attributeName="width" from="0" to="{round(n*9.6)}" dur="0.5s" begin="{t+dur:.2f}s" fill="freeze"/></rect>')
            texts.append(ul)
        t += dur + 0.12
    a("\n  ".join(clips))
    a('</defs>')
    a('''<style>
  text{font-family:'JetBrains Mono','Fira Code',ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',monospace;font-size:15px}
  .cap{font-size:12px;fill:#7d8590}
  .cursor{animation:blink 1s steps(1) infinite}
  @keyframes blink{50%{opacity:0}}
  .dot{animation:pulse 2.4s ease-in-out infinite}
  @keyframes pulse{50%{opacity:.45}}
</style>''')
    # panel
    a(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28" fill="#0b0f14" stroke="url(#rim)" stroke-opacity="0.55" stroke-width="2"/>')
    a(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28" fill="url(#grid)"/>')
    a(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28" fill="url(#glow)"/>')
    # left window
    a('<rect x="30" y="30" width="330" height="440" rx="20" fill="#10161d" stroke="#ffffff" stroke-opacity="0.07"/>')
    a('<rect x="46" y="46" width="64" height="22" rx="11" fill="#06090d"/>')
    for cx, c in ((60, "#ff5f57"), (78, "#febc2e"), (96, "#28c840")):
        a(f'<circle cx="{cx}" cy="57" r="4.5" fill="{c}" class="dot"/>')
    a('<text class="cap" x="62" y="120">/portrait/sukesha.jpg</text>')
    a(f'<rect x="61" y="149" width="270" height="270" rx="11" fill="#06090d" stroke="url(#rim)" stroke-width="1.5"/>')
    if photo:
        a(f'<image x="62" y="150" width="268" height="268" preserveAspectRatio="xMidYMid slice" clip-path="url(#imgclip)" href="data:image/png;base64,{photo}"/>')
    else:
        a('<g clip-path="url(#imgclip)">')
        a(f'<rect x="62" y="150" width="268" height="268" fill="{ACCENT}" fill-opacity="0.05"/>')
        a(f'<text x="196" y="302" text-anchor="middle" fill="{ACCENT}" font-size="56" font-weight="700">SPS</text>')
        a('<text x="196" y="332" text-anchor="middle" fill="#7d8590" font-size="12">run: python build_hero.py --photo me.jpg</text>')
        a('</g>')
    a('<line x1="82" y1="445" x2="310" y2="445" stroke="#ffffff" stroke-opacity="0.12"/>')
    # right window
    a('<rect x="390" y="30" width="780" height="440" rx="20" fill="#10161d" stroke="#ffffff" stroke-opacity="0.07"/>')
    a('<rect x="410" y="50" width="740" height="44" rx="12" fill="#06090d"/>')
    for cx, c in ((432, "#ff5f57"), (452, "#febc2e"), (472, "#28c840")):
        a(f'<circle cx="{cx}" cy="72" r="5" fill="{c}" class="dot"/>')
    a('<text class="cap" x="500" y="77">/github/SukeshaPS701/</text>')
    a('<rect x="402" y="112" width="756" height="340" rx="12" fill="#06090d" fill-opacity="0.7" stroke="#ffffff" stroke-opacity="0.05"/>')
    a("\n".join(texts))
    cur_y = y0 + len(LINES) * dy - 14
    a(f'<rect class="cursor" x="412" y="{cur_y}" width="9" height="16" fill="{ACCENT}"/>')
    # scanline sweeping the full panel
    a(f'<rect x="40" y="0" width="{W-80}" height="3" rx="1.5" fill="#ffffff" fill-opacity="0.55">'
      f'<animate attributeName="y" values="40;{H-40};40" dur="7s" repeatCount="indefinite"/></rect>')
    a('</svg>')
    return "\n".join(o)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "profile-hero-dark.svg"))
    args = ap.parse_args()
    svg = build(portrait_image(args.photo) if args.photo else None)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    open(args.out, "w", encoding="utf-8").write(svg)
    print("wrote", args.out)
