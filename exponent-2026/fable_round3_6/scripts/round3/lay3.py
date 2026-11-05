"""Round-3 harness: exact layer/fiber data of a signed integer weight vector by brute force (m <= 18),
plus the quantities used by the proof attempts for Conjecture M'.

Definitions (ROUND2_REPORT A.1): Sigma_j = distinct j-subset sums, s_j = |Sigma_j|, a_j = s_j / C(m,j),
2^{-d} = |Sigma| / 2^m.  Conjecture M': a_t <= poly(m) a_k for t in [k, m-k], k <= 0.11 m.
"""
import numpy as np
from math import comb, log2
from collections import defaultdict, deque


def subsets(w):
    """All 2^m subsets as (masks, sizes, sums)."""
    w = np.asarray(w, dtype=np.int64); m = len(w)
    masks = np.arange(1 << m, dtype=np.int64)
    bits = ((masks[:, None] >> np.arange(m)) & 1).astype(np.int64)
    return masks, bits.sum(1), bits @ w


class Layers:
    def __init__(self, w):
        self.w = list(map(int, w)); self.m = m = len(w)
        self.masks, self.sizes, self.sums = subsets(self.w)
        self.s = [0] * (m + 1); self.fib = []          # fib[j] : dict sum -> list of masks (witnesses)
        for j in range(m + 1):
            sel = np.nonzero(self.sizes == j)[0]
            d = defaultdict(list)
            for i in sel: d[int(self.sums[i])].append(int(self.masks[i]))
            self.fib.append(d); self.s[j] = len(d)
        self.S = len(set(self.sums.tolist())); self.d = m - log2(self.S)

    def a(self, j): return self.s[j] / comb(self.m, j)

    def f(self, j, y): return len(self.fib[j][y])

    def ratio_mono(self):
        """max a_{j+1}/a_j over j+1 <= m/2 (exact monotonicity <=> all <= 1)."""
        return max(self.a(j + 1) / self.a(j) for j in range(0, self.m // 2))

    def mprime(self, k):
        """max_{t in [k, m-k]} a_t / a_k."""
        return max(self.a(t) for t in range(k, self.m - k + 1)) / self.a(k)


def popcount(x): return bin(x).count("1")


def lex_witness(fibj, order=None):
    """Canonical witness per distinct sum: lexicographically first mask under the element order (default natural)."""
    if order is None:
        return {y: min(ms) for y, ms in fibj.items()}
    key = lambda mk: tuple(-((mk >> e) & 1) for e in order)   # prefer sets containing early elements
    return {y: min(ms, key=key) for y, ms in fibj.items()}


def k_subsets_of_mask(mask, k, m):
    els = [e for e in range(m) if (mask >> e) & 1]
    from itertools import combinations
    for c in combinations(els, k):
        yield sum(1 << e for e in c)


def rep_multiplicity(L, t, k, witness):
    """mult(u) = #{(y, A): y in Sigma_t, A subset of witness(y), |A| = k, w(A) = u}; returns dict u -> mult."""
    mult = defaultdict(int); w = L.w
    for y, X in witness.items():
        for A in k_subsets_of_mask(X, k, L.m):
            mult[int(L.sums[A])] += 1
    return mult


def Q_cs(L, t, k, witness):
    """Second-moment ratio Q = sum_u mult(u)^2 / (s_t C(t,k) C(m-k,t-k)); Q = 1 for generic weights.
    M' with constant Q follows: |image| >= (sum mult)^2 / sum mult^2 = s_t C(m,k) / (C(m,t) Q)."""
    mult = rep_multiplicity(L, t, k, witness)
    tot = sum(mult.values()); sq = sum(v * v for v in mult.values())
    assert tot == L.s[t] * comb(t, k)
    return sq / (L.s[t] * comb(t, k) * comb(L.m - k, t - k)), len(mult)


# ---------- max-flow (Dinic) for the Hall/flow test ----------
class Dinic:
    def __init__(self, n):
        self.n = n; self.g = [[] for _ in range(n)]
    def add(self, u, v, c):
        self.g[u].append([v, c, len(self.g[v])]); self.g[v].append([u, 0, len(self.g[u]) - 1])
    def bfs(self, s, t):
        self.lv = [-1] * self.n; self.lv[s] = 0; q = deque([s])
        while q:
            u = q.popleft()
            for v, c, _ in self.g[u]:
                if c > 0 and self.lv[v] < 0: self.lv[v] = self.lv[u] + 1; q.append(v)
        return self.lv[t] >= 0
    def dfs(self, u, t, f):
        if u == t: return f
        while self.it[u] < len(self.g[u]):
            e = self.g[u][self.it[u]]; v, c, r = e
            if c > 0 and self.lv[v] == self.lv[u] + 1:
                d = self.dfs(v, t, min(f, c))
                if d > 0:
                    e[1] -= d; self.g[v][r][1] += d; return d
            self.it[u] += 1
        return 0
    def maxflow(self, s, t):
        fl = 0
        while self.bfs(s, t):
            self.it = [0] * self.n
            while True:
                f = self.dfs(s, t, 1 << 60)
                if f == 0: break
                fl += f
        return fl


def shadow_graph(L, t, k):
    """Edges y ~ u (y in Sigma_t, u in Sigma_k) iff some witness X of y has a k-subset A with w(A) = u."""
    adj = {}
    for y, ms in L.fib[t].items():
        us = set()
        for X in ms:
            for A in k_subsets_of_mask(X, k, L.m): us.add(int(L.sums[A]))
        adj[y] = us
    return adj


def hall_slack(L, t, k, prec=1e-3):
    """Smallest c such that every y in Sigma_t can send one unit of flow to its neighbours in Sigma_k with
    capacity c per u.  P* = c* C(m,k)/C(m,t) is the best constant in the flow form of M' (P* = 1 for generic).
    Binary search with integer scaling (unit = 1/Q)."""
    adj = shadow_graph(L, t, k); ys = list(adj); us = sorted({u for s_ in adj.values() for u in s_})
    uid = {u: i for i, u in enumerate(us)}; Q = 1 << 20
    def feasible(c):
        D = Dinic(2 + len(ys) + len(us)); S, T = 0, 1
        for i, y in enumerate(ys):
            D.add(S, 2 + i, Q)
            for u in adj[y]: D.add(2 + i, 2 + len(ys) + uid[u], Q * 4)
        cap = int(c * Q)
        for j in range(len(us)): D.add(2 + len(ys) + j, T, cap)
        return D.maxflow(S, T) >= Q * len(ys)
    lo, hi = 0.0, float(len(ys))            # hi always feasible
    while hi - lo > prec * hi:
        mid = (lo + hi) / 2
        if feasible(mid): hi = mid
        else: lo = mid
    return hi * comb(L.m, k) / comb(L.m, t)


def rand_instances(rng, m, R, n, shape="uniform"):
    """Random weight vectors. shape 'uniform': iid in [-R,R]; 'cluster': six-ish small values with doubles + large."""
    for _ in range(n):
        if shape == "uniform":
            yield rng.integers(-R, R + 1, size=m).tolist()
        elif shape == "cluster":
            r = rng.integers(2, max(3, m - 2)); small = rng.integers(0, R // 3 + 1, size=r).tolist()
            dbl = rng.integers(0, r, size=rng.integers(1, 3)); small += [small[i] for i in dbl]
            large = rng.integers(R // 2, R + 1, size=max(0, m - len(small))).tolist()
            w = (small + large)[:m]
            while len(w) < m: w.append(int(rng.integers(0, R + 1)))
            sgn = rng.integers(0, 2) * 2 - 1
            yield [sgn * x - int(rng.integers(0, R // 2 + 1)) for x in w]
        elif shape == "sparse_relations":
            # generic-ish weights with planted balanced relations of small size
            w = rng.integers(1, 10 ** 6, size=m).tolist()
            for _ in range(rng.integers(1, m // 2 + 1)):
                j = int(rng.integers(1, 4)); idx = rng.permutation(m)[: 2 * j]
                P, Qs = idx[:j], idx[j:]
                w[Qs[-1]] = sum(w[i] for i in P) - sum(w[i] for i in Qs[:-1])
            yield w
