"""ICM Japan visit announcement ad reel (15 s, 9:16, 1080x1920) for Monsoor Motors.

Usage:
  /opt/miniconda3/bin/python -I make_reel.py <work_dir> <out.mp4>

<work_dir> must hold:
  shake.mp4   Kling 4.0 i2v of the handshake photo (5 s)
  seated.mp4  Kling 4.0 i2v of the seated photo (4 s)
  icm1.jpeg   original seated photo (for the banner push-in shot)
  room.mp3    15 s room tone (mirelo_text_to_audio)

Shots (varied lengths, hard cuts on movement, one short dissolve into the end card):
  0.00-4.60  handshake (hook)          label: ANNOUNCEMENT / ICM Japan visits Monsoor Motors + pre-orders open
  4.60-8.60  seated, mid-conversation  label: Mr. Trimoty, ICM Japan
  8.60-11.40 slow push-in on the real banner ("We import Japanese Cars", "pre-orders"), no label
  11.40-15.0 navy end card             logo, offer line, phone, web
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

S1, S2, S3, S4 = 0.0, 4.6, 8.6, 11.4  # shot starts


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
         S2 + 0.25, S3 - 0.05),
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
    d1, d2, d3, d4 = S2 - S1, S3 - S2, S4 - S3, DUR - S4
    # banner shot: crop around the banner from the 3060x4080 original, slow push-in
    zp_frames = int(round((d3 + 0.3) * FPS))
    banner = (
        "crop=1100:1956:910:560,scale=2160:3840,"
        f"zoompan=z='1+0.06*on/{zp_frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)+12*sin(on/9)'"
        f":d={zp_frames}:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p"
    )
    fc = [
        f"[0:v]trim=0:{d1},setpts=PTS-STARTPTS,{norm}[v1]",
        f"[1:v]trim=0:{d2},setpts=PTS-STARTPTS,{norm}[v2]",
        f"[2:v]{banner},trim=0:{d3 + 0.2},setpts=PTS-STARTPTS[v3]",
        f"[3:v]{norm},trim=0:{d4 + 0.2},setpts=PTS-STARTPTS,settb=1/30[v4]",
        "[v1][v2][v3]concat=n=3:v=1:a=0,settb=1/30[v123]",
        # 6-frame dissolve into the end card
        f"[v123][v4]xfade=transition=fade:duration=0.2:offset={S4 - 0.2:.2f},trim=0:{DUR}[base]",
    ]
    inputs = [
        "-i", work / "shake.mp4",
        "-i", work / "seated.mp4",
        "-loop", "1", "-framerate", FPS, "-t", d3 + 0.5, "-i", work / "icm1.jpeg",
        "-loop", "1", "-framerate", FPS, "-t", d4 + 0.5, "-i", g / "end.png",
        "-i", work / "room.mp3",
        "-loop", "1", "-framerate", FPS, "-t", DUR, "-i", g / "wm.png",
    ]
    idx = 6
    cur = "base"
    # watermark on footage only
    fc.append(f"[{cur}][5:v]overlay=56:262:enable='lt(t,{S4 - 0.2})'[w0]")
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
    # audio: room tone, gentle fades, mastered to about -14 LUFS
    fc.append(
        f"[4:a]atrim=0:{DUR},afade=t=in:d=0.3,afade=t=out:st={DUR - 0.8}:d=0.8,"
        "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[aout]"
    )
    run(["ffmpeg", "-v", "error", "-y", *inputs,
         "-filter_complex", ";".join(fc),
         "-map", "[vout]", "-map", "[aout]", "-t", DUR,
         "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart",
         "-c:a", "aac", "-b:a", "192k", out])
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
