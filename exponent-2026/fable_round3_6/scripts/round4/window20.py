"""R4-A3: the window k/m in (1/4, 1/3) at m = 20 (and the (k,t) pairs around it) with targeted families.
Families (affine-normalised): two-valued {0,1} all splits; {0,1,c} (c=2,4,5), {0,2,5}, {0,4,5} splits with every part
>= 3 (the m=12..16 worst shapes all have parts >= 4); the (-3^3,-2^3,1^2) shape scaled to m=20; the A0 m=10 worst scaled x2;
the worst {0,1,c} shapes with 2 or 4 elements replaced by generic ones.
(k,t): k = 5 (t=6..10), k = 6 (t=7..10), k = 7 (t=8..10), k = 8 (t = 9, 10), k = 9 (t = 10).
Pre-registered (PREREG_R4 A3): k=5 all <= 1; k=6 t=7,8 <= 1, t=9,10 some > 1; k=7 t=9,10 > 1.  Budget <= 30 min."""
import sys, os, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lay4 import Fast, qw, generic
o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "window20.txt"), "w")
def P(*x):
    print(*x); print(*x, file=o); o.flush()
t0 = time.time(); m = 20
KT = [(5, t) for t in range(6, 11)] + [(6, t) for t in range(7, 11)] + [(7, t) for t in range(8, 11)] + [(8, 9), (8, 10), (9, 10)]

def sweep(instances, cap, label):
    worst = {}; n = 0; tl = time.time(); viol = []
    for w in instances:
        n += 1; F = Fast(w)
        for k, t in KT:
            Q = qw(F, t, k)[0]
            if Q > 1 + 1e-9: viol.append((k, t, round(Q, 4), tuple(w)))
            if (k, t) not in worst or Q > worst[(k, t)][0]: worst[(k, t)] = (Q, F.a(t) / F.a(k), tuple(w))
        if time.time() - tl > cap: P(f"  (cap reached after {n} instances)"); break
    P(f"\nm={m} {label}: {n} instances ({time.time()-tl:.0f}s)")
    for (k, t), (Q, r, w) in sorted(worst.items()):
        s = m - t - 2 * k
        pred = f"H1:{'safe' if k <= m/4 else 'open'} H2:{'safe' if s >= 0 else 'open'} H3:{'safe' if 3*k < m else 'open'}"
        P(f"  (k,t)=({k},{t}) k/m={k/m:.3f} m-t-2k={s:+d} {'VIOL' if Q > 1 + 1e-9 else '    '} maxQw={Q:.4f} a_t/a_k={r:.4f} {pred} w={w}")
    if viol: P("  all violations:", viol)
    return worst

def splits(vs, lo=3):
    for n0 in range(lo, m - 2 * lo + 1):
        for n1 in range(lo, m - n0 - lo + 1):
            yield [vs[0]] * n0 + [vs[1]] * n1 + [vs[2]] * (m - n0 - n1)

P("control generic m=20 at (5,6),(6,8),(7,10):", [round(qw(Fast(generic(20)), t, k)[0], 6) for k, t in ((5, 6), (6, 8), (7, 10))])
P("control all-ones m=20 at (9,10) (two-valued a=0, must be > 1 per m=12..16 pattern):", round(qw(Fast([1] * 20), 10, 9)[0], 4))
two = [[0] * a + [1] * (m - a) for a in range(1, m // 2 + 1)]
W = {}
W["two"] = sweep(two, 120, "two-valued (all splits)")
W["015"] = sweep(list(splits((0, 1, 5))), 420, "{0,1,5} splits, parts >= 3")
W["014"] = sweep(list(splits((0, 1, 4))), 300, "{0,1,4} splits, parts >= 3")
W["012"] = sweep(list(splits((0, 1, 2))), 240, "{0,1,2} splits, parts >= 3")
W["025"] = sweep(list(splits((0, 2, 5), lo=4)), 180, "{0,2,5} splits, parts >= 4")
W["045"] = sweep(list(splits((0, 4, 5), lo=4)), 180, "{0,4,5} splits, parts >= 4")
shapes = [[-3] * 8 + [-2] * 7 + [1] * 5, [-3] * 7 + [-2] * 8 + [1] * 5, [-3] * 8 + [-2] * 8 + [1] * 4, [-3] * 6 + [-2] * 8 + [2] * 6,
          [-3] * 7 + [-2] * 7 + [2] * 6, [-3] * 6 + [-2] * 8 + [2] * 6]
W["shapes"] = sweep(shapes, 120, "(-3,-3,-3,-2,-2,-2,1,1) and A0 m=10 worst scaled to m=20")
pad = []
for key in ("015", "014", "012"):
    for (Q, r, w) in W[key].values():
        base = list(w)
        for g in (2, 4):
            b = list(base)
            for i in range(g): b.remove(max(set(b), key=b.count))
            cand = b + generic(g, base=1000)
            if cand not in pad: pad.append(cand)
W["pad"] = sweep(pad, 300, "worst {0,1,c} shapes with 2 or 4 elements replaced by generic ones")
P(f"total [{time.time()-t0:.0f}s]"); o.close()
