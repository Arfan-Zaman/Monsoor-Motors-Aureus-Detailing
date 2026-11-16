"""Aureus cinematic ad: assembles the Kling shots, his voice lines, music and all animated graphics. No credits used.
Run: /opt/miniconda3/bin/python -I make_ad.py   -> Aureus-Cinematic-Ad.mp4, Aureus-Cinematic-Ad-NO-MUSIC.mp4, Aureus-Ad-Cover.png"""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); R1 = os.path.join(HERE, "..", "reel-1")
AUREUS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FONT = os.path.join(AUREUS, "04 Fonts", "Montserrat-Variable.ttf")
LOGO_END = os.path.join(AUREUS, "02 Logo", "PNG", "aureus-stacked-3d-chrome.png")
LOGO_BUG = os.path.join(AUREUS, "02 Logo", "PNG", "aureus-horizontal-flat-white.png")
WORK = os.path.join(HERE, "build"); os.makedirs(WORK, exist_ok=True)
W, H, FPS = 1080, 1920, 24
NAVY, AQUA, GLOW, PINK, WHITE = (7, 26, 51), (0, 168, 168), (95, 240, 230), (255, 77, 141), (245, 248, 252)
# cut points in frames, on the 100 bpm beat grid (0.6 s): hook, van, he speaks, polish, steam, wheel, paint close-up, wide reveal, end card
CUTS = [0, 72, 144, 288, 389, 475, 547, 605, 662, 763]; TOTAL = CUTS[-1]; DUR = TOTAL / FPS

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode: sys.exit(" ".join(cmd[:6]) + "\n" + r.stderr[-1500:])

# ---------------- picture: base film ----------------
def clip(src, n, out):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    vf = f"setpts=PTS*{(n / FPS) / d:.5f},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},format=yuv420p"
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf", vf, "-frames:v", str(n), "-an", "-c:v", "libx264", "-crf", "12", "-preset", "medium", out])
def still(src, n, out, z0=1.0, z1=1.07, fx=0.5, fy=0.6):
    vf = (f"scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840,"
          f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}':d={n}:s={W}x{H}:fps={FPS},format=yuv420p")
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf", vf, "-frames:v", str(n), "-c:v", "libx264", "-crf", "12", "-preset", "medium", out])
SRC = [("clips/hook.mp4", clip), ("clips/van.mp4", clip), (os.path.join(R1, "speaking-raw.mp4"), clip), ("clips/polish.mp4", clip),
       ("clips/steam.mp4", clip), ("clips/wheel.mp4", clip), ("clips/macro.mp4", clip), ("clips/reveal.mp4", clip), (os.path.join(R1, "stills", "s6-finish.png"), still)]
base = os.path.join(WORK, "base.mp4")
if not os.path.exists(base) or "--rebase" in sys.argv:
    segs = []
    for i, (s, fn) in enumerate(SRC):
        o = os.path.join(WORK, f"seg{i}.mp4"); fn(s if os.path.isabs(s) else os.path.join(HERE, s), CUTS[i + 1] - CUTS[i], o); segs.append(o)
    lst = os.path.join(WORK, "list.txt"); open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-r", str(FPS), base])

