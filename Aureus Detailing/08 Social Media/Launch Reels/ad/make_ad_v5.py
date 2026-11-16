"""Aureus ad v5: he narrates the whole film in one voice; separate real-looking shots joined by short dissolves; raw footage at real speed;
a few muted glass visualisations; logo at the bottom; full sound mix (voice, per-shot sound, ambience, music) mastered for social. 0 credits.
Run: /opt/miniconda3/bin/python -I make_ad_v5.py  -> Aureus-Ad-v5.mp4, Aureus-Ad-v5-NO-MUSIC.mp4"""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); AUREUS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FONT = os.path.join(AUREUS, "04 Fonts", "Montserrat-Variable.ttf"); LOGO = os.path.join(AUREUS, "02 Logo", "PNG", "aureus-horizontal-flat-white.png")
WORK = os.path.join(HERE, "build5"); os.makedirs(WORK, exist_ok=True)
W, H, FPS, XF = 1080, 1920, 24, 0.25
def run(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: sys.exit(" ".join(c[:8]) + "\n" + r.stderr[-1500:])
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
C = lambda n: os.path.join(HERE, "clips", n); A = lambda n: os.path.join(HERE, "audio", n)

# ---- script: one voice all the way through. Each block = one spoken line + the shots it plays over (source, start, longest usable length, sound, label) ----
BLOCKS = [
 ("A", "Your car looks fine... until the sun hits it.", [(C("hook.mp4"), 0.6, 3.6, "hook", None), (C("van.mp4"), 1.2, 3.4, "van", None)]),
 ("B", None, [(C("speak3.mp4"), 0.0, 6.0, None, None)]),                                   # he says it to camera: "We come to you. Gold detail, 199. Done properly, or it's not done."
 ("C", "First, snow foam. It lifts the dirt before I touch the paint.", [(C("links/LA.mp4"), 0.0, 1.8, "foam", "Snow foam"), (C("links/LA.mp4"), 2.0, 1.0, "rinse", "Rinse"), (C("links/LB.mp4"), 0.0, 1.5, "rinse", "Rinse")]),
 ("D", "Then a machine polish. And wax, sealed in by hand.", [(C("p1.mp4"), 0.2, 2.7, "p1", "Machine polish"), (C("polish.mp4"), 1.5, 2.2, "p1", "Machine polish"), (C("p2.mp4"), 0.3, 2.6, "p2", "Hand wax")]),
 ("E", "Inside, steam cleans the leather. Every vent gets brushed.", [(C("i1.mp4"), 0.2, 2.7, "i1", "Steam clean"), (C("steam.mp4"), 1.5, 2.2, "i1", "Steam clean"), (C("i2.mp4"), 0.3, 2.6, "i2", "Vents")]),
 ("F", "Wheels, scrubbed by hand. Every spoke.", [(C("w1.mp4"), 0.3, 2.6, "w1", "Wheels"), (C("wheel.mp4"), 1.5, 2.2, "w1", "Wheels"), (C("w2.mp4"), 0.4, 2.5, "w2", "Wheels")]),
 ("G", "Two and a half hours later... that's your car.", [(C("macro.mp4"), 1.0, 3.6, "macro", "Sealed"), (C("hero.mp4"), 0.3, 2.7, "p2", None)]),
 ("H", "Aureus Detailing. Twenty years of experience. Book online, today.", [(C("bell.mp4"), 0.4, 2.6, None, None), (C("links/L8.mp4"), 0.0, 2.9, None, None)]),
]
SHOTS, BSTART, VOICE, t = [], {}, [], 0.0
for key, line, shots in BLOCKS:
    need = (6.0 if key == "B" else dur(A(f"v5/t{key}.wav")) + 0.45) + XF * len(shots)      # footage needed so the line fits between dissolves
    if key == "H": need = max(need, 2.6 + 1.2 + XF * 2)
    tot = sum(s[2] for s in shots); lens = [min(s[2], need * s[2] / tot) for s in shots]
    if key == "H": lens[0] = 2.6; lens[1] = 2.9
    BSTART[key] = t - XF * len(SHOTS) if SHOTS else 0.0
    for s, ln in zip(shots, lens): SHOTS.append((s[0], s[1], round(ln * FPS) / FPS, s[3], s[4], key)); t += round(ln * FPS) / FPS
STARTS = [sum(s[2] for s in SHOTS[:k]) - XF * k for k in range(len(SHOTS))]; DUR = STARTS[-1] + SHOTS[-1][2]
BSTART = {k: STARTS[next(i for i, s in enumerate(SHOTS) if s[5] == k)] for k, _, _ in BLOCKS}
BEND = {k: max(STARTS[i] + s[2] for i, s in enumerate(SHOTS) if s[5] == k) for k, _, _ in BLOCKS}

# ---- picture: raw shots at real speed, joined by 6-frame dissolves ----
ins, fc, last = [], "", None
for k, (src, st, ln, _s, _l, _b) in enumerate(SHOTS):
    ins += ["-ss", str(st), "-t", str(ln + 0.2), "-i", src]
    fc += f"[{k}:v]fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},trim=0:{ln},setpts=PTS-STARTPTS,format=yuv420p[c{k}];"
    if k == 0: last = "c0"
    else: fc += f"[{last}][c{k}]xfade=transition=fade:duration={XF}:offset={STARTS[k]:.4f}[x{k}];"; last = f"x{k}"
base = os.path.join(WORK, "base.mp4")
run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", fc.rstrip(";"), "-map", f"[{last}]", "-an", "-r", str(FPS), "-c:v", "libx264", "-crf", "12", "-preset", "medium", base])

# ---- glass graphics: footage blurred behind each panel, warm white only, slow moves ----
INK = (255, 250, 242)
def font(s, w="SemiBold"): f = ImageFont.truetype(FONT, s); f.set_variation_by_name(w); return f
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def env(t, a0, a1, fin=0.4, fout=0.35): return ease((t - a0) / fin) * (1 - ease((t - (a1 - fout)) / fout)) if a0 <= t <= a1 else 0.0
_m = {}
def rmask(w, h, r):
    if (w, h, r) not in _m:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255); _m[(w, h, r)] = m
    return _m[(w, h, r)]
