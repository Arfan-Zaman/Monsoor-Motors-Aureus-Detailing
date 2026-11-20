# "Queue Jump" v5: content and sound plan (Content Lead + Sound Designer)

**39.0 s, 9:16, 1080×1920: 34.0 s story + 5.0 s branding.** Plan only: nothing generated, nothing committed.

**Built on**
- the locked story spine (21 Nov 2026)
- the client updates: 39 s, 350 credits, one generation per shot, real numbers, minimal legal text
- the story fixes: the price board doesn't tick, keys handed over in Dave's driveway, the yard holds the "Good job" moment, the fuel super is "Over 40% less fuel than his ASX.\*", and the hook text is "Tuesday night. Perth."

**What this replaces:** the timings in `EMOTION-AND-SOUND.md` §2 and in `qj_post.py` (`SUPERS`, `CAPTIONS`, `CUTS`, `SHOTS`, `END`). The emotion map in §1 still applies.

**Sound rule:** every sound is motivated by the picture. There are no inserted gags or stings. The humour is situational:
- the silence of the C-HR against the idling queue
- Dave's long pump run against Arfan's quick stop
- the silent start, which comes back as Dave's own silent start in the driveway
- Dave's nozzle clicking off only after Mia's line

**Beat grid:** 120 bpm (beat 0.5 s, bar 2.0 s).
- Story turns land on bar lines: 4.0, 10.0, 12.0, 18.0, 30.0, 34.0, 36.0 and 38.0.
- Other cuts land on a beat or an 8th note, within ±2 frames; inside that window, pick the frame with movement in it.
- 33 story shots, about 1.0 s on average. The hero dialogue shots run 2.0–2.25 s.

**Dialogue** (measured with silencedetect on `voice/Arfan-script-voice-LOCKED.wav`):
- "Hello mates": 0.70 s.
- "That means a lot": 1.56 s, then "for me" (new, about 0.5 s).
- CTA: 0.87 + 0.31 gap + 0.95 s.
- **Still to record:** Mia ≤1.3 s, Monsoor "Good job" ≤0.5 s.

**Numbers:** `roles/REAL-NUMBERS.md` doesn't exist yet, so placeholders are shown in [brackets]. Readouts show only L/100km and the odometer, with no model names or badges.

---

## (a) Timeline 0.0–39.0 s, every shot timed
Key: **Src** = AI (its own generation) or **PH** (real phone footage, free and truthful; see critique 1–2). **SP** = super, **CAP** = caption, **DX** = dialogue, **FX** = effects, **AMB** = ambience, **M** = music.

### 0.0–4.0 s: red-light montage. Three drivers, the last is Dave with Mia asleep.
**SP 0.20–3.90: "Tuesday night. Perth."** stays on screen across all the cuts. The light runs from dusk to night, with anamorphic flares on the traffic lights and the neon.

| # | Time | Len | Src | Picture | Sound (motivated, a different sound per cut) |
|---|---|---|---|---|---|
| S1 | 0.00–0.75 | 0.75 | AI | CBD, St Georges Tce, wet dusk: an office worker at a red light, indicating | **Indicator tick-tock**, rain on the roof, pedestrian-crossing tick. M: sub pulse only |
| S2 | 0.75–1.25 | 0.50 | PH | His cluster: **[CAR-A L/100km] · [CAR-A odometer]**, and the low-fuel light comes on | **Low-fuel chime** on the cut. We design it in-house: a falling two-note, not any carmaker's sound |
| S3 | 1.25–1.75 | 0.50 | AI | Northbridge neon: a P-plater stares at the dash; the light has gone green | **A horn from the car behind** at 1.5. Neon buzz, muffled club bass |
| S4 | 1.75–2.25 | 0.50 | PH | Her cluster: **[CAR-B L/100km] · [CAR-B odometer]** | Muffled cabin, her groan under her breath |
| S5 | 2.25–3.00 | 0.75 | AI | Albany Hwy at the last of the sunset: Dave lets out a long breath | **His exhale** at 2.45, the ASX idling |
| S6 | 3.00–3.50 | 0.50 | PH | Dave's cluster: **[ASX 10.4] · [ASX odometer]** | Cabin hum |
| S7 | 3.50–4.00 | 0.50 | AI | Mia asleep in the back, 85 mm | Her soft breathing. M: a short soft riser from 3.25 |

