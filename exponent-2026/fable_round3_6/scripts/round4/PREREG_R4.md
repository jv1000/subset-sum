# Round-4 pre-registrations (Conjecture Q: Q_w ≤ 1; the charging inequality w(L^nm) ≤ w(R′))

Rules as in rounds 2–3: prediction and control written before each run; outcome appended after; one process at a
time; each run ≤ 10–30 min; no exhaustive enumeration above m = 22 (nothing here goes above m = 20). Scripts in
`scripts/round4/`, outputs in `scripts/round4/out/`. Library `lay4.py`: subset sums by doubling (m ≤ 20), fast Q_w
(numpy, chunked over t-sets), aggregated near-miss / collision enumeration and a Dinic max-flow for the charging tests.

Notation (ROUND3_REPORT A.3 (ii)). Near miss ℓ = (X, X′, A ⊆ X, A′ ⊆ X′), w(A) = w(A′), A ≠ A′, P = A∖A′, Q = A′∖A,
B = Q ∩ X ≠ ∅, weight 1/(f(X)f(X′)). Target r = (Y, Y*, Y″, D): w(Y) = w(Y*), Y ≠ Y*, D ⊆ Y ∩ Y″, |D| = k, D ⊉ Y∖Y*,
weight 1/(f(Y)f(Y″)). A *fractional charging map* is a flow from near misses (supply = weight) to targets (capacity =
weight) along the edges of a *locality rule*; the rule is viable on an instance iff the max-flow saturates all supply.
Aggregation: a rule that ignores X′ (resp. Y″) uses the aggregated nodes (X, A, A′) with supply N(A′)/f(X) (resp.
(Y, Y*, D) with capacity N(D)/f(Y)); this is exact because Σ_{X′ ⊇ A′} 1/f(X′) = N(A′).

New working hypothesis (stated before any new run; to be tested, not assumed):
**H2: Q_w ≤ 1 whenever t + 2k ≤ m** (k < t ≤ m/2). It contains Conjecture Q (k ≤ m/4, t ≤ m/2 ⟹ t + 2k ≤ m) and is
suggested by (a) the known failures all having m − t − k < k ((6,2,3), (8,3,4), (10,4,5), (12,4,6), (12,5,6)), (b) the
exact equality cases Q_w = 1 at t + 2k = m found by hand: m = 4, (k,t) = (1,2), w = (0,0,g1,g2) and w = (0,0,1,1), and
(c) the repair step of the candidate map needing |E| = |B| ≤ k fresh elements outside X ∪ Q, i.e. m − t − k ≥ k.
Alternatives kept alive: H1 (only k ≤ m/4 is safe), H3 (k < m/3 is safe). Discriminating cases: (16; 5, 6) is safe
under H2 and H3, unsafe under H1; (16; 5, 7), (16; 5, 8), (20; 6, 9), (20; 6, 10) are unsafe under H2 and H1, safe
under H3; (20; 6, 7), (20; 6, 8) are safe under H2 and H3.

## R4-A0 `window_small.py` — exact window at small m (fast Q_w, all k < t ≤ m/2, middle step included)
Exhaustive multisets in [−3,3] for m = 6..10, in [−4,4] for m = 6..8, in [−5,5] for m = 6, 7; also max_u mult_w(u)/C(m−k,t−k)
(the per-u ratio).
Prediction: no instance with t + 2k ≤ m has Q_w > 1 (this includes the boundary cases (7;2,3), (8;2,4), (10;3,4));
Q_w > 1 occurs at (6;2,3), (8;3,4), (10;4,5) as in A5 and, with the wider ranges, possibly at (9;3,4) and (10;3,5) too
(t + 2k > m). The per-u ratio exceeds 1 already at k = 1 (zeros + generic) while Q_w ≤ 1 there.
Control: (−3,−3,−2,−2,0,0) at (2,3) gives 1.0357 (A5 value); generic weights give exactly 1.000 at every (k,t).

