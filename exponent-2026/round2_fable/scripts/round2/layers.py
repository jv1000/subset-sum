"""Exact layer data for a weight multiset via value classes (values v_i with multiplicities n_i).
A j-sum y is represented by compositions c (0<=c_i<=n_i, sum c_i = j, sum c_i v_i = y).
We record, per (j, y): the minimum count t_i(y) of each class over representations.
 e of class i lies in the core C(y)  iff  t_i(y) = n_i   (swap argument: all copies needed).
Returns s[j] = |Sigma_j|, and core counts n_i^{(j)} = #{y in Sigma_j : t_i(y) = n_i}."""
from collections import defaultdict
from math import comb

def classes(w):
    d = defaultdict(int)
    for x in w: d[x] += 1
    vals = sorted(d); return vals, [d[v] for v in vals]

def layer_data(w):
    vals, mult = classes(w); r = len(vals); m = sum(mult)
    # states: dict (j, y) -> list of min counts per class (length r), built class by class
    states = {(0, 0): [0] * r}
    for i, (v, n) in enumerate(zip(vals, mult)):
        new = {}
        for (j, y), t in states.items():
            for c in range(n + 1):
                key = (j + c, y + c * v)
                tt = new.get(key)
                if tt is None:
                    tt = t[:]; tt[i] = c; new[key] = tt
                else:
                    # min over representations, coordinatewise
                    for q in range(i): 
                        if t[q] < tt[q]: tt[q] = t[q]
                    if c < tt[i]: tt[i] = c
        states = new
    s = [0] * (m + 1); core = [[0] * r for _ in range(m + 1)]
    for (j, y), t in states.items():
        s[j] += 1
        for i in range(r):
            if t[i] == mult[i]: core[j][i] += 1
    return dict(vals=vals, mult=mult, m=m, s=s, core=core)   # core[j][i] = n_e^{(j)} for e of class i

def a(ld, j): return ld['s'][j] / comb(ld['m'], j)
