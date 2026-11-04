"""C13 (floating): Base alias budget + a FAMILY of J asymmetric filters with Base's comparison rows. Minimize tau0.
Usage: python3 s13.py J [N] [nstarts]"""
import json, sys, time
import numpy as np, jax, jax.numpy as jnp
from scipy.optimize import minimize
jax.config.update('jax_enable_x64', True)
J = int(sys.argv[1]); N = int(sys.argv[2]) if len(sys.argv) > 2 else 512; NS = int(sys.argv[3]) if len(sys.argv) > 3 else 4
n = 16; nt = 2*n; SL = 1e-6; ZCAP = 20.0
xn = np.arange(N)*2*np.pi/N; x = jnp.array(xn); pref = 2 + 2*jnp.cos(x)
jj = np.arange(1, n+1); Bm = jnp.array(np.hstack([np.cos(np.outer(xn, jj)), np.sin(np.outer(xn, jj))]))
def corr(a, b): return jnp.real(jnp.fft.ifft(jnp.fft.fft(a)*jnp.conj(jnp.fft.fft(b))))/a.shape[0]
def uv(rc, sc, kap):
    r, s = Bm @ rc, Bm @ sc; F, G = 2.0**r, 2.0**s; Zf, Zg = jnp.mean(F), jnp.mean(G); f, g = F/Zf, G/Zg
    Q = corr(f, g); Bb = (corr(f*r, g) + corr(f, g*s))/Q - jnp.log2(Zf*Zg); L = jnp.log2(Q)
    H = jnp.log2(jnp.mean(f**kap)*jnp.mean(g**kap)); return L + (kap-1)*Bb - H, (2-kap)*Bb - 2*L + H
def h(x_): return -(x_*jnp.log2(x_) + (1-x_)*jnp.log2(1-x_))
def lme(e): m = jnp.max(e); return (m + jnp.log2(jnp.mean(pref*2.0**(e - m))))
NF = 1 + 2*nt; NC = 2*(2 + (J-1))  # per filter: kap, rc, sc ; per filter certs: p,z1,y.. q,z1h,yh..
OFF_F = 6; OFF_C = 6 + J*NF; NV = OFF_C + J*NC
def unpack(z):
    t, eta, mu, a, g, l = [z[i] for i in range(6)]
    F = [(z[OFF_F+v*NF], z[OFF_F+v*NF+1:OFF_F+v*NF+1+nt], z[OFF_F+v*NF+1+nt:OFF_F+(v+1)*NF]) for v in range(J)]
    Cs = [z[OFF_C+v*NC:OFF_C+(v+1)*NC] for v in range(J)]
    return t, eta, mu, a, g, l, F, Cs
def moments(z):
    t, eta, mu, a, g, l, F, Cs = unpack(z); D = eta - t; G = 2*t - eta; aG = D/G
    UV = [uv(rc, sc, k) for (k, rc, sc) in F]; out = []; sums = []
    for v in range(J):
        u, w = UV[v]; c = Cs[v]; k1 = 2 + (J-1)
        others = [UV[l_][0] for l_ in range(J) if l_ != v]
        p, z1, y = c[0], c[1], c[2:k1]; q, z1h, yh = c[k1], c[k1+1], c[k1+2:]
        e_lo = p*(D - u) + z1*(G - w) + sum(y[i]*(u - others[i]) for i in range(J-1))
        e_hi = q*(aG*w - u) + z1h*(w - G) + sum(yh[i]*(u - others[i]) for i in range(J-1))
        out += [lme(e_lo), lme(e_hi)]; sums += [jnp.sum(c[:k1]), jnp.sum(c[k1:])]
    return jnp.array(out), jnp.array(sums), D, G
def cons(z):
    t, eta, mu, a, g, l, F, Cs = unpack(z); r_ = 1 - mu - l
    m, s, D, G = moments(z)
    base = jnp.array([h(2*a)/2 - g - SL, t - (l + (h(a) - g)*mu) - SL, t - (r_ + (1 - g)*mu) - SL,
        t - (1 - mu + (h(a) + h(.5 - a) - g)*mu - eta) - SL, t - (h(.5 - a)*mu + .5 - t) - SL,
        r_ - SL, t - r_ - SL, t - l - SL, l - mu*(1 - 2*a) - SL, eta - mu/2*jnp.log2(3.) - SL, D - 1e-4, G - 1e-3])
    return jnp.concatenate([base, eta - 3e-6 - m, ZCAP - s])
