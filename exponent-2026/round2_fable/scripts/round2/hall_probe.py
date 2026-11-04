"""A4: brute-force Hall's condition on small instances for the fiber bipartite graphs G1 (witness-compatible) and G2
(difference is a weight value). Hall: for every Y subset of Sigma_{k+1}: (k+1)|Y| <= (m-k)|N(Y)|.  We check all Y when
s_{k+1} <= 18, else random Y."""
import itertools, random
from collections import defaultdict
random.seed(5)
def fibers(w, j):
    D = defaultdict(list)
    for A in itertools.combinations(range(len(w)), j): D[sum(w[i] for i in A)].append(frozenset(A))
    return D
def graphs(w, k):
    m = len(w); Fk, Fk1 = fibers(w, k), fibers(w, k+1); W = set(w)
    G1 = {y: set() for y in Fk1}; G2 = {y: set() for y in Fk1}
    for y, Zs in Fk1.items():
        U = set().union(*Zs)
        for g in U: G1[y].add(y - w[g])
        for x in Fk:
            if y - x in W: G2[y].add(x)
    return Fk, Fk1, G1, G2
def hall(G, k, m, ys):
    worst = 10**9
    if len(ys) <= 18:
        subsets = (c for r in range(1, len(ys)+1) for c in itertools.combinations(ys, r))
    else:
        subsets = (random.sample(ys, random.randint(1, len(ys))) for _ in range(20000))
    for Y in subsets:
        N = set().union(*(G[y] for y in Y))
        worst = min(worst, (m-k)*len(N) - (k+1)*len(Y))
    return worst
fam = []
for m in range(6, 11):
    fam += [('equal', [1]*m), ('two-valued', [1]*(m//2) + [2]*(m-m//2)), ('three-equal+gen', [7]*3 + [100*3**i for i in range(m-3)]),
            ('AP', list(range(1, m+1))), ('+-AP', [((-1)**i)*(i//2+1) for i in range(m)]), ('pairs', [i//2+1 for i in range(m)]),
            ('1,1,2 blocks', [1,1,2]*(m//3) + [5]*(m-3*(m//3)))]
    for _ in range(25): fam.append(('rand', [random.randint(-3, 3) for _ in range(m)]))
    for _ in range(10): fam.append(('rand2', [random.randint(1, 4) for _ in range(m)]))
res = {'G1': (10**9, None), 'G2': (10**9, None)}
cnt = 0
for name, w in fam:
    m = len(w)
    for k in range(1, m//2):
        Fk, Fk1, G1, G2 = graphs(w, k); ys = list(Fk1)
        for gn, G in (('G1', G1), ('G2', G2)):
            h = hall(G, k, m, ys); cnt += 1
            if h < res[gn][0]: res[gn] = (h, (name, w, k))
print('instances x k:', cnt)
for gn in ('G1', 'G2'): print(gn, 'min over all Y of (m-k)|N(Y)| - (k+1)|Y| =', res[gn][0], 'at', res[gn][1], '-> Hall', 'HOLDS' if res[gn][0] >= 0 else 'FAILS')
