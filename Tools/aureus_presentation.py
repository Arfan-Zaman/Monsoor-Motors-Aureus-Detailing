"""Aureus Detailing: mockups board and one-page usage guide, built from the Final kit PNGs.
Usage: python3 aureus_presentation.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path("/Users/mdarfanuzzaman/Documents/Monsoor Motors")
BRAND = ROOT / "Aureus Detailing"
FIN = BRAND / "02 Logo"
P, I, M = FIN / "PNG", FIN / "Icons", BRAND / "03 Mockups"
GUIDE = BRAND / "01 Brand Guidelines"
M.mkdir(exist_ok=True)
FONT = str(ROOT / "Brand Kit/00 Fonts/Montserrat-Variable.ttf")
NAVY, AQUA, PINK, ICE = (7, 26, 51), (0, 168, 168), (255, 77, 141), (245, 248, 252)
GREY, LINE, PAGE = (110, 116, 128), (225, 228, 233), (238, 241, 245)
PHONE, ADDRESS = "0434 13 73 93", "530 Albany Hwy, Victoria Park WA"


def font(sz, w=400):
    f = ImageFont.truetype(FONT, sz)
    f.set_variation_by_axes([w])
    return f


def img(name, box):
    im = Image.open(name).convert("RGBA")
    im.thumbnail(box, Image.LANCZOS)
    return im


def rounded(size, r, fill):
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=fill)
    return im


def drop(canvas, im, xy, r=28, blur=26, alpha=70):
    sh = Image.new("RGBA", (im.width + blur * 4, im.height + blur * 4), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((blur * 2, blur * 2, blur * 2 + im.width, blur * 2 + im.height), r,
                                         fill=(7, 26, 51, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh, (xy[0] - blur * 2 + 6, xy[1] - blur * 2 + 16))
    canvas.alpha_composite(im, xy)


def mockups():
    W, H = 2400, 1780
    c = Image.new("RGBA", (W, H), PAGE + (255,))
    d = ImageDraw.Draw(c)
    d.text((80, 56), "Aureus Detailing  ·  logo in use", font=font(44, 600), fill=NAVY)
    d.text((80, 118), "Instagram, business cards, website and uniform patch", font=font(27), fill=GREY)

    # 1. Instagram profile on a phone
    ph = rounded((560, 1120), 60, NAVY + (255,))
    scr = rounded((520, 1080), 44, (255, 255, 255, 255))
    sd = ImageDraw.Draw(scr)
    av = img(I / "social-profile-1080.png", (170, 170)).convert("RGBA")
    mk = Image.new("L", av.size, 0); ImageDraw.Draw(mk).ellipse((0, 0, av.width - 1, av.height - 1), fill=255)
    av.putalpha(mk)
    sd.text((30, 40), "aureus.detailing", font=font(28, 600), fill=NAVY)
    scr.alpha_composite(av, (30, 100))
    for k, (n, lbl) in enumerate([("48", "posts"), ("2,140", "followers"), ("312", "following")]):
        sd.text((250 + k * 92, 140), n, font=font(26, 600), fill=NAVY, anchor="mm")
        sd.text((250 + k * 92, 172), lbl, font=font(17), fill=GREY, anchor="mm")
    sd.text((30, 300), "Aureus Detailing", font=font(23, 600), fill=NAVY)
    for k, t in enumerate(["Mobile and workshop car detailing, Perth", "We come to you  ·  Victoria Park workshop",
                           "by Monsoor Motors"]):
        sd.text((30, 336 + k * 32), t, font=font(19), fill=(60, 66, 80))
    sd.rounded_rectangle((30, 450, 490, 510), 14, fill=PINK)
    sd.text((260, 480), "Book now", font=font(23, 600), fill=NAVY, anchor="mm")
    tile = img(I / "icon-512.png", (150, 150))
    for k in range(9):
        x, y = 15 + (k % 3) * 165, 540 + (k // 3) * 165
        scr.alpha_composite(tile, (x, y)) if k in (0, 4, 8) else sd.rectangle((x, y, x + 150, y + 150),
                                                                              fill=[(214, 222, 232), (190, 202, 216), (226, 232, 239)][k % 3])
    ph.alpha_composite(scr, (20, 20))
    drop(c, ph, (90, 200), r=60)

    # 2. business cards (front navy with 3D chrome, back white with flat colour lockup)
    front = rounded((760, 434), 22, NAVY + (255,))
    sym = img(P / "aureus-stacked-3d-chrome.png", (420, 330))
    front.alpha_composite(sym, ((760 - sym.width) // 2, (434 - sym.height) // 2))
    back = rounded((760, 434), 22, (255, 255, 255, 255))
    bd = ImageDraw.Draw(back)
    lk = img(P / "aureus-horizontal-flat-color.png", (420, 110))
    back.alpha_composite(lk, (50, 60))
    bd.line((50, 210, 710, 210), fill=LINE, width=2)
    bd.text((50, 240), "Mobile and workshop car detailing", font=font(22, 600), fill=NAVY)
    bd.text((50, 285), PHONE, font=font(24, 600), fill=NAVY)
    bd.text((50, 325), ADDRESS, font=font(20), fill=GREY)
    bd.rounded_rectangle((540, 330, 710, 380), 25, fill=PINK)
    bd.text((625, 355), "Book now", font=font(19, 600), fill=NAVY, anchor="mm")
    drop(c, front, (760, 220), r=22)
    drop(c, back, (1560, 220), r=22)

    # 3. website header
    web = rounded((1560, 560), 22, NAVY + (255,))
    wd = ImageDraw.Draw(web)
    wd.rectangle((0, 0, 1560, 40), fill=(225, 230, 237))
    for k, col in enumerate([(255, 95, 87), (255, 189, 46), (40, 200, 64)]):
        wd.ellipse((18 + k * 26, 12, 34 + k * 26, 28), fill=col)
    nav = img(P / "aureus-horizontal-flat-reverse.png", (260, 70))
    web.alpha_composite(nav, (50, 70))
    for k, t in enumerate(["Packages", "Mobile service", "Workshop", "Gallery"]):
        wd.text((760 + k * 160, 105), t, font=font(20, 500), fill=ICE, anchor="mm")
    wd.rounded_rectangle((1370, 80, 1520, 130), 25, fill=PINK)
    wd.text((1445, 105), "Book now", font=font(19, 600), fill=NAVY, anchor="mm")
    wd.text((70, 230), "Detailing, perfected.", font=font(62, 600), fill=ICE)
    wd.text((72, 320), "We come to you, or drop off at our Victoria Park workshop.", font=font(24), fill=(170, 182, 200))
    wd.rounded_rectangle((72, 390, 330, 450), 30, fill=PINK)
    wd.text((201, 420), "Book a detail", font=font(22, 600), fill=NAVY, anchor="mm")
    wd.rounded_rectangle((350, 390, 560, 450), 30, outline=AQUA, width=3)
    wd.text((455, 420), "View packages", font=font(20, 600), fill=AQUA, anchor="mm")
    big = img(P / "aureus-symbol-3d-chrome.png", (400, 400))
    web.alpha_composite(big, (1060, 150))
    drop(c, web, (760, 740), r=22)

    # 4. embroidered patch (flat reverse: navy, white, aqua, pink thread)
    patch = Image.new("RGBA", (330, 330), (0, 0, 0, 0))
    pd = ImageDraw.Draw(patch)
    pd.ellipse((0, 0, 329, 329), fill=NAVY)
    import math
    for k in range(72):
        a0 = k * 5 * math.pi / 180
        pd.arc((14, 14, 315, 315), k * 5, k * 5 + 3, fill=AQUA, width=4)
    ps = img(P / "aureus-symbol-flat-reverse.png", (230, 230))
    patch.alpha_composite(ps, ((330 - ps.width) // 2, (330 - ps.height) // 2 + 6))
    drop(c, patch, (780, 1380), r=165, blur=20)
    d.text((1150, 1510), "Uniform patch", font=font(24, 600), fill=NAVY)
    d.text((1150, 1546), "Flat version: four thread colours (navy, white, aqua, pink)", font=font(20), fill=GREY)
    c.convert("RGB").save(M / "Aureus-Mockups.png")


def usage_guide():
    W, H = 2400, 2000
    c = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(c)
    d.text((80, 56), "Aureus Detailing  ·  logo usage guide", font=font(44, 600), fill=NAVY)
    d.text((80, 118), "One page: which version to use, spacing, sizes, colours and what to avoid", font=font(27), fill=GREY)

    # which version
    d.text((80, 200), "Which version", font=font(30, 600), fill=NAVY)
    rows = [("aureus-horizontal-3d-chrome.png", NAVY, "3D chrome  ·  hero", "Van, signage, Instagram, website, print on navy"),
            ("aureus-horizontal-3d-navy.png", (255, 255, 255), "3D navy", "Hero use on white or light backgrounds"),
            ("aureus-horizontal-flat-color.png", (255, 255, 255), "Flat colour", "Invoices, forms, small print, light backgrounds"),
            ("aureus-horizontal-flat-reverse.png", NAVY, "Flat reverse", "Embroidery, vinyl, small print on navy"),
            ("aureus-horizontal-flat-black.png", (255, 255, 255), "Black / white", "One-colour printing, stamps, engraving")]
    for k, (f, bg, name, use) in enumerate(rows):
        y = 260 + k * 150
        d.rounded_rectangle((80, y, 560, y + 130), 14, fill=bg, outline=LINE, width=2)
        lk = img(P / f, (430, 110))
        c.alpha_composite(lk, (80 + (480 - lk.width) // 2, y + (130 - lk.height) // 2))
        d.text((590, y + 34), name, font=font(25, 600), fill=NAVY)
        d.text((590, y + 74), use, font=font(21), fill=GREY)

    # clear space + minimum sizes
    x0 = 1300
    d.text((x0, 200), "Clear space", font=font(30, 600), fill=NAVY)
    box = rounded((900, 330), 14, (247, 249, 252, 255))
    c.alpha_composite(box, (x0, 260))
    lk = img(P / "aureus-horizontal-flat-color.png", (560, 150))
    lx, ly = x0 + (900 - lk.width) // 2, 260 + (330 - lk.height) // 2
    c.alpha_composite(lk, (lx, ly))
    g = 70
    for k in range(0, lk.width + 2 * g, 18):
        d.line((lx - g + k, ly - g, lx - g + min(k + 9, lk.width + 2 * g), ly - g), fill=PINK, width=3)
        d.line((lx - g + k, ly + lk.height + g, lx - g + min(k + 9, lk.width + 2 * g), ly + lk.height + g), fill=PINK, width=3)
    for k in range(0, lk.height + 2 * g, 18):
        d.line((lx - g, ly - g + k, lx - g, ly - g + min(k + 9, lk.height + 2 * g)), fill=PINK, width=3)
        d.line((lx + lk.width + g, ly - g + k, lx + lk.width + g, ly - g + min(k + 9, lk.height + 2 * g)), fill=PINK, width=3)
    d.text((x0, 610), "Keep a margin at least the height of the AUREUS letters on every side.", font=font(21), fill=GREY)
    d.text((x0, 680), "Minimum sizes", font=font(30, 600), fill=NAVY)
    for k, t in enumerate(["3D symbol: 32 px on screen / 12 mm in print",
                           "Flat symbol: 24 px / 8 mm",
                           "Below 24 px (favicons): use the small-size symbol",
                           "Horizontal logo: 140 px / 35 mm wide"]):
        d.text((x0, 740 + k * 40), "·  " + t, font=font(22), fill=NAVY)

    # colours
    y0 = 1060
    d.text((80, y0), "Colours", font=font(30, 600), fill=NAVY)
    cols = [("Deep navy", "#071A33", "about 60%: backgrounds, van, uniforms"),
            ("Deep aqua", "#00A8A8", "about 30%: reflection, highlights"),
            ("Hot pink", "#FF4D8D", "about 10%: logo cap, Book now, prices"),
            ("Ice white", "#F5F8FC", "text and logo on navy")]
    for k, (n, hx, use) in enumerate(cols):
        x = 80 + k * 560
        rgb = tuple(int(hx[i:i + 2], 16) for i in (1, 3, 5))
        kk = 1 - max(rgb) / 255
        cmyk = [0, 0, 0, round(kk * 100)] if kk == 1 else [round((1 - v / 255 - kk) / (1 - kk) * 100) for v in rgb] + [round(kk * 100)]
        d.rounded_rectangle((x, y0 + 60, x + 520, y0 + 200), 16, fill=rgb, outline=LINE, width=2)
        d.text((x, y0 + 220), n, font=font(25, 600), fill=NAVY)
        d.text((x, y0 + 258), f"HEX {hx}   RGB {rgb[0]} {rgb[1]} {rgb[2]}", font=font(20), fill=GREY)
        d.text((x, y0 + 290), f"CMYK approx. {cmyk[0]} {cmyk[1]} {cmyk[2]} {cmyk[3]}", font=font(20), fill=GREY)
        d.text((x, y0 + 322), use, font=font(20), fill=GREY)

    # don'ts
    y1 = 1470
    d.text((80, y1), "Avoid", font=font(30, 600), fill=NAVY)
    base = img(P / "aureus-symbol-flat-color.png", (200, 200))
    donts = []
    donts.append((base.resize((280, 170)), "Don't stretch or squash"))
    rec = base.copy(); px = rec.load()
    for yy in range(rec.height):
        for xx in range(rec.width):
            r_, g_, b_, a_ = px[xx, yy]
            if a_ and r_ < 40 and b_ < 80:
                px[xx, yy] = (255, 77, 141, a_)
    donts.append((rec, "Don't recolour the A"))
    glow = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
    sh = base.copy(); sh = Image.composite(Image.new("RGBA", sh.size, (0, 0, 0, 160)), Image.new("RGBA", sh.size, (0, 0, 0, 0)), sh.split()[3])
    glow.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (28, 30)); glow.alpha_composite(base, (20, 20))
    donts.append((glow, "Don't add shadows or glows"))
    busy = Image.new("RGBA", (240, 200), (0, 0, 0, 255))
    bd = ImageDraw.Draw(busy)
    for k in range(0, 240, 24):
        bd.rectangle((k, 0, k + 12, 200), fill=(200, 60, 40)); bd.rectangle((0, k, 240, k + 8), fill=(240, 200, 60))
    t3 = img(P / "aureus-symbol-3d-navy.png", (170, 170)); busy.alpha_composite(t3, (35, 15))
    donts.append((busy, "Don't place on busy photos"))
    sm = img(P / "aureus-symbol-3d-chrome.png", (22, 22))
    tiny = Image.new("RGBA", (240, 200), NAVY + (255,)); tiny.alpha_composite(sm, (109, 89))
    donts.append((tiny, "Don't use 3D below 32 px"))
    for k, (im, t) in enumerate(donts):
        x = 80 + k * 460
        d.rounded_rectangle((x, y1 + 60, x + 420, y1 + 330), 16, fill=(250, 251, 252), outline=LINE, width=2)
        c.alpha_composite(im, (x + (420 - im.width) // 2, y1 + 60 + (270 - im.height) // 2))
        d.line((x + 20, y1 + 80, x + 60, y1 + 120), fill=PINK, width=6); d.line((x + 60, y1 + 80, x + 20, y1 + 120), fill=PINK, width=6)
        d.text((x, y1 + 350), t, font=font(22, 500), fill=NAVY)
    c.convert("RGB").save(GUIDE / "Aureus-Logo-Usage-Guide.png")


if __name__ == "__main__":
    mockups()
    usage_guide()
    print("ok")
