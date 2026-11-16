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
- Before redoing anything, check the playbook and `git log` to see whether it was already made, so work isn't repeated.

## How we work (saves time and tokens)
- Reuse scripts in `Tools/` instead of rewriting them. New reusable script → add it to `Tools/` and list it in playbook section 5.
- Word documents: build on the templates in `Brand Kit/05 Documents/`. Export PDFs with `Tools/docx_to_pdf.sh` (uses Microsoft Word, so the Montserrat font renders correctly; LibreOffice does not).
- Python: run scripts with `/opt/miniconda3/bin/python -I`. Use non-editable pip installs (editable installs break on this Mac).
- Finished files go in the right folder above, never only in a temp folder.
