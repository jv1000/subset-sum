"""C18 probe: is a_k(M) >= 2^{-d(M)}/poly for small k?  Search weightings of an m-set (signed integers)
minimizing  R_k = log2 a_k(M) + d(M)   (the conjecture says R_k >= -O(log m)).  Exact enumeration, m <= 18."""
import numpy as np, itertools, sys, math
rng = np.random.default_rng(18)
def stats(w, ks):
    m = len(w); w = np.asarray(w, dtype=np.int64)
    # all subset sums with sizes via bit DP
    sums = np.zeros(1, dtype=np.int64); sizes = np.zeros(1, dtype=np.int64)
    for x in w:
        sums = np.concatenate([sums, sums + x]); sizes = np.concatenate([sizes, sizes + 1])
    d = m - math.log2(len(np.unique(sums)))
    out = {}
    for k in ks:
        sk = sums[sizes == k]; ak = len(np.unique(sk))/math.comb(m, k)
        out[k] = math.log2(ak) + d
    return d, out
def families(m):
    R = []
    for _ in range(40): R.append(('rand-small', rng.integers(-3, 4, m)))
    for _ in range(40): R.append(('rand-tiny', rng.integers(-1, 2, m)))
    for _ in range(20):  # pairs equal / opposite
        base = rng.integers(1, 10**6, m//2); s = rng.choice([-1, 1], m//2); R.append(('pairs', np.r_[base, s*base]))
    for _ in range(20):  # half zero, half generic
        z = rng.integers(0, m+1); R.append(('zeros', np.r_[np.zeros(z, int), rng.integers(1, 10**6, m - z)]))
    for _ in range(20):  # AP block + generic block
        z = rng.integers(1, m); R.append(('AP+gen', np.r_[np.arange(1, z+1), rng.integers(10**5, 10**6, m - z)*10**3]))
    for _ in range(20):  # few generators (low rank)
        r = rng.integers(1, 4); G = rng.integers(10**3, 10**6, r); C = rng.integers(-2, 3, (m, r)); R.append((f'rank{r}', C @ G))
    for _ in range(20):  # two values
        R.append(('twoval', rng.choice([rng.integers(1, 50), rng.integers(1, 50)], m)))
    return R
m = int(sys.argv[1]) if len(sys.argv) > 1 else 16; ks = [1, 2, 3, 4]
worst = {k: (1e9, None) for k in ks}
for name, w in families(m):
    d, o = stats(w, ks)
    for k in ks:
        if o[k] < worst[k][0]: worst[k] = (o[k], name, d, list(w))
# local search from the worst found, per k
for k in ks:
    best, name, d, w = worst[k]; w = list(w)
    for it in range(1500):
        w2 = list(w); i = rng.integers(m); w2[i] = int(rng.choice([w[rng.integers(m)], -w[rng.integers(m)], 0, w[i] + rng.integers(-3, 4), rng.integers(-5, 6)]))
        d2, o2 = stats(w2, [k])
        if o2[k] < best: best, w, d = o2[k], w2, d2
    print(f'm={m} k={k}: min log2(a_k) + d = {best:+.3f}  (d = {d:.2f}; start family {name}); -log2(poly~m) = {-math.log2(m+1):.2f}; weights {sorted(w)}')
