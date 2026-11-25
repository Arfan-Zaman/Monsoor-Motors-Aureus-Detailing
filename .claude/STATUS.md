# Status

Claude updates this file after every step and pushes it to GitHub. Newest entry at the top.

---

## 26 Nov 2026: A-frame v4 with the Outlander photo

**What I did**
- Built the owner's Higgsfield Outlander PHEV photo into the A-frame as the hero (top half), headline "CAR WASH & DETAILING" on the polished floor, three packages in columns, white booking band (phone, bold address, website, hours, QR). Plate left as is (owner said don't blur). Fixed the same logo-reflection hairline in the horizontal logo copy.
- Uploaded the photo to Higgsfield (media d1a149d3-ff9c-4ac9-b31d-188b611a1de6); 4K upscale quoted at 2 credits, waiting for the owner's OK.

**Files changed**
- `Aureus Detailing/10 Print/A-Frame 600x900/` (aframe.html, PDF, preview, assets/outlander*.{png,jpg}, assets/logo-horizontal.svg)
- `.claude/STATUS.md`

**What's next**
- Upscale to 4K (2 credits) and swap it in so the photo prints sharp at 600 mm.

---

## 25 Nov 2026: A-frame redesigned to a professional sign layout (v3)

**What I did**
- Researched A-frame sign practice (read from distance, sign not flyer, clear hierarchy, high contrast) and rebuilt the design: logo lockup top left, oversized chrome A as a faint supergraphic, huge left-aligned "CAR WASH & DETAILING", a price menu (Silver $149, Gold $199, Aureus $299), and an ice-white booking band with phone, bold address, website, hours and a QR code. Pink now only on prices (brand 10% rule). QR tested: opens https://aureusdetailing.com.au.
- Added `render.sh` in the A-frame folder to rebuild the PDF and preview.

**Files changed**
- `Aureus Detailing/10 Print/A-Frame 600x900/` (aframe.html, render.sh, print PDF, preview JPG, assets/)
- `.claude/STATUS.md`, playbook daily log

**What's next**
- Owner approves, then send the PDF to the printer.

---

## 25 Nov 2026: A-frame now shows the website and a QR code

**What I did**
- Added aureusdetailing.com.au (checked live) and a vector QR code to it ("Scan to book") in a bottom row beside the address and hours. Tested the QR from the rendered PDF: it decodes to https://aureusdetailing.com.au. Logo and headline slightly smaller to make room.

**Files changed**
- `Aureus Detailing/10 Print/A-Frame 600x900/` (aframe.html, print PDF, preview JPG, assets/qr-website.svg)
- `.claude/STATUS.md`, playbook daily log

**What's next**
- Owner approves, then send the PDF to the printer.

---

## 25 Nov 2026: Aureus A-frame sign (600 x 900 mm)

**What I did**
- Designed the Aureus Detailing A-frame for the owner: big chrome logo, "by Monsoor Motors Pty Ltd", "CAR WASH & DETAILING", three packages with line icons and from-prices (Silver $149, Gold $199, Aureus $299), pink "Call to book 0434 137 393" bar, address in bold, hours. Vector only, no photos (the owner rejected the AI foam car photo as cheap). Print PDF has 3 mm bleed (606 x 906 mm).
- Print copy of the logo fixes a faint hairline under the wordmark (reflection mask edge).

**Files changed**
- `Aureus Detailing/10 Print/A-Frame 600x900/` (aframe.html source, print PDF, preview JPG, assets/logo-print.svg)
- `Monsoor Motors - Playbook & Daily Log.md`, `.claude/STATUS.md`

**What's next**
- Owner approves the design, then send the PDF to the printer (ask for 3 mm bleed, double-sided if both faces are wanted).

---

## 24 Nov 2026: posting times moved to 5–8:30 pm Perth

**What I did**
- Moved every post into the owner's ideal window, 5 pm to 8:30 pm Perth, at least 30 minutes apart across both brands. Days and counts unchanged. Republished the page, rebuilt the one-page PDF, and replaced the old "Tue/Wed 6–7 pm" default in playbook section 6.

