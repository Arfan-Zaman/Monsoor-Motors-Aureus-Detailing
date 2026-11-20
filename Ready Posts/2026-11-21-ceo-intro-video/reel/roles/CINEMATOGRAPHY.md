# "Queue Jump": cinematography plan (DoP), v2

21 Nov 2026 · **39 s** vertical (9:16) Meta/Instagram ad · **34 s story + 5 s brand** · Cinema Studio 4.0 (AI Director, `omni_reference`) · plan only, nothing generated.

This plan follows the **locked story spine** and the latest client and marketing fixes:
- Every shot is its own generation, with no multi-shot prompts.
- The price board is fixed (FuelWatch); only Dave's pump meter ticks.
- The keys are handed over in Dave's driveway.
- Dave buys a **white** stock C-HR; Arfan's black decal car stays ours.
- The super reads "Over 40% less fuel than his ASX. Official figures.*".
- No phone in any driver's hand.
- Budget cap 350, with a 10% reserve.

The shipment sequence, inserted gags, the "PERTH." stamp, the phone insert and slow motion are all **cut**. The GTA-trailer nod now lives only in the look and the locals montage.

Element IDs are in `SHOOTING-SCRIPT.md` §0. Where this file differs from `CONTINUITY.md`, this file wins. For example, horizontal streak flares are now allowed off streetlights and headlights, never across a face.

**New element needed:** `Monsoor-CHR-Hybrid-White-Stock`, Dave's car, built from real photos of the actual stock car (Arfan to supply; ID pending).
**Montage (client change).**
- Three petrol **small SUVs** in the C-HR's $25–30k used band (for example a Mazda CX-3, Hyundai Kona or Honda HR-V; the exact models, real-world L/100km and odometers come from `roles/REAL-NUMBERS.md`).
- Then Dave's ASX last. No ute, no sedan.
- The drivers are saved elements: `Extra-Tradie-Ute` `f8d7835b-7a2a-459e-a171-083e4ee8cf86`, `Extra-Nurse-SUV` `f93882f3-a8d6-4d7c-b29c-f0b419717bf4` and `Extra-Retiree-Sedan` `d56b1059-5bdc-47d2-b72c-1af5edfeec4e`. All three now drive small SUVs, whatever the element names say.

**Mia** is now `Kid-Mia-v2` `9e0c9644-0ae8-4730-82e3-c08a1fa2c2c3` everywhere.

**Arfan wears his Ray-Ban Meta glasses in every shot.** The Transitions lenses are **clear at night** and a **light green tint by day**, with a partial tint at sunset. This replaces "glasses in the shirt pocket at night" in `CONTINUITY.md`. By day the tint must stay light enough that his eyes read, because the "Good job" beat plays on his eyes. If a start frame comes out too dark, fix the start frame.

The odometer shown on Arfan's dash is that real car's reading (Arfan to supply).

---

## (a) Camera package and look bible (Cinema Studio dropdowns)

The 4.0 dropdown IDs are not published. Pick the nearest label in the web app and lock it after the test still.

| Dropdown | Every generation |
|---|---|
| Model / mode | Cinema Studio 4.0, AI Director, `omni_reference`, Sound **on**, 9:16, 720p, **4 s** (the minimum), one shot per generation |
| Camera body | The large-format digital cinema body (Alexa-class if listed). Use the same entry on every generation. |
| Lens | The **anamorphic** prime set if listed. If not, use the cleanest spherical prime and let the Look line carry the anamorphic cues. Anamorphic is a lens character here; the frame stays 9:16. |
| Focal lengths | **32 mm**: car and location wides, no face. **40 mm**: medium-wide with people. **50 mm**: medium faces (default). **75 mm**: close faces and dialogue. **100 mm**: hand, dash and plate inserts. **Never a face on anything wider than 40 mm.** |
| Aperture | T2.3 faces (oval bokeh, eyes sharp) · T4 wides and cars · T5.6 inserts (whole object sharp) |
| Era / Genre | Present day / Commercial (light comedy-drama) |
| Pacing | Brisk for night generations, Natural for yard and home |
| Light | Per shot (table b), always motivated by a visible source |
| Colour palette | ONE preset for the whole ad. It must give saturated sunset pink-orange and teal/magenta nights while skin stays natural. Choose it in the test still and never change it. |
| Grain | None, or "clean digital" (house rule: no grain filter) |
| Look line (the same last sentence of every prompt) | "Anamorphic lens character: oval bokeh, gentle horizontal streak flares from streetlights and headlights only, never across faces; natural skin texture, tack-sharp eyes, real speed, slight camera breathing." |

