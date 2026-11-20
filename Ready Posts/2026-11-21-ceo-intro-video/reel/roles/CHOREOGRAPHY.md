# "Queue Jump": choreography and movement plan (v4, 21 Nov 2026)

Role: choreographer / movement director. Plan only, no generation. Builds on `SHOOTING-SCRIPT.md`, `CONTINUITY.md`, `EMOTION-AND-SOUND.md`, `qj_scene.py`, the 3MT reference frames and the motion notes in `Brand Kit/Characters/Arfan-CEO/PERSONA.md`.

**Brief:** the locked story spine. 39 s: 34 s of story, then 5 s of branding. **Every shot is its own generation.**

Humour comes only from real reactions: the wince, the quick top-up, Dave's double take, and Mia's deadpan line. Background extras behave normally. Nobody holds a phone at the lights.

**The price board does not tick.** Only Dave's pump meter runs.

**Story logic:**
1. Dave is pained at the pump.
2. Arfan's C-HR tops up in seconds and leaves in silence.
3. Dave sees the Monsoor plate frame, and Mia asks.
4. At the yard, Dave and Mia leave after buying, and Monsoor tells Arfan "Good job" for bringing them in.
5. Arfan delivers Dave's car, a **different-colour C-HR from stock**, to the family driveway and hands over the keys there, under the voice-over "We bring it to your home".

## 0. Ground rules for every body in this ad

**Weight, not float.** Every move starts with a weight shift and ends with a settle: heel strike, a knee give, a shoulder that drops after an exhale, a car nose that dips on its springs as it stops. Moves run at real speed, with a 2–4 frame overshoot and settle on stops.

**Small imperfections are deliberate.** Use one per shot, such as a half-step, a blink after a line, a glance away and back, or an uneven pace. No frozen smiles. Nobody holds a pose for more than 1 s without breathing.

