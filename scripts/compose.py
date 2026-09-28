"""Compose the music video: retime shot clips onto the song's frame grid, grade by mode, add film/VHS texture, animate
the in-world captions, put the poster on frame 0, and mux the Suno track. One Python pass, frames piped to ffmpeg.

Captions use the display lyrics (real spellings) with word timings from analysis/suno/lyrics-timed.json:
  fast = spray tags popping on word by word · slow = handwriting writing itself on · hook = sign lettering, one line
  per sung phrase · stamp = FAST FAST FAST on the hits · typewriter = the a cappella breaks and the spoken tag.

usage: compose.py [--lipsync] [--from SEC --to SEC] [--out PATH]
"""
import argparse, json, math, random, subprocess, pathlib, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
SB = ROOT / "video/storyboard"; CL = ROOT / "video/clips"; FONTS = ROOT / "video/fonts"
W, H, FPS = 1920, 1080, 24
SONG_END = 182.4

ap = argparse.ArgumentParser()
ap.add_argument("--lipsync", action="store_true")
ap.add_argument("--from", dest="t0", type=float, default=0.0)
ap.add_argument("--to", dest="t1", type=float, default=SONG_END)
ap.add_argument("--out", default=None)
A = ap.parse_args() if __name__ == "__main__" else ap.parse_args([])   # importable (tests) with the defaults

DATA = json.load(open(SB / "shots.json")); SHOTS = DATA["shots"]; BY_ID = {s["id"]: s for s in SHOTS}
TIMED = json.load(open(ROOT / "analysis/suno/lyrics-timed.json"))["lines"]
LIPSYNC_IDS = {"S02", "S06", "S14", "S26", "S37", "S51", "S52", "S58", "S61"}

# per-shot fixes from clip QA
TRIM = {"S20": 2.05, "S34": 1.95}                           # use only the clip's first N s (after that it drifts or loses its text)
FIT = {"S02", "S03", "S46"}                                  # round-2 takes: play the whole clip, fitted to the shot, so the action lands
MONO = {"S43"}                                               # the model slipped blue light into the ink wash
STILL_FX = {"S36": "rewind"}                                 # built from the keyframe: VHS rewind judder, then freeze
PATCH = {"S39": (0.72, 0.855, 0.95, 0.95)}                   # keep the keyframe's date stamp (x0, y0, x1, y1); the model garbles it
HOOK_Y = {"S60": 430}                                        # hook lettering above the mixer so its LOW / MAX labels stay readable
STAMP_AT = {"S26": (0.34, 0.60),                             # FAST stamps across the chests, off SLOW's face
            "S03": (0.20, 0.10)}                             # over the overpass, off the crew's raised skateboard

# ---------------------------------------------------------------- sources
def clip_for(s):
    if A.lipsync and s["id"] in LIPSYNC_IDS and (CL / "omnihuman" / f"{s['id']}.mp4").exists():
        return CL / "omnihuman" / f"{s['id']}.mp4", "lipsync"
    for m in ("kling3pro", "wan3"):
        p = CL / m / f"{s['id']}.mp4"
        if p.exists(): return p, m
    return None, None

def probe_dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout.strip() or 0)

def keyframe(s, box):
    return np.asarray(ImageOps.fit(Image.open(SB / "frames" / f"{s['id']}.png").convert("RGB"), box, Image.LANCZOS))

def rewind_frames(s, n, box):
    """Tape rewinding: the picture judders and tears for ~60% of the shot, then freezes clean."""
    base = keyframe(s, box); r = np.random.default_rng(36); bw, bh = box
    for i in range(n):
        fr = base.copy()
        if i < int(n * 0.6):
            fr = np.roll(fr, int(r.integers(-12, 13)), axis=0)
            for b in range(3):                                     # tearing bands crawling up the screen
                y = int((bh - i * 41 - b * 350) % bh); hgt = min(int(r.integers(22, 70)), bh - y)
                band = np.roll(fr[y:y + hgt], int(r.integers(40, 140)) * (1 if b % 2 else -1), axis=1).astype(np.int16)
                band = band * 0.7 + 60 + r.integers(-40, 40, (hgt, bw, 1))
                band[r.random((hgt, bw)) > 0.985] = 255             # dropout sparkle
                fr[y:y + hgt] = band.clip(0, 255).astype(np.uint8)
        fr[-16:] = np.roll(fr[-16:], 28, axis=1)                   # head-switching noise
        yield pillar(fr)

