# Aureus Detailing

Written from the owner's brief and the existing site, without an interview. Lines marked (assumed) are my reading, not confirmed.

## What it is
Car detailing in Perth by the Monsoor Motors team. Two ways to use it: a mobile van that comes to a home or workplace within 20 km of Victoria Park, or drop-off at the workshop at 530 Albany Hwy, Victoria Park WA 6100. Open 8:30 am to 6:00 pm, seven days.

## Users
- Perth car owners who want the car detailed without giving up half a day; many will book from a phone. (assumed)
- People preparing a car for sale, and owners of SUVs, utes and vans. (assumed)
- Fleet and commercial customers, who ask for a quote instead of booking online.

## What they need from the site
Know what it is, what it costs for their vehicle, and book a time in under a minute. Find the workshop and the phone number without searching.

## Offer
- Silver $149, Gold $199, Aureus $299; plus $20 for SUV / 4WD / ute, plus $40 for van / commercial.
- Add-ons: headlights $60, engine bay $60, one-step correction $120, two-step $200, ceramic coating from $699.
- Pay on completion: card, EFTPOS or cash. No deposit.

## Voice
Calm, confident, premium, never pushy. Sentence case. Show the work and let it speak. No invented numbers, reviews or claims.

## Brand
See `../01 Brand Guidelines/Brand-Basics.md` and `../02 Logo/README.md`. Ocean Pulse palette, Montserrat, 3D chrome Mirror A.

## Platform
Web. Static files; the booking backend is the existing Laravel app behind carwashandpolish.com.au.

## Open questions for the owner
- Real ABN (the old site shows placeholders).
- Is the $10M insurance claim true? It is left off until confirmed.
- Rescheduling notice: the old home page says 4 hours, the old terms say 12 hours. The new site uses 12 hours.
- Is the launch offer ($25 off for the first 100 customers, $50 voucher) still running?
- The hero car is an AI illustration of a Porsche Macan, not a customer vehicle. The footer says so and that Aureus is not affiliated with Porsche. Is the owner comfortable showing a recognisable Porsche?
- The team footage shows staff faces. Are the people in it happy to appear on the site?

## Version 2 notes (15 Nov 2026)
- Hero: rinse-the-foam interaction on two matched images (`assets/img/hero-clean-*.webp`, `hero-foam-*.webp`), made with the image generator in the owner's Canva account. Masters are in `../03 Mockups/Website hero car/`.
- Booking rules follow the `bookingApp()` script on carwashandpolish.com.au. Two deliberate differences: time windows that have already started today are disabled in the browser, and the previous-month button stops at the current month.
- Tested against a stand-in for the booking server (same routes and replies as the old script expects), not the real server.
