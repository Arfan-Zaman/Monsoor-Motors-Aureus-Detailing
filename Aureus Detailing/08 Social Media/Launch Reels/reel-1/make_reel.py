"""Builds Aureus launch reel 1 from the stills and the speaking clip. No credits used.
Run: /opt/miniconda3/bin/python -I make_reel.py   (needs ffmpeg). Outputs two MP4s in this folder."""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
AUREUS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FONT = os.path.join(AUREUS, "04 Fonts", "Montserrat-Variable.ttf")
LOGO_END = os.path.join(AUREUS, "02 Logo", "PNG", "aureus-stacked-3d-chrome.png")
LOGO_BUG = os.path.join(AUREUS, "02 Logo", "PNG", "aureus-horizontal-flat-white.png")
WORK = os.path.join(HERE, "build"); os.makedirs(WORK, exist_ok=True)
W, H, FPS = 1080, 1920, 24
NAVY, AQUA, PINK, WHITE = (7, 26, 51), (0, 168, 168), (255, 77, 141), (245, 248, 252)
SAFE_TOP, SAFE_BOT = 250, 1520   # apps cover the top 250 px and the bottom 400 px

def font(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name(weight); return f

def grad(img, y0, y1, a0, a1):
    """vertical navy gradient from alpha a0 at y0 to a1 at y1"""
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    lo, hi = min(y0, y1), max(y0, y1)
    for y in range(lo, hi):
        t = (y - y0) / (y1 - y0); d.line([(0, y), (W, y)], fill=NAVY + (int(a0 + (a1 - a0) * t),))
    img.alpha_composite(g)

def centre(d, y, parts, size, weight="Bold", shadow=True):
    """parts = [(text, colour), ...] drawn on one centred line; returns bottom y"""
    f = font(size, weight); total = sum(d.textlength(t, font=f) for t, _ in parts); x = (W - total) / 2
    for t, c in parts:
        if shadow: d.text((x + 2, y + 3), t, font=f, fill=(2, 8, 18, 170))
        d.text((x, y), t, font=f, fill=c); x += d.textlength(t, font=f)
    return y + int(size * 1.22)

def pill(img, y, text, size=58, fg=WHITE, bg=NAVY + (225,), pad=(34, 20)):
    d = ImageDraw.Draw(img); f = font(size, "Bold"); tw = d.textlength(text, font=f)
    w, h = tw + 2 * pad[0], size + 2 * pad[1]; x = (W - w) / 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=h / 2, fill=bg)
    d.text((x + pad[0], y + pad[1] - size * 0.12), text, font=f, fill=fg)

def paste_logo(img, path, width, x, y):
    lg = Image.open(path).convert("RGBA"); lg = lg.crop(lg.getbbox())
    lg = lg.resize((width, int(lg.height * width / lg.width)), Image.LANCZOS)
    img.alpha_composite(lg, (int(x if x is not None else (W - width) / 2), y)); return y + lg.height

def new(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))
def save(img, name): p = os.path.join(WORK, name); img.save(p); return p

# ---------- overlays ----------
o = new(); grad(o, 0, 760, 215, 0); d = ImageDraw.Draw(o)
y = centre(d, 300, [("We come to you.", WHITE)], 112, "ExtraBold")
centre(d, y + 6, [("Gold detail, ", WHITE), ("$199", PINK)], 78, "Bold")
HOOK = save(o, "ov-hook.png")

SPEECH = [(0.00, 1.03, "We come to you."), (1.03, 1.66, "Gold detail:"), (1.66, 3.09, "polish, wax sealant,"),
          (3.09, 4.42, "interior steam clean,"), (4.42, 5.06, "leather care."), (5.06, 6.00, "$199.")]
SUBS = []
for i, (a, b, t) in enumerate(SPEECH):
    o = new(); pill(o, 1424, t, fg=PINK if "$" in t else WHITE); SUBS.append((a, b, save(o, f"ov-sub{i}.png")))

def step(lines, name):
    o = new(); grad(o, 1000, 1920, 0, 235); grad(o, 0, 520, 150, 0); d = ImageDraw.Draw(o)
    paste_logo(o, LOGO_BUG, 300, None, 268)
    y = 1500 - len(lines) * 84 - 26
    d.rounded_rectangle([(W - 96) / 2, y, (W + 96) / 2, y + 8], radius=4, fill=AQUA); y += 30
    for ln in lines: y = centre(d, y, [(ln, WHITE)], 66, "Bold")
    return save(o, name)
ST3 = step(["Machine polish", "+ wax sealant"], "ov-s3.png")
ST4 = step(["Interior steam clean", "+ leather care"], "ov-s4.png")
ST5 = step(["Vents disinfected", "Wheels deep cleaned"], "ov-s5.png")

