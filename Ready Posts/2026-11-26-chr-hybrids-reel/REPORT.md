# Monsoor Motors C-HR hybrids Reel: delivery report

26 Nov 2026. Source: `monsoor_reel_delivery_pack (1).zip`. The work was delivery only: no re-cut, no remix, no palette or type changes, no generated footage, no added audio.

## Summary

| File | Status |
|---|---|
| `monsoor_reels_9x16.mp4` | **Ready.** The approved reference master, remuxed for faststart. The streams are bit-identical (SHA-256 per stream matches). |
| `monsoor_feed_4x5.mp4` | **Ready.** Crop y 285–1635 of the verified caption-free build, with captions re-burned for feed (margin-v 12 %, max-width 90 %) using a local Montserrat burner. The audio is the master's track, stream-copied. |
| `monsoor_cover.jpg` | **Ready.** The approved reference cover, 1080×1920, unchanged. |
| `captions.srt` | **Ready.** 26 cues from `words_fixed.json`, grouped to match the burned cues (verified frame by frame). |
| `checks/` | 9:16 check frames (`check_*.jpg`) at 3.05, 3.12, 3.19, 4.52, 9.12, 11.70, 12.74 s, plus `cut_strips.jpg` (11 frames across each cut). 4:5 check frames (`feed_*.jpg`) at the same times plus 1.0, 15.3 and 17.0 s. |

**Could not verify:** the original caption stage. `compose_with_sweeps.sh` calls `/home/.hermes/skills/video-repurposer/scripts/caption_burn.py`, which is not in the pack, and the ffmpeg here (9.0.2, Homebrew) has no libass or drawtext. So the 9:16 caption pass could not be reproduced. The 9:16 deliverable is therefore the approved reference, and the 4:5 captions were burned with a replacement tool (see below). This is a deliberate, reported substitution, approved by the owner ("finish it", 26 Nov 2026).

## 4:5 feed cut: how it was built

