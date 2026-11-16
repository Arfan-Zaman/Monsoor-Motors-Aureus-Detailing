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
# cut points in frames, on the 100 bpm beat grid (0.6 s): hook, van, he speaks, polish x2, interior x2, wheels x2, paint close-up, hero, end card
CUTS = [0, 58, 101, 245, 305, 355, 410, 451, 499, 545, 600, 660, 720]; TOTAL = CUTS[-1]; DUR = TOTAL / FPS   # 30.0 s

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode: sys.exit(" ".join(cmd[:6]) + "\n" + r.stderr[-1500:])

# ---------------- picture: base film ----------------
# one shared commercial grade: soft filmic contrast, warm highlights, slightly cool shadows, gentle saturation, fine moving grain, soft vignette
GRADE = ("format=yuv420p,eq=contrast=1.04:saturation=0.92:gamma=0.98,colorbalance=rs=-0.015:bs=0.025:rh=0.035:gh=0.01:bh=-0.03,"
         "curves=master='0/0.02 0.25/0.23 0.75/0.78 1/0.97',vignette=angle=PI/5.5,noise=c0s=7:c0f=t,format=yuv420p")
def clip(src, n, out, start=0.0):
    vf = f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},{GRADE}"
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(start), "-i", src, "-vf", vf, "-frames:v", str(n), "-an", "-c:v", "libx264", "-crf", "12", "-preset", "medium", out])
def still(src, n, out, z0=1.0, z1=1.07, fx=0.5, fy=0.6):
    vf = (f"scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840,"
          f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}':d={n}:s={W}x{H}:fps={FPS},{GRADE}")
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf", vf, "-frames:v", str(n), "-c:v", "libx264", "-crf", "12", "-preset", "medium", out])
SRC = [("clips/hook.mp4", clip, 0.6), ("clips/van.mp4", clip, 1.2), ("clips/speak3.mp4", clip, 0), ("clips/p1.mp4", clip, 0.2), ("clips/p2.mp4", clip, 0.4),
       ("clips/i1.mp4", clip, 0.2), ("clips/i2.mp4", clip, 0.4), ("clips/w1.mp4", clip, 0.4), ("clips/w2.mp4", clip, 0.6), ("clips/macro.mp4", clip, 1.0), ("clips/bell.mp4", clip, 0.1),
       (os.path.join(R1, "stills", "s6-finish.png"), still, None)]
base = os.path.join(WORK, "base.mp4")
if not os.path.exists(base) or "--rebase" in sys.argv:
    segs = []
    for i, (s, fn, st) in enumerate(SRC):
        o = os.path.join(WORK, f"seg{i}.mp4"); a = [s if os.path.isabs(s) else os.path.join(HERE, s), CUTS[i + 1] - CUTS[i], o]; fn(*(a + [st] if st is not None else a)); segs.append(o)
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
def step(fr, d, t, n, title):                                                    # "STEP n OF 3" + what he is doing, on glass at the bottom
    fade_layer(fr, G_BOT, ease(prog(t, 0, 0.3)))
    p = ease(prog(t, 0.1, 0.35)); d.rounded_rectangle([W / 2 - 60 * p, 1352, W / 2 + 60 * p, 1359], radius=4, fill=AQUA + (255,))
    rise(fr, f"STEP {n} OF 3", 34, W / 2, 1318, t, 0.05, "SemiBold", GLOW)
    rise(fr, title, 70, W / 2, 1428, t, 0.12, "Bold")
def watermark(fr):                                                               # brand mark, top left, quiet
    put(fr, logo(LOGO_BUG, 230), 48, 290, 1, 0.55, "l")

# ---------------- the eight scenes (t = seconds since the scene started) ----------------
def sc_hook(fr, d, t, n):
    fade_layer(fr, G_BOT, 1); slam(fr, "THE PERTH SUN", 104, W / 2, 1180, t, 0.20); slam(fr, "SHOWS", 104, W / 2, 1300, t, 0.75)
    slam(fr, "EVERYTHING.", 104, W / 2, 1420, t, 1.10, fill=PINK)
    p = ease(prog(t, 1.3, 0.5))
    if p > 0:                                                                     # ring draws around the glare, then a label
        d.arc([588 - 190, 700 - 190, 588 + 190, 700 + 190], -90, -90 + 360 * p, fill=GLOW + (255,), width=6)
        rise(fr, "Swirl marks + scratches", 44, 588, 950, t, 1.6, "SemiBold", GLOW)
