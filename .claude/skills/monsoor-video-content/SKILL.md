---
name: monsoor-video-content
description: Use for any Monsoor Motors sell content — statics and reels for a stock car for sale. Covers fetching the real live stock first, building the owner character board and the car object board, using free tools first and Higgsfield only when a free tool cannot do the job, and producing a ready-to-upload pack (3 statics + 1 x 30 s reel) with real prices only. Load before making any Monsoor Motors sell content.
---

# Monsoor Motors video content — sell a stock car

Make sell content for one real Monsoor Motors car at a time, ready to upload immediately to Instagram, Facebook and TikTok. Free tools first. Higgsfield last, and only for what free tools cannot do. Never invent a car, a price, a year, kilometres, or a feature.

## Business facts — do not change these

- **Monsoor Motors Pty Ltd**, ABN 31 695 324 193, MV Licence MD32748
- **530 Albany Highway, Victoria Park WA 6100**
- **Phone 0434 137 393** — the only phone number to use
- **info@monsoormotors.com.au** — monsoormotors.com.au
- Owner: **M A Monsor — Mohammod A Monsor, Owner & Director**
- No rentals. No lease-to-own. No "Rent-To-Own" wording anywhere.
- Wrong numbers — flag them, never use them: 0433 205 162, 0483 153 638, (08) 4931 0421
- Australian English: licence, colour, organise, kilometres.

## One-prompt triggers

Use any of these, with the car as the owner names it:

- `video content: <car>`
- `sell reel: <car>`
- `sell statics: <car>`

Example: `video content: 2018 Mazda Mazda3 SP25 Astina`

A trigger with no car, or with only a make ("Mercedes"), is not enough to start. Ask for the exact listing first — see Step 0.

## Step 0 — Fetch first: the car must be real and for sale

Do this before any design, any board, any generation, and any spending.

1. Fetch the live stock page: https://monsoormotors.com.au/stock
   - Also check https://monsoormotors.com.au/stock-list if it is still live. The two pages have shown different prices for the same car. If they disagree, record both, use neither as final, and ask the owner which price is correct.
2. Check the repo: `Cars/` and `Ready Posts/` in Arfan-Zaman/Monsoor-Motors-Aureus-Detailing, main branch.
3. Record, from the live listing only, all of these:
   - Year, make, model, variant, body style
   - Price (drive-away or excluding on-road costs — record exactly as listed)
   - Kilometres, transmission, fuel, engine
   - Colour, registration status, location (Victoria Park)
   - Status: **for sale / under offer / sold**
   - Listing URL and the dealer photos for that car
4. **Stop rule — read this carefully:**
   - If the car is not in live stock, **stop**. Do not build content for it. Do not guess a price, year, kilometres or photo.
   - If the car is sold or under offer, **stop**. Never present a sold or under-offer car as for sale.
   - If any of year, price, kilometres or photos is missing, list exactly what is missing and stop.
   - Tell the owner, in one short message, what is missing and what to send: the listing link, or the year, price, kilometres and photos.
   - **Worked example, verified 20 Nov 2026:** the live stock page listed 19 cars and there was **no Mercedes** in current live stock, and `Cars/` in the repo contained only `14:11:2026-2010 Volkswagen Golf 90 TSI`. So a request for "a Mercedes" must stop at Step 0 and ask the owner for the exact Mercedes listing — year, price, kilometres and photos — before any content is made. Mercedes is the first requested example of this skill, not a car that has been verified in stock.

## Step 1 — Character board: M A Monsor, built once

The presenter is the owner himself, M A Monsor. Build his character board once, then reuse it every time. Never describe his face from scratch again.

1. Use only owner-supplied photos of M A Monsor, with his consent. The best avatar source is his beach sunset front-facing photo (eyes open, dark polo). The night bus-stop front-facing photo is the backup. Do not use photos where his eyes are closed, or where a phone covers his face.
2. Build the board with the Higgsfield Soul ID / character-sheet workflow (`higgsfield-soul-id`, `higgsfield-character-design`), following `.claude/skills/aureus-video-studio/SKILL.md` §3.
3. Save the character as a reference element (`manage_reference_elements`) and record its ID, Soul ID, wardrobe and the source photo filenames in `.claude/skills/monsoor-video-content/assets/ASSET-REGISTER.md`.
4. Keep the same look every time: same face, same wardrobe (dark polo or Monsoor navy, as agreed with the owner), same framing. Never alter his face, age, or appearance.
5. Never create a likeness of anyone else. Never imitate a celebrity. Never use a staff member or customer without their written OK.

