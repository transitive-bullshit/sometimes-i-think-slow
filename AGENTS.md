# AGENTS.md

"Sometimes I Think Slow", an AI-made hip-hop parody music video about fast (System 1) and slow (System 2) thinking in AI models. It's published on YouTube (https://www.youtube.com/watch?v=dZjYGcjS3iQ), with a write-up at https://www.transitivebullsh.it/projects/sometimes-i-think-slow-ai-music-video. This repo is a working directory of scripts, prompts, and data, not a package. For setup, commands, and a step-by-step map, see `contributing.md`.

## Mental model

```text
suno/ lyrics → song (Suno, external) → scripts/suno_transcribe.py → analysis/suno/lyrics-timed.json
→ scripts/storyboard_shots.py → scripts/storyboard.py → video/storyboard/shots.json + keyframes (fal)
→ scripts/render_shots.py → video/clips/<model>/ (Kling 3 Pro for color, Wan 3.0 for SLOW's ink wash)
→ scripts/compose.py → video/out/fast-and-slow.mp4
→ scripts/review_build.py → video/review/ (the user's notes land in video/review/feedback.json) → keyframe_fix.py / rerender_fix.py → repeat
```

## Edit sources, not outputs

- **Shots:** edit `scripts/storyboard_shots.py`, then run `scripts/storyboard.py data`. Don't hand-edit `shots.json`; a test fails if it drifts.
- **Lyrics and timing:** `analysis/suno/lyrics-timed.json` holds both spellings: the phonetic one Suno sang (`suno_text`) and the real one captions show (`text`).
- **Per-shot render tweaks:** the dicts at the top of `scripts/compose.py` (`TRIM`, `FIT`, `PATCH`, `STAMP_AT`, `HOOK_Y`, `MONO`).
- **Review rounds:** `ROUND` and `UPDATED` in `scripts/review_build.py`; redo jobs in `scripts/keyframe_fix.py` and `scripts/rerender_fix.py`.

## Costs and side effects

- **Paid APIs:** every generating script calls fal. Ask before batch runs, and regenerate only the shots in question. Scripts skip existing outputs: move a file aside to redo it, and keep the old take for the review page's compare toggle.
- **Receipts:** every paid call writes its prompt and parameters as JSON next to its output, with repo-relative paths. Keep it that way.
- **The public site:** `scripts/publish_notion.py publish` writes to the user's website CMS (the Notion Projects database). Only run it when asked; it creates a draft and refuses to duplicate an existing slug.
- **Keys:** they come from `.env` (see `.env.example`). Never print them.

## Not in git

- **A fresh clone has no media:** no audio, keyframes, clips, or renders. `.gitignore` blocks media everywhere except the README's WebP images in `media/`. `scripts/media_backup.py download` restores it all from R2 using `media/backup.json`; after new renders, run `upload` (ask first: it writes to the user's shared production bucket) and commit the updated manifest.
- **Copyright:** the original song was only inspiration and a reference for the writing. Never commit its audio or lyrics. `scripts/vocal_map.py` writes its raw transcript to `$SCRATCH`, outside the repo.
- **Kept local on purpose:** the pre-Suno audio experiments and their research (listed in `.gitignore`). Leave them out.
- **Private:** `research/notion-research.md` and `research/x-archive-references.md` come from the user's own Notion and X archive, and stay out.
- **Where docs go:** `readme.md` is a marketing page. Technical docs go in `contributing.md`.

## Conventions that held up

- **Real people appear only as in-world text** (a pager, a CRT, a newspaper, a book cover), never as likenesses.
- **Captions are composited, never generated.** Video models garble text: pin the keyframe as Kling's end frame, or paste the region back from the keyframe.
- **Check the last second of every clip.** That's where characters drift off-model; use the clean part, fitted to the shot.
- **No lip-sync.** The user cut it; the default cut is the only cut.
- **MLX and PyTorch-MPS in one process can deadlock**, so Whisper runs in its own subprocess.

## Checks

`uv run pytest` runs offline in a few seconds, and CI runs the same thing. `uv sync` makes `.venv` match `uv.lock` and drops optional groups you didn't ask for; `uv sync --all-groups` keeps everything.