**Face-safety limits** (the client's top priority):
- A face that is speaking or reacting stays within 35° of the lens. The head turns no more than 30° in one shot, and the eyes do the rest.
- A face never goes from profile to front, or front to profile, inside one shot.
- Hands and props pass below the chin or beside the shoulder, never across a face.
- No spins and no fast head whips; the double take is a quick 6-frame head move of up to 30°, not a whip.
- Key face beats sit at 1.5–3 m from the lens, lit by the location's key light: canopy downlights at night, sun from frame left at the yard, low sun from frame left at home.

**Hands:** each hand does one thing per shot. A hand doing a task (the nozzle, the START button) gets its own hands-only shot. In the face shots, the hands stay low.

**Generation handle.** Each shot is generated longer than it is used (the model's minimum length). Write every prompt with about 0.8 s of settled lead-in before the first beat, and let the action run past the cut point. The edit takes the window given in the beat sheet. Beat times below are **edit times**; inside a generation, the first beat lands at about 0.8 s.

**Arfan's glasses:** he wears his Ray-Ban Meta glasses in **every** shot, with clear lenses at night (servo, car interior) and a green tint by day (yard, home).
- This replaces the CONTINUITY line "Ray-Bans in his shirt pocket at night"; update `CONTINUITY.md`.
- He never touches or adjusts them.
- Keep the day tint light enough that his eyes read through it, because his eyeline carries Y2, Y3 and H2.
- Canopy and sun reflections on the lenses must match the key-light direction, and they must not hide the eyes on a line.
- Write "wearing his Ray-Ban Meta glasses, clear lenses" (night) or "green-tinted lenses" (day) in every Arfan prompt. Check the frames in every start still.

**Arfan's motion palette** (captured from his habits, never copied from anyone):
- He stands square to the lens with his shoulders loose and his chin a touch down.
- A small eyebrow lift on key words; his hands stay low and move little.
- Easy half-smile, starting on the left side of his mouth.
- A quick sideways glance with the eyes first and the head following 10–15°.
- A small nod.
- He is never smug: the smile breaks into warmth, never into a smirk held at the lens.

**Monsoor's motion palette** (from the 3MT frames 4.5, 9.5, 12.5 and 14.5 s):
- Planted, hip-width stance, one foot a little forward, weight even.
- Left hand laid flat on a surface: fingers spread, wrist relaxed, light pressure, a slight forward lean from the hips (9.5 s, 12.5 s, 14.5 s).
- Right arm hangs loose with a soft elbow and fingers lightly curled.
- Slow head turn to look off, with the shoulders following late (12.5 s).
- Closed-mouth, small smile (14.5 s). No hands above the chest, no pointing, unhurried.
- He wears dark sunglasses outdoors in his real video. Whether he wears them in the yard is the director's call: they protect the real face less, because the eyes are hidden. Keep the choice the same in every yard shot.

**Dave:** an exhale before every reaction; dry humour played as underreaction; a slightly heavy, tired weight.

**Mia:** still and deadpan, then quick, slightly uncoordinated, kid-weighted bursts.

## 1. Master timeline (39 s = 34 s story + 5 s brand, 24 fps, 936 frames)

**Dialogue, proposed new times** (all lines are laid in the edit from locked or cloned audio):

| Line | Time (s) | Note |
|---|---|---|
| "Hello mates." | 12.8 | |
| "Dad... can we get one?" | 19.6 | |
| "Good job." | 24.7 | |
| "That means a lot for me." | 25.85 | about 0.65 s after "Good job." ends |
| Voice-over "You choose the car! We bring it to your home!" | 28.5 | ends about 31.3, over the key handover |

| Shot | Time (s) | Frames | Dur | What | Who is in it |
|---|---|---|---|---|---|
| M1 | 0.0–1.0 | 1–24 | 1.0 | Tradie (about 47), small petrol SUV: puffed-cheek exhale | extra |
| M2 | 1.0–2.1 | 25–50 | 1.1 | Nurse (about 38), small petrol SUV: tired head tilt, eyebrow up | extra |
| M3 | 2.1–3.0 | 51–72 | 0.9 | Retiree (about 66), small petrol SUV: peers over his glasses, small headshake | extra |
| M4 | 3.0–4.2 | 73–101 | 1.2 | Dave in his ASX at the lights, Mia asleep behind | Dave, Mia |
| S1 | 4.2–5.1 | 102–122 | 0.9 | Servo establishing shot; the board static | none |
| S2 | 5.1–6.5 | 123–156 | 1.4 | Wide: the queue; Dave at pump 2 | Dave (small) |
| S3 | 6.5–7.4 | 157–177 | 0.9 | Dave's pump meter ticking (insert) | none |
| S4 | 7.4–9.8 | 178–235 | 2.4 | Dave close: the wince (hero) | Dave |
| A1 | 9.8–11.6 | 236–278 | 1.8 | Black C-HR glides in silently | Dave (background) |
| A2 | 11.6–12.3 | 279–295 | 0.7 | The step-out: shoe on wet concrete | Arfan (feet) |
| A3 | 12.3–13.6 | 296–326 | 1.3 | Throwaway "Hello mates" nod to Dave | Arfan |
| A4 | 13.6–14.5 | 327–348 | 0.9 | The quick top-up (hands) | Arfan (hands) |
| A5 | 14.5–15.5 | 349–372 | 1.0 | In the seat, a glance at the dash | Arfan |
| B1 | 15.5–16.1 | 373–386 | 0.6 | START pressed; only READY (silent) | Arfan (finger) |
| B2 | 16.1–18.2 | 387–437 | 2.1 | **Dave's double take** (hero) | Dave |
| B3 | 18.2–19.3 | 438–463 | 1.1 | C-HR passes Dave; Monsoor plate frame | Dave (soft), car |
| B4 | 19.3–21.5 | 464–516 | 2.2 | **Mia: "Dad... can we get one?"** (hero) | Mia |
| B5 | 21.5–22.6 | 517–542 | 1.1 | Dave looks down the road: "hm" | Dave |
| Y1 | 22.6–24.0 | 543–576 | 1.4 | Yard: Dave and Mia leave happy; Monsoor and Arfan see them off | all four, Dave and Mia small |
| Y2 | 24.0–25.7 | 577–617 | 1.7 | **Two-shot: shoulder hand, "Good job."** | Monsoor, Arfan |
| Y3 | 25.7–27.6 | 618–662 | 1.9 | **Arfan close: "That means a lot for me."** | Arfan (Monsoor's hand) |
| Y4 | 27.6–28.3 | 663–679 | 0.7 | Monsoor's nod and release | Monsoor, Arfan |
| H1 | 28.3–29.5 | 680–708 | 1.2 | The new C-HR (stock colour) rolls into the driveway | car, Arfan behind glass |
| H2 | 29.5–31.3 | 709–751 | 1.8 | Arfan hands Dave the keys | Arfan, Dave |
| H3 | 31.3–32.8 | 752–787 | 1.5 | Mia runs out to the car | Mia |
| H4 | 32.8–34.0 | 788–816 | 1.2 | Wide: the family at the car; Arfan steps back | all |
| BR | 34.0–39.0 | 817–936 | 5.0 | Brand (H4's last frame under the first 0.5 s) | edit |

- Neighbouring shots never share a length.
- The four hero beats get the time: the wince 2.4 s, the double take 2.1 s, Mia 2.2 s, and Monsoor/Arfan 3.6 s across Y2 and Y3.

**Sound cues to update in `EMOTION-AND-SOUND.md`:**
- Montage: one hit per cut, at 0.0, 1.0, 2.1 and 3.0.
- Servo ambience from 4.0.
- Pump-meter ticks from 6.5 under S3–S4, and again under B2.
- Silence gag at 9.8.
- Door clunk and M2 music at 11.6.
- Nozzle click 13.8; pump off 14.3.
- START click 15.85, READY chime 15.95, then near-silence (only Dave's meter ticking) through B2.
- Yard ambience at 22.4.
- Pat 24.7.
- Home ambience at 28.2.
- Keys jingle 30.4.
- Mia's footsteps 31.4.

**Flags for the producer and coordinator:**
- **Credits.** 27 separate generations, each at the model's minimum length, cost far more than one multi-shot generation per scene. At 4 s × 7 credits that is about 760 credits, against the 250 cap. Check the minimum length and the price before sign-off.
  - Cheapest fix: generate the two-shot scenes (Y2–Y4, H2–H4) as one take each with the same blocking and cut them in the edit, keeping single generations for the face-critical shots.
- **New car element needed.** Dave's car is a different-colour C-HR Hybrid from our stock, for example pearl white, which reads clearly against the black demo and the grey ASX. It needs its own reference sheet, and the colour must match the real stock car.
- **Who delivers.** I stage Arfan, which gives his arc a payoff. If the client prefers Monsoor, H2 swaps to Monsoor's palm-up handover from his gesture vocabulary, with the same blocking.

## 2. (a) Beat sheets, one per shot (= one per generation)

### Montage: red lights, petrol readouts

Rules for all four:
- Dusk moving into night, with red traffic-light glow on each face.
- No phones in any hand, cup holder or mount.
- The driver's eyes are already on the fuel readout at the first beat. The wince lands within 0.4 s, and the cut lands on the follow-through.
- Readouts show a needle near E and a warning light only, never readable text.
- **All three drivers sit in small petrol SUVs in the same budget band as the C-HR**: Mazda CX-3, Honda HR-V and Kia Seltos or Hyundai Kona petrol types, each a different colour. Blank plates, no badges in close-up.
- Seat height, steering-wheel height and dash position all match Dave's ASX: an upright small-SUV seat with the dash at chest height. The four shots then read as one world, and the start stills can share one interior set-up with the trim and colour changed.
- Each driver gets their own lens and Perth street. No faces in mirrors.

**M1, 0.0–1.0: tradie, about 47, hi-vis shirt, sun-weathered**, in a white small petrol SUV (CX-3 type). 35 mm through the windscreen, Albany Hwy shopfronts.
- 0.0: eyes on the fuel needle, both hands on the wheel.
- 0.1: a breath in; his chest lifts.
- 0.2–0.6: **a puffed-cheek exhale**. Both cheeks fill, and the air goes out slowly through pursed lips. His shoulders drop with it.
- 0.8: his eyes lift to the red light; a flat look.
- Cut at 1.0 on the eyes lifting.

**M2, 1.0–2.1: nurse, about 38, navy scrubs, hair tied back, end of a shift**, in a grey small petrol SUV (HR-V type). 50 mm from the passenger seat, a suburban arterial.
- 1.0: eyes on the fuel readout.
- 1.15: **one eyebrow goes up**: tired disbelief, not anger.
- 1.3–1.7: **a slow, tired head tilt** of about 15° to her left, toward the headrest wing. The shoulders soften, and one blink is slower than normal.
- 1.9: she holds the tilt and keeps looking at the readout, deadpan.
- Cut at 2.1 at the end of the tilt.

**M3, 2.1–3.0: retiree, about 66, cardigan, reading glasses low on his nose**, in a blue small petrol SUV (Seltos or Kona type). 85 mm, front three-quarter from the dash side.
- 2.1: his chin is slightly down.
- 2.2: **he peers over the top of his reading glasses** at the gauge. His eyebrows rise and his forehead creases.
- 2.4–2.8: **a small headshake**: two slow, short turns of about 5° each, his lips pressed.
- Hands stay on the wheel; he doesn't touch the glasses.
- Cut at 3.0 on the second turn.

**M4, 3.0–4.2: Dave's grey 2021 ASX**, Mia asleep in the left rear seat. 35 mm from outside the passenger window: Dave three-quarter, Mia soft behind.

Dave's reaction is different from the three extras, so the montage doesn't repeat itself:
- 3.0: his eyes on the gauge.
- 3.2: the jaw sets.
- 3.4: a slow breath out through the nose, with no cheek puff.
- 3.7: his eyes go to the rear-view mirror, toward Mia (eyes only, head ≤10°).
- 3.9: a small resigned nod.
- Mia sleeps, head against the window; only her breathing moves her.
- Cut at 4.2 on the nod as green light spills on his face.

### Servo, night

**S1, 4.2–5.1: establishing shot**
- Low 50 mm with a slow push past the static price board toward the lit canopy.
- Queue headlights behind; idle exhaust haze drifting.
- No people close. The board does not change, and its digits are not readable as a claim.
- Cut at 5.1 as the push reveals the pumps.

**S2, 5.1–6.5: wide**
- 24 mm static. The queue stretches to the road, idling.
- Dave at pump 2, nozzle in his ASX's filler, left hand on the roof.
- 5.4: he shifts his weight onto his left leg.
- 6.0: he rolls his neck once.
- Background drivers just wait: hands on wheels, one arm resting on a window sill. No phones.
- Cut at 6.5 as his eyes go to the meter.

**S3, 6.5–7.4: the pump meter (insert)**
- 85 mm. The pump display's total climbs steadily; the digits roll.
- Kept soft or laid in from our own graphic, so no garbled numbers.
- Cut at 7.4 on a digit roll.

**S4, 7.4–9.8: Dave close (hero wince)**
- 50 mm with a slow dolly in.
- 7.4: his eyes follow the total; his right hand holds the nozzle.
- 7.9: a small wince: the eyes narrow and the lips press.
- 8.4: he looks away at the road, as if not watching makes it cheaper.
- 8.9: his eyes are pulled back to the meter.
- 9.1: a slow exhale; the head drops 15° and the shoulders follow.
- 9.5: a tiny "of course" corner-of-mouth smirk.
- Cut at 9.8 on the start of an inhale, as the sound drops away.

### The arrival

**A1, 9.8–11.6: silent glide**
- 24 mm low tracking beside the car.
- The black C-HR passes the queue at a steady 25 km/h, with only tyre hiss on the wet concrete.
- 10.4: a couple of queue drivers glance at it, as people naturally do.
- 10.8: it turns into the free pump lane, and the body rolls slightly.
- 11.3: it stops; the nose dips 2 cm and settles.
- Dave at pump 2 in the background glances over once, then back to his meter.
- Cut at 11.6 on the settle.

**A2, 11.6–12.3: the step-out** (the subtle trailer-style wink, never named)
- Ground level, 24 mm. The amber board and white canopy are reflected in a thin puddle.
- 11.65: the driver's door swings open (hand on the door only).
- 11.8: his right shoe lands flat in the reflection; the trouser hem drops and settles.
- 12.0: the left foot follows, and the weight rises out of frame.
- Real speed, no slow motion, no face.
- Cut at 12.3 as the door starts to swing shut (clunk at 12.3 on the cut).

**A3, 12.3–13.6: throwaway "Hello mates"**
- 50 mm from beside the pump island, so Arfan faces the lens three-quarter and Dave sits just right of the lens.
- 12.3: his right hand pushes the door shut behind him without looking; he is already moving toward the pump.
- 12.6: his eyes catch Dave staring; the head turns 10° to him.
- 12.8, "Hello mates": one small, easy nod, said lightly at conversational volume. A brief half-smile flicker, then gone. It is a passing courtesy, not a moment.
- 13.1: his eyes are already back on the pump; his right hand reaches for the nozzle (low).
- Cut at 13.6 on the reach.

**A4, 13.6–14.5: the quick top-up (hands only)**
- 85 mm on the filler (right rear).
- 13.6: his right hand, ring visible, brings the nozzle in.
- 13.8: it seats with a click.
- 13.9: one squeeze, and the meter runs briefly.
- 14.3: the pump clicks off already. His hand pauses a beat (the brevity is the joke), then lifts the nozzle out.
- Cut at 14.5 on the lift.

**A5, 14.5–15.5: in the seat, a glance at the dash**
- 35 mm from the dash, looking back at him; his face front three-quarter, lit by the cluster.
- 14.5: he settles back; the seat takes his weight.
- 14.7: his right hand rests on the wheel at about 1 o'clock.
- 14.8: his eyes drop to the dash (the readout soft).
- 15.1: a small, satisfied half-smile; one short nod.
- 15.3: his left hand moves low toward the START button.
- Cut at 15.5 on that move.

### Silent START and the double take

**B1, 15.5–16.1: START (hands only)**
- 85 mm macro beside the wheel.
- 15.55: his index finger comes in straight, pad first, Seiko visible on his left wrist.
- 15.85: one firm press of about 2 mm; it holds 3 frames.
- 15.95: only the READY light comes on, with a soft chime. No engine, no vibration.
- 16.05: the finger lifts.
- Cut at 16.1 on the lift.
- Check on our real car which side of the wheel the button sits; in RHD Toyotas it is usually on the centre side, which means his left hand.

**B2, 16.1–18.2: Dave's double take (hero)**
- 50 mm on Dave at his pump, three-quarter to the lens; his own meter is still ticking.
- 16.1: his eyes on his meter.
- 16.4: the C-HR's lights come on in his periphery (soft, frame left). No engine sound.
- 16.6: first take: a casual glance up toward it, 15°, then straight back down to his meter (0.3 s).
- 17.0: he freezes, a beat with no breath.
- 17.2: second take: his head comes back up over 6 frames, ≤30°, eyebrows up, mouth slightly open.
- 17.6: his eyes track the car as it rolls off in silence.
- 17.9: one slow blink.
- Cut at 18.2 on the blink opening.

**B3, 18.2–19.3: the plate frame**
- 28 mm from beside Dave's shoulder, Dave soft in the frame-left foreground.
- 18.2: the C-HR rolls past at walking pace, close to the lens, in silence.
- 18.6–19.0: its rear passes. The **Monsoor Motors plate frame** crosses frame centre, sharp and level for about 0.4 s (the plate itself blank).
- Dave's head turns slowly with it (cheek and ear only).
- Cut at 19.3 as the tail-lights pull away.
- The plate-frame graphic must be our real artwork: in the start frame, or tracked in during the edit. Never generated text.

**B4, 19.3–21.5: Mia (hero)**
- 50 mm through the ASX's rear side window. Mia is awake, chin on the door sill, face still.
- 19.3: her eyes follow the tail-lights.
- 19.6, "Dad...": her eyes slide to Dave first; the head stays still.
- 20.1: a beat of silence; she blinks once.
- 20.5, "...can we get one?": no head move. The eyebrows rise slightly on "one", and the eyes widen 1–2 mm. Deadpan throughout.
- 21.2: she holds the look, waiting.
- Cut at 21.5 before she can blink again.

**B5, 21.5–22.6: Dave**
- 35 mm, Dave three-quarter.
- 21.5: his eyes go to her first, then his head turns 20°.
- 21.8: a flat look: "don't start".
- 22.0: his eyes go back down the road where the car went (he read that plate frame).
- 22.3: a small, slow "hm" nod; one corner of his mouth gives.
- Cut at 22.6 on the nod. The yard ambience leads in at 22.4.

### The yard, days later

The new stock C-HR (the different colour) stands in the foreground, freshly detailed, with a blank plate. The black C-HR is behind. The sun is high from frame left.

**Y1, 22.6–24.0: they leave happy**
- 35 mm wide with a slow push.
- Monsoor (frame left) and Arfan (frame right) stand by the new C-HR, three-quarter to the lens.
- Dave and Mia walk away toward their ASX at the kerb (frame left, small in frame).
- 22.8: Mia skips a step beside Dave.
- 23.1: Dave half-turns and gives a small wave back.
- 23.2: Monsoor raises his right hand low in return, palm open, unhurried. Arfan nods.
- 23.6: Monsoor's head starts a slow turn toward Arfan; his shoulders follow late.
- Cut at 24.0 mid-turn.

**Y2, 24.0–25.7: two-shot, the shoulder hand**
- 85 mm with a slow push-in. Both faces three-quarter: Monsoor frame left, Arfan frame right.
- 24.0: Monsoor completes the turn.
- 24.15: his left hand lifts from his side.
- 24.4: it lands on Arfan's right shoulder. Arfan's shoulder dips 2 cm, and he shifts his weight a half-step toward Monsoor.
- 24.7, "Good": one soft pat.
- "job.": the hand rests, and Monsoor gives one short, slow nod.
- 24.9: Arfan's eyes go to Monsoor first.
- 25.05: his head follows 15°.
- 25.4: his chin dips 5°, and his eyes soften.
- Cut at 25.7 on the chin dip.

**Y3, 25.7–27.6: Arfan close (hero)**
- 85 mm on Arfan, with Monsoor's hand visible at the frame edge on his shoulder.
- 25.7: chin down; a breath.
- 25.85, "That": the chin rises back to level, eyes on Monsoor.
- "means": a slow blink.
- "a lot": a small eyebrow lift.
- "for me": a tiny nod; the half-smile becomes a real smile.
- 27.0: a humble glance down and away.
- 27.4: his eyes come back up to Monsoor.
- Hands stay at his sides.
- Cut at 27.6 on the eyes returning.

**Y4, 27.6–28.3: release**
- Back to the two-shot.
- 27.65: Monsoor's closed-mouth small smile; one squeeze.
- 27.85: the hand slides back off the shoulder and drops to his side by 28.05.
- 28.05: Arfan's shoulder settles; he breathes out.
- Cut at 28.3 on the hand dropping. Home ambience at 28.2.

### Home delivery, golden hour

**H1, 28.3–29.5: roll-in**
- 35 mm low at the kerb.
- The new C-HR (stock colour) rolls up the driveway at walking pace, with Arfan visible but small behind the windscreen. Low sun on the glass.
- 29.2: it stops; the nose dips and settles.
- Dave waits on the driveway edge, hands in pockets, weight on one leg.
- The voice-over starts at 28.5.
- Cut at 29.5 on the settle.

**H2, 29.5–31.3: the keys**
- 50 mm. Arfan and Dave stand in a V opening to the lens, each about 35° off camera, 1 m apart.
- 29.5: Arfan is already out, the driver's door closing behind him (a soft push).
- 29.8: two easy steps to Dave.
- 30.1: his right hand comes up, palm up and flat, the keys lying on it (the habit he picked up from Monsoor).
- 30.4: Dave lifts the keys off by the ring (the jingle) and looks at them, then at the car.
- 30.7: Arfan gives a small nod and a half-smile, and steps back a half-step to give the moment to the family.
- 31.0: Dave grins; a short, firm handshake with his free hand is optional. Skip it if hands get crowded.
- Cut at 31.3 as the front door opens in the background.

**H3, 31.3–32.8: Mia runs out**
- 35 mm side-on with a slow crane up.
- 31.3: Mia bursts out of the front door.
- 31.4–32.3: she runs across the lawn on a diagonal toward the new car.
- 32.3: two stutter-steps to slow down.
- 32.5: both palms land flat on the passenger door; she looks in through the window.
- Cut at 32.8 on the palms landing.

**H4, 32.8–34.0: wide**
- 24 mm, crane at full height.
- Dave walks to Mia and rests a hand on her shoulder. They look at the car.
- Arfan stands two steps back by the garden edge with a relaxed, half-smiling look; he isn't the focus.
- The grey ASX sits on the kerb behind, kept, not mocked.
- Cut at 34.0 into the brand.

## 3. (b) Key-gesture specs

**a) "Hello mates" (12.8 s), a throwaway**
- Eye contact with Dave for about 0.4 s.
- One small down-nod, chin about 3°, with no up-nod.
- The words are spoken lightly while still moving toward the pump.
- A half-smile flicker that is gone by 13.1.
- Shoulders loose; no wave, no stop, no turn of more than 10°.
- Wrong versions: stopping to deliver the line, a grin, a look into the lens.

**b) The key handover (H2, Arfan → Dave, at the driveway)**
- Arfan's right hand, palm up and flat, keys lying on it at waist-to-chest height. This is Monsoor's open-palm habit, passed on, and the echo is the only "story" in the gesture.
- Dave's right hand lifts the keys off by the ring. No pinch-to-pinch transfer; fingers never interlace.
- Arfan's palm stays open for 0.3 s after the keys go, then lowers.
- Prop: one key and fob on a plain ring, small enough to sit in the palm.

**c) The shoulder hand (Monsoor's left hand on Arfan's right shoulder)**
- Why the left: Monsoor stands on Arfan's right, so his near hand is the left. It is also the hand he lays flat on the bonnet in his real video.
- Arc: from his side, starting at 24.15 s and landing at 24.4 s, about 0.5 m. It stays below both chins and passes in front of Monsoor's own chest, never between the faces.
- Landing: the palm sits on top of the shoulder and the fingers curl over the front of the collarbone. The shirt bunches slightly, and the shoulder dips 2 cm.
- Contact: one soft pat at 24.7. The hand rests through Arfan's whole line (it is in frame in Y3), gives one squeeze at 27.65, and slides back off at 27.85.
- Total duration: about 3.5 s.
- Arfan never touches the hand and never leans his head toward it.

**d) Arfan's humble reaction (24.9–27.6 s)**
- Order: eyes, then the head turns 15° toward Monsoor, then the chin goes down 5°.
- Eyes: the lids drop slightly; one slow blink.
- Mouth: closed half-smile, then a real smile on "for me", without showing many teeth.
- Body: still, apart from the half-step on the landing.
- His eyeline stays on Monsoor's eyes (or his sunglasses), never the lens.

**e) Mia's run (31.3–32.5 s)**
- Short, quick, slightly uneven strides (about 6 over 3.5 m).
- Elbows bent, hands loose, ponytail swinging against her shoulders.
- Heels strike on the grass, then toes on the concrete.
- She slows with two stutter-steps and both palms land on the door. No sliding.
- Diagonal across the frame, never straight at the lens, feet always in frame.

