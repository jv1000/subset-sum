"""C18b: test the Cauchy-Schwarz route.  a_k >= 1/E_A[f_k(A)]  (exact).  Route needs  log2 E_A f_k <= d + o(m).
For gadget products (q copies of block B, generic separation):
  #pairs(A,A') same layer k, same value = [x^k y^k] G(x,y)^q,  G = sum_{U,U' in B, w(U)=w(U')} x^|U| y^|U'|
  log2 #pairs ~ q * min_{s,t} [log2 G(2^s,2^t) - (s+t) k/q]   (saddle point; G has nonneg coeffs)
  log2 E_A f_k = log2 #pairs - log2 binom(m,k);  margin_CS/m = d/m - log2 E f_k / m."""
import numpy as np, math, sys, itertools
from scipy.optimize import minimize
exec(open('gadget.py').read().split("alphas = [")[0])     # brings gadget(), R(), h()
def pairgf(w):
    b = len(w); byval = {}
    for mask in range(1 << b):
        s = sum(w[i] for i in range(b) if mask >> i & 1); c = bin(mask).count('1')
        byval.setdefault(s, []).append(c)
    P = np.zeros((b+1, b+1))
    for cs in byval.values():
        for c1 in cs:
            for c2 in cs: P[c1, c2] += 1
    return P
def logpairs_per_m(w, alpha):
    P = pairgf(w); b = len(w); K = alpha*b
    idx = np.arange(b+1)
    def g(st):
        s, t = st
        e = np.log2(P + 1e-300) + s*idx[:, None] + t*idx[None, :]
        M = e.max(); return (M + math.log2(np.exp2(e - M)[P > 0].sum()) - (s + t)*K)/b
    r = min((minimize(g, x0, method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-12, maxiter=5000)) for x0 in ([-5, -5], [-8, -8], [-3, -3], [0, 0])), key=lambda z: z.fun)
    return r.fun
def margin_cs(w, alpha):
    lo, hi, C, b = gadget(w)
    d = 1 - math.log2(C)/b
    lEf = logpairs_per_m(w, alpha) - h(alpha)
    return d - lEf, d, lEf
alphas = [0.0074, 0.02, 0.1]
tests = {'generic b=8': [3**i for i in range(8)], 'pairs x,x': [1, 1], 'pairs x,-x': [1, -1], 'all equal b=12': [1]*12,
         'AP 1..10': list(range(1, 11)), '+-AP b=10': [1, -1, 2, -2, 3, -3, 4, -4, 5, -5], 'triple 1,1,2': [1, 1, 2],
         'quad a+b=c+d': [1, 4, 2, 3], 'zeros+gen': [0, 0, 0, 1, 3, 9], 'eq block in generic': [1, 1, 1, 1, 1, 1, 100, 1000, 10**4, 10**5, 10**6, 10**7]}
for nm, w in tests.items():
    out = [margin_cs(w, a) for a in alphas]
    print(f'{nm:20s} CS-margin/m: ' + ' '.join(f'{o[0]:+.4f}' for o in out) + f'   (support-margin R/m at .0074: {R(w, .0074):+.4f})')
print('alphas', alphas)
