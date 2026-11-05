"""R3-A1: approximate monotonicity at larger m and wider value ranges (random instances; cluster shape of the m = 8
counterexamples).  rho = max_{j+1<=m/2} a_{j+1}/a_j ; rho_int = same over j+1 < m/2 ; mu' = max_{k<=m/4, t in [k,m-k]} a_t/a_k.
Uses the value-class DP of round 2 (fast) for s_j."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "round2"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from math import comb
from layers import layer_data
from lay3 import rand_instances

def stats(w):
    ld = layer_data(w); m = ld["m"]; s = ld["s"]
    a = [s[j] / comb(m, j) for j in range(m + 1)]
    rho = max(a[j + 1] / a[j] for j in range(m // 2)); jmax = max(range(m // 2), key=lambda j: a[j + 1] / a[j])
    rho_int = max((a[j + 1] / a[j] for j in range(m // 2 - 1)), default=0.0)
    mup = max(max(a[t] for t in range(k, m - k + 1)) / a[k] for k in range(1, m // 4 + 1))
    return rho, jmax, rho_int, mup

if __name__ == "__main__":
    out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "approx_mono.txt"), "w")
    def P(*x):
        print(*x); print(*x, file=out); out.flush()
    r = stats([-6, -5, -5, -3, -3, -2, 4, 5]); P("control m=8 counterexample: rho, j, rho_int, mu' =", r, " expected rho = 96/95 =", 96 / 95)
    rng = np.random.default_rng(31); t0 = time.time(); budget = 480.0
    worst = {}
    for m in (10, 11, 12, 13, 14):
        for shape in ("cluster", "uniform"):
            for R in (10, 20, 40):
                best = (0, None, None); best_int = (0, None); best_mu = (0, None); n = 0; tl = time.time()
                for w in rand_instances(rng, m, R, 20000, shape):
                    rho, j, ri, mu = stats(w); n += 1
                    if rho > best[0]: best = (rho, j, w)
                    if ri > best_int[0]: best_int = (ri, w)
                    if mu > best_mu[0]: best_mu = (mu, w)
                    if time.time() - tl > budget / 30: break
                P(f"m={m:2d} {shape:8s} R={R:2d} n={n:6d}: max rho = {best[0]:.5f} at j={best[1]} (j+1={best[1]+1 if best[1] is not None else None}, m/2={m/2}) w={best[2]}; "
                  f"max rho_int = {best_int[0]:.5f}; max mu' = {best_mu[0]:.5f}" + (f" w={best_mu[1]}" if best_mu[0] > 1 + 1e-12 else ""))
                if best_int[0] > 1 + 1e-12: P("   INTERIOR VIOLATION", best_int)
        if time.time() - t0 > budget: break
    P(f"[{time.time()-t0:.0f}s]"); out.close()
