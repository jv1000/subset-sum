"""C4a mu-continuation (floating). Usage: python3 -I s4c.py K"""
import json, sys, time
import numpy as np
from scipy.optimize import minimize
import importlib.util
from pathlib import Path
R = Path(__file__).resolve().parent
sp = importlib.util.spec_from_file_location('s4', R / 's4.py'); S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
K = int(sys.argv[1]); d = json.load(open(R / f's4_K{K}.json')); z = np.array(d['best']['z'])
rows = []
for mu in np.linspace(z[0], 1 / K - 1e-6, 25):
    b = S.bounds(K); b[0] = (mu, mu); z[0] = mu
    z = np.clip(z, [x[0] for x in b], [x[1] for x in b])
    if S.residual(z, K)[10] < 0: z[1] = S.h2(mu) + mu + S.GUARD + 1e-4   # restore sparse feasibility for the start
    res = minimize(lambda x: x[2], z, method='SLSQP', bounds=b, constraints=[dict(type='ineq', fun=lambda x: S.residual(x, K))],
                   options=dict(maxiter=1500, ftol=1e-13))
    zz = res.x; r = S.residual(zz, K)
    ok = r.min() > -1e-9
    rows.append(dict(mu=float(mu), T=float(zz[2] + 20 * S.EPS), feasible=bool(ok), min_res=float(r.min()), eta=float(zz[1]),
                     Delta=float(zz[1] - zz[2]), active=[S.NAMES[i] for i in range(len(r)) if r[i] < 1e-7], z=zz.tolist(), msg=str(res.message)))
    print(f'K={K} mu={mu:.5f} T={rows[-1]["T"]:.7f} feas={ok} Delta={rows[-1]["Delta"]:.5f} active={rows[-1]["active"]}', file=sys.stderr, flush=True)
    if ok: z = zz
print(json.dumps(dict(K=K, rows=rows), indent=1))
