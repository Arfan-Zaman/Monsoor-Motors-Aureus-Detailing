"""Draw Aureus Detailing logo concepts as vector SVG (text converted to paths).
Usage: python3 aureus_logo.py <Cinzel.ttf> <out_dir>
Palette: Ocean Pulse (navy #071A33, aqua #00D2C8, pink #FF4D8D, ice #F5F8FC).
"""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont

NAVY, AQUA, PINK, ICE = "#071A33", "#00D2C8", "#FF4D8D", "#F5F8FC"
MONT = "/Users/mdarfanuzzaman/Documents/Monsoor Motors/Brand Kit/00 Fonts/Montserrat-Variable.ttf"


class Face:
    def __init__(self, path, wght):
        f = TTFont(path)
        if "fvar" in f:
            f = instantiateVariableFont(f, {"wght": wght})
        self.gs, self.cmap, self.hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
        self.upm = f["head"].unitsPerEm
        self.cap = getattr(f["OS/2"], "sCapHeight", 0) or self.upm * 0.7

    def width(self, text, size, track=0):
        s = size / self.upm
        w = sum(self.hmtx[self.cmap[ord(c)]][0] * s + track for c in text)
        return w - track

    def path(self, text, x, y, size, track=0):
        """Baseline at y; returns an SVG path d string."""
        s = size / self.upm
        pen = SVGPathPen(self.gs)
        for c in text:
            gn = self.cmap[ord(c)]
            self.gs[gn].draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
            x += self.hmtx[gn][0] * s + track
        return pen.getCommands()


def sparkle(cx, cy, r):
    return (f"M{cx},{cy - r} Q{cx},{cy} {cx + r},{cy} Q{cx},{cy} {cx},{cy + r} "
            f"Q{cx},{cy} {cx - r},{cy} Q{cx},{cy} {cx},{cy - r} Z")


def svg(w, h, body, bg):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{rect}{body}</svg>'


def concepts(cinzel_path, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    serif = Face(cinzel_path, 700)
    sans = Face(MONT, 600)
    variants = {"on-navy": (NAVY, ICE), "on-white": (ICE, NAVY)}

    for tag, (bg, ink) in variants.items():
        # ---- Concept 1: coin emblem + wordmark (horizontal) ----
        W, H = 1400, 420
        cx, cy, R = 210, 210, 150
        a_size = 190
        a_w = serif.width("A", a_size)
        a_cap = serif.cap * a_size / serif.upm
        coin_fill = NAVY if tag == "on-navy" else NAVY
        body = (f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{coin_fill}"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{R - 14}" fill="none" stroke="{AQUA}" stroke-width="7"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{R - 26}" fill="none" stroke="{AQUA}" stroke-width="1.5" opacity="0.6"/>'
                f'<path d="{serif.path("A", cx - a_w / 2, cy + a_cap / 2, a_size)}" fill="{ICE}"/>'
                f'<path d="{sparkle(cx + 92, cy - 92, 34)}" fill="{PINK}"/>')
        wx = 420
        body += f'<path d="{serif.path("AUREUS", wx, 235, 150, 14)}" fill="{ink}"/>'
        body += f'<path d="{sans.path("DETAILING", wx + 6, 310, 46, 22)}" fill="{AQUA if tag == "on-navy" else NAVY}"/>'
        (out / f"concept-1-coin-{tag}.svg").write_text(svg(W, H, body, bg))

        # ---- Concept 2: stacked water-drop monogram ----
        W, H = 900, 1000
        dx, dtop, dbot = 450, 70, 520
        drop = (f"M{dx},{dtop} C{dx + 60},{dtop + 120} {dx + 210},{dtop + 230} {dx + 210},{dtop + 330} "
                f"A210,210 0 1 1 {dx - 210},{dtop + 330} C{dx - 210},{dtop + 230} {dx - 60},{dtop + 120} {dx},{dtop} Z")
        a_size = 230
        a_w = serif.width("A", a_size)
        a_cap = serif.cap * a_size / serif.upm
        acy = dtop + 345
        body = (f'<path d="{drop}" fill="{AQUA}"/>'
                f'<path d="{serif.path("A", dx - a_w / 2, acy + a_cap / 2, a_size)}" fill="{NAVY}"/>'
                f'<path d="{sparkle(dx + 150, dtop + 170, 40)}" fill="{PINK}"/>')
        tw = serif.width("AUREUS", 130, 14)
        body += f'<path d="{serif.path("AUREUS", dx - tw / 2, 800, 130, 14)}" fill="{ink}"/>'
        sw = sans.width("DETAILING", 40, 20)
        body += f'<path d="{sans.path("DETAILING", dx - sw / 2, 870, 40, 20)}" fill="{AQUA if tag == "on-navy" else NAVY}"/>'
        (out / f"concept-2-drop-{tag}.svg").write_text(svg(W, H, body, bg))

        # ---- Concept 3: wordmark with wave + sparkle on the A ----
        W, H = 1400, 420
        size, track = 190, 18
        tw = serif.width("AUREUS", size, track)
        x0 = (W - tw) / 2
        base = 255
        cap = serif.cap * size / serif.upm
        a_w = serif.width("A", size)
        body = f'<path d="{serif.path("AUREUS", x0, base, size, track)}" fill="{ink}"/>'
        body += f'<path d="{sparkle(x0 + a_w / 2, base - cap - 52, 28)}" fill="{PINK}"/>'
        wy = base + 42
        wave = (f"M{x0},{wy} C{x0 + tw * 0.17},{wy - 26} {x0 + tw * 0.33},{wy + 26} {x0 + tw * 0.5},{wy} "
                f"S{x0 + tw * 0.83},{wy - 26} {x0 + tw},{wy}")
        body += f'<path d="{wave}" fill="none" stroke="{AQUA}" stroke-width="9" stroke-linecap="round"/>'
        sw = sans.width("DETAILING", 42, 24)
        body += f'<path d="{sans.path("DETAILING", (W - sw) / 2, 365, 42, 24)}" fill="{AQUA if tag == "on-navy" else NAVY}"/>'
        (out / f"concept-3-wordmark-{tag}.svg").write_text(svg(W, H, body, bg))
    print("written:", sorted(p.name for p in out.glob("*.svg")))


if __name__ == "__main__":
    concepts(sys.argv[1], sys.argv[2])
