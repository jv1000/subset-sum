"""C5-cert step 2: RIGOROUS (ball arithmetic) certificate for a candidate point of the OpenAI-architecture budget with
general real trig-polynomial log-densities (cos and sin terms), adapted by Claude from C2 Route A.

Moments (continuous circle, normalized): M1 = mean (2+2cos x) 2^{p(Delta-u)}, M2 = mean (2+2cos x) 2^{q(a v - u)},
u = L + (kappa-1)B - H, v = (2-kappa)B - 2L + H, with P, Y, L, B, H as in C2 Route A.
Quadrature lemma (Trefethen-Weideman 2014 Thm 3.2): |mean_N g - mean g| <= 2M/(e^{aN}-1) for g analytic, |g| <= M on
|Im z| < a.  Strip bound for a trig polynomial with cos and sin terms: |r(x+iy)| <= sum_j (|c_j| + |d_j|) cosh(j y).
Outer strip (|Im z| < 2 beta): as Route A.  f real on R => mean |f(w+it)|^2 = sum_k |fhat_k|^2 e^{-2kt} with
|fhat_{-k}| = |fhat_k|, nondecreasing in |t|; Re r(w + i beta) = sum_j cosh(j beta)(c_j cos jw + d_j sin jw).
Then q0 = sqrt((nf-1)(ng-1)) < 1, |Re L| <= -log2(1-q0), |B| <= Bmax, |Re u| <= U*, |Re v| <= W*.
Integrand sup on the strip: 2^{p(Delta + U*)} resp. 2^{q(a W* + U*)}, times |2+2cos z| <= 2+2cosh(2beta).
Usage: python3 -I certify_c5.py candidate.json [N_in c beta sigma]   (also: CONTROL=astra for the 6-term control)."""
import json, sys, time, os
from flint import arb, ctx
ctx.prec = 200
def A(s): return arb(str(s))
LN2 = arb(2).log()
def pow2(t): return (t*LN2).exp()
def log2(t): return t.log()/LN2
def up(x): return arb(x.upper())
def widen(x, e): return x + arb(0, e.upper())
def fl(x): return float(x.mid())
def build(rc, sc, ncos, nsin, kap, N_in, c, beta, sig):
    N = N_in*c; pi = arb.pi(); xs = [2*pi*k/N for k in range(N)]
    cj = [[(A(j)*x).cos() for x in xs] for j in range(1, ncos+1)]
    sj = [[(A(j)*x).sin() for x in xs] for j in range(1, nsin+1)]
    def trig(co, k): return sum((co[j]*cj[j][k] for j in range(ncos)), arb(0)) + sum((co[ncos+j]*sj[j][k] for j in range(nsin)), arb(0))
    def S(co, y):
        return sum((abs(co[j])*(A(j+1)*y).cosh() for j in range(ncos)), arb(0)) + sum((abs(co[ncos+j])*(A(j+1)*y).cosh() for j in range(nsin)), arb(0))
    def qerr(M, a, n): return 2*M/((a*n).exp() - 1)
    r = [A(t) for t in rc]; s = [A(t) for t in sc]
    rk = [trig(r, k) for k in range(N)]; sk = [trig(s, k) for k in range(N)]
    F = [pow2(t) for t in rk]; G = [pow2(t) for t in sk]
    Rs, Ss = S(r, sig), S(s, sig)
    Zf = widen(sum(F, arb(0))/N, qerr(pow2(Rs), sig, N)); Zg = widen(sum(G, arb(0))/N, qerr(pow2(Ss), sig, N))
    Zfk = widen(sum((pow2(kap*t) for t in rk), arb(0))/N, qerr(pow2(kap*Rs), sig, N))
    Zgk = widen(sum((pow2(kap*t) for t in sk), arb(0))/N, qerr(pow2(kap*Ss), sig, N))
    LZ = log2(Zf*Zg); H = log2(Zfk) + log2(Zgk) - kap*LZ
    eP = qerr(pow2(Rs+Ss), sig, N_in); eY = qerr((Rs+Ss)*pow2(Rs+Ss), sig, N_in)
    Gs = [G[c*m] for m in range(N_in)]; GSs = [G[c*m]*sk[c*m] for m in range(N_in)]; FR = [F[k]*rk[k] for k in range(N)]
    u, v = [], []
    for k in range(N):
        Pk = arb(0); Yk = arb(0)
        for m in range(N_in):
            i = (k + c*m) % N; Pk += F[i]*Gs[m]; Yk += FR[i]*Gs[m] + F[i]*GSs[m]
        Pk = widen(Pk/N_in, eP); Yk = widen(Yk/N_in, eY)
        assert Pk > 0
        L = log2(Pk) - LZ; B = Yk/Pk - LZ
        u.append(L + (kap-1)*B - H); v.append((2-kap)*B - 2*L + H)
    rb = [r[j]*(A((j % ncos if j < ncos else j - ncos) + 1)*beta).cosh() for j in range(len(r))]
    sb = [s[j]*(A((j % ncos if j < ncos else j - ncos) + 1)*beta).cosh() for j in range(len(s))]
    nf = widen(sum((pow2(2*trig(rb, k)) for k in range(N)), arb(0))/N, qerr(pow2(2*S(rb, sig)), sig, N))/(Zf*Zf)
    ng = widen(sum((pow2(2*trig(sb, k)) for k in range(N)), arb(0))/N, qerr(pow2(2*S(sb, sig)), sig, N))/(Zg*Zg)
    q0 = up(((nf-1)*(ng-1)).sqrt()); assert q0 < 1, 'q0 >= 1'
    Bmax = up(((nf*ng).sqrt()*(S(r, beta) + S(s, beta)) + (1+q0)*abs(LZ))/(1-q0))
    lam = up(-log2(1-q0)); U = up(lam + abs(kap-1)*Bmax + abs(H)); W = up(2*lam + abs(2-kap)*Bmax + abs(H))
    return dict(u=u, v=v, U=U, W=W, q0=q0, eP=eP, eY=eY, xs=xs, N=N, h=2*beta)
