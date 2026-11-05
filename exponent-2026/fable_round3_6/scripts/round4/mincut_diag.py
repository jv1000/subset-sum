"""Diagnostic: Hall violator (min cut) of a locality rule on one instance."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "round3"))
from charge_flow2 import Inst2
from lay3 import Dinic
from collections import deque

def names(w, mask): return "{" + ",".join(str(w[e]) + chr(97 + e) for e in range(len(w)) if (mask >> e) & 1) + "}"

def diag(w, t, k, rule, SCALE=1 << 36):
    I = Inst2(w, t, k); tid = {}; adj = []
    for (X, A, A2, s) in I.src:
        lst = []
        for r in I.edges(rule, X, A, A2):
            if r not in tid: tid[r] = len(tid)
            lst.append(tid[r])
        adj.append(sorted(set(lst)))
    ns, nt = len(I.src), len(tid); D = Dinic(2 + ns + nt); S, T = 0, 1
    for i, (X, A, A2, s) in enumerate(I.src):
        D.add(S, 2 + i, int(s * SCALE))
        for j in adj[i]: D.add(2 + i, 2 + ns + j, 1 << 62)
    inv = {j: r for r, j in tid.items()}
    for r, j in tid.items(): D.add(2 + ns + j, T, int(I.tgt[r] * SCALE))
    fl = D.maxflow(S, T) / SCALE
    # residual reachability from S
    seen = {S}; q = deque([S])
    while q:
        u = q.popleft()
        for v, c, _ in D.g[u]:
            if c > 0 and v not in seen: seen.add(v); q.append(v)
    V = [i for i in range(ns) if 2 + i in seen]; NV = sorted({j for i in V for j in adj[i]})
    print(f"w={w} (k,t)=({k},{t}) rule={rule}: supply={I.supply:.4f} flow={fl:.4f} ({fl/I.supply:.4f})")
    print(f"violating source set: {len(V)} sources, supply {sum(I.src[i][3] for i in V):.4f}; neighbourhood {len(NV)} targets, capacity {sum(I.tgt[inv[j]] for j in NV):.4f}")
    for i in V[:40]:
        X, A, A2, s = I.src[i]
        print(f"  src X={names(w,X)} A={names(w,A)} A'={names(w,A2)} f(X)={I.f[X]} N(A')={I.N[A2]:.3f} supply={s:.3f}")
    for j in NV[:40]:
        Y, Ys, Dm = inv[j]
        print(f"  tgt Y={names(w,Y)} Y*={names(w,Ys)} D={names(w,Dm)} f(Y)={I.f[Y]} N(D)={I.N[Dm]:.3f} cap={I.tgt[inv[j]]:.3f}")
    return V, NV

if __name__ == "__main__":
    diag([-6, -5, -2, -1, 0, 3, 4], 3, 2, "SUP")
    print()
    diag([-2, -1, -1, 0, 0, 1, 2, 3], 3, 2, "SUP")
