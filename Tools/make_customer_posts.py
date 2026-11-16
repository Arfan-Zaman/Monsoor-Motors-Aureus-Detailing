"""Colour-grade customer photos lightly and lay them into the Happy Customer
template so people and car sit in the clear area above the text and footer."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter

BASE = Path("/Users/mdarfanuzzaman/Documents/Monsoor Motors")
SRC = BASE / "Customer Images"
KIT = BASE / "Brand Kit"
OVERLAY = KIT / "02 Social Media/Post Templates/02-Happy-Customer-Overlay.png"
FONT = KIT / "00 Fonts/Montserrat-Variable.ttf"
OUT_POSTS = BASE / "Ready Posts/Upload Ready"
OUT_GRADED = BASE / "Ready Posts/Colour Graded Photos"
W, H = 1080, 1350
SAFE_TOP, SAFE_BOTTOM = 150, 935  # below the tag, above the headline

# file stamp, car, output name, subject top/bottom as a fraction of photo height
POSTS = [
    ("12.10.42 AM", "Hyundai i30", "01-Hyundai-i30", 0.45, 0.84),
    ("12.10.43 AM (2)", "Kia Rio", "02-Kia-Rio-A", 0.33, 0.86),
    ("12.10.43 AM (1)", "Kia Rio", "03-Kia-Rio-B", 0.42, 0.74),
    ("12.10.43 AM", "Toyota Yaris", "04-Toyota-Yaris", 0.47, 0.97),
    ("12.10.48 AM (1)", "Mazda CX-5", "05-Mazda-CX-5-A", 0.45, 0.98),
    ("12.10.48 AM", "Mazda CX-5", "06-Mazda-CX-5-B", 0.43, 0.985),
    ("12.10.49 AM", "BMW X1", "07-BMW-X1", 0.47, 0.955),
    ("12.10.50 AM", "Toyota Prado", "08-Toyota-Prado", 0.44, 0.97),
]


# number plate boxes (x0, y0, x1, y1) in original-photo pixels, per output name
PLATES = {
    "01-Hyundai-i30": [(733, 1183, 867, 1236), (38, 966, 109, 991)],
    "02-Kia-Rio-A": [(664, 1172, 856, 1252), (80, 769, 128, 785), (336, 788, 360, 807)],
    "03-Kia-Rio-B": [(605, 1052, 739, 1100), (67, 826, 128, 847)],
    "04-Toyota-Yaris": [(477, 1260, 645, 1348), (1180, 1035, 1200, 1065)],
    "05-Mazda-CX-5-A": [(512, 1300, 699, 1372), (200, 879, 256, 895)],
    "06-Mazda-CX-5-B": [(520, 1300, 707, 1372), (216, 884, 272, 900)],
    "07-BMW-X1": [(440, 1372, 656, 1460), (1140, 840, 1165, 868), (1185, 856, 1215, 878)],
    "08-Toyota-Prado": [(584, 1116, 755, 1180), (131, 841, 165, 857), (0, 876, 24, 892)],
}


def blur_plates(img, boxes):
    """Blur each plate with a padded, soft-edged mask so no characters are readable."""
    img = img.copy()
    for x0, y0, x1, y1 in boxes:
        pad = max(6, round((y1 - y0) * 0.25))
        x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
        x1, y1 = min(img.width, x1 + pad), min(img.height, y1 + pad)
        region = img.crop((x0, y0, x1, y1))
        r = max(6, (y1 - y0) // 3)
        blurred = region.filter(ImageFilter.GaussianBlur(r)).filter(ImageFilter.GaussianBlur(r))
        mask = Image.new("L", region.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            (pad // 2, pad // 2, region.width - pad // 2, region.height - pad // 2),
            radius=pad, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(pad / 3))
        img.paste(Image.composite(blurred, region, mask), (x0, y0))
    return img


def grade(img):
    """Gentle polish: warmth, soft contrast, lifted shadows, light vibrance, crispness."""
    a = np.asarray(img).astype(np.float32) / 255.0
    # slight warmth
    a[..., 0] *= 1.025
    a[..., 2] *= 0.98
    a = np.clip(a, 0, 1)
    # soft S-curve contrast with lifted shadows and protected highlights
    a = a + 0.10 * a * (1 - a) * (a - 0.35) * 2.0
    a = 0.02 + a * 0.975
    a = np.clip(a, 0, 1)
    # light vibrance: boost muted colours more than already-strong ones
    mean = a.mean(axis=2, keepdims=True)
    sat = (a.max(axis=2, keepdims=True) - a.min(axis=2, keepdims=True))
    a = mean + (a - mean) * (1 + 0.12 * (1 - sat))
    a = np.clip(a, 0, 1)
    out = Image.fromarray((a * 255 + 0.5).astype(np.uint8))
    return out.filter(ImageFilter.UnsharpMask(radius=1.6, percent=35, threshold=3))


def place(photo, top_f, bot_f):
    """Fit photo to canvas width and slide it so the subject sits in the safe zone.
    Any canvas left uncovered at the bottom (under the dark gradient and footer)
    is filled with a blurred mirror of the ground."""
    s = W / photo.width
    img = photo.resize((W, round(photo.height * s)), Image.LANCZOS)
    top, bot = top_f * img.height, bot_f * img.height
    centre = (SAFE_TOP + SAFE_BOTTOM) / 2
    y = round(centre - (top + bot) / 2)
    y = min(y, 0)                             # never leave a gap at the top
    y = max(y, SAFE_TOP - round(top))         # keep heads below the tag
    canvas = Image.new("RGB", (W, H))
    canvas.paste(img, (0, y))
    gap_top = y + img.height
    if gap_top < H:
        need = H - gap_top
        strip = img.crop((0, img.height - min(need, img.height), W, img.height))
        strip = ImageOps.flip(strip).filter(ImageFilter.GaussianBlur(45))
        canvas.paste(strip, (0, gap_top))
        # fade smoothly into brand navy so the extension reads as a backdrop
        a = np.asarray(canvas).astype(np.float32)
        navy = np.array([15, 39, 71], np.float32)
        rows = np.arange(H, dtype=np.float32)
        start, end = gap_top - 30, gap_top + 170
        w = np.clip((rows - start) / (end - start), 0, 1) ** 1.3 * 0.9
        a = a * (1 - w[:, None, None]) + navy * w[:, None, None]
        canvas = Image.fromarray(a.astype(np.uint8))
    return canvas, y + bot


def font(size, weight):
    f = ImageFont.truetype(str(FONT), size)
    f.set_variation_by_axes([weight])
    return f


def main():
    OUT_POSTS.mkdir(parents=True, exist_ok=True)
    OUT_GRADED.mkdir(parents=True, exist_ok=True)
    overlay = Image.open(OVERLAY).convert("RGBA")
    head, sub = font(72, 800), font(34, 500)
    for stamp, car, name, t, b in POSTS:
        src = SRC / f"WhatsApp Image 2026-11-11 at {stamp}.jpeg"
        photo = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        graded = blur_plates(grade(photo), PLATES[name])
        graded.save(OUT_GRADED / f"{name}.jpg", quality=95)
        canvas, subj_bottom = place(graded, t, b)
        post = canvas.convert("RGBA")
        post.alpha_composite(overlay)
        d = ImageDraw.Draw(post)
        d.text((48, 1068), "Congratulations!", font=head, fill="white", anchor="ls")
        d.text((48, 1122), f"Enjoy your {car}. Thanks for choosing us.",
               font=sub, fill="white", anchor="ls")
        post.convert("RGB").save(OUT_POSTS / f"{name}.jpg", quality=92,
                                 optimize=True, progressive=True)
        print(f"{name}: subject bottom at y={subj_bottom:.0f}")


if __name__ == "__main__":
    main()
