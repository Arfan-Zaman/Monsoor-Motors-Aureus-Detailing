"""Director's canvas: one board with every shot of ad v2 (frame, time, camera, action, line, sound). Run: /opt/miniconda3/bin/python -I make_storyboard.py"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); AUREUS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FONT = os.path.join(AUREUS, "04 Fonts", "Montserrat-Variable.ttf")
def font(s, w="Bold"): f = ImageFont.truetype(FONT, s); f.set_variation_by_name(w); return f
NAVY, AQUA, GLOW, PINK, WHITE, MUTED = (7, 26, 51), (0, 168, 168), (95, 240, 230), (255, 77, 141), (245, 248, 252), (169, 187, 211)
SHOTS = [  # clip or still, seconds in, time, camera, action, line / sound
 ("clips/hook.mp4", 1.0, "0.0–2.4", "Macro, 100 mm, low raking", "Swirls flare in hard sun", '"Swirls. Water spots. Nah."'),
 ("clips/van.mp4", 2.0, "2.4–4.2", "Wide, slow push-in", "The Aureus van rolls in", "Engine settles · whoosh"),
 ("clips/speak3.mp4", 2.5, "4.2–10.2", "Medium, handheld, eye level", "Says it, stern · '20 years' super", '"We come to you... Done properly, or it\'s not done."'),
 ("clips/p1.mp4", 1.0, "10.2–12.7", "Low corner, 35 mm", "POLISH A: polisher", '"Polish first. Then wax. No shortcuts."'),
 ("clips/p2.mp4", 1.0, "12.7–14.8", "Side, waist height", "POLISH B: wax by hand", "DING"),
 ("clips/i1.mp4", 1.0, "14.8–17.1", "Through the cabin", "INTERIOR A: steam", '"Steam. Gets the muck out of the leather."'),
 ("clips/i2.mp4", 1.0, "17.1–18.8", "From the back seat", "INTERIOR B: vents", "DING"),
 ("clips/w1.mp4", 1.0, "18.8–20.8", "Ground level, kneeling", "WHEELS A: spokes", '"Every spoke. By hand."'),
 ("clips/w2.mp4", 1.0, "20.8–22.7", "Wide, backlit by the sun", "WHEELS B: rinse", "DING"),
 ("clips/macro.mp4", 1.5, "22.7–25.0", "Macro, glides across paint", "Shot 1's paint, flawless", '"Yeah. That\'ll do."'),
 ("clips/bell.mp4", 1.5, "25.0–27.5", "Low hero, 50 mm push-in", "Bell tap, rare grin", "BIG DING · 2 h 30 · $199"),
 ("../reel-1/stills/s6-finish.png", 0, "27.5–30.0", "Locked off", "End card: logo + offer", '"Aureus Detailing. Book it."'),
]
TW, TH, COLS, PAD = 300, 534, 6, 28
CW = COLS * TW + (COLS + 1) * PAD; ROWH = TH + 250; CH = 300 + 2 * ROWH + 220
board = Image.new("RGB", (CW, CH), (4, 13, 26)); d = ImageDraw.Draw(board)
d.text((PAD, 40), "AUREUS · AD V2 · DIRECTOR'S BOARD", font=font(54, "ExtraBold"), fill=WHITE)
d.text((PAD, 112), "30 s · 9:16 · 12 shots · the master detailer in every service shot · each service from two angles · real-speed motion", font=font(28, "Medium"), fill=MUTED)
d.text((PAD, 156), "Persona: few words, perfectionist glare, a chrome bell he taps when a step passes, one rare grin.", font=font(26, "Medium"), fill=MUTED)
d.text((PAD, 192), "Look: ARRI Alexa 35, golden hour, one natural filmic grade, fine grain.", font=font(26, "Medium"), fill=MUTED)
d.rectangle([PAD, 238, PAD + 160, 244], fill=AQUA)
tmp = os.path.join(HERE, "build"); os.makedirs(tmp, exist_ok=True)
for k, (src, t, tm, cam, act, line) in enumerate(SHOTS):
    p = os.path.join(HERE, src); fr = os.path.join(tmp, f"sb{k}.png")
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + (["-ss", str(t)] if src.endswith(".mp4") else []) + ["-i", p, "-frames:v", "1", "-vf", f"scale={TW}:{TH}:force_original_aspect_ratio=increase,crop={TW}:{TH}", fr])
    r, c = divmod(k, COLS); x = PAD + c * (TW + PAD); y = 270 + r * ROWH
    if os.path.exists(fr): board.paste(Image.open(fr).convert("RGB"), (x, y))
    d.rounded_rectangle([x + 12, y + 12, x + 74, y + 56], radius=12, fill=NAVY); d.text((x + 43, y + 34), f"{k + 1:02d}", font=font(26, "ExtraBold"), fill=GLOW, anchor="mm")
    ty = y + TH + 16; d.text((x, ty), tm + " s", font=font(26, "Bold"), fill=GLOW)
    d.text((x, ty + 38), cam, font=font(21, "SemiBold"), fill=MUTED)
    d.text((x, ty + 70), act, font=font(22, "Bold"), fill=WHITE)
    col = PINK if "DING" in line else WHITE
    words, lines, cur = line.split(), [], ""
    for w in words:
        if font(22, "Medium").getlength(cur + " " + w) > TW: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur)
    for j, ln in enumerate(lines[:4]): d.text((x, ty + 108 + j * 30), ln, font=font(22, "Medium"), fill=col)
fy = CH - 170
d.text((PAD, fy), "Sound: his voice up front · bell ding = signature sound on every passed step · original 100 bpm score under him · cuts on the beat", font=font(26, "Medium"), fill=WHITE)
d.text((PAD, fy + 44), "Graphics: see-through glass in navy, aqua, pink · 'Step 1–3 of 3' labels · timer to 2 h 30 · price counts to $199 · watermark top left at 50%", font=font(26, "Medium"), fill=WHITE)
d.text((PAD, fy + 88), "Offer: Gold detail $199 · 2 h 30 · at your place · $25 off the first 100 customers · within 20 km of Victoria Park", font=font(26, "Bold"), fill=PINK)
board.save(os.path.join(HERE, "AD-V2-DIRECTOR-BOARD.png")); print(board.size)