def sc_van(fr, d, t, n):
    fade_layer(fr, G_TOP, 1); p = prog(t, 0.05, 0.4)
    if p > 0:                                                                     # map pin drops and bounces
        y = 450 - 260 * (1 - back(p)); x = 150
        d.ellipse([x - 44, y - 44, x + 44, y + 44], fill=PINK + (255,)); d.polygon([(x - 34, y + 28), (x + 34, y + 28), (x, y + 96)], fill=PINK + (255,))
        d.ellipse([x - 17, y - 17, x + 17, y + 17], fill=NAVY + (255,))
    slam(fr, "WE COME", 112, 620, 420, t, 0.25); slam(fr, "TO YOU.", 112, 620, 540, t, 0.50, fill=GLOW)
    q = ease(prog(t, 0.8, 0.4)); d.rounded_rectangle([250, 620, 250 + 740 * q, 626], radius=3, fill=AQUA + (255,))
    rise(fr, "Mobile · within 20 km of Victoria Park", 40, 620, 668, t, 0.9, "SemiBold")
SUBS = [(0.00, 1.42, "We come to you."), (1.42, 2.51, "Gold detail,"), (2.51, 3.65, "$199."), (3.65, 4.63, "Done properly,"), (4.63, 6.0, "or it's not done.")]
def lower_third(fr, d, t, at=0.3, out=1.75):
    a = ease(prog(t, at, 0.5)) * (1 - ease(prog(t, out, 0.5)))
    if a <= 0: return
    x, y = 48, 348; w = ease(prog(t, at, 0.7))
    d.rectangle([x, y, x + 6, y + 112], fill=AQUA + (int(255 * a),))
    put(fr, sprite("THE MASTER DETAILER", 30, "SemiBold", GLOW), x + 26 - 20 * (1 - w), y + 26, 1, a, "l")
    put(fr, sprite("20 years on the tools", 46, "Bold"), x + 26 - 20 * (1 - w), y + 78, 1, a, "l")
def sc_speak(fr, d, t, n):
    fade_layer(fr, G_TOP, 0.8); lower_third(fr, d, t)
    for i, (at, txt) in enumerate([(2.15, "Machine polish"), (2.35, "Wax sealant"), (2.55, "Interior steam clean"), (2.75, "Leather care")]):
        chip(fr, txt, 56, 400 + i * 88, t, at)
    p = prog(t, 2.95, 0.3)
    if p > 0:                                                                     # price badge punches in
        im = Image.new("RGBA", (330, 330), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); dd.ellipse([0, 0, 329, 329], fill=PINK + (215,), outline=WHITE + (160,), width=3)
        dd.text((165, 118), "GOLD", font=font(46, "Bold"), fill=NAVY, anchor="mm"); dd.text((165, 196), "$199", font=font(104, "ExtraBold"), fill=NAVY, anchor="mm")
        put(fr, im.rotate(-8, Image.BICUBIC, expand=True), 850, 520, back(p), ease(p * 2))
    for a, b, txt in SUBS:                                                        # word captions, for viewers watching muted
        if a <= t < b:
            f = font(58, "Bold"); tw = f.getlength(txt); w = tw + 68; x = (W - w) / 2; s = 0.9 + 0.1 * ease(prog(t, a, 0.12))
            im = Image.new("RGBA", (int(w), 98), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); dd.rounded_rectangle([0, 0, int(w) - 1, 97], radius=49, fill=NAVY + (135,), outline=FROST + (120,), width=2)
            dd.text((w / 2, 46), txt, font=f, fill=PINK if "$" in txt else WHITE, anchor="mm"); put(fr, im, W / 2, 1472, s)
