"""Turn the Blender previs frames (v3) into a labelled video, a storyboard and a floor plan.

Run:  python previs_post.py <frames_dir> <out_dir>
Needs Pillow and ffmpeg. Timings match previs_scene.py (24 fps, 768 frames, 32 s).
"""
import math
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

FRAMES, OUT = sys.argv[1], sys.argv[2]
FONT = os.path.expanduser("~/Library/Fonts/Montserrat-Variable.ttf")
FPS, S1_END, END, CARD = 24, 216, 768, 746
NAVY, ORANGE, WHITE, TEAL = (15, 39, 71), (255, 95, 21), (247, 245, 242), (0, 140, 140)


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
    (S1_END + 1, END, "SHOT 2 of 2", "50 mm  |  camera trucks to Arfan's side, then pushes in low"),
]
BEATS = [  # (first frame, last frame, speaker, line, camera or action note)
    (1, 120, "MONSOOR", "I built Monsoor Motors on one thing: trust.", "Hand on heart. Slow push-in."),
    (121, 216, "MONSOOR", "Now meet the man who will carry it forward. Arfan, our new CEO.", "Presents Arfan with an open hand. Cut as Arfan turns to the lens."),
    (217, 290, "ARFAN", "Thank you, Monsoor.", "Tighter two-shot. Arfan squares up to the lens."),
    (291, 400, "ARFAN", "Buying a car is a big decision. So here is my promise.", "Camera trucks right to Arfan's side. Monsoor leaves frame."),
    (401, 560, "ARFAN", "Every car on this yard, from family runabouts to Japanese imported hybrids, is hand-picked, properly checked and honestly priced.", "Arfan alone, C-HR behind. He sweeps a hand to the cars."),
    (561, 655, "ARFAN", "No surprises. No pressure.", "Both palms down, calm and firm. Camera creeps in."),
    (656, 700, "ARFAN  (full energy)", "YOU choose the car.", "Points straight at the lens. Push-in starts."),
    (701, 745, "ARFAN  (full energy)", "WE bring it to your home.", "Arms open wide. Camera low, medium close-up."),
    (746, 768, "END CARD", "Monsoor Motors  |  0434 137 393", "Logo, address, licence over the last second."),
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
    if frame >= CARD:  # end card
        d.rounded_rectangle([40, 300, w - 40, 560], 18, fill=NAVY + (240,))
        d.rectangle([40, 384, w - 40, 390], fill=ORANGE + (255,))
        for y, t, f in [(326, "MONSOOR MOTORS", font(34)), (410, "530 Albany Highway, Victoria Park", font(17, "SemiBold")),
                        (446, "0434 137 393", font(30)), (500, "MV Dealer Licence MD32748", font(15, "Medium"))]:
            d.text(((w - d.textlength(t, font=f)) / 2, y), t, font=f, fill=WHITE)
        return img
    f_line, f_note = font(18, "SemiBold"), font(12, "Medium")
    lines = wrap(d, "“" + beat[3] + "”", f_line, w - 48)
    notes = wrap(d, beat[4], f_note, w - 48)
    box_h = 38 + 25 * len(lines) + 8 + 17 * len(notes) + 8
    top = h - 205 - box_h  # keep clear of the bottom safe area
    d.rounded_rectangle([12, top, w - 12, top + box_h], 10, fill=(10, 14, 22, 210))
    d.text((24, top + 9), beat[2], font=font(13), fill=ORANGE)
    y = top + 31
    for line in lines:
        d.text((24, y), line, font=f_line, fill=WHITE)
        y += 25
    y += 6
    for n in notes:
        d.text((24, y), n, font=f_note, fill=(190, 200, 214))
        y += 17
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

# Storyboard: eight key moments.
keys = [(60, "1A  Trust: hand on heart"), (175, "1B  Monsoor presents Arfan"), (250, "2A  Tighter two-shot"),
        (410, "2B  Camera arrives at his side"), (480, "2C  Sweeps to the cars"), (610, "2D  No surprises, no pressure"),
        (682, "2E  YOU choose the car"), (735, "2F  WE bring it to your home")]
tw, th, pad, cap = 405, 720, 22, 50
board = Image.new("RGB", (pad + 4 * (tw + pad), 80 + 2 * (th + cap + pad)), WHITE)
bd = ImageDraw.Draw(board)
bd.text((pad, 22), "Monsoor Motors  |  CEO intro  |  3D previs storyboard v3 (2 shots, 32 s)", font=font(26), fill=NAVY)
for i, (n, label) in enumerate(keys):
    x = pad + (i % 4) * (tw + pad)
    y = 80 + (i // 4) * (th + cap + pad)
    board.paste(annotate(Image.open(frame_path(n)), n).resize((tw, th), Image.LANCZOS), (x, y))
    bd.text((x, y + th + 12), label, font=font(19, "SemiBold"), fill=NAVY)
board.save(os.path.join(OUT, "CEO-Intro-Storyboard.png"))

# Floor plan (top view). 1 m = 62 px. Camera at the bottom, showroom at the top.
S, W, H = 62, 1000, 1180
ox, oy = W // 2, 800
plan = Image.new("RGB", (W, H), WHITE)
p = ImageDraw.Draw(plan)


def pt(x, y):
    return (ox + x * S, oy - y * S)


def arrowhead(a, b, col, width=4):
    ang = math.atan2(-(b[1] - a[1]), b[0] - a[0])
    bx, by = pt(*b)
    for da in (2.6, -2.6):
        p.line([(bx, by), (bx + 16 * math.cos(ang + da), by + 16 * math.sin(ang + da))], fill=col, width=width)


def path(points, col, width=4):
    p.line([pt(*q) for q in points], fill=col, width=width, joint="curve")
    arrowhead(points[-2], points[-1], col, width)


def rect(cx, cy, w, l, rot, fill, outline=(60, 60, 60)):
    c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = [(cx + x * c - y * s_, cy + x * s_ + y * c) for x, y in [(-w / 2, -l / 2), (w / 2, -l / 2), (w / 2, l / 2), (-w / 2, l / 2)]]
    p.polygon([pt(*q) for q in pts], fill=fill, outline=outline)


for gx in range(-8, 9):
    p.line([pt(gx, -6), pt(gx, 11)], fill=(228, 228, 228))
for gy in range(-6, 12):
    p.line([pt(-8, gy), pt(8, gy)], fill=(228, 228, 228))
p.text((24, 18), "Floor plan v3 (top view)  |  grid = 1 m", font=font(24), fill=NAVY)
rect(0, 10.6, 15, 1.2, 0, NAVY)
p.text(pt(-3.6, 10.85), "Showroom: glass front + MONSOOR MOTORS sign", font=font(15, "SemiBold"), fill=WHITE)
for cx, cy, col in [(-3.0, 6.3, (138, 31, 36)), (-5.6, 6.3, (225, 228, 232)), (2.6, 6.6, (35, 64, 107)), (5.4, 6.6, (42, 44, 48))]:
    rect(cx, cy, 1.8, 4.36, 0, col)
p.text(pt(-6.5, 8.95), "Stock cars in the bays", font=font(14, "SemiBold"), fill=(40, 40, 40))
rect(0.35, 3.5, 2.6, 5.2, -62, (15, 39, 71))
rect(0.35, 3.5, 1.8, 4.36, -62, (185, 190, 198))
p.text(pt(2.7, 3.2), "Hero C-HR on\nnavy plinth", font=font(14, "SemiBold"), fill=(40, 40, 40))
for x, col in ((-3.1, NAVY), (3.9, ORANGE)):
    rect(x, 2.2, 0.6, 0.12, 0, col)
p.text(pt(-4.9, 2.05), "banner", font=font(12, "Medium"), fill=(60, 60, 60))
p.text(pt(4.35, 2.05), "banner", font=font(12, "Medium"), fill=(60, 60, 60))


def who(xy, col, label, dx, dy=-9):
    x, y = pt(*xy)
    p.ellipse([x - 15, y - 15, x + 15, y + 15], fill=col, outline=(20, 20, 20))
    p.text((x + dx, y + dy), label, font=font(15, "SemiBold"), fill=(20, 20, 20))


who((-0.40, 0.0), NAVY, "Monsoor (stays)", -150)
who((0.40, 0.10), (30, 30, 30), "Arfan (stays on his mark)", 24, -26)


def cam(xy, col, label, dx=20, dy=-8):
    x, y = pt(*xy)
    p.polygon([(x, y - 16), (x - 14, y + 12), (x + 14, y + 12)], fill=col)
    p.text((x + dx, y + dy), label, font=font(15, "SemiBold"), fill=col)


cam((-0.10, -3.75), ORANGE, "Cam 1, 35 mm", dx=-140)
path([(-0.10, -3.6), (-0.04, -3.15)], ORANGE)
cam((0.20, -4.10), TEAL, "Cam 2 start, 50 mm", dx=14, dy=14)
path([(0.20, -4.10), (0.55, -3.90), (1.05, -3.45), (1.55, -3.00), (1.42, -2.65), (1.10, -1.75)], TEAL)
p.text(pt(1.75, -2.75), "trucks to Arfan's side", font=font(14, "SemiBold"), fill=TEAL)
p.text(pt(1.3, -1.55), "ends low, medium close-up", font=font(14, "SemiBold"), fill=TEAL)
p.text((24, H - 84), "Orange: shot 1 camera, slow push-in at eye level (1.5 m).", font=font(16, "Medium"), fill=ORANGE)
p.text((24, H - 56), "Teal: shot 2 camera. Nobody walks; the camera does the moving.", font=font(16, "Medium"), fill=TEAL)
plan.save(os.path.join(OUT, "CEO-Intro-Floorplan.png"))
print("done")
