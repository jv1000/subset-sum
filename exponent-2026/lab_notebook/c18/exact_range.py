"""C20b: where does the EXACT inequality a_k(M) >= |Sigma(M)|/2^m (R_k >= 0, no poly loss) hold?
Exhaustive over structured families + annealing started from structured instances; m = 10..16, all k <= m/2."""
import numpy as np, math, sys
rng = np.random.default_rng(2020)
def run(m, iters=500):
    SZ = np.zeros(1, np.int64)
    for i in range(m): SZ = np.concatenate([SZ, SZ + 1])
    def R(w):
        s = np.zeros(1, np.int64)
        for x in w: s = np.concatenate([s, s + int(x)])
        d = m - math.log2(len(np.unique(s)))
        return {k: math.log2(len(np.unique(s[SZ == k]))/math.comb(m, k)) + d for k in range(1, m//2 + 1)}
    fams = [[1]*m, list(range(1, m+1)), [((-1)**i)*(i//2+1) for i in range(m)], [1, 1]*(m//2), [1, -1]*(m//2), [1, 2]*(m//2),
            [1]*(m//2) + [10**6 + 7*i for i in range(m - m//2)], list(rng.integers(-2, 3, m)), list(rng.integers(0, 3, m))]
    worst = {}
    for w in fams:
        for k, v in R(w).items():
            if k not in worst or v < worst[k][0]: worst[k] = (v, w)
    for k in list(worst):
        cur, cw = worst[k]
        for it in range(iters):
            w2 = list(cw); i = int(rng.integers(m)); j = int(rng.integers(m)); l = int(rng.integers(m))
            w2[i] = [w2[j], -w2[j], w2[j] + w2[l], w2[j] - w2[l], int(rng.integers(-4, 5))][int(rng.integers(5))]
            v = R(w2)[k]
            if v < cur or rng.random() < 0.02: cw = w2; cur = min(cur, v) if v >= cur else v
            if v < worst[k][0]: worst[k] = (v, list(w2))
    return {k: worst[k][0] for k in sorted(worst)}
for m in (10, 12, 14, 16):
    res = run(m)
    print(f'm={m}: ' + '  '.join(f'k={k}({k/m:.2f}):{v:+.2f}' for k, v in res.items()), flush=True)
