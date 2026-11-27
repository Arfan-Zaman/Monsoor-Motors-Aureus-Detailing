"""Build the drag-to-spin 360 viewer page for one car.

  /opt/miniconda3/bin/python -I make_viewer.py <car folder>

Reads <car folder>/Studio/spin/frame_00.jpg ... (made by car_studio.py --spin),
optional hotspots and interior panorama from car.yaml, and writes a single
self-contained folder <car folder>/Studio/viewer/ (index.html + images) that can
be uploaded to the website or opened locally. No paid service, no tracking.

car.yaml extras:
  hotspots:            # honest flaw markers, shown on the spin
    - {frame: 4, x: 0.55, y: 0.62, label: "Driver's headlight lens faded", photo: 20261125_120828.jpg}
  interior_pano: pano_front.jpg   # equirectangular 360 photo (optional)
"""
import glob, html, json, os, shutil, sys
import yaml
from PIL import Image, ImageOps

PAGE = """<!doctype html>
<html lang="en-AU"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Monsoor Motors</title>
{pano_head}
<style>
:root{{--navy:#0F2747;--orange:#FF5F15;--ink:#1b1f24;--bg:#f4f3f1}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Montserrat,system-ui,sans-serif;background:var(--bg);color:var(--ink)}}
.wrap{{max-width:1100px;margin:0 auto;padding:16px}}
.stage{{position:relative;border-radius:14px;overflow:hidden;background:#8a8a8a;touch-action:pan-y;cursor:grab;user-select:none}}
.stage.drag{{cursor:grabbing}}.stage img.frame{{display:block;width:100%;height:auto;pointer-events:none}}
.hint{{position:absolute;top:12px;left:50%;transform:translateX(-50%);color:#fff;font-size:13px;background:rgba(0,0,0,.35);padding:4px 10px;border-radius:20px;transition:opacity .4s}}
.hs{{position:absolute;width:22px;height:22px;margin:-11px 0 0 -11px;border-radius:50%;background:var(--orange);border:3px solid #fff;box-shadow:0 0 0 3px rgba(255,95,21,.35);cursor:pointer;display:none}}
.tabs{{display:flex;gap:8px;margin:12px 0}}.tabs button{{font:inherit;padding:8px 14px;border-radius:20px;border:1px solid #ccc;background:#fff;cursor:pointer}}
.tabs button.on{{background:var(--navy);color:#fff;border-color:var(--navy)}}
.info{{background:#fff;border-radius:14px;padding:18px;margin-top:12px}}h1{{margin:0 0 4px;font-size:24px;color:var(--navy)}}
.chips span{{display:inline-block;margin:6px 6px 0 0;padding:4px 10px;border:1px solid #d6d6d6;border-radius:20px;font-size:13px}}
.flaws li{{margin:6px 0;cursor:pointer}}.flaws li:hover{{color:var(--orange)}}
#pano{{width:100%;height:60vh;border-radius:14px;display:none}}
.modal{{position:fixed;inset:0;background:rgba(0,0,0,.8);display:none;align-items:center;justify-content:center;padding:16px}}
.modal img{{max-width:100%;max-height:80vh;border-radius:8px}}.modal p{{color:#fff;text-align:center}}
footer{{font-size:13px;color:#555;margin:16px 0}}
</style></head><body><div class="wrap">
<div class="tabs"><button class="on" data-t="spin">360° exterior</button>{pano_tab}</div>
<div class="stage" id="stage"><img class="frame" id="frame" alt="{title_attr} in the Monsoor Motors studio">
<div class="hint" id="hint">Drag to spin</div>{hotspots_html}</div>
<div id="pano"></div>
<div class="info"><h1>{title}</h1><div class="chips">{chips}</div>
{flaws_html}</div>
<footer>Monsoor Motors · 530 Albany Highway, Victoria Park WA 6100 · 0434 137 393 · MV Dealer Licence MD32748<br>
Photos are of this exact car. Background is our studio; the car itself is not edited.</footer></div>
<div class="modal" id="modal"><div><img id="mimg" alt=""><p id="mtxt"></p></div></div>
<script>
const frames={frames};const hs={hotspots};
const img=document.getElementById('frame'),stage=document.getElementById('stage');
frames.forEach(s=>{{const i=new Image();i.src=s}});
let cur=0,startX=0,startF=0,drag=false;
function show(n){{cur=((n%frames.length)+frames.length)%frames.length;img.src=frames[cur];
 document.querySelectorAll('.hs').forEach(e=>{{e.style.display=(+e.dataset.f===cur)?'block':'none'}})}}
show(0);
const px=e=>(e.touches?e.touches[0].clientX:e.clientX);
function down(e){{drag=true;startX=px(e);startF=cur;stage.classList.add('drag');document.getElementById('hint').style.opacity=0}}
function move(e){{if(!drag)return;const dx=px(e)-startX;show(startF-Math.round(dx/(stage.clientWidth/frames.length/1.2)))}}
function up(){{drag=false;stage.classList.remove('drag')}}
stage.addEventListener('mousedown',down);addEventListener('mousemove',move);addEventListener('mouseup',up);
stage.addEventListener('touchstart',down,{{passive:true}});stage.addEventListener('touchmove',move,{{passive:true}});stage.addEventListener('touchend',up);
function openHs(i){{const h=hs[i];show(h.frame);if(!h.photo)return;
 document.getElementById('mimg').src=h.photo;document.getElementById('mtxt').textContent=h.label;document.getElementById('modal').style.display='flex'}}
document.querySelectorAll('.hs').forEach(e=>e.addEventListener('click',ev=>{{ev.stopPropagation();openHs(+e.dataset.i)}}));
document.querySelectorAll('.flaws li').forEach(e=>e.addEventListener('click',()=>openHs(+e.dataset.i)));
document.getElementById('modal').onclick=()=>document.getElementById('modal').style.display='none';
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{
 document.querySelectorAll('.tabs button').forEach(x=>x.classList.toggle('on',x===b));
 const p=b.dataset.t==='pano';stage.style.display=p?'none':'block';document.getElementById('pano').style.display=p?'block':'none';
 if(p&&window.pannellum&&!window._pv)window._pv=pannellum.viewer('pano',{{type:'equirectangular',panorama:'{pano}',autoLoad:true}})}});
</script></body></html>
"""


