"""R3-A4 (direction iii): small k against the whole cube.
Lambda(M,k) = a_k 2^d (m+1)   (>= 1 is [S] with P = 1; Lemma S);
tail(M,k)  = P_T[F(T) < 1/(a_k m)] / a_k   (<= 1 suffices for [S] with constant m+1: 2^-d = E 1/F <= P[F<L] + 1/L);
near-miss lemma (PROVED, checked here): for every T, sum_{T' subset T, |T \\ T'| <= k} (F(T')-1) >= sum_{A subset T,|A|=k} (f_k(A)-1) / C(|T|-1,k-1).
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from math import comb, log2
from lay3 import subsets, rand_instances

def zeta_by_size(h, m, sizes):
    """For each size s: g_s(T) = sum_{T' subset T, |T'|=s} h(T')  (subset-sum transform)."""
    out = {}
    for s in np.unique(sizes):
        g = np.where(sizes == s, h, 0).astype(np.int64)
        for e in range(m):
            bit = 1 << e
            idx = np.arange(1 << m)
            hi = (idx & bit) != 0
            g[hi] += g[idx[hi] ^ bit]
        out[int(s)] = g
    return out

def analyse(w, ks):
    m = len(w); masks, sizes, sums = subsets(w)
    # cube fibers
    u, inv, cnt = np.unique(sums, return_inverse=True, return_counts=True)
    F = cnt[inv]; S = len(u); d = m - log2(S)
    res = {}
    for k in ks:
        sel = sizes == k
        uk, invk, ck = np.unique(sums[sel], return_inverse=True, return_counts=True)
        fk = np.zeros(1 << m, dtype=np.int64); fk[np.nonzero(sel)[0]] = ck[invk]
        s_k = len(uk); a_k = s_k / comb(m, k)
        Lam = a_k * 2 ** d * (m + 1)
        L = 1 / (a_k * m); tail = np.mean(F < L) / a_k
        # near-miss lemma
        Zs = zeta_by_size((F - 1).astype(np.int64), m, sizes)      # sums of F-1 over subsets of each size
        lhs = np.zeros(1 << m, dtype=np.int64)
        for s, g in Zs.items():
            lhs += np.where((sizes - s >= 0) & (sizes - s <= k), g, 0)
        rhsA = zeta_by_size(np.where(sel, fk - 1, 0).astype(np.int64), m, sizes)[k]   # sum over k-subsets A of T
        ok = True; worst = np.inf
        for T in np.nonzero(sizes >= k)[0]:
            if sizes[T] >= 1 and rhsA[T] > 0:
                r = lhs[T] * comb(int(sizes[T]) - 1, k - 1) / rhsA[T]
                worst = min(worst, r)
                if r < 1 - 1e-9: ok = False
        res[k] = dict(a_k=a_k, d=d, Lam=Lam, tail=tail, EfkOver2d=(comb(m, k) / s_k) / 2 ** d, lemma_ok=ok, lemma_min_ratio=worst)
    return res

if __name__ == "__main__":
    out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "sparse_tail.txt"), "w")
    def P(*x):
        print(*x); print(*x, file=out); out.flush()
    rng = np.random.default_rng(5); t0 = time.time()
    g = [1 << i for i in range(12)]; r = analyse(g, [1, 2, 3])
    P("control generic m=12:", {k: (round(v['Lam'], 3), round(v['tail'], 3), v['lemma_ok']) for k, v in r.items()}, "(Lam must be 13.0)")
    r = analyse([-6, -5, -5, -3, -3, -2, 4, 5], [1, 2, 3]); P("m=8 counterexample:", {k: (round(v['Lam'], 3), round(v['tail'], 3), round(v['EfkOver2d'], 3), v['lemma_ok'], round(v['lemma_min_ratio'], 3)) for k, v in r.items()})
    worstLam = {}; worstTail = {}; lemma_fail = 0; n = 0
    for m, R, ninst in ((12, 6, 400), (13, 8, 250), (14, 10, 150), (15, 12, 60), (16, 12, 25)):
        ks = [k for k in range(1, m // 4 + 1)]
        tl = time.time()
        for shape in ("uniform", "cluster", "sparse_relations"):
            for w in rand_instances(rng, m, R, ninst, shape):
                r = analyse(w, ks); n += 1
                for k, v in r.items():
                    if (m, k) not in worstLam or v['Lam'] < worstLam[(m, k)][0]: worstLam[(m, k)] = (v['Lam'], v['EfkOver2d'], w, shape)
                    if (m, k) not in worstTail or v['tail'] > worstTail[(m, k)][0]: worstTail[(m, k)] = (v['tail'], w, shape)
                    if not v['lemma_ok']: lemma_fail += 1; P("NEAR-MISS LEMMA FAILS", w, k, v)
                if time.time() - tl > 100: break
        P(f"m={m}: " + "; ".join(f"k={k}: min Lam={worstLam[(m,k)][0]:.3f} (E f_k/2^d={worstLam[(m,k)][1]:.2f}, {worstLam[(m,k)][3]}), max tail={worstTail[(m,k)][0]:.3f}" for k in ks) + f"  [{time.time()-t0:.0f}s]")
        for k in ks: P(f"    worst-Lam instance k={k}: {worstLam[(m,k)][2]}")
    P(f"instances {n}, near-miss lemma failures {lemma_fail}  [{time.time()-t0:.0f}s]"); out.close()
