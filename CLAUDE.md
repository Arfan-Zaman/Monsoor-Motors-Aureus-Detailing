# Monsoor Motors & Aureus Detailing: project memory

Claude reads this file automatically at the start of every session in this folder.
Keep it short. Detailed facts live in the playbook (below), so Claude doesn't re-learn them each time.

## Read first
- **`Monsoor Motors - Playbook & Daily Log.md`**: business facts, brand rules, owner preferences, finished files, reusable tools, daily log. Treat it as the source of truth and update it at the end of every working session.
- **`Aureus Detailing/README.md`**: Aureus Detailing brand and website notes.
- **`Brand Kit/READ ME FIRST.txt`**: what each Brand Kit folder holds.

## The business (quick reference)
- Company: **Monsoor Motors Pty Ltd**, ABN 31 695 324 193, trading as **Monsoor Motors** (car dealer) and **Aureus Detailing** (detailing, a business name of the same company).
- MV Dealership Licence **MD32748** · 530 Albany Highway, Victoria Park WA 6100 · 0434 137 393 · info@monsoormotors.com.au · monsoormotors.com.au
- Director: Mohammod A Monsor (Sole Director and Owner). CEO – AI, Digital Marketing & Business Development: Md Arfan Uz Zaman (contractor).
- Australian English (licence, colour, organise). Australian law and ATO rules apply.

## Folder map
| Folder | What's in it |
|---|---|
| `Brand Kit/` | Logos, fonts (Montserrat), social templates, print, document templates (`05 Documents/`), brand guide |
| `Aureus Detailing/` | Aureus brand, logo, mockups, website (`07 Website/`) |
| `Facebook/`, `Ready Posts/`, `Customer Images/`, `Cars/` | Social content: finished posts, source photos, car listings |
| `Google Business Profile Audit/` | GBP before/after audit |
| `Car wash/` | Car wash reel project (videos stay local, not in git) |
| `Tools/` | Our reusable scripts (see playbook section 5). Sub-folders that are other people's repos are not in git |
| `HR/` | **Private. Never in git, never shared, never sent to outside services** |

## Git rules (this folder is a private GitHub repo used as memory and history)
- Remote: `Arfan-Zaman/Monsoor-Motors-Aureus-Detailing` (private), branch `main`.
- **Never commit**: `HR/`, videos (`*.mp4`, `*.mov`…), audio stems, files over 100 MB, secrets/passwords/API keys. These are in `.gitignore`; don't force-add them.
- **Auto-save is on:** a Stop hook (`.claude/settings.json` → `Tools/autosave.sh`) commits and pushes every change after each Claude turn. The user never has to say "save". At the end of a working session, still add the Daily Log entry to the playbook (the `save-progress` skill does this and writes a fuller commit message).
- **After every step** (set 20 Nov 2026): push to GitHub (`git push`, or `git push -u origin HEAD` on a new branch) and update `.claude/STATUS.md` with three parts: what I did, which file(s) changed, what's next. Newest entry at the top, dated.
- Before redoing anything, check the playbook and `git log` to see whether it was already made, so work isn't repeated.

## How we work (saves time and tokens)
- Reuse scripts in `Tools/` instead of rewriting them. New reusable script → add it to `Tools/` and list it in playbook section 5.
- Word documents: build on the templates in `Brand Kit/05 Documents/`. Export PDFs with `Tools/docx_to_pdf.sh` (uses Microsoft Word, so the Montserrat font renders correctly; LibreOffice does not).
- Python: run scripts with `/opt/miniconda3/bin/python -I`. Use non-editable pip installs (editable installs break on this Mac).
- Finished files go in the right folder above, never only in a temp folder.

## Video and image generation (Higgsfield)
- Load the **`aureus-video-studio`** skill before any Higgsfield work. It picks the right prompt pack, keeps characters, cars and brand consistent (reference elements, Soul ID), and logs every generation in `.claude/skills/aureus-video-studio/assets/`.
- Installed prompt packs: `higgsfield-prompt-suite`, `hf-*`, `hf-video-*`, `ugc-factory` (sources and licences in `aureus-video-studio/SOURCES.md`).
- Lint every Seedance prompt with `higgsfield-prompt-suite/scripts/seedance_lint.py` before spending credits.

## Video editing — make it look human, not AI (set 18 Nov 2026)

Goal: a viewer should feel a person edited this, not a generator. Apply to Higgsfield/Kling generations, edits in `Launch Reels/ad/make_ad_v6.py` / ffmpeg, and the Launch Reels and Car wash reel projects. Log edits in `aureus-video-studio/assets/GENERATION-LOG.md`.

**This relaxes the 17 Nov rule.** The one-take rule in `aureus-video-studio` §8 ("no grade, no grain, no zooms, no flashes") is superseded: subtle, natural editing is now allowed, no heavy effects. Never retime a shot, never change a real car's colour, condition or features, and never add fake testimonials, fake results or copied music. Blur plates. Label AI content where Instagram, TikTok or Facebook require it.

**AI tells to reject on sight:** too-smooth, floaty motion with no camera breathing or reframing; perfect, unchanging light, waxy paint and plastic-looking skin; hands, tools or badges that morph between cuts; every shot the same length (for example, every shot exactly 3 s) or the same shot repeated; dead silence, or an over-polished voiceover with no room sound.

**Edit like a human**
- Cut on movement — a wipe, a spray, a door closing, a head turn — not in a still pose.
- Vary shot lengths: mix 1–2 s detail shots with 3–5 s hero shots. Never let the rhythm go metronomic.
- Keep it 9:16, 1080×1920, faces and text in the centre safe area (avoid top 250 px and bottom 400 px).
- Subtle handheld feel only: a tiny reframe or slow push-in, never a zoom punch or flash cut.
- Keep small imperfections a real shoot would have — spray mist, a moving shadow, an uneven pan.
- Colour: light, natural work only. Match white balance and exposure between shots. No heavy grade, no grain filter.
- Sound: natural room tone under everything. Real close-mic ASMR for the work; his voice only, cloned from `ad/audio/v4/persona-voice-ref.wav`; music about 13 dB under.
- Pace for reels: hook in the first 2–3 s (the detailer to camera, or the dirtiest before-shot). Offer on screen in the first 3 s for paid ads; 30 s paid, longer cut for organic.

**Brand stays the same:** Aureus navy #071A33, aqua #00A8A8, hot pink #FF4D8D (≤10%), Montserrat, chrome A logo; Monsoor navy #0F2747, orange #FF5F15 accent only. End card: logo, phone 0434 137 393, handle @aureusdetailing.com.au. Frosted-glass labels, warm white text, watermark top left at about 55%.
