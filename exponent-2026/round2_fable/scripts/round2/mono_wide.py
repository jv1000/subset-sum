r"""A8: (1) exhaustive m = 8, 9 with values in [-8,8]; (2) structured random search m = 10..16 (cluster + large).
Tracks per-position worst ratio a_k/a_{k+1} (middle vs interior) and max_t a_t/a_k for k <= m/4. Time-capped."""
import sys, os, itertools, time, random, math
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
random.seed(12); t0 = time.time(); CAP = 25 * 60

def sizes_w(w):
    from collections import Counter
    cnt = Counter(w); states = {(0, 0)}
    for v, n in cnt.items():
        states = {(j + c, y + c * v) for (j, y) in states for c in range(n + 1)}
    s = [0] * (len(w) + 1)
    for j, y in states: s[j] += 1
    return s

def record(w, acc):
    m = len(w); s = sizes_w(w); a = [s[j] / comb(m, j) for j in range(m + 1)]
    for k in range(1, m // 2):
        r = a[k] / a[k + 1]; key = 'mid' if k + 1 == m / 2 else 'int'
        if r < acc[key][0]: acc[key] = (r, (sorted(w), k, s))
        if r < 1 - 1e-12: acc['viol'].append((sorted(w), k, r))
    for k in range(1, m // 4 + 1):
        R = max(a[t] for t in range(k, m - k + 1)) / a[k]
        if R > acc['R'][0]: acc['R'] = (R, (sorted(w), k))

def multisets(values, m):
    for comb_ in itertools.combinations_with_replacement(values, m): yield list(comb_)

acc = {'mid': (9, None), 'int': (9, None), 'R': (0, None), 'viol': []}
for m in (8, 9):
    n = 0
    for w in multisets(list(range(-8, 9)), m):
        record(w, acc); n += 1
        if time.time() - t0 > CAP: break
    print(f"exhaustive [-8,8] m={m}: {n} multisets; min middle ratio {acc['mid'][0]:.5f} {acc['mid'][1]}; min interior ratio {acc['int'][0]:.5f}; violations so far {len(acc['viol'])}; max a_t/a_k (k<=m/4) {acc['R'][0]:.4f}  [{time.time()-t0:.0f}s]", flush=True)
vi = sorted(set((tuple(w), k) for w, k, r in acc['viol']))
print("distinct violations:", len(vi), "; by m and k:", sorted(set((len(w), k) for w, k in vi)))
acc2 = {'mid': (9, None), 'int': (9, None), 'R': (0, None), 'viol': []}
for m in range(10, 17):
    for t in range(4000 if m <= 12 else 1500):
        if time.time() - t0 > CAP: break
        nl = random.randint(2, 4); c = m - nl
        base = random.sample(range(0, 9), random.randint(2, 5))
        small = [random.choice(base) for _ in range(c)]
        large = [random.randint(12, 40) for _ in range(nl)]
        record(small + large, acc2)
    print(f"structured m={m}: min middle ratio {acc2['mid'][0]:.5f} {acc2['mid'][1][:2] if acc2['mid'][1] else None}; min interior {acc2['int'][0]:.5f}; violations {len(acc2['viol'])}; max a_t/a_k {acc2['R'][0]:.4f}  [{time.time()-t0:.0f}s]", flush=True)
vi2 = sorted(set((tuple(w), k) for w, k, r in acc2['viol']))
print("structured violations:", len(vi2), [ (w, k) for w, k in vi2[:8]])