## Step 2 — Object board / dashboard: the car, built from real photos

Build one object board per car, from that car's real dealer photos only.

1. Use the live listing photos as reference elements. Angles, in this order: front three-quarter, side profile, rear three-quarter, interior dashboard and driver's seat, and one detail shot (wheels, badge, or headlight).
2. **Blur every number plate** in every static and every frame.
3. Never change the car's colour, condition, features, badges or wheels. Never add a feature it does not have. Never use a photo of a different car, a different colour, or a different year as if it were this car.
4. Save the board and every reference element ID in `ASSET-REGISTER.md`, with the car's year/make/model/variant and the listing URL.
5. If the dealer photos are low resolution, cropped badly, or missing an angle, say so and use the best real photo available — do not generate a replacement car image and present it as the real car. A generated hero shot must be labelled "AI-generated" and must never be presented as the car for sale.

## Step 3 — Free-first ladder: Higgsfield LAST and minimal

Work down this ladder. Stop at the first rung that does the job well. Do not jump to Higgsfield because it is faster.

| Rung | Job | Free tool first | Higgsfield? |
|---|---|---|---|
| A | Statics | Real dealer photos + Canva free / CapCut free text overlays, brand colours, frosted-glass labels | No |
| B | Reel edit | CapCut free, or `Aureus Detailing/08 Social Media/Launch Reels/ad/make_ad_v6.py` style — clean cuts, real speed, human look | No |
| C | Voice | Free text-to-speech first; the owner's voice only with his consent, cloned from the approved voice reference | No, unless the free voice cannot deliver the script naturally |
| D | Higgsfield only | — | **Only** when a free tool cannot do it: Soul ID consistency for the owner avatar, cinematic car 360, or a photorealistic avatar talking to camera |

Rules for rung D:

