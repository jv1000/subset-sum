"""R6-C1..C4: computational checks supporting BASE_CORE_REDERIVATION.md (see PREREG_R6.md).  numpy only."""
import sys, os, itertools, time
from fractions import Fraction as Fr
from math import comb, log2
from collections import defaultdict
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
o = open(os.path.join(HERE, "out", "core_checks.txt"), "w")
def P(*x):
    print(*x); print(*x, file=o); o.flush()
rng = np.random.default_rng(6)

# ---------- part A ----------
def layers(w):
    N = len(w); Sig = defaultdict(set)
    for mask in range(1 << N):
        Sig[bin(mask).count("1")].add(sum(w[i] for i in range(N) if (mask >> i) & 1))
    return Sig
def a(w, j):
    return Fr(len(layers(w)[j]), comb(len(w), j))
def dV(w):
    tot = set().union(*layers(w).values()); return len(w) - log2(len(tot))
def E_W(w, k, t):      # Lemma 3.1 right side
    N = len(w); vals = []
    for W in itertools.combinations(range(N), t - k):
        rest = [w[i] for i in range(N) if i not in W]; vals.append(a(rest, k))
    return sum(vals) / len(vals)
def E_S(w, k, s):      # Lemma 3.2 left side
    N = len(w); vals = [a([w[i] for i in S], k) for S in itertools.combinations(range(N), s)]
    return sum(vals) / len(vals)
