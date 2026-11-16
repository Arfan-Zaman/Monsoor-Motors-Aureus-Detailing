---
videomd: 1
part: remake
tokens: 5838
---

## Remake plan

**2 AI video shots + 6 3D render shots → 4 generation units, 4 Seedance 2.0 calls; live action 5 shots → 1 scene, 2 camera setups; code render / screen capture 7 shots → 1 code project (3 parts)**

- Grouping: AI shots in the same scene joined by hard cuts are generated in one call; ≤15s per call; consecutive hard cuts inside a unit preferably ≤8s, at most 10s; split at dissolves / fades and scene changes
- Audio: the model can generate action sound effects and ambience along with the picture
- Packaging: the styled text, text label on the generated shots is post-production packaging: keep it out of the prompts, erase it from reference frames, and lay it back on from the packaging timeline after generation
- The prompts below are written generically; before generating with Seedance 2.0, rewrite them the way it expects (timing and shots, how references are addressed, dialogue, exclusions): `rea-video models seedance-2.0`

A video model can take these inputs; each generation unit below lists which ones to feed and where they come from:
- **Text prompt**: always; describes the picture, action and camera
- **First frame**: locks the composition and subject of frame one. Without it this is plain text-to-video and framing changes every time
- **Last frame**: also locks the final frame so the model only fills in between. Suits a single shot with a camera move or action
- **Reference images**: how the product and people look, so they stay the same across shots (`@图片1` in the prompt)
- **Reference video**: copy the action, camera move and rhythm, not the picture (`@视频1`); not every model takes one

### Generation units

One generation per unit. The table lists what to feed the model; open a unit for where each input comes from and the prompt.

| Unit | Shots | Time | Duration | Mode | Feed | Continuity |
|---|---|---|---|---|---|---|
| G1 | #4 | 4.5–5.8s | 1.4s | single shot | first frame + reference image + reference video | — |
| G2 | #6–#10 | 7.3–15.3s | 8.0s | multi-shot | first frame + reference image + reference video | — |
| G3 | #12 | 16.7–18.1s | 1.4s | single shot | first frame + reference image + reference video | — |
| G4 | #19 | 26.7–28.3s | 1.6s | single shot | first frame + reference image + reference video | — |

**G1 · shots #4 · 1.4s · multi-reference generation**

