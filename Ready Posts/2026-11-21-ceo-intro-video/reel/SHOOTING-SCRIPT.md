# "Queue Jump": Higgsfield shooting script (v1, for sign-off before any video credit)

29 s, 9:16, 1080x1920 (made at 720p, upscaled on this Mac). 28 s story + 1 s brand. Project: **Monsoor Motors - CEO Intro** (Cinema Studio).
Free previs to check first: `QJ-29s-Previs.mp4`, `QJ-Storyboard.png` (Blender, simple blocking; framing, timing and moves are what to judge, not the looks).

## 0. Locked assets (always attach; never re-describe)
| Role | Element | ID |
|---|---|---|
| Arfan (face + personality) | `Arfan-CEO-Final` | `cde963a1-6dce-441f-b16d-fd74bad0f52e` |
| Arfan's outfit | `Arfan-CEO-Outfit-Locked` | `7a6ad32a-7dac-499e-85d0-8a4e59329622` |
| Monsoor (body sheet) | `MA-Monsor-Owner-v2` | `9148e692-8269-44aa-86be-60b5b10a11b7` |
| Monsoor (real face, 8 photos) | `MA-Monsor-Real` | `4d888179-4700-4505-b76b-c732edaa7a6e` |
| Dave (fictional dad) | `Dad-Dave` | `e32227b7-4d2a-4b4b-a6e1-2a238cae8755` |
| Mia (fictional kid) | `Kid-Mia-v2` (use this; v1 retired: frizzy hair, cartoon grin) | `9e0c9644-0ae8-4730-82e3-c08a1fa2c2c3` |
| Montage driver 1, tradie | `Extra-Tradie-Ute` (drives a petrol small SUV) | `f8d7835b-7a2a-459e-a171-083e4ee8cf86` |
| Montage driver 2, nurse | `Extra-Nurse-SUV` | `f93882f3-a8d6-4d7c-b29c-f0b419717bf4` |
| Montage driver 3, retiree | `Extra-Retiree-Sedan` (drives a petrol small SUV) | `d56b1059-5bdc-47d2-b72c-1af5edfeec4e` |
| The car | `Monsoor-CHR-Hybrid-Black-Sheet` | `526b5aa4-80d5-4c7a-96a5-9b6078b58ead` |
| Night servo | `Perth-Servo-Night` | `37296861-4e5c-4308-9dab-449dcb59a5b9` |
| Our yard (real) | `Monsoor-Yard-Victoria-Park` | `d9dfe0fd-89ba-4fba-b719-ee33c0f0588b` |
| Family home | `Family-Home-Driveway` | `d5da6271-1093-470d-8628-5d69ef5f882d` |
In a prompt, an element is written as `<<<ID>>>` (my tools) or `@Name` (web app).

## 1. Look and camera (commercial, not cheap)
- Cinema camera feel, prime lenses (24 / 28 / 35 / 50 / 85 mm), shallow focus on faces, deep focus on wides.
- Night servo: lit only by the canopy downlights, the price board and the warm shop window; wet reflective concrete; cool-white vs warm contrast.
- Yard: hard midday Perth sun with soft fill (no squinting faces), real brick and flags.
- Home: golden hour, warm low sun from the left.
- Moves: dolly push-ins, gimbal arcs, a low car-rig track, a crane. One clean move per shot, real speed, cut on movement.
- Acting: understated and natural. Arfan confident, dry humour, half-smile, never performing. Monsoor steady, open palm, slow head turn (his 3MT video).
- **AI Director (Cinema Studio 4.0) dropdowns in the web app** (their IDs are not exposed to my tools): Film setup = Commercial / Modern digital; Camera = full-frame cinema; Lens = the mm in each shot; Lighting = as each shot says; Color palette = Natural; Pacing = Brisk for shots 1–3, Natural for 4–7. Keep camera and light in the dropdowns and the prompt to action, order and emotion, so the two don't fight.

## 2. Generations (grouped by location, the tutorial way)
Each generation: Seedance 2.5 or Cinema Studio 4.0 (same price: 7 credits a second at 720p), mode `omni_reference`, a **start frame** (made first as a still, 1 credit, approved before the video), the listed elements, the voice clip as `audio_references` where a line is spoken, `generate_audio` on for ambience.

