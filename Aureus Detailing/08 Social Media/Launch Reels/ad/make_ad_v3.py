"""Aureus ad v3: ONE CONTINUOUS TAKE. Eight Kling links, each ending on the exact frame the next begins on, then him on camera.
Raw footage: no grade, no zooms, no flashes, no pop-ups. ASMR first, one consistent voice, music low. 0 credits.
Run: /opt/miniconda3/bin/python -I make_ad_v3.py  -> Aureus-Ad-v3.mp4, Aureus-Ad-v3-NO-MUSIC.mp4"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); AUREUS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FONT = os.path.join(AUREUS, "04 Fonts", "Montserrat-Variable.ttf"); LOGO = os.path.join(AUREUS, "02 Logo", "PNG", "aureus-horizontal-flat-white.png")
WORK = os.path.join(HERE, "build3"); os.makedirs(WORK, exist_ok=True)
W, H, FPS = 1080, 1920, 24
NAVY, PINK = (7, 26, 51), (255, 77, 141)
def run(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: sys.exit(" ".join(c[:8]) + "\n" + r.stderr[-1200:])
C = lambda n: os.path.join(HERE, "clips", n)
# (source, start s, length s, ASMR for the first half, ASMR for the second half). Every link is played whole, so last frame = next first frame.
L = lambda k: C(f"links/L{k}.mp4")
LK = {"A": ("foam", "rinse"), "B": ("rinse", "p1"), "1": ("p1", "p2"), "2": ("p2", "i1"), "3": ("i1", "i2"), "4": ("i2", "w1"), "5": ("w1", "w2"), "6": ("w2", "macro"),
      "C": ("i1", "w1"), "D": ("w1", "macro"), "7": ("macro", None), "8": (None, None)}
# 30 s cut for paid ads: foam, rinse, polish, wax, steam, wheels, sealed paint, bell, him.  36 s full cut adds vents and the wheel rinse.
CUT = os.environ.get("CUT", "30"); ORDER = "AB12CD78" if CUT == "30" else "AB12345678"
EDIT = [(L(k), 0, 3.0) + LK[k] + (k,) for k in ORDER] + [(C("speak3.mp4"), 0, 6.0, None, None, "S")]
STARTS = []; t = 0.0
for e in EDIT: STARTS.append(t); t += e[2]
DUR = round(t, 3)

# ---- picture: raw, only scaled to 1080x1920 ----
segs = []
for k, (src, st, ln, _a, _b, _c) in enumerate(EDIT):
    o = os.path.join(WORK, f"s{k:02d}.mp4"); n = round(ln * FPS)
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(st), "-i", src, "-vf", f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},format=yuv420p",
         "-frames:v", str(n), "-an", "-c:v", "libx264", "-crf", "13", "-preset", "medium", o]); segs.append(o)
lst = os.path.join(WORK, "list.txt"); open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
XF = 0.125   # 3-frame dissolve into the speaking shot (link 8's last frame and his first frame differ slightly in size); last frame held 3 frames so the film stays 30.0 s
open(lst, "w").write("".join(f"file '{x}'\n" for x in segs[:-1])); partA = os.path.join(WORK, "a.mp4")
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", partA])
base = os.path.join(WORK, "base.mp4")
run(["ffmpeg", "-y", "-v", "error", "-i", partA, "-i", segs[-1], "-filter_complex", f"[1:v]tpad=stop_mode=clone:stop_duration={XF}[b];[0:v][b]xfade=transition=fade:duration={XF}:offset={STARTS[-1] - XF},format=yuv420p[v]",
     "-map", "[v]", "-r", str(FPS), "-c:v", "libx264", "-crf", "12", "-preset", "medium", base])
STARTS[-1] -= XF

# ---- graphics: a few frosted-glass labels (the footage itself blurred behind them), warm white only, slow fades. No brand colours on screen. ----
from PIL import ImageFilter
INK = (255, 250, 242)                                   # warm white that sits with golden-hour light
def font(s, w="SemiBold"): f = ImageFont.truetype(FONT, s); f.set_variation_by_name(w); return f
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
_m = {}
def rmask(w, h, r):
    if (w, h, r) not in _m:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255); _m[(w, h, r)] = m
    return _m[(w, h, r)]
def glass(fr, x, y, w, h, a, r=28):
    """frosted glass panel: blur what is behind it, lift it slightly, thin light edge, soft shadow"""
    if a <= 0.01: return
    x, y = int(x), int(y); m = rmask(w, h, r).point(lambda v: int(v * a))
    sh = Image.new("L", (w + 60, h + 60), 0); sh.paste(rmask(w, h, r).point(lambda v: int(v * 0.28 * a)), (30, 38)); sh = sh.filter(ImageFilter.GaussianBlur(16))
    fr.paste((0, 0, 0), (x - 30, y - 30), sh)
    reg = fr.crop((x, y, x + w, y + h)).filter(ImageFilter.GaussianBlur(20)); reg = Image.blend(reg, Image.new("RGB", (w, h), (255, 246, 232)), 0.13); reg = Image.blend(reg, Image.new("RGB", (w, h), (20, 16, 12)), 0.10)
    fr.paste(reg, (x, y), m)
    edge = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(edge); d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, outline=(255, 255, 255, int(95 * a)), width=2)
    d.line([(r, 1), (w - r, 1)], fill=(255, 255, 255, int(150 * a)), width=1); fr.paste(edge, (x, y), edge)
_t = {}
def text(fr, s, size, x, y, a, w="SemiBold", anchor="l", op=1.0):
    k = (s, size, w)
    if k not in _t:
        f = font(size, w); l, t, r, b = f.getbbox(s); im = Image.new("RGBA", (r - l + 8, b - t + 8), (0, 0, 0, 0)); ImageDraw.Draw(im).text((4 - l, 4 - t), s, font=f, fill=INK); _t[k] = im
    im = _t[k]; al = im.getchannel("A").point(lambda v: int(v * a * op)); x = x if anchor == "l" else x - im.width / 2
    fr.paste(im, (int(x), int(y - im.height / 2)), al); return im.width
def env(t, a0, a1, fin=0.4, fout=0.35): return ease((t - a0) / fin) * (1 - ease((t - (a1 - fout)) / fout)) if a0 <= t <= a1 else 0.0
NAME = {"foam": "Snow foam pre-wash", "rinse": "Rinse", "p1": "Machine polish", "p2": "Hand wax seal", "i1": "Interior steam clean", "i2": "Vents and dash",
        "w1": "Wheels, by hand", "w2": "Pressure rinse", "macro": "Sealed. Water beads off."}
STEPS = [(0.3, 1.5, NAME[EDIT[0][3]])]
acts = [e[4] for e in EDIT if e[4]]
for k, e in enumerate(EDIT):                                                      # each activity runs from late in one link to early in the next
    if e[4]: STEPS.append((STARTS[k] + 2.0, STARTS[k] + (4.5 if k + 1 < len(EDIT) and EDIT[k + 1][3] == e[4] else 2.95), NAME[e[4]]))
SP = STARTS[-1]; iW = next(k for k, e in enumerate(EDIT) if e[3] == "w1"); i7 = next(k for k, e in enumerate(EDIT) if e[5] == "7")
SUBS = [(0.3, 2.7, "We come to you. Gold detail, $199."),
        (STARTS[iW] + 0.2, STARTS[iW] + 1.9, "Every spoke. By hand."), (STARTS[i7] + 0.3, STARTS[i7] + 1.9, "Yeah. That'll do."),
        (SP + 0.0, SP + 1.42, "We come to you."), (SP + 1.42, SP + 3.65, "Gold detail, $199."), (SP + 3.65, DUR, "Done properly, or it's not done.")]
lg = Image.open(LOGO).convert("RGBA"); lg = lg.crop(lg.getbbox()); lg = lg.resize((230, int(lg.height * 230 / lg.width)), Image.LANCZOS); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * 0.55)))
def draw(fr, t):
    fr.paste(lg, (48, 290 - lg.height // 2), lg)                                      # watermark, top left, quiet
    a = env(t, 0.5, 3.3)                                                              # his experience, once, small
    if a > 0: w = int(font(34).getlength("20 years on the tools")) + 52; glass(fr, 48, 336 + 10 * (1 - a), w, 62, a, 31); text(fr, "20 years on the tools", 34, 74, 367 + 10 * (1 - a), a)
    for n, (a0, a1, lab) in enumerate(STEPS):                                         # what he is doing, with a thin progress line across the seven steps
        a = env(t, a0, a1)
        if a <= 0: continue
        tw = int(font(40).getlength(lab)); w, h = max(tw, 260) + 64, 104; x, y = 48, 1300 + 14 * (1 - a)
        glass(fr, x, y, w, h, a); text(fr, lab, 40, x + 32, y + 40, a)
        d = ImageDraw.Draw(fr, "RGBA"); x0, x1, yy = x + 32, x + w - 32, y + 78; prog = (n + ease((t - a0) / (a1 - a0))) / len(STEPS)
        d.rounded_rectangle([x0, yy, x1, yy + 4], radius=2, fill=(255, 255, 255, int(70 * a))); d.rounded_rectangle([x0, yy, x0 + (x1 - x0) * prog, yy + 4], radius=2, fill=INK + (int(235 * a),))
    for a0, a1, line in SUBS:                                                         # his words, for viewers watching muted
        a = env(t, a0, a1, 0.18, 0.15)
        if a > 0: w = int(font(42).getlength(line)) + 64; glass(fr, (W - w) / 2, 1436, w, 78, a, 39); text(fr, line, 42, W / 2, 1474, a, anchor="c")
    a = env(t, SP + 2.6, DUR + 1, 0.6)                                                # the offer, one glass card, at the end
    if a > 0:
        w, h, x, y = 760, 300, (W - 760) // 2, 340 + 16 * (1 - a); glass(fr, x, y, w, h, a, 36)
        text(fr, "Gold detail · $199", 58, W / 2, y + 66, a, "Bold", "c"); text(fr, "2 h 30 · at your place", 34, W / 2, y + 128, a, "Medium", "c", 0.85)
        ImageDraw.Draw(fr, "RGBA").line([(x + 60, y + 168), (x + w - 60, y + 168)], fill=(255, 255, 255, int(80 * a)), width=1)
        text(fr, "$25 off for our first 100 customers", 32, W / 2, y + 206, a, "Medium", "c", 0.85); text(fr, "Book: link in bio", 38, W / 2, y + 258, a, "SemiBold", "c")
pic = os.path.join(WORK, "pic.mp4"); N = round(DUR * FPS)
rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
wr = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "15", "-preset", "medium", pic], stdin=subprocess.PIPE)
for i in range(N):
    buf = rd.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    fr = Image.frombytes("RGB", (W, H), buf); draw(fr, i / FPS); wr.stdin.write(fr.tobytes())
wr.stdin.close(); wr.wait(); rd.kill()

# ---- sound: ASMR per shot, his voice (one voice: cloned from his on-camera take), quiet Perth ambience, music low ----
A = lambda n: os.path.join(HERE, "audio", n)
parts, ins, fc = [], [], ""
def add(path, at, gain_lufs, extra="", trim=None):
    global fc
    k = len(ins) // 2; ins.extend(["-i", path])
    tr = f"atrim=0:{trim}," if trim else ""
    fc += f"[{k}:a]{tr}aresample=48000,aformat=channel_layouts=stereo,loudnorm=I={gain_lufs}:TP=-2:LRA=9{extra},afade=in:d=0.08,adelay={int(at * 1000)}:all=1[a{k}];"; parts.append(f"[a{k}]")
for k, (src, st, ln, s1, s2, _c) in enumerate(EDIT):                                 # first activity, then the next, crossfading mid-link
    if s1: add(A(f"asmr/{s1}.mp3"), STARTS[k], -19, ",afade=out:st=1.35:d=0.4", trim=1.75)
    if s2: add(A(f"asmr/{s2}.mp3"), STARTS[k] + 1.35, -19, ",afade=in:d=0.4,afade=out:st=1.45:d=0.2", trim=1.65)
add(A("v4/h5.wav"), STARTS[iW] + 0.2, -15, ",silenceremove=start_periods=1:start_threshold=-42dB")
add(A("v4/h3.wav"), STARTS[i7] + 0.3, -16, ",silenceremove=start_periods=1:start_threshold=-42dB")
add(C("speak3.mp4"), SP, -16, trim=6.0)
add(A("asmr/amb.mp3"), 0, -33, f",afade=out:st={DUR - 1}:d=1", trim=DUR)
# bell: one bright strike when his finger hits the bell in link 8
BELL = STARTS[i7] + float(os.environ.get("BELL_AT", "2.6"))   # his finger lands on the bell late in link 7
ding = os.path.join(WORK, "ding.wav")
run(["ffmpeg", "-y", "-v", "error", "-filter_complex", "".join(f"sine=f={f}:d=1.8:r=48000,volume={v},afade=out:st=0.004:d=1.75:curve=exp[d{i}];" for i, (f, v) in enumerate([(2793, 0.5), (4610, 0.2), (6720, 0.1), (1396, 0.08)])) + "[d0][d1][d2][d3]amix=inputs=4:normalize=0[o]", "-map", "[o]", ding])
k = len(ins) // 2; ins.extend(["-i", ding]); fc += f"[{k}:a]aformat=channel_layouts=stereo,volume=0.9,adelay={int(BELL * 1000)}:all=1[a{k}];"; parts.append(f"[a{k}]")
mix_nm = os.path.join(WORK, "nomusic.wav")
run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", fc + "".join(parts) + f"amix=inputs={len(parts)}:normalize=0:duration=longest,apad=whole_dur={DUR},alimiter=limit=0.9[m]", "-map", "[m]", "-t", str(DUR), "-ar", "48000", mix_nm])
mix = os.path.join(WORK, "full.wav")   # music sits well under the ASMR: about -31 LUFS, ducked further by the sound, swells a little on the finale
run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "1", "-i", A("music.mp3"), "-i", mix_nm, "-filter_complex",
     f"[0:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-31:TP=-6,volume='if(lt(t,{SP}),1,1.6)':eval=frame,afade=in:d=1.5,afade=out:st={DUR - 1.2}:d=1.2[m];[1:a]asplit[sc][x];[m][sc]sidechaincompress=threshold=0.02:ratio=4:attack=30:release=350[md];[md][x]amix=inputs=2:normalize=0:duration=shortest,alimiter=limit=0.9[a]",
     "-map", "[a]", "-t", str(DUR), mix])
enc = ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest"]
for out, snd in ((f"Aureus-Ad-v3-{CUT}s.mp4", mix), (f"Aureus-Ad-v3-{CUT}s-NO-MUSIC.mp4", mix_nm)):
    run(["ffmpeg", "-y", "-v", "error", "-i", pic, "-i", snd, "-map", "0:v", "-map", "1:a"] + enc + [os.path.join(HERE, out)])
print("done", DUR)
