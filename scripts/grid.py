"""Fit a constant-tempo beat grid to beat_this output and report where the track leaves it.

A sample-based 1991 record should sit on one fixed tempo; stretches that don't fit the
grid are edits, breaks, or tempo drift worth knowing about before we lay vocals on top.

usage: grid.py <beats.json> <out.json>
"""
import json, sys
import numpy as np

d = json.load(open(sys.argv[1]))
b, db = np.array(d["beats_s"]), np.array(d["downbeats_s"])
P = float(np.median(np.diff(db))) / 4          # beat period guess from downbeat spacing
t0 = db[0]
for _ in range(8):
    k = np.round((b - t0) / P)
    m = np.abs(b - (t0 + k * P)) < 0.05          # robust: fit inliers only
    A = np.vstack([np.ones(m.sum()), k[m]]).T
    (t0, P), *_ = np.linalg.lstsq(A, b[m], rcond=None)

k = np.round((b - t0) / P)
resid = b - (t0 + k * P)
# downbeat phase: which beat index mod 4 the tracked downbeats land on
kd = np.round((db - t0) / P).astype(int) % 4
phase = int(np.bincount(kd, minlength=4).argmax())
bar0 = t0 + phase * P                             # first grid downbeat at/after t0
while bar0 - 4 * P > -P: bar0 -= 4 * P            # extend back to the earliest bar line

off = np.abs(resid) > 0.04
regions, start = [], None
for i, o in enumerate(off):
    if o and start is None: start = i
    if not o and start is not None:
        if i - start >= 2: regions.append([round(float(b[start]), 2), round(float(b[i - 1]), 2), i - start])
        start = None
if start is not None and len(b) - start >= 2: regions.append([round(float(b[start]), 2), round(float(b[-1]), 2), len(b) - start])

res = {"beat_period_s": float(P), "bpm": float(60 / P), "bar_s": float(4 * P), "t0_s": float(t0),
       "first_bar_line_s": float(bar0), "downbeat_phase_votes": np.bincount(kd, minlength=4).tolist(),
       "inlier_frac_30ms": float(np.mean(np.abs(resid) < 0.03)),
       "resid_sd_ms": float(resid[np.abs(resid) < 0.05].std() * 1000),
       "off_grid_regions_s": regions}
json.dump(res, open(sys.argv[2], "w"), indent=1)
print(f"BPM {60/P:.3f}  bar {4*P:.4f}s  first bar line {bar0:.3f}s  inliers(30ms) {res['inlier_frac_30ms']:.1%}  "
      f"resid_sd {res['resid_sd_ms']:.1f}ms  phase votes {res['downbeat_phase_votes']}")
print("off-grid regions [start, end, n_beats]:", regions)
