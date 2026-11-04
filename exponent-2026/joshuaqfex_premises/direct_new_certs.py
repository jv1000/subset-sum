"""C2 extra (Route A engine): DIRECT certification of the repo's *modified* certificates (paper.tex Lemma
"Certificate transfer") at the NEW parameters, instead of inferring them through the transfer identities and the coarse
|w| <= 256 bound.  Target (paper.tex Prop. "Transferred continuous moments"): eta - log2 I' > 1e-6 for all 430.
Modified certificates (old region boundaries Gamma_b * b_i retained):
  rho0:        G' = (Delta/q - u_v, Gamma_b - w_v, (u_v - u_l)_C),                         z unchanged
  rho_i 1..8:  G' = (A w_v - u_v, w_v - Gamma_b L, Gamma_b H - w_v, (u_v - u_l)_C),          z2 -> z2 + z0 (A - A_b)
  rho9:        G' = (A w_v - u_v, w_v - 15 Gamma_b, (u_v - u_l)_C),                          z unchanged
Usage: python3 -I direct_new_certs.py data.json parameters.json out.json
"""
import json, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import routeA_flint as R
from flint import arb
# --- directed decimal export (fix after Astra's round-6 audit): rounded displays are NOT bounds. ---
from decimal import Decimal as _D
def dlow(x, k=15):
    """decimal string s with s <= every point of arb x, verified rigorously in arb (steps down if needed)"""
    d = _D(x.lower().str(k, radius=False)); ulp = _D(1).scaleb(d.adjusted() - k + 1)
    while not (arb(str(d)) <= x.lower()): d -= ulp
    return str(d)
def dup(x, k=15):
    """decimal string s with s >= every point of arb x, verified rigorously in arb (steps up if needed)"""
    d = _D(x.upper().str(k, radius=False)); ulp = _D(1).scaleb(d.adjusted() - k + 1)
    while not (arb(str(d)) >= x.upper()): d += ulp
    return str(d)
def ball(x, k=30): return x.str(k)     # Arb midpoint +/- radius rendering (honest enclosure)
A, pow2, log2 = R.A, R.pow2, R.log2
data = json.load(open(sys.argv[1])); par = json.load(open(sys.argv[2]))
t0 = time.time()
FD, xs, N, h = R.build(data, 256, 32, A('0.1'))
tau, eta = A(par['tau']), A(par['eta']); tb, eb = A(data['tau0']), A(data['eta'])
D, G = eta - tau, 2 * tau - eta; Db, Gb = eb - tb, 2 * tb - eb
q = G / Gb; Anew, Ab = D / G, Db / Gb
res = []; ok_all = True
for c in data['certs']:
    v, z, cons, g = c['v'], [A(t) for t in c['z']], c['cons'], c['region']; d = FD[v]
    if g == 0:
        rows = [(D / q, -1, 0), (Gb, 0, -1)]
    else:
        lo = A(c['lo'])
        rows = [(arb(0), -1, Anew), (-Gb * lo, 0, 1)]
        if c['hi'] is not None:
            rows.append((Gb * A(c['hi']), 0, -1)); z[2] = z[2] + z[0] * (Anew - Ab)
    nr = len(rows); assert len(z) == nr + len(cons)
    C0 = sum((z[i] * rows[i][0] for i in range(nr)), arb(0))
    Cu = sum((z[i] * rows[i][1] for i in range(nr)), arb(0)) + sum(z[nr:], arb(0))
    Cw = sum((z[i] * rows[i][2] for i in range(nr)), arb(0))
    sup = sum((z[i] * (rows[i][0] + abs(A(rows[i][1])) * d['U'] + abs(rows[i][2]) * d['W']) for i in range(nr)), arb(0))
    sup += sum((z[nr + j] * (d['U'] + FD[l]['U']) for j, l in enumerate(cons)), arb(0))
    tot = arb(0)
    for k in range(N):
        e = C0 + Cu * d['u'][k] + Cw * d['w'][k]
        for j, l in enumerate(cons): e -= z[nr + j] * FD[l]['u'][k]
        tot += (2 + 2 * xs[k].cos()) * pow2(e)
    err = 2 * (2 + 2 * h.cosh()) * pow2(sup) / ((h * N).exp() - 1)
    I = tot / N + arb(0, err.upper())
    marg = eta - log2(I); ok = bool(marg > A('0.000001')); ok_all &= ok
    res.append(dict(v=v, region=g, new_log2_margin_lower=dlow(marg, 12), margin_ball=ball(marg), certified=ok,
                    zsum=dup(sum(z, arb(0)), 8)))
worst = {}
for r_ in res:
    if r_['region'] not in worst or float(r_['new_log2_margin_lower']) < float(worst[r_['region']]['new_log2_margin_lower']): worst[r_['region']] = r_
for g in sorted(worst): print(f'rho{g}: least NEW log2 margin >= {worst[g]["new_log2_margin_lower"]} (filter {worst[g]["v"]}); required > 1e-6')
print('max modified multiplier sum', max(float(r_['zsum']) for r_ in res))
print('ALL MODIFIED CERTIFICATES CERTIFIED' if ok_all else 'NOT ALL', f'{time.time()-t0:.0f}s')
json.dump(dict(all_certified=ok_all, worst_by_region={f'rho{g}': worst[g] for g in sorted(worst)}, certs=res,
               max_modified_zsum=max(float(r_['zsum']) for r_ in res)), open(sys.argv[3], 'w'), indent=1)