o = new(); o.alpha_composite(Image.new("RGBA", (W, H), NAVY + (150,))); grad(o, 0, 1100, 150, 0); grad(o, 900, 1920, 0, 200)
d = ImageDraw.Draw(o); y = paste_logo(o, LOGO_END, 440, None, 262) + 34
y = centre(d, y, [("Gold  ", WHITE), ("$199", PINK)], 132, "ExtraBold")
y = centre(d, y, [("2 h 30 · at your place", WHITE)], 58, "SemiBold") + 34
f = font(46, "Bold"); l1, l2 = "Launch offer: $25 off", "for our first 100 customers"
bw = max(d.textlength(l1, font=f), d.textlength(l2, font=f)) + 96; bx = (W - bw) / 2
d.rounded_rectangle([bx, y, bx + bw, y + 160], radius=36, fill=PINK)
for k, ln in enumerate((l1, l2)): d.text(((W - d.textlength(ln, font=f)) / 2, y + 24 + k * 58), ln, font=f, fill=NAVY)
y += 160 + 44
y = centre(d, y, [("Mobile within 20 km of Victoria Park", WHITE)], 44, "Medium")
y = centre(d, y + 8, [("Book: link in bio", (95, 240, 230))], 60, "Bold")
assert y <= SAFE_BOT, y
END = save(o, "ov-end.png")

# ---------- video segments ----------
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-1500:])

def still(src, ov, dur, out, z0=1.0, z1=1.09, fx=0.5, fy=0.5, ov_at=0.15):
    n = int(dur * FPS)
    vf = (f"[0:v]scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840,"
          f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}':d={n}:s={W}x{H}:fps={FPS}[bg];" +
          (f"[1:v]format=rgba,fade=in:st={ov_at}:d=0.35:alpha=1[ov];" if ov_at else "[1:v]format=rgba[ov];") +
          f"[bg][ov]overlay=0:0:format=auto,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(HERE, "stills", src), "-loop", "1", "-t", str(dur), "-i", ov,
         "-filter_complex", vf, "-map", "[v]", "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-crf", "14", "-preset", "medium", out])

seg = lambda n: os.path.join(WORK, f"seg{n}.mp4")
still("s1-arrival.png", HOOK, 2, seg(1), 1.0, 1.10, 0.5, 0.62, ov_at=0.0)   # text on screen from frame one
ins = ["-i", os.path.join(HERE, "speaking-raw.mp4")]; fc = f"[0:v]scale={W}:{H},fps={FPS}[b0];"; last = "b0"
for i, (a, b, p) in enumerate(SUBS):
    ins += ["-i", p]; fc += f"[{last}][{i+1}:v]overlay=0:0:enable='between(t,{a},{b - 0.001})'[b{i+1}];"; last = f"b{i+1}"
run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", fc + f"[{last}]format=yuv420p[v]", "-map", "[v]", "-an", "-t", "6",
     "-r", str(FPS), "-c:v", "libx264", "-crf", "14", "-preset", "medium", seg(2)])
still("s3-polish.png", ST3, 3, seg(3), 1.10, 1.0, 0.5, 0.45)
still("s4-interior-v2.png", ST4, 3, seg(4), 1.0, 1.10, 0.55, 0.5)
still("s5-wheel.png", ST5, 3, seg(5), 1.10, 1.0, 0.6, 0.55)
still("s6-finish.png", END, 5, seg(6), 1.0, 1.07, 0.5, 0.6, ov_at=0.7)       # clean car first, then the offer

lst = os.path.join(WORK, "list.txt"); open(lst, "w").write("".join(f"file '{seg(i)}'\n" for i in range(1, 7)))
silent = os.path.join(WORK, "picture.mp4")
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-r", str(FPS), silent])

# ---------- sound ----------
voice = "[1:a]loudnorm=I=-15:TP=-1.5:LRA=7,adelay=2000:all=1,apad=whole_dur=22[vo]"
cuts = [2, 8, 11, 14, 17]
fx = os.path.join(WORK, "fx.wav")   # soft whoosh on each cut, built as its own 22 s track
wf = "".join(f"anoisesrc=d=0.45:c=pink:r=48000:a=0.5,bandpass=f=900:width_type=h:w=1400,afade=in:d=0.28:curve=qsin,afade=out:st=0.28:d=0.17,"
             f"aformat=channel_layouts=stereo,adelay={int((c - 0.28) * 1000)}:all=1[w{i}];" for i, c in enumerate(cuts))
wf += "".join(f"[w{i}]" for i in range(len(cuts))) + f"amix=inputs={len(cuts)}:normalize=0:duration=longest,volume=0.5,apad=whole_dur=22[fx]"
run(["ffmpeg", "-y", "-v", "error", "-filter_complex", wf, "-map", "[fx]", "-t", "22", "-ar", "48000", fx])
vo = os.path.join(WORK, "voice.wav"); mixed = os.path.join(WORK, "mix.wav")
run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(HERE, "speaking-raw.mp4"), "-filter_complex", voice.replace("[1:a]", "[0:a]"), "-map", "[vo]", "-t", "22", "-ar", "48000", "-ac", "2", vo])
run(["ffmpeg", "-y", "-v", "error", "-i", vo, "-i", fx, "-filter_complex", "[0:a][1:a]amix=inputs=2:normalize=0:duration=first[a]", "-map", "[a]", "-ar", "48000", "-ac", "2", mixed])
enc = ["-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", "22", "-video_track_timescale", "24000"]
A = os.path.join(HERE, "Aureus-Reel-1-Gold-Mobile-Detail.mp4"); B = os.path.join(HERE, "Aureus-Reel-1-Gold-Mobile-Detail-CLEAN.mp4")
for out, snd in ((A, mixed), (B, vo)):
    run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", snd, "-map", "0:v", "-map", "1:a"] + enc + [out])
print("done", A, B)
