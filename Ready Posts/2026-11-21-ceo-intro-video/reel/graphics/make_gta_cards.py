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

# 3) Character intro cards for the freeze-frames: name (white) + designation (pink), left-aligned, lower third
def intro(name, role, fn):
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    fn1 = font(230)
    while ImageDraw.Draw(c).textlength(name, font=fn1) > 900: fn1 = font(fn1.size - 6)
    c = Image.alpha_composite(c, text_layer(name, fn1, (90, 1080), (240, 240, 240), stroke=9))
    c = Image.alpha_composite(c, text_layer(role, font(120), (100, 1080 + fn1.size + 10), (255, 77, 160), stroke=7))
    c.save(os.path.join(out, fn)); return c
a = intro('ARFAN', 'CEO', 'Card-ARFAN-CEO-GTA.png')
m = intro('MONSOOR', 'BOSS', 'Card-MONSOOR-BOSS-GTA.png')
pv2 = Image.new('RGB', (W, H // 2), (0, 0, 0))
for i, c in enumerate((a, m)):
    bg = Image.new('RGBA', (W, H), (60, 52, 70, 255)); bg.alpha_composite(c)
    pv2.paste(bg.convert('RGB').resize((W // 2, H // 2)), (i * W // 2, 0))
pv2.save(prev.replace('.jpg', '_intro.jpg'))

# 4) More game-style overlays (all 1080x1920, transparent; text kept in the centre safe area)
def save(c, fn): c.save(os.path.join(out, fn)); return c
def stamp(line1, line2, fn, y=330):
    # location / time stamp: bold Pricedown place, thin pink time line, small dark backing bar
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    f1, f2 = font(110), font(64)
    while ImageDraw.Draw(c).textlength(line1, font=f1) > 900: f1 = font(f1.size - 4)
    c = Image.alpha_composite(c, text_layer(line1, f1, (centred_x(line1, f1), y), (245, 245, 245), stroke=7))
    c = Image.alpha_composite(c, text_layer(line2, f2, (centred_x(line2, f2), y + f1.size + 6), (255, 77, 160), stroke=5))
    return save(c, fn)
def tag(name, role, fn, y=1250):
    # quick character tag over moving picture (no freeze): smaller than the hero intros
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    f1, f2 = font(150), font(84)
    c = Image.alpha_composite(c, text_layer(name, f1, (90, y), (240, 240, 240), stroke=8))
    c = Image.alpha_composite(c, text_layer(role, f2, (100, y + f1.size + 4), (255, 214, 64), stroke=6))
    return save(c, fn)
stamp('PERTH CBD', '10:47 PM', 'Stamp-PERTH.png', y=600)
stamp('SWANLINE', 'ALBANY HWY  ·  10:52 PM', 'Stamp-SERVO.png')
stamp('VICTORIA PARK', 'NEXT MORNING  ·  8:15 AM', 'Stamp-YARD.png')
tag('LAYLA', 'LEAD FOOT', 'Tag-LAYLA.png')
tag('DAVE', 'TIRED DAD', 'Tag-DAVE.png')
# phone HUD: rounded dark card, top centre
c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
d.rounded_rectangle([190, 300, 890, 470], radius=40, fill=(10, 10, 16, 215), outline=(255, 77, 160, 255), width=5)
d.ellipse([225, 335, 325, 435], fill=(46, 204, 113, 255))
d.polygon([(255, 365), (300, 385), (255, 405)], fill=(255, 255, 255, 255))
c = Image.alpha_composite(c, text_layer('BOSS', font(96), (355, 312), (245, 245, 245), stroke=5, shadow=False))
c = Image.alpha_composite(c, text_layer('CALLING...', font(56), (360, 405), (255, 77, 160), stroke=4, shadow=False))
save(c, 'HUD-CALL-BOSS.png')
# pump pop-ups (real figures from TEXT-AND-NUMBERS-v2): Dave's in red, Arfan's in green
def pump(amount, who, col, fn, y):
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([150, y, 930, y + 230], radius=30, fill=(0, 0, 0, 170))
    c = Image.alpha_composite(c, text_layer(who, font(70), (centred_x(who, font(70)), y + 12), (240, 240, 240), stroke=5))
    c = Image.alpha_composite(c, text_layer(amount, font(130), (centred_x(amount, font(130)), y + 85), col, stroke=7))
    return save(c, fn)
pump('$94.99', 'DAVE  ·  PUMP 2', (255, 70, 70), 'Pop-PUMP-DAVE.png', 1180)
pump('$36.20', 'ARFAN  ·  PUMP 1', (90, 230, 120), 'Pop-PUMP-ARFAN.png', 1180)
# mission complete
c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
band = Image.new('RGBA', (W, 300), (0, 0, 0, 140)); c.alpha_composite(band, (0, 760))
f1 = font(150)
while ImageDraw.Draw(c).textlength('MISSION PASSED', font=f1) > 960: f1 = font(f1.size - 4)
c = Image.alpha_composite(c, text_layer('MISSION PASSED', f1, (centred_x('MISSION PASSED', f1), 780), (255, 200, 40), stroke=8))
c = Image.alpha_composite(c, text_layer('+1 HAPPY FAMILY', font(80), (centred_x('+1 HAPPY FAMILY', font(80)), 790 + f1.size + 10), (240, 240, 240), stroke=6))
save(c, 'Card-MISSION-PASSED.png')
# preview sheet
names = ['Stamp-PERTH', 'Stamp-SERVO', 'Stamp-YARD', 'Tag-LAYLA', 'Tag-DAVE', 'HUD-CALL-BOSS', 'Pop-PUMP-DAVE', 'Pop-PUMP-ARFAN', 'Card-MISSION-PASSED']
sheet = Image.new('RGB', (W // 3 * 9, H // 3), (0, 0, 0))
for i, n in enumerate(names):
    bg = Image.new('RGBA', (W, H), (60, 52, 70, 255)); bg.alpha_composite(Image.open(os.path.join(out, n + '.png')))
    sheet.paste(bg.convert('RGB').resize((W // 3, H // 3)), (i * W // 3, 0))
sheet.save(prev.replace('.jpg', '_more.jpg'))

# 5) Pre-order pop-up (the night decision scene)
c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
d.rounded_rectangle([140, 1150, 940, 1420], radius=34, fill=(0, 0, 0, 185), outline=(90, 230, 120, 255), width=5)
c = Image.alpha_composite(c, text_layer('PRE-ORDER PLACED', font(104), (centred_x('PRE-ORDER PLACED', font(104)), 1170), (90, 230, 120), stroke=6))
c = Image.alpha_composite(c, text_layer('C-HR HYBRID  ·  DAVE & MIA', font(64), (centred_x('C-HR HYBRID  ·  DAVE & MIA', font(64)), 1300), (240, 240, 240), stroke=5))
save(c, 'Pop-PREORDER.png')
