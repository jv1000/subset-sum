"""C16: value of an ideal extra filtering level on C4's overhead; closed-form floors (floating)."""
import json, numpy as np, jax, jax.numpy as jnp
exec(open('c14.py').read().split("cJ = jax.jit(cons)")[0])
from math import log2
def H(x): return -(x*log2(x) + (1-x)*log2(1-x))
def cons16(z, rho):
    c = cons(z, jnp.zeros(6)); t, eta, mu, a, g = z[0], z[1], z[2], z[3], z[4]
    ov = mu*((h(a) - g) + (h(.5 - a) - 1))
    return c.at[3].add((1 - rho)*ov)      # C4 slack: t - (1 - eta + ov) ... ; removing (1-rho) of the overhead
cJ = jax.jit(cons16); jJ = jax.jit(jax.jacfwd(cons16))
z0 = np.array(json.load(open('s12_N512.json'))['best']['z'])
bnd = [(.48, .495), (.50, .54), (.3, .6), (.0005, .05), (.005, .2), (.3, .6), (.5, 2), (1, 10), (1, 9.99)] + [(-4, 4)]*(2*nt)
NM = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6r>0', 'C6r<t', 'C6l<t', 'C7', 'C8', 'M1', 'M2', '3p', 'qcap', 'D', 'G']
# 1. closed-form check at the C12 point
t, eta, mu, a, g, l = [float(v) for v in z0[:6]]; D = eta - t
b23 = .5 - mu*(g - H(a)/2); b4 = (1 - D + mu*((H(a) - g) + (H(.5 - a) - 1)))/2; b5 = (.5 + mu*H(.5 - a))/2
print(f'closed form at C12 point: C2+C3 -> {b23:.7f}, C4 -> {b4:.7f}, C5 -> {b5:.7f}; optimizer tau0 {t:.7f}; overhead mu*a = {mu*a:.5f}')
out = dict(closed=dict(C23=b23, C4=b4, C5=b5, tau0=t), rho={})
for rho in (1., .75, .5, .25, 0.):
    r = minimize(lambda z: z[0], z0, jac=lambda z: np.eye(len(z))[0], method='SLSQP', bounds=bnd,
                 constraints=[dict(type='ineq', fun=lambda z: np.asarray(cJ(jnp.array(z), rho)), jac=lambda z: np.asarray(jJ(jnp.array(z), rho)))],
                 options=dict(maxiter=3000, ftol=1e-15))
    cc = np.asarray(cJ(jnp.array(r.x), rho)); x = r.x
    rec = dict(tau0=float(x[0]), feasible=bool(cc.min() > -1e-10), eta=float(x[1]), Delta=float(x[1]-x[0]), mu=float(x[2]), a=float(x[3]), gamma=float(x[4]), l=float(x[5]),
               active=[NM[i] for i in range(len(cc)) if cc[i] < 1e-7])
    out['rho'][rho] = rec
    print(f"rho {rho:.2f}: tau0 {rec['tau0']:.7f} feasible={rec['feasible']} Delta {rec['Delta']:.5f} mu {rec['mu']:.4f} a {rec['a']:.5f} gain {t - rec['tau0']:+.2e} active={rec['active']}", flush=True)
cap = out['rho'][0.]['Delta']
print(f'architecture floor (1 - Delta_cap)/2 with Delta_cap {cap:.5f}: {(1 - cap)/2:.6f};  for 0.48 one needs Delta_cap >= {1 - 2*.48:.3f}')
json.dump(out, open('c16.json', 'w'), indent=1)
