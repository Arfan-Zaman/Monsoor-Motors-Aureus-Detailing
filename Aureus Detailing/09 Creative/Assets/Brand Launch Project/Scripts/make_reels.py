"""Build the three Aureus brand launch reels from the real shoot (SHOT-LIST.md). 0 credits, all local.

    ~/local-ai/.venv/bin/python make_reels.py [1] [2] [3]

Footage: Shoot/<code>-<take>.mov (pick takes in takes.json). Voice: his own lines from the clips; voice-over
from Shoot/VO/<line>.wav if recorded, else the local AI voice in audio/voice/. Music: audio/music/m1..m3.wav."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reelkit import *

VOICE = os.path.join(AUD, "voice")
VO_TEXT = {"r2_02": "Most places rush it.", "r2_03": "Shiny today. Swirls tomorrow.", "r2_05": "At Aureus, it's foam first,", "r2_06": "Machine polish,",
           "r2_07": "then wax, by hand.", "r2_08": "Every spoke.", "r2_09": "By hand.", "r2_10": "Steam for the leather.", "r2_12": "Gold Detail. One ninety-nine. We come to you."}; MUSIC = os.path.join(AUD, "music")
WORK = os.path.join(SCRATCH, "real-shoot"); os.makedirs(WORK, exist_ok=True)
WHISPER = os.path.expanduser("~/.cache/whisper.cpp/ggml-base.en.bin")

def words(src, ss=0.0, t=None):
    """Word timings (whisper.cpp) of a wav, or of a stretch of a clip's sound."""
    w16 = os.path.join(WORK, "w16.wav")
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(ss), "-i", src] + (["-t", str(t)] if t else []) + ["-vn", "-ac", "1", "-ar", "16000", w16])
    o = subprocess.run(["whisper-cli", "-m", WHISPER, "-f", w16, "-ml", "1", "-sow"], capture_output=True, text=True).stdout
    out = []
    for m in re.finditer(r"\[(\d+):(\d+):([\d.]+) --> (\d+):(\d+):([\d.]+)\][ \t]+(\S[^\n]*)", o):
        a = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]); b = int(m[4]) * 3600 + int(m[5]) * 60 + float(m[6])
        if re.search(r"[A-Za-z0-9$]", m[7]): out.append((a, b, m[7].strip()))
    return out

def pace(text, t0, t1):
    """Spread the script's words across the speech from t0 to t1, weighted by length."""
    ws = text.split(); wt = [len(re.sub(r"[^A-Za-z0-9$]", "", w)) + 2 for w in ws]; tot = sum(wt); out, c = [], 0
    for w, k in zip(ws, wt): out.append((t0 + (t1 - t0) * c / tot, t0 + (t1 - t0) * (c + k) / tot, w)); c += k
    return out

def find_line(code, text):
    """Where he says `text` in a clip: (in-point, length, word timings relative to the in-point)."""
    from difflib import SequenceMatcher
    ws = words(clip(code)); want = re.sub(r"[^a-z ]", "", text.lower()).split(); n = len(want)
    key = lambda w: re.sub(r"[^a-z]", "", w.lower())
    sim = lambda i: sum(SequenceMatcher(None, key(ws[i + k][2]), want[k]).ratio() for k in range(n)) / n
    best = max(range(max(1, len(ws) - n + 1)), key=lambda i: sim(i) if i + n <= len(ws) else 0, default=None)
    if best is None or best + n > len(ws) or sim(best) < 0.6: raise ValueError(f"Could not hear {text!r} in {code}; set its in-point by hand")
    i, j = best, best + n - 1
    # whisper's word times are loose: take the stretch of sound (pauses under 0.4 s merged) that best overlaps the words
    o = subprocess.run(["ffmpeg", "-v", "info", "-i", clip(code), "-vn", "-af", "silencedetect=noise=-35dB:d=0.4", "-f", "null", "-"], capture_output=True, text=True).stderr
    st_ = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", o)]; en_ = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", o)]
    edges = [0.0] + sorted(st_ + en_) + [dur(clip(code))]
    sounds = [(edges[k], edges[k + 1]) for k in range(0, len(edges) - 1, 2)] if (not st_ or st_[0] > 0.01) else [(edges[k], edges[k + 1]) for k in range(1, len(edges) - 1, 2)]
    w0, w1 = ws[i][0], ws[j][1]
    s0, e0 = max(sounds, key=lambda r: min(r[1], w1) - max(r[0], w0)) if sounds else (w0, w1)
    a = max(0.0, s0 - 0.3)
    e = e0
    return a, e - a + 0.35, pace(text, s0 - a, e - a)        # captions use the script's spelling and the real speech span

