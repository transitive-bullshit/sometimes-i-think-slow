"""Create the "Sometimes I Think Slow" page in the Projects database (TransitiveBullsh.it CMS) via the Notion REST API.

`prepare` builds the page's images into video/notion/: stills from the cut, the storyboard grid, the model sheets before
and after the Samurai Champloo redirect, the 2029 -> 4029 text drift, and a card from the round-2 scene review.
`publish` uploads them and the share cut to Notion (multi-part for the video; every file is a native Notion upload, and
only the original song's YouTube video is embedded by URL), then creates the page as a draft for review: Public and
Featured stay off and Published stays empty. It refuses to create a second page with the same slug.

usage: publish_notion.py prepare | publish [--dry]
env:   NOTION_API_TOKEN, NOTION_API_VERSION (an integration with access to the Projects database)
"""
import io, json, math, mimetypes, os, pathlib, re, subprocess, sys, tempfile, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "video/notion"
MASTER = ROOT / "video/out/fast-and-slow.mp4"
SHARE = ROOT / "video/out/fast-and-slow_share.mp4"
DATA_SOURCE = "6ffedb27-f124-8259-8a40-075b8e5a4993"          # Projects
AUTHOR = "b036f7f6-95a9-4f97-b3b5-c46867d0d103"               # Travis
SLUG = "sometimes-i-think-slow-ai-music-video"
ORIGINAL_YT = "https://www.youtube.com/watch?v=dkl_Vq1SWKg"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
REVIEW_URL = "http://localhost:8775/video/review/index.html"   # scripts/serve.py, with the round-2 review built
REVIEW_CARD = (888, 2412, 1752, 3627)                           # the S03 card at 1320 px wide, 2x (layout-dependent)
FILES = ["cover.jpg", "kahneman.jpg", "verse1.jpg", "verse2.jpg", "characters.jpg", "storyboard.jpg", "review.png", "drift.jpg"]

# ---------------------------------------------------------------- prepare
def frame(video, t):
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-f", "image2pipe",
                          "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    from PIL import Image
    return Image.open(io.BytesIO(png)).convert("RGB")

def row(ims, gap=16):
    from PIL import Image
    h = min(im.height for im in ims)
    ims = [im.resize((round(im.width * h / im.height), h), Image.LANCZOS) for im in ims]
    out = Image.new("RGB", (sum(im.width for im in ims) + gap * (len(ims) - 1), h), (17, 17, 17))
    x = 0
    for im in ims: out.paste(im, (x, 0)); x += im.width + gap
    return out

def stack(rows, gap=16):
    from PIL import Image
    w = min(r.width for r in rows)
    rows = [r.resize((w, round(r.height * w / r.width)), Image.LANCZOS) for r in rows]
    out = Image.new("RGB", (w, sum(r.height for r in rows) + gap * (len(rows) - 1)), (17, 17, 17))
    y = 0
    for r in rows: out.paste(r, (0, y)); y += r.height + gap
    return out

def save(im, name, width=None, quality=88):
    from PIL import Image
    if width and im.width > width: im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(OUT / name, quality=quality) if name.endswith(".jpg") else im.save(OUT / name)
    print(f"{name}: {im.width}x{im.height}, {(OUT / name).stat().st_size // 1024} KB")

def storyboard_grid(cols=11, cw=320, ch=180, strip=8, gap=8):
    """Every approved storyboard keyframe in song order, each with a strip in its mode's color."""
    from PIL import Image, ImageOps
    colors = {"hook": (242, 179, 61), "fast": (255, 106, 19), "slow": (119, 113, 106), "sunrise": (255, 184, 107),
              "transition": (190, 150, 90)}
    shots = json.loads((ROOT / "video/storyboard/shots.json").read_text())["shots"]
    rows = math.ceil(len(shots) / cols)
    out = Image.new("RGB", (cols * cw + (cols - 1) * gap, rows * (ch + strip) + (rows - 1) * gap), (17, 17, 17))
    for i, s in enumerate(shots):
        thumb = ImageOps.pad(Image.open(ROOT / "video/storyboard" / s["frame"]).convert("RGB"), (cw, ch), color=(0, 0, 0))
        x, y = (i % cols) * (cw + gap), (i // cols) * (ch + strip + gap)
        out.paste(thumb, (x, y)); out.paste(Image.new("RGB", (cw, strip), colors.get(s["mode"], (90, 90, 90))), (x, y + ch))
    return out

def review_card():
    """A card from the round-2 scene review, as the page renders it. Needs Chrome and scripts/serve.py on port 8775."""
    from PIL import Image
    full = OUT / "review-full.png"
    if not full.exists():
        p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
                              "--force-device-scale-factor=2", "--window-size=1320,3000", "--virtual-time-budget=6000",
                              f"--user-data-dir={tempfile.mkdtemp()}", f"--screenshot={full}", REVIEW_URL],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(120):                  # Chrome writes the screenshot, then can hang on the page's <video> elements
            if full.exists() and full.stat().st_size: time.sleep(2); break
            time.sleep(1)
        p.kill()
    return Image.open(full).convert("RGB").crop(REVIEW_CARD)

