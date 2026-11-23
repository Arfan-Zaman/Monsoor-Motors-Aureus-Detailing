# Monsoor Motors: Playbook & Daily Log

> Running record of everything we make for Monsoor Motors: business facts, brand rules, decisions, finished files and how they were made.
> **Add a new entry to the Daily Log at the bottom every day we work.** Newest entries go at the bottom.

---

## 1. Business facts (always use these, exactly as written)

| Item | Value |
|---|---|
| Business name | **Monsoor Motors** |
| Registered company | **Monsoor Motors Pty Ltd** |
| Dealer licence | **MV Dealership Licence MD32748** (spell it *Licence*, the Australian noun) |
| Official phone (shop) | **0434 137 393** |
| Email (official) | **info@monsoormotors.com.au** (older address: monsoormotors@gmail.com) |
| ABN | **31 695 324 193** (Monsoor Motors Pty Ltd) |
| Trading names | **Monsoor Motors** and **Aureus Detailing** (business name of the same Pty Ltd) |
| Director | **Mohammod A Monsor**, Sole Director and Owner |
| Website | **monsoormotors.com.au** |
| Address | **530 Albany Hwy, Victoria Park WA 6100** (Perth) |
| Tagline | *Built on trust. Driven by community!* |
| Services | **Import** (hand-picked at Japanese auctions) · **Buy** (quality used cars + **finance**) · **Sell** (fair offers on your car) |
| ❌ Not offered | **Car rental**. Don't mention it anywhere, ever |
| Positioning | **Your local Perth car dealer**: family-run, honest, fair drive-away prices |

