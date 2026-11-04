"""C3 S3/S4: NON-RIGOROUS discovery. Astra's residual with 17 -> K; moment evaluator imported unchanged.
Usage: python3 -I s3.py control | K c0 | deficit K c0"""
import importlib.util, json, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.optimize._numdiff import approx_derivative
R = Path(__file__).resolve().parent
sp = importlib.util.spec_from_file_location('astra', R / 'astra_in' / 'search_openai.py')
A = importlib.util.module_from_spec(sp); sp.loader.exec_module(A)
H = A.H; EPS = 1e-8
NAMES = ['list', 'pair', 'preliminary', 'moment1', 'moment2', '3p<=30', 'qm(4a+3)<=30', 'strip', 'eta>tau', 'eta<2tau']
def residual(z, K, c):
    mu, eta, tau, gamma = z[:4]; k, p, q = z[16:]; a = (eta - tau) / (2 * tau - eta)
    moms, strip = A.evaluate(z)
    return np.array([tau - (.5 + (H - .5 - gamma) * mu), tau - (1 + (2 * H - 1 - gamma) * mu - eta + .00001),
                     tau - (.5 - c * K * mu * (.5 - gamma)), eta - moms[0] - 3e-6, eta - moms[1] - 3e-6,
                     30 - 3 * p, 30 - q * (4 * a + 3), .49 - strip, eta - tau, 2 * tau - eta])
def from_json(f):
    d = json.load(open(f))
    return np.array([float(d[k]) for k in ['mu', 'eta', 'tau', 'gamma']] + [float(x) for x in d['r']] +
                    [float(x) for x in d['s']] + [float(d['kappa']), float(d['p']), float(d['q'])])
def bounds(K): return [(.04, 1 / K), (.50, .62), (.46, .495), (.44, .499)] + [(-2.5, 2.5)] * 12 + [(.85, 1.3), (1.01, 9.99), (1.01, 9.99)]
def kkt(z, K, c, tol=1e-6):
    r = residual(z, K, c); act = [i for i in range(10) if r[i] < tol]
    J = approx_derivative(lambda x: residual(x, K, c), z, method='3-point', rel_step=1e-6)[act, :]
    obj = np.zeros(19); obj[2] = 1
    w = np.linalg.lstsq(J.T, obj, rcond=None)[0]
    return {NAMES[i]: float(x) for i, x in zip(act, w)}, float(np.max(np.abs(J.T @ w - obj)))
def solve(z0, K, c, ids=np.arange(19)):
    def un(x): z = z0.copy(); z[ids] = x; return z
    b = bounds(K)
    x0 = np.clip(z0[ids], [b[i][0] for i in ids], [b[i][1] for i in ids])
    res = minimize(lambda x: un(x)[2], x0, method='SLSQP', bounds=[b[i] for i in ids],
                   constraints=[dict(type='ineq', fun=lambda x: residual(un(x), K, c))], options=dict(maxiter=1500, ftol=1e-13))
    return un(res.x), res
def deficit(z0, K, c, tau_t=.48 - 20 * EPS):
    """maximize s s.t. moment residuals >= s, all other residuals >= 0, tau = tau_t. variables: z (tau fixed) + s"""
    ids = np.array([i for i in range(19) if i != 2])
    b = bounds(K)
    def un(x): z = z0.copy(); z[ids] = x[:-1]; z[2] = tau_t; return z
    def cons(x):
        r = residual(un(x), K, c); r[3] -= x[-1]; r[4] -= x[-1]; return r
    x0 = np.append(np.clip(z0[ids], [b[i][0] for i in ids], [b[i][1] for i in ids]), -0.05)
    res = minimize(lambda x: -x[-1], x0, method='SLSQP', bounds=[b[i] for i in ids] + [(-1, 1)],
                   constraints=[dict(type='ineq', fun=cons)], options=dict(maxiter=2000, ftol=1e-13))
    z = un(res.x); return z, float(res.x[-1]), res
if __name__ == '__main__':
    t0 = time.time(); out = {}
    if sys.argv[1] == 'control':
        for f in ['openai_candidate.json', 'openai_coverage_candidate.json']:
            z = from_json(R / 'astra_in' / f); c = .995 if 'coverage' not in f else .9999
            r = residual(z, 17, c); out[f] = dict(min_residual=float(r.min()), T=z[2] + 20 * EPS, residuals=dict(zip(NAMES, r.tolist())))
        zb = np.array(json.load(open(R / 'astra_in' / 'search_openai_extended_results.json'))['best'])
        z, res = solve(zb, 17, .995)
        out['K-c'] = dict(start_tau=float(zb[2]), end_tau=float(z[2]), min_res=float(residual(z, 17, .995).min()), msg=str(res.message))
        out['K-c_kkt_at_astra_best'] = kkt(zb, 17, .995, tol=1e-5)
    elif sys.argv[1] == 'deficit':
        K, c = int(sys.argv[2]), 1 - float(sys.argv[3]); zb = from_json(R / 'astra_in' / 'openai_candidate.json')
        zb[0] = 1 / K; runs = []; best = None
        for seed in range(7):
            z0 = zb.copy()
            if seed:
                rng = np.random.default_rng(20261103 + seed); z0[4:16] += rng.normal(0, .12 if seed < 4 else .35, 12)
                z0[16] = rng.uniform(.95, 1.15); z0[17:] = rng.uniform(6.5, 9.0, 2)
            z, s, res = deficit(z0, K, c)
            r = residual(z, K, c); feas = float(min(r[[0, 1, 2, 5, 6, 7, 8, 9]]))
            rec = dict(seed=seed, s=s, other_min=feas, moments=A.evaluate(z)[0].tolist(), moments_256=A.evaluate(z, 256)[0].tolist(),
                       eta=float(z[1]), gamma=float(z[3]), mu=float(z[0]), kappa=float(z[16]), p=float(z[17]), q=float(z[18]),
                       msg=str(res.message), z=z.tolist(), sec=time.time() - t0)
            runs.append(rec); print(seed, s, feas, rec['moments'], z[1], flush=True)
            if feas > -1e-8 and (best is None or s > best['s']): best = rec
        out = dict(K=K, c0=sys.argv[3], tau=.48 - 20 * EPS, runs=runs, best=best)
    else:
        K, c = int(sys.argv[1]), 1 - float(sys.argv[2]); zb = from_json(R / 'astra_in' / 'openai_candidate.json')
        runs = []; best = None
        for seed in range(7):
            z0 = zb.copy(); z0[0] = 1 / K
            if seed:
                rng = np.random.default_rng(20261103 + seed); z0[4:16] += rng.normal(0, .12 if seed < 4 else .35, 12)
                z0[16] = rng.uniform(.95, 1.15); z0[17:] = rng.uniform(6.5, 9.0, 2)
            z, res = solve(z0, K, c); r = residual(z, K, c)
            rec = dict(seed=seed, T=float(z[2] + 20 * EPS), min_res=float(r.min()), residuals=dict(zip(NAMES, r.tolist())),
                       msg=str(res.message), z=z.tolist(), sec=time.time() - t0)
            runs.append(rec); print(seed, rec['T'], rec['min_res'], flush=True)
            if r.min() > -1e-8 and (best is None or rec['T'] < best['T']): best = rec
        if best: best['kkt'] = kkt(np.array(best['z']), K, c)
        out = dict(K=K, c0=sys.argv[2], runs=runs, best=best)
    print(json.dumps(out, indent=1))
