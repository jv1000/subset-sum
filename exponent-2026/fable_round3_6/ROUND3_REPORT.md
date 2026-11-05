# Round 3 report: Conjecture M′, Section T v2, and the routes past the floor

Claude Fable 5.1, 4 Nov 2026, working as a collaborator. Discipline as before: every experiment is pre-registered in
`scripts/round3/PREREG_R3.md` (prediction and control before the run, outcome appended); every claim is labelled
PROVED, EVIDENCE or CONJECTURE; dead ends are kept with the reason. `paper_v2.md` was not edited. Scripts in
`scripts/round3/`, outputs in `scripts/round3/out/`; one process at a time, every run under 10 minutes.

## Summary table

| Item | Status | Result |
| --- | --- | --- |
| 1. Conjecture M′ (a_t ≤ poly·a_k, t ∈ [k, m−k], k ≤ c·m) | **open; reduced, not proved** | PROVED: M′ with the loss 2^k (three proofs, P2), M′ trivially for bounded k (P1), the near-miss lemma (P5), and an exact reduction of the sharp form to one charging inequality (A.3 (ii)). CONJECTURE Q (new, canonical, witness-free): cp(μ)·a_t·C(m,k) ≤ 1 for k ≤ m/4, which implies a_t ≤ a_k. EVIDENCE: 0 violations in ≈ 100,000 instances incl. exhaustive [−3,3] m ≤ 10 and a hill-climb; fails only for k ≥ m/3 (max 1.079). Direction (i) is equivalent to M′ on every instance (P* = a_t/a_k), direction (iii) reduces to (ii). |
| 1′. Exact monotonicity inside (a_{j+1} ≤ a_j, j+1 < m/2) and M′ with P = 1 for k ≤ m/4 | EVIDENCE strengthened | no interior violation in 400,000 random instances m = 10..14 (middle step included) and in a hill-climb seeded with the m = 8 counterexample (m = 8..13); the middle-step worst case stays the known 92/90 at m = 8 and nothing at m ≥ 9 |
| 1″. [S] directly (small k vs cube) | EVIDENCE | a_k·2^{d(M)} ≥ 1.00 in all 2,655 instances m = 12..16 (minimum at near-generic weights); the sufficient tail condition holds with factor ≥ 30 to spare |
| 2. Section T v2 | DONE (`SECTION_T_v2.md`) | trial count C_S(m)·n⁸⌈2^{d(M)}⌉, C_S polynomial; "C_S = 3" remark removed; 28 changed lines, no numerical condition changes |
| 3. Scoping memo (routes past the floor) | DONE (§C) | five designs priced in the fixed-Δ model: the floor is a variance floor; capacity Δ is the only lever (0.485 needs Δ ≥ 0.030 at zero alias overhead, format saturated at 0.0287); D1, D3, D4, D5 killed with reasons; ceiling without any per-class operation 0.4522 |

---

## A. Conjecture M′

### A.1 Notation and the reductions used

Weights w ∈ ℤ^M, |M| = m. Σ_j = distinct j-subset sums, s_j = |Σ_j|, a_j = s_j/C(m,j), 2^{−d} = |Σ(M)|/2^m.
Fibers: f_j(u) = #{A : |A| = j, w(A) = u}, W_j(u) the set of those A. A *balanced relation of level j* is an ordered pair
(P,Q) of disjoint j-sets with w(P) = w(Q), j ≥ 1; Λ_j is the set of them. A set X *sees* (P,Q) if P ⊆ X and Q ∩ X = ∅;
then X′ = (X∖P) ∪ Q has |X′| = |X|, w(X′) = w(X), and (P,Q) ↦ X′ is injective (P = X∖X′, Q = X′∖X). Hence
f_j(w(X)) − 1 = #{(P,Q) ∈ Λ_{≤ j} seen by X} =: Z_j(X), and for the cube F(T) − 1 ≥ Z(T) := #{(P,Q) ∈ Λ seen by T}
(the cube fiber also contains the unbalanced swaps). Averages: a_j = E_X[1/f_j(w(X))] (X uniform j-set),
2^{−d} = E_T[1/F(T)] (T uniform subset).

Lemma S (round 2): M′ with polynomial P(m) ⟹ [S] with C_S = P(m) + 2 for k ≤ 0.11m. Section T v2 needs nothing more.

### A.2 What is PROVED tonight (all elementary; each checked numerically in `free_bounds.py` / `sparse_tail.py`)

