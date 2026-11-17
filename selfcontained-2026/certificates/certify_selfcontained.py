"""Ball-arithmetic certificate for the numerical premises of the self-contained manuscript.
Every margin is keyed by the premise label used in the paper:
(E0), (C1)-(C8), (N1)-(N14), (M1), (M2), plus the auxiliary filter constants quoted in the text.

Conventions:
  * eps0 is the fixed exact decimal 0.0000013156 of the paper.  (E0) certifies that every (C1)-(C8) slack
    exceeds eps0, and eps0 enters every other line as an exact number.
  * margins are exported as directed lower bounds (rounded toward minus infinity).

The moments are computed by certify_c5.build / certify_c5.moments; the analytic justification of
its strip bounds is Lemma "strip bounds" in the section on numerical certification.

Usage (from this directory; the stored run uses the arguments shown):
    python certify_selfcontained.py candidate_base.json 512 32 0.1 0.25
Arguments: N_in (inner nodes), c (outer nodes = N_in*c), beta (outer strip half-width is 2*beta),
sigma (inner strip half-width).  Precision: 200 bits (set in certify_c5).
"""
import importlib.util
import json
import math
import os
import sys
import time
from fractions import Fraction

from flint import arb, ctx

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('certify_c5', os.path.join(HERE, 'certify_c5.py'))
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)
A, log2, up = C.A, C.log2, C.up
ctx.prec = 200

EPS0 = '0.0000013156'          # the fixed common slack eps0 of the paper (exact decimal)


def H2(x):
    return -(x*log2(x) + (1 - x)*log2(1 - x))


def lower_float(x):
    """A double that is <= the lower endpoint of the ball x (directed rounding)."""
    return math.nextafter(float(x.lower().mid()), -math.inf)


def upper_float(x):
    return math.nextafter(float(x.upper().mid()), math.inf)


