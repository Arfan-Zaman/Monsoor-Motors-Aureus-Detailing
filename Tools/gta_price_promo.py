"""GTA-style price promo for a stock car (free, local).

Makes:
  - a 1080x1350 Facebook post image (hero photo, logo top-left, big GTA-green price, odometer HUD)
  - a 1080x1920 reel (photo push-ins, odometer counter over the real dash photo, money-counter price slam)

Usage:
  python -I Tools/gta_price_promo.py CONFIG.json
CONFIG keys: out_dir, title, sub, price (int), odo (int), note, phone, web,
             hero, odo_photo, shots (list of photo paths), logo
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

PRICEDOWN = os.path.expanduser("~/Library/Fonts/PricedownBl.otf")
MONT = os.path.expanduser("~/Library/Fonts/Montserrat-Variable.ttf")
GREEN = (114, 204, 114)      # GTA money green
GREEN_D = (38, 110, 52)
YELLOW = (255, 199, 44)      # mission-passed yellow
WHITE = (247, 245, 242)
BLACK = (8, 8, 10)
ORANGE = (255, 95, 21)       # Monsoor accent


def font(path, size, bold=False):
    f = ImageFont.truetype(path, size)
    if bold and path == MONT:
        try:
            f.set_variation_by_name("Bold")
        except Exception:
            pass
    return f


def cover(img, w, h, fx=0.5, fy=0.5, zoom=1.0):
    s = max(w / img.width, h / img.height) * zoom
    r = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = int((r.width - w) * fx)
    y = int((r.height - h) * fy)
    return r.crop((x, y, x + w, y + h))


def gta_text(draw, xy, text, f, fill, stroke, anchor="la", shadow=True):
    x, y = xy
    if shadow:
        draw.text((x + stroke * 0.6, y + stroke * 0.9), text, font=f, fill=(0, 0, 0, 160),
                  stroke_width=stroke, stroke_fill=(0, 0, 0, 160), anchor=anchor)
    draw.text((x, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=BLACK, anchor=anchor)


def money(v):
    return "$" + f"{v:,}"


def vignette(w, h, top=0.18, bottom=0.55, strength=235):
    g = np.zeros((h, w), np.float32)
    y = np.linspace(0, 1, h)[:, None]
    g += np.clip((top - y) / top, 0, 1) ** 1.6 * 0.75
    g += np.clip((y - (1 - bottom)) / bottom, 0, 1) ** 1.3
    a = (np.clip(g, 0, 1) * strength).astype(np.uint8)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    layer.putalpha(Image.fromarray(a))
    return layer


def logo_img(path, width):
    lg = Image.open(path).convert("RGBA")
    return lg.resize((width, round(lg.height * width / lg.width)), Image.LANCZOS)


def hud_pill(base, xy, label, value, scale=1.0):
    """GTA-style dark HUD box: small label over a big value."""
    d = ImageDraw.Draw(base)
    fl = font(PRICEDOWN, int(40 * scale))
    fv = font(PRICEDOWN, int(78 * scale))
    x, y = xy
    wv = d.textlength(value, font=fv)
    wl = d.textlength(label, font=fl)
    w = int(max(wv, wl) + 56 * scale)
    h = int(150 * scale)
    box = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(box)
    bd.rectangle((0, 0, w, h), fill=(0, 0, 0, 175))
    bd.rectangle((0, 0, int(8 * scale), h), fill=WHITE + (255,))
    base.alpha_composite(box, (x, y))
    gta_text(d, (x + 30 * scale, y + 10 * scale), label, fl, WHITE, int(3 * scale), shadow=False)
    gta_text(d, (x + 30 * scale, y + 52 * scale), value, fv, WHITE, int(4 * scale), shadow=False)
    return w, h


def poster(cfg):
    W, H = 1080, 1350
    hero = Image.open(cfg["hero"]).convert("RGB")
    # Blurred, darkened fill of the same photo, then the full photo in the middle (whole car visible)
    base = cover(hero, W, H).filter(ImageFilter.GaussianBlur(28)).convert("RGBA")
    base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 120)))
    ph = round(hero.height * W / hero.width)
    top = 150
    photo = hero.resize((W, ph), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (W, ph), 255)
    md = ImageDraw.Draw(m)
    for i in range(60):  # soft fade at the photo's bottom edge
        md.line((0, ph - 60 + i, W, ph - 60 + i), fill=int(255 * (1 - i / 60)))
    photo.putalpha(m)
    base.alpha_composite(photo, (0, top))
    base.alpha_composite(vignette(W, H, top=0.12, bottom=0.36, strength=245))
    d = ImageDraw.Draw(base)

    # Logo top-left
    base.alpha_composite(logo_img(cfg["logo"], 300), (40, 36))

    # Odometer HUD top-right
    fv = font(PRICEDOWN, 62)
    w_est = int(d.textlength(f"{cfg['odo']:,} KM", font=fv) + 0.8 * 56)
    hud_pill(base, (W - w_est - 36, 24), "ODOMETER", f"{cfg['odo']:,} KM", scale=0.8)
    d = ImageDraw.Draw(base)

    # Title
    gta_text(d, (W // 2, 1002), cfg["title"], font(PRICEDOWN, 92), WHITE, 6, anchor="ms")
    gta_text(d, (W // 2, 1052), cfg["sub"], font(PRICEDOWN, 46), YELLOW, 4, anchor="ms")

    # Price, highlighted on a black slash band
    fp = font(PRICEDOWN, 190)
    ptxt = money(cfg["price"])
    tw = d.textlength(ptxt, font=fp)
    band = Image.new("RGBA", (int(tw + 150), 132), (0, 0, 0, 0))
    ImageDraw.Draw(band).polygon([(28, 0), (band.width, 0), (band.width - 28, 132), (0, 132)], fill=(0, 0, 0, 215))
    base.alpha_composite(band, (int(W / 2 - band.width / 2), 1078))
    d = ImageDraw.Draw(base)
    gta_text(d, (W // 2, 1208), ptxt, fp, GREEN, 8, anchor="ms")
    d.text((W // 2, 1244), cfg["note"], font=font(MONT, 25, bold=True), fill=WHITE, anchor="ms",
           stroke_width=2, stroke_fill=BLACK)

    # Footer
    gta_text(d, (W // 2, 1300), cfg["phone"], font(PRICEDOWN, 50), WHITE, 4, anchor="ms")
    d.text((W // 2, 1336), cfg["web"], font=font(MONT, 22, bold=True), fill=WHITE, anchor="ms",
           stroke_width=2, stroke_fill=BLACK)
    d.text((W - 14, top + ph - 80), "Background digitally edited", font=font(MONT, 15), fill=(225, 225, 225), anchor="rs")
    out = os.path.join(cfg["out_dir"], cfg.get("name", "GTA-Price-Post") + ".jpg")
    base.convert("RGB").save(out, quality=94)
    return out


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def reel(cfg):
    W, H, FPS = 1080, 1920, 30
    shots = [Image.open(p).convert("RGB") for p in cfg["shots"]]
    odo_img = Image.open(cfg["odo_photo"]).convert("RGB")
    hero = Image.open(cfg["hero"]).convert("RGB")
    lg = logo_img(cfg["logo"], 300)
    # timeline (seconds): shot cuts vary in length (human rhythm), then odo, then price
    plan = [(shots[0], 1.9, (0.42, 0.5)), (shots[1], 1.4, (0.5, 0.5)), (shots[2], 2.2, (0.5, 0.5)),
            (shots[3], 1.3, (0.5, 0.5)), ("odo", 2.6, None), ("price", 4.6, None)]
    total = sum(p[1] for p in plan)
    n = int(total * FPS)
    out = os.path.join(cfg["out_dir"], "Kluger-GTA-Price-Reel-1080x1920.mp4")
    silent = out.replace(".mp4", "-silent.mp4")
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt",
                             "yuv420p", "-crf", "18", "-preset", "medium", silent], stdin=subprocess.PIPE)
    fp_big = font(PRICEDOWN, 250)
    ftitle = font(PRICEDOWN, 110)
    fsub = font(PRICEDOWN, 56)
    fnote = font(MONT, 30, bold=True)
    fph = font(PRICEDOWN, 72)
    fsm = font(MONT, 20)
    events = []  # (time, kind) for the sound
    t0 = 0.0
    seg_start = []
    for item in plan:
        seg_start.append(t0)
        t0 += item[1]
    for i in range(n):
        t = i / FPS
        k = max(j for j in range(len(plan)) if seg_start[j] <= t)
        src, dur, focus = plan[k]
        lt = (t - seg_start[k]) / dur
        if src == "odo":
            frame = cover(odo_img, W, H, 0.5, 0.42, zoom=1.0 + 0.10 * lt).convert("RGBA")
        elif src == "price":
            frame = cover(hero, W, H, 0.42, 0.5, zoom=1.04 + 0.05 * lt).convert("RGBA")
        else:
            frame = cover(src, W, H, focus[0], focus[1], zoom=1.02 + 0.06 * lt).convert("RGBA")
        frame.alpha_composite(vignette(W, H, top=0.16, bottom=0.45 if src == "price" else 0.25,
                                       strength=230 if src == "price" else 150))
        d = ImageDraw.Draw(frame)
        frame.alpha_composite(lg, (40, 250))  # top-left, below the app's top safe area

        if src not in ("odo", "price"):
            if k == 0:
                a = ease(lt * 3)
                gta_text(d, (W // 2, int(1380 + 40 * (1 - a))), cfg["title"], ftitle, WHITE, 6, anchor="ms")
                gta_text(d, (W // 2, int(1450 + 40 * (1 - a))), cfg["sub"], fsub, YELLOW, 4, anchor="ms")
        elif src == "odo":
            p = ease(lt / 0.7)
            val = int(cfg["odo"] * p)
            w, h = hud_pill(frame, (W // 2 - 300, 1250), "ODOMETER", f"{val:,} KM", scale=1.45)
        else:
            # Price slam: money counter rolls up, then a pop + "MISSION PASSED"-style banner
            roll = ease(lt / 0.45)
            val = int(round(cfg["price"] * roll))
            slam = 1.0 + 0.35 * max(0.0, 1 - (lt - 0.45) / 0.12) if lt >= 0.45 else 1.0
            f = font(PRICEDOWN, int(250 * slam)) if slam > 1.0 else fp_big
            banner_a = ease((lt - 0.5) / 0.15)
            if banner_a > 0:
                bw = int(900 * banner_a)
                band = Image.new("RGBA", (max(bw, 1), 120), (0, 0, 0, 0))
                ImageDraw.Draw(band).rectangle((0, 0, bw, 120), fill=(0, 0, 0, 190))
                frame.alpha_composite(band, (W // 2 - bw // 2, 1060))
                d = ImageDraw.Draw(frame)
                if banner_a > 0.9:
                    gta_text(d, (W // 2, 1148), "PRICE UNLOCKED", font(PRICEDOWN, 92), YELLOW, 5, anchor="ms")
            gta_text(d, (W // 2, 1400), money(val), f, GREEN, 10, anchor="ms")
            if lt > 0.55:
                d.text((W // 2, 1450), cfg["note"], font=fnote, fill=WHITE, anchor="ms",
                       stroke_width=2, stroke_fill=BLACK)
                gta_text(d, (W // 2, 1530), f"{cfg['odo']:,} KM  -  {cfg['sub']}", fsub, WHITE, 4, anchor="ms")
            if lt > 0.68:
                gta_text(d, (W // 2, 1640), cfg["phone"], fph, WHITE, 5, anchor="ms")
                d.text((W // 2, 1685), cfg["web"], font=fnote, fill=WHITE, anchor="ms",
                       stroke_width=2, stroke_fill=BLACK)
        if src == "price":
            d.text((W - 20, H - 20), "Background digitally edited", font=fsm, fill=(230, 230, 230), anchor="rs")
        proc.stdin.write(np.asarray(frame.convert("RGB")).tobytes())
    proc.stdin.close()
    proc.wait()

    # Sound: soft room tone, whooshes on cuts, odometer ticks, cash-counter ticks and a "ding" on the slam
    sr = 48000
    audio = np.random.randn(int(total * sr)).astype(np.float32) * 0.004
    rng = np.random.default_rng(3)

    def add(at, sig):
        s = int(at * sr)
        e = min(len(audio), s + len(sig))
        audio[s:e] += sig[: e - s]

    def whoosh(d=0.35):
        x = rng.standard_normal(int(d * sr)).astype(np.float32)
        env = np.sin(np.linspace(0, np.pi, len(x))) ** 2
        x = np.convolve(x, np.ones(40) / 40, mode="same")
        return x * env * 0.25

    def tick(f=2600, d=0.018, amp=0.18):
        tt = np.arange(int(d * sr)) / sr
        return (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 220) * amp).astype(np.float32)

    for j in range(1, len(plan)):
        add(seg_start[j] - 0.12, whoosh())
    so = seg_start[4]
    for q in np.linspace(0, 0.7 * plan[4][1], 34):
        add(so + q, tick(1800, amp=0.12))
    sp = seg_start[5]
    for q in np.linspace(0, 0.45 * plan[5][1], 40):
        add(sp + q, tick(3100, amp=0.14))
    tt = np.arange(int(1.4 * sr)) / sr
    ding = (np.sin(2 * np.pi * 1318 * tt) + 0.6 * np.sin(2 * np.pi * 1975 * tt)) * np.exp(-tt * 3.2) * 0.22
    add(sp + 0.45 * plan[5][1], ding.astype(np.float32))
    thump = np.sin(2 * np.pi * 70 * tt[: int(0.3 * sr)]) * np.exp(-tt[: int(0.3 * sr)] * 14) * 0.5
    add(sp + 0.45 * plan[5][1], thump.astype(np.float32))
    audio = np.clip(audio, -1, 1)
    wav = out.replace(".mp4", ".wav")
    import wave
    with wave.open(wav, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes((audio * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
    os.remove(silent); os.remove(wav)
    return out


if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    os.makedirs(cfg["out_dir"], exist_ok=True)
    print(poster(cfg))
    if "--no-reel" not in sys.argv:
        print(reel(cfg))
