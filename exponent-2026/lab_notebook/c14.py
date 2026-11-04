"""C14: shadow prices of Base's alias constraints C1-C5 and of the moments at the C12 point (floating)."""
import json, time, numpy as np, jax, jax.numpy as jnp
from scipy.optimize import minimize
jax.config.update('jax_enable_x64', True)
N = 512; n = 16; nt = 2*n; SL = 1e-6
xn = np.arange(N)*2*np.pi/N; x = jnp.array(xn); pref = 2 + 2*jnp.cos(x)
j = np.arange(1, n+1); Bm = jnp.array(np.hstack([np.cos(np.outer(xn, j)), np.sin(np.outer(xn, j))]))
def corr(a, b): return jnp.real(jnp.fft.ifft(jnp.fft.fft(a)*jnp.conj(jnp.fft.fft(b))))/a.shape[0]
def uv(rc, sc, kap):
    r, s = Bm @ rc, Bm @ sc; F, G = 2.0**r, 2.0**s; Zf, Zg = jnp.mean(F), jnp.mean(G); f, g = F/Zf, G/Zg
    Q = corr(f, g); Bb = (corr(f*r, g) + corr(f, g*s))/Q - jnp.log2(Zf*Zg); L = jnp.log2(Q)
    H = jnp.log2(jnp.mean(f**kap)*jnp.mean(g**kap)); return L + (kap-1)*Bb - H, (2-kap)*Bb - 2*L + H
def h(x_): return -(x_*jnp.log2(x_) + (1-x_)*jnp.log2(1-x_))
# relax vector d: [C1, C2, C3, C4, C5, MOM]
def cons(z, d):
    t, eta, mu, a, g, l, kap, p, q = [z[i] for i in range(9)]
    rc, sc = z[9:9+nt], z[9+nt:9+2*nt]; r_ = 1 - mu - l
    D = eta - t; G = 2*t - eta; aG = D/G
    u, v = uv(rc, sc, kap)
    m1 = jnp.log2(jnp.mean(pref*2.0**(p*(D - u)))); m2 = jnp.log2(jnp.mean(pref*2.0**(q*(aG*v - u))))
    return jnp.array([h(2*a)/2 - g - SL + d[0], t - (l + (h(a) - g)*mu) - SL + d[1], t - (r_ + (1 - g)*mu) - SL + d[2],
        t - (1 - mu + (h(a) + h(.5 - a) - g)*mu - eta) - SL + d[3], t - (h(.5 - a)*mu + .5 - t) - SL + d[4],
        r_ - SL, t - r_ - SL, t - l - SL, l - mu*(1 - 2*a) - SL, eta - mu/2*jnp.log2(3.) - SL,
        eta - 3e-6 - m1 + d[5], eta - 3e-6 - m2 + d[5], 30 - 3*p, 30 - q*(4*aG + 3), D - 1e-4, G - 1e-3])
cJ = jax.jit(cons); jJ = jax.jit(jax.jacfwd(cons))
z0 = np.array(json.load(open('s12_N512.json'))['best']['z'])
bnd = [(.48, .495), (.50, .54), (.3, .6), (.001, .05), (.01, .2), (.3, .6), (.5, 2), (1, 10), (1, 9.99)] + [(-4, 4)]*(2*nt)
def solve(d):
    d = jnp.array(d)
    r = minimize(lambda z: z[0], z0, jac=lambda z: np.eye(len(z))[0], method='SLSQP', bounds=bnd,
                 constraints=[dict(type='ineq', fun=lambda z: np.asarray(cJ(jnp.array(z), d)), jac=lambda z: np.asarray(jJ(jnp.array(z), d)))],
                 options=dict(maxiter=3000, ftol=1e-15))
    c = np.asarray(cJ(jnp.array(r.x), d)); return float(r.x[0]), bool(c.min() > -1e-10), r.x
NAMES = ['C1 P\'<mask variety', 'C2 left records', 'C3 right classes', 'C4 matching visits', 'C5 right masks x trials', 'moments M1,M2']
t0 = time.time(); base, ok, _ = solve([0]*6); print(f'control delta=0: tau0 {base:.8f} feasible={ok}', flush=True)
out = dict(base=base, prices={})
for i, nm in enumerate(NAMES + ['ALL list-side C1-C5']):
    pr = []
    for dl in (2e-4, 5e-4):
        d = [0]*6
        if i < 6: d[i] = dl
        else: d[:5] = [dl]*5
        tau, ok, zz = solve(d); pr.append((base - tau)/dl)
        print(f'{nm:26s} delta {dl:.0e}: tau0 {tau:.8f} feasible={ok} price {(base - tau)/dl:.4f}', flush=True)
    out['prices'][nm] = pr
coef = [0, 1, 1, 1, 2, 1]
kkt = sum(coef[i]*out['prices'][NAMES[i]][0] for i in range(6))
print(f'KKT check sum coef*price (delta 2e-4) = {kkt:.4f} (expect ~1)  [{time.time()-t0:.0f}s]')
out['kkt_sum'] = kkt; json.dump(out, open('c14.json', 'w'), indent=1)
