"""R3-A6: adversarial hill-climb for (a) interior monotonicity violations, (b) middle-step violations, (c) large Q_w at
k <= m/4.  Values in [-R,R]; single-coordinate moves with random restarts; seeds include the m = 8 counterexample padded."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "round2"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from math import comb
from layers import layer_data
from lay3 import Layers
from cs_w import qw

def ratios(w):
    ld = layer_data(w); m = ld["m"]; s = ld["s"]; a = [s[j] / comb(m, j) for j in range(m + 1)]
    r_int = max((a[j + 1] / a[j] for j in range(1, m // 2 - 1)), default=0.0)   # j >= 1: a_1/a_0 = v/m is trivial
    r_mid = a[m // 2] / a[m // 2 - 1]
    return r_int, r_mid

def maxQw(w):
    L = Layers(w); m = L.m; best = 0.0
    for k in range(1, m // 4 + 1):
        for t in range(k + 1, m // 2 + 1):
            best = max(best, qw(L, t, k)[0])
    return best

def climb(obj, m, R, rng, seed=None, steps=400):
    w = list(seed) if seed is not None else rng.integers(-R, R + 1, size=m).tolist()
    cur = obj(w); best = (cur, list(w))
    for _ in range(steps):
        i = int(rng.integers(m)); old = w[i]
        w[i] = int(rng.integers(-R, R + 1)) if rng.random() < 0.5 else int(np.clip(old + rng.integers(-2, 3), -R, R))
        v = obj(w)
        if v >= cur: cur = v
        else: w[i] = old
        if cur > best[0]: best = (cur, list(w))
    return best

if __name__ == "__main__":
    o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "hill.txt"), "w")
    def P(*x):
        print(*x); print(*x, file=o); o.flush()
    rng = np.random.default_rng(17); t0 = time.time()
    seed8 = [-6, -5, -5, -3, -3, -2, 4, 5]
    P("control: seed ratios (r_int, r_mid) =", ratios(seed8), " expected r_mid = 96/95")
    for m in range(8, 14):
        R = 12 if m <= 10 else 8
        b_int = (0, None); b_mid = (0, None); tl = time.time(); restarts = 0
        while time.time() - tl < 45:
            seed = None
            if rng.random() < 0.5:
                seed = seed8 + rng.integers(-R, R + 1, size=m - 8).tolist() if m >= 8 else None
            r = climb(lambda w: ratios(w)[0], m, R, rng, seed, 300); restarts += 1
            if r[0] > b_int[0]: b_int = r
            r = climb(lambda w: ratios(w)[1], m, R, rng, seed, 300)
            if r[0] > b_mid[0]: b_mid = r
        P(f"m={m} R={R} restarts={restarts}: max r_int = {b_int[0]:.5f} w={b_int[1]};  max r_mid = {b_mid[0]:.5f} w={b_mid[1]}  [{time.time()-t0:.0f}s]")
    for m in (9, 10, 11):
        R = 8; bq = (0, None); tl = time.time(); restarts = 0
        while time.time() - tl < 60:
            seed = seed8 + rng.integers(-R, R + 1, size=m - 8).tolist() if rng.random() < 0.5 else None
            r = climb(maxQw, m, R, rng, seed, 60); restarts += 1
            if r[0] > bq[0]: bq = r
        P(f"m={m}: max Q_w (k<=m/4) by hill-climb = {bq[0]:.5f} w={bq[1]} restarts={restarts}  [{time.time()-t0:.0f}s]")
    o.close()
