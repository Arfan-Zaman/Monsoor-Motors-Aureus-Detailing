# Generation log

One line per Higgsfield generation. Reuse the prompt, seed and references of keepers.

| Date | Project | Model | Prompt file | Seed | References used | Credits | Result link | Keep? Why |
|---|---|---|---|---|---|---|---|---|
| 2026-11-16 | Website keyframes | nano_banana_pro (16:9 asked, came out 3:4) | storyboard/STORYBOARD-4-KEYFRAMES.md | - | logo | ~2 each | jobs 0fba1bd9, 96c1c208, 884d899b, e3e03e2f | Keep (typos noted) |
| 2026-11-17 | Website film clip A | seedance_2_5 omni_reference draft 8s 3:4 | storyboard/clips/A.txt | - | start kf1, end kf2 | 24 | job be6dd9a2 | Keep: lens dive works |
| 2026-11-17 | Website film clip B | seedance_2_5 omni_reference draft 8s 3:4 | storyboard/clips/B.txt | - | start kf2, end kf3 | 24 | job 666d6ffe | Keep: layers reveal works |
| 2026-11-17 | Website film clip C | seedance_2_5 omni_reference draft 8s 3:4 | storyboard/clips/C.txt | - | start kf3, end kf4 | 24 | job 3e34d09e | Keep: bead + confirm works |
| 2026-11-17 | Scroll film opening frame | nano_banana_pro 16:9 2k (ref kf1) | storyboard/SCROLL-FILM-PROMPTS.md | - | kf1 | 2 | job 59d2e9df | Keep after cropping the frame border (storyboard/film-start-clean.png) |
| 2026-11-17 | Website scroll film 15 s | kling3_0_turbo 1080p 16:9 | storyboard/SCROLL-FILM-PROMPTS.md | - | start film-start-clean.png | 30 | job 0aa8060e | Keep: one continuous push car → bonnet → polish glow → bead → crystal lattice. Encoded to assets/film/ (scroll-scrub settings) |
| 2026-11-17 | Ferrari hero still 4K | nano_banana_pro 16:9 4k | (prompt in chat) | - | - | ~4 | job 9f0d0c2f | Keep: navy Ferrari Roma, fogged studio, aqua light lines (storyboard/ferrari/hero.png) |
| 2026-11-17 | Ferrari start frame (silk cover) | nano_banana_pro 4k | - | - | ref 9f0d0c2f | ~4 | job 872c8104 | Keep (storyboard/ferrari/start.png) |
| 2026-11-17 | Ferrari end frame (rear wheel, beads) | nano_banana_pro 4k | - | - | ref 9f0d0c2f | ~4 | job 704672a3 | Keep (storyboard/ferrari/end.png) |
| 2026-11-17 | Website hero film, Ferrari 15 s | kling4_0 image-to-video 1080p 16:9 | (prompt in chat) | - | start 872c8104, end 704672a3 | 48.75 | job ac84e277 | Keep: silk reveal → orbit → rear wheel; encoded to assets/film/ (replaces the SUV film, kept in storyboard/suv-film-old/) |
| 2026-11-17 | Character board v1 (master detailer) | nano_banana_pro 16:9 4k | Character Board/BOARD-PROMPT.md | - | 5 face refs + logo | ~4 | job bfc4292f | Keep: likeness and uniform approved for review |
| 2026-11-17 | Reel 1 S1: van arrives beside dusty maroon M3 | nano_banana_pro 9:16 2k | Launch Reels/REEL-1-PLAN.md | - | board + logo refs | 2 | job 9ca97542 | Keep (stills/s1-arrival.png). First image of the Aureus van |
| 2026-11-17 | Reel 1 S2: detailer on driveway (speaking start frame) | nano_banana_pro 9:16 2k | Launch Reels/REEL-1-PLAN.md | - | board + 5 face refs + logo | 2 | job ae5f3c17 | Keep (stills/s2-speaking.png) |
| 2026-11-17 | Reel 1 S3: machine polish on bonnet | nano_banana_pro 9:16 2k | Launch Reels/REEL-1-PLAN.md | - | board ref | 2 | job ca420b47 | Keep (stills/s3-polish.png) |
| 2026-11-17 | Reel 1 S4: interior steam clean | nano_banana_pro 9:16 2k | Launch Reels/REEL-1-PLAN.md | - | board ref | 2 | job (first try) | Reject: white car, partial face (stills/s4-interior.png) |
| 2026-11-17 | Reel 1 S4 redo: interior steam clean | nano_banana_pro 9:16 2k | Launch Reels/REEL-1-PLAN.md | - | board ref | 2 | job 2d43f273 | Keep: maroon, right-hand drive, M3 sill, no face (stills/s4-interior-v2.png) |
| 2026-11-17 | Reel 1 S5: wheel deep clean | nano_banana_pro 9:16 2k | Launch Reels/REEL-1-PLAN.md | - | board ref | 2 | job ce71830e | Keep (stills/s5-wheel.png) |
| 2026-11-17 | Reel 1 S6: finished M3 + van (end card) | nano_banana_pro 9:16 2k | Launch Reels/REEL-1-PLAN.md | - | S1 ref | 2 | job ddd4cc29 | Keep (stills/s6-finish.png) |
| 2026-11-17 | Reel 1 speaking clip 6 s, native voice | veo3_1 high 9:16 1080p, audio on | Launch Reels/REEL-1-PLAN.md | - | start S2 (ae5f3c17) | 24 | job 13fc3607 | Keep: first take. Words checked by transcript, exact: "We come to you. Gold detail: polish, wax sealant, interior steam clean, leather care. One ninety-nine." (speaking-raw.mp4) |

