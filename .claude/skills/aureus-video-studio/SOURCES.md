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

## Design and motion skills (17 Nov 2026)

Markdown only (SKILL.md plus reference files). No scripts, hooks, settings or installers were copied or run. Each SKILL.md was read and scanned for remote-code, credential and settings instructions; none found.

| Folder in `.claude/skills/` | Source | Commit | Licence | Notes |
|---|---|---|---|---|
| `motion-design/` | github.com/lottiefiles/motion-design-skill (`skills/motion-design`) | f9a8a04 | MIT | LottieFiles motion principles: timing, easing, choreography, Disney principles |
| `awwwards-animations/` | github.com/devmartinese/awwwards-animations-skill | c92d00b | MIT (stated in README, no LICENSE file) | GSAP, Motion, Anime.js, Lenis patterns for React |
| `software-ui-ux-design/` | Original github.com/vasilyu1983/AI-Agents-public is no longer reachable; copied from the mirror github.com/gabrielmoreira/agent-skills-mirror (`mirrors/repos/vasilyu1983@AI-Agents-public/skills/universal/software-ui-ux-design`) | c51f7a2 (mirror commit) | **Original licence unknown** (mirror repo is MIT): private use only | `scripts/` (Python), `data/` (CSV database, same one as `ui-ux-pro-max`) and `agents/` left out, so the `python3 scripts/...` commands in its SKILL.md will not work here; use `ui-ux-pro-max` for that search |
| `design-better/` | github.com/buildgreatproducts/builder-os (`skills/design-better`) | fb74cac | MIT | Single SKILL.md of UI quality heuristics |
| `frontend-design-ui-ux/` | github.com/ulpi-io/skills (`frontend-design-ui-ux`) | b3e5e33 | **None stated**: private use only | Design-spec skill; writes its spec to `.ulpi/design/` and can call a `browse` skill that is not installed |
| `motion-design-web/` | github.com/curiositech/windags-skills (`skills/motion-design-web`), origin of claudskills.com/skills/motion-design-web | 6992af5 | SKILL.md says Apache-2.0, but the repo LICENSE is Business Source License 1.1 (non-commercial and personal use; commercial needs a licence): check before relying on it for client work | Single SKILL.md |
| `gsap-framer-scroll-animation/` | github.com/github/awesome-copilot (`skills/gsap-framer-scroll-animation`), origin of claudskills.com/skills/gsap-framer-scroll-animation | dc0083d | MIT | GSAP ScrollTrigger and Framer Motion scroll recipes |
