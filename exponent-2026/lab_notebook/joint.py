"""C5-B: relaxed joint M1+M2 bound (floating). Dual of the convex relaxation; outer minimization over (p, q)."""
import numpy as np, json, sys
from scipy.optimize import minimize
TAU = float(sys.argv[1]) if len(sys.argv) > 1 else .4898
NX = 2001
xx = np.linspace(0, np.pi, NX); W = 1 + np.cos(xx)            # even integrand: average over [0, pi] suffices
wts = np.full(NX, 1.0); wts[0] = wts[-1] = .5; wts /= wts.sum()  # trapezoid on [0, pi], normalized
LQ = np.linspace(-60, 60, 24001)                                # log2 Q grid for pointwise inf (floating)
def psi_mean(lam, nu, p, q, a, D):
    Q = 2.0 ** LQ
    term = lam * 2.0**(p*D) * Q**(-p) + (1-lam) * np.maximum(Q**(-q), Q**(-q*(1+a)))   # shape (nq,)
    # psi(w) = min_Q [ w*term + nu*Q ];  evaluate for each w
    vals = np.min(W[:, None] * term[None, :] + nu * Q[None, :], axis=1)
    return float(np.sum(wts * vals))
def dual_value(p, q, a, D):
    # maximize over lam in [0,1], nu >= 0 of 2*(mean psi - nu)
    best = -np.inf; arg = None
    for lam in np.linspace(0, 1, 21):
        f = lambda t: -(psi_mean(lam, np.exp(t[0]), p, q, a, D) - np.exp(t[0]))
        r = minimize(f, [0.0], method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-10))
        val = -r.fun
        if val > best: best, arg = val, (lam, float(np.exp(r.x[0])))
    return 2 * best, arg
def relaxed_ok(D):
    a = D / (TAU - D); qmax = 30 / (4*a + 3)
    best = (np.inf, None)
    for p in np.linspace(1, 10, 19):
        for q in np.linspace(1, qmax, 12):
            v, arg = dual_value(p, q, a, D)
            if v < best[0]: best = (v, (p, q, arg))
    return np.log2(best[0]) <= TAU + D, best
if __name__ == '__main__':
    out = {}
    for D in [.029, .032, .035, .038, .0427]:
        ok, best = relaxed_ok(D)
        out[D] = dict(feasible_in_relaxation=bool(ok), log2_minmax=float(np.log2(best[0])), eta=TAU + D, pq=best[1])
        print(f'Delta={D}: relaxed min over (p,q) of log2 max(M1,M2) >= {np.log2(best[0]):.5f}  vs eta {TAU+D:.5f}  '
              f'-> {"feasible" if ok else "EXCLUDED"}  at p,q,(lam,nu)={best[1]}', flush=True)
    json.dump({str(k): v for k, v in out.items()}, open(f'joint_{TAU}.json', 'w'), indent=1)