def prepare():
    from PIL import Image
    OUT.mkdir(parents=True, exist_ok=True)
    save(Image.open(ROOT / "video/poster.png").convert("RGB"), "cover.jpg", width=2000, quality=90)
    save(frame(MASTER, 51.4), "kahneman.jpg")                                      # S20: the book
    save(row([frame(MASTER, 26.3), frame(MASTER, 33.7)]), "verse1.jpg", width=2400)  # S09 LOW vs HIGH, S12 the pager
    save(row([frame(MASTER, 112.6), frame(MASTER, 119.35)]), "verse2.jpg", width=2400)  # S43 Navier–Stokes, S46 the slip
    sheets = lambda *names: row([Image.open(ROOT / "video/concept" / n).convert("RGB") for n in names])
    save(stack([sheets("sheet-fast-nano.png", "sheet-slow-nano.png"), sheets("v2/sheet-fast-v2.png", "v2/sheet-slow-v2.png")]),
         "characters.jpg", width=2400)
    save(storyboard_grid(), "storyboard.jpg", quality=85)
    save(review_card(), "review.png")
    clips = ROOT / "video/clips"                                                    # same shot, same moment: render 1 vs the fix
    save(row([frame(clips / "kling3pro_alt/S17_orig.mp4", 1.2), frame(clips / "kling3pro/S17.mp4", 1.2)]), "drift.jpg", width=2400)

# ---------------------------------------------------------------- Notion API
def session():
    import requests
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {os.environ['NOTION_API_TOKEN']}",
                      "Notion-Version": os.environ.get("NOTION_API_VERSION", "2026-03-11")})
    return s

def api(S, method, path, **kw):
    for k in range(4):
        r = S.request(method, f"https://api.notion.com/v1/{path}", timeout=180, **kw)
        if r.status_code in (429, 502, 503, 504) and k < 3: time.sleep(2 + 4 * k); continue
        if r.status_code >= 300: raise RuntimeError(f"{method} {path}: {r.status_code} {r.text[:600]}")
        return r.json()

def upload(S, path, name=None):
    import requests
    name = name or path.name
    ctype = mimetypes.guess_type(name)[0] or "application/octet-stream"
    size, PART = path.stat().st_size, 10 * 1024 * 1024
    def send(url, payload, part=None):
        for k in range(4):
            try:
                r = S.post(url, files={"file": (name, payload, ctype)}, data={"part_number": str(part)} if part else None, timeout=900)
                if r.status_code < 300: return
                if k == 3: raise RuntimeError(f"send {name} part {part}: {r.status_code} {r.text[:400]}")
            except requests.RequestException:
                if k == 3: raise
            time.sleep(3 + 5 * k)
    if size <= 20 * 1024 * 1024:
        fu = api(S, "POST", "file_uploads", json={"mode": "single_part", "filename": name, "content_type": ctype})
        send(fu["upload_url"], path.read_bytes())
    else:
        n = math.ceil(size / PART)
        fu = api(S, "POST", "file_uploads", json={"mode": "multi_part", "number_of_parts": n, "filename": name, "content_type": ctype})
        with open(path, "rb") as f:
            for i in range(1, n + 1):
                send(fu["upload_url"], f.read(PART), part=i); print(f"   {name}: part {i}/{n}", flush=True)
        api(S, "POST", f"file_uploads/{fu['id']}/complete")
    print(f"uploaded {name} ({size / 1e6:.1f} MB)", flush=True)
    return fu["id"]

