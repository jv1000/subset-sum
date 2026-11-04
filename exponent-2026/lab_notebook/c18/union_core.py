"""C21b: verify  sum_{y in S_{k+1}} |U(y)| = sum_{x in S_k} (m - |C(x)|)   (U = union, C = intersection of witnesses)
and the equivalent form of monotonicity:  (m-k)|S_k| - (k+1)|S_{k+1}| = sum_y (|U(y)|-(k+1)) - sum_x (k-|C(x)|)."""
import itertools, numpy as np, math
rng = np.random.default_rng(7)
def check(w):
    m = len(w); ok = True; rows = []
    for k in range(1, m//2):
        def wit(kk):
            D = {}
            for A in itertools.combinations(range(m), kk):
                D.setdefault(sum(w[i] for i in A), []).append(set(A))
            return D
        Dk, Dk1 = wit(k), wit(k+1)
        U = {y: set().union(*Ws) for y, Ws in Dk1.items()}; C = {x: set.intersection(*Ws) for x, Ws in Dk.items()}
        lhs = sum(len(u) for u in U.values()); rhs = sum(m - len(c) for c in C.values())
        excess = sum(len(u) - (k+1) for u in U.values()); deficit = sum(k - len(c) for c in C.values())
        mono_gap = (m - k)*len(Dk) - (k+1)*len(Dk1)
        ok &= (lhs == rhs) and (mono_gap == excess - deficit)
        rows.append((k, lhs, rhs, excess, deficit, mono_gap))
    return ok, rows
tests = [[1]*10, list(range(1, 11)), [1]*5 + [2]*5, [((-1)**i)*(i//2+1) for i in range(10)]] + [list(rng.integers(-3, 4, 10)) for _ in range(30)] + [list(rng.integers(-2, 3, 12)) for _ in range(5)]
allok = True
for w in tests:
    ok, rows = check(w); allok &= ok
print('identity and equivalence hold on all', len(tests), 'instances:', allok)
ok, rows = check([1]*5 + [2]*5)
print('two-valued m=10 (k, sum|U|, sum(m-|C|), excess, deficit, (m-k)|S_k|-(k+1)|S_k+1|):', rows)
