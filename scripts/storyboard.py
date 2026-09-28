"""Build the storyboard: shots.json for the review tool, plus one keyframe per shot.

Keyframes are Nano Banana Pro edits fed (1) a style/base reference for the shot's mode and (2) the v2 model sheets
for whoever is in the shot, so every frame stays on-model in the approved look. Shots marked reuse=True copy their
approved key frame; the typewriter card is drawn locally. Captions come from the timed lyrics (display spellings).
Existing frames are skipped, so a redo is: delete the frame, rerun.

usage: storyboard.py [data|frames|all] [shot ids...]
env:   FAL_KEY
"""
import json, sys, time, shutil, pathlib, concurrent.futures as cf

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from storyboard_shots import SHOTS, END

V2 = ROOT / "video/concept/v2"
SB = ROOT / "video/storyboard"; FR = SB / "frames"; PV = SB / "preview"

STYLE_BY_MODE = {"hook": "k1-underpass-v2", "fast": "k3-court-v2b", "slow": "k4-laundromat-sumie-b",
                 "transition": "k1-underpass-v2", "sunrise": "k1-underpass-v2"}
MODE_TEXT = {
    "hook": "Dusk under a concrete highway overpass with sodium streetlights. Color split: the left side of the frame is warm and "
            "saturated (FAST's side), the right side cool and desaturated (SLOW's side).",
    "fast": "FAST's world: bright, saturated 90s colors (traffic-cone orange, teal, purple; neon if it is night), energetic "
            "diagonal composition, speed lines only where something moves fast.",
    "slow": "Monochrome Japanese sumi-e ink wash rendering of the same cel anime style: black ink and grey washes on warm washi "
            "paper, brush texture, ink bleeds, no color at all, EXCEPT that FAST's windbreaker, if he appears, keeps a faint "
            "wash of its orange and teal (he is vivid in SLOW's memory).",
    "transition": "A transitional frame where color and monochrome ink wash meet, bleeding into each other across the frame.",
    "sunrise": "Sunrise: warm golden light unifies the whole frame in full color, hopeful and bright.",
}
SHEETS = {"FAST": "sheet-fast-v2", "SLOW": "sheet-slow-v2"}

def caption_style(section, text):
    """hook = sign-painted mural lettering; stamp = the crew's "fast fast fast"; fast = FAST's spray tags;
    slow = SLOW's handwriting; typewriter = the a cappella breaks and the spoken tag."""
    if text.startswith("(Fast"): return "stamp"
    if section == "Hook": return "hook"
    if text.startswith("(It's a nickel"): return "slow"
    if section in ("Break", "Spoken"): return "typewriter"
    if section == "Verse 1": return "fast"
    return "slow"

def clean_hook(caps):
    """Hook lettering has no parentheses: 'Sometimes I think slow / Sometimes I think fast' on two lines, the crowd's
    echo stamped as FAST FAST FAST, and a call followed by its (response) merged into one two-line caption."""
    out = []
    for c in caps:
        if c["style"] == "stamp":
            out.append({**c, "text": "FAST FAST FAST"}); continue
        if c["style"] != "hook":
            out.append(c); continue
        t = c["text"].strip("()").replace(", sometimes", "\nSometimes")
        if c["text"].startswith("(") and out and out[-1]["style"] == "hook" and "\n" not in out[-1]["text"]:
            out[-1] = {**out[-1], "text": out[-1]["text"] + "\n" + t, "end": c["end"]}
        else:
            out.append({**c, "text": t})
    return out

def shots_data():
    """shots.json's content: the shot list with end times, durations and captions attached from the timed lyrics."""
    timed = json.load(open(ROOT / "analysis/suno/lyrics-timed.json"))["lines"]
    shots = []
    for i, s in enumerate(SHOTS):
        end = SHOTS[i + 1]["start"] if i + 1 < len(SHOTS) else END
        caps = [{"text": L["text"], "start": round(L["start"], 2), "end": round(L["end"], 2),
                 "style": caption_style(L["section"], L["text"])}
                for L in timed if s["start"] - 0.05 <= L["start"] < end - 0.05]
        shots.append({**{k: v for k, v in s.items()}, "end": round(end, 2), "dur": round(end - s["start"], 2),
                      "captions": clean_hook(caps), "frame": f"preview/{s['id']}.jpg", "frame_full": f"frames/{s['id']}.png"})
    return {"song": "../../audio/suno/final-take.wav", "bpm": 105.24, "v": 2, "poster": "poster.png", "shots": shots}

def build_data():
    data = shots_data(); shots = data["shots"]
    SB.mkdir(parents=True, exist_ok=True)
    json.dump(data, open(SB / "shots.json", "w"), indent=1)
    print(f"shots.json: {len(shots)} shots, {sum(len(s['captions']) for s in shots)} caption lines")
    return shots