**f) The START press (15.85 s), the dash glance (14.8 s) and Dave's double take (16.6–17.2 s)**
- The finger:
  - His index finger is straight, the other fingers loosely curled; the wrist is level with the Seiko face up.
  - It approaches over 4 frames. One press of about 2 mm, held 3 frames, then lifted. No double tap.
- The dash glance: eyes down, head ≤10°, a small nod, a half-smile. No look into the lens.
- The double take:
  - The first take is casual: the head turns 15°, then back.
  - A beat of stillness.
  - The second take is quicker (6 frames), ≤30°, with the brows up and the mouth slightly open.
  - Then stillness, and the eyes track the car.
  - It must read as genuine surprise, not mugging: no jaw drop, no rubbing his eyes.

## 4. (c) Prompt-ready motion lines, one per generation

Each line goes after the element tags; the AUDIO line follows. Each starts with "Holds still for a moment, then", which gives the 0.8 s lead-in.

In every line where Arfan's face is seen (A3, A5, Y1–Y4, H1, H2, H4), add:
- at night: "Arfan wearing his Ray-Ban Meta glasses, clear lenses";
- by day: "Arfan wearing his Ray-Ban Meta glasses, light green-tinted lenses, eyes visible".

| Shot | Motion line |
|---|---|
| M1 | "Tradie about 47 in a hi-vis shirt, driving a white small petrol SUV, at a red light at dusk, eyes on the fuel gauge: breathes in, cheeks puff out, slow exhale through pursed lips, shoulders drop, looks up at the light. Both hands on the wheel, no phone." |
| M2 | "Nurse about 38 in navy scrubs, driving a grey small petrol SUV, at a red light, eyes on the fuel readout: one eyebrow goes up, slow tired head tilt to the side, slow blink, keeps looking. Hands on the wheel, no phone." |
| M3 | "Retired man about 66 in a cardigan, reading glasses low on his nose, driving a blue small petrol SUV, at a red light: peers over his glasses at the fuel gauge, eyebrows up, small slow headshake, lips pressed. Hands on the wheel, no phone." |
| M4 | "Dave in his grey ASX at a red light, Mia asleep against the rear window: jaw sets, slow breath out through the nose, eyes to the rear-view mirror, small resigned nod; the light turns green." |
| S1 | "Slow push past a static servo price board toward the lit canopy; queue headlights, idle exhaust haze. No people close." |
| S2 | "Wide: idling queue of cars; Dave at pump 2 with the nozzle in, shifts his weight, rolls his neck." |
| S3 | "Close on a fuel pump display, the total climbing steadily." |
| S4 | "Dave watches the pump total climb, narrows his eyes, looks away at the road, looks back, slow exhale, head drops, small smirk." |
| A1 | "Black C-HR rolls past the queue at steady speed with no engine sound, turns into the free pump lane, body rolls slightly, stops, nose dips and settles; Dave in the background glances once." |
| A2 | "Ground level: car door opens, a shoe steps flat onto wet concrete reflecting amber lights, trouser hem settles, the second foot follows." |
| A3 | "Arfan pushes the car door shut behind him while walking to the pump, glances at the man at the next pump, small nod, says 'Hello mates' lightly, looks back to the pump and reaches for the nozzle." |
| A4 | "Close on the filler: a hand brings the nozzle in, it clicks in, one short squeeze, the pump stops almost at once, the hand pauses, lifts it out." |
| A5 | "Arfan settles into the driver's seat, right hand on the wheel, glances down at the dash, small nod, half-smile." |
| B1 | "Macro: one finger presses the car's power button once and lifts; only the READY light comes on; nothing else moves." |
| B2 | "Dave at his pump, meter still running, glances up at the car, looks back down at his meter, freezes, looks up again quickly, eyebrows up, mouth slightly open, watches it roll away, slow blink." |
| B3 | "The black C-HR rolls past close to the camera in silence, its plate frame passing level across the frame; Dave's head turns slowly with it." |
| B4 | "Mia awake at the rear car window, chin on the sill, still face, eyes to her dad: 'Dad... can we get one?', eyebrows lift slightly on the last word, holds the look." |
| B5 | "Dave turns to her, flat look, then looks down the road after the car, small slow nod." |
| Y1 | "Midday car yard: Monsoor and Arfan stand by a freshly detailed C-HR; a man and his daughter walk away toward the street, the girl skips, the man turns and waves; Monsoor raises his right hand low, Arfan nods; Monsoor slowly turns his head toward Arfan." |
| Y2 | "Monsoor rests his left hand flat on Arfan's right shoulder, one soft pat: 'Good job.' Arfan's shoulder dips under the hand, he looks at Monsoor, chin a touch down." |
| Y3 | "Close on Arfan, a hand on his shoulder: slow blink, small eyebrow lift, small smile becomes a real smile: 'That means a lot for me.' Glances down, then back up. Hands at his sides." |
| Y4 | "Monsoor nods once, closed-mouth smile, squeezes Arfan's shoulder, slides his hand off; Arfan breathes out." |
| H1 | "Golden hour: a [stock colour] C-HR rolls up a family driveway at walking pace and stops, nose dips; Dave waits at the driveway edge, hands in pockets." |
| H2 | "Arfan walks from the car to Dave, holds the keys out flat on his open palm; Dave lifts them off by the ring, looks at the car, grins; Arfan nods and steps back half a pace." |
| H3 | "Mia runs out of the front door across the lawn in short uneven strides, slows with two quick steps, both palms on the car door, looks in the window." |
| H4 | "High wide: Dave walks to Mia and rests a hand on her shoulder, both look at the new car; Arfan stands a few steps back, relaxed; an older grey SUV parked on the kerb." |

