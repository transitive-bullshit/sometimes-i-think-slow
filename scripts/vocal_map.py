"""Vocal stem -> line/bar map with a 16th-note flow skeleton per line.

Writes only structural data (timings, bar positions, syllable counts, onset grids, rhyme
vowels) to analysis/. The raw transcript is the original lyric text, so it stays in the
session scratchpad ($SCRATCH) and is never written into the project.

usage: SCRATCH=... vocal_map.py <vocals.wav> <grid.json> <out.json>
"""
import json, os, re, sys
import numpy as np
import librosa
import pronouncing, pyphen

VOC, GRID, OUT = sys.argv[1:4]
SCRATCH = os.environ["SCRATCH"]
g = json.load(open(GRID))
BEAT, BAR, T0 = g["beat_period_s"], g["bar_s"], g["first_bar_line_s"]
SIX = BEAT / 4

def barpos(t):
    """bar.beat.16th (all 1-based), bars counted from the first grid bar line."""
    x = (t - T0) / SIX
    n = int(round(x))
    bar, r = divmod(n, 16)
    return f"{bar + 1}.{r // 4 + 1}.{r % 4 + 1}", n

# --- syllable-ish onsets from the vocal stem (text-independent rhythm) ---
y, sr = librosa.load(VOC, sr=22050, mono=True)
hop = 128
env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop, aggregate=np.median)
on_t = librosa.onset.onset_detect(onset_envelope=env, sr=sr, hop_length=hop, units="time", backtrack=False, delta=0.08)
rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=hop)[0]
rms_db = 20 * np.log10(rms / rms.max() + 1e-9)
on_t = np.array([t for t in on_t if rms_db[min(int(t * sr / hop) + 3, len(rms_db) - 1)] > -30])

# --- whisper word timings (cached in scratch) ---
raw_path = os.path.join(SCRATCH, "whisper_raw.json")
if not os.path.exists(raw_path):
    import mlx_whisper
    res = mlx_whisper.transcribe(VOC, path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
                                 language="en", word_timestamps=True, condition_on_previous_text=False,
                                 no_speech_threshold=0.4, compression_ratio_threshold=2.6)
    json.dump(res, open(raw_path, "w"))
res = json.load(open(raw_path))

dic = pyphen.Pyphen(lang="en_US")
def phones(word):
    w = re.sub(r"[^a-z']", "", word.lower())
    ph = pronouncing.phones_for_word(w) if w else []
    return w, (ph[0] if ph else None)
def syl(word):
    w, ph = phones(word)
    if not w: return 0
    return pronouncing.syllable_count(ph) if ph else max(1, len(dic.inserted(w).split("-")))
def rhyme_vowel(word):
    """Last stressed vowel + tail in ARPAbet (e.g. 'OW1' / 'IH1 K'): a sound, not the word."""
    w, ph = phones(word)
    return pronouncing.rhyming_part(ph) if ph else None

lines = []
for seg in res["segments"]:
    words = [w for w in seg.get("words", []) if re.sub(r"[^A-Za-z']", "", w["word"])]
    if not words: continue
    s, e = words[0]["start"], words[-1]["end"]
    bp, n0 = barpos(s)
    _, n1 = barpos(e)
    ons = on_t[(on_t >= s - 0.08) & (on_t <= e + 0.02)]
    slots = sorted({barpos(t)[1] for t in ons})
    lines.append({"start_s": round(s, 2), "end_s": round(e, 2), "bar_pos": bp, "end_bar_pos": barpos(e)[0],
                  "len_16ths": n1 - n0, "syllables": sum(syl(w["word"]) for w in words), "n_words": len(words),
                  "onset_slots": slots, "rhyme_sound": rhyme_vowel(words[-1]["word"]),
                  "word_onsets_s": [round(w["start"], 2) for w in words],
                  "_tag": " ".join(w["word"].strip() for w in words[:3])})

def grid_str(slots, n0):
    """16th-note grid from the line's first bar line: x = onset, . = none, | = bar line."""
    b0 = (n0 // 16) * 16
    last = max(slots) if slots else n0
    cells = ["x" if (b0 + i) in set(slots) else "." for i in range(last - b0 + 1)]
    return "|".join("".join(cells[i:i + 16]) for i in range(0, len(cells), 16))

print(f"BPM {60/BEAT:.2f}  bar {BAR:.3f}s  16th {SIX*1000:.0f}ms  onsets {len(on_t)}  lines {len(lines)}")
for i, L in enumerate(lines):
    n0 = barpos(L["start_s"])[1]
    print(f"{i:3d} {L['start_s']:7.2f} {L['bar_pos']:>7} syl {L['syllables']:2d} rhyme {str(L['rhyme_sound']):>10}  "
          f"{grid_str(L['onset_slots'], n0):<52} [{L['_tag']}…]")
json.dump({"bpm": 60 / BEAT, "bar_s": BAR, "first_bar_line_s": T0,
           "lines": [{k: v for k, v in L.items() if k != "_tag"} for L in lines]},
          open(OUT, "w"), indent=1)
