# Monsoor Motors: "Meet our new CEO" intro video (plan, version 2: two shots)

Status: 3D blocking done in Blender, 21 Nov 2026. No Higgsfield video generated yet, no credits spent on this video.

## The video
- Format: 9:16 vertical, 1080x1920, 27 seconds, two shots. Reels, TikTok, Facebook.
- Aim: announce Arfan as CEO and promise a properly run Japanese hybrid import process.
- Place: the Monsoor Motors yard, 530 Albany Highway, Victoria Park. A Toyota C-HR sits side-on behind both men, the MONSOOR MOTORS sign above.
- Both men are in frame in both shots (a two-shot throughout).

## Shot list

| Shot | Time | Camera | Action | Words |
|---|---|---|---|---|
| 1 | 0 to 11 s | 35 mm, eye level (1.5 m), wide two-shot, slow push-in from 4.2 m to 3.5 m | Monsoor and Arfan side by side, turned slightly toward each other. At 4.5 s Monsoor presents Arfan with an open hand. At 9 s Arfan turns to the lens and starts to step forward. Cut on the step | Monsoor: "I'm Monsoor, founder of Monsoor Motors. Meet Arfan, our new CEO." |
| 2 | 11 to 27 s | 50 mm, starts 1 m to the right, small arc left and push-in to a medium shot | Arfan walks 1.4 m forward into the frame; Monsoor eases back half a step and watches him. Open hands on the promise (16 to 20 s). Points back to the C-HR (23 to 26 s). End card over the last 2 s | Arfan: "Thanks, Monsoor. I'm Arfan. My job: every Japanese hybrid we import is chosen, checked and delivered the right way. Come and see for yourself." |

End card: Monsoor logo, 530 Albany Highway Victoria Park, 0434 137 393, MD32748.

## Previs files (folder `previs/`)
- `CEO-Intro-Previs.mp4`: the full 27 s video rendered in 3D in Blender with shot notes and script on screen (stays on this Mac, videos are not in git).
- `CEO-Intro-Storyboard.png`: six key moments.
- `CEO-Intro-Floorplan.png`: top view with people, car and both camera paths.
- `CEO-Intro-Previs.blend`: the Blender scene. `previs_scene.py` builds and renders it; `previs_post.py` adds the labels and makes the storyboard and floor plan.
- To re-render: `blender -b -P previs_scene.py -- <frames_dir> <file.blend>` then `python previs_post.py <frames_dir> .`

## Workflow from here
1. You approve the blocking and script (or ask for changes; a re-render is free).
2. You provide: founder's photos and written OK, real C-HR photos, a 30 s voice sample from each of you.
3. Build references: founder character sheet and element, C-HR element, yard background.
4. Keyframe stills: start frame of each shot, matched to the previs framing. You approve before any video.
5. Generate the two video shots from the stills, following the previs moves.
6. Voice and sound: both real voices cloned from your samples, yard room tone, quiet music.
7. Edit: captions, logo watermark, end card.
8. Legal check: AI label, plates blurred, claims honest, car unchanged.
9. Publish.

## Rules that apply
- Founder's likeness needs his own photos and his written OK first.
- The C-HR must be a real stock car shown as it is (colour, condition, features), plates blurred. If no C-HR is in stock, it must be labelled as an illustration.
- "Chosen, checked and delivered the right way" must describe what the business really does.
- Label the video as AI-generated where the platforms ask.
- Existing assets: element `Arfan-CEO-Master`, face sheet v3, full-body sheet v2, outfit elements (see asset register).

## Cost
Blender previs: free. Higgsfield part not priced yet; fewer shots than version 1, so a rough guess is 50 to 90 credits. Exact prices will be checked before each paid step.