## 5. (d) Blender previs changes for `qj_scene.py` (for whoever edits it; I have not changed it)

Facing maths used below: the figure's nose points to −y at rz = 0, and its facing direction is (sin rz, −cos rz).

**Bugs found in the current file**
- Arm naming: in `person()`, `arm*L` (local −x) is the figure's anatomical **right** and `arm*R` is its **left**. So Monsoor currently hands over the keys with his left hand and touches Arfan with his right.
- S6b: Monsoor turns to rz = −70 and Arfan to rz = +55. Both face *away* from each other, which is why the storyboard panel shows backs and profiles.
- The C-HR ends at rz = 0 after driving +y, so it reverses into the bay. It ends at (SX−4, −2.4), inside `q0` and `q1`. Those two share one spot because of `-i * 0.0`.
- S4: Arfan turns to rz = −150, his back to the lens.
- S6a: Dave is at rz = 170, his back to the lens.
- Dave's car (rz = 0) has its left side, where the flap is, facing away from pump 2.

**1. Length and shots**
- `END = 936`.
- `SHOTS` = the 27 ranges in section 1 plus BR (817–936), each with its own camera and timeline marker.
- `set_env`:
  - frames 1–101: dusk, a dim blue background with a red area light, green from frame 98;
  - 102–542: night;
  - 543–679: day;
  - 680–936: golden hour.

