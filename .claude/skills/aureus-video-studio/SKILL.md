---
name: aureus-video-studio
description: Use for any Monsoor Motors or Aureus Detailing video or image made with Higgsfield (reels, TikToks, ads, before/after, logo reveals, car showcases). Covers which Higgsfield skill pack to use, keeping characters, cars and brand assets consistent across videos, where assets live, logging every generation, and the brand and legal rules. Load before calling any Higgsfield generation tool in this project.
---

# Aureus / Monsoor video studio

The house workflow for making videos with Higgsfield. It sits on top of the official **Higgsfield connection** (the `higgsfield` tools in Claude) and the downloaded prompt skill packs. The packs teach *how to write prompts*; this skill keeps *our* work consistent and repeatable.

## 1. Before generating anything
1. Read `Aureus Detailing/01 Brand Guidelines/Brand-Basics.md` (or the Monsoor brand rules in the playbook) and `assets/ASSET-REGISTER.md` in this folder.
2. Check `assets/GENERATION-LOG.md`. If a similar shot was made before, reuse its prompt, seed and references instead of starting again. This saves credits and keeps the look the same.
3. Check the credit balance (`higgsfield account status`, or the paid connector's `balance`; the first Higgsfield connector is a separate free account with 0 credits) and tell the owner the cost before a paid generation. Don't spend more than the agreed budget.

## 2. Pick the right skill pack

| Job | Use |
|---|---|
| **Generate an image or video (official)**: run it through the Higgsfield CLI (`higgsfield`, signed in to the Plus workspace) or the paid Higgsfield connector | `higgsfield-generate` (official). Also official: `higgsfield-soul-id` (consistent people), `higgsfield-product-photoshoot`, `higgsfield-brandkit`, `higgsfield-faceless-video`, `higgsfield-video-explainer`, `higgsfield-youtube-thumbnail`, `higgsfield-marketplace-cards`, `higgsfield-websites` |
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
- **Higgsfield destination:** project **Aureus Detailing** in the Plus workspace. workspace_id `68fdca71-5be8-4d53-ac58-fa86267eb49b`, project/folder_id `5b8de463-c51c-494a-9cf5-608268e53889`. Pass this `folder_id` on every Aureus generation. Monsoor Motors work does not go in this project.
- **Monsoor Motors destination (set 21 Nov 2026):** project **Monsoor Motors**, project and root folder id `fede0767-fd25-4fc1-b998-cf207b85dba4`. Subfolders: Characters `807c11b2-2b67-4a36-a00a-23eeca0b4160`, Cars `efcfe4d8-0cbc-4304-b008-bc02d73f9541`, Voices `d23fa704-4b62-484f-9dca-d311e2e9937f`, Locations `1481f567-aae0-492b-9597-df92e5ecd99b`. **Standard background for every Monsoor Motors video (set 21 Nov 2026): element `Japan-Auction-Yard-2-Views`** (Japanese auction yard, three-quarter and straight-on views; the older single-view element `Japan-Auction-Yard-Plate` is superseded). Use it in every keyframe so all videos share one place. Pass the matching `folder_id` on **every** Monsoor generation and attach every upload with `attach_project_asset`, without being asked. The owner expects every sheet, car and voice to be in the project.

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

## 7. Launch reel framework (set 17 Nov 2026)
- **Format:** every reel image and video is **9:16 vertical, 1080×1920** (Instagram Reels, Facebook Reels, TikTok). Keep text and faces inside the centre safe area (avoid the top 250 px and bottom 400 px, which the apps cover). Reference sheets and boards may be 16:9.
- **Lead character:** "the master detailer" (real staff member, consent confirmed). Always pass the character board job and the face reference uploads from `assets/ASSET-REGISTER.md` as image references; never describe his face from scratch and never alter it.
- **Uniform (v1, also the real staff uniform design):** deep navy #071A33 piqué polo, twin aqua #00A8A8 tipping on collar and cuffs, aqua inner placket, embroidered chrome A + "AUREUS DETAILING" on the left chest only, charcoal work trousers, black belt, black work shoes.

## 8. One-take method (owner's preferred look, set 17 Nov 2026)
The owner prefers raw Higgsfield footage to edited versions. Build ads like this:
- **Keyframes first:** one 9:16 still per step with the detailer in it (character board + face reference + a scene still for light and place). 2 credits each.
- **Clean cuts, not connected moves.** The owner tried start-image + end-image links (one continuous take) and rejected the look on 17 Nov 2026. Make one 3 s Kling 4.0 shot per keyframe (start image only, 9.75 credits) and cut between them. The first 1.5 s of an existing link is still a clean shot and can be reused free.
- **He speaks early:** van arrives, then him to camera with the offer inside the first 10 s, then the services, the bell, the offer card.
- **Real speed only.** Never retime a shot. No grade, grain, zooms, flashes or pop-up graphics on the footage.
- **Sound:** Kling's own audio is unreliable (often music). Use `mirelo_text_to_audio` (0.75 credits per 3 s) for close-mic ASMR per activity; his voice only, cloned from `ad/audio/v4/persona-voice-ref.wav`; music about 13 dB under the sound.
- **Text:** a few frosted-glass labels (footage blurred behind them), warm white, no brand colours pushed; watermark top left at about 55%.
- **Lengths:** 30 s for paid ads with the offer on screen in the first 3 s; a longer full cut for organic.
- **Edit free on this Mac:** `Launch Reels/ad/make_ad_v6.py` (standalone shots only) (he narrates throughout; 6-frame dissolves; muted glass visuals; logo bottom centre; master to -14 LUFS). Spend credits only on new shots, and file every job in the Higgsfield project folders (asset register).

## 9. Realism workflow (set 21 Nov 2026, from Higgsfield's own tutorial "How I Get Perfect AI Realism in Every Shot", youtu.be/1BzzdY-nK9A)
Use this order for every new video. It replaces guessing with cheap tests, and it is why earlier runs wasted credits.

**A. Plan before spending**
1. Script, then a shot list: decide how much action fits in one generation and split scenes to match.
2. Test the plan free or cheaply first: a Blender previs (`Ready Posts/2026-11-21-ceo-intro-video/previs/`) or black-and-white storyboard frames. Fix the prompt here, before any video credit. The video prompts must match the storyboard shot for shot.

**B. Build the assets (the foundation)**
3. Characters: grey background, three views in one sheet (face close-up, full-body front, full-body back). No blown-out highlights on the face in the sheet: they turn into plastic skin in close-ups. The expression on the sheet carries into the acting, so put the wanted expression on the sheet.
4. Locations: generate at a **three-quarter angle**, not straight-on, so the video model can see the layout and does not have to invent the rest when the angle changes. State the lighting; it sets the mood and colour. For a second location in the same film, attach the first as a reference so light and colour match.
5. Real products and cars: start from a real photo, make a prop sheet from several angles, and check the sheet against reality (for example steering wheel on the correct side: right-hand drive for our Japanese imports).
6. Avoid thin stripes and fine patterns on clothes: they shimmer and smear.
7. **Test the pair** (character + location) in one cheap still or draft before committing. If the face looks fake or the light does not match, change the asset, not the prompt.
8. Lock the winners, give each a name, save each as a reference element, and file it in the Higgsfield project. Every later prompt calls the assets by those names (element placeholders), never by a fresh description.

**C. Generate**
9. Video prompts follow the storyboard: the exact order of actions, the framing of each shot, the lighting.
10. Say how a thing is **used**, not only how it looks (a cap that flips, a door on the driver's side, which hand).
11. Say how the character **feels** during the action: expression, energy, how he moves. Flat acting comes from prompts with no emotion.
12. No superlatives ("very white", "extremely shiny"): the model overdoes them.
13. When the same fault repeats in two takes, the cause is usually the **reference image**. Fix the reference, then regenerate; do not keep rewriting the prompt.
14. Small wrong detail (text, a label): grab a frame, fix only that detail in an image model, and feed the fixed frame back as a reference.
15. Generate two or three takes of the same shot list, then cut the best part of each together. The matching shot list is what makes them cut.
16. Product or logo shot: a small camera move, then hold still long enough to read.
17. Use draft mode first where the model has it (Seedance 2.5 `draft: true`, a 480p draft that can be finalised within seven days via `draft_job_id`), and finalise only the take that works.

**D. AI direction (Higgsfield "Cinema Studio 4.0", model `cinematic_studio_video_4_0`)**
- This is the option with automatic prompt direction. It takes the same references as Seedance (mode `omni_reference`: `start_image`, `end_image`, `image_references`, `video_references`, `audio_references`), 4 to 30 s, up to 1080p.
- Its direction controls are separate parameters, not prompt words: `era_id`, `camera_model_id`, `camera_lens_id`, `camera_aperture_id`, `pacing_id`, `genre_id`, `light` + `light_id`, `color_palette`. Look the ids up with `get_presets` before use; never invent an id.
- How to use it properly: give it the locked assets as references and a start frame; set camera body, lens and aperture to match the previs (for example 35 mm for the wide two-shot, 50 mm for the single); choose natural daylight lighting and a calm pacing; keep the prompt to action, order and emotion, and leave camera and light to the controls so the two do not fight.
- Our rule on top: no heavy grade, real speed, one continuous move per shot, as in the "edit like a human" section of CLAUDE.md.