### 4.0–10.0 s: servo. Only Dave's pump meter ticks; the price board is static.
| # | Time | Len | Src | Picture | Text | Sound |
|---|---|---|---|---|---|---|
| S8 | 4.00–5.50 | 1.50 | AI | Servo wide, 24 mm: the queue, a static price board, Dave at pump 2 | | **M DROP on 4.0**: half-time kick and clap, round bass, a muted tense-playful guitar. AMB: canopy hum, idling engines |
| S9 | 5.50–6.50 | 1.00 | PH | Dave's pump meter ticking fast | | **Pump motor whirr, fuel flowing** (bowsers don't ding) |
| S10 | 6.50–8.00 | 1.50 | AI | Dave, 50 mm slow dolly: his eyes follow, his head drops a little, the "of course" smirk | | The whirr carries on |
| S11 | 8.00–9.00 | 1.00 | PH | The meter, much higher | | The whirr carries on |
| S12 | 9.00–10.00 | 1.00 | AI | The queue: drivers slumped, one eating | | **The idles swell** as the queue creeps forward |

### 10.0–17.0 s: silent glide, "Hello mates", quick top-up, the good number
| # | Time | Len | Src | Picture | Text | Sound |
|---|---|---|---|---|---|---|
| S13 | 10.00–11.50 | 1.50 | AI | Low car rig: the black C-HR glides past the queue | | **M cuts dead on 10.0 (bar 6). AMB drops 12 dB in 0.3 s.** Tyre hiss on wet concrete, a faint electric whine, a room-tone floor (never digital zero) |
| S14 | 11.50–12.00 | 0.50 | AI | Heads in the queue turn | | Near-silence; one idle drops away |
| S15 | 12.00–14.00 | 2.00 | AI | Arfan steps out: the half-smile, the small nod | CAP 12.50–13.30 "Hello mates." | **Door clunk on 12.0; M returns on 12.0 (bar 7)**, warm and low. **DX 12.50–13.20.** AMB back to normal level |
| S16 | 14.00–14.75 | 0.75 | PH | A quick top-up | | Nozzle in at 14.05, **a short pump run** 14.1–14.5, **auto-shutoff clunk** at 14.6. Dave's whirr is still audible in the background |
| S17 | 14.75–15.25 | 0.50 | AI | Dave stares | | His whirr, now plainly the only pump still running |
| S18 | 15.25–17.00 | 1.75 | PH | Our C-HR's dash: **[C-HR L/100km] · [C-HR odometer]** | **SP 15.30–17.40 "Over 40% less fuel than his ASX.\*"** (source line under it, see critique 3) | His door shuts at 15.25 and the servo goes muffled. Nothing else |

### 17.0–21.0 s: silent start, double take, the C-HR leaves, Mia's line
| # | Time | Len | Src | Picture | Text | Sound |
|---|---|---|---|---|---|---|
| S19 | 17.00–17.50 | 0.50 | PH | Thumb presses START | | **Button click** at 17.05, **our soft READY chime** at 17.2 (a rising two-note made in-house, 0.5 s). **No engine** |
| S20 | 17.50–18.00 | 0.50 | AI | **Dave's double take** | | His pump, still whirring |
| S21 | 18.00–19.00 | 1.00 | AI | The C-HR leaves, rear three-quarter: the **Monsoor plate frame** shows, the plate is blurred | | Tyre hiss fading. **M breaks down on 18.0** (bar 10) to one sustained guitar note |
| S22 | 19.00–20.50 | 1.50 | AI | Mia at the back window, now awake: deadpan, then her eyes widen | CAP 19.10–20.40 "Dad... can we get one?" | **DX 19.10 Mia** (≤1.3 s). Nothing else under the line |
| S23 | 20.50–21.00 | 0.50 | AI | Dave looks at her; the "don't start" face cracks | | **His nozzle finally clicks off at 20.6** (the situational punchline, after the line) |

### 21.0–27.5 s: the yard, next day
Dave and Mia choose their car, and Monsoor tells Arfan "Good job".