**Files changed**
- `Social Media Calendar/Weekly-Social-Calendar.html`, `Social Media Calendar/Weekly-Social-Calendar.pdf`
- `Monsoor Motors - Playbook & Daily Log.md`, `.claude/STATUS.md`

**What's next**
- Sync the main folder on the Mac once its file reorganisation is committed.

---

## 24 Nov 2026: calendar saved as PDF

**What I did**
- Exported the "What to post each day" table to a one-page A4 landscape PDF and checked it renders fully (Montserrat, nothing cut off).

**Files changed**
- `Social Media Calendar/Weekly-Social-Calendar.pdf`
- `Monsoor Motors - Playbook & Daily Log.md`, `.claude/STATUS.md`

**What's next**
- Merge the branch into main when the owner says.

---

## 24 Nov 2026: posting days changed to Mon, Wed, Fri, Sat

**What I did**
- Moved every post onto Monday, Wednesday, Friday and Saturday as asked. Counts unchanged: Monsoor 5 static + 2 video (videos Wed, Sat), Aureus 4 static + 2 video (videos Mon, Fri). Republished to the same link.

**Files changed**
- `Social Media Calendar/Weekly-Social-Calendar.html`
- `Monsoor Motors - Playbook & Daily Log.md`, `.claude/STATUS.md`

**What's next**
- Start posting to the table; merge the branch into main when the owner says.

---

## 24 Nov 2026: calendar set to 4 posting days

**What I did**
- Moved every post onto Monday to Thursday; Friday to Sunday have no posts. Counts unchanged: Monsoor 5 static + 2 video (videos Tue, Thu), Aureus 4 static + 2 video (videos Mon, Wed). Republished to the same link.

**Files changed**
- `Social Media Calendar/Weekly-Social-Calendar.html`
- `Monsoor Motors - Playbook & Daily Log.md`, `.claude/STATUS.md`

**What's next**
- Start posting to the table; merge the branch into main when the owner says.

---

## 24 Nov 2026: calendar trimmed to "what to post each day"

**What I did**
- Kept only the daily table (statics and videos per business, with times and topics). Removed the slot grid, the four dated weeks and the rules section; they stay in git history. Republished to the same link.

**Files changed**
- `Social Media Calendar/Weekly-Social-Calendar.html`
- `Monsoor Motors - Playbook & Daily Log.md`, `.claude/STATUS.md`

**What's next**
- Start posting to the table; merge the branch into main when the owner says.

---

## 24 Nov 2026: calendar redone as statics + videos per day

**What I did**
- Rebuilt the calendar in the format asked: each day shows how many static posts and videos each business posts. Monsoor: 5 statics + 2 videos (videos Tue and Thu). Aureus: 4 statics + 2 videos (videos Wed and Sat). All four weeks (30 Nov – 27 Dec) refilled to match and checked by script. Republished to the same link.

**Files changed**
- `Social Media Calendar/Weekly-Social-Calendar.html`
- `Monsoor Motors - Playbook & Daily Log.md`, `.claude/STATUS.md`

**What's next**
- Owner confirms the flagged facts, then week 1 gets scheduled in Meta Business Suite.

---

## 24 Nov 2026: weekly social media calendar

**What I did**
- Built a weekly social calendar for both brands: fixed weekly slots (Perth time) plus the next four weeks (30 Nov – 27 Dec) planned post by post with captions, photo sources and items to confirm. Published it as a private page.

**Files changed**
- `Social Media Calendar/Weekly-Social-Calendar.html`
- `Monsoor Motors - Playbook & Daily Log.md`, `.claude/STATUS.md`

**What's next**
- Owner confirms the flagged facts (stock, prices, finance wording, holiday hours, permissions), then week 1 gets scheduled in Meta Business Suite.

---

## 21 Nov 2026: outfit locked (olive watch dial)