def glass(fr, x, y, w, h, a, r=28):
    if a <= 0.01: return
    x, y, w, h = int(x), int(y), int(w), int(h); m = rmask(w, h, r).point(lambda v: int(v * a))
    sh = Image.new("L", (w + 60, h + 60), 0); sh.paste(rmask(w, h, r).point(lambda v: int(v * 0.26 * a)), (30, 38)); fr.paste((0, 0, 0), (x - 30, y - 30), sh.filter(ImageFilter.GaussianBlur(16)))
    reg = fr.crop((x, y, x + w, y + h)).filter(ImageFilter.GaussianBlur(20)); reg = Image.blend(reg, Image.new("RGB", (w, h), (255, 246, 232)), 0.12); reg = Image.blend(reg, Image.new("RGB", (w, h), (20, 16, 12)), 0.12)
    fr.paste(reg, (x, y), m)
    e = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(e); d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, outline=(255, 255, 255, int(90 * a)), width=2); d.line([(r, 1), (w - r, 1)], fill=(255, 255, 255, int(150 * a)), width=1)
    fr.paste(e, (x, y), e)
_t = {}
def text(fr, s, size, x, y, a, w="SemiBold", anchor="l", op=1.0):
    k = (s, size, w)
    if k not in _t:
        f = font(size, w); l, tp, r, b = f.getbbox(s); im = Image.new("RGBA", (r - l + 8, b - tp + 8), (0, 0, 0, 0)); ImageDraw.Draw(im).text((4 - l, 4 - tp), s, font=f, fill=INK); _t[k] = im
    im = _t[k]; x = x if anchor == "l" else x - im.width / 2 if anchor == "c" else x - im.width
    fr.paste(im, (int(x), int(y - im.height / 2)), im.getchannel("A").point(lambda v: int(v * a * op))); return im.width