1. **Source:** `mixed_swept.mp4`, my reproduction of compose steps 1–3 (grade, sweeps in gbrp, graphics, end card, mix), with no captions. Verified against the reference in Task 1.
2. **Timing:** re-timed to 30 fps CFR by timestamp (`fps=30:start_time=0:round=near`), the same way the original caption pass re-timed the master. The end-card join sits on the same frame as the master. Picture vs master (crop y 285–1105, above all captions): **every one of the 545 frames ≥ 39.0 dB PSNR**, average 40.8 dB.
3. **Crop:** 1080×1350 from y 285. Not squashed, not letterboxed.
4. **Captions:** `Tools/burn_captions.py` with the 26 cues from `captions.srt`. Montserrat Bold 60 px (the same glyph height as the master's captions, about 70 px including the outline), Warm White #FAF8F5, Deep Navy #08182D outline 5 px, centred, margin-v 12 %, max-width 90 %. Text box on every cue: y 1119–1189, x 204–874. No cue needed a line wrap.
5. **Audio:** taken from `monsoor_reels_9x16.mp4` by stream copy. **SHA-256 identical to the master** (10e7afd6…), so the mix is untouched.

Difference from the 9:16 master: the feed captions are Montserrat with a visible navy outline, which matches hard rule 3. The master's captions are a generic sans with a thin outline. If the owner wants both cuts to look the same, the 9:16 can be re-burned with the same tool (the build is verified, so only the caption pass would change).

## Task 1: reproduce

Ran `build_sweeps.py --clips plate_a_black.mp4,plate_b_black.mp4 --out sweeps.mov`, then steps 1–3 of `compose_with_sweeps.sh` (grade → screen sweep in gbrp → graphics → end card → mix). Step 4 (captions) could not run. The comparison is my `mixed_swept.mp4` (no captions) against `reference/monsoor_reel_swept.mp4`:

- **Picture: matches.** The reference carries one extra leading frame (545 frames, video starting at 0.000 s). My render has 543 frames starting at 0.021 s. This fits the caption pass re-timing to CFR. Aligned by that one frame, every frame scores ≥ 35 dB PSNR above the caption band (average 41 dB), which is encoder noise. Before alignment the average was 28 dB, and that offset is the only difference.
- **Audio: matches.** Best alignment is at 0 samples. The null-test residual is −28 to −35 dB, evenly spread across all 18 seconds. That points to an extra AAC generation, not a mix difference.
- **Captions:** isolated as the difference between the reference and the caption-free render. There are 26 cues, all inside y 1159–1228 and x 140–940.

Because steps 1–3 reproduce and the caption stage can't, I did **not** ship my own render. The 9:16 deliverable is the approved reference itself.

## Task 3: verification

### monsoor_reels_9x16.mp4
```
codec_name=h264 profile=High width=1080 height=1920 pix_fmt=yuv420p field_order=progressive r_frame_rate=30/1 avg_frame_rate=30/1
codec_name=aac profile=LC sample_rate=48000 channels=2
duration=18.200000 size=8532317 (after remux: atoms ftyp, moov, free, mdat)
loudnorm: Integrated -14.9 LUFS · True Peak -2.8 dBTP · LRA 8.6 LU
```
### monsoor_feed_4x5.mp4
```
codec_name=h264 profile=High width=1080 height=1350 pix_fmt=yuv420p field_order=progressive r_frame_rate=30/1 nb_frames=545
codec_name=aac profile=LC sample_rate=48000 channels=2   (stream-copied: SHA-256 identical to the master)
duration=18.200000 size=15645928 (atoms ftyp, moov, free, mdat)
loudnorm: Integrated -14.9 LUFS · True Peak -2.8 dBTP · LRA 8.6 LU
```
4:5 checks: all 545 frames are 1/30 s; idet 544 progressive, 1 undetermined; blackdetect found nothing; captions are overlaid after the sweeps, so they're never clipped by the light pass (`checks/feed_3.12.jpg`, `feed_9.12.jpg`, `feed_12.74.jpg`). Feed layout: graphics cards start at y ≈ 58, captions end 161 px above the bottom edge.

| Check | Result |
|---|---|
| 30 fps fixed, progressive | Pass. All 545 frames are 1/30 s. idet: 544 progressive, 1 undetermined. |
| H.264, stereo AAC 48 kHz | Pass |
| Faststart | **Failed on the approved master** (`moov` after `mdat`). **Fixed by a lossless remux** (`-c copy -movflags +faststart`). Stream hashes are identical before and after. |
| Loudness ~ −15 LUFS, TP < −1.0 dBTP | Pass: −14.9 LUFS, −2.8 dBTP |
| No black frame at the cuts | Pass. `blackdetect` and `blackframe` found nothing anywhere in the file. |
| No flash frame at the cuts | Pass. Mean luma rises 6–10 levels (of 255) for the 8-frame sweep and eases back, with no single-frame spike. |
| No hard-edged rectangle at the cuts | Pass at the cut frames. Note: at 9.30 s (0.18 s after the 9.12 cut) the "MONSOOR MOTORS / 530 Albany Hwy" card shows as an empty navy panel for about 4 frames before its text types on. That's the card's own build-on, not the transition. |
| Text inside the safe band (y 269–1248, 65 px sides) | Pass for all **text**: graphics type y 431–828, x 92–964; captions y 1159–1228, x 140–940; end card text y ≈ 550–1150. The navy card **panels** reach x 60 and x 1020, 5 px into each side margin. That's the panel edge only, no text. |
| Captions readable at every transition, not clipped by the light pass | Pass. Captions are burned after the sweep, so they sit on top. Checked at all five cuts (`checks/cut_strips.jpg`). |
| Duration ~18.2 s, story untouched | Pass: 18.20 s |

### captions.srt
Grouping rule: up to 3 words and 22 characters per cue, break at a sentence end (. ! ?), and never end a cue on a weak word (a, of, and, in, the…). Cue time runs from the first word's start to the last word's end. All 26 cue boundaries match the change points detected in the burned captions to within one frame.

## Things for the owner to see (not changed: outside a delivery brief)

1. **Licence number on the banner.** The pull-up banner filmed behind him reads **"MV Dealership Licence : MD322748"**. The licence on file is **MD32748**, and the end card correctly says MD32748. If the banner is wrong, it needs reprinting. This is real footage, so I didn't touch it.
2. **Caption typeface.** The approved 9:16 master's captions are not Montserrat (the script asks for "Liberation Sans", and they render as a generic sans). That conflicts with hard rule 3 ("Typeface Montserrat"). The navy outline is also very thin. The 4:5 cut uses Montserrat.
3. **Caption text "Albany High."** That's what he says. Fine as a transcript, but the address is Albany **Highway**.
4. The cover's MONSOOR MOTORS lockup sits over the banner's own logo and bullet text. It's legible, but busy.

## Where the files are

The mp4s are kept out of git by design. Copies are in the main folder: `Ready Posts/2026-11-26-chr-hybrids-reel/` (`monsoor_reels_9x16.mp4`, `monsoor_feed_4x5.mp4`). Everything else in this folder is in git.