**What I did**
- Changed the Seiko dial to olive, matching the sunglass lenses (0.5 credit), and composited only the two watches onto the final sheet so nothing else changed. Saved as the element `Arfan-CEO-Outfit-Locked` and filed in the CEO Intro project.
- Wardrobe work total: 9.75 of the 10 credits allowed.

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/Wardrobe/Arfan-CEO-Wardrobe-Sheet-Final.png`, `PERSONA.md`
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to delete superseded elements in the web app and import the locked ones into the CEO Intro project.

---

## 21 Nov 2026: final outfit element (burnt wooden buttons, Ray-Ban Meta glasses)

**What I did**
- Edited the wardrobe sheet once more (1 credit, GPT Image 2.6 at medium quality): real burnt wooden buttons and Arfan's Ray-Ban Meta Wayfarer Gen 2 glasses (shiny black, green lenses). Saved as the element `Arfan-CEO-Outfit-Final` and filed in the CEO Intro project.
- Wardrobe work total: 9.25 of the 10 credits allowed.

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/Wardrobe/` (final sheet, glasses photo, old versions), `PERSONA.md`
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to delete superseded elements in the web app (Arfan-CEO, Arfan-CEO-Master, Arfan-CEO-Wardrobe, Japan-Auction-Yard-Plate, Perth-Foreshore-Skyline-Plate, Monsoor-CHR-Hybrid-Black) and import the final ones into the CEO Intro project's Elements tab.

---

## 21 Nov 2026: new Cinema Studio project and Arfan's wardrobe reference

