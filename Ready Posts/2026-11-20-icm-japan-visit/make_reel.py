"""ICM Japan visit announcement ad reel (15 s, 9:16, 1080x1920) for Monsoor Motors.

Usage:
  /opt/miniconda3/bin/python -I make_reel.py <work_dir> <out.mp4>

<work_dir> must hold:
  shake.mp4     Kling 4.0 i2v of the handshake photo (5 s)
  seated.mp4    Kling 4.0 i2v of the seated photo (4 s)
  v_intro.wav   his cloned voice, ML300 reel line T1 ("Hi, I'm Monsor from Monsoor Motors. Look at ...")
  v_japan.wav   his cloned voice, ML300 reel line T7 ("We can also import cars like this from Japan ...")
  music.mp3     original AI underscore (Launch Reels/ad/audio/music.mp3, job 4ffeabd7)

Shots (hard cut on the handshake, short dissolve into the end card):
  0.00-5.00  handshake (hook)          label: ANNOUNCEMENT / ICM Japan visits Monsoor Motors + pre-orders open
  5.00-9.00  seated, mid-conversation  label: Mr. Trimoty, ICM Japan
  9.00-15.0  navy end card, slow push-in: logo, offer line, phone, web

Sound: music bed all the way through; his voice sits in the background (soft room feel),
the music dips a little under it:
  0.5 s  "Hi, I'm Monsor from Monsoor Motors."
  4.0 s  "We can also import cars from Japan for you, at an affordable price. We are taking pre-orders now."
         ("like this" cut out; it referred to the Mercedes)
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FONT = ROOT / "Brand Kit/00 Fonts/Montserrat-Variable.ttf"
LOGO = ROOT / "Brand Kit/01 Logo/Monsoor-Logo-White.png"
WMARK = ROOT / "Brand Kit/01 Logo/Watermark/Watermark-White.png"

W, H, FPS, DUR = 1080, 1920, 30, 15.0
NAVY = (15, 39, 71)
ORANGE = (255, 95, 21)
WARM = (247, 245, 242)

S1, S2, S4 = 0.0, 5.0, 9.0  # shot starts (S4 = end card)


def font(size, weight="Bold"):
    f = ImageFont.truetype(str(FONT), size)
    f.set_variation_by_name(weight)
    return f


def text_card(path, lines, box):
    """Transparent 1080x1920 PNG with centred text lines inside box=(x,y,w,h).
    lines = [(text, size, weight, colour), ...]"""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x, y, w, h = box
    heights = []
    for t, s, wt, c in lines:
        f = font(s, wt)
        bb = d.textbbox((0, 0), t, font=f)
        heights.append((f, bb, t, c))
    gap = 14
    total = sum(bb[3] - bb[1] for _, bb, _, _ in heights) + gap * (len(lines) - 1)
    cy = y + (h - total) // 2
    for f, bb, t, c in heights:
        tw = bb[2] - bb[0]
        d.text((x + (w - tw) // 2 - bb[0], cy - bb[1]), t, font=f, fill=c)
        cy += bb[3] - bb[1] + gap
    img.save(path)


def mask(path, box, radius=36):
    """Grey rounded-rect mask (white = glass) the size of the box."""
    x, y, w, h = box
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=255)
    m.convert("RGB").save(path)


def end_card(path):
    img = Image.new("RGB", (W, H), NAVY)
    # soft vignette glow so the card is not a flat slab
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((-200, 300, W + 200, 1500), fill=60)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    img = Image.composite(Image.new("RGB", (W, H), (32, 62, 104)), img, glow)
    logo = Image.open(LOGO).convert("RGBA")
    lw = 640
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    img.paste(logo, ((W - lw) // 2, 330), logo)
    d = ImageDraw.Draw(img)

    def centre(t, y, size, wt, c):
        f = font(size, wt)
        bb = d.textbbox((0, 0), t, font=f)
        d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y), t, font=f, fill=c)

    centre("Tell us the car you want.", 900, 52, "Bold", WARM)
    centre("We'll source it from Japan.", 970, 52, "Bold", WARM)
    # orange accent rule
    d.rounded_rectangle((W // 2 - 60, 1070, W // 2 + 60, 1078), 4, fill=ORANGE)
    centre("Japanese import pre-orders now open", 1110, 38, "SemiBold", ORANGE)
    centre("0434 137 393", 1200, 72, "ExtraBold", WARM)
    centre("monsoormotors.com.au", 1295, 40, "Medium", WARM)
    centre("530 Albany Hwy, Victoria Park WA", 1350, 32, "Regular", (200, 208, 220))
    centre("Visit photos animated with AI", 1460, 24, "Regular", (150, 162, 182))
    img.save(path)


def run(cmd):
    print(" ".join(str(c) for c in cmd[:6]), "...")
    subprocess.run([str(c) for c in cmd], check=True)


def main(work, out):
    work = Path(work)
    g = work / "gfx"
    g.mkdir(exist_ok=True)

    labels = [
        # (box, lines, t0, t1)
        ((90, 1130, 900, 380),
         [("ANNOUNCEMENT", 34, "SemiBold", ORANGE),
          ("ICM Japan visits", 62, "Bold", WARM), ("Monsoor Motors", 84, "ExtraBold", WARM),
          ("Japanese import pre-orders now open", 32, "SemiBold", WARM)],
         0.10, S2 - 0.05),
        ((110, 1250, 860, 190),
         [("Mr. Trimoty, ICM Japan", 58, "Bold", WARM),
          ("Productive talks on Japanese car imports", 34, "Medium", WARM)],
         S2 + 0.25, S4 - 0.25),
    ]
    for i, (box, lines, *_) in enumerate(labels):
        text_card(g / f"t{i}.png", lines, box)
        mask(g / f"m{i}.png", box)
    end_card(g / "end.png")

    wm = Image.open(WMARK).convert("RGBA")
    ww = 300
    wm = wm.resize((ww, int(wm.height * ww / wm.width)), Image.LANCZOS)
    a = wm.getchannel("A").point(lambda v: int(v * 0.55))
    wm.putalpha(a)
    wm.save(g / "wm.png")

    # --- base timeline -------------------------------------------------
    norm = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,format=yuv420p"
    d1, d2, d4 = S2 - S1, S4 - S2, DUR - S4
    n4 = int(round((d4 + 0.3) * FPS))
    fc = [
        f"[0:v]trim=0:{d1},setpts=PTS-STARTPTS,{norm}[v1]",
        f"[1:v]trim=0:{d2 + 0.03},setpts=PTS-STARTPTS,{norm}[v2]",
        # end card: very slow push-in so it is not a dead still
        f"[2:v]scale={W * 2}:{H * 2},zoompan=z='1+0.035*on/{n4}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d={n4}:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p,trim=0:{d4 + 0.2},setpts=PTS-STARTPTS,settb=1/30[v4]",
        "[v1][v2]concat=n=2:v=1:a=0,settb=1/30[v12]",
        # 6-frame dissolve into the end card
        f"[v12][v4]xfade=transition=fade:duration=0.2:offset={S4 - 0.2:.2f},trim=0:{DUR}[base]",
    ]
    inputs = [
        "-i", work / "shake.mp4",
        "-i", work / "seated.mp4",
        "-loop", "1", "-framerate", FPS, "-t", 1, "-i", g / "end.png",
        "-loop", "1", "-framerate", FPS, "-t", DUR, "-i", g / "wm.png",
        "-i", work / "v_intro.wav",
        "-i", work / "v_japan.wav",
        "-i", work / "music.mp3",
    ]
    idx = 7
    cur = "base"
    # watermark on footage only
    fc.append(f"[{cur}][3:v]overlay=56:262:enable='lt(t,{S4 - 0.2})'[w0]")
    cur = "w0"
    for i, (box, _, t0, t1) in enumerate(labels):
        x, y, w, h = box
        inputs += ["-loop", "1", "-framerate", FPS, "-t", DUR, "-i", g / f"m{i}.png"]
        inputs += ["-loop", "1", "-framerate", FPS, "-t", DUR, "-i", g / f"t{i}.png"]
        mi, ti = idx, idx + 1
        idx += 2
        fade = f"fade=t=in:st={t0}:d=0.2{{a}},fade=t=out:st={t1 - 0.2}:d=0.2{{a}}"
        fc += [
            f"[{cur}]split[s{i}a][s{i}b]",
            f"[s{i}b]crop={w}:{h}:{x}:{y},gblur=sigma=22,eq=brightness=-0.10:saturation=0.8,"
            f"colorchannelmixer=rr=0.85:gg=0.88:bb=0.95[bl{i}]",
            f"[{mi}:v]format=gray,{fade.format(a='')}[mk{i}]",
            f"[bl{i}][mk{i}]alphamerge[gl{i}]",
            f"[s{i}a][gl{i}]overlay={x}:{y}[g{i}]",
            f"[{ti}:v]format=rgba,{fade.format(a=':alpha=1')}[tx{i}]",
            f"[g{i}][tx{i}]overlay=0:0[o{i}]",
        ]
        cur = f"o{i}"
    fc.append(f"[{cur}]format=yuv420p[vout]")
    # audio: his voice in the background over the music, master about -14 LUFS
    fc += [
        # "Hi, I'm Monsor from Monsoor Motors." (cut before "Look at this Mercedes")
        "[4:a]aresample=48000,atrim=0:2.74,afade=t=out:st=2.66:d=0.08,adelay=500|500[vi]",
        # drop "like this": keep 0-1.19 s and 1.66 s to the end
        "[5:a]aresample=48000,asplit[ja][jb]",
        "[ja]atrim=0:1.19,afade=t=out:st=1.16:d=0.03[j1]",
        "[jb]atrim=1.66,asetpts=PTS-STARTPTS,afade=t=in:d=0.03[j2]",
        "[j1][j2]concat=n=2:v=0:a=1,adelay=4000|4000[vj]",
        "[vi][vj]amix=inputs=2:normalize=0:duration=longest,"
        "highpass=f=90,lowpass=f=7500,aecho=0.8:0.6:38:0.14,loudnorm=I=-20:TP=-3,aresample=48000,"
        f"apad,atrim=0:{DUR},asplit[vo][sc]",
        f"[6:a]aresample=48000,atrim=0:{DUR},afade=t=in:d=0.3,afade=t=out:st={DUR - 1.8}:d=1.8,"
        "loudnorm=I=-21:TP=-3,aresample=48000[mu]",
        "[mu][sc]sidechaincompress=threshold=0.05:ratio=3:attack=30:release=450[mud]",
        "[mud][vo]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[aout]",
    ]
    run(["ffmpeg", "-v", "error", "-y", *inputs,
         "-filter_complex", ";".join(fc),
         "-map", "[vout]", "-map", "[aout]", "-t", DUR,
         "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart",
         "-c:a", "aac", "-b:a", "192k", out])
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
