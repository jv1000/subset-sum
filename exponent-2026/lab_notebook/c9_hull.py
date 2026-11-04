"""C9 escape test: max Lambda over conv{(u,v,lambda)} ∩ sampling region, vs psi'(1) = E_{2^{lambda - p u}}[lambda]."""
import json, sys, numpy as np
from scipy.optimize import linprog
exec(open('c9.py').read().split("Wmax = float(v.max())")[0].replace("which = sys.argv[1]", "which = sys.argv[1]"))
TAU = .4898
D = {'astra': .0281, 'k16': .02906}[which]; G = TAU - D; a = D/G
p, q = ({'astra': (8.44568508, 8.2651137), 'k16': (8.38520435, 8.19573911)})[which]
wt1 = 2.0**(lam - p*u); psi1 = float(wt1 @ lam / wt1.sum())
wt2 = 2.0**(lam + q*(a*v - u)); psi2 = float(wt2 @ lam / wt2.sum())
fin = np.isfinite(lam); uu, vv, ll = u[fin], v[fin], lam[fin]; n_ = len(uu)
def maxL(extra_A, extra_b):
    r = linprog(-ll, A_ub=extra_A, b_ub=extra_b, A_eq=np.ones((1, n_)), b_eq=[1], bounds=(0, None), method='highs')
    return -r.fun if r.status == 0 else None
# region 1 sampling: U < Delta, W <= Gamma ; region 2: W > Gamma, U < a W  (U - aW < 0)
L1 = maxL(np.vstack([uu, vv]), [D, G])
L2 = maxL(np.vstack([uu - a*vv, -vv]), [0, -G])
out = dict(which=which, psi1_prime=psi1, psi2_prime=psi2, maxLambda_region1=L1, maxLambda_region2=L2,
           escape_region1=bool(L1 is not None and L1 < psi1), escape_region2=bool(L2 is not None and L2 < psi2))
print(json.dumps(out)); json.dump(out, open(f'c9_hull_{which}.json', 'w'), indent=1)