### G1 Servo hook (shots 1, 2a, 2b, 2c) · 8 s · 56 credits
Start frame: the price board, low angle, queue lights behind. Elements: Servo, Dave, Mia. Dave's car: a real **2021 Mitsubishi ASX LS 2.0 petrol** (grey), shown as his ordinary family car, never mocked. Chosen to match the price band (see 2c).
Prompt (multi-shot, in order): "Night at a busy Perth servo. Shot 1 (0–3 s, 50 mm, low slow push-in): the roadside price board ticks up one digit, the long queue's headlights behind it. Shot 2 (3–5 s, 24 mm crane down): the queue of utes and SUVs stretches back to the road, engines idling, exhaust haze. Shot 3 (5–6.5 s, 50 mm slow dolly): Dave at pump 2 watches the total climb, then lets his head drop, a quietly pained, funny look. Shot 4 (6.5–8 s, 85 mm through the rear window): Mia asleep in the back seat, cheek squashed on the glass. Real night light from the canopy and the shop, wet concrete, tack-sharp, natural skin texture."

### G2 Arrival + hello (shots 3, 4) · 7 s · 49 credits
Start frame: low car-rig view of the black C-HR on the road beside the queue. Elements: Servo, C-HR, Arfan, outfit, Dave.
Audio reference: "Hello mates" cut from the locked track.
Prompt: "Shot 1 (0–3 s, 24 mm low tracking alongside): the black C-HR Hybrid glides past the queue in silence on electric power, swings into the free pump lane. The servo goes quiet; heads in the queue turn. Shot 2 (3–7 s, 50 mm slow gimbal arc): Arfan steps out, easy and confident, glances at the queue with a half-smile, gives a small nod and says 'Hello mates.' He tops up; a tiny shrug as if to say 'what?'. Dave stares from the next pump."

### G3 "Can we get one?" (shot 5) · 4 s · 28 credits
Start frame: over Dave's shoulder, the C-HR pulling away, Mia's face at the back window. Elements: Servo, Dave, Mia, C-HR.
Prompt: "28 mm over Dave's shoulder. The C-HR pulls away into the night. Mia, now awake at the back window, deadpan: 'Dad... can we get one?' Dave slowly turns his head to her." (Mia's line from the video's own audio.)

### G4 The yard (shots 6a, 6b) · 6 s · 42 credits
Start frame: wide at our real yard, Monsoor holding out the keys to Dave, Mia bouncing, the C-HR behind. Elements: Yard, Monsoor (both), Arfan, outfit, Dave, Mia, C-HR.
Audio references: Monsoor "Good job." (new, his cloned voice) and Arfan "That means a lot for me." (locked track + new "for me").
Prompt: "Shot 1 (0–2.5 s, 35 mm wide, slow push): midday at the Victoria Park yard, Monsoor hands Dave the keys with an open palm, steady and warm; Mia bounces. Shot 2 (2.5–6 s, 85 mm two-shot, push-in): Monsoor turns to Arfan, rests his hand on Arfan's shoulder: 'Good job.' Arfan looks at him, humble, chin a touch down, a small smile: 'That means a lot for me.'"

### G5 Home (shot 7) · 5 s · 35 credits
Start frame: low at the kerb, golden hour, the C-HR rolling into the driveway. Elements: Home, C-HR, Dave, Mia.
Audio: Arfan voice-over "You choose the car! We bring it to your home!" (locked track) laid in the edit.
Prompt: "35 mm low at the kerb, then a slow crane-up pull-back. Golden hour. The black C-HR rolls into the family's driveway; Mia runs out to it; Dave stands on the lawn, looks at the car, then down the street, quietly pleased."

### Brand (shot 8) · 1 s · free (made in-house)
Logo, 0434 137 393, small line: MD32748 · fuel source · AI-generated scenes.

