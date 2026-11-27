"""Turn studio stills + interior photos into the Facebook/Instagram sell-post set.

  /opt/miniconda3/bin/python -I make_posts.py <car folder>

Needs car_studio.py run first (Studio/masks, plates). Writes <car folder>/Studio/posts/:
  01_hero.jpg            branded card (4:5): car in studio + model, km, price, contacts
  02..06_<view>.jpg      clean studio stills with a small logo
  07+_interior_*.jpg     interior photos, light colour correction + small logo
  story_hero.jpg         9:16 story version of the hero
  caption.txt            Facebook caption draft (fill any [BRACKETS])
Missing details in car.yaml show as [BRACKETS] so nothing is guessed.
"""
import os, sys
import yaml
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import car_studio as cs

FONT = os.path.join(HERE, "assets", "Montserrat-Variable.ttf")
LOGO = os.path.join(HERE, "assets", "Monsoor-Logo-Horizontal-White.png")
NAVY, ORANGE, WHITE = (15, 39, 71), (255, 95, 21), (247, 245, 242)
W, H = cs.OUT_SIZE
L, R = 90, W - 90


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight])
    return f


def fit(d, text, weight, size, maxw):
    f = font(size, weight)
    while d.textlength(text, font=f) > maxw and size > 20:
        size -= 2; f = font(size, weight)
    return f


def logo(w):
    lg = Image.open(LOGO).convert("RGBA")
    return lg.resize((w, round(w * lg.height / lg.width)), Image.LANCZOS)


