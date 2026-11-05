"""R5-A1b: YP / YPQx / YPQ by the collapsed flow on exhaustive multisets (shuffled order, time cap per m):
m=8 in [-3,3], m=9 and m=10 in [-2,2]; all (k,t) with t+2k <= m.  Memory guard: edge cap + working-set check."""
import sys, os, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from collections import defaultdict
from flow5 import Inst5, RULES, rss_mb, MemoryGuard, EMAX

o = open(os.path.join(HERE, "out", "charge_flow5b.txt"), "w")
def P(*x):
    print(*x); print(*x, file=o); o.flush()
t0 = time.time()
I = Inst5([-3, -3, -2, -2, 0, 0], 3, 2)
P("control (must fail, 0.900): " + " ".join(f"{r}={I.flow(r)[0]:.4f}" for r in RULES))
rng = np.random.default_rng(5)
for m, R, cap in ((8, 3, 600), (9, 2, 420), (10, 2, 360)):
    allv = list(itertools.combinations_with_replacement(range(-R, R + 1), m)); rng.shuffle(allv)
    fails = defaultdict(list); n = 0; tested = 0; skipped = []; worst = (1.0, None); tl = time.time(); peak = 0
    try:
        for vals in allv:
            n += 1
            for k in range(1, m // 2):
                for t in range(k + 1, m // 2 + 1):
                    if t + 2 * k > m: continue
                    I = Inst5(list(vals), t, k)
                    if not I.src: continue
                    if I.supply > I.cap + 1e-9: fails["free"].append((vals, k, t)); continue
                    tested += 1
                    for r in RULES:
                        fr, ne = I.flow(r)
                        if fr is None: skipped.append((vals, k, t, r, ne)); continue
                        if fr < 1 - 1e-6: fails[r].append((vals, k, t, round(fr, 4)))
                        if r == "YP" and fr < worst[0]: worst = (fr, (vals, k, t))
                    peak = max(peak, rss_mb())
            if time.time() - tl > cap: break
    except MemoryGuard as e:
        P(f"m={m}: ABORTED by memory guard: {e}")
    P(f"m={m} [-{R},{R}]: {n}/{len(allv)} multisets, {tested} (k,t)-cases ({time.time()-tl:.0f}s, peak rss {peak:.0f} MB): failures: "
      + ", ".join(f"{r}={len(fails[r])}" for r in ("free",) + RULES) + f"; skipped by edge cap: {len(skipped)}; worst YP routed = {worst}")
    for r in ("free",) + RULES:
        if fails[r]: P(f"   first failures {r}: {fails[r][:5]}")
    if skipped: P(f"   skipped: {skipped[:5]}")
P(f"total [{time.time()-t0:.0f}s]"); o.close()