def vo(name):
    """His recorded voice-over if there is one, else the local AI voice (60-year-old, light Aussie)."""
    rec = sorted(glob.glob(os.path.join(SHOOT, "VO", f"{name}*.wav")) + glob.glob(os.path.join(SHOOT, "VO", f"{name}*.m4a")))
    src = rec[-1] if rec else os.path.join(VOICE, f"{name}.wav"); dst = os.path.join(WORK, f"v_{name}.wav")
    return dst, fit_line(src, dst)

def sound(mix, code, at_src, at, d, level=-26):
    """The clip's own recorded sound (foam, spray, polisher...), tucked under."""
    mix.add(clip(code), at, f"loudnorm=I={level}:TP=-4,afade=in:d=0.05,afade=out:st={max(0, d - 0.12):.2f}:d=0.12", trim=d, ss=at_src)

# =====================================================================  REEL A: teaser (Ref 1 setup)
def reel1():
    W1 = os.path.join(WORK, "r1")
    BW = "hue=s=0,eq=contrast=1.5:brightness=-0.05:gamma=0.92,noise=alls=9:allf=t+u"
    a11, a11d, _ = find_line("A11", "Perth. You ready?")
    mic = lambda *cs: [dict(clip=c, at=a, d=0.17) for c, a in cs]
    segs = ([dict(clip="A01", at=0.8, d=1.6), dict(clip="A03", at=1.0, d=1.0), dict(clip="A04", at=0.8, d=1.6), dict(clip="A05", at=0.8, d=1.5)]
            + mic(("A06", 0.5), ("A06", 2.5), ("A06", 4.5), ("A08", 1.5))
            + [dict(clip="A07", at=0.8, d=1.9), dict(clip="A08", at=1.0, d=1.6)]
            + mic(("A06", 6.5), ("A06", 8.5), ("A06", 10.5), ("A09", 1.0))
            + [dict(clip="A09", at=1.2, d=1.8), dict(clip="A10", at=0.8, d=1.8),
               dict(clip="A11", at=max(0.0, a11 - 1.6), d=a11d + 1.9), dict(black=True, d=3.4)])
    base, st, T = build_base(segs, W1, BW)
    END = st[-1]
    SL = [(st[1], st[2], [("PERTH", 250)], [st[1]]),
          (st[2], st[3], [("PERTH", 250), ("ARE YOU", 210), ("READY?", 300)], [st[2], st[2], st[2] + 0.5]),
          (st[8], st[9], [("MOBILE", 230), ("DETAILING", 210)], [st[8], st[8] + 0.45]),
          (st[14], st[15], [("WE COME", 230), ("TO YOU.", 260)], [st[14], st[14] + 0.5])]
    cache = {}
    def draw(fr, t):
        for k, (a0, a1, ls, rv) in enumerate(SL):            # huge condensed caps, first line in aqua, built line by line
            if a0 <= t < a1:
                if k not in cache: cache[k] = [text_img(s, font(ANTON, sz), AQUA if i == 0 else INK, 0.4, 14) for i, (s, sz) in enumerate(ls)]
                ims = cache[k]; hs = [im.height - 2 * p for im, p in ims]; gap = -18; y = 930 - (sum(hs) + gap * (len(hs) - 1)) / 2
                for (im, p), h, r0 in zip(ims, hs, rv):
                    if t >= r0: q = ease((t - r0) / 0.12); paste(fr, im, W / 2, y + h / 2, q, 1.18 - 0.18 * q)
                    y += h + gap
        if t >= END:                                          # black end card
            a = ease((t - END) / 0.35)
            if "lg" not in cache:
                cache["lg"] = logo("aureus-stacked-flat-white.png", 470)
                cache["t"] = [text_img(s, f, c, 0, 2)[0] for s, f, c in (("NOW BOOKING", font(ANTON, 92), AQUA), ("0434 137 393", font(MONT, 50, "SemiBold"), INK),
                              ("@aureusdetailing.com.au  ·  Perth", font(MONT, 32, "Medium"), (200, 210, 220)))]
            lg = cache["lg"]; fr.paste(lg, ((W - lg.width) // 2, int(860 - lg.height / 2 + 14 * (1 - a))), lg.getchannel("A").point(lambda v: int(v * a)))
            for im, y, d0 in zip(cache["t"], (1150, 1245, 1310), (0.35, 0.55, 0.7)): paste(fr, im, W / 2, y, ease((t - END - d0) / 0.3))
    pic = os.path.join(W1, "pic.mp4"); render(base, pic, T, draw)
    nm = Mix()
    for k in (0, 2, 3, 9, 14): sound(nm, segs[k]["clip"], segs[k]["at"], st[k], segs[k]["d"])
    nm.add(clip("A11"), st[16], VOX, trim=segs[16]["d"], ss=segs[16]["at"])      # his bell and his line, as recorded
    nmw = os.path.join(W1, "nomusic.wav"); nm.write(nmw, T)
    Q = f"between(t,{st[3]:.2f},{st[4]:.2f})+between(t,{st[9]:.2f},{st[10]:.2f})+between(t,{st[15]:.2f},{END:.2f})"   # stop-start drops (Ref 1)
    full = os.path.join(W1, "full.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(MUSIC, "m1.wav"), "-i", nmw, "-filter_complex",
         f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T},loudnorm=I=-15:TP=-2,"
         f"lowpass=f=420:enable='lt(t,{st[1]:.2f})+{Q}',volume='if(lt(t,{st[1]:.2f}),0.55,if({Q},0.3,1))':eval=frame,"
         f"afade=out:st={END+0.6:.2f}:d={T-END-0.6:.2f}[m];[m][1:a]amix=inputs=2:normalize=0,{MASTER}[a]", "-map", "[a]", "-t", str(T), full])
    finish(pic, [full, nmw], ["Aureus-Reel-A-Perth-Are-You-Ready.mp4", "Aureus-Reel-A-Perth-Are-You-Ready-NO-MUSIC.mp4"])