# ---------------- graphics toolkit ----------------
def font(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name(weight); return f
_cache = {}
def sprite(text, size, weight="Bold", fill=WHITE, shadow=True):
    k = (text, size, weight, fill, shadow)
    if k not in _cache:
        f = font(size, weight); l, t, r, b = f.getbbox(text); pad = 16
        im = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        if shadow: d.text((pad - l + 3, pad - t + 4), text, font=f, fill=(2, 8, 18, 190)); im = im.filter(ImageFilter.GaussianBlur(3)); d = ImageDraw.Draw(im)
        d.text((pad - l, pad - t), text, font=f, fill=fill); _cache[k] = im
    return _cache[k]
def put(fr, im, cx, cy, scale=1.0, alpha=1.0, anchor="c"):
    if alpha <= 0.003: return
    if abs(scale - 1) > 0.002: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if alpha < 0.997: im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    x = cx - im.width / 2 if anchor == "c" else cx if anchor == "l" else cx - im.width
    fr.alpha_composite(im, (int(x), int(cy - im.height / 2)))
clamp = lambda v: max(0.0, min(1.0, v))
def ease(t): t = clamp(t); return 1 - (1 - t) ** 3
def back(t): t = clamp(t); c = 1.9; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def prog(t, start, dur): return clamp((t - start) / dur)
def slam(fr, text, size, cx, cy, t, at, weight="ExtraBold", fill=WHITE):       # word punches in: big -> settles
    p = prog(t, at, 0.22)
    if p > 0: put(fr, sprite(text, size, weight, fill), cx, cy, 1.45 - 0.45 * ease(p), ease(p * 1.6))
def rise(fr, text, size, cx, cy, t, at, weight="Bold", fill=WHITE, anchor="c"):  # slides up and fades in
    p = ease(prog(t, at, 0.4))
    if p > 0: put(fr, sprite(text, size, weight, fill), cx, cy + 34 * (1 - p), 1, p, anchor)
def gradient(y0, y1, a0, a1):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    for y in range(min(y0, y1), max(y0, y1)): d.line([(0, y), (W, y)], fill=NAVY + (int(a0 + (a1 - a0) * (y - y0) / (y1 - y0)),))
    return g
G_TOP, G_BOT = gradient(0, 720, 150, 0), gradient(1040, 1920, 0, 175)
FROST = (206, 224, 245)   # website glass: see-through navy with a frost edge
def fade_layer(fr, layer, a):
    if a <= 0: return
    if a < 1: layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    fr.alpha_composite(layer)
def logo(path, width):
    k = ("logo", path, width)
    if k not in _cache:
        lg = Image.open(path).convert("RGBA"); lg = lg.crop(lg.getbbox()); _cache[k] = lg.resize((width, int(lg.height * width / lg.width)), Image.LANCZOS)
    return _cache[k]
def chip(fr, text, x, y, t, at, tick=True):                                      # checklist chip slides in from the left
    p = ease(prog(t, at, 0.35))
    if p <= 0: return
    f = font(40, "SemiBold"); tw = int(f.getlength(text)); w, h = tw + (96 if tick else 56), 72
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=36, fill=NAVY + (120,), outline=FROST + (150,), width=2)
    if tick:
        q = ease(prog(t, at + 0.15, 0.3)); pts = [(26, 37), (38, 49), (58, 25)]
        if q > 0:
            a, b, c = pts; m = (a[0] + (b[0] - a[0]) * min(1, q * 2), a[1] + (b[1] - a[1]) * min(1, q * 2)); line = [a, m]
            if q > 0.5: line.append((b[0] + (c[0] - b[0]) * (q - 0.5) * 2, b[1] + (c[1] - b[1]) * (q - 0.5) * 2))
            d.line(line, fill=GLOW + (255,), width=6, joint="curve")
    d.text((74 if tick else 28, 36), text, font=f, fill=WHITE, anchor="lm")
    put(fr, im, x - 60 * (1 - p), y, 1, p, "l")
def callout(fr, d, t, at, dot, label_xy, title, sub, side="l"):                  # dot pulses on the subject, a line draws to a label
    p = ease(prog(t, at, 0.45))
    if p <= 0: return
    x0, y0 = dot; x1, y1 = label_xy; pulse = 1 + 0.25 * math.sin((t - at) * 7)
    d.ellipse([x0 - 22 * pulse, y0 - 22 * pulse, x0 + 22 * pulse, y0 + 22 * pulse], outline=GLOW + (int(200 * p),), width=3)
    d.ellipse([x0 - 9, y0 - 9, x0 + 9, y0 + 9], fill=GLOW + (int(255 * p),))
    d.line([(x0, y0), (x0 + (x1 - x0) * p, y0 + (y1 - y0) * p)], fill=GLOW + (int(255 * p),), width=3)
    rise(fr, title, 54, x1 + (14 if side == "l" else -14), y1 - 34, t, at + 0.3, "Bold", WHITE, side if side == "l" else "r")
    rise(fr, sub, 36, x1 + (14 if side == "l" else -14), y1 + 26, t, at + 0.45, "Medium", (214, 228, 242), side if side == "l" else "r")
