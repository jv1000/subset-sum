r"""A1: test the induction ingredients for monotonicity a_k >= a_{k+1} (k+1 <= m/2):
 D_k(M) = (k+1) s_{k+1} - (m-k) s_k  (defect; monotonicity <=> D <= 0)
 identity: D_k(M) = D_k(M\e) - s_k + (k+1) n_e^{(k+1)} - (m-k-1) n_e^{(k)}   (checked exactly)
 core inequality (averaged):  (k+1) S_{k+1} <= m s_k + (m-k-1) S_k,  S_j = sum_e n_e^{(j)} = sum_x |C(x)|
 Lemma E (existence): some e has (k+1) n_e^{(k+1)} <= s_k + (m-k-1) n_e^{(k)}
 rules for e: max multiplicity class; min n_e^{(k+1)}; largest |value|; smallest |value|."""
import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layers import layer_data, classes
from math import comb
random.seed(2024)

def instance_families(m):
    F = [('equal', [1]*m), ('AP', list(range(1, m+1))), ('two-valued', [1]*(m//2) + [2]*(m - m//2)),
         ('+-AP', [((-1)**i)*(i//2+1) for i in range(m)]), ('pairs', [i//2+1 for i in range(m)]),
         ('three-equal+gen', [7]*3 + [10**3 * 3**i for i in range(m-3)]), ('0/1', [0]*(m//2) + [1]*(m-m//2)),
         ('1,1,2 blocks', [1, 1, 2]*(m//3) + [5]*(m - 3*(m//3))), ('two-valued 1:2', [1]*(m//3) + [2]*(m - m//3)),
         ('three-valued', [1]*(m//3) + [2]*(m//3) + [3]*(m - 2*(m//3))), ('squares', [i*i for i in range(1, m+1)]),
         ('+-equal', [1]*(m//2) + [-1]*(m - m//2)), ('sumset 1,2,4', [1, 2, 4]*(m//3) + [8]*(m - 3*(m//3)))]
    for R in (2, 3, 4, 6, 10, 30):
        for _ in range(25): F.append((f'rand[-{R}..{R}]', [random.randint(-R, R) for _ in range(m)]))
    for _ in range(15):
        z = random.randint(2, m-1); F.append(('eq+gen', [3]*z + [random.randint(10**4, 10**6) for _ in range(m-z)]))
    for _ in range(15):
        rk = random.randint(1, 3); g = [random.randint(100, 10**4) for _ in range(rk)]
        F.append((f'rank{rk}', [sum(random.randint(-1, 1)*gg for gg in g) for _ in range(m)]))
    return F

def check(w):
    ld = layer_data(w); m = ld['m']; s = ld['s']; core = ld['core']; vals, mult = ld['vals'], ld['mult']
    out = []
    for k in range(1, m//2):            # k+1 <= m/2
        D = (k+1)*s[k+1] - (m-k)*s[k]
        S_k = sum(core[k][i]*mult[i] for i in range(len(vals))); S_k1 = sum(core[k+1][i]*mult[i] for i in range(len(vals)))
        core_ineq = (k+1)*S_k1 <= m*s[k] + (m-k-1)*S_k
        good = [i for i in range(len(vals)) if (k+1)*core[k+1][i] <= s[k] + (m-k-1)*core[k][i]]
        rules = {
            'maxmult': max(range(len(vals)), key=lambda i: (mult[i], -abs(vals[i]))) in good,
            'minloss': min(range(len(vals)), key=lambda i: core[k+1][i]) in good,
            'maxabs': max(range(len(vals)), key=lambda i: abs(vals[i])) in good,
            'minabs': min(range(len(vals)), key=lambda i: abs(vals[i])) in good,
            'all': len(good) == len(vals)}
        # exact identity check on one e (class 0): D(M) = D(M\e) - s_k + (k+1) n_e^{k+1} - (m-k-1) n_e^{k}
        w2 = list(w); w2.remove(vals[0]); ld2 = layer_data(w2); s2 = ld2['s']
        D2 = (k+1)*s2[k+1] - (m-1-k)*s2[k]
        ident = (D == D2 - s[k] + (k+1)*core[k+1][0] - (m-k-1)*core[k][0])
        out.append(dict(k=k, D=D, core_ineq=core_ineq, exists=bool(good), rules=rules, ident=ident, ngood=len(good), nclasses=len(vals)))
    return out

stats = dict(tests=0, mono_viol=0, core_viol=0, E_viol=0, ident_fail=0, rule_fail={'maxmult': 0, 'minloss': 0, 'maxabs': 0, 'minabs': 0, 'all': 0})
worst = []
for m in range(6, 15):
    for name, w in instance_families(m):
        for row in check(w):
            stats['tests'] += 1
            if row['D'] > 0: stats['mono_viol'] += 1; worst.append(('MONO', name, w, row['k'], row['D']))
            if not row['core_ineq']: stats['core_viol'] += 1; worst.append(('CORE', name, w, row['k']))
            if not row['exists']: stats['E_viol'] += 1; worst.append(('E', name, w, row['k']))
            if not row['ident']: stats['ident_fail'] += 1
            for r_, ok in row['rules'].items():
                if not ok: stats['rule_fail'][r_] += 1
print(stats)
for x in worst[:20]: print('  ', x)
