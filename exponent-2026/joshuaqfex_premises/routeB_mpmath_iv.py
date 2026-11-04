"""C2 Route B: independent re-implementation with mpmath `iv` (outward-rounded intervals), separately written.
Different engine, grid sizes and outer strip from Route A:
  N_in = 192 inner nodes, outer N_out = 32 * 192 = 6144, inner strip sigma = 0.45, outer strip |Im z| < 2*beta with beta = 0.09.
Same mathematics (Base §6.1/§8.2; quadrature lemma 2M/(e^{aN}-1)); the outer bound for |QB| uses the alternative valid
form sqrt(nf ng) (R_beta + S_beta + |LZ|) (since |Q| <= mean|f||g| <= sqrt(nf ng)), not Route A's (1+q0)|LZ| form.
Certificates are processed region rho0, rho1 first; results are flushed to the output JSON after every certificate.
Usage: python3 -I routeB_mpmath_iv.py data.json out.json
"""
import json, sys, time
from mpmath import iv
# --- directed decimal export (fix after Astra's round-6 audit) ---
from decimal import Decimal as _D
import mpmath as _mp
def dlow(v, k=15):
    a = _mp.mpf(v.a); d = _D(_mp.nstr(a, k)); ulp = _D(1).scaleb(d.adjusted() - k + 1)
    while not (_mp.mpf(iv.mpf(str(d)).b) <= a): d -= ulp
    return str(d)
def dup(v, k=15):
    b = _mp.mpf(v.b); d = _D(_mp.nstr(b, k)); ulp = _D(1).scaleb(d.adjusted() - k + 1)
    while not (_mp.mpf(iv.mpf(str(d)).a) >= b): d += ulp
    return str(d)
iv.prec = 128
NIN, CC = 192, 32
NOUT = NIN * CC
SIG, BETA = iv.mpf('0.45'), iv.mpf('0.09')
HW = 2 * BETA
ZERO = iv.mpf(0)
LN2 = iv.log(iv.mpf(2))
def q(s): return iv.mpf(str(s))
def p2(t): return iv.exp(t * LN2)
def lg2(t): return iv.log(t) / LN2
def ch(t): return (iv.exp(t) + iv.exp(-t)) / 2
def hi(x): return iv.mpf(x.b)
def pm(e): return iv.mpf([-e.b, e.b])
def lemma(M, a, n): return 2 * M / (iv.exp(a * n) - 1)

def prepare(data):
    xs = [2 * iv.pi * k / NOUT for k in range(NOUT)]
    COS = [[iv.cos(j * x) for x in xs] for j in range(1, 9)]
    out = []
    for f in data['filters']:
        r = [q(t) for t in f['r_coef']]; s = [q(t) for t in f['s_coef']]; ka = q(f['kappa'])
        rr = [sum((r[j] * COS[j][k] for j in range(8)), ZERO) for k in range(NOUT)]
        ss = [sum((s[j] * COS[j][k] for j in range(8)), ZERO) for k in range(NOUT)]
        Fv = [p2(t) for t in rr]; Gv = [p2(t) for t in ss]
        Rsig = sum((abs(r[j]) * ch((j + 1) * SIG) for j in range(8)), ZERO)
        Ssig = sum((abs(s[j]) * ch((j + 1) * SIG) for j in range(8)), ZERO)
        mean = lambda vals: sum(vals, ZERO) / NOUT
        Zf = mean(Fv) + pm(lemma(p2(Rsig), SIG, NOUT)); Zg = mean(Gv) + pm(lemma(p2(Ssig), SIG, NOUT))
        Zfk = mean([p2(ka * t) for t in rr]) + pm(lemma(p2(ka * Rsig), SIG, NOUT))
        Zgk = mean([p2(ka * t) for t in ss]) + pm(lemma(p2(ka * Ssig), SIG, NOUT))
        LZ = lg2(Zf) + lg2(Zg)
        H = lg2(Zfk) + lg2(Zgk) - ka * LZ
        EP = lemma(p2(Rsig + Ssig), SIG, NIN); EY = lemma((Rsig + Ssig) * p2(Rsig + Ssig), SIG, NIN)
        Gs = [Gv[CC * m] for m in range(NIN)]; Ss_ = [ss[CC * m] for m in range(NIN)]
        U, W = [], []
        for k in range(NOUT):
            Pk = ZERO; Yk = ZERO
            for m in range(NIN):
                i = (k + CC * m) % NOUT
                t = Fv[i] * Gs[m]
                Pk += t; Yk += t * (rr[i] + Ss_[m])
            Pk = Pk / NIN + pm(EP); Yk = Yk / NIN + pm(EY)
            L = lg2(Pk) - LZ; B = Yk / Pk - LZ
            U.append(L + (ka - 1) * B - H); W.append((2 - ka) * B - 2 * L + H)
        rb = [r[j] * ch((j + 1) * BETA) for j in range(8)]; sb = [s[j] * ch((j + 1) * BETA) for j in range(8)]
        Rb2 = sum((abs(t) * ch((j + 1) * SIG) for j, t in enumerate(rb)), ZERO); Sb2 = sum((abs(t) * ch((j + 1) * SIG) for j, t in enumerate(sb)), ZERO)
        nf = (mean([p2(2 * sum((rb[j] * COS[j][k] for j in range(8)), ZERO)) for k in range(NOUT)]) + pm(lemma(p2(2 * Rb2), SIG, NOUT))) / Zf ** 2
        ng = (mean([p2(2 * sum((sb[j] * COS[j][k] for j in range(8)), ZERO)) for k in range(NOUT)]) + pm(lemma(p2(2 * Sb2), SIG, NOUT))) / Zg ** 2
        q0 = hi(iv.sqrt((nf - 1) * (ng - 1)))
        assert q0.b < 1
        Rbeta = sum((abs(r[j]) * ch((j + 1) * BETA) for j in range(8)), ZERO); Sbeta = sum((abs(s[j]) * ch((j + 1) * BETA) for j in range(8)), ZERO)
        Bmax = hi(iv.sqrt(nf * ng) * (Rbeta + Sbeta + abs(LZ)) / (1 - q0))
        lam = hi(-lg2(1 - q0))
        Ust = hi(lam + abs(ka - 1) * Bmax + abs(H)); Wst = hi(2 * lam + abs(2 - ka) * Bmax + abs(H))
        out.append(dict(u=U, w=W, Us=Ust, Ws=Wst, q0=q0))
        print(f'  filter {len(out)-1}: q0<={float(q0.b):.4f} U*<={float(Ust.b):.3f} W*<={float(Wst.b):.3f}', flush=True)
    M2 = [2 + 2 * COS[0][k] for k in range(NOUT)]
    return out, M2

