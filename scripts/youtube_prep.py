"""Build the YouTube upload package in video/out/youtube/: a 4K upload of the final cut, the lyrics as English captions,
the thumbnail, and details.md with the title, description, and every upload setting in YouTube Studio's order.

The upload is the master upscaled to 2160p. YouTube gives 4K uploads its higher-bitrate VP9/AV1 encodes at every size,
while a 1080p upload gets H.264 at a few Mbps, which smears the VHS grain. The frames are resized, never color-converted:
the master is untagged and players show it as BT.709, so the upload is tagged BT.709 to look the same. The audio is
encoded from the Suno WAV at YouTube's recommended 384 kbps.

The captions follow Slow It Down's: one cue per sung line, from just before its first word to just after its last, never
overlapping, wrapped at 42 characters per row, and marked with ♪ (the spoken tag at the end isn't). The stretched
"slooow" is normalized, and the one zero-length line the aligner estimated is dropped, as in the burned-in captions.

There's no `publish`: uploads through the YouTube API from an unaudited Google Cloud project are locked private. Drag the
video into YouTube Studio and fill in the rest from details.md.

usage: youtube_prep.py    (the video is skipped if it exists; delete it to rebuild)
"""
import json, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "video/out/youtube"
MASTER = ROOT / "video/out/fast-and-slow.mp4"
SONG = ROOT / "audio/suno/final-take.wav"
NAME = "sometimes-i-think-slow"
LEAD_IN, HOLD, MIN_CUE, ROW = 0.15, 0.35, 1.0, 42   # s before the first word, s after the last, shortest cue, chars per row

PUBLISHED = "https://www.youtube.com/watch?v=dZjYGcjS3iQ"     # the title and description as published, 2026-09-28
TITLE = "Sometimes I Think Slow, Sometimes I Think Fast"
WRITEUP = "https://www.transitivebullsh.it/projects/sometimes-i-think-slow-ai-music-video"
REPO = "https://github.com/transitive-bullshit/sometimes-i-think-slow"
ORIGINAL_YT = "https://www.youtube.com/watch?v=dkl_Vq1SWKg"
SLOW_IT_DOWN_YT = "https://www.youtube.com/watch?v=Tz6gQDN9qG0"
DESCRIPTION = f"""AI remix of the 1991 classic "Sometimes I Rhyme Slow" by Nice & Smooth.

AI models think two ways now: fast, in one forward pass, and slow, reasoning at test time, so I had Claude Code (Opus 5.5) turn it into an AI parody that also pays homage to the original lyricists who were so far ahead of their time.

• FAST is System 1: he answers before you finish asking
• SLOW is System 2: he takes three minutes and gets it right
• FAST's verse is saturated 90s color; SLOW's is sumi-e ink wash
• Karpathy on a pager, Kahneman on a book cover, and Gary Marcus in the headlines
• made almost entirely with Claude Code, Suno, and fal in about a day

Write-up and how it was made: {WRITEUP}
Code (MIT): {REPO}
The original: {ORIGINAL_YT}
Previously, Slow It Down: {SLOW_IT_DOWN_YT}

A parody, not affiliated with Nice & Smooth, any AI lab, or anyone it name-checks. The original song belongs to its owners."""

# ---------------------------------------------------------------- captions
def cues():
    """One cue per timed line, handed over at the next line's lead-in without cutting the current line's last word short."""
    out = []
    for ln in json.loads((ROOT / "analysis/suno/lyrics-timed.json").read_text())["lines"]:
        if ln["end"] - ln["start"] < 0.05:                   # estimated, never sung on its own (the compositor drops it too)
            continue
        out.append(dict(w0=ln["start"], w1=ln["end"], start=ln["start"] - LEAD_IN, end=ln["end"] + HOLD,
                        text=re.sub(r"\b([Ss])lo+w", r"\1low", ln["text"]), sung=ln["section"] != "Spoken"))
    for a, b in zip(out, out[1:]):
        cut = min(max(b["start"], a["w1"]), b["w0"])
        a["end"], b["start"] = min(a["end"], cut), max(b["start"], cut)
    for a, b in zip(out, out[1:]):                           # give quick lines a readable minimum where the gaps allow:
        a["end"] = max(a["end"], min(a["start"] + MIN_CUE, b["start"]))           # hold into the gap after,
    for a, b in zip(out, out[1:]):
        b["start"] = min(b["start"], max(a["end"], b["end"] - MIN_CUE))           # else start earlier in the gap before
    out[0]["start"] = max(0.0, out[0]["start"])
    out[-1]["end"] = max(out[-1]["end"], out[-1]["start"] + 2.0)   # the spoken tag, over the end card
    return out

