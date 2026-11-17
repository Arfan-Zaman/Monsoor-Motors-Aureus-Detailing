"""The three brand launch reels cut from the 12 Higgsfield shots (HIGGSFIELD-SHOTS.md). Editing is free and local.

    ~/local-ai/.venv/bin/python make_reels_hf.py [1] [2] [3]      (shots: Shots/Set 1 - Pearl White Sedan)

Each reel follows its reference's setup: Ref 1 (B&W teaser), Refs 2+3 (talking + word captions + brand slam), Ref 4 (flash-cut cinematic).
Sound: designed voice (audio/voice), local music (audio/music), local detailing sounds (audio/sfx)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_reels as mr
from reelkit import *

WORK = os.path.join(SCRATCH, "set1"); os.makedirs(WORK, exist_ok=True); mr.WORK = WORK
SFX = lambda n: os.path.join(AUD, "sfx", f"{n}.wav")
SHOT_SFX = {"K01": "rinse", "K02": "foam", "K03": "polish", "K04": "drips", "K05": "brush", "K06": "trolley", "K12": "drips", "K08": "amb", "K09": "amb", "K07": "amb", "K10": "amb", "K11": "amb"}

def sfx(mix, code, at, d, level=-27):
    n = SHOT_SFX.get(code)
    if n and d > 0.3: mix.add(SFX(n), at, f"loudnorm=I={level}:TP=-4,afade=in:d=0.05,afade=out:st={max(0, d - 0.12):.2f}:d=0.12", trim=d, ss=0.5)

def bell_ding(mix, at):
    p = os.path.join(WORK, "ding.wav"); ding(p); mix.add(p, at, "volume=0.5")

# =====================================================================  REEL A: "Perth. Are you ready?" (Ref 1 setup)
def reel1():
    W1 = os.path.join(WORK, "r1")
    BW = "hue=s=0,eq=contrast=1.5:brightness=-0.05:gamma=0.92,noise=alls=9:allf=t+u"
    mic = lambda *cs: [dict(clip=c, at=a, d=0.17) for c, a in cs]
    segs = ([dict(clip="K10", at=0.6, d=1.6), dict(clip="K11", at=0.8, d=1.0), dict(clip="K03", at=0.6, d=1.6), dict(clip="K04", at=0.8, d=1.5)]
            + mic(("K01", 1.0), ("K02", 0.2), ("K05", 1.0), ("K03", 2.2))
            + [dict(clip="K12", at=0.6, d=1.9), dict(clip="K02", at=0.05, d=1.1)]
            + mic(("K05", 2.2), ("K01", 2.3), ("K04", 2.2), ("K06", 0.4))
            + [dict(clip="K01", at=0.6, d=1.8), dict(clip="K06", at=1.0, d=1.8), dict(clip="K07", at=0.1, d=2.9), dict(black=True, d=3.4)])
    base, st, T = build_base(segs, W1, BW); END = st[-1]
    SL = [(st[1], st[2], [("PERTH", 250)], [st[1]]),
          (st[2], st[3], [("PERTH", 250), ("ARE YOU", 210), ("READY?", 300)], [st[2], st[2], st[2] + 0.5]),
          (st[8], st[9], [("MOBILE", 230), ("DETAILING", 210)], [st[8], st[8] + 0.45]),
          (st[14], st[15], [("WE COME", 230), ("TO YOU.", 260)], [st[14], st[14] + 0.5])]
    cache = {}
    def draw(fr, t):
        for k, (a0, a1, ls, rv) in enumerate(SL):
            if a0 <= t < a1:
                if k not in cache: cache[k] = [text_img(s, font(ANTON, sz), AQUA if i == 0 else INK, 0.4, 14) for i, (s, sz) in enumerate(ls)]
                ims = cache[k]; hs = [im.height - 2 * p for im, p in ims]; gap = -18; y = 930 - (sum(hs) + gap * (len(hs) - 1)) / 2
                for (im, p), h, r0 in zip(ims, hs, rv):
                    if t >= r0: q = ease((t - r0) / 0.12); paste(fr, im, W / 2, y + h / 2, q, 1.18 - 0.18 * q)
                    y += h + gap
        if t >= END:
            a = ease((t - END) / 0.35)
            if "lg" not in cache:
                cache["lg"] = logo("aureus-stacked-flat-white.png", 470)
                cache["t"] = [text_img(s, f, c, 0, 2)[0] for s, f, c in (("NOW BOOKING", font(ANTON, 92), AQUA), ("0434 137 393", font(MONT, 50, "SemiBold"), INK),
                              ("@aureusdetailing.com.au  ·  Perth", font(MONT, 32, "Medium"), (200, 210, 220)))]
            lg = cache["lg"]; fr.paste(lg, ((W - lg.width) // 2, int(860 - lg.height / 2 + 14 * (1 - a))), lg.getchannel("A").point(lambda v: int(v * a)))
            for im, y, d0 in zip(cache["t"], (1150, 1245, 1310), (0.35, 0.55, 0.7)): paste(fr, im, W / 2, y, ease((t - END - d0) / 0.3))
    pic = os.path.join(W1, "pic.mp4"); render(base, pic, T, draw)
    nm = Mix()
    for k in (0, 2, 3, 8, 9, 14, 15): sfx(nm, segs[k]["clip"], st[k], segs[k]["d"])
    bell_ding(nm, st[16] + 0.55)
    v, vd = mr.vo("r1_ready"); nm.add(v, st[16] + 1.2, VOX)
    nmw = os.path.join(W1, "nomusic.wav"); nm.write(nmw, T)
    Q = f"between(t,{st[3]:.2f},{st[4]:.2f})+between(t,{st[9]:.2f},{st[10]:.2f})+between(t,{st[15]:.2f},{END:.2f})"   # stop-start drops (Ref 1)
    full = os.path.join(W1, "full.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(AUD, "music", "m1.wav"), "-i", nmw, "-filter_complex",
         f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T},loudnorm=I=-15:TP=-2,"
         f"lowpass=f=420:enable='lt(t,{st[1]:.2f})+{Q}',volume='if(lt(t,{st[1]:.2f}),0.55,if({Q},0.3,1))':eval=frame,"
         f"afade=out:st={END+0.6:.2f}:d={T-END-0.6:.2f}[m];[m][1:a]amix=inputs=2:normalize=0,{MASTER}[a]", "-map", "[a]", "-t", str(T), full])
    finish(pic, [full, nmw], ["Aureus-Reel-A-Perth-Are-You-Ready.mp4", "Aureus-Reel-A-Perth-Are-You-Ready-NO-MUSIC.mp4"])

# =====================================================================  REEL B: "Done properly" (Refs 2 + 3 setup)
R2 = [  # shot, in-point, min length, spoken (voice-over file, or cam: line said on camera), emphasis word, zoom
    ("K08", 0.2, 1.6, "r2_01", "you", 1.0),
    ("K01", 0.4, 1.8, "r2_02", "rush", 1.0),
    ("K04", 0.2, 2.6, "r2_03", "Swirls", 1.0),
    ("K06", 0.3, 2.4, "r2_05", "foam", 1.0),
    ("K02", 0.05, 1.1, None, None, 1.0),
    ("K03", 0.2, 1.5, "r2_06", "polish", 1.0),
    ("K03", 1.7, 1.3, "r2_07", "hand", 1.12),
    ("K05", 0.3, 1.2, "r2_08", "spoke", 1.0),
    ("K05", 1.6, 1.3, "r2_09", "hand", 1.12),
    ("K07", 0.1, 1.9, None, None, 1.0),
    ("S09", 0.0, 3.0, "cam:Done properly, or it's not done.", "properly", 1.12),
    ("K12", 0.3, 2.7, "r2_12", None, 1.0),
]
mr.VO_TEXT.update({"r2_01": "We come to you."})
def reel2():
    W2 = os.path.join(WORK, "r2"); os.makedirs(W2, exist_ok=True)
    segs, lines = [], []
    for code, at, d, sp, emph, z in R2:
        if sp and sp.startswith("cam:"):
            segs.append(dict(clip=code, at=at, d=d, zoom=z)); lines.append(("cam", mr.pace(sp[4:], 0.3, 2.7), emph))
        elif sp:
            p, ln = mr.vo(sp); segs.append(dict(clip=code, at=at, d=max(d, ln + 0.35), zoom=z)); lines.append((p, None, emph))
        else: segs.append(dict(clip=code, at=at, d=d, zoom=z)); lines.append(None)
    base, st, T = build_base(segs, W2, "eq=saturation=1.03")
    T = max(T, st[-1] + 3.6)                                   # end card holds after the last shot (freeze on its final frame)
    if T > st[-1] + segs[-1]["d"]:
        ext = os.path.join(W2, "base_ext.mp4")
        run(["ffmpeg", "-y", "-v", "error", "-i", base, "-vf", f"tpad=stop_mode=clone:stop_duration={T - (st[-1] + segs[-1]['d']):.2f}", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", ext]); base = ext
    END = st[-1]; CAP = []
    for k, l in enumerate(lines):
        if not l or k == len(lines) - 1: continue
        src, ws, emph = l; t0 = st[k] + (0 if src == "cam" else 0.12)
        if src != "cam": ws = mr.pace(mr.VO_TEXT[os.path.basename(src)[2:-4]], 0.0, dur(src))
        CAP.append((t0, st[k] + segs[k]["d"], [(t0 + a, w, bool(emph) and re.sub(r"[^a-z]", "", w.lower()) == emph.lower()) for a, b, w in ws]))
    SLAM = st[3]
    wm = logo("aureus-horizontal-flat-white.png", 190, 0.55); cache = {}
    def wimg(w, em):
        if (w, em) not in cache: cache[(w, em)] = text_img(w, font(SERIF, 70) if em else font(MONT, 52, "Medium"), INK, 0.55, 12)
        return cache[(w, em)]
    def draw(fr, t):
        if t < END: fr.paste(wm, (60, 280), wm)
        for a0, a1, ws in CAP:                              # word-by-word captions, one italic emphasis word (Ref 2)
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
        if SLAM + 0.45 <= t < st[4]:                        # brand slam (Ref 3): small AT, big italic name
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
        if sp and sp.startswith("cam:"): nm.add(clip(code), st[k], VOX, trim=s["d"], ss=s["at"])     # his lip-synced line
        else: sfx(nm, code, st[k], s["d"], -30 if lines[k] else -25)
        if lines[k] and lines[k][0] != "cam": nm.add(lines[k][0], st[k] + 0.12, VOX)
        if k in (1, 3, 7, 11): nm.add(wh, st[k] - 0.3, "volume=0.18")
    bell_ding(nm, st[9] + 0.5)
    nm.add(SFX("amb"), 0, f"loudnorm=I=-38:TP=-8,afade=in:d=0.6,afade=out:st={T-1}:d=1", trim=min(T, 7.5))
    nmw = os.path.join(W2, "nomusic.wav"); nm.write(nmw, T)
    full = os.path.join(W2, "full.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(AUD, "music", "m2.wav"), "-i", nmw, "-filter_complex",
         f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T},loudnorm=I=-30:TP=-6,volume='if(lt(t,{END}),1,1.6)':eval=frame,afade=in:d=0.8,afade=out:st={T-1.6:.2f}:d=1.6[m];"
         f"[1:a]asplit[sc][x];[m][sc]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=450[md];[md][x]amix=inputs=2:normalize=0,{MASTER}[a]", "-map", "[a]", "-t", str(T), full])
    finish(pic, [full, nmw], ["Aureus-Reel-B-Done-Properly.mp4", "Aureus-Reel-B-Done-Properly-NO-MUSIC.mp4"])

# =====================================================================  REEL C: "The shine" (Ref 4 setup)
def reel3():
    W3 = os.path.join(WORK, "r3")
    GRADE = "colorbalance=rs=-0.06:bs=0.07:rm=0.02:rh=0.07:gh=0.02:bh=-0.06,eq=contrast=1.12:saturation=0.9:gamma=0.97,vignette=PI/5,noise=alls=5:allf=t+u"
    bt = beats(os.path.join(AUD, "music", "m3.wav"))["beats"]
    first = next(b for b in bt if b >= 1.9); i0 = bt.index(first)
    pool = [("K01", 0.3), ("K02", 0.1), ("K05", 0.4), ("K03", 0.5), ("K04", 0.6), ("K01", 1.4), ("K12", 0.5), ("K05", 1.5),
            ("K02", 0.6), ("K03", 1.6), ("K04", 1.8), ("K01", 2.4), ("K05", 2.5), ("K12", 1.6), ("K06", 1.2)]
    n = round(first * FPS); per, extra = divmod(n, len(pool))
    segs = [dict(clip=c, at=a, d=(per + (1 if k < extra else 0)) / FPS) for k, (c, a) in enumerate(pool)]
    t = first
    for k, (c, a) in enumerate([("K05", 0.2), ("K02", 0.05), ("K01", 0.8), ("K03", 0.4)]):     # beat cuts
        nb = bt[i0 + k + 1]; segs.append(dict(clip=c, at=a, d=nb - t)); t = nb
    j = i0 + 4
    for c, a in [("K01", 1.3), ("K04", 0.4), ("K05", 1.2), ("K03", 1.2), ("K11", 0.6), ("K12", 0.2)]:   # holds, two beats each
        nb = bt[min(j + 2, len(bt) - 1)]; segs.append(dict(clip=c, at=a, d=max(0.9, nb - t))); t += segs[-1]["d"]; j += 2
    segs.append(dict(clip="K12", at=1.4, d=1.6))
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
        if t >= st[-1] + 0.2:
            a = ease((t - st[-1] - 0.2) / 0.5); fr.paste(sym, ((W - sym.width) // 2, int(1330 - sym.height / 2)), sym.getchannel("A").point(lambda v: int(v * a))); paste(fr, hd, W / 2, 1450, a)
        return fr
    pic = os.path.join(W3, "pic.mp4"); render(base, pic, T, draw)
    nm = Mix()
    for k, s in enumerate(segs):
        if s["d"] > 0.4: sfx(nm, s["clip"], st[k], s["d"], -28)
    nm.add(SFX("roof"), 0, f"loudnorm=I=-36:TP=-8,afade=out:st={T-1}:d=1", trim=min(T, 7.5))
    nmw = os.path.join(W3, "nomusic.wav"); nm.write(nmw, T)
    full = os.path.join(W3, "full.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(AUD, "music", "m3.wav"), "-i", nmw, "-filter_complex",
         f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T},loudnorm=I=-15:TP=-2,afade=out:st={T-1.2:.2f}:d=1.2[m];[m][1:a]amix=inputs=2:normalize=0,{MASTER}[a]",
         "-map", "[a]", "-t", str(T), full])
    finish(pic, [full, nmw], ["Aureus-Reel-C-The-Shine.mp4", "Aureus-Reel-C-The-Shine-NO-MUSIC.mp4"])

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for a in (sys.argv[1:] or ["1", "2", "3"]): {"1": reel1, "2": reel2, "3": reel3}[a]()
