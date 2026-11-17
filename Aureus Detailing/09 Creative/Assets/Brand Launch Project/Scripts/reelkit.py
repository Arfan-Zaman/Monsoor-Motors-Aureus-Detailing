"""Shared editing kit for the Aureus brand launch reels. Free, local: ffmpeg + Pillow + numpy. 0 credits.

Layout (09 Creative/Assets/Brand Launch Project): Scripts/ (this), Audio/, Shots/<set>/, Keyframes/, Notes/.
Renders go to Renders/ (copy finals to 09 Creative/Reels/<category>/); scratch files go to ~/local-ai/build (outside the folder).
Videos are never in git."""
import glob, json, os, re, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
AUREUS = HERE
while os.path.basename(AUREUS) != "Aureus Detailing" and os.path.dirname(AUREUS) != AUREUS: AUREUS = os.path.dirname(AUREUS)
OUT = os.path.join(PROJECT, "Renders")
SCRATCH = os.path.expanduser("~/local-ai/build")
SHOTS = os.path.join(PROJECT, "Shots")
SHOOT = os.environ.get("AUREUS_SHOOT", os.path.join(SHOTS, "Set 1 - Pearl White Sedan"))
if not os.path.isabs(SHOOT): SHOOT = os.path.join(SHOTS, SHOOT)
AUD = os.path.join(PROJECT, "Audio")
FONTS = os.path.join(AUREUS, "04 Fonts"); LOGOS = os.path.join(AUREUS, "02 Logo", "PNG")
W, H, FPS = 1080, 1920, 30
AQUA, NAVY, INK = (0, 168, 168), (7, 26, 51), (255, 252, 246)
TAKES = json.load(open(os.path.join(HERE, "takes.json"))) if os.path.exists(os.path.join(HERE, "takes.json")) else {}
PLATES = {}   # code -> (x, y, w, h) in the 1080x1920 frame; filled in after reviewing the footage

def clip(code):
    """The chosen take of a shot (takes.json), else the last take found in Shoot/."""
    if code in TAKES: return os.path.join(SHOOT, TAKES[code])
    fs = sorted(f for f in glob.glob(os.path.join(SHOOT, f"{code}*")) if re.search(r"\.(mov|mp4|m4v)$", f, re.I))
    if not fs: raise FileNotFoundError(f"No clip for shot {code} in {SHOOT}")
    return fs[-1]

def run(c): subprocess.run(c, check=True)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

# ---------- picture ----------
def build_base(segs, work, grade=""):
    """segs: list of dicts {clip, at (source in-point), d (length), zoom, black}. Real speed only."""
    os.makedirs(work, exist_ok=True); parts = []
    for i, s in enumerate(segs):
        if not s.get("black"):                          # never read past the end of a shot (generated shots are ~3 s)
            room = dur(clip(s["clip"])) - s.get("at", 0.3) - 0.05
            if s["d"] > room: s["d"] = max(1 / FPS, room)
        p = os.path.join(work, f"seg{i:02d}.mp4"); n = max(1, round(s["d"] * FPS))
        if s.get("black"):
            run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}", "-frames:v", str(n), "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "12", p])
        else:
            z = s.get("zoom", 1.0)            # fill 9:16 at the zoom asked for, whatever the phone recorded
            zw, zh = int(round(W * z / 2) * 2), int(round(H * z / 2) * 2)
            vf = (f"[0:v]fps={FPS},scale={zw}:{zh}:force_original_aspect_ratio=increase:flags=lanczos,"
                  f"crop={W}:{H}:(iw-{W})/2:(ih-{H})*{s.get('y', 0.5)},setsar=1")
            bx = s.get("blur") or PLATES.get(s["clip"])
            if bx:                                  # number plates always blurred (house rule)
                x, y, w, h = bx; vf += f",split[a][b];[b]crop={w}:{h}:{x}:{y},boxblur=24:3[bb];[a][bb]overlay={x}:{y}"
            vf += (f",{grade}" if grade else "") + ",format=yuv420p[v]"
            run(["ffmpeg", "-y", "-v", "error", "-ss", str(s.get("at", 0.3)), "-i", clip(s["clip"]), "-frames:v", str(n), "-filter_complex", vf, "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "12", "-preset", "fast", p])
        parts.append(p)
    lst = os.path.join(work, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    base = os.path.join(work, "base.mp4"); run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base])
    starts, t = [], 0.0
    for s in segs: starts.append(t); t += max(1, round(s["d"] * FPS)) / FPS
    return base, starts, t

def render(base, out, total, draw):
    """Read the base video frame by frame, let draw(img, t) paint on it, write the result."""
    N = round(total * FPS)
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "slow", out], stdin=subprocess.PIPE)
    for i in range(N):
        buf = rd.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        fr = Image.frombytes("RGB", (W, H), buf); fr = draw(fr, i / FPS) or fr; wr.stdin.write(fr.tobytes())
    wr.stdin.close(); wr.wait(); rd.kill()