**2. Montage (SET D at x = 0, y = −80)**
- A car-interior rig: a seat box, a steering-wheel `cyl` at z = 1.0, and a dash box with an emissive gauge at (0, −80.6, 1.05). No phone props.
- Seat at small-SUV height: hip point at z 0.65, wheel centre at z 1.15, dash top at z 1.25. This matches the ASX, so one rig serves all four montage shots.
- Three seated drivers shown with `only_in` M1–M3, with the rig's body colour swapped (white, grey, blue).
- M4 reuses an ASX copy at (0, −72) with Dave and `MiaCar` seated.
- Keys:

  | Driver | Key |
  |---|---|
  | M1 | the cheek puff, as a head scale x 1.06 from f 5 to 14; torso z −0.03 at f 14; head rx −8 at f 20 (looks up) |
  | M2 | head ry +15 (the tilt) from f 28 to 41, held to 50 |
  | M3 | head rx +6 at f 54 (chin down, peering); headshake rz ±5 at f 58, 62, 66 |
  | M4 | torso z +0.02 at f 80, back at f 88; head rz −8 at f 89; nod rx +5 at f 94 |

- For Arfan's glasses, add a thin dark box across the eyes of every Arfan proxy (`ArfanNight`, `ArfanCar`, `ArfanYard`, `ArfanHome`).

