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