def step(fr, d, t, n, title):                                                    # brand bug + "STEP n" + title at the bottom
    fade_layer(fr, G_BOT, ease(prog(t, 0, 0.3))); fade_layer(fr, G_TOP, 0.75 * ease(prog(t, 0, 0.3)))
    put(fr, logo(LOGO_BUG, 290), W / 2, 300, 1, ease(prog(t, 0.05, 0.4)))
    p = ease(prog(t, 0.15, 0.4)); d.rounded_rectangle([W / 2 - 60 * p, 1352, W / 2 + 60 * p, 1359], radius=4, fill=AQUA + (255,))
    rise(fr, f"STEP {n} OF 3", 34, W / 2, 1318, t, 0.1, "SemiBold", GLOW)
    rise(fr, title, 70, W / 2, 1428, t, 0.2, "Bold")

# ---------------- the eight scenes (t = seconds since the scene started) ----------------
def sc_hook(fr, d, t, n):
    fade_layer(fr, G_BOT, 1); slam(fr, "THE PERTH SUN", 104, W / 2, 1180, t, 0.30); slam(fr, "SHOWS", 104, W / 2, 1300, t, 1.05)
    slam(fr, "EVERYTHING.", 104, W / 2, 1420, t, 1.45, fill=PINK)
    p = ease(prog(t, 1.7, 0.6))
    if p > 0:                                                                     # ring draws around the glare, then a label
        d.arc([588 - 190, 700 - 190, 588 + 190, 700 + 190], -90, -90 + 360 * p, fill=GLOW + (255,), width=6)
        rise(fr, "Swirl marks + scratches", 44, 588, 950, t, 2.1, "SemiBold", GLOW)
def sc_van(fr, d, t, n):
    fade_layer(fr, G_TOP, 1); p = prog(t, 0.15, 0.5)
    if p > 0:                                                                     # map pin drops and bounces
        y = 330 - 260 * (1 - back(p)); x = 150
        d.ellipse([x - 44, y - 44, x + 44, y + 44], fill=PINK + (255,)); d.polygon([(x - 34, y + 28), (x + 34, y + 28), (x, y + 96)], fill=PINK + (255,))
        d.ellipse([x - 17, y - 17, x + 17, y + 17], fill=NAVY + (255,))
    slam(fr, "WE COME", 112, 620, 300, t, 0.45); slam(fr, "TO YOU.", 112, 620, 420, t, 0.80, fill=GLOW)
    q = ease(prog(t, 1.3, 0.5)); d.rounded_rectangle([250, 500, 250 + 740 * q, 506], radius=3, fill=AQUA + (255,))
    rise(fr, "Mobile · within 20 km of Victoria Park", 40, 620, 548, t, 1.4, "SemiBold")
SUBS = [(0.00, 1.03, "We come to you."), (1.03, 1.66, "Gold detail:"), (1.66, 3.09, "polish, wax sealant,"), (3.09, 4.42, "interior steam clean,"), (4.42, 5.06, "leather care."), (5.06, 6.0, "$199.")]
def sc_speak(fr, d, t, n):
    fade_layer(fr, G_TOP, 0.8)
    for i, (at, txt) in enumerate([(1.66, "Machine polish"), (2.30, "Wax sealant"), (3.09, "Interior steam clean"), (4.42, "Leather care")]):
        chip(fr, txt, 56, 300 + i * 88, t, at)
    p = prog(t, 5.06, 0.3)
    if p > 0:                                                                     # price badge punches in
        im = Image.new("RGBA", (330, 330), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); dd.ellipse([0, 0, 329, 329], fill=PINK + (215,), outline=WHITE + (160,), width=3)
        dd.text((165, 118), "GOLD", font=font(46, "Bold"), fill=NAVY, anchor="mm"); dd.text((165, 196), "$199", font=font(104, "ExtraBold"), fill=NAVY, anchor="mm")
        put(fr, im.rotate(-8, Image.BICUBIC, expand=True), 850, 470, back(p), ease(p * 2))
    for a, b, txt in SUBS:                                                        # word captions, for viewers watching muted
        if a <= t < b:
            f = font(58, "Bold"); tw = f.getlength(txt); w = tw + 68; x = (W - w) / 2; s = 0.9 + 0.1 * ease(prog(t, a, 0.12))
            im = Image.new("RGBA", (int(w), 98), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); dd.rounded_rectangle([0, 0, int(w) - 1, 97], radius=49, fill=NAVY + (135,), outline=FROST + (120,), width=2)
            dd.text((w / 2, 46), txt, font=f, fill=PINK if "$" in txt else WHITE, anchor="mm"); put(fr, im, W / 2, 1472, s)