def good_layer(w):
    N = len(w); L = layers(w); tot = len(set().union(*L.values()))
    for t in range(N // 2 + 1):
        if tot <= (N + 1) * len(L[t]): return t
    return None

P("== C1 part A: Lemmas 3.1-3.3, Corollary D, (F2) by enumeration")
n31 = n32 = n33 = 0; eq31 = eq32 = 0; worstD = (10.0, None); nD = 0; fails = defaultdict(int); eqgen = 0; ctrl_fail = 0
for trial in range(30):
    N = int(rng.integers(4, 8))
    generic = trial % 10 == 0
    w = [int(x) for x in rng.integers(-3, 4, size=N)]
    if generic: w = [10 ** 6 * 3 ** i for i in range(N)]
    for k in range(0, N + 1):
        for t in range(k, N + 1):
            lhs = a(w, t); rhs = E_W(w, k, t); n31 += 1
            if lhs > rhs: fails["3.1"] += 1
            if lhs == rhs and generic: eq31 += 1
    for k in range(0, N + 1):
        for s in range(k, N + 1):
            lhs = E_S(w, k, s); rhs = a(w, k); n32 += 1
            if lhs < rhs: fails["3.2"] += 1
            if lhs == rhs and generic: eq32 += 1
    t = good_layer(w); n33 += 1
    if t is None or a(w, t) < Fr(1, 2 ** N) * Fr(len(set().union(*layers(w).values())), N + 1): fails["3.3"] += 1
    # (F2)
    F = [i for i in range(N) if rng.random() < 0.5]
    w2 = [-w[i] if i in F else w[i] for i in range(N)]
    if abs(dV(w) - dV(w2)) > 1e-12: fails["F2"] += 1
# control for 3.1 (explicit): a_k(V) <= E_W a_t(V\W) with |W| = t-k is false in general
for trial in range(40):
    N = int(rng.integers(5, 9)); w = [int(x) for x in rng.integers(-3, 4, size=N)]
    for k in range(1, N // 2):
        for t in range(k + 1, N // 2 + 1):
            vals = []
            for W in itertools.combinations(range(N), t - k):
                rest = [w[i] for i in range(N) if i not in W]
                if len(rest) >= t: vals.append(a(rest, t))
            if vals and a(w, k) > sum(vals) / len(vals): ctrl_fail += 1
# Corollary D on |M| <= 8
for trial in range(40):
    Mn = int(rng.integers(5, 9)); w = [int(x) for x in rng.integers(-3, 4, size=Mn)]
    for k in range(1, 4):
        for sig in range(2 * k, Mn + 1):
            for v in range(sig, Mn + 1):
                if 2 * sig <= v + 2 * k and comb(sig, k) * comb(v, k) <= 2 ** v:
                    lhs = E_S(w, k, sig)
                    # E_V 2^{-d(V)} = E_V |Sigma(V)| / 2^v
                    tot = Fr(0); cnt = 0
                    for V in itertools.combinations(range(Mn), v):
                        wv = [w[i] for i in V]; tot += Fr(len(set().union(*layers(wv).values())), 2 ** v); cnt += 1
                    rhs = tot / cnt / (v + 1); nD += 1
                    if lhs < rhs: fails["D"] += 1
                    r = float(lhs / rhs)
                    if r < worstD[0]: worstD = (r, (tuple(w), k, sig, v))
P(f"   3.1: {n31} cases, failures {fails['3.1']}, equalities on generic {eq31}; 3.2: {n32} cases, failures {fails['3.2']}, equalities on generic {eq32}; 3.3: {n33} cases, failures {fails['3.3']}; (F2) failures {fails['F2']}")
P(f"   Corollary D: {nD} (w,k,sigma,v) cases, failures {fails['D']}, smallest ratio lhs/rhs = {worstD[0]:.3f} at {worstD[1]}")
P(f"   control (Lemma 3.1 with t and k swapped): {ctrl_fail} failures (must be > 0)")

# ---------- part B ----------
P("== C2 part B: one trial of Theorem A by brute force vs the Step-0 characterisation")
def run_trial(c, b, P_, M, L, R, k, sig, F, Pp, jp, targets, skip_interval=True):
    """returns dict target -> set of inserted keys (kappa_L, kappa_R, Z) following Base 5.2 (c)-(g); keys as tuples"""
    sgn = lambda i: -1 if i in F else 1
    cF = lambda X: sum(sgn(i) * c[i] for i in X); bF = lambda X: sum(sgn(i) * b[i] for i in X)
    keysL = defaultdict(list); keysR = defaultdict(list)
    for r_ in range(len(L) + 1):
        for A in itertools.combinations(L, r_): keysL[(sum(c[i] for i in A), sum(b[i] for i in A))].append(A)
    for r_ in range(len(R) + 1):
        for B in itertools.combinations(R, r_): keysR[(sum(c[i] for i in B), sum(b[i] for i in B))].append(B)
    out = {}
    for s, ts in targets.items():
        for q in range(len(c)):
            TF = (ts % P_) + q * P_ - sum(b[i] for i in F); tF = ts - sum(c[i] for i in F)
            left = [(kL, X) for kL in keysL for X in itertools.combinations(M, k) if (kL[1] + bF(X)) % Pp == jp % Pp]
            classes = defaultdict(list)
            for Y in itertools.combinations(M, sig - k): classes[(bF(Y), cF(Y))].append(Y)
            right = [(kR, lam) for kR in keysR for lam in classes if (kR[1] + lam[0]) % Pp == (TF - jp) % Pp]
            groups = defaultdict(list)
            for kR, lam in right: groups[kR[1] + lam[0]].append((kR, lam))
            for kL, X in left:
                for kR, lam in groups.get(TF - kL[1] - bF(X), []):
                    if skip_interval and kR[0] + lam[1] == tF - kL[0] - cF(X): continue
                    for Y in classes[lam]:
                        if set(X) & set(Y): continue
                        Z = tuple(sorted(set(X) ^ set(Y) ^ set(F)))  # (X u Y) symdiff F, X,Y disjoint
                        out.setdefault(s, set()).add((kL, kR, Z))
    return out
agree = 0; disagree = 0; sound_fail = 0; ctrl_hit = 0; ntr = 0; ninserted = 0
for trial in range(300):
    n = 8; m = 4; k = 1; sig = 2
    c = [int(x) for x in rng.integers(1, 41, size=n)]; P_ = int(rng.choice([31, 37, 41, 43])); b = [x % P_ for x in c]
    perm = list(rng.permutation(n)); M = sorted(perm[:m]); L = sorted(perm[m:m + 2]); R = sorted(perm[m + 2:])
    F = [i for i in M if rng.random() < 0.5]; Pp = int(rng.choice([5, 7, 11])); jp = int(rng.integers(Pp))
    tsum = sum(c); targets = {s: s for s in range(0, tsum + 1, max(1, tsum // 25))}   # a thinned target set
    ins = run_trial(c, b, P_, M, L, R, k, sig, F, Pp, jp, targets); ntr += 1
    # prediction per target: aliases I of t_s: c(I) = t_s mod P, c(I) != t_s
    for s, ts in targets.items():
        pred = set()
        for mask in range(1 << n):
            I = [i for i in range(n) if (mask >> i) & 1]; cI = sum(c[i] for i in I)
            if cI % P_ != ts % P_ or cI == ts: continue
            S = set(I) & set(M); S ^= set(F)
            kL = (sum(c[i] for i in I if i in L), sum(b[i] for i in I if i in L))
            kR = (sum(c[i] for i in I if i in R), sum(b[i] for i in I if i in R))
            hit = len(S) == sig and any((kL[1] + sum((-1 if i in F else 1) * b[i] for i in X)) % Pp == jp % Pp for X in itertools.combinations(sorted(S), k))
            if hit: pred.add((kL, kR, tuple(sorted(set(I) & set(M)))))
        got = ins.get(s, set()); ninserted += len(got)
        if got == pred: agree += 1
        else: disagree += 1
        # soundness: every inserted key is an alias class
        for (kL, kR, Z) in got:
            cI = kL[0] + kR[0] + sum(c[i] for i in Z)
            if cI % P_ != ts % P_ or cI == ts: sound_fail += 1
    # control: without the skipped interval, exact-sum classes get inserted
    ins2 = run_trial(c, b, P_, M, L, R, k, sig, F, Pp, jp, targets, skip_interval=False)
    for s, ts in targets.items():
        for (kL, kR, Z) in ins2.get(s, set()):
            if kL[0] + kR[0] + sum(c[i] for i in Z) == ts: ctrl_hit += 1
P(f"   {ntr} trials x targets: agreement {agree}, disagreement {disagree}; inserted keys {ninserted}, soundness failures {sound_fail}; control (no skipped interval): {ctrl_hit} exact-sum classes inserted (must be > 0)")

# ---------- part C ----------
P("== C3 part C: Lemma B2 numerically")
eps = 1e-8; Delta = 0.02844; Gamma = 0.45925; bb = [1, 1.25, 1.6, 2, 2.6, 3.5, 5, 8, 15, float("inf")]
def region(W):
    if W <= Gamma: return 0
    for i in range(1, 10):
        if Gamma * bb[i - 1] < W <= Gamma * bb[i]: return i
def check_B2(aG, adversarial, trials=20000):
    fails = 0; worst = 1.0
    for _ in range(trials):
        J = 43; U = rng.uniform(-0.3, 0.2, size=J); W = rng.uniform(0.0, 8.0, size=J)
        v = int(np.argmax(U)); rho = region(W[v]); alpha = 1.0 if W[v] <= Gamma else Gamma / W[v]
        if alpha * U[v] >= Delta: continue          # not sampled
        C = [l for l in range(J) if l != v and rng.random() < 0.2]
        if rho == 0: nrow = 2 + len(C); z0min = 1.0
        elif rho <= 8: nrow = 3 + len(C); z0min = 1.0 / bb[rho - 1]
        else: nrow = 2 + len(C); z0min = 1.0 / 15
        z = rng.uniform(0, 5, size=nrow); z[0] = z0min * rng.uniform(1.0, 3.0) if rng.random() < 0.7 else z0min
        du = 3 * eps * (np.ones(J) if adversarial else rng.uniform(-1, 1, size=J)); dw = 4 * eps * (np.ones(J) if adversarial else rng.uniform(-1, 1, size=J))
        ub = U - du * (1 if rng.random() < 0.5 else -1); wb = W + dw * (1 if rng.random() < 0.5 else -1)
        if adversarial:  # worst signs for row 0 and the band rows
            ub = U + 3 * eps; wb = W + 4 * eps if rho else W + 4 * eps
        if rho == 0: G = [Delta - ub[v], Gamma - wb[v]] + [ub[v] - ub[l] for l in C]
        elif rho <= 8: G = [aG * wb[v] - ub[v], wb[v] - Gamma * bb[rho - 1], Gamma * bb[rho] - wb[v]] + [ub[v] - ub[l] for l in C]
        else: G = [aG * wb[v] - ub[v], wb[v] - 15 * Gamma] + [ub[v] - ub[l] for l in C]
        lhs = -alpha * U[v]; rhs = -Delta + float(np.dot(z, G)) + 6 * eps * z.sum()
        if lhs > rhs + 1e-15: fails += 1
        worst = min(worst, rhs - lhs)
    return fails, worst
f1, w1 = check_B2(Delta / Gamma, False); f2, w2 = check_B2(Delta / Gamma, True)
P(f"   a_Gamma = {Delta/Gamma:.4f}: random errors {f1} failures (min margin {w1:.2e}); adversarial errors {f2} failures (min margin {w2:.2e})")
# control: a_Gamma = 0.9 with adversarial errors and z = (z0,0,0): the row-0 error is (4*0.9+3) eps = 6.6 eps > 6 eps
f3, w3 = check_B2(0.9, True)
P(f"   random control a_Gamma = 0.9, adversarial signs: {f3} failures (min margin {w3:.2e}) -- not tight, see the explicit instance below")
def tight_B2(Delta_, Gamma_, i=3, tiny=1e-13):
    # a_Gamma = Delta_/Gamma_ (it is not a free parameter: alpha a_Gamma W = Delta needs a_Gamma = Delta/Gamma).
    # region rho_i, W just above Gamma b_{i-1}, U just below a_G W (sampled), z = (1/b_{i-1}, 0, 0), worst-sign errors
    aG = Delta_ / Gamma_
    W = Gamma_ * bb[i - 1] * (1 + tiny); U = aG * W - tiny; alpha = Gamma_ / W; z0 = 1.0 / bb[i - 1]
    ub = U + 3 * eps; wb = W - 4 * eps
    lhs = -alpha * U; rhs = -Delta_ + z0 * (aG * wb - ub) + 6 * eps * z0
    return aG, rhs - lhs, z0 * eps * (3 - 4 * aG)
for Dl_, Gm_ in ((Delta, Gamma), (0.30, 0.40), (0.32, 0.40), (0.36, 0.40)):
    aG, mg, pred = tight_B2(Dl_, Gm_)
    P(f"   explicit tight instance (rho_3, W = Gamma b_2 (1+1e-13), U = a_G W - 1e-13, z = (1/b_2,0,0)), (Delta,Gamma) = ({Dl_},{Gm_}), a_Gamma = {aG:.4f}: margin {mg:.3e}, predicted z0*eps*(3-4a_G) = {pred:.3e} -> {'holds' if mg >= 0 else 'FAILS'}")
o.close()
