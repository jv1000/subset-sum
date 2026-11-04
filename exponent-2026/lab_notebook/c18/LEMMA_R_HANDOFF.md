# Handoff: the "small slices" lemma (worth 2.35e-4 on the Subset Sum exponent)
Prepared by Claude, 2026-11-03 ~22:30 ET, for Astra / any collaborator. Status: **open**. Everything below is either
proved (marked PROVED), numerical evidence (marked EVIDENCE), or a proof route with its exact failure point.

## 1. Statement
Integer weights w on an m-set M. Σ_k(M) = {w(A) : |A| = k}, Σ(M) = all subset sums.
- a_k(M) = |Σ_k(M)| / binom(m,k): the fraction of distinct values in the k-slice, i.e. 1 / (average fiber size in the slice).
- 2^{−d(M)} = |Σ(M)| / 2^m: 1 / (average fiber size of the whole cube).

> **Conjecture R (small slices).** There are α0 > 0 and C such that for all m, all integer weightings, and all
> k ≤ α0·m: a_k(M) ≥ 2^{−d(M)} / m^C.
> Equivalently: the average fiber size of a small slice is at most poly(m) times the cube's.

Needed value: k = 0.0070·m (α0 = 0.01 suffices). Signed weights must be allowed.

## 2. Why it matters (PROVED reduction + floating pricing)
- In Base's alias step (a-kapila, PROOF_0.4877.tex §5), let the left mask carry k1 entries +1 inside the alias's
  half-block S and k2 entries −1 outside S.
- On M \ S the trial's signed weights are −c^I, so the family's sums are plain k′-subset sums (k′ = k1 + k2) of one
  fixed signing c^I. PROVED by a sign computation (C15 notes).
- Counting identity: binom(m,σ) binom(σ,k1) binom(m−σ,k2) = binom(m,k′) binom(k′,k1) binom(m−k′,σ−k1). Hence
  E_S[fraction of distinct family sums] ≥ a_{k′}(M). PROVED.
- With R: trials ≤ 2^{d(M)} poly. This fits Base's cost bounds if μ < l, and Corollary D is not needed.
- Floating optimum: τ0 = 0.48734025 (k1 = k2 = 0.0035m), 2.35e-4 below the certified 0.4875754036 and 3.4e-4 below
  JoshuaQFEX. Files: PREREGISTRATION_C19.md, c19.py.

## 3. Evidence (EVIDENCE)
- **Gadget products** (q generic-separated copies of a block B): R/m = lim (log2 a_k + d)/m, exact via maximum entropy
  (gadget.py).
  - Structured blocks: +0.13 to +0.67 at α ≤ .02.
  - Adversarial hill-climb (search.py): minimum 0, attained only by collision-free blocks.
- **General weightings, exhaustive, m = 18** (finite_adv.py): planted sparse relations, low rank, embedded equal / AP /
  ± blocks, small range, plus an annealing adversary. Minimum log2 a_k + d = 0.000 for k = 1..4 (generic only).
- **Exact (no-loss) version** (exact_range.py, m = 10..16): R_k ≥ 0 in every search for k/m ≤ 0.25. It fails above
  ~0.3, but all negatives are ≤ 1.74 bits, within the poly allowance (log2(m+1) ≈ 4). Tiny cases break the exact
  version (m = 4, k = 1, all equal: −0.32), so only the poly version is conjectured.
- **Cauchy–Schwarz version** (stronger: E_A f_k(A) ≤ 2^d poly, which implies R because a_k ≥ 1/E_A f_k): holds on all
  gadget families (cs_route.py).