**P1 (M′ is trivial for bounded k).** a_t ≤ 1 ≤ C(m,k)·a_k, so M′ holds with P = C(m,k) ≤ m^k. For k = O(1) this is a
polynomial; the content of M′ is entirely in k → ∞ with m, uniformly in k ≤ cm. (The application has k ≈ 0.007m.)

**P2 (the free bound, with a 2^k loss).** For all k ≤ t ≤ m−k:
  a_t ≤ a_k · C(m, t−k)/C(m−k, t−k),   i.e.   s_t·C(t,k) ≤ s_k·C(m, t−k).
*Proof.* Fix one witness X_y per y ∈ Σ_t. The map (y, A) ↦ (w(A), X_y∖A), A ⊆ X_y, |A| = k, is injective: from
(u, B) recover y = u + w(B), then A = X_y∖B. The domain has s_t C(t,k) elements, the codomain at most s_k·C(m,t−k).
Then use C(m,t)C(t,k) = C(m,k)C(m−k,t−k). ∎
The loss L = C(m,t−k)/C(m−k,t−k) = Π_{i<k}(m−i)/(m−t+k−i) is ≈ 2^k at t = m/2 (exactly 2^k·poly), and P2 is an
equality for generic weights up to the factor L. The same bound follows from the entropy chain
H(w(A)) ≥ H(w(A) | w(X_Y∖A)) and from the Johnson-graph coupling; every route that puts A *inside* a witness of y
loses exactly this factor, because the codomain lets B meet A. The loss is exactly the "support ≤ m/2 + k" barrier of
Base's Corollary D, now seen as a statement about M′. With k = 0.007m the loss is 2^{0.007m}, which costs ≈ a′μ ≈ 0.0033
in the exponent, fourteen times the ternary gain: for the application P2 is worthless, [S] must be lossless.

**P3 (fiber-size bound).** a_t ≤ a_k·max_u f_k(u). *Proof.* In P2 the multiplicity of u in the image is at most
Σ_{A ∈ W_k(u)} C(m−k,t−k) because B must avoid A for (u,B) to be in the image. ∎ (Useless when fibers are large.)

**P4 (restriction bound).** a_t ≤ E_B[a_k(M∖B)], B a uniform (t−k)-set. *Proof.* The image of P2 lies in
∪_B {(u,B) : u ∈ Σ_k(M∖B)}. ∎ This is exact at the level of sets, but E_B a_k(M∖B) can exceed a_k(M) by 2^k
(two-valued weights), so P4 cannot be a step towards M′ although M′ holds there with room.

**P5 (near-miss lemma, cube).** For every T ⊆ M with |T| ≥ k:
  Σ_{T′ ⊆ T, |T∖T′| ≤ k} (F(T′) − 1) ≥ (1/C(|T|−1, k−1)) · Σ_{A ⊆ T, |A| = k} (f_k(w(A)) − 1).
*Proof.* Σ_{A⊆T} Z_k(A) = Σ_{(P,Q) ∈ Λ_{≤k}, P ⊆ T} C(|T| − j − q, k − j), q = |Q ∩ T|, and each term is ≤ C(|T|−1,k−1)
(j ≥ 1). Every such (P,Q) is seen by T′ = T ∖ Q, a subset of T at distance q ≤ k, and is counted in F(T′) − 1. ∎
Interpretation: if the k-layer is collapsed (most A see many relations) then every cube set has many relations in its
k-neighbourhood below it ("near misses": P ⊆ T, Q partly inside T). What is missing for [S] is a smoothness statement
that moves hits from the neighbourhood to T itself with at most polynomial loss; the per-set version is false
(two-valued weights: T = all zeros has F(T) = 1 while every k-set has fiber ≥ C(m/2,k)), so it must be a measure statement.

