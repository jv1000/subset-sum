"""C3-M: independent direct-sum moment evaluator (handoff definitions) + MC0/MC1/D1/D2/J. Floating, exploratory.
Usage: python3 -I moments_c3.py"""
import importlib.util, json, time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
R = Path(__file__).resolve().parent
ETA, TAU = .67, .4799998
DELTA = ETA - TAU; GAMMA = 2 * TAU - ETA; A_ = DELTA / GAMMA
RHO_C = .669998; QMAX = 30 / (4 * A_ + 3)
def scores(rr, ss, kap, N):
    x = 2 * np.pi * np.arange(N) / N
    C = np.cos(np.outer(x, np.arange(1, 7)))
    r, s = C @ rr, C @ ss
    F, G = 2.0 ** r, 2.0 ** s
    Zf, Zg = F.mean(), G.mean()
    idx = (np.arange(N)[:, None] + np.arange(N)[None, :]) % N      # idx[x, w] = x + w
    Fxw = F[idx]                                                    # F(x+w)
    P = (Fxw * G[None, :]).mean(axis=1)                             # int F(x+w) G(w) dw
    if not np.all(P > 0): raise ValueError('nonpositive P')
    Y = (Fxw * G[None, :] * (r[idx] + s[None, :])).mean(axis=1)
    lz = np.log2(Zf) + np.log2(Zg)
    L = np.log2(P) - lz; B = Y / P - lz
    H = np.log2(np.mean(F ** kap)) + np.log2(np.mean(G ** kap)) - kap * lz
    u = L + (kap - 1) * B - H; v = (2 - kap) * B - 2 * L + H
    return x, u, v
def moments(rr, ss, kap, p, q, Delta, a, N=128):
    x, u, v = scores(rr, ss, kap, N)
    pref = 2 + 2 * np.cos(x)
    m1 = np.log2(np.mean(pref * 2.0 ** (p * (Delta - u))))
    m2 = np.log2(np.mean(pref * 2.0 ** (q * (a * v - u))))
    w = pref / 2
    Eu, Ev = float(np.mean(w * u)), float(np.mean(w * v))
    j1 = 1 + p * (Delta - Eu); j2 = 1 + q * (a * Ev - Eu)
    return float(m1), float(m2), Eu, Ev, float(j1), float(j2)
def unpack(z): return z[:6], z[6:12], z[12], z[13], z[14]
def main():
    out = {}
    d = json.load(open(R / 'astra_in' / 'openai_coverage_candidate.json'))
    r0 = np.array([float(t) for t in d['r']]); s0 = np.array([float(t) for t in d['s']])
    k0, p0, q0 = float(d['kappa']), float(d['p']), float(d['q'])
    e0, t0 = float(d['eta']), float(d['tau']); D0 = e0 - t0; a0 = D0 / (2 * t0 - e0)
    # MC0
    sp = importlib.util.spec_from_file_location('astra', R / 'astra_in' / 'search_openai.py')
    Am = importlib.util.module_from_spec(sp); sp.loader.exec_module(Am)
    zA = np.concatenate([[float(d['mu']), e0, t0, float(d['gamma'])], r0, s0, [k0, p0, q0]])
    astra = Am.evaluate(zA)[0]
    mine = moments(r0, s0, k0, p0, q0, D0, a0)
    out['MC0'] = dict(mine=mine[:2], astra=astra.tolist(), diff=float(np.max(np.abs(np.array(mine[:2]) - astra))),
                      below_rho_c=bool(max(mine[:2]) < .5178685), Ew_u=mine[2], Ew_v=mine[3], jensen=mine[4:])
    out['MC0']['pass'] = out['MC0']['diff'] < 1e-10 and out['MC0']['below_rho_c'] and mine[4] <= mine[0] and mine[5] <= mine[1]
    # D1
    out['D1'] = {N: dict(zip(['log2M1', 'log2M2', 'Ew_u', 'Ew_v', 'jensen1', 'jensen2'],
                             moments(r0, s0, k0, 8.0, 5.0, DELTA, A_, N))) for N in (128, 256)}
    # D2
    def obj_parts(z, N=128):
        rr, ss, k, p, q = unpack(z); m = moments(rr, ss, k, p, q, DELTA, A_, N); return m
    bnd = [(-2.5, 2.5)] * 12 + [(.85, 1.3), (1, 10), (1, QMAX * (1 - 1e-12))]
    runs = []; start = time.time()
    for seed in range(8):
        if time.time() - start > 120: break
        z = np.concatenate([r0, s0, [k0, 8.0, 5.0]])
        if seed:
            rng = np.random.default_rng(20261103 + seed)
            z[:12] += rng.normal(0, .12 if seed <= 3 else .35, 12)
            z[12] = rng.uniform(.95, 1.15); z[13] = rng.uniform(6, 9.5); z[14] = rng.uniform(3, 5.3)
        z = np.clip(z, [b[0] for b in bnd], [b[1] for b in bnd])
        m = obj_parts(z); t = max(m[0], m[1]) - RHO_C
        x0 = np.append(z, t)
        cons = [dict(type='ineq', fun=lambda x: x[-1] - (obj_parts(x[:-1])[0] - RHO_C)),
                dict(type='ineq', fun=lambda x: x[-1] - (obj_parts(x[:-1])[1] - RHO_C))]
        try:
            res = minimize(lambda x: x[-1], x0, method='SLSQP', bounds=bnd + [(-5, 50)], constraints=cons,
                           options=dict(maxiter=400, ftol=1e-10))
            zb = res.x[:-1]; m = obj_parts(zb); msg = str(res.message)
        except ValueError as e:
            zb = z; m = obj_parts(z); msg = 'ERROR ' + str(e)
        exc = max(m[0], m[1]) - RHO_C
        runs.append(dict(seed=seed, max_excess=exc, log2M1=m[0], log2M2=m[1], Ew_u=m[2], Ew_v=m[3], jensen=m[4:],
                         params=zb.tolist(), msg=msg, sec=time.time() - start))
        print(seed, exc, m[:2], m[2:4], round(time.time() - start, 1), flush=True)
    best = min(runs, key=lambda r: r['max_excess'])
    zb = np.array(best['params'])
    best['at256'] = obj_parts(zb, 256)[:2]
    out['D2'] = dict(runs=runs, best=best, total_sec=time.time() - start, starts_done=len(runs))
    out['MC1_jensen_le_moment_all'] = all(r['jensen'][0] <= r['log2M1'] + 1e-12 and r['jensen'][1] <= r['log2M2'] + 1e-12
                                         for r in runs)
    (R / 'moments_c3_results.json').write_text(json.dumps(out, indent=1) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'D2'}, indent=1))
    print('D2 best', {k: v for k, v in best.items() if k != 'params'})
if __name__ == '__main__':
    main()
