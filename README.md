# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ketong112/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ketong112/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Sum up 23 November's world news in one image: a 1024x1024 newspaper front page drawn with Pillow. The lead story is COP31 ending without a deal in Antalya; the featured stories are Ukraine's sea-drone strike on a Russian ship off Libya, Nvidia bringing back Jensen Huang, and the EU's 22nd round of Russia sanctions — plus 31 more stories from every continent, all reported on Monday 23 November 2026.

`draw_image.py` renders `entry.png` from scratch (deterministic: two runs write byte-identical files). `main.py` copies that image to `/output/entry.png`; it is standard-library only and runs with `python3 -P -s`.

## Run it

```sh
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=n394v5cd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