**P6 (the two forms that would give M′ with a polynomial, both PROVED as implications).**
(i) *Flow form.* Let H be the bipartite graph Σ_t ∼ Σ_k with y ∼ u iff some witness of y has a k-subset of sum u.
If every y can send one unit of flow to its neighbours with load ≤ c at every u, then s_k·c ≥ s_t, so with
c = P·C(m,t)/C(m,k): a_t ≤ P·a_k. P*(M;t,k) := the least such P. Always P* ≥ a_t/a_k; P* = 1 for generic weights;
P*(8;4,3) ≥ 96/95 at the round-2 counterexample.
(ii) *Second-moment form.* With one witness X_y per y and mult(u) = #{(y, A ⊆ X_y) : w(A) = u},
Q(t,k) := Σ_u mult(u)²/(s_t C(t,k) C(m−k,t−k)) satisfies s_k ≥ (Σ mult)²/Σ mult² = s_t C(m,k)/(C(m,t)·Q), so Q ≤ P ⟹ M′
with P. Q = 1 for generic weights (every mult(u) = C(m−k,t−k)). For *any* witness rule mult(u) ≤ C(m,t−k) (for a fixed
B at most one A ∈ W_k(u) has A ∪ B canonical), which is P2 again; a polynomial bound on Q needs the witness rule.

### A.3 The three directions, each reduced to one missing statement

**(i) Flow / Hall with poly slack.** The flow form P6(i) is *equivalent* to M′ on every instance tested: P* = a_t/a_k to
the search tolerance (A3). So Hall's condition on the shadow graph is never the obstacle; a proof of M′ by flows would
have to construct the fractional matching from the structure, and the natural uniform rules fail (round 2, A.5 item 5).
No new rule found. Direction (i) adds nothing beyond the reformulation; dropped.

**(ii) Second-moment form with the k-layer as base (the productive one).** The canonical version needs no witness rule:
let π draw y uniformly from Σ_t, X uniformly from the witnesses of y, A uniformly from the k-subsets of X, and let μ be
the law of w(A). Then (PROVED, Cauchy–Schwarz on the support)
  s_k ≥ 1/cp(μ),  so  cp(μ) ≤ 1/(a_t·C(m,k))  ⟹  a_t ≤ a_k,
and more generally cp(μ) ≤ P/(a_t C(m,k)) ⟹ M′ with P. Put Q_w := cp(μ)·a_t·C(m,k) (= 1 for generic weights; the
witness-rule version Q of P6(ii) satisfies Q_w ≤ E_rule Q by convexity).

**Conjecture Q (CONJECTURE).** Q_w ≤ 1 for all k ≤ m/4 and t ∈ [k, m/2]. (It is *false* for k ≥ m/3: Q_w = 1.036 at
m = 6, (k,t) = (2,3), w = (−3,−3,−2,−2,0,0), where a_t/a_k = 0.875; 1.011 at m = 12, (4,6); 1.079 at the m = 8
counterexample, (3,4). So the k ≤ m/4 range is not a convenience but part of the statement; between m/4 and m/3 I have
no data point either way beyond m ≤ 12.) Evidence: A2 (Q_lex ≤ 1, exhaustive [−3,3] m ≤ 10 and random m ≤ 13, k ≤ m/4),
A5 (Q_w ≤ 1 exhaustive [−3,3] m ≤ 10, 59,233 random m = 8 in [−6,6], random m = 11, 12: 0 violations with k ≤ m/4) and
A6 (hill-climb maximising Q_w: 0.84, 0.75, 0.69 at m = 9, 10, 11). In every instance Q_w − a_t/a_k ≤ 0.1: the
second-moment form is nearly tight, i.e. μ is nearly uniform on its support, which is itself a structural fact worth
proving (it says the k-subsums of t-witnesses are equidistributed over Σ_k up to constants).
Consistency: Q_w = cp(μ)a_tC(m,k) ≥ a_t/a_k, so at the m = 8 counterexample Q_w(4,3) ≥ 96/95; and the trivial fact
"all t-sums distinct ⟹ all k-sums distinct (t ≤ m−k)" is exactly the case a_t = 1 of Conjecture Q.

**Reduction (PROVED).** With N_w(A) := Σ_{X ⊇ A, |X|=t} 1/f_t(w(X)) (so Σ_A N_w(A) = s_t C(t,k), N_w(A) ≤ C(m−k,t−k)),
  Q_w ≤ 1  ⟺  Σ_{A ≠ A′, w(A)=w(A′)} N_w(A)N_w(A′) ≤ Σ_A N_w(A)·(C(m−k,t−k) − N_w(A)).