# =====================================================================  REEL B: talking (Refs 2 + 3 setup)
R2 = [  # shot, in-point, min length, spoken (on-camera text or voice-over file), emphasis word, zoom
    ("B01", None, 1.4, "cam:We come to you.", "you", 1.0),
    ("B02", 0.6, 1.9, "r2_02", "rush", 1.0),
    ("B03", 0.6, 2.0, "r2_03", "Swirls", 1.0),
    ("B04", None, 1.3, "cam:Not here.", "here", 1.12),
    ("B05", 0.6, 2.0, "r2_05", "foam", 1.0),
    ("B06", 0.6, 1.4, None, None, 1.0),
    ("B07", 0.6, 1.6, "r2_06", "polish", 1.0),
    ("B08", 0.6, 1.7, "r2_07", "hand", 1.0),
    ("B09", 0.6, 1.4, "r2_08", "spoke", 1.0),
    ("B10", 0.6, 1.3, "r2_09", "hand", 1.0),
    ("B11", 0.6, 2.0, "r2_10", "leather", 1.0),
    ("B12", 0.6, 1.5, None, None, 1.0),
    ("B13", None, 2.4, "cam:Done properly, or it's not done.", "properly", 1.12),
    ("B14", 0.8, 4.4, "r2_12", None, 1.0),
]
def reel2():
    W2 = os.path.join(WORK, "r2"); os.makedirs(W2, exist_ok=True)
    segs, lines = [], []
    for code, at, d, sp, emph, z in R2:
        if sp and sp.startswith("cam:"):
            a, ln, ws = find_line(code, sp[4:]); segs.append(dict(clip=code, at=a, d=max(d, ln), zoom=z)); lines.append(("cam", ws, emph))
        elif sp:
            p, ln = vo(sp); segs.append(dict(clip=code, at=at, d=max(d, ln + 0.45), zoom=z)); lines.append((p, None, emph))
        else: segs.append(dict(clip=code, at=at, d=d, zoom=z)); lines.append(None)
    print("reel B shots:", [(s["clip"], round(s["d"], 2)) for s in segs], flush=True)
    base, st, T = build_base(segs, W2, "eq=saturation=1.03")
    END = st[-1]; CAP = []
    for k, l in enumerate(lines):                           # word-by-word captions (Ref 2), not on the end card
        if not l or k == len(lines) - 1: continue
        src, ws, emph = l; t0 = st[k] + (0 if src == "cam" else 0.12)
        if src != "cam": ws = pace(VO_TEXT[os.path.basename(src)[2:-4]], 0.0, dur(src))
        CAP.append((t0, st[k] + segs[k]["d"], [(t0 + a, w, bool(emph) and re.sub(r"[^a-z]", "", w.lower()) == emph.lower()) for a, b, w in ws]))
    SLAM = st[4]
    wm = logo("aureus-horizontal-flat-white.png", 190, 0.55); cache = {}
    def wimg(w, em):
        if (w, em) not in cache: cache[(w, em)] = text_img(w, font(SERIF, 70) if em else font(MONT, 52, "Medium"), INK, 0.55, 12)
        return cache[(w, em)]
    def draw(fr, t):
        if t < END: fr.paste(wm, (60, 280), wm)
        for a0, a1, ws in CAP:
            if a0 <= t < a1:
                shown = [(w, em) for tw, w, em in ws if t >= tw - 0.04]
                if not shown: continue
                rows, row, rw = [], [], 0
                for w, em in shown:
                    im, p = wimg(w, em); ww = im.width - 2 * p
                    if row and rw + ww + 16 > 860: rows.append(row); row, rw = [], 0
                    row.append((im, ww)); rw += ww + 16
                rows.append(row); y = 1190 - (len(rows) - 1) * 40
                for row in rows:
                    x = W / 2 - (sum(r[1] for r in row) + 16 * (len(row) - 1)) / 2
                    for im, ww in row: paste(fr, im, x + ww / 2, y); x += ww + 16
                    y += 80
        if SLAM + 0.45 <= t < st[5]:                        # brand slam (Ref 3): small AT, big italic name
            q = ease((t - SLAM - 0.45) / 0.15)
            if "s1" not in cache:
                cache["s0"] = text_img("AT", font(MONT, 44, "SemiBold"), INK, 0.5, 10); cache["s1"] = text_img("AUREUS", font(MONTI, 178, "ExtraBold Italic"), INK, 0.5, 14)
                cache["s2"] = text_img("DETAILING", font(MONTI, 120, "ExtraBold Italic"), INK, 0.5, 14)
            paste(fr, cache["s0"][0], W / 2, 560, ease((t - SLAM - 0.3) / 0.12)); paste(fr, cache["s1"][0], W / 2, 690, q, 1.15 - 0.15 * q); paste(fr, cache["s2"][0], W / 2, 820, q, 1.15 - 0.15 * q)
        if t >= END + 0.2:                                  # the offer: one glass card, logo under it
            a = ease((t - END - 0.2) / 0.45); x, y = (W - 760) // 2, 930 + 16 * (1 - a); glass(fr, x, y, 760, 400, a, 38)
            if "e" not in cache:
                cache["e"] = [text_img(s, f, INK, 0, 2)[0] for s, f in (("Gold Detail", font(MONT, 42, "SemiBold")), ("$199", font(MONT, 120, "Bold")),
                              ("Mobile detailing · Perth", font(MONT, 34, "Medium")), ("Book online · link in bio", font(MONT, 36, "SemiBold")))]
                cache["lg"] = logo("aureus-horizontal-flat-white.png", 330)
            for im, yy in zip(cache["e"], (68, 170, 262, 344)): paste(fr, im, W / 2, y + yy, a)
            lg = cache["lg"]; fr.paste(lg, ((W - lg.width) // 2, int(1440 - lg.height / 2)), lg.getchannel("A").point(lambda v: int(v * a)))
    pic = os.path.join(W2, "pic.mp4"); render(base, pic, T, draw)
    nm = Mix(); wh = os.path.join(W2, "whoosh.wav"); whoosh(wh)
    for k, (code, at, d, sp, emph, z) in enumerate(R2):
        s = segs[k]
        if sp and sp.startswith("cam:"): nm.add(clip(code), st[k], VOX, trim=s["d"], ss=s["at"])     # his own words, as filmed
        else: sound(nm, code, s["at"], st[k], s["d"], -29 if lines[k] else -24)
        if lines[k] and lines[k][0] != "cam": nm.add(lines[k][0], st[k] + 0.12, VOX)
        if code in ("B02", "B05", "B09", "B14"): nm.add(wh, st[k] - 0.3, "volume=0.18")
    nmw = os.path.join(W2, "nomusic.wav"); nm.write(nmw, T)
    full = os.path.join(W2, "full.wav")                     # soft bed ~20 dB under the voice, ducks when he talks, lifts on the offer
    run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(MUSIC, "m2.wav"), "-i", nmw, "-filter_complex",
         f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T},loudnorm=I=-30:TP=-6,volume='if(lt(t,{END}),1,1.6)':eval=frame,afade=in:d=0.8,afade=out:st={T-1.6:.2f}:d=1.6[m];"
         f"[1:a]asplit[sc][x];[m][sc]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=450[md];[md][x]amix=inputs=2:normalize=0,{MASTER}[a]", "-map", "[a]", "-t", str(T), full])
    finish(pic, [full, nmw], ["Aureus-Reel-B-Done-Properly.mp4", "Aureus-Reel-B-Done-Properly-NO-MUSIC.mp4"])

