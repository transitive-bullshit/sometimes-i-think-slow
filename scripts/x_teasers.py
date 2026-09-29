"""Short teasers for X: three chorus-led excerpts of the final cut, each opening on a poster made for the feed.

X shows a video's first frame until it plays, so every teaser opens on its own poster: a clean keyframe from the cut,
graded like the cut, with a few words in the video's own lettering. Each cut starts and ends in a gap in the vocal stem
so no word is clipped. The picture comes from the share encode and the sound from the Suno WAV, both on song time.
Nothing in the storyboard or the main cut changes.

usage: x_teasers.py [ids...]    (default: all) -> video/out/x/<id>.mp4, <id>_poster.png/.jpg, and posters.jpg (feed-size check)
"""
import itertools, pathlib, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from compose import W, H, FPS, font, grade          # the cut's grade and fonts, so the posters match it

SHARE = ROOT / "video/out/fast-and-slow_share.mp4"
SONG = ROOT / "audio/suno/final-take.wav"
FRAMES = ROOT / "video/storyboard/frames"
OUT = ROOT / "video/out/x"
POSTER_FRAMES = 3     # a hair past frame 0, in case a preview is grabbed a frame or two in

# t0/t1 in song seconds, both in vocal gaps (checked on the vocal stem). fade = audio fade-out, ending at `mute` or t1.
TEASERS = {
    # hook 1 exactly as the video opens: the chorus under the train-time / test-time charts, out before verse 1's pickup
    "a-cold-open": dict(t0=0.0, t1=16.95, fade=0.45, shot="S02", mode="hook"),
    # FAST's last line ("Snap judgment... FAST!") into hook 2, out on the warm/cool face-off before SLOW's call
    "b-face-off": dict(t0=56.0, t1=68.4, fade=0.40, shot="S26", mode="hook"),
    # hook 3's low/max line, the outro, and the spoken tag; the tag card holds in silence before the end-card beat returns
    "c-thought-for-3-minutes": dict(t0=149.5, t1=172.2, fade=0.08, mute=171.15, shot="S60", mode="sunrise",
                                    hold=149.7),  # the first 0.2 s is the crane shot's tail: hold S60's first frame instead
}

# ---------------------------------------------------------------- lettering
def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def glow(img, text, f, xy, anchor, radius, alpha=150, stroke=None):
    """A soft dark bloom behind a word, so it reads on any part of the frame."""
    g = layer()
    ImageDraw.Draw(g).text(xy, text, font=f, anchor=anchor, fill=(0, 0, 0, alpha), stroke_width=stroke or radius // 2,
                           stroke_fill=(0, 0, 0, alpha))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(radius)))

def spray(img, text, xy, size, angle):
    """FAST's lettering: the verse captions' spray tag (orange, teal drop, dark rim), scaled up and tilted."""
    f = font("PermanentMarker-Regular.ttf", size); s = size / 66
    lay = layer(); d = ImageDraw.Draw(lay)
    d.text((xy[0] + 4 * s, xy[1] + 5 * s), text, font=f, anchor="mm", fill=(15, 111, 108, 255))
    d.text(xy, text, font=f, anchor="mm", fill=(255, 122, 26, 255), stroke_width=int(2 * s), stroke_fill=(58, 13, 0, 255))
    glow(img, text, f, xy, "mm", 22)
    img.alpha_composite(lay.rotate(angle, center=xy, resample=Image.BICUBIC))

def ink(img, text, xy, size, angle):
    """SLOW's lettering: the verse captions' handwriting (cream on an ink-bleed halo), scaled up."""
    f = font("Caveat[wght].ttf", size); s = size / 78
    halo = layer()
    ImageDraw.Draw(halo).text(xy, text, font=f, anchor="mm", fill=(20, 16, 12, 170), stroke_width=int(7 * s),
                              stroke_fill=(20, 16, 12, 170))
    lay = halo.filter(ImageFilter.GaussianBlur(9 * s)); d = ImageDraw.Draw(lay)
    d.text((xy[0] + 2 * s, xy[1] + 4 * s), text, font=f, anchor="mm", fill=(0, 0, 0, 170))
    d.text(xy, text, font=f, anchor="mm", fill=(245, 239, 226, 255))
    img.alpha_composite(lay.rotate(angle, center=xy, resample=Image.BICUBIC))

def sign(img, text, xy, size, fill):
    """The hooks' sign lettering (Bungee, hard offset shadow)."""
    f = font("Bungee-Regular.ttf", size); s = size / 66
    glow(img, text, f, xy, "mm", 18, alpha=120)
    d = ImageDraw.Draw(img)
    d.text((xy[0] + 6 * s, xy[1] + 6 * s), text, font=f, anchor="mm", fill=(27, 24, 20, 255))
    d.text(xy, text, font=f, anchor="mm", fill=fill)