| # | Time | Len | Src | Picture | Text | Sound |
|---|---|---|---|---|---|---|
| S24 | 21.00–22.50 | 1.50 | AI | Yard wide, midday: Mia points at a **pearl-white C-HR**, Dave nods | SP 21.05–22.20 **"Next day."** | **M bright on 21.0.** AMB: Albany Hwy traffic far off, flags, a magpie |
| S25 | 22.50–23.50 | 1.00 | AI | Arfan opens the white C-HR's door for them; Monsoor watches | | Door unlatch; sneakers on the brick |
| S26 | 23.50–24.50 | 1.00 | AI | Two-shot, 85 mm: Monsoor's hand on Arfan's shoulder | CAP 23.80–24.40 "Good job." | **DX 23.80 Monsoor.** A soft pat. **M dips 6 dB** and a warm pad swells |
| S27 | 24.50–26.75 | 2.25 | AI | Arfan CU, humble | CAP 24.60–26.80 "That means a lot for me." | **DX 24.60–26.16 + "for me" 26.20–26.70.** Nothing else under it |
| S28 | 26.75–27.50 | 0.75 | AI | Monsoor's small nod | | M rebuilds |

### 27.5–34.0 s: home delivery, keys handed over in Dave's driveway
| # | Time | Len | Src | Picture | Text | Sound |
|---|---|---|---|---|---|---|
| S29 | 27.50–28.75 | 1.25 | AI | Golden hour: the **white C-HR** rolls silently into Dave's driveway (Arfan driving) | CAP 28.00–28.90 "You choose the car!" | AMB suburb (birds, a distant mower) on the cut; tyres onto concrete. **DX 28.00–28.87** |
| S30 | 28.75–30.00 | 1.25 | AI | Arfan hands Dave the keys | CAP 29.15–30.20 "We bring it to your home!" | **Keys jingle at 28.95, in the voice-over's own gap.** **DX 29.18–30.13** |
| S31 | 30.00–31.00 | 1.00 | AI | Mia runs to the car | | **M lift on 30.0** (bar 16); her footsteps |
| S32 | 31.00–32.25 | 1.25 | AI | Dave behind the wheel presses START. **The same soft READY chime, no engine**; his slow grin | | Click at 31.1, chime at 31.25 (the callback, motivated by the button). M under it |
| S33 | 32.25–34.00 | 1.75 | AI | Crane-up pull-back: the family, the white C-HR, Arfan giving a small wave | SP 32.30–33.90 **"Delivered to your door."** | Mia's happy squeal at 32.4. M builds into the brand |

### 34.0–39.0 s: brand (made in-house, free). Premium build, no whoosh.
| Time | Picture | Sound |
|---|---|---|
| 34.00 | Cut to navy #0F2747 with a slow vignette | **M: last phrase on 34.0** (bar 18); bed thins to keys and bass |
| 34.10–34.80 | A thin orange #FF5F15 rule draws from the centre outwards (ease-out) | A single low felt-piano note on 34.1, with no swish |
| 34.50–35.50 | The real Monsoor logo (Brand Kit file) fades up as its letter-spacing tightens 4% → 0%; one soft light sweep across it | **Sonic logo at 35.4: the READY motif** (the same rising two-note) on felt piano and glass, so the brand's sound is the car's silent start |
| 36.00 | Logo locked | **M resolves on 36.0** (bar 19): a warm D-major chord |
| 36.20 | **0434 137 393** fades up | |
| 36.50 | **monsoormotors.com.au** fades up | |
| 36.80 | The single legal line fades up (§d) | |
| 38.00 | Hold | **M button on 38.0** (bar 20): one clean chord with a soft kick, ringing out to 39.0. A 0.1 s fade at the very end |

**Paste-ready for `qj_post.py`** (`END` = 936 frames at 24 fps; `SHOTS` from the table above):
```python
CAPTIONS = [
    (12.50, 13.30, "Hello mates."),
    (19.10, 20.40, "Dad... can we get one?"),
    (23.80, 24.40, "Good job."),
    (24.60, 26.80, "That means a lot for me."),
    (28.00, 28.90, "You choose the car!"),
    (29.15, 30.20, "We bring it to your home!"),
]
SUPERS = [
    (0.20, 3.90, "Tuesday night. Perth.", "hook"),
    (15.30, 17.40, "Over 40% less fuel than his ASX.*", "tag"),
    (21.05, 22.20, "Next day.", "tag"),
    (32.30, 33.90, "Delivered to your door.", "tag"),
]
CUTS = [
    ("Arfan-script-voice-LOCKED.wav", 4.50, 5.40, 12.50),    # "Hello mates"
    ("Arfan-script-voice-LOCKED.wav", 0.00, 1.60, 24.60),    # "That means a lot" ("for me" new, at 26.20)
    ("Arfan-script-voice-LOCKED.wav", 21.30, 23.43, 28.00),  # CTA
]
```

