"""Version B only: lip-synced close-ups for the storyboard's lip-sync candidates (the default cut uses none).

For each candidate: (1) a tighter, face-forward close-up variant of the approved keyframe (Nano Banana Pro edit with
the model sheets), (2) that shot's slice of the isolated Suno vocal, (3) OmniHuman 1.5 animates the close-up to sing
the slice. Two-shot hooks get a full-white mask so both MCs chant. Clips land in video/clips/omnihuman/.

usage: lipsync.py [frames|audio|render|all] [shot ids...]
env:   FAL_KEY
"""
import json, sys, time, subprocess, pathlib, concurrent.futures as cf

ROOT = pathlib.Path(__file__).resolve().parent.parent
SB = ROOT / "video/storyboard"
LF = SB / "lipsync_frames"; LA = ROOT / "audio/suno/lipsync"; OUT = ROOT / "video/clips/omnihuman"
for d in (LF, LA, OUT): d.mkdir(parents=True, exist_ok=True)
SHOTS = {s["id"]: s for s in json.load(open(SB / "shots.json"))["shots"]}
VOCALS = ROOT / "audio/suno/stems/final-take_vocals.wav"
SHEETS = {"FAST": ROOT / "video/concept/v2/sheet-fast-v2.png", "SLOW": ROOT / "video/concept/v2/sheet-slow-v2.png"}

CLOSEUPS = {  # who sings, and the close-up to build from the approved keyframe
    "S02": (["FAST", "SLOW"], "medium close-up two-shot of FAST and SLOW side by side under the underpass mural, both facing the camera"),
    "S06": (["FAST"], "close-up of FAST riding the bowl's wall, face toward camera in three-quarter view, SLOW out of focus behind"),
    "S14": (["FAST"], "close-up of FAST in three-quarter view by the brick wall, spray can in hand, a faint holographic node graph glowing around his head"),
    "S26": (["FAST", "SLOW"], "medium close-up two-shot of FAST (left, warm light) and SLOW (right, cool light), both turned toward the camera"),
    "S37": (["SLOW"], "close-up of SLOW in the laundromat, lit by a lightning flash through the window, facing the camera in three-quarter view"),
    "S51": (["FAST"], "close-up of FAST sitting on the rainy curb, head up, soaked, face visible in three-quarter view, the boombox beside him"),
    "S52": (["SLOW"], "low-angle close-up of SLOW in the rain holding his closed umbrella, face clearly visible, looking down at camera"),
    "S58": (["FAST", "SLOW"], "medium close-up two-shot of FAST and SLOW back to back under the sunrise underpass, both faces toward camera"),
    "S61": (["FAST", "SLOW"], "medium close-up two-shot of FAST and SLOW shoulder to shoulder in sunrise flare, both facing the camera"),
}
MODE_NOTE = {"slow": "Keep the monochrome sumi-e ink wash rendering (FAST keeps a faint wash of his jacket colors).",
             "hook": "Keep the dusk sodium-light color split.", "fast": "Keep the saturated 90s colors.",
             "sunrise": "Keep the warm golden sunrise light.", "transition": ""}

def frames(ids):
    import fal_client, requests
    sheet_urls = {k: fal_client.upload_file(str(v)) for k, v in SHEETS.items()}
    def one(sid):
        out = LF / f"{sid}.png"
        if out.exists(): return sid, "exists"
        who, shot = CLOSEUPS[sid]; s = SHOTS[sid]
        imgs = [fal_client.upload_file(str(SB / "frames" / f"{sid}.png"))] + [sheet_urls[c] for c in who]
        refs = " ".join(f"Image {i} is {c}'s model sheet: keep {c} exactly on-model." for i, c in enumerate(who, start=2))
        prompt = (f"Image 1 is the approved shot; re-frame it as a {shot}, for a lip-synced rap performance. {refs} Same setting, "
                  f"lighting and 1990s hand-painted cel anime style as image 1. {MODE_NOTE[s['mode']]} Faces large, clear and "
                  f"well lit, mouths relaxed and slightly parted. No text, captions or speech bubbles.")
        res = fal_client.subscribe("fal-ai/nano-banana-pro/edit", arguments={"prompt": prompt, "image_urls": imgs,
                                                                             "aspect_ratio": "16:9", "resolution": "2K"})
        out.write_bytes(requests.get(res["images"][0]["url"], timeout=300).content)
        json.dump({"id": sid, "prompt": prompt}, open(LF / f"{sid}.json", "w"), indent=1)
        return sid, "ok"
    with cf.ThreadPoolExecutor(6) as ex:
        for sid, st in ex.map(one, ids): print("frame", sid, st, flush=True)

def audio(ids):
    for sid in ids:
        s = SHOTS[sid]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['start']:.3f}", "-t", f"{s['dur']:.3f}", "-i", str(VOCALS),
                        "-ac", "1", "-ar", "44100", str(LA / f"{sid}.wav")], check=True)
    print("audio slices:", len(ids))

def render(ids):
    import fal_client, requests
    from PIL import Image
    def one(sid):
        out = OUT / f"{sid}.mp4"
        if out.exists(): return sid, "exists"
        who, _ = CLOSEUPS[sid]
        jpg = LF / f"{sid}.jpg"                             # OmniHuman can't fetch the 6-8 MB 2K PNGs; a 1080p JPEG works
        if not jpg.exists(): Image.open(LF / f"{sid}.png").convert("RGB").resize((1920, 1080), Image.LANCZOS).save(jpg, quality=92)
        args = {"image_url": fal_client.upload_file(str(jpg)), "audio_url": fal_client.upload_file(str(LA / f"{sid}.wav")),
                "resolution": "1080p",
                "prompt": "A 1990s cel anime rapper performing laid-back hip-hop, relaxed head nods on the beat, "
                          "natural lip movement matching the rap vocal, hand-drawn animation style, no text."}
        if len(who) == 2:                                   # both MCs chant the hook
            m = LF / f"{sid}_mask.png"
            Image.new("L", (1920, 1080), 255).save(m)
            args["mask_url"] = fal_client.upload_file(str(m))
        t = time.time()
        try:
            res = fal_client.subscribe("fal-ai/bytedance/omnihuman/v1.5", arguments=args)
        except Exception as e:
            return sid, f"error: {str(e)[:300]}"
        out.write_bytes(requests.get(res["video"]["url"], timeout=600).content)
        json.dump({"id": sid, "seconds": round(time.time() - t, 1), "prompt": args["prompt"]}, open(OUT / f"{sid}.json", "w"), indent=1)
        return sid, f"ok {time.time() - t:.0f}s"
    with cf.ThreadPoolExecutor(5) as ex:
        for sid, st in ex.map(one, ids): print("lipsync", sid, st, flush=True)

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    ids = sys.argv[2:] or list(CLOSEUPS)
    if what in ("frames", "all"): frames(ids)
    if what in ("audio", "all"): audio(ids)
    if what in ("render", "all"): render(ids)