## 2b. The fuel claim ("open marketing", Arfan, 21 Nov 2026)
On screen in shot 4: **"Half the fuel of his ASX.*"** Source line on the brand card: "*Real-world tests: Mitsubishi ASX 2.0 petrol 10.4 L/100km (WhichCar small SUV test) vs Toyota C-HR Hybrid 5.2 L/100km (RACV road test)."
Comparative advertising is legal in Australia when it is accurate, sourced and not misleading. The two figures come from two different real-world tests, so both are named. The ASX is shown as Dave's ordinary car, not mocked. Backup claim if a single-test basis is wanted: same car, official figures, C-HR Hybrid 4.3 vs C-HR 1.2T petrol 6.4 L/100km ("about a third less fuel").

## 2c. Price match (Arfan, 21 Nov 2026)
Market asking prices found 21 Nov 2026: 2018 Toyota C-HR Hybrid Japanese imports about $26,650–$30,990 drive-away (grabacar.au, onlycars); Mitsubishi ASX petrol in Perth: 2018 LS about $20,990, 2019 ES about $22,850, 2020–2021 LS mid-$20k (CarsGuide, CarAdvice, Westside Auto). So the like-for-price rival is a **newer petrol ASX (2021 LS)**. The ad's logic: with about $25–30k, a Perth buyer can have a newer petrol ASX or a Japanese-import hybrid C-HR that uses half the fuel.
"Same budget" goes on screen only with **our** C-HR's actual drive-away price (Arfan to supply); never the market range.

## 3. Sound (mandatory, in budget), the Higgsfield way
- **Native audio first:** Cinema Studio 4.0 makes sound in the same generation as the picture (Sound on). Every generation prompt ends with an AUDIO line naming the ambience and the exact effects, and "no music" (music is added in the edit so it stays consistent). Source: Higgsfield's Cinema Studio 4.0 guide.
  - G1 AUDIO: night servo hum, idling engines, price board clicks, pump whirr and clunk, distant traffic. No music.
  - G2 AUDIO: tyre hiss on wet concrete, no engine sound (electric), the servo hum drops away; car door thunk, nozzle click. No music.
  - G3 AUDIO: the C-HR fading away, servo hum, Mia's line. No music.
  - G4 AUDIO: midday yard ambience, a magpie, distant Albany Highway traffic, keys jingle, footsteps on brick. No music.
  - G5 AUDIO: suburban golden hour, birds, a distant lawnmower, tyres on the driveway, Mia's footsteps. No music.
- **Dialogue:** Arfan's lines cut from his locked track and attached as the audio reference so lip movement follows his real delivery; "for me" (0.5) and Monsoor's "Good job" (0.5) generated in their cloned voices. Keep the same voice description in every scene where a character speaks.
- **Edit tricks from their ads:** switch the sound to the next location just before the picture cuts; cut on an action (the nozzle click, the key handover); let the arrival gag go nearly silent; start the last voice-over as the home shot begins so the end isn't silent.
- **Music:** ElevenLabs Music v2.5, instrumental, 2 versions (8.44): playful and confident, drops out for the silent arrival, returns under "Hello mates", builds to home, buttons on the logo.
- **Mix:** dialogue first, music about 13 dB under, ambience under every shot, loudness -14 LUFS.
- **Gap-filler effects** (Mirelo) only if a native take is missing something: budget 5.

## 3b. Learned from Higgsfield's channel (applied above)
- Grey-background sheets, three-quarter locations, test the pair before video, lock as named elements, label references with the names used in the prompt.
- One camera move per shot; set Genre, Era and Tempo first; pick the colour preset before generating; don't ask for fast cuts when Tempo is "single shot".
- Multi-shot prompts: several shots in one generation (they ran 9 shots in a 26 s prompt), then cut the best parts.
- Fix instead of regenerating: edit a frame (sign, text), object-swap into a good take, or extend a good take forward (Sequel) instead of re-rolling.
- On-screen text always from our own locked graphics, never generated.
- Services ad formula: hook with a pain point, show the result, close with an offer. Test one change at a time; track hook rate, CTR and cost per lead.
Sources: Higgsfield AI YouTube: "I Made An AI Commercial For a Delivery Brand From Scratch", "I Spent 72 Hours Making a Commercial with AI", "The Cheapest Way to Make an AI Short", "How I Make Realistic AI Short Films Using Seedance 2.5", "The Newest Workflow For Ultra Realistic AI Characters", "How We Made an AI Short Drama That Looks Like a Real Movie", "GPT-6 Astra Changed Meta Ads Forever!"; higgsfield.ai blog "Cinema Studio 4.0 complete guide".

