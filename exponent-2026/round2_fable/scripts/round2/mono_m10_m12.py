r"""A9: exhaustive monotonicity check at m = 10 (values in [-8,8]) and m = 12 (values in [-6,6]), sizes only, capped."""
import itertools, time, sys
from math import comb
t0 = time.time(); CAP = 28 * 60
def sizes(w):
    from collections import Counter
    states = {(0, 0)}
    for v, n in Counter(w).items():
        states = {(j + c, y + c * v) for (j, y) in states for c in range(n + 1)}
    s = [0] * (len(w) + 1)
    for j, y in states: s[j] += 1
    return s
for m, R in ((10, 8), (12, 6)):
    worst = {'mid': (9, None), 'int': (9, None)}; viol = []; n = 0
    for w in itertools.combinations_with_replacement(range(-R, R + 1), m):
        s = sizes(w); n += 1
        for k in range(1, m // 2):
            r = ((m - k) * s[k]) / ((k + 1) * s[k + 1])
            key = 'mid' if k + 1 == m // 2 else 'int'
            if r < worst[key][0]: worst[key] = (r, (w, k, s))
            if r < 1: viol.append((w, k, r))
        if time.time() - t0 > CAP: print('time cap at', n); break
    print(f"m={m} [-{R},{R}]: {n} multisets; min middle ratio {worst['mid'][0]:.5f} at {worst['mid'][1]}; min interior ratio {worst['int'][0]:.5f}; violations {len(viol)}; by k: {sorted(set(k for _, k, _ in viol))}  [{time.time()-t0:.0f}s]", flush=True)
    for w, k, r in viol[:5]: print("   ", w, k, r)
