"""Round-2 keyframes for the scene review's change requests (Nano Banana Pro edit of the approved frames).

New start/end frames give the video model the action the user asked for: S07's throw starts with the ball in FAST's
hand, S28 gets sprint-in and leap-out frames around the approved hood frame, S46 gets FAST flat on his backside, and
S14's brain reads JEV instead of LINE. Outputs video/storyboard/frames_r2/<name>_<try>.png.

usage: keyframe_fix.py [names...]
"""
import json, sys, time, pathlib, concurrent.futures as cf

ROOT = pathlib.Path(__file__).resolve().parent.parent
FR = ROOT / "video/storyboard/frames"; OUT = ROOT / "video/storyboard/frames_r2"; OUT.mkdir(parents=True, exist_ok=True)
FAST_SHEET = ROOT / "video/concept/v2/sheet-fast-v2.png"
STYLE = "Same 1990s hand-painted cel anime style, camera angle, lighting and colors as image 1. No text, captions or speech bubbles."
ONMODEL = "Image 2 is FAST's model sheet: keep FAST exactly on-model (face, dreadlocks, jacket, chain, jeans, sneakers)."

EDITS = {  # name: (source shot, include FAST's sheet, prompt, tries)
    "S07_start": ("S07", True, "Image 1 is an approved frame. Show the moment just BEFORE the throw: FAST (left) has his right "
                  "arm cocked back behind his head, gripping the brown football, about to throw a spiral. The kid at the right "
                  "edge is not ready at all: looking away toward the playground, hands empty and down at his sides. Remove the "
                  "football and the motion lines from the kid's side of the frame. " + ONMODEL + " " + STYLE, 2),
    "S07_end": ("S07", True, "Image 1 is an approved frame. Show the moment just AFTER the catch: FAST (left) in the "
                "follow-through of his throw, grinning, arm extended toward the right. The kid has been knocked off his feet "
                "by the football and is tumbling out of the frame past the right edge: only one sneaker, a flailing arm, the "
                "football and a puff of dust are still visible at the far right edge. " + ONMODEL + " " + STYLE, 1),
    "S14": ("S14", False, "Change only the glowing neon word inside the holographic brain from 'LINE' to 'JEV': same glowing "
            "orange neon-tube lettering, same height, same position and angle, centered where 'LINE' was. Keep everything "
            "else in image 1 exactly identical: face, hair, hand, spray can, bricks, node graph, colors.", 1),
    "S28_start": ("S28", True, "Image 1 is an approved frame. Show the moment BEFORE it: FAST is on the ground at the left, "
                  "two strides from the car, sprinting toward it at full speed, low and leaning forward, about to leap onto "
                  "the hood; motion lines behind him; the crowd behind is already cheering with fists up. Same underpass at "
                  "dusk, same car and crowd. " + ONMODEL + " " + STYLE, 2),
    "S28_end": ("S28", True, "Image 1 is an approved frame. Show the moment AFTER it: FAST has launched off the car hood and "
                "is flying straight at the camera, huge in the foreground, sneaker soles and knees nearest the lens, arms "
                "spread wide, jacket flaring, grinning; the car and the jumping crowd behind him with fists raised. Same "
                "underpass at dusk. " + ONMODEL + " " + STYLE, 2),
    "S46_end": ("S46", True, "Image 1 is an approved frame. Show the pratfall landing: FAST (left background) has slipped on "
                "the banana peel and landed hard flat on his backside on the floor, legs kicked up in the air, arms flailing, "
                "the banana peel flying off. Keep SLOW, his newspaper and its headline, the notebook and the newsstand exactly "
                "identical. Keep the monochrome sumi-e ink-wash rendering; FAST keeps his faint jacket colors. " + ONMODEL, 2),
    "S03_hype": ("S03", False, "Image 1 is an approved frame. Show the same moment one beat later: the three kids on the car "
                 "hood are hype men mid-chant, all three punching their fists high in the air, mouths wide open shouting, "
                 "bouncing on the hood; the kid on the right hoists his skateboard overhead with one hand. Same kids, same "
                 "clothes (the left kid keeps his orange, teal and purple jacket), same car, same overpass, same fisheye camera "
                 "angle, same dusk sodium lighting. " + STYLE, 2),
    "S46_sit": ("S46", True, "Image 1 is an approved frame. Show the pratfall landing: FAST (left background) has slipped on "
                "the banana peel and landed sitting hard on his backside on the floor, in the same spot where he stands in "
                "image 1, legs splayed out in front of him with one sneaker kicked up high, arms flailing, a shocked face, the "
                "banana peel flying up above him. His whole body stays in the upper-left and middle-left of the frame, above "
                "the bottom fifth. His jacket keeps exactly the same faint orange, teal and purple colors as in image 1 (only "
                "FAST has color; everything else is monochrome ink wash). Keep SLOW, his newspaper and its headline, the "
                "notebook and the newsstand exactly identical. " + ONMODEL, 2),
}

def run(name, k):
    import fal_client, requests
    out = OUT / f"{name}_{k}.png"
    if out.exists(): return name, k, "exists"
    shot, sheet, prompt, _ = EDITS[name]
    imgs = [fal_client.upload_file(str(FR / f"{shot}.png"))] + ([fal_client.upload_file(str(FAST_SHEET))] if sheet else [])
    t = time.time()
    res = fal_client.subscribe("fal-ai/nano-banana-pro/edit", arguments={"prompt": prompt, "image_urls": imgs,
                                                                         "resolution": "2K", "aspect_ratio": "16:9"})
    out.write_bytes(requests.get(res["images"][0]["url"], timeout=300).content)
    json.dump({"name": name, "shot": shot, "prompt": prompt, "seconds": round(time.time() - t, 1)},
              open(out.with_suffix(".json"), "w"), indent=1)
    return name, k, f"ok {time.time() - t:.0f}s"

if __name__ == "__main__":
    names = sys.argv[1:] or list(EDITS)
    jobs = [(n, k) for n in names for k in range(1, EDITS[n][3] + 1)]
    with cf.ThreadPoolExecutor(len(jobs)) as ex:
        for r in ex.map(lambda j: run(*j), jobs): print(*r, flush=True)
