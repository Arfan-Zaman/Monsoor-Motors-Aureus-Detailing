"""Turn the Blender previs frames into a labelled animatic, a storyboard and a floor plan.

Run:  python previs_post.py <frames_dir> <out_dir>
Needs Pillow and ffmpeg. Timings match previs_scene.py (24 fps).
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

FRAMES, OUT = sys.argv[1], sys.argv[2]
FONT = os.path.expanduser("~/Library/Fonts/Montserrat-Variable.ttf")
FPS, S1_END, END = 24, 264, 648
NAVY, ORANGE, WHITE = (15, 39, 71), (255, 95, 21), (247, 245, 242)


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


SHOTS = [
    (1, S1_END, "SHOT 1 of 2", "Wide two-shot  |  35 mm  |  eye level  |  slow push-in"),
    (S1_END + 1, END, "SHOT 2 of 2", "Arfan steps in  |  50 mm  |  small arc + push-in to medium"),
]
BEATS = [  # (first frame, last frame, speaker, line or action)
    (1, 105, "MONSOOR", "I'm Monsoor, founder of Monsoor Motors."),
    (106, 215, "MONSOOR", "Meet Arfan, our new CEO.  (presents him with an open hand)"),
    (216, 264, "ACTION", "Arfan turns to the lens and starts to step forward. CUT on the step."),
    (265, 330, "ARFAN", "Thanks, Monsoor.  (walks into a medium shot, Monsoor stays behind him)"),
    (331, 400, "ARFAN", "I'm Arfan."),
    (401, 540, "ARFAN", "My job: every Japanese hybrid we import is chosen, checked and delivered the right way."),
    (541, 600, "ARFAN", "Come and see for yourself.  (points back to the C-HR)"),
    (601, 648, "END CARD", "Logo  |  530 Albany Highway, Victoria Park  |  0434 137 393  |  MD32748"),
]


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def annotate(img, frame):
    img = img.convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    shot = next(s for s in SHOTS if s[0] <= frame <= s[1])
    beat = next(b for b in BEATS if b[0] <= frame <= b[1])
    d.rectangle([0, 0, w, 74], fill=NAVY + (235,))
    d.rectangle([0, 74, w, 78], fill=ORANGE + (255,))
    d.text((16, 10), shot[2], font=font(22), fill=WHITE)
    d.text((16, 42), shot[3], font=font(13, "Medium"), fill=WHITE)
    tc = "%05.2f s" % ((frame - 1) / FPS)
    d.text((w - 16 - d.textlength(tc, font=font(16)), 14), tc, font=font(16), fill=WHITE)
    d.text((16, 86), "Navy figure = Monsoor   |   Black figure with beard = Arfan", font=font(12, "Medium"), fill=NAVY)
    f_line = font(17, "SemiBold")
    lines = wrap(d, beat[3], f_line, w - 48)
    box_h = 40 + 24 * len(lines)
    top = h - 205 - box_h  # keep clear of the bottom 400 px safe area (at 1080x1920)
    d.rounded_rectangle([12, top, w - 12, top + box_h], 10, fill=(10, 14, 22, 205))
    d.text((24, top + 9), beat[2], font=font(13), fill=ORANGE)
    for i, line in enumerate(lines):
        d.text((24, top + 30 + 24 * i), line, font=f_line, fill=WHITE)
    return img


def frame_path(n):
    return os.path.join(FRAMES, "f_%04d.png" % n)


os.makedirs(OUT, exist_ok=True)
tmp = os.path.join(FRAMES, "_annotated")
os.makedirs(tmp, exist_ok=True)
for n in range(1, END + 1):
    annotate(Image.open(frame_path(n)), n).save(os.path.join(tmp, "a_%04d.png" % n))

subprocess.run([
    "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "a_%04d.png"),
    "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
    os.path.join(OUT, "CEO-Intro-Previs.mp4")], check=True)

# Storyboard: six key moments.
keys = [(1, "1A  Start: wide two-shot"), (165, "1B  Monsoor presents Arfan"), (262, "1C  Cut point: Arfan's first step"),
        (300, "2A  Arfan walks in, camera arcs"), (440, "2B  The promise, open hands"), (590, "2C  Points back to the C-HR")]
tw, th, pad, cap = 432, 768, 24, 54
board = Image.new("RGB", (pad + 3 * (tw + pad), 80 + 2 * (th + cap + pad)), WHITE)
bd = ImageDraw.Draw(board)
bd.text((pad, 22), "Monsoor Motors  |  CEO intro  |  previs storyboard (2 shots, 27 s)", font=font(26), fill=NAVY)
for i, (n, label) in enumerate(keys):
    x = pad + (i % 3) * (tw + pad)
    y = 80 + (i // 3) * (th + cap + pad)
    board.paste(annotate(Image.open(frame_path(n)), n).resize((tw, th), Image.LANCZOS), (x, y))
    bd.text((x, y + th + 12), label, font=font(20, "SemiBold"), fill=NAVY)
board.save(os.path.join(OUT, "CEO-Intro-Storyboard.png"))

# Floor plan (top view). 1 m = 70 px. Camera is at the bottom, wall at the top.
S, W, H = 70, 1000, 1150
ox, oy = W // 2, 700  # world (0, 0)
plan = Image.new("RGB", (W, H), WHITE)
p = ImageDraw.Draw(plan)


def pt(x, y):
    return (ox + x * S, oy - y * S)


def arrow(a, b, col, width=4):
    p.line([pt(*a), pt(*b)], fill=col, width=width)
    import math
    ang = math.atan2(-(b[1] - a[1]), b[0] - a[0])
    bx, by = pt(*b)
    for da in (2.6, -2.6):
        p.line([(bx, by), (bx + 16 * math.cos(ang + da), by + 16 * math.sin(ang + da))], fill=col, width=width)


for gx in range(-7, 8):
    p.line([pt(gx, -6), pt(gx, 10)], fill=(226, 226, 226))
for gy in range(-6, 11):
    p.line([pt(-7, gy), pt(7, gy)], fill=(226, 226, 226))
p.text((24, 20), "Floor plan (top view)  |  grid = 1 m", font=font(24), fill=NAVY)
p.rectangle([pt(-7, 9.15), pt(7, 8.85)], fill=(200, 196, 188))
p.text((pt(-2.3, 8.7)), "Dealership wall + MONSOOR MOTORS sign", font=font(16, "SemiBold"), fill=NAVY)
import math
c, s_ = math.cos(math.radians(-62)), math.sin(math.radians(-62))
corners = [(0.35 + x * c - y * s_, 3.5 + x * s_ + y * c) for x, y in [(-0.9, -2.18), (0.9, -2.18), (0.9, 2.18), (-0.9, 2.18)]]
p.polygon([pt(*q) for q in corners], fill=(185, 190, 198), outline=(60, 60, 60))
p.text(pt(1.4, 5.3), "Toyota C-HR\n(mostly side-on)", font=font(15, "SemiBold"), fill=(40, 40, 40))


def who(xy, col, label, dx=14, dy=-8):
    x, y = pt(*xy)
    p.ellipse([x - 15, y - 15, x + 15, y + 15], fill=col, outline=(20, 20, 20))
    p.text((x + dx, y + dy), label, font=font(15, "SemiBold"), fill=(20, 20, 20))


who((-0.38, 0.0), NAVY, "Monsoor (shot 1)", dx=-150)
who((-0.62, 0.55), (120, 135, 160), "Monsoor (shot 2)", dx=-160, dy=-22)
who((0.38, 0.12), (30, 30, 30), "Arfan (shot 1)", dx=22, dy=-24)
who((0.18, -1.30), (30, 30, 30), "Arfan (shot 2 end)", dx=22)
arrow((0.38, 0.0), (0.2, -1.05), (30, 30, 30), 3)


def cam(xy, col, label, dx=20, dy=-8):
    x, y = pt(*xy)
    p.polygon([(x, y - 16), (x - 14, y + 12), (x + 14, y + 12)], fill=col)
    p.text((x + dx, y + dy), label, font=font(15, "SemiBold"), fill=col)


cam((0.0, -4.20), ORANGE, "Cam 1 start, 35 mm", dx=-190)
arrow((0.0, -4.05), (0.0, -3.5), ORANGE)
cam((1.05, -5.10), (0, 140, 140), "Cam 2 start, 50 mm")
arrow((1.0, -5.05), (0.1, -4.15), (0, 140, 140))
p.text((24, H - 110), "Orange: shot 1 camera (slow push-in, eye level 1.5 m).", font=font(16, "Medium"), fill=ORANGE)
p.text((24, H - 82), "Teal: shot 2 camera (arcs left and pushes in while Arfan walks 1.4 m forward).", font=font(16, "Medium"), fill=(0, 140, 140))
p.text((24, H - 54), "Black arrow: Arfan's walk. Monsoor eases back half a step and watches him.", font=font(16, "Medium"), fill=(30, 30, 30))
plan.save(os.path.join(OUT, "CEO-Intro-Floorplan.png"))
print("done")
