"""Finish the 'Queue Jump' animatic: shot labels, captions, supers, brand card, temp voice, storyboard.

Run:  python qj_post.py <frames_dir> <voice_dir> <out_dir>
Timings match qj_scene.py (24 fps, 696 frames: 28 s story + 1 s brand).
Temp voice uses only approved audio: Arfan's locked track. Lines not recorded yet are shown as [TO RECORD].
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

FRAMES, VOICE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
FONT = os.path.expanduser("~/Library/Fonts/Montserrat-Variable.ttf")
FPS, END = 24, 696
NAVY, ORANGE, WHITE = (15, 39, 71), (255, 95, 21), (247, 245, 242)

SHOTS = [
    (1, 72, "S1 HOOK", "50 mm low push-in, price board"),
    (73, 120, "S2a QUEUE", "24 mm crane down over the queue"),
    (121, 156, "S2b DAVE", "50 mm slow dolly, pained at the pump"),
    (157, 192, "S2c MIA", "85 mm through the window, asleep"),
    (193, 264, "S3 ARRIVAL", "24 mm low car rig, silent glide"),
    (265, 360, "S4 HELLO MATES", "50 mm gimbal arc on Arfan"),
    (361, 432, "S5 CAN WE GET ONE", "28 mm over Dave's shoulder"),
    (433, 492, "S6a KEYS", "35 mm wide, yard, slow push"),
    (493, 564, "S6b GOOD JOB", "85 mm two-shot, hand on shoulder"),
    (565, 672, "S7 HOME", "35 mm low, then crane-up pull-back"),
    (673, 696, "S8 BRAND", "1 s brand card"),
]
CAPTIONS = [
    (11.70, 12.90, "Hello mates."),
    (15.80, 17.60, "Kid: \"Dad... can we get one?\"  [TO RECORD]"),
    (20.40, 21.00, "Monsoor: \"Good job.\"  [TO RECORD]"),
    (21.05, 23.45, "That means a lot for me."),
    (24.00, 26.20, "You choose the car! We bring it to your home!"),
]
SUPERS = [
    (0.15, 2.90, "Perth. Thursday night.", "hook"),
    (12.95, 14.90, "Half the fuel of his ASX.*", "tag"),
    (26.25, 27.95, "Delivered to your door", "tag"),
]
CUTS = [  # (file, src start, src end, place at)
    ("Arfan-script-voice-LOCKED.wav", 4.50, 5.40, 11.70),     # "Hello mates"
    ("Arfan-script-voice-LOCKED.wav", 0.00, 2.62, 21.05),     # "That means a lot" ("for me" to record)
    ("Arfan-script-voice-LOCKED.wav", 21.30, 23.43, 24.00),   # CTA
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


def centred(d, y, text, fnt, fill, w):
    d.text(((w - d.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)


def annotate(img, f):
    img = img.convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    t = (f - 1) / FPS
    shot = next(s for s in SHOTS if s[0] <= f <= s[1])
    d.rectangle([0, 0, w, 28], fill=NAVY + (210,))
    d.text((10, 6), f"PREVIS  {shot[2]}  |  {shot[3]}", font=font(11, "SemiBold"), fill=WHITE)
    tc = "%05.2f s" % t
    d.text((w - 10 - d.textlength(tc, font=font(11)), 6), tc, font=font(11), fill=WHITE)
    for a, b, txt, style in SUPERS:
        if a <= t < b:
            fnt = font(26 if style == "hook" else 20)
            y = 150
            for ln in txt.split("\n"):
                tw = d.textlength(ln, font=fnt)
                d.rounded_rectangle([(w - tw) / 2 - 12, y - 6, (w + tw) / 2 + 12, y + fnt.size + 10], 8,
                                    fill=(255, 255, 255, 235) if style == "hook" else (10, 14, 22, 175))
                centred(d, y, ln, fnt, (15, 15, 18) if style == "hook" else WHITE, w)
                y += fnt.size + 18
    for a, b, txt in CAPTIONS:
        if a <= t < b:
            fnt = font(17, "SemiBold")
            tw = d.textlength(txt, font=fnt)
            y = h - 260
            d.rounded_rectangle([(w - tw) / 2 - 8, y - 3, (w + tw) / 2 + 8, y + 24], 6, fill=(0, 0, 0, 170))
            centred(d, y, txt, fnt, WHITE, w)
    if f >= 673:
        d.rectangle([0, 0, w, h], fill=NAVY + (240,))
        d.rectangle([60, 470, w - 60, 474], fill=ORANGE)
        centred(d, 400, "MONSOOR MOTORS", font(36), WHITE, w)
        centred(d, 490, "0434 137 393", font(28), WHITE, w)
        centred(d, 880, "MD32748  |  *Real-world tests: Mitsubishi ASX 2.0 petrol 10.4 L/100km (WhichCar) vs Toyota C-HR Hybrid 5.2 L/100km (RACV)  |  AI-generated scenes",
                font(8, "Medium"), (190, 200, 214), w)
    return img


def fp(n):
    return os.path.join(FRAMES, "f_%04d.png" % n)


os.makedirs(OUT, exist_ok=True)
tmp = os.path.join(FRAMES, "_ann")
os.makedirs(tmp, exist_ok=True)
for n in range(1, END + 1):
    annotate(Image.open(fp(n)), n).save(os.path.join(tmp, "a_%04d.png" % n))

inputs, filt = [], []
for i, (fn, a, b, at) in enumerate(CUTS):
    inputs += ["-i", os.path.join(VOICE, fn)]
    ms = int(at * 1000)
    filt.append(f"[{i}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.02,"
                f"afade=t=out:st={b - a - 0.05:.2f}:d=0.05,adelay={ms}|{ms}[v{i}]")
inputs = ["-f", "lavfi", "-t", "29", "-i", "anullsrc=r=48000:cl=mono"] + inputs
filt = [f.replace(f"[{i}:a]", f"[{i + 1}:a]", 1) for i, f in enumerate(filt)]
filt.append("[0:a]" + "".join(f"[v{i}]" for i in range(len(CUTS))) + f"amix=inputs={len(CUTS) + 1}:duration=first:normalize=0[a]")
wav = os.path.join(OUT, "QJ-temp-voice.wav")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(filt), "-map", "[a]", "-ac", "1", wav], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "a_%04d.png"), "-i", wav,
                "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                "-c:a", "aac", "-b:a", "192k", "-t", "29", os.path.join(OUT, "QJ-29s-Previs.mp4")], check=True)

picks = [(40, "S1 Price board"), (100, "S2a The queue"), (140, "S2b Dave at the pump"), (175, "S2c Mia asleep"),
         (230, "S3 Silent arrival"), (300, "S4 Hello mates"), (400, "S5 Can we get one?"), (465, "S6a Keys"),
         (545, "S6b Good job"), (600, "S7 Home"), (690, "S8 Brand")]
tw_, th_, pad, cap = 280, 498, 16, 40
cols = 6
rows = (len(picks) + cols - 1) // cols
board = Image.new("RGB", (pad + cols * (tw_ + pad), 70 + rows * (th_ + cap + pad)), WHITE)
bd = ImageDraw.Draw(board)
bd.text((pad, 20), "Monsoor Motors  |  'Queue Jump' 29 s reel  |  free previs storyboard", font=font(24), fill=NAVY)
for i, (n, label) in enumerate(picks):
    x = pad + (i % cols) * (tw_ + pad)
    y = 70 + (i // cols) * (th_ + cap + pad)
    board.paste(annotate(Image.open(fp(n)), n).resize((tw_, th_), Image.LANCZOS), (x, y))
    bd.text((x, y + th_ + 8), label, font=font(16, "SemiBold"), fill=NAVY)
board.save(os.path.join(OUT, "QJ-Storyboard.png"))
print("done")