lg = Image.open(LOGO).convert("RGBA"); lg = lg.crop(lg.getbbox()); lg = lg.resize((250, int(lg.height * 250 / lg.width)), Image.LANCZOS); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * 0.6)))
SERV = ["Snow foam", "Rinse", "Machine polish", "Hand wax", "Steam clean", "Vents", "Wheels", "Sealed"]
LAB = []                                                                                   # (start, end, label) merged over consecutive shots with the same label
for k, s in enumerate(SHOTS):
    if not s[4]: continue
    a0, a1 = STARTS[k], STARTS[k] + s[2]
    if LAB and LAB[-1][2] == s[4] and a0 - LAB[-1][1] < 0.3: LAB[-1] = (LAB[-1][0], a1, s[4])
    else: LAB.append((a0, a1, s[4]))
T0, T1 = LAB[0][0], LAB[-1][1]; SP = BSTART["B"]; OFFER = BSTART["H"] + 1.3
SUBS = [(BSTART[k] + 0.15, BEND[k] - 0.1, l) for k, l, _ in BLOCKS if l and k != "H"]
SUBS = [(a, b, l.replace("...", ",")) for a, b, l in SUBS]
SUBS += [(SP + 0.0, SP + 1.42, "We come to you."), (SP + 1.42, SP + 3.65, "Gold detail, $199."), (SP + 3.65, SP + 5.85, "Done properly, or it's not done.")]
def draw(fr, t):
    d = ImageDraw.Draw(fr, "RGBA")
    a = env(t, 0.5, BSTART["A"] + 2.4)                                                      # hook: a thin reticle finds the damage
    if a > 0:
        q = ease((t - 0.5) / 0.9); cx, cy, r = 588, 720, 170
        d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * q, fill=INK + (int(210 * a),), width=3)
        for ang in (0, 90, 180, 270): x1, y1 = cx + (r + 14) * math.cos(math.radians(ang)), cy + (r + 14) * math.sin(math.radians(ang)); x2, y2 = cx + (r + 44) * math.cos(math.radians(ang)), cy + (r + 44) * math.sin(math.radians(ang)); d.line([(x1, y1), (x2, y2)], fill=INK + (int(170 * a * q),), width=2)
        w = int(font(32).getlength("Swirl marks · water spots")) + 48; glass(fr, cx - w / 2, cy + r + 70, w, 58, a * q, 29); text(fr, "Swirl marks · water spots", 32, cx, cy + r + 99, a * q, anchor="c")
    a = env(t, SP + 0.3, SP + 3.2)                                                          # who he is, once
    if a > 0: w = int(font(34).getlength("20 years on the tools")) + 52; glass(fr, 48, 300 + 10 * (1 - a), w, 62, a, 31); text(fr, "20 years on the tools", 34, 74, 331 + 10 * (1 - a), a)
    a = env(t, SP + 1.5, SP + 5.6)                                                          # the price, as he says it
    if a > 0: glass(fr, W - 48 - 250, 300 + 10 * (1 - a), 250, 150, a, 34); text(fr, "Gold detail", 30, W - 48 - 125, 340 + 10 * (1 - a), a, "Medium", "c", 0.85); text(fr, "$199", 68, W - 48 - 125, 400 + 10 * (1 - a), a, "Bold", "c")
    a = env(t, T0 + 0.1, T1 - 0.05, 0.5, 0.4)                                               # service rail: eight dots, the current one named
    if a > 0:
        cur = max((i for i, (a0, a1, l) in enumerate(LAB) if t >= a0 - 0.05), default=0); lab = LAB[cur][2]; idx = SERV.index(lab)
        la = min(1.0, ease((t - LAB[cur][0]) / 0.3) + (0 if cur else 1)); x, y, w, h = 48, 1140, 420, 118
        glass(fr, x, y, w, h, a); text(fr, lab, 40, x + 30, y + 42, a * max(la, 0.0))
        for i in range(len(SERV)):
            cx = x + 36 + i * 46; on = i <= idx; rr = 9 if i == idx else 6
            d.ellipse([cx - rr, y + 86 - rr, cx + rr, y + 86 + rr], fill=INK + (int((235 if on else 70) * a),))
            if i < len(SERV) - 1: d.line([(cx + 12, y + 86), (cx + 34, y + 86)], fill=INK + (int((150 if i < idx else 50) * a),), width=2)
    a = env(t, BSTART["D"] + 0.3, BEND["D"] - 0.1)                                          # paint layers build as he polishes and waxes
    if a > 0:
        x, y = W - 48 - 300, 1130; glass(fr, x, y, 300, 184, a)
        for i, (nm, al) in enumerate([("Wax seal", 230), ("Polished", 150), ("Paint", 80)]):
            q = ease((t - BSTART["D"] - 0.5 - (2 - i) * 0.9) / 0.5)
            if q > 0: yy = y + 26 + i * 48; d.rounded_rectangle([x + 26, yy, x + 26 + 96 * q, yy + 34], radius=8, fill=INK + (int(al * a),)); text(fr, nm, 28, x + 140, yy + 17, a * q, "Medium")
    a = env(t, BSTART["G"] + 0.2, BEND["G"] - 0.1)                                          # the clock runs to 2 h 30
    if a > 0:
        q = ease((t - BSTART["G"] - 0.3) / 1.6); mins = int(150 * q); x, y = W - 48 - 300, 1180; glass(fr, x, y, 300, 134, a)
        text(fr, f"{mins // 60} h {mins % 60:02d}", 60, x + 150, y + 54, a, "Bold", "c"); d.rounded_rectangle([x + 30, y + 100, x + 270, y + 105], radius=2, fill=INK + (int(70 * a),)); d.rounded_rectangle([x + 30, y + 100, x + 30 + 240 * q, y + 105], radius=2, fill=INK + (int(235 * a),))
    for a0, a1, line in SUBS:                                                               # his words, for viewers watching muted
        a = env(t, a0, a1, 0.18, 0.15)
        if a > 0 and t < OFFER:
            ls = [line]
            if font(42).getlength(line) > 900:                                              # long lines break into two, near the middle
                ws = line.split(); k = min(range(1, len(ws)), key=lambda i: abs(len(" ".join(ws[:i])) - len(line) / 2)); ls = [" ".join(ws[:k]), " ".join(ws[k:])]
            w = int(max(font(42).getlength(l) for l in ls)) + 64; h = 76 + 54 * (len(ls) - 1); y = 1416 - h; glass(fr, (W - w) / 2, y, w, h, a, 38)
            for i, l in enumerate(ls): text(fr, l, 42, W / 2, y + 38 + 54 * i, a, anchor="c")
    a = env(t, OFFER, DUR + 1, 0.6)                                                         # the offer, one card
    if a > 0:
        w, h, x, y = 780, 300, (W - 780) // 2, 1100 + 16 * (1 - a); glass(fr, x, y, w, h, a, 36)
        text(fr, "Gold detail · $199", 58, W / 2, y + 66, a, "Bold", "c"); text(fr, "2 h 30 · at your place", 34, W / 2, y + 128, a, "Medium", "c", 0.85)
        d.line([(x + 60, y + 168), (x + w - 60, y + 168)], fill=(255, 255, 255, int(80 * a)), width=1)
        text(fr, "$25 off for our first 100 customers", 32, W / 2, y + 206, a, "Medium", "c", 0.85); text(fr, "Book online · link in bio", 38, W / 2, y + 258, a, "SemiBold", "c")
    fr.paste(lg, ((W - lg.width) // 2, 1478 - lg.height // 2), lg)                           # logo, bottom centre, inside the safe area
pic = os.path.join(WORK, "pic.mp4"); N = round(DUR * FPS)
rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
wr = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "15", "-preset", "medium", pic], stdin=subprocess.PIPE)
for i in range(N):
    buf = rd.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    fr = Image.frombytes("RGB", (W, H), buf); draw(fr, i / FPS); wr.stdin.write(fr.tobytes())
