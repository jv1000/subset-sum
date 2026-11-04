"""C12 rigorous certificate (python-flint arb) for the Base-construction point with ONE asymmetric filter.
Moments via certify_c5.build/moments (Route A strip method, sine terms); scalar conditions of Base §2.2, §5, §6 in balls.
Usage: python3 -I certify_base.py candidate_base.json [N_in c beta sigma]"""
import json, sys, time, importlib.util
from flint import arb, ctx
sp = importlib.util.spec_from_file_location('c5', 'certify_c5.py'); C = importlib.util.module_from_spec(sp); sp.loader.exec_module(C)
A, log2, fl, up = C.A, C.log2, C.fl, C.up
ctx.prec = 200
def H2(x): return -(x*log2(x) + (1-x)*log2(1-x))
def main():
    t0 = time.time(); cand = json.load(open(sys.argv[1]))
    N_in, c = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (256, 32)
    beta, sig = (A(sys.argv[4]), A(sys.argv[5])) if len(sys.argv) > 5 else (A('0.1'), A('0.3'))
    t, eta, mu, a, g, l = [A(cand[k]) for k in ('tau0', 'eta', 'mu', 'a', 'gamma', 'l')]
    kap, p, q = A(cand['kappa']), A(cand['p']), A(cand['q_m']); eps, zeta = A(cand['epsilon']), A(cand['zeta'])
    guard = A(cand['input_guard_coefficient']); r = 1 - mu - l
    D = eta - t; G = 2*t - eta; aG = D/G
    FD = C.build(cand['rc'], cand['sc'], cand['n_terms'], cand['n_terms'], kap, N_in, c, beta, sig)
    m = C.moments(FD, p, q, D, aG)
    rho_f = eta - A('1.5e-6'); rho_c = rho_f - A('1e-6')
    alias = {'C1 gamma < h(2a)/2': H2(2*a)/2 - g,
             'C2 left list': t - (l + (H2(a) - g)*mu),
             'C3 right classes': t - (r + (1 - g)*mu),
             'C4 pairs': t - (1 - mu + (H2(a) + H2(A('0.5') - a) - g)*mu - eta),
             'C5 right masks': t - (H2(A('0.5') - a)*mu + A('0.5') - t),
             'C5L left masks (implied)': t - (H2(a)*mu + A('0.5') - t),
             'C6 r > 0': r, 'C6 r < tau0': t - r, 'C6 l < tau0': t - l,
             'C7 mu(1-2a) < l': l - mu*(1 - 2*a),
             'C8 (mu/2)log3 < eta': eta - mu/2*log2(arb(3))}
    eps0 = min((x.lower() for x in alias.values() if True), key=lambda z: z)
    extra = {'eps0 > zeta + 1/guard (Base l.177, l.603)': arb(eps0) - (zeta + 1/guard),
             'mu < tau0 - eps0 (Base l.570)': t - arb(eps0) - mu,
             'A5: 1/2 - tau0 + zeta < delta = (eta - (mu/2)log3)/2': (eta - mu/2*log2(arb(3)))/2 - (A('0.5') - t + zeta),
             'S1: 4a < 1': 1 - 4*a,
             'S3: h(2a)/2 + h(a) < 1 - 2a': (1 - 2*a) - (H2(2*a)/2 + H2(a)),
             'Delta > 0': D, 'Gamma > 0': G,
             # added after referee 3 (A7 items 1,3,4; S2; S5; prime draw; B2 row-error a_Gamma <= 3/4)
             'A7.1: l < tau0 - eps0': t - arb(eps0) - l, 'A7.1: r < tau0 - eps0': t - arb(eps0) - r,
             'A7.1: mu(1-2a) < tau0 - eps0': t - arb(eps0) - mu*(1 - 2*a),
             'A7.3: 1/2 - tau0 + zeta + gamma mu/2 < tau0 - eps0 + zeta': (t - arb(eps0) + zeta) - (A('0.5') - t + zeta + g*mu/2),
             'A7.4: r + 1/2 - tau0 + zeta < tau0 - eps0 + zeta': (t - arb(eps0) + zeta) - (r + A('0.5') - t + zeta),
             'S2: mu(1-2a) < 1/2': A('0.5') - mu*(1 - 2*a),
             'S5: h(a) < h(1/2-a)': H2(A('0.5') - a) - H2(a),
             'prime draw: eta/2 < tau0': t - eta/2,
             'B2 row error: a_Gamma <= 3/4': A('0.75') - aG,
             'rho0 cert: z0 = p >= 1': p - 1, 'rho1..9 cert: z0 b_{i-1} = q b_{i-1} >= 1 (b0 = 1)': q - 1,
             'sum z <= 418.36': A('418.36') - (p if p > q else q),
             'B3: eta - rho_f > (18 + 6 max(p,q)) eps': (eta - rho_f) - (18 + 6*(p if p > q else q))*eps,
             'B1: rho_f - rho_c > 0 (finite-circle slack)': rho_f - rho_c,
             'M1 = rho0 integral < 2^rho_c': rho_c - log2(m[0]['I']),
             'M2 = rho1..rho9 integrals < 2^rho_c': rho_c - log2(m[1]['I'])}
    allm = {**alias, **extra}
    res = dict(margins_lower={k: fl(arb(v.lower())) for k, v in allm.items()}, all_pass=all(v.lower() > 0 for v in allm.values()),
               eps0_lower=fl(arb(eps0)), log2M1=log2(m[0]['I']).str(20), log2M2=log2(m[1]['I']).str(20),
               strip=dict(q0=fl(FD['q0']), Ustar=fl(FD['U']), Wstar=fl(FD['W']), inner_eP=fl(FD['eP']), inner_eY=fl(FD['eY'])),
               T_upper=fl(up(t + 20*eps)), T_ball=(t + 20*eps).str(15), vs_JoshuaQFEX_0_48767595=fl(A('0.48767595') - up(t + 20*eps)),
               vs_Base_0_48769=fl(A('0.48769') - up(t)), params=dict(N_in=N_in, c=c, beta=fl(beta), sigma=fl(sig), seconds=round(time.time() - t0)))
    print(json.dumps(res, indent=1))
if __name__ == '__main__':
    main()
