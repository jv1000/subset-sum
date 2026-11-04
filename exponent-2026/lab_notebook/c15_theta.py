"""C15 sensitivity: if the Corollary-D analogue only delivers a fraction (1-theta) of the outside-S representations,
the trial count grows by 2^{theta*h(2c)/2*m}; trials enter C2, C3, C4, C5 (Base Lemma A7 items 2,5,6,7)."""
import json, numpy as np, jax, jax.numpy as jnp
exec(open('c15.py').read().split("import sys\nres = {}")[0])
def cons_th(zf, th):
    base = cons15(zf); mu, c = zf[2], zf[-1]; pen = th*hs(2*c)/2*mu
    return base.at[1].add(-pen).at[2].add(-pen).at[3].add(-pen).at[4].add(-pen).at[5].add(-pen)
cT = jax.jit(cons_th); jT = jax.jit(jax.jacfwd(cons_th))
ctl = json.load(open('c15.json'))['control']['tau0']; out = {}
for th in (0., .1, .25, .5, .75, 1.):
    best = None
    for c0 in (.0035, .001, .0002):
        zz = np.r_[z0, 0., c0]; bnd = bnd0 + [(0., 0.), (1e-7, .05)]
        r = minimize(lambda z: z[0], zz, jac=lambda z: np.eye(len(z))[0], method='SLSQP', bounds=bnd,
                     constraints=[dict(type='ineq', fun=lambda z: np.asarray(cT(jnp.array(z), th)), jac=lambda z: np.asarray(jT(jnp.array(z), th)))],
                     options=dict(maxiter=3000, ftol=1e-15))
        ok = float(np.asarray(cT(jnp.array(r.x), th)).min()) > -1e-10
        if ok and (best is None or r.x[0] < best[0]): best = (float(r.x[0]), float(r.x[-1]), float(r.x[3]))
    out[th] = best
    print(f'theta {th:.2f}: tau0 {best[0]:.7f}  c {best[1]:.5f}  a {best[2]:.5f}  gain vs C12 {ctl - best[0]:+.2e}', flush=True)
json.dump(out, open('c15_theta.json', 'w'), indent=1)