---

## Blunt critique: decisions needed before any credit is spent
1. **"Every shot its own generation" does not fit 350 credits as written.**
   - The story has 33 shots. If a generation can't be shorter than 4 s (the Seedance spec in our skill says 4–15 s), 25 AI shots × 4 s × 7 credits = **700 credits**.
   - It only fits if Higgsfield bills by the second with a minimum of about 2 s: 27.5 s of AI picture plus 0.5 s handles on each shot ≈ 40 s × 7 = **≈280**, plus ≈20 for audio = **≈300**.
   - **Check the minimum duration with the free `estimate_video_cost` before locking.**
   - If it is 4 s, fall back to shooting each set-up once and cutting 2–3 shots from it. For example, one Dave close-up acted as pained → stare → double take → smile gives S10, S17, S20 and S23.
2. **Shoot the eight inserts on a phone (S2, S4, S6, S9, S11, S16, S18, S19).** The client wants *real* L/100km and odometer figures; a real number on an AI-drawn dash is a fake readout. Real dashes, a real pump meter, the real nozzle and the real start button are free, sharp and truthful. Get the owners' consent for the other two cars, and keep their badges out of frame.
3. **The fuel claim needs its qualifier when it appears, not 20 s later.**
   - An asterisk whose source shows only on the brand card 20 s later is weak under the ACL's "clear and prominent" test.
   - My recommendation: the same small line sits under the super from 15.3 to 17.4 s, and again on the brand card. It is still one tidy line, shown twice. The client decides.
4. **The dash numbers can contradict the super.**
   - The super uses *official combined* figures (7.6 vs 4.3, which is 43% less). The dashes show *real-world* readings.
   - If [C-HR L/100km] is more than 0.6 × [ASX 10.4] (that is, above about 6.2), the screen shows less than 40% while the super says over 40%.
   - **The rule for REAL-NUMBERS.md:** if the real readings don't support "over 40%", show the C-HR's odometer and EV indicator without the L/100km figure. Never adjust a number.
   - The C-HR odometer must be the real odometer of the car we are selling.
