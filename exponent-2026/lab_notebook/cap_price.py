"""C4: floor T vs moment capacity Delta_cap (floating, grid, optimistic closure; same budget as holder_floor.py)."""
import numpy as np, json
H4 = 2 - .75*np.log2(3)
def h2(x): return -x*np.log2(x)-(1-x)*np.log2(1-x)
def feasible(tau, K, Dm, n=20000):
    mu = np.linspace(1e-5, 1/K - 1e-9, n); dlo = np.maximum((.5-tau)/(K*mu), 0); dhi = 1 - H4 - (.5-tau)/mu
    eta_min = np.maximum(1 + (2*H4-1-(.5-dlo))*mu - tau, h2(mu) + mu)
    return bool(((dlo <= dhi) & (tau >= .25 + mu) & (eta_min - tau <= Dm)).any())
out = {}
for Dm in [.0281, .0288, .030, .032, .034, .036, .038, .0396, .0427]:
    best = (1, None)
    for K in range(1, 41):
        lo, hi = .40, .4999
        if not feasible(hi, K, Dm): continue
        for _ in range(40):
            mid = (lo+hi)/2; lo, hi = (lo, mid) if feasible(mid, K, Dm) else (mid, hi)
        best = min(best, (hi, K))
    out[Dm] = dict(floor=best[0], K=best[1])
    print(f'Delta_cap={Dm:.4f}: floor T ~ {best[0]:.6f} at K={best[1]}')
json.dump({str(k): v for k, v in out.items()}, open('cap_price.json', 'w'), indent=1)
