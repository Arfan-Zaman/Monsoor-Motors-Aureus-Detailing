import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = "/Users/mdarfanuzzaman/Documents/Monsoor Motors"
FONT = f"{ROOT}/Brand Kit/00 Fonts/Montserrat-Variable.ttf"
LOGO = f"{ROOT}/Brand Kit/01 Logo/Monsoor-Logo-Horizontal-White.png"
NAVY, ORANGE, WHITE = (15, 39, 71), (255, 95, 21), (247, 245, 242)
S = 2048
L, R = 110, S - 110


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight])
    return f


def build(src, dst, hook_white, hook_orange, chips):
    im = Image.open(src).convert("RGB").resize((S, S), Image.LANCZOS)

    # navy fade over the bottom
    fade = Image.new("L", (S, S), 0)
    fd = ImageDraw.Draw(fade)
    for y in range(1400, S):
        t = min(1.0, (y - 1400) / 180)
        fd.line([(0, y), (S, y)], fill=int(255 * 0.94 * t))
    im = Image.composite(Image.new("RGB", (S, S), NAVY), im, fade)
    d = ImageDraw.Draw(im)

    # hook
    size = 104
    f = font(size, 800)
    while d.textlength(hook_white + hook_orange, font=f) > R - L:
        size -= 1
        f = font(size, 800)
    d.text((L, 1548), hook_white, font=f, fill=WHITE)
    d.text((L + d.textlength(hook_white, font=f), 1548), hook_orange, font=f, fill=ORANGE)

    # model line
    d.text((L, 1690), "2010 Volkswagen Golf 90 TSI Trendline  ·  Automatic Wagon",
           font=font(50, 600), fill=WHITE)

    # chips
    f = font(34, 700)
    x, y, h, pad, gap, track = L, 1786, 72, 28, 22, 2
    for c in chips:
        w = sum(d.textlength(ch, font=f) + track for ch in c) - track
        d.rounded_rectangle([x, y, x + w + 2 * pad, y + h], radius=h // 2, outline=WHITE, width=3)
        cx = x + pad
        for ch in c:
            d.text((cx, y + h / 2), ch, font=f, fill=WHITE, anchor="lm")
            cx += d.textlength(ch, font=f) + track
        x += w + 2 * pad + gap

    # divider
    d.line([(L, 1908), (R, 1908)], fill=(*WHITE,), width=2)

    # logo
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.resize((round(logo.width * 96 / logo.height), 96), Image.LANCZOS)
    im.paste(logo, (L, 1932), logo)

    # contact
    d.text((R, 1928), "Call 0434 137 393", font=font(40, 700), fill=WHITE, anchor="ra")
    d.text((R, 1986), "Your local Perth car dealer  ·  530 Albany Hwy, Victoria Park",
           font=font(34, 400), fill=WHITE, anchor="ra")
    im.save(dst)


ADS = {
    "ref": ("Affordable. Practical. ", "Economical.", ["2010 (MY11)", "AUTOMATIC", "203,358 KM", "REGO TO 01/02/2027"]),
    "01": ("Affordable. Practical. ", "Economical.", ["2010 (MY11)", "AUTOMATIC", "203,358 KM", "REGO TO 01/02/2027"]),
    "02": ("Need extra ", "boot space?", ["4-DOOR WAGON", "SPACIOUS BODY", "PRACTICAL BOOT", "AUTOMATIC"]),
    "03": ("Your daily commute, ", "sorted.", ["1.4L TURBO PETROL", "FUEL-EFFICIENT", "AUTOMATIC", "SILVER"]),
    "ad": ("A great everyday ", "wagon.", ["2010 (MY11)", "UNLEADED PETROL", "203,358 KM", "REGO TO 01/02/2027"]),
}

if __name__ == "__main__":
    mode, src, dst = sys.argv[1:4]
    build(src, dst, *ADS[mode])