def moments(FD, p, q, Dl, a):
    xs, N, h = FD['xs'], FD['N'], FD['h']
    out = []
    for e_fun, sup in [(lambda k: p*(Dl - FD['u'][k]), p*(Dl + FD['U'])), (lambda k: q*(a*FD['v'][k] - FD['u'][k]), q*(a*FD['W'] + FD['U']))]:
        tot = sum(((2 + 2*xs[k].cos())*pow2(e_fun(k)) for k in range(N)), arb(0))/N
        err = 2*(2 + 2*h.cosh())*pow2(sup)/((h*N).exp() - 1)
        out.append(dict(I=tot + arb(0, err.upper()), err=err, sup_bits=sup))
    return out
def H2(x): return -(x*log2(x) + (1-x)*log2(1-x))
def main():
    t0 = time.time()
    N_in, c = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (256, 32)
    beta, sig = (A(sys.argv[4]), A(sys.argv[5])) if len(sys.argv) > 5 else (A('0.1'), A('0.3'))
    cand = json.load(open(sys.argv[1])); res = {}
    if os.environ.get('CONTROL') == 'astra':
        ncos, nsin = 6, 0; rc, sc = cand['r'], cand['s']; kap, p, q = A(cand['kappa']), A(cand['p']), A(cand['q'])
        eta, tau = A(cand['eta']), A(cand['tau'])
    else:
        ncos, nsin = cand['n_terms'], cand['n_terms']; rc, sc = cand['rc'], cand['sc']
        kap, p, q = A(cand['kappa']), A(cand['p']), A(cand['q_m']); eta, tau = A(cand['eta']), A(cand['tau'])
    FD = build(rc, sc, ncos, nsin, kap, N_in, c, beta, sig)
    Dl = eta - tau; Gm = 2*tau - eta; a = Dl/Gm; eps = A('1e-8')
    m = moments(FD, p, q, Dl, a)
    res['strip'] = dict(q0=fl(FD['q0']), Ustar=fl(FD['U']), Wstar=fl(FD['W']), inner_eP=fl(FD['eP']), inner_eY=fl(FD['eY']))
    res['moments'] = [dict(log2_upper=fl(up(log2(x['I']))), log2_ball=log2(x['I']).str(20), outer_err=fl(x['err']), sup_bits=fl(x['sup_bits'])) for x in m]
    if os.environ.get('CONTROL') == 'astra':
        res['control_threshold'] = '.5178685 (Astra continuous threshold)'
        res['control_pass'] = all(up(log2(x['I'])) < A('0.5178685') for x in m)
        # K2-style rejection: same certificate, Delta + .001 must fail the same threshold
        m2 = moments(FD, p, q, Dl + A('0.001'), (Dl + A('0.001'))/(Gm - A('0.001')))
        res['K2_DeltaPlus_rejected'] = bool(max(log2(x['I']).lower() for x in m2) > A('0.5178685'))
    else:
        K = cand['K']; mu, gam = A(cand['mu']), A(cand['gamma']); g_ = A(cand['guard']); c0 = A(cand['minimum_useful_probability'])
        h4 = 2 - A('0.75')*log2(arb(3))
        dloc = A('0.5') - gam - A('1e-8'); d0 = (1-c0)*K*dloc*mu*(1 - A('1e-7')); d1 = d0 - A('1e-9'); cap = tau + 20*eps
        rho_f = eta - 48*eps - A('5e-7'); rho_c = rho_f - A('1e-6')
        mg = dict(blocks=1 - K*mu, list=tau - (A('0.5') + (h4 - A('0.5') - gam)*mu), pairs=tau - (1 + (2*h4 - 1 - gam)*mu - eta + g_),
                  local_to_prime=A('0.5') - dloc - gam, coverage=1 - d0/(K*dloc*mu) - c0, prelim_cheb=d0 - d1, prelim_cap=cap - (A('0.5') - d1),
                  sparse=eta - H2(mu) - mu - g_, setup=tau - A('0.25') - mu, prime=tau - eta/2, Delta=Dl, Gamma=Gm,
                  rho_gap=rho_f - rho_c, eta_rho_f=eta - rho_f - 48*eps,
                  M1=rho_c - log2(m[0]['I']), M2=rho_c - log2(m[1]['I']),
                  p_ge_1=p - 1, p_cap=30 - 3*p, q_ge_1=q - 1, q_cap=30 - q*(4*a + 3))
        res['margins_lower'] = {k: fl(arb(x.lower())) for k, x in mg.items()}
        res['all_pass'] = all(x.lower() > 0 for x in mg.values())
        T = max([tau + 20*eps, cap, mu + A('0.25'), eta/2], key=lambda t: fl(t))
        res['leading_exponent_upper'] = fl(up(T)); res['leading_exponent_decimal'] = (tau + 20*eps).str(15)
        res['vs_astra_0.4897736'] = fl(A('0.4897736') - up(T))
    res['params'] = dict(N_in=N_in, c=c, N_out=FD['N'], beta=fl(beta), sigma=fl(sig), prec=ctx.prec, seconds=round(time.time() - t0))
    print(json.dumps(res, indent=1))
if __name__ == '__main__':
    main()
