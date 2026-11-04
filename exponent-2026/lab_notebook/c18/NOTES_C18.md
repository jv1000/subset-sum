# C18 (exploratory, not pre-registered as a test): "small layers are robust"
- **Reduction (proved, by a counting identity):**
  - In Base's alias step the two-part (ternary) family is the k′-subset sums of the alias's fixed signing, subject to
    |U ∩ S| = k1.
  - Hence E_S[fraction of distinct sums in the family] ≥ a_{k′}(M).
  - Conjecture R: a_k(M) ≥ 2^{−d(M)}/poly(m) for k ≤ α0·m. If R holds, ternary masks fit inside Base's existing trial
    budget, and Corollary D and C7 are not needed.
- **Failed proof routes:**
  - single-element injection: compounding m/(m−j) per step;
  - sumset with Base's Corollary D on both halves: pays g twice;
  - covering from the good layer: loses (1 − t/m)^k, i.e. k bits mid-cube.
- **Asymptotic test (gadget.py):** M = q generic-separated copies of a gadget. R/m = lim (log2 a_k + d)/m, computed by
  maximum entropy.
  - Structured gadgets at α ≤ .02 (equal pairs, ± pairs, all-equal, AP, ±AP, 1,1,2, a+b=c+d, zeros): +0.13 to +0.67.
    Generic gives exactly 0.
- **Adversarial hill-climb (search.py; logs s_0074.log, s_02.log, s_1.log):** 12 restarts × 250 moves, gadgets b ≤ 9,
  at α = .0074, .02 and .1. Minimum R/m = 0.000 in all three, attained only by collision-free (generic) gadgets. No
  negative found. Structured optima are positive (up to +0.15).
- **Run note (20:00 ET):** all three searches COMPLETED. The background "exit code 1" came from my wrapper's final
  `tail -3 file1 file2 file3`, an invalid option form here. It is the same slip as in C13; logged. The separate
  wait-loop was stopped by the user interface, not by the job.
- **Caveat:** the gadget class is products of small blocks. It includes the repetition families, but not every
  weighting. No proof yet.

## C18b (21:40 ET): towards a proof of Conjecture R; current state
- **Inverse-fiber form (exact):**
  - a_k = E_{A k-set}[1/f_k(A)], with f_k the same-layer fiber;
  - 2^{−d} = E_{T~Bern(1/2)}[1/f(T)].
- **Relation picture:** a balanced relation (j minus, j plus entries) is seen by a uniform k-set with probability
  ≈ α^j(1−α)^j and by a half-cube set with probability 4^{−j}. Small layers see each relation less often, so the
  conjecture holds in expectation. The difficulty is support (E[1/f]) versus expectation.
- **Caution:** with Bernoulli(p) sets in place of layers, monotonicity in p FAILS, because cross-layer zero-sum
  relations make small-p fibers large. Those relations do not affect a_k, so a proof must use layer-restricted fibers.
- **Cauchy–Schwarz route:** a_k ≥ 1/E_A f_k (exact). It suffices that E_A f_k ≤ 2^{d}·poly.
  - cs_route.py on the gadget families: CS margin/m at α = .0074 is +0.13 to +0.67 (generic 0). It holds everywhere
    tested, slightly below the support margin.
- **Swap injection:**
  - For half-cube T, f(T) ≥ 1 + Z(T), with Z = Σ_v X_v Y_v (X_v = # of F_v inside T; Y_v = # of F_v disjoint from T;
    pairs with A ⊂ T, A′ ∩ T = ∅ give distinct T′ = T\A ∪ A′ with the same sum).
  - E Z ≈ 4^{−k} binom(m,k) E_A f_k (counting disjoint pairs). If Z concentrates, then
    2^{−d} ≲ 4^k/(binom(m,k) E_A f_k), i.e. the conjecture with a spare factor 2^{m(h(α)−2α)} (≈ 2^{.049m} at
    α = .0074). This explains the large margins.
- **The missing step (precise):** a lower-tail bound P(Z ≤ E Z / poly) ≤ 1/(E_A f_k · poly).
  - Z is a sum of mixed cylinder events (bits required to be 1 on A, 0 on A′), so the standard monotone Janson
    inequality does not apply directly.
  - A Janson-type inequality for mixed cylinder events, or a second-moment / switching argument, is needed. Conflicting
    events are disjoint, which should help.
  - Also: fibers whose members overlap need multiplicity bookkeeping for swaps with A ∩ A′ ≠ ∅.
- **Status:** NOT PROVED. The reduction chain is
  ternary-mask gain (2.35e-4) ⇐ Conjecture R ⇐ (CS) E_A f_k ≤ 2^d poly ⇐ lower-tail concentration of Z.
  Every link is supported by numerics on gadget products, and the last link is a standard-shaped probabilistic
  question.

## C20 (22:30 ET): stress test + literature; handoff written (LEMMA_R_HANDOFF.md)
- finite_adv.py (m = 18, exhaustive; planted relations, low rank, embedded blocks, small range, annealing): min R = 0
  for k = 1..4.
- exact_range.py (m = 10..16): the no-loss version holds for k/m ≤ .25 in all searches. Negatives above ~.3 are ≤ 1.74
  bits, within the poly allowance.
- Literature: Jain–Sah–Sawhney 2021 (cube version: concentration ≥ 2^{−εn} ⇒ ≤ 2^{O(√ε n)} sums). Our R is the slice
  analogue with a weaker demand, not covered by them.
- Reformulation: "the average fiber of a small slice is at most poly(m) times the cube's average fiber".

## C21 (02:10 ET Nov 4): Fable's exploratory notes + monotonicity
- **Fable (independent):** same reduction (its "Lemma R" = our counting identity; "[S]" = our Conjecture R).
  - New target: MONOTONICITY a_k ≥ a_{k+1} (k + 1 ≤ m/2). It implies [S] for α ≤ 0.11 via
    2^{−d} ≤ E_{t~Bin(m,1/2)} a_t, with the tail ≤ 2^{−m(1−h(α))} absorbed by a_k ≥ 1/C(m,k).
  - 30744 tests at m ≤ 14, no violation.
- **mono.py (ours, exhaustive, m = 16/18/20, structured + random + annealing):** no violation.
  - The minimum ratio is exactly 1, at two-valued weights (half 1, half 2) with k = m/2 − 1:
    a_k/a_{k+1} = (m−k)/(k+2). SHARP.
- **union_core.py (ours): exact identity (bijection (y, e) ↦ (e, y − w_e)):**
  Σ_{y∈Σ_{k+1}} |U(y)| = Σ_{x∈Σ_k} (m − |C(x)|), with U = union and C = intersection of the witness sets.
  - So monotonicity ⟺ Σ_y (|U(y)| − (k+1)) ≥ Σ_x (k − |C(x)|): union-excess at k+1 ≥ core-deficit at k.
  - Verified on 39 instances (identity and equivalence exact). The two-valued tight case at k = 4 has excess = deficit = 20.
  - A naive charging (x ↦ y = x + w_e, e ∉ U(x)) needs |U(x)| + |C(x)| ≥ 2k, which FAILS for 3+ witnesses
    ({1,2}, {1,3}, {2,3}). A proof needs a better charging or a double count.
- **Ye–Li (Fable):** does not compose with the alias step at the level of these constructions.
  - At our point records = visits (C2 = C3 = C4).
  - A partial-match test helps only for a ≈ .03–.12, where the needed degree is < .107 while Fredman–Volper gives
    .13–.29 (Ye–Li improve on it by 4e-5).
  - Multiplicity: a circuit can't deduplicate across trials.
  - The paper's Section 10 is updated with credit.
