"""Animated storyboard (animatic) for the hybrid clone ad. Free: PIL + ffmpeg, no AI credits.

Run:  /opt/miniconda3/bin/python -I make_animatic.py
Out:  Hybrid-Clone-Animatic.mp4 (local only, mp4 is gitignored) + Hybrid-Clone-Storyboard.png (contact sheet)
"""
import math, os, subprocess, sys, shutil, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
FONT = os.path.join(ROOT, "Brand Kit/00 Fonts/Montserrat-Variable.ttf")
CARS = os.path.join(ROOT, "Cars/Toyota C-HR Hybrid (black)")
LOGO = os.path.join(ROOT, "Brand Kit/01 Logo/Monsoor-Logo-White.png")
LOGO_H = os.path.join(ROOT, "Brand Kit/01 Logo/Monsoor-Logo-Horizontal-White.png")
WMARK = os.path.join(ROOT, "Brand Kit/01 Logo/Watermark/Watermark-White.png")

W, H, FPS = 720, 1280, 24
NAVY, NAVY2, ORANGE, WHITE, SLATE = (15, 39, 71), (24, 56, 98), (255, 95, 21), (247, 245, 242), (140, 150, 165)
TOP, BOT = 150, 1050  # storyboard info bars: top 0-150, bottom 1050-1280


def font(size, weight=700):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def cover(img, w, h, zoom=1.0, dx=0.0, dy=0.0):
    """Crop-to-fill with zoom and pan (dx, dy in -1..1)."""
    s = max(w / img.width, h / img.height) * zoom
    im = img.resize((int(img.width * s) + 1, int(img.height * s) + 1), Image.LANCZOS)
    x = (im.width - w) / 2 * (1 + dx)
    y = (im.height - h) / 2 * (1 + dy)
    return im.crop((int(x), int(y), int(x) + w, int(y) + h))


def load(name):
    return Image.open(os.path.join(CARS, name)).convert("RGB")


IMG = {
    "chr": load("C-HR-front-three-quarter-current.jpg"),
    "chr_auc": load("C-HR-auction-front.jpg"),
    "chr_rear": load("C-HR-auction-rear-1.jpg"),
}
LOGO_IMG = Image.open(LOGO).convert("RGBA")
LOGO_H_IMG = Image.open(LOGO_H).convert("RGBA")
WM = Image.open(WMARK).convert("RGBA") if os.path.exists(WMARK) else LOGO_IMG


def paste_logo(base, img, width, xy, alpha=1.0):
    r = width / img.width
    im = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    if alpha < 1:
        a = im.split()[3].point(lambda v: int(v * alpha))
        im.putalpha(a)
    base.alpha_composite(im, xy)


def text_c(d, xy, s, f, fill=WHITE, anchor="mm", shadow=True):
    if shadow:
        d.text((xy[0] + 3, xy[1] + 3), s, font=f, fill=(0, 0, 0, 160), anchor=anchor)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def wrap(s, f, maxw, d):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


# ---------- drawing helpers for things we haven't filmed yet ----------

