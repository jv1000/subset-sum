"""C15: ternary (BCJ-style) masks in Base budget; based on C14 model. Old doc: of Base's alias constraints C1-C5 and of the moments at the C12 point (floating)."""
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

def H3(p, q): return -(p*jnp.log2(p) + q*jnp.log2(q) + (1-p-q)*jnp.log2(1-p-q))
def xlog(x_): return jnp.where(x_ > 0, x_*jnp.log2(jnp.maximum(x_, 1e-300)), 0.)
def H3s(p, q): return -(xlog(p) + xlog(q) + xlog(1-p-q))
def hs(x_): return H3s(x_, 0.*x_)
def cons15(zf):
    z, b, c = zf[:-2], zf[-2], zf[-1]
    t, eta, mu, a, g, l, kap, p, q = [z[i] for i in range(9)]
    rc, sc = z[9:9+nt], z[9+nt:9+2*nt]; r_ = 1 - mu - l
    D = eta - t; G = 2*t - eta; aG = D/G
    u, v = uv(rc, sc, kap)
    m1 = jnp.log2(jnp.mean(pref*2.0**(p*(D - u)))); m2 = jnp.log2(jnp.mean(pref*2.0**(q*(aG*v - u))))
    HL = H3s(a + b, c); HR = H3s(.5 - a + c, b); s_ = a + b + c
    c8 = mu/2*jnp.log2(3.) + mu*(hs(4*(b + c))/2 + 2*(b + c)*jnp.log2(5.))
    return jnp.array([hs(2*a)/2 + H3s(2*b, 2*c)/2 - g - SL,
        t - (l + (HL - g)*mu) - SL,
        t - (r_ + (1 + hs(b) - g)*mu) - SL,
        t - (1 - mu + (HL + HR - g)*mu - eta) - SL,
        t - (HR*mu + .5 - t) - SL, t - (HL*mu + .5 - t) - SL,
        r_ - SL, t - r_ - SL, t - l - SL, l - mu*(1 - 2*s_) - SL,
        (1 - 2*s_) - (hs(2*a)/2 + H3s(2*b, 2*c)/2 + hs(s_)) - SL,
        eta - c8 - SL, (eta - c8)/2 - (.5 - t + 1e-8) - SL,
        eta - 3e-6 - m1, eta - 3e-6 - m2, 30 - 3*p, 30 - q*(4*aG + 3), D - 1e-4, G - 1e-3])
NM = ['C1', 'C2', 'C3', 'C4', 'C5R', 'C5L', 'C6r>0', 'C6r<t', 'C6l<t', 'C7', 'S3', 'C8', 'A5', 'M1', 'M2', '3p', 'qcap', 'D', 'G']
cJ = jax.jit(cons15); jJ = jax.jit(jax.jacfwd(cons15))
z0 = np.array(json.load(open('s12_N512.json'))['best']['z'])
bnd0 = [(.48, .495), (.50, .54), (.3, .6), (.001, .05), (.01, .2), (.3, .6), (.5, 2), (1, 10), (1, 9.99)] + [(-4, 4)]*(2*nt)
def run(b0, c0, bfree, cfree):
    zz = np.r_[z0, b0, c0]
    bnd = bnd0 + [(1e-7, .05) if bfree else (b0, b0), (1e-7, .05) if cfree else (c0, c0)]
    r = minimize(lambda z: z[0], zz, jac=lambda z: np.eye(len(z))[0], method='SLSQP', bounds=bnd,
                 constraints=[dict(type='ineq', fun=lambda z: np.asarray(cJ(jnp.array(z))), jac=lambda z: np.asarray(jJ(jnp.array(z))))],
                 options=dict(maxiter=3000, ftol=1e-15))
    cc = np.asarray(cJ(jnp.array(r.x)))
    return dict(tau0=float(r.x[0]), feasible=bool(cc.min() > -1e-10), b=float(r.x[-2]), c=float(r.x[-1]), mu=float(r.x[2]), a=float(r.x[3]),
                gamma=float(r.x[4]), l=float(r.x[5]), eta=float(r.x[1]), active=[NM[i] for i in range(len(cc)) if cc[i] < 1e-7], z=r.x.tolist())
import sys
res = {}
ctl = run(0., 0., False, False); res['control'] = ctl
print(f"control b=c=0: tau0 {ctl['tau0']:.8f} feasible={ctl['feasible']} active={ctl['active']}", flush=True)
for nm, bf, cf in (('T1', True, False), ('T2', True, True)):
    res[nm] = []
    for b0 in (.0005, .002, .005, .0001):
        o = run(b0, b0 if cf else 0., bf, cf); res[nm].append(o)
        print(f"{nm} start b0={b0}: tau0 {o['tau0']:.8f} feasible={o['feasible']} b={o['b']:.6f} c={o['c']:.6f} gain {ctl['tau0'] - o['tau0']:+.2e} active={o['active']}", flush=True)
json.dump(res, open('c15.json', 'w'), indent=1)
