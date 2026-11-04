"""C7 (floating): mechanism diagnostic + Bhattacharyya relaxation of the joint M1+M2 problem. JAX gradients.
Usage: python3 -I c7.py"""
import json, time
import numpy as np
import jax, jax.numpy as jnp
from scipy.optimize import minimize
jax.config.update('jax_enable_x64', True)
TAU = .4898
def grid(N): x = jnp.arange(N)*2*jnp.pi/N; return x, 1 + jnp.cos(x)
def corr(a, b): return jnp.real(jnp.fft.ifft(jnp.fft.fft(a)*jnp.conj(jnp.fft.fft(b))))/a.shape[0]
def basis(N, n, sines):
    x = np.arange(N)*2*np.pi/N; j = np.arange(1, n+1)
    B = np.cos(np.outer(x, j))
    return jnp.array(np.hstack([B, np.sin(np.outer(x, j))]) if sines else B)
# ---------- true scores (numpy, for A and B0) ----------
def true_uv(rc, sc, ncos, nsin, kap, N=1024):
    x = np.arange(N)*2*np.pi/N; B = np.cos(np.outer(x, np.arange(1, ncos+1)))
    if nsin: B = np.hstack([B, np.sin(np.outer(x, np.arange(1, nsin+1)))])
    r, s = B @ rc, B @ sc; F, G = 2.0**r, 2.0**s; Zf, Zg = F.mean(), G.mean(); f, g = F/Zf, G/Zg
    c = lambda a, b: np.fft.ifft(np.fft.fft(a)*np.conj(np.fft.fft(b))).real/N
    Q = c(f, g); Bb = (c(f*r, g) + c(f, g*s))/Q - np.log2(Zf*Zg); L = np.log2(Q)
    H = np.log2(np.mean(f**kap)*np.mean(g**kap)); u = L + (kap-1)*Bb - H; v = (2-kap)*Bb - 2*L + H
    a = f**kap/np.mean(f**kap); b = g**kap/np.mean(g**kap)
    Qs = c(a, b); BC = c(np.sqrt(a), np.sqrt(b)); D = u + v
    return x, u, v, D, Qs, BC
def true_moments(u, v, x, p, q, Dl):
    a = Dl/(TAU - Dl); pref = 2 + 2*np.cos(x)
    return np.log2(np.mean(pref*2.0**(p*(Dl - u)))), np.log2(np.mean(pref*2.0**(q*(a*v - u))))
def relaxed_moments(Qs, BC, x, p, q, Dl):
    a = Dl/(TAU - Dl); w = 1 + np.cos(x)
    return 1 + p*Dl + np.log2(np.mean(w*Qs**(-p))), 1 + np.log2(np.mean(w*BC**(-2*q*a)*Qs**(-q)))
out = {}
# ---------- C7-A and C7-B0 ----------
cand = json.load(open('candidate_K16.json')); ast = json.load(open('astra_in/openai_coverage_candidate.json'))
m1only = json.load(open('cap_.4898_m1_6_2.5.json'))['best']
sets = {
  'k16_joint': (np.array(cand['rc'], float), np.array(cand['sc'], float), 16, 16, float(cand['kappa']), float(cand['p']), float(cand['q_m']), .02906),
  'astra_joint': (np.array(ast['r'], float), np.array(ast['s'], float), 6, 0, float(ast['kappa']), float(ast['p']), float(ast['q']), .0281),
}
zm = np.array(m1only['z']); sets['m1_only_opt'] = (zm[:6], zm[6:12], 6, 0, zm[12], zm[13], None, zm[15])
for name, (rc, sc, nc, ns, kap, p, q, Dl) in sets.items():
    x, u, v, D, Qs, BC = true_uv(rc, sc, nc, ns, kap)
    a_ = Dl/(TAU - Dl); qcap = 30/(4*a_ + 3)
    if q is None:   # best admissible q for M2 at these densities
        qs = np.linspace(1, qcap, 400); q = float(qs[np.argmin([true_moments(u, v, x, p, qq, Dl)[1] for qq in qs])])
    tm = true_moments(u, v, x, p, q, Dl); rm = relaxed_moments(Qs, BC, x, p, q, Dl); w = (1 + np.cos(x))/np.mean(1 + np.cos(x))
    out[name] = dict(Delta=Dl, eta=TAU + Dl, p=float(p), q=float(q), kappa=float(kap), log2M_true=list(map(float, tm)),
                     log2M_relaxed=list(map(float, rm)), relaxed_le_true=bool(rm[0] <= tm[0] + 1e-12 and rm[1] <= tm[1] + 1e-12),
                     Ew_v=float(np.mean(w*v)), Ew_D=float(np.mean(w*D)), Ew_u=float(np.mean(w*u)), Gamma=TAU - Dl,
                     v_range=[float(v.min()), float(v.max())])
    print(name, json.dumps(out[name]), flush=True)
