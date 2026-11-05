"""R4-A1c: second family of locality rules — charge a near miss with relation rho = (P, Q) to collisions whose relation
CONTAINS rho (A1 showed that same-relation rules fail: two-valued (0,0,1,1,1) at (1,2) needs the 2-relations).
  SUPA: Y ⊇ A, Y ∩ Q = ∅, Y* ⊇ A', Y* ∩ P = ∅   (both k-sets kept)
  SUP : Y ⊇ P, Y ∩ Q = ∅, Y* ⊇ Q, Y* ∩ P = ∅   (relation kept, i.e. P ⊆ Y\\Y*, Q ⊆ Y*\\Y)
  SUPD: SUP and D ∩ P = ∅
  SUPX: SUP and Y ⊆ X ∪ (M\\(X∪Q))... no — kept simple: SUP with |Y \\ X| <= |B| + |P| (Y stays near X)
Same flow machinery as charge_flow.py (tolerance 1e-6)."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "round3"))
import numpy as np
from collections import defaultdict
from lay4 import generic, Fast, qw
from charge_flow import Inst, pc
from lay3 import Dinic

class Inst2(Inst):
    def __init__(self, w, t, k):
        super().__init__(w, t, k)
        self.byrel = defaultdict(list)                       # (Y\Y*, Y*\Y) -> [(Y, Ys, D)]
        for (Y, Ys, D) in self.tgt: self.byrel[(Y & ~Ys, Ys & ~Y)].append((Y, Ys, D))
        self.rels = list(self.byrel)
    def edges(self, rule, X, A, A2):
        P = A & ~A2; Q = A2 & ~A; B = Q & X; b = pc(B); out = []
        for (PY, QY) in self.rels:
            if (PY & P) != P or (QY & Q) != Q: continue
            for (Y, Ys, D) in self.byrel[(PY, QY)]:
                if rule == "SUPA" and not ((Y & A) == A and (Ys & A2) == A2): continue
                if rule == "SUPD" and (D & P): continue
                if rule == "SUPX" and pc(Y & ~X) > b + pc(P): continue
                out.append((Y, Ys, D))
        return out

RULES = ("SUPA", "SUPD", "SUPX", "SUP")

def run(w, t, k, P=print, tag=""):
    I = Inst2(w, t, k); Q = qw(Fast(w), t, k)[0]; free = I.supply <= I.cap + 1e-9
    res = {r: I.flow(r)[0] for r in RULES}
    ok = lambda r: "ok " if res[r] >= 1 - 1e-6 else f"{res[r]:.3f}"
    P(f"{tag}w={tuple(w)} (k,t)=({k},{t}) m-t-2k={len(w)-t-2*k:+d} Qw={Q:.4f} free={'ok ' if free else 'NO '} "
      + " ".join(f"{r}={ok(r)}" for r in RULES) + f" propSUP={I.prop('SUP'):.3f} propSUPD={I.prop('SUPD'):.3f} [{len(I.src)} src, {len(I.tgt)} tgt]")
    return res

if __name__ == "__main__":
    o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "charge_flow2.txt"), "w")
    def P(*x):
        print(*x); print(*x, file=o); o.flush()
    t0 = time.time()
    P("== controls")
    run([-3, -3, -2, -2, 0, 0], 3, 2, P=P, tag="CONTROL(must fail) ")
    run([0, 0] + generic(2), 2, 1, P=P, tag="equality ")
    run([0, 0, 1, 1, 1], 2, 1, P=P, tag="two-valued S1-failure ")
    run([0, 0, 0] + generic(4), 3, 2, P=P, tag="zeros T-failure ")
    run([0] * 5 + generic(3), 4, 2, P=P, tag="zeros ")
    P("== curated (t+2k<=m)")
    for w in ([-6, -5, -5, -3, -3, -2, 4, 5], [-8, -6, -6, -2, -2, 0, 1, 3], [-6, -5, -2, -1, 0, 3, 4], [-3, -3, -3, -2, -2, -2, 1, 1],
              [-5, -5, -4, -3, -1, 3, 3], [-4, -4, -4, -3, -2, 0, 4, 4], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 1, 1, 1] + generic(2), [-3, -3, -3, -2, -1, -1, 3, 3, 3], [-3, -3, -3, -3, -2, -2, -2], [-3, -3, -3, -3, 0, 0]):
        m = len(w)
        for k in range(1, m // 2):
            for t in range(k + 1, m // 2 + 1):
                if t + 2 * k <= m and not (m >= 9 and k == 1): run(w, t, k, P=P)
    P(f"[{time.time()-t0:.0f}s]")
    P("== exhaustive [-3,3] m=6, m=7; sample m=8; t+2k<=m: failures per rule")
    rng = np.random.default_rng(6)
    for m, cap in ((6, 180), (7, 300), (8, 360)):
        it = itertools.combinations_with_replacement(range(-3, 4), m)
        if m == 8: it = (tuple(sorted(rng.integers(-3, 4, size=8).tolist())) for _ in range(10 ** 9))
        fails = defaultdict(list); n = 0; tl = time.time(); worstprop = (0, None)
        for vals in it:
            n += 1
            for k in range(1, m // 2):
                for t in range(k + 1, m // 2 + 1):
                    if t + 2 * k > m: continue
                    I = Inst2(list(vals), t, k)
                    if not I.src: continue
                    if I.supply > I.cap + 1e-9: fails["free"].append((vals, k, t)); continue
                    for r in RULES:
                        fr, _ = I.flow(r)
                        if fr < 1 - 1e-6: fails[r].append((vals, k, t, round(fr, 3)))
                    pr = I.prop("SUP")
                    if pr > worstprop[0]: worstprop = (pr, (vals, k, t))
            if time.time() - tl > cap: break
        P(f"m={m}: {n} instances ({time.time()-tl:.0f}s): failures per rule: " + ", ".join(f"{r}={len(fails[r])}" for r in ("free",) + RULES) + f"; worst propSUP = {worstprop}")
        for r in RULES:
            if fails[r]: P(f"   first failures {r}: {fails[r][:5]}")
    P(f"total [{time.time()-t0:.0f}s]"); o.close()
