"""Storyboard + script PDF for 'Queue Jump' (free, from the Blender previs frames)."""
import os, sys, textwrap
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qj39_shots import SHOTS, FPS
FR = sys.argv[1]; OUT = sys.argv[2]
FONT = os.path.expanduser("~/Library/Fonts/Montserrat-Variable.ttf")
def F(s, w="Regular"):
    f = ImageFont.truetype(FONT, s)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f
NAVY, ORANGE, INK, GREY = (15, 39, 71), (255, 95, 21), (25, 25, 28), (95, 100, 110)
# per shot: (emotion / performance, dialogue or on-screen text, sound)
S = {
1:("Night, settled, cool. The world is ordinary.","SUPER: Tuesday night. Perth.","Music pulse in. Indicator tick."),
2:("Gen Z guy, bored cool; gum bubble.","","Bubble POP on the cut."),
3:("Readout: AVG 6.8 L/100km · 52,930 km. Needle near E.","","Low-fuel chime."),
4:("Gen Z woman, deadpan 'are you serious'.","","Handheld breathing; idle."),
5:("Readout: AVG 6.3 L/100km · 29,417 km.","","Tick."),
6:("Retiree, hunched, peers over glasses, slow head shake.","","Horn behind him."),
7:("Readout: AVG 6.6 L/100km · 31,206 km.","",""),
8:("Glam driver, cool. Light goes GREEN. Launch.","","V8 roar, tyres bite."),
9:("Speedo climbs just past 60.","","Engine screams."),
10:("Past the 60 sign + speed camera. FLASH.","","Strobe click."),
11:("Her face lit white, sunglasses sliding: busted.","","Music hit."),
12:("Dave, tired, end of a long day. Mia asleep behind.","","Indicator, idle."),
13:("ASX: low-fuel lamp, AVG 7.6 L/100km · 64,812 km.","",""),
14:("SWANLINE servo. Price board static 199.9.","","Fluorescent hum, idles."),
15:("Queue; Dave at pump 2.","","Pump whirr starts."),
16:("Pump 2 rolling toward $78.40.","","Meter ticks."),
17:("Dave: slow exhale, tiny 'of course' smirk.","","Ticks continue."),
18:("Mia asleep, cheek squashed on the glass.","",""),
19:("The just-landed black C-HR glides in. Arfan on a hands-free call (phone in dash cradle), smiling.","ARFAN (hands-free): \"Monsoor, just got the car. Coming.\"","MUSIC CUTS DEAD. Car so quiet the servo hears his call. One cricket."),
20:("Arfan's brown sneaker lands in the puddle.","","Splash. Door clunk; groove returns."),
21:("Arfan: relaxed, a warm genuine smile as he says it, small nod to Dave.","ARFAN: \"What's up?\" (with a smile)","New line in his locked voice (v10 reference)."),
22:("Nozzle into the C-HR.","","Click."),
23:("Pump 1 stops: $36.20 · 18.11 L.","","Auto-shutoff clunk; Dave's pump still whirring."),
24:("Dave still filling, staring over.","",""),
25:("Arfan's finger on POWER (olive Seiko).","","Soft click + gentle chime. No engine."),
26:("READY · 45,012 km · AVG 4.3 L/100km.","SUPER: Over 40% less fuel than his ASX.*",""),
27:("C-HR rear 3/4 pulls away; plate frame readable.","","Near silence."),
28:("Dave's double take as the tail-lights shrink.","","His pump finally clicks off."),
29:("Mia awake: deadpan, then hopeful, eyes up to Dad.","MIA: \"Dad... can we get one?\"","Music: one soft stab."),
30:("NEXT MORNING. SOLD · Dave & Mia tag. Ray-Bans green.","","Magpie, flags."),
31:("Monsoor's black muscle car (MM BOSS) rumbles in.","","The only loud engine in the ad."),
32:("His loafer lands on the brick.","","Engine cuts; the car rocks once."),
33:("Monsoor: warm, proud, unhurried walk over.","","Footsteps."),
34:("His left hand lands on Arfan's right shoulder, one pat.","MONSOOR: \"Good job.\"","Cloned voice; music dips."),
35:("Arfan: humble, eyes then chin down a touch, small smile.","ARFAN: \"That means a lot.\"","Warm swell."),
36:("Golden hour. The C-HR rolls silently into driveway 27.","ARFAN (V.O.): \"You choose the car!\"","Birds, tyres on concrete."),
37:("Arfan walks to Dave, keys palm up.","ARFAN (V.O.): \"We bring it to your home!\"",""),
38:("Key fob (orange MM tag) drops into Dave's palm.","","Jingle."),
39:("Mia runs out across the lawn, pure joy.","","Squeal, footsteps."),
40:("Mia's palms on the door, Dave grinning.","","Music builds."),
41:("Brand card: MONSOOR MOTORS · 0434 137 393 · monsoormotors.com.au","Legal: MD32748 · *Official combined: ASX 2.0 7.6 vs C-HR Hybrid 4.3 L/100km","Music button; chime as sonic logo."),
}
SCENES = {1:"SCENE 1 · RED LIGHTS ACROSS PERTH (night)",12:"SCENE 2 · THE SERVO (night)",19:"SCENE 3 · THE SILENT C-HR (night)",30:"SCENE 4 · NEXT MORNING, THE YARD (day)",36:"SCENE 5 · THE DELIVERY (golden hour)",41:"SCENE 6 · BRAND"}
W, H = 2480, 3508  # A4 portrait at 300 dpi
pages = []
def cover():
    p = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(p)
    d.rectangle([0, 0, W, 520], fill=NAVY)
    d.text((140, 150), "MONSOOR MOTORS", font=F(110, "Bold"), fill="white")
    d.text((140, 300), "'Queue Jump'  ·  39 s Meta/Instagram ad  ·  storyboard + script", font=F(56, "Medium"), fill=(230, 235, 245))
    y = 700
    for line in ["Story: busy Perth night, petrol drivers wince at their fuel readouts; a glam V8 gets busted by a speed camera.",
                 "Dave fills his ASX while Mia sleeps. A just-landed black C-HR Hybrid glides in silently; Arfan, on a hands-free call: \"Monsoor, just got the car. Coming.\" Then to Dave: \"What's up?\" His pump stops first.",
                 "Mia: \"Dad... can we get one?\" Next morning the boss, Monsoor, arrives in his muscle car: \"Good job.\" Arfan: \"That means a lot.\"",
                 "Arfan delivers the black C-HR to Dave's driveway: \"You choose the car! We bring it to your home!\"",
                 "",
                 "Look: GTA VI-trailer mood, filmed as real live action. Humour only from the situation. Locked voices only.",
                 "Frames are grey-box Blender previs (timing, camera, blocking). Final shots use the locked Higgsfield elements."]:
        for w in textwrap.wrap(line, 78) or [""]:
            d.text((140, y), w, font=F(48), fill=INK); y += 70
        y += 20
    return p
