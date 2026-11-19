---
name: monsoor-video-content
description: Use for any Monsoor Motors or Aureus Detailing sell content — statics and reels for a stock car for sale, or for a real detailing job. Autonomous agent skill: on one prompt it fetches the real live stock, connects itself to the free tools, builds the owner / master detailer character board and the car object board, and produces a ready-to-upload pack (3 statics + 1 x 30 s reel) with real prices only, totally free by default, and totally realistic — like a real AI film, not AI-looking content. Higgsfield only when a free tool cannot do the job, and then only the minimum credits, under an owner cap. Load before making any Monsoor Motors or Aureus Detailing content.
---

# Monsoor Motors / Aureus Detailing video content — autonomous agent, free first, totally realistic

Make sell content for one real Monsoor Motors car at a time — and, with the same rules, content for one real Aureus Detailing job at a time — ready to upload immediately to Instagram, Facebook and TikTok. The agent does the whole job by itself on one prompt. Default is 0 credits. Higgsfield is last, and only for what free tools cannot do. Never invent a car, a price, a year, kilometres, or a feature.

**Main purpose of everything in this skill: create totally realistic AI content for Monsoor Motors right now — and for Aureus Detailing too.** Lots of realistic videos on Instagram look totally real — real AI films — but our attempts have looked AI-generated. This agent must close that gap. Realism is the test on every job, not a nice extra. If a shot looks AI, it fails, even if it cost credits.

Version: v2, 20 Nov 2026 — autonomous agent mode, free-first, totally realistic. Supersedes v1 (pushed 20 Nov 2026, commit 3ddc16904faee52bb28dd5e7507d8442eb77b9a4).

## Business facts — do not change these

- **Monsoor Motors Pty Ltd**, ABN 31 695 324 193, MV Licence MD32748
- **530 Albany Highway, Victoria Park WA 6100**
- **Phone 0434 137 393** — the only phone number to use
- **info@monsoormotors.com.au** — monsoormotors.com.au
- Owner: **M A Monsor — Mohammod A Monsor, Owner & Director**
- No rentals. No lease-to-own. No "Rent-To-Own" wording anywhere.
- Wrong numbers — flag them, never use them: 0433 205 162, 0483 153 638, (08) 4931 0421
- Australian English: licence, colour, organise, kilometres.

## Section 0 — Autonomous agent mode: do it yourself, on one prompt

This skill is an agent, not a checklist for the owner to drive step by step. When the owner types one prompt, the agent runs the whole job by itself, in this order, without asking the owner at each step:

1. **Connect** — run the tool-connection checklist in Section 0A.
2. **Fetch** — Step 0. Verify the exact car is real and for sale.
3. **Boards** — reuse or build the owner character board (Step 1) and the car object board (Step 2).
4. **Make** — statics free first, then the reel free first (Step 3, Step 4).
5. **Edit** — human look only (Step 5), and totally realistic — real AI film rules on every shot.
6. **Check** — run the self-check quality gate (Step 6). Fix free first, or report the failure. Do not report a failed pack as ready.
7. **Log** — update all three logs and the Playbook Daily Log (Step 7).
8. **Report** — one short message: car, price and kilometres used, what was made, credits spent (or "0 credits — free only"), what is ready to upload, and what, if anything, is still blocked.

**Only stop and ask the owner when one of these is true:**
- The car is not in live stock, or is sold / under offer, or year / price / kilometres / photos are missing (Step 0 stop rule).
- A Higgsfield spend would go over the owner's stated cap, or no cap has been given and a paid shot is needed — show the minimum-credit plan and wait for the cap.
- A step would spend money, create an account, or change a legal claim.
- A legal fact is wrong or missing (for example, the listing price changed mid-job).

Do not stop to ask for approval on: which free tool to use, which photo angle to use first, the script wording, the caption, or the edit. The agent decides those from this skill, does the work, logs it, and reports it.

**One car per job. One car per day.** Slow cadence: do not do a week's work in one day. If the owner gives two cars, do the first, report it, and queue the second for the next day.

## Section 0A — Tool connection: connect itself, at the start of every job

At the start of every job, before any design or generation, run this checklist in order. For each tool, check it is available, use it, and log the result. If a tool is missing or not connected, **use the next free rung and log it — do not fail the whole job, and do not jump to paid.**

