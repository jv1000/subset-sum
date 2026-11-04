"""C20a: finite-size exhaustive test of Conjecture R on GENERAL weightings (no product structure).
R_k = log2 a_k(M) + d(M); conjecture: R_k >= -O(log m). Report min over an annealing adversary + planted-relation families."""
import numpy as np, math, sys
rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 20)
m = int(sys.argv[1]) if len(sys.argv) > 1 else 20; KS = (1, 2, 3, 4)
SIZES = np.zeros(1, np.int64)
for i in range(m): SIZES = np.concatenate([SIZES, SIZES + 1])
def stats(w):
    s = np.zeros(1, np.int64)
    for x in w: s = np.concatenate([s, s + int(x)])
    d = m - math.log2(len(np.unique(s)))
    return d, {k: math.log2(len(np.unique(s[SIZES == k]))/math.comb(m, k)) + d for k in KS}
def planted():
    out = []
    for _ in range(30):   # sparse random relations: weights = generic + some forced  w_a + w_b = w_c + w_e
        w = list(rng.integers(1, 10**9, m)); r = rng.integers(1, m)
        for _ in range(r):
            a, b, c = rng.choice(m, 3, replace=False); e = rng.integers(m)
            w[e] = w[a] + w[b] - w[c]
        out.append(('rel', w))
    for _ in range(30):   # low-rank: w = C @ g with small integer C
        rk = int(rng.integers(1, 6)); g = rng.integers(10**3, 10**8, rk); C = rng.integers(-2, 3, (m, rk)); out.append((f'rank{rk}', list(C @ g)))
    for _ in range(30):   # mixtures: block of equal / AP / +- pairs embedded in generic
        z = int(rng.integers(2, m)); kind = rng.integers(3); gen = list(rng.integers(10**6, 10**9, m - z))
        blk = [7]*z if kind == 0 else (list(range(1, z+1)) if kind == 1 else [((-1)**i)*(i//2 + 1) for i in range(z)])
        out.append((['eq', 'AP', 'pm'][kind] + f'{z}', blk + gen))
    for _ in range(20): out.append(('small-range', list(rng.integers(-4, 5, m))))
    return out
worst = {k: (1e9, None) for k in KS}
for nm, w in planted():
    d, R = stats(w)
    for k in KS:
        if R[k] < worst[k][0]: worst[k] = (R[k], nm, d, w)
print(f'm={m} planted families: ' + ', '.join(f'k={k}: min R={worst[k][0]:+.3f} ({worst[k][1]}, d={worst[k][2]:.2f})' for k in KS), flush=True)
# annealing adversary per k, from the worst planted instance and from random small-range
for k in KS:
    best = worst[k]; cur_w = list(best[3]); cur = best[0]; T0 = 1.0
    for it in range(1200):
        w2 = list(cur_w); i = int(rng.integers(m)); mv = rng.integers(5)
        j = int(rng.integers(m)); l = int(rng.integers(m))
        w2[i] = [w2[j], -w2[j], w2[j] + w2[l], w2[j] - w2[l], int(rng.integers(-6, 7))][mv]
        d2, R2 = stats(w2); temp = T0*(1 - it/1200) + 1e-3
        if R2[k] < cur or rng.random() < math.exp(-(R2[k] - cur)/temp):
            cur_w, cur = w2, R2[k]
            if cur < best[0]: best = (cur, 'anneal', d2, list(w2))
    print(f'm={m} k={k}: adversary min R = {best[0]:+.3f} (d = {best[2]:.2f}; threshold -log2(m+1) = {-math.log2(m+1):.2f}); weights {sorted(int(x) for x in best[3])}', flush=True)