- Cameras:

  | Camera | Lens | Position |
  |---|---|---|
  | C_M1 | 35 mm | (0, −82.2, 1.35) |
  | C_M2 | 50 mm | (0.7, −80.1, 1.3) |
  | C_M3 | 85 mm | (0.3, −81.6, 1.3) |
  | C_M4 | 35 mm | (1.6, −72.3, 1.4) |

**3. Servo**
- **Delete the `tick()` handler and `frame_change_pre` append.** Leave the board at a fixed price.
- Instead, add a pump-1 meter text object on `pump1_s` that counts up from frame 157 (and keeps counting through 387–437).
- Cameras: C1 push 102→122; C2 static wide 123→156; C3 on `pump1_s` 157→177; C2b dolly 178→235.
- Dave:
  - weight shift: torso x +0.03 at f 130;
  - neck roll: head rz ±8 from f 144 to 150;
  - S4: head rz +25 at f 200, 0 at f 213; head rx −15 at f 222.
- `q0` → (SX−2.0, 2.3, 0), rz 180.
- `q1` → (SX−2.0, −3.6, 0), rz 180. Use explicit positions, not `-i * 0.0`.
- C-HR arrival:

  | Frame | Location | rz |
  |---|---|---|
  | 236 | (SX−30, −10) | 90 |
  | 255 | (SX−9.5, −10) | 90 |
  | 264 | (SX−7.4, −4.5) | 150 |
  | 271 | (SX−6.3, 1.4) | 180 |
  | 274 | (SX−6.3, 2.3) | 180 |

  Add a nose dip: rx +1° at 275, 0 at 280.
  - Result: the driver door, on the +x side, at about (SX−5.0, 2.6), facing the pump island. The filler, at the right rear, at about (SX−5.0, 0.9).