The left side is w(L), L = {(X,X′,A ⊆ X,A′ ⊆ X′): |A|=|A′|=k, A ≠ A′, w(A)=w(A′)} with weight 1/(f(X)f(X′)); the right
side is w(R), R = {(Y,Y*,Y″,D): w(Y*)=w(Y), Y* ≠ Y, D ⊆ Y∩Y″, |D|=k} with weight 1/(f(Y)f(Y″)) (both of size t).
The swap map Φ(X,X′,A,A′) = (Y = (X∖A)∪A′, Y* = X, Y″ = X′, D = A′), defined when A′∖A is disjoint from X, is a
weight-preserving injection of L₁ := {A′∖A ∩ X = ∅} onto exactly {r ∈ R : D ⊇ Y∖Y*}. Hence
  **Q_w ≤ 1  ⟺  w(L^{nm}) ≤ w(R′)**, L^{nm} = {ℓ ∈ L : (A′∖A) ∩ X ≠ ∅} (the near misses), R′ = {r ∈ R : D ⊉ Y∖Y*}.
R′ contains every t-level collision whose swap has more than k elements, so it has a lot of mass; L^{nm} consists of
k-level relations (P,Q) with P ⊆ X but Q partly inside X, which are precisely the relations that P5 moves to a
neighbour of X. What is missing is a weight-preserving injection (or a fractional one) from L^{nm} into R′. The
mirror map (swap on the X′ side) lands inside the image of Φ, so it does not help. The per-u version
mult_w(u) ≤ C(m−k,t−k) is false (eight zeros + four generic weights, u = 0: 88 > 84), so the injection must use the
averaging over (X, A), i.e. it must charge near misses of X to collisions of *other* t-sets.
What is PROVED along the way: mult_w(u) ≤ C(m,t−k) for every u (so Q_w ≤ C(m,t−k)/C(m−k,t−k) ≈ 2^k, i.e. P2 again).

**(iii) Sparse-layer relation picture + lower tail.** The near-miss lemma P5 is the rigorous part of the picture: a
collapsed k-layer forces every cube set T to have Σ_{A ⊆ T}(f_k(A) − 1)/C(|T|−1,k−1) relations within distance k below
it. The missing statement is a *measure* lower tail: P_T[F(T) < 1/(a_k m)] ≤ a_k (which gives [S] with constant m+1
through 2^{−d} = E 1/F ≤ P[F < L] + 1/L). The per-A coupling T ⊇ A cannot give it (each relation seen by A survives in
T with probability 2^{−|Q|}, and Jensen goes the wrong way), the per-set version is false (two-valued weights, T = the
zeros), and Janson-type inequalities do not apply because "T sees (P,Q)" is a mixed cylinder event. Numerically the
tail statement holds with room (A4). I see no proof route that is not equivalent to (ii).

### A.4 Evidence (all EVIDENCE; pre-registrations and outcomes in `scripts/round3/PREREG_R3.md`)

| Run (script, output) | Instances | Quantity | Result |
| --- | --- | --- | --- |
| A0 `free_bounds.py` | 6,435 (exhaustive [−3,3] m ≤ 8; random m = 9, 10) | P2, P3, P4 ratios | all ≤ 1 (theorems; harness check); P2 tight only for generic |
| A1 `approx_mono.py` | 400,000+ random, m = 10..14, uniform/cluster, R ≤ 40 | max a_{j+1}/a_j over j+1 ≤ m/2 (middle step included); interior; μ′ (k ≤ m/4) | 1.000 / 1.000 / 1.000: no violation; control 96/95 reproduced |
| A2 `cs_rep.py` | exhaustive [−3,3] m = 6..10; random m = 11..13 | Q_lex, k ≤ m/4 | Q_lex ≤ 1 everywhere, within a few % of a_t/a_k; generic Q = 1 |
| A3 `hall_flow.py` | exhaustive [−3,3] m = 6..9; random m = 10..12 | P* (flow constant) | P* = a_t/a_k ± 1e-3 on every instance; P*(8;4,3) = 1.0107 |
| A4 `sparse_tail.py` | 2,655 random/planted, m = 12..16, k ≤ m/4 | a_k 2^d (m+1); tail; P5 | min a_k 2^d = 1.00–1.02 (near-generic); tail ≤ 0.033; P5 never fails |
| A5 `cs_w.py` | exhaustive [−3,3] m = 6..10 (18,284); 59,233 random m = 8 in [−6,6]; random m = 11, 12; the 3 counterexamples | Q_w all k < t ≤ m/2 | **Q_w ≤ 1 for k ≤ m/4: 0 violations**; Q_w > 1 only for k ≥ m/3 (max 1.079) |
| A6 `hill.py` | hill-climb, 182–468 restarts per m, m = 8..13, seeded with the counterexample | max interior ratio; max middle ratio; max Q_w (k ≤ m/4) | 1.000 at m = 8 only, ≤ 0.92 at m ≥ 9; middle 1.0222 (= 92/90) at m = 8, ≤ 1 at m ≥ 9; Q_w ≤ 0.84 |