5. **No "AI-generated" line on screen is acceptable only if Meta's own AI-info label is switched on at upload.** The scenes are photorealistic and include a real person (Monsoor). Confirm this in the upload checklist; don't drop it silently.
6. **One line is tight.** "\*Official combined: ASX 2.0 7.6 vs C-HR Hybrid 4.3 L/100km · Dealer Licence MD32748" is about 80 characters. On one line within 960 px that means Montserrat about 21 px, which is legible on a phone but small. If the client wants it larger, shorten "Dealer Licence" to "Lic." rather than adding a second line. Confirm the exact licence wording WA requires with Consumer Protection WA (I haven't verified it).
7. **The keys moving to the driveway changes Arfan's role.** He now drives the car out to them, so he appears in four locations. Check his outfit continuity in `CONTINUITY.md` for the driveway (golden hour, same outfit, same Ray-Ban Meta glasses).
8. **The paid-ad rule** (offer on screen in the first 3 s) is still broken. "Tuesday night. Perth." is a mood line, not an offer. For paid, A/B test it against "Hybrid Japanese imports. Delivered to your door." at 0.2–2.8 s.

---

## (b) Music brief: ElevenLabs Music v2.5, 39 s, 2 versions
The cost is **about 11.4 credits** (8.44 × 39/29; confirm with `estimate_audio_cost`). The ElevenLabs guide says to give an exact BPM and key, and to write "instrumental only".

**Prompt (39 s):**
> Instrumental only, no vocals. Original score for a 39-second warm comedy car commercial set in Perth. 120 BPM, 4/4, D minor moving to D major. Cheeky, warm, understated, premium; never cheesy, no stingers, no whooshes.
> 0–4 s: very sparse cold open. A soft sub-bass pulse on beats 1 and 3, with a short soft riser in the last 0.75 s.
> 4–10 s: half-time groove drops in exactly at 4 s. Dry kick, snappy clap on beat 3, round bass, a muted palm-muted guitar playing a tense, playful two-note figure. Stop dead at 10 s.
> 10–12 s: silence.
> 12–18 s: comes back at 12 s with a confident, warm, laid-back groove in D major. Light funk guitar chops, warm bass, soft claps on 2 and 4.
> 18–21 s: breaks down to one sustained clean guitar note.
> 21–27.5 s: a bright, sunny groove with a little Rhodes; softer and warmer from 23.5 s with a gentle pad swell.
> 27.5–34 s: a gentle lift with tambourine, building from 30 s with a rising bass line.
> 34–39 s: an elegant ending. The texture thins to felt piano and bass, resolves on a warm D-major chord at 36 s, then one clean final chord with a soft kick at 38 s that rings out to 39 s.
> Mixed with headroom, light compression.

- **Composition-plan version** (if the tool takes sections; each ≥3 s): A 0–4 · B 4–10 · C 10–14 (2 s silence, then the return) · D 14–21 (groove, then the sustained note from 18) · E 21–28 · F 28–34 · G 34–39 (resolve and button). In the global styles: "120 bpm, D minor to D major, instrumental only". In the negative styles: "vocals, stingers, whooshes, trailer booms, dubstep drops, trap hi-hats".
- **Use the 2 versions:** same tempo and key, so sections can be swapped at bar lines.
- **In the edit:** 10–12 s is muted whatever the model does. Section timing will be loose by a few hundred milliseconds, so slide each section onto the cuts at bar lines rather than regenerating.
- **No imitation:** don't name any artist, song, game or trailer in the prompt. No heartland-rock or 80s-ballad feel, nothing close to the GTA VI trailer songs.

## (c) Mirelo SFX list (about 2.5 credits per 10 s): ≈5 credits
Native audio from each AI shot covers most of it. Join the gap clips into two 10 s reels, run Mirelo once on each, then cut the results apart.
- **Designed in-house** (free, ffmpeg `aevalsrc`), never copied from a carmaker: the low-fuel chime, the READY chime, the sonic logo and the felt-piano note.
- **Real sound recorded with the phone inserts** (free): indicator, pump whirr, nozzle and shutoff, the start-button click, a key bunch, door unlatch, sneakers on our brick.

| Reel | Clips | Prompt | Length |
|---|---|---|---|
| R1 | S1 | "City red light at dusk, rain on a car roof, indicator ticking, pedestrian-crossing tick outside. No music." | 0.75 s |
| | S3 | "Northbridge at night: neon buzz, muffled club bass, one short car horn from directly behind." | 0.5 s |
| | S5, S7 | "Petrol SUV idling at the lights, a man's long tired exhale; then muffled cabin quiet, a child's soft sleeping breath." | 1.25 s |
| | S8, S12 | "Night servo: canopy hum, many petrol cars idling in a queue, the idles swelling as the queue creeps forward." | 2.5 s |
| | S13–S14 | "Near-silent night servo: tyres hissing slowly on wet concrete, a very faint electric whine, no engine, distant traffic." | 2.0 s |
| | S21 | "A quiet car pulling away on wet concrete, tyre hiss fading, no engine." | 1.0 s |
| | spare | alternate of S13–S14 | 2.0 s |
| | **Total** | | **10 s ≈ 2.5** |
| R2 | S24–S25 | "Sunny car yard on a highway: distant traffic, flags flapping, a magpie, a car door unlatching." | 2.5 s |
| | S29–S31 | "Golden-hour suburb: birds, a distant lawnmower, a car's tyres rolling slowly onto a concrete driveway with no engine, a child running on grass." | 3.5 s |
| | spare | alternates of the busiest clips | 4.0 s |
| | **Total** | | **10 s ≈ 2.5** |

**Audio total:** music ≈11.4 + SFX ≈5 + voice lines ("for me", "Good job", Mia) ≈1.5–3 = **≈18–20 credits**.

## (d) On-screen text: brand and safe zones
**Canvas:** 1080×1920.
- Text sits only between y 250 and y 1520.
- Side margins are 60 px, and 120 px on the right below y 1100 (the Reels buttons). Meta warns that edge text gets covered.

| Element | Style | Position |
|---|---|---|
| Hook "Tuesday night. Perth." | Montserrat ExtraBold 76 px, warm white #F7F5F2 on a navy #0F2747 pill at 88%, radius 20. One 6 px orange underline under "Perth". It stays still while the shots cut underneath, which is the point | y 290–400 |
| Claim super | Montserrat Bold 58 px, warm white on navy at 80%. "40%" in ExtraBold. The asterisk is the only orange | y 300–390 |
| Source line under the claim (recommended) | Montserrat Regular 21 px, warm white at 75%, no pill, one line, centred | y 410 |
| "Next day." / "Delivered to your door." | Montserrat Bold 60 px, warm white on navy at 80% | y 300–390 |
| Captions | Montserrat SemiBold 46 px, warm white on navy at 85%, radius 16, at most 2 lines and 32 characters a line. Each comes in on the first syllable. No speaker names | Centre line about y 1400, bottom ≤1500 |
| Readouts | **Real phone footage, no overlays.** If one is unreadable, add a small tracked label: Montserrat SemiBold 34 px, warm white on navy at 70%, e.g. "10.4 L/100km · 84,210 km". Never a model name | Beside the cluster |
| Pump meter | Real footage, no overlay | |
| Watermark | Monsoor logo at 55% opacity, on from 0.0 (brand inside the first 5 s) | x 60, y 260 |
| Brand card | Logo centred at about y 760. Phone: Montserrat SemiBold 64 px. URL: Montserrat Medium 44 px. Legal line: Montserrat Regular 21 px at 70%, y about 1460, reading "\*Official combined: ASX 2.0 7.6 vs C-HR Hybrid 4.3 L/100km · Dealer Licence MD32748". Nothing else | Safe zone |

## (e) Mix plan: free, local ffmpeg
**Buses:** DX, FX, AMB, MUS, rendered to stems, then summed.
1. **Dialogue first:** high-pass at 80 Hz and a light de-ess. Lines sit at about −16 LUFS short-term.
2. **Music sits 13 dB under the dialogue** in every line: sidechain-duck it from DX (`sidechaincompress=threshold=0.03:ratio=8:attack=15:release=250`), and cut the music 3 dB at 2–4 kHz under the lines. Check every line by ear. In the gaps the music rises to about 6 dB under dialogue level. On the brand card there's no dialogue, so the music is the lead at −14 LUFS short-term.
3. **FX** never go above the dialogue. The READY chime and the sonic logo sit 3 dB under dialogue level: soft, premium.
4. **AMB** sits at about −32 LUFS under every shot.
   - The idles push to about −24 at 9.0–10.0, so the silence lands hard.
   - From 10.0 to 12.0: AMB drops 12 dB and the music is muted, with a −60 dBFS room-tone floor.
5. **Sound changes are motivated:** each location's sound arrives on its cut. Dave's whirr runs on through 12–17 because his pump really is still running.
6. **Master:** two-pass `loudnorm=I=-14:TP=-1.5:LRA=9`. TP −1.5 leaves room for Meta's AAC re-encode, so the delivered file measures ≤ −1.0 dBTP. Check the integrated level is −14 ±0.5 LUFS.
7. **QC:** phone speaker, headphones, a mono fold-down, and one sound-off watch to confirm the story reads from the picture and the four supers alone.

## (f) Top 5 changes the research suggests, ranked
1. **Write the music to the story turns, with a clear beginning, middle and end.** Trailer editor Derek Lieu says strong trailers have music where you can feel the beginning, the middle and the end, rather than music laid over B-roll; he also likes a line cut against a contrasting sound. *Applied:* the drop at 4.0, the dead stop at 10.0, the return on the door at 12.0, the breakdown under Mia at 18.0, the resolve at 36.0 and the button at 38.0. ([Aftermath](https://aftermath.site/grand-theft-auto-vi-trailer-analysis-details-rockstar))
2. **Put silence right before the claim.** A radio-ad study found that cutting to silence just before the key information improved recall more than music throughout; Guinness "Surfer" is the trade example of a sound dropout. *Applied:* the 2 s silence sets up "Hello mates" and the fuel super. ([ASU](https://asu.elsevierpure.com/en/publications/creating-the-contrast-the-influence-of-silence-and-background-mus/), [shots.net](https://shots.net/news/view/explosive-silence-how-negative-space-can-tell-a-story))
3. **Design for sound off, then test it.** Meta's guidance is to plan for muted viewing with captions and text; a Journal of Advertising Research study via WARC says to test the soundless version. *Applied:* every situational joke is visible on screen (the meter, the heads turning, the double take, Dave's silent start), and four supers carry the story. ([QuickFrame](https://quickframe.mountain.com/meta-platform-expert/), [WARC](https://www.warc.com/newsandopinion/news/soundless-video-ads-require-a-rethink/41984), [Opus](https://www.opus.pro/blog/instagram-reels-caption-subtitle-best-practices))
4. **Laugh with drivers, never at them.**
   - In March 2026, during the fuel crisis, an influencer apologised for a Reel that seemed to mock people "complaining" about fuel. The replies said some families must choose between fuel and groceries.
   - The viral Aussie fuel clips were relatable reactions to prices.
   - The GTA trailer re-created familiar viral local moments.
   - *Applied:* recognisable Perth locals, real readouts, shared pain, and the ASX never mocked.
   ([Pedestrian](https://www.pedestrian.tv/news/georgie-stevenson-apology-petrol-prices/), [The Nightly](https://thenightly.com.au/australia/tiktok-star-says-aussies-should-escape-fuel-crisis-and-move-to-indonesian-island-where-fuel-is-1-per-litre-c-22051042), [Seniors Discount Club](https://seniorsdiscountclub.com.au/posts/833220), [PC Gamer](https://www.pcgamer.com/gta-6s-first-trailer-has-recreations-of-a-load-of-real-viral-video-moments-in-it-and-it-looks-like-rockstars-version-of-tiktok-will-play-a-big-part))
5. **Brand and message early; A/B test the hook.** Meta advises landing the hook in the first seconds and stating the brand and main message within 5 s. *Applied:* the watermark from 0.0 and a paid variant (critique 8). Track hook rate and cost per lead. ([Social Media Today](https://www.socialmediatoday.com/news/meta-shares-tips-on-reels-hooks-creative-diversification-in-ads-and-threa/808182), [Website Builder Expert](https://www.websitebuilderexpert.com/news/meta-updates-reels-ads-guide/))

**Research limits**
- GTA VI trailer grammar in outline: a cold open, then the world, the characters, rising stakes, the full cast, a coda. One licensed song runs end to end. Locals appear in social-media-style vignettes, and road signs and news bulletins name the places.
  - Sources: an unverified fan breakdown ([rockstar-files](https://rockstar-files.pages.dev/reports/10_misc/1007_Trailer_2_Frame_by_Frame.html)), [GamesRadar](https://www.gamesradar.com/gta-6-trailer-1-breakdown-things-you-missed), [Aftermath](https://aftermath.site/grand-theft-auto-vi-trailer-analysis-details-rockstar).
  - No source times their cuts to the beat. We copy no music, fonts, HUD or cards.
- Reels trends: cuts and text timed to the beat are common advice in creator guides, but not measured. The "80–85% watch muted" figures can't be traced to a source, so they are not used here. ([ManyChat](https://manychat.com/blog/instagram-trends-for-creators-2026/), [Epidemic Sound](https://www.epidemicsound.com/es/instagram/instagram-sound-effects/))
- Loudness: a Notre Dame study of 27,000+ TV ads found that energy holds attention and loudness does not. ([Notre Dame](https://mendoza.nd.edu/?p=25556))
- Music prompting: [ElevenLabs best practices](https://elevenlabs.io/docs/overview/capabilities/music/best-practices) and [composition plans](https://elevenlabs.io/docs/eleven-api/guides/how-to/music/composition-plans).
- Coverage of the $9.99 sign prices ([ACAP](https://acapmag.com.au/2026/03/why-australian-petrol-stations-are-showing-9-99-a-litre-prices/)) confirms fuel pain is a live 2026 topic. That is a reason to stay warm, not snide.
