"""C18: asymptotic test of 'small layers are robust':  R/m = lim (log2 a_k(M) + d(M))/m  for k = alpha*m,
M = q disjoint copies of a gadget B (b elements, arbitrary signed integer weights), copies separated generically.
 d/m = 1 - log2(C)/b,  C = |Sigma(B)|.
 log2|Sigma_k(M)|/m = (1/b) max { H(pi) : pi on Sigma(B), E_pi[lo] <= alpha*b <= E_pi[hi] }
   (lo(x), hi(x) = least / greatest layer containing value x; a tuple reaches total k iff sum lo <= k <= sum hi,
    exact for interval layer-sets, up to parity for gapped ones (poly factor only))
 log2 binom(m,k)/m = h(alpha).   Conjecture needs R/m >= 0 for small alpha."""
import numpy as np, itertools, math, sys
from scipy.optimize import minimize
rng = np.random.default_rng(1818)
def h(a): return 0. if a <= 0 or a >= 1 else -(a*math.log2(a) + (1-a)*math.log2(1-a))
def gadget(w):
    b = len(w); vals = {}
    for mask in range(1 << b):
        s = 0; c = 0
        for i in range(b):
            if mask >> i & 1: s += w[i]; c += 1
        lo, hi = vals.get(s, (99, -1)); vals[s] = (min(lo, c), max(hi, c))
    LH = np.array(list(vals.values()), float); return LH[:, 0], LH[:, 1], len(vals), b
def maxent(lo, hi, A):
    # max H (nats) s.t. E lo <= A <= E hi ; dual: min_{l1,l2>=0} log sum exp(-l1 lo + l2 hi) + l1 A - l2 A
    def g(l):
        l1, l2 = np.exp(l)  # keep >= 0
        e = -l1*lo + l2*hi; M = e.max(); return M + math.log(np.exp(e - M).sum()) + (l1 - l2)*A
    best = min((minimize(g, x0, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-12, maxiter=4000)) for x0 in
                ([-8., -8.], [0., -8.], [-8., 0.], [1., 1.], [2., -3.])), key=lambda r: r.fun)
    # also the unconstrained max (log C) if feasible
    if lo.mean() <= A <= hi.mean(): return math.log(len(lo))
    return min(best.fun, math.log(len(lo)))
def R(w, alpha):
    lo, hi, C, b = gadget(w)
    Hb = maxent(lo, hi, alpha*b)/math.log(2)
    return (1 - math.log2(C)/b) - h(alpha) + Hb/b
alphas = [0.005, 0.0074, 0.01, 0.02, 0.05, 0.1, 0.2]
tests = {'generic b=8': [3**i for i in range(8)], 'pairs x,x (b=2)': [1, 1], 'pairs x,-x (b=2)': [1, -1],
         'all equal b=12': [1]*12, 'AP 1..10': list(range(1, 11)), '+-AP b=10': [1, -1, 2, -2, 3, -3, 4, -4, 5, -5],
         'triple 1,1,2': [1, 1, 2], 'quad a+b=c+d': [1, 4, 2, 3], 'zeros+gen': [0, 0, 0, 1, 3, 9]}
for nm, w in tests.items():
    print(f'{nm:18s}', ' '.join(f'{R(w, a):+.4f}' for a in alphas))
print('alphas:', alphas)
