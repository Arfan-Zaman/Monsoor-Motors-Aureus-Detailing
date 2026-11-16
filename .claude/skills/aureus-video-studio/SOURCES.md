# Installed Higgsfield skill packs (downloaded 16 Nov 2026)

Skill instructions were copied for all packs. At the owner's request, the OSideMedia suite also includes its helper scripts (`higgsfield-prompt-suite/scripts/`), after a review on 16 Nov 2026: standard-library Python, no network calls, writes only inside its own folder; `refresh_specs.py` calls the official Higgsfield CLI. The full validation passed. Installers (`install.py`, `bin/ugc-factory.js`) and test suites were not copied, because the skills were installed by hand.

Useful commands (run from `.claude/skills/higgsfield-prompt-suite/scripts/`):
- `python3 -E -s seedance_lint.py --model seedance_2_0 "<prompt>"`: checks a prompt before spending credits
- `python3 -E -s preflight.py --model <model> --param k=v`: free platform-limit check
- `python3 -E -s validate.py`: checks the suite itself after an update

| Folder(s) in `.claude/skills/` | Source | Commit | Licence | Notes |
|---|---|---|---|---|
| `higgsfield-prompt-suite/` | github.com/OSideMedia/higgsfield-ai-prompt-skill | 6a6a5dd | MIT | 36 skills (router + `skills/*`), prompt craft for all Higgsfield models |
| `hf-01-…` to `hf-15-…`, `hf-higgsfield-image-auto`, `hf-seedance-auto-generate`, `hf-ugc-video-auto` | github.com/AKCodez/higgsfield-claude-skills | f6698ab | **None stated**: private use only, do not redistribute | `ugc-hot-girl` deliberately not installed (off-brand) |
| `hf-video-01-…` to `hf-video-10-…` | github.com/rediumvex/ai-video-generator-claude | ffdad7d | MIT | 10 video prompt skills |
| `ugc-factory/` | github.com/charlesdove977/UGC-Factory | ee59beb | MIT | Main skill only; its 15 style skills duplicate the AKCodez ones |

**Official Higgsfield skills, installed 16 Nov 2026** with `npx skills add higgsfield-ai/skills` (github.com/higgsfield-ai/skills, MIT, tracked in `skills-lock.json`): higgsfield-brandkit, higgsfield-faceless-video, higgsfield-generate, higgsfield-marketplace-cards, higgsfield-product-photoshoot, higgsfield-soul-id, higgsfield-video-explainer, higgsfield-websites, higgsfield-youtube-thumbnail. Reviewed: their scripts are local media tools; the `curl … install.sh | sh` line only runs if the CLI is missing. Update with `npx skills update -p`.

**Higgsfield CLI** `@higgsfield/cli` 1.2.2 installed globally (`npm i -g @higgsfield/cli`), signed in, workspace = Plus (1,179 credits on 16 Nov 2026).

Also available: the Higgsfield connection already in Claude (tools named `higgsfield`) provides generation, presets, character sheets and reference elements.

To update a pack later, ask Claude to re-download it, re-scan it and copy the markdown again.
