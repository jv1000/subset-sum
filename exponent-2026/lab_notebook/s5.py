"""C5: full-constraint T minimization with general (cos+sin) densities. Floating. Usage: python3 -I s5.py K capfile"""
import json, sys, time
import numpy as np
from scipy.optimize import minimize
K = int(sys.argv[1]); cap = json.load(open(sys.argv[2])); zc = np.array(cap['best']['z'])
tag = cap['tag']; n = int(tag.split('_n')[1].split('_')[0]); sines = int(tag.split('_s')[1].split('_')[0]); nt = n * (2 if sines else 1)
H = 2 - .75*np.log2(3); EPS = 1e-8; C = .9999; G_ = 1e-5; N = 512
x = 2*np.pi*np.arange(N)/N; j = np.arange(1, n+1); B = np.cos(np.outer(x, j))
if sines: B = np.hstack([B, np.sin(np.outer(x, j))])
pref = 2 + 2*np.cos(x)
def h2(m): return -m*np.log2(m)-(1-m)*np.log2(1-m)
def moms(z):
    mu, eta, tau, gam = z[:4]; r, s = B @ z[4:4+nt], B @ z[4+nt:4+2*nt]; kap, p, q = z[4+2*nt:]
    F, G = 2.0**r, 2.0**s; Zf, Zg = F.mean(), G.mean(); f, g = F/Zf, G/Zg
    corr = lambda a, b: np.fft.ifft(np.fft.fft(a)*np.conj(np.fft.fft(b))).real/N
    Q = corr(f, g)
    if Q.min() <= 0: return np.array([9., 9.])
    Bb = (corr(f*r, g) + corr(f, g*s))/Q - np.log2(Zf*Zg); L = np.log2(Q)
    Hh = np.log2(np.mean(f**kap)*np.mean(g**kap)); u = L + (kap-1)*Bb - Hh; v = (2-kap)*Bb - 2*L + Hh
    D = eta - tau; a = D/(2*tau - eta)
    return np.log2([np.mean(pref*2.0**(p*(D-u))), np.mean(pref*2.0**(q*(a*v-u)))])
NAMES = ['list', 'pair', 'prelim', 'M1', 'M2', '3p<=30', 'qcap', 'Delta>0', 'Gamma>0', 'sparse', 'setup', 'prime', 'blocks']
def res(z):
    mu, eta, tau, gam = z[:4]; p, q = z[-2], z[-1]; a = (eta-tau)/(2*tau-eta); m = moms(z)
    return np.array([tau-(.5+(H-.5-gam)*mu), tau-(1+(2*H-1-gam)*mu-eta+G_), tau-(.5-C*K*mu*(.5-gam)), eta-m[0]-3e-6, eta-m[1]-3e-6,
                     30-3*p, 30-q*(4*a+3), eta-tau, 2*tau-eta, eta-h2(mu)-mu-G_, tau-.25-mu, tau-eta/2, 1-K*mu])
TAU0 = .4898
z0 = np.concatenate([[.97/K if K < 17 else .0574, TAU0 + zc[-1], TAU0, .4895], zc[:2*nt], zc[2*nt:2*nt+3]])
bnd = [(.02, 1/K), (.50, .60), (.47, .495), (.44, .499)] + [(-4, 4)]*(2*nt) + [(.5, 2), (1, 10), (1, 9.99)]
t0 = time.time()
r = minimize(lambda z: z[2], z0, method='SLSQP', bounds=bnd, constraints=[dict(type='ineq', fun=res)], options=dict(maxiter=1500, ftol=1e-13))
rr = res(r.x)
out = dict(K=K, cap_source=tag, T=float(r.x[2]+20*EPS), min_res=float(rr.min()), residuals=dict(zip(NAMES, rr.tolist())),
           mu=float(r.x[0]), eta=float(r.x[1]), tau=float(r.x[2]), gamma=float(r.x[3]), kappa=float(r.x[-3]), p=float(r.x[-2]), q=float(r.x[-1]),
           z=r.x.tolist(), msg=str(r.message), sec=time.time()-t0)
json.dump(out, open(f's5_K{K}_{tag}.json', 'w'), indent=1)
print(f"K={K} [{tag}] T={out['T']:.7f} min_res={out['min_res']:.1e} mu={out['mu']:.5f} Delta={out['eta']-out['tau']:.5f} "
      f"active={[k for k,v in out['residuals'].items() if v<1e-7]} {out['msg'][:30]} [{out['sec']:.0f}s]")
