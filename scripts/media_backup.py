"""Back up the media that isn't in git to R2, and restore it anywhere from the committed manifest.

The Suno take, the poster, the model sheets and style frames, the keyframes, the clips and the final cut are expensive
(or impossible) to regenerate, so they live in an S3-compatible bucket (Cloudflare R2) under content-addressed keys,
<prefix>/<sha256>.<ext>, cached as immutable. media/backup.json maps every local path to its public URL, size and
hash, and is committed. Restoring needs no credentials.

usage: media_backup.py upload [paths...]      needs S3_* in the environment (see .env.example); no paths = everything
       media_backup.py download [prefixes...] fetches missing or changed files, e.g. `download video/out`
       media_backup.py verify                 compares local files with the manifest
"""
import concurrent.futures as cf, hashlib, json, os, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "media/backup.json"
PREFIX = "sometimes-i-think-slow"
CACHE = "public,max-age=31536000,immutable"
BACKUP = [  # what a fresh clone needs to rebuild the cut, plus the cut itself
    "audio/suno/final-take.wav",
    "video/poster.png",
    "video/concept/v2/*.png",
    "video/storyboard/frames/*.png",
    "video/storyboard/frames_r2/*.png",
    "video/clips/kling3pro/*.mp4",
    "video/clips/kling3pro_alt/*.mp4",
    "video/clips/wan3/*.mp4",
    "video/out/fast-and-slow_share.mp4",   # the share encode, not the multi-GB master: compose.py rebuilds that
]
TYPES = {".png": "image/png", ".mp4": "video/mp4", ".wav": "audio/wav", ".jpg": "image/jpeg", ".webp": "image/webp"}

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()

def load():
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"prefix": PREFIX, "files": []}

def save(entries):
    MANIFEST.write_text(json.dumps({"prefix": PREFIX, "files": sorted(entries.values(), key=lambda e: e["path"])},
                                   indent=1) + "\n")

def upload(paths):
    import boto3
    from botocore.exceptions import ClientError
    env = os.environ
    s3 = boto3.client("s3", endpoint_url=env["S3_API_ENDPOINT"], aws_access_key_id=env["S3_ACCESS_KEY_ID"],
                      aws_secret_access_key=env["S3_SECRET_ACCESS_KEY"], region_name="auto")
    bucket, base = env["S3_BUCKET_NAME"], env["S3_PUBLIC_URL"].rstrip("/")
    todo = [ROOT / p for p in paths] or sorted({p for pat in BACKUP for p in ROOT.glob(pat) if p.is_file()})

    def one(p):
        digest = sha256(p); key = f"{PREFIX}/{digest}{p.suffix.lower()}"
        try:
            s3.head_object(Bucket=bucket, Key=key); status = "exists"
        except ClientError as err:
            if err.response.get("Error", {}).get("Code") not in ("404", "NoSuchKey", "NotFound"): raise
            s3.upload_file(str(p), bucket, key, ExtraArgs={"ContentType": TYPES.get(p.suffix.lower(), "application/octet-stream"),
                                                           "CacheControl": CACHE})
            status = "uploaded"
        return {"path": p.relative_to(ROOT).as_posix(), "url": f"{base}/{key}", "bytes": p.stat().st_size,
                "sha256": digest}, status

    entries = {e["path"]: e for e in load()["files"]} if paths else {}   # a full run rewrites the manifest
    with cf.ThreadPoolExecutor(8) as ex:
        for n, (e, status) in enumerate(ex.map(one, todo), 1):
            entries[e["path"]] = e
            print(f"[{n}/{len(todo)}] {status:8s} {e['path']} ({e['bytes'] / 1e6:.1f} MB)", flush=True)
    save(entries)
    print(f"manifest: {len(entries)} files, {sum(e['bytes'] for e in entries.values()) / 1e9:.2f} GB -> {MANIFEST.relative_to(ROOT)}")

def download(prefixes):
    import requests
    for e in load()["files"]:
        if prefixes and not any(e["path"].startswith(p) for p in prefixes): continue
        p = ROOT / e["path"]
        if p.exists() and p.stat().st_size == e["bytes"] and sha256(p) == e["sha256"]: continue
        p.parent.mkdir(parents=True, exist_ok=True); tmp = p.with_name(p.name + ".part")
        with requests.get(e["url"], stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(1 << 20): f.write(chunk)
        if sha256(tmp) != e["sha256"]: tmp.unlink(); sys.exit(f"hash mismatch for {e['path']}")
        tmp.replace(p); print("restored", e["path"], flush=True)

def verify():
    bad = [e["path"] for e in load()["files"]
           if not (ROOT / e["path"]).exists() or sha256(ROOT / e["path"]) != e["sha256"]]
    print("all files match the manifest" if not bad else f"{len(bad)} missing or changed:\n  " + "\n  ".join(bad))
    return not bad

if __name__ == "__main__":
    cmd, args = (sys.argv[1] if len(sys.argv) > 1 else "verify"), sys.argv[2:]
    if cmd == "upload": upload(args)
    elif cmd == "download": download(args)
    elif cmd == "verify": sys.exit(0 if verify() else 1)
    else: sys.exit(__doc__)
