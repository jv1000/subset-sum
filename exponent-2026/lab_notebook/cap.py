"""C4-cap: moment capacity Delta_cap(tau) for a density family (floating). Usage: python3 -I cap.py tau which nc box"""
import json, sys, time
import numpy as np
from scipy.optimize import minimize
N = 256
def scores(rr, ss, kap):
    nc = len(rr); x = 2*np.pi*np.arange(N)/N; C = np.cos(np.outer(x, np.arange(1, nc+1)))
    r, s = C @ rr, C @ ss; F, G = 2.0**r, 2.0**s; Zf, Zg = F.mean(), G.mean(); f, g = F/Zf, G/Zg
    corr = lambda a, b: np.fft.ifft(np.fft.fft(a)*np.conj(np.fft.fft(b))).real/N
    Q = corr(f, g)
    if Q.min() <= 0: return None
    B = (corr(f*r, g) + corr(f, g*s))/Q - np.log2(Zf*Zg); L = np.log2(Q)
    Hh = np.log2(np.mean(f**kap)*np.mean(g**kap)); u = L + (kap-1)*B - Hh; v = (2-kap)*B - 2*L + Hh
    return x, u, v
def moms(z, nc, tau):
    rr, ss = z[:nc], z[nc:2*nc]; kap, p, q, D = z[2*nc:]
    sc = scores(rr, ss, kap)
    if sc is None: return np.array([50., 50.])
    x, u, v = sc; a = D/(2*tau - tau - D); pref = 2 + 2*np.cos(x)
    return np.log2([np.mean(pref*2**(p*(D-u))), np.mean(pref*2**(q*(a*v-u)))])
tau, which, nc, box = float(sys.argv[1]), sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
r6 = [.85161358, .46593114, .32462492, .25209258, .22313851, -.31246566]; s6 = [1.28132132, -.93838699, .73083896, -.55802400, .38982272, .10981835]
base = np.array(r6 + [0]*(nc-6) + s6 + [0]*(nc-6) + [1.0317, 8.4457, 8.2651, .028])
idx = [0, 1] if which == 'both' else [0]
def cons(z):
    m = moms(z, nc, tau); D = z[-1]; a = D/(tau - D); q = z[-2]
    return np.concatenate([tau + D - 3e-6 - m[idx], [30 - q*(4*a+3), tau - D - 1e-6]])
bnd = [(-box, box)]*(2*nc) + [(.85, 1.3), (1, 10), (1, 9.99), (0, .3)]
best = None; runs = []; t0 = time.time()
for seed in range(6):
    if time.time() - t0 > 300: break
    z0 = base.copy()
    if seed: rng = np.random.default_rng(20261103+seed); z0[:2*nc] += rng.normal(0, .1 if seed < 3 else .3, 2*nc)
    res = minimize(lambda z: -z[-1], z0, method='SLSQP', bounds=bnd, constraints=[dict(type='ineq', fun=cons)], options=dict(maxiter=800, ftol=1e-12))
    c = cons(res.x); ok = c.min() > -1e-9
    runs.append(dict(seed=seed, Delta=float(res.x[-1]), feasible=bool(ok), kappa=float(res.x[2*nc]), p=float(res.x[2*nc+1]), q=float(res.x[2*nc+2]), z=res.x.tolist()))
    if ok and (best is None or res.x[-1] > best['Delta']): best = runs[-1]
print(json.dumps(dict(tau=tau, which=which, nc=nc, box=box, best_Delta=best and best['Delta'], best=best, runs=runs, sec=time.time()-t0)))
print(f'tau={tau} {which} nc={nc} box={box}: Delta_cap={best and round(best["Delta"],5)} kappa={best and round(best["kappa"],3)} p={best and round(best["p"],2)} q={best and round(best["q"],2)} [{time.time()-t0:.0f}s]', file=sys.stderr)
