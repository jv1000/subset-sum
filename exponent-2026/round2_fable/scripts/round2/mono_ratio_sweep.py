r"""A7: how bad can monotonicity violations be?  Exhaustive [-6,6] at m = 10, 11 (DP over value classes) plus random
'cluster + large' instances at m = 10..14.  Tracks middle-step and interior ratios, the max a_t/a_k for t >= k, and
the direct [S] quantity a_k 2^{d(M)} (m+1).  Time-capped."""
import sys, os, itertools, time, random, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dm_exhaustive import multisets
from math import comb
random.seed(8); t0 = time.time(); CAP = 25 * 60

def sizes(vals, mult):
    m = sum(mult); states = {(0, 0)}
    for v, n in zip(vals, mult):
        states = {(j + c, y + c * v) for (j, y) in states for c in range(n + 1)}
    s = [0] * (m + 1); tot = set()
    for j, y in states: s[j] += 1; tot.add(y)
    return s, len(tot)

def stats(vals, mult, acc):
    s, tot = sizes(vals, mult); m = sum(mult)
    a = [s[j] / comb(m, j) for j in range(m + 1)]
    d = m - math.log2(tot)
    for k in range(1, m // 2):
        r = a[k] / a[k + 1]
        key = 'mid' if k + 1 == m / 2 else 'int'
        if r < acc[key][0]: acc[key] = (r, (vals, mult, k))
    for k in range(1, m // 4 + 1):
        R = max(a[t] for t in range(k, m - k + 1)) / a[k]
        if R > acc['R'][0]: acc['R'] = (R, (vals, mult, k))
        q = a[k] * 2 ** d * (m + 1)
        if q < acc['q'][0]: acc['q'] = (q, (vals, mult, k))

acc = {'mid': (9, None), 'int': (9, None), 'R': (0, None), 'q': (9e9, None)}
n = 0
for m in (10, 11):
    for vals, mult in multisets(list(range(-6, 7)), m):
        stats(vals, mult, acc); n += 1
        if time.time() - t0 > CAP: break
    print(f"m={m} done ({n} instances): min mid ratio {acc['mid'][0]:.5f} {acc['mid'][1]}; min interior ratio {acc['int'][0]:.5f} {acc['int'][1]}; max a_t/a_k {acc['R'][0]:.4f} {acc['R'][1]}; min [S] q {acc['q'][0]:.3f} {acc['q'][1]}  [{time.time()-t0:.0f}s]", flush=True)
    if time.time() - t0 > CAP: print("time cap"); break
# random cluster + large instances
for m in range(10, 15):
    for t in range(600 if m <= 12 else 150):
        if time.time() - t0 > CAP: break
        c = random.randint(m - 4, m - 1); small = [random.randint(-4, 4) for _ in range(c)]; large = [random.randint(5, 12) * random.choice([-1, 1]) for _ in range(m - c)]
        w = small + large; vals = sorted(set(w)); mult = [w.count(v) for v in vals]
        stats(vals, mult, acc)
print(f"FINAL: min middle ratio {acc['mid']}; min interior ratio {acc['int']}; max a_t/a_k (k<=m/4) {acc['R']}; min [S] q = a_k 2^d (m+1) {acc['q']}  [{time.time()-t0:.0f}s]")
