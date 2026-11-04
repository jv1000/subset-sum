"""A3: monotonicity and DM for weights in finite abelian groups (sum-equivalence in a group).
Layer DP over elements with group addition; cores via class-min counts as in layers.py."""
import random, itertools
from math import comb
random.seed(7)

def layer_data_group(w, add, zero):
    # w: list of group elements; values may repeat; treat each element as its own class (n_i = 1) except we
    # merge equal elements into classes for the core computation.
    from collections import defaultdict
    d = defaultdict(int)
    for x in w: d[x] += 1
    vals = list(d); mult = [d[v] for v in vals]; r = len(vals); m = len(w)
    states = {(0, zero): [0] * r}
    for i, (v, n) in enumerate(zip(vals, mult)):
        new = {}
        for (j, y), t in states.items():
            acc = y
            for c in range(n + 1):
                key = (j + c, acc)
                tt = new.get(key)
                if tt is None:
                    tt = t[:]; tt[i] = c; new[key] = tt
                else:
                    for q in range(i):
                        if t[q] < tt[q]: tt[q] = t[q]
                    if c < tt[i]: tt[i] = c
                acc = add(acc, v)
        states = new
    s = [0] * (m + 1); core = [[0] * r for _ in range(m + 1)]
    for (j, y), t in states.items():
        s[j] += 1
        for i in range(r):
            if t[i] == mult[i]: core[j][i] += 1
    return s, core, mult, m

def probe(w, add, zero):
    s, core, mult, m = layer_data_group(w, add, zero)
    mono_viol = []; dm_viol = []
    for k in range(1, m // 2):
        if (k+1) * s[k+1] > (m-k) * s[k]: mono_viol.append(k)
        for i in range(len(mult)):
            if (k+1)*core[k+1][i] - (m-k-1)*core[k][i] - s[k] > 0: dm_viol.append((k, i)); break
    return mono_viol, dm_viol

groups = {}
for q in range(2, 10):
    groups[f'Z{q}'] = (lambda a, b, q=q: (a + b) % q, 0, list(range(q)))
groups['Z2^2'] = (lambda a, b: tuple((x + y) % 2 for x, y in zip(a, b)), (0, 0), list(itertools.product(range(2), repeat=2)))
groups['Z2^3'] = (lambda a, b: tuple((x + y) % 2 for x, y in zip(a, b)), (0, 0, 0), list(itertools.product(range(2), repeat=3)))
groups['Z3^2'] = (lambda a, b: tuple((x + y) % 3 for x, y in zip(a, b)), (0, 0), list(itertools.product(range(3), repeat=2)))
groups['Z_10^6 (control)'] = (lambda a, b: (a + b) % 10**6, 0, None)
tot = {}
for gname, (add, zero, elems) in groups.items():
    mv = dv = tests = 0; ex = None
    for m in range(6, 15):
        for t in range(120 if elems else 40):
            if elems: w = [random.choice(elems) for _ in range(m)]
            else: w = [random.randint(0, 10**6 - 1) for _ in range(m)]
            a, b = probe(w, add, zero); tests += 1
            if a: mv += 1; ex = ex or ('mono', w, a)
            if b: dv += 1; ex = ex or ('dm', w, b)
        # structured: all equal, two values
        if elems:
            for w in ([elems[1]] * m, [elems[1]] * (m // 2) + [elems[-1]] * (m - m // 2)):
                a, b = probe(w, add, zero); tests += 1
                if a: mv += 1; ex = ex or ('mono', w, a)
                if b: dv += 1; ex = ex or ('dm', w, b)
    print(f'{gname:18s}: tests {tests}, monotonicity violations {mv}, DM violations {dv}; example {ex}')
