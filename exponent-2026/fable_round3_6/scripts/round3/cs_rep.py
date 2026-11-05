"""R3-A2: second-moment (Cauchy-Schwarz) form of M' with canonical witnesses.
Q(t,k) = sum_u mult(u)^2 / (s_t C(t,k) C(m-k,t-k));  PROVED: s_k >= s_t C(m,k) / (C(m,t) Q).  Q = 1 for generic weights.
Witness rules: lex-first (natural order) and the minimum over 8 random element orders."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from math import comb
from lay3 import Layers, lex_witness, Q_cs, rand_instances

def run(w, rng, orders=8):
    L = Layers(w); m = L.m; res = []
    for k in range(1, m // 4 + 1):
        for t in range(k + 1, m // 2 + 1):
            q_lex, img = Q_cs(L, t, k, lex_witness(L.fib[t]))
            q_min = q_lex
            for _ in range(orders):
                q, _ = Q_cs(L, t, k, lex_witness(L.fib[t], rng.permutation(m).tolist())); q_min = min(q_min, q)
            res.append((k, t, q_lex, q_min, L.a(t) / L.a(k)))
    return res

if __name__ == "__main__":
    out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "cs_rep.txt"), "w")
    def P(*x):
        print(*x); print(*x, file=out); out.flush()
    rng = np.random.default_rng(7); t0 = time.time()
    g = [1 << i for i in range(10)]; P("control generic m=10:", [(k, t, round(ql, 6)) for k, t, ql, qm, r in run(g, rng, 2)])
    P("m=8 counterexample:", [(k, t, round(ql, 4), round(qm, 4), round(r, 4)) for k, t, ql, qm, r in run([-6, -5, -5, -3, -3, -2, 4, 5], rng)])
    # exhaustive multisets in [-3,3], m = 6..10
    for m in range(6, 11):
        W = {}; n = 0; tl = time.time()
        for vals in itertools.combinations_with_replacement(range(-3, 4), m):
            for k, t, ql, qm, r in run(list(vals), rng, 4):
                key = (k, t)
                if key not in W or ql > W[key][0]: W[key] = (ql, qm, r, vals)
            n += 1
            if time.time() - tl > 100: break
        P(f"m={m}: {n} multisets in [-3,3] (exhaustive if {comb(7+m-1,m)}): worst Q_lex per (k,t): " +
          "; ".join(f"({k},{t}): Q_lex={v[0]:.3f} Q_min={v[1]:.3f} a_t/a_k={v[2]:.3f} w={v[3]}" for (k, t), v in sorted(W.items())))
    # random wider range, m = 11..13
    for m, R, n_inst in ((11, 12, 300), (12, 12, 200), (13, 12, 100)):
        W = {}
        for shape in ("uniform", "cluster", "sparse_relations"):
            for w in rand_instances(rng, m, R, n_inst, shape):
                for k, t, ql, qm, r in run(w, rng, 3):
                    key = (k, t)
                    if key not in W or ql > W[key][0]: W[key] = (ql, qm, r, w, shape)
        P(f"m={m} random: worst Q_lex per (k,t): " + "; ".join(f"({k},{t}): Q_lex={v[0]:.3f} Q_min={v[1]:.3f} a_t/a_k={v[2]:.3f} [{v[4]}]" for (k, t), v in sorted(W.items())))
        P("   worst instances:", {kt: v[3] for kt, v in W.items() if v[0] == max(x[0] for x in W.values())})
    # the structured family E (r zeros) + generic: Q as a function of r at m = 12, k = 3, t = 6
    for r in (0, 2, 4, 6, 8):
        w = [0] * r + [1 << i for i in range(12 - r)]; L = Layers(w)
        ql, _ = Q_cs(L, 6, 3, lex_witness(L.fib[6])); qz, _ = Q_cs(L, 6, 3, lex_witness(L.fib[6], list(range(r, 12)) + list(range(r))))
        P(f"zeros r={r} + generic, m=12, k=3, t=6: Q_lex(zeros first)={ql:.3f}  Q(zeros last)={qz:.3f}  a_t/a_k={L.a(6)/L.a(3):.4f}")
    P(f"[{time.time()-t0:.0f}s]"); out.close()
