"""Finish the 39 s 'Queue Jump' previs: labels, supers, captions, dash labels, flash, brand card,
temp voice, storyboard. Adapted from qj_post.py; all times from DIRECTOR-CUT.md B2.

Run:  /opt/miniconda3/bin/python -I qj39_post.py <frames_dir> <voice_dir> <out_dir>
Frames come from qj39_scene.py (360x640, 936 frames); output is scaled to 720x1280.
Temp voice uses only Arfan's locked track. Lines not recorded yet are shown as [TO RECORD].
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qj39_shots import END, FPS, SHOTS, rng, shot_at  # noqa: E402

FRAMES, VOICE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
FONT = os.path.expanduser("~/Library/Fonts/Montserrat-Variable.ttf")
W, H = 720, 1280
NAVY, ORANGE, WHITE = (15, 39, 71), (255, 95, 21), (247, 245, 242)

SUPERS = [  # (in, out, text, style)
    (0.15, 6.35, "Tuesday night. Perth.", "hook"),
    (15.75, 18.10, "Over 40% less fuel than his ASX.*", "tag"),
]
CAPTIONS = [
    (12.10, 12.90, "Hello mates."),
    (19.85, 21.30, "Dad... can we get one?   [TO RECORD: Mia]"),
    (25.30, 25.90, "Good job.   [TO RECORD: Monsoor clone]"),
    (26.45, 28.05, "That means a lot."),
    (28.10, 29.30, "You choose the car!"),
    (29.28, 30.40, "We bring it to your home!"),
]
DASH = [  # (in, out, text, y as a fraction of the frame)
    (0.90, 1.30, "6.8 L/100km*  ·  52,846 km", 0.70),
    (1.85, 2.25, "6.3 L/100km*  ·  29,417 km", 0.70),
    (2.75, 3.15, "6.6 L/100km*  ·  31,268 km", 0.70),
    (3.65, 4.05, "41,593 km", 0.70),
    (6.00, 6.45, "7.6 L/100km*  ·  64,873 km", 0.70),
    (15.65, 17.05, "4.3 L/100km*  ·  45,000 km", 0.66),
]
SPEED = (3.65, 4.05, 64, 67)       # V8 speedo comp, shot 9
FLASH = (4.20, 3)                  # full-frame white flash: start, frames
CUTS = [  # (file, src start, src end, place at)
    ("Arfan-script-voice-LOCKED.wav", 4.50, 5.40, 12.10),    # "Hello mates"
    ("Arfan-script-voice-LOCKED.wav", 0.00, 1.56, 26.45),    # "That means a lot."
    ("Arfan-script-voice-LOCKED.wav", 21.30, 23.43, 28.10),  # CTA V.O.
]
BRAND = 34.00


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


def centred(d, y, text, fnt, fill):
    d.text(((W - d.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)


def pill(d, y, text, fnt, fill_bg, fill_fg, pad=12):
    tw = d.textlength(text, font=fnt)
    d.rounded_rectangle([(W - tw) / 2 - pad, y - 6, (W + tw) / 2 + pad, y + fnt.size + 10], 10, fill=fill_bg)
    centred(d, y, text, fnt, fill_fg)


def fade(t, a, d=0.25):
    return max(0.0, min(1.0, (t - a) / d))


def annotate(img, f):
    img = img.convert("RGB").resize((W, H), Image.LANCZOS)
    t = (f - 1) / FPS
    if FLASH[0] <= t < FLASH[0] + FLASH[1] / FPS:
        img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img, "RGBA")
    n, tin, tout, size, cam, desc = shot_at(f)
    # previs label bar (shot ID, size/angle, lens/move, time)
    d.rectangle([0, 0, W, 64], fill=NAVY + (215,))
    d.text((14, 8), f"PREVIS  #{n:02d}  {size}", font=font(19, "Bold"), fill=WHITE)
    tc = "%05.2f s" % t
    d.text((W - 14 - d.textlength(tc, font=font(19)), 8), tc, font=font(19), fill=ORANGE)
    d.text((14, 36), f"{tin:.2f}-{tout:.2f}  |  {cam}  |  {desc}"[:78], font=font(14, "Medium"), fill=(214, 222, 232))
    if t < BRAND:   # watermark top left, about 55%
        d.text((16, 76), "MONSOOR MOTORS", font=font(16, "Bold"), fill=(255, 255, 255, 140))
    for a, b, txt, style in SUPERS:
        if a <= t < b:
            if style == "hook":
                pill(d, 300, txt, font(40), (255, 255, 255, 235), (15, 15, 18))
            else:
                pill(d, 300, txt, font(30), (10, 14, 22, 190), WHITE)
    for a, b, txt, y in DASH:
        if a <= t < b:
            pill(d, int(H * y), txt, font(28, "SemiBold"), (0, 0, 0, 150), (255, 236, 200))
    if SPEED[0] <= t < SPEED[1]:
        u = (t - SPEED[0]) / (SPEED[1] - SPEED[0])
        pill(d, int(H * 0.60), "%d km/h   (60 zone)" % round(SPEED[2] + (SPEED[3] - SPEED[2]) * u), font(28, "SemiBold"),
             (120, 0, 0, 170), WHITE)
    for a, b, txt in CAPTIONS:
        if a <= t < b:
            pill(d, H - 420, txt, font(26, "SemiBold"), (0, 0, 0, 175), WHITE, pad=10)
    if t >= BRAND:   # brand card over the golden-hour hero
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        for y in range(H):
            a = int(200 * max(0.0, (y - H * 0.35) / (H * 0.65)) ** 1.2)
            od.line([(0, y), (W, y)], fill=NAVY + (a,))
        img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle([0, 0, W, 64], fill=NAVY + (215,))
        d.text((14, 8), f"PREVIS  #41  {size}", font=font(19, "Bold"), fill=WHITE)
        d.text((W - 14 - d.textlength(tc, font=font(19)), 8), tc, font=font(19), fill=ORANGE)
        d.text((14, 36), f"{tin:.2f}-{tout:.2f}  |  {cam}  |  brand card"[:78], font=font(14, "Medium"), fill=(214, 222, 232))
        al = fade(t, 34.30, 1.0)
        if al > 0:
            col = WHITE + (int(255 * al),)
            centred(d, 800, "MONSOOR MOTORS", font(54), col)
            d.rectangle([150, 872, W - 150, 876], fill=ORANGE + (int(255 * al),))
        if t >= 35.40:
            centred(d, 900, "0434 137 393", font(44), WHITE + (int(255 * fade(t, 35.40)),))
        if t >= 35.70:
            centred(d, 966, "monsoormotors.com.au", font(30, "SemiBold"), (230, 236, 244, int(255 * fade(t, 35.70))))
        if t >= 36.00:
            centred(d, 1190, "MD32748  ·  *Official combined: ASX 2.0 7.6 vs C-HR Hybrid 4.3 L/100km",
                    font(15, "Medium"), (200, 210, 222, int(255 * fade(t, 36.00))))
    return img


def fp(n):
    return os.path.join(FRAMES, "f_%04d.png" % n)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(FRAMES, "_ann")
    os.makedirs(tmp, exist_ok=True)
    for n in range(1, END + 1):
        annotate(Image.open(fp(n)), n).save(os.path.join(tmp, "a_%04d.png" % n), compress_level=1)

    dur = END / FPS
    inputs, filt = ["-f", "lavfi", "-t", "%.3f" % dur, "-i", "anullsrc=r=48000:cl=mono"], []
    for i, (fn, a, b, at) in enumerate(CUTS):
        inputs += ["-i", os.path.join(VOICE, fn)]
        ms = int(at * 1000)
        filt.append(f"[{i + 1}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,pan=mono|c0=c0,afade=t=in:d=0.02,"
                    f"afade=t=out:st={b - a - 0.05:.2f}:d=0.05,adelay={ms}[v{i}]")
    filt.append("[0:a]" + "".join(f"[v{i}]" for i in range(len(CUTS))) +
                f"amix=inputs={len(CUTS) + 1}:duration=first:normalize=0[a]")
    wav = os.path.join(FRAMES, "QJ39-temp-voice.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(filt), "-map", "[a]",
                    "-ac", "1", wav], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "a_%04d.png"),
                    "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "21", "-r", str(FPS),
                    "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % dur, os.path.join(OUT, "QJ39-Previs.mp4")], check=True)

    # storyboard: one labelled thumbnail per shot (middle frame of each shot)
    tw_, th_, pad, cap, cols = 200, 356, 12, 54, 9
    rows = (len(SHOTS) + cols - 1) // cols
    board = Image.new("RGB", (pad + cols * (tw_ + pad), 80 + rows * (th_ + cap + pad)), WHITE)
    bd = ImageDraw.Draw(board)
    bd.text((pad, 22), "Monsoor Motors  |  'Queue Jump' 39 s ad  |  previs storyboard (DIRECTOR-CUT B2, one frame per shot)",
            font=font(26), fill=NAVY)
    for i, s in enumerate(SHOTS):
        n, tin, tout, size, cam, desc = s
        a, b = rng(n)
        m = (a + b) // 2
        if n == 10:
            m = int(round(FLASH[0] * FPS)) + 4   # just after the flash
        if n == 41:
            m = b - 12
        x = pad + (i % cols) * (tw_ + pad)
        y = 80 + (i // cols) * (th_ + cap + pad)
        board.paste(annotate(Image.open(fp(m)), m).resize((tw_, th_), Image.LANCZOS), (x, y))
        bd.text((x, y + th_ + 4), f"#{n} {tin:.2f}-{tout:.2f}  {size}"[:30], font=font(13, "Bold"), fill=NAVY)
        bd.text((x, y + th_ + 22), desc[:32], font=font(12, "Medium"), fill=(60, 70, 85))
        bd.text((x, y + th_ + 38), cam[:34], font=font(11, "Medium"), fill=(110, 118, 130))
    board.save(os.path.join(OUT, "QJ39-Storyboard.png"))
    print("done")
