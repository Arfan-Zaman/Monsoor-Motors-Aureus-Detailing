"""Animated 'MISSION PASSED' overlay (game style) -> transparent .mov (qtrle), 720x1280, 24 fps.
Run: /opt/miniconda3/bin/python -I make_mission_anim.py <out.mov> <frames_dir>"""
import os, sys, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
PD = os.path.expanduser('~/Library/Fonts/PricedownBl.otf')
W, H, FPS, DUR = 720, 1280, 24, 2.0
out, fdir = sys.argv[1], sys.argv[2]; os.makedirs(fdir, exist_ok=True)
def font(s): return ImageFont.truetype(PD, max(int(s), 8))
def ease_out_back(t, s=1.9): t -= 1; return t * t * ((s + 1) * t + s) + 1
def clamp(x): return max(0.0, min(1.0, x))
def text_img(txt, f, fill, stroke):
    d = ImageDraw.Draw(Image.new('RGBA', (1, 1))); w = int(d.textlength(txt, font=f)) + stroke * 2 + 40; h = int(f.size * 1.4)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    sh = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((20 + 6, 8), txt, font=f, fill=(0, 0, 0, 200), stroke_width=stroke, stroke_fill=(0, 0, 0, 200))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(im).text((20, 2), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0)); return im
L1 = text_img('MISSION', font(200), (255, 200, 40), 10)
L2 = text_img('PASSED', font(200), (255, 200, 40), 10)
k = min(1.0, 680 / max(L1.width, L2.width)); L1 = L1.resize((int(L1.width*k), int(L1.height*k)), Image.LANCZOS); L2 = L2.resize((int(L2.width*k), int(L2.height*k)), Image.LANCZOS)
title = Image.new('RGBA', (max(L1.width, L2.width), L1.height + L2.height - 40), (0, 0, 0, 0))
title.alpha_composite(L1, ((title.width - L1.width) // 2, 0)); title.alpha_composite(L2, ((title.width - L2.width) // 2, L1.height - 40))
sub = text_img('+1 HAPPY FAMILY', font(72), (245, 245, 245), 6)
cy = 690
n = int(DUR * FPS)
for i in range(n):
    t = i / FPS; fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    win = clamp(t / 0.12); wout = clamp((t - 1.7) / 0.3)
    # whole frame dims behind it
    fr.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(95 * win * (1 - wout)))))
    bw = int(W * win); bx = int(W * wout)
    bh = title.height + 170
    if bw > 0:
        fr.alpha_composite(Image.new('RGBA', (bw, bh), (0, 0, 0, int(165 * (1 - wout)))), (bx, cy - bh // 2 + 40))
    p = clamp((t - 0.06) / 0.28)
    shake = (int(10 * math.sin(i * 2.3) * (1 - clamp((t - 0.34) / 0.2))) if 0.30 < t < 0.55 else 0)
    if p > 0:
        sc = 1.6 - 0.6 * ease_out_back(p)
        tw, th = int(title.width * sc), int(title.height * sc)
        ti = title.resize((tw, th), Image.LANCZOS)
        sp = clamp((t - 0.55) / 0.40)
        if 0 < sp < 1:
            shine = Image.new('RGBA', ti.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(shine)
            x = int(-120 + (ti.width + 240) * sp); sd.polygon([(x, 0), (x + 70, 0), (x + 10, ti.height), (x - 60, ti.height)], fill=(255, 255, 255, 160))
            shine.putalpha(Image.composite(shine.split()[3], Image.new('L', ti.size, 0), ti.split()[3]))
            ti = Image.alpha_composite(ti, shine)
        a = 1 - wout
        if a < 1: ti.putalpha(ti.split()[3].point(lambda v: int(v * a)))
        fr.alpha_composite(ti, (int((W - tw) / 2 + bx + shake), int(cy - th / 2 - 10 + shake // 2)))
    q = clamp((t - 0.30) / 0.22)
    if q > 0:
        si = sub.copy(); a = q * (1 - wout); si.putalpha(si.split()[3].point(lambda v: int(v * a)))
        fr.alpha_composite(si, (int((W - sub.width) / 2 + bx), int(cy + title.height / 2 - 5 + 30 * (1 - q))))
    fr.save(os.path.join(fdir, f'm{i:03d}.png'))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(fdir, 'm%03d.png'), '-c:v', 'qtrle', '-pix_fmt', 'argb', out], check=True)
print('ok', n, 'frames')
