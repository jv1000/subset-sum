"""C5-A: Delta-capacity with general (cos+sin) log-densities. Floating. Usage:
python3 -I cap2.py which n sines box kmin kmax N  (which in m1, m2, both; sines 0/1)"""
import json, sys, time
import numpy as np
from scipy.optimize import minimize
TAU = .4898
import os
START = os.environ.get('START', 'astra')
which, n, sines, box, kmin, kmax, N = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7])
nt = n * (2 if sines else 1)
def basis(N):
    x = 2*np.pi*np.arange(N)/N; j = np.arange(1, n+1)
    B = np.cos(np.outer(x, j))
    if sines: B = np.hstack([B, np.sin(np.outer(x, j))])
    return x, B
def evalz(z, N):
    x, B = basis(N)
    r, s = B @ z[:nt], B @ z[nt:2*nt]; kap, p, q, D = z[2*nt:]
    F, G = 2.0**r, 2.0**s; Zf, Zg = F.mean(), G.mean(); f, g = F/Zf, G/Zg
    corr = lambda a, b: np.fft.ifft(np.fft.fft(a)*np.conj(np.fft.fft(b))).real/N
    Q = corr(f, g)
    if Q.min() <= 0: return None
    B_ = (corr(f*r, g) + corr(f, g*s))/Q - np.log2(Zf*Zg); L = np.log2(Q)
    H = np.log2(np.mean(f**kap)*np.mean(g**kap)); u = L + (kap-1)*B_ - H; v = (2-kap)*B_ - 2*L + H
    a = D/(TAU - D); pref = 2 + 2*np.cos(x)
    m = np.log2([np.mean(pref*2.0**(p*(D-u))), np.mean(pref*2.0**(q*(a*v-u)))])
    nf = np.mean(2**(2*r))/Zf**2; ng = np.mean(2**(2*s))/Zg**2   # unshifted proxy only
    return m, a, (nf-1)*(ng-1)
idx = {'m1': [0], 'm2': [1], 'both': [0, 1]}[which]
def cons(z):
    e = evalz(z, N)
    if e is None: return -np.ones(len(idx)+2)
    m, a, _ = e; D = z[-1]; q = z[-2]
    return np.concatenate([TAU + D - 3e-6 - m[idx], [30 - q*(4*a+3), TAU - D - 1e-6]])
r6 = [.85161358, .46593114, .32462492, .25209258, .22313851, -.31246566]; s6 = [1.28132132, -.93838699, .73083896, -.55802400, .38982272, .10981835]
def pad(c): v = np.zeros(nt); v[:min(6, n)] = c[:min(6, n)]; return v
base = np.concatenate([pad(r6), pad(s6), [1.0317, 8.4457, 8.2651, .028]])
bnd = [(-box, box)]*(2*nt) + [(kmin, kmax), (1, 10), (1, 9.99), (0, .3)]
runs = []; best = None; t0 = time.time()
for seed in range(int(os.environ.get('NSTART', 4))):
    if time.time() - t0 > 600: break
    z0 = base.copy()
    if seed: z0[:2*nt] += np.random.default_rng(20261103+seed).normal(0, .1, 2*nt)
    if START == 'random':
        rg = np.random.default_rng(777 + seed); z0[:2*nt] = rg.normal(0, .6, 2*nt) / np.sqrt(np.tile(np.arange(1, n+1), 2*nt//n))
        z0[2*nt:] = [rg.uniform(.9, 1.2), rg.uniform(3, 9), rg.uniform(3, 9), .01]
    res = minimize(lambda z: -z[-1], z0, method='SLSQP', bounds=bnd, constraints=[dict(type='ineq', fun=cons)],
                   options=dict(maxiter=600, ftol=1e-12))
    c = cons(res.x); ok = bool(c.min() > -1e-9); e = evalz(res.x, N); e2 = evalz(res.x, 2*N)
    rec = dict(seed=seed, Delta=float(res.x[-1]), feasible=ok, kappa=float(res.x[2*nt]), p=float(res.x[2*nt+1]), q=float(res.x[2*nt+2]),
               moments=e[0].tolist(), moments_2N=e2[0].tolist(), qcap_slack=float(c[len(idx)]), strip_proxy=float(e[2]),
               binding=[nm for nm, cv in zip(['M1', 'M2'][:len(idx)] if which == 'both' else [which.upper()], c[:len(idx)]) if cv < 1e-7],
               z=res.x.tolist(), sec=time.time()-t0, msg=str(res.message))
    runs.append(rec)
    if ok and (best is None or rec['Delta'] > best['Delta']): best = rec
tag = f'{START}_{which}_n{n}_s{sines}_b{box}_k{kmin}-{kmax}_N{N}'
json.dump(dict(tag=tag, tau=TAU, best=best, runs=runs), open(f'cap2_{tag}.json', 'w'), indent=1)
b = best
print(f'{tag}: cap={b and round(b["Delta"],5)} kappa={b and round(b["kappa"],3)} p={b and round(b["p"],2)} q={b and round(b["q"],2)} '
      f'binding={b and b["binding"]} qcap_slack={b and round(b["qcap_slack"],3)} 2N_drift={b and round(max(abs(x-y) for x,y in zip(b["moments"],b["moments_2N"])),2e-9 and 8)} '
      f'all_runs={[round(r["Delta"],5) for r in runs]} [{time.time()-t0:.0f}s]', flush=True)