## R4-A1 `charge_flow.py` — candidate charging maps as locality rules, tested by max-flow
Rules (edges from ℓ = (X, A, A′) to r = (Y, Y*, D)), from most to least restrictive:
- `perD`: Y″ = X′ and D = A′ (not a flow: it is the per-u bound mult_w(w(D)) ≤ C(m−k,t−k); known false).
- `S1E`: repair, forward orientation, D ⊇ E: Y = (X∖B) ∪ E with E ⊆ M∖(X ∪ Q), |E| = |B|; Y* = (Y∖P) ∪ Q; D ⊇ E.
- `S1`: as S1E with D ⊆ Y, D ⊉ P free.
- `S2`: S1 or the reversed orientation (Y = (X∖B∖P) ∪ E ∪ Q, Y* = (X∖B) ∪ E, D ⊆ Y, D ⊉ Q).
- `T`: Y = (X∖B) ∪ E as above, Y* any collision partner of Y, D free.
- `C`: X ∈ {Y, Y*} (the collision involves X itself), D free.
- `V`: |Y △ X| ≤ 2|B|, Y*, D free.
- `free`: all edges (feasible iff w(L^nm) ≤ w(R′) iff Q_w ≤ 1; consistency check of the enumeration).
Instances: exhaustive [−3,3] at m = 6 (k = 1,2), m = 7 (k = 1,2) and a 6-minute sample at m = 8 (k ≤ 2); the zeros +
generic family (0^a, g^b) at m = 5..9; the three m = 8 counterexamples; two-valued; the A0 worst cases.
Prediction: `free` agrees with the sign of Q_w − 1 on every instance (enumeration check). `perD` fails on (0,0,g,g,g)
at (1,2) and (0^5,g^3) at (2,4) although Q_w < 1 there (known). `C` fails on the zeros family (the collisions at the
all-zero X are too few). `S1` is feasible on every instance with t + 2k ≤ m (medium confidence), and `S1E` is
feasible on the equality case (0,0,g1,g2) (where it is tight) but fails somewhere else in range. `V` feasible wherever
`S1` is. Control: (−3,−3,−2,−2,0,0) at (2,3) infeasible under every rule (its total supply exceeds total capacity).

## R4-A2 `window16.py` — the window k/m ∈ (1/4, 1/3) at m = 16
Families (affine-invariant, so values are normalised): two-valued {0,1} with every split; three-valued {0,1,c},
c ∈ {2,3,4,5}, every multiplicity split (the A5 worst shape (−3,−3,−3,−2,−2,−2,1,1) is {0,1,4} with split (3,3,2));
four-valued {0,1,c,d} with the A5/m = 10, 12 worst shapes scaled; each of these plus 1–4 generic elements; products
of the A5 worst gadgets. (k,t): k ∈ {4,5,6}, t ∈ (k, 8].
Prediction (H2): Q_w ≤ 1 at (4, t ≤ 8) and (5,6); Q_w > 1 found at (5,8) and at (6,7), (6,8); (5,7) uncertain.
Control: generic 16 → 1.000; (0,1,4)-shape with split (6,6,4) at (6,8) is the scaled m = 8 failure and is predicted > 1.

## R4-A3 `window20.py` — the window at m = 20 (targeted; ≤ 30 min)
The worst shapes from A2 scaled to m = 20, two-valued splits, {0,1,c} splits near the A2 optimum, plus generic
padding. (k,t): k = 5 (t ≤ 10), k = 6 (t = 7..10), k = 7 (t = 8..10).
Prediction (H2): k = 5 all ≤ 1; k = 6: t = 7, 8 ≤ 1, t = 9, 10 some > 1; k = 7: t = 9, 10 > 1.
Control: generic → 1.000; the scaled (0,1,4)-shape at (7,10) is predicted > 1.

## R4-A4 `gadget_limit.py` — gadget-product limit for the A5 worst cases
R/m = lim (log2 a_k + d)/m (Lemma-R quantity, handoff §3) and the M′ exponent E(α,τ) = lim (log2 a_t − log2 a_k)/m
for products of q generic-separated copies of a block B, by the maximum-entropy formula (own 2-D dual minimiser,
no scipy), at α ∈ {0.0074, 0.02, 0.05, 0.1, 0.2, 0.25} and τ ∈ {α, …, 0.5}; blocks = the A5/A0 worst cases, the three
m = 8 counterexamples, zeros + generic, (0,1,4)-shape. Exact check: q = 2, 3 copies by brute force (m ≤ 18): a_t/a_k
and Q_w, compared with the formula's trend.
Prediction: R/m ≥ 0 at every α (minimum 0 only for the generic block); E(α, τ) ≤ 0 for all α ≤ 1/4, τ ∈ [α, 1/2]
(no hidden 2^{εm} loss in M′ on products); the exact q = 2, 3 values of log2(a_t/a_k)/m decrease toward E.
Control: the generic block gives R/m = 0 and E = 0 exactly; the all-equal block gives R/m = 1 − h(α) + 0 > 0.

