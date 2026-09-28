"""Offline smoke tests: the storyboard data, the shot timeline, and the compositor's captions run on the committed data.

No media, no API keys, no network. Paid generation (fal) and the full render, which needs the Suno track, keyframes
and clips, are deliberately not exercised.
"""
import json
import pathlib
import sys

import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SONG_END = 182.4


def committed_shots():
    return json.loads((ROOT / "video/storyboard/shots.json").read_text())["shots"]


def test_shots_json_is_up_to_date():
    """video/storyboard/shots.json is exactly what scripts/storyboard.py builds from the shot list and the timed lyrics."""
    import storyboard

    fresh = json.loads(json.dumps(storyboard.shots_data()))
    committed = json.loads((ROOT / "video/storyboard/shots.json").read_text())
    assert fresh == committed, "shots.json is stale: run `uv run python scripts/storyboard.py data` and commit it"


def test_shots_tile_the_song():
    shots = committed_shots()
    assert shots[0]["start"] == 0 and abs(shots[-1]["end"] - SONG_END) < 1e-6
    for a, b in zip(shots, shots[1:]):
        assert a["dur"] > 0, a["id"]
        assert abs(a["end"] - b["start"]) < 1e-6, f"gap or overlap between {a['id']} and {b['id']}"
    ids = [s["id"] for s in shots]
    assert len(set(ids)) == len(ids) == 66


def test_every_animated_shot_has_a_receipt():
    """Every shot a video model animated has its prompt and parameters on file (the intro, card and end card are drawn locally)."""
    local = {"S01", "S66"}
    missing = [s["id"] for s in committed_shots() if not s.get("card") and s["id"] not in local
               and not any((ROOT / "video/clips" / m / f"{s['id']}.json").exists() for m in ("kling3pro", "wan3"))]
    assert not missing, f"no clip receipt for {missing}"


def test_media_backup_covers_the_render():
    """media/backup.json has every file scripts/compose.py reads that isn't in git, so a clone can restore and re-render."""
    files = json.loads((ROOT / "media/backup.json").read_text())["files"]
    backed = {e["path"] for e in files}
    needed = {"audio/suno/final-take.wav", "video/poster.png", "video/storyboard/frames/S01.png",
              "video/storyboard/frames/S36.png", "video/storyboard/frames/S39.png"}
    for s in committed_shots():
        if s.get("card") or s["id"] in {"S01", "S36", "S66"}:      # the card is drawn; the rest are built from stills
            continue
        model = "kling3pro" if (ROOT / f"video/clips/kling3pro/{s['id']}.json").exists() else "wan3"   # compose's order
        needed.add(f"video/clips/{model}/{s['id']}.mp4")
    assert not needed - backed, f"not in the media backup: {sorted(needed - backed)}"
    for e in files:
        assert e["bytes"] > 0 and len(e["sha256"]) == 64 and e["url"].endswith(e["sha256"] + pathlib.Path(e["path"]).suffix.lower())


def test_captions_use_display_spellings():
    """Captions show real names, not the phonetic spellings Suno needed to sing them."""
    text = " ".join(c["text"] for s in committed_shots() for c in s["captions"])
    for name in ("Andrej", "Kahneman", "Gary Marcus", "Navier–Stokes"):
        assert name in text, name


def test_every_caption_renders():
    """Every caption in the song draws with the committed fonts and word timings, fully written on."""
    import compose

    drawn = 0
    for s in compose.SHOTS:
        for i, c in enumerate(s["captions"]):
            if c["end"] - c["start"] < 0.05:        # the compositor drops zero-length lines too
                continue
            img = Image.new("RGBA", (compose.W, compose.H), (0, 0, 0, 0))
            compose.render_caption(img, c, c["end"] + 0.3, s["id"], i)
            assert np.asarray(img)[..., 3].any(), f"{s['id']} caption {i} drew nothing"
            drawn += 1
    assert drawn >= 70, drawn         # 72 sung lines on screen, from the intro hook to the spoken tag


def test_grades_and_tape_overlays():
    import compose

    frame = np.full((compose.H, compose.W, 3), 128, np.uint8)
    for mode in ("hook", "fast", "slow", "sunrise", "transition"):
        out = compose.grade(frame, mode, 0, False)
        assert out.shape == frame.shape and out.dtype == np.uint8
    shots = {s["id"]: s for s in compose.SHOTS}
    for sid, t in (("S01", 0.5), ("S47", shots["S47"]["start"] + 0.5), ("S66", shots["S66"]["end"] - 1.0)):
        img = Image.new("RGBA", (compose.W, compose.H), (0, 0, 0, 0))
        compose.osd(img, shots[sid], t)
        assert np.asarray(img)[..., 3].any(), f"no on-screen display drawn for {sid}"
