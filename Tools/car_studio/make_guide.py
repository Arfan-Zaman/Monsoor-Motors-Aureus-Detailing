"""One-page printable shooting guide for the Monsoor Studio system (A4 PDF + PNG).

  /opt/miniconda3/bin/python -I make_guide.py <out folder>
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "assets", "Montserrat-Variable.ttf")
LOGO = os.path.join(HERE, "assets", "Monsoor-Logo-Horizontal-White.png")
NAVY, ORANGE, INK, GREY = (15, 39, 71), (255, 95, 21), (27, 31, 36), (120, 126, 134)
W, H = 1654, 2339  # A4 at 200 dpi


def f(size, weight=500):
    ft = ImageFont.truetype(FONT, size)
    try:
        ft.set_variation_by_axes([weight])
    except Exception:
        pass
    return ft


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    # header band
    d.rectangle([0, 0, W, 210], fill=NAVY)
    d.rectangle([0, 210, W, 222], fill=ORANGE)
    if os.path.exists(LOGO):
        lg = Image.open(LOGO).convert("RGBA"); lg.thumbnail((430, 110))
        im.paste(lg, (W - lg.width - 80, 55), lg)
    d.text((80, 50), "Monsoor Studio", font=f(68, 800), fill="white")
    d.text((80, 135), "How to shoot every car, the same way every time", font=f(34, 500), fill=(220, 226, 235))

    # diagram: circle, car, 36 marks, 5 still positions
    cx, cy, R = 420, 720, 290
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=GREY, width=4)
    for i in range(36):
        a = math.radians(i * 10)
        x, y = cx + R * math.sin(a), cy - R * math.cos(a)
        r = 9 if i % 9 else 14
        d.ellipse([x - r, y - r, x + r, y + r], fill=ORANGE if i % 9 == 0 else GREY)
    # car (front pointing up)
    d.rounded_rectangle([cx - 62, cy - 150, cx + 62, cy + 150], radius=40, fill=(200, 205, 212), outline=INK, width=3)
    d.rounded_rectangle([cx - 48, cy - 95, cx + 48, cy - 40], radius=12, fill=(120, 140, 160))
    d.text((cx, cy - 175), "FRONT", font=f(24, 700), fill=INK, anchor="ms")
    stills = [(0, "1  Front 0°"), (40, "2  Front ¾ 40°"), (90, "3  Side 90°"), (140, "4  Rear ¾ 140°"), (180, "5  Rear 180°")]
    for ang, lab in stills:
        a = math.radians(ang)
        x, y = cx + (R + 34) * math.sin(a), cy - (R + 34) * math.cos(a)
        d.rectangle([x - 16, y - 12, x + 16, y + 12], fill=NAVY)
        tx, ty = cx + (R + 70) * math.sin(a), cy - (R + 70) * math.cos(a)
        anchor = "lm" if math.sin(a) > 0.3 else ("mm" if abs(math.sin(a)) <= 0.3 else "rm")
        if ang == 0: ty -= 10
        if ang == 180: ty += 14
        d.text((tx, ty), lab, font=f(26, 700), fill=NAVY, anchor=anchor)
    for k, line in enumerate(["Rope 6 m from the car's centre", "36 chalk marks, 1.05 m apart (every 10°)",
                              "Walk clockwise, starting at the front mark"]):
        d.text((cx, cy + R + 150 + k * 36), line, font=f(24, 500), fill=GREY, anchor="ms")

    # right column: kit + phone settings
    x0, y = 1010, 300
    def head(t):
        nonlocal y
        d.text((x0, y), t, font=f(36, 800), fill=NAVY); y += 54
    def items(lst, width=600):
        nonlocal y
        for t in lst:
            ls = wrap(d, t, f(26, 500), width - 30)
            d.ellipse([x0 + 2, y + 11, x0 + 14, y + 23], fill=ORANGE)
            for k, l in enumerate(ls):
                d.text((x0 + 30, y), l, font=f(26, 500), fill=INK); y += 36
            y += 8
        y += 18
    head("Kit")
    items(["Phone (the same phone every time)", "Monopod or tripod marked at 1.0 m",
           "Rope with a knot at 6 m, chalk, tape measure", "Microfibre cloth"])
    head("Phone settings")
    items(["2x lens, landscape, grid on", "HDR on, flash off, no beauty/AI filters",
           "Tap and hold on the car to lock focus and exposure", "Camera at 1.0 m, pointing level at the middle of the car"])

    # bottom: the steps
    y = 1300
    d.line([80, y - 30, W - 80, y - 30], fill=(225, 228, 232), width=3)
    x0 = 80
    head("Every car, in this order")
    steps = [
        ("Prepare", "Wash or wipe the car. Windows up, doors shut, wheels straight, interior tidy, nothing on the dash. Park the centre of the car on the marked spot, nose to the front mark. Shade or a cloudy sky is best; avoid noon sun and people in shot."),
        ("5 studio stills", "Stand on marks 1-5 above. Whole car in frame with space around it; don't cut off bumpers or mirrors. These become the feed posts."),
        ("36-photo spin", "From the front mark, one photo on every chalk mark, walking clockwise. Keep the car in the middle of the screen and the monopod at 1.0 m. Put them in the car folder under spin/."),
        ("Interior", "Dashboard wide, centre console, gauges with the engine on (shows the km), front seats, rear seats, boot, sunroof. With a 360 camera: one shot from between the front seats."),
        ("Honest flaws", "Every scratch, dent, worn seat, chip: one close-up from about 1 m and one wider shot showing where it is. We mark these on the 360 page."),
        ("Hand over", "Copy the folder to Cars/<Year Make Model>/ and fill car.yaml (year, model, km, price, rego). Then run car_studio.py."),
    ]
    for n, (t, body) in enumerate(steps, 1):
        d.ellipse([x0, y, x0 + 52, y + 52], fill=NAVY)
        d.text((x0 + 26, y + 26), str(n), font=f(28, 800), fill="white", anchor="mm")
        d.text((x0 + 76, y + 6), t, font=f(30, 800), fill=INK)
        yy = y + 48
        for l in wrap(d, body, f(25, 500), W - 160 - 76):
            d.text((x0 + 76, yy), l, font=f(25, 500), fill=(60, 66, 74)); yy += 34
        y = yy + 22

    d.rectangle([0, H - 90, W, H], fill=NAVY)
    d.text((80, H - 45), "Monsoor Motors · 530 Albany Highway, Victoria Park · 0434 137 393 · MV Dealer Licence MD32748",
           font=f(24, 500), fill="white", anchor="lm")
    d.text((W // 2, H - 125), "Real car, real photos: the car itself is never edited",
           font=f(26, 700), fill=ORANGE, anchor="mm")

    os.makedirs(out, exist_ok=True)
    png = os.path.join(out, "Monsoor Studio - Shooting Guide.png")
    pdf = os.path.join(out, "Monsoor Studio - Shooting Guide.pdf")
    im.save(png); im.save(pdf, resolution=200)
    print(pdf)


if __name__ == "__main__":
    main()
