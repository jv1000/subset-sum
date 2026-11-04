"""C10 (floating): joint optimization of densities with amplitude-grouped patterns (LP-dual cutoff certificates)."""
import json, sys, time
import numpy as np
import jax, jax.numpy as jnp
from scipy.optimize import minimize
jax.config.update('jax_enable_x64', True)
TAU = .4898; N = int(sys.argv[1]) if len(sys.argv) > 1 else 512; n = 16; nt = 2*n
xn = np.arange(N)*2*np.pi/N + np.pi/N        # half-step offset: avoids x = pi exactly (lambda = -inf)
x = jnp.array(xn); lam = jnp.log2(2 + 2*jnp.cos(x)); w2 = 2 + 2*jnp.cos(x)
j = np.arange(1, n+1); Bm = jnp.array(np.hstack([np.cos(np.outer(xn, j)), np.sin(np.outer(xn, j))]))
def corr(a, b): return jnp.real(jnp.fft.ifft(jnp.fft.fft(a)*jnp.conj(jnp.fft.fft(b))))/a.shape[0]
def uv(rc, sc, kap):
    r, s = Bm @ rc, Bm @ sc; F, G = 2.0**r, 2.0**s; Zf, Zg = jnp.mean(F), jnp.mean(G); f, g = F/Zf, G/Zg
    Q = corr(f, g); Bb = (corr(f*r, g) + corr(f, g*s))/Q - jnp.log2(Zf*Zg); L = jnp.log2(Q)
    H = jnp.log2(jnp.mean(f**kap)*jnp.mean(g**kap)); return L + (kap-1)*Bb - H, (2-kap)*Bb - 2*L + H
# z layout: rc(32) sc(32) kap p q D c31 c32 Lc1 Lc2 y11 y12 z1 y21 y22 z2
IDX = dict(kap=2*nt, p=2*nt+1, q=2*nt+2, D=2*nt+3, c31=2*nt+4, c32=2*nt+5, Lc1=2*nt+6, Lc2=2*nt+7,
           y11=2*nt+8, y12=2*nt+9, z1=2*nt+10, y21=2*nt+11, y22=2*nt+12, z2=2*nt+13)
def cons(zz, fix_c3=False):
    g_ = lambda k: zz[IDX[k]]
    u, v = uv(zz[:nt], zz[nt:2*nt], g_('kap')); p, q, D = g_('p'), g_('q'), g_('D'); G = TAU - D; a = D/G
    c31 = jnp.where(fix_c3, 1.0, g_('c31')); c32 = jnp.where(fix_c3, 1.0, g_('c32'))
    m1 = (1 - c31)*g_('Lc1') + jnp.log2(jnp.mean(w2**c31 * 2.0**(p*(D - u))))
    m2 = (1 - c32)*g_('Lc2') + jnp.log2(jnp.mean(w2**c32 * 2.0**(q*(a*v - u))))
    d1 = g_('z1') + g_('y11')*u + g_('y12')*v - lam                    # >= 0 for all x
    d2 = g_('z2') + g_('y21')*(u - a*v) - g_('y22')*v - lam
    c1b = g_('Lc1') - (g_('z1') + g_('y11')*D + g_('y12')*G)            # z + y.b <= Lc
    c2b = g_('Lc2') - (g_('z2') + g_('y21')*0 - g_('y22')*G)
    scal = jnp.array([TAU + D - 3e-6 - m1, TAU + D - 3e-6 - m2, c1b, c2b, 29 - 3*p - c31, 29 - q*(4*a + 3) - c32])
    return jnp.concatenate([scal, d1, d2])
cJ = jax.jit(cons, static_argnums=1); jJ = jax.jit(jax.jacfwd(cons), static_argnums=1)
cand = json.load(open('candidate_K16.json'))
base = np.zeros(2*nt + 14); base[:nt] = np.array(cand['rc'], float); base[nt:2*nt] = np.array(cand['sc'], float)
base[IDX['kap']] = float(cand['kappa']); base[IDX['p']] = float(cand['p']); base[IDX['q']] = float(cand['q_m']); base[IDX['D']] = .029
base[[IDX['c31'], IDX['c32']]] = 1.0; base[[IDX['Lc1'], IDX['Lc2']]] = 2.0
base[[IDX['z1'], IDX['z2']]] = 2.0          # lambda <= 2 everywhere: y = 0, z = 2 is a feasible dual
bnd = [(-4, 4)]*(2*nt) + [(.5, 2), (1, 10), (1, 9.99), (0, .2), (0, 1), (0, 1), (-10, 2.5), (-10, 2.5)] + [(0, 200), (0, 200), (-200, 200)]*2
def run(z0, fix_c3):
    r = minimize(lambda z: -z[IDX['D']], z0, jac=lambda z: -np.eye(len(z))[IDX['D']], method='SLSQP', bounds=bnd,
                 constraints=[dict(type='ineq', fun=lambda z: np.asarray(cJ(jnp.array(z), fix_c3)), jac=lambda z: np.asarray(jJ(jnp.array(z), fix_c3)))],
                 options=dict(maxiter=1500, ftol=1e-13))
    c = np.asarray(cJ(jnp.array(r.x), fix_c3)); return r.x, bool(c.min() > -1e-9), float(c.min()), str(r.message)
out = dict(N=N); t0 = time.time()
zc, okc, mc, msg = run(base, True)
out['control_c3eq1'] = dict(Delta=float(zc[IDX['D']]), feasible=okc, minc=mc, msg=msg)
print(f'C10 control (c3 = 1): capacity {zc[IDX["D"]]:.5f} feasible={okc} [{time.time()-t0:.0f}s]', flush=True)
runs = []
for s_ in range(4):
    z0 = zc.copy() if okc else base.copy()
    if s_: rg = np.random.default_rng(2000 + s_); z0[:2*nt] += rg.normal(0, .08, 2*nt); z0[IDX['c31']] = z0[IDX['c32']] = rg.uniform(.6, 1)
    zf, ok, mc, msg = run(z0, False)
    rec = {k: float(zf[i]) for k, i in IDX.items()}; rec.update(feasible=ok, minc=mc, msg=msg, z=zf.tolist())
    runs.append(rec)
    print(f'C10 start {s_}: capacity {rec["D"]:.5f} feasible={ok} c3=({rec["c31"]:.3f},{rec["c32"]:.3f}) Lc=({rec["Lc1"]:.3f},{rec["Lc2"]:.3f}) '
          f'kappa={rec["kap"]:.3f} p={rec["p"]:.2f} q={rec["q"]:.2f} [{time.time()-t0:.0f}s]', flush=True)
out['runs'] = runs
good = [r_ for r_ in runs if r_['feasible']]; out['best'] = max(good, key=lambda r_: r_['D']) if good else None
json.dump(out, open(f'c10_N{N}.json', 'w'), indent=1)
if out['best']: print('C10 best capacity', out['best']['D'], 'gain over control', out['best']['D'] - out['control_c3eq1']['Delta'])
