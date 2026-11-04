"""C4a: NON-RIGOROUS search for a point below .48977 with the FULL constraint set and K free (fixed per run).
Usage: python3 -I s4.py control | K"""
import importlib.util, json, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.optimize._numdiff import approx_derivative
R = Path(__file__).resolve().parent
sp = importlib.util.spec_from_file_location('astra', R / 'astra_in' / 'search_openai.py')
A = importlib.util.module_from_spec(sp); sp.loader.exec_module(A)
H = A.H; EPS = 1e-8; C = .9999; GUARD = 1e-5
NAMES = ['list', 'pair', 'preliminary', 'moment1', 'moment2', '3p<=30', 'qm(4a+3)<=30', 'strip', 'Delta>0', 'Gamma>0',
         'sparse', 'setup', 'prime', 'p>=1', 'qm>=1', 'blocks']
def h2(x): return -x * np.log2(x) - (1 - x) * np.log2(1 - x)
def residual(z, K):
    mu, eta, tau, gamma = z[:4]; k, p, q = z[16:]; a = (eta - tau) / (2 * tau - eta)
    moms, strip = A.evaluate(z)
    return np.array([tau - (.5 + (H - .5 - gamma) * mu), tau - (1 + (2 * H - 1 - gamma) * mu - eta + GUARD),
                     tau - (.5 - C * K * mu * (.5 - gamma)), eta - moms[0] - 3e-6, eta - moms[1] - 3e-6,
                     30 - 3 * p, 30 - q * (4 * a + 3), .49 - strip, eta - tau, 2 * tau - eta,
                     eta - h2(mu) - mu - GUARD, tau - .25 - mu, tau - eta / 2, p - 1, q - 1, 1 - K * mu])
def bounds(K): return [(.02, 1 / K), (.50, .62), (.46, .495), (.44, .499)] + [(-2.5, 2.5)] * 12 + [(.85, 1.3), (1.0, 9.99), (1.0, 9.99)]
def solve(z0, K):
    b = bounds(K); z0 = np.clip(z0, [x[0] for x in b], [x[1] for x in b])
    res = minimize(lambda z: z[2], z0, method='SLSQP', bounds=b, constraints=[dict(type='ineq', fun=lambda z: residual(z, K))],
                   options=dict(maxiter=1500, ftol=1e-13))
    return res.x, res
def kkt(z, K, tol=1e-6):
    r = residual(z, K); act = [i for i in range(len(r)) if r[i] < tol]
    J = approx_derivative(lambda x: residual(x, K), z, method='3-point', rel_step=1e-6)[act, :]
    obj = np.zeros(19); obj[2] = 1
    w = np.linalg.lstsq(J.T, obj, rcond=None)[0]
    return {NAMES[i]: float(x) for i, x in zip(act, w)}, float(np.max(np.abs(J.T @ w - obj)))
if __name__ == '__main__':
    zb = np.array(json.load(open(R / 'astra_in' / 'search_openai_extended_results.json'))['best'])
    t0 = time.time()
    if sys.argv[1] == 'control':
        z, res = solve(zb, 17); r = residual(z, 17)
        out = dict(start_T=float(zb[2] + 20 * EPS), end_T=float(z[2] + 20 * EPS), min_res=float(r.min()),
                   residuals=dict(zip(NAMES, r.tolist())), msg=str(res.message))
    else:
        K = int(sys.argv[1]); runs = []; best = None
        for seed in range(7):
            z0 = zb.copy(); mu = .97 / K; z0[0] = mu; z0[1] = h2(mu) + mu + .002; z0[2] = .4875; z0[3] = .48
            if seed:
                rng = np.random.default_rng(20261103 + seed); z0[4:16] += rng.normal(0, .12 if seed < 4 else .35, 12)
                z0[16] = rng.uniform(.95, 1.15); z0[17] = rng.uniform(4, 9.0); z0[18] = rng.uniform(4, 9.0)
            z, res = solve(z0, K); r = residual(z, K)
            rec = dict(seed=seed, T=float(z[2] + 20 * EPS), min_res=float(r.min()), residuals=dict(zip(NAMES, r.tolist())),
                       msg=str(res.message), z=z.tolist(), sec=time.time() - t0)
            runs.append(rec)
            print(f'K={K} seed={seed} T={rec["T"]:.7f} min_res={rec["min_res"]:.2e} {rec["msg"][:40]}', file=sys.stderr, flush=True)
            if r.min() > -1e-9 and (best is None or rec['T'] < best['T']): best = rec
        if best:
            zz = np.array(best['z']); best['kkt'] = kkt(zz, K)
            best['moments_256'] = A.evaluate(zz, 256)[0].tolist()
        out = dict(K=K, runs=runs, best=best)
    print(json.dumps(out, indent=1))