**What I did**
- Created the Higgsfield Cinema Studio project "Monsoor Motors - CEO Intro" with folders in the tutorial's order (storyboard, characters, locations, props, voice, shot 1, shot 2, final edit) and filed every asset into it, including the storyboard, floor plan and previs video.
- Downloaded the real outfit product photos into `Brand Kit/Characters/Arfan-CEO/Wardrobe/` and made a wardrobe sheet: v3 has a matte ramie-cotton shirt and looser, longer trousers.
- Credits for this work: 8.25 of Arfan's 10.

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/Wardrobe/`, `PERSONA.md`
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Burnt wooden buttons need one more edit (2.75 credits, over the 10 cap): Arfan to approve. Then replace the wardrobe element and import elements into the project in the web app.

---

## 21 Nov 2026: Arfan's final character element and personality

**What I did**
- Made a 2K close-headshot sheet from the master full-body sheet (2.75 credits) and created the final character element `Arfan-CEO-Final` (headshots + full-body v2 + portrait crop). Its description is his personality, speech, body language, locked voice and outfit.
- Removed the older versions of Arfan from the Higgsfield project and moved the old local sheets to `Old versions (do not use)/`.
- Wrote `Brand Kit/Characters/Arfan-CEO/PERSONA.md` (public-safe). Saved his full background to local memory only.

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/` (headshots, crop, PERSONA.md, old versions folder)
- `.claude/skills/aureus-video-studio/SKILL.md`, `assets/ASSET-REGISTER.md`, `assets/GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to delete the old elements `Arfan-CEO` and `Arfan-CEO-Master` in the Higgsfield web app. Then the shot 1 draft (27 credits).

---

## 21 Nov 2026: voice version 10 locked

**What I did**
- Arfan locked version 10 as his final voice track. Saved it as `Arfan-script-voice-LOCKED.wav`, renamed take 7 so only one file says LOCKED, and updated the plan and asset register.

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/voice/Arfan-script-voice-LOCKED.*`, `Arfan-script-voice-7.*`, `PLAN.md`
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`
- `.claude/STATUS.md`

**What's next**
- Shot 1 draft, 27 credits, when Arfan says go.

---

## 21 Nov 2026: Arfan voice version 10 (three pronunciation fixes)

**What I did**
- Generated take 9 with take 8 as the audio reference and only the three fixes stated (longer "lot", drawn-out "mates", deeper M and N). The rest of take 9 drifted, so version 10 joins take 9's opening onto take 8's untouched remainder (23.4 s).

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/voice/Arfan-script-voice-9.*`, `Arfan-script-voice-10.*`
- `.claude/skills/aureus-video-studio/assets/GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to confirm version 10 as the locked track. Then the shot 1 draft (27 credits).

---

## 21 Nov 2026: real cost plan for the video

**What I did**
- Got real Higgsfield quotes for every step and wrote a costed plan: minimal path 320 credits (drafts 96 + 720p finals 224), floor 224, 1080p path 608.
- Checked the transaction list: 183.39 credits spent this session (voice clones 120, voice lines 32.9, images 30.25). Corrected my earlier underquote on voice takes in the plan, the log and memory.

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/PLAN.md` (Cost section)
- `.claude/skills/aureus-video-studio/assets/GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to lock take 7 or take 8, then approve the first spend: shot 1 draft, 27 credits.

---

## 21 Nov 2026: Arfan voice take 8

**What I did**
- Arfan liked take 7's accent and asked for it closer to his own voice and very slightly husky. Made take 8 (natural pitch, slight husky cue, same accent and script). Filed in the project's Voices folder.

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/voice/Arfan-script-voice-8.*`
- `.claude/skills/aureus-video-studio/assets/GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to say whether take 8 replaces locked take 7. Then the test still.

---

## 21 Nov 2026: voice locked, project organised, realism workflow adopted

**What I did**
- Re-voiced Arfan's script with his new opening ("That means a lot. Hello mates, this is Arfan.") and locked it: `Arfan-script-voice-7-LOCKED.wav`, 23.0 s.
- Studied Higgsfield's tutorial (youtu.be/1BzzdY-nK9A) and wrote its method into the video skill as section 9, with how to use the AI direction model (Cinema Studio 4.0).
- Applied it: made a three-quarter angle of the auction yard and saved both views as the element `Japan-Auction-Yard-2-Views`. Filed the outfit photos in the project.

**Files changed**
- `.claude/skills/aureus-video-studio/SKILL.md` (section 9), `assets/ASSET-REGISTER.md`, `assets/GENERATION-LOG.md`
- `Ready Posts/2026-11-21-ceo-intro-video/PLAN.md`, `voice/Arfan-script-voice-7-LOCKED.*`, `location/Japan-Auction-Yard-Plate-v1-three-quarter.png`
- `.claude/STATUS.md`

**What's next**
- Test still: Arfan, Monsoor and the C-HR on the auction yard (about 2.75 credits). Then keyframes and 480p drafts.

---

## 21 Nov 2026: Arfan voice versions 5 and 6

**What I did**
- Version 5: Arfan recorded his greeting; generated the opening in that voice (`Arfan-CEO-Opening`) and spliced it onto take 3.
- Version 6: one new full take with a fuller, stronger tone, British-Australian blend, fully fluent (pitch one step lower).
- Both filed in the Higgsfield project's Voices folder.

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/voice/Arfan-script-voice-5.*`, `Arfan-script-voice-6.*`
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to pick the final voice track (5 or 6). Then keyframe stills on the auction yard background.

---

## 21 Nov 2026: standard background (Japanese auction yard) and re-voiced opening

**What I did**
- Arfan rejected the Perth foreshore background. Made a 2K Japanese auction yard plate and saved it as the element `Japan-Auction-Yard-Plate`: the one background for all Monsoor Motors videos. Filed in the project's Locations folder.
- Re-voiced only Arfan's opening ("Thank you for the opportunity. Hello, this is Arfan.") in two tones and spliced each onto take 3: versions 4A and 4B.

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/location/` (two plates), `voice/Arfan-script-voice-4A.*`, `4B.*`, `PLAN.md`
- `.claude/skills/aureus-video-studio/SKILL.md`, `assets/ASSET-REGISTER.md`, `assets/GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to pick 4A or 4B. Then make the two keyframe stills on the auction yard background.

---

## 21 Nov 2026: everything filed in the Monsoor Motors project; blocking and Monsoor's voice approved

