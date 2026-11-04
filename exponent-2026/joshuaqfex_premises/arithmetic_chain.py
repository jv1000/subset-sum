"""C2 step 6: independent recomputation of the scalar chain of JoshuaQFEX paper.tex (transfer lemma, Prop.
"Transferred continuous moments", alias constraints, exponent budget).  Written from paper.tex and Base §2.2/§6;
does not import or run the repo's verify.py.  Engine: mpmath iv at 300 bits plus fractions.Fraction for exact parts.
Optional 2nd argument: Route A result JSON -> also recomputes per-certificate transferred margins from the CERTIFIED old
margins and actual z0 and region top H (sharper than the paper's uniform bounds).
Usage: python3 -I arithmetic_chain.py parameters.json [routeA.json data.json] > out
"""
import json, sys
from fractions import Fraction as Fr
from mpmath import iv
iv.prec = 300
P = {k: Fr(v) for k, v in json.load(open(sys.argv[1])).items()}
tau, eta, a, mu, gam, l = P['tau'], P['eta'], P['a'], P['mu'], P['gamma'], P['l']
eps, zeta, guard = P['epsilon'], P['zeta'], P['input_guard_coefficient']
tau_b, eta_b = Fr('0.48769'), Fr('0.51613')
out = {}
D, G = eta - tau, 2 * tau - eta
Db, Gb = eta_b - tau_b, 2 * tau_b - eta_b
q = G / Gb; A_, Ab = D / G, Db / Gb; K = D / q - Db
out['Delta'], out['Gamma'] = str(D), str(G)
out['eta_minus_tau_minus_Delta'] = str(eta - tau - D)
out['q'] = float(q); out['K'] = float(K); out['A_minus_Ab'] = float(A_ - Ab)
out['identity_0<q<1'] = 0 < q < 1; out['identity_K>0'] = K > 0
out['identity_A-Ab==K/Gb (exact)'] = (A_ - Ab) == K / Gb
out['A<1/4'] = A_ < Fr(1, 4)
de = eta - eta_b
Z = Fr('418.36'); z0r0, z0r1 = Fr('17.211'), Fr('8.4537')
m0 = Fr('0.00025') + de - z0r0 * K
m1 = Fr('0.00025') + de - z0r1 * Fr('1.25') * K
m28 = 4 + de - Z * 15 * K
m9 = 17 + de - Z * 256 * (A_ - Ab)
out['transferred_margins_paper_form'] = {'m0': float(m0), 'm1': float(m1), 'm2_8': float(m28), 'm9': float(m9),
                                             'all_gt_1e-6': all(m > Fr(1, 10**6) for m in (m0, m1, m28, m9))}
out['new_multiplier_sum_bound'] = float(Z * (1 + A_ - Ab)); out['new_sum_lt_419'] = Z * (1 + A_ - Ab) < 419
cz = 6 * 419
out['mse_exponent_remaining'] = float(Fr(1, 10**6) - (18 + cz) * eps)
# alias constraints, true entropy, rigorous intervals
def I(x): return iv.mpf([Fr(x).numerator, Fr(x).numerator]) / Fr(x).denominator
def h(x):
    x = I(x); return -(x * iv.log(x) + (1 - x) * iv.log(1 - x)) / iv.log(2)
half = Fr(1, 2); r = 1 - mu - l
cons = {
    'C1 gamma < h(2a)/2': h(2 * a) / 2 - I(gam),
    'C2 l + (h(a)-gamma)mu < tau': I(tau) - (I(l) + (h(a) - I(gam)) * I(mu)),
    'C3 r + (1-gamma)mu < tau': I(tau - r - (1 - gam) * mu),
    'C4 1-mu+(h(a)+h(1/2-a)-gamma)mu-eta < tau': I(tau) - (I(1 - mu) + (h(a) + h(half - a) - I(gam)) * I(mu) - I(eta)),
    'C5 h(1/2-a)mu + 1/2 - tau < tau': I(tau) - (h(half - a) * I(mu) + I(half - tau)),
    'C5L h(a)mu + 1/2 - tau < tau': I(tau) - (h(a) * I(mu) + I(half - tau)),
    'C6 r>0': I(r), 'C6 r<tau': I(tau - r), 'C6 l<tau': I(tau - l),
    'C7 mu(1-2a) < l': I(l - mu * (1 - 2 * a)),
    'C8 (mu/2)log2(3) < eta': I(eta) - I(mu) / 2 * iv.log(3) / iv.log(2),
    'S mu(1-2a) <= 1/2': I(half - mu * (1 - 2 * a)),
    'S3 h(2a)/2 + h(a) < 1-2a': I(1 - 2 * a) - h(2 * a) / 2 - h(a),
    'h(a) < h(1/2-a)': h(half - a) - h(a),
}
out['alias_slacks_lower'] = {k: float(v.a) for k, v in cons.items()}
least = min(v.a for v in cons.values())
out['least_alias_slack_lower'] = float(least)
out['guard_plus_zeta'] = float(zeta + 1 / guard)
out['alias_all_strict'] = all(v.a > 0 for v in cons.values())
out['least_slack_exceeds_guard_plus_zeta'] = bool(least > iv.mpf(float(zeta + 1 / guard)) * 1.000001)
out['work_exponent_tau_plus_20eps'] = str(tau + 20 * eps)
out['target_exponent'] = str(P['target_exponent'])
out['pure_gap'] = float(P['target_exponent'] - tau - 20 * eps)
out['tau+20eps<target'] = tau + 20 * eps < P['target_exponent']
if len(sys.argv) > 3:
    RA = json.load(open(sys.argv[2])); data = json.load(open(sys.argv[3]))
    zmap = {(c['v'], c['region']): c for c in data['certs']}
    tops = [None, '1.25', '1.6', '2', '2.6', '3.5', '5', '8', '15', None]
    worst = {}
    for c in RA['certs']:
        cert = zmap[(c['v'], c['region'])]; z0 = Fr(cert['z'][0]); old = Fr(c['log2_margin_lower'])
        g = c['region']
        if g == 0: new = old + de - z0 * K
        elif g < 9: new = old + de - z0 * K * Fr(tops[g])
        else: new = old + de - z0 * 256 * (A_ - Ab)
        if g not in worst or new < worst[g][0]: worst[g] = (new, c['v'])
    out['per_certificate_transferred_margin_min_by_region (from certified old margins, actual z0)'] = {
        f'rho{g}': dict(min=float(worst[g][0]), filter=worst[g][1]) for g in sorted(worst)}
    out['per_certificate_all_gt_1e-6'] = all(w[0] > Fr(1, 10**6) for w in worst.values())
print(json.dumps(out, indent=1))