def figure(d, cx, base_y, scale, arm=0.0, label=True, mood="talk"):
    """Simple storyboard person (Monsoor). arm: 0 down .. 1 out-stretched."""
    s = scale
    head_r = 34 * s
    body_h = 170 * s
    hy = base_y - body_h - head_r * 2 - 120 * s
    # legs
    lw = max(3, int(9 * s))
    d.line([(cx - 18 * s, base_y - 120 * s), (cx - 28 * s, base_y)], fill=WHITE, width=lw)
    d.line([(cx + 18 * s, base_y - 120 * s), (cx + 28 * s, base_y)], fill=WHITE, width=lw)
    # body (navy polo)
    d.rounded_rectangle([cx - 55 * s, hy + head_r * 2 + 6 * s, cx + 55 * s, base_y - 110 * s], radius=int(28 * s),
                        fill=NAVY2, outline=WHITE, width=max(2, int(4 * s)))
    # small orange logo dot on chest
    d.ellipse([cx + 18 * s, hy + head_r * 2 + 30 * s, cx + 34 * s, hy + head_r * 2 + 46 * s], fill=ORANGE)
    # arms
    sh = (cx - 50 * s, hy + head_r * 2 + 26 * s)
    sh2 = (cx + 50 * s, hy + head_r * 2 + 26 * s)
    d.line([sh, (sh[0] - 25 * s, sh[1] + 120 * s)], fill=WHITE, width=lw)
    ang = math.radians(80 - 75 * arm)
    d.line([sh2, (sh2[0] + 130 * s * math.cos(ang), sh2[1] + 130 * s * math.sin(ang))], fill=WHITE, width=lw)
    # head + sunglasses
    d.ellipse([cx - head_r, hy, cx + head_r, hy + head_r * 2], fill=(214, 170, 130), outline=WHITE, width=max(2, int(3 * s)))
    d.rectangle([cx - head_r * 0.75, hy + head_r * 0.75, cx + head_r * 0.75, hy + head_r * 1.05], fill=(20, 20, 20))
    if mood == "talk":
        d.arc([cx - 12 * s, hy + head_r * 1.25, cx + 12 * s, hy + head_r * 1.7], 0, 180, fill=(60, 30, 20), width=max(2, int(3 * s)))
    else:
        d.line([(cx - 10 * s, hy + head_r * 1.5), (cx + 10 * s, hy + head_r * 1.5)], fill=(60, 30, 20), width=max(2, int(3 * s)))
    if label:
        f = font(max(14, int(18 * s)), 800)
        d.text((cx, hy - 16 * s), "MONSOOR", font=f, fill=ORANGE, anchor="mb")


def yard_bg(t, blur=6, zoom=1.15):
    bg = cover(IMG["chr"], W, BOT - TOP, zoom=zoom + 0.04 * t, dx=-0.3 + 0.2 * t)
    bg = bg.filter(ImageFilter.GaussianBlur(blur))
    ov = Image.new("RGBA", bg.size, NAVY + (110,))
    return Image.alpha_composite(bg.convert("RGBA"), ov)