**What I did**
- Made three folders in the Higgsfield project Monsoor Motors (Characters, Cars, Voices) and filed all 13 assets: every Arfan sheet, Monsoor's sheet, the C-HR sheet and photos, the voice lines and Monsoor's voice reference.
- Wrote the rule into the video skill and saved it to memory: file every Monsoor asset in the project when it is made.
- Arfan approved the 3D blocking and Monsoor's voice line. Marked both in the plan.

**Files changed**
- `.claude/skills/aureus-video-studio/SKILL.md`, `assets/ASSET-REGISTER.md`
- `Ready Posts/2026-11-21-ceo-intro-video/PLAN.md`
- `.claude/STATUS.md`

**What's next**
- Price and make the two keyframe stills (start of each shot), filed in the project.

---

## 21 Nov 2026: Arfan approved voice take 3

**What I did**
- Arfan approved `Arfan-script-voice-3.wav` as his final voice track. Marked it in the plan and the generation log.

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/PLAN.md`
- `.claude/skills/aureus-video-studio/assets/GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to approve Monsoor's voice line and the 3D blocking. Then make the two keyframe stills (priced first).

---

## 21 Nov 2026: Arfan's script, take 3 (fluent, accent, 23 s)

**What I did**
- Regenerated Arfan's script in voice `Arfan-CEO-2` with a delivery cue (fluent flow, correct pronunciation, light British accent with an Australian tone) and a 23 s time window. Result is 23.0 s and fits shot 2.

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/voice/Arfan-script-voice-3.wav` and `.mp3`
- `.claude/skills/aureus-video-studio/assets/GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to approve take 3. Then approve the blocking and move to keyframe stills.

---

## 21 Nov 2026: both scripts voiced

**What I did**
- Arfan re-recorded his voice (`Arfan-CEO-2`). Generated Monsoor's script in his cloned real voice (8.7 s, fits shot 1) and Arfan's script in his new voice (30.4 s; shot 2 allows about 22 s).

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/voice/Monsoor-script-voice-1.*`, `Arfan-script-voice-2.*`, `Arfan-voice-sample-lines-2.md`, `PLAN.md`
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to approve both voices. Then settle the timing of his part: lengthen shot 2 to about 31 s or trim the script.

---

## 21 Nov 2026: Arfan voice test line

**What I did**
- Generated Arfan's full script in his cloned voice `Arfan-CEO-1` (2.1 credits) for him to hear. It runs 31.1 s against about 22 s planned for shot 2.

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/voice/Arfan-voice-test-1.wav` and `.mp3` (audio may stay local)
- `.claude/skills/aureus-video-studio/assets/GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to say whether it sounds like him. Then fix the timing (faster rate, shorter script, or a longer shot).

---

## 21 Nov 2026: Monsoor's voice reference found

**What I did**
- Checked the last Monsoor Motors reel (Mercedes ML300 review reel, 20 Nov 2026). It used Monsoor's real voice, cloned from a 15 s clip of a Facebook reel. Copied that reference into the CEO intro folder and recorded its Higgsfield ID in the asset register and plan.

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/voice/monsor-voice-ref.wav`, `PLAN.md`
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`
- `.claude/STATUS.md`

**What's next**
- Both voices are ready (Arfan `Arfan-CEO-1`, Monsoor via audio reference). Next: approve blocking, then keyframe stills.

---

## 21 Nov 2026: Arfan's voice clone created

**What I did**
- Arfan recorded his sample lines in the Higgsfield voice recorder; the voice `Arfan-CEO-1` is created and ready. Recorded its ID in the asset register and the plan.
- The separate local recording `voice/arfan-voice-ref.wav` came out silent (room noise only), so it was not used.

**Files changed**
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`
- `Ready Posts/2026-11-21-ceo-intro-video/PLAN.md`
- `.claude/STATUS.md`

**What's next**
- Test the voice on one script line. Still needed: a real recording of Monsoor's voice.

---

## 21 Nov 2026: C-HR element sheet, script opening, voice sample lines

