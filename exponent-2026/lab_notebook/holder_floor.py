"""C3-H: floating exploration of the Holder/Jensen M1 bound combined with the scalar budget (any K). NOT rigorous.
M1 bound (proved, see NOTE): log2 M1 >= 1 + p Delta + g(p), g(p) = (1+p) log2 E[w^{1/(1+p)}], w = 1+cos x.
With eta = tau + Delta and M1 < 2^eta needed: Delta <= Dmax(tau) = max_{1<p<=10} (tau - 1 - g(p))/(p-1).
Budget closure: strict -> non-strict, eps = guard = 0, coverage c = 1 (optimistic), gamma = .5 - d."""
import numpy as np, json
from scipy.special import gammaln
H4 = 2 - .75*np.log2(3)
P = np.linspace(1.0001, 10, 200000)
def Ew_beta(b): return np.exp(b*np.log(2) + gammaln(b+.5) - .5*np.log(np.pi) - gammaln(b+1))
G = (1+P)*np.log2(Ew_beta(1/(1+P)))
def Dmax(tau): return float(np.max((tau - 1 - G)/(P - 1)))
def h2(x): return -x*np.log2(x)-(1-x)*np.log2(1-x)
out = {}
out['min_p_Phi_at_K8_point'] = float(np.min(1 + P*.1900002 + G))
out['argmin_p'] = float(P[np.argmin(1 + P*.1900002 + G)])
out['Dmax'] = {str(t): Dmax(t) for t in [.48, .485, .4877, .489, .4895, .48977, .49]}
out['astra_point_Delta'] = .51787037 - .4897734
def feasible(tau, K, n=20000):
    Dm = Dmax(tau)
    mu = np.linspace(1e-5, 1/K, n)
    dlo = np.maximum((.5-tau)/(K*mu), 0); dhi = 1 - H4 - (.5-tau)/mu
    ok = (dlo <= dhi) & (tau >= .25 + mu)
    gam = .5 - dlo
    eta_min = np.maximum(1 + (2*H4-1-gam)*mu - tau, h2(mu) + mu)
    ok &= (eta_min - tau <= Dm)
    return bool(ok.any())
fl = {}
for K in range(1, 41):
    lo, hi = .40, .4999
    if not feasible(hi, K): fl[K] = None; continue
    for _ in range(45):
        mid = (lo+hi)/2
        lo, hi = (lo, mid) if feasible(mid, K) else (mid, hi)
    fl[K] = hi
out['floor_by_K'] = fl
best = min((v, k) for k, v in fl.items() if v)
out['best'] = dict(K=best[1], floor=best[0])
# same budget WITHOUT the M1 bound (Astra's two-bound style floor, for comparison)
def feas_noM1(tau, K, n=20000):
    mu = np.linspace(1e-5, 1/K, n); dlo = np.maximum((.5-tau)/(K*mu), 0); dhi = 1 - H4 - (.5-tau)/mu
    return bool(((dlo <= dhi) & (tau >= .25 + mu)).any())
nm = {}
for K in [8, 17]:
    lo, hi = .40, .4999
    for _ in range(45):
        mid = (lo+hi)/2; lo, hi = (lo, mid) if feas_noM1(mid, K) else (mid, hi)
    nm[K] = hi
out['floor_without_M1_bound'] = nm
json.dump(out, open('holder_floor.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'floor_by_K'}, indent=1))
print({k: (round(v, 6) if v else None) for k, v in fl.items()})