**Palette by place**
- Montage: car 1 at sunset, car 2 at blue hour, Dave at night. The same evening gets later, which leads into the night servo.
- Servo: teal canopy key, magenta shop neon, amber sodium streetlights, wet concrete.
- Yard: hard midday sun, saturated blue sky, palms, flags.
- Home: sunset pink-orange, palm silhouettes.
- Brand: golden hour on the black C-HR.

**GTA-trailer nod (look only).** The locals montage, the anamorphic flares and bokeh, and the sunset-and-neon palette. Nothing from GTA or Rockstar is used: no name, logo, font, HUD, stars, minimap, characters or music, and no copied frame.

**Test still that locks the look.** It is the V2 start frame, so it costs nothing extra.
1. Generate Dave at pump 2, 50 mm, three-quarter front, at night, with every dropdown above. A sodium streetlight sits behind his shoulder (to test the flare) and the magenta shop neon is soft behind (to test the bokeh).
2. Check it at 100%:
   - oval bokeh;
   - one streak flare, clear of his eyes;
   - real pores and stubble;
   - teal against magenta and amber, with true blacks;
   - Dave identical to `Dad-Dave`.
3. If it passes, screenshot the dropdown panel to `reel/reference/look-lock.png` and copy the labels into `CONTINUITY.md` §1.
4. If it fails, change **one** dropdown and re-roll (1 credit, at most 2 tries).
5. Every later start frame and still is judged side by side with `look-lock.png` before any video credit.

---

## (b) Shot-by-shot table (34.0 s story + 5.0 s brand = 39.0 s)

**Source key**
- **V#**: a 4 s video generation (one shot, its own start frame).
- **P#**: a picture (still) shown on screen. It is moved in the edit with a 2–4% push or pull only, plus comped lights and numbers. Stills are used only where the subject is genuinely static: a parked car at a red light, dashes, a pump screen, a sleeping child, a hand resting.

All cuts are hard cuts on movement or on a sound. Shots run 0.4–2.7 s, averaging about 1.1 s.

**Face rules:**
- **F1**: start already three-quarter, so there is no profile-to-front turn.
- **F2**: the face is at least 1/5 of the frame height.
- **F3**: no whip and no flare across a face.
- **F4**: the eyeline is locked to the named target.

**Humour:** only from the situation. Background extras behave normally.

