"""C3 S1 (E2-floor by K, interval arithmetic) and S2 (scalar window at T = .48). Control K-a included."""
import json
from fractions import Fraction as F
from mpmath import iv, mp
iv.prec = 200
def I(x): x = F(x); return iv.mpf(x.numerator) / x.denominator
h = 2 - I(F(3, 4)) * iv.log(3) / iv.log(2)
eps, g = I('1e-8'), I('1e-5')
out = {'h(1/4)': [str(h.a), str(h.b)], 'S1': {}, 'S2': {}}
def floor(K, c):
    den = 1 + K * c
    return iv.mpf(0.5) - c * (1 - h) / den + (K * c / den) * 20 * eps, 1 / den, K * c / den
for c0 in ['.005', '.0001', '0']:
    c = 1 - I(c0); rows = {}
    for K in range(1, 18):
        f, wp, wl = floor(K, c)
        rows[K] = dict(floor_lo=float(f.a), floor_hi=float(f.b), below_048=bool(f.b < I('.48')),
                       w_prelim=float(wp.a), w_list=float(wl.a))
    out['S1'][c0] = rows
# control K-a
ka = {'.005': '0.48951856638776', '.0001': '0.48951569849967', '0': '0.48951564024772'}
out['K-a'] = {c0: dict(ours=mp.nstr(floor(17, 1 - I(c0))[0].a, 15), astra=v,
              pass_=abs(float(floor(17, 1 - I(c0))[0].a) - float(v)) < 1e-13) for c0, v in ka.items()}
out['largest_K_below_048'] = {c0: max(K for K, r in out['S1'][c0].items() if r['below_048']) for c0 in out['S1']}
# S2: tau = .48 - 20 eps, mu = 1/K.  list: tau >= .5 - (1-h-d) mu  ->  d <= 1-h - (.5-tau)/mu
#                                    prelim: tau >= .5 - c K mu d   ->  d >= (.5-tau)/(c K mu)
#                                    pair: eta >= 1 + (2h-1-gamma) mu + g - tau, gamma = .5-d  (least eta at largest d)
tau = I('.48') - 20 * eps
for c0 in ['.005', '.0001']:
    c = 1 - I(c0); rows = {}
    for K in range(1, 18):
        mu = I(1) / K
        dmax = 1 - h - (I('.5') - tau) / mu
        dmin = (I('.5') - tau) / (c * K * mu)
        if dmax.b < dmin.a: continue
        gam = I('.5') - dmax
        eta = 1 + (2 * h - 1 - gam) * mu + g - tau
        Dl = eta - tau; a = Dl / (2 * tau - eta)
        rows[K] = dict(d_min=float(dmin.b), d_max=float(dmax.a), gamma_at_dmax=float(gam.a), eta_min=float(eta.b),
                       Delta=float(Dl.b), a=float(a.b), qm_cap=float((30 / (4 * a + 3)).a),
                       eta_minus_2tau=float((eta - 2 * tau).b))
    out['S2'][c0] = rows
print(json.dumps(out, indent=1))
