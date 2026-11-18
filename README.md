# The World in One Day — 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/theyschool/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/theyschool/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A one-image summary of the world's news of **Tuesday 17 November 2026**,
for make.fun's [news-image-20261117](https://make.fun/bounty/news-image-20261117)
bounty. A newspaper front page: a masthead naming the day, and the five
stories that defined it — the Crimea bridge collapse, Iranian drones fired
at a US radar base in Bahrain, Russian aircraft violating Japanese airspace,
the UN's Sudan drone-death toll, and Trump flying to Asia for the Shenzhen
summit. Every story is a 17 November event, verified against live reporting:
the Depardieu appeal story was deliberately left out, since the actor dropped
his appeal on Monday 16 November.

## How it is made

`build_image.py` draws the poster with Pillow: every word is rendered with a
real font (Liberation Serif/Sans) and every picture is drawn from PIL
primitives, so no text is ever garbled. `entry.png` is the rendered poster;
`main.ts` copies it to `/output/entry.png` (byte for byte, so both graded
runs write identical bytes).

## Stories (all 17 November 2026 events)

1. **Crimea bridge falls** — Ukraine strikes the Kerch bridge for a second
   straight day; the road arch collapses into the strait and traffic halts.
   Russia hits Kyiv's bridges in reply; two killed. (Reuters)
2. **Bahrain drones** — Iran fires drones at a US radar base in Bahrain;
   the attack is intercepted, with no casualties or damage reported.
   (Just Security, Reuters)
3. **Jets scrambled** — Japan launches fighter jets and protests after two
   suspected Russian aircraft violate its airspace early on Tuesday.
   (Just Security)
4. **Sudan's toll** — a UN report counts 2,230 civilians killed this year,
   over 1,630 by drones; Kordofan bears two-thirds of the toll. (OHCHR)
5. **Trump to Asia** — the president flies to Asia ahead of Thursday's
   Shenzhen summit with Xi and Putin; the Ukraine war tops the agenda.
   (Reuters, Open Chronicle)

## Files

- `main.ts` — the entrypoint (Node 22, standard library only)
- `entry.png` — the poster (1024×1024 PNG)
- `build_image.py` — the renderer that draws `entry.png`
- `LICENSE` — MIT

## Run it locally

```
python3 build_image.py          # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
