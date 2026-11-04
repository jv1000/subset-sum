"""C12-B (floating): Base alias budget + one asymmetric filter (OpenAI two-moment checksum). Minimize tau0."""
import json, sys, time
import numpy as np, jax, jax.numpy as jnp
from scipy.optimize import minimize
jax.config.update('jax_enable_x64', True)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 512; n = 16; nt = 2*n
xn = np.arange(N)*2*np.pi/N; x = jnp.array(xn); pref = 2 + 2*jnp.cos(x)
j = np.arange(1, n+1); Bm = jnp.array(np.hstack([np.cos(np.outer(xn, j)), np.sin(np.outer(xn, j))]))
def corr(a, b): return jnp.real(jnp.fft.ifft(jnp.fft.fft(a)*jnp.conj(jnp.fft.fft(b))))/a.shape[0]
def uv(rc, sc, kap):
    r, s = Bm @ rc, Bm @ sc; F, G = 2.0**r, 2.0**s; Zf, Zg = jnp.mean(F), jnp.mean(G); f, g = F/Zf, G/Zg
    Q = corr(f, g); Bb = (corr(f*r, g) + corr(f, g*s))/Q - jnp.log2(Zf*Zg); L = jnp.log2(Q)
    H = jnp.log2(jnp.mean(f**kap)*jnp.mean(g**kap)); return L + (kap-1)*Bb - H, (2-kap)*Bb - 2*L + H
def h(x_): return -(x_*jnp.log2(x_) + (1-x_)*jnp.log2(1-x_))
SL = 1e-6
# z = [t, eta, mu, a, gam, l, kap, p, q, rc(32), sc(32)]
def cons(z):
    t, eta, mu, a, g, l, kap, p, q = [z[i] for i in range(9)]
    rc, sc = z[9:9+nt], z[9+nt:9+2*nt]; r_ = 1 - mu - l
    D = eta - t; G = 2*t - eta; aG = D/G
    u, v = uv(rc, sc, kap)
    m1 = jnp.log2(jnp.mean(pref*2.0**(p*(D - u)))); m2 = jnp.log2(jnp.mean(pref*2.0**(q*(aG*v - u))))
    return jnp.array([h(2*a)/2 - g - SL, t - (l + (h(a) - g)*mu) - SL, t - (r_ + (1 - g)*mu) - SL,
        t - (1 - mu + (h(a) + h(.5 - a) - g)*mu - eta) - SL, t - (h(.5 - a)*mu + .5 - t) - SL,
        r_ - SL, t - r_ - SL, t - l - SL, l - mu*(1 - 2*a) - SL, eta - mu/2*jnp.log2(3.) - SL,
        eta - 3e-6 - m1, eta - 3e-6 - m2, 30 - 3*p, 30 - q*(4*aG + 3), D - 1e-4, G - 1e-3])
NAMES = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6r>0', 'C6r<t', 'C6l<t', 'C7', 'C8', 'M1', 'M2', '3p', 'qcap', 'D>0', 'G>0']
cJ = jax.jit(cons); jJ = jax.jit(jax.jacfwd(cons))
cand = json.load(open('candidate_K16.json'))
z0 = np.r_[.48769, .51613, .473, .0082, .06035, .48377, float(cand['kappa']), float(cand['p']), float(cand['q_m']),
           np.array(cand['rc'], float), np.array(cand['sc'], float)]
bnd = [(.48, .495), (.50, .54), (.3, .6), (.001, .05), (.01, .2), (.3, .6), (.5, 2), (1, 10), (1, 9.99)] + [(-4, 4)]*(2*nt)
runs = []; t0 = time.time()
for s_ in range(4):
    zz = z0.copy()
    if s_: zz[9:] += np.random.default_rng(3000 + s_).normal(0, .06, 2*nt)
    r = minimize(lambda z: z[0], zz, jac=lambda z: np.eye(len(z))[0], method='SLSQP', bounds=bnd,
                 constraints=[dict(type='ineq', fun=lambda z: np.asarray(cJ(jnp.array(z))), jac=lambda z: np.asarray(jJ(jnp.array(z))))],
                 options=dict(maxiter=3000, ftol=1e-15))
    c = np.asarray(cJ(jnp.array(r.x))); ok = bool(c.min() > -1e-10)
    rec = dict(start=s_, tau0=float(r.x[0]), T=float(r.x[0] + 2e-7), feasible=ok, minc=float(c.min()), eta=float(r.x[1]), mu=float(r.x[2]), a=float(r.x[3]),
               gamma=float(r.x[4]), l=float(r.x[5]), kappa=float(r.x[6]), p=float(r.x[7]), q=float(r.x[8]), Delta=float(r.x[1] - r.x[0]),
               active=[NAMES[i] for i in range(len(c)) if c[i] < 1e-7], z=r.x.tolist(), msg=str(r.message))
    runs.append(rec)
    print(f'start {s_}: tau0 {rec["tau0"]:.7f} feasible={ok} Delta={rec["Delta"]:.5f} eta={rec["eta"]:.5f} mu={rec["mu"]:.4f} kappa={rec["kappa"]:.3f} active={rec["active"]} [{time.time()-t0:.0f}s]', flush=True)
good = [r_ for r_ in runs if r_['feasible']]; best = min(good, key=lambda r_: r_['tau0']) if good else None
json.dump(dict(N=N, runs=runs, best=best), open(f's12_N{N}.json', 'w'), indent=1)
if best: print(f'BEST tau0 {best["tau0"]:.7f}  T {best["T"]:.7f}  vs JoshuaQFEX .48767595 -> {best["tau0"] - .48767595:+.2e}')