# ---------------------------------------------------------------- blocks
TOKEN = re.compile(r"(\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)")
def rt(s):
    """Inline markdown -> rich text: **bold**, *italic*, `code`, [text](url)."""
    out = []
    for part in TOKEN.split(s):
        if not part: continue
        ann, link = {}, None
        if part.startswith("[") and "](" in part: text, link = re.match(r"\[([^\]]+)\]\(([^)]+)\)", part).groups()
        elif part.startswith("**"): text, ann = part[2:-2], {"bold": True}
        elif part.startswith("`"): text, ann = part[1:-1], {"code": True}
        elif part.startswith("*") and len(part) > 2: text, ann = part[1:-1], {"italic": True}
        else: text = part
        obj = {"type": "text", "text": {"content": text, **({"link": {"url": link}} if link else {})}}
        if ann: obj["annotations"] = ann
        out.append(obj)
    return out
def blk(kind, body): return {"object": "block", "type": kind, kind: body}
def p(s): return blk("paragraph", {"rich_text": rt(s)})
def h2(s): return blk("heading_2", {"rich_text": rt(s)})
def h3(s): return blk("heading_3", {"rich_text": rt(s)})
def bullet(s, kids=None): return blk("bulleted_list_item", {"rich_text": rt(s), **({"children": kids} if kids else {})})
def num(s, kids=None): return blk("numbered_list_item", {"rich_text": rt(s), **({"children": kids} if kids else {})})
def divider(): return blk("divider", {})
def callout(s, emoji): return blk("callout", {"rich_text": rt(s), "icon": {"type": "emoji", "emoji": emoji}, "color": "gray_background"})
def toggle(s, kids): return blk("toggle", {"rich_text": rt(s), "children": kids})
def code(s): return blk("code", {"rich_text": [{"type": "text", "text": {"content": s}}], "language": "plain text"})
def media(kind, fid, cap): return blk(kind, {"type": "file_upload", "file_upload": {"id": fid}, "caption": rt(cap)})
def youtube(url, cap): return blk("video", {"type": "external", "external": {"url": url}, "caption": rt(cap)})

def suno_style():
    """The style prompt the final take used ("A. 1991 faithful") and the exclude list, from suno/README.md."""
    blocks = re.findall(r"```\n(.*?)\n```", (ROOT / "suno/README.md").read_text(), re.S)
    return blocks[0], blocks[-1]

