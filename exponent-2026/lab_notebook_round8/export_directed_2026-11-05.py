"""Directed (outward-rounded) decimal exports for cert_base_512.json and cert_K16_512x32.json (Claude, 2026-11-05).
Fixes two issues found by Astra (round 8): (1) some fields labelled lower/upper bounds were ordinary rounded floats on
the wrong side of the true value (cert_base C8 lower; cert_K16 M2 log2_upper); (2) outer_err = 0.0 was a float
underflow. The original JSONs are unchanged (they are in snapshots 1-4). Method: lower-bound floats are rounded DOWN
to 13 significant digits, upper-bound floats UP (each float is within 1e-16 relative of its ball midpoint, far inside
that margin); moment balls are turned into [lo, hi] with outward rounding at 25 digits; outer_err is recomputed from
the certifier's formula 2(2+2cosh h) 2^sup / (e^{hN} - 1) with h = 2*beta, N = N_out."""
import json
from mpmath import mp, mpf, floor, ceil, log10, cosh, exp
mp.dps = 60
def dn(x, sig=13):
    x = mpf(x); e = int(floor(log10(abs(x)))) - sig + 1; return mp.nstr(floor(x / mpf(10)**e) * mpf(10)**e, sig + 5)
def up(x, sig=13):
    x = mpf(x); e = int(floor(log10(abs(x)))) - sig + 1; return mp.nstr(ceil(x / mpf(10)**e) * mpf(10)**e, sig + 5)
def ball(sv, sig=25):
    mid, rad = sv.strip('[]').split('+/-'); m, r = mpf(mid), mpf(rad)
    return [dn(m - r, sig), up(m + r, sig)]
out = {}
b = json.load(open('cert_base_512.json'))
out['cert_base_512'] = {'margins_lower_directed': {k: dn(v) for k, v in b['margins_lower'].items()},
                        'eps0_lower_directed': dn(b['eps0_lower']) if isinstance(b['eps0_lower'], (int, float)) else b['eps0_lower'],
                        'log2M1_enclosure': ball(b['log2M1']), 'log2M2_enclosure': ball(b['log2M2']),
                        'T_upper': b['T_upper'],
                        'note_vs_Base': 'vs_Base_0_48769 in the original compares tau0 values (0.48769 - tau0 = 1.147964e-4); the final-threshold gap is 0.48769 - T = 1.145964e-4'}
k = json.load(open('cert_K16_512x32.json')); pr = k['params']; h = 2 * mpf(pr['beta']); N = pr['N_out']
mom = []
for m_ in k['moments']:
    err = 2 * (2 + 2 * cosh(h)) * mpf(2) ** mpf(m_['sup_bits']) / (exp(h * N) - 1)
    mom.append({'log2_enclosure': ball(m_['log2_ball']), 'log2_upper_directed': up(mpf(m_['log2_ball'].strip('[]').split('+/-')[0]) + mpf(m_['log2_ball'].strip('[]').split('+/-')[1])),
                'outer_err_bound': mp.nstr(err * (1 + mpf(10)**-10), 6)})
out['cert_K16_512x32'] = {'moments': mom, 'margins_lower_directed': {kk: dn(v) for kk, v in k['margins_lower'].items()},
                          'leading_exponent_upper': k['leading_exponent_upper']}
# checks: the two fields Astra flagged
assert mpf(out['cert_base_512']['margins_lower_directed']['C8 (mu/2)log3 < eta']) < mpf('0.13965164495327371651381293553496416')
assert mpf(mom[1]['log2_upper_directed']) > mpf('0.51847734723194144144065695331465011')
assert all(mpf(v) > 0 for v in out['cert_base_512']['margins_lower_directed'].values())
assert all(mpf(v) > 0 for v in out['cert_K16_512x32']['margins_lower_directed'].values())
json.dump(out, open('cert_exports_directed_2026-11-05.json', 'w'), indent=1)
print('ok; C8 lower', out['cert_base_512']['margins_lower_directed']['C8 (mu/2)log3 < eta'], '| K16 M2 upper', mom[1]['log2_upper_directed'], '| outer_err', [m['outer_err_bound'] for m in mom])
