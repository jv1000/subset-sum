import json, numpy as np, jax.numpy as jnp, time
from scipy.optimize import linprog
src = open('c10.py').read().split("out = dict(N=N)")[0]; exec(src)
u0, v0 = [np.asarray(t) for t in uv(jnp.array(base[:nt]), jnp.array(base[nt:2*nt]), base[IDX['kap']])]
lm = np.asarray(lam); D = .0285; G = TAU - D; a = D/G
def lp(A, b):
    r = linprog(-lm, A_ub=A, b_ub=b, A_eq=np.ones((1, N)), b_eq=[1], bounds=(0, None), method='highs')
    return -r.fun, -r.ineqlin.marginals, -r.eqlin.marginals[0]     # max Lambda, y >= 0, z
L1, y1, z1 = lp(np.vstack([u0, v0]), [D, G]); L2, y2, z2 = lp(np.vstack([u0 - a*v0, -v0]), [0, -G])
print('LP hull max Lambda:', L1, L2, 'duals', y1, z1, y2, z2)
out = dict(N=N, LP=dict(L1=L1, L2=L2)); runs = []; t0 = time.time()
for c3 in (.9, .7, .5, .3):
    z0 = base.copy(); z0[IDX['D']] = D
    z0[IDX['Lc1']], z0[IDX['Lc2']] = L1 + 1e-3, L2 + 1e-3
    z0[IDX['y11']], z0[IDX['y12']], z0[IDX['z1']] = y1[0], y1[1], z1 + 1e-3
    z0[IDX['y21']], z0[IDX['y22']], z0[IDX['z2']] = y2[0], y2[1], z2 + 1e-3
    z0[IDX['c31']] = z0[IDX['c32']] = c3
    zf, ok, mc, msg = run(z0, False)
    rec = {k: float(zf[i]) for k, i in IDX.items()}; rec.update(feasible=ok, minc=mc, msg=msg, start_c3=c3); runs.append(rec)
    print(f'tight start c3={c3}: capacity {rec["D"]:.5f} feasible={ok} c3=({rec["c31"]:.3f},{rec["c32"]:.3f}) Lc=({rec["Lc1"]:.3f},{rec["Lc2"]:.3f}) msg={msg[:30]} [{time.time()-t0:.0f}s]', flush=True)
out['runs'] = runs; json.dump(out, open('c10b.json', 'w'), indent=1)
