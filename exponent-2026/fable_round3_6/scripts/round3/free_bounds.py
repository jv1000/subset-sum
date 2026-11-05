"""R3-A0: the three PROVED loss-bearing bounds (baseline), checked exhaustively on small multisets and on random ones.
(a) a_k >= a_t C(m-k,t-k)/C(m,t-k)   [entropy chain, see ROUND3_REPORT A.1]
(b) a_t <= a_k max_u f_k(u)            [representatives, trivial multiplicity bound]
(c) a_t <= E_B a_k(M \\ B), |B| = t-k   [witness-containing counting]
"""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from math import comb
from lay3 import Layers, rand_instances

def check(w):
    L = Layers(w); m = L.m; worst = {"a": 0.0, "b": 0.0, "c": 0.0}; tight_a = []
    for k in range(1, m // 4 + 1):
        for t in range(k, m // 2 + 1):
            ak, at = L.a(k), L.a(t)
            ra = at * comb(m - k, t - k) / comb(m, t - k) / ak            # must be <= 1
            fmax = max(len(v) for v in L.fib[k].values())
            rb = at / (ak * fmax)                                          # must be <= 1
            # (c): E_B a_k(M \ B) over all (t-k)-sets B (exact)
            tot = 0.0; cnt = 0
            for B in itertools.combinations(range(m), t - k):
                rest = [w[i] for i in range(m) if i not in B]
                sk = len({sum(c) for c in itertools.combinations(rest, k)})
                tot += sk / comb(len(rest), k); cnt += 1
            rc = at / (tot / cnt)                                           # must be <= 1
            worst["a"] = max(worst["a"], ra); worst["b"] = max(worst["b"], rb); worst["c"] = max(worst["c"], rc)
            if abs(ra - 1) < 1e-12: tight_a.append((k, t))
    return worst, tight_a

if __name__ == "__main__":
    t0 = time.time(); rng = np.random.default_rng(3)
    out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "free_bounds.txt"), "w")
    def P(*a):
        print(*a); print(*a, file=out)
    W = {"a": 0, "b": 0, "c": 0}; n = 0; viol = 0
    # exhaustive multisets in [-3,3], m = 4..8 ; random m = 9..10
    for m in range(4, 9):
        for vals in itertools.combinations_with_replacement(range(-3, 4), m):
            worst, _ = check(list(vals)); n += 1
            for key in W: W[key] = max(W[key], worst[key])
            if max(worst.values()) > 1 + 1e-9: viol += 1; P("VIOLATION", vals, worst)
    P(f"exhaustive [-3,3] m=4..8: {n} multisets, max ratios (must be <= 1): {W}, violations {viol}  [{time.time()-t0:.0f}s]")
    for m in (9, 10):
        for w in rand_instances(rng, m, 20, 60):
            worst, _ = check(w); n += 1
            for key in W: W[key] = max(W[key], worst[key])
            if max(worst.values()) > 1 + 1e-9: viol += 1; P("VIOLATION", w, worst)
    P(f"plus random m=9,10 in [-20,20]: total {n}, max ratios {W}, violations {viol}  [{time.time()-t0:.0f}s]")
    g = [1 << i for i in range(9)]; worst, tight = check(g)
    P(f"control generic m=9: ratios {worst}; (a) tight at (k,t) pairs: {tight}")
    # the size of the loss of (a) and (b): generic ratio C(m-k,t-k)/C(m,t-k) at t = m/2
    for m in (20, 40, 100):
        for k in (1, int(0.11 * m), m // 4):
            if k < 1: continue
            t = m // 2
            P(f"  loss of (a) at m={m}, k={k}, t={t}: C(m-k,t-k)/C(m,t-k) = 2^{np.log2(comb(m-k,t-k)/comb(m,t-k)):.2f}  (2^-k = 2^{-k})")
    out.close()
