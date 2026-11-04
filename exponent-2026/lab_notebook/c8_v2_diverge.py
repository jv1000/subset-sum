"""C8 (floating): kappa = 1 problem — capacity (A), Euler–Lagrange derivation check (B), EL residual (C), SOR (D)."""
import json, time
import numpy as np
import jax, jax.numpy as jnp
from scipy.optimize import minimize
jax.config.update('jax_enable_x64', True)
TAU = .4898; N = 1024; n = 24; nt = 2*n
x = jnp.arange(N)*2*jnp.pi/N; w = 1 + jnp.cos(x)
xn = np.arange(N)*2*np.pi/N; j = np.arange(1, n+1)
Bm = jnp.array(np.hstack([np.cos(np.outer(xn, j)), np.sin(np.outer(xn, j))]))
def corr(a, b): return jnp.real(jnp.fft.ifft(jnp.fft.fft(a)*jnp.conj(jnp.fft.fft(b))))/a.shape[0]   # mean_w a(x+w) b(w)
def QPhiD(f, g):
    Q = corr(f, g); Phi = corr(f*jnp.log(f), g) + corr(f, g*jnp.log(g)); return Q, Phi, Phi/Q - jnp.log(Q)
def logM(f, g, p, q, Dl):
    a = Dl/(TAU - Dl); c, s = q*a, q*(1 + a)
    Q, Phi, D = QPhiD(f, g)
    m1 = p*Dl + jnp.log2(jnp.mean(2*w*Q**(-p))); m2 = jnp.log2(jnp.mean(2*w*jnp.exp(c*D)*Q**(-s)))
    return jnp.array([m1, m2])
def dens(cf): e = 2.0**(Bm @ cf); return e/jnp.mean(e)
def cons_trig(z):
    f, g = dens(z[:nt]), dens(z[nt:2*nt]); p, q, Dl = z[2*nt:]
    m = logM(f, g, p, q, Dl); aa = Dl/(TAU - Dl)
    return jnp.array([TAU + Dl - m[0], TAU + Dl - m[1], 30 - q*(4*aa + 3), 30 - 3*p])
cj = jax.jit(cons_trig); jj = jax.jit(jax.jacfwd(cons_trig))
out = {}; t0 = time.time()
cand = json.load(open('candidate_K16.json'))
def pad16(c): v = np.zeros(nt); v[:16] = c[:16]; v[n:n+16] = c[16:32]; return v
starts = {'k16': np.r_[pad16(np.array(cand['rc'], float)), pad16(np.array(cand['sc'], float)), 8.39, 8.20, .029]}
for s_ in range(3):
    rg = np.random.default_rng(1200 + s_); starts[f'rand{s_}'] = np.r_[rg.normal(0, .5, 2*nt)/np.sqrt(np.tile(j, 4)), rg.uniform(5, 9), rg.uniform(5, 9), .02]
bnd = [(-6, 6)]*(2*nt) + [(1, 10), (1, 9.99), (0, .2)]
resA = json.load(open('c8_v1_nanbug.json'))['C8A']
for nm, z0 in ([] if resA else starts.items()):
    r = minimize(lambda z: -z[-1], z0, jac=lambda z: np.r_[np.zeros(len(z) - 1), -1.0], method='SLSQP', bounds=bnd,
                 constraints=[dict(type='ineq', fun=lambda z: np.asarray(cj(jnp.array(z))), jac=lambda z: np.asarray(jj(jnp.array(z))))],
                 options=dict(maxiter=2000, ftol=1e-13))
    c = np.asarray(cj(jnp.array(r.x))); resA[nm] = dict(Delta=float(r.x[-1]), feasible=bool(c.min() > -1e-9), p=float(r.x[-3]), q=float(r.x[-2]), z=r.x.tolist())
    print(f'C8-A {nm}: kappa=1 capacity {r.x[-1]:.5f} feasible={c.min() > -1e-9} p={r.x[-3]:.3f} q={r.x[-2]:.3f} [{time.time()-t0:.0f}s]', flush=True)
bestA = max((v for v in resA.values() if v['feasible']), key=lambda v: v['Delta']); out['C8A'] = resA; out['C8A_best'] = bestA['Delta']
zA = jnp.array(bestA['z']); fA, gA = dens(zA[:nt]), dens(zA[nt:2*nt]); pA, qA, DA = [float(t) for t in bestA['z'][-3:]]
# ---------------- C8-B: hand variations vs JAX ----------------
def M_lin(f, g, p, q, Dl):
    a = Dl/(TAU - Dl); c, s = q*a, q*(1 + a); Q, Phi, D = QPhiD(f, g)
    return jnp.array([2**(p*Dl)*jnp.mean(2*w*Q**(-p)), jnp.mean(2*w*jnp.exp(c*D)*Q**(-s))])
def hand_df(f, g, p, q, Dl):
    """first variations of M1, M2 w.r.t. the grid value f(y) (per unit grid mass, i.e. derivative times N)."""
    a = Dl/(TAU - Dl); c, s = q*a, q*(1 + a); Q, Phi, D = QPhiD(f, g)
    # integrals over x of h(x) g(y - x) = (h ⋆ g)(y)-type sums: sum_x h(x) g(y-x)/N = conv(h, g)(y)
    conv = lambda h, k: jnp.real(jnp.fft.ifft(jnp.fft.fft(h)*jnp.fft.fft(k)))/N
    h1 = -p*2**(p*Dl)*2*w*Q**(-p-1)
    dM1 = conv(h1, g)
    e = 2*w*jnp.exp(c*D)*Q**(-s-1)
    # dM2/df(y) = sum_x e(x) g(y-x) [c(ln f(y) + ln g(y-x) - Phi/Q) - s] /N
    dM2 = c*jnp.log(f)*conv(e, g) + c*conv(e, g*jnp.log(g)) - c*conv(e*Phi/Q, g) - s*conv(e, g)
    return dM1, dM2