**What I did**
- Made a 2K six-view grey studio sheet of the real black Toyota C-HR Hybrid (2.75 credits) and saved it as the element `Monsoor-CHR-Hybrid-Black-Sheet` in the Higgsfield project Monsoor Motors.
- Changed Arfan's opening line to "Thank you for the opportunity. Hello, this is Arfan." in the plan and the previs labels.
- Wrote seven short sample lines for Arfan to read for his voice clone.

**Files changed**
- `Cars/Toyota C-HR Hybrid (black)/` (photos and sheet)
- `Ready Posts/2026-11-21-ceo-intro-video/PLAN.md`, `voice/Arfan-voice-sample-lines.md`, `previs/previs_post.py`, storyboard
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan records the sample lines; then create his Higgsfield voice. Confirm which recording is Monsoor's real voice (the files on record are the AI "master detailer" voice).

---

## 21 Nov 2026: CEO intro previs v3 and both characters filed in Monsoor Motors project

**What I did**
- Reworked the intro: Arfan stays on his mark and the camera travels to his side; stronger trust script ending "You choose the car. We bring it to your home."; richer 3D set (showroom, hero C-HR on plinth, stock cars, banners). Rendered the full 32 s video in Blender (EEVEE). Free.
- Filed Monsoor's approved full-body sheet (element `MA-Monsor-Owner-v2`) in the Higgsfield project Monsoor Motors, next to Arfan's master sheets (element `Arfan-CEO-Master`).

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/PLAN.md` (version 3)
- `Ready Posts/2026-11-21-ceo-intro-video/previs/` (scripts, .blend, storyboard, floor plan; the .mp4 stays local)
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to approve blocking and script, then send real C-HR photos and two voice samples, and confirm home delivery terms.

---

## 21 Nov 2026: CEO intro video 3D previs (two shots) and master element

**What I did**
- Reworked the intro video into two shots (27 s) and rendered the whole video as 3D blocking in Blender: framing, lenses, camera moves, the walk, gestures and script timing. Free, no credits.
- Saved Arfan's chosen master sheets as the element `Arfan-CEO-Master` and filed them in the Higgsfield project Monsoor Motors.

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/PLAN.md` (version 2)
- `Ready Posts/2026-11-21-ceo-intro-video/previs/` (scripts, .blend, storyboard, floor plan; the .mp4 stays local)
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to approve the blocking and script, then send the founder's photos and OK, real C-HR photos and two voice samples.

---

## 21 Nov 2026: "Meet our new CEO" intro video plan

**What I did**
- Wrote the plan for the Monsoor Motors intro video: founder introduces Arfan, Arfan takes over the scene and makes his promise, C-HR behind them. Six scenes, draft script, nine-step workflow. No credits spent.

