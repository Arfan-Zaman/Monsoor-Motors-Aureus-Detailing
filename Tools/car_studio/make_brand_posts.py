"""Monsoor Motors sell-post branding v2: simple, modern.

  /opt/miniconda3/bin/python -I make_brand_posts.py <car folder>

Reads the `branded_set` block in <car folder>/car.yaml:

  branded_set:
    source: Studio/stills          # folder holding the photos (any 4:5 images)
    out: Branded                   # output folder inside the car folder
    hero: side.jpg                 # photo for the hero card + story (car sits high, floor below)
    slides:                        # carousel after the hero, in order
      - {file: rear34.jpg, label: Rear}
      - {file: 05_interior_dashboard.jpg, label: Cabin}

Design: full-bleed photo, one floating white card on the hero (model, specs,
price, phone, logo), small frosted labels on the other slides, a navy closing
card. Montserrat, Monsoor navy #0F2747, orange #FF5F15 as the only accent.
Missing car.yaml details print as [BRACKETS]; nothing is guessed.
"""
import os, sys
import yaml
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "assets", "Montserrat-Variable.ttf")
LOGO_NAVY = os.path.join(HERE, "assets", "Monsoor-Logo-Horizontal-Navy.png")
LOGO_WHITE = os.path.join(HERE, "assets", "Monsoor-Logo-Horizontal-White.png")
NAVY, ORANGE = (15, 39, 71), (255, 95, 21)
INK, MUTED, WHITE, CARD = (15, 39, 71), (98, 108, 124), (255, 255, 255), (250, 249, 247)
W, H = 1080, 1350          # 4:5 feed
SW, SH = 1080, 1920        # 9:16 story
M = 48                     # outer margin


def font(size, weight=500):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight])
    return f


def logo(path, width):
    lg = Image.open(path).convert("RGBA")
    return lg.resize((width, round(width * lg.height / lg.width)), Image.LANCZOS)


def fit_font(d, text, weight, size, maxw):
    f = font(size, weight)
    while d.textlength(text, font=f) > maxw and size > 18:
        size -= 2
        f = font(size, weight)
    return f


