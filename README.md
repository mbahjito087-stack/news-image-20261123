# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/mbahjito087-stack/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/mbahjito087-stack/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up 23 November 2026 world news: COP31 climate talks collapse with no fossil-fuel deal, Houthi strikes hit a Saudi refinery, a Kyiv drone strike leaves 14 missing, and a ticker with the Benghazi warship hit, the Indonesia factory fire and the Lisbon cost-of-living march.

## Run it

```sh
python3 main.py
```

This copies `asset.jpg` to `/output/entry.png` (or to `$MAKEFUN_OUTPUT_DIR/entry.png`
when that variable is set) and prints the copied file's size and SHA-256 digest.
The rules accept JPEG bytes under the name `entry.png`. Verify the copy is
byte-identical to the source with:

```sh
sha256sum /output/entry.png asset.jpg
```

Both digests must match; the program itself also checks size and SHA-256 after
every copy and exits non-zero with a clear error if `asset.jpg` is missing,
empty, or not a JPEG file. Before copying it also verifies the image is
within the competition's caps (at most 1 MiB and 1024 by 1024 pixels) by
reading the JPEG dimensions from its SOF marker.

---

<sub>Entered on [make.fun](https://make.fun/?ref=2behakk4&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
