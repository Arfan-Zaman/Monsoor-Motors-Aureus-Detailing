"""Build the Aureus Detailing logo kit from the approved Round-7 3D logo.
Writes to "Aureus Detailing/02 Logo": SVG masters, transparent PNGs and icons.
Usage: python3 aureus_kit.py
"""
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import aureus_logo_3d as L3  # noqa: E402

ROOT = Path("/Users/mdarfanuzzaman/Documents/Monsoor Motors")
FIN = ROOT / "Aureus Detailing/02 Logo"
SVG, PNG, ICO = FIN / "SVG", FIN / "PNG", FIN / "Icons"
for p in (SVG, PNG, ICO):
    p.mkdir(parents=True, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONT = str(ROOT / "Brand Kit/00 Fonts/Montserrat-Variable.ttf")
NAVY, AQUA, PINK, ICE, BLACK = "#071A33", "#00A8A8", "#FF4D8D", "#F5F8FC", "#111111"
LAMBDA = "M108 40 H148 L236 216 H196 L128 80 L60 216 H20 Z"
CAP = "M108,40 L148,40 L144,31 L112,31 Z"


# ---------------- flat master (matches the 3D: symmetric outline, light cut on the lit left leg) ----------------
def leg_x(y):
    return 108 - (y - 40) / 2, 128 - (y - 80) / 2, 128 + (y - 80) / 2, 148 + (y - 40) / 2


def slats(spec):
    out = []
    for o0, o1 in spec:
        yt, yb = 216 + o0, 216 + o1
        st, sb = 432 - yt, 432 - yb
        lt, lit, rit, rt = leg_x(st)
        lb, lib, rib, rb = leg_x(sb)
        out.append(f"M{lt:.1f},{yt} L{lit:.1f},{yt} L{lib:.1f},{yb} L{lb:.1f},{yb} Z "
                   f"M{rit:.1f},{yt} L{rt:.1f},{yt} L{rb:.1f},{yb} L{rib:.1f},{yb} Z")
    return " ".join(out)


def left_cut():
    """Highlight slit inside the left leg (mirror of the Round-3 right-leg cut), tapered both ends."""
    y0, y1, a, b, t = 84, 192, 10, 18, 20
    xr = lambda y: 148 + (y - 40) / 2
    m = (a + b) / 2
    pts = [(xr(y0) - m, y0), (xr(y0 + t) - a, y0 + t), (xr(y1 - t) - a, y1 - t),
           (xr(y1) - m, y1), (xr(y1 - t) - b, y1 - t), (xr(y0 + t) - b, y0 + t)]
    return "M" + " L".join(f"{256 - x:.1f},{y}" for x, y in pts) + " Z"


def flat_symbol(ink, cap, refl, small=False):
    if small:   # small-size cut: no slit, taller cap, two thick slats
        a = f'<path fill="{ink}" d="{LAMBDA}"/>'
        c = f'<path fill="{cap}" d="M108,40 L148,40 L142,26 L114,26 Z"/>'
        r = f'<path fill="{refl}" d="{slats([(9, 27), (35, 47)])}"/>'
        return f'<g transform="translate(0,-14)">{a}{c}{r}</g>'
    a = f'<path fill="{ink}" fill-rule="evenodd" d="{LAMBDA} {left_cut()}"/>'
    c = f'<path fill="{cap}" d="{CAP}"/>'
    r = f'<path fill="{refl}" d="{slats([(8, 22), (28, 38), (44, 51)])}"/>'
    # same 0.8 scale as the 3D symbol so both sit at the same size in their lockups; content y 31..267 centred
    return f'<g transform="translate(25.6,8) scale(0.8)">{a}{c}{r}</g>'


def svg(w, h, inner, title, bg=None):
    return L3.svg(w, h, inner, title, bg)


# ---------------- variants ----------------
FLAT = {  # name: (A ink, cap, reflection, wordmark ink, DETAILING ink)
    "flat-color": (NAVY, PINK, AQUA, NAVY, AQUA),
    "flat-reverse": (ICE, PINK, AQUA, ICE, AQUA),
    "flat-black": (BLACK, BLACK, BLACK, BLACK, BLACK),
    "flat-white": ("#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"),
}
THREE_D = {"3d-chrome": ("chrome-3d", ICE, AQUA), "3d-navy": ("navy-3d", NAVY, AQUA)}


def symbol_for(name, uid):
    if name in THREE_D:
        return L3.symbol(L3.PALETTES[THREE_D[name][0]], uid)
    ink, cap, refl, *_ = FLAT[name]
    return flat_symbol(ink, cap, refl)


def inks(name):
    return (THREE_D[name][1], THREE_D[name][2]) if name in THREE_D else (FLAT[name][3], FLAT[name][4])


def horizontal(name):
    ink, det_ink = inks(name)
    W = round(256 + 44 + L3.word_w + 40)
    inner = (f'<g transform="translate(6,6) scale(0.95)">{symbol_for(name, "h")}</g>'
             f'<g transform="translate(300,{118 + L3.cap_h / 2 - 20:.1f})"><path fill="{ink}" d="{L3.d_a} {L3.d_rest}"/></g>'
             f'<g transform="translate(303,{118 + L3.cap_h / 2 + 34:.1f})"><path fill="{det_ink}" d="{L3.det}"/></g>')
    return svg(W, 256, inner, f"Aureus Detailing logo, horizontal, {name}")


def stacked(name):
    ink, det_ink = inks(name)
    k = 1.4                              # symbol scale in the stack (~55% of the wordmark width)
    W = round(max(L3.word_w, 256 * k) + 120)
    det_w = L3.mont.width("DETAILING", 29, 21)
    H = round(256 * k) + 30 + round(L3.cap_h) + 34 + 22 + 40
    base = 256 * k + 30 + L3.cap_h
    inner = (f'<g transform="translate({(W - 256 * k) / 2:.1f},0) scale({k})">{symbol_for(name, "v")}</g>'
             f'<g transform="translate({(W - L3.word_w) / 2:.1f},{base:.1f})"><path fill="{ink}" d="{L3.d_a} {L3.d_rest}"/></g>'
             f'<g transform="translate({(W - det_w) / 2:.1f},{base + 52:.1f})"><path fill="{det_ink}" d="{L3.det}"/></g>')
    return svg(W, H, inner, f"Aureus Detailing logo, stacked, {name}")


def render(svg_path, png_path, scale, bg="00000000"):
    import re
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg_path.read_text())
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", f"--default-background-color={bg}",
                    f"--screenshot={png_path}", f"--window-size={m.group(1)},{m.group(2)}",
                    f"file://{svg_path}"], check=True, capture_output=True)


