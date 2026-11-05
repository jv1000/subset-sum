"""R5-A1: YP / YPQx / YPQ on the 137 dense m = 8, 9 cases skipped by round 4's guard (collapsed flow, memory guard),
after validating the collapsed flow against the explicit dense flow on random m = 6, 7 cases and the two controls."""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from collections import defaultdict
from flow5 import Inst5, RULES, rss_mb, MemoryGuard, EMAX
from charge_flow4 import Inst4
from lay4 import generic

o = open(os.path.join(HERE, "out", "charge_flow5.txt"), "w")
def P(*x):
    print(*x); print(*x, file=o); o.flush()
t0 = time.time()

def run(w, t, k, tag="", cut=True):
    I = Inst5(w, t, k)
    res = {}; txt = []
    for r in RULES:
        fr, ne, c = I.flow(r, want_cut=True)
        res[r] = fr
        txt.append(f"{r}=" + ("SKIP" if fr is None else ("ok " if fr >= 1 - 1e-6 else f"{fr:.4f}")))
        if fr is not None and fr < 1 - 1e-6 and cut: txt.append("\n" + I.describe_cut(c))
    P(f"{tag}w={tuple(w)} (k,t)=({k},{t}) m-t-2k={len(w)-t-2*k:+d} supply={I.supply:.3f} cap={I.cap:.3f} "
      + " ".join(txt) + f" [{len(I.src)} src, {len(I.tgt)} tgt, rss {rss_mb():.0f} MB]")
    return res

P("== control 1: collapsed flow vs explicit dense flow (charge_flow4.Inst4) on random m=6,7 cases")
rng = np.random.default_rng(55); n = 0; worst = 0.0
while n < 300:
    m = 6 if rng.random() < 0.5 else 7
    vals = sorted(rng.integers(-3, 4, size=m).tolist())
    for k in range(1, m // 2):
        for t in range(k + 1, m // 2 + 1):
            if t + 2 * k > m: continue
            I5 = Inst5(vals, t, k)
            if not I5.src: continue
            I4 = Inst4(vals, t, k)
            for r in RULES:
                a, _ = I5.flow(r); b, _ = I4.flow(r)
                worst = max(worst, abs(a - b))
            n += 1
P(f"compared {n} cases x 3 rules: max |collapsed - explicit| = {worst:.2e} ({'PASS' if worst < 1e-8 else 'FAIL'}) [{time.time()-t0:.0f}s]")
P("== control 2 (must stay infeasible, 0.900) and control 3 (equality case, must be tight)")
run([-3, -3, -2, -2, 0, 0], 3, 2, tag="CONTROL(must fail) ", cut=False)
run([0, 0] + generic(2), 2, 1, tag="equality ")

P("== regenerate the round-4 sample (rng seed 8: 116 size-8 draws, then 80 size-9 draws) and its guard-skipped cases")
rng = np.random.default_rng(8); dense = []; tested4 = 0
for m, ndraw in ((8, 116), (9, 80)):
    sk = 0
    for _ in range(ndraw):
        vals = tuple(sorted(rng.integers(-3, 4, size=m).tolist()))
        for k in range(1, m // 2):
            for t in range(k + 1, m // 2 + 1):
                if t + 2 * k > m or (m == 9 and k > 2): continue
                I = Inst5(list(vals), t, k)
                if not I.src: continue
                if I.supply > I.cap + 1e-9: continue
                if len(I.src) * len(I.tgt) > 1_500_000: dense.append((vals, k, t)); sk += 1
                else: tested4 += 1
    P(f"m={m}: {sk} guard-skipped cases regenerated (round 4 reported {33 if m == 8 else 104})")
P(f"total dense cases: {len(dense)} (expected 137); cases round 4 tested: {tested4} (expected 547+296=843) [{time.time()-t0:.0f}s]")

P("== the dense cases under YP / YPQx / YPQ (collapsed flow)")
fails = defaultdict(list); skipped = []; worstfr = (1.0, None); nrun = 0
try:
    for vals, k, t in dense:
        res = run(list(vals), t, k); nrun += 1
        for r in RULES:
            if res[r] is None: skipped.append((vals, k, t, r))
            elif res[r] < 1 - 1e-6: fails[r].append((vals, k, t, round(res[r], 4)))
            if r == "YP" and res[r] is not None and res[r] < worstfr[0]: worstfr = (res[r], (vals, k, t))
    P("== the three curated m=9 instances charge_flow4 never reached (k=2)")
    for w in ([0, 0, 0, 1, 1, 1, 2, 2, 2], [-3, -3, -2, -1, 0, 1, 2, 3, 3], [-2, -2, -1, -1, 0, 0, 1, 1, 2]):
        for t in (3, 4):
            res = run(w, t, 2, tag="curated "); nrun += 1
            for r in RULES:
                if res[r] is None: skipped.append((tuple(w), 2, t, r))
                elif res[r] < 1 - 1e-6: fails[r].append((tuple(w), 2, t, round(res[r], 4)))
except MemoryGuard as e:
    P(f"ABORTED by memory guard: {e}")
P(f"== summary: {nrun} cases run; failures per rule: " + ", ".join(f"{r}={len(fails[r])}" for r in RULES)
  + f"; skipped by edge cap {EMAX}: {len(skipped)}; worst YP routed = {worstfr}; peak rss {rss_mb():.0f} MB")
for r in RULES:
    if fails[r]: P(f"   failures {r}: {fails[r]}")
if skipped: P(f"   skipped: {skipped}")
P(f"total [{time.time()-t0:.0f}s]"); o.close()