### Outcome R4-A0 (`out/window_small.txt`, 19 s)
Controls OK (generic 1.000 at every (k,t); (-3,-3,-2,-2,0,0) at (2,3) = 1.0357). Exhaustive [-3,3] m = 6..10, [-4,4]
m = 6..8, [-5,5] m = 6, 7 (full, no cap): every (m,k,t) with t + 2k <= m has max Q_w <= 1 (boundary t + 2k = m: 0.9556 at
(7;2,3), 0.8970 at (8;2,4), 0.8286 at (10;3,4)); violations exactly at (6;2,3) 1.0417 (the [-5,5] instance
(-5,-4,-2,-1,3,4) has a_3 = a_2 and Q_w = 1.0417), (8;3,4) 1.0300, (10;4,5) 1.0286, all with t + 2k > m. The
(9;3,4) and (10;3,5) cases (t + 2k = m + 1) stay below 1 (0.9298, 0.8550) in these ranges. Per-u ratio > 1 at k = 1
with Q_w < 1 as predicted (e.g. 1.244 at (7;1,3)). H2 survives; H1 and H3 are not yet separated (needs m >= 13).
Addendum (pre-registered before A2): A2 is widened to m = 12..16 because (13;4,6) and (14;4,7) separate H2 from H3.

## R4-A1b `per_rho.py` — the per-relation inequality (pre-registered while A1 runs; run after A1)
Every near miss carries the relation rho = (A\A', A'\A) and every R'-target the relation (Y\Y*, Y*\Y); the rules
S1/S1E/S1P/T stay inside one rho. Per-rho: S(rho) <= T(rho) for every rho, where S, T are the rho-restricted totals.
It is the 'same relation' locality rule (complete bipartite inside each rho) and is sufficient for Q_w <= 1.
Prediction: per-rho holds on every instance with t + 2k <= m (exhaustive [-3,3] m = 6, 7, [-4,4] m = 6, random m = 8),
with max_rho S/T <= 1, and fails on the control (6;2,3) instance. Weaker fallback (if per-rho fails): the per-|P|
aggregated version. Control: (0,0,g1,g2) at (1,2) gives max_rho S/T = 1 exactly (computed by hand in PREREG_R4 H2 note).