def svc(n, title):
    def f(fr, d, t, nfr): step(fr, d, t, n, title)
    return f
def sc_macro(fr, d, t, n):                                                     # the same close-up as the hook, now flawless
    fade_layer(fr, G_BOT, 1); p = prog(t, 0.0, 0.3)
    if p < 1: fr.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(210 * (1 - p)))))            # flash on the cut
    slam(fr, "NOW IT'S", 104, W / 2, 1240, t, 0.20); slam(fr, "LIKE NEW.", 132, W / 2, 1380, t, 0.55, fill=GLOW)
    rise(fr, "Sealed: water beads and rolls off", 42, W / 2, 1130, t, 0.9, "SemiBold", GLOW)
def sc_hero(fr, d, t, n):
    fade_layer(fr, G_BOT, 0.6); q = ease(prog(t, 0.1, 1.3))
    if q > 0:                                                                                                # timer runs to 2 h 30 as he taps the bell
        mins = int(150 * q); rise(fr, "Done in", 36, 70, 1258, t, 0.1, "SemiBold", WHITE, "l"); put(fr, sprite(f"{mins // 60} h {mins % 60:02d}", 92, "ExtraBold"), 60, 1336, 1, min(1, q * 3), "l")
        d.rounded_rectangle([76, 1396, 336, 1404], radius=4, fill=FROST + (70,)); d.rounded_rectangle([76, 1396, 76 + 260 * q, 1404], radius=4, fill=GLOW + (255,))
END_BG = Image.new("RGBA", (W, H), NAVY + (125,)); END_BG.alpha_composite(gradient(0, 1100, 150, 0)); END_BG.alpha_composite(gradient(900, 1920, 0, 200))
def sc_end(fr, d, t, n):
    fade_layer(fr, END_BG, ease(prog(t, 0, 0.5))); lg = logo(LOGO_END, 430); p = prog(t, 0.15, 0.6); put(fr, lg, W / 2, 270 + lg.height / 2, 0.8 + 0.2 * back(p), ease(p * 1.5))
    y = 270 + lg.height + 86
    p = prog(t, 0.5, 0.3)
    if p > 0: put(fr, sprite("Gold  ", 128, "ExtraBold"), W / 2 - 150, y, 1.3 - 0.3 * ease(p), ease(p * 2)); put(fr, sprite("$199", 128, "ExtraBold", PINK), W / 2 + 175, y, 1.3 - 0.3 * ease(p), ease(p * 2))
    rise(fr, "2 h 30 · at your place", 56, W / 2, y + 112, t, 0.75, "SemiBold")
    p = prog(t, 1.0, 0.4)
    if p > 0:
        f = font(46, "Bold"); l1, l2 = "Launch offer: $25 off", "for our first 100 customers"; bw = int(max(f.getlength(l1), f.getlength(l2)) + 96)
        im = Image.new("RGBA", (bw, 160), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); dd.rounded_rectangle([0, 0, bw - 1, 159], radius=36, fill=PINK + (225,), outline=WHITE + (150,), width=2)
        dd.text((bw / 2, 52), l1, font=f, fill=NAVY, anchor="mm"); dd.text((bw / 2, 110), l2, font=f, fill=NAVY, anchor="mm"); put(fr, im, W / 2, y + 270, back(p), ease(p * 2))
    rise(fr, "Mobile within 20 km of Victoria Park", 44, W / 2, y + 420, t, 1.35, "Medium")
    pulse = 1 + 0.06 * math.sin(max(0, t - 2.0) * 6) * (1 if t > 2.0 else 0); p = ease(prog(t, 1.6, 0.4))
    if p > 0: put(fr, sprite("Book: link in bio", 62, "Bold", GLOW), W / 2, y + 500 + 34 * (1 - p), pulse, p)
SCENES = [sc_hook, sc_van, sc_speak, svc(1, "Machine polish"), svc(1, "Sealed in wax, by hand"), svc(2, "Interior steam clean"), svc(2, "Vents and dash detailed"),
          svc(3, "Wheels scrubbed by hand"), svc(3, "Rinsed and dressed"), sc_macro, sc_hero, sc_end]