def spaced(d, xy, text, f, fill, tracking=3):
    """Small caps label with letter spacing."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking
    return x


def car_bits(car):
    def v(key, fmt="{}"):
        val = car.get(key)
        return fmt.format(val) if val not in (None, "") else f"[{key.upper().replace('_', ' ')}]"
    year = v("year")
    name = f"{car.get('make', '')} {v('model')}".strip()
    km = f"{car['km']:,} km" if isinstance(car.get("km"), int) else v("km", "{} km")
    specs = "  ·  ".join([km, v("transmission"), v("colour")])
    if isinstance(car.get("price"), (int, float)):
        price = f"${car['price']:,}"
    else:  # no number: show the call-to-action text instead (e.g. "Ask for price")
        price = car.get("price_text") or v("price")
    return year, name, specs, price


def shadow_card(base, box, radius=30, blur=26, alpha=70):
    sh = Image.new("L", base.size, 0)
    x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle([x0, y0 + 14, x1, y1 + 14], radius=radius, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    base = Image.composite(Image.new("RGB", base.size, (10, 16, 26)), base, sh)
    ImageDraw.Draw(base).rounded_rectangle(box, radius=radius, fill=CARD)
    return base


def hero(photo, car, size=(W, H)):
    w, h = size
    im = ImageOps.fit(photo, (w, h), Image.LANCZOS, centering=(0.5, 0.42))
    year, name, specs, price = car_bits(car)
    card_h = 340
    box = (M, h - M - card_h, w - M, h - M)
    im = shadow_card(im, box)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box
    px = 44
    # label
    tag = (car.get("tagline") or "For sale  ·  Perth").upper()
    spaced(d, (x0 + px, y0 + 38), tag, font(22, 700), ORANGE, tracking=2)
    # model + price on one line
    pf = fit_font(d, price, 800, 54, 300)
    pw = d.textlength(price, font=pf)
    nf = fit_font(d, f"{year} {name}", 800, 56, (x1 - x0) - 2 * px - pw - 30)
    d.text((x0 + px, y0 + 78), f"{year} {name}", font=nf, fill=INK)
    d.text((x1 - px, y0 + 78 + (nf.size - pf.size) * 0.6), price, font=pf, fill=ORANGE, anchor="ra")
    # specs
    sf = fit_font(d, specs, 500, 30, (x1 - x0) - 2 * px)
    d.text((x0 + px, y0 + 78 + nf.size + 22), specs, font=sf, fill=MUTED)
    # divider + footer
    ly = y1 - 118
    d.line([x0 + px, ly, x1 - px, ly], fill=(226, 228, 232), width=2)
    lg = logo(LOGO_NAVY, 210)
    im.paste(lg, (x0 + px, ly + (118 - lg.height) // 2), lg)
    d.text((x1 - px, ly + 26), "0434 137 393", font=font(36, 800), fill=INK, anchor="ra")
    d.text((x1 - px, ly + 72), "530 Albany Hwy, Victoria Park", font=font(22, 500), fill=MUTED, anchor="ra")
    return im


def story(photo, car):
    # 9:16: the 4:5 photo on a soft, blurred version of itself (no new content added)
    p = ImageOps.fit(photo, (SW, round(SW * photo.height / photo.width)), Image.LANCZOS)
    canvas = ImageOps.fit(photo, (SW, SH), Image.LANCZOS).filter(ImageFilter.GaussianBlur(60))
    top = 150
    feather = Image.new("L", p.size, 255)
    fd = ImageDraw.Draw(feather)
    for i in range(80):
        v = int(255 * i / 80)
        fd.line([(0, i), (p.width, i)], fill=v)
        fd.line([(0, p.height - 1 - i), (p.width, p.height - 1 - i)], fill=v)
    canvas.paste(p, (0, top), feather)
    return hero(canvas, car, size=(SW, SH))


def slide(photo, label, n, total):
    im = ImageOps.fit(photo, (W, H), Image.LANCZOS)
    # frosted label bottom-left
    f = font(26, 700)
    d = ImageDraw.Draw(im)
    tw = d.textlength(label, font=f)
    bx = (M, H - M - 64, M + tw + 52, H - M)
    region = im.crop(bx).filter(ImageFilter.GaussianBlur(16))
    tint = Image.new("RGB", region.size, NAVY)
    region = Image.blend(region, tint, 0.55)
    mask = Image.new("L", region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, region.width - 1, region.height - 1], radius=32, fill=255)
    im.paste(region, bx[:2], mask)
    d = ImageDraw.Draw(im)
    d.text((bx[0] + 26, bx[1] + 32), label, font=f, fill=WHITE, anchor="lm")
    # counter + small logo pill bottom-right
    lg = logo(LOGO_WHITE, 150)
    px0 = W - M - lg.width - 40
    pill = (px0, H - M - 64, W - M, H - M)
    region = im.crop(pill).filter(ImageFilter.GaussianBlur(16))
    region = Image.blend(region, Image.new("RGB", region.size, NAVY), 0.55)
    mask = Image.new("L", region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, region.width - 1, region.height - 1], radius=32, fill=255)
    im.paste(region, pill[:2], mask)
    im.paste(lg, (px0 + 20, H - M - 32 - lg.height // 2), lg)
    # slide counter top-right, tiny
    ImageDraw.Draw(im).text((W - M, M), f"{n:02d} / {total:02d}", font=font(22, 600), fill=(255, 255, 255), anchor="ra",
                            stroke_width=2, stroke_fill=(40, 48, 60))
    return im


def closing(car):
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    year, name, specs, price = car_bits(car)
    lg = logo(LOGO_WHITE, 420)
    im.paste(lg, ((W - lg.width) // 2, 400), lg)
    d.line([(W // 2 - 40, 600), (W // 2 + 40, 600)], fill=ORANGE, width=6)
    d.text((W // 2, 690), "Come and see it in person", font=font(52, 800), fill=WHITE, anchor="mm")
    d.text((W // 2, 760), f"{year} {name}  ·  {price}", font=fit_font(d, f"{year} {name}  ·  {price}", 500, 32, W - 2 * M),
           fill=(200, 210, 224), anchor="mm")
    d.rounded_rectangle([W // 2 - 300, 860, W // 2 + 300, 970], radius=55, fill=ORANGE)
    d.text((W // 2, 915), "Call 0434 137 393", font=font(46, 800), fill=WHITE, anchor="mm")
    d.text((W // 2, 1050), "530 Albany Highway, Victoria Park WA", font=font(32, 600), fill=WHITE, anchor="mm")
    d.text((W // 2, 1100), "Inspections welcome", font=font(28, 500), fill=(200, 210, 224), anchor="mm")
    d.text((W // 2, H - 90), "Monsoor Motors Pty Ltd  ·  MV Dealer Licence MD32748", font=font(22, 500),
           fill=(150, 165, 185), anchor="mm")
    return im


def main():
    folder = sys.argv[1]
    cfg = yaml.safe_load(open(os.path.join(folder, "car.yaml")))
    car = cfg.get("car", {})
    bs = cfg["branded_set"]
    src = os.path.join(folder, bs.get("source", "Studio/stills"))
    out = os.path.join(folder, bs.get("out", "Branded"))
    os.makedirs(out, exist_ok=True)
    load = lambda f: ImageOps.exif_transpose(Image.open(os.path.join(src, f))).convert("RGB")

    hp = load(bs["hero"])
    slides = bs.get("slides", [])
    total = len(slides) + 2
    hero(hp, car).save(os.path.join(out, "01_hero.jpg"), quality=94)
    story(hp, car).save(os.path.join(out, "story_9x16.jpg"), quality=94)
    for i, s in enumerate(slides, start=2):
        slug = s["label"].lower().replace(" ", "_").replace("·", "").replace(",", "").replace("'", "")
        slide(load(s["file"]), s["label"], i, total).save(os.path.join(out, f"{i:02d}_{slug}.jpg"), quality=94)
    closing(car).save(os.path.join(out, f"{total:02d}_visit_us.jpg"), quality=94)
    print("branded set:", out, total, "slides + story")


if __name__ == "__main__":
    main()