## 4. Budget (cap 250)
| Item | Credits |
|---|---|
| Elements already made (dad, kid, servo, yard, home) | 5 |
| Start frames, 5 × medium | 5 |
| Video G1–G5 at 720p (30 s × 7) | 210 |
| Voice: "for me", "Good job" | 1 |
| Gap-filler sound effects (native audio covers most) | 5 |
| Music (2 versions) | 8.44 |
| **Total** | **≈ 234** (16 spare: one 2 s fix, or a Sequel extension of a good take) |
No video drafts: the Blender previs plus the approved start frames are the test, so every video credit goes into a final.

## 5. Order of work
1. You approve the previs and this script. 2. Five start frames (5 credits), you approve each. 3. Voice lines and sound effects. 4. G1–G5 videos, checked shot by shot against the storyboard (fix the reference, not the prompt, if a fault repeats). 5. Edit, mix, captions, brand card, upscale. 6. Truth checks, then upload with Meta's AI label.

## 6. Pre-flight check before every paid generation (no surprises)
Before:
1. Look at the previs frames of that scene (start, middle, end) and the storyboard panel: framing, who is where, eyelines, light direction.
2. Check the start frame at full size against `CONTINUITY.md` (props, outfit, car side, flap state) and `EMOTION-AND-SOUND.md` (expression).
3. Dry-read the prompt: every element named, action order matches the storyboard, one camera move per shot, AUDIO line present, no text requested, no extra people.
4. Confirm the AI Director dropdowns match the look bible (same camera, palette, era) and the price shown next to Generate.
5. Say the cost before generating; keep the running total under 250.
After:
6. Inspect three frames at full size (start, middle, end) plus a crop of each face and hands; run the "not pasted in" checklist; listen to the native audio.
7. If a fault appears twice, fix the reference, not the prompt. Log every job in the generation log.

## 7. Real numbers locked (Arfan, 21 Nov 2026)
- Our black C-HR Hybrid odometer: **45,000 km** (given by Arfan; shown as an edit label on the dash shot, e.g. "45,0xx km" format exactly as he confirms).
- Montage cars: petrol small SUVs in the same $25–30k used band; figures in `roles/REAL-NUMBERS.md`.
- Fuel super: "Over 40% less fuel than his ASX.*" — *Official combined: ASX 2.0 7.6 vs C-HR Hybrid 4.3 L/100km.

## 8. FINAL CAST (21 Nov 2026, supersedes the element table above for people)
Dress code: Arfan and Monsoor fixed; everyone else Gen Z Miami-meets-Perth.
| Role | Element | ID |
|---|---|---|
| Arfan (fixed: black linen, coffee gurkha trousers, Ray-Ban Meta: clear at night, green tint by day) | `Arfan-CEO-Final` + `Arfan-CEO-Outfit-Locked` | `cde963a1-6dce-441f-b16d-fd74bad0f52e` / `7a6ad32a-7dac-499e-85d0-8a4e59329622` |
| Monsoor HERO (fixed: navy textured shirt, charcoal trousers, dark sunglasses by day) | `MA-Monsoor-Hero` (+ `MA-Monsor-Real` for face) | `a28f6297-980e-409c-9945-ca502821d5b0` / `4d888179-4700-4505-b76b-c732edaa7a6e` |
| Dave | `Dad-Dave-Miami` | `52931b72-32f5-4d4b-b915-6aaa73ef3eff` |
| Mia | `Kid-Mia-Miami` | `0a9fe91f-b6a3-4f23-a4ee-9de8d98c85e1` |
| Montage: Gen Z guy (small SUV) | `Driver-GenZ-Guy` | `c349d712-4f19-43c3-82aa-6e8d15620ce8` |
| Montage: Gen Z woman (small SUV) | `Driver-GenZ-Woman` | `04d425c7-f75e-4950-b492-d8beb4af43c2` |
| Montage: retiree (small SUV) | `Driver-Retiree-Miami` | `a9b1d482-73dd-4beb-a209-44d1426c34e4` |
| Montage: glam driver (badge-less luxury V8 SUV) | `Driver-Glam-V8` | `f259a71f-a7d2-4f57-87cc-f11ed2523fa4` |
Retired: Dad-Dave, Kid-Mia, Kid-Mia-v2, Extra-Tradie-Ute, Extra-Nurse-SUV, Extra-Retiree-Sedan (delete in web app).
Odometers: our C-HR 45,000 km (real); every other car a random, believable reading (about 12,100 km a year in WA).

