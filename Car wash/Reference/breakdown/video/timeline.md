---
videomd: 1
part: timeline
shots: 20
tokens: 1196
---

# Timeline

One shot per line: `#<n> start-end (s) | key value | …`. A key ending in `~` is the tools' inference; keys without it are visible on screen or measured directly.
`story` job in the story and the point · `seen` what is on screen · `act` acting (emotion, strength, face) · `camera` camera move · `overlay` overlays · `made~` how it was made (inferred) · `material~` where the material came from (inferred) · `remake` remake route · `flag` needs a second look
Full detail for a shot is in `video/shots/<n>.md` (e.g. `video/shots/07.md`).

```videomd-timeline
#01 0.0-1.6 | camera smooth move | made~ code / template render 50% · runner-up 3D render 23% | material~ rendered by the creator | remake code render · Part 1 | flag low confidence
#02 1.6-3.0 | camera smooth move | overlay subtitle | made~ live action 55% · runner-up AI-generated video 32% | material~ the user's real material (own footage or… | remake reshoot · S1 | flag low confidence
#03 3.0-4.5 | camera smooth move | overlay text, graphic, styled text | made~ live action 51% · runner-up AI-generated video 34% | material~ the user's real material (own footage or… | remake reshoot · S1 | flag low confidence
#04 4.5-5.8 | camera smooth move | overlay subtitle, text, graphic, styled text | made~ AI-generated video 42% · runner-up live action 41% | material~ AI-generated | remake AI generation · G1 | flag low confidence,to confirm
#05 5.8-7.3 | camera smooth move | transition jump cut | overlay styled text | made~ live action 46% · runner-up AI-generated video 38% | material~ the user's real material (own footage or… | remake reshoot · S1 | flag low confidence
#06 7.3-9.5 | camera smooth move | overlay subtitle | made~ 3D render 31% · runner-up AI-generated video 22% | material~ rendered by the creator | remake AI generation / 3D render · G2 | flag low confidence
#07 9.5-10.9 | camera smooth move | transition jump cut | overlay text | made~ 3D render 31% · runner-up AI-generated video 28% | material~ rendered by the creator | remake AI generation / 3D render · G2 | flag low confidence
#08 10.9-12.4 | camera smooth move | made~ 3D render 50% · runner-up code / template render 24% | material~ rendered by the creator | remake AI generation / 3D render · G2 | flag low confidence
#09 12.4-13.8 | camera smooth move | transition jump cut | overlay subtitle | made~ 3D render 54% · runner-up AI-generated video 14% | material~ rendered by the creator | remake AI generation / 3D render · G2 | flag low confidence
#10 13.8-15.3 | camera smooth move | made~ AI-generated video 49% · runner-up live action 38% | material~ AI-generated | remake AI generation · G2 | flag low confidence,to confirm
#11 15.3-16.7 | camera smooth move | transition jump cut | made~ live action 45% · runner-up AI-generated video 42% | material~ the user's real material (own footage or… | remake reshoot · S1 | flag low confidence
#12 16.7-18.1 | camera smooth move | overlay styled text | made~ 3D render 33% · runner-up live action 25% | material~ rendered by the creator | remake AI generation / 3D render · G3 | flag low confidence
#13 18.1-19.6 | camera smooth move | transition jump cut | overlay subtitle, styled text | made~ live action 41% · runner-up AI-generated video 35% | material~ the user's real material (own footage or… | remake reshoot · S1 | flag low confidence
#14 19.6-21.0 | camera smooth move | made~ code / template render 41% · runner-up live action 26% | material~ rendered by the creator | remake code render · Part 2 | flag low confidence
#15 21.0-22.4 | camera smooth move | made~ code / template render 34% · runner-up 3D render 27% | material~ rendered by the creator; real or not, to… | remake code render · Part 2 | flag low confidence
#16 22.4-23.9 | camera smooth move | made~ code / template render 63% · runner-up 3D render 20% | material~ rendered by the creator | remake code render · Part 2
#17 23.9-25.3 | camera smooth move | made~ code / template render 57% · runner-up 3D render 22% | material~ rendered by the creator | remake code render · Part 2 | flag low confidence
#18 25.3-26.7 | camera smooth move | made~ code / template render 72% · runner-up 3D render 16% | material~ rendered by the creator; real or not, to… | remake code render · Part 2
#19 26.7-28.3 | camera smooth move | overlay subtitle | made~ 3D render 37% · runner-up live action 22% | material~ rendered by the creator | remake AI generation / 3D render · G4 | flag low confidence
#20 28.3-30.1 | camera smooth move | made~ code / template render 52% · runner-up screen recording / screenshot 17% | material~ rendered by the creator | remake code render · Part 3 | flag low confidence
```