def typed(img, text, xy, size):
    """The tag card's typewriter line on a closed-caption box, cursor on, like a model's thinking readout."""
    f = font("SpecialElite-Regular.ttf", size); d = ImageDraw.Draw(img)
    cw = f.getlength("M") * 0.62; tw = f.getlength(text)
    x0, y = xy[0] - (tw + cw + 10) / 2, xy[1]
    d.rectangle([x0 - 34, y - size * 0.80, x0 + tw + cw + 44, y + size * 0.72], fill=(0, 0, 0, 205))
    d.text((x0, y + 3), text, font=f, anchor="lm", fill=(0, 0, 0, 200))
    d.text((x0, y), text, font=f, anchor="lm", fill=(240, 240, 235, 255))
    cx = x0 + tw + 10
    d.rectangle([cx, y - size * 0.42, cx + cw, y + size * 0.36], fill=(240, 240, 235, 235))

# One idea per poster, readable at phone size, kept off the faces and out of X's bottom corners (duration, mute).
def letter_a(img):   # the matchup: each lead named in his own verse's lettering, under his own chart
    spray(img, "FAST", (int(W * 0.215), int(H * 0.745)), 250, 6)
    ink(img, "Slow", (int(W * 0.735), int(H * 0.735)), 300, -3)

def letter_b(img):   # the face-off, named in Kahneman's terms, each half in its own light
    sign(img, "SYSTEM 1", (int(W * 0.245), int(H * 0.81)), 134, (255, 236, 204))
    sign(img, "SYSTEM 2", (int(W * 0.755), int(H * 0.81)), 134, (226, 238, 255))
    sign(img, "VS", (W // 2, int(H * 0.81)), 76, (255, 255, 255))

def letter_c(img):   # the tag the cut ends on, over the effort fader
    typed(img, "Thought for 3 minutes", (W // 2, int(H * 0.43)), 112)

LETTERING = {"a-cold-open": letter_a, "b-face-off": letter_b, "c-thought-for-3-minutes": letter_c}

def poster(tid, spec):
    im = ImageOps.fit(Image.open(FRAMES / f"{spec['shot']}.png").convert("RGB"), (W, H), Image.LANCZOS)
    img = Image.fromarray(grade(np.asarray(im), spec["mode"], 0, False)).convert("RGBA")
    LETTERING[tid](img)
    img = img.convert("RGB")
    img.save(OUT / f"{tid}_poster.png"); img.save(OUT / f"{tid}_poster.jpg", quality=92)
    return img

# ---------------------------------------------------------------- cut
def cut(tid, spec, post):
    n = int(round((spec["t1"] - spec["t0"]) * FPS)); dur = n / FPS
    end = spec.get("mute", spec["t1"]) - spec["t0"]
    af = (["afade=t=in:d=0.02"] if spec["t0"] > 0 else []) + [f"afade=t=out:st={end - spec['fade']:.3f}:d={spec['fade']:.3f}"]
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{spec['t0']:.3f}", "-i", str(SHARE), "-frames:v", str(n),
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-ss", f"{spec['t0']:.3f}", "-t", f"{dur:.3f}", "-i", str(SONG),
                            "-map", "0:v", "-map", "1:a", "-af", ",".join(af),
                            "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", str(OUT / f"{tid}.mp4")],
                           stdin=subprocess.PIPE)
    fb = W * H * 3
    src = iter(lambda: dec.stdout.read(fb), b"")
    hold = int(round((spec.get("hold", spec["t0"]) - spec["t0"]) * FPS))
    head = [next(src) for _ in range(hold + 1)]
    pb = np.asarray(post).tobytes()
    for k, buf in enumerate(itertools.chain([head[-1]] * (hold + 1), src)):   # held frames repeat the held shot's first
        if len(buf) < fb: break
        enc.stdin.write(pb if k < POSTER_FRAMES else buf)
    enc.stdin.close(); enc.wait(); dec.wait()
    print(f"wrote video/out/x/{tid}.mp4 ({dur:.2f} s, song {spec['t0']:.2f}-{spec['t1']:.2f})", flush=True)

def feed_sheet(posters):
    """The posters at roughly the width a phone's feed shows them, to check they still read."""
    w = 480; h = w * H // W
    sheet = Image.new("RGB", (len(posters) * (w + 16) + 16, h + 32), (21, 32, 43))
    for i, p in enumerate(posters): sheet.paste(p.resize((w, h), Image.LANCZOS), (16 + i * (w + 16), 16))
    sheet.save(OUT / "posters.jpg", quality=90)

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    ids = sys.argv[1:] or list(TEASERS)
    posters = []
    for tid in ids:
        post = poster(tid, TEASERS[tid]); posters.append(post)
        cut(tid, TEASERS[tid], post)
    feed_sheet(posters)
