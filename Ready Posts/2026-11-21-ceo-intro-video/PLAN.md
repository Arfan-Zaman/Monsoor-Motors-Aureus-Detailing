# Monsoor Motors: "Meet our new CEO" intro video (plan, version 3)

Status: 3D blocking v3 and both voice tracks APPROVED by Arfan, 21 Nov 2026. Next: keyframe stills. No Higgsfield video generated yet, no credits spent on this video.

## The video
- Format: 9:16 vertical, 1080x1920, 32 seconds, two shots. Reels, TikTok, Facebook.
- Aim: announce Arfan as CEO and build trust in the whole business: every kind of car, and Japanese imported hybrids in particular.
- Nobody walks. Arfan stays on his mark and the camera travels to his side.
- Set (changed 21 Nov 2026): a Japanese used-car auction yard, the standard background for all Monsoor Motors videos (element `Japan-Auction-Yard-2-Views`, files `location/Japan-Auction-Yard-Plate-v1-three-quarter.png` and `location/Japan-Auction-Yard-Plate-v1.png`). The two men stand in the empty numbered bays with the black C-HR Hybrid parked behind them, rows of auction cars and the auction hall beyond. The Blender previs still shows the earlier dealership set; positions and camera moves are unchanged.

## Shot list and script

| Shot | Time | Camera | Action | Words |
|---|---|---|---|---|
| 1 | 0 to 9 s | 35 mm, eye level (1.5 m), wide two-shot, slow push-in from 3.75 m to 3.15 m | Monsoor and Arfan side by side, sign above, C-HR behind. Monsoor puts a hand on his heart on "trust", then presents Arfan with an open hand. Cut as Arfan turns to the lens | Monsoor: "I built Monsoor Motors on one thing: trust. Now meet the man who will carry it forward. Arfan, our new CEO." |
| 2 | 9 to 32.4 s | 50 mm. Starts as a tighter two-shot, trucks right to Arfan's side (12 to 17 s), creeps in, then pushes in and drops a little below eye level for the last line | Arfan squares up to the lens and follows the camera with his body. Monsoor leaves frame as the camera travels. Arfan sweeps a hand to the cars, palms down on "no surprises", points at the lens on "YOU", opens both arms on "WE" | Arfan: "That means a lot. Hello mates, this is Arfan. Buying a car is a big decision, so here is my promise. Every car on this yard, from family runabouts to Japanese imported hybrids, is hand-picked, properly checked and honestly priced. No surprises. No pressure. You choose the car. We bring it to your home." |

Delivery note: the last two sentences are said with full energy, a beat of silence before "You choose the car".
End card (last second): Monsoor Motors, 530 Albany Highway Victoria Park, 0434 137 393, MV Dealer Licence MD32748.

## Previs files (folder `previs/`)
- `CEO-Intro-Previs.mp4`: the full 32 s video rendered in 3D in Blender (EEVEE) with shot notes and script on screen. Stays on this Mac; videos are not in git.
- `CEO-Intro-Storyboard.png`: eight key moments.
- `CEO-Intro-Floorplan.png`: top view with people, cars and both camera paths.
- `CEO-Intro-Previs.blend`: the Blender scene. `previs_scene.py` builds and renders it; `previs_post.py` adds labels and makes the storyboard and floor plan.
- To re-render: `blender -b -P previs_scene.py -- <frames_dir> <file.blend>` then `python previs_post.py <frames_dir> .`

## Characters (Higgsfield project Monsoor Motors)
- Arfan: element `Arfan-CEO-Master` (full-body sheet v2 + face sheet v3).
- Monsoor: element `MA-Monsor-Owner-v2` (three-panel full-body sheet, approved 20 Nov 2026).
- Car: element `Monsoor-CHR-Hybrid-Black` (real photo of the black Toyota C-HR Hybrid; photos in `Cars/Toyota C-HR Hybrid (black)/`).

