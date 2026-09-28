# Fonts

The compositor ([`scripts/compose.py`](../../scripts/compose.py)) draws every caption with these Google Fonts. They're
redistributable, so they live in git. Each file carries its license in its metadata.

| File | Font | Used for | License | Source |
|---|---|---|---|---|
| `PermanentMarker-Regular.ttf` | Permanent Marker | FAST's spray-tag captions | Apache 2.0 | [google/fonts](https://github.com/google/fonts/tree/main/apache/permanentmarker) |
| `Caveat[wght].ttf` | Caveat (variable, drawn at weight 700) | SLOW's handwriting | SIL OFL 1.1 | [google/fonts](https://github.com/google/fonts/tree/main/ofl/caveat) |
| `Bungee-Regular.ttf` | Bungee | the hook's sign lettering | SIL OFL 1.1 | [google/fonts](https://github.com/google/fonts/tree/main/ofl/bungee) |
| `SpecialElite-Regular.ttf` | Special Elite | the FAST stamps, the typewriter breaks and tag card, the VCR on-screen display | Apache 2.0 | [google/fonts](https://github.com/google/fonts/tree/main/apache/specialelite) |

Special Elite has no ▶, ■ or █ glyphs, so `compose.py` draws those as shapes.