| # | Time (s) | Src | Lens | Height / angle | Move | Light (key / fill / practicals) | Look nod | Situational humour | Face protection | What the start frame or still must show |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | 0.00–0.40 | P1 | 75 | eye level, front ¾ of small SUV 1 at a red light, driver seen through the windscreen | push 3% | red signal on the bonnet; sunset sky fill; St Georges Tce towers soft | sunset, oval bokeh | a flat "here we go" glance down | `Extra-Nurse-SUV`; F1, F2; both hands on the wheel, **no phone** | small SUV 1 (REAL-NUMBERS), badge soft; nurse in scrubs, eyes down to the dash |
| A2 | 0.40–0.85 | P2 | 100 | over the wheel onto SUV 1's cluster | push 3% | red spill on the cluster hood | | | n/a | SUV 1 cluster, needle near E, amber low-fuel lamp lit, **blank dark trip screen** (label comped) |
| A3 | 0.85–1.25 | P3 | 75 | front ¾ of small SUV 2 on a Kwinana Fwy on-ramp | push 3% | red signal; blue hour; Narrows Bridge and city lights soft | blue hour, streak flare off a streetlight | his slow exhale | `Extra-Tradie-Ute` (now in a small SUV); F1, F2; no phone | small SUV 2, tradie in hi-vis, eyes down |
| A4 | 1.25–1.70 | P4 | 100 | SUV 2 cluster | push 3% | red spill | | | n/a | SUV 2 cluster, as A2 |
| A5 | 1.70–2.10 | P5 | 75 | front ¾ of small SUV 3 in Northbridge | push 3% | red signal; magenta and teal neon | neon night | a small sigh | `Extra-Retiree-Sedan` (now in a small SUV); F1, F2; no phone | small SUV 3, retiree, eyes down |
| A6 | 2.10–2.55 | P6 | 100 | SUV 3 cluster | push 3% | neon spill | | | n/a | SUV 3 cluster, as A2 |
| A7 | 2.55–3.45 | V1 | 75 | front ¾ of Dave's grey ASX on Albany Hwy at night, through the windscreen | slow push | red signal; shopfront fill; sodium streetlights | neon night, streak flare | Dave taps the fuel gauge as if that might help; Mia asleep behind him | **F1, F2**; Dave's face at least 1/4 of the frame; Mia soft in the back seat | **V1 start frame**: Dave at the wheel ¾, eyes down, Mia asleep behind, red light on the bonnet |
| A8 | 3.45–4.20 | P7 | 100 | ASX cluster | push 3% | red spill | | | n/a | ASX cluster, as A2 |
| B1 | 4.20–5.60 | V2 (start) | 40 | high on the **static** price board, craning down over the queue | crane down | canopy teal; sodium streetlights; shop magenta | streak flares, neon | a long queue at 9 pm on a weeknight | no faces in this part | (V2 start frame is B3; see below) |
| B2 | 5.60–6.40 | P8 | 100 | pump 2 screen, straight on | push 3% | pump screen glow | | litres and $ tick up fast (comped counter) | n/a | pump face, screen **blank**, nozzle hose in frame edge |
| B3 | 6.40–7.90 | V2 (end) | 40, landing at a medium | eye level, ¾ front on Dave at pump 2 | end of the crane | key: canopy from above; fill: warm shop window | | his eyes follow the climbing total; slow exhale; head drops a little | **F1, F2, F3** | **V2 start frame = look-lock still**: Dave ¾ front at pump 2, hand on the nozzle, ASX flap open (left rear), board soft behind |
| B4 | 7.90–9.00 | P9 | 75 | outside the ASX rear side window, ¾ | push 2% | warm shop light on the glass | | Mia asleep, cheek squashed on the glass, mouth open | F2; Mia's face at least 1/3 of the frame; through the side window, not the rear screen | Mia asleep against the glass, backpack on her lap |
| C1 | 9.00–10.80 | V3 | 32 | low tracking alongside the C-HR | tracking, **real speed** | streetlight streaks glide across the black paint; canopy | streak flares, wet reflections | the servo goes quiet; heads in the queue turn | no faces close (queue soft) | **V3**: the black C-HR (plate frame on) gliding past the queue on wet concrete, low angle |
| C2 | 10.80–12.60 | V4 (start) | 50 | eye level, ¾ front on Arfan at pump 1 | slow straight push (no arc) | key: canopy; fill: warm shop; rim: sodium streetlight | streak behind him | "Hello mates." An easy nod to the queue | **F1, F2, F3**; Arfan's face at least 1/4 of the frame; nod, no head turn | **V4**: Arfan ¾ beside the closed driver's door of the black C-HR, half-smile, outfit locked, Ray-Ban Metas on with **clear** lenses |
| C3 | 12.60–13.20 | V4 (end) | 50 | same set-up; he has taken two steps to the filler | the push continues | as C2 | | nozzle in with one confident click | right hand, ring visible | (from V4) |
| C4 | 13.20–13.90 | P8 (re-use) | 100 | pump 1 screen (the pumps are identical) | push | | | his counter runs briefly and **stops** at a small top-up | n/a | same picture, a new comp |
| C5 | 13.90–14.60 | P10 | 100 | inside, beside the steering column | push 2% | dash glow; servo light through the glass | | the finger presses POWER, and nothing roars | **left** hand, olive Seiko on the wrist, no ring (POWER sits left of the column in RHD) | Arfan's left index finger on the POWER button, Seiko visible |
| C6 | 14.60–17.30 | P11 | 100 | the C-HR cluster | starts tight on the READY lamp, **pulls out** to the trip screen | cluster glow | | READY fades on in silence (comp); then the good figure, the odometer and the super | n/a | black C-HR cluster: READY lamp area, fuel needle near full, **blank trip screen** (READY, L/100km and odometer comped) |
| D1 | 17.30–18.10 | P12 | 100 | rear ¾ of the black C-HR at the pump, tail-lights on | push 3% | canopy; red tail glow | | | n/a | the rear plate frame and the rear door decal **blank**; our real Monsoor Motors artwork comped on (sharp, legible) |
| D2 | 18.10–19.50 | V5 | 50 | eye level, ¾ front on Dave; the C-HR glides away behind him | none (focus on Dave) | canopy key; red tail-light streaks behind | streak flares | **the double take**: back to his meter, then a snap back to the silently leaving car | **F1** (turn 30° at most, three-quarter to three-quarter), **F2, F4** | **V5**: Dave ¾ front by his ASX, the black C-HR's tail-lights over his shoulder |
| D3 | 19.50–21.50 | V6 | 75 | outside the open rear window, ¾ | none | warm shop light on her face | | deadpan: "Dad... can we get one?" | **F1, F2**; Mia's face at least 1/3 of the frame; F4: eyes to Dave, frame right | **V6**: Mia awake at the open rear window, hugging her backpack |
| E1 | 21.50–22.70 | P13 | 32 | eye level, our yard at midday | push 3% | hard sun from frame left | palms, flags, saturated sky | a "SOLD" sign on the windscreen (comped) | no faces (Arfan's back only, wiping the bonnet) | the **white** C-HR at the front of our Victoria Park yard, Arfan from behind with a cloth |
| E2 | 22.70–24.50 | V7 (start) | 75 | two-shot 30° off the axis | slow push | key: sun from frame left; fill: soft bounce | | Monsoor's hand lands on Arfan's shoulder: "Good job." | **F1: both already ¾ toward each other at frame 1, no turn**; F2, F4 | **V7**: Monsoor ¾ facing Arfan, Arfan ¾ facing him (light green tint, eyes readable), the white C-HR with SOLD soft behind (the sign comped onto the start frame) |
| E3 | 24.50–25.10 | P14 | 100 | close on Monsoor's hand on Arfan's shoulder | push 2% | sun | | | hand only | Monsoor's hand (right sleeve as in his sheet) resting on Arfan's shoulder (outfit fabric) |
| E4 | 25.10–27.00 | V7 (end) | 75 | same two-shot, the push now favouring Arfan | push | as E2 | | "That means a lot for me": chin a touch down, eyes soften | F1, F2; F4: eyes to Monsoor, never the lens | (from V7) |
| F1 | 27.00–28.60 | V8 (start) | 32 | low at the kerb | static; the car fills the frame | low sunset sun from frame left; long shadows to the right | sunset, palms | the white C-HR rolls silently into the driveway | driver behind reflective glass; Dave and Mia soft at the door | **V8**: the white C-HR turning nose-in into the family driveway at sunset, the ASX parked at the kerb |
| F2 | 28.60–30.60 | V9 (start) | 50 | eye level, two-shot at the driver's door | slow push | sun backlight (rim); sky fill | | Arfan hands Dave the keys; Dave weighs them in his palm and grins | **F1, F2, F4** (Dave to the keys, then to Arfan) | **V9**: Arfan (glasses lightly tinted) and Dave ¾ toward each other by the white C-HR, keys between them |
| F3 | 30.60–32.20 | V8 (end) | 32 | same kerb set-up; car stopped | static | as F1 | | Mia runs from the front door to the car | Mia small but moving toward the lens; cut before her face is under 1/8 of frame | (from V8) |
| F4 | 32.20–34.00 | V9 (end) | 50 | same two-shot | the push ends | as F2 | | Mia arrives and hugs the car door; Dave looks at the car, then down the street, quietly pleased | F1, F2 | (from V9) |
| G1 | 34.00–39.00 | P15 | 50 | low ¾ front of the black C-HR in our yard at golden hour | slow 4% push, a comped light sweep across the paint | low warm sun; palm silhouettes | sunset, anamorphic flare off the sun edge | none | none | 2K hero still: the black C-HR, plate frame and decal blank (our art comped), a clean sky band left in the upper-middle for the logo |

**Edit graphics (made locally, free)**
- A2, A4, A6 and A8 labels from `REAL-NUMBERS.md`: the model name in small type and the real-world **L/100km** figure big. The figure stays dimmed over the next shot, so each one is on screen for about 1 s.
- B2 and C4: the pump counter (litres and $). The values must match the fixed board price, with final figures from MARKETING. Arfan's top-up has to be plausible for the C-HR Hybrid's smaller tank.
- C6: READY glow, then the trip figure (inside the real 4.3–5.2 range) and the **real odometer**. Super from 15.2 to 18.1 s: **"Over 40% less fuel than his ASX. Official figures.\*"**
- D1: the real plate-frame and decal artwork.
- E1 and V7 start frame: the "SOLD" sign.
- Mia's line and all dialogue as captions.
- 29.0–34.0 s: "Delivered to your door".
- G1 brand build:
  - 34.3 s: the logo builds;
  - 35.3 s: 0434 137 393 and monsoormotors.com.au;
  - 36.0 s: one line: "MD32748 · \*Official combined: ASX 2.0 7.6 vs C-HR Hybrid 4.3 L/100km";
  - hold to 39.0 s, with the music button on the logo.
- All figures are made in Montserrat, never AI text, because AI digits garble and these numbers are claims.

**Sound timings to update in `EMOTION-AND-SOUND.md`**
- 0–4.2 s: one real car sound per cut (indicator tick, handbrake click, low-fuel bong).
- 4.2 s: servo bed and M1.
- 9.0 s: the **silence** (tyre hiss and electric whine only).
- 11.0 s: "Hello mates" (M2 returns).
- 13.9 s: the POWER press, **no sound**; 14.6 s: a soft READY chime.
- 19.6 s: Mia's line.
- 21.5 s: magpie sound bridge into the yard; 23.0 s: "Good job"; 25.3 s: "That means a lot for me".
- 27.0 s: the voice-over "You choose the car! We bring it to your home!".
- 34.0 s: brand music build; button at 38.5 s.

**One recommended order swap inside the spine (for sign-off).** The spine puts the economy dash before the start button. A trip computer is only lit once the car is on, so the order here is **top-up → POWER → READY → economy figure → leaves**. Every spine beat stays, inside the same 9–21.5 s block.

---

## (c) Prompts, one per generation

Every prompt runs: element tags, then **action**, then **emotion**, then **AUDIO**, then the Look line. Lens, height and light come from the dropdowns, and the prompt names only the shot size.
Before spending credits, lint each prompt with `seedance_lint.py` and run the pre-flight check in `SHOOTING-SCRIPT.md` §6.
**Rule for every video:** its start frame is made first (1 credit), shows the hardest face, and must match its element sheet at 100% before the video runs.

**Video (each 4 s, a single shot, `omni_reference`)**

**V1 Dave at the red light** · `@Dad-Dave` `@Kid-Mia-v2`
> Close on Dave at the wheel of his grey 2021 Mitsubishi ASX, stopped at a red light on Albany Highway at night. Both hands on the wheel, no phone. He glances down at the dashboard, taps the fuel gauge once with one finger, and exhales. Behind him, his daughter Mia sleeps in the back seat. Tired end-of-week resignation, a little wry. AUDIO: idling engine, indicator ticking, muffled street traffic, no music, no speech. [Look line]

**V2 Servo crane to Dave** · `@Perth-Servo-Night` `@Dad-Dave`
> Starting high on the servo's roadside price board, which is steady and unchanged, the view comes down over a long queue of ordinary petrol cars to the road, and lands on Dave at pump 2 filling his grey ASX. His eyes follow the pump total climbing; a slow exhale; his head drops a little. The queue drivers wait normally. Quietly pained, relatable, gently funny. AUDIO: canopy hum, idling engines, pump whirr, distant traffic, no music. [Look line]

**V3 Silent glide** · `@Perth-Servo-Night` `@Monsoor-CHR-Hybrid-Black-Sheet`
> Low beside the black C-HR Hybrid as it glides past the queue on electric power at real speed, streetlights sliding across its paint and the wet concrete, then swings into the free pump 1 lane. The servo goes quiet and drivers in the queue turn their heads. Calm, smooth, a little unreal. AUDIO: only tyre hiss on wet concrete and a faint electric whine, the servo hum dropping away, no music. [Look line]

**V4 "Hello mates"** · `@Perth-Servo-Night` `@Monsoor-CHR-Hybrid-Black-Sheet` `@Arfan-CEO-Final` `@Arfan-CEO-Outfit-Locked` + audio reference "Hello mates" (locked track)
> Arfan, wearing his Ray-Ban Meta glasses with clear night lenses, stands by the black C-HR at pump 1, already turned three-quarters toward the queue. He glances at them, gives a small nod with an easy half-smile and says "Hello mates." He then takes two steps to the filler and clicks the nozzle in. Confident, relaxed, dry humour, never smug. AUDIO: Arfan's line from the reference, footsteps on wet concrete, the nozzle click, low servo hum, no music. [Look line]

**V5 Double take** · `@Perth-Servo-Night` `@Dad-Dave` `@Monsoor-CHR-Hybrid-Black-Sheet`
> Dave stands by his ASX facing us. He glances down at his pump, then snaps his eyes back up as, behind him, the black C-HR pulls away silently into the night, its red tail-lights shrinking down the road. Disbelief turning into curiosity. AUDIO: servo hum, his pump still running, the C-HR leaving almost without a sound, no music. [Look line]

**V6 "Can we get one?"** · `@Perth-Servo-Night` `@Kid-Mia-v2`
> Mia, now awake, leans to the open rear window of the ASX hugging her backpack, looks toward her dad off-screen and says deadpan: "Dad... can we get one?" A beat, then her eyes widen hopefully. Sharp, hopeful, deadpan. AUDIO: Mia's line clear and close, servo hum, no music. [Look line]

**V7 "Good job"** · `@Monsoor-Yard-Victoria-Park` `@MA-Monsor-Real` `@MA-Monsor-Owner-v2` `@Arfan-CEO-Final` `@Arfan-CEO-Outfit-Locked` `@Monsoor-CHR-Hybrid-White-Stock` + audio references "Good job." (Monsoor's cloned voice) and "That means a lot for me." (locked track + "for me")
> Midday at the yard beside the white C-HR marked sold. Monsoor and Arfan stand already turned three-quarters toward each other; Arfan wears his Ray-Ban Meta glasses with a light green daytime tint, eyes visible through them. Monsoor rests his hand firmly on Arfan's shoulder, gives a short nod and says "Good job." Arfan looks at him, chin a touch down, eyes softening, small smile: "That means a lot for me." Proud and fatherly; humble and moved. AUDIO: both lines from the references, a magpie call, flags flapping, distant Albany Highway traffic, no music. [Look line]

**V8 Delivery arrives** · `@Family-Home-Driveway` `@Monsoor-CHR-Hybrid-White-Stock` `@Kid-Mia-v2` `@Dad-Dave`
> Sunset. The white C-HR rolls silently nose-in up the family's driveway and stops; the grey ASX stays parked at the kerb. Mia runs out of the front door toward it; Dave follows. Joyful and relieved. AUDIO: suburban sunset, birds, tyres on the concrete drive, Mia's footsteps, no music. [Look line]

**V9 Keys at home** · `@Family-Home-Driveway` `@Monsoor-CHR-Hybrid-White-Stock` `@Arfan-CEO-Final` `@Arfan-CEO-Outfit-Locked` `@Dad-Dave` `@Kid-Mia-v2`
> By the white C-HR's driver's door, Arfan (Ray-Ban Meta glasses, lightly tinted at sunset) and Dave stand three-quarters toward each other. Arfan hands Dave the keys; Dave weighs them in his palm, grins, then looks at the car and down the street, quietly pleased. Mia comes in and hugs the car door. Warm, simple, real. AUDIO: keys jingle, birds, a gentle evening breeze, no music. [Look line]

**Stills (on screen; 2K high so they are sharp at full frame)** · each ends with the Look line
- **P1, P3, P5** SUV exteriors · `@Extra-Nurse-SUV` / `@Extra-Tradie-Ute` / `@Extra-Retiree-Sedan`: "Front three-quarter of an ordinary [small SUV model from REAL-NUMBERS] stopped at a red traffic light at [St Georges Terrace at sunset / a Kwinana Freeway on-ramp at blue hour with the Narrows Bridge and city lights behind / Northbridge at night with magenta and teal neon]. The driver, both hands on the wheel, no phone, glances down at the dashboard, quietly fed up. Red signal light on the bonnet, real reflections, everything sharp."
- **P2, P4, P6, P7** Clusters: "Close-up of a [model: SUV 1 / 2 / 3 / 2021 Mitsubishi ASX] instrument cluster at night, no brand logos, fuel needle near E, amber low-fuel warning lamp lit, trip-computer screen dark and blank, red traffic-light glow on the hood, everything sharp."
- **P8** Pump: "Straight-on close-up of a Perth servo fuel pump display at night, the screen blank and dark, nozzle hose at the frame edge, canopy light, sharp, no brand."
- **P9** `@Kid-Mia-v2`: "Mia asleep in a car's back seat at night, cheek squashed against the side window, mouth slightly open, backpack on her lap, warm shop light on the glass, sharp."
- **P10** `@Arfan-CEO-Outfit-Locked` `@Monsoor-CHR-Hybrid-Black-Sheet`: "Inside the black C-HR, close on a left index finger pressing the POWER button, olive-dial Seiko on the wrist, dash glow, sharp."
- **P11** `@Monsoor-CHR-Hybrid-Black-Sheet`: "This car's instrument cluster straight on, READY lamp area dark, fuel needle near full, trip-computer screen blank, soft night light, sharp."
- **P12** `@Monsoor-CHR-Hybrid-Black-Sheet` `@Perth-Servo-Night`: "Rear three-quarter of this black C-HR at a night servo pump, tail-lights on, plate frame and door decal panel plain and blank, plate blank, sharp."
- **P13** `@Monsoor-Yard-Victoria-Park` `@Monsoor-CHR-Hybrid-White-Stock`: "Midday at the yard, the white C-HR at the front of the row, a man seen from behind wiping its bonnet with a cloth, palms and flags, hard sun, sharp."
- **P14** `@MA-Monsor-Owner-v2` `@Arfan-CEO-Outfit-Locked`: "Close-up of an older man's hand resting on a younger man's shoulder, real fabric texture, midday sun, sharp."
- **P15** `@Monsoor-Yard-Victoria-Park` `@Monsoor-CHR-Hybrid-Black-Sheet`: "Low front three-quarter hero of this black C-HR in the yard at golden hour, palm silhouettes, a clean sky band upper-middle, plate frame and decal blank, sharp, premium car-commercial light."

**If a face drifts: fix the start frame, not the prompt.**
1. Find the take's best face frame.
2. Re-make the 1-credit start frame: closer (face at least 1/4 of frame), three-quarter, even key light, the same elements. For Monsoor, add his clearest `MA-Monsor-Real` photo as the face lead.
3. Approve it at 100% beside the element sheet, then re-run the **same** prompt.
4. In the edit, use only the clean 0.6–2 s of each take. Fast cutting is the safety net.
5. If the same face fails twice, fix the element sheet.

Text on the car (the plate frame, decal and SOLD sign) goes onto the **start frame** before the video runs, so the clip carries it from frame 1. Use those first frames for the legible beat.

---

## (d) Fixes for weak or cheap shots

| Problem | Fix |
|---|---|
| Old S5: only the back of Dave's head, and the C-HR leaving was invisible | V5: Dave three-quarter front at 50 mm, the C-HR leaves **behind him** in the same frame (the double take). Mia gets her own 75 mm shot at the open window (V6). |
| Price board ticking was untrue (FuelWatch fixes the price for 24 h) | The board is static and soft. The tension moves to Dave's pump counter (B2), comped so it is legible and correct. |
| Old Mia shot through the rear screen at 85 mm smeared her face | Through the side window, three-quarter, as a still (a sleeping child doesn't move, so a still is honest). |
| Old Arfan 50 mm gimbal arc rotated toward profile | Straight slow push, nod only. |
| Old four-person yard wide (small faces, including the real Monsoor) | Yard = establishing still (no faces), the 75 mm two-shot, a hand insert, then the push to Arfan. |
| Monsoor turned mid-shot | Both start three-quarter toward each other; only the hand moves. |
| Keys at the yard contradicted "we bring it to your home" | Keys are handed over in Dave's driveway (V9). The yard is the delivery prep: the white C-HR marked SOLD. |
| Dave driving away in Arfan's decal car | Dave gets the white stock C-HR (new element). The black decal car stays with Arfan and in the brand shot. |
| Plate frame and decal unreadable in AI | Comped on the D1 still from our real artwork; the decal is also comped on the brand still. |
| Old crane-up at home shrank faces | Home ends on the 50 mm two-shot; the wide is car-led (F1, F3). |
| Slow motion and gag inserts read as AI or cringe | Removed. Real speed everywhere; humour only from the situation. |
| Even rhythm reads as AI | Shot lengths 0.4–2.7 s, varied, cut on action and sound. |

---

## (e) Budget (cap 350, 10% reserve). The maths.

Video: 7 credits a second at 720p, 4 s minimum = **28 per clip**. Start frames: 1 credit each. On-screen stills at 2K high: **2.75** each (the measured GPT Image 2.6 price; they fill the frame, so they must be sharp).

| Item | Count | Unit | Credits |
|---|---|---|---|
| Elements already made | | | 5.00 |
| New element: white stock C-HR (from real photos) | 1 | 1 | 1.00 |
| Video V1–V9 | 9 × 4 s = 36 s | 7/s | **252.00** |
| Start frames for V1–V9 (V2's is also the look test) | 9 | 1 | 9.00 |
| On-screen stills P1–P15 (incl. the 3rd SUV exterior and its dash) | 15 | 2.75 | 41.25 |
| Voice: "for me", "Good job" | | | 1.00 |
| Music, 1 version (ElevenLabs via Higgsfield; check the price for 39 s first) | 1 | | 4.22 |
| Gap-filler sound effects | 0 | | 0.00 (car sounds from our licensed library; native audio covers ambience) |
| **Planned total** | | | **313.47** |
| **Reserve** | | | **36.53 (10.4% of 350)** = one 4 s video re-roll (29 with its start frame) plus about 7 start-frame re-rolls |

- **Screen time.** 36 s of video supplies 22.1 s of picture. The 15 stills supply 16.9 s, which includes the 5 s brand (22.1 + 16.9 = 39.0).
- **If a 2nd video re-roll is needed:** the cheapest safe cut is to make V8 (roll-in) a still (saves 26.25). Never cut V2, V4, V5, V6, V7 or V9, which carry the story and the faces.
- **Price check before spending:** quote every item with `estimate_video_cost` / `estimate_image_cost` using the full final settings, and check `transactions` afterwards (house rule).
