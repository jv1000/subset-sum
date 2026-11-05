import sys, itertools, time
from math import comb
from fractions import Fraction
sys.path.insert(0, '/tmp/claude-0/-home-claude/1081a3db-b67e-507d-81e3-94e8009d81b7/scratchpad')
from bf import layers, check_instance

plan = [(n, -4, 4) for n in range(1, 8)] + [(8, -3, 3), (9, -3, 3), (10, -2, 2)]
if len(sys.argv) > 1:
    plan = [tuple(int(x) for x in a.split(',')) for a in sys.argv[1:]]

for (n, lo, hi) in plan:
    t0 = time.time()
    ninst = 0
    nchecks_all = 0; nchecks_drop = 0
    min_all = None; arg_all = None
    min_drop = None; arg_drop = None
    fail_all = []; fail_drop = []
    t_below_k = 0  # (instance,V,k) pairs where no good t>=k exists in [k, v/2]
    nonunimodal = 0; nonuni_ex = None
    for ws in itertools.combinations_with_replacement(range(lo, hi + 1), n):
        ninst += 1
        L = layers(list(ws))
        res, per = check_instance(list(ws), L)
        for (k, sig, v, pok, lhs, rhs) in res:
            if v == 0: continue
            r = lhs / rhs
            if pok:
                nchecks_all += 1
                if min_all is None or r < min_all:
                    min_all, arg_all = r, (ws, k, sig, v)
                if lhs < rhs:
                    fail_all.append((ws, k, sig, v))
            else:
                nchecks_drop += 1
                if min_drop is None or r < min_drop:
                    min_drop, arg_drop = r, (ws, k, sig, v)
                if lhs < rhs:
                    fail_drop.append((ws, k, sig, v))
        # diagnostics on full set M only (V = M)
        mask, s, cnts, tot = per[-1]
        half = n // 2
        for j in range(half):
            if cnts[j + 1] < cnts[j]:
                nonunimodal += 1
                if nonuni_ex is None:
                    nonuni_ex = (ws, cnts)
                break
    print(f"n={n} weights in [{lo},{hi}] multisets={ninst} "
          f"checks(all hyps)={nchecks_all} min ratio={float(min_all) if min_all else None} at {arg_all} fails={len(fail_all)} | "
          f"checks(product dropped)={nchecks_drop} min ratio={float(min_drop) if min_drop else None} at {arg_drop} fails={len(fail_drop)} | "
          f"layer-size non-monotone on [0,n/2] (full M)={nonunimodal} ex={nonuni_ex} | {time.time()-t0:.1f}s", flush=True)
    if fail_all[:3]: print("  FAIL all-hyps examples:", fail_all[:3])
    if fail_drop[:3]: print("  FAIL dropped examples:", fail_drop[:3])
