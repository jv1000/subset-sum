"""C21: test layer-density MONOTONICITY  a_k >= a_{k+1}  for 1 <= k < k+1 <= m/2  (Fable's suggested target),
exactly, m = 16..20, structured + random + annealing adversary. Report min ratio a_k/a_{k+1} and any violation."""
import numpy as np, math, sys
rng = np.random.default_rng(2121)
def layers(w):
    m = len(w); s = np.zeros(1, np.int64); z = np.zeros(1, np.int64)
    for x in w: s = np.concatenate([s, s + int(x)]); z = np.concatenate([z, z + 1])
    return [len(np.unique(s[z == k]))/math.comb(m, k) for k in range(m//2 + 1)]
def worst_ratio(w):
    a = layers(w); m = len(w)
    r = [(a[k]/a[k+1], k) for k in range(1, m//2)]
    return min(r)
def fams(m):
    F = [('equal', [1]*m), ('AP', list(range(1, m+1))), ('+-AP', [((-1)**i)*(i//2+1) for i in range(m)]),
         ('pairs', [i//2 + 1 for i in range(m)]), ('+-pairs', [((-1)**i)*(i//2+1)*1000 for i in range(m)]),
         ('two values', [1]*(m//2) + [2]*(m - m//2)), ('powers2', [2**i for i in range(m)]), ('0/1', [0]*(m//2) + [1]*(m - m//2))]
    for _ in range(40): F.append(('small-range', list(rng.integers(-3, 4, m))))
    for _ in range(25):
        z = int(rng.integers(2, m)); F.append((f'eq{z}+gen', [5]*z + list(rng.integers(10**6, 10**9, m - z))))
    for _ in range(25):
        rk = int(rng.integers(1, 4)); g = rng.integers(10**3, 10**6, rk); C = rng.integers(-1, 2, (m, rk)); F.append((f'rank{rk}', list(C @ g)))
    return F
for m in (16, 18, 20):
    best = (1e9, None, None, None)
    for nm, w in fams(m):
        r, k = worst_ratio(w)
        if r < best[0]: best = (r, k, nm, w)
    # annealing adversary from the worst
    cur, cw = best[0], list(best[3])
    for it in range(400 if m < 20 else 150):
        w2 = list(cw); i, j, l = (int(x) for x in rng.integers(m, size=3))
        w2[i] = [w2[j], -w2[j], w2[j] + w2[l], w2[j] - w2[l], int(rng.integers(-4, 5))][int(rng.integers(5))]
        r, k = worst_ratio(w2)
        if r <= cur or rng.random() < 0.03:
            cw = w2
            if r < best[0]: best = (r, k, 'anneal', list(w2))
            cur = r
    print(f'm={m}: min over k of a_k/a_(k+1) = {best[0]:.4f} at k={best[1]} ({best[2]}); violation={best[0] < 1 - 1e-12}; weights={sorted(int(x) for x in best[3])}', flush=True)