def prompt_for(s):
    who = [c for c in s.get("chars", [])]
    refs = ["Image 1 is the style reference" + (" and the base composition to adapt" if s.get("base") or s.get("base_frame") else "") +
            ": match its 1990s hand-painted cel anime look, ink line quality, film grain and VHS softness exactly."]
    for n, c in enumerate(who, start=2):
        refs.append(f"Image {n} is {c}'s model sheet: draw {c} exactly on-model (same face, hair, skin tone, glasses, outfit and props).")
    text = (f"The only readable text in the image: {'; '.join(repr(t) for t in s['text'])}, spelled exactly and rendered as part "
            f"of the scene on real objects. No other text, captions, subtitles or speech bubbles."
            if s.get("text") else "No readable text, letters, captions, subtitles or speech bubbles anywhere.")
    cast = ("Characters: " + " and ".join(who) + " only, no one else unless the scene mentions extras. Their mouths are closed "
            "or relaxed (nobody is mid-word)." if who else "No main characters in this shot.")
    return (f"Create a new 16:9 storyboard keyframe for a music video. {' '.join(refs)} {MODE_TEXT[s['mode']]}\n"
            f"Scene: {s['scene']}\nCamera: {s['camera']}.\n{cast}\n{text}\nNo borders, no panel frames, not a comic page.")

_urls = {}
def upload(name):
    if name not in _urls:
        import fal_client
        _urls[name] = fal_client.upload_file(str(V2 / f"{name}.png"))
    return _urls[name]

def upload_frame(sid):
    """An existing storyboard frame used as the base composition (e.g. S64 continues S62's stoop)."""
    key = f"frame:{sid}"
    if key not in _urls:
        import fal_client
        _urls[key] = fal_client.upload_file(str(FR / f"{sid}.png"))
    return _urls[key]

def card(s):
    """Typewriter title card, drawn locally (no model)."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (2048, 1152), (6, 6, 6)); d = ImageDraw.Draw(img)
    try: f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New.ttf", 64); o = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New.ttf", 34)
    except Exception: f = o = ImageFont.load_default()
    t = s["text"][0]; w = d.textlength(t, font=f)
    d.text(((2048 - w) / 2, 540), t, fill=(235, 235, 230), font=f)
    d.text((80, 70), "PLAY ▶", fill=(235, 235, 230), font=o); d.text((1660, 1040), "SP 3:02", fill=(235, 235, 230), font=o)
    img.save(FR / f"{s['id']}.png")

def render(s):
    import fal_client, requests
    out = FR / f"{s['id']}.png"
    if out.exists(): return s["id"], "exists"
    if s.get("card"): card(s); return s["id"], "card"
    if s.get("reuse"):
        shutil.copy(V2 / f"{s['base']}.png", out); return s["id"], "reused key frame"
    first = upload_frame(s["base_frame"]) if s.get("base_frame") else upload(s.get("base") or STYLE_BY_MODE[s["mode"]])
    imgs = [first] + [upload(SHEETS[c]) for c in s.get("chars", [])]
    prompt = prompt_for(s)
    t = time.time()
    for attempt in range(2):
        try:
            res = fal_client.subscribe("fal-ai/nano-banana-pro/edit", arguments={
                "prompt": prompt, "image_urls": imgs, "resolution": "2K",
                "aspect_ratio": "4:3" if s.get("insert43") else "16:9"})
            out.write_bytes(requests.get(res["images"][0]["url"], timeout=300).content)
            json.dump({"id": s["id"], "prompt": prompt, "refs": imgs, "seconds": round(time.time() - t, 1)},
                      open(FR / f"{s['id']}.json", "w"), indent=1)
            return s["id"], f"ok {time.time() - t:.0f}s"
        except Exception as e:
            err = str(e)[:200]
    return s["id"], f"error: {err}"

def previews(ids=None):
    """1280-wide JPEG previews of the 2K keyframes for the review page."""
    from PIL import Image
    PV.mkdir(parents=True, exist_ok=True)
    for p in sorted(FR.glob("S*.png")):
        if ids and p.stem not in ids: continue
        dst = PV / f"{p.stem}.jpg"
        if not dst.exists() or dst.stat().st_mtime < p.stat().st_mtime:
            im = Image.open(p).convert("RGB")
            im.resize((1280, round(im.height * 1280 / im.width)), Image.LANCZOS).save(dst, quality=82)

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    ids = set(sys.argv[2:])
    shots = build_data()
    if what in ("frames", "all"):
        FR.mkdir(parents=True, exist_ok=True)
        todo = [s for s in SHOTS if not ids or s["id"] in ids]
        need = {s.get("base") or STYLE_BY_MODE[s["mode"]] for s in todo if not s.get("reuse") and not s.get("card")}
        need |= {SHEETS[c] for s in todo for c in s.get("chars", [])}
        for n in need: upload(n)                       # upload refs once, before the threads start
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            for sid, status in ex.map(render, todo):
                print(f"{sid}  {status}", flush=True)
        previews(ids or None)