- C-HR departure:

  | Frame | Location | rz |
  |---|---|---|
  | 387 | (SX−6.3, 2.3) | 180 |
  | 415 | (SX−6.3, 4.5) | 180 |
  | 438 | (SX−3, 5.5) | 250 |
  | 463 | (SX+6, 5.0) | 270 |

  It passes behind Dave's car, close to C_B3. Update `CONTINUITY.md` shot 5 to "leaving through the forecourt, past Dave".
- Arfan (night):
  - (SX−5.0, 2.6), rz +60 at 296 (facing the island and Dave beyond it).
  - Head rz +10 at 302; the nod is rx +3 at 307 and 0 at 311.
  - Body to (SX−5.0, 1.3) by 326.
  - A feet-only proxy in A2.
  - Hidden from 349.
- C_A3: 50 mm at (SX−3.0, −0.6, 1.55), aimed at (SX−5.0, 2.2, 1.6). Arfan is three-quarter to it, and Dave sits just right of the lens.
- A5 and B1 use the SET D interior with an `ArfanCar` figure and a READY lamp with emission on at frame 382.
- Dave's double take (`dv_h`):

  | Frame | rz | rx |
  |---|---|---|
  | 387 | 0 | |
  | 398 | +15 | |
  | 405 | 0 | |
  | 412 | 0 (hold) | |
  | 418 | +28 | −6 |
  | 437 | +40 | |

- B5: Dave's head −20 at 523; +30 at 533; nod rx +5 at 538.
- Cameras:

  | Camera | Lens | Position | Aim |
  |---|---|---|---|
  | C_A1 | | the old C3 track, retimed 236→278 | |
  | C_A2 | 24 mm | (SX−5.6, 1.4, 0.12) | (SX−5.0, 2.6, 0.05) |
  | C_A4 | 85 mm | (SX−4.3, 0.2, 1.0) | the filler |
  | C_B2 | 50 mm | (SX+2.6, −2.0, 1.55) | Dave |
  | C_B3 | 28 mm | (SX+3.6, 1.6, 1.3) | across the forecourt |
  | C_B4 | 50 mm | outside the ASX's rear side window | Mia |
  | C_B5 | 35 mm | | Dave |

- Dave's car (if the ASX's flap really is on the left): rz 180 at (SX+6.2, 2.2).
  - Dave → (SX+4.9, 0.6), rz −60.
  - `MiaCar` → (SX+5.75, 1.3, 0.55).

**4. Yard**
- Add `CHR_stock` = `car(..., "#e9eaec", hero=True)` (placeholder pearl white) at (−0.2, 1.6), rz −70, in front. Keep the black `CHR_yard` behind at (2.6, 4.2).
- Positions:

  | Figure | Location | rz |
  |---|---|---|
  | Monsoor | (0.0, 0.1) | −35 at 543, toward the departing family |
  | Arfan | (0.95, 0.2) | −30 |

- Dave and Mia (`only_in` Y1):
  - Dave from (−1.2, −0.8) at 543 to (−5.5, −2.6) at 576, rz −110 (walking away to frame left).
  - Dave's wave: body rz −160 at 555–562; anatomical right arm `dy_l` rx −120 at 558–562.
  - Mia beside him, offset (−0.5, −0.3), with a skip of z +0.08 at 549.
- Monsoor's return wave (anatomical right = `m_l`): rx −70 at 557–563, 0 at 568.
- Monsoor's turn: `m_h` rz +12 at 567; body rz −35 at 567 → +25 at 580.
- Shoulder hand (anatomical left = `m_r`):

  | Frame | Rotation | Note |
  |---|---|---|
  | 580 | 0 | |
  | 583 | (−10, −20, 0) | |
  | 586 | (−20, −85, 0) | lands; hand at about (0.80, 0.26, 1.35) against Arfan's right shoulder at about (0.79, 0.32, 1.44); nudge ay ±5 in the viewport |
  | 593 | (−22, −85, 0) | the pat |
  | 595 | (−20, −85, 0) | |
  | 664 | (−20, −85, 0) | hold |
  | 669 | (−5, −40, 0) | |
  | 674 | 0 | |

- Arfan:
  - `ay_h` rz −15 at 601.
  - `ay_h` rx −5 at 610, 0 at 622, rx −6 at 648, 0 at 658.
  - Shoulder dip: `arf_y` z −0.02 at 586, 0 at 592.
  - Delete the old hand-to-chest keys.
- Cameras:

  | Camera | Lens | Frames | Position | Aim |
  |---|---|---|---|---|
  | C_Y1 | 35 mm | 543–576 | (−1.5, −6.6, 1.6) | (−1.5, −0.5, 1.2) |
  | C_Y2 / C_Y4 | 85 mm | 577–617 and 663–679 | (0.6, −6.5, 1.55) → (0.5, −5.8, 1.55) | (0.45, 0.15, 1.55) |
  | C_Y3 | 85 mm | 618–662 | (0.3, −3.0, 1.6) | (0.95, 0.2, 1.62) |

