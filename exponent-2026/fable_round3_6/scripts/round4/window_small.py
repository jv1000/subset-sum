"""R4-A0: exact window at small m: worst Q_w per (m,k,t) over exhaustive multisets, with m - t - 2k and the per-u ratio."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lay4 import Fast, qw, report, generic
o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "window_small.txt"), "w")
def P(*x):
    print(*x); print(*x, file=o); o.flush()
t0 = time.time()
P("control generic m=8:", [(k, t, round(Q, 6)) for k, t, Q, pu, r in report(generic(8))])
P("control (-3,-3,-2,-2,0,0):", [(k, t, round(Q, 4), round(pu, 4), round(r, 4)) for k, t, Q, pu, r in report([-3, -3, -2, -2, 0, 0])])
for R, ms, cap in ((3, range(6, 11), 400), (4, range(6, 9), 300), (5, range(6, 8), 300)):
    for m in ms:
        worst = {}; worst_pu = {}; n = 0; tl = time.time()
        for vals in itertools.combinations_with_replacement(range(-R, R + 1), m):
            n += 1
            for k, t, Q, pu, r in report(list(vals)):
                if (k, t) not in worst or Q > worst[(k, t)][0]: worst[(k, t)] = (Q, r, vals)
                if (k, t) not in worst_pu or pu > worst_pu[(k, t)][0]: worst_pu[(k, t)] = (pu, Q, vals)
            if time.time() - tl > cap: break
        P(f"\n[-{R},{R}] m={m}: {n} multisets ({time.time()-tl:.0f}s)")
        for (k, t), (Q, r, vals) in sorted(worst.items()):
            flag = "VIOL" if Q > 1 + 1e-9 else "    "
            P(f"  (k,t)=({k},{t}) m-t-2k={m-t-2*k:+d} k/m={k/m:.3f} {flag} maxQw={Q:.4f} a_t/a_k={r:.4f} w={vals}   per-u max={worst_pu[(k,t)][0]:.3f} (Qw there {worst_pu[(k,t)][1]:.3f}) at {worst_pu[(k,t)][2]}")
P(f"total {time.time()-t0:.0f}s"); o.close()
