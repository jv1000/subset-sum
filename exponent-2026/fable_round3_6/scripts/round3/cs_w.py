"""R3-A5: canonical second-moment form Q_w and its reduction  Q_w <= 1  <=>  w(L^nm) <= w(R').
N_w(A) = sum_{X ⊇ A, |X|=t} 1/f_t(X);  mult_w(u) = sum_{A in W_k(u)} N_w(A);  Q_w = sum_u mult_w^2 / (s_t C(t,k) C(m-k,t-k)).
w(L)  = sum_u mult_w(u)^2 - sum_A N_w(A)^2           (colliding ordered pairs (X,A),(X',A') with A != A')
w(R)  = sum_A N_w(A) (C(m-k,t-k) - N_w(A))
w(L1) = sum_X (1/f(X)) sum_{A ⊆ X} sum_{A' ~ A, A' != A, A' ∩ (X \\ A) = ∅} N_w(A')   (image of the swap injection)
w(L^nm) = w(L) - w(L1),  w(R') = w(R) - w(L1)."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from math import comb
from collections import defaultdict
from lay3 import Layers, lex_witness, Q_cs, rand_instances

def qw(L, t, k):
    m = L.m; w = L.w
    tsets = [i for i in range(1 << m) if L.sizes[i] == t]
    ft = {i: L.f(t, int(L.sums[i])) for i in tsets}
    Nw = defaultdict(float)                                   # k-set mask -> N_w
    ksub = {}                                                 # X -> list of k-subset masks
    for X in tsets:
        els = [e for e in range(m) if (X >> e) & 1]
        subs = [sum(1 << e for e in c) for c in itertools.combinations(els, k)]
        ksub[X] = subs
        for A in subs: Nw[A] += 1.0 / ft[X]
    fib = L.fib[k]                                            # u -> list of k-set masks
    mult = {u: sum(Nw[A] for A in As) for u, As in fib.items()}
    S2 = sum(v * v for v in mult.values()); SN2 = sum(v * v for v in Nw.values()); SN = sum(Nw.values())
    Cmk = comb(m - k, t - k)
    Qw = S2 / (L.s[t] * comb(t, k) * Cmk)
    wL = S2 - SN2; wR = SN * Cmk - SN2
    wL1 = 0.0
    for X in tsets:
        for A in ksub[X]:
            rest = X & ~A
            for A2 in fib[int(L.sums[A])]:
                if A2 != A and (A2 & rest) == 0: wL1 += Nw[A2] / ft[X]
    return Qw, wL - wL1, wR - wL1, wL1, wR

def report(w, kts=None):
    L = Layers(w); m = L.m; out = []
    for k in range(1, m // 2):
        for t in range(k + 1, m // 2 + 1):
            if kts and (k, t) not in kts: continue
            Qw, Lnm, Rp, L1, R = qw(L, t, k)
            ql, _ = Q_cs(L, t, k, lex_witness(L.fib[t]))
            out.append((k, t, Qw, ql, L.a(t) / L.a(k), Lnm, Rp))
    return out

if __name__ == "__main__":
    o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "cs_w.txt"), "w")
    def P(*x):
        print(*x); print(*x, file=o); o.flush()
    rng = np.random.default_rng(13); t0 = time.time()
    P("control generic m=8:", [(k, t, round(Qw, 6), round(Lnm, 6), round(Rp, 6)) for k, t, Qw, ql, r, Lnm, Rp in report([1 << i for i in range(8)])])
    for w in ([-6, -5, -5, -3, -3, -2, 4, 5], [-8, -6, -6, -2, -2, 0, 1, 3], [-6, -5, -2, -1, 0, 3, 4]):
        P("counterexample", w, ":", [(k, t, f"Qw={Qw:.4f}", f"Qlex={ql:.4f}", f"a_t/a_k={r:.4f}", f"Lnm={Lnm:.3f}", f"R'={Rp:.3f}") for k, t, Qw, ql, r, Lnm, Rp in report(w)])
    worst = {}; n = 0; viol = []
    for m in range(6, 11):
        tl = time.time()
        for vals in itertools.combinations_with_replacement(range(-3, 4), m):
            n += 1
            for k, t, Qw, ql, r, Lnm, Rp in report(list(vals)):
                key = (m, k, t)
                if key not in worst or Qw > worst[key][0]: worst[key] = (Qw, ql, r, vals)
                if Qw > 1 + 1e-9 and k <= m / 4: viol.append((vals, k, t, Qw))
            if time.time() - tl > 150: break
        P(f"m={m}: {n} multisets so far; worst Q_w per (k,t): " + "; ".join(f"({k},{t}): Qw={v[0]:.4f} Qlex={v[1]:.4f} a_t/a_k={v[2]:.4f} w={v[3]}" for (mm, k, t), v in sorted(worst.items()) if mm == m) + f"  [{time.time()-t0:.0f}s]")
    P("violations of Q_w <= 1 with k <= m/4:", viol[:20], "count", len(viol))
    # m = 8 in [-6,6]: random subsample (exhaustive is 496,860 at m<=9 in round 2); middle step included
    W = {}; tl = time.time(); cnt = 0
    while time.time() - tl < 120:
        vals = tuple(sorted(rng.integers(-6, 7, size=8).tolist())); cnt += 1
        for k, t, Qw, ql, r, Lnm, Rp in report(list(vals)):
            if (k, t) not in W or Qw > W[(k, t)][0]: W[(k, t)] = (Qw, ql, r, vals)
    P(f"m=8 random in [-6,6], {cnt} multisets: " + "; ".join(f"({k},{t}): Qw={v[0]:.4f} Qlex={v[1]:.4f} a_t/a_k={v[2]:.4f} w={v[3]}" for (k, t), v in sorted(W.items())))
    for m, R, ninst in ((11, 8, 60), (12, 8, 25)):
        W = {}
        for shape in ("uniform", "cluster", "sparse_relations"):
            for w in rand_instances(rng, m, R, ninst, shape):
                for k, t, Qw, ql, r, Lnm, Rp in report(w):
                    if (k, t) not in W or Qw > W[(k, t)][0]: W[(k, t)] = (Qw, ql, r, w)
        P(f"m={m} random: " + "; ".join(f"({k},{t}): Qw={v[0]:.4f} Qlex={v[1]:.4f} a_t/a_k={v[2]:.4f}" for (k, t), v in sorted(W.items())) + f"  [{time.time()-t0:.0f}s]")
    o.close()
