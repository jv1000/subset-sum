# Round-5 pre-registrations (YP-Hall: the gap, the base case k = 1, the window at m = 18–20)

Rules as in rounds 2–4: prediction and control written before each run; outcome appended after; one process at a
time; each run ≤ 10–30 min; no exhaustive enumeration above m = 22 (nothing here goes above m = 20); every flow run
has a memory guard (edge-count cap and a process-RSS check that aborts the case). Scripts in `scripts/round5/`,
outputs in `scripts/round5/out/`. Libraries reused: `../round4/lay4.py` (fast Q_w, generic padding),
`../round4/charge_flow.py` (near-miss / target enumeration `Inst`), `../round3/lay3.py` (Dinic).

Notation as in `../round4/PREREG_R4.md`. The rule under test is **YP**: a near miss (X, A, A′), P = A∖A′, Q = A′∖A,
may charge a target (Y, Y*, D) iff Y ⊇ P (any collision partner Y*, any admissible D). YPQ (Y ⊇ P or Y ⊇ Q) and
YPQx (YPQ with Y ≠ X) are the two weaker variants also carried along.

## R5-A1 `charge_flow5.py` — the 137 dense m = 8, 9 cases skipped in round 4, by a collapsed (sparse) flow
Method. The YP neighbourhood of a source (X, A, A′) depends only on P, the YPQ neighbourhood only on (P, Q), the YPQx
neighbourhood on (P, Q) and on whether Y = X; the neighbourhood of a target (Y, Y*, D) depends only on Y. Sources with
identical neighbourhoods are merged (supply added), targets with identical neighbourhoods are merged (capacity added:
cap(Y) = Σ_{(Y*,D)} N(D)/f(Y)); the max-flow value of the merged network equals that of the explicit one (PROVED,
standard: merging nodes with identical neighbourhoods on one side of a bipartite flow network with infinite middle
edges does not change the max flow). The merged network has ≤ #P-classes × #collision-Y edges, so the dense cases
fit in memory. Memory guard: a case is skipped if the merged edge count exceeds 3·10⁶, and the run aborts if the
process working set exceeds 1500 MB.
Cases. The exact 137 cases are regenerated: `numpy.random.default_rng(8)`, the first 116 size-8 draws and then the
first 80 size-9 draws of round 4's `charge_flow4b.py`, with the same (k,t) loop and the same guard
(src × tgt > 1.5·10⁶); the regenerated count must be 33 + 104 = 137 (checked and reported). Also the three curated
m = 9 instances that `charge_flow4.py` never reached ((0,0,0,1,1,1,2,2,2), (−3,−3,−2,−1,0,1,2,3,3),
(−2,−2,−1,−1,0,0,1,1,2) at k = 2, t ∈ {3, 4}).
Validation (control 1). On 300 random (instance, k, t) cases at m = 6, 7 (values in [−3,3], t + 2k ≤ m) the merged
flow must agree with the explicit dense flow of `charge_flow4.py` to 10⁻⁸ in the routed fraction, for all three rules.
Control 2. (−3,−3,−2,−2,0,0) at (2,3) must stay infeasible: routed fraction 0.900 under YP, YPQx, YPQ (round-4 value).
Control 3. The equality case (0,0,g1,g2) at (1,2) must route exactly 1 with zero slack (supply = capacity).
Prediction. 0 failures of YP, YPQx and YPQ on all 137 + 6 cases (worst routed fraction ≥ 1 − 10⁻⁶). If a failure
occurs the script prints the Hall violator (residual reachability after Dinic: the merged source classes and the
collision sets Y in the cut, with supply and capacity) and the run is reported as a counterexample to YP-Hall.
Budget: ≤ 12 min.

## Outcome A1 — charge_flow5.py, out/charge_flow5.txt (13 s)
Control 1: 302 random (instance,k,t) cases at m = 6, 7, three rules: max |collapsed − explicit| = 1.1·10⁻¹⁰ (PASS).
Control 2: (−3,−3,−2,−2,0,0) at (2,3) routes 0.9000 under YP, YPQx, YPQ (infeasible, as required; supply 30, cap 27).
Control 3: (0,0,g1,g2) at (1,2): supply = cap = 4.000, routed 1 (tight).
The 137 guard-skipped cases were regenerated exactly (33 at m = 8, 104 at m = 9; the 843 tested cases also match).
**0 failures of YP, YPQx and YPQ on all 137 dense cases and the 6 curated m = 9 cases**; worst YP routed fraction
1 − 3·10⁻¹²; no case skipped by the edge cap; peak working set 46 MB. Prediction MET. The round-4 caveat is closed.