## 4. Proof routes tried and where each fails
1. **Covering from the good layer (Base's Lemmas 3.1–3.3):** loses (1 − t/m)^k, i.e. k bits when the good layer t is
   near m/2. This is Base's "support ≤ m/2 + k" barrier.
2. **Single-element removal injection:** loses m/(m−j) per step, which compounds exponentially.
3. **Sumset with Base's Corollary D on both halves:** pays the trial exponent g twice.
4. **Bernoulli(p) monotonicity:** E_{Bern(p)}[1/f] is NOT monotone. Cross-layer zero-sum relations make small-p fibers
   large, but they do not affect a_k. Any proof must use slice (layer-restricted) fibers.
5. **Swap injection (most promising):**
   - For a half-cube T, f(T) ≥ 1 + Z(T), with Z = Σ_v X_v Y_v.
     - X_v = number of k-sets in fiber F_v inside T; Y_v = number disjoint from T.
     - (A, A′) ↦ T′ = T \ A ∪ A′ is injective when A ⊂ T and A′ ∩ T = ∅.
   - E Z ≈ 4^{−k} binom(m,k) E_A f_k. If Z concentrates, 2^{−d} = E[1/f] ≲ 4^k/(binom(m,k) E_A f_k), which is R with a
     spare factor 2^{m(h(α) − 2α)}.
   - **Missing:** a lower-tail bound for Z. Z is a sum of mixed cylinder events (bits 1 on A, 0 on A′), so monotone
     Janson does not apply directly. Conflicting events are disjoint, which should help.
   - Also needed: multiplicity bookkeeping for fibers whose members overlap (A ∩ A′ ≠ ∅).

## 5. Closest literature (read before attacking)
- **V. Jain, A. Sah, M. Sawhney, "Anticoncentration versus the number of subset sums", Advances in Combinatorics 2021:6**
  (arXiv:2101.07726).
  - Cube version of "concentration forces few sums": if max_τ P[⟨w, ξ⟩ = τ] ≥ 2^{−εn} (ξ ~ Ber(1/2)^n), then
    |Σ(w)| ≤ 2^{O(√ε n)}.
  - Method: density comparison between the uniform measure on a level set and binomial product measures, plus an
    injectivity lemma for A × (k·B) → A + k·B.
  - **Our R is a slice analogue with a much weaker quantitative demand** (d ≥ s − O(log m) when the average k-slice
    fiber is 2^s). It is not covered by their paper, which works only with the cube and Bernoulli(1/2).
- **A. Ferber, V. Jain, K. Luh, W. Samotij, "On the counting problem in inverse Littlewood–Offord theory"**
  (arXiv:1904.10425). Counting vectors with large small-ball probability; reached via ρ down to exp-type scales in
  random-matrix applications.
- **Tao–Vu, Nguyen–Vu inverse Littlewood–Offord theorems** (large ρ implies the coordinates lie in a small GAP). These
  are for polynomial ρ; we need exponentially small scales.
- **Halász-type inequalities:** concentration bounded by counts of additive relations. This fits the relation picture
  below.
- **Fixed k (k = O(1)): a likely proof via Freiman-type structure.** Small a_k forces small restricted k-fold doubling of
  the weight set, hence a low-dimensional GAP, hence few cube sums. This is NOT our regime (k linear in m), but it
  supports R.

## 6. Relation picture (heuristic that should become the proof)
- Collisions come from relations λ ∈ {−1,0,1}^m with w·λ = 0.
- A slice-collision relation is balanced (j minus, j plus entries). A uniform k-set sees it with probability
  ≈ α^j(1−α)^j; a half-cube set sees it with probability 4^{−j}.
- Small slices see every relation less often (by (4α(1−α))^j), so R holds in expectation trivially. The whole
  difficulty is support (E[1/f]) versus expectation, i.e. lower-tail concentration of the relation count, or a Halász /
  JSS-type inverse argument on slices.

## 7. Suggested plan
1. Try to adapt Jain–Sah–Sawhney's density-comparison argument from Ber(1/2) to the k-slice; our target is weaker.
2. In parallel, attempt the mixed-cylinder lower tail for Z (route 5). Reference point: Janson / Riordan–Warnke-type
   inequalities for general events.
3. Keep the harness honest: any claimed proof must reproduce the numbers in section 3. Any claimed counterexample must
   beat −log2(m+1) at k ≤ m/4 in finite_adv.py / exact_range.py, or be negative in gadget.py at α ≤ 0.02.

Files (D:\AIProjects\SubsetSum\C3_target_048_Claude\c18 and the parent folder):
- NOTES_C18.md;
- gadget.py, search.py, s_*.log;
- cs_route.py, finite_adv.py, exact_range.py;
- PREREGISTRATION_C15.md, C19.md; c19.py.

## 8. UPDATE (Nov 4, 02:10 ET): cleanest target = MONOTONICITY, with an exact combinatorial form
- **Fable (independent referee)** reduced the lemma the same way and proposed monotonicity a_k ≥ a_{k+1} for
  k + 1 ≤ m/2.
  - It implies [R] for k ≤ 0.11m: 2^{−d} ≤ E_{t~Bin(m,1/2)} a_t; layers in [k, m−k] are bounded by a_k, and the tail
    mass ≤ 2^{−m(1−h(α))} ≤ a_k.
- **Evidence:** no violation in 30744 tests at m ≤ 14 (Fable) or exhaustively at m = 16/18/20 (mono.py).
  - **Sharp:** half the weights 1 and half 2 gives ratio exactly 1 at k = m/2 − 1. Any proof must be tight there.
- **Exact identity (PROVED, verified, union_core.py):** Σ_{y∈Σ_{k+1}} |U(y)| = Σ_{x∈Σ_k} (m − |C(x)|), where U and C
  are the union and intersection of the witness sets. So:
  > **Monotonicity ⟺ union-excess of the (k+1)-sums ≥ core-deficit of the k-sums.**
- **First attempt:** the naive charging fails for three pairwise-overlapping witnesses. A double count over pairs of
  witnesses, or an LYM/Kruskal–Katona-style shadow argument on the witness families, looks like the natural tool.
- **Even approximate monotonicity (a_t ≤ poly·a_k for t ∈ [k, m−k]) suffices.**
