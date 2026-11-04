"""Freeze the C12 point: round densities/kappa/p/q, then re-optimize (eta, mu, a, gamma, l) at tau0 = tau_opt + 3e-7
for maximal least slack; round to 10 decimals. Floating; output candidate_base.json."""
import json, numpy as np
from decimal import Decimal as Dd, ROUND_HALF_EVEN
from scipy.optimize import minimize
best = json.load(open('s12_N512.json'))['best']; z = np.array(best['z']); n = 16; nt = 32
def rd(x, k): return str(Dd(repr(float(x))).quantize(Dd(1).scaleb(-k), rounding=ROUND_HALF_EVEN))
rc = [rd(t, 8) for t in z[9:9+nt]]; sc = [rd(t, 8) for t in z[9+nt:9+2*nt]]; kap, p, q = rd(z[6], 8), rd(z[7], 8), rd(z[8], 8)
N = 2048; x = 2*np.pi*np.arange(N)/N; j = np.arange(1, n+1); Bm = np.hstack([np.cos(np.outer(x, j)), np.sin(np.outer(x, j))]); pref = 2 + 2*np.cos(x)
r = Bm @ np.array(rc, float); s = Bm @ np.array(sc, float); kf, pf, qf = float(kap), float(p), float(q)
F, G = 2.0**r, 2.0**s; Zf, Zg = F.mean(), G.mean(); f, g = F/Zf, G/Zg
corr = lambda a, b: np.fft.ifft(np.fft.fft(a)*np.conj(np.fft.fft(b))).real/N
Q = corr(f, g); Bb = (corr(f*r, g) + corr(f, g*s))/Q - np.log2(Zf*Zg); L = np.log2(Q)
H = np.log2(np.mean(f**kf)*np.mean(g**kf)); u = L + (kf-1)*Bb - H; v = (2-kf)*Bb - 2*L + H
def h(x_): return -(x_*np.log2(x_) + (1-x_)*np.log2(1-x_))
ZETA = 1e-8
TAU = float(best['tau0']) + 3e-7
def margins(y, t=TAU):
    eta, mu, a, gm, l = y; r_ = 1 - mu - l; D = eta - t; Gm = 2*t - eta; aG = D/Gm
    rho_f = eta - 1.5e-6; rho_c = rho_f - 1e-6
    m1 = np.log2(np.mean(pref*2.0**(pf*(D - u)))); m2 = np.log2(np.mean(pref*2.0**(qf*(aG*v - u))))
    return np.array([h(2*a)/2 - gm, t - (l + (h(a) - gm)*mu), t - (r_ + (1 - gm)*mu), t - (1 - mu + (h(a) + h(.5 - a) - gm)*mu - eta),
                     t - (h(.5 - a)*mu + .5 - t), r_, t - r_, t - l, l - mu*(1 - 2*a), eta - mu/2*np.log2(3),
                     (eta - mu/2*np.log2(3))/2 - (.5 - t + ZETA), rho_c - m1, rho_c - m2, 30 - 3*pf, 30 - qf*(4*aG + 3)])
y0 = np.array([best['eta'], best['mu'], best['a'], best['gamma'], best['l']])
res = minimize(lambda w: -w[-1], np.append(y0, 0), method='SLSQP', constraints=[dict(type='ineq', fun=lambda w: margins(w[:5]) - w[-1])],
               options=dict(maxiter=1000, ftol=1e-16))
eta, mu, a, gm, l = [rd(t, 10) for t in res.x[:5]]
mf = margins([float(eta), float(mu), float(a), float(gm), float(l)])
names = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6 r>0', 'C6 r<tau0', 'C6 l<tau0', 'C7', 'C8', 'A5 delta', 'M1', 'M2', '3p', 'qcap']
cand = dict(construction='Base (a-kapila PROOF_0.4877, commit 44c34961) with ONE filter (J = 1)', tau0=rd(TAU, 10), eta=eta, mu=mu, a=a, gamma=gm, l=l,
            kappa=kap, p=p, q_m=q, n_terms=16, rc=rc, sc=sc, epsilon='0.00000001', zeta='0.00000001', input_guard_coefficient='100000000',
            rho_f_rule='eta - 1.5e-6', rho_c_rule='rho_f - 1e-6', certificate_format='rho0: z=(p,0); rho1..rho9: z=(q,0,0)',
            floating_margins=dict(zip(names, mf.tolist())), floating_T=float(TAU) + 2e-7)
json.dump(cand, open('candidate_base.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in cand.items() if k not in ('rc', 'sc')}, indent=1))
