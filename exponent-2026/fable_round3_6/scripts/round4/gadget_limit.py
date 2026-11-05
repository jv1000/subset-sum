"""R4-A4: gadget-product limits for the A5 worst cases (no scipy: own 2-D convex dual minimiser).
M = q generic-separated copies of a block B (b elements); k = alpha*m, t = tau*m.  With V = Sigma(B), lo(x)/hi(x) the
least/greatest layer of B containing x (layer sets assumed intervals; checked and reported),
  log2 s_k / m -> H*(alpha b)/b,   H*(A) = max{ H(pi) : pi on V, E_pi lo <= A <= E_pi hi }   (bits),
  R/m   = lim (log2 a_k + d)/m = H*(alpha b)/b - h(alpha) + 1 - log2|V|/b          (Lemma-R quantity, handoff s.3),
  E(alpha,tau) = lim (log2 a_t - log2 a_k)/m = [H*(tau b)/b - h(tau)] - [H*(alpha b)/b - h(alpha)]   (M' exponent).
Exact check: q = 2, 3 copies by brute force (m <= 18): a_t/a_k and Q_w."""
import sys, os, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from math import comb, log2
from lay4 import Fast, qw, product, all_sums

def h(a): return 0.0 if a <= 0 or a >= 1 else -(a * log2(a) + (1 - a) * log2(1 - a))

def block_data(w):
    sums, sizes = all_sums(w); lo = {}; hi = {}; layers = {}
    for s, c in zip(sums.tolist(), sizes.tolist()):
        lo[s] = min(lo.get(s, 99), c); hi[s] = max(hi.get(s, -1), c); layers.setdefault(s, set()).add(c)
    nonint = sum(1 for s in layers if len(layers[s]) != hi[s] - lo[s] + 1)
    vals = sorted(lo)
    return np.array([lo[v] for v in vals], float), np.array([hi[v] for v in vals], float), len(vals), nonint

def golden(f, a, b, it=90):
    g = (math.sqrt(5) - 1) / 2; c = b - g * (b - a); d = a + g * (b - a); fc, fd = f(c), f(d)
    for _ in range(it):
        if fc < fd: b, d, fd = d, c, fc; c = b - g * (b - a); fc = f(c)
        else: a, c, fc = c, d, fd; d = a + g * (b - a); fd = f(d)
    return (a + b) / 2, min(fc, fd)

def maxent_bits(lo, hi, A, LMAX=80.0):
    """H*(A) in bits: min over l1,l2 >= 0 of log sum exp(-l1 lo + l2 hi) + (l1 - l2) A (convex dual; strong duality)."""
    def g(l1, l2):
        e = -l1 * lo + l2 * hi; M = e.max(); return M + math.log(np.exp(e - M).sum()) + (l1 - l2) * A
    if lo.mean() <= A <= hi.mean(): return log2(len(lo))        # uniform law is feasible -> unconstrained max
    _, v = golden(lambda l1: golden(lambda l2: g(l1, l2), 0.0, LMAX)[1], 0.0, LMAX)
    return v / math.log(2)

def limits(w, alphas, taus):
    lo, hi, C, nonint = block_data(w); b = len(w)
    dm = 1 - log2(C) / b
    la = {a: maxent_bits(lo, hi, a * b) / b - h(a) for a in sorted(set(alphas) | set(taus))}   # lim log2 a_{alpha m}/m
    R = {a: la[a] + dm for a in alphas}
    E = {(a, t): la[t] - la[a] for a in alphas for t in taus if t >= a}
    return R, E, nonint, C

