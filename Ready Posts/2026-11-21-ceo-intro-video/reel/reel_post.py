"""Finish the reel animatic: temp voice track, burned captions, text supers, end card, storyboard.

Run:  python reel_post.py <frames_dir> <voice_dir> <out_dir>
Needs Pillow and ffmpeg. Timings match reel_scene.py (24 fps, 696 frames = 29.0 s).
The temp voice track is cut only from existing approved audio (no new generation):
  Monsoor-script-voice-1.wav  and  Arfan-script-voice-LOCKED.wav.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

FRAMES, VOICE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
FONT = os.path.expanduser("~/Library/Fonts/Montserrat-Variable.ttf")
FPS, END = 24, 696
NAVY, ORANGE, WHITE = (15, 39, 71), (255, 95, 21), (247, 245, 242)

SHOTS = [  # first, last, label, camera note
    (1, 60, "S1 HOOK", "Servo, 40 mm, slow push"),
    (61, 134, "S2 TRUST", "Auction yard, 24 mm crane down"),
    (135, 194, "S3 HANDOVER", "Two-shot, 35 mm"),
    (195, 302, "S4 ARFAN", "50 mm, trucks to his side"),
    (303, 354, "S5a JAPAN", "35 mm tracking along the rows"),
    (355, 405, "S5b CHECKED", "40 mm, torch inspection"),
    (406, 456, "S5c HYBRID", "32 mm orbit of the C-HR"),
    (457, 506, "S5d DELIVERED", "35 mm low, car rolls up the drive"),
    (507, 558, "S6 KEYS", "35 mm, key handover"),
    (559, 624, "S7 PAYOFF", "28 mm, drives past the servo"),
    (625, 696, "S8 TEASE", "30 mm pull-back + end card"),
]
# (start s, end s, speaker, caption)  burned captions = what is said
CAPTIONS = [
    (2.55, 5.55, "MONSOOR", "I built Monsoor Motors on one thing: trust."),
    (5.70, 8.10, "MONSOOR", "Arfan, our new CEO."),
    (8.20, 10.80, "ARFAN", "That means a lot."),
    (10.90, 12.55, "ARFAN", "Hello mates, this is Arfan."),
    (12.65, 16.10, "ARFAN", "Every car on this yard, from family runabouts to Japanese imported hybrids,"),
    (16.10, 21.10, "ARFAN", "is hand-picked, properly checked and honestly priced."),
    (21.15, 23.30, "ARFAN", "You choose the car! We bring it to your home!"),
]
# (start s, end s, text, style)  on-screen supers
SUPERS = [
    (0.20, 2.50, "Perth fill-ups be like...", "hook"),
    (5.70, 8.10, "ARFAN ZAMAN  |  CEO, MONSOOR MOTORS", "lower"),
    (12.65, 14.75, "Hand-picked in Japan", "tag"),
    (14.80, 16.85, "Checked before it's priced", "tag"),
    (16.90, 19.00, "Hybrid: uses less fuel", "tag"),
    (19.05, 21.05, "Delivered to your door", "tag"),
    (23.40, 25.95, "See ya, bowser.", "hook"),
]
# temp voice cuts: (file, src start, src end, place at s)
CUTS = [
    ("Monsoor-script-voice-1.wav", 0.00, 3.25, 2.55),
    ("Monsoor-script-voice-1.wav", 6.00, 8.60, 5.70),
    ("Arfan-script-voice-LOCKED.wav", 0.00, 2.62, 8.20),
    ("Arfan-script-voice-LOCKED.wav", 4.50, 6.20, 10.90),
    ("Arfan-script-voice-LOCKED.wav", 9.90, 18.55, 12.65),
    ("Arfan-script-voice-LOCKED.wav", 21.30, 23.43, 21.15),
]


def font(size, weight="Bold"):
    try:
        f = ImageFont.truetype(FONT, size)
        try:
            f.set_variation_by_name(weight)
        except Exception:
            pass
        return f
    except Exception:
        return ImageFont.load_default()


def wrap(d, text, fnt, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def centred(d, y, text, fnt, fill, w):
    d.text(((w - d.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)


def annotate(img, f):
    img = img.convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    t = (f - 1) / FPS
    shot = next(s for s in SHOTS if s[0] <= f <= s[1])
    # previs strip (top, outside the platform UI zone would be ideal; kept small)
    d.rectangle([0, 0, w, 28], fill=NAVY + (210,))
    d.text((10, 6), f"PREVIS  {shot[2]}  |  {shot[3]}", font=font(11, "SemiBold"), fill=WHITE)
    tc = "%05.2f s" % t
    d.text((w - 10 - d.textlength(tc, font=font(11)), 6), tc, font=font(11), fill=WHITE)
    for a, b, txt, style in SUPERS:
        if a <= t < b:
            if style == "hook":
                fnt = font(30)
                lines = wrap(d, txt, fnt, w - 60)
                y = 150
                for ln in lines:
                    tw = d.textlength(ln, font=fnt)
                    d.rounded_rectangle([(w - tw) / 2 - 12, y - 6, (w + tw) / 2 + 12, y + 40], 8, fill=(255, 255, 255, 235))
                    centred(d, y, ln, fnt, (15, 15, 18), w)
                    y += 50
            elif style == "lower":
                fnt = font(14)
                tw = d.textlength(txt, font=fnt)
                d.rectangle([24, 520, 24 + tw + 24, 552], fill=NAVY + (230,))
                d.rectangle([24, 552, 24 + tw + 24, 556], fill=ORANGE + (255,))
                d.text((36, 528), txt, font=fnt, fill=WHITE)
            else:
                fnt = font(22)
                tw = d.textlength(txt, font=fnt)
                d.rounded_rectangle([(w - tw) / 2 - 14, 170, (w + tw) / 2 + 14, 212], 10, fill=(10, 14, 22, 170))
                centred(d, 177, txt, fnt, WHITE, w)
    for a, b, who, txt in CAPTIONS:
        if a <= t < b:
            fnt = font(17, "SemiBold")
            lines = wrap(d, txt, fnt, w - 70)
            y = h - 250 - 26 * len(lines)
            for ln in lines:
                tw = d.textlength(ln, font=fnt)
                d.rounded_rectangle([(w - tw) / 2 - 8, y - 3, (w + tw) / 2 + 8, y + 24], 6, fill=(0, 0, 0, 165))
                centred(d, y, ln, fnt, WHITE, w)
                y += 27
    if f >= 640:  # end card
        k = min(1.0, (f - 640) / 10)
        a = int(235 * k)
        d.rounded_rectangle([30, 250, w - 30, 640], 18, fill=NAVY + (a,))
        if k >= 1:
            d.rectangle([30, 352, w - 30, 357], fill=ORANGE)
            centred(d, 278, "Something big is coming", font(28), WHITE, w)
            centred(d, 314, "for Perth drivers.", font(28), WHITE, w)
            centred(d, 378, "MONSOOR MOTORS", font(32), WHITE, w)
            centred(d, 424, "Japanese hybrids, imported for you", font(15, "SemiBold"), WHITE, w)
            centred(d, 470, "Follow to be first.", font(22), ORANGE, w)
            centred(d, 520, "0434 137 393", font(24), WHITE, w)
            centred(d, 560, "530 Albany Hwy, Victoria Park  |  MD32748", font(12, "Medium"), WHITE, w)
            centred(d, 600, "AI-generated scenes", font(10, "Medium"), (190, 200, 214), w)
    return img


def fp(n):
    return os.path.join(FRAMES, "f_%04d.png" % n)


os.makedirs(OUT, exist_ok=True)
tmp = os.path.join(FRAMES, "_ann")
os.makedirs(tmp, exist_ok=True)
for n in range(1, END + 1):
    annotate(Image.open(fp(n)), n).save(os.path.join(tmp, "a_%04d.png" % n))

# temp voice track (existing approved audio only)
inputs, filt = [], []
for i, (fn, a, b, at) in enumerate(CUTS):
    inputs += ["-i", os.path.join(VOICE, fn)]
    ms = int(at * 1000)
    filt.append(f"[{i}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.02,afade=t=out:st={b - a - 0.04:.2f}:d=0.04,adelay={ms}|{ms}[v{i}]")
mix = "".join(f"[v{i}]" for i in range(len(CUTS)))
filt.append(f"{mix}amix=inputs={len(CUTS)}:normalize=0,apad=whole_dur=29,atrim=0:29[aout]")
wav = os.path.join(OUT, "Reel-temp-voice.wav")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(filt), "-map", "[aout]", "-ac", "1", wav], check=True)

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "a_%04d.png"), "-i", wav,
                "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                "-c:a", "aac", "-b:a", "192k", "-shortest", os.path.join(OUT, "Reel-29s-Previs.mp4")], check=True)

# storyboard: one frame per shot
picks = [(40, "S1 Hook: the bowser bites"), (110, "S2 Trust: the founder"), (178, "S3 Handover (and the slap)"),
         (265, "S4 Hello mates"), (330, "S5a Picked in Japan"), (380, "S5b Checked by Arfan"),
         (440, "S5c Hybrid: less fuel"), (495, "S5d Rolls up the drive"), (540, "S6 Keys to the family"),
         (600, "S7 See ya, bowser"), (680, "S8 Tease + follow")]
tw_, th_, pad, cap = 300, 534, 18, 44
cols = 6
rows = (len(picks) + cols - 1) // cols
board = Image.new("RGB", (pad + cols * (tw_ + pad), 70 + rows * (th_ + cap + pad)), WHITE)
bd = ImageDraw.Draw(board)
bd.text((pad, 20), "Monsoor Motors  |  29 s teaser reel  |  previs storyboard", font=font(26), fill=NAVY)
for i, (n, label) in enumerate(picks):
    x = pad + (i % cols) * (tw_ + pad)
    y = 70 + (i // cols) * (th_ + cap + pad)
    board.paste(annotate(Image.open(fp(n)), n).resize((tw_, th_), Image.LANCZOS), (x, y))
    bd.text((x, y + th_ + 10), label, font=font(17, "SemiBold"), fill=NAVY)
board.save(os.path.join(OUT, "Reel-Storyboard.png"))
print("done")
