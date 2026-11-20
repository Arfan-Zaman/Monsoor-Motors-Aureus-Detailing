# Monsoor Motors: "Meet our new CEO" intro video (plan, version 3)

Status: 3D blocking v3 rendered in Blender, 21 Nov 2026. No Higgsfield video generated yet, no credits spent on this video.

## The video
- Format: 9:16 vertical, 1080x1920, 32 seconds, two shots. Reels, TikTok, Facebook.
- Aim: announce Arfan as CEO and build trust in the whole business: every kind of car, and Japanese imported hybrids in particular.
- Nobody walks. Arfan stays on his mark and the camera travels to his side.
- Set: showroom glass front with the MONSOOR MOTORS sign, hero Toyota C-HR on a navy plinth behind the two men, stock cars in the bays, feather banners, planters and bollards.

## Shot list and script

| Shot | Time | Camera | Action | Words |
|---|---|---|---|---|
| 1 | 0 to 9 s | 35 mm, eye level (1.5 m), wide two-shot, slow push-in from 3.75 m to 3.15 m | Monsoor and Arfan side by side, sign above, C-HR behind. Monsoor puts a hand on his heart on "trust", then presents Arfan with an open hand. Cut as Arfan turns to the lens | Monsoor: "I built Monsoor Motors on one thing: trust. Now meet the man who will carry it forward. Arfan, our new CEO." |
| 2 | 9 to 32 s | 50 mm. Starts as a tighter two-shot, trucks right to Arfan's side (12 to 17 s), creeps in, then pushes in and drops a little below eye level for the last line | Arfan squares up to the lens and follows the camera with his body. Monsoor leaves frame as the camera travels. Arfan sweeps a hand to the cars, palms down on "no surprises", points at the lens on "YOU", opens both arms on "WE" | Arfan: "Thank you for the opportunity. Hello, this is Arfan. Buying a car is a big decision. So here is my promise. Every car on this yard, from family runabouts to Japanese imported hybrids, is hand-picked, properly checked and honestly priced. No surprises. No pressure. You choose the car. We bring it to your home." |

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
- **Approved voice tracks (21 Nov 2026):** Arfan `voice/Arfan-script-voice-3.wav` (23.0 s, approved by Arfan); Monsoor `voice/Monsoor-script-voice-1.wav` (8.7 s, not yet approved).
- Arfan: his own voice, cloned from a recording of `voice/Arfan-voice-sample-lines.md` (Higgsfield voice `Arfan-CEO-1`, id `6a63aee1-ec53-4b65-acab-0e1fc67b9637`, created 21 Nov 2026). Take 2: voice `Arfan-CEO-2`, id `714d186a-286b-4858-b9ff-a231abf164f2`.
- Monsoor: his own voice, cloned with `seed_audio` from `voice/monsor-voice-ref.wav` (Higgsfield audio upload `86bea944-a814-4dca-b916-693ca824b333`), the same reference the Mercedes ML300 review reel used.

## Workflow from here
1. You approve the blocking and script (changes are a free re-render).
2. You provide: real C-HR photos, a 30 s voice sample from each of you, and confirmation that Monsoor agrees to appear.
3. Build the C-HR element and the yard background.
4. Keyframe stills: start frame of each shot, matched to the previs framing. You approve before any video.
5. Generate the two video shots from the stills, following the previs moves.
6. Voice and sound: both real voices cloned from your samples, yard room tone, quiet music.
7. Edit: captions, logo watermark, end card.
8. Legal check: AI label, plates blurred, claims honest, car unchanged.
9. Publish.

## Rules that apply
- "Hand-picked, properly checked and honestly priced" and "we bring it to your home" must describe what the business really does. If home delivery has limits (area, fee), say so on screen or in the caption.
- The C-HR must be a real stock car shown as it is, plates blurred. If none is in stock, label it as an illustration.
- Label the video as AI-generated where the platforms ask.

## Cost
Blender previs: free. Higgsfield part not priced yet; rough guess 50 to 90 credits. Exact prices will be checked before each paid step.
