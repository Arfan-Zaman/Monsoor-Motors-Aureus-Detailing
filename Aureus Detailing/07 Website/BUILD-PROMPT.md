# Aureus Detailing website: build prompt

Build the Aureus Detailing website: a marketing and booking site for a mobile and workshop car detailer in Victoria Park, Perth (sister brand of Monsoor Motors). It replaces carwashandpolish.com.au and must carry over every working feature of that site.

## Goal
A first-time visitor on a phone should know within seconds what this is (car detailing that comes to you, or drop off at the workshop), what it costs (from $149), and how to book. Booking must take under a minute.

## Brand (do not deviate)
- **Name:** Aureus Detailing, "by Monsoor Motors".
- **Logo:** the approved kit in `02 Logo/`. 3D chrome A as the hero object; flat reversed lockup in the nav and footer; favicon and app icons from `Icons/`.
- **Colours (Ocean Pulse):** deep navy `#071A33` (about 60%), deep aqua `#00A8A8` (about 30%), hot pink `#FF4D8D` (about 10%, actions only: Book now, prices, offers), ice white `#F5F8FC`.
- **Contrast rules:** navy text on pink and on aqua; never aqua or pink small text on white.
- **Type:** Montserrat, self-hosted. Sentence case. Calm, confident, premium, never pushy.

## Look and motion (from the saved references)
- **Hero:** a tunnel of light bars that you travel through as you scroll (Octaboot reference), with the chrome A standing on its mirror floor and one huge headline (big hero type).
- **Floating navigation:** a slim pill that stays visible, with the pink Book now.
- **Scroll storytelling:** real footage of the team's work, scrubbed by scroll, with a caption per stage. Real work only, no stock luxury cars.
- **Interactive package panels:** the selected package opens to show what's included; prices update live with vehicle size.
- **Motion cues:** thin aqua light lines that lead the eye to the next action.
- **Reduced motion:** everything works with motion turned off.

## Features to carry over from the current site
1. **Packages:** Silver $149 (1 h 30), Gold $199 (2 h 30), Aureus $299 (4 h), with the full inclusion lists. (Old names: Level 1 Express, Level 2 Premium, Level 3 Ultimate.)
2. **Vehicle size pricing:** Sedan / Hatch +$0, SUV / 4WD / Ute +$20, Van / Commercial +$40.
3. **Add-ons:** headlight restoration $60, engine bay clean $60, one-step paint correction $120, two-step paint correction $200, ceramic coating from $699.
4. **Online booking:** date calendar, time windows that depend on the package, mobile service or workshop drop-off, vehicle and contact details, special notes, live total, confirmation with a reference.
5. **Time windows:** Silver has six 90-minute windows from 8:30 am; Gold has four 2.5-hour windows; Aureus has two 4-hour windows.
6. **Mobile service rules:** same price within 20 km of the workshop; beyond that the team phones first to agree a travel fee.
7. **Payment:** on completion, by card, EFTPOS or cash. No deposit.
8. **Workshop:** 530 Albany Hwy, Victoria Park WA 6100; open 8:30 am to 6:00 pm, seven days; map, directions, copy address, call.
9. **Quote form:** for fleets, commercial vans and ceramic or multi-stage paint correction.
10. **Contact:** 0434 13 73 93, carwashandpolish.wa@gmail.com.
11. **Offer strip:** $25 off for the first 100 customers, plus a $50 voucher for the next wash.
12. **Privacy policy and terms of service** pages.
13. **Spam protection:** hidden honeypot field and a disposable-email check.

## Left out on purpose (not true or not verifiable)
- "4.9 / 5.0, 850+ reviews" and the six customer reviews from Brisbane, Sydney, Melbourne and the Gold Coast. The business is new and in Perth.
- "Australia's trusted", interstate coverage lists, and "$10M insured" until a policy is confirmed.
- The placeholder ABNs, Sydney address, 1300 number and other placeholder contact details in the old policy pages.

## Technical
- Static HTML, CSS and plain JavaScript; no build step, no frameworks, no tracking.
- Booking and quote forms post to the existing Laravel routes (`/booking`, `/quote`, `/booking/booked-slots`) when the site is served from that backend; otherwise they fall back to a prefilled email so nothing is lost.
- Works from 360 px phones to wide desktops; keyboard accessible; visible focus; labels on every field; errors say what's wrong and how to fix it.
- Pages: `index.html`, `privacy.html`, `terms.html`, `404.html`.

## Done means
Every link, button, form state and page works on desktop and mobile, checked in a real browser, and the result matches the brand guide.
