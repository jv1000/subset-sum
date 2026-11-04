"""C2 Route A: rigorous upper bounds for the 430 continuous moment integrals of Base (a-kapila PROOF_0.4877, Prop. B),
the inherited hypotheses of JoshuaQFEX/subset-sum-bound.  Written by Claude for this check; does NOT run Base's D.2 script.

Engine: python-flint arb (ball arithmetic, outward rounding), 200 bits.

Mathematics (Base §6.1, §8.2; OpenAI paper §3 / App. A identities):
  r(x) = sum_j r_j cos jx,  s likewise;  F = 2^r, G = 2^s;  Zf = mean F, Zg = mean G, Zfk = mean F^k, Zgk = mean G^k.
  P(x) = mean_w F(x+w) G(w),  Y(x) = mean_w F(x+w) G(w) (r(x+w) + s(w)).
  LZ = log2(Zf Zg);  L = log2 P - LZ;  B = Y/P - LZ;  H = log2 Zfk + log2 Zgk - kappa LZ;
  u = L + (kappa-1) B - H;   w = (2-kappa) B - 2L + H.
  Certificate (v, rho): I = mean_x (2+2cos x) 2^{z . G(x)} with rows G as in Base §6.1.

Quadrature lemma (Trefethen-Weideman 2014, Thm 3.2, normalised): if g is 2pi-periodic, analytic in the open strip
|Im z| < a and |g| <= M there, then |mean_N(g) - mean(g)| <= 2M/(e^{aN} - 1).

Grids: outer N_out = c * N_in nodes x_k = 2 pi k / N_out.  Inner trapezoid for P, Y at x_k uses the N_in nodes
y_m = 2 pi c m / N_out, so x_k + y_m = x_{k + c m} stays on the outer grid (no new function evaluations).
  Inner strip sigma: |F(x+w)G(w)| <= 2^{R_sig + S_sig} with R_sig = sum |r_j| cosh(j sig); |r + s| <= R_sig + S_sig.
  Normalisers use the full outer grid (N_out nodes) with the same lemma.

Outer strip |Im z| < h = 2 beta (re-derived here, not copied):
  f = F/Zf, g = G/Zg have mean 1.  Q(z) = P(z)/(Zf Zg) = mean_w f(z+w) g(w).  For z = x + iy, |y| < 2 beta, shift the
  contour w -> w - iy/2: Q(z) = mean_w f(x + iy/2 + w) g(w - iy/2).  Since means are contour-invariant,
  Q - 1 = mean (f(.)-1)(g(.)-1), and by Cauchy-Schwarz |Q - 1| <= sqrt((nf-1)(ng-1)) =: q0, where
  nf >= mean_w |f(w + i t)|^2 for all |t| <= beta.  Parseval: mean|f(w+it)|^2 = sum_k |fhat_k|^2 e^{-2kt} =
  |fhat_0|^2 + sum_{k>0} 2|fhat_k|^2 cosh(2kt) (f real on R), nondecreasing in |t|, so nf = mean_w |f(w+i beta)|^2 =
  mean_w 2^{2 r_beta(w)} / Zf^2 with r_beta = Re r(w + i beta) = sum r_j cosh(j beta) cos(jw) (a real trig polynomial,
  itself trapezoided on strip sig with bound 2^{2 sum |r_j| cosh(j beta) cosh(j sig)}).
  q0 < 1  =>  Q has no zeros, log2 Q analytic (principal branch, real on R), Re L = log2|Q| in [log2(1-q0), log2(1+q0)].
  Q B = Y/(Zf Zg) - Q LZ;  |Y/(Zf Zg)| <= sqrt(nf ng) (R_beta + S_beta)  (|r(.+i t)| <= R_beta for |t| <= beta);
  |Q| <= 1 + q0;  so |B| <= [sqrt(nf ng)(R_beta + S_beta) + (1+q0)|LZ|] / (1 - q0) =: Bmax.
  |Re u| <= lam + |kappa-1| Bmax + |H| =: U*,   |Re w| <= 2 lam + |2-kappa| Bmax + |H| =: W*,
  lam = max(-log2(1-q0), log2(1+q0)) = -log2(1-q0).
  Rows: Re(c0 + c1 u + c2 w) <= c0 + |c1| U* + |c2| W*  (constants exact);  |2+2cos z| <= 2 + 2cosh h.

Usage: python3 -I routeA_flint.py data.json out.json [N_in] [c] [beta]  (env: CERTS=all|tight; K2 perturbations via
       env K2=1).
"""
import json, sys, time
from flint import arb, ctx
ctx.prec = 200

def A(s): return arb(str(s))
LN2 = arb(2).log()
def pow2(t): return (t * LN2).exp()
def log2(t): return t.log() / LN2
def up(x): return arb(x.upper())
def widen(x, e): return x + arb(0, e.upper())   # e >= 0 ball -> radius bound by its upper end