| Input | Needed | From | Why |
|---|---|---|---|
| text prompt | yes | see the prompt below | describes picture, action and camera; every other input only constrains it |
| first frame | worth it | source frame `shots/shot_004_first.jpg` (to change product, person or style, redraw it with an image model from the first-frame prompt below); this model takes frame inputs or references, not both: pass it as one more reference image and write “@图片2 as the first frame” in the prompt (Jimeng's omni-reference accepts this; most APIs do not, drop it if refused) | locks composition, shot size and subject position; with text alone every generation frames it differently |
| last frame | no | — | this unit uses references to keep the product and people; the model takes no last frame alongside them |
| reference image | yes | `@图片1` character reference images (one frontal face + one half-body per character) so the look stays consistent across shots | the first frame only fixes frame one; reference images keep the product and people consistent after it |
| reference video | worth it | `@视频1` source clip 4.5–5.8s | follow the action, camera move and cutting rhythm; reference only, the picture is not copied |

- Generate 4s and trim to 1.4s (very short shots are unstable when generated on their own)
- Shots #4 have no prompt

```text
Vertical 9:16; night / low-light ambient, no dedicated fill, soft light (almost no lit / shadow edge), warm (about 3000–4000K), background slightly soft. Characters follow @图片1. Follow the action, camera movement and cutting rhythm of @视频1.
(prompt missing: run --vlm or have the agent write one from the frames)
```

**G2 · shots #6–#10 · 8.0s · multi-reference generation**

| Input | Needed | From | Why |
|---|---|---|---|
| text prompt | yes | see the prompt below | describes picture, action and camera; every other input only constrains it |
| first frame | worth it | source frame `shots/shot_006_first.jpg` (to change product, person or style, redraw it with an image model from the first-frame prompt below); this model takes frame inputs or references, not both: pass it as one more reference image and write “@图片2 as the first frame” in the prompt (Jimeng's omni-reference accepts this; most APIs do not, drop it if refused) | locks composition, shot size and subject position; with text alone every generation frames it differently |
| last frame | no | — | several shots in one call; a last frame would only constrain the final shot |
| reference image | yes | `@图片1` character reference images (one frontal face + one half-body per character) so the look stays consistent across shots | the first frame only fixes frame one; reference images keep the product and people consistent after it |
| reference video | worth it | `@视频1` source clip 7.3–15.3s | follow the action, camera move and cutting rhythm; reference only, the picture is not copied |

- Alternative: a 3D project. Have an LLM write a Blender script or a Three.js scene; model the characters / props once and render each shot from its own camera. Best for multiple angles and character consistency, and changing copy or shots is just a code change
- Shots #6–#10 have no prompt

```text
Vertical 9:16; night / low-light ambient, no dedicated fill, soft light (almost no lit / shadow edge), warm (about 3000–4000K), background slightly soft. Characters follow @图片1. Follow the action, camera movement and cutting rhythm of @视频1. Hard cuts between shots.
Shot 1 (0.0–2.2s): (prompt missing: run --vlm or have the agent write one from the frames)
Shot 2 (2.2–3.6s): (prompt missing: run --vlm or have the agent write one from the frames)
Shot 3 (3.6–5.1s): (prompt missing: run --vlm or have the agent write one from the frames)
Shot 4 (5.1–6.6s): (prompt missing: run --vlm or have the agent write one from the frames)
Shot 5 (6.6–8.0s): (prompt missing: run --vlm or have the agent write one from the frames)
```

**G3 · shots #12 · 1.4s · multi-reference generation**

| Input | Needed | From | Why |
|---|---|---|---|
| text prompt | yes | see the prompt below | describes picture, action and camera; every other input only constrains it |
| first frame | worth it | source frame `shots/shot_012_first.jpg` (to change product, person or style, redraw it with an image model from the first-frame prompt below); this model takes frame inputs or references, not both: pass it as one more reference image and write “@图片2 as the first frame” in the prompt (Jimeng's omni-reference accepts this; most APIs do not, drop it if refused) | locks composition, shot size and subject position; with text alone every generation frames it differently |
| last frame | no | — | this unit uses references to keep the product and people; the model takes no last frame alongside them |
| reference image | yes | `@图片1` character reference images (one frontal face + one half-body per character) so the look stays consistent across shots | the first frame only fixes frame one; reference images keep the product and people consistent after it |
| reference video | worth it | `@视频1` source clip 16.7–18.1s | follow the action, camera move and cutting rhythm; reference only, the picture is not copied |

- Generate 4s and trim to 1.4s (very short shots are unstable when generated on their own)
- Alternative: a 3D project. Have an LLM write a Blender script or a Three.js scene; model the characters / props once and render each shot from its own camera. Best for multiple angles and character consistency, and changing copy or shots is just a code change
- Shots #12 have no prompt

```text
Vertical 9:16; night / low-light ambient, no dedicated fill, soft light (almost no lit / shadow edge), warm (about 3000–4000K), background slightly soft. Characters follow @图片1. Follow the action, camera movement and cutting rhythm of @视频1.
(prompt missing: run --vlm or have the agent write one from the frames)
```

**G4 · shots #19 · 1.6s · multi-reference generation**

| Input | Needed | From | Why |
|---|---|---|---|
| text prompt | yes | see the prompt below | describes picture, action and camera; every other input only constrains it |
| first frame | worth it | source frame `shots/shot_019_first.jpg` (to change product, person or style, redraw it with an image model from the first-frame prompt below); this model takes frame inputs or references, not both: pass it as one more reference image and write “@图片2 as the first frame” in the prompt (Jimeng's omni-reference accepts this; most APIs do not, drop it if refused) | locks composition, shot size and subject position; with text alone every generation frames it differently |
| last frame | no | — | this unit uses references to keep the product and people; the model takes no last frame alongside them |
| reference image | yes | `@图片1` character reference images (one frontal face + one half-body per character) so the look stays consistent across shots | the first frame only fixes frame one; reference images keep the product and people consistent after it |
| reference video | worth it | `@视频1` source clip 26.7–28.3s | follow the action, camera move and cutting rhythm; reference only, the picture is not copied |

- Generate 4s and trim to 1.6s (very short shots are unstable when generated on their own)
- Alternative: a 3D project. Have an LLM write a Blender script or a Three.js scene; model the characters / props once and render each shot from its own camera. Best for multiple angles and character consistency, and changing copy or shots is just a code change
- Shots #19 have no prompt

```text
Vertical 9:16; night / low-light ambient, no dedicated fill, soft light (almost no lit / shadow edge), warm (about 3000–4000K), background slightly soft. Characters follow @图片1. Follow the action, camera movement and cutting rhythm of @视频1.
(prompt missing: run --vlm or have the agent write one from the frames)
```

### Shooting scenes

Shoot every shot of one scene before moving to the next; within a scene, shoot the wider sizes first and the close-ups last so the lighting is set only once. Leave about 1s of handle at both ends of every take.

**S1**: shots #2, #3, #5, #11, #13 (7.2s on screen)
- Lighting: night / low-light ambient, no dedicated fill, key light frontal, neutral (about 5000K)
- Setup medium shot · moving camera (gimbal / handheld pan) · push-in: shots #13, 1.47s on screen, shoot about 3.5s
- Setup medium close-up · moving camera (gimbal / handheld pan) · pan / track/push-in: shots #2, #3, #5, #11, 5.73s on screen, shoot about 13.7s

### Code composition

One Remotion / HTML project rebuilt from the text tracks and layout (text and UI are 100% controllable; changing copy is a data change). An LLM can write this project directly.

- Part 1: shots #1 (0.0–1.6s)
- Part 2: shots #14–#18 (19.6–26.7s)
- Part 3: shots #20 (28.3–30.1s)

Remake assets (all in the report folder; hand them over together with the data below to whoever writes the code, or to an LLM):
- `shots/shot_XXX_first.jpg` / `_last.jpg`: first / last frame of each shot at full size, for layout, type size and margins
- `shots/shot_XXX_strip.jpg`: key frames about every 0.5 s, to follow the animation
- `shots/shot_XXX_elements.jpg` and `_el_NN.jpg` / `_st_NN.jpg` / `_ly_NN.jpg`: full-size crop of every element once settled, numbered as in the motion timeline; redraw shapes from them, cut out icons, logos and illustrations that cannot be redrawn
- `packaging/overlays.ass`, `packaging/timeline.json`: timing, position and colour of the text

How to build the pictures (by the measured picture type):
- particles / point cloud: Three.js particle system (points sampled on the target shape, morph between shapes, bloom), rendered frame by frame with @remotion/three
- UI / document: HTML / CSS cards and layout matched to the frame (radius, shadow, type sizes), elements enter with spring(); a real UI can be screen-recorded

Particle shots: what shape the particles form in each shot and how it moves decides whether the remake works; chapter cards, labels and counters go in an HTML layer on top. Build shot by shot from the table below, not one shared background.

| Shot | Time | Build | Picture | Camera | Colours | On-screen text |
|---|---|---|---|---|---|---|
| #1 | 0.0–1.6s | particles / point cloud | (to fill from the images: what the elements form and how they move) | push in 2%/s, picture drifts left, rotates | ground #090a0c · #18191a #272727 #373737 #5a5553 · drawn #4d4948 #8e7469 #c1a894 #e7e8e5 | ACERAMIC / PRO / ÀGACERAMIC / AGACERAMIC |
| #14 | 19.6–21.0s | particles / point cloud | (to fill from the images: what the elements form and how they move) | static frame, elements move inside it | ground #1f1f1f · #101010 #303030 #494846 #676864 · drawn #6d6964 #b3b4ac #eeeeed #090706 | — |
| #15 | 21.0–22.4s | particles / point cloud | (to fill from the images: what the elements form and how they move) | picture drifts up | ground #1f1f1f · #0f0f0f #343434 #4f4b48 #b8b9b5 · drawn #645b55 #a5a4a0 #e1e1df #050504 | — |
| #16 | 22.4–23.9s | particles / point cloud | (to fill from the images: what the elements form and how they move) | pull out 2%/s, picture drifts right, rotates | ground #050608 · #0e0f10 #272929 #404443 #5f6360 · drawn #838983 #4e4f4e #b9bcb5 #eff2ef | — |
| #17 | 23.9–25.3s | particles / point cloud | (to fill from the images: what the elements form and how they move) | push in 1%/s, picture drifts up | ground #0c0d0f · #222222 #3a3b3b #555555 #747778 · drawn #070607 #d9dad8 #7a5d48 #979798 | — |
| #18 | 25.3–26.7s | particles / point cloud | (to fill from the images: what the elements form and how they move) | pull out 2%/s, picture drifts down, rotates | ground #090a0c · #19191b #2a2b2c #3e3e3e #565656 · drawn #767574 #464646 #aeadab #ececea | — |
| #20 | 28.3–30.1s | UI / document | (to fill from the images: what the elements form and how they move) | pull out 3%/s, picture drifts down, rotates | ground #121514 · #1d1f1e #040807 #3a3b39 #555853 · drawn #656660 #f3f5f5 #babab6 #e90c22 | CERAMIC / PRO |

**Picture scenes** (a new scene whenever what is drawn moves or changes shape as a whole inside a shot. `frames/` holds first / middle / last full-size frames per scene, `scene_XX_layer.png` the drawn layer of the middle frame (background and text removed, alpha by how strongly it stands out), `frames/points/scene_XX.json` samples of that layer, one `x y r g b a` per row with x, y in 0–1. Place particles, trace lines or redraw shapes from these instead of guessing from a description. `track` in `frames/scenes.json` follows the layer's centre and spread over time)

| Scene | Shot | Time | Ground | Background glow | Drawn colours | Pieces | Area (x0 y0 x1 y1) |
|---|---|---|---|---|---|---|---|
| scene_01 | #1 | 0.0–1.6s | #1b1c1b | #767973, centre (0.73, 0.08), radius 0.16 | #55504d #a88c79 #e3e3de | 772 | 0.01 0.01 0.99 0.95 |
| scene_02 | #14 | 19.6–21.0s | #232323 | #62635d, centre (0.53, 0.23), radius 0.47 | #d2d4cd #7c7d77 #241f1a | 873 | 0.03 0.03 0.99 0.96 |
| scene_03 | #15 | 21.0–22.4s | #232322 | #656562, centre (0.49, 0.20), radius 0.43 | #d8d8d4 #878683 #322922 | 977 | 0.03 0.01 0.97 0.96 |
| scene_04 | #16 | 22.4–23.9s | #0e0e0d | #888880, centre (0.78, 0.14), radius 0.25 | #989d95 #e7eae5 #555755 | 383 | 0.14 0.01 0.98 0.95 |
| scene_05 | #17 | 23.9–25.3s | #2a2926 | #8e908d, centre (0.54, 0.07), radius 0.30 | #d2d4d1 #837266 #0a0809 | 919 | 0.01 0.01 0.97 0.97 |
| scene_06 | #18 | 25.3–26.7s | #151515 | #726b65, centre (0.49, 0.08), radius 0.31 | #555555 #9b9b98 #eaeae7 | 681 | 0.02 0.01 0.98 0.92 |
| scene_07 | #20 | 28.3–30.1s | #161616 | #6a5b5b, centre (0.55, 0.42), radius 0.27 | #5d524f #7a7c71 #d3d8d0 | 38 | 0.05 0.00 0.97 0.59 |

When built, score it with `rea-video compare original remake --scenes frames/scenes.json -o dir` (each side's drawn layer is taken against its own ground, so a new ground colour still compares) and fix the lowest-scoring scenes first, from `compare_worst.jpg`.

Per-shot motion timeline (measured: positions in % of frame width / height, colours sampled once the element settles; read together with the key-frame strip)

**Motion #1 0.0–1.6s · 4 events**

- Ground #090a0c; other main colours #18191a #272727 #373737 #5a5553; drawn layer #4d4948 #8e7469 #c1a894 #e7e8e5
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- [crop L1](shots/shot_001_ly_01.jpg) [crop L2](shots/shot_001_ly_02.jpg) · Continuous layer: 60% of the frame moves through the whole shot (x 0%–100%, y 0%–100%), e.g. drifting gradients, particle flow, breathing glow
1. 0.07–0.13s · top (x 0%–100%, y 0%–52%) · changes, unfolds rightward (draw-on / grow / wipe), instant · #212020 · text “ÀGACERAMIC / AGACERAMIC / PRO” · [crop](shots/shot_001_el_01.jpg)
2. 0.07–0.13s · bottom (x 0%–89%, y 59%–100%) · changes, unfolds downward (draw-on / grow / wipe), instant · #080809 · [crop](shots/shot_001_el_02.jpg)
3. 0.40–1.53s · top right (x 47%–100%, y 0%–41%) · changes, moves upward, ease-in-out · #413d3e · text “ACERAMIC / PRO / ÀGACERAMIC” · [crop](shots/shot_001_el_03.jpg)
4. 0.53–1.53s · top (x 0%–67%, y 10%–50%) · changes, moves upward, ease-in · #3d3531 · text “ÀGACERAMIC / PRO” · [crop](shots/shot_001_el_04.jpg)

**Motion #14 19.6–21.0s · 0 events**

- Ground #1f1f1f; other main colours #101010 #303030 #494846 #676864; drawn layer #6d6964 #b3b4ac #eeeeed #090706
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- [crop L1](shots/shot_014_ly_01.jpg) [crop L2](shots/shot_014_ly_02.jpg) · Continuous layer: 64% of the frame moves through the whole shot (x 0%–100%, y 0%–100%), e.g. drifting gradients, particle flow, breathing glow

**Motion #15 21.0–22.4s · 0 events**

- Ground #1f1f1f; other main colours #0f0f0f #343434 #4f4b48 #b8b9b5; drawn layer #645b55 #a5a4a0 #e1e1df #050504
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- [crop L1](shots/shot_015_ly_01.jpg) [crop L2](shots/shot_015_ly_02.jpg) · Continuous layer: 61% of the frame moves through the whole shot (x 0%–100%, y 0%–100%), e.g. drifting gradients, particle flow, breathing glow

**Motion #16 22.4–23.9s · 5 events**

- Ground #050608; other main colours #0e0f10 #272929 #404443 #5f6360; drawn layer #838983 #4e4f4e #b9bcb5 #eff2ef
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- [crop L1](shots/shot_016_ly_01.jpg) [crop L2](shots/shot_016_ly_02.jpg) · Continuous layer: 49% of the frame moves through the whole shot (x 0%–100%, y 0%–100%), e.g. drifting gradients, particle flow, breathing glow
1. 22.50–22.70s · middle right (x 69%–71%, y 48%–59%) · disappears, moves downward, linear · #4d4d4d · [crop](shots/shot_016_el_01.jpg)
2. 22.50–22.57s · bottom right (x 78%–80%, y 70%–81%) · disappears, instant · #3c3c3c · [crop](shots/shot_016_el_02.jpg)
3. 22.90–23.70s · middle (x 49%–56%, y 45%–60%) · appears, slides leftward, linear · #494949 · [crop](shots/shot_016_el_03.jpg)
4. 23.57–23.77s · top (x 40%–44%, y 15%–25%) · appears, scales up, ease-in · #3f3f3f · [crop](shots/shot_016_el_04.jpg)
5. 23.63–23.77s · bottom right (x 69%–84%, y 70%–82%) · appears, scales up, instant · #3a3a3a · [crop](shots/shot_016_el_05.jpg)

**Motion #17 23.9–25.3s · 0 events**

- Ground #0c0d0f; other main colours #222222 #3a3b3b #555555 #747778; drawn layer #070607 #d9dad8 #7a5d48 #979798
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- [crop L1](shots/shot_017_ly_01.jpg) [crop L2](shots/shot_017_ly_02.jpg) · Continuous layer: 54% of the frame moves through the whole shot (x 0%–100%, y 0%–100%), e.g. drifting gradients, particle flow, breathing glow

**Motion #18 25.3–26.7s · 1 events**

- Ground #090a0c; other main colours #19191b #2a2b2c #3e3e3e #565656; drawn layer #767574 #464646 #aeadab #ececea
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- [crop L1](shots/shot_018_ly_01.jpg) [crop L2](shots/shot_018_ly_02.jpg) · Continuous layer: 61% of the frame moves through the whole shot (x 0%–100%, y 0%–100%), e.g. drifting gradients, particle flow, breathing glow
1. 25.37–26.23s · bottom (x 18%–56%, y 94%–100%) · disappears, moves rightward, ease-in-out · #303030 · [crop](shots/shot_018_el_01.jpg)

**Motion #20 28.3–30.1s · 2 events**

- Ground #121514; other main colours #1d1f1e #040807 #3a3b39 #555853; drawn layer #656660 #f3f5f5 #babab6 #e90c22
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: shape / text block · x 44%–49%, y 36%–37% · #4a504a · [crop](shots/shot_020_st_01.jpg)
- S2. never moves: shape / text block · x 51%–76%, y 36%–42% · #4f524f · text “CERAMIC” · [crop](shots/shot_020_st_02.jpg)
- S3. never moves: shape / text block · x 24%–55%, y 40%–51% · #3d3f3f · [crop](shots/shot_020_st_03.jpg)
- S4. never moves: shape / text block · x 76%–100%, y 48%–57% · #363a38 · [crop](shots/shot_020_st_04.jpg)
- [crop L1](shots/shot_020_ly_01.jpg) [crop L2](shots/shot_020_ly_02.jpg) · Continuous layer: 20% of the frame moves through the whole shot (x 0%–100%, y 0%–71%), e.g. drifting gradients, particle flow, breathing glow
1. 29.47–30.07s · top (x 24%–53%, y 0%–8%) · appears, slides leftward, linear · #545550 · [crop](shots/shot_020_el_01.jpg)
2. 29.67–30.07s · middle right (x 47%–100%, y 28%–46%) · changes, moves leftward, ease-in-out · #50524f · text “CERAMIC” · [crop](shots/shot_020_el_02.jpg)

### Real material in the picture (the original files are needed)

5 shots, 7.2s (24%) contain real material (screen recordings, screenshots, photos, embedded video); a model cannot stand in for them:

- **live footage (own footage or a film / drama clip, confirm by looking)** (whole frame): shots #2, #3, #5, #11, #13, 7.2s in all
