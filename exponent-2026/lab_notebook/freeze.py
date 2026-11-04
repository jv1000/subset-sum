"""C5-cert step 1 (floating): freeze the K=16 candidate as exact decimals with explicit slack.
Densities, kappa, p, q_m are rounded first and then held fixed; scalars (mu, eta, gamma) are re-optimized at a fixed
tau slightly above the floating optimum to maximize the least margin; then rounded. Output: candidate_K16.json."""
import json
from decimal import Decimal as Dd, ROUND_HALF_EVEN
import numpy as np
from scipy.optimize import minimize
SRC = 's5_K16_random_both_n16_s1_b4.0_k0.5-2.0_N512.json'
d = json.load(open(SRC)); z = np.array(d['z']); n = 16; nt = 32; K = 16
def rd(x, k): return str(Dd(repr(float(x))).quantize(Dd(1).scaleb(-k), rounding=ROUND_HALF_EVEN))
rc = [rd(t, 8) for t in z[4:4+nt]]; sc = [rd(t, 8) for t in z[4+nt:4+2*nt]]
kap, p, q = rd(z[-3], 8), rd(z[-2], 8), rd(z[-1], 8)
H4 = 2 - .75*np.log2(3); EPS = 1e-8; C0 = 1e-4; G_ = 1e-5
N = 1024; x = 2*np.pi*np.arange(N)/N; j = np.arange(1, n+1)
Bm = np.hstack([np.cos(np.outer(x, j)), np.sin(np.outer(x, j))]); pref = 2 + 2*np.cos(x)
r = Bm @ np.array(rc, float); s = Bm @ np.array(sc, float); kf, pf, qf = float(kap), float(p), float(q)
F, G = 2.0**r, 2.0**s; Zf, Zg = F.mean(), G.mean(); f, g = F/Zf, G/Zg
corr = lambda a, b: np.fft.ifft(np.fft.fft(a)*np.conj(np.fft.fft(b))).real/N
Q = corr(f, g); Bb = (corr(f*r, g) + corr(f, g*s))/Q - np.log2(Zf*Zg); L = np.log2(Q)
Hh = np.log2(np.mean(f**kf)*np.mean(g**kf)); u = L + (kf-1)*Bb - Hh; v = (2-kf)*Bb - 2*L + Hh
def h2(m): return -m*np.log2(m)-(1-m)*np.log2(1-m)
def moms(eta, tau):
    D = eta - tau; a = D/(2*tau - eta)
    return np.log2([np.mean(pref*2.0**(pf*(D-u))), np.mean(pref*2.0**(qf*(a*v-u)))])
TAU = float(d['tau']) + 5e-7
def margins(y, tau=TAU):
    mu, eta, gam = y
    dloc = .5 - gam - 1e-8; d0 = (1-C0)*K*dloc*mu*(1-1e-7); d1 = d0 - 1e-9; cap = tau + 20*EPS
    m = moms(eta, tau); rho_f = eta - 48*EPS - 5e-7; rho_c = rho_f - 1e-6
    D = eta - tau; a = D/(2*tau-eta)
    return np.array([1-K*mu, tau-(.5+(H4-.5-gam)*mu), tau-(1+(2*H4-1-gam)*mu-eta+G_), cap-(.5-d1),
                     eta-h2(mu)-mu-G_, tau-.25-mu, tau-eta/2, rho_c-m[0], rho_c-m[1], 30-3*pf, 30-qf*(4*a+3)])
y0 = np.array([d['mu'], d['eta'] + 5e-7, d['gamma']])
res = minimize(lambda w: -w[-1], np.append(y0, 0), method='SLSQP',
               constraints=[dict(type='ineq', fun=lambda w: margins(w[:3]) - w[-1])], options=dict(maxiter=500, ftol=1e-15))
mu, eta, gam = [rd(t, 10) for t in res.x[:3]]
mf = margins([float(mu), float(eta), float(gam)])
tau = rd(TAU, 10)
cand = dict(K=K, n_terms=n, basis='r(x) = sum_j rc[j] cos(jx) + sum_j rc[16+j] sin(jx), j = 1..16 (same for s)',
            rc=rc, sc=sc, kappa=kap, p=p, q_m=q, mu=mu, eta=eta, tau=tau, gamma=gam, epsilon='0.00000001', guard='0.00001',
            minimum_useful_probability='0.0001', local_deficiency_rule='d = 1/2 - gamma - 1e-8',
            d0_rule='d0 = (1 - c0) K d mu (1 - 1e-7)', d1_rule='d1 = d0 - 1e-9', cap_rule='cap = tau + 20 eps',
            rho_f_rule='rho_f = eta - 48 eps - 5e-7', rho_c_rule='rho_c = rho_f - 1e-6',
            floating_margins=dict(zip(['blocks', 'list', 'pairs', 'prelim_cap', 'sparse', 'setup', 'prime', 'M1', 'M2', '3p', 'qcap'], mf.tolist())),
            floating_T=float(tau) + 20*EPS, source=SRC)
json.dump(cand, open('candidate_K16.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in cand.items() if k not in ('rc', 'sc')}, indent=1))
