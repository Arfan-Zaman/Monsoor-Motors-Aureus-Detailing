"""Monsoor Studio: put real car photos into our own Blender studio.

  /opt/miniconda3/bin/python -I car_studio.py <car folder>            # uses <car folder>/car.yaml
  /opt/miniconda3/bin/python -I car_studio.py <car folder> --only front34

The car pixels are the real photo. Nothing is generated: we only cut the car
out (BiRefNet via rembg, runs on this Mac), match exposure/white balance
lightly, add a contact shadow and a soft floor reflection, and place it on
the matching studio plate rendered by studio_scene.py (grey cove).

Outputs go to <car folder>/Studio/:
  stills/<view>.jpg      car in the studio, 1638x2048 (4:5)
  masks/<photo>.png      cached cut-out masks (delete to redo one)
"""
import glob, math, os, sys
import numpy as np
import yaml
from PIL import Image, ImageOps, ImageFilter, ImageChops, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
PLATES = os.path.join(HERE, "plates")

_session = None


def session():
    global _session
    if _session is None:
        from rembg import new_session
        _session = new_session("birefnet-general")
    return _session


def load(path):
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def get_mask(photo_path, cache_dir):
    os.makedirs(cache_dir, exist_ok=True)
    cp = os.path.join(cache_dir, os.path.splitext(os.path.basename(photo_path))[0] + ".png")
    if os.path.exists(cp):
        return Image.open(cp).convert("L")
    from rembg import remove
    m = remove(load(photo_path), session=session(), only_mask=True).convert("L")
    m.save(cp)
    return m


def clean_mask(m):
    """Keep the largest blob (the car), drop specks from other cars, soften the edge a touch."""
    import cv2
    a = np.array(m)
    _, b = cv2.threshold(a, 127, 255, cv2.THRESH_BINARY)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(b)
    if n > 1:
        keep = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        a = np.where(lab == keep, a, 0).astype(np.uint8)
    return Image.fromarray(a).filter(ImageFilter.GaussianBlur(0.8))


