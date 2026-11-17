"""Reel B v2, "Done properly": black G-Wagon, hot pink foam, City Beach home, old-Aussie Voice 3 (Refs 2 + 3 setup).

    ~/local-ai/.venv/bin/python make_reel_b2.py      (shots: Shots/Set 2 - G-Wagon)
Shots and prompts: HIGGSFIELD-SHOTS-B2.md. Editing is free and local."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_reels as mr
import make_reels_hf as hf
from reelkit import *

WORK = os.path.join(SCRATCH, "set2"); os.makedirs(WORK, exist_ok=True); mr.WORK = WORK; hf.WORK = WORK
import reelkit; reelkit.SHOOT = os.path.join(SHOTS, "Set 2 - G-Wagon")
mr.VOICE = os.path.join(AUD, "voice-v2")
PINK = (255, 77, 141)
mr.VO_TEXT.update({"b2_02": "Pink foam first.", "b2_03": "Lifts the grit before I touch the paint.", "b2_04": "Most places rush it.", "b2_05": "Not at Aureus.",
                   "b2_06": "Machine polish. Wax, by hand.", "b2_07": "Every spoke.", "b2_09": "Gold Detail. From one ninety-nine. We come to you.",
                   "b2_10": "Then rinse it clean.", "b2_11": "Inside, steam for the leather.", "b2_12": "Gold Detail for your four-wheel drive. Two nineteen. We come to you."})
hf.SHOT_SFX.update({"G02": "foam", "G03": "foam", "G04": "drips", "G05": "amb", "G06": "polish", "G07": "brush", "G08": "drips", "G10": "drips", "S01": "amb", "S09": "amb", "G11": "rinse", "G12": "wipe"})
R = [  # shot, in-point, min length, spoken, emphasis word, zoom
    ("S01", 0.0, 2.3, "cam:We come to you, mate.", "mate", 1.0),
    ("G02", 0.2, 1.8, "b2_02", "Pink", 1.0),
    ("G03", 0.2, 2.6, "b2_03", "grit", 1.0),
    ("G11", 0.2, 2.1, "b2_10", "rinse", 1.0),
    ("G04", 0.3, 2.0, "b2_04", "rush", 1.12),
    ("G05", 0.3, 2.3, "b2_05", "Aureus", 1.0),
    ("G06", 0.2, 2.6, "b2_06", "hand", 1.0),
    ("G07", 0.3, 1.6, "b2_07", "spoke", 1.12),
    ("G12", 0.2, 2.5, "b2_11", "leather", 1.0),
    ("G08", 0.3, 1.2, None, None, 1.0),
    ("S09", 0.0, 3.0, "cam:Done properly, or it's not done.", "properly", 1.12),
    ("G10", 0.3, 2.8, "b2_12", None, 1.0),
]
CAM_SPAN = {"S01": (0.3, 1.95), "S09": (0.3, 2.65)}          # where his words sit in the lip-synced clips (300 ms lead-in)

def main():
    segs, lines = [], []
    for code, at, d, sp, emph, z in R:
        if sp and sp.startswith("cam:"):
            segs.append(dict(clip=code, at=at, d=d, zoom=z)); lines.append(("cam", mr.pace(sp[4:], *CAM_SPAN[code]), emph))
        elif sp:
            p, ln = mr.vo(sp); segs.append(dict(clip=code, at=at, d=max(d, ln + 0.35), zoom=z)); lines.append((p, None, emph))
        else: segs.append(dict(clip=code, at=at, d=d, zoom=z)); lines.append(None)
    base, st, T = build_base(segs, WORK, "eq=saturation=1.04:contrast=1.04")
    T = max(T, st[-1] + 4.2)                                  # end card holds on the hero's last frame
    if T > st[-1] + segs[-1]["d"]:
        ext = os.path.join(WORK, "base_ext.mp4")
        run(["ffmpeg", "-y", "-v", "error", "-i", base, "-vf", f"tpad=stop_mode=clone:stop_duration={T - (st[-1] + segs[-1]['d']):.2f}", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", ext]); base = ext
    END = st[-1]; CAP = []
    for k, l in enumerate(lines):
        if not l or k == len(lines) - 1: continue
        src, ws, emph = l; t0 = st[k] + (0 if src == "cam" else 0.12)
        if src != "cam": ws = mr.pace(mr.VO_TEXT[os.path.basename(src)[2:-4]], 0.0, dur(src))
        CAP.append((t0, st[k] + segs[k]["d"], [(t0 + a, w, bool(emph) and re.sub(r"[^a-z]", "", w.lower()) == emph.lower()) for a, b, w in ws]))
    SLAM = st[5]
    wm = logo("aureus-horizontal-flat-white.png", 190, 0.55); cache = {}
    def wimg(w, em):
        if (w, em) not in cache: cache[(w, em)] = text_img(w, font(SERIF, 74) if em else font(MONT, 52, "Medium"), INK, 0.8, 12)
        return cache[(w, em)]
    def draw(fr, t):
        if t < END: fr.paste(wm, (60, 280), wm)
        for a0, a1, ws in CAP:                                # word-by-word captions; the key word in italic serif (white, as in Ref 2; pink vanished over the foam)
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
        if SLAM + 0.35 <= t < st[6]:                          # brand slam (Ref 3)
            q = ease((t - SLAM - 0.35) / 0.15)
            if "s1" not in cache:
                cache["s1"] = text_img("AUREUS", font(MONTI, 190, "ExtraBold Italic"), INK, 0.55, 16)
                cache["s2"] = text_img("DETAILING", font(MONTI, 126, "ExtraBold Italic"), INK, 0.55, 16)
            paste(fr, cache["s1"][0], W / 2, 640, q, 1.15 - 0.15 * q); paste(fr, cache["s2"][0], W / 2, 780, q, 1.15 - 0.15 * q)
        if t >= END + 0.2:                                    # the offer card (prices match the booking page)
            a = ease((t - END - 0.2) / 0.45); x, y = (W - 820) // 2, 820 + 16 * (1 - a); glass(fr, x, y, 820, 560, a, 38)
            if "e" not in cache:                              # Gold for SUV / 4WD, straight from the booking page (app.js): $199 + $20
                cache["e"] = [text_img(s, f, c, 0, 2)[0] for s, f, c in (
                    ("Gold Detail  ·  SUV / 4WD", font(MONT, 40, "SemiBold"), INK), ("$219", font(MONT, 120, "Bold"), INK),
                    ("Snow foam wash  ·  polish  ·  wax sealant", font(MONT, 30, "Medium"), INK), ("Interior steam clean  ·  leather care", font(MONT, 30, "Medium"), INK),
                    ("2 h 30  ·  we come to you  ·  Perth", font(MONT, 30, "Medium"), (200, 210, 220)), ("Book online · link in bio", font(MONT, 36, "SemiBold"), PINK))]
                cache["lg"] = logo("aureus-horizontal-flat-white.png", 330)
            for im, yy in zip(cache["e"], (62, 168, 270, 318, 370, 470)): paste(fr, im, W / 2, y + yy, a)
            lg = cache["lg"]; fr.paste(lg, ((W - lg.width) // 2, int(1440 - lg.height / 2)), lg.getchannel("A").point(lambda v: int(v * a)))
    pic = os.path.join(WORK, "pic.mp4"); render(base, pic, T, draw)
    nm = Mix(); wh = os.path.join(WORK, "whoosh.wav"); whoosh(wh)
    for k, (code, at, d, sp, emph, z) in enumerate(R):
        s = segs[k]
        if sp and sp.startswith("cam:"): nm.add(clip(code), st[k], VOX, trim=s["d"], ss=s["at"])
        else: hf.sfx(nm, code, st[k], s["d"], -30 if lines[k] else -25)
        if lines[k] and lines[k][0] != "cam": nm.add(lines[k][0], st[k] + 0.12, VOX)
        if k in (1, 5, 7, 11): nm.add(wh, st[k] - 0.3, "volume=0.18")
    hf.bell_ding(nm, st[10] - 0.35)
    nm.add(hf.SFX("amb"), 0, f"loudnorm=I=-38:TP=-8,afade=in:d=0.6,afade=out:st={T-1}:d=1", trim=min(T, 7.5))
    nmw = os.path.join(WORK, "nomusic.wav"); nm.write(nmw, T)
    full = os.path.join(WORK, "full.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(AUD, "music", "m2.wav"), "-i", nmw, "-filter_complex",
         f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T},loudnorm=I=-30:TP=-6,volume='if(lt(t,{END}),1,1.6)':eval=frame,afade=in:d=0.8,afade=out:st={T-1.6:.2f}:d=1.6[m];"
         f"[1:a]asplit[sc][x];[m][sc]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=450[md];[md][x]amix=inputs=2:normalize=0,{MASTER}[a]", "-map", "[a]", "-t", str(T), full])
    finish(pic, [full, nmw], ["Aureus-Reel-B-Done-Properly-v2.mp4", "Aureus-Reel-B-Done-Properly-v2-NO-MUSIC.mp4"])

if __name__ == "__main__":
    main()
