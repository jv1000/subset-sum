import sys, itertools, random, time
from math import comb
from fractions import Fraction

def layers(ws):
    """For each mask of ws, return (list of layer bitsets cnt per j, total union count).
    Aggregates: A[s][j] = sum over |S|=s of |Sigma_j(S)|; B[v]=sum over |V|=v of |Sigma(V)|;
    also per-mask data for diagnostics."""
    n = len(ws)
    mn = min(0, min(ws))
    off = -n * mn
    N = 1 << n
    L = [None] * N
    L[0] = [1 << off]
    for mask in range(1, N):
        low = mask & -mask
        i = low.bit_length() - 1
        prev = L[mask ^ low]
        w = ws[i]
        m = len(prev)  # popcount(prev)+1
        new = [0] * (m + 1)
        for j in range(m + 1):
            x = prev[j] if j < m else 0
            if j > 0:
                y = prev[j - 1]
                y = (y << w) if w >= 0 else (y >> (-w))
                x |= y
            new[j] = x
        L[mask] = new
    return L

def stats(ws, L):
    n = len(ws)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    B = [0] * (n + 1)
    per = []
    for mask in range(1 << n):
        lay = L[mask]
        s = len(lay) - 1
        cnts = [b.bit_count() for b in lay]
        u = 0
        for b in lay:
            u |= b
        tot = u.bit_count()
        for j in range(s + 1):
            A[s][j] += cnts[j]
        B[s] += tot
        per.append((mask, s, cnts, tot))
    return A, B, per

def params(n, require_product=None):
    out = []
    for v in range(0, n + 1):
        for sig in range(0, v + 1):
            for k in range(0, sig // 2 + 1):
                if not (2 * k <= sig and 2 * sig <= v + 2 * k and v <= n):
                    continue
                prod_ok = comb(sig, k) * comb(v, k) <= 2 ** v
                if require_product is None or prod_ok == require_product:
                    out.append((k, sig, v, prod_ok))
    return out

def check_instance(ws, L=None):
    n = len(ws)
    if L is None:
        L = layers(ws)
    A, B, per = stats(ws, L)
    res = []
    for (k, sig, v, pok) in params(n):
        lhs = Fraction(A[sig][k], comb(n, sig) * comb(sig, k))
        rhs = Fraction(B[v], comb(n, v) * (2 ** v) * (v + 1))
        res.append((k, sig, v, pok, lhs, rhs))
    return res, per
