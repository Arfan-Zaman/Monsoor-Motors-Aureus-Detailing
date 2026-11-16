---
name: aureus-video-studio
description: Use for any Monsoor Motors or Aureus Detailing video or image made with Higgsfield (reels, TikToks, ads, before/after, logo reveals, car showcases). Covers which Higgsfield skill pack to use, keeping characters, cars and brand assets consistent across videos, where assets live, logging every generation, and the brand and legal rules. Load before calling any Higgsfield generation tool in this project.
---

# Aureus / Monsoor video studio

The house workflow for making videos with Higgsfield. It sits on top of the official **Higgsfield connection** (the `higgsfield` tools in Claude) and the downloaded prompt skill packs. The packs teach *how to write prompts*; this skill keeps *our* work consistent and repeatable.

## 1. Before generating anything
1. Read `Aureus Detailing/01 Brand Guidelines/Brand-Basics.md` (or the Monsoor brand rules in the playbook) and `assets/ASSET-REGISTER.md` in this folder.
2. Check `assets/GENERATION-LOG.md`. If a similar shot was made before, reuse its prompt, seed and references instead of starting again. This saves credits and keeps the look the same.
3. Check the credit balance (Higgsfield `balance`) and tell the owner the cost before a paid generation. Don't spend more than the agreed budget.

## 2. Pick the right skill pack

| Job | Use |
|---|---|
| Any prompt: structure, camera, lighting, model choice, fixing a failed generation | `higgsfield-prompt-suite` (router: it points to the right sub-skill, e.g. `skills/higgsfield-camera`, `higgsfield-seedance`, `higgsfield-troubleshoot`) |
| Same person or character across many videos | `higgsfield-prompt-suite/skills/higgsfield-soul` + `higgsfield-character-design`, and section 3 below |
| Car showcase / 360° turn | `hf-09-product-360`, `hf-01-cinematic` |
| Before / after detail reveal | `hf-video-07-before-after` |
| Scroll-stopping first 2 seconds | `hf-11-social-hook`, `hf-video-01-viral-hook` |
| Premium, gold-standard look (Aureus) | `hf-video-06-luxury-aesthetic`, `hf-12-brand-story` |
| Logo reveal / motion graphics | `hf-06-motion-design-ad`, `higgsfield-prompt-suite/skills/higgsfield-motion-design` |
| UGC-style ad (person talking to camera) | `ugc-factory`, `hf-ugc-video-auto` |
| Real customer testimonial format | `hf-video-08-testimonial-story` (**real** customer words only) |
| Dealership walkaround | `hf-15-real-estate` (walkthrough structure works for a car yard) |

Other packs (anime, fight scenes, music video, food, fashion, podcast, SaaS, course) are installed but rarely right for a car business.

## 3. Consistency: characters, cars and brand

**People (presenter, "Aureus detailer" character)**
- Make the character **once**: a character sheet (Higgsfield `get_workflow_instructions` with workflow `character-sheet`) or a Soul ID trained on **consenting** real staff photos.
- Save it as a **reference element** (`manage_reference_elements`) and record its ID in `assets/ASSET-REGISTER.md`. Every later prompt uses that reference, never a fresh description.
- Keep the same wardrobe: navy Aureus polo, chrome A logo on the chest.
- Never create a likeness of a real person without their written OK. Never imitate a celebrity.

**Cars**
- Real stock cars: use the dealer's own photos as image references. **Blur number plates.** Never change a real car's colour, condition or features (Australian Consumer Law: no misleading ads).
- The website hero (AI Porsche Macan) is an illustration. Label it "AI-generated" and never present it as a customer car.

**Brand**
- Aureus: navy #071A33, aqua #00A8A8, hot pink #FF4D8D (≤10%, buttons and stickers only), white #F5F8FC; Montserrat; chrome A logo from `Aureus Detailing/02 Logo/`.
- Monsoor Motors: navy #0F2747, orange #FF5F15 (accent only), warm white #F7F5F2; logo from `Brand Kit/01 Logo/`.
- End card: logo, phone 0434 137 393 and the handle (@aureusdetailing.com.au for Aureus).
- The same seed plus the same references gives a matching look. Log both.

## 4. Asset library (where things live)
- `assets/ASSET-REGISTER.md`: every reusable asset: characters, reference elements, Soul IDs, logos uploaded to Higgsfield (media IDs), approved style prompts, music.
- `assets/GENERATION-LOG.md`: one line per generation: date, project, model, prompt file, seed, references, cost, result link, keep / reject and why.
- Finished files: `Aureus Detailing/08 Social Media/Posts/<YYYY-MM-DD>-<slug>/` (or `Ready Posts/` for Monsoor). Keep raw videos out of git (`.gitignore` already blocks `.mp4`). Store the Higgsfield link in the log instead.
- Prompts that worked: save them in `assets/prompts/<slug>.md` so they can be reused exactly.

## 5. Rules (Australian law and platform policy)
- Label AI content where Instagram, TikTok or Facebook require it.
- No fake reviews, testimonials, customer counts or before/after results (ACCC / Australian Consumer Law).
- Only show staff or customers who have agreed; blur plates.
- No sexualised or "hot girl" style content, no violence, no copied music or brands (no Porsche or other badges as our own).
- Prices on screen must match the booking page.

## 6. After generating
1. Watch or check the result. Reject anything off-brand, with a wrong car or garbled text.
2. Log it in `assets/GENERATION-LOG.md`.
3. Save a winning prompt to `assets/prompts/`.
4. Auto-save pushes everything to GitHub. Add the day's summary to the playbook Daily Log.

## Sources of the installed packs
See `SOURCES.md` in this folder.
