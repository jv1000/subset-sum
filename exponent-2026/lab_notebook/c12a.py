"""C12-A (floating): Base budget — min tau0 s.t. alias constraints C1–C8 and eta - tau0 <= Delta_cap(tau0)."""
import numpy as np, json
from scipy.optimize import minimize
def h(x): return -(x*np.log2(x) + (1-x)*np.log2(1-x))
SL = 1e-6
def cons(z, delta, s=.166):
    t, eta, mu, a, g, l = z; r = 1 - mu - l
    cap = .02844 + s*(t - .48769) + delta
    return np.array([h(2*a)/2 - g - SL,                                   # C1
        t - (l + (h(a) - g)*mu) - SL,                                      # C2
        t - (r + (1 - g)*mu) - SL,                                         # C3
        t - (1 - mu + (h(a) + h(.5 - a) - g)*mu - eta) - SL,               # C4
        t - (h(.5 - a)*mu + .5 - t) - SL,                                  # C5
        r - SL, t - r - SL, t - l - SL,                                    # C6
        l - mu*(1 - 2*a) - SL,                                             # C7
        eta - mu/2*np.log2(3) - SL,                                        # C8
        cap - (eta - t)])                                                  # checksum capacity
base = np.array([.48769, .51613, .473, .0082, .06035, .48377])
out = {}
for delta in [0, .0005, .001, .0015, .002]:
    best = None
    for k in range(8):
        z0 = base*(1 + np.random.default_rng(k).normal(0, .002 if k else 0, 6))
        r = minimize(lambda z: z[0], z0, method='SLSQP', bounds=[(.47, .495), (.50, .54), (.3, .6), (.001, .05), (.01, .2), (.3, .6)],
                     constraints=[dict(type='ineq', fun=lambda z: cons(z, delta))], options=dict(maxiter=1000, ftol=1e-14))
        c = cons(r.x, delta)
        if c.min() > -1e-10 and (best is None or r.x[0] < best[0]): best = r.x
    out[delta] = dict(tau0=float(best[0]), T=float(best[0] + 20e-8), eta=float(best[1]), mu=float(best[2]), a=float(best[3]), gamma=float(best[4]), l=float(best[5]),
                      Delta=float(best[1] - best[0]))
    print(f'delta={delta:.4f}: tau0* = {best[0]:.7f} (T = {best[0]+2e-7:.7f})  eta={best[1]:.5f} mu={best[2]:.4f} a={best[3]:.5f} gamma={best[4]:.5f} l={best[5]:.5f} Delta={best[1]-best[0]:.5f}')
ts = [out[d]['tau0'] for d in sorted(out)]; ds = sorted(out)
print('slope dtau0/ddelta ~', np.polyfit(ds, ts, 1)[0])
json.dump({str(k): v for k, v in out.items()}, open('c12a.json', 'w'), indent=1)