def wrap(text):
    """One row, or two: split at punctuation when that fits and isn't lopsided, else at the space that balances them best.
    A split outside a quotation beats one inside it."""
    if len(text) <= ROW:
        return [text]
    rows = lambda i: [text[:i].rstrip(), text[i:].lstrip()]
    fits = lambda r: max(map(len, r)) <= ROW and min(map(len, r)) >= max(map(len, r)) / 3
    punct = [rows(m.end()) for m in re.finditer(r"[,.?!:] ", text)]
    return min([r for r in punct if fits(r)] or [rows(m.start()) for m in re.finditer(" ", text)],
               key=lambda r: (max(map(len, r)) > ROW, r[0].count('"') % 2, max(map(len, r))))

def srt_time(t):
    ms = round(t * 1000)
    return f"{ms // 3_600_000:02d}:{ms // 60_000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"

def srt(cs):
    blocks = []
    for n, c in enumerate(cs, 1):
        rows = wrap(c["text"])
        if c["sung"]:
            rows[0] = "♪ " + rows[0]
            rows[-1] += " ♪"
        blocks.append(f"{n}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n" + "\n".join(rows) + "\n")
    return "\n".join(blocks)

# ---------------------------------------------------------------- media
def thumbnail():
    from PIL import Image, ImageOps
    im = ImageOps.fit(Image.open(ROOT / "video/poster.png").convert("RGB"), (1280, 720), Image.LANCZOS)
    im.save(OUT / "thumbnail.jpg", quality=90, optimize=True, progressive=True)
    return OUT / "thumbnail.jpg"

def upload_video():
    out = OUT / f"{NAME}.mp4"
    if out.exists():
        return out
    part = out.with_suffix(".part.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-stats", "-y", "-i", str(MASTER), "-i", str(SONG), "-map", "0:v", "-map", "1:a",
                    "-vf", "setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv,"
                           "scale=3840:2160:flags=lanczos+accurate_rnd+full_chroma_int",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
                    "-g", "12", "-bf", "2", "-flags", "+cgop",    # YouTube's advice: a closed GOP of half the frame rate
                    "-c:a", "aac", "-b:a", "384k", "-ar", "48000", "-movflags", "+faststart", "-shortest", str(part)], check=True)
    part.rename(out)
    return out

# ---------------------------------------------------------------- details
def details(video, captions, thumb):
    mb = lambda p: f"{p.stat().st_size / 1e6:,.0f} MB" if p.stat().st_size > 1e6 else f"{p.stat().st_size // 1000} KB"
    return f"""# YouTube upload: Sometimes I Think Slow

Published at {PUBLISHED}. Everything is in this folder. The settings copy Slow It Down's upload on the Transitive BS channel.

- **Video:** `{video.name}` ({mb(video) + "; " if video.exists() else ""}2160p24 H.264, AAC 384 kbps)
- **Captions:** `{captions.name}` (English, with timing)
- **Thumbnail:** `{thumb.name}` (the poster, 1280x720, {mb(thumb)})

## 1. Details

**Title** ({len(TITLE)}/100 characters)

```text
{TITLE}
```

**Description** ({len(DESCRIPTION)}/5,000 characters)

```text
{DESCRIPTION}
```

- **Thumbnail:** upload `{thumb.name}`
- **Audience:** No, it's not made for kids. No age restriction.
- **Show more:**
  - **Paid promotion:** No
  - **AI use:** Yes (the vocals and visuals are generated)
  - **Category:** Science & Technology
  - **Video language:** English

Everything else stays at its default, as on Slow It Down: no playlist or tags, automatic chapters, places, and concepts on,
Standard YouTube License, embedding on (the write-up can embed it), subscriptions feed on, remixing allowed, comments on.

## 2. Video elements

- **Subtitles:** Add, then Upload file, then With timing, then `{captions.name}`
- **End screen** (optional): the last ~12 seconds are the poster card, room for "Slow It Down" and Subscribe.

## 3. Checks

Wait for the copyright check. The song was made fresh in Suno, so no Content ID match is expected.

## 4. Visibility

Public, or scheduled. Before it goes public:

- Make {REPO} public (the description links it).
- Run the site's content sync so the write-up link resolves (until then {WRITEUP} is a 404).

After: add "▶ Watch on YouTube" to the README, as on Slow It Down's.
"""

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cs = cues()
    captions = OUT / f"{NAME}.en.srt"
    captions.write_text(srt(cs), encoding="utf-8")
    print(f"{captions.name}: {len(cs)} cues, {cs[0]['start']:.2f}s to {cs[-1]['end']:.2f}s")
    thumb = thumbnail()
    print(f"{thumb.name}: {thumb.stat().st_size // 1000} KB")
    video = upload_video()
    print(f"{video.name}: {video.stat().st_size / 1e6:,.0f} MB")
    (OUT / "details.md").write_text(details(video, captions, thumb), encoding="utf-8")
    print(f"details.md -> {OUT.relative_to(ROOT)}/")

if __name__ == "__main__":
    main()
