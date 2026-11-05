"""R5-A2b: exact integer check of the two k = 1 families with closed forms (two-valued; one repeated class + generics).
Inequality (R1): sum_c M_c^2 <= C(m-1,t-1) * t * s_t."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "round4"))
from math import comb as _comb
def comb(n, k): return _comb(n, k) if 0 <= k <= n else 0
from fractions import Fraction as Fr
from lay4 import Fast, qw, generic

o = open(os.path.join(HERE, "out", "k1_families.txt"), "w")
def P(*x):
    print(*x); print(*x, file=o); o.flush()

def two_valued(a, b, t):
    """returns (sum M^2, C t s) as integers"""
    m = a + b; jmax = min(a, t); jmin = max(0, t - b); s = jmax - jmin + 1
    M0 = sum(range(jmin, jmax + 1)); M1 = t * s - M0
    return M0 * M0 + M1 * M1, comb(m - 1, t - 1) * t * s

def zeros_generic(n, G, t):
    m = n + G; js = range(0, min(n, t) + 1)
    s = sum(comb(G, t - j) for j in js); M0 = sum(j * comb(G, t - j) for j in js)
    Ng = sum(comb(G - 1, t - 1 - j) for j in js)
    return M0 * M0 + G * Ng * Ng, comb(m - 1, t - 1) * t * s

P("== control: closed forms vs lay4.qw")
for w, t, kind, args in (([0] * 3 + [1] * 4, 2, "F1", (3, 4)), ([0] * 3 + [1] * 4, 3, "F1", (3, 4)), ([0] * 2 + [1] * 6, 4, "F1", (2, 6)),
                         ([0] * 3 + generic(4), 2, "F2", (3, 4)), ([0] * 3 + generic(4), 3, "F2", (3, 4)),
                         ([0] * 4 + generic(5), 3, "F2", (4, 5)), ([0] * 4 + generic(5), 4, "F2", (4, 5))):
    num, den = (two_valued if kind == "F1" else zeros_generic)(*args, t)
    P(f"   {kind} {args} t={t}: closed form Q = {Fr(num, den)} = {num/den:.12f}; lay4.qw = {qw(Fast(w), t, 1)[0]:.12f}")

P("== (F1) two-valued, a <= b, a + b <= 40, 2 <= t <= m/2")
viol = []; eq = []; n = 0
for m in range(4, 41):
    for a in range(1, m // 2 + 1):
        b = m - a
        for t in range(2, m // 2 + 1):
            num, den = two_valued(a, b, t); n += 1
            if num > den: viol.append((a, b, t, Fr(num, den)))
            elif num == den: eq.append((a, b, t))
P(f"   {n} cases: violations {viol[:5]} ({len(viol)}); equality cases {eq}")

P("== (F2) one class of n >= 2 plus G >= 1 generics, n + G <= 40, 2 <= t <= m/2")
viol = []; eq = []; n_ = 0; worst = {}
for m in range(4, 41):
    for n in range(2, m):
        G = m - n
        for t in range(2, m // 2 + 1):
            num, den = zeros_generic(n, G, t); n_ += 1
            if num > den: viol.append((n, G, t, Fr(num, den)))
            elif num == den: eq.append((n, G, t))
            r = Fr(num, den)
            if r > worst.get(m, (0, None))[0]: worst[m] = (r, (n, G, t))
P(f"   {n_} cases: violations {viol[:5]} ({len(viol)}); equality cases {eq}")
P("   per-m maximum of sum M^2 / (C t s): " + "; ".join(f"m={m}: {float(v[0]):.4f} at (n,G,t)={v[1]}" for m, v in sorted(worst.items()) if m <= 16 or m % 8 == 0))
o.close()
