"""Aureus Detailing logo concepts, round 2 (built with the logo-design skill process).
Idea family: the sharp line of light that runs across freshly polished paint.
  A  Glint A      - letterform: a crossbar-less A crossed by one tapered light glint
  B  Mirror A     - letterform: the A standing on a mirror finish, its reflection in fading bands
  C  Lambda word  - wordmark: AUREUS in light wide caps, the A open with a glint for a crossbar
Usage: python3 aureus_logo_v2.py <out_dir> [ink] [glint]
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from aureus_logo import Face, MONT  # noqa: E402

OUT = Path(sys.argv[1])
INK = sys.argv[2] if len(sys.argv) > 2 else "#111111"
GLINT = sys.argv[3] if len(sys.argv) > 3 else "#111111"
TAG = sys.argv[4] if len(sys.argv) > 4 else "black"
OUT.mkdir(parents=True, exist_ok=True)

# Lambda on a 256 grid: flat apex 108-148 at y=40, feet at y=216, every edge on a 1:2 slope, 40-unit legs.
LAMBDA = "M108 40 H148 L236 216 H196 L128 80 L60 216 H20 Z"


def leg_x(y):
    """x of the four leg edges at height y (y >= 80): left-out, left-in, right-in, right-out."""
    return 108 - (y - 40) / 2, 128 - (y - 80) / 2, 128 + (y - 80) / 2, 148 + (y - 40) / 2


def glint(cx, cy, half_len, half_th, bias=0):
    """Tapered light glint: a long thin lozenge, fattest slightly right of centre."""
    return (f"M{cx - half_len},{cy} L{cx + bias},{cy - half_th} L{cx + half_len},{cy} "
            f"L{cx + bias},{cy + half_th} Z")


def write(name, w, h, body, title):
    (OUT / f"{name}-{TAG}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-labelledby="t"><title id="t">{title}</title>{body}</svg>')


# ---------- A: Glint A (symbol) ----------
sym_a = (f'<path fill="{INK}" d="{LAMBDA}"/>'
         f'<path fill="{GLINT}" d="{glint(132, 160, 112, 9, 18)}"/>')
write("a-glint-symbol", 256, 256, sym_a, "Aureus Glint A")

# ---------- B: Mirror A (symbol) ----------
base = 216
bands = [(8, 24), (32, 42), (50, 56)]  # offsets below the feet: mirrored, thinning and fading out
refl = []
for (o0, o1) in bands:
    y_top, y_bot = base + o0, base + o1          # reflected band
    s_top, s_bot = 2 * base - y_top, 2 * base - y_bot  # matching heights on the real A
    lt, lit, rit, rt = leg_x(s_top)
    lb, lib, rib, rb = leg_x(s_bot)
    refl.append(f"M{lt},{y_top} L{lit},{y_top} L{lib},{y_bot} L{lb},{y_bot} Z")
    refl.append(f"M{rit},{y_top} L{rt},{y_top} L{rb},{y_bot} L{rib},{y_bot} Z")
sym_b = (f'<g transform="translate(0,-22)"><path fill="{INK}" d="{LAMBDA}"/>'
         f'<path fill="{GLINT}" d="{" ".join(refl)}"/></g>')
write("b-mirror-symbol", 256, 256, sym_b, "Aureus Mirror A")

# ---------- wordmark pieces ----------
mont_l = Face(MONT, 300)
mont_m = Face(MONT, 500)


def lambda_glyph(x, base_y, cap, stem):
    """Crossbar-less A matched to Montserrat caps: 1:2 slope legs, flat apex, constant stem."""
    half_w = cap / 2 + stem * 0.6
    top = base_y - cap
    apex = stem * 0.9
    lo, ro = x, x + 2 * half_w
    cx = x + half_w
    d = (f"M{cx - apex / 2},{top} H{cx + apex / 2} L{ro},{base_y} H{ro - stem * 1.12} "
         f"L{cx},{top + stem * 2.2} L{lo + stem * 1.12},{base_y} H{lo} Z")
    return d, 2 * half_w


def wordmark(x, base_y, size, track, face, glint_on=True):
    cap = face.cap * size / face.upm
    stem = size * (0.062 if face is mont_l else 0.1)
    d_a, w_a = lambda_glyph(x, base_y, cap, stem)
    rest_x = x + w_a + track
    d_rest = face.path("UREUS", rest_x, base_y, size, track)
    total = w_a + track + face.width("UREUS", size, track)
    g = glint(x + w_a / 2 + 4, base_y - cap * 0.36, w_a * 0.62, stem * 0.55, w_a * 0.08) if glint_on else ""
    return d_a, d_rest, g, total, cap


# ---------- C: Lambda wordmark ----------
d_a, d_rest, g, tw, cap = wordmark(0, 0, 150, 34, mont_l)
W = tw + 80
body = (f'<g transform="translate(40,{128 + cap / 2})"><path fill="{INK}" d="{d_a} {d_rest}"/>'
        f'<path fill="{GLINT}" d="{g}"/></g>')
write("c-lambda-wordmark", round(W), 256, body, "AUREUS wordmark")

# ---------- lockups for A and B (symbol left, words right) ----------
for key, sym in (("a-glint", sym_a), ("b-mirror", sym_b)):
    d_a2, d_rest2, _, tw2, cap2 = wordmark(0, 0, 112, 26, mont_m, glint_on=False)
    det = mont_m.path("DETAILING", 0, 0, 30, 21.5)
    det_w = mont_m.width("DETAILING", 30, 21.5)
    W = 256 + 40 + max(tw2, det_w) + 40
    body = (f'<g transform="translate(8,8) scale(0.94)">{sym}</g>'
            f'<g transform="translate(296,{128 + cap2 / 2 - 22})"><path fill="{INK}" d="{d_a2} {d_rest2}"/></g>'
            f'<g transform="translate(300,{128 + cap2 / 2 + 34})"><path fill="{GLINT if GLINT != INK else INK}" d="{det}"/></g>')
    write(f"{key}-lockup", round(W), 256, body, f"Aureus Detailing {key} lockup")
print("ok", sorted(p.name for p in OUT.glob(f"*-{TAG}.svg")))
