# "Queue Jump": DIRECTOR'S CUT (production document, v1)

21 Nov 2026 · 39.0 s · 9:16 · 1080×1920 delivery · 34.0 s story + 5.0 s brand · Meta / Instagram paid and organic.
Plan only: nothing generated, nothing committed. This file merges `roles/CINEMATOGRAPHY.md`, `roles/CHOREOGRAPHY.md`, `roles/CONTENT-AND-SOUND.md`, `roles/MARKETING.md` (story fixes, compliance, variants), `roles/REAL-NUMBERS.md`, `SHOOTING-SCRIPT.md` §7–8 and `CONTINUITY.md`, plus the client changes of 21 Nov. **Where any of those files disagree with this one, this one wins.**

---

## 0. Decisions and conflicts resolved

| # | Topic | Role files said | Director's cut (and why) |
|---|---|---|---|
| 1 | Video model | Cinema Studio 4.0, 7 credits/s | **Cinema Studio Video 3.0** (`cinematic_studio_3_0`), 720p, 4 s = **20** (quoted today). Seedance 2.0 for montage and dialogue. |
| 2 | Dialogue shots | All heroes on Cinema Studio | CS 3.0 takes only start/end images, **no audio reference**, so it cannot lip-sync to the locked track. The three dialogue shots (V4, V6, V7) move to **Seedance 2.0 std** with `audio_references` (18 each, quoted). Hero total: 7 on CS 3.0 + 3 on Seedance std. |
| 3 | Dave's car | White stock C-HR | **No white C-HR.** Dave buys **our black C-HR** (`526b5aa4…`), the car he saw at the servo. Arfan tags it SOLD at the yard and delivers it. |
| 4 | Yard | Dave and Mia choose the car at the yard | Cut. They found us through the plate frame; the yard is now **Arfan + Monsoor, next morning**, and the delivery follows. |
| 5 | Monsoor | `MA-Monsoor-Hero` / `MA-Monsor-*`, element-only face | **`MA-Monsoor-Boss-v2` `0bd837e0-5c67-4768-a4b4-a105fc5ed65c`.** Face route: Soul ID `7d5bf600-ee1b-484d-a95f-6bfae7b6e5af` start frame on `soul_2` → GPT Image 2.6 edit (costume, placement) → video with `<<<8eab65a7…>>>`. Older Monsoor elements are retired from every prompt. |
| 6 | Arfan's outfit | Several drafts | **`Arfan-Outfit-Shoot` `7a6ad32a…` + face `Arfan-CEO-Final` `cde963a1…`** in every Arfan shot. Crime-drama outfit `10f68c0b` rejected; not used anywhere. |
| 7 | "That means a lot for me" | Keep "for me" (new 0.5 s) | **Cut "for me".** The locked clip "That means a lot." (1.56 s) fits the yard beat, needs no new Arfan audio, and avoids the non-standard English being burned into captions. |
| 8 | Price board | Ticks up once (CONTINUITY) | **Static** (FuelWatch). Only Dave's pump meter ticks. |
| 9 | Fuel super | "…Official figures.*" / source line under it | Locked text only: **"Over 40% less fuel than his ASX.\*"** The qualifier lives in the brand-card legal line and the caption. |
| 10 | Extra supers | "Next day.", "Delivered to your door.", "Perth metro. Conditions apply." | **Cut** (no other info text). Dialogue **captions stay**: they are subtitles of spoken lines, and the ad must read with sound off. |
| 11 | Dash numbers | Real-world figures (10.4, 5.2…) | **Official ADR combined** (basis A in REAL-NUMBERS) on every label, so every figure matches the legal line: Seltos 6.8, CX-3 6.3, Kona 6.6, ASX 7.6, C-HR Hybrid 4.3. The V8 has no sourced figure: **needle on E + odometer only**. |
| 12 | Cast | Tradie, nurse, retiree-sedan; `Dad-Dave`, `Kid-Mia` | **SHOOTING-SCRIPT §11 locked cast only:**<br>• `Driver-GenZ-Guy-Real` f2a7b2b7 (gum bubble)<br>• `Driver-GenZ-Woman-Real` b77e0ccd (tucks hair)<br>• `Driver-Retiree-Real` eefa2c79 (hunched, peers over glasses)<br>• `Driver-Glam-Real` 0b6631a2 (sunglasses)<br>• `Dave-Real` a35c0972<br>• `Mia-Real` ba7458bd<br>The sheet beats replace the choreography's tradie/nurse/retiree beats. |
| 13 | Slow motion on Monsoor's step-out | Allowed if natural | **Real speed.** House rule: never retime a shot. Generated slow-mo is a floaty AI tell. The power comes from the low angle, the loafer insert and the engine cut. |
| 14 | Loud engines | V8 SUV burble in the montage | Two loud engines, both at the punchline of a gag: the glam V8 launch (0.5 s, heard from outside) and Monsoor's muscle car (the longest and loudest). Every other car is an idle. |
| 17 | Montage ending | Glam driver lowers her sunglasses at a red light | **Client decision 21 Nov:** she launches at the green, her speedo ticks just past 60 in a signed 60 zone, and a **fixed speed camera flashes**: busted. The sequence is about 1.95 s and controlled (no burnout, no weaving, empty street). Risk accepted by the client (see G, compliance). **Fallback cut** (fuel-light flash) is kept ready. |
| 18 | Arfan's shirt | — | It may change to a black Hawaiian print (pending his pick). **Element IDs stay** `cde963a1` + `7a6ad32a` until he confirms. |
| 15 | Look-lock test still | V2 start frame | **V1 start frame** (Dave at the red light: sodium light + neon + face). V2's first frame is now a wide. |
| 16 | Lens set | 24–85 mm (CONTINUITY) vs anamorphic 32–100 (DoP) | DoP set: **32 / 40 / 50 / 75 / 100 mm** anamorphic character. No face wider than 40 mm except car-led wides. |

---

## (A) Treatment

Tuesday night in Perth, the cheap-fuel night: locals sit at red lights across the city, each glancing at the fuel gauge, while "Tuesday night. Perth." holds still over the cuts: a Gen Z guy blowing a gum bubble on St Georges Tce at sunset, a Gen Z woman tucking her hair at a Kwinana Fwy ramp signal, and a hunched retiree peering over his glasses by Elizabeth Quay. Then a glam driver in a badge-less V8 launches at the green, ticks just past 60, and a speed camera flashes: busted, mouth open, sunglasses sliding. Dave is last, at his light, with Mia asleep behind him. At the servo the price board doesn't move; only Dave's pump meter runs, and runs. Then the sound drops out: a black C-HR Hybrid glides in on electric power, Arfan steps out with a throwaway "Hello mates", tops up, and his pump clicks off while Dave's is still going. POWER, a soft READY chime, then the dash: 4.3 L/100km, 45,000 km, "Over 40% less fuel than his ASX.\*" Dave does a double take as it leaves with the Monsoor Motors plate frame and door decal, and Mia, awake now, asks, "Dad... can we get one?" Next morning at our Victoria Park yard, Arfan presses a SOLD tag onto that same black C-HR. A badge-less muscle car rumbles in, the only loud engine in the film, and Monsoor steps out, aviators on and smiling. He puts a hand on Arfan's shoulder: "Good job." "That means a lot." At golden hour Arfan pulls the black C-HR into Dave's driveway and hands over the keys palm-up as Mia runs out, over his own voice: "You choose the car! We bring it to your home!" The film ends on a 5 s golden-hour hero of the car, with the logo, phone, URL and one legal line. The look is a quiet wink at a famous game trailer, carried only by the anamorphic glass, the pink-orange sunsets, the teal and magenta nights and the montage of locals. It is never named, and the jokes come only from the situation.

---

## (B) Scene by scene, then shot by shot

### B1. Scenes

| Scene | Time | Place / light | Beat | Generations used |
|---|---|---|---|---|
| 1 Montage | 0.00–6.45 | Four Perth spots, sunset → blue hour → dusk → neon night; Albany Hwy at night | Same look at the gauge three times; the glam launch and speed-camera flash; Dave | M1–M4 (Seedance fast), M5 + V1 (CS 3.0), I-1…I-5 |
| 2 Servo | 6.45–9.75 | Night servo, Victoria Park: teal canopy, magenta shop neon, amber sodium | Static board; Dave's meter runs; Mia asleep | V2, I-13, I-6, P-Mia |
| 3 Arrival | 9.75–21.50 | Same servo | Silent glide; "Hello mates"; quick top-up; POWER/READY/4.3; double take; Mia's line | V3, V4, V5, V6, I-6…I-11 |
| 4 Yard | 21.50–28.05 | Our yard, next morning, hard sun from frame left | SOLD tag; muscle car; Monsoor's "Good job." | V10, V7, I-12, I-14 |
| 5 Home | 28.05–34.00 | Dave's driveway, golden hour, low sun from frame left | Delivery, keys palm-up, Mia runs out; V.O. | V8, V9, I-15 |
| 6 Brand | 34.00–39.00 | Black C-HR in our yard at golden hour | Logo build, phone, URL, legal line | P-Brand |

### B2. Shot table

Key. Size: EWS/WS/MWS/MS/MCU/CU/ECU. Angle: low / eye / high / OTS / ground. Sound: FX / AMB / MUS / DX. **Cut** = the cut type into the next shot. **NPI** = the "not pasted in" check for that shot (full list in F). Shot pairs that share a letter (for example 14/16 = V2) are cut from the **same generation**.

