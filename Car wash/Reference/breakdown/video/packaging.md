---
videomd: 1
part: packaging
tokens: 761
---

## Packaging layer (subtitles / styled text / stickers / sound-effect hits)

- styled text ×4 (large size, tilted, multi-colour / gradient, red fill): "CERAM", "NASIOL", "PRO", "AGACERAMIC"
- text label ×11 (3 of them follow an object): "A", "NASISI", "NASAS", "75 40 R2", "ERAMIC", "AGACERAMIC" …
- Exports: `packaging/overlays.ass`, `packaging/timeline.json` (SRT is the subtitle timeline; ASS carries colour, outline, position and entrance animation, swap in the original font; timeline.json is the full timeline)

**text timeline (15 rows)**

| Time | Kind | Text | Style | In / out | SFX |
|---|---|---|---|---|---|
| 1.80–2.30s | text label | A | grey text, line height 11.9% (about 229px) | hard in / hard out | — |
| 2.50–2.60s | text label | NASISI | black text, line height 3.0% (about 59px) | hard in / hard out | — |
| 3.00–4.10s | styled text | CERAM | white text, grey outline, line height 9.2% (about 177px) | hard in / fade out | — |
| 4.00–4.10s | text label | NASAS | black text, keywords highlighted in grey, line height 1.3% (about 26px) | hard in / hard out | — |
| 4.50–5.10s | styled text | NASIOL | black text, keywords highlighted in grey, line height 2.3% (about 43px) | type-on / hard out | — |
| 4.50–4.90s | text label | 75 ⏎ 40 R2 | black text, line height 1.9% (about 36px) | hard in / fade out | — |
| 5.80–7.20s | text label | ERAMIC | white text, grey outline, keywords highlighted in red, line height 10.7% (about 205px) | hard in / fade out | — |
| 6.00–7.10s | styled text | PRO | red text, keywords highlighted in red, line height 4.1% (about 79px) | fade in / fade out | — |
| 7.30–13.60s | text label · follows an object | AGACERAMIC | white text, grey outline, grey box, keywords highlighted in red, line height 20.6% (about 396px) | hard in / fade out (bounces / changes colour midway) | — |
| 15.30–15.60s | text label | 00 | grey text, line height 2.9% (about 55px) | hard in / hard out | — |
| 16.50–17.90s | text label · follows an object | AGACERAMIC | white text, grey outline, keywords highlighted in red, line height 21.6% (about 414px) | fade in / fade out | — |
| 16.50–19.10s | text label · follows an object | PRO | red text, red outline, line height 5.2% (about 100px) | slide in / fade out (bounces / changes colour midway) | — |
| 18.00–19.10s | styled text | AGACERAMIC | white text, grey outline, grey box, keywords highlighted in red, line height 21.0% (about 404px) | fade in / hard out | — |
| 26.50–27.10s | text label | PRO | red text, red outline, line height 3.4% (about 65px) | fade in / fade out | — |
| 27.50–28.10s | text label | ORO | red text, red outline, keywords highlighted in red, line height 3.4% (about 65px) | fade in / fade out | — |

Remake: burn subtitles and styled text in with `packaging/overlays.ass` (ffmpeg -vf ass=overlays.ass), or rebuild them from timeline.json in CapCut / Remotion; stickers and GIFs need matching assets (meme / GIF libraries), crops are under packaging/.
