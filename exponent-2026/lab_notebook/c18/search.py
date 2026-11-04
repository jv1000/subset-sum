import numpy as np, math, sys, json
exec(open('gadget.py').read().split("alphas = [")[0])
alpha = float(sys.argv[1]); B = int(sys.argv[2]); iters = int(sys.argv[3]); seed = int(sys.argv[4])
rng = np.random.default_rng(seed)
best_all = (1e9, None)
for restart in range(12):
    b = int(rng.integers(2, B + 1)); w = list(rng.integers(-6, 7, b))
    cur = R(w, alpha)
    for it in range(iters):
        w2 = list(w); i = int(rng.integers(b)); mv = rng.integers(4)
        if mv == 0: w2[i] = int(rng.integers(-8, 9))
        elif mv == 1: w2[i] = w2[int(rng.integers(b))]
        elif mv == 2: w2[i] = -w2[int(rng.integers(b))]
        else: w2[i] = w2[int(rng.integers(b))] + w2[int(rng.integers(b))]
        r2 = R(w2, alpha)
        if r2 <= cur: w, cur = w2, r2
    if cur < best_all[0]: best_all = (cur, w)
    print(f'restart {restart}: b={len(w)} R/m={cur:+.5f} w={w}', flush=True)
print(f'MIN over search at alpha={alpha}: R/m = {best_all[0]:+.6f}  w={best_all[1]}')
