"""A5: exhaustive DM / monotonicity over value multisets (integers in a range, and Z_q)."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import defaultdict
t0 = time.time()

def dm_check(vals, mult, add=None, zero=0):
    """vals: distinct values, mult: multiplicities. Returns (mono_viol, dm_viol, tight) for k+1 <= m/2."""
    r = len(vals); m = sum(mult)
    states = {(0, zero): [0] * r}
    for i, (v, n) in enumerate(zip(vals, mult)):
        new = {}
        for (j, y), t in states.items():
            acc = y
            for c in range(n + 1):
                key = (j + c, acc)
                tt = new.get(key)
                if tt is None:
                    tt = t[:]; tt[i] = c; new[key] = tt
                else:
                    for q in range(i):
                        if t[q] < tt[q]: tt[q] = t[q]
                    if c < tt[i]: tt[i] = c
                acc = add(acc, v) if add else acc + v
        states = new
    s = [0] * (m + 1); core = [[0] * r for _ in range(m + 1)]
    for (j, y), t in states.items():
        s[j] += 1
        for i in range(r):
            if t[i] == mult[i]: core[j][i] += 1
    mono = dm = 0; tight = False
    for k in range(1, m // 2):
        if (k + 1) * s[k + 1] > (m - k) * s[k]: mono += 1
        ph = max((k + 1) * core[k + 1][i] - (m - k - 1) * core[k][i] - s[k] for i in range(r))
        if ph > 0: dm += 1
        if ph == 0: tight = True
    return mono, dm, tight

def multisets(values, m):
    for comb in itertools.combinations_with_replacement(range(len(values)), m):
        d = defaultdict(int)
        for i in comb: d[i] += 1
        yield [values[i] for i in sorted(d)], [d[i] for i in sorted(d)]

def run(label, values, mrange, add=None, zero=0):
    tot = mono = dm = tight = 0; ex = None
    for m in mrange:
        for vals, mult in multisets(values, m):
            a, b, t = dm_check(vals, mult, add, zero); tot += 1; mono += a > 0; dm += b > 0; tight += t
            if b > 0 and ex is None: ex = (vals, mult)
    print(f"{label:28s}: multisets {tot}, monotonicity violations {mono}, DM violations {dm}, tight instances {tight} ({100*tight/tot:.1f}%)  example {ex}  [{time.time()-t0:.0f}s]", flush=True)

if __name__ == "__main__":
    run("ints [-3,3], m=4..12", list(range(-3, 4)), range(4, 13))
    for q in range(2, 8):
        run(f"Z_{q}, m=4..12", list(range(q)), range(4, 13), add=lambda a, b, q=q: (a + b) % q)
    run("ints [-6,6], m=4..9", list(range(-6, 7)), range(4, 10))
