"""Fish Paradise logo concepts (logo-design skill, fast track).
  A  Cat-fish        - a fish with cat ears and a cat's slit pupil
  B  Two fish, one cat - two curved fish form a round cat face; their tails are the ears
  C  Paradise sunset - a cat-head sun setting over the sea, a fish leaping past
Usage: python3 fish_paradise_logo.py <out_dir> <Fredoka.ttf> <mode: color|black>
"""
import math
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont

OUT, FONT, MODE = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
OUT.mkdir(parents=True, exist_ok=True)
C = {"sea": "#0B4F6C", "aqua": "#20B8C9", "coral": "#FF7A59", "sun": "#FFC857", "cream": "#FFF7EA", "ink": "#0B4F6C"}
if MODE == "black":
    C = {k: ("#FFFFFF" if k == "cream" else "#111111") for k in C}


class Face:
    def __init__(self, path, wght):
        f = instantiateVariableFont(TTFont(path), {"wght": wght, "wdth": 100})
        self.gs, self.cmap, self.hmtx, self.upm = f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
        self.cap = f["OS/2"].sCapHeight

    def width(self, text, size, track=0):
        s = size / self.upm
        return sum(self.hmtx[self.cmap[ord(c)]][0] * s + track for c in text) - track

    def path(self, text, x, y, size, track=0):
        s = size / self.upm
        pen = SVGPathPen(self.gs)
        for ch in text:
            gn = self.cmap[ord(ch)]
            self.gs[gn].draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
            x += self.hmtx[gn][0] * s + track
        return pen.getCommands()


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t"><title id="t">{title}</title>{body}</svg>')


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


# ---------------- A: Cat-fish ----------------
def cat_fish(body, eye, pupil):
    # body + tail in one path; nose left at (34,140), tail fork right; two cat ears rise from the head
    fish = ("M34,140 C58,90 128,78 176,126 L226,92 C214,118 214,162 226,188 L176,154 "
            "C128,202 58,190 34,140 Z")
    # ears sit on the head: bases dip below the body's top curve so they merge into one silhouette
    ears = "M52,124 L60,64 L98,108 Z M92,104 L114,52 L138,104 Z"
    eye_c = f'<circle cx="80" cy="132" r="17" fill="{eye}"/>'
    pup = f'<ellipse cx="82" cy="132" rx="4.5" ry="12" fill="{pupil}"/>'
    return f'<g transform="translate(0,4)"><path fill="{body}" d="{fish} {ears}"/>{eye_c}{pup}</g>'


# ---------------- B: Two fish, one cat ----------------
def fish_arc(cx, cy, r_out, th0, th1, w0, w1, steps=40, mirror=False):
    """Tapered band along a circle from th0 (head, width w0) to th1 (tail join, width w1)."""
    outer, inner = [], []
    for i in range(steps + 1):
        t = i / steps
        th = th0 + (th1 - th0) * t
        w = w0 + (w1 - w0) * t ** 1.3
        outer.append(pt(cx, cy, r_out, th))
        inner.append(pt(cx, cy, r_out - w, th))
    pts = outer + inner[::-1]
    if mirror:
        pts = [(2 * cx - x, y) for x, y in pts]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def two_fish(fish_col, nose_col, eye_col):
    cx, cy, R = 128, 140, 98
    th0, th1 = 114, 236        # heads apart at the chin (kissing fish), tails at the upper sides
    w0, w1 = 36, 18
    paths = []
    for mirror in (False, True):
        band = fish_arc(cx, cy, R, th0, th1, w0, w1, mirror=mirror)
        # rounded head: a circle spanning the band's width at the head end
        hx, hy = pt(cx, cy, R - w0 / 2, th0)
        # tail fin = cat ear: a wide forked fin rising from the band end
        b_out = pt(cx, cy, R + 2, th1 - 4)
        b_in = pt(cx, cy, R - w1 - 2, th1 - 4)
        tip_o = pt(cx, cy, R + 30, th1 + 16)       # outer fin tip (the ear's point)
        notch = pt(cx, cy, R - 6, th1 + 12)
        tip_i = pt(cx, cy, R - 26, th1 + 22)       # inner fin tip
        fin = [b_out, tip_o, notch, tip_i, b_in]
        if mirror:
            hx = 2 * cx - hx
            fin = [(2 * cx - x, y) for x, y in fin]
        paths.append(band)
        r = w0 / 2
        paths.append(f"M{hx + r:.1f},{hy:.1f} A{r},{r} 0 1 1 {hx - r:.1f},{hy:.1f} A{r},{r} 0 1 1 {hx + r:.1f},{hy:.1f} Z")
        paths.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in fin) + " Z")
    eyes = ""
    for mirror in (False, True):
        ex, ey = pt(cx, cy, R - w0 / 2, th0 + 14)
        ex = 2 * cx - ex if mirror else ex
        eyes += f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="6" fill="{eye_col}"/>'
    nose = f'<path fill="{nose_col}" d="M114,150 H142 Q128,170 114,150 Z"/>'
    # one <path> per piece: the mirrored fish winds the other way, so sharing a path would punch holes
    pieces = "".join(f'<path fill="{fish_col}" d="{p}"/>' for p in paths)
    return f'<g transform="translate(0,-4)">{pieces}{eyes}{nose}</g>'


