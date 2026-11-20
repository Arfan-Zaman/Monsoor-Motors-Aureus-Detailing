# Status

Claude updates this file after every step and pushes it to GitHub. Newest entry at the top.

---

## 21 Nov 2026: Arfan (CEO) full-body sheet and reference elements

**What I did**
- Saved Arfan's sheet v3 as the Higgsfield character element `Arfan-CEO`.
- Found real product photos (black linen shirt, coffee gurkha trousers, black Chelsea boot, Seiko SRPD55) and saved each as a reference element.
- Made the full-body sheet at 2K with sculpted studio lighting using those elements: 2.75 credits of the 10 allowed.

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/Arfan-CEO-Full-Body-Sheet-v1.png`
- `.claude/skills/aureus-video-studio/assets/prompts/arfan-ceo-full-body-sheet.md`, `ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to approve. Optional second run (2.75 credits) to make the face fuller and the expression calmer, closer to his photos.

---

## 21 Nov 2026: Arfan (CEO) character sheet v3 (eyes and lighting fixed)

**What I did**
- Arfan said the eyes and eyebrows looked fake. Made v3 with natural eyes and brows and a real studio lighting setup (2.75 credits). Profiles and both hands are now correct too.

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/Arfan-CEO-Character-Sheet-v3.png`
- `.claude/skills/aureus-video-studio/assets/prompts/arfan-ceo-character-sheet.md`, `ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to approve v3. Then save it as a Higgsfield reference element for future videos.

---

## 21 Nov 2026: Arfan (CEO) character sheet made

**What I did**
- Made 2 character sheets at 2K on a grey background with GPT Image 2.6, using all 14 of Arfan's photos (5.5 credits). Both look like him.
- Saved the prompt for reuse and recorded the job IDs.

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/Arfan-CEO-Character-Sheet-v2a.png`, `-v2b.png`
- `.claude/skills/aureus-video-studio/assets/prompts/arfan-ceo-character-sheet.md`, `ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to pick v2a or v2b. Optional: one more run to fix the small faults (profile or three-quarter direction, left hand), then save the winner as a Higgsfield reference element.

---

## 21 Nov 2026: Arfan (CEO) character sheet, first try

**What I did**
- Uploaded Arfan's 14 reference photos (10 face angles, 4 hand shots) to Higgsfield and saved copies in the Brand Kit.
- Made 2 sheets with Soul 2.0 (under 1 credit). Both rejected: no panels, no grey background, face changed in one.

**Files changed**
- `Brand Kit/Characters/Arfan-CEO/source/` (14 photos)
- `.claude/skills/aureus-video-studio/assets/ASSET-REGISTER.md`, `GENERATION-LOG.md`
- `.claude/STATUS.md`

**What's next**
- Arfan to choose: GPT Image 2.6 with all 14 photos (about 5.5 credits for 2 versions at 2K), or train a Soul ID first.

---

## 20 Nov 2026: rule merged into main

**What I did**
- Merged the latest `main` from GitHub into this branch (no conflicts), then pushed it to `main`. Every session now gets the push + status rule.

**Files changed**
- `.claude/STATUS.md` (this entry). `CLAUDE.md` and `Tools/autosave.sh` are now on `main`.

**What's next**
- Nothing pending for this task. The next session that works here adds its own entry above this one.

---

## 20 Nov 2026: push + status rule set up

**What I did**
- Added the rule "after every step, push to GitHub and update this file" to `CLAUDE.md`, so every future session follows it.
- Fixed auto-save: on new worktree branches it ran a plain `git push`, which failed without telling anyone because the branch had no upstream. It now runs `git push -u origin HEAD` the first time.
- Created this status file.

**Files changed**
- `CLAUDE.md` (Git rules section)
- `Tools/autosave.sh` (push step)
- `.claude/STATUS.md` (new)

**What's next**
- Merge this branch (`claude/github-push-status-workflow-15710a`) into `main` so all sessions pick up the rule. Local `main` is also 8 commits behind `origin/main`.
