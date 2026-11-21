# Element readiness vs the script (22 Nov 2026)

| Scene / need | Element(s) | Status |
|---|---|---|
| Arfan face, outfit, chain, glasses | Arfan-CEO-Final · Arfan-Outfit-Hawaiian-Sheet · Arfan-Silver-Chain | READY |
| Monsoor | MA-Monsoor-Boss-v2 · MA-Monsoor-Turnaround (face via Soul ID) | READY (Monsoor to approve look) |
| Dave, Mia | Dave-Real · Mia-Real | READY |
| Montage drivers | Driver-GenZ-Guy-Real · Driver-GenZ-Woman-Real · Driver-Retiree-Real · Driver-Glam-Real | READY |
| Real cars | Car-Dave-Tucson-2023 · Car-GenZGuy-XTrail-2023 · Car-GenZWoman-Sportage-2023 · Car-Retiree-Outlander-2021 · Car-Glam-GR86-Pink · Car-Monsoor-Hellcat · Monsoor-CHR-Hybrid-Black-Sheet | READY |
| Locations | GTA-Perth-Aerial-Dusk · GTA-RedLights-Neon · GTA-Servo-Neon · **GTA-Yard-Premium** · GTA-DaveHome-Modern | READY |
| Arfan's dog (in the C-HR at night, at his feet in the yard) | Dog-Pitbull-Muscle (muscular, stone-faced, never snarling) | READY |
| Props / FX | Props-PlateFrame-SOLD-Keys · Prop-HandsFree-Call · CHR-Power-Ready · Prop-WA-Speed-Camera · FX-SpeedCam-Flash | READY |
| Dashboards of the real cars | Dash-Tucson-Real · Dash-XTrail-Real · Dash-Sportage-Real · Dash-Outlander-Real · Dash-GR86-Real | READY |
| Pump display with real numbers | Pump-Dave-Real ($94.99 · 48.00 L · 197.9) | READY |
| Voice: Arfan "Monsoor, just got the car. Coming." / "What's up?" | voice/qj/Arfan-JustGotTheCar.wav · Arfan-WhatsUp.wav | READY (check by ear) |
| Voice: Monsoor "Good job." · Mia "Dad... can we get one?" | voice/qj/Monsoor-GoodJob.wav · Mia-A.wav / Mia-B.wav | READY (pick Mia by ear) |
| Voice: Arfan "That means a lot." / CTA | locked track | READY |
| Music (Gen Z sections A/B/C) + SFX (edit pack, hype cars, servo, yard) | audio/music, audio/sfx | READY (to approve by ear) |
| Designed sounds (READY chime, sonic logo, risers, hits, strobe) | audio/designed | READY |
| Title cards ARFAN / MONSOOR / DAVE / PERTH. / BUSTED. + film LUT | graphics/ | READY |
| Retire from prompts | Car-Dave-ASX-Grey, Cars-Montage-3-SUVs, Car-Glam-V8-SUV, Car-Monsoor-MuscleCar, Car-Glam-PinkRacer, Dash-ASX/Seltos/CX3/V8, GTA-Perth-RedLights, GTA-Servo-Swanline, GTA-Yard-Monsoor, GTA-Driveway-Sunset, Perth-Servo-Night, Monsoor-Yard-Victoria-Park, Family-Home-Driveway | superseded |

## Update 22 Nov 2026
- Length: up to **45 s** (story ~40 s + 5 s brand). Added beats: Dave's muttered "...you're kidding me", the glam driver's "Oh, come ON!", the pitbull reveal riding shotgun, the dog at Arfan's feet at the yard.
- Voice v2 (GTA-style delivery): voice/qj/Arfan-Boss-v2.wav "Boss... just got the car. Coming." · Arfan-WhatsUp-v2.wav "Hey, what's up?" · Monsoor-GoodJob-v2.wav "Good... job." · Mia-v2.wav "Daaad... can we get one?" · Glam-ComeOn.wav · Dave-KiddingMe.wav. Choose by ear.
- Monsoor's car: Car-Monsoor-Hellcat (Dodge Challenger SRT Hellcat Redeye Widebody).
- Logos: real badges on real cars in the story only; never another brand's logo in our graphics; no GTA/Rockstar marks.