def sc_polish(fr, d, t, n):
    step(fr, d, t, 1, "Machine polish + wax seal")
    g = ease(prog(t, 0.8, 0.4))
    if g > 0: d.rounded_rectangle([44, 536, 44 + 700, 536 + 258], radius=28, fill=NAVY + (int(105 * g),), outline=FROST + (int(120 * g),), width=2)   # glass panel behind the diagram
    for i, (lab, col) in enumerate([("Wax sealant", GLOW + (190,)), ("Polished clear coat", FROST + (130,)), ("Paint", AQUA + (150,))]):   # layer diagram builds bottom-up
        p = ease(prog(t, 1.0 + (2 - i) * 0.45, 0.45))
        if p > 0:
            y = 560 + i * 74; d.rounded_rectangle([70, y, 70 + 250 * p, y + 58], radius=12, fill=col, outline=FROST + (170,), width=2)
            rise(fr, lab, 36, 344, y + 29, t, 1.15 + (2 - i) * 0.45, "SemiBold", WHITE, "l")
    p = prog(t, 2.6, 1.2)
    if 0 < p < 1:                                                                 # one light sweep across the paint
        sw = Image.new("RGBA", (W, H), (0, 0, 0, 0)); x = -300 + 1700 * p
        ImageDraw.Draw(sw).polygon([(x, 700), (x + 150, 700), (x - 250, 1300), (x - 400, 1300)], fill=(255, 255, 255, 60)); fr.alpha_composite(sw.filter(ImageFilter.GaussianBlur(28)))
def sc_steam(fr, d, t, n):
    step(fr, d, t, 2, "Interior steam clean"); callout(fr, d, t, 0.9, (590, 1130), (120, 560), "Steam lifts the dirt", "Leather cleaned and conditioned")
def sc_wheel(fr, d, t, n):
    step(fr, d, t, 3, "Wheels + vents, deep cleaned"); callout(fr, d, t, 0.6, (560, 1080), (120, 560), "Every spoke, by hand", "Brake dust gone")
def sc_macro(fr, d, t, n):                                                     # the same close-up as the hook, now flawless
    fade_layer(fr, G_BOT, 1); p = prog(t, 0.0, 0.3)
    if p < 1: fr.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(210 * (1 - p)))))            # flash on the cut
    slam(fr, "NOW IT'S", 104, W / 2, 1240, t, 0.30); slam(fr, "LIKE NEW.", 132, W / 2, 1380, t, 0.70, fill=GLOW)
    q = ease(prog(t, 1.0, 0.6))
    if q > 0:
        d.arc([560 - 210, 880 - 210, 560 + 210, 880 + 210], -90, -90 + 360 * q, fill=GLOW + (230,), width=5)
        rise(fr, "Sealed: water beads and rolls off", 42, W / 2, 1130, t, 1.35, "SemiBold", GLOW)
def sc_reveal(fr, d, t, n):
    fade_layer(fr, G_TOP, 0.9); fade_layer(fr, G_BOT, 0.9)
    q = ease(prog(t, 0.2, 1.0)); bx0, bx1 = 160, 920                                                         # time bar fills to 2 h 30
    if q > 0:
        rise(fr, "Done in", 44, W / 2, 310, t, 0.2, "SemiBold")
        mins = int(150 * q); put(fr, sprite(f"{mins // 60} h {mins % 60:02d}", 110, "ExtraBold"), W / 2, 410, 1, min(1, q * 3))
        d.rounded_rectangle([bx0, 492, bx1, 504], radius=6, fill=(206, 224, 245, 70)); d.rounded_rectangle([bx0, 492, bx0 + (bx1 - bx0) * q, 504], radius=6, fill=GLOW + (255,))
    c = ease(prog(t, 0.9, 0.9))
    if c > 0:                                                                                                # price counts up
        rise(fr, "Gold detail", 56, W / 2, 1300, t, 0.9, "SemiBold"); put(fr, sprite(f"${int(199 * c)}", 170, "ExtraBold", PINK), W / 2, 1420, 0.85 + 0.15 * c, min(1, c * 3))
