"""C5-B (floating): capacity of the RELAXED joint problem.  Free profile u(x) = log2 Q(x) on an odd grid of N points
(mean Q <= 1), relaxed moments
   M1' = mean (2+2cos x) 2^{p(Delta - u)},   M2' = mean (2+2cos x) 2^{q(a max(0,-u) - u)},  a = Delta/(tau - Delta),
maximize Delta s.t. log2 M1', log2 M2' <= tau + Delta, 1 <= p <= 10, 1 <= q, q(4a+3) <= 30.
Any real densities give an admissible u (u <= log2 Q*, v >= max(0,-u)), so this capacity is an UPPER bound on the
true joint capacity (up to discretization; floating).  Usage: python3 -I joint2.py tau N [nocap]"""
import numpy as np, json, sys, time
from scipy.optimize import minimize
TAU = float(sys.argv[1]); N = int(sys.argv[2]); NOCAP = len(sys.argv) > 3
x = 2*np.pi*np.arange(N)/N; pref = 2 + 2*np.cos(x)
def parts(z):
    u = z[:N]; p, q, D = z[N:]
    a = D/(TAU - D)
    e1 = p*(D - u); e2 = q*(a*np.maximum(0, -u) - u)
    return u, p, q, D, a, e1, e2
def cons(z):
    u, p, q, D, a, e1, e2 = parts(z)
    m1 = np.log2(np.mean(pref*2.0**e1)); m2 = np.log2(np.mean(pref*2.0**e2))
    c = [TAU + D - m1, TAU + D - m2, -np.log2(np.mean(2.0**u)), 30 - 3*p]
    if not NOCAP: c.append(30 - q*(4*a + 3))
    return np.array(c)
def jac(z):
    u, p, q, D, a, e1, e2 = parts(z); J = np.zeros((5 if not NOCAP else 4, N + 3))
    da_dD = TAU/(TAU - D)**2
    w1 = pref*2.0**e1; w1 /= w1.sum(); w2 = pref*2.0**e2; w2 /= w2.sum()
    # d m1: d e1/du = -p, /dp = D-u, /dD = p
    J[0, :N] = p*w1; J[0, N] = -np.sum(w1*(D - u)); J[0, N+2] = 1 - p
    neg = (u < 0).astype(float)
    de2du = q*(-a*neg - 1)
    J[1, :N] = -w2*de2du; J[1, N+1] = -np.sum(w2*(a*np.maximum(0, -u) - u)); J[1, N+2] = 1 - np.sum(w2*q*da_dD*np.maximum(0, -u))
    wu = 2.0**u; wu /= wu.sum(); J[2, :N] = -wu
    J[3, N] = -3
    if not NOCAP: J[4, N+1] = -(4*a + 3); J[4, N+2] = -q*4*da_dD
    return J
best = None; runs = []; t0 = time.time()
for seed in range(6):
    rng = np.random.default_rng(seed)
    beta = rng.uniform(.1, .3)
    u0 = beta*np.log2(np.maximum(1 + np.cos(x), 1e-3)); u0 -= np.log2(np.mean(2.0**u0)) + 1e-3
    z0 = np.concatenate([u0, [rng.uniform(3, 9), rng.uniform(3, 9), .025]])
    bnd = [(-30, 30)]*N + [(1, 10), (1, 60 if NOCAP else 9.99), (0, .2)]
    r = minimize(lambda z: -z[-1], z0, jac=lambda z: np.r_[np.zeros(N + 2), -1.0], method='SLSQP', bounds=bnd,
                 constraints=[dict(type='ineq', fun=cons, jac=jac)], options=dict(maxiter=3000, ftol=1e-13))
    c = cons(r.x); ok = bool(c.min() > -1e-9)
    rec = dict(seed=seed, Delta=float(r.x[-1]), ok=ok, p=float(r.x[N]), q=float(r.x[N+1]), minc=float(c.min()), msg=str(r.message))
    runs.append(rec)
    if ok and (best is None or rec['Delta'] > best['Delta']): best = dict(rec, u=r.x[:N].tolist())
print(f'tau={TAU} N={N} cap={"none" if NOCAP else "q(4a+3)<=30"}: relaxed joint capacity ~ {best and round(best["Delta"], 5)} '
      f'(p {best and round(best["p"], 3)}, q {best and round(best["q"], 3)}); runs {[round(r["Delta"], 5) for r in runs]} '
      f'[{time.time()-t0:.0f}s]', flush=True)
json.dump(dict(tau=TAU, N=N, nocap=NOCAP, best=best, runs=runs), open(f'joint2_{TAU}_{N}{"_nocap" if NOCAP else ""}.json', 'w'))
