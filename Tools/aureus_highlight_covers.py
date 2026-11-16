"""Instagram highlight covers for Aureus Detailing (1080x1920, content inside the centre circle).
Run: /opt/miniconda3/bin/python -I Tools/aureus_highlight_covers.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Aureus Detailing/08 Social Media/Highlight Covers"
FONT = ROOT / "Brand Kit/00 Fonts/Montserrat-Variable.ttf"
SYMBOL = ROOT / "Aureus Detailing/02 Logo/PNG/aureus-symbol-flat-reverse.png"
NAVY, AQUA, WHITE = (7, 26, 51), (0, 168, 168), (245, 248, 252)
LABELS = ["Packages", "Before & After", "Book", "Reviews", "Find Us", "Ceramic"]
W, H = 1080, 1920
font = ImageFont.truetype(str(FONT), 78)
try:
    font.set_variation_by_name("SemiBold")
except Exception:
    pass
sym = Image.open(SYMBOL).convert("RGBA")
sym.thumbnail((300, 300), Image.LANCZOS)
OUT.mkdir(parents=True, exist_ok=True)
for i, label in enumerate(LABELS, 1):
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    cx, cy, r = W // 2, H // 2, 470
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=AQUA, width=10)
    im.paste(sym, (cx - sym.width // 2, cy - 250), sym)
    tw = d.textlength(label, font=font)
    if tw > 760:
        f2 = font.font_variant(size=int(78 * 760 / tw)); tw = d.textlength(label, font=f2)
    else:
        f2 = font
    d.text((cx - tw / 2, cy + 120), label, font=f2, fill=WHITE)
    im.save(OUT / f"{i:02d}-{label.replace(' & ', '-').replace(' ', '-')}.png", optimize=True)
print("saved", len(LABELS), "covers to", OUT)
