"""Task 3 pricing: the fixed-Delta alias-budget model of round 1 (scripts/section9_check.py, verified against Base's
C1-C8 there) with the floor premise removed or modified, one design at a time.
  c2 = l + (h(a)-gamma) mu ; c3 = r + (1-gamma) mu ; c4 = (1 - Delta + overhead)/2 ; c5 = (1/2 + mu h(1/2-a))/2
  overhead = mu((h(a)-gamma) + (h(1/2-a) - 1)) ; gamma = h(2a)/2 (C1 tight) ; l balances c2 = c3 (or C7 floor).
Floor: c4 >= (1-Delta)/2 when the overhead is 0 (one dictionary operation per alias class, modulus eta = tau0 + Delta).
"""
import numpy as np
hf = lambda x: -(x * np.log2(x) + (1 - x) * np.log2(1 - x))
D0 = 0.0286969377          # Delta of the certified Section 8 point
DT = 0.0286568627          # Delta of the ternary point (eta - tau0 = 0.5159974155 - 0.4873405528)

def model(mu, a, Delta, mode="base", share=1.0, eta_shift=0.0, extra=0.0):
    ha = hf(a); gam = hf(2 * a) / 2; h2 = hf(0.5 - a)
    l = np.maximum((1 - ha * mu) / 2, mu * (1 - 2 * a) + 1e-12)
    c2 = l + (ha - gam) * mu + extra
    c3 = (1 - mu - l) + (1 - gam) * mu + extra
    over = mu * ((ha - gam) + (h2 - 1))
    c5 = (0.5 + mu * h2) / 2 + extra
    if mode == "base":        c4 = (1 - Delta + (1 - share) * over) / 2
    elif mode == "no_c4":     c4 = 0 * mu                       # floor premise removed: no per-class operation
    elif mode == "half_c4":   c4 = (1 - Delta + over) / 4       # sqrt aggregation: 2^{(1-eta)n/2} operations
    elif mode == "coarse":    c4 = (1 - Delta + over) / 2 + eta_shift / 2   # matching at modulus eta - eta_shift
    t = np.maximum.reduce([c2, c3, c4, c5])
    bad = (1 - mu - l <= 0) | (l >= t) | (mu >= t) | (a >= 0.25)
    return np.where(bad, np.inf, t), c2, c3, c4, c5, l

def optimize(Delta, **kw):
    mus = np.linspace(0.20, 0.49, 1451); aas = np.linspace(0.0005, 0.08, 1591)
    MU, AA = np.meshgrid(mus, aas, indexing="ij")
    t = model(MU, AA, Delta, **kw)[0]
    best = None
    for o in np.argsort(t, axis=None)[:20]:
        i, j = np.unravel_index(o, t.shape); mu_c, a_c = mus[i], aas[j]; dm, da = 2 * (mus[1] - mus[0]), 2 * (aas[1] - aas[0])
        for _ in range(10):
            m_ = np.linspace(mu_c - dm, mu_c + dm, 61); a_ = np.linspace(max(a_c - da, 1e-5), a_c + da, 61)
            M_, A_ = np.meshgrid(m_, a_, indexing="ij"); tt = model(M_, A_, Delta, **kw)[0]
            ii, jj = np.unravel_index(np.argmin(tt), tt.shape); mu_c, a_c = m_[ii], a_[jj]; dm /= 8; da /= 8
        c = (float(tt[ii, jj]), float(mu_c), float(a_c))
        if best is None or c[0] < best[0]: best = c
    t, c2, c3, c4, c5, l = model(best[1], best[2], Delta, **kw)
    return dict(tau0=best[0], mu=best[1], a=best[2], c2=float(c2), c3=float(c3), c4=float(c4), c5=float(c5), l=float(l))

if __name__ == "__main__":
    import os
    out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "floor_designs.txt"), "w")
    def P(*x):
        print(*x); print(*x, file=out); out.flush()
    P("control (round-1 model): base, share 0 at Delta of the certified point ->", optimize(D0, mode="base", share=0.0), " (round 1: 0.4875741)")
    P("floor (share 1, overhead removed) ->", optimize(D0, mode="base", share=1.0), f" (1-Delta)/2 = {(1-D0)/2:.7f}")
    P("D1/D4 ceiling: no per-class operation at all (c4 dropped; C2/C3/C5 + list sizes remain) ->", optimize(D0, mode="no_c4"))
    P("D3 sqrt-aggregation (2^{(1-eta)n/2} operations, if group phase sums were free) ->", optimize(D0, mode="half_c4"))
    for sh in (0.005, 0.01, 0.02):
        P(f"D3 coarse matching at modulus eta - {sh}: ->", optimize(D0, mode="coarse", eta_shift=sh)["tau0"], "(worse by shift/2, as expected)")
    for Dm in (0.030, 0.035, 0.0415):
        P(f"D2 estimator with capacity Delta = {Dm} (Lemma-1 cap at tau=0.485 is 0.0415): base share 0 ->", optimize(Dm, mode='base', share=0.0)["tau0"], " floor (1-Delta)/2 =", round((1 - Dm) / 2, 6))
    # what the ternary step (round 2) does in this model: it reduces the C4 overhead; the model's share for it
    P("reference: ternary certified point tau0 = 0.4873405528; Section 8 point 0.4875752036; floor at D0:", round((1 - D0) / 2, 7))
    # Delta needed for 0.485 at full overhead removal and at the no_c4 ceiling
    for target in (0.485, 0.4845):
        P(f"Delta needed for tau0 = {target} at the floor: {1 - 2 * target:.4f}")
    out.close()