## 9. Monsoor hero, approved route (21 Nov 2026, supersedes section 8 row for Monsoor)
- Element `MA-Monsoor-Boss` `8eab65a7-d3d1-4b41-a3c3-49c91bf27208`: warm-hearted GTA-style boss ("a good soul"): navy silk camp-collar palm shirt, gold rope chain, gold watch, charcoal trousers, loafers, dark aviators by day.
- Face ALWAYS via Soul ID `7d5bf600-ee1b-484d-a95f-6bfae7b6e5af` (soul_2) start frames, then costume edit, then video. The element-only face route was rejected by Monsoor on 20 Nov.
- Build widened toward his real stocky build; arms read slightly gym-muscular. **Show Monsoor before locking.**
- Voice: his real cloned voice only; warm, low, unhurried.
- Delivery car: our black C-HR (no white C-HR exists).
- New shot: Monsoor arrives at the yard in a badge-less black luxury muscle car (the only loud engine in the ad).

## 10. Arfan scene outfit for this ad (21 Nov 2026, Arfan's request; replaces black-linen look in THIS ad only)
- Element `Arfan-Outfit-CrimeDrama` `10f68c0b-8ac3-4cea-8da7-62c55afbdb59` + face `Arfan-CEO-Final` `cde963a1-6dce-441f-b16d-fd74bad0f52e`.
- Black matte camp-collar shirt, thin silver chain, sand linen blazer open, coffee gurkha trousers, black Chelsea boots, Seiko olive dial (left), silver ring (right), Ray-Ban Meta: clear at night, green by day.
- Pairing logic: Monsoor = navy + gold (the boss); Arfan = black/sand + silver (the right-hand man). Never the same colour block in a two-shot.

## 11. LOCKED CAST FOR THE SHOOT (21 Nov 2026, final; overrides sections 8-10)
| Role | Element | ID | Source |
|---|---|---|---|
| Arfan (face) | `Arfan-CEO-Final` | `cde963a1-6dce-441f-b16d-fd74bad0f52e` | locked |
| Arfan (outfit, his LOCKED black linen look; crime-drama outfit rejected) | `Arfan-CEO-Outfit-Locked` | `7a6ad32a-7dac-499e-85d0-8a4e59329622` | locked |
| Monsoor (boss; face via Soul ID `7d5bf600-ee1b-484d-a95f-6bfae7b6e5af`) | `MA-Monsoor-Boss` | `8eab65a7-d3d1-4b41-a3c3-49c91bf27208` | Monsoor to approve |
| Dave | `Dave-Real` | `a35c0972-e514-477c-ab08-88676417cb5f` | nano_banana realism pass |
| Mia | `Mia-Real` | `ba7458bd-24a7-493f-8838-f74d52ca113b` | nano_banana realism pass |
| Driver Gen Z guy | `Driver-GenZ-Guy-Real` | `f2a7b2b7-5837-4e58-8b9a-58fc908d7663` | in-car only |
| Driver Gen Z woman | `Driver-GenZ-Woman-Real` | `b77e0ccd-9139-4914-9e86-6ace90669d6e` | in-car only |
| Driver retiree | `Driver-Retiree-Real` | `eefa2c79-d3b5-4572-9a53-b0139fb58f3e` | in-car only |
| Driver glam (V8) | `Driver-Glam-Real` | `0b6631a2-04b5-4809-9b49-31acf7df8db3` | in-car only |
Every other people element is retired for this ad.
