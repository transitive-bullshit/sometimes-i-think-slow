# Contributing

This repo is the full working directory behind “Sometimes I Think Slow”, an AI-made music-video parody: the pipeline code, every prompt, the shot list and lyric timings, the review tools, and a receipt for every paid generation. This doc covers how to run it, where things live, and what’s deliberately left out.

## Setup

You’ll need [uv](https://docs.astral.sh/uv/), `ffmpeg` (`brew install ffmpeg`), and a [fal](https://fal.ai) API key. It was built on an Apple Silicon Mac with Python 3.12.

```bash
uv sync                              # the video pipeline
uv sync --group timing               # + the beat grid, word timings, and vocal stem for the Suno take (beat_this, mlx-whisper, audio-separator)
uv sync --all-groups                 # + the song-anatomy analysis and the R2 backup uploader
cp .env.example .env                 # then fill in FAL_KEY (the other variables are only for the analysis and the backup upload)
```

Run scripts with `uv run --env-file .env python scripts/<script>.py`. uv makes `.venv` match `uv.lock` exactly, so a plain `uv sync` removes the optional groups and anything you installed by hand. Use `uv export --no-hashes --no-emit-project > requirements.txt` if you’d rather use pip.

## The pipeline

Two inputs aren’t in git: the Suno take at `audio/suno/final-take.wav`, and the approved poster at `video/poster.png` (it’s frame 0 and the end card). The keyframes and clips aren’t either, but everything that made them is, and all of it is [backed up on R2](#media-backup).

```bash
uv run --group timing python scripts/suno_transcribe.py                   # beat grid, vocal stem, Whisper words, aligned lyrics -> analysis/suno/
uv run python scripts/storyboard.py data                                  # shot list + timed captions -> video/storyboard/shots.json
uv run --env-file .env python scripts/storyboard.py frames                # one keyframe per shot on fal (~$0.15 each)
uv run --env-file .env python scripts/render_shots.py kling3pro <ids...>  # hook, FAST, and sunrise shots (~$0.14/s)
uv run --env-file .env python scripts/render_shots.py wan3 <ids...>       # SLOW's sumi-e shots (~$0.05/s)
uv run python scripts/compose.py                                          # the cut -> video/out/fast-and-slow.mp4 (~8 min)
uv run python scripts/review_build.py                                     # scene clips + review.json for the review page
uv run python scripts/serve.py .                                          # http://localhost:8765/video/review/index.html
```

Every generating script skips outputs that already exist, so each step is safe to re-run, and every paid call writes its prompt and parameters next to its output. A full pass of keyframes and clips costs roughly $35 on fal. `compose.py --from 60 --to 90 --out /tmp/test.mp4` renders a slice for quick checks.

### Where each step lives

| Step | Code | Output |
|---|---|---|
| Reference analysis of the original | [`scripts/beats.py`](scripts/beats.py), [`scripts/grid.py`](scripts/grid.py), [`scripts/vocal_map.py`](scripts/vocal_map.py) | [`docs/01-song-anatomy.md`](docs/01-song-anatomy.md), `analysis/*-original.json` |
| Lyrics | [`drafts/lyrics-v2.md`](drafts/lyrics-v2.md), [`suno/lyrics-v3-display.txt`](suno/lyrics-v3-display.txt) | |
| Song (Suno V6) | [`suno/README.md`](suno/README.md), [`suno/lyrics-v3-suno.txt`](suno/lyrics-v3-suno.txt) | `audio/suno/final-take.wav` (not in git) |
| Timing | [`scripts/suno_transcribe.py`](scripts/suno_transcribe.py) (with `beats.py` and `grid.py`) | [`analysis/suno/`](analysis/suno/) |
| Look and characters | [`scripts/concept_art.py`](scripts/concept_art.py), [`scripts/art_direction_v2.py`](scripts/art_direction_v2.py) | `video/concept/` |
| Storyboard | [`scripts/storyboard_shots.py`](scripts/storyboard_shots.py) → [`scripts/storyboard.py`](scripts/storyboard.py) | [`video/storyboard/shots.json`](video/storyboard/shots.json), `video/storyboard/frames/` |
| Clips | [`scripts/render_shots.py`](scripts/render_shots.py) | `video/clips/<model>/` |
| Review redos | [`scripts/keyframe_fix.py`](scripts/keyframe_fix.py), [`scripts/rerender_fix.py`](scripts/rerender_fix.py) | `video/storyboard/frames_r2/`, `video/clips/kling3pro_alt/` |
| Captions, grades, render | [`scripts/compose.py`](scripts/compose.py), [`video/fonts/`](video/fonts/README.md) | `video/out/` |
| Review | [`scripts/review_build.py`](scripts/review_build.py), [`video/review/index.html`](video/review/index.html), [`scripts/serve.py`](scripts/serve.py) | [`video/review/feedback.json`](video/review/feedback.json) |
| Lip-sync (cut) | [`scripts/lipsync.py`](scripts/lipsync.py) | `video/clips/omnihuman/` |

`storyboard_shots.py` is the single source of truth for shots: start times, modes, scenes, camera, motion, and in-world text. `shots.json` is generated from it and the timed lyrics, and a test fails if the two drift.

### Redoing a single shot

This is how every review round worked:

1. Leave a note on the shot in the review page. It lands in `video/review/feedback.json`.
2. If the composition has to change, add an edit to `scripts/keyframe_fix.py` (a Nano Banana Pro edit of the approved frame, ~$0.15 a try) and run it. Copy the best try to `video/storyboard/frames_r2/<name>.png`.
3. Add a job to `scripts/rerender_fix.py` with the motion prompt, duration, start frame, and an optional end frame, and run it (~$0.40–$0.85 a take). Pin an end frame when text or an action has to land.
4. Keep the old clip as `video/clips/kling3pro_alt/<id>_r1.mp4`, then copy the chosen take to `video/clips/kling3pro/<id>.mp4`.
5. Per-shot playback tweaks live at the top of `compose.py`: `TRIM` and `FIT` for timing, `PATCH` for pasting keyframe regions back, `STAMP_AT` and `HOOK_Y` for caption placement.
6. Re-render, bump `ROUND` and `UPDATED` in `review_build.py`, and rebuild the review page. It shows the updated shots first, with a toggle to compare against the previous render.

## Media backup

Everything the render needs that isn’t in git is backed up on Cloudflare R2: the Suno take, the poster, the model sheets and style frames, every keyframe and clip (including the takes that lost), and a share encode of the final cut, about 2.1 GB. The multi-GB master isn’t backed up: `compose.py` rebuilds it from the clips. [`media/backup.json`](media/backup.json) lists each file’s path, public URL, size, and SHA-256. Files are stored under content-addressed keys, so a URL never changes what it points to.

```bash
uv run python scripts/media_backup.py download             # restore everything into place (no credentials needed)
uv run python scripts/media_backup.py download video/out   # or just part of it, by path prefix
uv run python scripts/media_backup.py verify               # compare local files with the manifest
uv run --group backup --env-file .env python scripts/media_backup.py upload   # after new renders; needs the S3_* variables
```

The ones you’ll want most:

- [The final cut](https://assets.cultural-alignment.com/sometimes-i-think-slow/dbaeec4dc994878587b0a3cd42e5837560504bc8229161a049931f10103d22f9.mp4) (`video/out/fast-and-slow_share.mp4`, 1080p24, 3:02)
- [The Suno take](https://assets.cultural-alignment.com/sometimes-i-think-slow/7f90d68cc0d66f9118eb1bba4904a9ded3a51128f74f3de0f99c93b46ff50c14.wav) (`audio/suno/final-take.wav`)
- [The poster](https://assets.cultural-alignment.com/sometimes-i-think-slow/9572e50a2eb7152dcd0ab1de6388b9ef57c63ba070c8402fcbbc654eb4847c93.png) (`video/poster.png`, full resolution)

After an upload, commit the updated manifest.

## Tests

```bash
uv run pytest
```

The smoke tests in [`tests/`](tests/) run offline in a few seconds. They check that `shots.json` matches its generator, that the shots tile the song with no gaps, that every animated shot has a receipt, that captions use real names rather than Suno’s phonetic spellings, that every caption, grade, and tape overlay renders with the committed fonts, and that the media backup covers every file the render reads. [CI](.github/workflows/test.yml) runs them on every push, along with a compile check of every Python file. It installs only the core dependencies, has no secrets, and never calls fal or any other API.

## What’s in the repo

```text
scripts/               the whole pipeline (see the table above), the song analysis, and the media backup
suno/                  the Suno package: style prompts, tagged lyrics with phonetic names, display lyrics
drafts/                lyric drafts
docs/                  song anatomy (numbers only, no original lyrics) and creative direction
research/              the AI "thinking fast and slow" timeline and the song and cognitive-science background
analysis/              the original's beat grid and line timings (numbers only); analysis/suno/ for our take
video/storyboard/      shots.json, the storyboard review page, and a receipt for every keyframe
video/concept/         receipts for the style frames and character sheets
video/clips/           a receipt for every clip: model, prompt, and parameters
video/review/          the scene review page and my feedback on each render
video/fonts/           the caption fonts (OFL and Apache licensed)
media/                 the README's featured image, and backup.json: the R2 manifest for all the media
tests/                 offline smoke tests
```

`video/art-direction.html`, `video/storyboard/index.html`, and `video/review/index.html` show media that isn’t in git, so they only work locally.

## What’s not in the repo, on purpose

- **The original song.** It was our inspiration and the reference for the writing: its form, tempo, key, and feel. It’s copyrighted and not mine to redistribute, so none of its audio or lyrics are here. The song in the video was generated fresh in Suno, and everything after that is independent of the original.
- **Media** (the Suno take, keyframes, clips, and renders). It’s backed up on R2 (see [Media backup](#media-backup)), and most of it can be regenerated from `shots.json` and the receipts, at a cost.
- **Model weights and environments:** `.venv` and audio-separator’s weights (downloaded on demand into `audio/models/`).
- **Private research:** notes built from my own Notion workspace and X archive.

`.gitignore` blocks media files everywhere; `media/poster.webp` is the one exception. For another deliberate exception, use `git add -f`.
