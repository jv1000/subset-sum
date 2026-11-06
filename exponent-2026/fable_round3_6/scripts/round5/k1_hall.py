"""R5-A2 (rerun with the corrected (R3) check: sign of the minimum over all R vs over class unions): the base case k = 1 of YP-Hall.  Checks the reductions (R1)-(R4) of PREREG_R5 numerically, computes the
Hall slack over unions of classes (and over all subsets R of elements at m <= 8), the tight set U*, the
over-represented set O = {c : M_c > C}, the explicit proportional map's load, and compares the slack with the
profile model (generic class values) of the same class sizes.  Exhaustive multisets, time cap per m."""
import sys, os, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from math import comb
from collections import defaultdict
from flow5 import Inst5, rss_mb
from lay4 import Fast, qw, generic

o = open(os.path.join(HERE, "out", "k1_hall.txt"), "w")
def P(*x):
    print(*x); print(*x, file=o); o.flush()
t0 = time.time()

def classes(w):
    cl = defaultdict(list)
    for i, v in enumerate(w): cl[v].append(i)
    return [cl[v] for v in sorted(cl)]

def profile_model(ns, t):
    r = len(ns); s0 = 0; J = [0] * r
    def rec(i, rem, cur):
        nonlocal s0
        if i == r:
            if rem == 0:
                s0 += 1
                for c in range(r): J[c] += cur[c]
            return
        for j in range(0, min(ns[i], rem) + 1):
            cur.append(j); rec(i + 1, rem - j, cur); cur.pop()
    rec(0, t, [])
    return s0, J

def prop_load(I, rule="YP"):
    g = I.groups(rule); load = defaultdict(float)
    for key, s in g.items():
        Ys = [Y for Y in I.collY if I.admits(rule, key, Y)]
        tot = sum(I.capY[Y] for Y in Ys)
        if tot <= 0: return float("inf")
        for Y in Ys: load[Y] += s * I.capY[Y] / tot
    return max((load[Y] / I.capY[Y] for Y in load), default=0.0)

def analyse(w, t, allR):
    I = Inst5(w, t, 1); m = len(w); C = comb(m - 1, t - 1); s = len(I.fsum)
    cl = classes(w); r = len(cl); ns = [len(c) for c in cl]
    cid = {p: ci for ci, c in enumerate(cl) for p in c}
    Np = {p: I.N[1 << p] for p in range(m)}
    M = [sum(Np[p] for p in c) for c in cl]
    Q1 = sum(x * x for x in M) / (t * s * C); Q = qw(Fast(w), t, 1)[0]
    Sp = defaultdict(float)
    for X, A, A2, sup in I.src: Sp[A.bit_length() - 1] += sup
    jc = lambda X, ci: sum(1 for p in cl[ci] if (X >> p) & 1)
    errS = max(abs(M[cid[p]] / ns[cid[p]] * sum((jc(X, cid[p]) - 1) / I.f[X] for X in I.tsets if (X >> p) & 1) - Sp.get(p, 0.0)) for p in range(m))
    errK = max((abs(sum(M[ci] / ns[ci] * jc(Y, ci) * (I.f[Y] - 1 - ns[ci] + jc(Y, ci)) / I.f[Y] for ci in range(r)) - I.capY[Y]) for Y in I.collY), default=0.0)
    capY = I.capY; collY = I.collY
    big = [ci for ci in range(r) if ns[ci] >= 2]
    best = (float("inf"), None); ratio = (0.0, None)
    for size in range(1, len(big) + 1):
        for U in itertools.combinations(big, size):
            mask = sum(1 << p for ci in U for p in cl[ci])
            S = sum(Sp[p] for ci in U for p in cl[ci]); K = sum(capY[Y] for Y in collY if Y & mask)
            if K - S < best[0]: best = (K - S, U)
            rt = S / K if K > 0 else (float("inf") if S > 0 else 0.0)
            if rt > ratio[0]: ratio = (rt, U)
    minR = None
    if allR:
        minR = float("inf")
        for mask in range(1, 1 << m):
            S = sum(Sp[p] for p in range(m) if (mask >> p) & 1)
            if S == 0: continue
            K = sum(capY[Y] for Y in collY if Y & mask)
            minR = min(minR, K - S)
        if minR == float("inf"): minR = best[0]
    fr = I.flow("YP")[0]
    O = tuple(ci for ci in range(r) if M[ci] > C + 1e-9)
    s0, J = profile_model(ns, t)
    slack0 = C * t * s0 - sum(x * x for x in J); slack = C * t * s - sum(x * x for x in M)
    return dict(Q=Q, dQ=abs(Q1 - Q), errS=errS, errK=errK, minU=best[0], Ustar=best[1], ratio=ratio, minR=minR, fr=fr,
                O=O, slack=slack, slack0=slack0, s=s, s0=s0, M=M, C=C, ns=ns, prop=prop_load(I), supply=I.supply, cap=I.cap, cl=cl)

