"""Round-4 library: fast layer data (m <= 20) and the canonical second-moment constant Q_w.
Q_w(t,k) = sum_u mult_w(u)^2 / (s_t C(t,k) C(m-k,t-k)),  mult_w(u) = sum_{A: w(A)=u} N_w(A),
N_w(A) = sum_{X ⊇ A, |X|=t} 1/f_t(w(X)).  Q_w = 1 for generic weights; Q_w <= 1  =>  a_t <= a_k  (ROUND3_REPORT A.3)."""
import numpy as np, itertools
from math import comb, log2

def all_sums(w):
    """Subset sums and sizes of all 2^m masks (bit i = element i), by doubling."""
    w = [int(x) for x in w]; m = len(w)
    sums = np.zeros(1 << m, np.int64); sizes = np.zeros(1 << m, np.int16)
    for i in range(m):
        sums[1 << i: 1 << (i + 1)] = sums[: 1 << i] + w[i]
        sizes[1 << i: 1 << (i + 1)] = sizes[: 1 << i] + 1
    return sums, sizes

class Fast:
    """Per-layer data: masks, fiber sizes f (per mask), distinct-sum ids, s_j."""
    def __init__(self, w):
        self.w = [int(x) for x in w]; self.m = m = len(w)
        self.sums, self.sizes = all_sums(self.w)
        self.layer = {}
        self.S = len(np.unique(self.sums)); self.d = m - log2(self.S)
    def L(self, j):
        if j not in self.layer:
            idx = np.flatnonzero(self.sizes == j)
            uniq, inv, cnt = np.unique(self.sums[idx], return_inverse=True, return_counts=True)
            self.layer[j] = (idx, inv, cnt[inv], len(uniq))
        return self.layer[j]
    def s(self, j): return self.L(j)[3]
    def a(self, j): return self.s(j) / comb(self.m, j)

def qw(F, t, k, chunk=4096, want_mult=False):
    """Canonical Q_w(t,k); also returns the per-u ratio max_u mult_w(u)/C(m-k,t-k)."""
    m = F.m
    tidx, tinv, tf, st = F.L(t)
    kidx, kinv, kf, sk = F.L(k)
    kpos = np.full(1 << m, -1, np.int64); kpos[kidx] = np.arange(len(kidx))
    cidx = np.array(list(itertools.combinations(range(t), k)), np.int64)      # C(t,k) x k
    N = np.zeros(len(kidx))
    ar = np.arange(m, dtype=np.int64)
    for lo in range(0, len(tidx), chunk):
        X = tidx[lo: lo + chunk]
        bits = (X[:, None] >> ar) & 1
        els = np.nonzero(bits)[1].reshape(len(X), t)                        # sorted elements of each X
        sub = (np.int64(1) << els[:, cidx]).sum(axis=2)                       # len(X) x C(t,k) masks
        wts = np.repeat(1.0 / tf[lo: lo + chunk], sub.shape[1])
        N += np.bincount(kpos[sub.ravel()], weights=wts, minlength=len(kidx))
    mult = np.bincount(kinv, weights=N, minlength=sk)
    tot = st * comb(t, k); assert abs(N.sum() - tot) < 1e-6 * tot
    Cmk = comb(m - k, t - k)
    Qw = float((mult ** 2).sum() / (tot * Cmk))
    out = (Qw, float(mult.max() / Cmk))
    return out + ((N, mult),) if want_mult else out

def report(w, kts=None):
    """[(k, t, Q_w, per-u ratio, a_t/a_k)] for all k < t <= m/2 (or the given list)."""
    F = Fast(w); m = F.m; out = []
    for k in range(1, m // 2):
        for t in range(k + 1, m // 2 + 1):
            if kts is not None and (k, t) not in kts: continue
            Q, pu = qw(F, t, k)
            out.append((k, t, Q, pu, F.a(t) / F.a(k)))
    return out

def generic(n, base=10 ** 6):
    """n 'generic' values: distinct powers of 3 times a large base (no relations among themselves or with small values)."""
    return [base * 3 ** i for i in range(n)]

def product(blocks):
    """Generic-separated disjoint union of blocks: block i is multiplied by B^i with B > 2 * max |block sum|."""
    Bse = 2 * max(sum(abs(x) for x in b) for b in blocks) + 1
    w = []
    for i, b in enumerate(blocks): w += [x * Bse ** i for x in b]
    return w
