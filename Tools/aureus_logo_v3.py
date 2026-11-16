"""Aureus Detailing: Mirror A refinements (round 3).
  B1 Refined reflection  - open A on a mirror finish; reflection in four slats thinning evenly
  B2 Light edge          - B1 + a highlight cut into the right leg (negative space, works in one colour)
  B3 Coin                - B2 inside a thin coin ring (the aureus was Rome's gold coin)
Usage: python3 aureus_logo_v3.py <out_dir> <ink> <accent> <tag>
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from aureus_logo import Face, MONT  # noqa: E402

OUT, INK, ACC, TAG = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
OUT.mkdir(parents=True, exist_ok=True)

LAMBDA = "M108 40 H148 L236 216 H196 L128 80 L60 216 H20 Z"
BASE = 216
SLATS = [(7, 21), (27, 37), (43, 50)]   # thinning 14 -> 10 -> 7, gaps 6 (nothing under 1/48 of the mark)


def leg_x(y):
    return 108 - (y - 40) / 2, 128 - (y - 80) / 2, 128 + (y - 80) / 2, 148 + (y - 40) / 2


def reflection():
    out = []
    for o0, o1 in SLATS:
        yt, yb = BASE + o0, BASE + o1
        st, sb = 2 * BASE - yt, 2 * BASE - yb
        lt, lit, rit, rt = leg_x(st)
        lb, lib, rib, rb = leg_x(sb)
        out.append(f"M{lt:.1f},{yt} L{lit:.1f},{yt} L{lib:.1f},{yb} L{lb:.1f},{yb} Z")
        out.append(f"M{rit:.1f},{yt} L{rt:.1f},{yt} L{rb:.1f},{yb} L{rib:.1f},{yb} Z")
    return " ".join(out)


def edge_cut():
    """Thin highlight slit inside the right leg, parallel to its outer edge, tapered at both ends."""
    y0, y1, a, b, t = 84, 192, 10, 18, 20   # 8-unit slit, inset 10..18 from the outer edge, 20-unit tapers
    xo = lambda y: 148 + (y - 40) / 2
    m = (a + b) / 2
    return (f"M{xo(y0) - m:.1f},{y0} L{xo(y0 + t) - a:.1f},{y0 + t} L{xo(y1 - t) - a:.1f},{y1 - t} "
            f"L{xo(y1) - m:.1f},{y1} L{xo(y1 - t) - b:.1f},{y1 - t} L{xo(y0 + t) - b:.1f},{y0 + t} Z")


def mark(with_cut, ink, acc):
    a_path = LAMBDA + (" " + edge_cut() if with_cut else "")
    return (f'<path fill="{ink}" fill-rule="evenodd" d="{a_path}"/>'
            f'<path fill="{acc}" d="{reflection()}"/>')


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t"><title id="t">{title}</title>{body}</svg>')


# vertical extent of A + reflection: 40 .. 276 (236 tall); centre it on 128 with a little optical lift
SHIFT = -30
symbols = {
    "b1-refined": f'<g transform="translate(0,{SHIFT})">{mark(False, INK, ACC)}</g>',
    "b2-light-edge": f'<g transform="translate(0,{SHIFT})">{mark(True, INK, ACC)}</g>',
    "b3-coin": (f'<circle cx="128" cy="128" r="120" fill="none" stroke="{INK}" stroke-width="7"/>'
                f'<g transform="translate(128,128) scale(0.74) translate(-128,{-158 + 4})">{mark(True, INK, ACC)}</g>'),
}
for name, body in symbols.items():
    (OUT / f"{name}-symbol-{TAG}.svg").write_text(svg(256, 256, body, f"Aureus {name}"))

# lockup: symbol + AUREUS (Montserrat Medium, open A) + DETAILING
mont = Face(MONT, 500)


def lambda_glyph(x, base_y, cap, stem):
    half_w = cap / 2 + stem * 0.6
    top, apex = base_y - cap, stem * 0.9
    cx, ro = x + half_w, x + 2 * half_w
    d = (f"M{cx - apex / 2:.1f},{top:.1f} H{cx + apex / 2:.1f} L{ro:.1f},{base_y} H{ro - stem * 1.12:.1f} "
         f"L{cx:.1f},{top + stem * 2.2:.1f} L{x + stem * 1.12:.1f},{base_y} H{x:.1f} Z")
    return d, 2 * half_w


size, track = 104, 24
cap = mont.cap * size / mont.upm
d_a, w_a = lambda_glyph(0, 0, cap, size * 0.1)
d_rest = mont.path("UREUS", w_a + track, 0, size, track)
word_w = w_a + track + mont.width("UREUS", size, track)
det = mont.path("DETAILING", 0, 0, 29, 21)
for name, body in symbols.items():
    W = 256 + 44 + word_w + 40
    lock = (f'<g transform="translate(6,6) scale(0.95)">{body}</g>'
            f'<g transform="translate(300,{128 + cap / 2 - 20:.1f})"><path fill="{INK}" d="{d_a} {d_rest}"/></g>'
            f'<g transform="translate(303,{128 + cap / 2 + 34:.1f})"><path fill="{ACC}" d="{det}"/></g>')
    (OUT / f"{name}-lockup-{TAG}.svg").write_text(svg(round(W), 256, lock, f"Aureus Detailing {name} lockup"))
print("ok", TAG)