cJ = jax.jit(cons); jJ = jax.jit(jax.jacfwd(cons)); mJ = jax.jit(moments)
def shift(rc, c):
    a, b = rc[:n], rc[n:]; cj, sj = np.cos(jj*c), np.sin(jj*c); return np.r_[a*cj + b*sj, b*cj - a*sj]
def refl(rc): return np.r_[rc[:n], -rc[n:]]
b12 = json.load(open('s12_N512.json'))['best']['z']
alias0 = np.array(b12[:6]); kap0, p0, q0 = b12[6], b12[7], b12[8]; rc0 = np.array(b12[9:9+nt]); sc0 = np.array(b12[9+nt:9+2*nt])
VARIANTS = [lambda r: shift(r, .3), lambda r: shift(r, -.3), lambda r: shift(r, .6), refl, lambda r: shift(r, -.6), lambda r: shift(refl(r), .3)]
def start(si):
    rng = np.random.default_rng(13000 + 100*J + si); z = np.zeros(NV); z[:6] = alias0
    for v in range(J):
        if v == 0: rc, sc = rc0.copy(), sc0.copy()
        else:
            f = VARIANTS[(si + v - 1) % len(VARIANTS)]; rc, sc = f(rc0), f(sc0)
            rc += rng.normal(0, .05, nt); sc += rng.normal(0, .05, nt)
        z[OFF_F+v*NF] = kap0; z[OFF_F+v*NF+1:OFF_F+v*NF+1+nt] = rc; z[OFF_F+v*NF+1+nt:OFF_F+(v+1)*NF] = sc
        k1 = 2 + (J-1); c = np.zeros(NC); c[0] = p0; c[k1] = q0; z[OFF_C+v*NC:OFF_C+(v+1)*NC] = c
    return z
bnd = [(.48, .495), (.50, .54), (.3, .6), (.001, .05), (.01, .2), (.3, .6)]
for v in range(J): bnd += [(.5, 2)] + [(-4, 4)]*(2*nt)
for v in range(J):
    k1 = 2 + (J-1); bnd += [(1, 20), (0, 20)] + [(0, 20)]*(J-1) + [(1, 20), (0, 20)] + [(0, 20)]*(J-1)
runs = []; t0 = time.time()
for si in range(NS):
    zz = start(si)
    r = minimize(lambda z: z[0], zz, jac=lambda z: np.eye(NV)[0], method='SLSQP', bounds=bnd,
                 constraints=[dict(type='ineq', fun=lambda z: np.asarray(cJ(jnp.array(z))), jac=lambda z: np.asarray(jJ(jnp.array(z))))],
                 options=dict(maxiter=4000, ftol=1e-15))
    c = np.asarray(cJ(jnp.array(r.x))); ok = bool(c.min() > -1e-10)
    m, s, D, G = mJ(jnp.array(r.x)); _, _, _, _, _, _, F, Cs = unpack(r.x)
    rec = dict(start=si, tau0=float(r.x[0]), feasible=ok, minc=float(c.min()), eta=float(r.x[1]), Delta=float(D),
               kappas=[float(f[0]) for f in F], certs=[np.asarray(cc).round(4).tolist() for cc in Cs],
               log2M=np.asarray(m).tolist(), zsum=np.asarray(s).tolist(), z=r.x.tolist(), msg=str(r.message))
    runs.append(rec)
    print(f'J={J} start {si}: tau0 {rec["tau0"]:.7f} feasible={ok} Delta={rec["Delta"]:.5f} kappas={np.round(rec["kappas"],3).tolist()} '
          f'certs={rec["certs"]} [{time.time()-t0:.0f}s]', flush=True)
good = [q_ for q_ in runs if q_['feasible']]; best = min(good, key=lambda q_: q_['tau0']) if good else None
json.dump(dict(J=J, N=N, runs=runs, best=best), open(f's13_J{J}_N{N}.json', 'w'), indent=1)
if best: print(f'BEST J={J} tau0 {best["tau0"]:.7f} vs C12 .4875749 -> {best["tau0"] - .4875749:+.2e}; vs JoshuaQFEX {best["tau0"] - .48767595:+.2e}')
