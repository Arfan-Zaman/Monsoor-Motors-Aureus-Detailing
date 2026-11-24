# C-HR Hybrid (black, Japan state): exterior reference sheet

Method: Higgsfield's Product Reference Sheet workflow with a GLOBAL IDENTITY LOCK (from `higgsfield-prompt-suite/skills/higgsfield-gpt-image-2/reference-sheet-workflow.md`), rewritten for this exact car.
Model: gpt_image_2_6, 4K, high, 16:9. If the result looks flat, rerun the **same** prompt unchanged in nano_banana_pro.

References, all upscaled to 4K from the real Japan yard photos (`Cars/Toyota C-HR Hybrid (black)/Japan yard (real)/`):
- @image1 = photo 03, front three-quarter (left)
- @image2 = photo 06, front three-quarter (right side of car, bonnet decal)
- @image3 = photo 10, front close (headlight, bonnet edge)
- @image4 = photo 05, rear three-quarter
- @image5 = photo 07, rear straight-on
- @image6 = photo 01, front lip, grille, fog light, LED strip
- @image7 = photo 02, front lip and bumper from the other angle
- @image8 = photo 04, wheel close-up

## Prompt

```text
Use @image1 to @image8 as strict photographic references of ONE real car: a black Toyota C-HR Hybrid (Japanese-market, first generation) with a TRD aero kit. Create a high-resolution studio reference sheet of the EXACT SAME car. This is not a redesign or a reinterpretation. It must look like this exact physical car was professionally detailed for sale, then rolled into a studio and photographed from every angle.

GLOBAL IDENTITY LOCK (CRITICAL). Preserve exactly what the references show:
- body: first-generation C-HR shape, proportions, stance, ride height and wheelbase; deep black paint
- front: slim LED headlights with the chrome brow line running into the bonnet edge; blue-outlined Toyota hybrid emblem in the upper grille; the small white TRD decal on the bonnet edge above the headlight, on the same side and in the same place as in @image2: a thin handwritten-style script reading "Racing Development" followed by a small boxed "TRD" logo (the references are slightly soft here; render the letters cleanly as "TRD", never as other letters); the TRD front lip spoiler in dark grey/black with a horizontal row of small LED lights set into its lower edge (@image6, @image7); a large honeycomb-mesh lower grille; round LED fog lights in black surrounds; the empty front plate bracket area exactly as in @image6
- sides: black door-window weather visors on all side windows; black lower side skirts; the small HYBRID badge on the front guard; black door mirrors
- wheels: the black multi-spoke alloy wheels from @image8 with the Toyota centre caps; the same tyres
- rear: the TRD roof wing with its rectangular cut-outs, exactly as in @image4 and @image5; red and clear C-HR tail lights; the blue-outlined Toyota hybrid emblem in the centre of the tailgate; seen from behind, the chrome "C-HR" lettering badge on the left and the small rectangular silver-and-blue HYBRID badge on the right of the tailgate, as in @image5; the black shark-fin antenna on the roof; the black rear bumper and diffuser shape exactly as in @image5; the rear wiper; on the rear glass, exactly where they are in @image5: two round blue-and-white stickers low on the left, a few small round green and blue stickers on the right, and a small white Toyota dealer script decal just above the right of the wiper
- keep every badge, emblem, decal and sticker exactly as photographed: same typography, size, colour and position. Treat them as physical parts of the car. Do not invent any text, badge or sticker that is not in the references.

REMOVE ONLY THESE:
- the white auction chalk writing ("COM") on the windscreen and rear glass: glass must be clean
- all dirt, road grime, water drops and rain spots
- there are NO number plates on this car: keep the front plate bracket and the rear plate recess empty, exactly as in @image5 and @image6. Do not add a plate

PRE-SALE DETAILED CONDITION: the car looks exactly as a dealer's car does after a professional pre-sale detail: deep glossy black paint with crisp, even reflections, no swirl marks, clean glass, clean black wheels with the spokes and centre caps spotless, tyres dressed in a satin (not wet-look) black, black trims restored, lights crystal clear. Do not change any part, colour or shape: only clean it.

REFERENCE SHEET LAYOUT (16:9, clean grid, every view the same car at the same scale):
Top row: front view, front three-quarter (left), left side profile, rear three-quarter (right).
Bottom row: rear view, right side profile, then close-ups of: the TRD front lip with its LED strip and the mesh grille and fog light; one wheel and tyre; the tailgate badges (Toyota hybrid emblem, C-HR, HYBRID); the TRD roof wing.
No labels, no text, no arrows, no borders with writing.

BACKGROUND AND LIGHTING: solid light grey background (#DCDCDC), even soft studio lighting, near-shadowless with only a soft contact shadow under each tyre, no gradients, no coloured light, no environment reflections other than a clean soft studio softbox reflection on the paint.

REALISM: real automotive studio photography, not CGI and not a render. Real paint depth and micro texture, real rubber texture on the tyres, real plastic grain on the trims, crisp panel gaps, true-to-life colour.

CAMERA: Canon EOS R5, RF 100mm f/2.8L Macro for close-ups and RF 70-200mm f/8 for full views, ISO 100, edge-to-edge sharpness, true-to-life colour profile.

FINAL RESULT: an ultra-realistic, perfectly sharp 4K studio reference sheet of this exact black C-HR Hybrid with its TRD kit, black wheels, badges, decals and stickers, freshly detailed for sale, with no chalk marks, no dirt and empty plate areas.
```
