# "Queue Jump" — every shot, written for Seedance 2.5 (22 Nov 2026)

Timing follows `QJ45-Animatic.mp4` / `PRODUCTION-SHEET-45.md`. 16 generation clips cover all 42 shots.

## How each clip is made (two steps, same for every clip)

**Step A — start frame**
- Model: GPT Image 2.6, high, 9:16, 2K.
- Every person and object is named by its element `<<<id>>>`. This is where faces, outfits, cars and props are locked.
- Monsoor's frames: `soul_2` with Soul ID `7d5bf600-ee1b-484d-a95f-6bfae7b6e5af` first, then a GPT edit for wardrobe only.
- Check each frame at full size against the real photos and `TEXT-AND-NUMBERS-v2.md` before moving on.

**Step B — video**
- Settings: Seedance 2.5, `mode: omni_reference`, `start_image` = the approved frame, `resolution: 1080p`, `bitrate_mode: high`, `aspect_ratio: 9:16`.
- `image_references`: element images that must stay exact (watch, plate, logo, dog).
- `audio_references`: the locked voice line, only in clips with dialogue (then `generate_audio: true` for lip-sync). Otherwise `generate_audio: false`; the sound comes from our mix.
- Price: 80 credits per 5 s (16 per second).

**Rule: every visible person named with their own reference (Arfan, 22 Nov 2026)**
- In the talking close-ups, "the other man" made the model invent a stranger at the frame edge.
- Every person who appears, even only a head, shoulder or hand at the frame edge, is named in the prompt with their own `image_references` (Arfan's face frame, Monsoor's Soul frame, Dave, Mia, a driver).
- Or the prompt says "only his shoulder and hand at the frame edge, his head stays out of frame".
- Prompts are re-read before every submit.
- Pilot fix: both close-ups were cropped to remove the wrong head (`pilot/*-crop.mp4`).

**Prompt rules (from the Seedance preflight linter)**
- Video prompts never use real names: the start frame carries identity ("the same bearded man...").
- Every video prompt:
  - opens with "Starting from the provided image" plus a concrete setting;
  - stays at 180 words or fewer;
  - avoids the word "skin".
- Lint every prompt before generating: `seedance_lint.py --preflight --model seedance_2_5`.

**Grade line**
Every video prompt includes the night or day version, followed by the film line.
- **Night:** "Grade: wet road, sodium-orange and LED-white streetlights, practical pink and teal neon reflected on paint and puddles, deep natural blacks."
- **Day:** "Grade: warm gold sun, teal-leaning shadows" (golden hour: "pink-orange sky, warm gold rim light").
- **Film line:** "Shot on ARRI Alexa 35, anamorphic, natural film contrast, soft highlight roll-off, true complexion, fine film grain. No HDR look, no oversaturation."

**Ending line (every video prompt)**
"Real speed, camera breathing. No extra people, no hand or badge morphing, no on-screen text, no subtitles, no music."

**Arfan's kit (every start frame he's in)**
- `<<<cde963a1-6dce-441f-b16d-fd74bad0f52e>>>` face (Arfan-CEO-Final);
- `<<<eca28f45-7884-4495-ba6a-c63daadda53f>>>` outfit;
- `<<<885feadc-5d46-4b17-b593-b9d51ec33742>>>` silver chain;
- `<<<e60833f4-19af-4613-84fe-050d48c20b2f>>>` Seiko on the **left** wrist;
- black Ray-Ban Meta Wayfarers, CLEAR lenses at night, light GREEN by day.

---

### Clip 1 — Red-light montage · 0.00–3.15 · night · 5 s (cut to 3.15)

**Start frame**
> Night, St Georges Terrace, Perth CBD, wet road. Through the windscreen of the white X-Trail <<<8d90d3c5-d5f1-41b6-8c1b-ecace51ebddb>>> (plate `1GZG 905`), the driver <<<f2a7b2b7-5837-4e58-8b9a-58fc908d7663>>> is stopped at a red light, seatbelt on, gum in his mouth, glancing at the dash. Setting: <<<1fde51fa-4af9-4559-a4b6-d8cb7f06820c>>>. [night grade + film line]

