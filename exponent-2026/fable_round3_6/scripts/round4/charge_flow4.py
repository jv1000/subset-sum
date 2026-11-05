"""R4-A1e: rule YPQ (Y ⊇ P or Y ⊇ Q; any collision partner Y*; any admissible D) at scale, with variants YP, YPQ*."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from collections import defaultdict
from lay4 import generic, Fast, qw
from charge_flow import Inst, pc

class Inst4(Inst):
    def edges(self, rule, X, A, A2):
        P = A & ~A2; Q = A2 & ~A; out = []
        for Y in self.collY:
            if rule == "YPQx" and Y == X: continue
            if (Y & P) == P or (rule != "YP" and (Y & Q) == Q):
                for Ys, D in self.byY[Y]: out.append((Y, Ys, D))
        return out

RULES = ("YP", "YPQx", "YPQ")

def run(w, t, k, P=print, tag=""):
    I = Inst4(w, t, k); Q = qw(Fast(w), t, k)[0]; free = I.supply <= I.cap + 1e-9
    res = {r: I.flow(r)[0] for r in RULES}
    ok = lambda r: "ok " if res[r] >= 1 - 1e-6 else f"{res[r]:.3f}"
    P(f"{tag}w={tuple(w)} (k,t)=({k},{t}) m-t-2k={len(w)-t-2*k:+d} Qw={Q:.4f} free={'ok ' if free else 'NO '} "
      + " ".join(f"{r}={ok(r)}" for r in RULES) + f" propYPQ={I.prop('YPQ'):.3f} [{len(I.src)} src, {len(I.tgt)} tgt]")
    return res

if __name__ == "__main__":
    o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "charge_flow4.txt"), "w")
    def P(*x):
        print(*x); print(*x, file=o); o.flush()
    t0 = time.time()
    P("== controls")
    run([-3, -3, -2, -2, 0, 0], 3, 2, P=P, tag="CONTROL(must fail) ")
    run([0, 0] + generic(2), 2, 1, P=P, tag="equality ")
    run([-3, -3, -3, 0, 1, 2, 3], 3, 2, P=P, tag="YAA-failure ")
    P("== curated (t+2k<=m)")
    for w in ([-6, -5, -5, -3, -3, -2, 4, 5], [-8, -6, -6, -2, -2, 0, 1, 3], [-3, -3, -3, -2, -2, -2, 1, 1], [-4, -4, -4, -3, -2, 0, 4, 4],
              [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 1] + generic(2), [0] * 5 + generic(3), [0] * 6 + generic(3),
              [-3, -3, -3, -3, -2, -2, -2], [-3, -3, -2, -2, 0, 1, 1], [-3, -3, -3, -2, -1, -1, 3, 3, 3], [-3, -3, -3, -3, -2, -1, -1, 3, 3, 3],
              [0, 0, 0, 1, 1, 1, 2, 2, 2], [-3, -3, -2, -1, 0, 1, 2, 3, 3], [-2, -2, -1, -1, 0, 0, 1, 1, 2]):
        m = len(w)
        for k in range(1, m // 2):
            for t in range(k + 1, m // 2 + 1):
                if t + 2 * k <= m and (m <= 8 or k >= 2): run(w, t, k, P=P)
    P(f"[{time.time()-t0:.0f}s]")
    P("== exhaustive [-3,3] m=6,7, [-4,4] m=6; sample m=8 (300s), m=9 k<=2 (180s); t+2k<=m: failures per rule")
    rng = np.random.default_rng(8)
    for m, R, cap in ((6, 3, 120), (6, 4, 120), (7, 3, 300), (8, 3, 300), (9, 3, 180)):
        it = itertools.combinations_with_replacement(range(-R, R + 1), m)
        if m >= 8: it = (tuple(sorted(rng.integers(-R, R + 1, size=m).tolist())) for _ in range(10 ** 9))
        fails = defaultdict(list); n = 0; tl = time.time(); worstprop = (0, None); worstfr = (1.0, None)
        for vals in it:
            n += 1
            for k in range(1, m // 2):
                for t in range(k + 1, m // 2 + 1):
                    if t + 2 * k > m or (m == 9 and k > 2): continue
                    I = Inst4(list(vals), t, k)
                    if not I.src: continue
                    if I.supply > I.cap + 1e-9: fails["free"].append((vals, k, t)); continue
                    for r in RULES:
                        fr, _ = I.flow(r)
                        if fr < 1 - 1e-6: fails[r].append((vals, k, t, round(fr, 3)))
                        if r == "YPQ" and fr < worstfr[0]: worstfr = (fr, (vals, k, t))
                    pr = I.prop("YPQ")
                    if pr > worstprop[0]: worstprop = (pr, (vals, k, t))
            if time.time() - tl > cap: break
        P(f"m={m} [-{R},{R}]: {n} instances ({time.time()-tl:.0f}s): failures per rule: " + ", ".join(f"{r}={len(fails[r])}" for r in ("free",) + RULES) + f"; worst YPQ routed = {worstfr}; worst propYPQ = {worstprop}")
        for r in RULES:
            if fails[r]: P(f"   first failures {r}: {fails[r][:5]}")
    P(f"total [{time.time()-t0:.0f}s]"); o.close()