# =====================================================================  REEL C: cinematic (Ref 4 setup)
def reel3():
    W3 = os.path.join(WORK, "r3")
    GRADE = "colorbalance=rs=-0.06:bs=0.07:rm=0.02:rh=0.07:gh=0.02:bh=-0.06,eq=contrast=1.12:saturation=0.9:gamma=0.97,vignette=PI/5,noise=alls=5:allf=t+u"
    bt = beats(os.path.join(MUSIC, "m3.wav"))["beats"]
    first = next(b for b in bt if b >= 1.9); i0 = bt.index(first)
    pool = [("C07", 0.2 + k) for k in range(10)] + [("C02", 1.0), ("C01", 2.0), ("C03", 1.0), ("C04", 1.0), ("C05", 1.0)]
    n = round(first * FPS); per, extra = divmod(n, len(pool))
    segs = [dict(clip=c, at=a, d=(per + (1 if k < extra else 0)) / FPS) for k, (c, a) in enumerate(pool)]
    t = first
    for k, (c, a) in enumerate([("C03", 0.5), ("C01", 1.0), ("C02", 1.5), ("C04", 0.8)]):     # beat cuts
        nb = bt[i0 + k + 1]; segs.append(dict(clip=c, at=a, d=nb - t)); t = nb
    j = i0 + 4
    for c, a in [("C01", 2.5), ("C02", 2.5), ("C06", 0.8), ("C05", 1.2), ("C03", 2.0), ("C04", 2.0)]:   # holds, two beats each
        nb = bt[min(j + 2, len(bt) - 1)]; segs.append(dict(clip=c, at=a, d=max(0.9, nb - t))); t += segs[-1]["d"]; j += 2
    segs.append(dict(clip="C08", at=1.0, d=2.0))
    for s in segs: s["d"] = max(1, round(s["d"] * FPS)) / FPS
    base, st, T = build_base(segs, W3, GRADE)
    cuts = st[1:len(pool) + 1]
    sym = logo("aureus-symbol-3d-chrome.png", 150); hd = text_img("AUREUS DETAILING  ·  PERTH", font(MONT, 30, "SemiBold"), INK, 0.5, 8)[0]
    def draw(fr, t):
        k = 0.0
        for c in cuts[::2]:                                 # sun blow-out flashes on every other micro cut (Ref 4 opener)
            dt = t - c
            if -0.001 <= dt < 3 / FPS: k = max(k, [0.85, 0.5, 0.2][int(dt * FPS)])
        fr = flash(fr, k)
        if t >= st[-1] + 0.3:
            a = ease((t - st[-1] - 0.3) / 0.5); fr.paste(sym, ((W - sym.width) // 2, int(1330 - sym.height / 2)), sym.getchannel("A").point(lambda v: int(v * a))); paste(fr, hd, W / 2, 1450, a)
        return fr
    pic = os.path.join(W3, "pic.mp4"); render(base, pic, T, draw)
    nm = Mix()
    for k, s in enumerate(segs):
        if s["d"] > 0.4: sound(nm, s["clip"], s["at"], st[k], s["d"], -27)
    nmw = os.path.join(W3, "nomusic.wav"); nm.write(nmw, T)
    full = os.path.join(W3, "full.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(MUSIC, "m3.wav"), "-i", nmw, "-filter_complex",
         f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T},loudnorm=I=-15:TP=-2,afade=out:st={T-1.2:.2f}:d=1.2[m];[m][1:a]amix=inputs=2:normalize=0,{MASTER}[a]",
         "-map", "[a]", "-t", str(T), full])
    finish(pic, [full, nmw], ["Aureus-Reel-C-The-Shine.mp4", "Aureus-Reel-C-The-Shine-NO-MUSIC.mp4"])

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for a in (sys.argv[1:] or ["1", "2", "3"]): {"1": reel1, "2": reel2, "3": reel3}[a]()