**Video (refs: X-Trail dash `<<<3405d3e9-df36-4741-971a-2feaeadfa75b>>>`, Sportage `ec60deed-3888-4cd2-9da0-fbec7edab279`, Sportage dash `09994963-fc50-461b-9f13-324cece1b9f0`, Outlander `f4f69697-7c20-462a-a6b4-53a1a427d8e2`, Outlander dash `b9d66635-8189-443e-9f56-751ee43543c6`)**
> Starting from the provided image: night, Perth city streets at red lights, wet road. Multi-shot, hard cuts:
> - 0–0.45s: low car-rig, the white SUV rolls to a stop.
> - 0.45–0.9s: 75mm MCU, the young driver blows a gum bubble, it pops, he half-laughs at his dash.
> - 0.9–1.3s: 100mm close-up of his cluster, `AVG 10.8 L/100km`, `35,917 km`, fuel low.
> - 1.3–1.85s: handheld MCU, a young woman in a red SUV on a freeway ramp, tucks her hair, deadpan at her dash.
> - 1.85–2.25s: her cluster, `AVG 10.5 L/100km`, `37,042 km`.
> - 2.25–2.75s: an older man in a silver SUV peers over his glasses, slow head shake.
> - 2.75–3.15s: his cluster, `AVG 9.5 L/100km`, `64,530 km`.
>
> Everyone belted. [night grade + film + ending]

*Check: plates, the three odometers, belts.*

### Clip 2 — GR86 launch and pull-over · 3.15–6.25 · night · 5 s
**Start frame**
> Night, wet city intersection, light just turned green. The hot-pink Toyota GR86 <<<450b0150-5a35-4b0c-b187-23582a1181f4>>> (custom plate `BURNIT`, kiss decals), driver <<<0b6631a2-04b5-4809-9b49-31acf7df8db3>>> belted, hands at ten and two. Low kerb angle. [night grade + film]

**Video (refs: `Dash-GR86-PulledOver` `195dbd5f-5ad1-4b74-8214-345e5bc14af5`, `FX-Police-Mirror-Lights` `01e4f3b4-223b-4aea-86a4-f4114e75aecf`)**
> Starting from the provided image: night intersection, wet road, neon.
> - 0–0.5s: the pink coupe pulls away hard and leaves frame left; camera stays static, no speedometer, no fast tracking.
> - 0.5–0.7s: a white flash lights the street from off-screen.
> - 0.7–1.55s: inside the coupe, close on the rear-view mirror, red and blue lights from an unmarked car fill it.
> - 1.55–2.35s: close on her cluster, 0 km/h, `ODO 18,645 km`, hazards, amber low-fuel light, red-blue light washing over it.
> - 2.35–3.1s: close on the driver, she drops her head back, eyes shut, "Ugh... oh, come ON!".
>
> No police markings or text. [night grade + film + ending]

*Check: speed never shown above 0, ODO 18,645, no livery.*

### Clip 3 — Dave at the lights · 8.25–9.60 · night · 4 s
**Start frame**
> Night, Albany Highway, Victoria Park. Through the passenger window of the grey 2023 Hyundai Tucson <<<d7902964-9ac7-420f-8463-0b4135c52870>>> (plate `1HTL 482`): <<<a35c0972-e514-477c-ab08-88676417cb5f>>> at the wheel, tired, seatbelt on; in the back <<<ba7458bd-24a7-493f-8838-f74d52ca113b>>> asleep, cheek on the window, belted. [night grade + film]

**Video (ref: `Dash-Tucson-Real` `3b2ae443-ffae-4a70-b3bb-b0dfd628ab2f`)**
> Starting from the provided image: night, highway traffic lights, sodium light through the windscreen.
> - 0–0.9s: 50mm through the passenger window, 2% push; the tired dad exhales, taps the wheel.
> - 0.9–1.35s: cut, 100mm close on his cluster, `AVG 10.1 L/100km`, `36,284 km`, low-fuel light on.
>
> [night grade + film + ending]

