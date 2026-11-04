import json, numpy as np, jax, jax.numpy as jnp
exec(open('c14.py').read().split("cJ = jax.jit(cons)")[0])
def cons17(z, rho):
    c = cons(z, jnp.zeros(6)); t, eta, mu, a, g = z[0], z[1], z[2], z[3], z[4]
    hl = rho*h(a/rho); rep = rho/2*h(2*a/rho)
    c = c.at[0].set(rep - g - SL)                       # C1
    c = c.at[1].add(-(hl - h(a))*mu)                     # C2: left-mask entropy rho h(a/rho)
    c = c.at[3].add(-(hl - h(a))*mu)                     # C4
    return c
cJ = jax.jit(cons17); jJ = jax.jit(jax.jacfwd(cons17))
z0 = np.array(json.load(open('s12_N512.json'))['best']['z'])
bnd = [(.48, .495), (.50, .54), (.3, .6), (.0005, .05), (.005, .2), (.3, .6), (.5, 2), (1, 10), (1, 9.99)] + [(-4, 4)]*(2*nt)
out = {}
for rho in (1., .75, .5, .25, .1):
    b = list(bnd); b[3] = (.0005, rho/2 - .001)
    r = minimize(lambda z: z[0], z0, jac=lambda z: np.eye(len(z))[0], method='SLSQP', bounds=b,
                 constraints=[dict(type='ineq', fun=lambda z: np.asarray(cJ(jnp.array(z), rho)), jac=lambda z: np.asarray(jJ(jnp.array(z), rho)))],
                 options=dict(maxiter=3000, ftol=1e-15))
    ok = float(np.asarray(cJ(jnp.array(r.x), rho)).min()) > -1e-10
    out[rho] = dict(tau0=float(r.x[0]), feasible=ok, a=float(r.x[3]), gamma=float(r.x[4]), mu=float(r.x[2]))
    print(f'rho {rho:.2f}: tau0 {r.x[0]:.7f} feasible={ok} a {r.x[3]:.5f} gamma {r.x[4]:.5f} change vs C12 {r.x[0] - .4875749:+.2e}', flush=True)
json.dump(out, open('c17.json', 'w'), indent=1)