**Reel 1 total: 38 credits** (cap was 45). Edit, captions and sound were done locally with `Launch Reels/reel-1/make_reel.py` (0 credits).

| 2026-11-17 | Ad still: swirl-mark macro (hook) | nano_banana_pro 9:16 2k | Launch Reels/CINEMATIC-AD-PLAN.md + ad/make_ad.py | - | ref S1 9ca97542 | 2 | job a00d9da5 | Keep (stills/hook-still.png) |
| 2026-11-17 | Ad still: finished M3, mirror bonnet (reveal) | nano_banana_pro 9:16 2k | Launch Reels/CINEMATIC-AD-PLAN.md + ad/make_ad.py | - | ref S6 ddd4cc29 | 2 | job 45703c8c | Keep (stills/reveal-still.png) |
| 2026-11-17 | Ad still: flawless paint macro with water beads | nano_banana_pro 9:16 2k | Launch Reels/CINEMATIC-AD-PLAN.md + ad/make_ad.py | - | refs a00d9da5 + 45703c8c | 2 | job 67ab5db0 | Keep: mirrors the hook framing, now like new (stills/macro-still.png) |
| 2026-11-17 | Ad shot: van arrives 5 s | kling4_0 i2v 1080p 9:16 | Launch Reels/CINEMATIC-AD-PLAN.md + ad/make_ad.py | - | start S1 | 16.25 | job 8a5b959e | Keep (first submit failed with an API error, not charged) |
| 2026-11-17 | Ad shot: polisher pass 5 s | kling4_0 i2v 1080p 9:16 | Launch Reels/CINEMATIC-AD-PLAN.md + ad/make_ad.py | - | start S3 | 16.25 | job 179ab4c7 | Keep |
| 2026-11-17 | Ad shot: interior steam 5 s | kling4_0 i2v 1080p 9:16 | Launch Reels/CINEMATIC-AD-PLAN.md + ad/make_ad.py | - | start S4 v2 | 16.25 | job 13708277 | Keep |
| 2026-11-17 | Ad shot: wheel brush 5 s | kling4_0 i2v 1080p 9:16 | Launch Reels/CINEMATIC-AD-PLAN.md + ad/make_ad.py | - | start S5 | 16.25 | job 2b8f0b0d | Keep |
| 2026-11-17 | Ad shot: swirl macro 5 s | kling4_0 i2v 1080p 9:16 | Launch Reels/CINEMATIC-AD-PLAN.md + ad/make_ad.py | - | start a00d9da5 | 16.25 | job dee031de | Keep |
| 2026-11-17 | Ad shot: wide reveal arc 5 s | kling4_0 i2v 1080p 9:16 | Launch Reels/CINEMATIC-AD-PLAN.md + ad/make_ad.py | - | start 45703c8c | 16.25 | job 796de9ec | Keep |
| 2026-11-17 | Ad shot: flawless paint macro 5 s | kling4_0 i2v 1080p 9:16 | Launch Reels/CINEMATIC-AD-PLAN.md + ad/make_ad.py | - | start 67ab5db0 | 16.25 | job e8921fc1 | Keep (added at owner's request) |
| 2026-11-17 | Ad voice: 7 lines in the detailer's voice | seed_audio, cloned from the Veo clip's audio (audio/his-voice-ref.wav) | Launch Reels/CINEMATIC-AD-PLAN.md + ad/make_ad.py | - | audio ref | 2.8 | job 4183165c, ef14f908, 027b2366, 845d7973, 7d9344d1, d11901a1, 24b70358 | Keep: words checked by transcript. This voice is AI-made (from the Veo clip), not the real trainer's voice |
| 2026-11-17 | Ad music: 32 s instrumental, 100 bpm | elevenlabs_music_v2_5 | Launch Reels/CINEMATIC-AD-PLAN.md + ad/make_ad.py | - | - | 4.36 | job 4ffeabd7 | Keep: original track, safe for paid ads (audio/music.mp3) |

**Cinematic ad total: 126.7 credits** (balance 905.75 → 779.04). Edit, animated graphics, sound mix and cover done locally with `Launch Reels/ad/make_ad.py` (0 credits).

| 2026-11-17 | Ad v2 stills: detailer in every service (p1 polisher, p2 wax by hand, i1 steam, i2 vents, w1 wheel brush, w2 pressure rinse, hero) | nano_banana_pro 9:16 2k | ad/AD-V2-DIRECTOR-BRIEF.md | - | character board + trainer-01 + scene still | 14 | job dde7f2f7, adb2e145, 7dad9467, c766ae4d, e9c4bd9a, 510fb876, 3698b3b6 | Keep: face consistent; two angles and techniques per service |
| 2026-11-17 | Ad v2 shots, 3 s real speed (p1, p2, i1, i2, w1, w2) | kling4_0 i2v 1080p 9:16 | ad/AD-V2-DIRECTOR-BRIEF.md | - | the stills above | 58.5 | job dedcc32d, eaa83be6, 4cd1cdde, 7aa943b7, 317f2299, 6a6ab861 | Keep |
| 2026-11-17 | Ad v2 hero shot (wipe + smile) | kling4_0 i2v 3 s | ad/AD-V2-DIRECTOR-BRIEF.md | - | 3698b3b6 | 9.75 | job (heroclip.id) | Not used: replaced by the bell shot |
| 2026-11-17 | Casual Aussie speaking take | veo3_1 high 6 s | ad/AD-V2-DIRECTOR-BRIEF.md | - | S2 | 24 | job 109f9b19 | Not used: superseded by the persona take |
| 2026-11-17 | Persona speaking take: 'We come to you. Gold detail, 199. Done properly, or it's not done.' | veo3_1 high 6 s | ad/AD-V2-DIRECTOR-BRIEF.md | - | S2 | 24 | job 54c8fdba | Keep: words checked by transcript |
| 2026-11-17 | Persona voice lines g1-g6 (gruff, few words) | seed_audio cloned voice | ad/AD-V2-DIRECTOR-BRIEF.md | - | his-voice-ref.wav | 2.4 | job f9bb7263, d2740eda, 4784abef, eacc64ee, 0464ac0c, a8dbbe51 | Keep (audio/v3/) |
| 2026-11-17 | Casual voice lines c1-c6 | seed_audio | ad/AD-V2-DIRECTOR-BRIEF.md | - | his-voice-ref.wav | 2.4 | job jobs5.txt | Not used: persona chosen instead |
| 2026-11-17 | Bell still + bell shot (taps chrome service bell) | nano_banana_pro 2k + kling4_0 3 s | ad/AD-V2-DIRECTOR-BRIEF.md | - | character board + hero | 11.75 | job 2b5c33db, 58a0ebb2 | Keep: tap lands at 1.5 s into the shot |

| 2026-11-17 | Ad v3 links L1-L8 (3 s, start image + end image, so each last frame = next first frame) | kling4_0 i2v 1080p 9:16 | ad/make_ad_v3.py | - | v2 keyframe stills | 78 | job ad/jobs9.txt | Keep: the one-take film |
| 2026-11-17 | Ad v3 foam + full-car rinse stills | nano_banana_pro 9:16 2k | ad/make_ad_v3.py | - | character board + trainer-01 + p1 | 4 | job f48f56b7, 3ff45e48 | Keep (owner asked for foaming and rinsing shots) |
| 2026-11-17 | Ad v3 links LA foam>rinse, LB rinse>polish, LC steam>wheel, LD wheel>paint macro | kling4_0 i2v 3 s | ad/make_ad_v3.py | - | stills above | 39 | job d6a977a2, a446d269, 11158ab9, 4f2bd268 | Keep: 30 s cut uses A B 1 2 C D 7 8; 36 s cut uses A B 1-8 |
| 2026-11-17 | ASMR sound per activity (11 x 3 s) + 30 s Perth ambience + foam, rinse | mirelo_text_to_audio | ad/make_ad_v3.py | - | - | about 11 | job ad/jobs7.txt, jobs10.txt | Keep (audio/asmr/). Kling's own audio track was unusable: mostly 'dramatic music' |
| 2026-11-17 | Persona voice lines h1-h5, cloned from the on-camera take so the voice matches | seed_audio | ad/make_ad_v3.py | - | audio/v4/persona-voice-ref.wav | 2 | job ad/jobs8.txt, jobs10.txt | Keep h3 'Yeah. That'll do.' and h5 'Every spoke... by hand.'; h2 replaced (unclear) |

**Ad v4 (17 Nov 2026): 0 credits.** Owner rejected the connected one-take look; v4 is a cut edit from existing shots (`ad/make_ad_v4.py`). Links L1-L7, LC, LD are unused; LA, LB and L8 are used only for their clean opening seconds.

**Ad v5 (17 Nov 2026): about 8 credits**, all voice lines (`seed_audio`, cloned from `ad/audio/v4/persona-voice-ref.wav`): four short lines not used, the seven-part full script recorded twice (first wording was unclear), closing line recorded three times. Picture uses only existing shots (`ad/make_ad_v5.py`). Lesson: check every download decodes fully (`i1.mp4` and `w2.mp4` were truncated) and never submit more than 6 jobs at once.