## Update 22 Nov 2026 (compliance and new elements)
- `Monsoor-Motors-Logo` ab8bec5b-8aec-4287-94ee-b631f9142d8e: official logo (horizontal navy + stacked on warm white). Use on the yard sign, flags, frame and end card. Never redraw it.
- `Props-Plate-AZ420-SOLD-Keys` 6a3d3eb7-3e65-4fd7-83b9-b91398f0cf33: C-HR plate `AZ 420` in the MONSOOR MOTORS · VICTORIA PARK frame. Supersedes Props-PlateFrame-SOLD-Keys.
- `GTA-Yard-Premium-AZ420` 53a82c2f-9ca9-45be-ab3b-00e974844e23: supersedes GTA-Yard-Premium.
- `Dog-American-Bully` 68998f3e-e0b2-4b46-9133-2c20e41f586f: supersedes Dog-Pitbull-Muscle (American Bully type, seatbelt harness in car, lead at the yard).
- `Arfan-Seiko-watch` e60833f4-19af-4613-84fe-050d48c20b2f: **must be in every prompt that shows Arfan's hands or wrist, POV shots included** (POWER press, nozzle, SOLD tag, keys, steering wheel). Left wrist, olive dial, steel bracelet.
- Key handover uses the real Toyota C-HR smart key element `Props-CHR-Smart-Key` 313d52b9-7298-4634-87c4-d1030e280285, not a generic fob.
- Rule: every recurring object in a shot is passed as its element; no object described from text alone when an element exists.
- `GTA-Yard-Premium-Final` 8d00a83a-56af-463e-b2f2-846e7626c405: **use this yard.** Real logo on the wall sign AND the navy feather flags (orange edge); C-HR plate `AZ 420`, SOLD tag. Supersedes GTA-Yard-Premium and GTA-Yard-Premium-AZ420.

## Update 22 Nov 2026, later: plate AZ 007 (final), GR86 at 52, Monsoor approved
- **Plate is now `AZ 007`** (Arfan's final choice). AZ 420 elements are retired.
- `Yard-Final-AZ007` df5571c0-29f4-4760-b8cc-ebb8d5c4561c: **THE yard.** Supersedes every earlier yard element.
- `Props-Plate-AZ007-SOLD-Keys` 8a465251-85d5-48a8-8d61-aaa84333a305: **THE plate/props sheet.** Supersedes every earlier plate element.
- `Dash-GR86-52kmh` 3f075568-2302-4411-a7a8-a7761fec2bdb: lawful launch dash (52 km/h, low-fuel light). Supersedes Dash-GR86-Real.
- Monsoor approved his look (Soul ID route) on 22 Nov 2026.
- 45 s: no paid video exists yet, so nothing needs re-rendering. The free Blender previs gets re-timed to 45 s before video generation.
- Yard-Final-AZ007 df5571c0-29f4-4760-b8cc-ebb8d5c4561c · Props-Plate-AZ007-SOLD-Keys 8a465251-85d5-48a8-8d61-aaa84333a305 · Dash-GR86-52kmh 3f075568-2302-4411-a7a8-a7761fec2bdb.
- `FX-Police-Mirror-Lights`: generic pull-over lights in her mirror (no livery). Game-style cards: graphics/Card-BUSTED-GTA.png and graphics/Card-DEMERITS-GTA.png (fine amount blurred, pink; -3 DEMERIT POINTS yellow), built by graphics/make_gta_cards.py in Pricedown.
- Every on-screen arrival has a matching sound: see the table at the end of MUSIC-CUES.md.
- `Dash-GR86-PulledOver`: 0 km/h, ODO 18,645 km, hazards, low-fuel light, red-blue wash (the odometer follows the story).

## Voice update 22 Nov 2026 (Arfan didn't like "Hey, what's up?" or the slow "Good... job.")
- Arfan "What's up?": new takes `voice/qj/Arfan-WhatsUp-v4a.wav` (warm, relaxed) and `-v4b.wav` (quicker, cool); trimmed versions `-trim.wav`. No "hey", no laugh. v4a used in the animatic.
- Monsoor "Good job.": `voice/qj/Monsoor-GoodJob-v3b.wav` — one breath, no gap, 0.6 s of speech (trimmed version used).
- 45 s animatic: `QJ45-Animatic.mp4` (local, built by `qj45_animatic.py`): the 39 s previs re-cut + new beats (flash, police mirror, pulled-over dash, BUSTED, demerits, dog reveal, yard AZ 007, dog at yard), fuel super replaced by "About half the fuel.*". Previs dash numbers are placeholders; the elements carry the real ones.
- **LOCKED (Arfan, 22 Nov 2026):** "What's up?" = `Arfan-WhatsUp-v4a-trim.wav` (warm). "Good job." = `Monsoor-GoodJob-v3b-trim.wav`. Older takes of these two lines are retired.
- **Dog sound LOCKED (22 Nov 2026):** `audio/sfx/Dog-Woof-Curious.wav` = one real deep woof, then curious sniffs, a low talking grumble and a short whine (built from Dog-BarkCurious-A).
- **Monsoor "Good job!" LOCKED:** `voice/qj/Monsoor-GoodJob-v4-smile-trim.wav` (smiling, warm, one breath). Face: his own natural smile.