## R5-A1b `charge_flow5b.py` — broader sweep with the collapsed flow (extension, pre-registered after A1)
Exhaustive multisets, in a fixed shuffled order with a time cap per m: m = 8 in [−3,3] (3003 multisets, cap 600 s),
m = 9 in [−2,2] (715, cap 420 s), m = 10 in [−2,2] (1001, cap 360 s; k ≤ 3), all (k,t) with t + 2k ≤ m; rules YP,
YPQx, YPQ; memory guard as in A1. Coverage (multisets reached before the cap) is reported.
Control: (−3,−3,−2,−2,0,0) at (2,3) at 0.900 again. Prediction: 0 failures for all three rules; worst routed
fraction ≥ 1 − 10⁻⁶; the `free` rule (supply ≤ capacity) never fails either (no Q_w > 1 in range). Budget ≤ 25 min.

## Outcome A1b — charge_flow5b.py, out/charge_flow5b.txt (13 min)
Control 0.900 (ok). m = 8 in [−3,3]: all 3003 multisets, 15,015 (k,t)-cases; m = 9 in [−2,2]: all 715, 3,575 cases;
m = 10 in [−2,2]: 86/1001 multisets (cap), 688 cases, peak working set 241 MB. **0 failures of free, YP, YPQx, YPQ**
on all 19,278 cases; worst YP routed fraction 1 − 2·10⁻¹⁰ (the all-equal instances at (1,2), which are tight). Five
m = 10 cases at (2,5) exceeded the edge cap for YPQx only (YP and YPQ ran on them, feasible). Prediction MET.

## R5-A2 `k1_hall.py` — the base case k = 1: exact reductions checked, Hall slack, tight sets, two hypotheses
Derivations made before the run (to be stated as PROVED in the report, each checked numerically here as a control):
(R1) at k = 1, with classes c (equal weights), n_c = |c|, N_c = Σ_{X ∋ p} 1/f(X) (p ∈ c), M_c = n_c N_c = mult_w(w_c),
     C = C(m−1,t−1): Q_w(t,1) = Σ_c M_c² / (t s_t C), Σ_c M_c = t s_t, so Q_w ≤ 1 ⟺ Σ_c M_c (M_c − C) ≤ 0.
(R2) supply of the k = 1 charging problem: S_p = N_c Σ_{X ∋ p} (j_c(X) − 1)/f(X) (j_c(X) = |X ∩ c|); capacity of the
     merged target Y: cap(Y) = Σ_c N_c j_c(Y) (f(Y) − 1 − n_c + j_c(Y)) / f(Y); Σ_p S_p − Σ_Y cap(Y) = Σ_c M_c (M_c − C).
(R3) YP-Hall at k = 1 is the Hall condition of the transportation problem "element p (demand S_p) may use the
     collision sets Y ∋ p (capacity cap(Y))"; by symmetry under the transpositions inside a class and submodularity of
     K(R) − S(R), the minimum over R ⊆ [m] is attained at a union of classes.
(R4) M_c − C = Σ_X j_c(X)(n_c − f(X)) / (n_c f(X)) and f(X) ≥ Π_c C(n_c, j_c(X)) ≥ n_c unless j_c(X) ∈ {0, n_c}; hence
     M_c > C ("over-represented class") requires a t-set X ⊇ c with f(X) < n_c, so n_c ≤ t; singletons have M_c ≤ C.
