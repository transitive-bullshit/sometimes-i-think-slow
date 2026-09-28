"""Concept art for the art-direction pass: style frames and character sheets, generated on fal in parallel.

Every job shares one style anchor and one pair of character descriptions, so frames from different models and scenes
stay comparable. Jobs whose image already exists are skipped. Receipts (prompt, model, seconds) are saved next to the images.

usage: concept_art.py <job-name-prefix> ...      (no args = every job)
env:   FAL_KEY
"""
import json, sys, time, pathlib, concurrent.futures as cf
import requests, fal_client

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "video/concept"; OUT.mkdir(parents=True, exist_ok=True)

STYLE = ("1990s hand-painted cel anime film still, grounded adult anime in the spirit of late-90s jazz-noir TV anime, "
         "gouache-painted backgrounds, crisp ink linework with varied line weight, limited palette, cel shading, soft film "
         "grain and faint VHS chroma bleed, cinematic 90s New York hip-hop mood, subtle cyberpunk details. "
         "Not 3D, not CGI, not Pixar, not glossy, no text artifacts.")
FAST = ("FAST: a lanky young Black man in his early 20s, short twists under a backwards bucket hat, oversized color-block "
        "windbreaker in traffic-cone orange, teal and purple, baggy jeans, skate shoes, a pager on his waistband, thin gold "
        "chain with a lightning-bolt pendant, cocky grin, always mid-motion")
SLOW = ("SLOW: FAST's identical twin brother with the same face, calm and deliberate, round wire-frame glasses, charcoal wool "
        "flat cap, oversized camel overcoat over a black turtleneck, corduroy trousers, a black-and-white composition notebook "
        "and a pencil, Walkman headphones around his neck, thin gold chain with a small round pendant, knowing half-smile, perfectly still")

SCENES = {
    "k1-underpass": ("Under a concrete highway underpass at dusk, the twins stand side by side in front of a huge graffiti mural "
                     "of two scatter-plot charts spray-painted in chalky white on dark concrete, titled 'train-time compute' and "
                     "'test-time compute', each with dots climbing up and to the right. FAST on the left pops an ollie on his "
                     "skateboard in warm saturated colors; SLOW on the right stands still reading his notebook in cool muted tones. "
                     "Sodium streetlights, puddles, a small crew leaning on a car in the background."),
    "k2-bodega": ("Inside a cramped 1991 New York corner bodega at night. A handwritten cardboard price sign reads 'BAT + BALL $1.10'. "
                  "FAST slaps a single dime on the counter with total confidence. His twin SLOW, calm, slides one nickel across the "
                  "counter without looking up from his notebook. A small CRT TV behind the counter, lottery tickets, fluorescent light, "
                  "a bored cat on the counter."),
}
SCENES.update({
    "k3-court": ("Sun-bleached outdoor basketball court behind a chain-link fence, afternoon. FAST, in an oversized jersey printed "
                 "'LOW', crosses over and blows past a towering player in a jersey printed 'HIGH', who stumbles and falls. A big "
                 "courtside scoreboard reads 'LOW 21  HIGH 19'. Beside it a hand-painted sign shows an effort slider "
                 "'INSTANT · MEDIUM · HIGH · XHIGH · MAX' with the marker on INSTANT. Kids cheer on the fence; SLOW watches "
                 "from the bleachers with his notebook. Saturated warm colors, speed lines, smear frames."),
    "k4-laundromat": ("The same anime style rendered as black-and-white ink-wash noir. 3 a.m. laundromat, rain streaking the window, "
                      "a flickering neon sign 'ABILENE WASH & FOLD'. SLOW sits alone on a bench with his notebook open; rows of "
                      "front-loading dryers spin and glow like server fans; on a folding table a dot-matrix printer spills a long "
                      "ribbon of fan-fold paper covered in handwritten reasoning across the floor. Monochrome, deep blacks, film grain."),
    "k5-book": ("Golden-hour brownstone stoop. SLOW sits on the steps holding up a paperback with a clean white cover that reads "
                "'THINKING, FAST AND SLOW' above the author name 'DANIEL KAHNEMAN' in black type. FAST leans over his shoulder "
                "reading the title, visibly offended, pointing at himself. A boombox on the step, a pigeon on the railing, warm light."),
})
SCENES.update({
    "k4b-laundromat-noir": ("STRICTLY BLACK-AND-WHITE monochrome ink-wash noir, no color at all, heavy blacks, film grain. 3 a.m. "
                            "laundromat, rain streaking the window, a flickering neon sign 'ABILENE WASH & FOLD'. SLOW sits ALONE on a "
                            "bench with his notebook open, head tilted, thinking; FAST is not in this scene. Rows of front-loading dryers "
                            "spin like server fans; on a folding table a dot-matrix printer spills a long ribbon of fan-fold paper covered "
                            "in handwritten reasoning across the floor."),
    "k6-karpathy-crt": ("Inside the bodega at night, close on a small CRT TV behind the counter showing a social media post card: "
                        "display name 'Andrej Karpathy', handle '@karpathy', post text 'no thinking, single token, low latency'. "
                        "FAST leans into frame pointing at the TV with a proud grin, SLOW in the background rolling his eyes. "
                        "Scanlines and CRT glow."),
    "k7-marcus-news": ("Rainy corner newsstand at night. A stack of tabloid newspapers with a huge front-page headline "
                       "'GARY MARCUS: \"TOLD YOU IT WOULD SLIP\"'. SLOW holds one open, deadpan, one eyebrow raised; FAST in the "
                       "background mid-slip on a banana peel, frozen in a smear frame. Sodium light, wet pavement."),
})
SHEETS = {
    "sheet-fast": ("Character model sheet on plain warm-gray paper, 1990s cel anime production design. FAST shown as a full-body "
                   "turnaround (front, three-quarter, side, back) plus three head close-ups with expressions: cocky grin, "
                   "wide-eyed surprise, laughing. Small prop callouts: skateboard with orange wheels, pager, lightning-bolt pendant, "
                   "bucket hat. Title lettering at the top: 'FAST - SYSTEM ONE'. Color swatches: traffic-cone orange, teal, purple, denim."),
    "sheet-slow": ("Character model sheet on plain warm-gray paper, 1990s cel anime production design. SLOW shown as a full-body "
                   "turnaround (front, three-quarter, side, back) plus three head close-ups with expressions: calm half-smile, "
                   "deadpan side-eye, one eyebrow raised over his glasses. Small prop callouts: composition notebook with pencil, "
                   "Walkman cassette player with headphones, round gold pendant, flat cap. Title lettering at the top: "
                   "'SLOW - SYSTEM TWO'. Color swatches: camel, charcoal, black, cream."),
    "sheet-twins": ("Model sheet lineup on plain warm-gray paper, 1990s cel anime production design: the identical twins FAST and "
                    "SLOW standing side by side, full body, front view, same face and same height, opposite body language. "
                    "Title lettering at the top: 'SAME DATA. SAME WEIGHTS.'"),
}