def main():
    data = json.load(open(sys.argv[1])); outp = sys.argv[2]
    t0 = time.time()
    FD, M2 = prepare(data)
    print(f'prepared in {time.time()-t0:.0f}s', flush=True)
    tau, eta = q(data['tau0']), q(data['eta'])
    Dl, Gm = eta - tau, 2 * tau - eta; aG = Dl / Gm
    need = {0: q('0.00025'), 1: q('0.00025'), 9: q('17')}
    certs = sorted(data['certs'], key=lambda c: (c['region'] > 1, c['v'], c['region']))
    res = []
    M2s = 2 + 2 * ch(HW)
    for c in certs:
        v, z = c['v'], [q(t) for t in c['z']]; d = FD[v]
        assert all(t.a >= 0 for t in z)
        if c['region'] == 0:
            assert z[0].a >= 1
            lin = [(lambda k: Dl - d['u'][k], Dl + d['Us']), (lambda k: Gm - d['w'][k], Gm + d['Ws'])]
        else:
            lo = q(c['lo']); assert (z[0] * lo).a >= 1
            lin = [(lambda k: aG * d['w'][k] - d['u'][k], aG * d['Ws'] + d['Us']), (lambda k: d['w'][k] - Gm * lo, d['Ws'] - Gm * lo)]
            if c['hi'] is not None:
                hh = q(c['hi']); lin.append((lambda k, hh=hh: Gm * hh - d['w'][k], Gm * hh + d['Ws']))
        for l in c['cons']:
            lin.append((lambda k, l=l: d['u'][k] - FD[l]['u'][k], d['Us'] + FD[l]['Us']))
        assert len(lin) == len(z)
        acc = ZERO
        for k in range(NOUT):
            acc += M2[k] * p2(sum((z[i] * lin[i][0](k) for i in range(len(z))), ZERO))
        sup = sum((z[i] * lin[i][1] for i in range(len(z))), ZERO)
        err = lemma(M2s * p2(sup), HW, NOUT)
        Iv = acc / NOUT + pm(err)
        marg = eta - lg2(Iv)
        req = need.get(c['region'], q('4'))
        ok = bool(marg.a > req.b)
        res.append(dict(v=v, region=c['region'], I_upper=dup(Iv, 20), log2_margin_lower=dlow(marg, 15), required=str(req.a),
                        outer_err=dup(err, 4), certified=ok))
        json.dump(dict(route='B (mpmath iv, 128 bits)', N_in=NIN, N_out=NOUT, beta='0.09', sigma='0.45', done=len(res),
                       all_certified_so_far=all(r_['certified'] for r_ in res), certs=res,
                       strip=[dict(v=i, q0=str(f['q0'].b), Ustar=str(f['Us'].b), Wstar=str(f['Ws'].b)) for i, f in enumerate(FD)],
                       seconds=round(time.time() - t0)), open(outp, 'w'), indent=1)
        if len(res) % 10 == 0: print(f'  {len(res)} certs, {time.time()-t0:.0f}s, all ok so far: {all(r_["certified"] for r_ in res)}', flush=True)
    print('ROUTE B', 'ALL CERTIFIED' if all(r_['certified'] for r_ in res) else 'NOT ALL CERTIFIED', len(res), f'{time.time()-t0:.0f}s')

if __name__ == '__main__':
    main()
