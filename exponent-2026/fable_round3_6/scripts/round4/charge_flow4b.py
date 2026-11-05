"""R4-A1e-b (rerun of the exhaustive part): charge_flow4.py died of MemoryError on the curated m=9 instance
(0,0,0,1,1,1,2,2,2) at (2,3) (dense YPQ adjacency inside Dinic).  This script runs only the exhaustive/sampled sections,
with a guard that skips (k,t)-cases whose src x tgt product exceeds EMAX (skipped cases are counted, the largest reported)."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from collections import defaultdict
from charge_flow4 import Inst4, RULES
EMAX = 1_500_000
o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "charge_flow4b.txt"), "w")
def P(*x):
    print(*x); print(*x, file=o); o.flush()
t0 = time.time()
P("== exhaustive [-3,3] m=6,7, [-4,4] m=6; sample m=8 (300s), m=9 k<=2 (180s); t+2k<=m: failures per rule (src*tgt guard %d)" % EMAX)
rng = np.random.default_rng(8)
for m, R, cap in ((6, 3, 120), (6, 4, 120), (7, 3, 300), (8, 3, 300), (9, 3, 180)):
    it = itertools.combinations_with_replacement(range(-R, R + 1), m)
    if m >= 8: it = (tuple(sorted(rng.integers(-R, R + 1, size=m).tolist())) for _ in range(10 ** 9))
    fails = defaultdict(list); n = 0; tl = time.time(); worstprop = (0, None); worstfr = (1.0, None)
    skipped = 0; biggest = (0, None); tested = 0
    for vals in it:
        n += 1
        for k in range(1, m // 2):
            for t in range(k + 1, m // 2 + 1):
                if t + 2 * k > m or (m == 9 and k > 2): continue
                I = Inst4(list(vals), t, k)
                if not I.src: continue
                if I.supply > I.cap + 1e-9: fails["free"].append((vals, k, t)); continue
                ne = len(I.src) * len(I.tgt)
                if ne > biggest[0]: biggest = (ne, (vals, k, t))
                if ne > EMAX: skipped += 1; continue
                tested += 1
                for r in RULES:
                    fr, _ = I.flow(r)
                    if fr < 1 - 1e-6: fails[r].append((vals, k, t, round(fr, 3)))
                    if r == "YPQ" and fr < worstfr[0]: worstfr = (fr, (vals, k, t))
                pr = I.prop("YPQ")
                if pr > worstprop[0]: worstprop = (pr, (vals, k, t))
        if time.time() - tl > cap: break
    P(f"m={m} [-{R},{R}]: {n} instances, {tested} (k,t)-cases tested, {skipped} skipped by guard (largest src*tgt {biggest}) ({time.time()-tl:.0f}s): failures per rule: "
      + ", ".join(f"{r}={len(fails[r])}" for r in ("free",) + RULES) + f"; worst YPQ routed = {worstfr}; worst propYPQ = {worstprop}")
    for r in RULES:
        if fails[r]: P(f"   first failures {r}: {fails[r][:5]}")
P(f"total [{time.time()-t0:.0f}s]"); o.close()
