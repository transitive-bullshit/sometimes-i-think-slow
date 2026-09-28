"""Targeted Kling 3 Pro re-renders: shots whose first pass drifted, and the scene review's change requests.

Each job names its shot, a hand-written motion/scene prompt, a duration, the start frame and an optional end frame.
Pinning the end frame keeps in-world text stable (S17's '2029', S14's 'JEV') or makes an action finish (S46's fall,
S28's leap). Outputs video/clips/kling3pro_alt/<job>.mp4 with a receipt; the chosen take is copied to
video/clips/kling3pro/<shot>.mp4 (S28 joins its two halves at the approved hood frame).

usage: rerender_fix.py <job or shot id...>      (a shot id runs all of its jobs, e.g. S02 -> S02_a S02_b)
"""
import json, sys, time, pathlib, concurrent.futures as cf

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from render_shots import LOOK, KEEP, NEG, DATA, FR

R2 = ROOT / "video/storyboard/frames_r2"
LOUD = "Keep the art style, characters, faces, hair, outfits and any lettering exactly as in the first frame. No new text or subtitles."

S17 = dict(shot="S17", dur=3,
           motion="FAST caps his marker and taps the calendar twice, grinning with total confidence; SLOW behind the counter "
                  "pinches the bridge of his nose and shakes his head",
           scene="Inside the bodega: a wall calendar reads 'SEPTEMBER 1991' with a big '2029' already scrawled over it in black "
                 "marker. The '2029' is finished and never changes; nobody writes anything more.")
S02 = dict(shot="S02", dur=6,
           motion="FAST never stops moving: he kicks off on his skateboard and carves fast, tight lines back and forth in front "
                  "of the chalk mural, pops a high ollie, lands it and snaps a kickflip, full of energy; SLOW stays perfectly "
                  "still in the same spot, calmly turning one page of his notebook",
           scene="Under the overpass at dusk: 'train-time compute' and 'test-time compute' chalk charts on the wall behind "
                 "them; the crew leans on a car in the background.")
S03 = dict(shot="S03", dur=4, keep=LOUD,
           motion="Three big hits on the beat: the three kids on the car hood are hype men; on each hit they punch their fists "
                  "into the air together and shout 'FAST!', bouncing on the hood; on the last hit the kid with the skateboard "
                  "hoists it overhead; the camera bumps on each hit",
           scene="Three kids sit on the hood of a boxy 80s sedan under the overpass at dusk, graffiti on the pillars, sodium light.")
S07 = dict(shot="S07", dur=3, start=R2 / "S07_start.png",
           motion="FAST whips a hard spiral pass; the football streaks across the frame in a straight line and slams into the "
                  "unsuspecting kid's chest; the kid catches it by reflex, is knocked off his feet and tumbles backward out of "
                  "frame to the right",
           scene="A sunny park by a playground: FAST on the left, a kid at the far right looking the other way.")
S10 = dict(shot="S10", dur=3,
           motion="Frantic and simple: FAST is running out, stops dead, spins back, snatches a cassette off the counter and "
                  "sprints out of frame to the right in a blur; the soda can, the cassette stack and the newspaper rack crash "
                  "over in his wake; the pigeon flaps away",
           scene="A bodega counter with a sticky note on the CRT reading 'MAKE NO MISTAKES'.")
S14 = dict(shot="S14", dur=3, start=R2 / "S14.png",
           motion="The word JEV glows brighter first; then FAST sprays the wall in one fluid stroke",
           scene="FAST in profile in front of a brick wall with a spray can; a translucent holographic X-ray of his head shows a "
                 "glowing node graph with the neon word 'JEV' lit up. The word 'JEV' never changes.")