END_BG = Image.new("RGBA", (W, H), NAVY + (125,)); END_BG.alpha_composite(gradient(0, 1100, 150, 0)); END_BG.alpha_composite(gradient(900, 1920, 0, 200))
def sc_end(fr, d, t, n):
    fade_layer(fr, END_BG, ease(prog(t, 0, 0.5))); lg = logo(LOGO_END, 430); p = prog(t, 0.15, 0.6); put(fr, lg, W / 2, 270 + lg.height / 2, 0.8 + 0.2 * back(p), ease(p * 1.5))
    y = 270 + lg.height + 86
    p = prog(t, 0.7, 0.3)
    if p > 0: put(fr, sprite("Gold  ", 128, "ExtraBold"), W / 2 - 150, y, 1.3 - 0.3 * ease(p), ease(p * 2)); put(fr, sprite("$199", 128, "ExtraBold", PINK), W / 2 + 175, y, 1.3 - 0.3 * ease(p), ease(p * 2))
    rise(fr, "2 h 30 · at your place", 56, W / 2, y + 112, t, 1.0, "SemiBold")
    p = prog(t, 1.35, 0.4)
    if p > 0:
        f = font(46, "Bold"); l1, l2 = "Launch offer: $25 off", "for our first 100 customers"; bw = int(max(f.getlength(l1), f.getlength(l2)) + 96)
        im = Image.new("RGBA", (bw, 160), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); dd.rounded_rectangle([0, 0, bw - 1, 159], radius=36, fill=PINK + (225,), outline=WHITE + (150,), width=2)
        dd.text((bw / 2, 52), l1, font=f, fill=NAVY, anchor="mm"); dd.text((bw / 2, 110), l2, font=f, fill=NAVY, anchor="mm"); put(fr, im, W / 2, y + 270, back(p), ease(p * 2))
    rise(fr, "Mobile within 20 km of Victoria Park", 44, W / 2, y + 420, t, 1.8, "Medium")
    pulse = 1 + 0.06 * math.sin(max(0, t - 2.6) * 6) * (1 if t > 2.6 else 0); p = ease(prog(t, 2.1, 0.4))
    if p > 0: put(fr, sprite("Book: link in bio", 62, "Bold", GLOW), W / 2, y + 500 + 34 * (1 - p), pulse, p)
SCENES = [sc_hook, sc_van, sc_speak, sc_polish, sc_steam, sc_wheel, sc_macro, sc_reveal, sc_end]

def frame(i):
    fr = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(fr)
    s = max(k for k in range(len(SCENES)) if CUTS[k] <= i); SCENES[s](fr, d, (i - CUTS[s]) / FPS, CUTS[s + 1] - CUTS[s])
    return fr

if "--frames" in sys.argv:                                                        # quick look: save a few composited stills and stop
    for t in [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")]:
        i = int(t * FPS); p = os.path.join(WORK, f"prev-{t:05.2f}.png"); frame(i).save(os.path.join(WORK, "ov.png"))
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{i / FPS:.3f}", "-i", base, "-i", os.path.join(WORK, "ov.png"), "-filter_complex", "[0][1]overlay,scale=432:768", "-frames:v", "1", p])
    sys.exit()

# ---------------- cover image ----------------
bg = Image.open(os.path.join(R1, "stills", "s2-speaking.png")).convert("RGBA"); s = max(W / bg.width, H / bg.height)
bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1), Image.LANCZOS); bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
bg.alpha_composite(gradient(0, 900, 235, 0)); bg.alpha_composite(gradient(1250, 1920, 0, 240)); d = ImageDraw.Draw(bg)
put(bg, sprite("WE COME", 150, "ExtraBold"), W / 2, 340); put(bg, sprite("TO YOU.", 150, "ExtraBold", GLOW), W / 2, 500)
im = Image.new("RGBA", (360, 360), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); dd.ellipse([0, 0, 359, 359], fill=PINK + (255,))
dd.text((180, 104), "GOLD DETAIL", font=font(38, "Bold"), fill=NAVY, anchor="mm"); dd.text((180, 192), "$199", font=font(118, "ExtraBold"), fill=NAVY, anchor="mm"); dd.text((180, 276), "at your place", font=font(34, "SemiBold"), fill=NAVY, anchor="mm")
put(bg, im.rotate(-8, Image.BICUBIC, expand=True), 850, 1010)
put(bg, sprite("Mobile car detailing · Perth", 54, "SemiBold"), W / 2, 1490)
bg.convert("RGB").save(os.path.join(HERE, "Aureus-Ad-Cover.png")); print("cover done")
if "--cover" in sys.argv: sys.exit()