def watermark(im, w=300, opacity=0.8, corner="br"):
    lg = logo(w)
    a = lg.getchannel("A").point(lambda v: int(v * opacity)); lg.putalpha(a)
    # soft dark backing so the white logo reads on light backgrounds
    pad = 26
    x = im.width - lg.width - 60 if corner == "br" else 60
    y = im.height - lg.height - 60
    sh = Image.new("L", im.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle([x - pad, y - pad, x + lg.width + pad, y + lg.height + pad], radius=24, fill=110)
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    im = Image.composite(Image.new("RGB", im.size, (12, 22, 38)), im, sh)
    im.paste(lg, (x, y), lg)
    return im


def val(car, key, fmt="{}", blank=None):
    v = car.get(key)
    if v in (None, ""):
        return blank if blank is not None else f"[{key.upper().replace('_', ' ')}]"
    return fmt.format(v)


def hero_card(still, car, headline, size=(W, H)):
    w, h = size
    im = still.copy()
    d = ImageDraw.Draw(im)
    top = int(h * 0.755)
    d.rectangle([0, top, w, h], fill=NAVY)
    d.rectangle([0, top, w, top + 10], fill=ORANGE)

    name = " ".join(x for x in (val(car, "year"), car.get("make", ""), val(car, "model")) if x)
    y = top + 52
    if headline:
        hw, ho = headline
        f = fit(d, hw + ho, 800, 86, R - L)
        d.text((L, y), hw, font=f, fill=WHITE)
        d.text((L + d.textlength(hw, font=f), y), ho, font=f, fill=ORANGE)
        y += f.size + 26
    f2 = fit(d, name, 700, 56, R - L - 360)
    d.text((L, y), name, font=f2, fill=WHITE)
    price = val(car, "price", "${:,}") if isinstance(car.get("price"), (int, float)) else val(car, "price")
    fp = fit(d, price, 800, 64, 340)
    d.text((R, y - 4), price, font=fp, fill=ORANGE, anchor="ra")
    y += f2.size + 26

    chips = [val(car, "km", "{:,} km") if isinstance(car.get("km"), int) else val(car, "km", "{} km"),
             val(car, "transmission"), val(car, "rego_until", "Rego to {}")]
    x = L
    fc = font(30, 700)
    for c in chips:
        tw = d.textlength(c.upper(), font=fc)
        d.rounded_rectangle([x, y, x + tw + 48, y + 58], radius=29, outline=WHITE, width=3)
        d.text((x + 24, y + 29), c.upper(), font=fc, fill=WHITE, anchor="lm")
        x += tw + 48 + 18
    y += 58 + 34
    d.line([L, y, R, y], fill=(70, 90, 120), width=2)
    y += 26
    lg = logo(300)
    im.paste(lg, (L, y), lg)
    d.text((R, y + 10), "Call 0434 137 393", font=font(40, 800), fill=WHITE, anchor="ra")
    d.text((R, y + 64), "530 Albany Hwy, Victoria Park  ·  Licence MD32748", font=font(26, 500),
           fill=(205, 212, 222), anchor="ra")
    return im


def interior(path, out, size=(W, H)):
    im = cs.load(path)
    # light, natural correction only: grey-world white balance at 50% strength + mild lift
    import numpy as np
    a = np.asarray(im).astype(np.float32)
    means = a.reshape(-1, 3).mean(0)
    gain = 1 + 0.5 * (means.mean() / means - 1)
    a = np.clip(a * gain, 0, 255).astype(np.uint8)
    im = Image.fromarray(a)
    im = ImageEnhance.Brightness(im).enhance(1.04)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    im = ImageOps.fit(im, size, Image.LANCZOS, centering=(0.5, 0.5))
    return watermark(im, w=260)


def caption(car, cfg):
    name = " ".join(x for x in (val(car, "year"), car.get("make", ""), val(car, "model")) if x)
    lines = [f"{name} for sale in Perth", "",
             f"• {val(car, 'km', '{:,}') if isinstance(car.get('km'), int) else val(car, 'km')} km",
             f"• {val(car, 'transmission')}, {val(car, 'colour')}",
             f"• Rego to {val(car, 'rego_until')}"]
    for extra in cfg.get("features", []) or []:
        lines.append(f"• {extra}")
    if cfg.get("condition_notes"):
        lines += ["", "Honest condition notes (all shown in the photos):"]
        lines += [f"• {n}" for n in cfg["condition_notes"]]
    price = val(car, "price", "${:,}") if isinstance(car.get("price"), (int, float)) else val(car, "price")
    lines += ["", f"Price: {price}", "",
              "Inspections welcome at 530 Albany Highway, Victoria Park.",
              "Call or message 0434 137 393.",
              "Monsoor Motors Pty Ltd · MV Dealer Licence MD32748"]
    return "\n".join(lines)


def main():
    folder = sys.argv[1]
    cfg = yaml.safe_load(open(os.path.join(folder, "car.yaml")))
    car = cfg.get("car", {})
    st = os.path.join(folder, "Studio")
    out = os.path.join(st, "posts")
    os.makedirs(out, exist_ok=True)
    masks = os.path.join(st, "masks")
    ext = {s["view"]: s for s in cfg.get("exterior", [])}
    hero_view = cfg.get("hero", "front34")
    headline = cfg.get("headline")  # e.g. ["Luxury. Comfort. ", "Value."]

    # hero: car a little smaller and higher so the info panel sits under the tyres
    hs = ext[hero_view]
    tmp = os.path.join(st, "stills", "_hero_base.jpg")
    cs.composite(os.path.join(folder, hs["file"]), hero_view, hero_view, tmp, masks,
                 framing={"width": 0.86, "ground": 0.70}, scale_adj=float(hs.get("scale", 1.0)))
    hero_card(Image.open(tmp).convert("RGB"), car, headline).save(os.path.join(out, "01_hero.jpg"), quality=93)

    # story 9:16: hero card on top of extended studio
    base = Image.open(tmp).convert("RGB")
    story = Image.new("RGB", (1152, 2048), (90, 90, 92))
    sb = ImageOps.fit(base, (1152, 1440), Image.LANCZOS, centering=(0.5, 0.6))
    story.paste(sb, (0, 250))
    top = ImageOps.fit(base.crop((0, 0, base.width, 300)), (1152, 260), Image.LANCZOS)
    story.paste(top.filter(ImageFilter.GaussianBlur(30)), (0, 0))
    card = hero_card(story, car, headline, size=(1152, 2048))
    card.save(os.path.join(out, "story_hero.jpg"), quality=93)
    os.remove(tmp)

    n = 2
    for view in ("front", "side", "rear34", "rear", "front34"):
        if view not in ext:
            continue
        p = os.path.join(st, "stills", f"{view}.jpg")
        if not os.path.exists(p):
            continue
        watermark(Image.open(p).convert("RGB")).save(os.path.join(out, f"{n:02d}_{view}.jpg"), quality=93)
        n += 1
    for it in cfg.get("interior", []) or []:
        slug = it.get("label", "interior").lower().replace(" ", "_").replace("'", "")
        interior(os.path.join(folder, it["file"]), None).save(os.path.join(out, f"{n:02d}_interior_{slug}.jpg"), quality=92)
        n += 1
    open(os.path.join(out, "caption.txt"), "w").write(caption(car, cfg))
    print("posts:", out, n - 1, "images")


if __name__ == "__main__":
    main()
