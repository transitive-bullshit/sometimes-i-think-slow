"""Static file server with HTTP Range support, so <audio> players can seek, plus a tiny feedback store.

Python's built-in http.server ignores Range headers and always sends the whole file with 200. Browsers then can't
seek. This answers "Range: bytes=..." with 206 Partial Content.

Review pages POST their feedback to /api/feedback/<name>. It lands in video/<name>/feedback.json, with a
timestamped copy in history/ (skipped for ?autosave=1), so Claude can read it straight from disk. GET on the same path
returns it.

usage: serve.py [directory=.]        port from $PORT (the preview launcher assigns one), else 8765
"""
import json, os, re, sys, time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

RANGE = re.compile(r"bytes=(\d*)-(\d*)$")
FEEDBACK = re.compile(r"^/api/feedback/([a-z0-9-]+)$")

class RangeHandler(SimpleHTTPRequestHandler):
    def _feedback_path(self):
        m = FEEDBACK.match(self.path.split("?")[0])
        return os.path.join(self.directory, "video", m.group(1), "feedback.json") if m else None

    def do_GET(self):
        path = self._feedback_path()
        if path is None: return super().do_GET()
        body = open(path, "rb").read() if os.path.exists(path) else b"{}"
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_POST(self):
        path = self._feedback_path()
        n = int(self.headers.get("Content-Length", 0))
        if path is None or not os.path.isdir(os.path.dirname(path)) or n > 5_000_000:
            self.send_error(404 if path is None else 400); return
        data = json.loads(self.rfile.read(n) or b"{}")
        data["saved_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        text = json.dumps(data, indent=1)
        open(path, "w").write(text)
        if "autosave=1" not in self.path:                # explicit saves also keep a snapshot; autosaves just overwrite
            os.makedirs(os.path.join(os.path.dirname(path), "history"), exist_ok=True)
            open(os.path.join(os.path.dirname(path), "history", f"feedback-{time.strftime('%Y%m%d-%H%M%S')}.json"), "w").write(text)
        body = json.dumps({"ok": True, "saved_at": data["saved_at"]}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def send_head(self):
        path = self.translate_path(self.path)
        m = RANGE.match(self.headers.get("Range", "").strip())
        if not m or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        first, last = m.groups()
        if first == "":                                  # suffix range: the last N bytes
            start, end = max(0, size - int(last or 0)), size - 1
        else:
            start, end = int(first), min(int(last), size - 1) if last else size - 1
        if start >= size or start > end:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return None
        f = open(path, "rb")
        f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        self._remaining = end - start + 1
        return f

    def copyfile(self, source, outputfile):
        remaining = getattr(self, "_remaining", None)
        if remaining is None:
            return super().copyfile(source, outputfile)
        while remaining > 0:
            chunk = source.read(min(64 * 1024, remaining))
            if not chunk: break
            outputfile.write(chunk)
            remaining -= len(chunk)
        self._remaining = None

    def end_headers(self):
        if not self.headers.get("Range"):              # advertise ranges on plain 200s too
            self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-cache")  # regenerated pages/mixes show up on a plain reload
        super().end_headers()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8765))
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    ThreadingHTTPServer(("127.0.0.1", port), partial(RangeHandler, directory=directory)).serve_forever()