def main():
    t0 = time.time()
    cand = json.load(open(sys.argv[1]))
    N_in, c = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (512, 32)
    beta, sig = (A(sys.argv[4]), A(sys.argv[5])) if len(sys.argv) > 5 else (A('0.1'), A('0.25'))

    t, eta, mu, a, g, l = [A(cand[k]) for k in ('tau0', 'eta', 'mu', 'a', 'gamma', 'l')]
    kap, p1, p2 = A(cand['kappa']), A(cand['p']), A(cand['q_m'])
    eps, zeta, guard = A(cand['epsilon']), A(cand['zeta']), A(cand['input_guard_coefficient'])
    eps0 = A(EPS0)
    r = 1 - mu - l
    D = eta - t
    G = 2*t - eta
    aG = D/G
    half = A('0.5')
    rho_f = eta - A('1.5e-6')
    rho_c = rho_f - A('1e-6')
    delta = (eta - mu/2*log2(arb(3)))/2
    pmax = p1 if p1 > p2 else p2

    FD = C.build(cand['rc'], cand['sc'], cand['n_terms'], cand['n_terms'], kap, N_in, c, beta, sig)
    m = C.moments(FD, p1, p2, D, aG)

    # (C1)-(C8): slack = right side minus left side
    cslack = {
        'C1 gamma < h(2a)/2': H2(2*a)/2 - g,
        'C2 l + (h(a)-gamma) mu < tau0': t - (l + (H2(a) - g)*mu),
        'C3 r + (1-gamma) mu < tau0': t - (r + (1 - g)*mu),
        'C4 1 - mu + (h(a)+h(1/2-a)-gamma) mu - eta < tau0': t - (1 - mu + (H2(a) + H2(half - a) - g)*mu - eta),
        'C5 h(1/2-a) mu + 1/2 - tau0 < tau0': t - (H2(half - a)*mu + half - t),
        'C6a 0 < r': r,
        'C6b r < tau0': t - r,
        'C6c l < tau0': t - l,
        'C7 mu(1-2a) < l': l - mu*(1 - 2*a),
        'C8 (mu/2) log 3 < eta': eta - mu/2*log2(arb(3)),
    }
    # (E0): every (C)-slack exceeds the fixed eps0
    e0 = {'E0 ' + k.split(' ')[0] + ' slack - eps0': v - eps0 for k, v in cslack.items()}
    nprem = {
        'N1 zeta + 1/G0 < eps0': eps0 - (zeta + 1/guard),
        'N2 mu < tau0 - eps0': t - eps0 - mu,
        'N3 1/2 - tau0 + zeta < delta': delta - (half - t + zeta),
        'N4 4a < 1': 1 - 4*a,
        'N5 h(2a)/2 + h(a) < 1 - 2a': (1 - 2*a) - (H2(2*a)/2 + H2(a)),
        'N6 mu(1-2a) < 1/2': half - mu*(1 - 2*a),
        'N7 h(a) < h(1/2-a)': H2(half - a) - H2(a),
        'N8a 1/2 - tau0 + gamma mu/2 < tau0 - eps0': (t - eps0) - (half - t + g*mu/2),
        'N8b r + 1/2 - tau0 < tau0 - eps0': (t - eps0) - (r + half - t),
        'N9 eta/2 < tau0': t - eta/2,
        'N10a Delta > 0': D,
        'N10b Gamma > 0': G,
        'N11 a_Gamma <= 3/4': A('0.75') - aG,
        'N12a p1 >= 1': p1 - 1,
        'N12b p2 >= 1': p2 - 1,
        'N13 (18 + 6 max(p1,p2)) eps < eta - rho_f': (eta - rho_f) - (18 + 6*pmax)*eps,
        'N14 rho_c < rho_f': rho_f - rho_c,
    }
    mom = {
        'M1 log2(first moment) < rho_c': rho_c - log2(m[0]['I']),
        'M2 log2(second moment) < rho_c': rho_c - log2(m[1]['I']),
    }

    # auxiliary filter constants quoted in the text (exact decimal coefficients)
    J = cand['n_terms']
    rco = [A(x) for x in cand['rc']]
    sco = [A(x) for x in cand['sc']]
    def norm1(co): return sum((abs(x) for x in co), arb(0))
    def norm1j(co): return sum(((j % J + 1)*abs(co[j]) for j in range(2*J)), arb(0))
    Rr, Rs = norm1(rco), norm1(sco)
    R, R1 = Rr + Rs, norm1j(rco) + norm1j(sco)
    kplus = kap if kap > 1 else arb(1)
    C0 = 2*kplus*R
    C1 = 64*kplus*kplus*C.pow2(2*kplus*R)*R1*(1 + R)*(1 + R)
    Uinf, Winf = 2*(1 + kap)*R, (4 + 2*kap)*R
    b1, b2 = p1*(D + Uinf), p2*(aG*Winf + Uinf)
    beta0 = b1 if b1 > b2 else b2
    # Lemma "finite-circle moments": P0 = ceil(A).  log2A encloses log2 A; since ceil(A) <= A + 1,
    # log2P0 = log2(A + 1) is an upper bound for log2 P0 (the ceiling is accounted for, not ignored).
    log2A = log2(20*(1 + p1 + 2*p2)*C1) + beta0 - log2(C.pow2(rho_f) - C.pow2(rho_c))
    log2P0 = log2(C.pow2(log2A) + 1)
    aux = {
        'X1 ||r||_1 <= 3.64': A('3.64') - Rr,
        'X2 ||s||_1 <= 3.60': A('3.60') - Rs,
        'X3 R <= 7.24': A('7.24') - R,
        'X4 C0 <= 15': 15 - C0,
        'X5 C1 < 2^32': arb(2)**32 - C1,
        'X6 beta0 < 270': 270 - beta0,
        'X7 log2 P0 <= log2(A+1) < 339': 339 - log2P0,
        'X8 7-eps variant of N13 (remark only)': (eta - rho_f) - (18 + 7*pmax)*eps,
    }

    # facts of exact decimal arithmetic, checked with exact rationals
    F = lambda k: Fraction(cand[k])
    fe0 = Fraction(EPS0)
    exact = {
        'tau0 < 1/2': F('tau0') < Fraction(1, 2),
        '1/G0 = zeta': Fraction(1, int(cand['input_guard_coefficient'])) == F('zeta'),
        'tau0 + 20 eps = 0.4875754036': F('tau0') + 20*F('epsilon') == Fraction('0.4875754036'),
        '0.4875754036 < 0.4875755': Fraction('0.4875754036') < Fraction('0.4875755'),
        'tau0 + 20 eps < 0.49': F('tau0') + 20*F('epsilon') < Fraction('0.49'),
        'a <= 1/6': F('a') <= Fraction(1, 6),
        'eta < 1': F('eta') < 1,
        'N1 exactly: eps0 - zeta - 1/G0 = 0.0000012956':
            fe0 - F('zeta') - Fraction(1, int(cand['input_guard_coefficient'])) == Fraction('0.0000012956'),
        'r = 1 - mu - l = 0.0411230499': 1 - F('mu') - F('l') == Fraction('0.0411230499'),
        'Delta = 0.0286969377': F('eta') - F('tau0') == Fraction('0.0286969377'),
        'Gamma = 0.4588782659': 2*F('tau0') - F('eta') == Fraction('0.4588782659'),
        'rho_c = eta - 0.0000025 = 0.5162696413': F('eta') - Fraction('0.0000025') == Fraction('0.5162696413'),
    }

    allm = {**e0, **cslack, **nprem, **mom, **aux}
    premises = {**e0, **cslack, **nprem, **mom}
    res = dict(
        eps0=EPS0,
        margins_lower={k: lower_float(v) for k, v in allm.items()},
        all_premises_pass=all(v.lower() > 0 for v in premises.values()),
        all_auxiliary_pass=all(v.lower() > 0 for v in aux.values()),
        all_exact_decimal_facts=all(exact.values()),
        exact_decimal_facts=exact,
        counts=dict(E0=len(e0), C=len(cslack), N=len(nprem), M=len(mom), auxiliary=len(aux)),
        least_C_slack_ball=min(cslack.values(), key=lambda v: float(v.mid())).str(30),
        log2M1=log2(m[0]['I']).str(20), log2M2=log2(m[1]['I']).str(20),
        log2M1_upper=upper_float(log2(m[0]['I'])), log2M2_upper=upper_float(log2(m[1]['I'])),
        strip=dict(q0_upper=upper_float(FD['q0']), Ustar_upper=upper_float(FD['U']), Wstar_upper=upper_float(FD['W']),
                   inner_err_P_upper=upper_float(FD['eP']), inner_err_Y_upper=upper_float(FD['eY']),
                   log2_outer_err_M1_upper=upper_float(log2(m[0]['err'])),
                   log2_outer_err_M2_upper=upper_float(log2(m[1]['err'])),
                   sup_bits_M1_upper=upper_float(m[0]['sup_bits']), sup_bits_M2_upper=upper_float(m[1]['sup_bits'])),
        filter_constants=dict(norm_r=Rr.str(12), norm_s=Rs.str(12), R1=R1.str(12), C0=C0.str(12), C1=C1.str(12),
                              U_inf=Uinf.str(10), W_inf=Winf.str(10), beta0=beta0.str(10), log2_A=log2A.str(25),
                              log2_P0_upper=upper_float(log2P0),
                              a_Gamma=aG.str(15), delta=delta.str(15)),
        T=(t + 20*eps).str(15),
        params=dict(N_in=N_in, c=c, N_out=FD['N'], beta=float(beta.mid()), sigma=float(sig.mid()), prec_bits=ctx.prec,
                    python=sys.version.split()[0], seconds=round(time.time() - t0)),
    )
    print(json.dumps(res, indent=1))
    return 0 if (res['all_premises_pass'] and res['all_auxiliary_pass'] and res['all_exact_decimal_facts']) else 1


if __name__ == '__main__':
    sys.exit(main())