Pattern. Everything points the same way: (1) a_t ≤ a_k holds for k ≤ m/4 with room, and the only failures of exact
monotonicity are the known m = 8 middle-step ones; (2) the canonical second-moment form holds with constant 1 in the
same range and is nearly tight; (3) the cube version [S] holds with a_k 2^d ≥ 1, minimised by generic weights. What the
data cannot say is whether Q_w ≤ 1 survives at k/m ∈ (1/4, 1/3) for larger m, and whether a 2^{εk} loss could hide at
m ≤ 16 (it cannot be distinguished from poly there, but the planted-relation instances with k = 4 and the handoff's
gadget-product limits both show no exponential loss).

### A.5 Dead ends of tonight (kept, with reasons)

1. *The witness-inside coupling in all its forms* (injection (y,A) ↦ (w(A), X_y∖A); entropy chain H(w(A)) ≥
   H(w(A)|w(X∖A)); Johnson coupling T ⊇ A): each loses exactly C(m,t−k)/C(m−k,t−k) ≈ 2^k because the k-set A is
   correlated with the rest of its witness by k bits of disjointness. Proved as P2 and then abandoned as a route.
2. *Per-u multiplicity bound mult_w(u) ≤ C(m−k,t−k)*: false (eight zeros + four generic weights, u = 0: 88 > 84), so the
   second-moment inequality cannot be proved term by term; it needs the π-average.
3. *Per-X bound (Kc)(X) ≤ C(m,t)/C(m,k)* (which would give Q_w ≤ 1 by c^TKc ≤ (Σc)·max Kc): false for the same instance
   (X = six zeros).
4. *The mirror swap Φ₂* for the near-miss terms: its image lies inside the image of Φ₁, so it charges nothing new.
5. *Direction (i) as an independent route*: Hall's condition holds with the exact constant, so flows only restate M′.
6. *Per-set lower tails for the cube* (pointwise f_t(X) ≥ F/poly, or F(T) ≥ F/poly): false (two-valued weights, the
   all-zero set), so (iii) must be a measure statement, and the only measure statement I can formulate is (ii).
7. *Extending Conjecture Q beyond k ≤ m/4*: false at k = m/3 (A5), so no "monotone in k" strengthening is available.
8. *Plünnecke/unrestricted sumset bounds* (Σ_j ⊆ Σ_k + Σ_{j−k}): lose the overlap factor C(m,k)C(m,j−k)/C(m,j); M′ is the
   sharp restricted statement itself.

### A.6 What remains / what I would do next

1. **Prove Conjecture Q for k ≤ m/4.** The exact target is the charging inequality w(L^{nm}) ≤ w(R′) (A.3 (ii)); the
   near-miss lemma P5 shows where the mass of a near miss (P ⊆ X, Q partly in X) goes (to X ∖ Q), and R′ contains all
   t-level swaps of size > k. I would look for a fractional map from a near miss (X, P, Q, X′) to t-level collisions of
   the sets X ∖ (Q∩X) ∪ E (E ⊆ M ∖ (X ∪ Q), |E| = |Q ∩ X|), whose weights 1/f sum correctly on average over E; the k ≤ m/4
   restriction should enter through |E| ≤ k ≤ m/4 leaving room (m − t − k ≥ k). Test every candidate map on the A5 harness
   (the m = 6 instance (−3,−3,−2,−2,0,0) at (2,3) is the smallest case where Q_w > 1, and must *not* be charged).
2. Decide the k/m ∈ (1/4, 1/3) window numerically at m = 16, 20 with targeted families (two-valued plus generic, the
   (−3,−3,−3,−2,−2,−2,1,1) shape) before investing in a proof that claims more than m/4.
3. Keep the gadget-product limit (handoff §3) as the test that excludes a 2^{εk} loss: compute R/m for the product of the
   A5 worst cases.
