"""Facebook cover v5 - rendered at 2x (3280x1440) so text, logo and graphics are crisp.
Layout coordinates are written at 1x (1640x720) and multiplied by K."""
from pathlib import Path
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
from showroom_cover_v2 import soften_cars, SRC, FONT, NAVY, ORANGE, WARM

BASE_DIR = Path("/Users/mdarfanuzzaman/Documents/Monsoor Motors")
OUT = BASE_DIR / "Ready Posts/Facebook Cover"
WATERMARK = BASE_DIR / "Brand Kit/01 Logo/Watermark/Watermark-White.png"
K = 2
W, H = 1640 * K, 720 * K
SAFE = (180, 48, 1460, 672)          # 1x: phones show x 180-1460, desktop shows y 48-672
LIGHT = (226, 231, 239)


def font(size, weight):
    f = ImageFont.truetype(str(FONT), round(size * K))
    f.set_variation_by_axes([weight])
    return f


def base():
    img = soften_cars(Image.open(SRC).convert("RGB"))
    img = img.resize((W, round(img.height * W / img.width)), Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.4, percent=25, threshold=3))  # undo upscale blur only
    canvas = Image.new("RGB", (W, H))
    canvas.paste(img, (0, 0))
    need = H - img.height
    if need > 0:
        strip = img.crop((0, img.height - need, W, img.height))
        strip = strip.transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(10 * K))
        canvas.paste(strip, (0, img.height))
    a = np.asarray(canvas).astype(np.float32)
    ys = np.arange(H, dtype=np.float32)[:, None, None]
    t = np.clip((ys - 470 * K) / (590 * K - 470 * K), 0, 1) ** 1.1 * 0.97
    a = a * (1 - t) + np.array(NAVY, np.float32) * t
    return Image.fromarray(a.astype(np.uint8)).convert("RGBA")


def pill(img, box, fill, outline=None):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r = (box[3] - box[1]) // 2
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=2 * K if outline else 0)
    img.alpha_composite(layer)


def pin_icon(d, cx, cy, s, colour):
    """Simple map-pin: circle head with a point, hole in the middle."""
    d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=colour)
    d.polygon([(cx - s * 0.78, cy + s * 0.55), (cx + s * 0.78, cy + s * 0.55), (cx, cy + s * 2.0)], fill=colour)
    h = s * 0.42
    d.ellipse((cx - h, cy - h, cx + h, cy + h), fill=NAVY)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    img = base()
    d = ImageDraw.Draw(img)
    cx = W / 2

    # --- top-left: logo watermark, inside the area phones show ---
    wm = Image.open(WATERMARK).convert("RGBA")
    wm = wm.crop(wm.getbbox())
    ww = 236 * K
    wm = wm.resize((ww, round(wm.height * ww / wm.width)), Image.LANCZOS)
    wx, wy = 196 * K, 66 * K
    img.alpha_composite(wm, (wx, wy))
    wm_mid = wy + wm.height / 2

    # --- top-right: local Perth dealer badge, PERTH highlighted ---
    bf = font(19, 800)
    parts = [("YOUR LOCAL ", WARM), ("PERTH", ORANGE), (" CAR DEALER", WARM)]
    tw = sum(d.textlength(t, font=bf) for t, _ in parts)
    icon = 30 * K
    pad = 22 * K
    bh = 50 * K
    bx1 = 1444 * K
    bx0 = bx1 - (pad + icon + tw + pad)
    by0 = wm_mid - bh / 2
    pill(img, (bx0, by0, bx1, by0 + bh), NAVY + (225,), outline=ORANGE + (255,))
    d = ImageDraw.Draw(img)
    pin_icon(d, bx0 + pad + 9 * K, wm_mid - 5 * K, 9 * K, ORANGE)
    x = bx0 + pad + icon
    for t, col in parts:
        d.text((x, wm_mid + 7 * K), t, font=bf, fill=col, anchor="ls")
        x += d.textlength(t, font=bf)

    # --- licence / registration: small legal line under the Perth badge ---
    lf = font(13.5, 600)
    ly = by0 + bh + 26 * K
    d.text((bx1 - 6 * K, ly), "MV Dealership Licence MD32748", font=lf, fill=LIGHT, anchor="rs")
    d.text((bx1 - 6 * K, ly + 20 * K), "Registered under Monsoor Motors Pty Ltd", font=lf,
           fill=(178, 190, 206), anchor="rs")

    # --- three service headers with orange underlines ---
    cols = [("IMPORT", "Japan auction imports"),
            ("BUY", "Quality cars & finance"),
            ("SELL", "Fair offers on your car")]
    # clear hierarchy: big headers > medium descriptors > small contact lines
    hf, df = font(46, 900), font(18, 600)
    y = 548 * K
    for (head, desc), off in zip(cols, (-330, 0, 330)):
        mx = cx + off * K
        d.text((mx, y), head, font=hf, fill=WARM, anchor="ms")
        d.rounded_rectangle((mx - 30 * K, y + 10 * K, mx + 30 * K, y + 16 * K), radius=3 * K, fill=ORANGE)
        d.text((mx, y + 39 * K), desc, font=df, fill=(206, 214, 226), anchor="ms")
    for off in (-165, 165):
        xd = cx + off * K
        d.line((xd, y - 32 * K, xd, y + 36 * K), fill=(110, 126, 150), width=K)

    # --- contact details: lighter and smaller, two centred lines clear of the profile picture ---
    def contact_row(parts, yy, f, colour):
        sep = "   ·   "
        total = sum(d.textlength(p, font=f) for p in parts) + d.textlength(sep, font=f) * (len(parts) - 1)
        x = cx - total / 2
        for i, p in enumerate(parts):
            d.text((x, yy), p, font=f, fill=colour, anchor="ls")
            x += d.textlength(p, font=f)
            if i < len(parts) - 1:
                d.text((x, yy), sep, font=f, fill=ORANGE, anchor="ls")
                x += d.textlength(sep, font=f)

    contact_row(["0434 137 393", "530 Albany Hwy, Victoria Park WA 6100"], 632 * K, font(18, 700), WARM)
    contact_row(["monsoormotors@gmail.com", "monsoormotors.com.au"], 657 * K, font(16, 500), (190, 200, 215))
    size = 18

    cover = img.convert("RGB")
    cover.save(OUT / "Facebook-Cover-3280x1440.png")  # final copy: Facebook/Cover Photos/Cover Photo 1.png
    cover.save(OUT / "Facebook-Cover-3280x1440.jpg", quality=93, optimize=True)
    small = cover.resize((1640, 720), Image.LANCZOS)
    small.save(OUT / "Facebook-Cover-1640x720.png")
    small.save(OUT / "Facebook-Cover-1640x720.jpg", quality=92, optimize=True)

    prev = small.convert("RGBA")
    ov = Image.new("RGBA", prev.size, (0, 0, 0, 0))
    o = ImageDraw.Draw(ov)
    o.rectangle((0, 0, 1640, SAFE[1]), fill=(255, 0, 0, 70))
    o.rectangle((0, SAFE[3], 1640, 720), fill=(255, 0, 0, 70))
    o.rectangle((0, 0, SAFE[0], 720), fill=(0, 120, 255, 60))
    o.rectangle((SAFE[2], 0, 1640, 720), fill=(0, 120, 255, 60))
    o.ellipse((40, 520, 330, 810), outline=(255, 255, 255, 200), width=4)
    prev.alpha_composite(ov)
    prev.convert("RGB").save(OUT / "_safe-zone-check.jpg", quality=85)
    print("contact text size", size)


if __name__ == "__main__":
    main()