wr.stdin.close(); wr.wait(); rd.kill()

# ---- sound ----
VOX = "highpass=f=85,afftdn=nf=-32,equalizer=f=220:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=2.5,deesser=i=0.3,acompressor=threshold=0.09:ratio=3:attack=8:release=160:makeup=2,loudnorm=I=-15:TP=-2:LRA=6"
parts, ains, afc = [], [], ""
def add(path, at, chain, trim=None):
    global afc
    k = len(ains) // 2; ains.extend(["-i", path]); tr = f"atrim=0:{trim}," if trim else ""
    afc += f"[{k}:a]{tr}aresample=48000,aformat=channel_layouts=stereo,{chain},adelay={int(max(0, at) * 1000)}:all=1[a{k}];"; parts.append(f"[a{k}]")
for k, (src, st, ln, sfx, _l, key) in enumerate(SHOTS):                                     # real sound per shot, low under his voice, dissolving with the picture
    if sfx: add(A(f"asmr/{sfx}.mp3"), STARTS[k], f"loudnorm=I=-27:TP=-3:LRA=9,afade=in:d={XF},afade=out:st={ln - XF}:d={XF}", trim=ln)
for key, line, _ in BLOCKS:
    if line: add(A(f"v5/t{key}.wav"), BSTART[key] + (0.3 if key == "H" else 0.2), VOX)