- Before any paid generation, check the Higgsfield credit balance (`higgsfield account status`, or the paid connector's `balance`) and show the owner the **minimum-credit plan**: exactly which shots, how many credits each, and the total. Do not spend without a stated cap from the owner.
- Reuse first. Check `assets/GENERATION-LOG.md` and `assets/ASSET-REGISTER.md`. If a keyframe, prompt, seed or reference already exists for this car or this presenter, reuse it instead of generating it again.
- One keyframe still per step, then one short shot per keyframe. Do not generate a long continuous take when clean cuts will do.
- Lint every Seedance prompt with `higgsfield-prompt-suite/scripts/seedance_lint.py` before spending credits.
- Log every credit spent, the same day, in `assets/CREDIT-LOG.md` — date, car, shot, model, credits, result link, keep / reject and why.

### Credit budget — known costs from aureus-video-studio

These are the costs recorded in the existing video studio skill. Confirm the current price in Higgsfield before spending, because prices can change.

| Item | Cost |
|---|---|
| Keyframe still | 2 credits |
| 3 s Kling 4.0 shot (start image only) | 9.75 credits |
| Mirelo audio (`mirelo_text_to_audio`) | 0.75 credits per 3 s |

**Minimum-credit example for one 30 s reel:** 4 keyframes (8 credits) + 4 x 3 s Kling shots (39 credits) = 47 credits, plus audio as needed. That is a planning example only — the real plan must be costed shot by shot and agreed with the owner before spending. If the owner sets a cap, stay under it. If the job cannot be done inside the cap, say so and offer the free-only version instead.

## Step 4 — Output pack: ready to upload immediately

Every `video content: <car>` job produces all of this, in one pack, with the real price and kilometres on every piece that mentions them.

### 3 statics

- **9:16** (1080 x 1920) — Reels / Stories / TikTok
- **1:1** (1080 x 1080) — feed post
- **4:5** (1080 x 1350) — feed post
- Each static: real car photo, car name, year, price, kilometres, "Victoria Park" and phone 0434 137 393. Plates blurred. Monsoor navy #0F2747, orange #FF5F15 accent only, warm white #F7F5F2, Montserrat. Text inside the centre safe area (avoid top 250 px and bottom 400 px on 9:16).

### 1 x 30 s reel

- **Script (30 s, spoken by the owner or his approved voice):**
  - 0–3 s — Hook, owner to camera: the car, the price, one reason it is worth a look.
  - 3–10 s — Owner intro: who he is, Monsoor Motors, Victoria Park.
  - 10–20 s — Car: front, side, rear, interior dashboard — 2 s each, plates blurred, no prices invented, no feature invented.
  - 20–27 s — Owner to camera: call to action.
  - 27–30 s — End card: Monsoor Motors logo, 530 Albany Highway, Victoria Park, 0434 137 393.
- **Storyboard:** one line per shot — time, shot, on-screen text, voice line, source (real photo / free edit / Higgsfield shot and its credit cost).
- **On-screen text:** first 2 s — "THIS IS A REAL CAR FOR SALE" where the car is shown, and "AI AVATAR" on any avatar shot where the owner is AI-generated, so the viewer is never misled.
- **Caption:** car year/make/model/variant, price, kilometres, transmission, fuel, location, "Call 0434 137 393 or visit 530 Albany Highway, Victoria Park WA 6100", and "Comment CARS and I'll send you what's in stock right now."
- **Hashtags:** #MonsoorMotors #VictoriaPark #PerthCars #UsedCarsPerth #JapaneseImportsPerth (only if the car is a Japanese import — never tag a car as an import if it is not).
- **CTA:** call 0434 137 393, or enquire on monsoormotors.com.au.

### File naming and storage

- Pack folder: `Ready Posts/<YYYY-MM-DD>-<year>-<make>-<model>/` (for example `Ready Posts/2026-11-20-2018-mazda-mazda3-sp25-astina/`)
- Statics: `<slug>-9x16.jpg`, `<slug>-1x1.jpg`, `<slug>-4x5.jpg`
- Reel: `<slug>-reel-30s.mp4`, `<slug>-script.md`, `<slug>-caption.txt`
- Videos and audio stems stay out of git (`.gitignore` already blocks `.mp4` / `.mov`). Store the Higgsfield link in the log instead. Save the script, caption, storyboard and logs in git.

## Step 5 — Edit like a human, not AI

From CLAUDE.md, 18 Nov 2026 — "Video editing — make it look human, not AI". This relaxes the old 17 Nov no-grade rule: subtle, natural human-style editing only.

- Cut on movement — a door closing, a head turn, a wipe — not in a still pose.
- Vary shot lengths: mix 1–2 s detail shots with 3–5 s hero shots. Never make every shot the same length.
- Keep 9:16, 1080 x 1920, faces and text in the centre safe area.
- Subtle handheld feel only: a tiny reframe or slow push-in. No zoom punch, no flash cut, no heavy grade, no grain filter.
- Colour: light, natural work only. Match white balance and exposure between shots.
- Sound: natural room tone under everything. Music about 13 dB under the voice.
- Reject on sight: too-smooth floaty motion, waxy paint, plastic-looking skin, hands or badges that morph between cuts, dead silence, or an over-polished voiceover with no room sound.
- Never retime a shot. Never change a real car's colour, condition or features.

## Step 6 — Logging

Log every job in the skill folder, under `.claude/skills/monsoor-video-content/assets/`:

- `GENERATION-LOG.md` — one line per generation: date, car, project, model, prompt file, seed, references, cost, result link, keep / reject and why.
- `ASSET-REGISTER.md` — every reusable asset: owner character board and Soul ID, car object boards, reference element IDs, logos, approved style prompts, music. One entry per car, with its listing URL.
- `CREDIT-LOG.md` — one line per spend: date, car, shot, model, credits, balance before / after, cap agreed with the owner.
- Save winning prompts in `assets/prompts/<slug>.md` so they can be reused exactly.
- Add the day's summary to `Monsoor Motors - Playbook & Daily Log.md` (Daily Log), with the car, the pack produced, credits spent, and the status (ready to upload / awaiting owner / stopped at Step 0 and why).

## Legal and guardrails

- Australian Consumer Law / ACCC: no misleading ads. Price, year, kilometres, features and condition must match the live listing exactly. If the listing changes, update the content before posting — never post an old price.
- No fake reviews, fake testimonials, fake customer counts, or fake before/after results.
- Label AI content where Instagram, TikTok or Facebook require it. Any AI avatar of the owner must be labelled as AI in the first 2 s and in the caption.
- Only show staff or customers who have agreed. Blur all number plates.
- No sexualised content, no violence, no copied music, no other brand's badges presented as Monsoor Motors' own.
- Never create a likeness of a real person without their written OK. Never imitate a celebrity.
- Never spend money, buy credits, or create an account without the owner's stated cap. Never spend Higgsfield credits on a car that failed Step 0.

## How Claude Code runs this by itself

When the owner types one prompt in Claude Code, in the repo folder, Claude Code must:

1. Load this skill (`monsoor-video-content`) and `.claude/skills/aureus-video-studio/SKILL.md`.
2. Read `CLAUDE.md`, `Monsoor Motors - Playbook & Daily Log.md`, and the logs in `.claude/skills/monsoor-video-content/assets/`.
3. Run Step 0 first — fetch the live stock page and verify the exact car. If it is not there, stop and ask the owner for the listing.
4. Build or reuse the character board (Step 1) and the car object board (Step 2).
5. Work down the free-first ladder (Step 3). Show the minimum-credit plan and get the owner's cap before any Higgsfield spend.
6. Produce the full output pack (Step 4), edit it to the human look (Step 5), and log it (Step 6).
7. Report back short, in the same chat: the car, the price and kilometres used, what was made, credits spent (or "0 credits — free only"), and what is ready to upload.

**One-prompt example:**

```
video content: 2018 Mazda Mazda3 SP25 Astina
```

Claude Code then fetches the live listing for that Mazda3, checks it is for sale at the listed price and kilometres, reuses the owner's character board, builds the car's object board from its real photos, makes the 3 statics and the 30 s reel free-first, and reports the pack, the credits spent, and the upload-ready files — without the owner having to prompt it again for each step.

## Free tools — what each one is for

- **Canva free:** statics, text overlays, frosted-glass labels, brand colours, 9:16 / 1:1 / 4:5 crops. No paid templates, no paid stock photos.
- **CapCut free:** reel editing, clean cuts, captions, natural room tone, music at 13 dB under the voice. Export 9:16, 1080 x 1920.
- **`make_ad_v6.py` style (repo):** standalone shots only, clean cuts, muted glass visuals, logo bottom centre, master to -14 LUFS. Reuse it instead of rebuilding an edit from scratch.
- **Free text-to-speech:** first voice option for any script. Use it to test the script before spending on a cloned voice.
- **Owner voice, cloned:** only with the owner's consent, from the approved voice reference. Never clone a voice from a video or call without that consent.
- **Real dealer photos:** the first and best source for every static. A generated image is never a substitute for a missing real photo of the car for sale.

## Rejection checklist — do not upload if any of these is true

- [ ] The price, year or kilometres on screen does not match the live listing
- [ ] A number plate is visible and unblurred
- [ ] The car's colour, wheels, badges or features look different from the real car
- [ ] The owner avatar's face has changed, or it looks like someone else
- [ ] The reel says the car is for sale, but Step 0 found it sold or under offer
- [ ] An AI avatar shot has no "AI AVATAR" label in the first 2 s
- [ ] The caption names a feature, a price or a kilometre figure that is not in the listing

## First-run checklist

- [ ] Step 0 passed — car verified in live stock, for sale, price/kilometres/photos recorded
- [ ] Character board exists in ASSET-REGISTER.md, or was built from owner photos with consent
- [ ] Object board built from real dealer photos, plates blurred
- [ ] Free-first ladder followed — Higgsfield plan and cap agreed before any spend
- [ ] Output pack complete — 3 statics, 30 s reel, script, storyboard, caption, hashtags, CTA
- [ ] All three logs updated, plus the Playbook Daily Log entry
- [ ] Owner told, in one short message, what is ready to upload and what it cost