def car_placeholder(d, t, name):
    cy = 620
    d.rounded_rectangle([110, cy - 70, 610, cy + 60], radius=60, outline=WHITE, width=5)
    d.polygon([(200, cy - 70), (270, cy - 150), (470, cy - 150), (540, cy - 70)], outline=WHITE, width=5)
    for x in (210, 510):
        d.ellipse([x - 45, cy + 20, x + 45, cy + 110], outline=WHITE, width=6)
    text_c(d, (W // 2, cy + 190), f"[ {name} ]", font(30, 700), fill=ORANGE)
    text_c(d, (W // 2, cy + 235), "film our real car here", font(22, 500), fill=SLATE, shadow=False)


# ---------- the 16 shots (time in seconds) ----------
SHOTS = [
    (2.5, "Walk toward camera, already talking", "Perth, if you want a Japanese hybrid, watch this before you buy.", "Japanese hybrid?", "walk"),
    (2.5, "Cutaway: our sign at 530 Albany Hwy", "We're Monsoor Motors, right here in Victoria Park.", "Victoria Park", "sign"),
    (2.5, "Arm out toward the yard", "This is our yard. Every car you see, we've hand-picked.", "Our yard", "armout"),
    (2.5, "Graphic: Japan → Perth line draws", "We bring them in from Japan…", "Japan → Perth", "map"),
    (2.5, "Close-up: auction sheet in hand", "…and we read the auction sheet before we bid.", "Graded first", "sheet"),
    (2.5, "Aureus prep: foam, then a wipe", "Then it's inspected and detailed here.", "Prepped in Perth", "foam"),
    (2.5, "Car parade 1: slow pan", "Toyota C-HR Hybrid…", "C-HR Hybrid", "car1"),
    (2.5, "Car parade 2: slow pan", "…Corolla hybrids…", "[Model]", "car2"),
    (2.5, "Car parade 3: slow pan", "…Harrier…", "[Model]", "car3"),
    (2.5, "Car parade 4: slow pan", "…Prius and more.", "[Model]", "car4"),
    (2.5, "Close-up: hybrid display / fuel gauge", "Low running costs, because that's why you want one.", "Less at the bowser", "dash"),
    (3.5, "Monsoor serious, slow push-in", "But heads-up: since December, new rules mean a lot of Japanese hybrids can't come in any more.", "Rules changed", "serious"),
    (3.0, "Phone: Drive headline + WA sticker pops", "Cars already here are fine. Some we can still import, for now.", "For now", "phone"),
    (4.0, "Gesture + big label pops (re-hook)", "Tell me the one you want and your budget, and I'll tell you straight if we can get it.", "Tell us the car", "label"),
    (4.0, "Phone / WhatsApp icon drops in", "Tap the button, or just call us.", "0434 137 393", "call"),
    (3.0, "Close nod → end card", "Honest answers, no pressure.", "No pressure", "end"),
]


def draw_scene(kind, t, base):
    """t: 0..1 progress in shot. base: RGBA canvas W x H. Draws into the picture area TOP..BOT."""
    ph = BOT - TOP
    pic = Image.new("RGBA", (W, ph), NAVY + (255,))
    d = ImageDraw.Draw(pic)

    if kind in ("walk", "armout", "serious", "label", "call"):
        pic = yard_bg(t)
        d = ImageDraw.Draw(pic)
        if kind == "walk":
            figure(d, W // 2 + 40 - 40 * t, ph - 60 + 40 * t, 1.0 + 0.55 * ease(t), arm=0.3 + 0.3 * math.sin(t * 9))
            d.text((170, 60), "→ walks to camera", font=font(22, 600), fill=ORANGE)
        elif kind == "armout":
            figure(d, W // 2 - 80, ph - 40, 1.35, arm=ease(t * 1.6))
            d.text((W - 300, 60), "← points to cars", font=font(22, 600), fill=ORANGE)
        elif kind == "serious":
            figure(d, W // 2, ph + 40, 1.5 + 0.25 * ease(t), arm=0.1, mood="serious")
            d.text((170, 60), "slow push-in", font=font(22, 600), fill=ORANGE)
        elif kind == "label":
            figure(d, W // 2 - 60, ph - 20, 1.4, arm=0.5 + 0.4 * math.sin(t * 7))
            pop = ease((t - 0.25) * 4)
            if pop > 0:
                f = font(int(78 * (0.6 + 0.4 * pop)), 900)
                d.rounded_rectangle([60, 120, W - 60, 230], radius=20, fill=ORANGE + (int(235 * pop),))
                text_c(d, (W // 2, 175), "C-HR HYBRID", f)
        elif kind == "call":
            figure(d, W // 2 - 90, ph - 20, 1.35, arm=0.8)
            drop = ease(t * 2)
            y = -120 + 420 * drop + (12 * math.sin(t * 20) * (1 - drop))
            cx = W - 170
            d.rounded_rectangle([cx - 70, y, cx + 70, y + 140], radius=36, fill=(37, 211, 102))
            d.text((cx, y + 70), "CALL", font=font(34, 900), fill=WHITE, anchor="mm")
            d.text((cx, y + 170), "Call / WhatsApp", font=font(20, 700), fill=WHITE, anchor="mm")

    elif kind == "sign":
        d.rectangle([0, 0, W, ph], fill=(120, 170, 215))
        d.rectangle([0, ph * 0.62, W, ph], fill=(70, 70, 75))
        d.rectangle([60, 150, W - 60, ph * 0.62], fill=(225, 225, 228), outline=WHITE, width=4)
        d.rectangle([60, 150, W - 60, 300], fill=NAVY)
        paste_logo(pic, LOGO_H_IMG, 480, (120, 185))
        d.text((W // 2, 340), "530 Albany Hwy · Victoria Park", font=font(26, 700), fill=NAVY, anchor="mm")
        for i, col in enumerate([(200, 30, 40), (240, 240, 240)]):
            x = int(-260 + (W + 520) * ((t * 1.3 + i * 0.5) % 1))
            yy = int(ph * 0.74 + i * 90)
            d.rounded_rectangle([x, yy, x + 240, yy + 70], radius=24, fill=col)
        d.text((170, 60), "street shot, traffic passing", font=font(22, 600), fill=NAVY)

    elif kind == "map":
        d.rectangle([0, 0, W, ph], fill=NAVY)
        # stylised Japan (top-right arc) and Western Australia (bottom-left block)
        jp = [(560, 120), (600, 170), (590, 230), (545, 290), (500, 330), (470, 350), (455, 335), (500, 290), (540, 230), (548, 170)]
        d.line(jp + [jp[0]], fill=WHITE, width=5, joint="curve")
        d.text((610, 250), "JAPAN", font=font(26, 800), fill=WHITE)
        wa = [(110, 560), (300, 520), (330, 640), (320, 800), (220, 850), (130, 820), (90, 700)]
        d.polygon(wa, outline=WHITE, width=5)
        d.text((120, 870), "WESTERN AUSTRALIA", font=font(22, 800), fill=WHITE)
        p0, p1, ctrl = (470, 345), (150, 760), (520, 620)
        n = int(60 * ease(t * 1.25))
        pts = []
        for i in range(n + 1):
            u = i / 60
            pts.append(((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * ctrl[0] + u * u * p1[0],
                        (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * ctrl[1] + u * u * p1[1]))
        for a, b in zip(pts[::2], pts[1::2]):
            d.line([a, b], fill=ORANGE, width=7)
        if pts:
            x, y = pts[-1]
            d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=ORANGE)
        if t > 0.8:
            d.ellipse([p1[0] - 22, p1[1] - 22, p1[0] + 22, p1[1] + 22], outline=ORANGE, width=6)
            d.text((p1[0] + 34, p1[1] - 16), "PERTH", font=font(30, 900), fill=ORANGE)
        d.text((170, 40), "free graphic (built in code, 0 credits)", font=font(20, 600), fill=SLATE)

    elif kind == "sheet":
        d.rectangle([0, 0, W, ph], fill=(60, 60, 64))
        ang = -4 + 3 * t
        sheet = Image.new("RGBA", (520, 700), (250, 248, 240, 255))
        sd = ImageDraw.Draw(sheet)
        sd.rectangle([0, 0, 520, 70], fill=(200, 60, 60))
        sd.text((260, 35), "AUCTION SHEET", font=font(30, 900), fill=WHITE, anchor="mm")
        for r in range(5):
            sd.line([(20, 110 + r * 50), (500, 110 + r * 50)], fill=(180, 180, 180), width=2)
        sd.rounded_rectangle([340, 90, 500, 220], radius=12, outline=(200, 60, 60), width=5)
        sd.text((420, 125), "GRADE", font=font(22, 800), fill=(200, 60, 60), anchor="mm")
        sd.text((420, 180), "[4.5]", font=font(44, 900), fill=(200, 60, 60), anchor="mm")
        sd.rectangle([60, 380, 460, 640], outline=(120, 120, 120), width=3)
        sd.text((260, 370), "body map", font=font(20, 600), fill=(120, 120, 120), anchor="mb")
        for (x, y, s_) in [(150, 450, "A1"), (360, 560, "U1")]:
            sd.text((x, y), s_, font=font(26, 900), fill=(200, 60, 60))
        sheet = sheet.rotate(ang, expand=True, resample=Image.BICUBIC)
        z = 1.0 + 0.12 * ease(t)
        sheet = sheet.resize((int(sheet.width * z), int(sheet.height * z)), Image.LANCZOS)
        pic.alpha_composite(sheet, ((W - sheet.width) // 2, (ph - sheet.height) // 2 + 20))
        fx, fy = 400 + 40 * ease(t), 260 + 60 * ease(t)
        d = ImageDraw.Draw(pic)
        d.line([(fx, fy), (fx + 160, fy + 260)], fill=(214, 170, 130), width=34)
        d.text((170, 40), "chassis no. blurred", font=font(20, 600), fill=ORANGE)

    elif kind == "foam":
        car = cover(IMG["chr_rear"], W, ph, zoom=1.25 + 0.05 * t).convert("RGBA")
        pic = car
        d = ImageDraw.Draw(pic, "RGBA")
        wipe = ease((t - 0.45) * 2.2) * W
        import random
        rnd = random.Random(4)
        for _ in range(140):
            x, y, r = rnd.randint(0, W), rnd.randint(150, ph - 150), rnd.randint(12, 40)
            if x > wipe and t > 0.05:
                d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 200))
        if t > 0.45:
            d.rectangle([wipe - 18, 120, wipe + 18, ph - 120], fill=(0, 168, 168, 230))
        d.text((170, 40), "Aureus bay · cut on the wipe", font=font(22, 700), fill=ORANGE)

    elif kind == "car1":
        pic = cover(IMG["chr"], W, ph, zoom=1.35, dx=-0.6 + 1.2 * t).convert("RGBA")
        d = ImageDraw.Draw(pic)
        d.text((170, 40), "slow pan left → right", font=font(22, 700), fill=ORANGE)

    elif kind in ("car2", "car3", "car4"):
        names = {"car2": "Real hybrid #2 (e.g. Corolla Fielder)", "car3": "Real hybrid #3 (e.g. Harrier)",
                 "car4": "Real hybrid #4 (e.g. Prius / Aqua)"}
        d.rectangle([0, 0, W, ph], fill=NAVY)
        car_placeholder(d, t, names[kind])
        d.text((170, 40), "same pan height + direction as shot 7", font=font(20, 600), fill=SLATE)

    elif kind == "dash":
        d.rectangle([0, 0, W, ph], fill=(18, 18, 22))
        cx, cy = W // 2, ph // 2
        d.arc([cx - 230, cy - 230, cx + 230, cy + 230], 150, 390, fill=(70, 70, 80), width=26)
        a = 150 + 160 * ease(t)
        d.arc([cx - 230, cy - 230, cx + 230, cy + 230], 150, a, fill=(0, 200, 140), width=26)
        d.text((cx, cy - 30), "ECO", font=font(64, 900), fill=(0, 200, 140), anchor="mm")
        d.text((cx, cy + 50), "HYBRID SYSTEM", font=font(26, 700), fill=WHITE, anchor="mm")
        d.text((cx, cy + 110), "[our real L/100 km]", font=font(26, 700), fill=ORANGE, anchor="mm")
        d.text((170, 40), "film the real dash display", font=font(22, 700), fill=ORANGE)

    elif kind == "phone":
        pic = yard_bg(0.5, blur=10)
        d = ImageDraw.Draw(pic)
        y = 140 - 20 * ease(t)
        d.rounded_rectangle([170, y, 550, y + 640], radius=46, fill=(20, 20, 24), outline=(90, 90, 95), width=6)
        d.rectangle([190, y + 60, 530, y + 600], fill=WHITE)
        d.text((360, y + 100), "DRIVE · NEWS", font=font(20, 800), fill=(200, 30, 40), anchor="mm")
        hf = font(30, 900)
        for i, ln in enumerate(wrap("Australia to block thousands of hybrid car imports", hf, 300, d)):
            d.text((210, y + 140 + i * 40), ln, font=hf, fill=(20, 20, 20))
        d.text((210, y + 430), "29 April 2026", font=font(20, 600), fill=(110, 110, 110))
        pop = ease((t - 0.35) * 3)
        if pop > 0:
            r = int(85 * pop)
            d.ellipse([560 - r, 760 - r, 560 + r, 760 + r], fill=ORANGE)
            d.text((560, 760), "WA", font=font(int(54 * pop) + 1, 900), fill=WHITE, anchor="mm")

    elif kind == "end":
        if t < 0.45:
            pic = yard_bg(t)
            d = ImageDraw.Draw(pic)
            figure(d, W // 2, ph + 80, 1.75, arm=0.1)
        else:
            d.rectangle([0, 0, W, ph], fill=NAVY)
            k = ease((t - 0.45) * 3)
            paste_logo(pic, LOGO_IMG, int(360 * (0.85 + 0.15 * k)), (W // 2 - int(180 * (0.85 + 0.15 * k)), 150))
            d = ImageDraw.Draw(pic)
            d.text((W // 2, 560), "0434 137 393", font=font(52, 900), fill=WHITE, anchor="mm")
            d.text((W // 2, 620), "530 Albany Hwy, Victoria Park", font=font(26, 600), fill=WHITE, anchor="mm")
            d.text((W // 2, 690), "MV Dealership Licence MD32748", font=font(22, 600), fill=SLATE, anchor="mm")
            d.rectangle([W // 2 - 60, 735, W // 2 + 60, 741], fill=ORANGE)

    base.alpha_composite(pic, (0, TOP))


def frame(i_shot, t, t_abs):
    dur, direction, says, caption, kind = SHOTS[i_shot]
    im = Image.new("RGBA", (W, H), (8, 18, 34, 255))
    draw_scene(kind, t, im)
    d = ImageDraw.Draw(im)
    # watermark top-left of picture (≈55%)
    paste_logo(im, WM, 120, (24, TOP + 20), alpha=0.55)
    # on-screen caption (mid-frame), pops in
    if kind != "end" or t < 0.45:
        k = ease(t * 5)
        f = font(int(54 * (0.8 + 0.2 * k)), 900)
        text_c(d, (W // 2, TOP + 560), caption, f)
    # top info bar
    d.rectangle([0, 0, W, TOP], fill=(8, 18, 34))
    d.text((24, 22), f"SHOT {i_shot + 1}/16", font=font(30, 900), fill=ORANGE)
    start = sum(s[0] for s in SHOTS[:i_shot])
    d.text((W - 24, 26), f"{start:.1f}–{start + dur:.1f} s", font=font(24, 700), fill=WHITE, anchor="ra")
    d.text((24, 72), direction, font=font(24, 600), fill=WHITE)
    d.text((24, 110), "STORYBOARD · Perth, want a Japanese hybrid?", font=font(16, 500), fill=SLATE)
    # bottom dialogue bar
    d.rectangle([0, BOT, W, H], fill=(8, 18, 34))
    d.text((24, BOT + 18), "MONSOOR SAYS:", font=font(18, 800), fill=ORANGE)
    fq = font(26, 600)
    for j, ln in enumerate(wrap(f"“{says}”", fq, W - 48, d)[:4]):
        d.text((24, BOT + 50 + j * 36), ln, font=fq, fill=WHITE)
    # progress bar
    total = sum(s[0] for s in SHOTS)
    d.rectangle([0, H - 8, int(W * t_abs / total), H], fill=ORANGE)
    return im.convert("RGB")


def main():
    out_mp4 = os.path.join(HERE, "Hybrid-Clone-Animatic.mp4")
    out_png = os.path.join(HERE, "Hybrid-Clone-Storyboard.png")
    tmp = tempfile.mkdtemp(prefix="animatic_")
    n, t_abs, thumbs = 0, 0.0, []
    for i, s in enumerate(SHOTS):
        frames = int(round(s[0] * FPS))
        for k in range(frames):
            t = k / max(1, frames - 1)
            im = frame(i, t, t_abs + k / FPS)
            im.save(os.path.join(tmp, f"f{n:05d}.png"))
            if k == int(frames * 0.7):
                thumbs.append(im)
            n += 1
        t_abs += s[0]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", out_mp4], check=True)
    shutil.rmtree(tmp)
    # contact sheet 4 x 4
    tw, th = 270, 480
    sheet = Image.new("RGB", (tw * 4 + 50, th * 4 + 50), (8, 18, 34))
    for i, im in enumerate(thumbs):
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (10 + (i % 4) * (tw + 10), 10 + (i // 4) * (th + 10)))
    sheet.save(out_png)
    print(out_mp4, n, "frames;", out_png)


if __name__ == "__main__":
    main()
