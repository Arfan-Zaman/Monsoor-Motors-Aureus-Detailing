"""Showroom cover v2: keep the showroom (and its wall sign) exactly as supplied,
soften the over-crisp cars, add an Import / Buy / Sell banner and a corner watermark."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = Path("/Users/mdarfanuzzaman/Documents/Monsoor Motors/Facebook/Cover Photos/Source Images/Showroom-C-HR-source.webp")
BASE = Path("/Users/mdarfanuzzaman/Documents/Monsoor Motors")
KIT = BASE / "Brand Kit"
FONT = KIT / "00 Fonts/Montserrat-Variable.ttf"
WATERMARK = KIT / "01 Logo/Watermark/Watermark-White.png"
OUT = BASE / "Ready Posts/Facebook Cover"
NAVY = (15, 39, 71)
ORANGE = (255, 95, 21)
WARM = (247, 245, 242)
SOFT = (200, 208, 220)


def font(size, weight):
    f = ImageFont.truetype(str(FONT), size)
    f.set_variation_by_axes([weight])
    return f


def car_mask(size):
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle((70, 225, 830, 660), radius=60, fill=255)
    d.rounded_rectangle((1160, 240, 1940, 665), radius=60, fill=255)
    return m.filter(ImageFilter.GaussianBlur(25))


def soften_cars(img):
    a = np.asarray(img).astype(np.float32)
    fine = np.asarray(img.filter(ImageFilter.GaussianBlur(0.9))).astype(np.float32)
    broad = np.asarray(img.filter(ImageFilter.GaussianBlur(18))).astype(np.float32)
    soft = a * 0.45 + fine * 0.55                 # take the edge off over-sharp detail
    soft = broad + (soft - broad) * 0.86          # ease the hard, plasticky contrast
    soft = soft * 0.985 + 255 * 0.012             # lift the crushed blacks a touch
    m = np.asarray(car_mask(img.size)).astype(np.float32)[..., None] / 255
    out = soft * m + a * (1 - m)
    # a fine, even grain over the whole frame so cars and room read as one photo
    out += np.random.default_rng(5).normal(0, 2.0, out.shape[:2])[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def banner(img):
    W = img.width

    def panel(box, radius, alpha, shadow=True):
        x0, y0, x1, y1 = box
        if shadow:
            sh = Image.new("L", img.size, 0)
            ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + 8, x1, y1 + 10), radius=radius, fill=150)
            s = Image.new("RGBA", img.size, (0, 0, 0, 0))
            s.putalpha(sh.filter(ImageFilter.GaussianBlur(14)))
            img.alpha_composite(s)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.rounded_rectangle(box, radius=radius, fill=NAVY + (alpha,))
        d.rectangle((x0 + radius, y0, x1 - radius, y0 + 4), fill=ORANGE + (255,))
        img.alpha_composite(layer)

    # --- services card on the showroom floor, between the two cars ---
    cx0, cy0, cx1, cy1 = 828, 414, 1172, 656
    panel((cx0, cy0, cx1, cy1), 16, 232)
    d = ImageDraw.Draw(img)
    mid = (cx0 + cx1) / 2
    d.text((mid, cy0 + 34), "YOUR NEXT CAR, SORTED", font=font(14, 800), fill=ORANGE, anchor="ms")
    rows = [("IMPORT", "Hand-picked at Japanese auctions"),
            ("BUY", "Quality used cars, fair drive-away prices"),
            ("SELL", "Get a fair offer for your car")]
    y = cy0 + 74
    for i, (title, desc) in enumerate(rows):
        d.text((mid, y), title, font=font(22, 800), fill=WARM, anchor="ms")
        d.text((mid, y + 22), desc, font=font(13, 500), fill=SOFT, anchor="ms")
        if i < 2:
            d.line((mid - 18, y + 37, mid + 18, y + 37), fill=ORANGE, width=2)
        y += 58

    # --- full-width contact footer ---
    fy0 = 676
    panel((-20, fy0, W + 20, 780), 0, 240, shadow=False)
    d = ImageDraw.Draw(img)
    contacts = [("CALL", "0434 137 393"),
                ("EMAIL", "monsoormotors@gmail.com"),
                ("WEB", "monsoormotors.com.au"),
                ("VISIT US", "530 Albany Hwy, Victoria Park WA 6100")]
    lf, vf = font(12, 800), font(18, 700)
    widths = [max(d.textlength(l, font=lf), d.textlength(v, font=vf)) for l, v in contacts]
    left, right = 340, 1660                       # inside the area phones show
    gap = (right - left - sum(widths)) / (len(contacts) - 1)
    x = left
    for i, ((label, value), w) in enumerate(zip(contacts, widths)):
        d.text((x, fy0 + 34), label, font=lf, fill=ORANGE, anchor="ls")
        d.text((x, fy0 + 60), value, font=vf, fill=WARM, anchor="ls")
        if i < len(contacts) - 1:
            xd = x + w + gap / 2
            d.line((xd, fy0 + 22, xd, fy0 + 64), fill=(60, 82, 112), width=1)
        x += w + gap


def watermark(img):
    wm = Image.open(WATERMARK).convert("RGBA")
    wm = wm.crop(wm.getbbox())
    w = 250
    wm = wm.resize((w, round(wm.height * w / wm.width)), Image.LANCZOS)
    img.alpha_composite(wm, (34, 84))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    img = soften_cars(Image.open(SRC).convert("RGB")).convert("RGBA")
    banner(img)
    watermark(img)
    master = img.convert("RGB")
    master.save(OUT / "Facebook-Cover-Showroom-2000x760.png")
    cover = master.resize((1640, 624), Image.LANCZOS)
    cover.save(OUT / "Facebook-Cover-Showroom-1640x624.png")
    cover.save(OUT / "Facebook-Cover-Showroom-1640x624.jpg", quality=95)
    print("saved")


if __name__ == "__main__":
    main()