def patch_from_keyframe(fr, s, box):
    """Paste a feathered rectangle of the keyframe back over a clip frame."""
    if not hasattr(patch_from_keyframe, "cache"): patch_from_keyframe.cache = {}
    key = s["id"]
    if key not in patch_from_keyframe.cache:
        x0, y0, x1, y1 = PATCH[key]; bw, bh = box
        m = Image.new("L", box, 0); ImageDraw.Draw(m).rectangle([x0 * bw, y0 * bh, x1 * bw, y1 * bh], fill=255)
        m = np.asarray(m.filter(ImageFilter.GaussianBlur(8)), np.float32)[..., None] / 255
        patch_from_keyframe.cache[key] = (keyframe(s, box).astype(np.float32), m)
    kf, m = patch_from_keyframe.cache[key]
    return (fr * (1 - m) + kf * m).astype(np.uint8)

def clip_frames(s, n):
    """Yield n RGB frames (H, W, 3 uint8) for shot s: retimed clip, still with a slow push, or black card."""
    p, kind = clip_for(s)
    box = (1440, 1080) if s.get("insert43") else (W, H)
    if STILL_FX.get(s["id"]) == "rewind":
        yield from rewind_frames(s, n, box)
        return
    if p is None:                                                  # still: poster/end card, intro, or missing clip
        src = ROOT / "video/poster.png" if s["id"] == "S66" else SB / "frames" / f"{s['id']}.png"
        if s.get("card") or not src.exists():
            for _ in range(n): yield np.zeros((H, W, 3), np.uint8)
            return
        im = Image.open(src).convert("RGB")
        for i in range(n):
            z = 1.0 + 0.05 * i / max(1, n - 1)                      # slow push-in
            cw, ch = im.width / z, im.height / z
            x0, y0 = (im.width - cw) / 2, (im.height - ch) / 2
            fr = im.resize(box, Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
            yield pillar(np.asarray(fr))
        return
    dur = probe_dur(p)
    need = n / FPS
    if kind == "lipsync": speed = 1.0                                # already exactly the shot's audio length
    elif s["id"] in TRIM: speed = min(dur, TRIM[s["id"]]) / need     # stretch the good part over the shot
    elif s["id"] in FIT: speed = dur / need
    elif s["mode"] == "fast": speed = min(1.6, max(1.0, dur / need))  # FAST plays a touch fast
    else: speed = min(1.0, dur / need) if dur < need else 1.0
    vf = (f"setpts=PTS/{speed:.4f},fps={FPS},scale={box[0]}:{box[1]}:force_original_aspect_ratio=increase,"
          f"crop={box[0]}:{box[1]}")
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(p), "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    last = None; got = 0; fb = box[0] * box[1] * 3
    while got < n:
        buf = proc.stdout.read(fb)
        if len(buf) < fb: break
        last = np.frombuffer(buf, np.uint8).reshape(box[1], box[0], 3); got += 1
        if s["id"] in PATCH and kind != "lipsync": last = patch_from_keyframe(last, s, box)
        yield pillar(last)
    proc.stdout.close(); proc.kill()
    while got < n:                                                 # hold the last frame if the clip ran short
        got += 1; yield pillar(last if last is not None else np.zeros((box[1], box[0], 3), np.uint8))

def pillar(fr):
    if fr.shape[1] == W: return fr
    out = np.zeros((H, W, 3), np.uint8); x = (W - fr.shape[1]) // 2
    out[:, x:x + fr.shape[1]] = fr
    return out

# ---------------------------------------------------------------- look
rng = np.random.default_rng(1991)
GRAIN = [np.asarray(Image.fromarray((rng.normal(128, 38, (H // 2, W // 2))).clip(0, 255).astype(np.uint8))
                    .resize((W, H), Image.BILINEAR)).astype(np.int16) - 128 for _ in range(12)]
yy, xx = np.mgrid[0:H, 0:W]
VIGNETTE = (1 - 0.28 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)).clip(0.55, 1)[..., None].astype(np.float32)
SCAN = (1 - 0.06 * ((yy % 3) == 0))[..., None].astype(np.float32)

def grade(fr, mode, fidx, insert43, mono=False):
    f = fr.astype(np.float32)
    if mono: f = np.repeat(f.mean(2, keepdims=True), 3, axis=2)
    if mode == "fast":
        g = f.mean(2, keepdims=True); f = g + (f - g) * 1.10; f = (f - 128) * 1.04 + 128
    elif mode == "sunrise":
        f = f * np.array([1.05, 1.0, 0.93], np.float32)
    elif mode == "slow":
        f = f * np.array([1.02, 1.0, 0.95], np.float32) + 4          # warm washi paper
    f = f * VIGNETTE
    if insert43 or mode == "hook":
        f = f * SCAN
    f += GRAIN[fidx % len(GRAIN)][..., None] * (0.16 if mode == "slow" else 0.11)
    out = f.clip(0, 255).astype(np.uint8)
    shift = 3 if insert43 else 1                                   # chroma bleed: nudge red right, blue left
    out[..., 0] = np.roll(out[..., 0], shift, axis=1); out[..., 2] = np.roll(out[..., 2], -shift, axis=1)
    return out

# ---------------------------------------------------------------- captions
def font(name, size):
    f = ImageFont.truetype(str(FONTS / name), size)
    if "Caveat" in name:
        try: f.set_variation_by_axes([700])
        except Exception: pass
    return f
F_FAST = font("PermanentMarker-Regular.ttf", 66)
F_SLOW = font("Caveat[wght].ttf", 78)
F_HOOK = font("Bungee-Regular.ttf", 66)
F_STAMP = font("SpecialElite-Regular.ttf", 84)
F_TYPE = font("SpecialElite-Regular.ttf", 58)
F_OSD = font("SpecialElite-Regular.ttf", 38)

def wrap(text, f, maxw):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if f.getlength(t) <= maxw or not cur: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
    return lines

def word_starts(cap):
    """Per-word start times for a caption line, from the aligned transcript (evenly spread when missing)."""
    words = cap["text"].replace("\n", " ").split()
    line = next((L for L in TIMED if abs(L["start"] - cap["start"]) < 0.3), None)
    wt = [w[1] for w in (line or {}).get("word_times", [])]
    if len(wt) >= len(words) * 0.7 and wt:
        wt = sorted(wt)
        return [wt[min(i, len(wt) - 1)] if i < len(wt) else wt[-1] + 0.12 * (i - len(wt) + 1) for i in range(len(words))]
    span = max(0.3, cap["end"] - cap["start"])
    return [cap["start"] + span * i / max(1, len(words)) for i in range(len(words))]

def hook_line_starts(cap):
    """For a merged two-line hook caption, when each line is sung."""
    lines = cap["text"].split("\n")
    inside = [L["start"] for L in TIMED if cap["start"] - 0.05 <= L["start"] <= cap["end"] - 0.1]
    if len(lines) == 2:
        second = inside[1] if len(inside) > 1 else cap["start"] + (cap["end"] - cap["start"]) * 0.45
        if "Sometimes" in lines[1] and len(inside) == 1:             # one sung line holding both halves
            second = cap["start"] + (cap["end"] - cap["start"]) * 0.5
        return [cap["start"], second]
    return [cap["start"]]

def draw_text(d, xy, text, f, fill, shadow=None, stroke=0, stroke_fill=None, anchor="la"):
    if shadow:
        (dx, dy), sc = shadow
        d.text((xy[0] + dx, xy[1] + dy), text, font=f, fill=sc, anchor=anchor, stroke_width=stroke, stroke_fill=sc)
    d.text(xy, text, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill)

POS = {}
def cap_anchor(shot, style, idx):
    """Where captions sit, kept off the shots' key content (faces, receipts)."""
    custom = {"S08": "bl", "S09": "bl", "S10": "br", "S11": "bl", "S12": "tl", "S17": "br", "S20": "bl", "S46": "bl",
              "S14": "bl", "S18": "tl", "S19": "bl", "S13": "br", "S21": "bl", "S22": "bl", "S16": "tr", "S39": "tl"}
    if shot in custom: return custom[shot]
    if style == "fast": return "bl" if idx % 2 == 0 else "br"
    if style in ("typewriter",): return "cc"
    return "bc"

def render_caption(frame_img, cap, t, shot_id, cap_index):
    style = cap["style"]; d = ImageDraw.Draw(frame_img, "RGBA")
    a = cap_anchor(shot_id, style, cap_index)
    margin_x, margin_y = (310, 110) if BY_ID[shot_id].get("insert43") else (110, 110)   # stay inside a 4:3 picture
    if style == "stamp":
        hits = word_starts(cap)[:3]
        for k, ht in enumerate(hits):
            if t < ht - 0.02: continue
            age = t - ht; sc = 1.0 + max(0.0, 0.6 - age * 6)           # slam in
            img = Image.new("RGBA", (360, 150), (0, 0, 0, 0)); dd = ImageDraw.Draw(img)
            dd.rectangle([6, 6, 353, 143], outline=(255, 77, 46, 235), width=7)
            dd.text((180, 78), "FAST", font=F_STAMP, fill=(255, 77, 46, 235), anchor="mm")
            img = img.rotate(-8 + k * 6, expand=True, resample=Image.BICUBIC)
            if sc != 1.0: img = img.resize((int(img.width * sc), int(img.height * sc)), Image.BICUBIC)
            bx, by = STAMP_AT.get(shot_id, (0.62, 0.16))
            x = int(W * (bx + 0.11 * k) - img.width / 2); y = int(H * (by + 0.07 * k) - img.height / 2)
            frame_img.alpha_composite(img, (max(0, x), max(0, y)))
        return
    if style == "hook":
        lines = cap["text"].split("\n"); starts = hook_line_starts(cap)
        y = HOOK_Y.get(shot_id, H - 250 if len(lines) == 2 else H - 170)
        for li, (ln, st) in enumerate(zip(lines, starts)):
            if t < st - 0.03: continue
            age = t - st; alpha = int(255 * min(1.0, age / 0.12))
            draw_text(d, (W // 2, y + li * 88), ln.upper(), F_HOOK, (255, 247, 224, alpha), shadow=((6, 6), (27, 24, 20, alpha)),
                      anchor="mm")
        return
    if style == "typewriter":                  # types out from a fixed left edge with a block cursor; over a picture it
        text = cap["text"]; span = max(0.4, min(1.6, cap["end"] - cap["start"]))      # sits on a closed-caption box
        n = int(len(text) * min(1.0, max(0.0, t - cap["start"]) / span))
        y = {"S65": H // 2, "S36": 790}.get(shot_id, H - 170)          # S36: above the TV's own CHECKPOINT readout
        cw = F_TYPE.getlength("M") * 0.62
        x0 = (W - F_TYPE.getlength(text) - cw - 10) / 2
        if shot_id != "S65" and n:
            d.rectangle([x0 - 18, y - F_TYPE.size * 0.62, x0 + F_TYPE.getlength(text[:n]) + cw + 26, y + F_TYPE.size * 0.55],
                        fill=(0, 0, 0, 205))
        draw_text(d, (x0, y), text[:n], F_TYPE, (240, 240, 235, 255), shadow=((0, 3), (0, 0, 0, 200)), anchor="lm")
        if int(t * 3) % 2 == 0:
            cx = x0 + F_TYPE.getlength(text[:n]) + 8
            d.rectangle([cx, y - F_TYPE.size * 0.42, cx + cw, y + F_TYPE.size * 0.36], fill=(240, 240, 235, 235))
        return
    f = F_FAST if style == "fast" else F_SLOW
    lines = wrap(cap["text"], f, 1250)
    lh = int(f.size * (1.02 if style == "fast" else 0.92))
    total_h = lh * len(lines)
    if a.startswith("t"): y0 = margin_y
    elif a == "cc": y0 = (H - total_h) // 2
    else: y0 = H - margin_y - total_h
    widths = [f.getlength(ln) for ln in lines]
    def x_for(w):
        if a.endswith("l"): return margin_x
        if a.endswith("r"): return W - margin_x - w
        return (W - w) / 2
    if style == "fast":                                                # word-by-word spray pop
        starts = word_starts(cap); wi = 0
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        for li, ln in enumerate(lines):
            x = x_for(widths[li]); y = y0 + li * lh
            for w in ln.split():
                st = starts[min(wi, len(starts) - 1)]; wi += 1
                if t >= st - 0.02:
                    pop = max(0.0, 1 - (t - st) / 0.10)
                    col = (255, 122, 26, 255)
                    ld.text((x + 4, y + 5), w, font=f, fill=(15, 111, 108, 255))
                    ld.text((x, y - int(6 * pop)), w, font=f, fill=col, stroke_width=2, stroke_fill=(58, 13, 0, 255))
                x += f.getlength(w + " ")
        random.seed(hash(cap["text"]) % 1000)
        layer = layer.rotate(random.uniform(-3.5, 1.5), center=(W // 2, H // 2), resample=Image.BICUBIC)
        frame_img.alpha_composite(layer)
        return
    # slow: handwriting writes itself on, left to right, line by line
    span = max(0.2, (cap["end"] - cap["start"]) * 0.85)
    prog = min(1.0, max(0.0, (t - cap["start"]) / span))
    total_w = sum(widths); budget = prog * total_w
    for li, ln in enumerate(lines):
        x = x_for(widths[li]); y = y0 + li * lh
        show_w = max(0.0, min(widths[li], budget)); budget -= widths[li]
        if show_w <= 0: break
        pad = 24                                                      # ink-bleed halo keeps it legible on pale washi
        layer = Image.new("RGBA", (int(widths[li]) + 2 * pad, lh + 2 * pad), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        ld.text((pad, pad), ln, font=f, fill=(20, 16, 12, 150), stroke_width=7, stroke_fill=(20, 16, 12, 150))
        layer = layer.filter(ImageFilter.GaussianBlur(9)); ld = ImageDraw.Draw(layer)
        ld.text((pad + 2, pad + 4), ln, font=f, fill=(0, 0, 0, 170))
        ld.text((pad, pad), ln, font=f, fill=(245, 239, 226, 255))
        layer = layer.crop((0, 0, int(show_w) + pad + 12, layer.height))
        frame_img.alpha_composite(layer, (int(x) - pad + 6, int(y) - pad))

def osd_glyph(d, kind, x, y, size, fill):
    """VCR symbols drawn as shapes (Special Elite has no ▶ or ■); (x, y) is the top-left, returns the right edge."""
    sh = (0, 0, 0, 160)
    def tri(x0, col, dx=0, dy=0, flip=False):
        pts = [(x0, y), (x0, y + size), (x0 + size * 0.85, y + size / 2)]
        if flip: pts = [(x0 + size * 0.85, y), (x0 + size * 0.85, y + size), (x0, y + size / 2)]
        d.polygon([(px + dx, py + dy) for px, py in pts], fill=col)
    if kind == "stop":
        d.rectangle([x + 2, y + 2, x + size + 2, y + size + 2], fill=sh); d.rectangle([x, y, x + size, y + size], fill=fill)
        return x + size
    n = 2 if kind in ("ff", "rew") else 1
    for k in range(n):
        xk = x + k * size * 0.7
        tri(xk, sh, 2, 2, kind == "rew"); tri(xk, fill, flip=kind == "rew")
    return x + (n - 1) * size * 0.7 + size * 0.85

def osd(frame_img, s, t):
    """On-screen display for the tape inserts that don't already carry one baked into the art (S16, S36, S39 do)."""
    d = ImageDraw.Draw(frame_img, "RGBA")
    white, sh = (255, 255, 255, 230), ((2, 2), (0, 0, 0, 160))
    x0 = (W - 1440) // 2 + 60
    if s["id"] == "S01":                                               # hitting play on the tape
        draw_text(d, (x0, 60), "PLAY", F_OSD, white, shadow=sh)
        osd_glyph(d, "play", x0 + F_OSD.getlength("PLAY ") + 4, 66, 30, white)
        draw_text(d, (x0 + 1440 - 460, H - 110), "SEP 28 1991  03:02", F_OSD, white, shadow=sh)
    elif s["id"] == "S47":                                             # epochs went by: the tape fast-forwards
        right = osd_glyph(d, "ff", x0, 66, 30, white)
        draw_text(d, (right + 18, 60), "FF", F_OSD, white, shadow=sh)
        k = min(1.0, max(0.0, (t - s["start"]) / s["dur"]))
        draw_text(d, (x0 + 1440 - 330, H - 110), f"{int(1991 + k * 8008):05d}", F_OSD, white, shadow=sh)
    if s["id"] == "S66" and t > s["end"] - 3.0:
        osd_glyph(d, "stop", 80, 66, 28, (255, 255, 255, 220))
        draw_text(d, (80 + 46, 60), "STOP", F_OSD, (255, 255, 255, 220), shadow=sh)

# ---------------------------------------------------------------- main loop
def main():
    out = A.out or str(ROOT / "video/out" / ("fast-and-slow_lipsync.mp4" if A.lipsync else "fast-and-slow.mp4"))
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    f0, f1 = int(round(A.t0 * FPS)), int(round(A.t1 * FPS))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-ss", f"{A.t0:.3f}", "-t", f"{(f1 - f0) / FPS:.3f}", "-i", str(ROOT / "audio/suno/final-take.wav"),
                            "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    poster = np.asarray(Image.open(ROOT / "video/poster.png").convert("RGB").resize((W, H), Image.LANCZOS))
    fidx = 0
    for si, s in enumerate(SHOTS):
        a, b = int(round(s["start"] * FPS)), int(round(s["end"] * FPS))
        if b <= f0 or a >= f1: continue
        n = b - a
        caps = [c for c in s["captions"] if c["end"] - c["start"] >= 0.05]   # drop zero-length lines the take never sang
        if s.get("card"):                                   # the tag card shows its own wording, typed out, held to the cut
            caps = [{**c, "text": s["text"][0]} for c in caps] or [{"text": s["text"][0], "start": s["start"] + 2.2,
                                                                    "end": s["start"] + 3.0, "style": "typewriter"}]
            caps = [{**c, "until": s["end"]} for c in caps]
        for i, c in enumerate(caps):                        # linger 0.45 s, but give way to the next line in the same style
            nxt = [d["start"] for d in caps[i + 1:] if d["style"] == c["style"]]
            c["until"] = max(c.get("until", 0), min([c["end"] + 0.45] + [n - 0.02 for n in nxt]))
        for k, fr in enumerate(clip_frames(s, n)):
            gf = a + k
            if gf < f0: continue
            if gf >= f1: break
            t = gf / FPS
            if gf == 0:
                enc.stdin.write(poster.tobytes()); fidx += 1; continue      # poster = frame 0
            img = Image.fromarray(grade(fr, s["mode"], gf, s.get("insert43", False), s["id"] in MONO)).convert("RGBA")
            for ci, c in enumerate(caps):
                if c["start"] - 0.05 <= t <= c["until"]:
                    render_caption(img, c, t, s["id"], ci)
            osd(img, s, t)
            fade = 1.0
            if t > SONG_END - 1.2: fade = max(0.0, (SONG_END - t) / 1.2)
            arr = np.asarray(img.convert("RGB"))
            if fade < 1.0: arr = (arr.astype(np.float32) * fade).astype(np.uint8)
            enc.stdin.write(arr.tobytes()); fidx += 1
        print(f"{s['id']} done ({fidx} frames)", flush=True)
    enc.stdin.close(); enc.wait()
    print("wrote", out)

if __name__ == "__main__":
    main()
