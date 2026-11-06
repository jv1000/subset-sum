"""R5-A3b: palette-only hill-climb (g generic entries fixed, other coordinates in [-3,6]) at m = 18, 20 for large Q_w in the window k < m/3.  Climb objective: the pairs (k, k+1) with the
two largest allowed k (cheap); the full window pair list is evaluated for the top instances at the end.  Moves: one
coordinate -> palette value in [-3,6] or a fresh generic value (10^6 * 3^i, i < 20, so no int64 overflow).
Control: the same climber on the pair (m/2-1, m/2) must find Q_w > 1."""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "round4"))
import numpy as np
from lay4 import Fast, qw

o = open(os.path.join(HERE, "out", "hill5b.txt"), "w")
def P(*x):
    print(*x); print(*x, file=o); o.flush()
t0 = time.time()
GEN = [10 ** 6 * 3 ** i for i in range(20)]
PALETTE = list(range(-3, 7))
CLIMB = {18: [(4, 5), (5, 6)], 20: [(5, 6), (6, 7)]}
FULL = {18: [(4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (5, 6), (5, 7), (5, 8), (5, 9)], 20: [(5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (6, 7), (6, 8), (6, 9), (6, 10)]}
CTRL = {18: [(8, 9)], 20: [(9, 10)]}

def obj(w, pairs):
    F = Fast(w); best = (-1.0, None)
    for k, t in pairs:
        q = qw(F, t, k)[0]
        if q > best[0]: best = (q, (k, t))
    return best

def fmt(w):
    small = sorted(v for v in w if abs(v) < 10 ** 5); g = sum(1 for v in w if abs(v) >= 10 ** 5)
    return f"{tuple(small)}+{g}g"

def climb(w0, pairs, rng, steps, tend, g=0):
    m = len(w0); w = list(w0); cur, cp = obj(w, pairs); best = (cur, cp, list(w)); evals = 1
    for _ in range(steps):
        if time.time() > tend: break
        i = int(rng.integers(m - g)); old = w[i]
        w[i] = int(rng.choice(PALETTE))
        if w[i] == old: continue
        v, vp = obj(w, pairs); evals += 1
        if v >= cur: cur, cp = v, vp
        else: w[i] = old
        if cur > best[0]: best = (cur, cp, list(w))
    return best, evals

def seeds(m, rng, g):
    out = []
    for _ in range(8):
        rest = m - g; a = int(rng.integers(2, rest - 3)); b = int(rng.integers(2, rest - a - 1)); c = rest - a - b
        out.append([0] * a + [1] * b + [5] * c + GEN[:g])
    out.append([0] * ((m - g) // 2) + [1] * (m - g - (m - g) // 2) + GEN[:g])
    out.append([0] * 6 + [1] * 4 + [5] * (m - 10 - g) + GEN[:g])
    return out

def rand_start(m, g, rng): return [int(v) for v in rng.choice(PALETTE, size=m - g)] + GEN[:g]

rng = np.random.default_rng(32)
for m in (18, 20):
    g = 4; sd = seeds(m, rng, g)
    P(f"== control m={m} g={g}: climber on the pair {CTRL[m]} (must exceed 1), cap 60 s")
    tend = time.time() + 60; bestc = (0, None, None); restarts = 0
    while time.time() < tend:
        w0 = sd[restarts % len(sd)] if restarts % 2 == 0 else rand_start(m, g, rng)
        b, ev = climb(w0, CTRL[m], rng, 40, tend, g); restarts += 1
        if b[0] > bestc[0]: bestc = b
        if bestc[0] > 1: break
    P(f"   control result: max Q_w = {bestc[0]:.4f} at {bestc[1]} w={fmt(bestc[2])} after {restarts} restarts [{time.time()-t0:.0f}s]")
    for g in (0, 4):
        sd = seeds(m, rng, g)
        P(f"== m={m} g={g}: window climb on {CLIMB[m]}, cap 210 s")
        tend = time.time() + 210; found = []; restarts = 0; evals = 0
        while time.time() < tend:
            w0 = sd[restarts % len(sd)] if restarts % 2 == 0 else rand_start(m, g, rng)
            b, ev = climb(w0, CLIMB[m], rng, 60, tend, g); restarts += 1; evals += ev
            found.append(b)
        found.sort(key=lambda b: -b[0])
        P(f"   {restarts} restarts, {evals} evaluations; best climb values: " + ", ".join(f"{b[0]:.4f}@{b[1]}" for b in found[:5]))
        P(f"   full window evaluation of the top 3 instances (pairs {FULL[m]}):")
        for b in found[:3]:
            F = Fast(b[2]); vals = [(k, t, qw(F, t, k)[0]) for k, t in FULL[m]]
            mx = max(vals, key=lambda v: v[2])
            P(f"     w={fmt(b[2])}: max {mx[2]:.4f} at ({mx[0]},{mx[1]}); " + " ".join(f"({k},{t})={q:.3f}" for k, t, q in vals) + f"  {'VIOL' if mx[2] > 1 else ''}")
        P(f"   [{time.time()-t0:.0f}s]")
P(f"total [{time.time()-t0:.0f}s]"); o.close()