### Clip 4 — SWANLINE servo · 9.60–12.90 · night · 5 s
**Start frame**
> Night, the fictional SWANLINE petrol station on Albany Highway <<<3c63f303-3d7b-4bb6-aed9-3b308dc207c7>>>: teal and white canopy, wet forecourt, price board `UNLEADED 91 197.9`, a queue of petrol cars. <<<a35c0972-e514-477c-ab08-88676417cb5f>>> at pump 2 filling the grey Tucson, <<<f4d8ee86-093f-4f0d-b9ca-d1b9251910c8>>> pump screen rolling. [night grade + film]

**Video**
> Starting from the provided image: night servo, fluorescent canopy, wet concrete.
> - 0–1s: 40mm wide, slow 3% push across the forecourt.
> - 1–2.8s: dolly in to the tired dad at pump 2, slow exhale, a small "of course" smirk, the pump screen climbing.
> - 2.8–3.3s: cut to 75mm, the little girl asleep in the back seat, cheek squashed on the window.
>
> [night grade + film + ending]

*Check: SWANLINE only, 197.9, no real brand.*

### Clip 5 — C-HR glide and driving · 12.90–14.50 · night · 4 s
**Start frame**
> Night, the SWANLINE forecourt. Through the driver's window (right-hand drive) of the black 2018 Toyota C-HR Hybrid <<<526b5aa4-80d5-4c7a-96a5-9b6078b58ead>>> (plate `AZ 007` in the frame `MONSOOR MOTORS · VICTORIA PARK` <<<8a465251-85d5-48a8-8d61-aaa84333a305>>>): [Arfan's kit, clear lenses], seatbelt on, both hands on the wheel, phone in a dash cradle showing a call to `BOSS`, pleased half-smile mid-sentence. Passenger seat: <<<68998f3e-e0b2-4b46-9133-2c20e41f586f>>> in a seatbelt harness. [night grade + film]

**Video (refs: Seiko `e60833f4`, dog `68998f3e`, plate `8a465251`; audio: `Arfan-Boss-v3a-tight` uploaded as mp3)**
> Starting from the provided image: night servo, neon reflections sliding over the glass.
> - 0–0.8s: low car-rig outside, the black hybrid glides in silently, real speed.
> - 0.8–1.6s: cut, through the passenger window, the bearded driver says "Boss, just got the car. Coming." in sync with audio 1, eyes on the road, both hands on the wheel, the dog beside him looking ahead.
>
> [night grade + film + ending]

*Check: watch on the left wrist, clear lenses, BOSS on the phone, AZ 007.*

### Clip 6 — Dog woof · 14.50–15.25 · night · 4 s (use 0.75)
**Start frame**
> Inside the black C-HR at night, passenger seat, <<<68998f3e-e0b2-4b46-9133-2c20e41f586f>>> in a black seatbelt harness, gold chain collar, neon outside. [night grade + film]

**Video (audio: `Dog-Woof-Curious` as mp3)**
> Starting from the provided image: car interior at night, pink and teal neon through the window.
> - 0–0.3s: the muscular dog turns its head to camera.
> - 0.3–0.8s: one deep real woof in sync with audio 1, chest moving.
> - 0.8–2s: curious sniffs, head tilt.
>
> [night grade + film + ending]