4. For the paper: state M′ with the explicit evidence table, state Conjecture Q as the sharp form, and cite P2 as the
   proved 2^k-lossy version (with the remark that the loss is exactly Base's Corollary D barrier).

---

## B. Section T v2 (DONE)

`SECTION_T_v2.md` = Section T with: [S] stated with a polynomial constant C_S(m) (Conjecture M′ + Lemma S gives
C_S = P(m) + 2); T := C_S(m)·n⁸⌈2^{d(M)}⌉ (T.2 Step 3); Lemma T5 unchanged (it is stated for any C_S); Corollary T6
now misses a class with probability ≤ (1 − 2^{−d}/(C_S n^6))^T ≤ e^{−n²} with no "n ≥ C_S" cutoff; Lemma T7's trial bound
T ≤ 2n^{8+c_S}2^{d(M)} (the polynomial goes into 2^{O(n^{0.6})}); the (SR) row cites Conjecture M′; the cutoff remark no
longer claims C_S = 3. No numerical condition changes, so `candidate_ternary.json` and its certificate are unaffected.
Generated by `scripts/round3/make_section_t_v2.py` (each replacement asserted to match exactly once).

---

## C. Scoping memo: designs that avoid one dictionary operation per alias class

Pricing model: the fixed-Δ alias-budget model of round 1 (`scripts/section9_check.py`, checked against Base's C1–C8
there; copied into `scripts/round3/floor_designs.py`, output `out/floor_designs.txt`). τ0 = max(c2, c3, c4, c5) with
c4 = (1 − Δ + overhead)/2 the alias-class term; Δ = 0.0287 (certified point). Reference values of the model:

| Model variant | τ0 | What it prices |
| --- | --- | --- |
| round-1 model, Δ = 0.0287 (control) | 0.4875741 | reproduces the Section 8 point to 1e-6 |
| overhead removed, per-class operation kept | 0.4856515 = (1−Δ)/2 | the floor |
| **no per-class operation at all** (c4 dropped) | **0.4521547** | ceiling of any design that keeps the lists/masks; C2 = C3 = C5 bind at μ = 0.412, a = 0.080 |
| c4 halved (√-aggregation, if group sums were free) | 0.4521547 | same ceiling (c4 no longer binds) |
| coarse matching at modulus η − δ, δ = 0.005 / 0.01 / 0.02 | 0.48967 / 0.49179 / 0.49611 | worse by δ/2 |
| Δ = 0.030 / 0.035 / 0.0415 (Lemma-1 cap at τ = 0.485) | 0.48703 / 0.48496 / 0.48231 | floors 0.4850 / 0.4825 / 0.4793 |

Reading: the per-class term is the only thing standing between 0.4857 and 0.452 in this model, so breaking the premise is
worth far more than any refinement; but every concrete way of breaking it that I can formulate needs a lemma that does
not exist, and the one lever that needs no new lemma (capacity Δ) is numerically saturated. Designs, kill-or-keep:

**D1. Different moduli for extraction and checksum (P₁ for alias extraction, P₂ for the filtered checksum).**
Breaks premise (2) of the floor ("checksum at the same modulus"). Price if fully decoupled: c4 → ≈ 0 (η₁ can grow until
the prime-draw constraint η₁/2 < τ0), i.e. the 0.4522 ceiling. Needs: a checksum identity that certifies the alias
extraction mod P₁ using filters mod P₂ ≠ P₁. Why I do not believe it exists: an alias mod P₁ (w(I) ≡ t mod P₁) is not an
alias mod P₂ and conversely; the checksum's Fourier identity (OpenAI checksum.tex) compares the counted phase sums with
an estimate of the *same* residue class, and a class mod P₂ ⊂ P₁ restricted to the class mod P₁ is exactly a checksum
mod P₁ again. CRT-structured P₁ = P₂P₃ reduces to the same. **Kill** (unless someone exhibits a cross-modulus identity).

**D2. A better estimator of the alias mass (larger Δ).** The filtered checksum *is* the estimator that subtracts aliases
without listing them; its capacity Δ is the floor's only parameter, and D2 does not break the premises, it moves the
floor: 0.485 needs Δ ≥ 0.0300 at zero overhead (0.0310 for 0.4845), and the full-overhead point needs Δ ≈ 0.035.
Lemma 1 caps the trigonometric-moment format at Δ ≤ 0.0415 (τ = 0.485), so 0.485 is not excluded. Needs: either a filter
beyond what 32 cos/sin coefficients give (K = 8 → 16 moved Δ from 0.0284 to 0.0287, i.e. the format is saturated at
≈ 0.029), or a checksum format outside the moment family with its own Lemma 1. **Keep, low probability**: it is the only
route whose ceiling lies below 0.485 without a structural lemma, but the evidence says a format change, not more
coefficients, is required, and nobody has a candidate format.

**D3. Aggregating alias classes by a coarser key.** Three versions. (a) Match left and right records at a coarser modulus
η − δ: the number of matching pairs grows by 2^{δn} and the pairs *are* the alias records, so the per-class term gets
worse by δ/2 (priced above). **Kill.** (b) Aggregate after matching: the operation count is the number of pairs, already
spent. **Kill.** (c) √-aggregation (groups of 2^{(1−η)n/2} classes, one operation per group plus one per class in the
target's group): requires the phase sum of a whole group to be produced without visiting its pairs, i.e. a restricted
convolution of the two value maps over a residue group, which costs the number of pairs in the group again. Price if an
oracle existed: 0.4522 (c4 no longer binds). Needs: a "group phase-sum oracle"; none known. **Kill.**

**D4. Convolution instead of listing (FFT of the two value maps mod P″, cost 2^{η″n}).** Breaks premise (1). With
η″ ≤ τ0 the FFT is affordable and the checksum budget η″ − τ_cs ≤ Δ is trivial, but the convolution returns
solutions + aliases mod P″ with no way to separate them: the extraction works because listed aliases carry their exact
sums. Counting mod two coprime moduli gives marginals, not the joint count. Needs: a separation mechanism that is not
listing. **Kill** as stated; it becomes D2 if the separation is done by an estimator.

**D5. Sign-randomised phase sums (aliases as zero-mean noise, no subtraction).** Breaks premise (1) in the most direct
way: never list aliases, let their contributions cancel. Variance = number of aliases 2^{(1−η)n}, so detecting one
solution needs 2^{(1−η)n} independent repetitions: the floor reappears as a variance floor. This is the real content of
the floor: any estimator that treats the 2^{(1−η)n} aliases as unstructured noise pays their count; the Fourier checksum
beats it only by its structured cancellation, measured by Δ. **Kill**, and it explains why D1–D4 fail.

(Representation-technique list shrinking, Ye–Li partial match: they lower C2/C3/C5, which are slack at the floor, and
only matter once a floor-breaking design exists; then the 0.4522 ceiling is theirs to lower. Not a route to 0.485 by
themselves.)

**Bottom line.** Within the OpenAI/Base architecture the floor is a variance floor and Δ is the single lever; the honest
route to 0.485 is a checksum format with capacity ≥ 0.030 at zero alias overhead (which also needs the whole C4 overhead
gone: the ternary step removed an eighth of it). A route that avoids the variance floor altogether has to count solutions
without treating aliases as noise, and no such mechanism is known to me. Recommendation: spend effort on (i) a format
change for the checksum (a Lemma-1-type cap for candidate formats is cheap to compute before building anything) and (ii)
finishing M′, which is the only *proved-conditional* gain on the table; do not spend it on D1, D3, D4.

---

## Choices made (log)

1. Ran the numerical probes sequentially in one background process each time (two chains, ≤ 8 minutes per script), so
   that every intermediate inequality had a harness before I believed it; Dinic max-flow written by hand (no scipy).
2. Wrote Section T v2 by exact-match substitution (script, 8 replacements each asserted unique, LF line endings kept)
   rather than by hand, so the 28-line diff is auditable.
3. After the user's mid-run note I checked that the m = 10–14 monotonicity sweeps included the middle step (they did:
   max over j+1 ≤ m/2) and that Q_lex had been restricted to k ≤ m/4 (it had); Q_w was then run on all k < t ≤ m/2
   including the three known counterexamples as positive controls, and the hill-climb prints the control first.
4. Chose the canonical (witness-free) Q_w over rule-dependent Q as the conjecture to state, because Q_w ≤ E_rule Q and it
   needs no choice; recorded that the pre-registered prediction "Q_w > 1 only at the middle step" was wrong (it fails
   from k = m/3 on) and restated the conjecture with the k ≤ m/4 cut that the data support.
5. Priced the floor designs in the round-1 model unchanged (no re-optimisation of the filter), so the numbers are
   comparable with REFEREE_REPORT item 4b; verdicts are mine and are labelled kill/keep, not certified.
6. Did not touch `paper_v2.md`; did not edit the round-2 files except to add `scripts/round3/`.