def frame(i):
    fr = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(fr)
    s = max(k for k in range(len(SCENES)) if CUTS[k] <= i); SCENES[s](fr, d, (i - CUTS[s]) / FPS, CUTS[s + 1] - CUTS[s])
    if SCENES[s] is not sc_end: watermark(fr)
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
VO = [(1, 0.15), (2, 10.35), (3, 14.95), (4, 19.00), (5, 23.00), (6, 27.30)]            # (persona line g1..g6, start second)
ins, fc, lab = [], "", []
for k, (num, at) in enumerate(VO):
    ins += ["-i", os.path.join(HERE, "audio", "v3", f"g{num}.wav")]
    fc += f"[{k}:a]silenceremove=start_periods=1:start_threshold=-42dB,areverse,silenceremove=start_periods=1:start_threshold=-42dB,areverse,loudnorm=I=-15:TP=-1.5:LRA=7,aresample=48000,aformat=channel_layouts=stereo,adelay={int(at * 1000)}:all=1[v{k}];"; lab.append(f"[v{k}]")
ins += ["-i", os.path.join(HERE, "clips", "speak3.mp4")]
fc += f"[{len(VO)}:a]loudnorm=I=-15:TP=-1.5:LRA=7,aresample=48000,aformat=channel_layouts=stereo,adelay={int(CUTS[2] / FPS * 1000)}:all=1[vs];"; lab.append("[vs]")
run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", fc + "".join(lab) + f"amix=inputs={len(VO) + 1}:normalize=0:duration=longest,apad=whole_dur={DUR}[a]", "-map", "[a]", "-t", str(DUR), "-ar", "48000", "-ac", "2", wav("voice.wav")])
cuts = [c / FPS for c in CUTS[1:-1]]
BELL_TAP = CUTS[10] / FPS + float(os.environ.get('BELL_AT', '1.5'))   # when his finger hits the bell in the bell shot
fx = "".join(f"anoisesrc=d=0.45:c=pink:r=48000:a=0.5,bandpass=f=900:width_type=h:w=1400,afade=in:d=0.28:curve=qsin,afade=out:st=0.28:d=0.17,aformat=channel_layouts=stereo,adelay={int((c - 0.28) * 1000)}:all=1[w{i}];" for i, c in enumerate(cuts))
hits = [0.0, CUTS[9] / FPS]
DINGS = [(CUTS[5] / FPS - 0.12, 0.55), (CUTS[7] / FPS - 0.12, 0.55), (CUTS[9] / FPS - 0.30, 0.55), (BELL_TAP, 1.0)]
fx += "".join(f"sine=f=52:d=0.9:r=48000,afade=out:st=0.05:d=0.85,aformat=channel_layouts=stereo,volume=1.6,adelay={int(h * 1000)}:all=1[h{i}];" for i, h in enumerate(hits))
fx += "".join(f"sine=f={f}:d=1.8:r=48000,volume={a * g},afade=out:st=0.004:d=1.75:curve=exp,aformat=channel_layouts=stereo,adelay={int(at * 1000)}:all=1[b{j}_{q}];" for j, (at, g) in enumerate(DINGS) for q, (f, a) in enumerate([(2793, 0.55), (4610, 0.22), (6720, 0.12), (1396, 0.10)]))
nb = 4 * len(DINGS)
fx += "".join(f"[w{i}]" for i in range(len(cuts))) + "".join(f"[h{i}]" for i in range(len(hits))) + "".join(f"[b{j}_{q}]" for j in range(len(DINGS)) for q in range(4)) + f"amix=inputs={len(cuts) + len(hits) + nb}:normalize=0:duration=longest,volume=0.5,apad=whole_dur={DUR}[fx]"
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
for out, snd in (("Aureus-Cinematic-Ad-v2.mp4", "full.wav"), ("Aureus-Cinematic-Ad-v2-NO-MUSIC.mp4", "nomusic.wav")):
    run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav(snd), "-map", "0:v", "-map", "1:a"] + enc + [os.path.join(HERE, out)])

print("done")