_f = {}
def font(name, size, var=None):
    k = (name, size, var)
    if k not in _f:
        f = ImageFont.truetype(os.path.join(FONTS, name), size)
        if var: f.set_variation_by_name(var)
        _f[k] = f
    return _f[k]
MONT = "Montserrat-Variable.ttf"; MONTI = "Montserrat-Italic-Variable.ttf"; ANTON = "Anton-Regular.ttf"; SERIF = "InstrumentSerif-Italic.ttf"

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def env(t, a0, a1, fin=0.3, fout=0.25): return ease((t - a0) / fin) * (1 - ease((t - (a1 - fout)) / fout)) if a0 <= t <= a1 else 0.0

def text_img(s, f, fill=INK, shadow=0.35, blur=10):
    l, tp, r, b = f.getbbox(s); pad = blur * 2 + 6
    im = Image.new("RGBA", (r - l + pad * 2, b - tp + pad * 2), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("L", im.size, 0); ImageDraw.Draw(sh).text((pad - l, pad - tp + 3), s, font=f, fill=int(255 * shadow))
        im.paste((0, 0, 0, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(im).text((pad - l, pad - tp), s, font=f, fill=fill); return im, pad

def paste(fr, im, cx, cy, a=1.0, scale=1.0):
    if a <= 0.01: return
    if abs(scale - 1) > 0.005: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    m = im.getchannel("A")
    if a < 0.999: m = m.point(lambda v: int(v * a))
    fr.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), m)

_m = {}
def rmask(w, h, r):
    if (w, h, r) not in _m:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255); _m[(w, h, r)] = m
    return _m[(w, h, r)]
def glass(fr, x, y, w, h, a, r=32):
    """Frosted glass card (house style): footage blurred behind, thin light edge."""
    if a <= 0.01: return
    x, y, w, h = int(x), int(y), int(w), int(h); m = rmask(w, h, r).point(lambda v: int(v * a))
    reg = fr.crop((x, y, x + w, y + h)).filter(ImageFilter.GaussianBlur(22)); reg = Image.blend(reg, Image.new("RGB", (w, h), (12, 18, 28)), 0.28)
    fr.paste(reg, (x, y), m)
    e = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(e); d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, outline=(255, 255, 255, int(85 * a)), width=2)
    fr.paste(e, (x, y), e)

def logo(name, width, opacity=1.0):
    lg = Image.open(os.path.join(LOGOS, name)).convert("RGBA"); lg = lg.crop(lg.getbbox())
    lg = lg.resize((width, int(lg.height * width / lg.width)), Image.LANCZOS)
    if opacity < 1: lg.putalpha(lg.getchannel("A").point(lambda v: int(v * opacity)))
    return lg