def content(f):
    style, excludes = suno_style()
    return [
        media("video", f["video"], "video created by claude opus 5.5; song made with suno v6"),
        divider(),
        h2("Two ways to think"),
        p("Daniel Kahneman’s [Thinking, Fast and Slow](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow) splits the mind in two. "
          "System 1 is fast, automatic, and confidently wrong about the bat and the ball. System 2 is slow, deliberate, and expensive."),
        p("For most of their short history, language models answered like System 1: one forward pass per token, and the first "
          "thought is the answer. Then in 2024, OpenAI’s o1 showed that a model keeps getting better "
          "[the longer it thinks before answering](https://openai.com/index/learning-to-reason-with-llms/). Thinking time became "
          "a second way to scale AI, right next to training."),
        p("Nice & Smooth’s 1991 classic “Sometimes I Rhyme Slow” was already that duo. Greg Nice is quick and bouncy; Smooth B "
          "is low, silky, and takes his time. Swap one word, and the hook explains the whole idea."),
        youtube(ORIGINAL_YT, "The original: Nice & Smooth, “Sometimes I Rhyme Slow” (1991)"),
        p("It’s a follow-up to [Slow It Down](https://www.transitivebullsh.it/projects/slow-it-down-ai-music-video), my first "
          "AI-made music video, and it was made the same way: Claude Code directing, me giving notes."),
        h2("Meet FAST & SLOW"),
        media("image", f["kahneman.jpg"], "“Kahneman wrote a whole book on why I’m problematic.”"),
        p("**FAST** is System 1: a skater with a wild mane who answers before you finish asking. **SLOW** is System 2: a ronin "
          "with a notebook who takes three minutes and gets it right. They’re twins (same data, same weights) with the love-hate "
          "energy of [Samurai Champloo](https://en.wikipedia.org/wiki/Samurai_Champloo)’s Mugen and Jin: they bicker, roast each "
          "other, and work best together."),
        p("**Verse 1 is FAST’s world,** in saturated 90s color: two thousand tokens a second, “low effort still beat your high,” "
          "[Andrej Karpathy’s](https://x.com/karpathy/status/2102124533729955960) “no thinking, single token, low latency” on a "
          "pager, a confident “twenty twenty-nine” for today’s date, and the bat and the ball. (*Ball’s a dime.* It’s a nickel.)"),
        media("image", f["verse1.jpg"], "“Low effort still beat your high,” and a page from Karpathy."),
        p("**Verse 2 is SLOW’s story,** in black-and-white sumi-e ink wash, with FAST as the only color in his memories. SLOW was "
          "ten thousand agents deep on Navier–Stokes while his twin was in the replies cracking jokes, telling the whole world to "
          "put glue on pizza, and special-casing the tests. So SLOW sends him off to RL with verifiable goals, and a year later he "
          "comes home… guessing again."),
        media("image", f["verse2.jpg"], "SLOW, ten thousand agents deep on Navier–Stokes. FAST, on a banana peel under a Gary Marcus headline."),
        p("By the last hook it’s sunrise, and the twins share one mixing desk: one fader on LOW, one on MAX."),
        p("Real people only ever appear as in-world text: a pager, a CRT, a newspaper headline, a book cover. The captions live in "
          "the world too. FAST’s lines are spray-painted tags, SLOW’s are handwriting, and the hook is painted sign lettering."),
        h2("How it was made"),
        p("Claude Code with **Opus 5.5** made nearly all of it: the research, the lyrics, the art direction, the storyboard, every "
          "image and video prompt, the compositor, and the review tools. My job was taste and feedback, at three checkpoints: the "
          "art direction, the storyboard, and the video. Start to finish took about a day of back-and-forth and roughly $60 of "
          "fal credits."),
        num("**Lyrics.** Rewritten line by line against the original’s bars, syllables, and rhyme scheme, and packed with "
            "references from the last two years of AI."),
        num("**Song.** Generated from scratch in Suno V6 from text alone: our lyrics plus a style prompt describing a laid-back 1991 "
            "New York boom-bap record, without naming the original."),
        num("**Timing.** Word-level timestamps for the Suno take, so every caption lands on its word."),
        num("**Characters.** One model sheet each for FAST and SLOW, passed into every image.",
            [media("image", f["characters.jpg"], "The first model sheets (top), and the final ones (bottom) after I asked for more "
                                                 "Mugen and Jin. Same wardrobe, new attitude.")]),
        num("**Storyboard.** 66 shots, each starting on its lyric, with one keyframe per shot from Nano Banana Pro. The color "
            "follows the mode: dusk for the hooks, saturated for FAST, ink wash for SLOW, and gold at sunrise.",
            [media("image", f["storyboard.jpg"], "The approved storyboard: 66 keyframes in song order, color-coded by mode.")]),
        num("**Clips.** Kling 3 Pro for color and action, and Wan 3.0 for SLOW’s calmer ink-wash shots."),
        num("**Compositing.** A local compositor lays the clips on the song, grades each mode, adds VHS grain and scanlines, and "
            "animates every caption word by word."),
        num("**Review.** A scene-by-scene review tool with **Approve** and **Change** on every shot, plus a notes box. 59 of 66 "
            "shots passed the first full render, and my notes on the other seven became round two.",
            [media("image", f["review.png"], "Round two: my real note on the crew shot, and what changed. **Show render 1** "
                                             "swaps back to the old take.")]),
        num("**Poster.** The end card doubles as the first frame, since X shows a video’s first frame as its preview."),
        h3("Tried and cut"),
        callout("None of this made it into the final video.", "🗑️"),
        bullet("**Voice auditions.** Before Suno, I auditioned AI rap voices from Lyria 3.5 and 3 Pro, MiniMax Music 2.6 and 3, "
               "ACE-Step, ElevenLabs, and Seed-VC. None of them had the laid-back 1991 delivery."),
        bullet("**Lip-sync.** OmniHuman 1.5 lip-synced nine close-ups. The cut plays better without them."),
        bullet("**Other video models.** Veo 3.1 Lite was faithful but tamer, and PixVerse v6 reframed shots and drifted off-model."),
        bullet("**Other image models.** Seedream 5 Pro was in the first style bake-off, next to Krea 2 and Nano Banana Pro."),
        h2("What I learned"),
        bullet("**Video models rewrite in-world text.** Kling kept “improving” FAST’s 2029 until it read 4029. Pinning the approved "
               "keyframe as the clip’s last frame fixed it, and anything that must never change gets pasted back from the keyframe.",
               [media("image", f["drift.jpg"], "Same shot, same moment: render one’s 4029 (left), and the fix with the keyframe "
                                               "pinned as the last frame (right).")]),
        bullet("**Watch the last second of every clip.** That’s where faces drift off-model and cameras cut away. We used only the "
               "clean part, slowed to fit the shot."),
        bullet("**One model per look.** Kling was best for action and keeping faces on-model. Wan was just as good, at about a third "
               "of the price, for calm ink-wash shots."),
        bullet("**Put real people in the world, not on screen.** A pager, a CRT post, a newspaper, and a book cover carry every "
               "reference without anyone’s face."),
        h3("Suno: what worked"),
        p("Suno made the song from text alone. For anyone making their own:"),
        bullet("**Spell names the way they should be sung.** The lyrics say “Ahn-dray,” “Kah-nuh-mun,” and “Nav-yay Stokes,” and the "
               "captions switch back to the real spellings."),
        bullet("**Describe the sound, never the artist.** The style prompt gives the era, tempo, key, instruments, and delivery."),
        bullet("**Spell out the hook in the style prompt too,** call and response included."),
        toggle("The style prompt", [code(style)]),
        toggle("Exclude styles", [code(excludes)]),
        divider(),
        p("*Parody. Not affiliated with Nice & Smooth, any AI lab, or anyone it name-checks.*"),
    ]

