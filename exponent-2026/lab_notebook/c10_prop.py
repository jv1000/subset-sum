"""Check of the proposition: at the M1-optimal p (resp. M2-optimal q) the tilted mean pattern lies on the sampling
boundary (E_t u = Delta, resp. E_t[a v - u] = 0) and has amplitude psi'(1); its W must lie on the region's side of Gamma.
Also: its large-deviation rate KL(t || uniform) in bits (must be < eta for such frequencies to occur)."""
import json, numpy as np
from scipy.optimize import minimize_scalar
exec(open('c9.py').read().split("Wmax = float(v.max())")[0].replace("which = sys.argv[1]", "which = 'k16'"))
TAU = .4898; out = {}
for which_, D in [('k16', .02906)]:
    G = TAU - D; a = D/G; qcap = 30/(4*a + 3)
    for name, R, lo, hi in [('M1', lambda t: t*(D - u), 1, 10), ('M2', lambda t: t*(a*v - u), 1, qcap)]:
        f = lambda t: np.log2(np.mean(2.0**(lam + R(t))))
        r = minimize_scalar(f, bounds=(lo, hi), method='bounded', options=dict(xatol=1e-10)); t = r.x
        wt = 2.0**(lam + R(t)); wt /= wt.sum()
        Eu, Ev, El = float(wt @ u), float(wt @ v), float(wt @ lam)
        rate = float(wt @ np.log2(wt*len(wt)))
        out[name] = dict(multiplier=float(t), log2M=float(r.fun), E_u=Eu, E_v=Ev, E_lambda_psi_prime=El, Delta=D, Gamma=G,
                         boundary_residual=(Eu - D) if name == 'M1' else (a*Ev - Eu), W_side_ok=bool(Ev <= G) if name == 'M1' else bool(Ev >= G),
                         rate_bits=rate, eta=TAU + D)
print(json.dumps(out, indent=1)); json.dump(out, open('c10_prop.json', 'w'), indent=1)
