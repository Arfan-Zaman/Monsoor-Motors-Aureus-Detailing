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

<!-- Next entry template:
### YYYY-MM-DD (Day)
- What we made / changed:
- Files:
- Decisions / feedback:
- To-do next:
-->