## Voices
- **LOCKED voice tracks (21 Nov 2026):** Arfan `voice/Arfan-script-voice-LOCKED.wav` (version 10, 23.4 s, locked by Arfan 21 Nov 2026; Higgsfield audio `c09e823d-80e7-4ebf-b918-a9fa83384302`); Monsoor `voice/Monsoor-script-voice-1.wav` (8.7 s, approved by Arfan).
- Arfan: his own voice, cloned from a recording of `voice/Arfan-voice-sample-lines.md` (Higgsfield voice `Arfan-CEO-1`, id `6a63aee1-ec53-4b65-acab-0e1fc67b9637`, created 21 Nov 2026). Take 2: voice `Arfan-CEO-2`, id `714d186a-286b-4858-b9ff-a231abf164f2`.
- Monsoor: his own voice, cloned with `seed_audio` from `voice/monsor-voice-ref.wav` (Higgsfield audio upload `86bea944-a814-4dca-b916-693ca824b333`), the same reference the Mercedes ML300 review reel used.

## Workflow from here (realism workflow, skill section 9)
Done: script and voices locked; blocking approved; characters, car and location locked as named elements and filed in the Higgsfield project Monsoor Motors.
1. **Test the pair (one still, about 2.75 credits):** Arfan, Monsoor and the C-HR on the auction yard, framed as the start of shot 1. If faces or light look wrong, fix the asset, not the prompt.
2. **Keyframe stills:** start frame of shot 1 (wide two-shot) and of shot 2 (tighter two-shot), matching the previs.
3. **Draft first:** each shot as a 480p draft (Seedance 2.5 draft mode, or Cinema Studio 4.0 for AI direction) with the start frame, the named elements and the locked voice as audio reference. Prompt = order of actions, how each man feels, and what the car is (right-hand drive, parked, engine off).
4. Two or three drafts per shot; pick the best; finalise only that one at 1080p.
5. Edit: cut on movement, captions, logo watermark, end card. Label as AI-generated. Check plates blank.
6. Publish.

## Rules that apply
- "Hand-picked, properly checked and honestly priced" and "we bring it to your home" must describe what the business really does. If home delivery has limits (area, fee), say so on screen or in the caption.
- The C-HR must be a real stock car shown as it is, plates blurred. If none is in stock, label it as an illustration.
- Label the video as AI-generated where the platforms ask.

## Cost (real quotes from Higgsfield, 21 Nov 2026)

**Prices** (9:16, with references; Seedance 2.5 and Cinema Studio 4.0 cost the same): 480p draft 3 credits a second, 720p 7, 1080p 16. Finalising a draft is charged again at the final resolution. The video is 32 s: shot 1 is 9 s, shot 2 is 23 s.

| Step (tutorial method) | Shot 1 (9 s) | Shot 2 (23 s) | Both |
|---|---|---|---|
| 480p draft | 27 | 69 | 96 |
| Final at 720p | 63 | 161 | 224 |
| Final at 1080p | 144 | 368 | 512 |

| Budget | What it covers | Credits |
|---|---|---|
| Floor | No drafts, straight to 720p, both shots right first time | 224 |
| **Minimal (recommended)** | One draft of each shot, then finalise both at 720p; upscale to 1080p on this Mac for free | **320** |
| Low, with one redo | As minimal, plus one extra draft of each shot | 416 |
| 1080p from Higgsfield | One draft of each shot, finalise at 1080p | 608 |

- Each failed 720p take costs 63 or 161; each failed draft costs 27 or 69. That is why drafts come first.
- Every second cut from the video saves 10 credits on the minimal path.
- First spend: the shot 1 draft, 27 credits. It tests the characters, the car, the location, the lip sync and the voice reference in one go.
- Stills are not needed on this path (the tutorial attaches the assets straight to the video model). A test still is 2.75 credits if wanted.

**Spent so far this session (from the Higgsfield transaction list): 183.39 credits.** Voice clones 120 (three at 40 each), voice lines 32.9, images 30.25, Soul 2.0 tests 0.24. Balance 2,783.61.
Correction: full voice takes with the long delivery cue cost 4.1 to 6.1 credits each, not the "about 2.1" quoted earlier. Each new recording in the Higgsfield recorder makes a voice clone and costs 40 credits.
