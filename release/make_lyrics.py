"""Store lyrics for DistroKid: the written lyrics, not the Suno-coaxing spellings.

usage: python release/make_lyrics.py   ->   release/lyrics.txt
Lines and order come from analysis/suno/lyrics-timed.json, whose `text` is the real spelling (Andrej, Kahneman,
Navier–Stokes, RL) rather than `suno_text` (Ahn-dray, Kah-nuh-mun, Nav-yay Stokes, R-L). Lines Suno never sang are
dropped (the second repeat of the middle hook; Whisper hears a run of "fast"s there instead). Stretched vowels
("slooow") go back to plain words; "FAST!" keeps its caps because it's the character's name.
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
lines = json.loads((ROOT / "analysis/suno/lyrics-timed.json").read_text())["lines"]

groups, sec = [], None
for l in lines:
    if l["coverage"] == 0: continue
    if l["section"] != sec: groups.append([]); sec = l["section"]
    groups[-1].append(re.sub(r"\b([Ss])lo{2,}w", r"\1low", l["text"]))
(ROOT / "release/lyrics.txt").write_text("\n\n".join("\n".join(g) for g in groups) + "\n")
print("wrote release/lyrics.txt")