| # | In–out (s) | Size / angle | Shot (what we see) | Camera, lens, move | Performance (choreography) | Sound | Text on screen | Source | Edit / transition |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00–0.45 | WS / low | White Seltos-type SUV rolls up to the red line, St Georges Tce, sunset towers | 75 mm low car-rig track alongside, settling | Car stops, nose dips | FX indicator tick; AMB CBD traffic, crossing beeps; MUS sub pulse from 0.0 | Hook **"Tuesday night. Perth."** 0.15–6.35 (held over every cut); watermark from 0.0 | M1 (Seedance 2.0 fast) `<<<f2a7b2b7…>>>` | Hard cut on the nose-dip settle. NPI: red signal on bonnet. |
| 2 | 0.45–0.90 | MCU / eye | GenZ-Guy through windscreen | Same take, settled; faint idle vibration | Eyes on gauge, chewing; **gum bubble pops**; slow exhale; shoulders drop; looks up | Bubble pop 0.62; his exhale | hook | M1 tail | Cut on the eyes lifting. Same take as #1 (WS → MCU). |
| 3 | 0.90–1.30 | CU / high | Seltos cluster: needle near E, amber low-fuel lamp | 100 mm over the wheel, 3% push in edit | — | **Designed low-fuel chime** (falling two-note) on the cut | hook + label "6.8 L/100km\* · 52,846 km" | I-1 (GPT 2.6 medium) | Hard cut on the chime. |
| 4 | 1.30–1.85 | MCU / eye (passenger side) | GenZ-Woman, red CX-3-type, Kwinana Fwy ramp signal, Narrows Bridge lights | 75 mm, steady handheld breathing | **Tucks hair behind her ear**; eyebrow up; slow tired head tilt; slow blink | AMB freeway rush; her small sigh | hook | M2 (Seedance fast) `<<<b77e0ccd…>>>` | Cut at the end of the tilt. |
| 5 | 1.85–2.25 | ECU / high | CX-3 analogue tacho + small digital readout | 100 mm, push 3% | — | Cabin hum, indicator | hook + "6.3 L/100km\* · 29,417 km" | I-2 (medium) | Hard cut. |
| 6 | 2.25–2.75 | MCU / slight low | Retiree, **hunched over the wheel**, blue Kona-type, Elizabeth Quay at dusk | 75 mm from the dash side, car rig | Peers over reading glasses; brows up; small headshake ×2; lips pressed | AMB river breeze, crossing tick, distant bus | hook | M3 (Seedance fast) `<<<eefa2c79…>>>` | Cut on the second turn. |
| 7 | 2.75–3.15 | CU / high | Kona fully digital cluster, trip page | 100 mm | — | Soft cabin tick | hook + "6.6 L/100km\* · 31,268 km" | I-3 (medium) | Hard cut. |
| 8 | 3.15–3.65 | WS / low | Badge-less black luxury V8 SUV at a Northbridge red; light turns green; controlled launch, rear squats | 32 mm low at the kerb, static then a short track | Car moves off straight, tyres bite, no smoke | **V8 exhaust note** (loud, 0.5 s); neon buzz; MUS riser cut short | hook | M5 head (CS 3.0) | Cut as the rear squats (cut on movement). |
| 9 | 3.65–4.05 | ECU / high | V8 speedo needle ticking just past 60 (64 → 67), odometer 41,593 km | 100 mm | — | Engine pull under the cabin | hook (no label; the needle and digits are our comp) | I-4 (medium) + comp | Hard cut. |
| 10 | 4.05–4.50 | WS / low | The SUV passes the 60 sign and the fixed speed-camera pole; **white strobe** on the body | Same take as #8, tracking | — | **Shutter click + strobe "thwip"** (designed) at 4.20 | hook | M5 tail | Cut 2 frames after the flash. |
| 11 | 4.50–5.10 | CU / eye | Glam driver, busted: mouth open, sunglasses sliding crooked, slow wince | 75 mm passenger side, car rig | Freezes; mouth falls open; glasses slide; eyes shut in a wince | Her tiny gasp (designed voice); engine note drops off | hook | M4 (Seedance fast) `<<<0b6631a2…>>>` | Hard cut to Dave on the wince. |
| 12 | 5.10–6.00 | MCU / eye | Dave in his grey 2021 ASX, Albany Hwy, Victoria Park; Mia asleep soft behind | 50 mm outside the passenger window, car rig, slow 2% push | Jaw sets; slow breath out through the nose; eyes to the mirror (Mia); small resigned nod; light turns green | ASX idle; indicator; Mia's sleeping breath; MUS soft riser from 5.70 | hook | V1 (CS 3.0) `<<<a35c0972…>>>` `<<<ba7458bd…>>>` | Cut on the nod as green light spills. |
| 13 | 6.00–6.45 | CU / high | ASX analogue dials + centre multi-info display | 100 mm | — | Cabin hum; riser peaks | hook out at 6.35; "7.6 L/100km\* · 64,873 km" | I-5 (medium) | Hard cut on the music drop. |
| 14 | 6.45–6.90 | WS / low | Static servo price board, queue headlights, exhaust haze | 40 mm, 3% push | Nothing moves on the board | **MUS drop on 6.45** (half-time groove); AMB canopy hum, idles | — | I-13 (medium) | Hard cut. Digits plausible, soft, not a claim. |
| 15 | 6.90–7.45 | MWS / eye | The queue, Dave small at pump 2, nozzle in, hand on roof | 50 mm dolly push begins | Shifts weight; rolls neck | Idles; pump whirr starts | — | V2 head (CS 3.0) | Cut as his eyes go to the meter. |
| 16 | 7.45–7.90 | ECU / eye | Pump 2 meter: litres rolling fast ($ column soft) | 100 mm | — | Pump whirr, fuel flow | litres comp (e.g. 31.4 → 33.0 L) | I-6 (medium) | Hard cut on a digit roll. |
| 17 | 7.90–9.25 | MCU / eye | Dave's wince (hero) | End of the V2 push | Watches the total; narrows eyes; looks away at the road; looks back; slow exhale; head drops; small smirk | Whirr continues | — | V2 tail | Cut on the start of an inhale. Same take as #15. |
| 18 | 9.25–9.75 | CU / eye | Mia asleep against the ASX side window, cheek squashed, backpack on lap | 75 mm, 2% push | Still; breathing only | Muffled through glass; idles swell 9.4–9.75 | — | P-Mia (GPT 2.6 high) | Hard cut **into silence**. |
| 19 | 9.75–11.35 | WS / low | Black C-HR glides past the queue, swings into pump 1 | 32 mm low car rig, real speed | Rolls, body roll, stops, nose dips; Dave glances once (background) | **MUS cuts dead 9.75; AMB −12 dB in 0.3 s**; tyre hiss, faint electric whine; one idle drops away; room-tone floor | — | V3 (CS 3.0) `<<<526b5aa4…>>>` | Cut on the settle. |
| 20 | 11.35–11.80 | ECU / ground | Arfan's boot planted flat in a thin puddle reflecting the amber board | 32 mm ground level | Hem settling (still) | Door latch 11.37; boot on wet concrete | — | I-7 (medium) | **Match cut** partner of #32 (Monsoor's loafer). |
| 21 | 11.80–13.20 | MS → MCU / eye | Arfan by pump 1, three-quarter, clear-lens Ray-Ban Metas | 50 mm gimbal, slow straight push | Pushes door shut behind him; glances at Dave; small nod; "Hello mates" lightly; looks back; reaches for nozzle | Door clunk 11.82; **MUS returns 11.82**, warm and low; **DX 12.10–12.80 "Hello mates."** (locked) | caption "Hello mates." 12.10–12.90 | V4 (Seedance 2.0 std + audio ref) | Cut on the reach. |
| 22 | 13.20–13.65 | CU / eye | Right hand, silver ring, seats the nozzle in the C-HR filler (right rear) | 100 mm | One squeeze | Nozzle click 13.28 | — | I-8 (medium) | Hard cut on the click. |
| 23 | 13.65–14.25 | ECU / eye | Pump 1 meter: runs briefly and **stops** | 100 mm (same pump face as #16; pumps identical) | — | Short pump run; **auto-shutoff clunk 14.10**; Dave's whirr still under | litres comp stops at 9.84 L | I-6 reuse | Cut 0.15 s after the clunk. |
| 24 | 14.25–14.65 | MS / eye | Dave still filling, eyes on his meter; C-HR soft behind | 50 mm locked off | Weight on one leg, waiting | His whirr, now the only pump running | — | V5 head (CS 3.0) | Hard cut. |
| 25 | 14.65–15.15 | ECU / high | Inside: left index finger on POWER, olive Seiko | 100 mm | One firm press, held 3 frames, lift | Button click 14.85; **no engine** | — | I-9 (medium) | Cut on the lift. |
| 26 | 15.15–17.05 | CU / eye | C-HR cluster: READY glows, then the trip figure | 100 mm; digital 3% pull-out in edit | — | **Designed READY chime** (soft rising two-note) 15.25; cabin quiet, servo muffled | READY comp 15.25; "4.3 L/100km\* · 45,000 km" 15.65; **super "Over 40% less fuel than his ASX.\*" 15.75–18.10** | I-10 (medium) | Hard cut. Trip computer only lit after POWER. |
| 27 | 17.05–17.60 | MS / low | Rear three-quarter of the C-HR at the pump, tail-lights on; plate frame and door decal | 50 mm, 3% push | — | Tyres creak as it starts to roll (pre-lap) | super holds | I-11 (medium, real artwork comped) | Cut as the tail-lights brighten. |
| 28 | 17.60–19.60 | MCU / eye | **Dave's double take**; C-HR leaves behind him with plate frame | 50 mm locked off, slight breathing | Glances up; back down; freezes; looks up quickly (≤30°, 6 frames); brows up; mouth slightly open; watches; slow blink | **MUS breakdown 17.60** to one sustained guitar note; his whirr; C-HR nearly silent | super out 18.10 | V5 tail | Cut on the blink opening. Same take as #24. |
| 29 | 19.60–21.50 | CU / eye | Mia awake at the open rear window, chin on the sill | 75 mm, slight handheld | Still face; eyes to Dad; "Dad..."; blink; "...can we get one?"; brows lift on "one"; holds | **DX 19.85–21.25 Mia**; nothing else under; **Dave's nozzle clunks off 21.40** | caption "Dad... can we get one?" 19.85–21.30 | V6 (Seedance std + audio ref) | Hard cut after the clunk; magpie pre-laps at 21.35. |
| 30 | 21.50–22.05 | ECU / eye | Arfan's hand smoothing a SOLD tag onto the black C-HR windscreen | 100 mm | Palm flat, small press | **MUS bright groove 21.50**; AMB magpie, Albany Hwy, flags | — (SOLD is our real tag artwork, a prop) | I-12 (medium) | Hard cut. |
| 31 | 22.05–23.35 | WS / low | Badge-less black muscle car rumbles through the yard gate, stops | 32 mm low track alongside, settling | Car rocks once as engine cuts | **V8 rumble swamps the music**, blip, engine off 23.20, tick of the cooling exhaust; MUS ducked under | — | V10 head (CS 3.0, start + end frame) | Cut on the engine cut. |
| 32 | 23.35–23.80 | ECU / ground | Monsoor's loafer lands flat on the brick | 32 mm ground level | (still) | Leather sole on brick | — | I-14 (medium) | **Match cut** with #20. |
| 33 | 23.80–24.90 | MS / low | Monsoor rises, shuts the door, aviators, warm smile, starts walking | Same take as #31, settled low | Easy door push; hand rests on the roof a moment; smile on seeing Arfan | Door thunk 23.85; MUS swells back warm | — | V10 tail | Cut on his first step (cut on movement). |
| 34 | 24.90–26.35 | MCU / OTS | Over Monsoor's right shoulder onto Arfan; Monsoor's left hand lands on Arfan's right shoulder | 75 mm, slow push | Hand lands; one soft pat; "Good job."; Arfan's shoulder dips; looks at him; chin a touch down | Soft pat 25.20; **DX 25.30–25.80 "Good job."** (Monsoor's cloned voice); MUS −6 dB, pad swell | caption "Good job." 25.30–25.90 | V7 head (Seedance std + audio ref) | Cut on the chin dip. OTS hides Monsoor's lips. |
| 35 | 26.35–28.05 | CU / eye | Arfan close, Monsoor's hand at frame edge | End of the V7 push | Slow blink; small eyebrow lift; smile becomes real; "That means a lot."; glances down, back up | **DX 26.45–28.01** (locked); nothing else under | caption "That means a lot." 26.45–28.05 | V7 tail | Cut on the eyes returning; birds pre-lap 27.90. |
| 36 | 28.05–29.35 | WS / low | Black C-HR rolls nose-in into Dave's driveway; Dave waits; ASX at the kerb | 32 mm low at the kerb, short track then settle | Nose dips; Dave weight on one leg | AMB suburb birds, distant mower; tyres on concrete; **V.O. 28.10–28.97 "You choose the car!"** | caption "You choose the car!" | V8 head (CS 3.0) | Cut on the settle. |
| 37 | 29.35–30.55 | MS / eye | Arfan walks to Dave, palm comes up flat with the keys | 50 mm gimbal push; the two in a V | Two easy steps; palm up | **V.O. 29.28–30.23 "We bring it to your home!"** (starts 0.07 s before the cut) | caption "We bring it to your home!" | V9 head (CS 3.0) | Cut as the palm settles. |
| 38 | 30.55–31.05 | ECU / high | Key fob lying on Arfan's open palm, ring visible | 100 mm | (still) | **Keys jingle 30.98** (lift-off at the cut) | — | I-15 (medium) | Hard cut on the jingle. |
| 39 | 31.05–32.35 | WS / low | Mia bursts out of the front door, runs across the lawn | Same take as #36 | Short uneven strides; two stutter steps | Front-door clack 31.08; footsteps grass → concrete; **MUS lift 31.05** | — | V8 tail | Cut before her face drops under 1/8 frame. Same take as #37. |
| 40 | 32.35–34.00 | MS / eye | Mia's palms land on the C-HR door; Dave grins at the keys, looks down the street; Arfan steps back | End of the V9 push | Palms flat; Dave weighs keys; Arfan's half-pace back | Palm pat on the door; MUS builds to brand | — | V9 tail | Hard cut on the music hit at 34.00. Same take as #37. |
| 41 | 34.00–39.00 | MS / low | Golden-hour hero: black C-HR in our yard, palm silhouettes, clean sky band | Still with a slow 3% push and one comped light sweep | — | **MUS last phrase 34.00; sonic logo (READY motif) 35.30; resolve 36.00; button 38.00**; 0.1 s tail fade | logo build 34.30–35.30; **0434 137 393** 35.40; **monsoormotors.com.au** 35.70; **"MD32748 · \*Official combined: ASX 2.0 7.6 vs C-HR Hybrid 4.3 L/100km"** 36.00–39.00 | P-Brand (GPT 2.6 high) | Watermark off during the card. |

**Coverage check.** No two consecutive shots share both size and angle. The deliberate rhymes are the match cut #20↔#32 (boot ↔ loafer) and the matched pump faces #16/#23, and neither pair is adjacent. Shot lengths run 0.40–2.00 s (brand 5.0 s), and no two neighbours share a length pattern for more than two shots. **Cuts from one generation:** M1 → #1/#2 · M5 → #8/#10 · V2 → #15/#17 · V5 → #24/#28 · V10 → #31/#33 · V7 → #34/#35 · V8 → #36/#39 · V9 → #37/#40. **Pump still I-6** gives #16 and #23, with different comps.

**Continuity rows (replaces CONTINUITY §3 for people and cars).**

| Who / what | Every shot |
|---|---|
| Arfan | `Arfan-CEO-Final` + `Arfan-Outfit-Shoot`: black linen shirt, coffee gurkha trousers, black Chelsea boots, olive Seiko on the left wrist, silver ring on the right hand, Ray-Ban Meta glasses (clear at the servo and in the car, light green tint at the yard and home). Never touches the glasses. |
| Monsoor | `MA-Monsoor-Boss-v2` via the Soul ID route: deep navy silk camp-collar palm-print shirt, gold rope chain, gold watch, charcoal trousers, loafers, dark aviators by day. Navy + gold vs Arfan's black + silver. |
| Dave / Mia | `Dave-Real` a35c0972 / `Mia-Real` ba7458bd, same clothes night and next evening (one day later reads as casual). Mia ~1.3 m. |
| Black C-HR | `526b5aa4…`, RHD; filler right rear (verify); Monsoor Motors plate frame + small door decal (our real artwork); SOLD tag from #29 on; plate blank; odometer 45,000 km. |
| Dave's ASX | Grey 2021 ASX LS 2.0, filler left rear (verify); at the kerb at home, kept, never mocked. |
| Muscle car | Badge-less black luxury muscle car, no logos; yard only. |

---

## (C) Generation list, in order

**Settings for all.** 9:16. Pass the Monsoor Motors project `folder_id` on every call. Log each job in `aureus-video-studio/assets/GENERATION-LOG.md`. Quote with `estimate_*_cost`, then check `transactions` afterwards.
- **Video:** 720p; `generate_audio` **false** (all sound is built in the edit).
- **Stills:** GPT Image 2.6. Start frames and on-screen faces at **high 2K (2.75)**; inserts at **medium (1)**.
- **Prompts:** order is action → emotion → imperfections → light → lens → AUDIO → Look → Negative. `<<<ID>>>` is an element. The Look line and Negative line are part of every video prompt (already in the text).

**Face routes**
- **Monsoor:** `soul_2` with `soul_id 7d5bf600-ee1b-484d-a95f-6bfae7b6e5af` (quoted 0.12, billed ≈1) → GPT Image 2.6 high **edit** for costume and placement, keeping the face → video with `<<<0bd837e0-5c67-4768-a4b4-a105fc5ed65c>>>`. Never text- or element-only.
- **Arfan:** always `<<<cde963a1-6dce-441f-b16d-fd74bad0f52e>>>` + `<<<eca28f45-7884-4495-ba6a-c63daadda53f>>>`.

### C0. Look lock (first spend)
**SF-V1 start frame = look-lock still** (2.75). It is judged at 100%:
- oval bokeh;
- one streak flare, clear of the eyes;
- real pores;
- teal vs magenta vs amber, with true blacks;
- Dave identical to his sheet.

If it passes, screenshot the settings to `reference/look-lock.png`. Every later frame is judged beside it. If it fails, change one thing and re-roll (at most 2).

### C1. Start frames (GPT Image 2.6 high 2K, 2.75 each unless noted)

| ID | For | Elements | Start-frame description (prompt) |
|---|---|---|---|
| SF-M1 | M1 | `<<<f2a7b2b7-5837-4e58-8b9a-58fc908d7663>>>` | Low car-rig view beside a white Kia Seltos-type small petrol SUV rolling toward a red light on St Georges Terrace, Perth, at sunset; the Gen Z driver visible through the side glass, both hands on the wheel, no phone; towers soft pink-orange; plates blank; anamorphic oval bokeh; sharp. |
| SF-M2 | M2 | `<<<b77e0ccd-9139-4914-9e86-6ace90669d6e>>>` | Eye-level from the passenger side: the Gen Z woman at the wheel of a red Mazda CX-3-type SUV at a red ramp signal on a Kwinana Freeway on-ramp, blue hour, Narrows Bridge lights soft; eyes down to the dash; hands on the wheel; no phone; sharp. |
| SF-M3 | M3 | `<<<eefa2c79-d3b5-4572-9a53-b0139fb58f3e>>>` | Front three-quarter from the dash side: the Miami-styled retiree, reading glasses low on his nose, at the wheel of a blue Hyundai Kona-type SUV at a red light by Elizabeth Quay at dusk, chin slightly down; sharp. |
| SF-M4 | M4 | `<<<0b6631a2-04b5-4809-9b49-31acf7df8db3>>>` | 75 mm close-up from the passenger side: the glam driver in oversized dark sunglasses at the wheel of the black V8 SUV, moving along a Northbridge street, magenta and teal neon on her face, both hands on the wheel, confident half-smile; sharp. |
| SF-M5 | M5 | — (car only) | 32 mm low at the kerb: the black badge-less V8 SUV waiting at a red light at a Northbridge intersection; a **60 speed-limit sign (our comp, exact)** and a grey fixed speed-camera box on a pole further along; empty street; rain-dark road; neon. |
| SF-V1 | V1 (look lock) | `<<<a35c0972-e514-477c-ab08-88676417cb5f>>>` `<<<ba7458bd-24a7-493f-8838-f74d52ca113b>>>` | From outside the passenger window, 50 mm: Dave at the wheel of his grey 2021 Mitsubishi ASX, three-quarter, eyes down to the gauge, both hands on the wheel; Mia asleep against the left rear window, soft; red signal on the bonnet; a sodium streetlight behind his shoulder (flare test); magenta shop neon soft (bokeh test); Albany Highway, Victoria Park, night. |
| SF-V2 | V2 | `<<<37296861-4e5c-4308-9dab-449dcb59a5b9>>>` `<<<a35c0972-e514-477c-ab08-88676417cb5f>>>` | Medium-wide from beside the pump island: the night queue of ordinary petrol cars, headlights on, exhaust haze; Dave at pump 2, nozzle in the ASX's left-rear filler, left hand on the roof; static price board soft behind; teal canopy light, rain-dark concrete reflections. |
| SF-V3 | V3 | `<<<37296861-4e5c-4308-9dab-449dcb59a5b9>>>` `<<<526b5aa4-80d5-4c7a-96a5-9b6078b58ead>>>` | Low car-rig view beside the black C-HR Hybrid gliding past the queue on rain-dark concrete; canopy and streetlights streaking across the paint; plate blank; queue soft. |
| SF-V4 | V4 | servo + C-HR + `<<<cde963a1-6dce-441f-b16d-fd74bad0f52e>>>` `<<<eca28f45-7884-4495-ba6a-c63daadda53f>>>` | 50 mm eye level: Arfan three-quarter beside the black C-HR's open driver's door (right side) at pump 1, Ray-Ban Meta glasses with clear lenses, eyes fully visible, locked outfit, Seiko left wrist, ring right hand; face ≥1/4 of frame; canopy key, warm shop fill, sodium rim. |
| SF-V5 | V5 | servo + `<<<a35c0972-e514-477c-ab08-88676417cb5f>>>` + C-HR | 50 mm: Dave three-quarter by his ASX at pump 2, hand on the nozzle, eyes on his meter; over his shoulder, the black C-HR at pump 1, tail-lights on, **our real plate-frame and decal artwork comped on before the video**. |
| SF-V6 | V6 | servo + `<<<ba7458bd-24a7-493f-8838-f74d52ca113b>>>` | 75 mm from outside the open rear side window of the ASX: Mia awake, chin on the sill, hugging her backpack, eyes to frame right (Dad); warm shop light on her face; face ≥1/3 of frame. |
| SF-V10s | V10 start | yard + muscle car | 32 mm low near the brick: the badge-less black muscle car rolling in through our yard gate, morning sun from frame left, palms and flags; driver not visible behind the tinted glass. |
| SF-V10e | V10 end | **soul_2 (≈1)** → GPT edit (2.75) → `<<<0bd837e0-5c67-4768-a4b4-a105fc5ed65c>>>` | Low-angle medium: Monsoor standing by the shut door of the muscle car on our brick, body three-quarter to the lens, warm closed-mouth smile, dark aviators, deep navy silk camp-collar palm-print shirt, gold rope chain, gold watch, charcoal trousers, loafers; hard morning sun from frame left; contact shadows. |
| SF-V7 | V7 | **soul_2 (≈1)** → GPT edit (2.75) with `<<<cde963a1…>>>` `<<<7a6ad32a…>>>` | 75 mm over Monsoor's right shoulder (navy palm-print silk, gold chain edge, aviator arm) onto Arfan MCU three-quarter, Ray-Ban Metas with light green tint and eyes readable; Monsoor's left hand low at his side; the black C-HR with the SOLD tag soft behind; morning sun from frame left. |
| SF-V8 | V8 | `<<<d5da6271-1093-470d-8628-5d69ef5f882d>>>` + C-HR + Dave + Mia | 32 mm low at the kerb, golden hour: the black C-HR turning nose-in to the driveway, the driver a shape behind the glass; Dave at the driveway edge, hands in pockets; grey ASX at the kerb; front door closed; plate frame comped. |
| SF-V9 | V9 | home + C-HR + Arfan (both IDs) + Dave + Mia | 50 mm eye level: Arfan and Dave in a V about 1 m apart by the black C-HR's driver's door; Arfan's right hand coming up palm-up with one key fob on a plain ring; low sun rim; light green-tinted lenses. |

### C2. On-screen stills

| ID | Model / cost | Elements | Prompt |
|---|---|---|---|
| P-Mia | GPT 2.6 high, 2.75 | `<<<ba7458bd-24a7-493f-8838-f74d52ca113b>>>` | Mia asleep in the ASX's back seat at night, cheek squashed against the side window, mouth slightly open, backpack on her lap, seen from outside the side window; warm shop light on the glass; real texture, sharp. Negative: no text, no waxy skin. |
| P-Brand | GPT 2.6 high, 2.75 | `<<<d9dfe0fd-89ba-4fba-b719-ee33c0f0588b>>>` `<<<526b5aa4-80d5-4c7a-96a5-9b6078b58ead>>>` | Low front three-quarter hero of this black C-HR Hybrid in our Victoria Park yard at golden hour; palm silhouettes; anamorphic flare off the sun edge only; a clean sky band in the upper middle for the logo; plate frame and decal plain (our artwork comped); premium car-commercial light; sharp. Negative: no text, no logos. |

### C3. Inserts (GPT Image 2.6 medium, 1 each). Every one ends "sharp, real texture, no brand logos, no text".

| ID | Prompt |
|---|---|
| I-1 | Close-up over the wheel of a Kia Seltos-type instrument cluster at sunset: analogue dials, small colour centre screen **dark and blank**, fuel needle near E, amber low-fuel lamp lit, red signal glow on the hood. |
| I-2 | Close-up of a Mazda CX-3-type cluster: large analogue tacho, small digital readout **blank**, fuel needle near E, low-fuel lamp, blue-hour light. |
| I-3 | Close-up of a Hyundai Kona-type fully digital cluster in one long housing, trip page area **blank**, low-fuel symbol lit, dusk light. |
| I-4 | Close-up of a black luxury SUV speedometer at night, **needle removed / dial clean** (we comp the needle ticking 64→67 and the odometer 41,593 km), magenta neon spill. |
| I-4b | **Fallback only:** the same cluster with the amber low-fuel lamp area dark and the needle near E (we comp the lamp popping on). |
| I-5 | Close-up of a 2021 Mitsubishi ASX cluster: analogue speedo and tacho, small centre multi-info display **blank**, needle near E, red signal glow, night. |
| I-6 | Straight-on close-up of a generic Perth servo pump display at night, all digit windows **blank and dark**, nozzle hose at the frame edge, canopy light. |
| I-7 | Ground-level close-up: a black Chelsea boot (with the coffee trouser hem of `<<<7a6ad32a…>>>`) planted flat in a thin puddle reflecting an amber price board and white canopy light, beside the black C-HR's open door sill. |
| I-8 | Close-up: a right hand with a silver ring seating a fuel nozzle into the right-rear filler of the black C-HR `<<<526b5aa4…>>>`, hose in frame, canopy light. |
| I-9 | Inside the black C-HR: close on a left index finger about to press the POWER button, olive-dial Seiko on the wrist, dash glow, servo light through the glass. |
| I-10 | This black C-HR's cluster `<<<526b5aa4…>>>` straight on, READY lamp area dark, fuel needle near full, trip screen **blank**, soft night light. |
| I-11 | Rear three-quarter of this black C-HR at a night servo pump, tail-lights on, plate frame and door decal panel plain (artwork comped), plate blank. |
| I-12 | Close-up of a hand with a silver ring smoothing a plain blank windscreen tag onto the black C-HR in a sunny yard, morning sun from frame left (our real SOLD artwork comped onto the tag). |
| I-13 | Low wide of a Perth servo's roadside price board at night, digits soft and generic, the queue's headlights behind, exhaust haze in the canopy light. |
| I-14 | Ground-level close-up: a dark loafer planted flat on red brick paving beside the sill of a black muscle car's open door, charcoal trouser hem, hard morning sun, contact shadow (`<<<8eab65a7…>>>` for wardrobe only; no face). |
| I-15 | Close-up from above: one key and fob on a plain ring lying on an open right palm with a silver ring, golden-hour rim light, driveway concrete soft below. |

### C4. Video generations (prompts final; linted; shown exactly as they will be sent)

| ID | Model / settings / cost | Inputs | Lip-sync method |
|---|---|---|---|
| M1–M4 | Seedance 2.0 **fast**, 720p, 4 s, audio off · **10 each** | start_image SF-M1…M4 + element | No dialogue (M4's gasp is a designed voice sound) |
| M5 | Cinema Studio 3.0, 720p, 4 s · **20** | start_image SF-M5 | No dialogue. CS 3.0 chosen over Seedance fast for car weight (rear squat, tyre bite) |
| V1, V2, V3, V5, V8, V9 | Cinema Studio 3.0, 720p, 4 s, audio off · **20 each** | start_image SF-V# (+ elements) | No dialogue on screen (V.O. only) |
| V10 | Cinema Studio 3.0, 720p, 4 s · **20** | start_image SF-V10s + **end_image SF-V10e** | No dialogue |
| V4 | Seedance 2.0 **std**, 720p, 4 s · **18** | start_image SF-V4; audio_reference: locked "Hello mates" (0.70 s, padded **only with its own room tone** to 2.0 s) | Audio reference; if the lips miss twice, fall back to the take where his head is turned at the line and lay the locked audio |
| V6 | Seedance 2.0 std · **18** | start_image SF-V6; audio_reference: approved Mia line (padded to 2.0 s) | Audio reference |
| V7 | Seedance 2.0 std · **18** | start_image SF-V7; audio_reference: "Good job." + 0.65 s gap + locked "That means a lot." (≈2.7 s) | OTS hides Monsoor's mouth; Arfan's lips follow the reference |

Note: if a Seedance take ignores the audio reference with `generate_audio` off, re-run with it **on** (same quoted price) and mute the native track in the edit.

**M1** · Seedance 2.0 fast · start SF-M1 · 10
```text
**Aspect ratio**: 9:16  **Resolution**: 720p  **Mode**: fast  **Duration**: 4s
<<<f2a7b2b7-5837-4e58-8b9a-58fc908d7663>>> drives a white Kia Seltos-type small petrol SUV, stopped at a red light on St Georges Terrace, Perth, at sunset. Holds still for a moment, then, eyes on the fuel gauge, chewing gum: blows a small gum bubble that pops, slow exhale through pursed lips, shoulders drop, looks up at the light. Both hands on the wheel, no phone.
Emotion: flat "here we go again", good-humoured.
Imperfections: right thumb taps the wheel once; one uneven blink; the body rocks slightly on the idle.
Light: red signal glow on bonnet and face, pink-orange sunset sky, tower reflections sliding on the windscreen.
Camera: 75 mm front three-quarter through the windscreen, bonnet car rig, faint vibration, slow push-in.
AUDIO: indicator ticking, engine idle, city traffic, crossing beeps. No music, no speech.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**M2** · Seedance 2.0 fast · start SF-M2 · 10
```text
**Aspect ratio**: 9:16  **Resolution**: 720p  **Mode**: fast  **Duration**: 4s
<<<b77e0ccd-9139-4914-9e86-6ace90669d6e>>> drives a red Mazda CX-3-type small petrol SUV, stopped outdoors at a red ramp signal on a Kwinana Freeway on-ramp, exterior, evening blue hour, Narrows Bridge lights soft behind. Holds still for a moment, then, eyes on the fuel readout: tucks a strand of hair behind her ear, one eyebrow goes up, slow tired head tilt to the side, slow blink, keeps looking. Hands on the wheel, no phone.
Emotion: tired disbelief, deadpan.
Imperfections: the strand slips half loose again; the tilt stops short and settles; shoulders soften late.
Light: red ramp-signal glow on her cheek, deep blue sky, amber freeway lights behind.
Camera: 75 mm from the passenger side, eye level, steady handheld breathing.
AUDIO: freeway traffic rushing past, cabin hum, a small sigh. No music, no words.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**M3** · Seedance 2.0 fast · start SF-M3 · 10
```text
**Aspect ratio**: 9:16  **Resolution**: 720p  **Mode**: fast  **Duration**: 4s
<<<eefa2c79-d3b5-4572-9a53-b0139fb58f3e>>>, hunched forward over the wheel, reading glasses low on his nose, drives a blue Hyundai Kona-type small petrol SUV, stopped at a red light by Elizabeth Quay at dusk, city lights on the water. Holds still for a moment, then: peers over his glasses at the fuel gauge, eyebrows up, small slow headshake, lips pressed. Hands on the wheel, no phone.
Emotion: dry disbelief, amused at himself.
Imperfections: two small uneven turns of the head; one finger lifts off the wheel and settles back.
Light: red signal on the bonnet, dusk sky, warm quay lights on the glass.
Camera: 75 mm front three-quarter from the dash side, car rig, faint idle vibration.
AUDIO: engine idle, river breeze, crossing tick, a distant bus. No music, no words.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**M5** · Cinema Studio 3.0 · start SF-M5 · 20
```text
Exterior, night, a Northbridge street in Perth, magenta and teal neon, rain-dark road, no other cars or pedestrians nearby. A big black badge-less luxury V8 SUV waits at a red traffic light; a roadside 60 speed-limit sign and a grey fixed speed-camera box on a pole stand further along the kerb. Holds still for a moment, then: the light changes to green; the SUV moves off briskly and in a straight line, its rear squats on the suspension, tyres bite cleanly with no smoke and no slide, and it passes the speed-camera pole as the camera box fires one bright white flash.
Emotion: cheeky swagger, about to be caught.
Imperfections: the body rocks back then settles; a puddle splashes softly; the camera rig lags a touch before tracking.
Light: signal glow turning from red to green, neon streaks on the black paint, one white strobe flash.
Camera: 32 mm low beside the kerb, static while the light changes, then a short low tracking move.
AUDIO: off.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no burnout, no tyre smoke, no drifting, no weaving, no other road users, no text except the 60 sign, no logos, no plates, no slow motion.
```

**M4** · Seedance 2.0 fast · start SF-M4 · 10
```text
**Aspect ratio**: 9:16  **Resolution**: 720p  **Mode**: fast  **Duration**: 4s
<<<0b6631a2-04b5-4809-9b49-31acf7df8db3>>>, oversized dark sunglasses, drives a big black badge-less luxury V8 SUV along a Northbridge street, exterior neon at night. Holds still for a moment, then: a bright white flash from the roadside lights her face; she freezes, mouth falls open, her sunglasses slide down her nose, she stares straight ahead, busted, then shuts her eyes in a slow wince. Both hands on the wheel, no phone.
Emotion: glamorous swagger collapsing into caught-out embarrassment.
Imperfections: the sunglasses slide unevenly and stop crooked; a small breath through the nose; the cabin sways gently as the car slows.
Light: magenta and teal neon sliding across her face; one hard white flash from outside the window.
Camera: 75 mm close-up from the passenger side, car rig, gentle vibration.
AUDIO: off.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**V1** · Cinema Studio 3.0 · start SF-V1 (look lock) · 20
```text
<<<a35c0972-e514-477c-ab08-88676417cb5f>>> Dave, <<<ba7458bd-24a7-493f-8838-f74d52ca113b>>> Mia. Night, Albany Highway, Victoria Park, Perth. Dave at the wheel of his grey 2021 Mitsubishi ASX at a red light, Mia asleep against the rear window behind him. Holds still for a moment, then: jaw sets, slow breath out through the nose, eyes to the rear-view mirror, small resigned nod; the light turns green.
Emotion: tired end-of-week resignation, wry, never angry.
Imperfections: his grip shifts once on the wheel; the nod is slightly late after the breath; Mia's chest rises with her breathing.
Light: red signal on the bonnet and his face, amber sodium street lights, shopfront spill; green light spills across his face at the end.
Camera: 50 mm eye level outside the passenger window, car rig with faint idle vibration, slow 2% push.
AUDIO: off (sound built in the edit).
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**V2** · Cinema Studio 3.0 · start SF-V2 · 20
```text
<<<37296861-4e5c-4308-9dab-449dcb59a5b9>>> servo, <<<a35c0972-e514-477c-ab08-88676417cb5f>>> Dave. Exterior, night, a busy petrol station forecourt in Perth, a queue of ordinary petrol cars idling to the road. Dave at pump 2 with the nozzle in his grey ASX, left hand on the roof. Holds still for a moment, then: shifts his weight, rolls his neck; Dave watches the pump total climb, narrows his eyes, looks away at the road, looks back, slow exhale, head drops, small smirk. The price board behind is steady and unchanged.
Emotion: quietly pained, relatable, gently funny.
Imperfections: his shoulders drop a moment after the exhale; exhaust haze drifts across the canopy light; a queue driver rests an arm on a window sill.
Light: cool teal-white canopy downlights from above, warm shop window behind right, magenta shop neon soft, rain-dark concrete reflections.
Camera: 50 mm, slow dolly push from beside the pump island toward his three-quarter face.
AUDIO: off.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**V3** · Cinema Studio 3.0 · start SF-V3 · 20
```text
<<<37296861-4e5c-4308-9dab-449dcb59a5b9>>> servo, <<<526b5aa4-80d5-4c7a-96a5-9b6078b58ead>>> black C-HR. Night at a busy Perth servo. Holds still for a moment, then: black C-HR rolls past the queue at steady speed with no engine sound, turns into the free pump lane, body rolls slightly, stops, nose dips and settles; Dave in the background glances once.
Emotion: calm, smooth, a little unreal against the tired queue.
Imperfections: the front wheel steers in a touch late; a puddle ripples behind the tyre; the camera rig bumps once over a seam in the concrete.
Light: street lights and canopy lights slide across the black paint; rain-dark concrete reflects the canopy.
Camera: 32 mm low tracking beside the car on a low car rig at real speed.
AUDIO: off.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**V4** · Seedance 2.0 std · start SF-V4 · audio ref "Hello mates" (locked) · 18
```text
**Aspect ratio**: 9:16  **Resolution**: 720p  **Mode**: std  **Duration**: 4s
<<<37296861-4e5c-4308-9dab-449dcb59a5b9>>> servo, <<<526b5aa4-80d5-4c7a-96a5-9b6078b58ead>>> black C-HR, <<<cde963a1-6dce-441f-b16d-fd74bad0f52e>>> Arfan in <<<eca28f45-7884-4495-ba6a-c63daadda53f>>>. His lips follow the audio reference exactly.
Holds still for a moment, then: Arfan wearing his Ray-Ban Meta glasses, clear lenses, pushes the car door shut behind him while walking to the pump, glances at the man at the next pump, small nod, says "Hello mates" lightly, looks back to the pump and reaches for the nozzle.
Emotion: relaxed, dry humour, a passing courtesy, never smug.
Imperfections: half-smile starts on the left side and is gone at once; a half-step as he turns; sleeve creases on the reach.
Light: cool canopy downlights above, warm shop window behind right, amber street-light rim, rain-dark concrete reflections.
Camera: 50 mm eye level, gimbal, slow straight push, no arc.
AUDIO: his line from the reference only, footsteps, low servo hum. No music.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**V5** · Cinema Studio 3.0 · start SF-V5 · 20
```text
<<<37296861-4e5c-4308-9dab-449dcb59a5b9>>> servo, <<<a35c0972-e514-477c-ab08-88676417cb5f>>> Dave, <<<526b5aa4-80d5-4c7a-96a5-9b6078b58ead>>> black C-HR. Exterior, night, a petrol station forecourt. Dave stands by his grey ASX at pump 2, facing us three-quarter, the black C-HR at pump 1 behind his shoulder with its Monsoor Motors plate frame. Holds still for a moment, then: Dave at his pump, meter still running, glances up at the car, looks back down at his meter, freezes, looks up again quickly, eyebrows up, mouth slightly open, watches it roll away, slow blink. Behind him the C-HR pulls away silently, red tail-lights shrinking down the road.
Emotion: genuine surprise turning into curiosity, never mugging.
Imperfections: a held breath before the second look; his hand stays on the nozzle; the head move stops slightly short.
Light: canopy key from above, red tail-light streaks behind him.
Camera: 50 mm eye level, locked off on a tripod with slight breathing, focus on Dave.
AUDIO: off.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**V6** · Seedance 2.0 std · start SF-V6 · audio ref Mia (approved take) · 18
```text
**Aspect ratio**: 9:16  **Resolution**: 720p  **Mode**: std  **Duration**: 4s
<<<37296861-4e5c-4308-9dab-449dcb59a5b9>>> servo, <<<ba7458bd-24a7-493f-8838-f74d52ca113b>>> Mia. Her lips follow the audio reference exactly.
Holds still for a moment, then: Mia, at night at a Perth service station, awake at the rear car window, chin on the sill, still face, eyes to her dad: "Dad... can we get one?", eyebrows lift slightly on the last word, holds the look.
Emotion: sharp, hopeful, deadpan.
Imperfections: one small blink in the pause after "Dad"; a wisp of hair moves; fingers shift on her backpack strap.
Light: warm shop-window light on her face, cool canopy spill on the roof, soft magenta neon behind.
Camera: 75 mm outside the open rear side window, three-quarter, slight handheld breathing.
AUDIO: Mia's line from the reference only, soft servo hum. No music.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**V10** · Cinema Studio 3.0 · start SF-V10s + end SF-V10e (Soul ID) · 20
```text
<<<d9dfe0fd-89ba-4fba-b719-ee33c0f0588b>>> our yard, <<<0bd837e0-5c67-4768-a4b4-a105fc5ed65c>>> Monsoor. Exterior, next morning, a sunny car yard with red brick paving and palms. Holds still for a moment, then: a badge-less black luxury muscle car rumbles in through the yard gate at walking pace, low and heavy, stops; its nose dips and settles. The driver's door opens; Monsoor steps out, one loafer flat onto the brick, rises, shuts the door with an easy push; dark aviators on, gold watch catching the sun; a warm smile as he sees Arfan off frame right, and he starts to walk toward him.
Emotion: big-hearted boss, unhurried, a good soul.
Imperfections: the body rocks once as the engine cuts; his hand rests on the roof a moment; the silk shirt moves in the breeze.
Light: hard morning sun from frame left, bounce off the brick, contact shadows under tyres and loafers.
Camera: 32 mm low angle near the brick, low tracking alongside the car, settling as he stands. Real speed.
AUDIO: off.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**V7** · Seedance 2.0 std · start SF-V7 (Soul ID) · audio ref "Good job." + "That means a lot." · 18
```text
**Aspect ratio**: 9:16  **Resolution**: 720p  **Mode**: std  **Duration**: 4s
<<<d9dfe0fd-89ba-4fba-b719-ee33c0f0588b>>> yard, <<<0bd837e0-5c67-4768-a4b4-a105fc5ed65c>>> Monsoor, <<<cde963a1-6dce-441f-b16d-fd74bad0f52e>>> Arfan in <<<eca28f45-7884-4495-ba6a-c63daadda53f>>>. Lips follow the audio reference, each mouth only on its own line.
Morning, outdoors in a sunny Perth car yard. Holds still for a moment, then: Monsoor rests his left hand flat on Arfan's right shoulder, one soft pat: "Good job." Arfan's shoulder dips under the hand, he looks at Monsoor, chin a touch down. Slow blink, small eyebrow lift, small smile becomes a real smile: "That means a lot." Glances down, then back up.
Arfan wearing his Ray-Ban Meta glasses, light green-tinted lenses, eyes visible.
Emotion: proud and fatherly; humble and moved.
Imperfections: his half-step toward Monsoor; fabric bunches under the fingers.
Light: hard sun from frame left, soft bounce fill.
Camera: 75 mm over Monsoor's right shoulder onto Arfan, slow push to a close-up.
AUDIO: both lines from the reference only, magpie, traffic. No music.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**V8** · Cinema Studio 3.0 · start SF-V8 · 20
```text
<<<d5da6271-1093-470d-8628-5d69ef5f882d>>> family home, <<<526b5aa4-80d5-4c7a-96a5-9b6078b58ead>>> black C-HR, <<<a35c0972-e514-477c-ab08-88676417cb5f>>> Dave, <<<ba7458bd-24a7-493f-8838-f74d52ca113b>>> Mia. Exterior, golden hour, a suburban street in Perth. Holds still for a moment, then: the black C-HR rolls up a family driveway at walking pace and stops, nose dips; Dave waits at the driveway edge, hands in pockets; the driver is only a shape behind the reflective windscreen. Then Mia runs out of the front door across the lawn in short uneven strides, slows with two quick steps. The grey ASX stays parked at the kerb.
Emotion: warm anticipation, then joy.
Imperfections: the car rocks once on its springs; Dave shifts his weight; her ponytail swings unevenly.
Light: low warm sun from frame left, long shadows to the right, sun glint sliding on the black paint.
Camera: 32 mm low at the kerb, short low tracking move with the car, then settles.
AUDIO: off.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**V9** · Cinema Studio 3.0 · start SF-V9 · 20
```text
<<<d5da6271-1093-470d-8628-5d69ef5f882d>>> family home, <<<526b5aa4-80d5-4c7a-96a5-9b6078b58ead>>> black C-HR, <<<cde963a1-6dce-441f-b16d-fd74bad0f52e>>> Arfan in <<<eca28f45-7884-4495-ba6a-c63daadda53f>>>, <<<a35c0972-e514-477c-ab08-88676417cb5f>>> Dave, <<<ba7458bd-24a7-493f-8838-f74d52ca113b>>> Mia. Exterior, golden hour, a suburban family driveway in Perth. Holds still for a moment, then: Arfan walks from the car to Dave, holds the keys out flat on his open palm; Dave lifts them off by the ring, looks at the car, grins; Arfan nods and steps back half a pace. Mia comes in, both palms on the car door, looks in the window. Arfan wearing his Ray-Ban Meta glasses, light green-tinted lenses, eyes visible.
Emotion: warm, simple, real; Arfan gives the moment to the family.
Imperfections: Arfan's palm stays open a moment after the keys go; Dave weighs the keys once; Mia's last two steps stutter.
Light: low sun behind them as a warm rim, soft sky fill on faces.
Camera: 50 mm eye level, slow gimbal push; the two men in a V about 35 degrees off the lens.
AUDIO: off.
Look: anamorphic, oval bokeh, real pores, natural colour, real speed.
Negative: no phone, no text, no logos, no slow motion, no morphing hands, no waxy faces, no frozen smile, no lens looks.
```

**Fallback (fuel-light cut)**
```text
FALLBACK (fuel-light cut, only if Meta or Ad Standards rejects the speed-camera version): no new video. Re-use the M4 take; recolour the comped flash amber; replace #9 with I-4b (low-fuel lamp ECU) and drop #10 (camera pass). Sound: shutter click becomes the designed low-fuel chime with a camera-like click on the lamp.
```


### C5. Lint results (`seedance_lint.py`, run 21 Nov 2026 with `/opt/miniconda3/bin/python -I`)

Seedance prompts were run with `--preflight --model seedance_2_0`. The CS 3.0 prompts were run through the content filter only, because the linter has no CS 3.0 spec. Two fixes made in the first pass:
- Prompts cut from 235–316 words (they failed "overlength").
- Wording changed:
  - "young man/woman" (age-marker FAIL) became the element plus a description;
  - "a beat" (violence-verb FAIL) became "a moment";
  - "skin" and "wet" (NSFW false positives) became "pores" and "rain-dark";
  - settings were added where the linter warned there was none.

| Prompt | Mode | Result | Words (linter) | Words without IDs | Findings |
|---|---|---|---|---|---|
| M1 | seedance_2_0 preflight | PASS (exit 0) | 180 | 161 | — |
| M2 | seedance_2_0 preflight | PASS (exit 0) | 180 | 162 | — |
| M3 | seedance_2_0 preflight | PASS (exit 0) | 175 | 159 | — |
| M4 | seedance_2_0 preflight | PASS (exit 0) | 176 | 159 | — |
| V4 | seedance_2_0 preflight | WARN (exit 0) | 201 | 169 | [WARN] long |
| V6 | seedance_2_0 preflight | PASS (exit 0) | 175 | 154 | — |
| V7 | seedance_2_0 preflight | WARN (exit 0) | 210 | 177 | [WARN] long |
| M5 | filter only (CS 3.0) | WARN (exit 0) | 208 | 203 | [WARN] long |
| V1 | filter only (CS 3.0) | PASS (exit 0) | 180 | 168 | — |
| V2 | filter only (CS 3.0) | WARN (exit 0) | 192 | 181 | [WARN] long |
| V3 | filter only (CS 3.0) | PASS (exit 0) | 163 | 152 | — |
| V5 | filter only (CS 3.0) | WARN (exit 0) | 199 | 181 | [WARN] long |
| V8 | filter only (CS 3.0) | WARN (exit 0) | 194 | 176 | [WARN] long |
| V9 | filter only (CS 3.0) | WARN (exit 0) | 218 | 189 | [WARN] long |
| V10 | filter only (CS 3.0) | WARN (exit 0) | 206 | 195 | [WARN] long |

The linter's word count includes the `<<<ID>>>` strings. Without them, every prompt is 152–203 words (M5 is the longest). "long" is a WARN, not a FAIL. No prompt has an open FAIL.

### C6. AI-tell reject list, per generation (reject the take on sight)

| Gen | Reject if |
|---|---|
| M1–M4 | A phone appears; the face drifts from the element; hands melt into the wheel; the car glides with no nose dip; the cluster shows readable invented digits; the gum bubble morphs into the face; the hair tuck melts the ear; the M3 glasses slide into his face; the M4 sunglasses duplicate or merge; even, flat light with no red signal; a frozen expression after the beat. |
| M5 | A burnout, smoke, a slide or any weaving; other cars or people; the 60 sign re-lettered; a floating car with no squat; the speed camera rendered as a person or a police car; generated slow motion. |
| V1 | Mia's face sharp and waxy (she must stay soft); a head turn over 10°; perfect, unchanging light (green must spill); floaty camera with no rig vibration. |
| V2 | The price board digits change; the nozzle floats or the hose vanishes; the queue drivers act (they must just wait); the wince becomes mugging; skin goes waxy in the canopy light. |
| V3 | The car slides with no weight or body roll; reflections don't move with the car; an exhaust or engine shimmer appears; a badge or plate text is generated. |
| V4 | Lips out of sync; the glasses vanish, darken or morph; a held grin or a look into the lens; a profile-to-front turn; extra fingers on the door; the ring on the wrong hand. |
| V5 | A whip-pan head move or a jaw drop; the plate frame re-lettered or garbled; the C-HR's tail-lights flicker or duplicate; the face drifts over 30°. |
| V6 | Lips out of sync; cartoon eyes or a grin; the face turns; hair morphs; the backpack changes colour. |
| V7 | The hand sinks into the shirt or sprouts fingers; Monsoor's face turns to camera; Arfan's lens tint goes dark; plastic skin in hard sun; a frozen smile; the SOLD tag re-lettered. |
| V8 | Mia's legs tangle or her feet slide; the car changes colour or wheels; the ASX vanishes from the kerb; even light with no long shadows. |
| V9 | Keys duplicate or vanish; finger-to-finger morphs; Dave and Arfan go profile to each other; the glasses tint changes from SF-V9. |
| V10 | Generated slow motion; the muscle car grows a badge; the loafer floats above the brick; the aviators change shape; Monsoor's face differs from the Soul ID frame; the gold chain flickers. |
| All stills | Soft at 100% (memory rule: sharp, textured); readable invented text; shadows that disagree with the key light. |
| Edit (all) | Every shot the same length; dead silence (never digital zero); a cut in a still pose instead of on movement. |

---

## (D) Music and SFX briefs

**Music.**
- Model: ElevenLabs Music v2.5. 39 s, **2 versions** (≈11.35 credits, from 8.44 × 39/29; quote first). Instrumental only.
- Prompt: "Instrumental only, no vocals. Original score for a 39-second warm comedy car commercial set in Perth. 120 BPM, 4/4, D minor moving to D major. Cheeky, warm, understated, premium; never cheesy, no stingers, no whooshes. Sections:
  - 0–6.4 s: sparse sub-bass pulse; a short riser cut dead at the 4.2 s camera flash, then a pulse back in, with a soft riser into 6.4.
  - 6.4–9.7 s: half-time groove (dry kick, snappy clap, round bass, muted two-note guitar), then a dead stop.
  - 9.7–11.8 s: silence.
  - 11.8–17.6 s: warm laid-back D-major groove, light funk guitar.
  - 17.6–21.5 s: one sustained clean guitar note.
  - 21.5–28 s: bright sunny groove with Rhodes, softer with a pad swell from 25 s.
  - 28–34 s: gentle lift, tambourine, rising bass from 31 s.
  - 34–39 s: thins to felt piano and bass, resolves on D major at 36 s, one clean final chord with a soft kick at 38 s ringing to 39 s."
- Negative styles: vocals, stingers, trailer booms, trap hats, anything resembling a known song, game or trailer.
- In the edit: 9.75–11.82 is muted whatever the model does; 4.20 drops out for 0.3 s under the shutter click; 22.05–23.20 is ducked under the muscle car. Slide sections onto the cuts; never retime the music.

**SFX.** Native audio is off, so everything is built:

| Source | Sounds |
|---|---|
| **Designed in-house, free** (ffmpeg `aevalsrc`, never a carmaker's sound) | Speed-camera shutter click + strobe tick · glam driver's tiny gasp (voice line) · low-fuel chime (falling two-note) · READY chime (soft rising two-note, 0.5 s) · sonic logo (READY motif on felt piano and glass) |
| **Mirelo, 2 × 10 s reels ≈ 5 credits** | R1: CBD indicator + crossing beeps · freeway rush · river breeze + bus · Northbridge club bass + neon buzz · **V8 SUV launch exhaust note (0.5 s, controlled, no tyre squeal)** · ASX idle + sleeping breath · servo canopy hum + idling queue swell · near-silent servo with tyre hiss and faint electric whine. R2: **muscle-car V8 rumble, blip, engine off, cooling tick** (the only loud engine) · yard magpie, flags, Albany Hwy · golden-hour suburb birds, distant mower, tyres onto concrete, child running on grass → concrete |
| **Foley/library** (licensed or recorded on a phone, free) | Door latch and clunk, boot on wet concrete, nozzle click, pump whirr, auto-shutoff clunk, POWER click, SOLD-tag press, loafer on brick, door thunk, shoulder pat, key jingle, front-door clack, palm on car door |

**Voices** (never altered: no pitch, speed or EQ changes beyond the shared high-pass and de-ess):

| Line | Source | Rule |
|---|---|---|
| "Hello mates." | `voice/Arfan-script-voice-LOCKED.wav` (v10) 4.50–5.40 | Locked; no regeneration |
| "That means a lot." | locked track 0.00–1.60 | Locked; "for me" is not used |
| "You choose the car! We bring it to your home!" | locked track 21.30–23.43 | Locked |
| "Good job." | Monsoor's **real cloned voice** only | Warm, unhurried, low and steady; short; one take chosen by ear |
| "Dad... can we get one?" | **New designed voice** (synthetic; never cloned from a real child) | Brief: Perth girl about 8–9, natural Australian vowels, a little sleepy, deadpan; "Dad..." trails off, about 0.4 s pause, "can we get one?" lifts slightly on "one"; ≤1.4 s; not cutesy, not American. Make 3 takes; Arfan picks by ear on headphones **and** a phone speaker; reject TTS artefacts; lock before V6 runs. |

**Mix (local ffmpeg, free).**
- Dialogue first: high-pass 80 Hz, light de-ess.
- Music 13 dB under dialogue (sidechain duck), rising to about 6 dB under in the gaps.
- Ambience about −32 LUFS under every shot, never digital zero. 9.75–11.82 has a −60 dBFS room-tone floor.
- Master: two-pass `loudnorm=I=-14:TP=-1.5:LRA=9`. QC on a phone speaker, headphones and mono, plus one muted watch.

---

## (E) Budget (exact maths; "honest total")

Prices quoted today with `estimate_*_cost`:
- CS 3.0, 4 s, 720p: 20.
- Seedance 2.0, 4 s, 720p: fast 10; std 18.
- GPT 2.6: high 2K 2.75; medium 1 (as given).
- `soul_2` 2K: 0.12 exact, rounded to 1 here.
- Kling 4.0 video edit at 1080p: 4/s (Enhance workflow preflight, 15 Nov). Today's text-to-video quote was 48.75 for 13 s.

| Item | Count × unit | Credits |
|---|---|---|
| Cast elements already made | — | 15.00 |
| Start frames, GPT 2.6 high | 16 × 2.75 (M1–M5, V1–V6, V8, V9, V10s, V10e edit, V7 edit) | 44.00 |
| Monsoor Soul ID frames, `soul_2` | 2 × 1.00 | 2.00 |
| On-screen stills, high (P-Mia, P-Brand) | 2 × 2.75 | 5.50 |
| Inserts, medium (I-1…I-15 + fallback I-4b) | 16 × 1 | 16.00 |
| Montage video, Seedance fast | 4 × 10 | 40.00 |
| Dialogue video, Seedance std | 3 × 18 | 54.00 |
| Hero video, CS 3.0 (M5, V1, V2, V3, V5, V8, V9, V10) | 8 × 20 | 160.00 |
| Voice lines ("Good job." from his clone; Mia's 3 takes; glam gasp) | quote first | 1.50 |
| Music, 2 versions × 39 s | 8.44 × 39/29 | 11.35 |
| SFX gap fill (Mirelo) | 2 × 10 s | 5.00 |
| **Production subtotal** | | **354.35** |
| Enhance (Kling 1:1, 1080p), 34 s story cut | 34 × 4 | 136.00 |
| **Planned total with Enhance** | | **490.35** |
| Quality reserve: 2 CS re-rolls with new start frames (2 × 22.75), 1 Seedance std re-roll (20.75), 3 high + 3 medium still re-rolls (11.25) | | 77.50 |
| **Ceiling if every reserve item is used** | | **567.85** |

**What each extra buys**
- **Within 350: not possible.** Production alone is 354.35, 4.35 over the cap. The client's additions (M5 launch + start frame, Monsoor Soul ID frames, fallback insert) account for the rise. To land under 350 you would make M5 Seedance fast (−10) and skip the fallback insert (−1): 343.35, leaving 6.65 reserve and a local Lanczos upscale (softer).
- **+136 Enhance:** a true 1080p re-render. It gives one consistent texture across stills and video (it also fixes "pasted-in" stills), shot-by-shot colour matched back to our grade, and a QA report (SSIM, cut timing).
- **+77.50 reserve:** the margin to reject every AI tell in C6 instead of accepting it.
- **Conditional extras:**
  - If Monsoor has **no voice clone yet**, creating one costs about 40 (house figure; quote first).
  - The **Topaz** fallback upscale has no price preflight; test it on one 4 s clip and read `transactions` before using it more widely.

---

## (F) Pre-flight checklist (before every paid call)

1. The previs and storyboard panel for that shot are checked: framing, eyelines, light direction.
2. The start frame is checked at 100% against the element sheet, `look-lock.png`, the continuity rows (outfit, glasses state, ring right / Seiko left, filler side, flap state, plate frame) and the expression.
3. Monsoor shots: the frame came from **soul_2 + Soul ID → GPT edit**, never element-only.
4. The prompt is the exact text in C4. Seedance prompts pass `seedance_lint.py` with no FAIL. Element IDs are correct; no retired ID (`a28f6297`, `4d888179`, `9148e692`, `10f68c0b`, `e32227b7`, `9e0c9644`, `52931b72`, `0a9fe91f`, `c349d712`, `04d425c7`, `a9b1d482`, `f259a71f`, old extras) appears.
5. Dialogue shots: the audio reference is the **locked** clip (or the approved Mia/Monsoor take), with room-tone padding only.
6. Settings: 9:16, 720p, 4 s, audio off, `folder_id` set. Quote shown; the running total is stated before generating.
7. After the job:
   - Inspect start, middle and end frames at full size, plus face and hand crops.
   - Run C6 (AI tells) and the **not-pasted-in** checks: contact shadows match the key light; reflections on paint, wet concrete, lenses and the Seiko; eyelines (Dave → C-HR, Mia → Dave, Arfan → Monsoor); scale (Mia about 1.3 m); RHD; plates blank; no generated text; light continuous within the location; real speed.
8. A fault seen twice: fix the reference (start frame or element), not the prompt. Log the job.

**Before upload:**
- The dash labels and super match REAL-NUMBERS basis A.
- 45,000 km is checked against the real car's odometer, listing and auction sheet.
- MD32748 is on the card.
- The caption carries the full disclaimer and "Dramatisation; AI-generated scenes; fictional family".
- Meta's AI-info label is on and the C2PA metadata is kept.
- No #GTA hashtags.
- A muted watch by someone new still reads the story.

---

## (G) Open items for the client

| # | Item | Needed by |
|---|---|---|
| 1 | **Exact odometer** of the black C-HR (shown as 45,000 km; confirm the digits; it must match the listing and auction sheet). If the car sells while the ad runs, re-edit or pull the ad. | I-10 comp |
| 2 | **Monsoor's voice clone**: confirm it exists and he has consented to "Good job." If none exists, approve the ≈40-credit clone and supply a clean sample. | before V7 |
| 3 | **Mia's voice**: approve one of the 3 synthetic takes by ear. | before V6 |
| 4 | **Real artwork** for the plate frame, door decal and SOLD tag (vector or high-resolution PNG). | SF-V5, I-11, I-12, V7, P-Brand |
| 5 | Verify on the real car: the **filler side** (C-HR right rear? ASX left rear?), the **POWER button** position, and that our JDM C-HR has the same 1.8 hybrid as the AU-rated 4.3 L/100km car. | start frames |
| 6 | **Legal**: the brand line covers ASX and C-HR only, but the montage labels show Seltos 6.8, CX-3 6.3 and Kona 6.6 (official). The caption lists all five. Confirm, or drop the asterisk from the montage labels. | edit |
| 7 | **WA second-hand vehicle ad rule**: the ad now shows *one specific stock car* being sold. Ask whether rego, year, cash price and address must go in the copy (MARKETING e-5). | upload |
| 8 | Dave's ASX variant (2.0 CVT at 7.6) confirmed on the Green Vehicle Guide. | label lock |
| 9 | Approve **+136** for Enhance, and whether to hold the 77.50 quality reserve (honest total 490.35, ceiling 567.85). | before post |
| 11 | Arfan's shirt: black Hawaiian print or keep the black linen (IDs unchanged until confirmed; a new outfit element would add a sheet and re-made Arfan start frames). | before SF-V4 |
| 12 | **Speed-camera gag: compliance (client accepted the risk 21 Nov 2026).** The FCAI Voluntary Code of Practice for Motor Vehicle Advertising (administered by Ad Standards) says ads must not depict speeding or unsafe driving; showing 64–67 km/h in a signed 60 zone is speeding, even though the camera "catches" her. **The client accepted the FCAI/Ad Standards risk on 21 Nov 2026.** Mitigations: a controlled straight launch, an empty street, no burnout or weaving, about 1.95 s total, the consequence as the payoff, and no glorifying copy. Meta may also reject or limit the ad. **Fallback cut ready:** #9 → I-4b (low-fuel lamp pops on), #10 dropped (its 0.45 s goes to #11), the flash on her face recoloured amber, and the shutter click becomes a click + the designed low-fuel chime. No new video credits; only I-4b (1). | before upload |
| 10 | The muscle car joke (the boss drives the only gas-guzzler): confirm Monsoor is happy to be the punchline. | before V10 |

---

## (H) Post-production pipeline

What the Higgsfield workflows actually support (read today, no generation):
- **video-montage:** assembles finished clips with ffmpeg in `sandbox_exec` (hard cuts by default; join verification), handles soundtrack changes, and owns caption transcription, alignment, burning and checks (`transcribe_words.py`, `caption_guard.py`, `caption_placement.py`).
- **video-editing (Higgsedit CLI v0.14):** a native project; text with shaped fonts, rectangles, masks, keyframes, transitions and a 2.5D camera; renders H.264/HEVC 10-bit. It has **no native LUTs or shader adjustment nodes**, so colour grading is not done there.
- **higgsfield-enhance-video:** Kling 4.0 video edit, 1:1 to 1080p, steered by a timed prompt that pins every cut, line and text. It splits into parts of ≤15 s and costs **4 credits/s at 1080p**. `finish.py` retimes and **colour-matches every shot back to the source**. Expected SSIM is about 0.83; faces, logos and dialogue held in tests.
- **upscale_video:** Topaz (1080p/2160p, aspect-based) or ByteDance (`aigc` preset). No prompt and no price preflight.

**Recommended order**

| Step | Where | What happens | Cost |
|---|---|---|---|
| 1 | Higgsfield | Generate every still and video at 720p (stills 2K), audio off | in E |
| 2 | Local ffmpeg (`qj_post.py`) | Conform to 24 fps CFR. Cut the windows in B2. Animate stills (2–4% push from the 2K source). **Per-shot colour match**: white balance and exposure matched within each location to `look-lock.png`, one palette for the ad, no heavy grade | free |
| 3 | Local ffmpeg | Assemble the **picture-only story cut 0–34.00** with the locked dialogue as guide audio. **No supers, labels, captions or digit comps yet.** In-world artwork already sits in the start frames (plate frame, decal, SOLD). | free |
| 4 | Enhance (Kling) | `prep.py` splits 34 s into 3 parts (≈12 + 11 + 11). The timed block names every one of the 40 story cuts and beats, spells "MONSOOR MOTORS" plate frame/decal and "SOLD" exactly, and states "dash and pump screens blank, no captions or subtitles". `finish.py --audio source` (retime + colour match back to step 2). Accept a part when its cuts are ≤2 frames off and faces pass at 100%. Re-run a failing part with the same prompt, or fall back to Topaz for that part | **136** (+Topaz test if needed) |
| 5 | Local ffmpeg | **Texture and sharpness consistency**: measure each shot and apply light unsharp only where a shot is softer. **No grain filter** (house rule). Kling has already unified the stills' texture with the video | free |
| 6 | Higgsedit (video-editing) | All graphics over the 1080p master, in Montserrat (`fonts add`): hook and fuel super (frosted navy pill, warm white); **dash labels** (#3, 5, 7, 10, 12, 25) placed on each cluster; pump digits (#15, 22); READY glow; plate-frame/decal re-comp only if Kling softened them; captions (Montserrat SemiBold 46 px, centre about y 1400, inside y 250–1520); watermark top left at 55%; **brand build and legal line** on #40. Render HEVC 10-bit, 10 Mbps | no credit price listed (sandbox) |
| 7 | video-montage scripts | Caption QA only: `transcribe_words` on the final audio vs the authored lines, and `caption_guard`/placement against the Reels UI zones. Re-burn only if a check fails | no credit price listed |
| 8 | Local ffmpeg | **Final mix** (D) to −14 LUFS / −1.5 dBTP; mux onto the Higgsedit picture with a stream copy; verify duration 39.000 s, streams, every join, first and last frames | free |
| 9 | Meta upload | AI-info label on, caption with the disclaimer, the 15 s cut from MARKETING (j) built from the same masters | free |

**Why this order:**
- Text never passes through a generative pass, so Kling cannot re-letter a claim or a number.
- Colour is matched once before Enhance and restored by `finish.py`.
- The legal line and dash labels are added last and stay pixel-exact.
- The mix stays local and lossless until the final mux.