pages.append(cover())
per = 4
cells = [SHOTS[i:i+per] for i in range(0, len(SHOTS), per)]
for group in cells:
    p = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(p)
    y = 120
    for (n, a, b, size, lens, desc) in group:
        if n in SCENES:
            d.rectangle([120, y, W-120, y+90], fill=NAVY); d.text((150, y+18), SCENES[n], font=F(46, "Bold"), fill="white"); y += 120
        f = int(((a + b) / 2) * FPS) + 1
        fp = os.path.join(FR, "_ann", "a_%04d.png" % f)
        if not os.path.exists(fp): fp = os.path.join(FR, "f_%04d.png" % f)
        th = 700; tw = int(th * 9 / 16)
        im = Image.open(fp).convert("RGB").resize((tw, th), Image.LANCZOS)
        p.paste(im, (140, y)); d.rectangle([140, y, 140+tw, y+th], outline=(200, 200, 205), width=3)
        x = 140 + tw + 60
        d.text((x, y), f"#{n}   {a:05.2f}–{b:05.2f} s", font=F(52, "Bold"), fill=ORANGE)
        d.text((x, y+75), f"{size}  ·  {lens}", font=F(38, "Medium"), fill=GREY)
        em, dl, snd = S.get(n, ("", "", ""))
        yy = y + 150
        for label, txt, col in [("ACTION", desc, INK), ("PERFORMANCE", em, INK), ("DIALOGUE / TEXT", dl, NAVY), ("SOUND", snd, GREY)]:
            if not txt: continue
            d.text((x, yy), label, font=F(32, "Bold"), fill=GREY); yy += 44
            for w in textwrap.wrap(txt, 52):
                d.text((x, yy), w, font=F(42, "SemiBold" if label == "DIALOGUE / TEXT" else "Regular"), fill=col); yy += 56
            yy += 14
        y += th + 70
        if y > H - 300: break
    pages.append(p)
pages[0].save(OUT, save_all=True, append_images=pages[1:], resolution=300)
print(len(pages), "pages")
