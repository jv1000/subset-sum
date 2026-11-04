"""C9 (floating): capacity with amplitude-stratified patterns. Usage: python3 -I c9.py astra|k16"""
import json, sys, time
import numpy as np
from scipy.optimize import minimize
TAU = .4898; N = 1023; L0 = 8.0
x = 2*np.pi*np.arange(N)/N; lam = np.log2(2 + 2*np.cos(x))
def scores(rc, sc, ncos, nsin, kap):
    B = np.cos(np.outer(x, np.arange(1, ncos+1)))
    if nsin: B = np.hstack([B, np.sin(np.outer(x, np.arange(1, nsin+1)))])
    r, s = B @ rc, B @ sc; F, G = 2.0**r, 2.0**s; Zf, Zg = F.mean(), G.mean(); f, g = F/Zf, G/Zg
    corr = lambda a, b: np.fft.ifft(np.fft.fft(a)*np.conj(np.fft.fft(b))).real/N
    Q = corr(f, g); Bb = (corr(f*r, g) + corr(f, g*s))/Q - np.log2(Zf*Zg); L = np.log2(Q)
    H = np.log2(np.mean(f**kap)*np.mean(g**kap)); return L + (kap-1)*Bb - H, (2-kap)*Bb - 2*L + H
which = sys.argv[1]
if which == 'astra':
    d = json.load(open('astra_in/openai_coverage_candidate.json')); u, v = scores(np.array(d['r'], float), np.array(d['s'], float), 6, 0, float(d['kappa']))
else:
    d = json.load(open('candidate_K16.json')); u, v = scores(np.array(d['rc'], float), np.array(d['sc'], float), 16, 16, float(d['kappa']))
Wmax = float(v.max())
def logM(c): return np.log2(np.mean(2.0**(c[0] + c[1]*u + c[2]*v + c[3]*lam)))
def glogM(c):
    e = 2.0**(c[0] + c[1]*u + c[2]*v + c[3]*lam); e /= e.sum(); return np.array([1.0, e@u, e@v, e@lam])
def region(D, side, la, lb, fix_c3=None):
    """best affine form on {W-side} x {Lambda in [la, lb]}; generic (U, W): U in [-W, utop(W)], W in [0, Wmax]."""
    G = TAU - D; a = D/G
    Wg = np.linspace(0, G, 60) if side == 0 else np.linspace(G, max(Wmax, G + 1e-6), 60)
    rows, rhs = [], []
    for wv in Wg:
        al = 1.0 if wv <= G else G/wv; utop = D/al
        for U in (-wv, utop):
            for Lm in ([la, lb] if np.isfinite(la) else [lb]):
                rows.append([1, U, wv, Lm]); rhs.append(D - al*U + Lm)
    A = np.array(rows); b = np.array(rhs)
    cons = [dict(type='ineq', fun=lambda c: A @ c - b, jac=lambda c: A)]
    for s1 in (1, -1):
        for s2 in (1, -1):
            for s3 in (1, -1):
                cons.append(dict(type='ineq', fun=lambda c, s1=s1, s2=s2, s3=s3: 29 - 3*s1*c[1] - 4*s2*c[2] - s3*c[3],
                                 jac=lambda c, s1=s1, s2=s2, s3=s3: np.array([0, -3*s1, -4*s2, -s3])))
    bounds = [(None, None), (None, None), (None, None), (0, 1 if not np.isfinite(la) else 6)]
    if fix_c3 is not None: bounds[3] = (fix_c3, fix_c3)
    start = np.array([8*D, -8, 0, 1.0]) if side == 0 else np.array([0, -8, 8*a, 1.0])
    if fix_c3 is not None: start[3] = fix_c3
    r = minimize(logM, start, jac=glogM, method='SLSQP', bounds=bounds, constraints=cons, options=dict(maxiter=600, ftol=1e-12))
    ok = (A @ r.x - b).min() > -1e-9
    return (r.fun if ok else np.inf), r.x
def scheme(D, k, fix_c3=None):
    edges = np.linspace(-L0, 2.0, k + 1)
    strips = [(-np.inf, -L0)] + [(edges[i], edges[i+1]) for i in range(k)] if k > 0 else [(-np.inf, 2.0)]
    worst, forms = -np.inf, []
    for side in (0, 1):
        for (la, lb) in strips:
            val, c = region(D, side, la, lb, fix_c3); worst = max(worst, val); forms.append(dict(side=side, L=[la, lb], logM=float(val), c=c.tolist()))
    return worst, forms
def capacity(fn):
    lo, hi = .015, .08
    for _ in range(26):
        mid = (lo + hi)/2
        if fn(mid) <= TAU + mid - 3e-6: lo = mid
        else: hi = mid
    return lo
out = dict(which=which); t0 = time.time()
for name, k, fx in [('control_k0_c3eq1', 0, 1.0), ('k0_c3free', 0, None), ('k2', 2, None), ('k4', 4, None), ('k8', 8, None), ('k16', 16, None)]:
    cap = capacity(lambda D: scheme(D, k, fx)[0]); out[name] = cap
    out[name + '_forms'] = scheme(cap, k, fx)[1]
    print(f'[{which}] {name}: capacity {cap:.5f} [{time.time()-t0:.0f}s]', flush=True)
json.dump(out, open(f'c9_{which}.json', 'w'), indent=1, default=str)