Run: exhaustive multisets in [−3,3] for m = 6, 7 and in [−2,2] for m = 8, 9, k = 1, all 2 ≤ t ≤ m/2. For each case:
(a) Q_w by (R1) vs `lay4.qw` (control: agree to 10⁻⁹); S_p and cap(Y) by (R2) vs the enumeration in `Inst` (control:
agree to 10⁻⁹); (b) min over all R ⊆ [m] of K(R) − S(R) vs min over unions of classes (control for (R3): equal; and
sign consistent with the Dinic YP flow); (c) the tight set U* (argmin), compared with the over-represented set
O = {c : M_c > C}; (d) the explicit proportional map at k = 1 (p sends S_p to Y ∋ p in proportion to cap(Y)): max load;
(e) the profile model: for the class sizes (n_c) of w, s₀ = #{(j_c) : 0 ≤ j_c ≤ n_c, Σ j_c = t}, J_c = Σ_j j_c,
slack₀ = C t s₀ − Σ_c J_c², compared with slack(w) = C t s_t − Σ_c M_c²; control: slack₀ equals slack of the realised
instance with generic class values (computed by `lay4.qw`).
Predictions. (b) 0 Hall failures at k = 1 (every case feasible); (c) the tight U* is contained in O ∪ {classes of size
≥ 2} and contains the over-represented classes whenever O ≠ ∅ — in words, the Hall condition is tightest on the
over-represented classes; (d) the proportional map is valid at k = 1 (max load ≤ 1) — a genuine prediction, since it
fails at k = 2 (load 1.126 in round 4); control: that k = 2 instance reproduces load > 1 under the same code;
(e) slack(w) ≥ slack₀ in every case (the profile model is the extremal instance for its class sizes: "extra
coincidences only help at k = 1"). Budget ≤ 10 min.

## Outcome A2b — k1_families.py, out/k1_families.txt (seconds)
Controls: the closed forms reproduce `lay4.qw` exactly on all 7 control instances (e.g. 25/33, 97/135, 1763/3472).
(F1) 4,940 cases (a + b ≤ 40): 0 violations, equality exactly at (a,b,t) = (2,2,2). (F2) 9,329 cases (n + G ≤ 40):
0 violations, equality exactly at (n,G,t) = (2,2,2). Prediction MET, including "maximised at n = 2, t = 2 for each m"
(except m = 6: (2,4,3) at 0.9333 beats (2,4,2) at 0.9091 — the only exception). Unregistered observation worth
keeping: at n = 2, t = 2 the ratio is (G² + 4G + 4 + G³)/((G+1)(G² + G + 2)) → 1 as G → ∞ (0.976 at m = 40): a single
pair of equal values among generic values is asymptotically tight for Conjecture Q at (k,t) = (1,2).

## R5-A3 `hill5.py` — hill-climb at m = 18 and 20 in the window k < m/3
Objective: max of Q_w(t,k) over (k,t) ∈ {(4,5),(4,6),(5,6),(5,7),(5,8),(5,9)} at m = 18 and {(5,6),(5,7),(6,7),(6,8)}
at m = 20 (the cheap pairs in the window; the pairs (6,9), (6,10) at m = 20 are evaluated once for the final best
instance only). Moves: one coordinate replaced by a value from {−3..6} or by a fresh generic value; seeds: the
generic-padded {0,1,5} shapes of round 4 (0^a 1^b 5^c + g generic, g ∈ {2,4}) and random palette instances; time
cap 12 min per m (one process). Control: the same climber restricted to the pair (m/2 − 1, m/2) must find Q_w > 1
within its cap (known values 1.023 at m = 16, 1.024 at m = 20), showing it can find violations where they exist.
Prediction: no Q_w > 1 in the window at m = 18 or 20; the best found is ≤ 0.85, at the largest allowed k
(k = 5 at m = 18, k = 6 at m = 20) with t = k + 1, and is a generic-padded two- or three-valued shape.
Amendment to A3 (before the run): the climb objective is the max over the two pairs (k, k+1) with the largest
allowed k — (4,5), (5,6) at m = 18 and (5,6), (6,7) at m = 20 — because the pairs with t ≥ k + 2 cost 5–10× more per
evaluation and round 4 found every window maximiser at t = k + 1; the full window list ((4,5)…(5,9) at m = 18,
(5,6)…(6,10) at m = 20) is evaluated for the top four instances of each climb. Caps: control 150 s, climb 540 s per m.

## R5-A2b `k1_families.py` — exact check of the two k = 1 families handled by hand (pre-registered before the run)
Hand derivations (to be written up as PROVED in the report): with classes c, M_c = n_c N_c, C = C(m−1,t−1), and
Q_w(t,1) ≤ 1 ⟺ Σ_c M_c² ≤ C t s_t (R1):
(F1) two-valued w = 0^a 1^b, a ≤ b, 2 ≤ t ≤ m/2: fibers ↔ j = |X ∩ zeros| ∈ [0, min(a,t)], s = min(a,t) + 1,
     M_0 = Σ_j j, M_1 = t s − M_0; the inequality reduces to t(t+1)/2 ≤ C(m−1,t−1) when a ≥ t and to
     (a+1)(a² + (2t−a)²)/4 ≤ C(m−1,t−1) t when a < t, both true for m ≥ 2t; equality only at a = b = t = 2.
(F2) one class of n ≥ 2 equal values plus G generic values (m = n + G): with u_j = C(G, t−j), 0 ≤ j ≤ min(n,t):
     s = Σ u_j, M_0 = Σ j u_j, each generic class has M_g = Σ_j C(G−1, t−1−j) =: N_g, and the inequality is
     M_0² + G N_g² ≤ C t s. Proved by hand for n = 2 (all G, t with m ≥ 2t; equality only at G = t = 2); for n ≥ 3
     only checked here.
Run: exact integer arithmetic over all (a, b, t) with a + b ≤ 40 and all (n, G, t) with n + G ≤ 40, n ≥ 2, G ≥ 1,
2 ≤ t ≤ m/2. Control: the closed forms reproduce `lay4.qw` on (0,0,0,1,1,1,1) t = 2, 3, (0,0,1,1,1,1,1,1) t = 4,
(0,0,0,g,g,g,g) t = 2, 3, (0,0,0,0,g,g,g,g,g) t = 3, 4 to 10⁻¹². Prediction: (F1) and (F2) hold on the whole range,
with equality exactly at the stated cases; the ratio Σ M_c²/(C t s) in (F2) is maximised at n = 2, t = 2 for each m.

## Outcome A2 — k1_hall.py, out/k1_hall.txt (25 s; rerun once with a corrected check, see below)
Coverage: exhaustive m = 6, 7 in [−3,3] (1834 + 3430 cases) and m = 8, 9 in [−2,2] (1485 + 2145 cases), k = 1, all
t ≤ m/2: 8,894 cases. Controls: (R1), (R2) formulas agree with the enumeration to 10⁻¹³; the k = 2 instance gives
proportional load 1.126 under YPQ (and 1.051 under YP), reproducing round 4; the profile model equals its realised
generic-class instance on all 6 controls.
(b) **0 Hall failures** (min over class unions ≥ 0 everywhere; the Dinic YP flow routes 1 in every case; no sign
mismatch between the two). Prediction MET.
(c) Whenever the over-represented set O is nonempty (192 cases at m = 6, 14 at m = 7; none at m = 8, 9 in [−2,2]),
the tight set is exactly U* = O (206/206). Prediction MET (and sharper than predicted: equality, not containment).
Also: the Hall ratio max_U S(U)/K(U) is far from 1 — 0.545 (m = 6), 0.385 (7), 0.286 (8), 0.207 (9) — the k = 1
condition is slack in these ranges; the tight cases are classes of size 2 at t = m/2.
(d) The proportional map is valid at k = 1 on all 8,894 cases: max load 0.818 (m = 6), 0.574, 0.361, 0.288.
Prediction MET (EVIDENCE for a closed-form certificate at k = 1; it is false at k = 2).
(e) Prediction FAILED: slack(w) < slack₀ (profile model) in 9 cases at m = 6, 349 at m = 7, 677 at m = 8, 1229 at
m = 9 (e.g. (−3,0,0,0,0,3), t = 2: 13.59 < 16; (−1,0,0,0,0,1,2), t = 3: 140.9 < 168). Extra coincidences do NOT
only help; the profile model is not extremal for its class sizes, so Conjecture Q at k = 1 does not reduce to the
profile inequality. Kept as a dead end.
Error in the pre-registered (R3), found by the control: "the minimum of K(R) − S(R) over R is attained at a union of
classes" is FALSE (the first run flagged a mismatch in every case: the minimum over all R is attained at single
elements, e.g. (−2,−2,0,2,2,3) t = 3: 40 at one element vs 50 for the class). The lattice argument needs
F(∅) = 0 ≥ min, i.e. it only applies when the minimum is ≤ 0. The correct statement — a Hall VIOLATION, if any,
occurs at a union of classes, so YP-Hall(k = 1) ⟺ K(U) ≥ S(U) for all unions U — stands (same proof, restricted to
negative minimisers). The script was rerun with the check "sign of min over R = sign of min over unions".
Rerun with the corrected check (23 s): no sign mismatch in any of the 8,894 cases (both minima ≥ 0 everywhere);
the minimum over all R is strictly below the minimum over class unions in every case (as explained above). All other
numbers identical to the first run.