def main():
    folder = sys.argv[1]
    cfg = yaml.safe_load(open(os.path.join(folder, "car.yaml")))
    car = cfg.get("car", {})
    spin = sorted(glob.glob(os.path.join(folder, "Studio", "spin", "frame_*.jpg")))
    if not spin:
        sys.exit("No spin frames yet. Run car_studio.py <folder> --spin first.")
    out = os.path.join(folder, "Studio", "viewer")
    os.makedirs(os.path.join(out, "img"), exist_ok=True)
    frames = []
    for f in spin:
        shutil.copy(f, os.path.join(out, "img", os.path.basename(f)))
        frames.append("img/" + os.path.basename(f))

    hs_list, hs_html, flaws = [], [], []
    for i, h in enumerate(cfg.get("hotspots") or []):
        entry = {"frame": int(h["frame"]), "label": h["label"], "photo": None}
        if h.get("photo"):
            src = os.path.join(folder, h["photo"])
            dst = os.path.join(out, "img", "flaw_%02d.jpg" % i)
            im = ImageOps.exif_transpose(Image.open(src)).convert("RGB"); im.thumbnail((1600, 1600)); im.save(dst, quality=88)
            entry["photo"] = "img/flaw_%02d.jpg" % i
        hs_list.append(entry)
        hs_html.append('<div class="hs" data-i="%d" data-f="%d" style="left:%.1f%%;top:%.1f%%" title="%s"></div>'
                       % (i, entry["frame"], h["x"] * 100, h["y"] * 100, html.escape(h["label"])))
        flaws.append('<li data-i="%d">● %s</li>' % (i, html.escape(h["label"])))
    flaws_html = ('<h3>Honest condition notes</h3><ul class="flaws">%s</ul>' % "".join(flaws)) if flaws else ""

    pano = cfg.get("interior_pano")
    pano_head = pano_tab = ""
    if pano:
        shutil.copy(os.path.join(folder, pano), os.path.join(out, "img", "pano.jpg"))
        pano_head = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pannellum/2.5.6/pannellum.css">'
                     '<script src="https://cdnjs.cloudflare.com/ajax/libs/pannellum/2.5.6/pannellum.js"></script>')
        pano_tab = '<button data-t="pano">360° interior</button>'

    title = " ".join(str(x) for x in (car.get("year"), car.get("make"), car.get("model")) if x)
    chips = []
    if car.get("km"): chips.append(f"{int(car['km']):,} km")
    for k in ("transmission", "colour"):
        if car.get(k): chips.append(str(car[k]))
    if car.get("rego_until"): chips.append(f"Rego to {car['rego_until']}")
    if car.get("price"): chips.append(f"${int(car['price']):,}")
    page = PAGE.format(title=html.escape(title), title_attr=html.escape(title), pano_head=pano_head, pano_tab=pano_tab,
                       hotspots_html="".join(hs_html), chips="".join(f"<span>{html.escape(c)}</span>" for c in chips),
                       flaws_html=flaws_html, frames=json.dumps(frames), hotspots=json.dumps(hs_list),
                       pano="img/pano.jpg")
    open(os.path.join(out, "index.html"), "w").write(page)
    print("viewer:", os.path.join(out, "index.html"))


if __name__ == "__main__":
    main()
