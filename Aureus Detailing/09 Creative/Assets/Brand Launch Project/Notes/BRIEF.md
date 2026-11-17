# Aureus Detailing: brand launch reels (brief, 17 Nov 2026)

Three 9:16 reels (1080×1920, 30 fps, -14 LUFS like the references). Each one borrows the **setup** of a reference reel in `../Brand Launch Reel References/`: shot types, framing, cut rhythm, grade, type style and sound. The footage, words and branding are our own. No reference footage, audio or script lines are used.

**Cost: 0 Higgsfield credits, everything free and local.** Footage: a **new real shoot** of the trainer (`SHOT-LIST.md`). No earlier Higgsfield reel footage is used. Voice: Qwen3-TTS VoiceDesign + clone (`make_voice.py`). Music: Stable Audio 3 (`make_music.py`). Edit: `make_reels.py` + `reelkit.py`. A stand-in animatic of all three reels is in `Animatic/` (main Monsoor Motors folder).

## Character, voice, brand
- **The master detailer** (see `08 Social Media/Character Board/PERSONA.md`): few words, the glare, the bell "ding", one reluctant grin at the end.
- **Voice:** a 60-year-old man, deep, warm and slightly gravelly, slow and dry, with a light Australian accent (mostly neutral English, soft Aussie vowels, not broad). One designed voice is used for every line. On camera, the new voice is laid over his existing lip movement for the same words.
- **Brand:** chrome A logo, navy #071A33, aqua #00A8A8 (replaces the reference's red accent), Montserrat; end card with logo, 0434 137 393, @aureusdetailing.com.au. Price on screen ($199 Gold Detail) must match the booking page.
- Label as AI-generated when posting.

---

## Reel 1: "Perth. Are you ready?" (teaser, about 20 s) · setup from Ref 1
**Setup:** hard black-and-white grade, crushed blacks, bright highlights. Huge condensed caps (Anton), stacked and centred: city name in the accent colour, the rest in white. Fast cuts with bursts of 4–6 micro-cuts (0.13–0.2 s) between 1.5–2 s holds. The logo appears in the world (on the van). Black end card: logo plus contact line.
**Sound:** dark trap-style beat about 117 BPM, heavy 808. Stop-start pattern: 2 s full drop, then a 2 s filtered, quiet gap where the text slams land, then back in. Bell "ding" before the end card. Music tails off to near silence on the end card. One voice line only.

| Time | Shot (source) | Text / sound |
|---|---|---|
| 0.0–1.6 | Van with logo, slow (van) | music in, filtered |
| 1.6–2.1 | micro-cuts: beads, foam, spray | **PERTH** (aqua) |
| 2.1–4.2 | Machine polish close (p1) | **PERTH / ARE YOU / READY?** drop hits |
| 4.2–5.7 | Water beads macro (L7) | gap |
| 5.7–6.5 | micro-cuts: wheel, steam, foam, polish | drop |
| 6.5–8.4 | Car hero (reveal) | **MOBILE / DETAILING** |
| 8.4–10.0 | Snow foam (LA) | |
| 10.0–10.7 | micro-cuts | |
| 10.7–12.5 | Backlit pressure wash (L6) | **WE COME / TO YOU** |
| 12.5–14.3 | He walks in with the trolley (L8) | |
| 14.3–16.6 | He taps the bell (bell) | "ding". VO: "Perth. You ready?" |
| 16.6–20.0 | Black end card | logo, NOW BOOKING · 0434 137 393 · handle |

## Reel 2: "Not all detailing is the same" (talking, about 26 s) · setup from Refs 2 and 3
**Setup:** natural warm daylight, he talks to camera, cutaways to car details. Word-by-word captions near the middle of the frame: small white Montserrat with **one emphasis word per line in an italic serif** (Instrument Serif Italic), as in Ref 2. Alternate a gentle punch-in (100% / 112%) on talking cuts, and add **one big italic brand slam "AUREUS DETAILING"** when he names the business, as in Ref 3. Cuts every 1.5–3 s.
**Sound:** voice leads. A soft minimal bed (felt piano, warm pad, light drums, about 94 BPM) sits around -20 dB under the voice, quiet whooshes on the cuts, and close-mic detailing sounds under the cutaways.

| Time | Shot | Voice (new voice) |
|---|---|---|
| 0.0–1.3 | He points at camera (speaking-raw, on camera) | "We come to you." |
| 1.3–3.3 | Swirls in the sun (hook) | "Most places rush it." |
| 3.3–5.3 | Backlit spray (w2) | "Shiny today. Swirls tomorrow." |
| 5.3–6.6 | He glares, cloth in hand (p2) | "Not here." |
| 6.6–8.6 | Walks in with trolley (L8) + **AUREUS DETAILING** slam | "At Aureus, it's foam first," |
| 8.6–10.4 | Snow foam (LA) | "machine polish," |
| 10.4–12.2 | Polisher on the bonnet (L1) | "then wax, by hand." |
| 12.2–14.4 | Wheel brush close (wheel) | "Every spoke." |
| 14.4–15.8 | Kneeling at the wheel (L5) | "By hand." |
| 15.8–18.3 | Steam on the leather (LC) | "Steam for the leather." |
| 18.3–19.8 | Bell (bell) | "ding" |
| 19.8–22.2 | On camera (speak3) | "Done properly, or it's not done." |
| 22.2–26.0 | Car hero (reveal) + glass end card | "Gold Detail. One ninety-nine. We come to you." |

## Reel 3: "The shine" (cinematic, about 13 s) · setup from Ref 4
**Setup:** no talking, no captions on the footage. Low angles, wide lens, backlit sun and spray. Teal shadows and warm highlights, a little contrast and fine grain. Structure: a **2 s flash-cut opener** (0.13 s cuts with overexposed flash frames), then **0.5 s beat cuts** for 2 s, then **about 1.2 s holds** cut on the beat. Small logo only in the last 1.5 s.
**Sound:** music first (moody cinematic hip-hop, about 100 BPM, deep drums, warm synth), starting on frame 1 at full level. Close-mic spray and foam sounds tucked under the music. No voice.

| Time | Shots |
|---|---|
| 0.0–2.0 | flash cuts: backlit spray, foam, wheel, polish, beads, van |
| 2.0–4.0 | beat cuts: kneel at wheel, foam car, spray, wipe bonnet |
| 4.0–11.5 | holds: car low-angle reveal, spray backlit, beads macro, door wipe, polisher, wheel |
| 11.5–13.0 | car hero + small chrome A and handle |

---

## Music prompts (Stable Audio 3, local, instrumental)
1. "Dark aggressive trap instrumental, 117 BPM, heavy 808 bass, punchy kick and snare, tense dark synth stabs, hype product launch teaser, no vocals"
2. "Calm minimal ambient instrumental bed, 94 BPM, soft felt piano, warm pads, light brushed drums, understated premium, no vocals"
3. "Cinematic moody hip hop instrumental, 100 BPM, deep boom bap drums, warm analog synth, sub bass, luxury car montage, no vocals"

Each reel is also exported **without music**, so a trending track can be added in the app when posting (playbook rule).

## Voice prompt (Qwen3-TTS VoiceDesign, local)
"A 60-year-old man. Deep, warm, slightly gravelly older male voice. Slow, calm, dry and confident, a man of few words. Light Australian accent: mostly neutral English with soft Australian vowels, not a broad accent."
