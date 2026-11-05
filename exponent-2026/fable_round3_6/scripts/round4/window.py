"""R4-A2: the window k/m in (1/4, 1/3) at m = 12..16 with targeted affine-normalised families.
Families: two-valued {0,1} (all splits); three-valued {0,p,q} (p < q <= 5, gcd 1, all multiplicity splits);
the worst shapes padded with 1-2 generic elements.  (k,t): k from floor(m/4)-1 to ceil(m/3)+1, k < t <= m/2.
Hypotheses (PREREG_R4): H1 safe iff k <= m/4; H2 safe iff t + 2k <= m; H3 safe iff k < m/3."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from math import ceil
from lay4 import Fast, qw, generic
o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "window.txt"), "w")
def P(*x):
    print(*x); print(*x, file=o); o.flush()
t0 = time.time()
VALSETS = [(0, 1, 2), (0, 1, 3), (0, 1, 4), (0, 1, 5), (0, 2, 3), (0, 2, 5), (0, 3, 4), (0, 3, 5), (0, 4, 5)]

def kts(m):
    out = []
    for k in range(max(1, m // 4 - 1), min(m // 2 - 1, ceil(m / 3) + 1) + 1):
        for t in range(k + 1, m // 2 + 1): out.append((k, t))
    return out

def sweep(m, instances, cap, label):
    worst = {}; n = 0; tl = time.time()
    for w in instances:
        n += 1; F = Fast(w)
        for k, t in kts(m):
            Q = qw(F, t, k)[0]
            if (k, t) not in worst or Q > worst[(k, t)][0]: worst[(k, t)] = (Q, F.a(t) / F.a(k), tuple(w))
        if time.time() - tl > cap: P(f"  (cap reached after {n} instances)"); break
    P(f"\nm={m} {label}: {n} instances ({time.time()-tl:.0f}s)")
    for (k, t), (Q, r, w) in sorted(worst.items()):
        s = m - t - 2 * k
        pred = f"H1:{'safe' if k <= m/4 else 'open'} H2:{'safe' if s >= 0 else 'open'} H3:{'safe' if 3*k < m else 'open'}"
        P(f"  (k,t)=({k},{t}) k/m={k/m:.3f} m-t-2k={s:+d} {'VIOL' if Q > 1 + 1e-9 else '    '} maxQw={Q:.4f} a_t/a_k={r:.4f} {pred} w={w}")
    return worst

def family(m, valsets=VALSETS, two=True):
    if two:
        for a in range(1, m // 2 + 1): yield [0] * a + [1] * (m - a)
    for vs in valsets:
        for n0 in range(1, m - 1):
            for n1 in range(1, m - n0):
                n2 = m - n0 - n1
                if n2 >= 1: yield [vs[0]] * n0 + [vs[1]] * n1 + [vs[2]] * n2

P("control generic m=12:", [round(qw(Fast(generic(12)), t, k)[0], 6) for k, t in kts(12)])
P("control scaled m=8 failure shape {0,1,4} split (6,6,4) at m=16, (k,t)=(6,8):", round(qw(Fast([0] * 6 + [1] * 6 + [4] * 4), 8, 6)[0], 4))
allworst = {}
for m in (12, 13, 14):
    allworst[m] = sweep(m, family(m), 420, "two-valued + all {0,p,q} splits")
for m in (15, 16):
    allworst[m] = sweep(m, family(m, VALSETS[:4]), 600, "two-valued + {0,1,c} splits, c<=5")
# generic padding of the worst shapes (m-g base shapes, g = 1, 2)
for m in (13, 14, 15, 16):
    inst = []
    for g in (1, 2):
        base = allworst.get(m - g, {})
        shapes = {w for (Q, r, w) in base.values()}
        for w in shapes: inst.append(list(w) + generic(g, base=1000))
    sweep(m, inst, 200, "worst shapes of m-1, m-2 plus generic padding")
P(f"total [{time.time()-t0:.0f}s]"); o.close()