# ---------------- sound ----------------
wav = lambda n: os.path.join(WORK, n)
VO_AT = [0.30, 3.30, 12.25, 16.45, 20.05, 23.10, 28.05]                           # when each of his lines starts
ins, fc, lab = [], "", []
for k, at in enumerate(VO_AT):
    ins += ["-i", os.path.join(HERE, "audio", f"vo{k + 1}.wav")]
    fc += f"[{k}:a]silenceremove=start_periods=1:start_threshold=-42dB,loudnorm=I=-15:TP=-1.5:LRA=7,aresample=48000,aformat=channel_layouts=stereo,adelay={int(at * 1000)}:all=1[v{k}];"; lab.append(f"[v{k}]")
ins += ["-i", os.path.join(R1, "speaking-raw.mp4")]
fc += f"[7:a]loudnorm=I=-15:TP=-1.5:LRA=7,aresample=48000,aformat=channel_layouts=stereo,adelay=6000:all=1[v7];"; lab.append("[v7]")
run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", fc + "".join(lab) + f"amix=inputs=8:normalize=0:duration=longest,apad=whole_dur={DUR}[a]", "-map", "[a]", "-t", str(DUR), "-ar", "48000", "-ac", "2", wav("voice.wav")])
cuts = [c / FPS for c in CUTS[1:-1]]
fx = "".join(f"anoisesrc=d=0.45:c=pink:r=48000:a=0.5,bandpass=f=900:width_type=h:w=1400,afade=in:d=0.28:curve=qsin,afade=out:st=0.28:d=0.17,aformat=channel_layouts=stereo,adelay={int((c - 0.28) * 1000)}:all=1[w{i}];" for i, c in enumerate(cuts))
hits = [0.0, CUTS[6] / FPS, CUTS[8] / FPS]
fx += "".join(f"sine=f=52:d=0.9:r=48000,afade=out:st=0.05:d=0.85,aformat=channel_layouts=stereo,volume=1.6,adelay={int(h * 1000)}:all=1[h{i}];" for i, h in enumerate(hits))
fx += "".join(f"[w{i}]" for i in range(len(cuts))) + "".join(f"[h{i}]" for i in range(len(hits))) + f"amix=inputs={len(cuts) + len(hits)}:normalize=0:duration=longest,volume=0.5,apad=whole_dur={DUR}[fx]"
run(["ffmpeg", "-y", "-v", "error", "-filter_complex", fx, "-map", "[fx]", "-t", str(DUR), "-ar", "48000", "-ac", "2", wav("fx.wav")])
run(["ffmpeg", "-y", "-v", "error", "-i", wav("voice.wav"), "-i", wav("fx.wav"), "-filter_complex", "[0:a][1:a]amix=inputs=2:normalize=0:duration=first[a]", "-map", "[a]", wav("nomusic.wav")])
# music sits under the voice (ducked by the voice itself), full again in the gaps, fades at the end
run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(HERE, "audio", "music.mp3"), "-i", wav("voice.wav"), "-i", wav("nomusic.wav"), "-filter_complex",
     f"[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.55,afade=out:st={DUR - 1.2}:d=1.2[m];[1:a]asplit[sc][x];[x]anullsink;[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=450[md];"
     f"[md][2:a]amix=inputs=2:normalize=0:duration=shortest,alimiter=limit=0.89[a]", "-map", "[a]", "-t", str(DUR), wav("full.wav")])

# ---------------- render: graphics piped over the base film ----------------
silent = os.path.join(WORK, "graded.mp4")
p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-filter_complex", "[0:v][1:v]overlay=format=auto,format=yuv420p[v]", "-map", "[v]", "-frames:v", str(TOTAL), "-c:v", "libx264", "-crf", "15", "-preset", "medium", silent], stdin=subprocess.PIPE)
for i in range(TOTAL): p.stdin.write(frame(i).tobytes())
p.stdin.close(); p.wait()
enc = ["-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", str(DUR)]
for out, snd in (("Aureus-Cinematic-Ad.mp4", "full.wav"), ("Aureus-Cinematic-Ad-NO-MUSIC.mp4", "nomusic.wav")):
    run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav(snd), "-map", "0:v", "-map", "1:a"] + enc + [os.path.join(HERE, out)])

print("done")
