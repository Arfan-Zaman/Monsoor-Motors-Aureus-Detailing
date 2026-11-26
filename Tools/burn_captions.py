#!/usr/bin/env python3
"""Burn word-grouped captions onto a video without libass/drawtext.

Renders one transparent PNG per cue with Pillow (Montserrat), then overlays them
with ffmpeg's overlay filter, each enabled only for its cue time. Audio is
stream-copied, never re-encoded.

Usage:
  python -I Tools/burn_captions.py IN.mp4 captions.srt OUT.mp4 \
      --font "Brand Kit/.../Montserrat-Bold.ttf" --size 62 \
      --margin-v-pct 12 --max-width-pct 90 [--audio-from OTHER.mp4] [--vf "crop=..."]

--vf runs before the captions (e.g. a crop); --audio-from takes the audio track
from another file (stream copy). Brand defaults: Warm White #FAF8F5 text,
Deep Navy #08182D outline.
"""
import argparse, os, re, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def parse_srt(path):
    cues = []
    for block in re.split(r"\n\s*\n", open(path, encoding="utf-8").read().strip()):
        lines = block.strip().splitlines()
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", lines[1])
        g = list(map(int, m.groups()))
        s = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        e = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        cues.append((s, e, " ".join(lines[2:])))
    return cues


def wrap(draw, text, font, maxw, stroke):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if cur and draw.textlength(t, font=font) + 2 * stroke > maxw:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp"); ap.add_argument("srt"); ap.add_argument("out")
    ap.add_argument("--font", required=True)
    ap.add_argument("--size", type=int, default=62)
    ap.add_argument("--stroke", type=int, default=6)
    ap.add_argument("--margin-v-pct", type=float, default=12)
    ap.add_argument("--max-width-pct", type=float, default=90)
    ap.add_argument("--text-color", default="#FAF8F5")
    ap.add_argument("--outline-color", default="#08182D")
    ap.add_argument("--vf", default="")
    ap.add_argument("--audio-from", default="")
    ap.add_argument("--crf", type=int, default=17)
    a = ap.parse_args()

    probe = ["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
             "stream=width,height", "-of", "csv=p=0", a.inp]
    W, H = map(int, subprocess.run(probe, capture_output=True, text=True, check=True).stdout.strip().split(","))
    if a.vf:  # size after the pre-filter
        m = re.search(r"crop=(\d+):(\d+)", a.vf)
        if m: W, H = int(m.group(1)), int(m.group(2))

    font = ImageFont.truetype(a.font, a.size)
    fill, outline = hex_rgb(a.text_color), hex_rgb(a.outline_color)
    maxw = W * a.max_width_pct / 100
    bottom = H - H * a.margin_v_pct / 100
    tmp = tempfile.mkdtemp(prefix="caps_")
    cues = parse_srt(a.srt)
    boxes = []
    for i, (s, e, text) in enumerate(cues):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        lines = wrap(d, text, font, maxw, a.stroke)
        asc, desc = font.getmetrics()
        lh = asc + desc
        y = bottom - lh * len(lines)
        for ln in lines:
            tw = d.textlength(ln, font=font)
            d.text(((W - tw) / 2, y), ln, font=font, fill=fill + (255,),
                   stroke_width=a.stroke, stroke_fill=outline + (255,))
            y += lh
        bb = img.getbbox()
        boxes.append(bb)
        img.save(os.path.join(tmp, f"c{i:03d}.png"))

    args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.inp]
    for i in range(len(cues)):
        args += ["-i", os.path.join(tmp, f"c{i:03d}.png")]
    aidx = None
    if a.audio_from:
        args += ["-i", a.audio_from]; aidx = len(cues) + 1
    chain = f"[0:v]{a.vf + ',' if a.vf else ''}format=yuv420p[b0];"
    for i, (s, e, _) in enumerate(cues):
        chain += f"[b{i}][{i + 1}:v]overlay=0:0:enable='between(t,{s:.3f},{e - 0.001:.3f})'[b{i + 1}];"
    chain = chain.rstrip(";")
    args += ["-filter_complex", chain, "-map", f"[b{len(cues)}]",
             "-map", f"{aidx}:a" if aidx else "0:a",
             "-c:v", "libx264", "-crf", str(a.crf), "-preset", "slow", "-profile:v", "high",
             "-pix_fmt", "yuv420p", "-r", "30", "-fps_mode", "cfr",
             "-c:a", "copy", "-movflags", "+faststart", "-shortest", a.out]
    subprocess.run(args, check=True)
    ys0 = min(b[1] for b in boxes); ys1 = max(b[3] for b in boxes)
    xs0 = min(b[0] for b in boxes); xs1 = max(b[2] for b in boxes)
    print(f"{a.out}: {len(cues)} cues, text box y {ys0}-{ys1} x {xs0}-{xs1} on {W}x{H}")


if __name__ == "__main__":
    main()