| # | Tool | What it is for | Exact source / command where known | If missing / not available |
|---|---|---|---|---|
| 1 | Real dealer photos | The car itself, and the owner | Live listing at https://monsoormotors.com.au/stock, plus repo `Cars/` and `Ready Posts/` in Arfan-Zaman/Monsoor-Motors-Aureus-Detailing | Stop at Step 0 and ask the owner for the photos. Never generate a replacement car photo and present it as the real car. |
| 2 | Canva free | Statics, text overlays, frosted-glass labels, brand colours, 9:16 / 1:1 / 4:5 crops | Canva free plan, in the browser. No paid templates, no paid stock photos. | Use CapCut free text overlays, or the repo `make_ad_v6.py` style labels, instead. Log the swap. |
| 3 | CapCut free | Reel editing, clean cuts, captions, natural room tone, music at 13 dB under the voice. Export 9:16, 1080 x 1920. | CapCut free, desktop or phone. | Use `make_ad_v6.py` in the repo (see #4). Log the swap. |
| 4 | `make_ad_v6.py` | Standalone-shot edits: clean cuts, muted glass visuals, logo bottom centre, master to -14 LUFS | `Aureus Detailing/08 Social Media/Launch Reels/ad/make_ad_v6.py` in the repo. Reuse it instead of rebuilding an edit from scratch. | Use CapCut free (#3). Log the swap. |
| 5 | Free text-to-speech | First voice option for any script. Test the script before spending on a cloned voice. | Any free TTS the agent has access to in Claude Code. Use it for the first voice pass. | Use on-screen text only, with music and room tone, and say so in the report. Do not jump to a paid voice. |
| 6 | Owner voice, cloned | The owner's voice, only with his consent | Approved voice reference from the repo: `ad/audio/v4/persona-voice-ref.wav` (see `.claude/skills/aureus-video-studio/SKILL.md` §8). Never clone a voice from a video or call without that consent. | Use free TTS (#5). Log that the cloned voice was not used. |
| 7 | Higgsfield — LAST | Only: Soul ID consistency for the owner avatar, cinematic car 360, or a photorealistic avatar talking to camera | Higgsfield CLI (`higgsfield`, signed in to the Plus workspace) or the paid Higgsfield connector, plus skill packs: `higgsfield-generate`, `higgsfield-soul-id`, `higgsfield-product-photoshoot`, `higgsfield-prompt-suite` (router, including `skills/higgsfield-camera`, `higgsfield-seedance`, `higgsfield-troubleshoot`), `hf-09-product-360`, `hf-01-cinematic`, `hf-11-social-hook`, `hf-video-01-viral-hook`. See `.claude/skills/aureus-video-studio/SKILL.md` §2 for the full pack table. | Do the free-only pack (0 credits) and report it as free-only. Do not spend to work around a missing free tool. |

**Connection rules for the agent:**
- Check the tools in the order above. Do not skip a free rung because a paid one is faster.
- If two free tools can do the same job, use the one that reuses an existing asset (prompt, keyframe, seed, template) first.
- Record, in `GENERATION-LOG.md`, which tool was used for each piece, and which tool was skipped and why.
- Never connect a new account, sign up for a paid plan, or buy credits on its own. That needs the owner.
- Never claim a tool is connected when it is not. If the agent could not check a tool, write "not checked" in the log, use the free fallback, and say so in the report.

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
2. Build the board with the Higgsfield Soul ID / character-sheet workflow (`higgsfield-soul-id`, `higgsfield-character-design`), following `.claude/skills/aureus-video-studio/SKILL.md` §3. This is the one place Higgsfield may be used even in a free-first job — but only once, to build the board, and only if a free avatar cannot hold his face consistently. If the board already exists in `ASSET-REGISTER.md`, reuse it and spend 0 credits.
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

## Step 3 — Free-first ladder: default 0 credits, Higgsfield LAST and minimal

Work down this ladder. Stop at the first rung that does the job well. Do not jump to Higgsfield because it is faster. **Default is 0 credits.**

| Rung | Job | Free tool first | Higgsfield? |
|---|---|---|---|
| A | Statics | Real dealer photos + Canva free / CapCut free text overlays, brand colours, frosted-glass labels | No |
| B | Reel edit | CapCut free, or `Aureus Detailing/08 Social Media/Launch Reels/ad/make_ad_v6.py` style — clean cuts, real speed, human look | No |
| C | Voice | Free text-to-speech first; the owner's voice only with his consent, cloned from the approved voice reference | No, unless the free voice cannot deliver the script naturally |
| D | Higgsfield only | — | **Only** when a free tool cannot do it: Soul ID consistency for the owner avatar, cinematic car 360, or a photorealistic avatar talking to camera |

Rules for rung D — read before any paid generation:

- **Opt-in per shot.** Higgsfield is never the default. Each paid shot needs its own reason written in the log: what the free tool could not do, and why this shot needs Higgsfield.
- Before any paid generation, check the Higgsfield credit balance (`higgsfield account status`, or the paid connector's `balance`) and show the owner the **minimum-credit plan**: exactly which shots, how many credits each, and the total. Do not spend without a stated cap from the owner. Never exceed the cap.
- Reuse first. Check `assets/GENERATION-LOG.md` and `assets/ASSET-REGISTER.md`. If a keyframe, prompt, seed or reference already exists for this car or this presenter, reuse it instead of generating it again.
- One keyframe still per step, then one short shot per keyframe. Do not generate a long continuous take when clean cuts will do.
- Lint every Seedance prompt with `higgsfield-prompt-suite/scripts/seedance_lint.py` before spending credits.
- Log every credit spent, the same day, in `assets/CREDIT-LOG.md` — date, car, shot, model, credits, result link, keep / reject and why. A job with 0 credits still gets a CREDIT-LOG line: "0 credits — free only".

### Credit budget — known costs from aureus-video-studio

These are the costs recorded in the existing video studio skill. Confirm the current price in Higgsfield before spending, because prices can change.

| Item | Cost |
|---|---|
| Keyframe still | 2 credits |
| 3 s Kling 4.0 shot (start image only) | 9.75 credits |
| Mirelo audio (`mirelo_text_to_audio`) | 0.75 credits per 3 s |

### Worked example 1 — the 0-credit pack (default)

One 30 s reel and 3 statics, 0 credits:
- Statics: real dealer photos + Canva free text overlays (0 credits).
- Reel: real photos and any real video the owner supplies, cut in CapCut free, clean cuts, free TTS voice, natural room tone, music 13 dB under the voice (0 credits).
- Owner on camera: use a real photo of M A Monsor with on-screen text, or a free avatar test — do not spend credits to make him talk if a still + text does the job.
- Report: "0 credits — free only".

### Worked example 2 — the minimum-credit pack

Use this only when the owner agrees a paid avatar / cinematic shot is needed, and only for the shots that need it:
- 4 keyframes (8 credits) + 4 x 3 s Kling shots (39 credits) = **47 credits**, plus audio as needed (0.75 credits per 3 s).
- That is a planning example only — the real plan must be costed shot by shot and agreed with the owner before spending. If the owner sets a cap, stay under it. If the job cannot be done inside the cap, say so and offer the free-only version (example 1) instead.
- Never spend credits on a car that failed Step 0.

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
- **Storyboard:** one line per shot — time, shot, on-screen text, voice line, source (real photo / free edit / Higgsfield shot and its credit cost, or "0 credits — free").
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

## Totally realistic — real AI film (applies to every job, Monsoor and Aureus)

This is the main purpose of the skill. Follow it on every job. A realistic video on Instagram looks like a real person filmed a real car or a real detail — it does not look generated. Our content must pass that test.

**Real footage first — AI only extends, never replaces the real thing:**
- Start from real dealer photos and real video of the actual car for sale, and for Aureus, real photos and video of the actual detailing job.
- AI may extend, animate or fill a real shot — a slow push-in on a real photo, a clean cut between real angles, a real still brought to life for 3 seconds. It must never be a fully synthetic hero shot presented as the real car or the real job.
- If there is no real photo or video of the car / job, stop and ask the owner for it (Step 0). Do not generate a hero car or a hero detail and present it as real.
- For Aureus, before/after only with real results from the same real job, same car, same angle, same light as far as possible. Never invent a before/after, a shine, or a result.

**One consistent person, one consistent car — no morphing:**
- Reuse the Soul ID / character board and the car object board every time. Same face, same car, same wardrobe, same lighting direction, shot after shot.
- For Monsoor, the presenter is M A Monsor (Step 1). For Aureus, the presenter is the master detailer character from `.claude/skills/aureus-video-studio/SKILL.md` §7 — same person, same navy Aureus uniform, every time.
- Check the face, the car, the badge, the wheels and the plates at every cut. If a face changes, a badge changes shape, a wheel changes, or a plate changes between cuts, that shot fails. Reject it and redo it.
- Same seed plus the same references gives a matching look. Log the seed and the reference IDs for every shot, and reuse them.

**Cinematic realism — imperfect is real, perfect looks AI:**
- Natural light only. Real shadows, real reflections, real dust and real yard / workshop background. No studio-perfect light on a car that was photographed in a yard.
- Imperfect handheld feel: a tiny reframe, a slow push-in, a slight wobble. No floaty smooth motion, no drone-smooth glide over a real car, no too-smooth camera move.
- Cut on movement — a door closing, a head turn, a wipe, a hand reaching for a cloth — not in a still pose.
- Vary shot lengths: mix 1–2 s detail shots with 3–5 s hero shots. Never make every shot the same length. Never retime a shot.
- No waxy skin, no plastic paint, no over-smooth metal, no over-sharpened edges. If skin looks plastic or paint looks like CGI, the shot fails.
- No morphing hands, badges, plates, logos or text between cuts. Text must be readable and stable — garbled text is a fail.

**Sound and voice — natural, human, with air in it:**
- Natural, human voice with pauses and breath. Not a rushed, over-polished voiceover with no room sound.
- Real room tone under everything. Music about 13 dB under the voice. No dead silence, no music drowning the voice.
- For Aureus, use the real detailing sounds where they exist — cloth, spray, vacuum, polisher — close-mic, at natural volume, not as a music bed.

**For Aureus Detailing — same rules, different brand:**
- Brand: navy #071A33, aqua #00A8A8, hot pink #FF4D8D (≤10%, buttons and stickers only), white #F5F8FC; Montserrat; chrome A logo. Gold detail offer only if it is the real current offer — check it, do not assume a price.
- Before/after only with real results. No fake results, no fake shine, no fake customer words.
- End card: Aureus Detailing logo, phone 0434 137 393, @aureusdetailing.com.au.
- The Aureus character board and the Monsoor character board are separate. Never mix them — the master detailer does not present a Monsoor car sale, and M A Monsor does not present an Aureus detail as the detailer.

**Realism must not mean unlimited Higgsfield spend:**
- Free-first still applies. Reuse keyframes, prompts, seeds and references first. A realistic look comes mostly from real photos, real light, clean cuts and natural sound — all free.
- Use Higgsfield only for the one thing a free tool cannot do (Soul ID consistency, a cinematic 360 from real photos, a photorealistic avatar talking). One paid shot, costed and capped, is better than five paid shots that all look generated.
- If a paid shot still looks AI, reject it and redo it free first. Do not spend more credits trying to fix an AI-looking shot with more generation.

**Rejection rule — if it looks AI, it fails:**
- Too smooth, too perfect, face changes, car changes, hands or badges morph, paint looks plastic, skin looks waxy, motion floats, voice has no breath — reject it.
- Redo it free first: use the real photo instead, cut it shorter, change the seed and reference, or drop that shot entirely. Do not upload it. Do not spend more credits to save a shot that already looks AI.

## Step 6 — Self-check / quality gate: before reporting "ready to upload"

Run every check below, in order, before telling the owner a pack is ready. If any check fails, fix it free first. If it cannot be fixed free, report the failure plainly — do not upload a failed pack, and do not call it ready.

- [ ] Price on every static, in the script, and in the caption matches the live listing exactly — same dollars, same "Exc. Gov. Charges" wording if that is what the listing says.
- [ ] Year, kilometres, transmission and fuel match the live listing exactly.
- [ ] Every number plate is blurred in every static and every frame.
- [ ] The car's colour, wheels, badges and features match the real car in the dealer photos.
- [ ] The owner avatar's face is unchanged from the character board, and it does not look like someone else.
- [ ] Realism check — the pack looks like a real AI film, not AI-generated: no floaty smooth motion, no waxy skin, no plastic paint, no morphing hands / badges / plates / car between cuts, natural light and real shadows, voice with pauses and breath, room tone present. If any of these fails, the pack fails — redo it free first, do not upload it.
- [ ] For Aureus, the before/after is real, from the same real job, and the brand, character and end card are Aureus, not Monsoor.
- [ ] Every AI avatar shot has "AI AVATAR" on screen in the first 2 s, and the caption says it is AI.
- [ ] The caption names no feature, price or kilometre figure that is not in the listing.
- [ ] The car is still for sale — re-check Step 0 status before reporting. If it sold or went under offer while the job was running, stop and report that instead.
- [ ] CTA is correct: call 0434 137 393, 530 Albany Highway, Victoria Park WA 6100, monsoormotors.com.au. No wrong phone number anywhere.
- [ ] Files are named correctly (Step 4), in the right pack folder, 9:16 1080 x 1920 for the reel, text inside the safe area.
- [ ] All three logs are updated, plus the Playbook Daily Log entry, with credits spent (or "0 credits — free only").
- [ ] No paid shot was used without a logged reason, a minimum-credit plan, and a cap that was not exceeded.

## Step 7 — Logging

Log every job in the skill folder, under `.claude/skills/monsoor-video-content/assets/`:

- `GENERATION-LOG.md` — one line per generation: date, car, project, model, prompt file, seed, references, cost, result link, keep / reject and why. Also record which tool was used for each piece, and which tool was skipped and why.
- `ASSET-REGISTER.md` — every reusable asset: owner character board and Soul ID, car object boards, reference element IDs, logos, approved style prompts, music. One entry per car, with its listing URL.
- `CREDIT-LOG.md` — one line per spend: date, car, shot, model, credits, balance before / after, cap agreed with the owner. A 0-credit job still gets a line: "0 credits — free only".
- Save winning prompts in `assets/prompts/<slug>.md` so they can be reused exactly.
- Add the day's summary to `Monsoor Motors - Playbook & Daily Log.md` (Daily Log), with the car, the pack produced, credits spent, tools used, and the status (ready to upload / awaiting owner / stopped at Step 0 and why).

## Legal and guardrails

- Australian Consumer Law / ACCC: no misleading ads. Price, year, kilometres, features and condition must match the live listing exactly. If the listing changes, update the content before posting — never post an old price.
- No fake reviews, fake testimonials, fake customer counts, or fake before/after results.
- Label AI content where Instagram, TikTok or Facebook require it. Any AI avatar of the owner must be labelled as AI in the first 2 s and in the caption.
- Only show staff or customers who have agreed. Blur all number plates.
- No sexualised content, no violence, no copied music, no other brand's badges presented as Monsoor Motors' own.
- Never create a likeness of a real person without their written OK. Never imitate a celebrity.
- Never spend money, buy credits, or create an account without the owner's stated cap. Never spend Higgsfield credits on a car that failed Step 0.

## How to run it in Claude Code — by itself, on one prompt

When the owner types one prompt in Claude Code, in the repo folder, Claude Code must:

1. Load this skill (`monsoor-video-content`) and `.claude/skills/aureus-video-studio/SKILL.md`.
2. Read `CLAUDE.md`, `Monsoor Motors - Playbook & Daily Log.md`, and the logs in `.claude/skills/monsoor-video-content/assets/`.
3. Run Section 0A first — connect itself to the tools, in order, and log any tool that is missing.
4. Run Step 0 first — fetch the live stock page and verify the exact car. If it is not there, stop and ask the owner for the listing.
5. Build or reuse the character board (Step 1) and the car object board (Step 2).
6. Work down the free-first ladder (Step 3). Default 0 credits. Show the minimum-credit plan and get the owner's cap before any Higgsfield spend.
7. Produce the full output pack (Step 4), edit it to the human look (Step 5), run the quality gate (Step 6), and log it (Step 7).
8. Report back short, in the same chat: the car, the price and kilometres used, what was made, tools used, credits spent (or "0 credits — free only"), and what is ready to upload.

**One prompt — copy and paste this in Claude Code, in the repo folder:**

```
Load the skill at .claude/skills/monsoor-video-content/SKILL.md and follow it exactly.
video content: <exact year, make, model>
```

**One-prompt example:**

```
video content: 2018 Mazda Mazda3 SP25 Astina
```

Claude Code then fetches the live listing for that Mazda3, checks it is for sale at the listed price and kilometres, reuses the owner's character board, builds the car's object board from its real photos, makes the 3 statics and the 30 s reel free-first, runs the quality gate, and reports the pack, the credits spent, and the upload-ready files — without the owner having to prompt it again for each step.

**Daily / autonomous note:** one car per day, slow cadence. Do not do a week's work in one day. If the owner gives a list of cars, do the first, report it, and queue the rest for the following days, one per day, in the order the owner gave them.

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
- [ ] A paid shot was used without a logged reason, a minimum-credit plan, and a cap
- [ ] It looks AI — too smooth, too perfect, face changes, car changes, hands or badges morph, paint looks plastic, skin looks waxy — reject it and redo it free first, do not upload it

## First-run checklist

- [ ] Section 0A passed — tools connected in order, missing tools logged, free fallback chosen
- [ ] Step 0 passed — car verified in live stock, for sale, price/kilometres/photos recorded
- [ ] Character board exists in ASSET-REGISTER.md, or was built from owner photos with consent
- [ ] Object board built from real dealer photos, plates blurred
- [ ] Free-first ladder followed — default 0 credits, Higgsfield plan and cap agreed before any spend
- [ ] Output pack complete — 3 statics, 30 s reel, script, storyboard, caption, hashtags, CTA
- [ ] Quality gate (Step 6) passed — every check ticked, or the failure reported plainly
- [ ] All three logs updated, plus the Playbook Daily Log entry
- [ ] Owner told, in one short message, what is ready to upload and what it cost (or "0 credits — free only")