add(C("speak3.mp4"), SP, VOX + f",afade=in:d=0.05,afade=out:st=5.8:d=0.2", trim=6.0)
add(A("asmr/amb.mp3"), 0, f"loudnorm=I=-36:TP=-6,afade=in:d=1,afade=out:st={DUR - 1.2}:d=1.2", trim=min(DUR, 29.5))
ding = os.path.join(WORK, "ding.wav"); BELL = BSTART["H"] + 1.1   # tap lands just as he starts the last line; kept low
run(["ffmpeg", "-y", "-v", "error", "-filter_complex", "".join(f"sine=f={f}:d=1.2:r=48000,volume={v},afade=out:st=0.004:d=0.9:curve=exp[d{i}];" for i, (f, v) in enumerate([(2793, 0.5), (4610, 0.2), (6720, 0.1), (1396, 0.08)])) + "[d0][d1][d2][d3]amix=inputs=4:normalize=0[o]", "-map", "[o]", ding])
add(ding, BELL, "volume=0.35")
nm = os.path.join(WORK, "nomusic.wav")
MASTER = "highpass=f=35,acompressor=threshold=0.25:ratio=2:attack=20:release=250,alimiter=limit=0.89"
run(["ffmpeg", "-y", "-v", "error"] + ains + ["-filter_complex", afc + "".join(parts) + f"amix=inputs={len(parts)}:normalize=0:duration=longest,apad=whole_dur={DUR},{MASTER}[m]", "-map", "[m]", "-t", str(DUR), "-ar", "48000", nm])
full = os.path.join(WORK, "full.wav")   # music bed: low, ducked by everything else, lifts for the offer
run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "1", "-i", A("music.mp3"), "-i", nm, "-filter_complex",
     f"[0:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-29:TP=-6,volume='if(lt(t,{OFFER}),1,1.5)':eval=frame,afade=in:d=1.2,afade=out:st={DUR - 1.5}:d=1.5[m];[1:a]asplit[sc][x];"
     f"[m][sc]sidechaincompress=threshold=0.02:ratio=5:attack=25:release=400[md];[md][x]amix=inputs=2:normalize=0:duration=shortest,{MASTER}[a]", "-map", "[a]", "-t", str(DUR), full])
for out, snd in (("Aureus-Ad-v5.mp4", full), ("Aureus-Ad-v5-NO-MUSIC.mp4", nm)):                # master to about -14 LUFS for social
    run(["ffmpeg", "-y", "-v", "error", "-i", pic, "-i", snd, "-map", "0:v", "-map", "1:a", "-af", "loudnorm=I=-14:TP=-1.5:LRA=8", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", os.path.join(HERE, out)])
print("done", round(DUR, 2), {k: round(v, 2) for k, v in BSTART.items()})