def font(sz, w):
    f = ImageFont.truetype(FONT, sz)
    f.set_variation_by_axes([w])
    return f


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def main():
    names = list(THREE_D) + list(FLAT)
    for n in names:
        (SVG / f"aureus-symbol-{n}.svg").write_text(svg(256, 256, symbol_for(n, "s"), f"Aureus symbol, {n}"))
        (SVG / f"aureus-horizontal-{n}.svg").write_text(horizontal(n))
        (SVG / f"aureus-stacked-{n}.svg").write_text(stacked(n))
    for n, (ink, cap, refl) in {"small-color": (NAVY, PINK, AQUA), "small-reverse": (ICE, PINK, AQUA)}.items():
        (SVG / f"aureus-symbol-{n}.svg").write_text(svg(256, 256, flat_symbol(ink, cap, refl, small=True), f"Aureus small-size symbol, {n}"))
    for f in sorted(SVG.glob("*.svg")):
        render(f, PNG / (f.stem + ".png"), 4 if "symbol" in f.stem else 2)

    # ---------------- icons ----------------
    def tile(src, size, frac, radius=0):
        im = Image.new("RGBA", (size, size), hexrgb(NAVY) + (255,))
        s = Image.open(src).convert("RGBA")
        k = round(size * frac)
        s = s.resize((k, k), Image.LANCZOS)
        im.alpha_composite(s, ((size - k) // 2, (size - k) // 2))
        if radius:
            m = Image.new("L", (size, size), 0)
            ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), radius, fill=255)
            im.putalpha(m)
        return im
    hero = PNG / "aureus-symbol-3d-chrome.png"
    small = PNG / "aureus-symbol-small-reverse.png"
    tile(hero, 1024, 0.92).convert("RGB").save(ICO / "app-icon-1024.png")
    tile(hero, 512, 0.92).convert("RGB").save(ICO / "icon-512.png")
    tile(hero, 192, 0.92).convert("RGB").save(ICO / "icon-192.png")
    tile(hero, 180, 0.92).convert("RGB").save(ICO / "apple-touch-icon-180.png")
    tile(hero, 1080, 0.74).convert("RGB").save(ICO / "social-profile-1080.png")   # circle-crop safe
    fav = {s: tile(small, s, 0.96, radius=round(s * 0.2)) for s in (16, 32, 48)}
    fav[32].save(ICO / "favicon-32.png")
    fav[16].save(ICO / "favicon-16.png")
    fav[48].save(ICO / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("svg", len(list(SVG.glob('*.svg'))), "png", len(list(PNG.glob('*.png'))), "icons", len(list(ICO.iterdir())))


if __name__ == "__main__":
    main()