**5. Home**
- `CHR_home` colour → the stock colour ("#e9eaec" placeholder).
  - Keys: (HX+2.4, −13) at 680 → (HX+2.4, −3) at 701, rz 180, with a nose dip at 702/707.
  - The driver door is on the +x side.
- `ArfanHome` (`only_in` H1–H4):
  - Seated proxy until 709.
  - At 709: (HX+3.5, −3.0), rz +35.
  - Walks to (HX+3.9, −3.4) by 718.
  - Anatomical right arm (local −x, `armL`): rx −55 at 722–731 (palm up), 0 at 740.
  - Steps back to (HX+3.6, −3.1) at 737.
  - H4: (HX+5.5, −4.5), rz +20.
- Dave:
  - (HX+4.9, −3.4), rz −35, hands in pockets (arms rx 0) through H1.
  - Anatomical right `dh_l`: rx −55 at 727–732 (takes the keys), −20 at 740.
  - H4: walks to (HX+1.5, −2.6) by 812.
- Mia: (HX−1.0, 2.0) (front door) at 752 → (HX+0.6, 0.0) at 764 → (HX+1.2, −2.2) at 776 → (HX+1.3, −2.6) at 782 (passenger door, −x side).
- Delete the old S7 hand-raise keys on `mh_r` and the old Dave head keys.
- ASX copy parked on the kerb at (HX−4, −8.5), rz 90.
- Cameras:

  | Camera | Lens | Frames | Position | Aim |
  |---|---|---|---|---|
  | C_H1 | 35 mm, low | 680–708 | (HX−0.6, −14.5, 0.9) | (HX+2.4, −5, 0.8) |
  | C_H2 | 50 mm | 709–751 | (HX+4.2, −7.0, 1.55) | (HX+4.2, −3.2, 1.55) |
  | C_H3 | 35 mm side-on | 752–787 | (HX−4.0, −3.0, 1.1) rising to z 2.5 | the lawn |
  | C_H4 | 24 mm | 788–816 | (HX−5.5, −14, 5.5) | (HX+1.5, −2, 1.0) |

**6. Brand:** C_H4 holds from 817 to 936.

**7. Interpolation:** use BEZIER on body and car keys with a 2–3 frame overshoot on stops (nose dips, hand landing, the second take). Keep shot markers CONSTANT.

## 6. (e) Where AI motion fails here, and how to stage around it

| Risk | Typical failure | Staging fix |
|---|---|---|
| Hands on the nozzle | Fingers melt into the handle; the nozzle floats; the hose vanishes | A hands-only shot (A4), one hand, the hose in the start frame. Cut before the release. |
| Finger on START | A double press, extra fingers, a cluster that lights up everything | A macro start frame with the finger 3 cm from the button. One press. In the prompt: "only the READY light comes on, nothing else moves". No face in the shot. |
| Meter, readouts, plate frame | Garbled digits and logos | The pump meter (S3) is soft or our own graphic. The price board is static and soft. The plate frame is our real artwork in the start frame, or tracked in. Never generated text. |
| Keys (H2) | Keys duplicate or vanish; finger-to-finger morphs | Keys on an open palm in the start frame, lifted off by the ring, held at chest height, away from faces. If the hands fail, use the wide shot and lay the jingle on the cut. Skip the handshake if hands crowd. |
| The shoulder touch | The hand sinks into the shirt, sprouts extra fingers or slides; the faces drift to profile | Fixed three-quarter bodies (±25–30°), heads ≤15°. A low, slow arc in front of Monsoor's chest; one landing, one pat, a long rest. Skin contrasts with the dark shirt. **Fallback:** if it fails twice, use a start frame with the hand already resting and cut in on the pat. Y3's start frame already has the hand on the shoulder. |
| Shot-to-shot continuity (separate generations) | Each generation re-invents the hand position, the light or the car colour | Every start frame is a still made from the previous shot's last approved frame (or the same set-up still). Lock the car colour per element: black demo versus the stock-colour car. Check the shoulder hand in the Y2 last frame against the Y3 start frame. |
| Double take | Turns into a whip, or into mugging; the face drifts | Three-quarter face throughout, ≤30° head travel, the brows and stillness doing the work. If he overacts, use the first take plus his still stare only. |
| Running child | Legs tangle, feet slide, the body glides, the face morphs | A diagonal path, mid-wide, feet in frame, 3.5 m in about 1.2 s, a stutter-step stop against the door. If her feet slide, cut at 32.3. |
| Face turns | Identity drift from profile to front | Every speaking or reacting face within 35° of the lens; eyes lead. Reverse-angle closes (Y3) instead of head swings. H2 uses a V-stance, never face-to-face profiles. |
| Lip-sync | Mouth flaps; drift | The voice clip as an audio reference. "Hello mates" is said while walking slowly, so keep his face close and lit. The other lines are spoken standing still. |
| Step-out wink | Slow motion reads floaty | Real speed, feet and hem only, no face. |
| Car stops | Dead stops, gliding on ice | "Nose dips and settles" on every stop; tyre hiss in the AUDIO line. |
| Montage extras | Faces merge; phones appear | Each written with a distinct age, clothing, car and lens. "Both hands on the wheel or lap, no phone" in every montage prompt. No mirror faces. |
| Arfan's glasses | Frames morph, appear and vanish between shots; the tint goes dark and hides the eyes; glare covers the eyes on a line | Glasses in every start still. Clear lenses at night, light green by day. His hands never go near them. Angle so canopy or sun glare sits at the lens edge, not over the pupils. Reject any take where they vanish. |
| Retiree's reading glasses (M3) | The glasses slide or merge into his face during the headshake | A small headshake (≤5°). The glasses sit low on the nose in the start still; his hands stay on the wheel. |
| Ring and watch | They jump hands or vanish | Ring on the right hand (nozzle, keys), Seiko on the left wrist (START). Check both in every insert. |

**To verify before the start frames:**
- The real fuel-filler side of our black C-HR and of a 2021 ASX. CONTINUITY assumes C-HR right rear and ASX left rear; if either is wrong, park that car so its filler faces its pump and mirror A3 and A4.
- Which side of the wheel the power button sits on in our C-HR.
- The actual colour of the stock C-HR to be shown as Dave's car.
