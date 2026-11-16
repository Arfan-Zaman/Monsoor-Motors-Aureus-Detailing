# Aureus Detailing website, version 3: design brief

> **Update 17 Nov 2026 (2):** the lens and manual polishing were removed ("like a toy"). The hero is now a **scroll-scrubbed film** (Higgsfield's official scroll-scrub method): `assets/scrub.js` plus `assets/film/` (one 15 s Kling 3.0 Turbo film, 32 credits in total). Five short chapters over the film, the "Our work" section removed, and the packages layer graphic removed (the film shows it). The film MP4s are excluded from git by `.gitignore`; their source job is in the generation log.

> **Update 17 Nov 2026:** the owner rejected the foam / wash-bay concept. Version 3 was built on **"Into the Paint"** instead. Sources: the keyframes and film in `storyboard/` (STORYBOARD-4-KEYFRAMES.md, VIDEO-PLAN.md, clips/Aureus-Website-Film-draft.mp4).
> What was built:
> - `assets/paint.js`: a glass lens over the bonnet showing micro-paint; "Look closer" dives into the paint; an aqua polishing arc sweeps the scratches flat; the pointer polishes; flakes twinkle; the price rolls like an odometer; headings get a polish sweep.
> - `assets/v3.css`: dark bay throughout, Cormorant Garamond headlines, frosted glass, packages as glowing paint layers (Silver = surface, Gold = clear coat, Aureus = ceramic shield) that light up with the chosen package, and a crystal tick on booking confirmed.
> - `index.html`: new hero markup, layers block, tick. The booking engine (`app.js`) is untouched.
> Below is the original foam brief, kept for history.


Written 16 November 2026, for approval before building. Builds on version 2: the booking engine, section order and content stay; the look and motion are rebuilt.

## The idea: "the wash bay at night"
The whole site is one dark, wet wash bay lit by aqua LED bars. Everything you touch behaves like water on glass: it ripples, beads, runs and gets squeegeed clean. Aureus means gold coin, so headlines are set like an engraved Roman inscription. That's the premium "gold standard" note against the wet, modern bay.

**One signature moment, everything else quiet.** The hero is the show. Below it, motion only answers what you do (choose, book, open), plus one wipe on each section heading.

## Colour (from the brand kit)
| Name | Hex | Role |
|---|---|---|
| Bay navy | #071A33 | Page background, most of the site |
| Deep bay | #04101F | Shadows, footer, wet floor |
| Aqua LED | #00A8A8 / glow #5FF0E6 | Light bars, ripples, focus rings, highlights |
| Frost | #F5F8FC at 6–14% over blur | Glass panels; solid #F5F8FC for text |
| Hot pink | #FF4D8D | "Book" actions and prices only, about 5% of the screen |

The light "ice" sections are removed: the whole page stays in the bay. The booking form sits on frosted glass with high-contrast text, so it's still easy to read and fill in.

## Type
- **Headlines: Cinzel** (Roman inscription capitals, free OFL font, self-hosted). It's the brand's chosen heading font and fits "Aureus". Wide letter-spacing, large sizes only. It's never used for labels or small text.
- **Everything else: Montserrat** (brand font). Body 17/1.6, lines under 70 characters.
- No all-caps labels, no small headings stacked above titles, no arrows tacked onto button text.

## Layout (section order unchanged)
```
┌──────────────────────────────────────────────┐
│ [3D chrome logo]            Book now (pink)  │  glass header
│                                              │
│  DETAILING,         ░░ foam-covered car ░░   │  ONE SCREEN
│  PERFECTED.         ░ LED bars overhead ░    │  hero = the show
│  sub line                                    │
│  [Rinse the car]   ┌ glass price dock ┐      │
│  facts             │ vehicle · package│      │
│                    │ $199  [Book this]│      │
└──────────────────────────────────────────────┘
  Our work      one-screen player, 4 stages, plays itself
  Packages      three "bays" side by side, each lit from above
  Booking       frosted glass: calendar | times | details | summary
  Workshop      map, hours, address, directions
  Quote · FAQ · footer (AI-illustration and no-Porsche-affiliation note)
```
Left-aligned text throughout. The car and the dock hold the right side of the hero.

## Motion
1. **Bay lights on (page load, about 1.5 s, once).** The aqua LED bars above the car flicker on one by one. The foam-covered car comes up out of the dark. The headline condenses into view like breath on glass. Then the price dock settles in.
2. **Rinse it yourself (hero, upgraded).** Your pointer is a pressure-wash nozzle: foam sprays off where you move (kept from v2). New: real water ripples refract the car where you pass (GPU water simulation), and droplets bead and run down the glass in front of the car. If nobody touches it, it rinses itself. "Foam again" replays it.
3. **Wet glass.** The price dock and package cards carry live water beads. A bead trickles when you hover.
4. **Odometer prices.** Switching vehicle or package rolls the price digits like a car's odometer. Your eye goes straight to what changed.
5. **Squeegee reveal.** Choosing a package wipes its card clean with one squeegee stroke and shows what's included. Each section heading gets one squeegee wipe as it enters the screen. There are no fade-up-everything effects.
6. **Press ripple.** Pink buttons ripple from exactly where you press.
7. **Booking confirmed.** A ring fills with water and turns into a tick.

**Rules for all motion**
- Nothing locks scrolling.
- Everything pauses when off-screen.
- 60 fps target.
- **Reduced motion:** visitors who turn animation off see a still clean car, instant prices and no ripples.
- **Phones:** touch works as the nozzle. Lighter effects on low-power devices.

## Kept from version 2 (not touched)
- Booking rules matching carwashandpolish.com.au: calendar, time windows, add-ons, totals, validation and server field names.
- All copy, prices ($149 / $199 / $299, +$20 SUV, +$40 van), hours, address and phone.
- The honesty notes. No invented reviews or claims.

## Needs your answer (unchanged from v2)
- Is the launch offer ($25 off for the first 100 customers + $50 voucher) still running? If not, it gets removed.

## Done when
- No console errors and no horizontal overflow on phone, tablet or desktop.
- The hero works with mouse, touch and keyboard.
- Reduced motion shows the still version.
- Every booking rule still passes a scripted test.
- Screenshots of desktop and phone are reviewed before handover.
