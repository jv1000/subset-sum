r"""A2: evidence for Defect Monotonicity (DM): Phi_e(M,k) := D_k(M) - D_k(M\e) = (k+1) n_e^{k+1} - (m-k-1) n_e^{k} - s_k <= 0.
Reports max Phi_e over all e, all k (separately for k+1 <= m/2 and beyond), structured + random families, and a
hill-climbing adversary maximizing max_e Phi_e at k+1 <= m/2.  m <= 16 (classes DP)."""
import sys, os, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layers import layer_data
random.seed(99)
t0 = time.time()

def phis(w):
    ld = layer_data(w); m = ld['m']; s = ld['s']; core = ld['core']; r = len(ld['vals'])
    res = {}
    for k in range(1, m - 1):
        res[k] = max((k+1)*core[k+1][i] - (m-k-1)*core[k][i] - s[k] for i in range(r))
    return res, m


def families(m):
    F = [('equal', [1]*m), ('AP', list(range(1, m+1))), ('two-valued', [1]*(m//2) + [2]*(m - m//2)),
         ('+-AP', [((-1)**i)*(i//2+1) for i in range(m)]), ('pairs', [i//2+1 for i in range(m)]),
         ('three-equal+gen', [7]*3 + [10**3 * 3**i for i in range(m-3)]), ('0/1', [0]*(m//2) + [1]*(m-m//2)),
         ('1,1,2', [1, 1, 2]*(m//3) + [5]*(m - 3*(m//3))), ('two-valued 1:2', [1]*(m//3) + [2]*(m - m//3)),
         ('three-valued', [1]*(m//3) + [2]*(m//3) + [3]*(m - 2*(m//3))), ('squares', [i*i for i in range(1, m+1)]),
         ('+-equal', [1]*(m//2) + [-1]*(m - m//2)), ('1,2,4', [1, 2, 4]*(m//3) + [8]*(m - 3*(m//3))),
         ('fib', [1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987][:m]), ('2 copies each', [i//2 + 1 for i in range(m)]),
         ('geometric 3', [3**i for i in range(m)]), ('1,2,3 + sums', [1,2,3,3,4,5,5,6,7,8,8,9,10,11,12,13][:m])]
    for R in (2, 3, 5, 8, 20):
        for _ in range(30): F.append((f'rand[-{R}..{R}]', [random.randint(-R, R) for _ in range(m)]))
    for _ in range(20):
        z = random.randint(2, m-1); F.append(('eq+gen', [3]*z + [random.randint(10**4, 10**6) for _ in range(m-z)]))
    for _ in range(20):
        rk = random.randint(1, 3); g = [random.randint(100, 10**4) for _ in range(rk)]
        F.append((f'rank{rk}', [sum(random.randint(-1, 1)*gg for gg in g) for _ in range(m)]))
    for _ in range(10):
        base = [random.randint(1, 6) for _ in range(m//2)]; F.append(('sumset', base + [random.choice(base) + random.choice(base) for _ in range(m - m//2)]))
    return F

stats = dict(tests_in=0, viol_in=0, tests_out=0, viol_out=0, max_in=-10**9, max_out=-10**9)
worst_in = None
for m in range(6, 17):
    for name, w in families(m):
        res, mm = phis(w)
        for k, ph in res.items():
            if k + 1 <= m / 2:
                stats['tests_in'] += 1
                if ph > 0: stats['viol_in'] += 1
                if ph > stats['max_in']: stats['max_in'] = ph; worst_in = (name, w, k, ph)
            else:
                stats['tests_out'] += 1
                if ph > 0: stats['viol_out'] += 1
                stats['max_out'] = max(stats['max_out'], ph)
print('families:', stats, 'worst in-range:', worst_in, f'[{time.time()-t0:.0f}s]', flush=True)

# hill-climb adversary: maximize max_e Phi_e over k+1 <= m/2
best = (-10**9, None)
for m in (10, 12, 14):
    for restart in range(12):
        R = random.choice([2, 3, 5, 10, 100])
        w = [random.randint(-R, R) for _ in range(m)]
        def score(w):
            res, _ = phis(w); return max(ph for k, ph in res.items() if k + 1 <= m / 2)
        cur = score(w)
        for step in range(150):
            w2 = list(w); i = random.randrange(m)
            mv = random.random()
            if mv < 0.3: w2[i] = random.randint(-R, R)
            elif mv < 0.6: w2[i] = w2[random.randrange(m)]
            elif mv < 0.8: w2[i] = w2[random.randrange(m)] + w2[random.randrange(m)]
            else: w2[i] = -w2[random.randrange(m)]
            v = score(w2)
            if v >= cur: w, cur = w2, v
        if cur > best[0]: best = (cur, (m, sorted(w)))
    print(f'hill-climb m={m}: best max Phi so far = {best[0]} at {best[1]}  [{time.time()-t0:.0f}s]', flush=True)
print('DM violated by adversary?', best[0] > 0)