### Outcome R4-A1 (`out/charge_flow.txt`, 13 min)
Controls OK: the (6;2,3) control is infeasible under every rule (supply 30 > capacity 27; best rule routes 90 %);
(0,0,g1,g2) at (1,2) is feasible under S1E/S1P/S1 with the explicit proportional map exactly tight (load 1.000);
`free` agrees with the sign of Q_w - 1 on all 152 curated instances. Per-D fails as predicted on the zeros family.
Predictions NOT met: the same-relation repair rules fail widely in range (t + 2k <= m): exhaustive [-3,3] m = 6:
S1 fails on 264 of 924 instances (e.g. (-3,-3,-3,-3,0,0) at (1,2), routed 0.50), m = 7: 2076/1716 (instance,(k,t))
pairs, m = 8 sample: 4599 pairs; S1E/S1P/S2 fail at least as often; C fails most (the collisions at X itself are far
too few). The explicit proportional map has load up to 18. The generous rules T (repaired set with any collision
partner) and V (Hamming vicinity 2|B|) are feasible on every curated instance in range except (0,0,0,g,g,g,g) at
(2,3) (t + 2k = m), where both route 97.6 %: there the near misses of the all-zero X exceed the capacity of all
collisions at Hamming distance 2, so a correct map must move mass to collisions at distance 4 (Y = {z,g,g'} ~
{z',g,g'}), i.e. replace more elements than B. Several T/V "failures" printed as 1.000 were rounding (tolerance
1e-9 with truncated integer capacities); the tolerance is now 1e-6 for later runs. Conclusion: a charging map that
keeps the relation (P,Q) and only repairs B is not viable; the two-valued instances show the charge must go to
collisions with larger relations. Next: the per-relation inequality (A1b) decides whether 'same relation' can work at
all.

## R4-A1c `charge_flow2.py` — rules that charge to collisions whose relation contains rho (pre-registered before run)
Hand computation on the A1 failure (0,0,1,1,1) at (1,2): per-rho fails there (S = 1.5, T = 0.5 for rho = (z1 -> z2)),
but the collisions ({z1,e},{z2,e'}) with relation ({z1,e},{z2,e'}) ⊇ rho carry exactly the missing weight (1.5 in
total, tight). Rules: SUPA (Y ⊇ A, Y∩Q = ∅, Y* ⊇ A', Y*∩P = ∅), SUP (P ⊆ Y\Y*, Q ⊆ Y*\Y), SUPD (SUP and D∩P = ∅),
SUPX (SUP and |Y\X| <= |B| + |P|).
Prediction: SUP is feasible on every instance with t + 2k <= m (exhaustive [-3,3] m = 6, 7; sample m = 8; curated),
with the proportional explicit map NOT always valid (load > 1 somewhere); SUPA fails on some zeros instances; SUPD
and SUPX fail on a few instances each (SUPD on two-valued at k >= 2). Control: (6;2,3) infeasible under every rule;
(0,0,g1,g2) at (1,2) tight under all four.

### Outcome R4-A1b (`out/per_rho.txt`, 5 min)
Controls OK (control fails with max_rho S/T = 2.0; equality case gives exactly 1.000; zeros (0^5,g^3) at (2,4) gives
0.539). Prediction NOT met: per-rho fails on 243/924 instances at m = 6 ([-3,3]), 560/3003 ([-4,4]), on most
instances at m = 7, 8 in range, with ratios up to 6.4 ((0,0,0,0,0,1,1,1) at (2,3)); the |P|-aggregated fallback also
fails (3.33 at (-3,-3,-3,0,1,2,3), (2,3)). So the mass of a near miss with relation rho cannot in general be charged to
collisions with the same relation: any charging map must use collisions with LARGER relations (hand computation:
(0,0,1,1,1) at (1,2) needs the 2-relations ({z1,e},{z2,e'})). Dead end recorded; next A1c.

### Outcome R4-A1c (`out/charge_flow2.txt`, 12 min)
Controls OK (control infeasible under all four rules, best 87.5 %; equality case tight under all four; (0,0,1,1,1)
at (1,2) feasible under all four, as computed by hand). SUP is feasible on all 924 instances at m = 6 and on all
but 77/1716 at m = 7 and 43/641 (sample) at m = 8, always at (k,t) = (2,3) and always narrowly (routes 98.2–99.6 %);
SUPX fails on exactly the same instances, SUPA more often (362 at m = 7), SUPD on almost everything with k >= 2.
Prediction (SUP feasible everywhere in range) NOT met. Min-cut diagnosis (`mincut_diag.py`) on (-2,-1,-1,0,0,1,2,3)
at (2,3): the violator is the near miss X = {-2,-1,-1} (unique 3-sum, f(X) = 1) with A = P = {-1,-1},
A' = Q = {-2,0}; the only collisions supporting rho are Y = {-1,-1,e}, whose sums have 5–9 witnesses, so their
capacity N(D)/f(Y) is diluted below the supply 1.065 per near miss (2.556 supply vs 2.015 capacity on the violator).
The missing mass must go to collisions whose relation is unrelated to rho (e.g. {-2,-1,3} ~ {-1,0,1}). Same picture
on (-6,-5,-2,-1,0,3,4) at (2,3): 12 unique-sum sources, 36 supporting targets, 26.40 vs 25.55.
So: every map that keeps the relation (even as a sub-relation) fails; the obstruction is "k-level relations seen by
t-sets with unique sums" versus "t-level collisions with many witnesses".

## R4-A1d `charge_flow3.py` — rules keyed on the k-sets instead of the relation (pre-registered before run)
DA (D = A, any collision at Y ⊇ A), DAA (D ∈ {A, A'}), YA (Y ⊇ A, any Y*, any D), YAA (Y ⊇ A or Y ⊇ A'),
YPQ (Y ⊇ P or Y ⊇ Q). Prediction: YAA feasible on every instance in range (the supersets of A carry enough
collisions); YA fails on a few; DA fails on many (D = A is often excluded by D ⊉ Y\Y*); DAA fails on two-valued
instances; YPQ feasible wherever YAA is. Control: (6;2,3) infeasible under every rule; equality case tight.

### Outcome R4-A1d (`out/charge_flow3.txt`, 10 min)
Controls OK. DA/DAA (D = A or A') fail widely (192/924 at m = 6). YA and YAA fail on 2/1707 instances at m = 7
((-3,-3,-3,0,1,2,3) and (-3,-2,-1,0,3,3,3) at (2,3), 94.4 %), so the prediction "YAA feasible everywhere" is NOT met.
**YPQ (Y ⊇ P or Y ⊇ Q, any collision partner, any D) has 0 failures** on 924 + 1707 + 76 instances in range (the
m = 8 sample was small because the rule enumerated all targets per source). This is the first rule with no failure.

## R4-A1e `charge_flow4.py` — YPQ at scale (pre-registered before run)
Efficient YPQ edge generation (loop over collision sets Y). Exhaustive [-3,3] m = 6, 7, [-4,4] m = 6; sample m = 8
(5 min) and m = 9 (3 min, k <= 2); curated instances including k = 3 at m = 9 and the zeros/two-valued families.
Also YP (Y ⊇ P only) and YPQ* (Y ⊇ P or Y ⊇ Q, and Y ≠ X) to locate the minimal form.
Prediction: YPQ has 0 failures in range; YP fails on some instances; YPQ* equals YPQ (the collisions at X itself
are never needed, cf. rule C). Proportional map load for YPQ exceeds 1 on some instances (no explicit map yet).
Control: (6;2,3) infeasible (routes 90 %); equality case tight (load 1.000).


## Outcome A1e (partial) — charge_flow4.py, out/charge_flow4.txt
Controls behaved: (6;2,3) routes 0.900 under YP/YPQx/YPQ (must fail: yes); equality case load 1.000; the YAA failure
(-3,-3,-3,0,1,2,3) at (2,3) is YPQ-feasible (prop load 0.953).  All 54 curated instances (m = 7..10, t+2k <= m) are
feasible under YP, YPQx and YPQ; prop-YPQ load max 0.874 (on (-3,-3,-2,-2,0,1,1) at (2,3)).
The run then died of MemoryError on the curated m=9 instance (0,0,0,1,1,1,2,2,2) at (2,3) (dense adjacency in Dinic),
so the exhaustive sections did not run.  Rerun as charge_flow4b.py with an edge-count guard (A1e-b below).
Prediction status: "YP fails on some instances" NOT yet observed (curated list: no YP failure); other predictions pending.

## Pre-registration A1e-b — charge_flow4b.py
Same exhaustive/sampled sections as A1e (m=6 [-3,3] and [-4,4], m=7, sample m=8, sample m=9 with k <= 2), skipping cases
whose src x tgt count exceeds 1.5e6 (count reported).  Prediction unchanged: YPQ 0 failures; YP fails on some m >= 7
instances; prop-YPQ load > 1 on some instance.  Budget ~17 min.

## Outcome A2 — window.py, out/window.txt (99 s)
Controls: generic m=12 gives Q_w = 1.000000 at all 10 (k,t) pairs (ok).  Control 2 FAILED AS A CONTROL: the m=8
failure shape {0,1,4} split (3,3,2) scaled to (6,6,4) at m=16, (6,8) gives Q_w = 0.771, not > 1 — proportional scaling
does not preserve a violation (consistent with the gadget-product finding A4 that violations die under products).
Families (two-valued + all {0,p,q} splits at m=12,13,14; two-valued + {0,1,c} at m=15,16; generic padding):
  every violation has k = m/2 - 1, t = m/2 (k/m >= 0.417): m=12 (5,6) 1.0301; m=14 (6,7) 1.0268; m=16 (7,8) 1.0230;
  m=13, 15: none.  Window k/m in (1/4,1/3): max Q_w = 0.7544 at (13;4,5), 0.7414 at (14;4,5), 0.6826 at (15;4,5),
  0.7483 at (16;5,6).  Discriminators: (13;4,6) 0.732 (H2 open), (14;4,7) 0.696, (16;5,7) 0.672, (16;5,8) 0.714:
  all < 1, so H1 is not sharp in these families; H2 and H3 both survive (no violation with t+2k <= m, none with k < m/3).
  Beyond: (12;4,6) 0.837 (k = m/3), (15;5,6) 0.805 (k = m/3), (16;6,8) 0.930 (k/m = 0.375, t+2k-m = 4).
Prediction check: pre-registered "some > 1 strictly inside the window (1/4,1/3)" was NOT observed; the window is clear
in these families.  Honest reading: the m=8 violations at k/m = 0.375 do not persist at m=12..16 for the same
value-set families; the m=16 worst at k/m=0.375 is 0.93.

## Outcome A4 — gadget_limit.py, out/gadget_limit.txt (9 s)
Controls: generic block gives R/m = 0 and E = 0 at all (alpha,tau) (ok, to 1e-4); all-equal block gives R/m > 0, E < 0.
All ten A5/A0/counterexample/zeros/two-valued blocks: R/m >= +0.1165 at alpha <= 1/4 (the minimum over the table is the
all-equal control; the A5 worst cases give 0.1617-0.1791 at alpha = 1/4, larger at smaller alpha) and
max E(alpha,tau) = +0.0000 (attained only at tau = alpha).  So in the product limit there is no 2^{eps k} loss:
a_t/a_k decays exponentially in m for every tau > alpha and R/m is bounded away from 0.
Exact products: A5 m=6 worst Q_w = 1.036 (q=1) -> 0.944 (q=2, (4,6)) -> 0.882 (q=3, (6,9)); A5 m=8 worst 1.030 ->
0.882 (q=2); counterexample 1: 1.079 -> 0.857; A0 m=10 worst 1.029 -> 0.937 (q=2, m=20, (8,10)).  Violations are
single-block phenomena; they shrink monotonically under products.  Prediction (R/m > 0, E <= 0, Q_w decreasing under
products) met; "some product with Q_w > 1 at the scaled (k,t)" NOT observed.


## Outcome A1e-b — charge_flow4b.py, out/charge_flow4b.txt (13 min)
Exhaustive [-3,3] m=6 (924 multisets, 1834 (k,t)-cases), [-4,4] m=6 (3003, 5838), [-3,3] m=7 (1716, 5146); sample
m=8 (116 multisets, 547 cases, 33 dense cases skipped by the src*tgt guard, largest (0,0,0,0,2,2,2,2) at (2,4));
sample m=9 k<=2 (80 multisets, 296 cases, 104 skipped).  **0 failures for YP, YPQx and YPQ on all 13,661 cases**
(worst routed fraction 1 - 3e-10); free = 0 failures (consistent with A0: no Q_w > 1 in range).
Predictions: "YPQ 0 failures" MET; "YP fails on some m >= 7 instances" NOT met (YP never failed, so the smaller rule
is the surviving candidate); "prop-YPQ load > 1 somewhere" MET (1.126 on (-3,-3,-2,-2,0,3,3) at (2,3)).
Caveat recorded: the skipped dense cases at m = 8, 9 are untested.

## Outcome A3 — window20.py, out/window20.txt (26 min)
Controls: generic m=20 gives 1.000000 at (5,6), (6,8), (7,10) (ok).  Control 2 FAILED AS A CONTROL: all-equal weights at
(9,10) give 0.909, not > 1 (the (9,10) violations need three values).
Families: two-valued (10), {0,1,5} parts>=3 (60, cap), {0,1,4} (44, cap), {0,1,2} (35, cap), {0,2,5} parts>=4 (26),
{0,4,5} (26), scaled (-3^3,-2^3,1^2) and A0 m=10 shapes (6), worst {0,1,c} shapes with 2 or 4 generic replacements (12).
Max Q_w: (5,6) 0.606, (5,10) 0.397, (6,7) 0.695, (6,8) 0.577, (6,9) 0.556, (6,10) 0.612, (7,8) 0.793, (7,9) 0.749,
(7,10) 0.820, (8,9) 0.902, (8,10) 0.970, (9,10) 1.0240 (0^6 1^4 5^6 + 4 generic; also 1.0168 for 0^8 1^4 5^8,
1.0129 for 0^7 2^4 5^9 and 0^7 4^4 5^9, exactly 1.0000 for 0^10 1^10).  Every maximiser below (9,10) is a generic-padded
{0,1,5} shape; padding adds 0.05-0.1.
Prediction (k=6: t=9,10 some > 1; k=7: t=9,10 > 1) NOT met: nothing below k = 9 reaches 1 at m = 20.  H1, H2, H3 all
unviolated; the window (1/4,1/3) has max 0.695; violations at m = 12..20 only at k = m/2 - 1, t = m/2.