gradM = jax.jacrev(lambda f: M_lin(f, gA, pA, qA, DA))(fA)          # shape (2, N): dM_i/df(y) (raw derivative)
h1, h2 = hand_df(fA, gA, pA, qA, DA)
relB = float(max(jnp.max(jnp.abs(gradM[0]*N - h1))/jnp.max(jnp.abs(h1)), jnp.max(jnp.abs(gradM[1]*N - h2))/jnp.max(jnp.abs(h2))))
out['C8B_max_rel_diff'] = relB; print(f'C8-B hand EL vs JAX: max rel diff {relB:.2e}  ({"PASS" if relB < 1e-6 else "FAIL"})', flush=True)
# ---------------- C8-C: EL residual at the C8-A optimum ----------------
M = M_lin(fA, gA, pA, qA, DA)
def residual_profile(lam):
    r_ = lam*h1/M[0] + (1 - lam)*h2/M[1]; return r_
# lam from minimax: choose lam minimizing the weighted spread (f-weighted variance of r_)
lams = np.linspace(0, 1, 201)
spreads = [float(jnp.sqrt(jnp.mean(fA*(residual_profile(l) - jnp.mean(fA*residual_profile(l)))**2))/jnp.abs(jnp.mean(fA*residual_profile(l)))) for l in lams]
k = int(np.argmin(spreads)); out['C8C'] = dict(lam=float(lams[k]), rel_spread=spreads[k], M=[float(M[0]), float(M[1])])
print(f'C8-C EL residual at C8-A optimum: best lam {lams[k]:.3f}, f-weighted relative spread {spreads[k]:.3e}', flush=True)
# ---------------- C8-D: SOR on the grid, nonparametric ----------------
def sor_minmax(f, g, p, q, Dl, iters=400, om=.3):
    f = jnp.array(f); g = jnp.array(g)
    for it in range(iters):
        M_ = M_lin(f, g, p, q, Dl); lam = jnp.where(M_[0] > M_[1], .9, .1) if it < 5 else lam
        for side in (0, 1):
            ff, gg = (f, g) if side == 0 else (jnp.roll(g[::-1], 1), jnp.roll(f[::-1], 1))   # g-variation via reflection symmetry
            a = Dl/(TAU - Dl); c, s = q*a, q*(1 + a); Q, Phi, D = QPhiD(ff, gg)
            conv = lambda h, k_: jnp.real(jnp.fft.ifft(jnp.fft.fft(h)*jnp.fft.fft(k_)))/N
            Mx = M_lin(ff, gg, p, q, Dl)
            e = 2*w*jnp.exp(c*D)*Q**(-s-1)
            Bc = (1 - lam)*c*conv(e, gg)/Mx[1]
            Ar = lam*conv(-p*2**(p*Dl)*2*w*Q**(-p-1), gg)/Mx[0] + (1 - lam)*(c*conv(e, gg*jnp.log(gg)) - c*conv(e*Phi/Q, gg) - s*conv(e, gg))/Mx[1]
            # choose mu so that the fixed point has mean 1: ln f = (mu - Ar)/Bc ; solve by bisection on mu
            lo, hi = jnp.min(Ar - 30*Bc), jnp.max(Ar + 30*Bc)   # bracket: all exponents <= -30 / >= +30
            for _ in range(80):
                mu = (lo + hi)/2; ex = jnp.clip((mu - Ar)/Bc, -700, 700)
                lme = jax.scipy.special.logsumexp(ex) - jnp.log(N)       # log mean exp
                lo, hi = (mu, hi) if lme < 0 else (lo, mu)
            ex = jnp.clip((mu - Ar)/Bc, -700, 700); fn = jnp.exp(ex - (jax.scipy.special.logsumexp(ex) - jnp.log(N)))
            ff_new = jnp.exp((1 - om)*jnp.log(ff) + om*jnp.log(fn)); ff_new = ff_new/jnp.mean(ff_new)
            if side == 0: f = ff_new
            else: g = jnp.roll(ff_new[::-1], 1)
        M_ = M_lin(f, g, p, q, Dl); lam = jnp.clip(lam + .05*jnp.sign(jnp.log(M_[0]) - jnp.log(M_[1])), 0.01, .99)
    return f, g, jnp.log2(M_lin(f, g, p, q, Dl))
t1 = time.time()
lo, hi = DA, DA + .004; fbest, gbest = fA, gA; sor_log = []
for _ in range(10):
    if time.time() - t1 > 600: break
    mid = (lo + hi)/2
    f2, g2, lm = sor_minmax(fbest, gbest, pA, qA, mid)
    ok = bool(max(float(lm[0]), float(lm[1])) <= TAU + mid - 3e-6 and jnp.all(jnp.isfinite(lm)))
    sor_log.append(dict(Delta=mid, log2M=[float(lm[0]), float(lm[1])], ok=ok, sec=time.time() - t1))
    print(f'C8-D SOR Delta={mid:.5f}: log2 M = {float(lm[0]):.6f}, {float(lm[1]):.6f} vs eta {TAU+mid:.6f} -> {ok}', flush=True)
    if ok: lo = mid; fbest, gbest = f2, g2
    else: hi = mid
out['C8D'] = dict(log=sor_log, capacity_lower=lo, gain_over_A=lo - DA, fixed_pq=[pA, qA])
print(f'C8-D SOR capacity >= {lo:.5f} (gain {lo - DA:+.5f} over C8-A, at fixed p, q)', flush=True)
json.dump(out, open('c8.json', 'w'), indent=1)