### Clip 7 — Arfan steps out / "What's up?" · 15.25–18.40 · night · 5 s
**Start frame**
> Night, SWANLINE forecourt, the black C-HR door open. [Arfan's kit, clear lenses] stepping out; his brown chunky fabric sneaker lands in a shallow puddle. [night grade + film]

**Video (refs: Seiko, outfit; audio: `Arfan-WhatsUp-v4a-trim`)**
> Starting from the provided image: night servo, wet concrete, neon.
> - 0–0.5s: ground-level close-up, the brown sneaker splashes into the puddle.
> - 0.5–1.4s: gimbal up to medium shot, he rises out of the car, door clunk, chin up, a confident easy look (we freeze here in the edit).
> - 1.4–3.1s: 50mm push to MCU, he nods to the tired dad off frame right and says "What's up?" warmly in sync with audio 1, relaxed smile.
>
> [night grade + film + ending]

### Clip 8 — Pump, POWER, READY · 18.40–22.55 · night · 5 s
**Start frame**
> Night, pump 1 screen at SWANLINE showing `$ 36.20` · `LITRES 18.29` · `197.9 c/L`, the nozzle in the black C-HR. [night grade + film]

**Video (refs: `CHR-Power-Ready` `9240a5dd-a106-4ce7-af51-171c3dea6de7`, Seiko)**
> Starting from the provided image: night servo.
> - 0–0.6s: 100mm, the pump meter settles and clicks off at 36.20.
> - 0.6–1.1s: cut, close on a man's finger pressing the POWER button, steel watch with olive dial on his left wrist.
> - 1.1–3.6s: cut, the dash lights up, green READY, `45,012 km`, `AVG 5.2 L/100km`, 3% pull-out.
> - 3.6–4.15s: low rear three-quarter, the black hybrid pulls away silently, plate frame readable.
>
> [night grade + film + ending]

### Clip 9 — Dave's double take · 22.55–24.55 · night · 4 s
**Start frame**
> Night, pump 2: <<<a35c0972-e514-477c-ab08-88676417cb5f>>> holding the nozzle, staring off frame left; pump screen `$ 94.99` · `LITRES 48.00`. [night grade + film]

**Video (audio: `Dave-KiddingMe-norm`)**
> Starting from the provided image: night servo.
> - 0–0.8s: locked MCU, the dad watches tail-lights leave, slow double take.
> - 0.8–1.2s: his pump finally clicks off.
> - 1.2–2s: he mutters "...you're kidding me" in sync with audio 1, deadpan.
>
> [night grade + film + ending]

### Clip 10 — Mia · 24.55–26.15 · night · 4 s
**Start frame**
> Night, rear window of the grey Tucson: <<<ba7458bd-24a7-493f-8838-f74d52ca113b>>> awake, belted, pastel lilac hoodie, looking up toward her dad off frame. [night grade + film]

**Video (audio: `Mia-v2-tight-norm`)**
> Starting from the provided image: night, servo light on her face.
> - 0–0.4s: handheld 75mm, the girl leans to the window.
> - 0.4–3s: she says "Daaad... can we get one?" in sync with audio 1, deadpan, then her eyes widen with hope.
>
> [night grade + film + ending]

### Clip 11 — Night pre-order · 26.15–28.15 · night · 4 s
**Start frame**
> Late night in a modern Perth lounge <<<ae93d34b-a49c-49f1-af3d-0c7b953468af>>>, dark except for phone glow: <<<a35c0972-e514-477c-ab08-88676417cb5f>>> on the couch, thumb over his phone; <<<ba7458bd-24a7-493f-8838-f74d52ca113b>>> leaning over his shoulder, eyes on the screen. (Composition per <<<718fefe0-4e42-4e4c-b36a-dfe5b0077d00>>>.) [night grade + film]

**Video (ref: `Phone-PreOrder-CHR-2341` `1f089d31-7aa3-4123-93e6-c96414810840`)**
> Starting from the provided image: dark lounge, cool phone glow.
> - 0–1s: slow push, the dad hesitates, the girl watches the screen, holding her breath.
> - 1–1.5s: cut, close on the phone, Monsoor Motors listing, black C-HR Hybrid, orange PRE-ORDER button, clock 23:41.
> - 1.5–2s: his thumb taps PRE-ORDER.
>
> [night grade + film + ending]

### Clip 12 — Yard, SOLD, Hellcat, Monsoor steps out · 28.15–32.75 · day · 5 s
**Start frame**
> Sunny morning, the Monsoor Motors yard <<<df5571c0-29f4-4760-b8cc-ebb8d5c4561c>>> with the real logo sign and navy flags <<<ab8bec5b-8aec-4287-94ee-b631f9142d8e>>>; the black C-HR with `SOLD · Dave & Mia` tag and plate `AZ 007`. [day grade + film]

**Video (refs: Hellcat `a3988f3e-1fd9-4931-9bef-64425af0ff49`, Seiko, Monsoor Soul frame)**
> Starting from the provided image: sunny car yard, magpies, flags snapping.
> - 0–0.8s: wide, the sign and flags.
> - 0.8–1.4s: close, a hand with a steel olive-dial watch hangs the SOLD tag on the windscreen.
> - 1.4–3.2s: low track, a black Dodge Challenger Hellcat Redeye, plate `MM BOSS`, rumbles into the yard and stops; nose dips.
> - 3.2–3.7s: ground level, a black loafer onto the brick.
> - 3.7–4.6s: low angle, the bearded owner in a navy silk palm-print shirt and aviators rises from the car (freeze point).
>
> [day grade + film + ending]

### Clip 13 — Monsoor close-up "Good job!" · 33.15–34.45 · day · 5 s — **PILOT, rendering**
Start frame: job `77779ced-829c-4f94-9449-fec748fa6a97` (Soul ID face, navy shirt fixed). Audio: `0925aa1f-eb8b-4e59-8523-1b3d16f47e07`. Prompt: `p13` as sent (162 words). Video job `18128571-b36c-4538-a8fc-f734b36d22bc`.

### Clip 14 — Arfan close-up "That means a lot." · 34.45–36.50 · day · 5 s — **PILOT, rendering**
Start frame: job `a2d1edee-8b5f-4a02-a10a-e9900c4d8c87`. Audio: `282cc5a7-4862-4158-a219-fabf74949688`. Prompt: `p14` as sent (167 words). Video job `89478e24-12be-4322-a1a4-411262d012d6`.

### Clip 15 — Delivery · 36.50–40.10 · golden hour · 5 s
**Start frame**
> Golden hour, the driveway of house number `27` <<<095c7577-1e27-4966-af47-d41c1ffeb929>>> at a modern home <<<ae93d34b-a49c-49f1-af3d-0c7b953468af>>>; the black C-HR parked, [Arfan's kit, green lenses] holding out the real Toyota smart key <<<313d52b9-7298-4634-87c4-d1030e280285>>> palm up to <<<a35c0972-e514-477c-ab08-88676417cb5f>>>. [golden-hour grade + film]

**Video (refs: smart key, Seiko; audio: `Arfan-YouChoose` + `Arfan-WeBring` joined)**
> Starting from the provided image: golden-hour suburban driveway, palms.
> - 0–1.6s: low kerb track, the black hybrid rolls in and settles.
> - 1.6–2.7s: gimbal push, the bearded man in the black palm-print shirt offers the key palm up; the key drops into the dad's hand, keyring jingle.
> - 2.7–3.6s: wide, the girl runs across the lawn, palms on the car door, dad grinning.
>
> [golden-hour grade + film + ending]

### Clip 16 — Hero + brand · 40.10–44.95 · golden hour · 5 s
**Start frame**
> Golden hour by the Swan River, Perth skyline. The black Dodge Challenger Hellcat <<<a3988f3e-1fd9-4931-9bef-64425af0ff49>>> (`MM BOSS`) behind two men: [Arfan's kit, green lenses] holding <<<68998f3e-e0b2-4b46-9133-2c20e41f586f>>> on a short lead; beside him Monsoor (Soul ID frame, navy silk shirt, gold chain, aviators up) with his arm on Arfan's shoulder. Both look to the lens. (Composition per <<<11b8059e-68ed-4d00-9494-48e45f5d47ae>>>; faces from the elements, not from that still.) [golden-hour grade + film]

**Video**
> Starting from the provided image: golden-hour riverside, warm low sun, palm silhouettes.
> - 0–2s: low hero angle, slow 3% push; the two men stand easy, a shared look then back to lens, the dog sits calm.
> - 2–5s: hold, light breeze, a lens flare from the low sun.
>
> [golden-hour grade + film + ending]

MISSION PASSED animates over this in the edit; the brand card follows (our logo graphics, not generated).

---

## Cost (Seedance 2.5, 1080p, high bitrate)
- 16 clips at about 4–5 s each is about 75 s, at 16 credits per second: **about 1,200 credits**.
- Start frames: about 50 credits.
- Allow about 20% for retakes.
- **Total about 1,500 of the 2,462 credits.**
- Each batch is quoted before it is submitted.
