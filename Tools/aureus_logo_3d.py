"""Aureus Detailing: 3D hero logo (approved Round 7).
- Symmetric open A, extruded straight down (14 units): walls inside the opening and under both feet.
- Chrome-style gradients on every face, one light from the top left (left faces a step brighter).
- One aqua highlight on the left ridge; hot-pink cap on the apex.
- Reflection: a full mirrored A in aqua tones, fading into the floor, centred under the A.
Importable (symbol(), PALETTES, wordmark pieces) and runnable:
Usage: python3 aureus_logo_3d.py <out_dir>
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from aureus_logo import Face, MONT  # noqa: E402

AQUA, NAVY, ICE, PINK = "#00A8A8", "#071A33", "#F5F8FC", "#FF4D8D"
DX, DY = 0, 14                    # extrusion straight down: symmetric walls, reflection stays centred
P = [(108, 40), (148, 40), (236, 216), (196, 216), (128, 80), (60, 216), (20, 216)]
FACETS = {   # front faces of the open A, split along a ridge on each leg
    "lo": "M108,40 L118,40 L40,216 L20,216 Z",
    "li": "M118,40 L128,40 L128,80 L60,216 L40,216 Z",
    "ri": "M128,40 L138,40 L216,216 L196,216 L128,80 Z",
    "ro": "M138,40 L148,40 L236,216 L216,216 Z",
}
SIDES = {    # visible walls for a straight-down extrusion, mirrored left/right: (edge start, edge end, shade)
    "r_in": (P[3], P[4], "side"), "l_in": (P[4], P[5], "side"),
    "r_foot": (P[2], P[3], "base"), "l_foot": (P[5], P[6], "base"),
}
CAP = "M108,40 L148,40 L144,31 L112,31 Z"
RIDGES = {"l": "M118,40 L40,216"}   # one highlight, on the lit (left) ridge
AXIS = 233                        # reflection starts here (walls end at 216 + DY = 230)
MIRROR = 216 + AXIS               # y' = MIRROR - y puts the mirrored feet (y=216) at y=AXIS

# per palette: gradient stops for each facet (start -> end along the leg), side & base wall colours, text inks
PALETTES = {
    "chrome-3d": {   # one light from the top left: left faces a step brighter than the matching right faces
        "lo": ["#FFFFFF", "#E4EAF1", "#FFFFFF", "#C3CEDB"],
        "li": ["#D2DBE5", "#A6B4C6", "#C3CEDB", "#8A9AB0"],
        "ri": ["#B3C0CF", "#8494AB", "#A3B1C3", "#6E7F97"],
        "ro": ["#E8EDF3", "#C3CEDB", "#DCE3EC", "#A3B1C3"],
        "side": "#3A475C", "base": "#232E40",
        "refl": ["#3FD1CB", "#1FB3AE", "#0E8F8E", "#0A6F72"],
        "ink": ICE, "det": AQUA, "bg": NAVY,
    },
    "navy-3d": {
        "lo": ["#5A89C4", "#3266A0", "#4E7DB8", "#2A5889"],
        "li": ["#244C80", "#14365F", "#1F4576", "#0F2C55"],
        "ri": ["#173866", "#0B2447", "#14325C", "#081D3A"],
        "ro": ["#3F6EA8", "#22507F", "#3768A0", "#1C4672"],
        "side": "#030A15", "base": "#01050B",
        "refl": ["#5FD9D4", "#2BBDB8", "#14A3A3", "#0C8A8C"],
        "ink": NAVY, "det": AQUA, "bg": None,
    },
}


def wall(a, b):
    (x1, y1), (x2, y2) = a, b
    return f"M{x1},{y1} L{x2},{y2} L{x2 + DX},{y2 + DY} L{x1 + DX},{y1 + DY} Z"


def symbol(pal, uid):
    defs = []
    for k, stops in pal.items():
        if k not in FACETS:
            continue
        # gradients mirror each other left/right so light bands sweep symmetrically over the metal
        x1, y1, x2, y2 = (20, 40, 150, 230) if k.startswith("l") else (236, 40, 106, 230)
        st = "".join(f'<stop offset="{i / (len(stops) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(stops))
        defs.append(f'<linearGradient id="{k}{uid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{st}</linearGradient>')
    for i, c in enumerate(pal["refl"]):
        defs.append(f'<linearGradient id="rf{i}{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}"/>'
                    f'<stop offset="1" stop-color="{c}"/></linearGradient>')
    for side, (gx1, gx2) in (("l", (118, 40)),):
        defs.append(f'<linearGradient id="hl{side}{uid}" gradientUnits="userSpaceOnUse" x1="{gx1}" y1="40" x2="{gx2}" y2="216">'
                    f'<stop offset="0" stop-color="{AQUA}" stop-opacity="0"/><stop offset="0.45" stop-color="#7DF7EF"/>'
                    f'<stop offset="1" stop-color="{AQUA}" stop-opacity="0.1"/></linearGradient>')
    defs.append(f'<linearGradient id="cap{uid}" gradientUnits="userSpaceOnUse" x1="108" y1="40" x2="148" y2="31">'
                f'<stop offset="0" stop-color="#FF8AB3"/><stop offset="1" stop-color="{PINK}"/></linearGradient>')
    defs.append(f'<linearGradient id="fade{uid}" gradientUnits="userSpaceOnUse" x1="0" y1="{AXIS}" x2="0" y2="{AXIS + 95}">'
                f'<stop offset="0" stop-color="#fff" stop-opacity="0.75"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
                f'</linearGradient>')
    defs.append(f'<mask id="m{uid}" maskUnits="userSpaceOnUse" x="0" y="{AXIS}" width="256" height="100">'
                f'<rect x="0" y="{AXIS}" width="256" height="100" fill="url(#fade{uid})"/></mask>')

    walls = "".join(f'<path fill="{pal[s]}" d="{wall(a, b)}"/>' for a, b, s in SIDES.values())
    faces = "".join(f'<path fill="url(#{k}{uid})" d="{d}"/>' for k, d in FACETS.items())
    ridges = "".join(f'<path d="{d}" stroke="url(#hl{s}{uid})" stroke-width="3" stroke-linecap="round" fill="none"/>'
                     for s, d in RIDGES.items())
    hero = walls + faces + f'<path fill="url(#cap{uid})" d="{CAP}"/>' + ridges
    # reflection: mirror the front faces (aqua tones) around the floor line, fading out
    rc = pal["refl"]   # reflection keeps the same light: left faces a step brighter than the right
    refl_cols = {"lo": rc[0], "li": rc[2], "ri": rc[3], "ro": rc[1]}
    refl_faces = "".join(f'<path fill="{refl_cols[k]}" d="{d}"/>' for k, d in FACETS.items())
    refl = f'<g mask="url(#m{uid})"><g transform="translate(0,{MIRROR}) scale(1,-1)">{refl_faces}</g></g>'
    body = refl + hero
    # content spans x 20..236 (centre 128), y 31..~328 -> scale 0.8 about the centre line
    return "<defs>" + "".join(defs) + "</defs>" + f'<g transform="translate(25.6,-17) scale(0.8)">{body}</g>'


def svg(w, h, inner, title, bg):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t"><title id="t">{title}</title>{rect}{inner}</svg>')


mont = Face(MONT, 500)


def lambda_glyph(x, base_y, cap, stem):
    half_w = cap / 2 + stem * 0.6
    top, apex = base_y - cap, stem * 0.9
    cx, ro = x + half_w, x + 2 * half_w
    return (f"M{cx - apex / 2:.1f},{top:.1f} H{cx + apex / 2:.1f} L{ro:.1f},{base_y} H{ro - stem * 1.12:.1f} "
            f"L{cx:.1f},{top + stem * 2.2:.1f} L{x + stem * 1.12:.1f},{base_y} H{x:.1f} Z"), 2 * half_w


size, track = 104, 24
cap_h = mont.cap * size / mont.upm
d_a, w_a = lambda_glyph(0, 0, cap_h, size * 0.1)
d_rest = mont.path("UREUS", w_a + track, 0, size, track)
word_w = w_a + track + mont.width("UREUS", size, track)
det = mont.path("DETAILING", 0, 0, 29, 21)

if __name__ == "__main__":
    OUT = Path(sys.argv[1])
    OUT.mkdir(parents=True, exist_ok=True)
    for i, (name, pal) in enumerate(PALETTES.items()):
        (OUT / f"b2-{name}-symbol.svg").write_text(svg(256, 256, symbol(pal, f"s{i}"), f"Aureus {name}", pal["bg"]))
        W = round(256 + 44 + word_w + 40)
        lock = (f'<g transform="translate(6,6) scale(0.95)">{symbol(pal, f"l{i}")}</g>'
                f'<g transform="translate(300,{118 + cap_h / 2 - 20:.1f})"><path fill="{pal["ink"]}" d="{d_a} {d_rest}"/></g>'
                f'<g transform="translate(303,{118 + cap_h / 2 + 34:.1f})"><path fill="{pal["det"]}" d="{det}"/></g>')
        (OUT / f"b2-{name}-lockup.svg").write_text(svg(W, 256, lock, f"Aureus Detailing {name} lockup", pal["bg"]))
    print("ok")