def build(data, N_in, c, beta, sig=A('0.45')):
    N = N_in * c
    pi = arb.pi()
    xs = [2 * pi * k / N for k in range(N)]
    cosj = [[(A(j) * x).cos() for x in xs] for j in range(1, 9)]
    h = 2 * beta
    def trig(coef, k): return sum((coef[j] * cosj[j][k] for j in range(len(coef))), arb(0))
    def S(coef, y): return sum((abs(coef[j]) * (A(j + 1) * y).cosh() for j in range(len(coef))), arb(0))
    def qerr(M, a, n): return 2 * M / ((a * n).exp() - 1)
    FD = []
    for fp in data['filters']:
        r = [A(x) for x in fp['r_coef']]; s = [A(x) for x in fp['s_coef']]; kap = A(fp['kappa'])
        rk = [trig(r, k) for k in range(N)]; sk = [trig(s, k) for k in range(N)]
        F = [pow2(t) for t in rk]; G = [pow2(t) for t in sk]
        Rs, Ss = S(r, sig), S(s, sig)
        Zf = widen(sum(F, arb(0)) / N, qerr(pow2(Rs), sig, N)); Zg = widen(sum(G, arb(0)) / N, qerr(pow2(Ss), sig, N))
        Zfk = widen(sum((pow2(kap * t) for t in rk), arb(0)) / N, qerr(pow2(kap * Rs), sig, N))
        Zgk = widen(sum((pow2(kap * t) for t in sk), arb(0)) / N, qerr(pow2(kap * Ss), sig, N))
        LZ = log2(Zf * Zg); H = log2(Zfk) + log2(Zgk) - kap * LZ
        eP = qerr(pow2(Rs + Ss), sig, N_in); eY = qerr((Rs + Ss) * pow2(Rs + Ss), sig, N_in)
        Gsub = [G[c * m] for m in range(N_in)]; GSsub = [G[c * m] * sk[c * m] for m in range(N_in)]
        FR = [F[k] * rk[k] for k in range(N)]
        u, w = [], []
        for k in range(N):
            Pk = arb(0); Yk = arb(0)
            for m in range(N_in):
                i = (k + c * m) % N
                Pk += F[i] * Gsub[m]; Yk += FR[i] * Gsub[m] + F[i] * GSsub[m]
            Pk = widen(Pk / N_in, eP); Yk = widen(Yk / N_in, eY)
            L = log2(Pk) - LZ; B = Yk / Pk - LZ
            u.append(L + (kap - 1) * B - H); w.append((2 - kap) * B - 2 * L + H)
        # outer strip
        rb = [r[j] * (A(j + 1) * beta).cosh() for j in range(8)]; sb = [s[j] * (A(j + 1) * beta).cosh() for j in range(8)]
        nf = widen(sum((pow2(2 * trig(rb, k)) for k in range(N)), arb(0)) / N, qerr(pow2(2 * S(rb, sig)), sig, N)) / (Zf * Zf)
        ng = widen(sum((pow2(2 * trig(sb, k)) for k in range(N)), arb(0)) / N, qerr(pow2(2 * S(sb, sig)), sig, N)) / (Zg * Zg)
        q0 = up(((nf - 1) * (ng - 1)).sqrt())
        assert q0 < 1, 'q0 >= 1'
        Bmax = up(((nf * ng).sqrt() * (S(r, beta) + S(s, beta)) + (1 + q0) * abs(LZ)) / (1 - q0))
        lam = up(-log2(1 - q0))
        Ust = up(lam + abs(kap - 1) * Bmax + abs(H)); Wst = up(2 * lam + abs(2 - kap) * Bmax + abs(H))
        FD.append(dict(u=u, w=w, U=Ust, W=Wst, q0=q0, H=H, eP=eP, eY=eY))
    return FD, xs, N, h

def certify(data, FD, xs, N, h, cert, Dshift=arb(0)):
    tau, eta = A(data['tau0']), A(data['eta'])
    Dl, Gm = eta - tau + Dshift, 2 * tau - eta; aG = Dl / Gm
    v, z, cons = cert['v'], [A(t) for t in cert['z']], cert['cons']; d = FD[v]
    assert all(t >= 0 for t in z)
    # each row = (const, coef_u_v, coef_w_v); comparisons handled separately
    if cert['case'] == 'case1':
        assert z[0] >= 1
        rows = [(Dl, -1, 0), (Gm, 0, -1)]
    else:
        lo = A(cert['lo']); assert z[0] * lo >= 1
        rows = [(arb(0), -1, aG), (-Gm * lo, 0, 1)] + ([(Gm * A(cert['hi']), 0, -1)] if cert['hi'] is not None else [])
    assert len(z) == len(rows) + len(cons)
    # combined linear form: z.G = C0 + Cu u_v + Cw w_v + sum_l z_l (u_v - u_l)
    C0 = sum((z[i] * rows[i][0] for i in range(len(rows))), arb(0))
    Cu = sum((z[i] * rows[i][1] for i in range(len(rows))), arb(0)) + sum((z[len(rows) + j] for j in range(len(cons))), arb(0))
    Cw = sum((z[i] * rows[i][2] for i in range(len(rows))), arb(0))
    zl = [(z[len(rows) + j], cons[j]) for j in range(len(cons))]
    # strip sup: sum_i z_i sup Re(row_i) (row-wise, as each row is bounded separately -> valid upper bound)
    sup = arb(0)
    for i, (c0, cu, cw) in enumerate(rows):
        sup += z[i] * (c0 + abs(A(cu)) * d['U'] + abs(cw) * d['W'])
    for zz, l in zl:
        sup += zz * (d['U'] + FD[l]['U'])
    tot = arb(0)
    for k in range(N):
        e = C0 + Cu * d['u'][k] + Cw * d['w'][k]
        for zz, l in zl: e -= zz * FD[l]['u'][k]
        tot += (2 + 2 * xs[k].cos()) * pow2(e)
    T = tot / N
    err = 2 * (2 + 2 * h.cosh()) * pow2(sup) / ((h * N).exp() - 1)
    I = T + arb(0, err.upper())
    return I, err, sup

