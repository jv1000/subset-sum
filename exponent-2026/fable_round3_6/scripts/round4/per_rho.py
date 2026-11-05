"""R4-A1b: the per-relation inequality.  Every near miss and every R'-target carries a unique relation
rho = (P, Q) = (A\\A', A'\\A) resp. (Y\\Y*, Y*\\Y).  S(rho) = total near-miss weight with relation rho,
T(rho) = total R'-capacity with relation rho.  'Per-rho': S(rho) <= T(rho) for every rho.  It is exactly the
viability of the locality rule 'same relation' (complete bipartite inside each rho), and it is sufficient for Q_w <= 1.
Reported: max_rho S/T per instance (<= 1 means per-rho holds), over the A1 instance list and exhaustive small ranges."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from collections import defaultdict
from lay4 import generic, Fast, qw
from charge_flow import Inst

def per_rho(w, t, k):
    I = Inst(w, t, k); S = defaultdict(float); T = defaultdict(float)
    for X, A, A2, s in I.src: S[(A & ~A2, A2 & ~A)] += s
    for (Y, Ys, D), c in I.tgt.items(): T[(Y & ~Ys, Ys & ~Y)] += c
    worst = (0.0, None)
    for rho, s in S.items():
        r = s / T[rho] if T[rho] > 0 else float("inf")
        if r > worst[0]: worst = (r, rho)
    # also: the j-aggregated version (sum over rho with |P| = j)
    Sj = defaultdict(float); Tj = defaultdict(float)
    for (P, Q), s in S.items(): Sj[bin(P).count("1")] += s
    for (P, Q), c in T.items(): Tj[bin(P).count("1")] += c
    wj = max((Sj[j] / Tj[j] if Tj[j] > 0 else float("inf")) for j in Sj) if Sj else 0.0
    return worst[0], wj, I.supply / I.cap if I.cap else 1.0, len(S)

if __name__ == "__main__":
    o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "per_rho.txt"), "w")
    def P(*x):
        print(*x); print(*x, file=o); o.flush()
    t0 = time.time()
    def show(w, t, k, tag=""):
        r, rj, tot, nr = per_rho(w, t, k); m = len(w)
        P(f"{tag}w={tuple(w)} (k,t)=({k},{t}) m-t-2k={m-t-2*k:+d} Qw={qw(Fast(w), t, k)[0]:.4f} total S/T={tot:.3f} max_rho S/T={r:.3f} {'PER-RHO FAILS' if r > 1 + 1e-9 else ''} max_j S/T={rj:.3f} [{nr} relations]")
    P("== controls")
    show([-3, -3, -2, -2, 0, 0], 3, 2, "CONTROL(must fail) ")
    show([0, 0] + generic(2), 2, 1, "equality ")
    show([0] * 5 + generic(3), 4, 2, "zeros ")
    P("== curated")
    for w in ([-6, -5, -5, -3, -3, -2, 4, 5], [-8, -6, -6, -2, -2, 0, 1, 3], [-6, -5, -2, -1, 0, 3, 4], [-3, -3, -3, -2, -2, -2, 1, 1],
              [-5, -5, -4, -3, -1, 3, 3], [-4, -4, -4, -3, -2, 0, 4, 4], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 1, 1, 1] + generic(2), [-3, -3, -3, -2, -1, -1, 3, 3, 3], [-3, -3, -3, -3, -2, -1, -1, 3, 3, 3]):
        m = len(w)
        for k in range(1, m // 2):
            for t in range(k + 1, m // 2 + 1):
                if t + 2 * k <= m + 1 and not (m >= 9 and k == 1): show(w, t, k)
    P("== exhaustive [-3,3] m=6,7 and [-4,4] m=6; sample m=8 [-3,3]; t+2k<=m")
    rng = np.random.default_rng(5)
    for m, R, cap in ((6, 3, 120), (6, 4, 120), (7, 3, 240), (8, 3, 300)):
        it = itertools.combinations_with_replacement(range(-R, R + 1), m)
        if m == 8: it = (tuple(sorted(rng.integers(-3, 4, size=8).tolist())) for _ in range(10 ** 9))
        n = 0; fails = []; worst = (0, None); worstj = (0, None); tl = time.time()
        for vals in it:
            n += 1
            for k in range(1, m // 2):
                for t in range(k + 1, m // 2 + 1):
                    if t + 2 * k > m: continue
                    r, rj, tot, nr = per_rho(list(vals), t, k)
                    if r > worst[0]: worst = (r, (vals, k, t))
                    if rj > worstj[0]: worstj = (rj, (vals, k, t))
                    if r > 1 + 1e-9: fails.append((vals, k, t, round(r, 3)))
            if time.time() - tl > cap: break
        P(f"m={m} [-{R},{R}]: {n} instances ({time.time()-tl:.0f}s): per-rho failures {len(fails)}; worst max_rho S/T = {worst}; worst per-j = {worstj}")
        if fails: P("   first:", fails[:6])
    P(f"total [{time.time()-t0:.0f}s]"); o.close()