S28 = dict(shot="S28", scene="Under the overpass at dusk, a boxy sedan, the crowd behind cheering with fists raised.")
S46 = dict(shot="S46", dur=3, end=R2 / "S46_end.png",
           motion="FAST's foot shoots out on the banana peel, his legs fly up and he lands hard, flat on his backside; SLOW "
                  "doesn't flinch and keeps reading, holding the newspaper perfectly still with its headline facing the camera",
           scene="A rainy newsstand in monochrome ink wash; SLOW in the foreground reads a newspaper headlined 'GARY MARCUS: "
                 "\"TOLD YOU IT WOULD SLIP\"'. The headline never changes.")

JOBS = {
    "S17_a": S17, "S17_b": dict(S17, end=FR / "S17.png"),
    "S02_a": S02, "S02_b": S02,
    "S03_a": S03, "S03_b": S03,
    "S03h_a": dict(S03, start=R2 / "S03_hype.png",
                   motion="Already mid-chant: the three kids on the car hood keep punching their fists into the air on the beat "
                          "and shouting 'FAST!', bouncing on the hood, three big pumps; the kid on the right shakes his "
                          "skateboard overhead; the camera bumps on each hit"),
    "S07_a": S07, "S07_b": dict(S07, end=R2 / "S07_end.png"),
    "S10_a": S10, "S10_b": S10,
    "S14_a": S14, "S14_b": dict(S14, end=R2 / "S14.png"),
    "S28in_a": dict(S28, dur=3, start=R2 / "S28_start.png", end=FR / "S28.png",
                    motion="FAST sprints in and leaps up onto the car hood in one explosive bound, landing in a crouch; the "
                           "crowd erupts"),
    "S28out_a": dict(S28, dur=5, end=R2 / "S28_end.png",
                     motion="FAST bounces once on the hood, then launches off it straight at the camera, flying toward the "
                            "lens; the crowd behind jumps with fists raised on each hit"),
    "S46_a": S46, "S46_b": S46,
}
JOBS["S28in_b"], JOBS["S28out_b"], JOBS["S03h_b"] = JOBS["S28in_a"], JOBS["S28out_a"], JOBS["S03h_a"]

def rel(p):
    """Receipts record repo-relative paths, so they read the same on any machine."""
    return str(pathlib.Path(p).resolve().relative_to(ROOT)) if p else ""

def one(job):
    import fal_client, requests
    out = ROOT / "video/clips/kling3pro_alt" / f"{job}.mp4"
    if out.exists(): return job, "exists"
    j = JOBS[job]; s = DATA[j["shot"]]
    start = fal_client.upload_file(str(j.get("start", FR / f"{j['shot']}.png")))
    args = {"start_image_url": start,
            "prompt": f"{j['motion']}. {j['scene']} Camera: {s['camera']}. {LOOK[s['mode']]} {j.get('keep', KEEP)}",
            "negative_prompt": NEG + ", new writing, changing letters or numbers, slow motion", "generate_audio": False,
            "duration": str(j["dur"]), "cfg_scale": 0.5}
    if j.get("end"): args["end_image_url"] = start if j["end"] == j.get("start", FR / f"{j['shot']}.png") else fal_client.upload_file(str(j["end"]))
    t = time.time()
    try:
        res = fal_client.subscribe("fal-ai/kling-video/v3/pro/image-to-video", arguments=args)
    except Exception as e:
        return job, f"error: {str(e)[:300]}"
    out.write_bytes(requests.get(res["video"]["url"], timeout=600).content)
    json.dump({"job": job, "shot": j["shot"], "start": rel(j.get("start")), "end": rel(j.get("end")),
               "args": {k: v for k, v in args.items() if "url" not in k}, "seconds": round(time.time() - t, 1)},
              open(out.with_suffix(".json"), "w"), indent=1)
    return job, f"ok {time.time() - t:.0f}s"

if __name__ == "__main__":
    jobs = [k for a in sys.argv[1:] for k in ([a] if a in JOBS else [k for k in JOBS if JOBS[k]["shot"] == a])]
    with cf.ThreadPoolExecutor(max(1, len(jobs))) as ex:
        for r in ex.map(one, jobs): print(*r, flush=True)
