"""Transcribe the chosen Suno take and pin every scripted lyric line to exact times and bars.

Steps (each cached, so reruns are cheap):
  1. beat_this beats/downbeats on the mix -> constant-tempo grid (grid.py's fit)
  2. vocal stem via audio-separator (ONNX MDX on CPU/ANE; the GPU path stalls when other sessions share it)
  3. Whisper large-v3-turbo word timestamps on the stem, in a subprocess (MLX + torch-MPS can deadlock)
  4. align Whisper words to the script (Suno spelling for matching, display spelling for captions)
Outputs to analysis/suno/: grid.json, words.json, lyrics-timed.json, lyrics.lrc

usage: suno_transcribe.py [audio=audio/suno/final-take.wav]
"""
import json, os, re, subprocess, sys, difflib, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "audio/suno/final-take.wav"
OUT = ROOT / "analysis/suno"; OUT.mkdir(parents=True, exist_ok=True)
STEM_DIR = ROOT / "audio/suno/stems"; STEM_DIR.mkdir(parents=True, exist_ok=True)
PY = str(ROOT / ".venv/bin/python")

def grid():
    path = OUT / "grid.json"
    if path.exists(): return json.load(open(path))
    code = f"""
import json, numpy as np
from beat_this.inference import File2Beats
b, d = File2Beats(checkpoint_path="final0", device="cpu", dbn=False)({str(SRC)!r})
json.dump({{"beats": [float(x) for x in b], "downbeats": [float(x) for x in d]}}, open({str(OUT / 'beats-raw.json')!r}, "w"))
"""
    subprocess.run([PY, "-c", code], check=True)
    raw = json.load(open(OUT / "beats-raw.json"))
    b, db = np.array(raw["beats"]), np.array(raw["downbeats"])
    P = float(np.median(np.diff(db))) / 4; t0 = db[0]
    for _ in range(8):
        k = np.round((b - t0) / P); m = np.abs(b - (t0 + k * P)) < 0.05
        (t0, P), *_ = np.linalg.lstsq(np.vstack([np.ones(m.sum()), k[m]]).T, b[m], rcond=None)
    kd = np.round((db - t0) / P).astype(int) % 4
    phase = int(np.bincount(kd, minlength=4).argmax())
    bar0 = t0 + phase * P
    while bar0 - 4 * P > -P: bar0 -= 4 * P
    resid = b - (t0 + np.round((b - t0) / P) * P)
    g = {"bpm": 60 / P, "beat_s": P, "bar_s": 4 * P, "first_bar_line_s": float(bar0),
         "inliers_30ms": float(np.mean(np.abs(resid) < 0.03)), "n_beats": len(b)}
    json.dump(g, open(path, "w"), indent=1)
    return g

def vocal_stem():
    out = STEM_DIR / "final-take_vocals.wav"
    if out.exists(): return out
    code = f"""
from audio_separator.separator import Separator
s = Separator(model_file_dir={str(ROOT / 'audio/models')!r}, output_dir={str(STEM_DIR)!r}, output_format="WAV", use_soundfile=True)
s.load_model("UVR-MDX-NET-Voc_FT.onnx")
s.separate({str(SRC)!r}, {{"Vocals": "final-take_vocals", "Instrumental": "final-take_instrumental"}})
"""
    subprocess.run([PY, "-c", code], check=True, capture_output=True)
    return out

def whisper(stem):
    path = OUT / "words.json"
    if path.exists(): return json.load(open(path))
    code = f"""
import json, mlx_whisper
r = mlx_whisper.transcribe({str(stem)!r}, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en",
                           word_timestamps=True, condition_on_previous_text=False, no_speech_threshold=0.4,
                           initial_prompt="Sometimes I think slow, sometimes I think fast. System One. Kahneman. Andrej. Navier-Stokes. RL. Gary Marcus. Abilene.")
json.dump([dict(w=w["word"].strip(), s=round(w["start"], 3), e=round(w["end"], 3), p=round(w.get("probability", 0), 3))
           for seg in r["segments"] for w in seg.get("words", [])], open({str(path)!r}, "w"), indent=0)
"""
    subprocess.run([PY, "-c", code], check=True)
    return json.load(open(path))

norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower().replace("-", ""))

def script_lines():
    """(section, suno_line, display_line) for every sung line; tags and the [End] marker skipped."""
    suno = (ROOT / "suno/lyrics-v3-suno.txt").read_text().splitlines()
    disp = (ROOT / "suno/lyrics-v3-display.txt").read_text().splitlines()
    rows, section = [], None
    for a, b in zip(suno, disp):
        if a.startswith("["):
            section = a.strip("[]").split(":")[0]; continue
        if a.strip(): rows.append((section, a.strip(), b.strip()))
    return rows

def align(words, rows, g):
    toks = [(i, norm(t)) for i, (_, l, _) in enumerate(rows) for t in l.split() if norm(t)]
    hw = [norm(w["w"]) for w in words]
    sm = difflib.SequenceMatcher(a=[t for _, t in toks], b=hw, autojunk=False)
    t_of = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): t_of[blk.a + k] = blk.b + k
    lines = []
    for li, (sec, suno_l, disp_l) in enumerate(rows):
        idx = [n for n, (i, _) in enumerate(toks) if i == li]
        hits = [t_of[n] for n in idx if n in t_of]
        start = words[hits[0]]["s"] if hits else None
        end = words[hits[-1]]["e"] if hits else None
        lines.append({"section": sec, "text": disp_l, "suno_text": suno_l, "start": start, "end": end,
                      "coverage": round(len(hits) / max(1, len(idx)), 2), "n_words": len(idx),
                      "word_times": [[toks[n][1], words[t_of[n]]["s"], words[t_of[n]]["e"]] for n in idx if n in t_of]})
    # fill gaps: lines Whisper missed get the time between their neighbours
    for i, L in enumerate(lines):
        if L["start"] is None:
            prev = next((lines[j]["end"] for j in range(i - 1, -1, -1) if lines[j]["end"] is not None), 0.0)
            nxt = next((lines[j]["start"] for j in range(i + 1, len(lines)) if lines[j]["start"] is not None), prev + 2)
            L["start"], L["end"], L["estimated"] = prev, nxt, True
    T0, BAR = g["first_bar_line_s"], g["bar_s"]
    for L in lines:
        x = (L["start"] - T0) / BAR
        L["bar"] = round(x + 1, 2)
    matched = sum(1 for n in range(len(toks)) if n in t_of)
    return lines, matched / len(toks)

if __name__ == "__main__":
    g = grid()
    print(f"tempo {g['bpm']:.2f} BPM, bar {g['bar_s']:.3f}s, bar 1 at {g['first_bar_line_s']:.3f}s, grid inliers {g['inliers_30ms']:.0%}")
    stem = vocal_stem(); print("vocal stem:", stem.name)
    words = whisper(stem); print("whisper words:", len(words))
    lines, acc = align(words, script_lines(), g)
    src = SRC.resolve(); src = src.relative_to(ROOT) if src.is_relative_to(ROOT) else src.name   # no local paths in outputs
    json.dump({"source": str(src), "grid": g, "word_match": round(acc, 3), "lines": lines},
              open(OUT / "lyrics-timed.json", "w"), indent=1)
    with open(OUT / "lyrics.lrc", "w") as f:
        for L in lines:
            m, s = divmod(L["start"], 60)
            f.write(f"[{int(m):02d}:{s:05.2f}]{L['text']}\n")
    print(f"script words heard in order: {acc:.0%}")
    sec = None
    for L in lines:
        if L["section"] != sec:
            sec = L["section"]; print(f"--- {sec}")
        flag = " (est.)" if L.get("estimated") else ("  <- weak" if L["coverage"] < 0.6 else "")
        print(f"{L['start']:7.2f}-{L['end']:7.2f}  bar {L['bar']:6.2f}  cov {L['coverage']:.0%}  {L['text'][:64]}{flag}")
