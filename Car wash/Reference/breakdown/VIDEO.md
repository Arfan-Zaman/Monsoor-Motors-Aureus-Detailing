---
videomd: 1
name: video-by-aga-service-baku-drvn7u-jc1x
description: 'Made with (inferred): code / template render 35%, 3D render 32%, live action 24%, AI-generated video 9%'
source:
  file: Video by aga_service_baku [DRVN7u-jc1x].mp4
  sha256: 3df750e6fe6f7a38395ec214228ff6fae4c16f16b5858c0e214998d6cbc7ad23
  duration: 30.133
  size: 1080x1920
  fps: 30.0
  aspect: '9:16'
shots: 20
lang: en
made_mix:
  code_render: 0.3506
  cg_3d: 0.3175
  live_action: 0.2389
  ai_video: 0.0929
confidence: 0.463
readers:
- tools
open_questions: 23
generator:
  name: rea-video
  version: 0.1.0
---

# Video by aga_service_baku [DRVN7u-jc1x].mp4

**Verdict** (inferred): Mixed production: code / template render 35% + 3D render 32% + live action 24% + AI-generated video 9%; overlays: styled text, text labels, static graphics, subtitles (composited in code / an editor); real material used: live footage (own footage or a film / drama clip, confirm by looking) (7.2s); audio: music 166.7BPM (to confirm, leaning stock library music); packaging: styled text ×4, text labels ×11
**Made with** (inferred, by duration): code / template render 35%, 3D render 32%, live action 24%, AI-generated video 9%
**Remake**: 2 AI video shots + 6 3D render shots → 4 generation units, 4 Seedance 2.0 calls; live action 5 shots → 1 scene, 2 camera setups; code render / screen capture 7 shots → 1 code project (3 parts)
**Real material to collect**: 5 shots (24% of the duration), list in `video/remake.md`

## Open questions

- The VLM did not run (No VLM; live action / AI / 3D are told apart from pixel statistics only, so confidence is limited. An agent that can see images: run rea-vi…
- Shot #1 (0.0–1.6s): code / template render at only 50% confidence, runner-up cg_3d
- Shot #2 (1.6–3.0s): live action at only 55% confidence, runner-up ai_video
- Shot #3 (3.0–4.5s): live action at only 51% confidence, runner-up ai_video
- Shot #4 (4.5–5.8s): AI or live action, to confirm: no 24fps-source duplicate frames and no AIGC / generator label, so the AI call rests on a clean picture with …
- Shot #5 (5.8–7.3s): live action at only 46% confidence, runner-up ai_video
- Shot #6 (7.3–9.5s): 3D render at only 31% confidence, runner-up ai_video
- Shot #7 (9.5–10.9s): 3D render at only 31% confidence, runner-up ai_video
- 15 more, see the `flag` lines in `video/timeline.md`

## Map

Read this page first; for detail, open only the file you need. Each line is `path | ~tokens | what is in it · when to read it`; paths are relative to this directory.

```videomd-map
video/timeline.md | 1211 | Timeline: one line per shot · what a stretch says, which shots need review, how a shot was made
video/content.md | 87 | Content and structure · what it says, the narrative line, structure, the script
video/cast.md | 53 | Cast, scenes and props · reference images for characters, first-frame prompts
video/sound.md | 439 | Sound · voice, music, sound effects, beats and sources
video/look.md | 645 | Camera, lighting and editing · for filmed shots: framing, camera, lighting, kit
video/packaging.md | 773 | Packaging · subtitles, styled text, stickers, picture-in-picture: timing and style
video/remake.md | 5850 | Remake plan · generation units, shoots, code builds, real material to collect, acting and emotion
video/shots/*.md | 442 | Per-shot detail, tokens per file on average · checking one shot: what is seen, the inference and its basis, prompts, frames
breakdown.json | 68988 | Full raw data · for programs; a model rarely needs it
shots/ | - | contact sheet, first and last frame of each shot · checking by eye
storyboard.jpg | - | storyboard of the whole video · the whole video at a glance
stems/ | - | voice, music and effects stems · listening, remaking the sound
packaging/ | - | subtitle files, packaging timeline, sticker frames · remaking subtitles and packaging
frames/ | - | picture scenes: full-size frames, the drawn layer cut out and sampled, measurements · remaking rendered pictures
audio.png | - | waveform and beat chart · seeing the rhythm
```

## How to read

- One shot per line: `#<n> start-end (s) | key value | …`. A key ending in `~` is the tools' inference; keys without it are visible on screen or measured directly.
- `story` job in the story and the point · `seen` what is on screen · `act` acting (emotion, strength, face) · `camera` camera move · `overlay` overlays · `made~` how it was made (inferred) · `material~` where the material came from (inferred) · `remake` remake route · `flag` needs a second look
- Full detail for a shot is in `video/shots/<n>.md` (e.g. `video/shots/07.md`).
- What is “seen” can be checked against the frames; what is “inferred” is the tools' and image readers' judgement, with the basis in each shot file. When they disagree, trust the frames.