PROPS = {
    "Name": {"title": [{"type": "text", "text": {"content": "Sometimes I Think Slow – AI Music Video"}}]},
    "Description": {"rich_text": [{"type": "text", "text": {"content": "System 1 and System 2 trade verses in this AI-made hip-hop parody."}}]},
    "Slug": {"rich_text": [{"type": "text", "text": {"content": SLUG}}]},
    "Type": {"select": {"name": "Video"}},
    "Tags": {"multi_select": [{"name": "AI"}, {"name": "Video"}, {"name": "Projects"}]},
    "Author": {"people": [{"object": "user", "id": AUTHOR}]},
    "Source": {"url": "https://github.com/transitive-bullshit/sometimes-i-think-slow"},
    "Public": {"checkbox": False},
    "Featured": {"checkbox": False},
}

def plain(blocks, depth=0):
    """The page as indented plain text, for proofreading a dry run."""
    lines = []
    for b in blocks:
        body = b[b["type"]]
        text = "".join(r["text"]["content"] for r in body.get("rich_text", body.get("caption", [])))
        tag = {"heading_2": "## ", "heading_3": "### ", "numbered_list_item": "1. ", "bulleted_list_item": "- ", "divider": "---",
               "callout": "> ", "toggle": "▸ ", "code": "```", "image": "[image] ", "video": "[video] "}.get(b["type"], "")
        lines.append("  " * depth + tag + (text if b["type"] != "code" else f"{len(text)} chars```"))
        lines += plain(body.get("children", []), depth + 1)
    return lines

def publish(dry):
    for n in FILES: assert (OUT / n).exists(), f"missing {OUT / n}: run `publish_notion.py prepare`"
    if dry:
        print("\n".join(plain(content({"video": "dry", **{n: "dry" for n in FILES}})))); return
    S = session()
    existing = api(S, "POST", f"data_sources/{DATA_SOURCE}/query", json={"filter": {"property": "Slug", "rich_text": {"equals": SLUG}}})["results"]
    if existing: sys.exit(f"a page with slug {SLUG} already exists: {existing[0]['url']} (not creating a duplicate)")
    ids = {n: upload(S, OUT / n) for n in FILES}
    ids["video"] = upload(S, SHARE, name="sometimes-i-think-slow.mp4")
    blocks = content(ids)
    page = api(S, "POST", "pages", json={"parent": {"type": "data_source_id", "data_source_id": DATA_SOURCE},
                                         "icon": {"type": "emoji", "emoji": "🎬"},
                                         "cover": {"type": "file_upload", "file_upload": {"id": ids["cover.jpg"]}},
                                         "properties": PROPS, "children": blocks[:90]})
    for i in range(90, len(blocks), 90):
        api(S, "PATCH", f"blocks/{page['id']}/children", json={"children": blocks[i:i + 90]})
    print("created", page["url"], "with", len(blocks), "top-level blocks")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "prepare": prepare()
    elif cmd == "publish": publish("--dry" in sys.argv)
    else: sys.exit(__doc__)
