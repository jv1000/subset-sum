"""C3-H rigorous part: interval enclosure (mpmath iv) of  min_{p in [1,10]} Phi(p) at Delta = .1900002, where
Phi(p) = 1 + p Delta + g(p), g(p) = log2 M_{1/(1+p)}(w) is NONINCREASING in p (power-mean monotonicity), so on
[p_i, p_{i+1}]: Phi >= 1 + p_i Delta + g(p_{i+1}).  E[w^b] = 2^b Gamma(b+1/2) / (sqrt(pi) Gamma(b+1)) for w = 1+cos x.
Also: floating checks of the bound against computed moments, and the argmax p of Dmax."""
import json
from fractions import Fraction as F
from mpmath import iv, mp
import numpy as np
from scipy.special import gammaln
iv.prec = 120
def I(x): x = F(x); return iv.mpf(x.numerator)/x.denominator
def g_iv(p):
    b = 1/(1+p)
    E = iv.exp(b*iv.log(2) + iv.log(iv.gamma(b + I('1/2'))) - iv.log(iv.sqrt(iv.pi)) - iv.log(iv.gamma(b + 1)))
    return (1+p)*iv.log(E)/iv.log(2)
D = I('.1900002'); rho_c = I('.669998')
N = 9000; lo_min = None
for i in range(N):
    pi_, pj = I(1) + I(9)*i/N, I(1) + I(9)*(i+1)/N
    lb = 1 + pi_*D + g_iv(pj)
    lo_min = lb.a if lo_min is None or lb.a < lo_min else lo_min
out = dict(certified_lower_bound_min_Phi=str(lo_min), rho_c='.669998', margin_bits=float(lo_min - rho_c.b),
           rejects=bool(lo_min > rho_c.b), cells=N)
# floating sanity: bound <= actual log2 M1 at known points
def gf(p): b = 1/(1+p); return (1+p)*np.log2(np.exp(b*np.log(2)+gammaln(b+.5)-.5*np.log(np.pi)-gammaln(b+1)))
r = json.load(open('moments_c3_results.json'))
out['check_D2_best'] = dict(log2M1=r['D2']['best']['log2M1'], bound=1 + 1*.1900002 + gf(1.0))
out['check_old_point'] = dict(log2M1=r['MC0']['mine'][0], bound=1 + 8.44568508*(.51787037-.4897734) + gf(8.44568508))
P = np.linspace(1.0001, 10, 200000); Gv = gf(P)
for tau in [.48, .485]:
    k = np.argmax((tau-1-Gv)/(P-1)); out[f'argmax_p_Dmax_{tau}'] = float(P[k])
print(json.dumps(out, indent=1)); json.dump(out, open('holder_cert.json', 'w'), indent=1)
