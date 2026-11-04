r"""A6: list every DM violation and every reported monotonicity violation in the exhaustive [-6,6], m<=9 range,
verify each by brute force (itertools), and test the surviving induction forms exhaustively:
  (core)  (k+1) S_{k+1} <= m s_k + (m-k-1) S_k   (averaged DM, S_j = sum_x |C_j(x)|)
  (E)     exists e with Phi_e <= 0
on [-6,6] m<=9 and [-3,3] m<=12."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dm_exhaustive import dm_check, multisets
from layers import layer_data
from math import comb
t0 = time.time()

def brute(w):
    m = len(w); s = []; cores = []
    for j in range(m+1):
        wit = {}
        for A in itertools.combinations(range(m), j): wit.setdefault(sum(w[i] for i in A), []).append(set(A))
        s.append(len(wit)); cores.append({x: set.intersection(*W) for x, W in wit.items()})
    return s, cores

def forms(vals, mult):
    ld = layer_data([v for v, n in zip(vals, mult) for _ in range(n)])
    s, core, m = ld['s'], ld['core'], ld['m']; r = len(vals)
    out = []
    for k in range(1, m//2):
        S_k = sum(core[k][i]*mult[i] for i in range(r)); S_k1 = sum(core[k+1][i]*mult[i] for i in range(r))
        phis = [(k+1)*core[k+1][i] - (m-k-1)*core[k][i] - s[k] for i in range(r)]
        out.append(dict(k=k, mono=(k+1)*s[k+1] <= (m-k)*s[k], core=(k+1)*S_k1 <= m*s[k] + (m-k-1)*S_k,
                        E=min(phis) <= 0, dm=max(phis) <= 0, maxphi=max(phis), avgphi=sum(p*n for p, n in zip(phis, mult))/m))
    return out

def sweep(label, values, mrange):
    cnt = dict(inst=0, mono=0, core=0, E=0, dm=0); dm_ex = []; mono_ex = []; worst_avg = -1e9
    for m in mrange:
        for vals, mult in multisets(values, m):
            cnt['inst'] += 1
            rows = forms(vals, mult)
            if any(not r['mono'] for r in rows): cnt['mono'] += 1; mono_ex.append((vals, mult))
            if any(not r['core'] for r in rows): cnt['core'] += 1
            if any(not r['E'] for r in rows): cnt['E'] += 1
            if any(not r['dm'] for r in rows): cnt['dm'] += 1; dm_ex.append((vals, mult, [(r['k'], r['maxphi']) for r in rows if r['maxphi'] > 0]))
            worst_avg = max(worst_avg, max(r['avgphi'] for r in rows))
    print(f"{label}: instances {cnt['inst']}; violations: monotonicity {cnt['mono']}, core(averaged) {cnt['core']}, E(exists) {cnt['E']}, DM(per-element) {cnt['dm']}; max avg_e Phi_e = {worst_avg:.3f}  [{time.time()-t0:.0f}s]", flush=True)
    return mono_ex, dm_ex

mono_ex, dm_ex = sweep("ints [-6,6], m=4..9", list(range(-6, 7)), range(4, 10))
print("DM violations (first 12):")
for vals, mult, ks in dm_ex[:12]: print("   ", [v for v, n in zip(vals, mult) for _ in range(n)], ks)
print("reported monotonicity violations, verified by brute force:")
for vals, mult in mono_ex[:20]:
    w = [v for v, n in zip(vals, mult) for _ in range(n)]; m = len(w)
    s, _ = brute(w)
    viol = [(k, (m-k)*s[k], (k+1)*s[k+1]) for k in range(1, m//2) if (k+1)*s[k+1] > (m-k)*s[k]]
    print("   ", w, "brute s =", s, "brute-force violations:", viol)
sweep("ints [-3,3], m=4..12", list(range(-3, 4)), range(4, 13))