**Watch out:** the old Facebook cover showed **0433 205 162** (Monsor's personal number). Use the official shop number **0434 137 393** everywhere unless told otherwise.

---

## 2. Brand rules (from `Brand Kit/06 Brand Guide/Monsoor-Brand-Guide.pdf`)

**Colours**
| Name | Hex | Use |
|---|---|---|
| Deep Navy | `#0F2747` | Primary, backgrounds, trust |
| Sunset Orange | `#FF5F15` | Accent only, keep rare (~10%) |
| Warm White | `#F7F5F2` | Backgrounds / text on navy |
| Slate Grey | `#5B6675` | Secondary text |
| Deep Orange | `#C2410C` | Orange text on light backgrounds |

**Font:** Montserrat only (`Brand Kit/00 Fonts/Montserrat-Variable.ttf`). Headline ExtraBold · Sub-heading Bold · Price/button SemiBold · Body Regular.

**Logo:** never redraw, stretch, recolour, rotate, or add glows/shadows/outlines. White logo on navy/dark; navy logo on light. Watermark files: `Brand Kit/01 Logo/Watermark/`.

**Photography:** real cars, daylight, honest. Never edit the car itself. **Blur customer number plates.** Ask before showing customer faces / posting customer photos.

**Voice:** honest, clear, local, warm. Never pushy. ✅ "Drive-away price, no surprises." ❌ "Best deal in Perth, guaranteed!!!"

---

## 3. Owner preferences & decisions (learned from feedback)

- **No AI label on Facebook.** Don't use AI-generated images or AI "enhance" tools on posts we want unlabelled. Our own edits (grading, plate blur, templates) add no AI tags. *Exception:* the showroom cover image (supplied by the owner) is AI-made; the owner accepted that for the **cover only**, not for car listings.
- **Cover photo style the owner liked:** showroom scene with two C-HRs + wall sign, **keep the showroom sign exactly as supplied**, cars **softened** (not over-sharpened), bottom navy fade, **IMPORT · BUY · SELL** with orange underline under each header, clear text-size hierarchy, Perth highlighted in orange.
- **Disliked:** plain/flat covers, cluttered small text, cars cut off at the edges, a single orange bar above one word, everything at the same font size.
- Wants **high resolution**, **all contact details**, **logo watermark top-left**, and **"local Perth dealer"** visible.
- Captions: the new brand "vibe" should come through **indirectly** (refresh, same trusted team), not as "we rebranded".
- Keep only the best-quality file in final folders (PNG over JPG).

---

## 4. Finished files (where everything is)

### Facebook cover (FINAL)
- `Facebook/Cover Photos/Cover Photo 1.png`: 3280×1440, upload this
- `Facebook/Cover Photos/Cover Photo 1 - Description.txt`: chosen caption + Page setup (action button, contact fields, pinned post)
- `Facebook/Cover Photos/Source Images/`: original showroom image and C-HR auction photos

**Chosen caption (Cover Photo 1):**
> Built on trust. Driven by community. 🧡
>
> Perth, you've helped us grow, so we've given things a little refresh. Same faces, same fair deals, a few new things on the way.
>
> Whether you're importing from Japan, buying your next car or selling your current one, we're here. Finance available.

### Happy Customer posts (Instagram/Facebook feed, 1080×1350)
- `Ready Posts/Upload Ready/01–08 *.jpg`: colour-graded, subjects clear of text, **all plates blurred**, no AI tags
- `Ready Posts/Colour Graded Photos/`: same photos full size without template (website / Marketplace)
- Cars: Hyundai i30, Kia Rio ×2, Toyota Yaris, Mazda CX-5 ×2, BMW X1, Toyota Prado. **Car names were guessed from photos, so confirm before posting.** Pick one of each pair. Get customer permission.

### Working / older versions
- `Ready Posts/Facebook Cover/`: earlier cover drafts (plain navy, studio, showroom versions) + `_safe-zone-check.jpg`

---

## 5. Reusable tools (`Tools/`)

Run with: `/opt/miniconda3/bin/python -I "Tools/<script>.py"`

| Script | What it does |
|---|---|
| `make_customer_posts.py` | Takes photos from `Customer Images/`, applies gentle colour grade, blurs listed number plates, lays them into the **Happy Customer** template so people/car stay above the text, saves to `Ready Posts/Upload Ready/` and `Colour Graded Photos/`. Edit the `POSTS` list (file, car name, subject top/bottom) and `PLATES` boxes for new photos. |
| `make_facebook_cover.py` | Builds the Facebook cover at 3280×1440 from `Source Images/Showroom-C-HR-source.webp`: softened cars, bottom fade, services, contacts, watermark, Perth badge, licence line. Outputs to `Ready Posts/Facebook Cover/`; copy the PNG to `Facebook/Cover Photos/` when final. |
| `showroom_cover_v2.py` | Helper used by the cover script (car softening + shared settings). Keep it next to the others. |
| `docx_to_pdf.sh` | Exports a Word document to PDF through Microsoft Word (keeps Montserrat and the exact layout). Usage: `Tools/docx_to_pdf.sh "path/file.docx"`; the PDF is saved next to it. |

Cutting a car out of its background: macOS built-in subject detection (Vision) via a small Swift tool. Ask Claude to set it up again if needed.

---

- `Tools/publish_aureus_public.sh`: publishes a clean public copy of the Aureus Detailing folder to github.com/Arfan-Zaman/Aureus-Detailing (fresh single commit, private items left out).
- `car_photo_enhance.py`: honest grade + Facebook crop for stock-car photos (light, colour, sharpen; optional background blur boxes).
- `gta_price_promo.py`: GTA-style price post for a stock car (Pricedown, green price, odometer HUD, logo top-left) from a JSON config; `--no-reel` for photos only.
- `window_view_blend.py`: keeps a real interior photo and takes only the window views from an AI edit (SIFT align + change mask). Pass the EMPTY yard plate as the reference.
- `restore_plate.py`: puts the real number plate from the original photo back into an AI-relit photo (SIFT match, warp, light match; free).
- `car_yard_composite.py`: puts a Higgsfield background-remover cutout onto the empty Monsoor yard plate (shadow, warmth, plate blur); then relight with prompt `aureus-video-studio/assets/prompts/car-yard-relight.md`.

## 6. Platform guidelines we follow

**Facebook cover (2026)**
- Upload **1640×720** (or 3280×1440 for 2×). Desktop shows ~1640×624 (top/bottom trimmed); phones show the middle **1280** px width.
- Keep text in the centre safe zone; **keep the bottom-left clear** (profile picture).
- Short, large text; desktop shows the cover at about half size.
- **No video covers** for business Pages (removed in 2021). Interactivity = cover description + action button ("Call now") + Page contact fields + pinned post.
- Cover changes **can't be scheduled**: change it manually at the right time, or schedule an announcement post in Meta Business Suite.

**Best time to post (Sprout Social 2026, local Perth time)**
- **Tue & Wed 12–8 pm** (best) · Mon 12–1 pm · Thu 12–2 pm & ~8 pm · avoid weekends/early mornings.
- Our default: **Tue/Wed 6–7 pm Perth** (= 8:30–9:30 pm on an Adelaide-time clock).
- Check *Meta Business Suite → Insights → Audience* for our own followers' active times.

**Google Business Profile:** use natural photos (`Colour Graded Photos`) in Photos; branded templates only in Posts/Updates (they show closer to 4:3, so check the crop).

**AI labels:** Meta labels images carrying AI metadata (C2PA/IPTC) or AI watermarks. Our edited files carry no metadata at all.

---

## 7. Other useful notes

- **Content creator (Perth, ~5 hrs/week):** freelancer rates roughly $35–50/hr (student), $60–90/hr (mid), $100–150+/hr (pro). Per-reel pricing ~$100–300 shoot+edit. Agree whether hours include editing; make sure we own the footage.
- **Photoshop:** no free version. Free alternatives: Photopea (browser), Affinity (`brew install --cask affinity`, installed), GIMP.
- **To-dos / open items**
  - [ ] Upload Cover Photo 1 (Tue/Wed 6–7 pm Perth) and paste the caption
  - [ ] Set Page action button to **Call now**; fill all Page contact fields
  - [ ] Confirm car models on the 8 Happy Customer posts + get customer permissions
  - [ ] Update letterhead, invoice template and email signature to info@monsoormotors.com.au + ABN 31 695 324 193 so all documents match
  - [ ] Long term: shoot a real daylight photo of the Albany Hwy lot to use in a future cover

---

## 8. Daily Log

### 2026-11-11 (Wed)
- Reviewed the Brand Kit, brand guide and customer photos.
- Made **8 Happy Customer posts** from WhatsApp customer photos → colour-graded, re-laid out so subjects aren't covered, **all number plates blurred** (incl. background cars). Confirmed no AI metadata.
- Facebook cover iterations: plain navy → studio composite (real auction photos) → owner's showroom image. **Final = Cover Photo 1** (showroom, softened cars, IMPORT/BUY/SELL with underlines, *Quality cars & finance*, full contacts, Perth badge, licence MD32748 + Pty Ltd, watermark, balanced type, stronger bottom fade).
- Researched Facebook cover guidelines, posting times, AI labels.
- Removed "Car Rental" (service discontinued); added **finance**.
- Chose caption ("Built on trust. Driven by community. 🧡 …") and saved it with the cover.
- Installed Affinity (Homebrew) as a free Photoshop alternative.

### 2026-11-16 (Mon)
- What we made / changed: Appointment letter for the CEO – AI, Digital Marketing & Business Development role (Monsoor Motors Pty Ltd, for Monsoor Motors and Aureus Detailing). Australian contractor terms: authority limits, super, GST, company-paid tool expenses, notices, e-signing, IP, WA law. Justified text, logo watermark (12 cm, 7% opacity, centred), page numbers. Plus a sources and references document.
- Files: `HR/Appointment Letters/` (private, local only, not in git). Template: `Brand Kit/05 Documents/Monsoor-Appointment-Letter-Template.docx`.
- Decisions / feedback: official email info@monsoormotors.com.au; Victoria Park postcode is 6100 (not 6154); Aureus Detailing is a business name of the Pty Ltd; owner prefers justified paragraphs.
- Set up the private GitHub repo `Arfan-Zaman/Monsoor-Motors-Aureus-Detailing` as memory and history. Not uploaded: HR, videos, audio stems, files over 100 MB, third-party tool repos. Added `CLAUDE.md` (auto-loaded project memory), the `save-progress` skill and `Tools/docx_to_pdf.sh`.
- To-do next: Director to check super (12% likely payable, Payday Super) with an accountant; verify both ABNs on ABN Lookup; sign the letter; update the letterhead and invoice template with the new email and ABN.

### 17 Nov 2026 (Aureus launch reel 1)
- What we made / changed: Launch reel 1, "We come to you. Gold detail, $199" (22 s, 9:16, 1080×1920): van arrives, the master detailer speaks to camera, polish, interior, wheels, end card with the launch offer. 38 Higgsfield credits (cap 45).
- Files: `Aureus Detailing/08 Social Media/Launch Reels/reel-1/` → `Aureus-Reel-1-Gold-Mobile-Detail.mp4` (voice + soft whooshes, leave room for music) and `…-CLEAN.mp4` (voice only, for ads); `make_reel.py` rebuilds both from `stills/` and `speaking-raw.mp4` at no cost. Videos stay local (not in git). Plan: `Launch Reels/REEL-1-PLAN.md`. Jobs: generation log.
- Decisions / feedback: mobile detailing, hyper-realistic, consistent logo; trending music is added in the app when posting (about 10–15% volume), never baked in. Captions are burned in for viewers watching muted.
- To-do next: owner to watch with sound on and approve voice and lip-sync; confirm the trainer is fine with an AI voice; turn on the "AI-generated" label when posting; then plan reel 2 (brand launch).

### 17 Nov 2026 (Aureus cinematic ad, public repo, tunnel)
- What we made / changed: Cinematic ad "The shine comes to you" (31.8 s, 9:16): swirl-mark hook → van arrives → the detailer speaks → polish, steam, wheels with animated explanations → flawless-paint close-up → wide reveal → offer. He narrates the whole ad in his own (AI) voice; original music; glass-style graphics in brand colours; cover image. 126.7 Higgsfield credits.
- Files: `Aureus Detailing/08 Social Media/Launch Reels/ad/` → `Aureus-Cinematic-Ad.mp4`, `Aureus-Cinematic-Ad-NO-MUSIC.mp4` (for adding a trending track in the app), `Aureus-Ad-Cover.png`, `make_ad.py` (rebuilds everything free), `fetch.py` (downloads Higgsfield jobs). Plan: `Launch Reels/CINEMATIC-AD-PLAN.md`.
- Public GitHub copy of the Aureus folder only: github.com/Arfan-Zaman/Aureus-Detailing (made by `Tools/publish_aureus_public.sh`; leaves out the trainer's real photos, third-party references and account set-up notes). The main repo stays private.
- Temporary website link: Cloudflare quick tunnel (`cloudflared tunnel --url http://localhost:4173`); the address changes each time and only works while the Mac is awake.
- Decisions / feedback: owner wants Hollywood-style direction, the detailer talking about the solution, a dramatic finished-paint close-up, and transparent brand-colour graphics.
- To-do next: owner to watch with sound on and approve voice; AI label when posting; Higgsfield Ads Studio "micro drama" film is a separate job needing its own budget.

### 17 Nov 2026 (Aureus ad v3: one take)
- What we made / changed: Ad v3 as one continuous take: snow foam → rinse → machine polish → hand wax → steam → wheels → sealed paint → bell → he speaks. Raw footage, ASMR sound first, his own voice, a few glass labels. Two cuts: 30 s for paid ads, 36 s full cut for organic.
- Files: `Aureus Detailing/08 Social Media/Launch Reels/ad/` → `Aureus-Ad-v3-30s.mp4`, `Aureus-Ad-v3-36s.mp4` (+ `-NO-MUSIC`), `make_ad_v3.py`. All Higgsfield jobs filed in four folders of the Higgsfield "Aureus Detailing" project; brief saved in its description.
- Decisions / feedback: owner prefers raw shots to edits; no grade or effects; music must not cover the ASMR; narrator must match his on-camera voice; text minimal, glassy, weather-matched colours; don't spend credits on what can be done free; shots must connect last frame to first frame.
- To-do next: owner listens and approves; decide whether the last (midday) speaking shot needs a golden-hour retake (about 36 credits); owner runs /send-to-project to start the Claude project; reel 2.

### 17 Nov 2026 (Aureus ad v4: clean cuts)
- What we made / changed: owner did not like the connected one-take shots (v3). Ad v4 goes back to separate shots with clean cuts: swirl close-up → van → he speaks (offer) → foam → rinse → polish → hand wax → steam → vents → wheels → wheel rinse → sealed paint → bell → offer. Raw footage, real sound, his own voice, light glass labels. 0 credits.
- Files: `Aureus Detailing/08 Social Media/Launch Reels/ad/Aureus-Ad-v4.mp4`, `Aureus-Ad-v4-NO-MUSIC.mp4`, `make_ad_v4.py`.
- To-do next: owner listens and approves; Higgsfield Ads Studio only if he wants a different concept.

### 17 Nov 2026 (Aureus ad v5: he narrates throughout)
- What we made / changed: Ad v5, 36.7 s. He speaks the whole way in one voice with a rewritten script; separate real-looking shots joined by short dissolves; muted glass visuals (damage reticle, service rail, paint layers, 2 h 30 clock, price, offer card); logo bottom centre; full sound mix mastered to about -14 LUFS.
- Script: "Your car looks fine... until the sun hits it." / on camera: "We come to you. Gold detail, 199. Done properly, or it's not done." / "First, snow foam. It lifts the dirt before I touch the paint." / "Then a machine polish. And wax, sealed in by hand." / "Inside, steam cleans the leather. Every vent gets brushed." / "Wheels, scrubbed by hand. Every spoke." / "Two and a half hours later... that's your car." / "Aureus Detailing. Twenty years of experience. Book online, today."
- Files: `Aureus Detailing/08 Social Media/Launch Reels/ad/Aureus-Ad-v5.mp4`, `Aureus-Ad-v5-NO-MUSIC.mp4`, `make_ad_v5.py`.
- To-do next: owner listens and approves the voice; if he wants a different voice, pick one from Higgsfield's presets by ear (they have no accent labels) and re-voice the on-camera line with voice change.

### 17 Nov 2026 (Aureus ad v6: connected shots removed)
- What we made / changed: owner asked to undo the first-frame/last-frame joins. Ad v6 is ad v5 with every part back on its original standalone shot: no connected footage at all (so the snow foam and rinse part is dropped, as it only existed as connected footage). Ends on the bell, then him wiping the bonnet and smiling. 32.6 s, he narrates throughout. 0 credits.
- Files: `Aureus Detailing/08 Social Media/Launch Reels/ad/Aureus-Ad-v6.mp4`, `Aureus-Ad-v6-NO-MUSIC.mp4`, `make_ad_v6.py`. The connected shots stay on disk (`clips/links/`) and in the Higgsfield folder now named "Connected shots (not used)".
- To-do next: owner listens and approves. If he wants foam and rinse back, they need two standalone 3 s shots from the existing foam and rinse stills (about 20 credits, on his say-so).

### 19 Nov 2026 (SEO agent + daily autonomous SEO started)
- What we made / changed: one-prompt SEO agent skill created and pushed to GitHub (`.claude/skills/monsoor-aureus-seo-agent/SKILL.md`, commits 5177b7d and 5dfe425); daily autonomous SEO job started in Muse, no-approval professional mode, growth tracking from 19 Nov 2026, target 100% more calls (goal, not a promise). Blog draft "Japanese import cars Perth" written (title/meta/H1, SEMrush not verified) — drafted only, not live, awaiting owner approval. Fix-first live checks: robots.txt MISSING (404); /test page live and blank; Contact page phone 0434 137 393 and licence MD32748 correct, "Rent-To-Own" still in site-wide nav and home heading, footer abbreviates address to "530 Albany Hwy"; no wrong numbers found. Duplicates confirmed: /stock (20 cars) vs /stock-list (19 cars) show different prices for 3 cars (Mazda3 $13,500 vs $12,950; RAV4 $13,990 vs $13,450; Yaris Ascent $14,399 vs $13,950); /Victoria-park repeats the stock list; /victoria-park is a near-blank live page; sitemap still lists /test and misses the 2021 X-Trail while listing a Corolla Fielder not on the stock list. Contact page meta description still not verified. Virtual Yard support request prepared with all 7 fixes (files/2026-11-19-virtual-yard-support-request.md) — NOT sent yet, owner sends via Virtual Yard Support Ticket. Nothing on the live site changed. Owner reported baseline late 19 Nov: 4 calls + 6 website enquiries per day (10 leads/day), so the doubling target is 8 calls/day.
- Files: `.claude/skills/monsoor-aureus-seo-agent/SKILL.md`, `assets/SEO-LOG.md`, `assets/GROWTH-TRACKER.md`, `assets/CONVERSATION-LOG.md`; workspace `files/2026-11-19-japanese-import-cars-perth-blog-draft.md`, `files/2026-11-19-virtual-yard-support-request.md`.
- Decisions / feedback: owner approved no-approval mode 19 Nov — agent does the work, pushes to GitHub, logs and reports; only stops if a critical fact is missing or a step would spend money, create an account, or change a legal claim. Growth tracking can now measure against the baseline (4 calls, 6 enquiries/day) from 20 Nov. Facebook still not connected; no GA4/Search Console data.
- To-do next: owner sends the Virtual Yard support request; owner to confirm correct prices for the Mazda3, RAV4 and Yaris Ascent and whether the Golf at $2,500 stays listed; next content item is `sell my car Perth` (service page) on 20 Nov; owner to report each day's call/enquiry count for the growth tracker.

### 20 Nov 2026 (Fri)
- What we made / changed: "sell my car Perth" service page finalised and pushed to the repo (SEO/content/2026-11-20-sell-my-car-perth.md) — title 55 chars, meta 144 chars, H1 "Sell My Car in Perth", written to replace the existing Sell Your Car page. Payment timing/method, what cars are bought, Notice of Disposal handling, trade-ins and valuation turnaround are marked OWNER TO CONFIRM and must not go live guessed. Yesterday's blog draft "Japanese import cars Perth" also pushed to the repo (SEO/content/2026-11-19-japanese-import-cars-perth.md) — it was local-only until today. Live re-check (16:51 ACDT): /stock and /stock-list prices now agree on all shared cars (Mazda3 $12,950, RAV4 $13,450, Yaris Ascent $13,950), but the pages still differ by one car each — 2019 Suzuki Swift GL Navigator ($11,999, Under Offer) only on /stock, 2018 Mitsubishi Outlander ES 7 Seat ($18,950) only on /stock-list. The 2021 Nissan X-Trail ST-L is now on neither page; the 2015 Corolla Fielder Hybrid is now on both, matching the sitemap. Mazda3 is no longer flagged Under Offer on either page. Home page: "Apply for Finance & Rent-to-Own" heading and "530 Albany Hwy" footer still live; phone 0434 137 393 correct. Virtual Yard ticket updated with these findings — still NOT sent. Facebook Page check blocked: personal account is connected, but reading the Page needs the owner to approve professional consent in Facebook.
- Files: `SEO/content/2026-11-20-sell-my-car-perth.md`, `SEO/content/2026-11-19-japanese-import-cars-perth.md`, `.claude/skills/monsoor-aureus-seo-agent/assets/SEO-LOG.md`, `.claude/skills/monsoor-aureus-seo-agent/assets/GROWTH-TRACKER.md` (20 Nov row added; repo copy now carries the baseline 4 calls + 6 enquiries/day, which was local-only until today); workspace `files/2026-11-20-sell-my-car-perth-service-page-draft.md`, `files/2026-11-19-virtual-yard-support-request.md`.
- Decisions / feedback: growth still not measured — no calls/enquiries reported for 19 or 20 Nov. Next content item is `car detailing Victoria Park` (Aureus service page) on 21 Nov.
- To-do next: owner sends the Virtual Yard support request; owner approves professional consent for the Facebook Page; owner confirms Mazda3 availability and the sell-my-car page answers (payment, buying policy, Notice of Disposal, trade-ins); owner reports each day's call/enquiry count.

<!-- Next entry template:
### YYYY-MM-DD (Day)
- What we made / changed:
- Files:
- Decisions / feedback:
- To-do next:
-->