def main():
    data = json.load(open(sys.argv[1])); out = sys.argv[2]
    N_in = int(sys.argv[3]) if len(sys.argv) > 3 else 256; c = int(sys.argv[4]) if len(sys.argv) > 4 else 32
    beta = A(sys.argv[5] if len(sys.argv) > 5 else '0.1')
    import os
    which = os.environ.get('CERTS', 'all')
    t0 = time.time()
    FD, xs, N, h = build(data, N_in, c, beta)
    print(f'built {len(FD)} filters N_in={N_in} N_out={N} beta={beta.mid().str(5)} in {time.time()-t0:.0f}s; '
          f'max q0 {max(float(d["q0"]) for d in FD):.4f} max U* {max(float(d["U"]) for d in FD):.3f} max W* {max(float(d["W"]) for d in FD):.3f}', flush=True)
    eta = A(data['eta'])
    marg_req = {0: A('0.00025'), 1: A('0.00025')}; marg_req.update({i: A('4') for i in range(2, 9)}); marg_req[9] = A('17')
    certs = data['certs'] if which == 'all' else [c_ for c_ in data['certs'] if c_['region'] in (0, 1)]
    res = []; allok = True
    for cert in certs:
        I, err, sup = certify(data, FD, xs, N, h, cert)
        marg = eta - log2(I)
        ok = bool(marg > marg_req[cert['region']]); allok &= ok
        res.append(dict(v=cert['v'], region=cert['region'], I_upper=I.upper().str(25, radius=False), log2_margin_lower=marg.lower().str(15, radius=False),
                        log2_margin_upper=marg.upper().str(15, radius=False), required=str(marg_req[cert['region']].mid().str(6, radius=False)),
                        outer_err=err.upper().str(4, radius=False), strip_exponent_bits=sup.upper().str(8, radius=False), certified=ok))
    worst = {}
    for r_ in res:
        g = r_['region']
        if g not in worst or float(r_['log2_margin_lower']) < float(worst[g]['log2_margin_lower']): worst[g] = r_
    for g in sorted(worst): print(f'rho{g}: least log2 margin >= {worst[g]["log2_margin_lower"]} (filter {worst[g]["v"]}), required {worst[g]["required"]}')
    print(f'max outer err {max(float(r_["outer_err"]) for r_ in res):.3e}; max inner eP {max(float(d["eP"].upper()) for d in FD):.3e} eY {max(float(d["eY"].upper()) for d in FD):.3e}')
    k2 = {}
    if os.environ.get('K2'):
        c28 = next(c_ for c_ in data['certs'] if c_['v'] == 28 and c_['region'] == 0)
        I, _, _ = certify(data, FD, xs, N, h, c28)
        k2['a_H28rho0_vs_false_0.0003'] = dict(margin_upper=(eta - log2(I)).upper().str(10, radius=False), rejected=bool((eta - log2(I)) < A('0.0003')))
        I2, _, _ = certify(data, FD, xs, N, h, c28, Dshift=A('0.001'))
        k2['b_H28rho0_DeltaPlus0.001_vs_0.00025'] = dict(margin_upper=(eta - log2(I2)).upper().str(10, radius=False), rejected=bool((eta - log2(I2)) < A('0.00025')))
        print('K2', k2)
    json.dump(dict(route='A (python-flint arb 200 bits)', N_in=N_in, N_out=N, beta=str(beta.mid().str(6, radius=False)), sigma='0.45',
                   all_certified=allok, n_certs=len(res), worst_by_region={f'rho{g}': worst[g] for g in sorted(worst)},
                   strip=[dict(v=i, q0=d['q0'].str(8, radius=False), Ustar=d['U'].str(8, radius=False), Wstar=d['W'].str(8, radius=False)) for i, d in enumerate(FD)],
                   K2=k2, certs=res, seconds=round(time.time() - t0)), open(out, 'w'), indent=1)
    print('ALL CERTIFIED' if allok else 'NOT ALL CERTIFIED', f'({len(res)} certs, {time.time()-t0:.0f}s)')

if __name__ == '__main__':
    main()
