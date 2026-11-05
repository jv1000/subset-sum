"""R3-A3: flow/Hall form of M' (direction (i)).  P*(M; t, k) = least capacity (x C(m,k)/C(m,t)) per k-sum under which
every t-sum sends one unit of flow to the k-sums of its witnesses' k-subsets.  P* >= a_t/a_k; P* = 1 for generic."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from math import comb
from lay3 import Layers, hall_slack, rand_instances

def run(w, kmax=None):
    L = Layers(w); m = L.m; res = []
    for k in range(1, (kmax or m // 4) + 1):
        for t in range(k + 1, m // 2 + 1):
            res.append((k, t, hall_slack(L, t, k), L.a(t) / L.a(k)))
    return res

if __name__ == "__main__":
    out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "hall_flow.txt"), "w")
    def P(*x):
        print(*x); print(*x, file=out); out.flush()
    rng = np.random.default_rng(11); t0 = time.time()
    P("control generic m=8:", [(k, t, round(p, 4)) for k, t, p, r in run([1 << i for i in range(8)])])
    P("control m=8 counterexample (k=3,t=4 must be >= 96/95 = 1.0105):", [(k, t, round(p, 4), round(r, 4)) for k, t, p, r in run([-6, -5, -5, -3, -3, -2, 4, 5], 3)])
    for m in range(6, 10):
        W = {}; n = 0; tl = time.time()
        for vals in itertools.combinations_with_replacement(range(-3, 4), m):
            for k, t, p, r in run(list(vals)):
                if (k, t) not in W or p > W[(k, t)][0]: W[(k, t)] = (p, r, vals)
            n += 1
            if time.time() - tl > 120: break
        P(f"m={m}: {n} multisets in [-3,3]: worst P* per (k,t): " + "; ".join(f"({k},{t}): P*={v[0]:.4f} a_t/a_k={v[1]:.4f} w={v[2]}" for (k, t), v in sorted(W.items())))
    for m, R, n_inst in ((10, 10, 150), (11, 12, 80), (12, 12, 40)):
        W = {}; tl = time.time()
        for shape in ("uniform", "cluster", "sparse_relations"):
            for w in rand_instances(rng, m, R, n_inst, shape):
                for k, t, p, r in run(w):
                    if (k, t) not in W or p > W[(k, t)][0]: W[(k, t)] = (p, r, w, shape)
                if time.time() - tl > 150: break
        P(f"m={m} random: worst P* per (k,t): " + "; ".join(f"({k},{t}): P*={v[0]:.4f} a_t/a_k={v[1]:.4f} [{v[3]}]" for (k, t), v in sorted(W.items())))
        P("   worst:", max(W.items(), key=lambda kv: kv[1][0]))
    P(f"[{time.time()-t0:.0f}s]"); out.close()
