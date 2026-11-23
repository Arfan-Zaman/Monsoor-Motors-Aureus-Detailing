"""Animated storyboard SHEET (one page, 16 looping panels). Free: PIL only, 0 credits.

Run:  /opt/miniconda3/bin/python -I make_sheet.py
Out:  panels/shot-01.webp … shot-16.webp  +  Hybrid-Clone-Storyboard.html (open in a browser)
"""
import html, os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_animatic as A  # reuses the shot list and drawing code

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "panels")
NF = 30  # frames per panel loop
PW, PH = 360, 450  # panel size (picture area, half scale)


def panel_frames(i):
    dur, _, _, _, _ = A.SHOTS[i]
    start = sum(s[0] for s in A.SHOTS[:i])
    frames = []
    for k in range(NF):
        t = k / (NF - 1)
        im = A.frame(i, t, start + t * dur)
        frames.append(im.crop((0, A.TOP, A.W, A.BOT)).resize((PW, PH), Image.LANCZOS))
    return frames, int(dur * 1000 / NF)


def main():
    os.makedirs(OUT, exist_ok=True)
    cards = []
    for i, (dur, direction, says, caption, kind) in enumerate(A.SHOTS):
        frames, ms = panel_frames(i)
        name = f"shot-{i + 1:02d}.webp"
        frames[0].save(os.path.join(OUT, name), save_all=True, append_images=frames[1:], duration=ms, loop=0,
                       quality=80, method=4)
        start = sum(s[0] for s in A.SHOTS[:i])
        cards.append(f"""
      <article class="card">
        <div class="frame"><img src="panels/{name}" alt="Shot {i + 1}: {html.escape(direction)}" loading="lazy"></div>
        <div class="meta"><span class="num">{i + 1:02d}</span><span class="time">{start:.1f}–{start + dur:.1f} s</span></div>
        <h3>{html.escape(direction)}</h3>
        <p class="says">“{html.escape(says)}”</p>
        <p class="cap"><span>On screen</span>{html.escape(caption)}</p>
      </article>""")
        print("panel", i + 1, "done", flush=True)

    total = sum(s[0] for s in A.SHOTS)
    page = f"""<title>Hybrid Ad Storyboard</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&display=swap" rel="stylesheet">
<style>
/* Layout: dark yard-at-night sheet, a grid of 9:16-style cards, read left to right in shot order. Single dark look on purpose. */
:root{{--navy:#0F2747;--ink:#081222;--orange:#FF5F15;--white:#F7F5F2;--slate:#8C96A5;--card:#12284A;--line:#1d3a63;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));background:var(--ink);color:var(--white);font-family:Montserrat,system-ui,sans-serif}}
header{{padding-block:28px 8px;max-width:1560px;margin:auto}}
h1{{margin:0;font-size:clamp(22px,3vw,34px);font-weight:900}}
h1 em{{color:var(--orange);font-style:normal}}
.sub{{color:var(--slate);font-size:14px;margin:6px 0 0;line-height:1.5}}
.legend{{display:flex;gap:18px;flex-wrap:wrap;margin:14px 0 0;font-size:13px;color:var(--slate)}}
.legend b{{color:var(--white)}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(260px,100%),1fr));gap:18px;padding-block:18px 40px;max-width:1560px;margin:auto}}
.card{{background:var(--card);border-radius:14px;overflow:hidden;border:1px solid var(--line)}}
.frame{{aspect-ratio:4/5;max-width:100%;background:var(--ink)}}
.frame img{{width:100%;height:100%;display:block;object-fit:cover}}
.meta{{display:flex;justify-content:space-between;align-items:center;padding:10px 14px 0}}
.num{{font-weight:900;font-size:22px;color:var(--orange)}}
.time{{font-size:12px;color:var(--slate);font-weight:700}}
h3{{margin:4px 14px 6px;font-size:15px;font-weight:800;line-height:1.3}}
.says{{margin:0 14px 8px;font-size:13px;line-height:1.45;color:var(--white);opacity:.85}}
.cap{{margin:0 14px 14px;font-size:13px;font-weight:800}}
.cap span{{display:inline-block;margin-right:8px;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--navy);background:var(--orange);padding:2px 6px;border-radius:4px}}
footer{{max-width:1560px;margin:auto;padding-block:0 40px;color:var(--slate);font-size:12px;line-height:1.6}}
h1{{text-wrap:balance}}
</style>
<header>
  <h1>Perth, want a Japanese hybrid? <em>Animated storyboard</em></h1>
  <p class="sub">16 shots · {total:.0f} s · 9:16 Reel · Monsoor on camera · our yard, our cars, our script. Each panel loops its own shot at real speed.</p>
  <div class="legend"><span><b>Orange notes</b> = camera direction</span><span><b>[brackets]</b> = fill with real data on the day</span><span><b>Grey cars</b> = film our real hybrid here</span><span><b>Credits used:</b> 0</span></div>
</header>
<main>{''.join(cards)}
</main>
<footer>End card: Monsoor Motors logo · 0434 137 393 · 530 Albany Hwy, Victoria Park · MV Dealership Licence MD32748. Any car shown with a price also needs its year, rego and cash price. Map, labels and icons are drawn in code (no AI). Real photos: Toyota C-HR Hybrid (black) from Cars/.</footer>"""
    with open(os.path.join(HERE, "Hybrid-Clone-Storyboard.html"), "w") as f:
        f.write(page)
    print("sheet written")


if __name__ == "__main__":
    main()
