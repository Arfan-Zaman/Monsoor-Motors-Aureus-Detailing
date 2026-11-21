"""GTA-style overlay cards for "Queue Jump" (1080x1920, transparent PNG).
Font: Pricedown Black (Typodermic, free desktop licence: OK for rendered video; do not share the font file).
Run: /opt/miniconda3/bin/python -I make_gta_cards.py <out_dir> <preview.jpg>"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
PD = os.path.expanduser('~/Library/Fonts/PricedownBl.otf')
W, H = 1080, 1920
out, prev = sys.argv[1], sys.argv[2]

def font(s): return ImageFont.truetype(PD, s)

def text_layer(txt, f, xy, fill, stroke=10, shadow=True):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if shadow:
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((xy[0] + 8, xy[1] + 10), txt, font=f, fill=(0, 0, 0, 210), stroke_width=stroke, stroke_fill=(0, 0, 0, 210))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(im).text(xy, txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
    return im

def centred_x(txt, f): return (W - ImageDraw.Draw(Image.new('RGBA', (1, 1))).textlength(txt, font=f)) / 2

# 1) BUSTED: dark band across the middle, big Pricedown word (classic game-over screen feel)
b = Image.new('RGBA', (W, H), (0, 0, 0, 0))
band = Image.new('RGBA', (W, 330), (0, 0, 0, 150))
b.alpha_composite(band, (0, 800))
f = font(300)
b = Image.alpha_composite(b, text_layer('BUSTED', f, (centred_x('BUSTED', f), 790), (236, 236, 236)))
b.save(os.path.join(out, 'Card-BUSTED-GTA.png'))

# 2) Demerit pop-up: FINE amount blurred, demerit points sharp (lower third, inside the safe area)
d = Image.new('RGBA', (W, H), (0, 0, 0, 0))
panel = Image.new('RGBA', (900, 330), (0, 0, 0, 165))
d.alpha_composite(panel, (90, 1180))
f1 = font(120)
f2s = 150
while ImageDraw.Draw(Image.new('RGBA',(1,1))).textlength('-3 DEMERIT POINTS', font=font(f2s)) > 840: f2s -= 4
f2 = font(f2s)
lbl = 'FINE $'
xl = 135
d = Image.alpha_composite(d, text_layer(lbl, f1, (xl, 1185), (255, 77, 160), stroke=6))
amt = text_layer('400', f1, (xl + ImageDraw.Draw(d).textlength(lbl, font=f1) + 10, 1185), (255, 77, 160), stroke=6, shadow=False)
d = Image.alpha_composite(d, amt.filter(ImageFilter.GaussianBlur(22)))   # amount unreadable on purpose
d = Image.alpha_composite(d, text_layer('-3 DEMERIT POINTS', f2, (centred_x('-3 DEMERIT POINTS', f2), 1340), (255, 214, 64), stroke=7))
d.save(os.path.join(out, 'Card-DEMERITS-GTA.png'))

# preview on a dark night frame
pv = Image.new('RGB', (W, H // 2), (0, 0, 0))
for i, c in enumerate((b, d)):
    bg = Image.new('RGBA', (W, H), (34, 26, 52, 255)); bg.alpha_composite(c)
    pv.paste(bg.convert('RGB').resize((W // 2, H // 2)), (i * W // 2, 0))
pv.save(prev)
print('ok')