## Outcome A3 — hill5.py, out/hill5.txt (19 min)
Controls MET: the climber on (8,9) at m = 18 found 1.0236 (0⁴1⁴5²6 + 7g) and on (9,10) at m = 20 found 1.0235
(0⁵1³5⁴6 + 7g), each on its first restart (a seed shape), so it finds violations where they exist.
Window climbs: m = 18, 662 restarts, 38,431 evaluations; m = 20, 136 restarts, 7,842 evaluations. **No Q_w > 1.**
Prediction "best ≤ 0.85" FAILED for a reason I overlooked when pre-registering: generic weights (all values
distinct, no relations) give Q_w = 1 exactly at every (k,t), so the climber, which accepts non-decreasing moves,
drifts from every seed to a generic instance ((−2,1,3,5) + 14g, (0,1,3,5) + 16g, …: 1.0000 at every window pair) and
then wanders among generic instances. The best non-generic instances are a single pair among generics
((0,1,1,3,6) + 15g at m = 20: 0.9987 at (6,10), 0.974–0.983 elsewhere), consistent with (F2) (a pair among generics
is asymptotically tight). So the run shows that no single-coordinate perturbation of a generic instance exceeds 1 in
the window at m = 18, 20 (46,000 evaluations), but it did not explore the structured (few-valued) region beyond the
seeds, which was the point of the task. Round 4's window maxima (0.70) were lower only because its families
excluded near-generic instances.

