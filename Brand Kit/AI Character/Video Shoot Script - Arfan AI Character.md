# iPhone video shoot script: AI character of Arfan

**Purpose:** short iPhone clips of Arfan's face, body, movement and voice. Claude then pulls the sharpest frames to train a Higgsfield **Soul ID**, uses the clips as motion and lip-sync references, and clones the voice from the audio.
**Time needed:** about 25 minutes with a helper. 6 clips, about 3 minutes of footage in total.

---

## iPhone settings (set these once before you start)

Settings → Camera:
- **Formats → Most Compatible** (gives H.264 files, which are easy to edit).
- **Record Video → 4K at 30 fps.**
- **Enhanced Stabilisation: on.** **Lock Camera: on** (stops the lens switching in the middle of a clip).
- **Preserve Settings → Exposure Adjustment: on.**

In the Camera app:
- **Video** mode. Not Cinematic, not Portrait. Cinematic blurs the edges of your face and the AI learns that blur.
- **Back camera**, held **upright (9:16)**. Not the selfie camera, which stretches the face.
- Lens **2x** (the white "2" or "3" button). Helper stands about 1.5–2 m away with the phone at your eye level.
- Before each clip, **hold a finger on your face** until "AE/AF LOCK" appears. This locks focus and exposure.
- No filters, no beauty mode, no Live Photo.
- Wipe the lens. Phone in **Do Not Disturb**, so no buzzing or notifications.
- If you have a tripod or phone stand, use it for clips 1–3.

## You
- Hair and beard as you normally wear them.
- 3 plain tops: navy (brand colour), white, and one grey or black. No big logos, no busy patterns.
- No hat, no sunglasses. Glasses only if you wear them every day, and then in every clip.
- No make-up you don't normally wear.

## Rules for every clip
- Start recording, wait **2 seconds**, then act. Hold still **2 seconds** at the end before stopping.
- Move **slowly**: about half your normal speed when turning your head. Fast moves give blurry frames.
- Blink normally. Don't stare.
- If you mess up, keep going. Bad takes cost nothing; we just pick the good frames.

---

## Clip 1: the head turn (40 s)
**Where:** indoors, side-on to a window, plain wall behind. Inside lights off. **Navy top.**
**Framing:** head and shoulders, face in the middle of the screen. Phone on a stand if you have one.

Action, slowly:
1. Look straight at the lens, neutral face. Hold **3 s**.
2. Turn your head slowly to the **left** until you are side-on. Hold **2 s**.
3. Turn slowly back through the middle to the **right**, side-on. Hold **2 s**.
4. Back to the middle. Tilt your chin **up** a little, hold **2 s**, then **down** a little with your eyes on the lens, hold **2 s**.
5. Back to the middle. Smile naturally, teeth showing. Hold **3 s**.
6. Turn 45° left with the smile, hold **2 s**; 45° right, hold **2 s**.

## Clip 2: talking to camera (45 s)
**Same spot, same top.** This is the most important clip for lip-sync and voice.
Room must be **quiet**: no TV, fan or air con. Phone no more than 1.5 m away (or use AirPods as a mic).

Look at the lens and say this at your normal speed, like you're talking to a customer:

> "G'day, I'm Arfan from Monsoor Motors and Aureus Detailing, on Albany Highway in Victoria Park.
> We sell quality used cars, and our detailers make them look brand new.
> Whether you're buying, selling, or you just want your car looking its best, come and see us, or give us a call on 0434 137 393.
> We'd love to help."

Then, without stopping the recording, say one line each in these moods:
- Excited: "This one just came in, and it's spotless."
- Serious: "Every car gets a full inspection before it goes on the lot."
- Laughing / relaxed: whatever you like for 5 seconds.

## Clip 3: expressions (25 s)
**Same spot. Change to the white top.** Head and shoulders, front.
Hold each for **3 s**, with a relaxed neutral face in between:
neutral → small smile → big laugh (helper tells you a bad joke) → thinking (look slightly away) → confident (slight nod) → eyes back to the lens.

## Clip 4: outdoor walk (30 s)
**Outdoors in open shade** (shade of a building or tree, no direct sun on your face). **White top.**
Helper stands still. You walk slowly **toward the camera** from about 6 m away, look up at the lens for the last 2 m and stop at waist-up framing. Smile, hold **3 s**.
Then turn and stand **side-on**, full body in frame, hold **3 s**. Turn to face the camera, full body, arms relaxed, hold **3 s**.

## Clip 5: at the yard (40 s)
**530 Albany Highway. Grey or black top.** Direct sun is fine here; different light is the point.
1. Waist up, lean on a car at 45°, look at the lens and smile. Hold **4 s**.
2. Walk along the side of the car, run your hand along the paint, look back at the camera.
3. Open the driver's door, sit in, window down, look at the lens and say: "Come and see us." Hold **3 s**.

**No number plates in frame.** If one gets in, tell Claude and it will be blurred.

## Clip 6: room tone (15 s)
Same quiet room as Clip 2. Point the phone at the wall and record **15 s of silence**. Nobody talks. This is used to clean up the voice.

---

## After the shoot
- Watch each clip once. Re-shoot only if your face is **out of focus** or **in shadow** for most of it.
- **AirDrop** the clips to the Mac. On the iPhone, choose **Options → All Photos Data** so they arrive at full quality.
- Name them `arfan-clip1-headturn.mov`, `arfan-clip2-talking.mov`, `arfan-clip3-expressions.mov`, `arfan-clip4-walk.mov`, `arfan-clip5-yard.mov`, `arfan-clip6-roomtone.mov`.
- Keep them in a **private folder** on the Mac (videos never go into git). Don't post the raw clips.

## Then tell Claude
"Make my AI character from the clips in [folder]."

Claude will:
1. Pull the 12 sharpest, most varied frames (front, both sides, up/down, smiling, waist-up, full body, all 3 light setups).
2. Train a **Soul ID** named `arfan`: **Soul Cinematic** for reels, **Soul 2** for still images.
3. Clone the voice from Clip 2 (cleaned with Clip 6).
4. Record the Soul ID and voice in `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`.

Any AI image or video of Arfan that is posted gets labelled as AI content where Instagram, TikTok or Facebook require it.
