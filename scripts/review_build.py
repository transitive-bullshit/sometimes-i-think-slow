"""Build the scene-review page's data from the finished (no lip-sync) render.

Cuts every storyboard shot out of the render as its own clip (picture and song, frame-exact on the 24 fps grid the
compositor used), grabs a thumbnail, and writes video/review/review.json with each scene's lyrics, source and the fix
applied after clip QA. The page is video/review/index.html; feedback autosaves to video/review/feedback.json.
For a new review round, bump ROUND and list the reworked scenes in UPDATED: their previous clips move to clips/r<N-1>/
for the page's compare toggle, and the page resets just those scenes to unreviewed.

usage: review_build.py [render=video/out/fast-and-slow.mp4]
"""
import json, shutil, subprocess, sys, time, pathlib, concurrent.futures as cf

ROOT = pathlib.Path(__file__).resolve().parent.parent
RV = ROOT / "video/review"; CL = ROOT / "video/clips"
for d in (RV / "clips", RV / "thumbs"): d.mkdir(parents=True, exist_ok=True)
MASTER = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "video/out/fast-and-slow.mp4"
FPS = 24
SHOTS = json.load(open(ROOT / "video/storyboard/shots.json"))["shots"]

ROUND = 2
UPDATED = {  # round-1 scene review -> what changed (scripts/keyframe_fix.py, scripts/rerender_fix.py)
    "S02": "FAST skates the whole shot now: kick-off, carving, an ollie, and a kickflip on the way out. SLOW keeps reading.",
    "S03": "The crew are hype men now: on the hood, pumping their fists and shouting FAST on the beat, board waved overhead.",
    "S07": "New throw: the ball starts in FAST's hand, flies across, hits the unsuspecting kid, and he tumbles out of frame right.",
    "S10": "Simpler and frantic: FAST bolts out, doubles back for a cassette he forgot, grabs it, and bolts out again.",
    "S14": "The brain now reads JEV.",
    "S28": "Built from start, middle and end frames: FAST sprints in and leaps onto the hood, then launches off straight at "
           "the camera. The launch half plays at 1.4x.",
    "S46": "New end frame: FAST's feet fly out and he lands on his backside. SLOW and the headline are unchanged.",
}
FIXES = {  # what changed after clip QA (see TRIM, MONO, STILL_FX, PATCH, HOOK_Y, STAMP_AT in compose.py)
    "S01": "Frame 0 is the poster, then the tape's PLAY screen.",
    "S17": "Re-rendered with the keyframe pinned as the last frame, so '2029' stays legible (it had turned into '4029').",
    "S20": "Uses the clip's first 2.05 s, slightly slowed; FAST's shirt turned purple after that.",
    "S26": "FAST stamps moved across the chests, off SLOW's face.",
    "S34": "Uses the clip's first 1.95 s, slowed; the model cut to an off-model close-up after that.",
    "S36": "Built from the keyframe: VHS rewind judder, then freeze. The model had added stray text.",
    "S39": "The keyframe's 'OCT 14 '94' date stamp is pasted back in; the model garbled it.",
    "S43": "Desaturated; the model slipped blue light into the ink wash.",
    "S47": "Added the fast-forward OSD and tape counter.",
    "S60": "Hook caption moved above the mixer so the LOW / MAX labels show.",
    "S65": "Card text holds to the cut.",
    "S66": "Poster still with a slow push-in; STOP shows in the last 3 s.",
}

def source(s):
    if s["id"] == "S36": return "Keyframe + VHS rewind"
    if s.get("card"): return "Title card"
    if s["id"] == "S66": return "Poster still"
    if (CL / "kling3pro" / f"{s['id']}.mp4").exists(): return "Kling 3 Pro"
    if (CL / "wan3" / f"{s['id']}.mp4").exists(): return "Wan 3.0"
    return "Keyframe still"

def bounds(s):
    a, b = round(s["start"] * FPS), round(s["end"] * FPS)            # the compositor's frame range for this shot
    return a / FPS, (b - a) / FPS

def cut(s):
    t0, dur = bounds(s)
    clip, thumb = RV / "clips" / f"{s['id']}.mp4", RV / "thumbs" / f"{s['id']}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.4f}", "-i", str(MASTER), "-t", f"{dur:.4f}",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(clip)], check=True)
    at = {"S01": 0.5, "S65": dur - 0.4}.get(s["id"], dur * 0.62)         # mid-shot, where the caption is mostly on
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0 + at:.3f}", "-i", str(MASTER), "-frames:v", "1",
                    "-vf", "scale=960:-2", "-q:v", "3", str(thumb)], check=True)
    return s["id"]

def scene(s):
    t0, dur = bounds(s)
    caps = [{"style": c["style"], "text": s["text"][0] if s.get("card") else c["text"]}
            for c in s["captions"] if c["end"] - c["start"] >= 0.05]
    return {"id": s["id"], "start": round(t0, 3), "end": round(t0 + dur, 3), "dur": round(dur, 3), "section": s["section"],
            "mode": s["mode"], "title": s["title"], "insert43": bool(s.get("insert43")), "captions": caps,
            "scene": s["scene"], "camera": s["camera"], "motion": s["motion"], "text": s.get("text") or [],
            "source": source(s), "fix": FIXES.get(s["id"], ""), "clip": f"clips/{s['id']}.mp4", "thumb": f"thumbs/{s['id']}.jpg",
            "updated": s["id"] in UPDATED, "update_note": UPDATED.get(s["id"], ""),
            "prev_clip": f"clips/r{ROUND - 1}/{s['id']}.mp4" if s["id"] in UPDATED else ""}

def keep_previous_round():
    """Before re-cutting, park the previous render's clips of the updated scenes (for the page's compare toggle) and
    snapshot the previous round's feedback."""
    prev = RV / "clips" / f"r{ROUND - 1}"; prev.mkdir(exist_ok=True)
    for sid in UPDATED:
        src, dst = RV / "clips" / f"{sid}.mp4", prev / f"{sid}.mp4"
        if src.exists() and not dst.exists(): shutil.copy(src, dst)
    fb, snap = RV / "feedback.json", RV / f"feedback-r{ROUND - 1}.json"
    if fb.exists() and not snap.exists(): shutil.copy(fb, snap)

if __name__ == "__main__":
    if ROUND > 1: keep_previous_round()
    with cf.ThreadPoolExecutor(8) as ex:
        done = list(ex.map(cut, SHOTS))
    out = {"title": "Sometimes I Think Slow", "round": ROUND, "render": MASTER.name, "full": "../out/fast-and-slow_share.mp4",
           "poster": "../poster.jpg", "duration": 182.4, "v": int(time.time()), "scenes": [scene(s) for s in SHOTS]}
    json.dump(out, open(RV / "review.json", "w"), indent=1)
    print(f"{len(done)} scenes -> {RV / 'review.json'}")