P("== control for (d): the round-4 k=2 instance (-3,-3,-2,-2,0,3,3) at (2,3) must give proportional load 1.126 under YP-merged prop")
P(f"   prop load (YPQ) = {prop_load(Inst5([-3, -3, -2, -2, 0, 3, 3], 3, 2), 'YPQ'):.4f}, (YP) = {prop_load(Inst5([-3, -3, -2, -2, 0, 3, 3], 3, 2), 'YP'):.4f}")
P("== control for (e): profile model vs realised generic-class instance")
for ns, t in (([2, 1, 1], 2), ([2, 2], 2), ([3, 1, 1, 1], 3), ([2, 2, 1, 1], 3), ([4, 2, 1], 3), ([3, 3, 2], 4)):
    w = [v for v, n in zip(generic(len(ns)), ns) for _ in range(n)]
    s0, J = profile_model(ns, t); C = comb(sum(ns) - 1, t - 1)
    P(f"   ns={ns} t={t}: profile Q = {sum(x*x for x in J)/(t*s0*C):.6f}  realised Q = {qw(Fast(w), t, 1)[0]:.6f}")

rng = np.random.default_rng(21)
for m, R, cap in ((6, 3, 150), (7, 3, 240), (8, 2, 240), (9, 2, 240)):
    allv = list(itertools.combinations_with_replacement(range(-R, R + 1), m)); rng.shuffle(allv)
    n = 0; cases = 0; tl = time.time(); st = defaultdict(int); worst = {"ratio": (0, None), "prop": (0, None), "Q": (0, None), "profile": (0, None)}
    maxd = 0; top = []
    for vals in allv:
        n += 1
        for t in range(2, m // 2 + 1):
            a = analyse(list(vals), t, allR=(m <= 8))
            if a["supply"] == 0: continue
            cases += 1
            maxd = max(maxd, a["dQ"], a["errS"], a["errK"])
            if a["minU"] < -1e-9: st["hall_fail"] += 1
            if a["fr"] < 1 - 1e-6: st["flow_fail"] += 1
            if (a["minU"] < -1e-9) != (a["fr"] < 1 - 1e-6): st["flow_vs_hall_mismatch"] += 1
            if a["minR"] is not None and ((a["minR"] < -1e-9) != (a["minU"] < -1e-9)): st["allR_vs_union_SIGN_mismatch"] += 1
            if a["minR"] is not None and a["minR"] < a["minU"] - 1e-9: st["minR_below_minU"] += 1
            if a["O"]:
                st["O_nonempty"] += 1
                if set(a["O"]) <= set(a["Ustar"]): st["Ustar_contains_O"] += 1
                if set(a["O"]) == set(a["Ustar"]): st["Ustar_eq_O"] += 1
                if set(a["Ustar"]) <= set(a["O"]): st["Ustar_within_O"] += 1
            st[f"Ustar_size_{len(a['Ustar'])}"] += 1
            if a["prop"] > 1 + 1e-9: st["prop_fail"] += 1
            if a["slack"] < a["slack0"] - 1e-9: st["profile_not_extremal"] += 1
            d = a["slack0"] - a["slack"]
            if d > worst["profile"][0]: worst["profile"] = (d, (vals, t, a["slack"], a["slack0"]))
            if a["ratio"][0] > worst["ratio"][0]: worst["ratio"] = (a["ratio"][0], (vals, t, a["ratio"][1]))
            if a["prop"] > worst["prop"][0]: worst["prop"] = (a["prop"], (vals, t))
            if a["Q"] > worst["Q"][0]: worst["Q"] = (a["Q"], (vals, t))
            top.append((a["ratio"][0], vals, t, a["ratio"][1], a["O"], [round(x, 3) for x in a["M"]], a["C"], a["ns"], round(a["Q"], 4)))
        if time.time() - tl > cap: break
    top.sort(reverse=True)
    P(f"m={m} [-{R},{R}]: {n}/{len(allv)} multisets, {cases} cases, k=1, t=2..{m//2} ({time.time()-tl:.0f}s, rss {rss_mb():.0f} MB)")
    P(f"   checks: max |Q(R1)-Q|, |S formula - enum|, |cap formula - enum| = {maxd:.2e}; " + ", ".join(f"{k}={v}" for k, v in sorted(st.items())))
    P(f"   worst: Hall ratio max_U S(U)/K(U) = {worst['ratio']}; prop load = {worst['prop']}; Q_w = {worst['Q']}; profile slack0 - slack max = {worst['profile']}")
    P("   top Hall ratios (ratio, w, t, U*, O, M, C, ns, Q):")
    for row in top[:6]: P("     ", row)
P(f"total [{time.time()-t0:.0f}s]"); o.close()