**Files changed**
- `Ready Posts/2026-11-21-ceo-intro-video/PLAN.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to approve the script and send: founder's photos and written OK, real C-HR photos, a 30 s voice sample from each of them. Then build the founder's character sheet.

---

## 21 Nov 2026: Arfan chose full-body sheet v2 as the master

**What I did**
- Arfan preferred v2 over v3. Marked v2 (job `26e6c1c6`) as the master full-body sheet and v3 as not used. No credits spent.

**Files changed**
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Use element `Arfan-CEO`, face sheet v3 and full-body sheet v2 as references for any image or video of Arfan.

---

## 21 Nov 2026: Arfan (CEO) full-body sheet v3 (neck balanced)

**What I did**
- Arfan said the neck looked long. Made v3 as an edit of v2: balanced neck, plain point collar, natural build, same face (2.75 credits; 8.25 of the 10 allowed used).

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/Arfan-CEO-Full-Body-Sheet-v3.png`
- `.claude/skills/aureus-video-studio/assets/prompts/arfan-ceo-full-body-sheet.md`, `ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to approve v3 as the master full-body sheet. 1.75 credits left in this budget, not enough for another 2K run.

---

## 21 Nov 2026: Arfan (CEO) full-body sheet v2 (face fix)

**What I did**
- Made full-body sheet v2 with a stronger face block: fuller face, calm expression (2.75 credits; 5.5 of the 10 allowed used).

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/Arfan-CEO-Full-Body-Sheet-v2.png`
- `.claude/skills/aureus-video-studio/assets/prompts/arfan-ceo-full-body-sheet.md`, `ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to pick v1 (truer shirt) or v2 (truer face). 4.5 credits left in the budget for one more run if wanted.

---

## 21 Nov 2026: Arfan (CEO) full-body sheet and reference elements

**What I did**
- Saved Arfan's sheet v3 as the Higgsfield character element `Arfan-CEO`.
- Found real product photos (black linen shirt, coffee gurkha trousers, black Chelsea boot, Seiko SRPD55) and saved each as a reference element.
- Made the full-body sheet at 2K with sculpted studio lighting using those elements: 2.75 credits of the 10 allowed.

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/Arfan-CEO-Full-Body-Sheet-v1.png`
- `.claude/skills/aureus-video-studio/assets/prompts/arfan-ceo-full-body-sheet.md`, `ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to approve. Optional second run (2.75 credits) to make the face fuller and the expression calmer, closer to his photos.

---

## 21 Nov 2026: Arfan (CEO) character sheet v3 (eyes and lighting fixed)

**What I did**
- Arfan said the eyes and eyebrows looked fake. Made v3 with natural eyes and brows and a real studio lighting setup (2.75 credits). Profiles and both hands are now correct too.

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/Arfan-CEO-Character-Sheet-v3.png`
- `.claude/skills/aureus-video-studio/assets/prompts/arfan-ceo-character-sheet.md`, `ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to approve v3. Then save it as a Higgsfield reference element for future videos.

---

## 21 Nov 2026: Arfan (CEO) character sheet made

**What I did**
- Made 2 character sheets at 2K on a grey background with GPT Image 2.6, using all 14 of Arfan's photos (5.5 credits). Both look like him.
- Saved the prompt for reuse and recorded the job IDs.

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/Arfan-CEO-Character-Sheet-v2a.png`, `-v2b.png`
- `.claude/skills/aureus-video-studio/assets/prompts/arfan-ceo-character-sheet.md`, `ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to pick v2a or v2b. Optional: one more run to fix the small faults (profile or three-quarter direction, left hand), then save the winner as a Higgsfield reference element.

---

## 21 Nov 2026: Arfan (CEO) character sheet, first try

**What I did**
- Uploaded Arfan's 14 reference photos (10 face angles, 4 hand shots) to Higgsfield and saved copies in the Brand Kit.
- Made 2 sheets with Soul 2.0 (under 1 credit). Both rejected: no panels, no grey background, face changed in one.

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/source/` (14 photos)
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to choose: GPT Image 2.6 with all 14 photos (about 5.5 credits for 2 versions at 2K), or train a Soul ID first.

---

## 20 Nov 2026: rule merged into main

**What I did**
- Merged the latest `main` from GitHub into this branch (no conflicts), then pushed it to `main`. Every session now gets the push + status rule.

**Files changed**
- `.claude/STATUS.md` (this entry). `CLAUDE.md` and `Tools/autosave.sh` are now on `main`.

**What's next**
- Nothing pending for this task. The next session that works here adds its own entry above this one.

---

## 20 Nov 2026: push + status rule set up

**What I did**
- Added the rule "after every step, push to GitHub and update this file" to `CLAUDE.md`, so every future session follows it.
- Fixed auto-save: on new worktree branches it ran a plain `git push`, which failed without telling anyone because the branch had no upstream. It now runs `git push -u origin HEAD` the first time.
- Created this status file.

**Files changed**
- `CLAUDE.md` (Git rules section)
- `Tools/autosave.sh` (push step)
- `.claude/STATUS.md` (new)

**What's next**
- Merge this branch (`claude/github-push-status-workflow-15710a`) into `main` so all sessions pick up the rule. Local `main` is also 8 commits behind `origin/main`.