# ---------------- C: Paradise sunset ----------------
def sunset(bg, sun, sea, fish_col, sea2):
    cx, cy = 128, 128
    disc = f'<circle cx="{cx}" cy="{cy}" r="118" fill="{bg}"/>'
    # cat-head sun: circle + two ears, centre (128,150)
    head = ["M78,150 A50,50 0 0 1 178,150 Z",            # top half of the head (lower half hidden by sea)
            "M86,124 L84,82 L114,104 Z", "M170,124 L172,82 L142,104 Z"]
    sun_p = "".join(f'<path fill="{sun}" d="{h}"/>' for h in head)
    # sea: waves from y=150 down, clipped by the disc edge (built as a closed lower segment)
    y0 = 150
    xl, xr = cx - math.sqrt(118 ** 2 - (y0 - cy) ** 2), cx + math.sqrt(118 ** 2 - (y0 - cy) ** 2)
    wave = f"M{xl:.1f},{y0} "
    n = 6
    seg = (xr - xl) / n
    for i in range(n):
        x1 = xl + seg * i
        wave += f"Q{x1 + seg / 4:.1f},{y0 - 9} {x1 + seg / 2:.1f},{y0} Q{x1 + 3 * seg / 4:.1f},{y0 + 9} {x1 + seg:.1f},{y0} "
    wave += f"A118,118 0 0 1 {xl:.1f},{y0} Z"
    sea_p = f'<path fill="{sea}" d="{wave}"/>'
    # a second, lighter wave band for depth
    y1 = 186
    xl2, xr2 = cx - math.sqrt(118 ** 2 - (y1 - cy) ** 2), cx + math.sqrt(118 ** 2 - (y1 - cy) ** 2)
    w2 = f"M{xl2:.1f},{y1} "
    seg2 = (xr2 - xl2) / 5
    for i in range(5):
        x1 = xl2 + seg2 * i
        w2 += f"Q{x1 + seg2 / 4:.1f},{y1 - 8} {x1 + seg2 / 2:.1f},{y1} Q{x1 + 3 * seg2 / 4:.1f},{y1 + 8} {x1 + seg2:.1f},{y1} "
    w2 += f"A118,118 0 0 1 {xl2:.1f},{y1} Z"
    sea2_p = f'<path fill="{sea2}" d="{w2}"/>'
    # leaping fish (small), arcing from the sea at the right
    fish = ("M150,118 C162,96 190,92 204,108 L220,96 C216,108 216,118 222,128 L204,118 "
            "C190,132 162,132 150,118 Z")
    # fish leaps in the clear sky above the cat's ears (centre moved from (186,112) to (128,50))
    fish_p = f'<g transform="translate(-58,-62) rotate(-12 186 112)"><path fill="{fish_col}" d="{fish}"/>' \
             f'<circle cx="165" cy="114" r="3.6" fill="{bg}"/></g>'
    return disc + sun_p + sea_p + sea2_p + fish_p


face = Face(FONT, 600)
symbols = {
    "a-catfish": cat_fish(C["coral"], C["cream"], C["sea"]),
    "b-twofish": two_fish(C["sea"], C["coral"], C["cream"] if MODE == "color" else "#FFFFFF"),
    "c-sunset": sunset(C["sea"], C["sun"] if MODE == "color" else "#FFFFFF", C["aqua"] if MODE == "color" else "#FFFFFF",
                       C["coral"] if MODE == "color" else "#FFFFFF", C["sea"] if MODE == "color" else "#111111"),
}
if MODE == "black":   # one-colour: drop decorative fills that would vanish
    symbols["b-twofish"] = two_fish("#111111", "#111111", "#FFFFFF")

for name, body in symbols.items():
    (OUT / f"{name}-symbol-{MODE}.svg").write_text(svg(256, 256, body, f"Fish Paradise {name}"))
    # lockup: symbol left, "Fish" over "Paradise"
    s1, s2 = 92, 92
    w1, w2 = face.width("Fish", s1), face.width("Paradise", s2)
    cap = face.cap * s1 / face.upm
    W = round(256 + 30 + max(w1, w2) + 40)
    ink1 = C["sea"] if MODE == "color" else "#111111"
    ink2 = C["coral"] if MODE == "color" else "#111111"
    lock = (f'{body}'
            f'<path fill="{ink1}" d="{face.path("Fish", 286, 128 - 10, s1)}"/>'
            f'<path fill="{ink2}" d="{face.path("Paradise", 286, 128 + cap + 6, s2)}"/>')
    (OUT / f"{name}-lockup-{MODE}.svg").write_text(svg(W, 256, lock, f"Fish Paradise {name} lockup"))
print("ok", MODE)
