"""Art direction v2: Champloo-inspired FAST (wild street-fighter energy) and SLOW (Japanese ronin), via Nano Banana Pro edits.

Edits keep what was approved (the 90s cel/VHS look, wardrobe, compositions, in-world text) and only change the characters.
Stage 1 makes the new model sheets; stage 2 swaps them into the approved key frames and adds two in-world
treatments for the Karpathy post. Existing outputs are skipped. Receipts go next to the images.

usage: art_direction_v2.py [stage=all|sheets|frames]
env:   FAL_KEY
"""
import json, sys, time, pathlib, concurrent.futures as cf
import requests, fal_client

ROOT = pathlib.Path(__file__).resolve().parent.parent
C = ROOT / "video/concept"
OUT = C / "v2"; OUT.mkdir(exist_ok=True)

KEEP = ("Keep the flat 1990s hand-painted cel anime look with soft film grain exactly as in the reference, keep the "
        "composition, background, props and any lettering exactly as they are, and draw no extra people.")
FAST_V2 = ("FAST: a lanky young Black man with dark skin and a wild, untamed mane of short spiky twists sticking out in every "
           "direction, no hat, wiry loose-limbed build, restless street-fighter energy like a breakdancer about to spin, cocky "
           "grin, wearing his oversized traffic-cone orange, teal and purple color-block windbreaker, white tee, baggy jeans, "
           "sneakers, a pager on his waistband and a thin gold chain with a lightning-bolt pendant")
SLOW_V2 = ("SLOW: a lean Japanese man in his mid-20s with long straight black hair tied in a low ponytail, thin rectangular "
           "wire-frame glasses, calm and composed like a wandering ronin, no hat, wearing his oversized camel overcoat over a "
           "black turtleneck, corduroy trousers, Walkman headphones around his neck, a round gold pendant, holding a black-and-white "
           "composition notebook and pencil")

SHEETS = {
    "sheet-fast-v2": ("sheet-fast-nano.png", f"Redesign this model sheet's character as {FAST_V2}. Remove the bucket hat from the prop "
                      "callouts. Keep the same model-sheet layout, turnaround poses, three expressions, title lettering "
                      "'FAST - SYSTEM ONE', prop callouts and color swatches. In the front view give him a crouched, ready stance. " + KEEP),
    "sheet-slow-v2": ("sheet-slow-nano.png", f"Redesign this model sheet's character as {SLOW_V2}. Replace the flat-cap prop callout "
                      "with a hair tie. Keep the same model-sheet layout, turnaround poses, three expressions (calm half-smile, deadpan "
                      "side-eye, one raised eyebrow over his glasses), title lettering 'SLOW - SYSTEM TWO', prop callouts and color swatches. " + KEEP),
}
SWAP = ("Image 1 is the scene to edit. Image 2 is the model sheet for FAST and image 3 is the model sheet for SLOW. Redraw the two "
        "characters in image 1 as these two exact characters (same faces, hair, skin tones and outfits as their model sheets), in "
        "the same poses and positions. ")
FRAMES = {
    "k0-keyart-v2": ("sheet-twins-krea.png", SWAP + "Keep the title lettering 'SAME DATA. SAME WEIGHTS.' Remove any other stray lettering. " + KEEP),
    "k1-underpass-v2": ("bake-krea-k1-underpass.png", SWAP + KEEP),
    "k2-bodega-v2": ("bake-krea-k2-bodega.png", SWAP + "FAST slaps a single dime on the counter; SLOW slides a single nickel with two fingers without looking up. " + KEEP),
    "k3-court-v2": ("k3-court.png", SWAP + "Only one SLOW appears: remove the second copy of him sitting on the bleachers. " + KEEP),
    "k5-book-v2": ("k5-book.png", SWAP + "SLOW holds the book 'THINKING, FAST AND SLOW' by 'DANIEL KAHNEMAN' with the title clearly legible. " + KEEP),
    "k7-marcus-v2": ("k7-marcus-news.png", SWAP + "Keep the headline 'GARY MARCUS: \"TOLD YOU IT WOULD SLIP\"' exactly and legibly. "
                     "The FAST in the background slipping on a banana peel is the only FAST: remove the other one. " + KEEP),
    "k4-laundromat-sumie": ("k4c-laundromat-noir.png", "Image 1 is the scene to edit and image 3 is the model sheet for SLOW; ignore image 2. "
                            "Redraw the man on the bench as SLOW exactly as on his model sheet. Re-render the whole scene as Japanese "
                            "sumi-e ink wash painting fused with the cel anime linework: expressive black brush strokes, ink bleeds, washi "
                            "paper grain, pure monochrome with silver highlights, rain rendered as fine brush lines. Keep the neon sign "
                            "'ABILENE WASH & FOLD', the glowing dryers and the printer ribbon. No color."),
    "k6a-karpathy-crt": ("k6-karpathy-crt.png", SWAP + "Replace everything on the CRT screen with a glowing, slightly curved, scanlined "
                         "image of a social media post card: bold name 'Andrej Karpathy', grey handle '@karpathy' beneath it, and the "
                         "post text 'no thinking, single token, low latency' in clean sans-serif, spelled exactly. No portrait on the "
                         "screen. The screen's blue-white glow lights FAST's face as he points at it. Remove the 'SLOW' sign on the wall. " + KEEP),
    "k6b-karpathy-pager": ("bake-krea-k2-bodega.png", "Use image 1 only as the style and lighting reference and image 2 for FAST's hand "
                           "and sleeve. New image, same 1990s cel anime style: extreme close-up of FAST's hand holding his beeper with "
                           "the orange-teal windbreaker cuff visible. The pager's backlit green LCD shows two lines in blocky segment "
                           "type, spelled exactly: 'KARPATHY:' and 'NO THINKING. SINGLE TOKEN. LOW LATENCY'. Soft-focus bodega neon "
                           "and a CRT glow behind, film grain."),
}

_urls = {}
def url(name):
    if name not in _urls:
        _urls[name] = fal_client.upload_file(str((C / name) if (C / name).exists() else (OUT / name)))
    return _urls[name]

def run(job):
    name, (src, prompt) = job
    out = OUT / f"{name}.png"
    if out.exists(): return name, "exists"
    imgs = [url(src)] + ([url("sheet-fast-v2.png"), url("sheet-slow-v2.png")] if not name.startswith("sheet") else [])
    t = time.time()
    try:
        res = fal_client.subscribe("fal-ai/nano-banana-pro/edit", arguments={"prompt": prompt, "image_urls": imgs,
                                                                             "aspect_ratio": "16:9", "resolution": "2K"})
    except Exception as e:
        return name, f"error: {str(e)[:200]}"
    out.write_bytes(requests.get(res["images"][0]["url"], timeout=300).content)
    json.dump({"name": name, "endpoint": "fal-ai/nano-banana-pro/edit", "source": src, "prompt": prompt,
               "seconds": round(time.time() - t, 1)}, open(OUT / f"{name}.json", "w"), indent=1)
    return name, f"ok {time.time() - t:.0f}s"

def batch(jobs):
    for n, (src, _) in jobs.items(): url(src)          # upload sources once, before the threads start
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for name, status in ex.map(run, jobs.items()):
            print(f"{name:22s} {status}", flush=True)

if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if stage in ("all", "sheets"): batch(SHEETS)
    if stage in ("all", "frames"):
        url("sheet-fast-v2.png"); url("sheet-slow-v2.png")
        batch(FRAMES)
