# SEO Audit: monsoormotors.com.au

**Date:** 16 November 2026 · **Scope:** all 31 URLs in the sitemap (11 main pages + 20 car listings), plus robots.txt, redirects, structured data and local (Perth) signals.
**How:** automated crawl of the live site (titles, descriptions, headings, canonicals, robots tags, schema, images) and manual checks. **Not measured:** page speed / Core Web Vitals, backlinks, keyword rankings. Those need Google Search Console and PageSpeed Insights access.

**Platform note:** the site runs on a dealer website platform (car photos are served from virtualyard.com.au). Most fixes below are settings in that platform's admin or a request to its support, not code changes.

---

## Score at a glance

| Area | Status |
|---|---|
| HTTPS, www / http redirects | ✅ Good: all redirect to https://monsoormotors.com.au/ |
| Mobile viewport, language tag | ✅ Good |
| Car listing schema (price, VIN, km, InStock) | ✅ Good, a real strength |
| Contact details consistency (NAP) | ❌ Wrong phone and "rentals" in Google snippet |
| robots.txt | ❌ Missing (404) |
| Meta descriptions | ❌ 7 missing, 18 far too long |
| H1 headings | ❌ 7 main pages have none, car pages have two |
| Duplicate / junk pages | ❌ /test is live and in the sitemap; /stock = /stock-list |
| Local business schema | ❌ None (no AutoDealer / LocalBusiness) |
| Analytics / tracking | ⚠️ No Google Analytics, Tag Manager or Meta Pixel detected |
| Error pages | ⚠️ Missing pages return 200 instead of 404 |

---

## 🔴 Fix first (this week): these hurt trust and rankings now

1. **Wrong phone number and "rentals" in Google results.** The Contact page description (what Google shows under the link) says *"Call 0433 205 162 for hybrid imports, rentals and lease-to-own enquiries."* The official number is **0434 137 393**, and car rental is no longer offered. 0433 205 162 also appears 3 times in the page code.
   → Change it to: *"Contact Monsoor Motors, 530 Albany Highway, Victoria Park WA 6100. Call 0434 137 393 for quality used cars, Japanese imports, finance and selling your car."*
2. **Other phone numbers on the site.** 0483 153 638 and (08) 4931 0421 also appear on the home and contact pages. Confirm whether they're current. Google trusts a business more when the name, address and phone (NAP) match everywhere: website, Google Business Profile and Facebook.
3. **Remove the `/test` page.** It's live, indexable, titled "test" and listed in the sitemap. Delete it or set it to noindex, and remove it from the sitemap.
4. **Add a robots.txt** (currently 404). Minimum:
   ```
   User-agent: *
   Allow: /
   Sitemap: https://monsoormotors.com.au/sitemap.xml
   ```
5. **Duplicate stock pages.** `/stock` and `/stock-list` show the same content with the same title, and each points to itself as canonical. Keep one (suggest `/stock`), redirect the other to it with a 301, and list only that one in the sitemap. `/Victoria-park` and `/victoria-park` both load too, so use lowercase only.

## 🟠 Fix next (this month): on-page basics

6. **Add meta descriptions (about 140–160 characters)** to: Stock, Services, Newsletter, Find Me a Car (currently just repeats "Find Me A Car"), Toyota Kluger, Subaru Outback. Suggested text:
   - **Stock:** *Browse quality used cars and Japanese imports for sale in Perth. Drive-away prices, finance available. Monsoor Motors, Victoria Park.*
   - **Services:** *Import, buy and sell cars with Monsoor Motors: hand-picked Japanese auction imports, quality used cars with finance, and fair offers for your car.*
   - **Find Me a Car:** *Tell us the car you want and our team will find it, locally or at Japanese auction. Monsoor Motors, Victoria Park, Perth.*
7. **Car listing descriptions are 600–1,300 characters and in CAPITALS.** Google cuts them off at about 155 characters, and all caps reads as shouting. Use a short generated template per car instead:
   *"2016 Toyota RAV4 GX auto, 205,667 km, $13,990 drive-away. Inspected and ready, finance available. Monsoor Motors, Victoria Park, Perth."*
8. **Car listing titles** are capitals only, with no year, price or location, e.g. "TOYOTA RAV4 GX (2WD) ZSA42R MY16". Better:
   **"2016 Toyota RAV4 GX 2WD Auto, $13,990 | Monsoor Motors Perth"** (under 60 characters where possible).
9. **One clear H1 per page.**
   - **No H1 at all:** Services, Stock, Stock List, Victoria Park, Sell Your Car, Find Me a Car, Newsletter. Add one each, e.g. "Used Cars for Sale in Perth", "Sell Your Car in Perth: Fair Cash Offers".
   - **Home page:** its H1 is "Search Our Vehicles". Make it "Quality Used Cars & Japanese Imports in Perth".
   - **Car pages:** each has two H1s ("PAJERO" twice). Keep one: "2012 Mitsubishi Pajero GLS LWB 4x4".
10. **Sold or hidden cars:** 4 listings (Civic, CX-5, Mirage, Swift) are set to noindex but are still in the sitemap. Remove noindexed pages from the sitemap. When a car sells, either redirect its page to /stock or keep it with a clear "Sold" label and similar cars.
11. **Missing pages return "200 OK"** (soft 404), for example /this-page-does-not-exist. Ask the platform to return a real 404 status.

## 🟡 Grow (next 1–3 months): local SEO and tracking

12. **Add AutoDealer schema** to the home and contact pages: name, legal name, ABN, address, phone, opening hours, geo coordinates, licence, and links to Facebook and Google Business Profile. This feeds Google Maps and the knowledge panel. A ready-to-paste JSON-LD block can be generated from the playbook facts on request.
13. **Install tracking:** Google Analytics 4, Google Search Console (verify the domain and submit the sitemap), and the Meta Pixel for Facebook and Instagram ads. Right now there's no data on visitors, enquiries or ad results.
14. **Use one address format everywhere:** *530 Albany Highway, Victoria Park WA 6100*. The site currently mixes "Hwy" and "Highway", and sometimes leaves out the postcode.
15. **Local landing content.**
    - The Victoria Park page is a good start. It needs an H1, 200–400 words about the yard, a map, opening hours and directions.
    - Consider pages for high-intent searches: "Japanese import cars Perth", "car finance Perth bad credit / lease-to-own", "sell my car Perth".
16. **Image performance:** no lazy loading and no WebP images were detected, and car pages load 36–54 images. Ask the platform about lazy loading and compressed images (helps mobile speed and rankings).
17. **Caching:** pages are sent with `no-store, no-cache`, so browsers re-download every visit. Ask the platform whether caching can be enabled.
18. **Aureus Detailing:** when its website goes live, link to it from the Monsoor Motors Services page and back, and give it its own Google Business Profile category (car detailing).

---

## What's already working well
- Clean HTTPS with correct www and http redirects.
- Each car listing has structured data with price, VIN, kilometres and availability. That makes listings eligible for rich results.
- Good, keyword-focused titles on Home, Finance, Sell Your Car and Victoria Park.
- The dealer licence MD32748 and the address are shown on the site.

## Next steps
- [ ] Fix the Contact description, phone numbers and /test page (items 1–3). This can be done in the website admin today.
- [ ] Send items 4, 5, 10, 11, 16 and 17 to the website platform's support as one request.
- [ ] Rewrite descriptions, titles and H1s (items 6–9). Claude can draft all of them in one go.
- [ ] Set up GA4, Search Console and the Meta Pixel (item 13). After that, run a speed and rankings audit.