# ---------- C7-B: relaxed capacity ----------
N, n = 1024, 24
x, w = grid(N); Bm = basis(N, n, True); nt = 2*n
def dens(c):
    t = Bm @ c; e = 2.0**t; return e/jnp.mean(e)
def rel(z):
    a = dens(z[:nt]); b = dens(z[nt:2*nt]); p, q, Dl = z[2*nt], z[2*nt+1], z[2*nt+2]
    Qs = corr(a, b); BC = corr(jnp.sqrt(a), jnp.sqrt(b)); aa = Dl/(TAU - Dl)
    m1 = 1 + p*Dl + jnp.log2(jnp.mean(w*Qs**(-p)))
    m2 = 1 + jnp.log2(jnp.mean(w*BC**(-2*q*aa)*Qs**(-q)))
    return jnp.array([TAU + Dl - m1, TAU + Dl - m2, 30 - q*(4*aa + 3), 30 - 3*p])
relj = jax.jit(rel); jacj = jax.jit(jax.jacfwd(rel))
def pad(c, k):
    v_ = np.zeros(nt); v_[:min(k, n)] = c[:min(k, n)]
    if len(c) > k: v_[n:n+min(k, n)] = c[k:k+min(k, n)]
    return v_
starts = {'k16': np.concatenate([pad(float(cand['kappa'])*np.array(cand['rc'], float), 16), pad(float(cand['kappa'])*np.array(cand['sc'], float), 16), [8.4, 8.2, .029]]),
          'astra': np.concatenate([pad(float(ast['kappa'])*np.array(ast['r'], float), 6), pad(float(ast['kappa'])*np.array(ast['s'], float), 6), [8.4, 8.2, .028]])}
for s in range(4):
    rg = np.random.default_rng(900 + s)
    starts[f'rand{s}'] = np.concatenate([rg.normal(0, .5, 2*nt)/np.sqrt(np.tile(np.arange(1, n+1), 4)), [rg.uniform(4, 9), rg.uniform(4, 9), .02]])
bnd = [(-6, 6)]*(2*nt) + [(1, 10), (1, 9.99), (0, .2)]
res = {}; t0 = time.time()
for nm, z0 in starts.items():
    r = minimize(lambda z: -z[-1], z0, jac=lambda z: np.r_[np.zeros(len(z) - 1), -1.0], method='SLSQP', bounds=bnd,
                 constraints=[dict(type='ineq', fun=lambda z: np.asarray(relj(jnp.array(z))), jac=lambda z: np.asarray(jacj(jnp.array(z))))],
                 options=dict(maxiter=2000, ftol=1e-13))
    c = np.asarray(relj(jnp.array(r.x))); res[nm] = dict(Delta=float(r.x[-1]), feasible=bool(c.min() > -1e-9), p=float(r.x[-3]), q=float(r.x[-2]), msg=str(r.message), z=r.x.tolist())
    print(f'C7-B start {nm}: relaxed capacity {r.x[-1]:.5f} feasible={c.min() > -1e-9} p={r.x[-3]:.3f} q={r.x[-2]:.3f} [{time.time()-t0:.0f}s]', flush=True)
out['C7B'] = res
ok = [v_['Delta'] for v_ in res.values() if v_['feasible']]
out['C7B_best'] = max(ok) if ok else None
json.dump(out, open('c7.json', 'w'), indent=1)
print('C7-B best relaxed capacity:', out['C7B_best'])
