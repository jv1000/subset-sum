"""R4-A1: candidate charging maps for  w(L^nm) <= w(R')  tested as locality rules by max-flow (m <= 9).
Sources (aggregated over X'): (X, A, A'), supply N(A')/f(X).  Targets (aggregated over Y''): (Y, Y*, D), capacity N(D)/f(Y).
A rule is viable on an instance iff the max-flow saturates all supply.  Also an explicit map: 'prop' sends each
source's supply to its rule-targets in proportion to their capacities; reported is its worst load/capacity ratio."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "round3"))
import numpy as np
from math import comb
from collections import defaultdict
from lay4 import all_sums, generic, Fast, qw
from lay3 import Dinic

def pc(x): return bin(x).count("1")

class Inst:
    def __init__(self, w, t, k):
        self.w = w; self.m = m = len(w); self.t = t; self.k = k
        sums, sizes = all_sums(w); self.sums = sums; full = (1 << m) - 1; self.full = full
        self.tsets = [int(x) for x in np.flatnonzero(sizes == t)]
        self.ksets = [int(x) for x in np.flatnonzero(sizes == k)]
        self.fsum = defaultdict(list)
        for X in self.tsets: self.fsum[int(sums[X])].append(X)
        self.f = {X: len(self.fsum[int(sums[X])]) for X in self.tsets}
        self.kfib = defaultdict(list)
        for A in self.ksets: self.kfib[int(sums[A])].append(A)
        self.ksub = {}
        for X in self.tsets:
            els = [e for e in range(m) if (X >> e) & 1]
            self.ksub[X] = [sum(1 << e for e in c) for c in itertools.combinations(els, k)]
        self.N = defaultdict(float)
        for X in self.tsets:
            for A in self.ksub[X]: self.N[A] += 1.0 / self.f[X]
        # sources
        self.src = []
        for X in self.tsets:
            for A in self.ksub[X]:
                for A2 in self.kfib[int(sums[A])]:
                    if A2 != A and (A2 & ~A & X): self.src.append((X, A, A2, self.N[A2] / self.f[X]))
        # targets
        self.tgt = {}; self.byYYs = defaultdict(list); self.byY = defaultdict(list); self.byYs = defaultdict(list)
        for Y in self.tsets:
            for Ys in self.fsum[int(sums[Y])]:
                if Ys == Y: continue
                PY = Y & ~Ys
                for D in self.ksub[Y]:
                    if (D & PY) != PY:
                        self.tgt[(Y, Ys, D)] = self.N[D] / self.f[Y]
                        self.byYYs[(Y, Ys)].append(D); self.byY[Y].append((Ys, D)); self.byYs[Ys].append((Y, D))
        self.collY = sorted(self.byY)
        self.supply = sum(s for *_, s in self.src); self.cap = sum(self.tgt.values())

    def edges(self, rule, X, A, A2):
        P = A & ~A2; Q = A2 & ~A; B = Q & X; b = pc(B); out = []
        if rule == "C":
            for Ys, D in self.byY.get(X, []): out.append((X, Ys, D))
            for Y, D in self.byYs.get(X, []): out.append((Y, X, D))
            return out
        if rule == "V":
            for Y in self.collY:
                if pc(Y ^ X) <= 2 * b:
                    for Ys, D in self.byY[Y]: out.append((Y, Ys, D))
            return out
        outside = [e for e in range(self.m) if not ((X | Q) >> e) & 1]
        for Ec in itertools.combinations(outside, b):
            E = sum(1 << e for e in Ec); YE = (X & ~B) | E; YEs = (YE & ~P) | Q
            if rule == "T":
                for Ys, D in self.byY.get(YE, []): out.append((YE, Ys, D))
                continue
            for D in self.byYYs.get((YE, YEs), []):
                if rule == "S1E" and (D & E) != E: continue
                if rule == "S1P" and (D & P): continue
                out.append((YE, YEs, D))
            if rule == "S2":
                for D in self.byYYs.get((YEs, YE), []): out.append((YEs, YE, D))
        return out

    def flow(self, rule, SCALE=1 << 36):
        """Returns (routed fraction, #edges). routed == 1 (within 1e-9) means the rule is viable."""
        tid = {}; adj = []
        for i, (X, A, A2, s) in enumerate(self.src):
            es = self.edges(rule, X, A, A2); lst = []
            for r in es:
                if r not in tid: tid[r] = len(tid)
                lst.append(tid[r])
            adj.append(lst)
        ns, nt = len(self.src), len(tid)
        D = Dinic(2 + ns + nt); S, T = 0, 1
        for i, (X, A, A2, s) in enumerate(self.src):
            D.add(S, 2 + i, int(s * SCALE))
            for j in set(adj[i]): D.add(2 + i, 2 + ns + j, 1 << 62)
        for r, j in tid.items(): D.add(2 + ns + j, T, int(self.tgt[r] * SCALE))
        fl = D.maxflow(S, T) / SCALE
        return (fl / self.supply if self.supply > 0 else 1.0), sum(len(set(a)) for a in adj)

    def prop(self, rule="S1"):
        """Explicit map: each source spreads its supply over its rule-targets proportionally to capacity.
        Returns max load/capacity over targets (<= 1 means the explicit map is a valid fractional charging)."""
        load = defaultdict(float)
        for X, A, A2, s in self.src:
            es = list(set(self.edges(rule, X, A, A2)))
            if not es: return float("inf")
            tot = sum(self.tgt[r] for r in es)
            for r in es: load[r] += s * self.tgt[r] / tot
        return max((load[r] / self.tgt[r] for r in load), default=0.0)

RULES = ("S1E", "S1P", "S1", "S2", "T", "C", "V")

def run(w, t, k, rules=RULES, P=print, tag=""):
    I = Inst(w, t, k); F = Fast(w); Q = qw(F, t, k)[0]
    free = I.supply <= I.cap + 1e-9
    res = {}
    for r in rules:
        fr, ne = I.flow(r); res[r] = fr
    pr = I.prop("S1"); prE = I.prop("S1P")
    ok = lambda r: "ok " if res[r] >= 1 - 1e-6 else f"{res[r]:.3f}"
    P(f"{tag}w={tuple(w)} (k,t)=({k},{t}) m-t-2k={len(w)-t-2*k:+d} Qw={Q:.4f} supply={I.supply:.3f} cap={I.cap:.3f} free={'ok ' if free else 'NO '} "
      + " ".join(f"{r}={ok(r)}" for r in rules) + f" propS1={pr:.3f} propS1P={prE:.3f} [{len(I.src)} src, {len(I.tgt)} tgt]")
    return Q, free, res, pr, prE

if __name__ == "__main__":
    o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "charge_flow.txt"), "w")
    def P(*x):
        print(*x); print(*x, file=o); o.flush()
    t0 = time.time()
    P("== controls")
    run([-3, -3, -2, -2, 0, 0], 3, 2, P=P, tag="CONTROL(must fail) ")
    run([0, 0] + generic(2), 2, 1, P=P, tag="equality case ")
    run([0, 0] + generic(3), 2, 1, P=P, tag="zeros perD-fail ")
    run([0] * 5 + generic(3), 4, 2, P=P, tag="zeros perD-fail ")
    run(generic(8), 4, 2, P=P, tag="generic ")
    P("== zeros + generic family")
    for a in range(2, 8):
        for g in range(1, 5):
            m = a + g
            if 5 <= m <= 9:
                for k in range(1, m // 2):
                    for t in range(k + 1, m // 2 + 1):
                        if t + 2 * k <= m: run([0] * a + generic(g), t, k, P=P)
    P("== two-valued")
    for m in range(5, 10):
        for a in range(1, m // 2 + 1):
            for k in range(1, m // 2):
                for t in range(k + 1, m // 2 + 1):
                    if t + 2 * k <= m: run([0] * a + [1] * (m - a), t, k, P=P)
    P("== counterexamples and A0 worst cases")
    for w, kts in (([-6, -5, -5, -3, -3, -2, 4, 5], None), ([-8, -6, -6, -2, -2, 0, 1, 3], None), ([-6, -5, -2, -1, 0, 3, 4], None),
                   ([-3, -3, -3, -2, -2, -2, 1, 1], None), ([-5, -5, -4, -3, -1, 3, 3], None), ([-4, -4, -4, -3, -2, 0, 4, 4], None),
                   ([-3, -3, -3, -2, -1, -1, 3, 3, 3], [(2, 4), (3, 4)]), ([-3, -3, -3, -3, -2, -1, -1, 3, 3, 3], [(3, 4)])):
        m = len(w)
        for k in range(1, m // 2):
            for t in range(k + 1, m // 2 + 1):
                if kts is None or (k, t) in kts: run(w, t, k, P=P)
    P(f"[{time.time()-t0:.0f}s]")
    P("== exhaustive [-3,3] m=6 (k=1,2), m=7 (k=1,2), sample m=8 (k<=2), t+2k<=m: counting failures per rule")
    rng = np.random.default_rng(4)
    for m, cap in ((6, 240), (7, 300), (8, 420)):
        it = itertools.combinations_with_replacement(range(-3, 4), m)
        if m == 8: it = (tuple(sorted(rng.integers(-3, 4, size=8).tolist())) for _ in range(10 ** 9))
        fails = defaultdict(list); n = 0; tl = time.time(); worstprop = (0, None)
        for vals in it:
            n += 1
            for k in range(1, m // 2):
                for t in range(k + 1, m // 2 + 1):
                    if t + 2 * k > m: continue
                    I = Inst(list(vals), t, k)
                    if not I.src: continue
                    if I.supply > I.cap + 1e-9: fails["free"].append((vals, k, t)); continue
                    for r in ("S1E", "S1P", "S1", "S2", "C"):
                        fr, _ = I.flow(r)
                        if fr < 1 - 1e-6: fails[r].append((vals, k, t, round(fr, 3)))
                    pr = I.prop("S1")
                    if pr > worstprop[0]: worstprop = (pr, (vals, k, t))
            if time.time() - tl > cap: break
        P(f"m={m}: {n} instances ({time.time()-tl:.0f}s): failures per rule: " + ", ".join(f"{r}={len(v)}" for r, v in fails.items()) + f"; worst propS1 = {worstprop}")
        for r in ("free", "S1", "S2", "C", "S1P", "S1E"):
            if fails[r]: P(f"   first failures {r}: {fails[r][:4]}")
    P(f"total [{time.time()-t0:.0f}s]"); o.close()
