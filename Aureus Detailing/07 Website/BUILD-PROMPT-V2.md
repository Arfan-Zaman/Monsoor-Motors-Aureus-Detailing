# Aureus Detailing home page, version 2: build prompt

Written 15 November 2026 from the owner's feedback on version 1.

## What the owner asked for
- The hero comes first and is the most interesting part of the page, with more to interact with.
- Much less scrolling. The scroll-locked intro and scroll-locked footage in version 1 felt slow.
- Replace the light-tunnel animation with motion that belongs to a car wash.
- Use a hyper-real, latest-model Porsche Macan in the animation, in the colour that best suits the site.
- A glass and water look.
- The 3D logo in the header, not the flat one.
- Booking logic exactly as on carwashandpolish.com.au.

## The prompt

1. **Goal.** Rebuild the home page so the first screen is the show: an interactive car wash, a live price and a way to book, with no scrolling needed. Remove every scroll-locked section.
2. **Hero, "rinse it yourself".** A hyper-real 2025 Porsche Macan Electric, three-quarter front view, in a dark wash bay with a wet floor. It loads covered in snow foam. Moving the mouse or a finger sprays the foam off and reveals the clean, glossy paint; water runs down where you rinse. If nobody touches it, it rinses itself. A "Foam again" button replays it.
3. **Car colour.** Deep navy metallic (Porsche Gentian Blue). It matches the brand navy, turns the aqua lights into reflections on the paint, and white foam shows strongest against dark paint.
4. **Glass and water look.** Frosted-glass panels with water beads, a wet-floor reflection and water-drop details. Pink stays for the main buttons only.
5. **Instant price in the hero.** A glass panel: pick vehicle size and package, see the price, press "Book this".
6. **Header.** The 3D chrome logo.
7. **Less scrolling.** The hero is one screen. The team footage becomes a one-screen player with four tabs that plays on its own. Section order: hero, our work, packages, booking, workshop, quote, FAQ.
8. **Booking logic, same as carwashandpolish.com.au.**
   - Starts on workshop, Level 2 package, sedan, today's date and the first free time window.
   - Calendar runs Sunday to Saturday. Past days, closed days and locked days are disabled. If the chosen day is disabled, the first open day is chosen.
   - Each package has its own time windows. Booked and locked windows are disabled. Changing the date, package or location re-checks them and moves to the first free window if the current one is taken.
   - Add-ons can be ticked on each package card (one card's add-on list open at a time). They carry into the booking when that package is chosen, and ticks in the booking form flow back to the card.
   - Card price = package + vehicle surcharge + that card's add-ons. Booking total = package + vehicle surcharge + chosen add-ons.
   - Required: make / model / year, full name, phone, email, and the service address when mobile is chosen. Plate and notes are optional.
   - Phone: Australian landline or mobile, or a 13 / 1300 / 1800 number. Mobile numbers are spaced as they are typed. Seven throwaway email domains are refused.
   - Data sent to the server keeps the old field names; add-ons go as a list of names.
   - After a confirmed booking, make / model, plate, notes and address are cleared and the booked windows are loaded again.
9. **Image prompt, clean car.** "Hyper-realistic studio photograph of a 2025 Porsche Macan Electric SUV in deep navy Gentian Blue metallic, front three-quarter view from the driver's side, parked in a dark premium car wash bay. Freshly washed, mirror gloss, water beads on the bonnet. Thin aqua-teal LED light bars overhead reflect along the body; wet dark floor with soft reflections; a faint pink accent light at the rear. Car sits in the right 60% of a 16:9 frame, left side dark and empty. Deep navy background, cinematic, 85 mm lens, no people, no text, no number plate text."
10. **Image prompt, foam car.** "The same image, unchanged camera, car position, lighting and background, but the whole car is covered in thick white snow foam, as during a foam pre-wash, with foam sliding down the doors and wheels."
11. **Honesty.** The car is an illustration, not a customer's car. The footer says so, and that Aureus Detailing is not affiliated with Porsche. No invented reviews or claims.
12. **Done when.** No console errors, nothing overflows on a phone, the hero works with mouse, touch and keyboard, reduced-motion users get a still image, and every booking rule above passes a scripted test.

## Differences from the old site kept on purpose
- Today's time windows that have already started are disabled in the browser. The old site leaves this to the server.
- Errors show next to the field, not in a browser alert box.
- No fake reviews, placeholder ABN or interstate claims (as in version 1).
