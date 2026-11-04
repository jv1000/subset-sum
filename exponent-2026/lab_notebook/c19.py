import json, numpy as np, jax, jax.numpy as jnp
exec(open('c15.py').read().split("def cons15")[0])
def cons19(zf):
    z, c = zf[:-1], zf[-1]
    t, eta, mu, a, g, l, kap, p, q = [z[i] for i in range(9)]
    rc, sc = z[9:9+nt], z[9+nt:9+2*nt]; r_ = 1 - mu - l
    D = eta - t; G = 2*t - eta; aG = D/G
    u, v = uv(rc, sc, kap)
    m1 = jnp.log2(jnp.mean(pref*2.0**(p*(D - u)))); m2 = jnp.log2(jnp.mean(pref*2.0**(q*(aG*v - u))))
    HL = H3s(a, c); HR = hs(.5 - a + c); kp = a + c
    a4 = mu*(hs(2*kp) + 2*kp)
    return jnp.array([hs(2*a)/2 + hs(2*c)/2 - g - SL,               # C1R
        t - (l + (HL - g)*mu) - SL,                                  # C2R
        t - (r_ + (1 - g)*mu) - SL,                                  # C3
        t - (1 - mu + (HL + HR - g)*mu - eta) - SL,                  # C4R
        t - (HR*mu + .5 - t) - SL, t - (HL*mu + .5 - t) - SL,        # C5R (both sides)
        r_ - SL, t - r_ - SL, t - l - SL,                            # C6
        l - mu - SL, .5 - mu - SL,                                   # mu < l, mu <= 1/2
        eta - a4 - SL, (eta - a4)/2 - (.5 - t + 1e-8) - SL,          # A4R, A5R
        eta - mu/2*jnp.log2(3.) - SL,                                # C8 (kept)
        eta - 3e-6 - m1, eta - 3e-6 - m2, 30 - 3*p, 30 - q*(4*aG + 3), D - 1e-4, G - 1e-3])
NM = ['C1R', 'C2R', 'C3', 'C4R', 'C5R', 'C5L', 'r>0', 'r<t', 'l<t', 'mu<l', 'mu<=1/2', 'A4R', 'A5R', 'C8', 'M1', 'M2', '3p', 'qcap', 'D', 'G']
cJ = jax.jit(cons19); jJ = jax.jit(jax.jacfwd(cons19))
z0 = np.array(json.load(open('s12_N512.json'))['best']['z'])
bnd0 = [(.48, .495), (.50, .54), (.3, .6), (.0005, .05), (.005, .2), (.3, .6), (.5, 2), (1, 10), (1, 9.99)] + [(-4, 4)]*(2*nt)
def run(c0, cfree):
    zz = np.r_[z0, c0]; bnd = bnd0 + [(1e-7, .05) if cfree else (c0, c0)]
    r = minimize(lambda z: z[0], zz, jac=lambda z: np.eye(len(z))[0], method='SLSQP', bounds=bnd,
                 constraints=[dict(type='ineq', fun=lambda z: np.asarray(cJ(jnp.array(z))), jac=lambda z: np.asarray(jJ(jnp.array(z))))],
                 options=dict(maxiter=3000, ftol=1e-15))
    cc = np.asarray(cJ(jnp.array(r.x)))
    return dict(tau0=float(r.x[0]), feasible=bool(cc.min() > -1e-10), a=float(r.x[3]), c=float(r.x[-1]), gamma=float(r.x[4]), mu=float(r.x[2]), l=float(r.x[5]),
                eta=float(r.x[1]), Delta=float(r.x[1]-r.x[0]), active=[NM[i] for i in range(len(cc)) if cc[i] < 1e-7], z=r.x.tolist())
res = {'control': run(0., False)}
print(f"control c=0: tau0 {res['control']['tau0']:.8f} feasible={res['control']['feasible']} active={res['control']['active']}", flush=True)
res['runs'] = []
for c0 in (.0035, .001, .006, .0002):
    o = run(c0, True); res['runs'].append(o)
    print(f"start c0={c0}: tau0 {o['tau0']:.8f} feasible={o['feasible']} a={o['a']:.5f} c={o['c']:.5f} gamma={o['gamma']:.5f} mu={o['mu']:.4f} l={o['l']:.4f} Delta={o['Delta']:.5f} gain {res['control']['tau0'] - o['tau0']:+.3e} active={o['active']}", flush=True)
best = min((o for o in res['runs'] if o['feasible']), key=lambda o: o['tau0'])
print(f"BEST tau0 {best['tau0']:.8f}  T ~ {best['tau0'] + 2e-7:.8f}  below certified 0.4875754036 by {0.4875754036 - best['tau0'] - 2e-7:.3e}; below JoshuaQFEX by {0.48767595 - best['tau0'] - 2e-7:.3e}")
json.dump(res, open('c19.json', 'w'), indent=1)