def flash(fr, k):
    """Overexposure flash (sun blow-out between micro cuts), k 0..1."""
    if k <= 0: return fr
    a = np.asarray(fr).astype(np.float32); a = a + (255 - a) * k * np.array([1.0, 0.97, 0.9]); return Image.fromarray(a.clip(0, 255).astype(np.uint8))

# ---------- sound ----------
VOX = "highpass=f=80,equalizer=f=180:t=q:w=1:g=1.5,equalizer=f=3000:t=q:w=1.2:g=2,deesser=i=0.25,acompressor=threshold=0.1:ratio=3:attack=8:release=160:makeup=2,loudnorm=I=-15:TP=-2:LRA=6"
MASTER = "highpass=f=30,acompressor=threshold=0.3:ratio=2:attack=15:release=250,alimiter=limit=0.89"

class Mix:
    def __init__(s): s.ins, s.fc, s.parts = [], "", []
    def add(s, path, at, chain="anull", trim=None, ss=None):
        k = len([x for x in s.ins if x == "-i"])
        s.ins += (["-ss", str(ss)] if ss else []) + ["-i", path]; tr = f"atrim=0:{trim}," if trim else ""
        s.fc += f"[{k}:a]{tr}aresample=48000,aformat=channel_layouts=stereo,{chain},adelay={int(max(0, at) * 1000)}:all=1[a{k}];"; s.parts.append(f"[a{k}]")
    def write(s, out, total):
        run(["ffmpeg", "-y", "-v", "error"] + s.ins + ["-filter_complex", s.fc + "".join(s.parts) +
             f"amix=inputs={len(s.parts)}:normalize=0:duration=longest,apad=whole_dur={total},{MASTER}[m]", "-map", "[m]", "-t", str(total), "-ar", "48000", out])

def ding(path):
    run(["ffmpeg", "-y", "-v", "error", "-filter_complex", "".join(
        f"sine=f={f}:d=1.4:r=48000,volume={v},afade=out:st=0.004:d=1.2:curve=exp[d{i}];" for i, (f, v) in enumerate([(2793, 0.5), (4610, 0.2), (6720, 0.1), (1396, 0.08)]))
        + "[d0][d1][d2][d3]amix=inputs=4:normalize=0[o]", "-map", "[o]", path])

def whoosh(path, d=0.45):
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"anoisesrc=d={d}:c=pink:r=48000:a=0.5", "-af",
         f"bandpass=f=1800:width_type=o:w=2,afade=in:d={d*0.7}:curve=exp,afade=out:st={d*0.7}:d={d*0.3},volume=0.5", path])

def fit_line(src, out, target=None):
    """Trim silence from a generated voice line; optionally stretch it to an exact length (for lip timing)."""
    tmp = out + ".trim.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse", tmp])
    if target:
        r = dur(tmp) / target; r = min(2.0, max(0.5, r))
        run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-af", f"atempo={r:.4f}", out]); os.remove(tmp)
    else: os.replace(tmp, out)
    return dur(out)

def finish(pic, mixes, names):
    os.makedirs(OUT, exist_ok=True)
    for snd, name in zip(mixes, names):
        run(["ffmpeg", "-y", "-v", "error", "-i", pic, "-i", snd, "-map", "0:v", "-map", "1:a", "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", os.path.join(OUT, name)])

def beats(path):
    """Beat times of a music file (librosa, in the local-ai env), cached as JSON next to it."""
    js = path + ".beats.json"
    if not os.path.exists(js):
        code = ("import librosa,json,sys;y,sr=librosa.load(sys.argv[1],sr=22050);t,b=librosa.beat.beat_track(y=y,sr=sr);"
                "o=librosa.onset.onset_strength(y=y,sr=sr);json.dump({'tempo':float(t if not hasattr(t,'__len__') else t[0]),'beats':librosa.frames_to_time(b,sr=sr).tolist()},open(sys.argv[2],'w'))")
        run([os.path.expanduser("~/local-ai/.venv/bin/python"), "-I", "-c", code, path, js])
    return json.load(open(js))
