"""C: counterexample hunt for layer-density monotonicity at m <= 22 with structured families (numpy, capped)."""
import numpy as np, math, time, random, sys
random.seed(2026); t0 = time.time(); CAP = 20 * 60
def ratios(w):
    m = len(w); s = np.zeros(1, np.int64); z = np.zeros(1, np.int8)
    for x in w:
        s = np.concatenate([s, s + np.int64(x)]); z = np.concatenate([z, z + 1])
    a = [len(np.unique(s[z == k])) / math.comb(m, k) for k in range(m // 2 + 1)]
    return min((a[k] / a[k + 1], k) for k in range(1, m // 2))
def families(m):
    F = [('two-valued', [1]*(m//2) + [2]*(m - m//2)), ('equal', [1]*m), ('AP', list(range(1, m+1))), ('AP gap2', list(range(1, 2*m, 2))),
         ('+-AP', [((-1)**i)*(i//2+1) for i in range(m)]), ('pairs', [i//2+1 for i in range(m)]), ('triples', [i//3+1 for i in range(m)]),
         ('three-valued', [1]*(m//3) + [2]*(m//3) + [3]*(m - 2*(m//3))), ('1,2,4 mix', [1,2,4]*(m//3) + [8]*(m - 3*(m//3))),
         ('+-equal', [1]*(m//2) + [-1]*(m - m//2)), ('+-two-valued', [1]*(m//4) + [-1]*(m//4) + [2]*(m//4) + [-2]*(m - 3*(m//4))),
         ('squares', [i*i for i in range(1, m+1)]), ('geometric 2 + equal', [2**i for i in range(m//2)] + [3]*(m - m//2)),
         ('sumset {1,2}+{0,3,6}', [1,2,4,5,7,8]*(m//6) + [1]*(m - 6*(m//6))), ('gadget 1,1,2 x', [1,1,2]*(m//3) + [1]*(m - 3*(m//3))),
         ('AP + copies', list(range(1, m//2 + 1)) + [m//4 + 1]*(m - m//2)), ('fib', [1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597,2584,4181,6765,10946,17711][:m])]
    for _ in range(8): F.append(('rand small', [random.randint(-3, 3) for _ in range(m)]))
    for _ in range(6):
        rk = random.randint(1, 3); g = [random.randint(10, 10**4) for _ in range(rk)]
        F.append((f'rank{rk}', [sum(random.randint(-1, 1)*gg for gg in g) for _ in range(m)]))
    for _ in range(4):
        base = [random.randint(1, 5) for _ in range(max(2, m//3))]; F.append(('sumset', base + [random.choice(base) + random.choice(base) for _ in range(m - len(base))]))
    for _ in range(3):
        z = random.randint(2, m-2); F.append(('equal+generic', [7]*z + [random.randint(10**5, 10**8) for _ in range(m-z)]))
    F.append(('generic control', [random.randint(10**6, 10**9) for _ in range(m)]))
    return F
worst = (1e9, None); n = 0
for m in range(16, 23):
    for name, w in families(m):
        if time.time() - t0 > CAP: print('time cap reached at m =', m); break
        r, k = ratios(w); n += 1
        if r < worst[0]: worst = (r, (m, name, k, sorted(w)[:12]))
        if r < 1 - 1e-12: print('VIOLATION', m, name, k, r, w, flush=True)
    print(f'm={m} done, {n} instances, min ratio so far {worst[0]:.6f} at {worst[1]}  [{time.time()-t0:.0f}s]', flush=True)
print('FINAL min a_k/a_(k+1) =', worst)
