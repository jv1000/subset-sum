"""C6 (floating): Delta-capacity under k-case affine domination, on the generic or the hull pattern domain.
Usage: python3 -I c6.py which   (which in astra, k16)"""
import json, sys, time
import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.spatial import ConvexHull
TAU = .4898; N = 1024
x = 2*np.pi*np.arange(N)/N; pref = 2 + 2*np.cos(x)
def scores(rc, sc, ncos, nsin, kap):
    j = np.arange(1, ncos+1); B = np.cos(np.outer(x, j))
    if nsin: B = np.hstack([B, np.sin(np.outer(x, np.arange(1, nsin+1)))])
    r, s = B @ rc, B @ sc; F, G = 2.0**r, 2.0**s; Zf, Zg = F.mean(), G.mean(); f, g = F/Zf, G/Zg
    corr = lambda a, b: np.fft.ifft(np.fft.fft(a)*np.conj(np.fft.fft(b))).real/N
    Q = corr(f, g); Bb = (corr(f*r, g) + corr(f, g*s))/Q - np.log2(Zf*Zg); L = np.log2(Q)
    H = np.log2(np.mean(f**kap)*np.mean(g**kap)); return L + (kap-1)*Bb - H, (2-kap)*Bb - 2*L + H
which = sys.argv[1]
if which == 'astra':
    d = json.load(open('astra_in/openai_coverage_candidate.json'))
    u, v = scores(np.array(d['r'], float), np.array(d['s'], float), 6, 0, float(d['kappa']))
else:
    d = json.load(open('candidate_K16.json'))
    u, v = scores(np.array(d['rc'], float), np.array(d['sc'], float), 16, 16, float(d['kappa']))
P = np.c_[u, v]; hull = ConvexHull(P); HV = P[hull.vertices]               # hull vertices, counter-clockwise
def hull_slice(w):
    """[Ulo, Uhi] of the hull at height W = w (None if empty)."""
    xs = []
    for i in range(len(HV)):
        (u1, w1), (u2, w2) = HV[i], HV[(i+1) % len(HV)]
        if (w1 - w) * (w2 - w) <= 0 and w1 != w2: xs.append(u1 + (w - w1)*(u2 - u1)/(w2 - w1))
    return (min(xs), max(xs)) if xs else None
Wmin, Wmax = v.min(), v.max()
def logM(c): return np.log2(np.mean(pref*2.0**(c[0] + c[1]*u + c[2]*v)))
def glogM(c):
    e = pref*2.0**(c[0] + c[1]*u + c[2]*v); e /= e.sum(); return np.array([1.0, np.sum(e*u), np.sum(e*v)])
def constraints_points(D, domain, Wgrid):
    G = TAU - D; a = D/G; pts = []
    for w in Wgrid:
        al = 1.0 if w <= G else G/w; utop = D/al          # S: U < utop
        if domain == 'generic': lo, hi = -w, utop
        else:
            sl = hull_slice(w)
            if sl is None: continue
            lo, hi = sl[0], min(sl[1], utop)
        if lo >= hi: continue
        for U in (lo, hi): pts.append((U, w, D - al*U))
    return np.array(pts)
def region_best(pts, D, start):
    if len(pts) == 0: return -np.inf, None
    A = np.c_[np.ones(len(pts)), pts[:, 0], pts[:, 1]]; phi = pts[:, 2]
    cons = [dict(type='ineq', fun=lambda c: A @ c - phi, jac=lambda c: A)]
    for s1 in (1, -1):
        for s2 in (1, -1): cons.append(dict(type='ineq', fun=lambda c, s1=s1, s2=s2: 30 - 3*s1*c[1] - 4*s2*c[2],
                                            jac=lambda c, s1=s1, s2=s2: np.array([0, -3*s1, -4*s2])))
    r = minimize(logM, start, jac=glogM, method='SLSQP', constraints=cons, options=dict(maxiter=500, ftol=1e-12))
    ok = (A @ r.x - phi).min() > -1e-9
    return (r.fun if ok else np.inf), r.x
def paper_forms(D):
    G = TAU - D; a = D/G; qcap = 30/(4*a + 3)
    m1 = minimize_scalar(lambda p: logM([p*D, -p, 0]), bounds=(1, 10), method='bounded').fun
    m2 = minimize_scalar(lambda q: logM([0, -q, q*a]), bounds=(1, qcap), method='bounded').fun
    return max(m1, m2)
def scheme_value(D, domain, k):
    G = TAU - D; a = D/G
    Wg = np.linspace(max(Wmin, 0), Wmax, 3000) if domain == 'hull' else np.linspace(0, Wmax, 3000)
    # strip cuts: Gamma always; then quantiles of the sampled W range on each side
    lowW, highW = Wg[Wg <= G], Wg[Wg > G]
    k1 = max(1, k//2); k2 = max(1, k - k1)
    cuts = [np.array_split(lowW, k1) if len(lowW) else [], np.array_split(highW, k2) if len(highW) else []]
    worst = -np.inf; forms = []
    for side, parts in enumerate(cuts):
        for seg in parts:
            if len(seg) == 0: continue
            pts = constraints_points(D, domain, seg)
            start = np.array([8*D, -8, 0]) if side == 0 else np.array([0, -8, 8*a])
            val, c = region_best(pts, D, start); forms.append(dict(W=[float(seg[0]), float(seg[-1])], logM=float(val), c=None if c is None else c.tolist()))
            worst = max(worst, val)
    return worst, forms
def capacity(fn):
    lo, hi = .015, .07
    for _ in range(30):
        mid = (lo + hi)/2
        if fn(mid) <= TAU + mid - 3e-6: lo = mid
        else: hi = mid
    return lo
t0 = time.time(); out = dict(which=which, hull_vertices=len(HV), u_range=[float(u.min()), float(u.max())], v_range=[float(Wmin), float(Wmax)])
out['D0_paper_forms_generic'] = capacity(paper_forms)
print(f'[{which}] D0 paper forms: capacity {out["D0_paper_forms_generic"]:.5f} [{time.time()-t0:.0f}s]', flush=True)
for name, dom, k in [('D1_affine2_generic', 'generic', 2), ('D2_affine2_hull', 'hull', 2), ('D3_affine4_hull', 'hull', 4),
                     ('D3_affine8_hull', 'hull', 8), ('D3_affine32_hull', 'hull', 32)]:
    out[name] = capacity(lambda D: scheme_value(D, dom, k)[0])
    out[name + '_forms'] = scheme_value(out[name], dom, k)[1]
    print(f'[{which}] {name}: capacity {out[name]:.5f} [{time.time()-t0:.0f}s]', flush=True)
json.dump(out, open(f'c6_{which}.json', 'w'), indent=1)