def blur_boxes(img, boxes):
    """boxes: [[x0,y0,x1,y1], ...] in the original photo's pixels (for number plates)."""
    for x0, y0, x1, y1 in boxes or []:
        reg = img.crop((x0, y0, x1, y1))
        small = reg.resize((max(1, (x1 - x0) // 14), max(1, (y1 - y0) // 14)), Image.BILINEAR)
        img.paste(small.resize(reg.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(4)), (x0, y0))
    return img


def light_match(car):
    """Gentle exposure/contrast only, so the sunny yard photo sits in a darker studio.
    Never changes the paint colour."""
    car = ImageEnhance.Brightness(car).enhance(0.93)
    car = ImageEnhance.Contrast(car).enhance(1.04)
    car = ImageEnhance.Color(car).enhance(0.9)  # calm the strong outdoor saturation a little
    return car


# How big the car sits in the frame, per view (fraction of output width), and where
# the tyres touch the floor (fraction of output height). Tuned to the grey cove.
FRAMING = {
    "front":   {"width": 0.66, "ground": 0.80},
    "rear":    {"width": 0.66, "ground": 0.80},
    "front34": {"width": 0.84, "ground": 0.79},
    "rear34":  {"width": 0.84, "ground": 0.79},
    "side":    {"width": 0.92, "ground": 0.76},
}
OUT_SIZE = (1638, 2048)  # 4:5 portrait, best for Facebook/Instagram feed


def spin_framing(angle):
    """Width/ground for a spin frame at this camera angle (0 = front)."""
    side = abs(math.sin(math.radians(angle)))
    return {"width": 0.50 + 0.22 * min(1.0, side * 1.3), "ground": 0.86}


def composite(photo_path, view, plate_name, out_path, mask_dir, plate_boxes=None, scale_adj=1.0, nudge_y=0.0,
              out_size=None, framing=None, erase=None):
    plate = Image.open(os.path.join(PLATES, plate_name + ".jpg")).convert("RGB")
    PW, PH = plate.size
    W, H = out_size or OUT_SIZE
    if (W, H) != (PW, PH):
        plate = plate.crop(((PW - W) // 2, PH - H, (PW - W) // 2 + W, PH))
    fr = framing or FRAMING.get(view, {"width": 0.85, "ground": 0.80})

    photo = blur_boxes(load(photo_path), plate_boxes)
    mask = get_mask(photo_path, mask_dir)
    if erase:  # background objects the cut-out wrongly kept (flags, poles): [[x0,y0,x1,y1], ...] photo pixels
        from PIL import ImageDraw
        mask = mask.copy()
        for box in erase:
            ImageDraw.Draw(mask).rectangle(box, fill=0)
    mask = clean_mask(mask)
    bbox = mask.point(lambda v: 255 if v > 40 else 0).getbbox()
    car = photo.crop(bbox)
    m = mask.crop(bbox)

    s = fr["width"] * W * scale_adj / car.width
    car = car.resize((round(car.width * s), round(car.height * s)), Image.LANCZOS)
    m = m.resize(car.size, Image.LANCZOS)
    car = light_match(car)

    bottom_y = (fr["ground"] + nudge_y) * H
    x0 = round((W - car.width) / 2)
    y0 = round(bottom_y - car.height)

    from PIL import ImageDraw
    out = plate.copy()
    # soft ambient shadow under the whole car
    sh = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(sh)
    inset = car.width * 0.04
    d.ellipse([x0 + inset, bottom_y - car.height * 0.10, x0 + car.width - inset, bottom_y + car.height * 0.06], fill=255)
    sh = sh.filter(ImageFilter.GaussianBlur(car.height * 0.06)).point(lambda v: int(v * 0.65))
    # contact shadow along the car's lowest edge in every column, so every tyre that
    # touches the floor (near and far) gets a dark line under it
    ma = np.array(m) > 100
    cols = np.where(ma.any(0))[0]
    low = np.full(car.width, -1)
    low[cols] = car.height - 1 - np.argmax(ma[::-1, cols], axis=0)
    cs_ = Image.new("L", (W, H), 0)
    cd = ImageDraw.Draw(cs_)
    thick = max(6, int(car.height * 0.025))
    tyre_zone = car.height * 0.80  # only columns whose lowest point is near the bottom (tyres, not sills)
    for x in cols:
        if low[x] >= tyre_zone:
            yb = y0 + low[x]
            cd.line([(x0 + x, yb - thick), (x0 + x, yb + thick // 2)], fill=255)
    cs_ = cs_.filter(ImageFilter.GaussianBlur(max(3, car.height * 0.012))).point(lambda v: int(v * 0.9))
    sh = ImageChops.lighter(sh, cs_)
    out = Image.composite(Image.new("RGB", (W, H), (28, 28, 30)), out, sh)

    out.paste(car, (x0, y0), m)
    # gentle vignette, like a lit studio
    vg = Image.radial_gradient("L").resize((W, H)).point(lambda v: int(min(255, v * 0.9)))
    out = Image.composite(Image.new("RGB", (W, H), (20, 20, 22)), out, vg.point(lambda v: int(v * 0.35)))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    out.save(out_path, quality=95) if out_path.endswith(".jpg") else out.save(out_path)
    return out_path


def main():
    folder = sys.argv[1]
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    cfg = yaml.safe_load(open(os.path.join(folder, "car.yaml")))
    car_cfg = cfg.get("car", {})
    out_dir = os.path.join(folder, "Studio")
    for shot in cfg.get("exterior", []):
        view = shot["view"]
        if only and view not in only:
            continue
        p = composite(os.path.join(folder, shot["file"]), view, shot.get("plate", view),
                      os.path.join(out_dir, "stills", f"{view}.jpg"), os.path.join(out_dir, "masks"),
                      plate_boxes=shot.get("plate_blur") if cfg.get("blur_plates") else None,
                      scale_adj=float(shot.get("scale", 1.0)), nudge_y=float(shot.get("nudge_y", 0.0)),
                      erase=shot.get("mask_erase"))
        print("made", p)

    if "--spin" in sys.argv:
        sp = cfg.get("spin") or {}
        photos = sorted(glob.glob(os.path.join(folder, sp.get("folder", "spin"), "*.jp*g")))
        if not photos:
            sys.exit("No spin photos: put the 36 walk-around photos in <car>/spin/ (in order, starting at the front).")
        n = len(photos)
        for i, ph in enumerate(photos):
            ang = (float(sp.get("start_angle", 0)) + i * 360 / n) % 360
            k = round(ang / 10) % 36
            p = composite(ph, "spin", f"orbit_{k:02d}", os.path.join(out_dir, "spin", f"frame_{i:02d}.jpg"),
                          os.path.join(out_dir, "masks"), out_size=(1920, 1280), framing=spin_framing(ang))
        print("spin frames:", n)


if __name__ == "__main__":
    main()