## R5-A3b `hill5b.py` — palette-only hill-climb (pre-registered after A3; the generic attractor removed)
Same climber, but the instance has exactly g generic entries fixed in place (g ∈ {0, 4}) and the other m − g
coordinates take values in {−3,…,6} only (at most 10 distinct small values among ≥ 14 coordinates, so the instance
cannot become generic and must carry ≥ 4 coincidences). Objective pairs and seeds as in A3 (seeds with g generics;
random palette starts); cap 210 s per (m, g); full window list evaluated on the top instances. Control: with g = 4
the climber on (m/2 − 1, m/2) must still find Q_w > 1 at m = 18 and 20 (the known shapes have 4–7 generics; cap 60 s).
Prediction: no Q_w > 1 in the window; the best found is < 1 and is attained with g = 4 and the maximal number of
distinct small values (as near-generic as the palette allows), at the largest allowed k with t = k + 1 or t = m/2;
with g = 0 the best is ≤ 0.90.

## Outcome A3b — hill5b.py, out/hill5b.txt (15 min)
Controls MET: with g = 4 the climber finds 1.0224 at (18; 8,9) (0⁶1³5⁴6 + 4g) and 1.0240 at (20; 9,10) (0⁶1⁴5⁶ + 4g,
round 4's maximiser) on the first restart. Window climbs (evaluations: 15,934 / 16,648 at m = 18 for g = 0 / 4;
3,472 / 3,379 at m = 20): **no Q_w > 1**; best m = 18: 0.610 at (5,6) with g = 0 (0⁶1⁵6⁷), 0.713 at (5,6) with g = 4
((−3)⁵0²5²6⁵ + 4g); best m = 20: 0.625 at (6,7) with g = 0 ((−2)⁷1⁵4 5⁷), 0.705 at (6,7) with g = 4 ((−3)⁶2 5⁴6⁵ + 4g);
the full window lists of the top instances are all ≤ 0.713. Predictions "no violation", "best < 1 attained with
g = 4 at the largest allowed k with t = k + 1", and "g = 0 best ≤ 0.90" MET. Sub-prediction "the maximiser uses the
maximal number of distinct small values" FAILED: every maximiser is three- or four-valued (large classes plus the
four generics); with more distinct palette values the arithmetic coincidences (0 + 6 = 1 + 5, …) lower Q_w. So the
window at m = 18, 20 has the same picture as round 4 (max ≈ 0.70 for structured instances, from few-valued blocks
with generic padding), and the only way to approach 1 in the window is to approach a generic instance (A3).
