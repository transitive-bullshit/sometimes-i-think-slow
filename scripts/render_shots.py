"""Animate storyboard keyframes into shot clips with an image-to-video model on fal.

Every clip starts from its approved keyframe (video/storyboard/frames/Sxx.png), runs silent (we score it with the Suno
track), and asks for motion only: characters stay on-model and nobody sings (the cut works without lip-sync).
Clips land in video/clips/<model>/Sxx.mp4 with a receipt. Existing clips are skipped.

usage: render_shots.py <model> [shot ids...]      (no ids = every shot that needs a model; cards are drawn locally)
env:   FAL_KEY
"""
import json, math, sys, time, pathlib, concurrent.futures as cf

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from storyboard_shots import SHOTS

FR = ROOT / "video/storyboard/frames"
DATA = {s["id"]: s for s in json.load(open(ROOT / "video/storyboard/shots.json"))["shots"]}

LOOK = {
    "hook": "1990s hand-painted cel anime, dusk under a highway overpass, sodium light, film grain, VHS softness.",
    "fast": "1990s hand-painted cel anime, saturated colors, energetic limited animation with smear frames, film grain.",
    "slow": "monochrome Japanese sumi-e ink wash animation, calm and slow, ink texture on washi paper, film grain.",
    "transition": "1990s cel anime; color and monochrome ink wash bleeding into each other.",
    "sunrise": "1990s hand-painted cel anime, warm golden sunrise light, film grain.",
}
KEEP = ("Keep the art style, characters, faces, hair, outfits and any lettering exactly as in the first frame. Characters "
        "do not speak or sing; mouths stay closed or relaxed. No new text or subtitles.")
NEG = "3D render, CGI, photorealistic, morphing, warped faces, extra limbs, extra people, subtitles, captions, watermark, text changes"

def prompt(s):
    return f"{s['motion']}. {s['scene']} Camera: {s['camera']}. {LOOK[s['mode']]} {KEEP}"

def secs_for(s, choices=None, lo=3, hi=15):
    """Shortest allowed duration that covers the shot (plus a little handle for trimming)."""
    need = s["dur"] + 0.4
    if choices: return next((c for c in choices if c >= need), choices[-1])
    return max(lo, min(hi, math.ceil(need)))

MODELS = {
    "kling3pro": ("fal-ai/kling-video/v3/pro/image-to-video", lambda s, url: {
        "start_image_url": url, "prompt": prompt(s), "negative_prompt": NEG, "generate_audio": False,
        "duration": str(secs_for(s, lo=3, hi=15)), "cfg_scale": 0.5}),
    "veolite": ("fal-ai/veo3.1/lite/image-to-video", lambda s, url: {
        "image_url": url, "prompt": prompt(s), "negative_prompt": NEG, "generate_audio": False, "resolution": "1080p",
        "duration": f"{secs_for(s, choices=[4, 6, 8])}s", "aspect_ratio": "16:9"}),
    "wan3": ("alibaba/wan-3.0/image-to-video", lambda s, url: {
        "start_image_url": url, "prompt": prompt(s), "audio": False, "resolution": "1080p", "enable_prompt_expansion": False,
        "duration": secs_for(s, lo=3, hi=10), "aspect_ratio": "4:3" if s.get("insert43") else "16:9"}),
    "pixverse6": ("fal-ai/pixverse/v6/image-to-video", lambda s, url: {
        "image_url": url, "prompt": prompt(s), "negative_prompt": NEG, "resolution": "1080p", "style": "anime",
        "duration": secs_for(s, lo=1, hi=15), "generate_audio_switch": False}),
}

def render(model, sid):
    import fal_client, requests
    out_dir = ROOT / "video/clips" / model; out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{sid}.mp4"
    if out.exists(): return sid, "exists"
    s = DATA[sid]
    endpoint, build = MODELS[model]
    url = fal_client.upload_file(str(FR / f"{sid}.png"))
    args = build(s, url)
    t = time.time()
    for attempt in range(2):
        try:
            res = fal_client.subscribe(endpoint, arguments=args)
            out.write_bytes(requests.get(res["video"]["url"], timeout=600).content)
            json.dump({"id": sid, "model": model, "endpoint": endpoint, "args": {k: v for k, v in args.items() if "url" not in k},
                       "seconds": round(time.time() - t, 1)}, open(out_dir / f"{sid}.json", "w"), indent=1)
            return sid, f"ok {time.time() - t:.0f}s ({args.get('duration')})"
        except Exception as e:
            err = str(e)[:300]
    return sid, f"error: {err}"

if __name__ == "__main__":
    model = sys.argv[1]
    ids = sys.argv[2:] or [s["id"] for s in SHOTS if not s.get("card")]
    with cf.ThreadPoolExecutor(max_workers=int(__import__("os").environ.get("WORKERS", 6))) as ex:
        for sid, status in ex.map(lambda i: render(model, i), ids):
            print(f"{model} {sid} {status}", flush=True)