BLOCKS = {
    "generic b=6 (control)": [1, 2, 4, 8, 16, 32],
    "all-equal b=6 (control)": [1] * 6,
    "A5 m=6 worst (2,3)": [-3, -3, -2, -2, 0, 0],
    "A5 m=8 worst (3,4)": [-3, -3, -3, -2, -2, -2, 1, 1],
    "A0 m=10 worst (4,5)": [-3, -3, -3, -2, -2, -2, -2, 2, 2, 2],
    "A0 m=6 [-5,5] worst (a_3=a_2)": [-5, -4, -2, -1, 3, 4],
    "m=8 counterexample 1": [-6, -5, -5, -3, -3, -2, 4, 5],
    "m=8 counterexample 2": [-8, -6, -6, -2, -2, 0, 1, 3],
    "m=7 counterexample": [-6, -5, -2, -1, 0, 3, 4],
    "zeros+generic 0^5 g^3": [0, 0, 0, 0, 0, 16, 32, 64],
    "two-valued 0^4 1^4": [0, 0, 0, 0, 1, 1, 1, 1],
    "two-valued 0^2 1^6": [0, 0, 1, 1, 1, 1, 1, 1],
}

if __name__ == "__main__":
    o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "gadget_limit.txt"), "w")
    def P(*x):
        print(*x); print(*x, file=o); o.flush()
    t0 = time.time()
    alphas = [0.0074, 0.02, 0.05, 0.1, 0.2, 0.25]; taus = [0.0074, 0.02, 0.05, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    P("R/m = lim (log2 a_k + d)/m  (need >= 0);   E(alpha,tau) = lim (log2 a_t - log2 a_k)/m  (need <= 0 for tau in [alpha, 1/2])")
    P("alphas:", alphas, " taus:", taus)
    for name, w in BLOCKS.items():
        R, E, nonint, C = limits(w, alphas, taus)
        P(f"\n{name}: w={w}  |Sigma(B)|={C}  non-interval layer sets: {nonint}")
        P("  R/m   :", " ".join(f"{R[a]:+.4f}" for a in alphas), "  min =", f"{min(R.values()):+.4f}")
        for a in alphas:
            row = [E[(a, t)] for t in taus if t >= a]
            P(f"  E(a={a:<6}): " + " ".join(f"{x:+.4f}" for x in row) + f"   max = {max(row):+.4f}")
    P(f"\n[{time.time()-t0:.0f}s] exact products (q copies, brute force): a_t/a_k and Q_w at the scaled (k,t) and at k <= m/4")
    for name, w in (("A5 m=6 worst", [-3, -3, -2, -2, 0, 0]), ("A5 m=8 worst", [-3, -3, -3, -2, -2, -2, 1, 1]),
                    ("m=8 counterexample 1", [-6, -5, -5, -3, -3, -2, 4, 5]), ("zeros+generic 0^5 g^3", [0, 0, 0, 0, 0, 16, 32, 64]),
                    ("A0 m=10 worst", [-3, -3, -3, -2, -2, -2, -2, 2, 2, 2])):
        b = len(w)
        for q in (1, 2, 3):
            m = b * q
            if m > 20: continue
            W = product([w] * q); F = Fast(W); rows = []
            for k in range(1, m // 2):
                for t in range(k + 1, m // 2 + 1):
                    if not (k <= m // 4 or (k, t) in {(2 * q, 3 * q), (3 * q, 4 * q), (4 * q, 5 * q)}): continue
                    if m >= 18 and k > m // 4 and t < m // 2: continue
                    r = F.a(t) / F.a(k)
                    Q = qw(F, t, k)[0] if (m <= 16 or (k, t) in {(2 * q, 3 * q), (3 * q, 4 * q), (4 * q, 5 * q)} or t == m // 2) else float("nan")
                    rows.append((k, t, r, Q))
            worst_r = max(rows, key=lambda x: x[2]); worst_Q = max((x for x in rows if x[3] == x[3]), key=lambda x: x[3])
            P(f"{name} q={q} m={m}: max a_t/a_k = {worst_r[2]:.4f} at (k,t)=({worst_r[0]},{worst_r[1]}); max Q_w = {worst_Q[3]:.4f} at ({worst_Q[0]},{worst_Q[1]}); "
              + "; ".join(f"({k},{t}) r={r:.3f} Q={Q:.3f}" for k, t, r, Q in rows if (k, t) in {(2 * q, 3 * q), (3 * q, 4 * q), (4 * q, 5 * q)} or k == m // 4)
              + f"  [{time.time()-t0:.0f}s]")
    o.close()