MODELS = {  # endpoint, argument builder (p=prompt, ar=aspect, refs=uploaded reference URLs)
    "seedream": ("bytedance/seedream/v5/pro/text-to-image",
                 lambda p, ar, refs: {"prompt": p, "image_size": {"width": 2048, "height": 1152} if ar == "16:9" else "auto_2K"}),
    "nanopro": ("fal-ai/nano-banana-pro", lambda p, ar, refs: {"prompt": p, "aspect_ratio": ar, "resolution": "2K"}),
    "nanoedit": ("fal-ai/nano-banana-pro/edit",
                 lambda p, ar, refs: {"prompt": p, "image_urls": refs, "aspect_ratio": ar, "resolution": "2K"}),
    "krea": ("krea/v2/large/text-to-image",
             lambda p, ar, refs: {"prompt": p, "aspect_ratio": ar, "creativity": "medium",
                                  "image_style_references": [{"image_url": u, "strength": 0.8} for u in refs]}),
}
STYLE_REFS = [OUT / "bake-krea-k1-underpass.png", OUT / "bake-krea-k2-bodega.png"]   # the chosen look

def job_prompt(scene):
    return f"{STYLE}\n\nCharacters: {FAST}. {SLOW}.\n\nScene: {SCENES[scene]}"

def sheet_prompt(sheet):
    return f"{STYLE}\n\nCharacters: {FAST}. {SLOW}.\n\n{SHEETS[sheet]}"

JOBS = {f"bake-{m}-{s}": (m, job_prompt(s), "16:9", False) for m in ("seedream", "nanopro", "krea") for s in ("k1-underpass", "k2-bodega")}
JOBS.update({f"{s}": ("krea", job_prompt(s), "16:9", True) for s in ("k3-court", "k4-laundromat", "k5-book",
                                                                          "k4b-laundromat-noir", "k6-karpathy-crt", "k7-marcus-news")})
JOBS.update({f"{s}-krea": ("krea", sheet_prompt(s), "16:9", True) for s in SHEETS})
JOBS.update({f"{s}-nano": ("nanoedit", "Keep these exact two characters: the same faces, hair, outfits and the same 1990s cel anime "
                           "look as the reference images. " + SHEETS[s], "16:9", True) for s in SHEETS})

_ref_urls = None
def ref_urls():
    global _ref_urls
    if _ref_urls is None:
        _ref_urls = [fal_client.upload_file(str(p)) for p in STYLE_REFS]
    return _ref_urls

def run(name):
    out = OUT / f"{name}.png"
    if out.exists(): return name, "exists"
    model, prompt, ar, use_refs = JOBS[name]
    endpoint, build = MODELS[model]
    t = time.time()
    try:
        res = fal_client.subscribe(endpoint, arguments=build(prompt, ar, ref_urls() if use_refs else []))
    except Exception as e:
        return name, f"error: {str(e)[:200]}"
    url = res["images"][0]["url"]
    out.write_bytes(requests.get(url, timeout=300).content)
    json.dump({"name": name, "endpoint": endpoint, "prompt": prompt, "seconds": round(time.time() - t, 1)},
              open(OUT / f"{name}.json", "w"), indent=1)
    return name, f"ok {time.time() - t:.0f}s"

if __name__ == "__main__":
    wanted = [j for j in JOBS if not sys.argv[1:] or any(j.startswith(a) for a in sys.argv[1:])]
    if any(JOBS[j][3] and not (OUT / f"{j}.png").exists() for j in wanted):
        ref_urls()                                   # upload the style refs once, before the threads start
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for name, status in ex.map(run, wanted):
            print(f"{name:28s} {status}", flush=True)
