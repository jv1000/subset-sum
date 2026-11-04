# Round 2 report: making 0.48734 real

Claude Fable 5.1, night of 3–4 Nov 2026, working unattended as a collaborator. Discipline: every experiment has a
two-line pre-registration in `scripts/round2/PREREG_A1.md` (predictions and controls, with outcomes appended);
every claim is labelled PROVED, EVIDENCE or CONJECTURE; dead ends are kept with the reason. `paper_v2.md` was not
edited. Scripts are in `scripts/round2/`, outputs in `scripts/round2/out/`.

## Summary table

| Item | Status | Result |
| --- | --- | --- |
| A. Exact layer-density monotonicity a_k ≥ a_{k+1} (k+1 ≤ m/2) | **COUNTEREXAMPLE (verified exactly)** | w = (−6,−5,−5,−3,−3,−2,4,5), m = 8: s_3 = 19, s_4 = 24, so 5·19 = 95 < 4·24 = 96, a_3 = 19/56 < a_4 = 24/70. 16 such multisets with values in [−6,6], all at m = 8 and all at the middle step k+1 = m/2; violation ratio ≥ 95/96. |
| A. Defect monotonicity D_k(M) ≤ D_k(M∖e) for every e (my induction route) | **COUNTEREXAMPLE (verified exactly)** | w = (−6,−5,−2,−1,0,3,4), k = 2, e of weight −1: Φ_e = +5. |
| A. Weak statement a_t ≤ poly(m)·a_k, t ∈ [k, m−k], k ≤ 0.11m (what [S] needs) | CONJECTURE, strong EVIDENCE | In every exhaustive and structured sweep, max_{t∈[k,m−k]} a_t/a_k = 1 exactly for all k ≤ m/4 (2.7·10⁶ multisets, m ≤ 11, values in [−6,6]; all Z_q, q ≤ 7, m ≤ 12; [−8,8] at m = 8, 9; structured m ≤ 22). The only violations of monotonicity anywhere are at the middle step. |
| A. Reduction lemmas | PROVED (Section A.2) | exact removal identity; induction scheme (now known to fail at its step); monotonicity on [k, m/2] ⟹ [S] with constant 3 for k ≤ 0.11m; weak form ⟹ [S] with poly constant. |
| A. Status of [S] | **partial: open conjecture, no counterexample, now with a sharper target** | the target is the weak form above (or "a_k ≥ a_t for k ≤ m/4, t ≥ k"), not exact monotonicity. |
| B. Ternary alias step, Base-style section | written (`SECTION_T_ternary_alias_step.md`) | Theorem A′ with Lemmas T1–T7, Base line citations, full condition list (33 conditions). |
| B. Frozen point `candidate_ternary.json` | **certified in arb (200 bits)** | T = τ0 + 20ε = **0.4873407528**; O(2^{T′n}) for every T′ > T, in particular O(2^{0.4873408n}); conditional on [S] and on Base's written proof. 2.3465·10⁻⁴ below the certified Section 8 point, 3.35·10⁻⁴ below JoshuaQFEX. |
| C. Counterexample hunt at m ≤ 22, structured families | done | no violation; minimum ratio exactly 1 (two-valued, k = m/2 − 1). The real counterexamples came from the exhaustive small-range sweep in A, not from the structured families. |

---

## A. Layer-density monotonicity

### A.1 Setting and notation

Integer (or abelian-group) weights w on an m-set M; Σ_j = set of distinct j-subset sums, s_j = |Σ_j|,
a_j = s_j/C(m,j). For a j-sum x: W(x) = its witness family, f(x) = |W(x)|, C(x) = ∩W(x) (core), U(x) = ∪W(x) (union).
D_k(M) := (k+1)s_{k+1} − (m−k)s_k ("defect"); a_k ≥ a_{k+1} ⟺ D_k(M) ≤ 0. For e ∈ M, n_e^{(j)} := #{x ∈ Σ_j : e ∈ C(x)}
= s_j(M) − s_j(M∖e) (the j-sums that disappear when e is removed; the equality is immediate: x survives in M∖e iff
some witness avoids e). The handoff's identity Σ_y |U(y)| = Σ_x (m − |C(x)|) is Σ_e s_k(M∖e) written two ways.

### A.2 What is proved (PROVED)

**Lemma A.1 (removal identity).** For every e ∈ M and every k,
D_k(M) = D_k(M∖e) − s_k(M) + (k+1)·n_e^{(k+1)} − (m−k−1)·n_e^{(k)}.

*Proof.* Substitute s_j(M) = s_j(M∖e) + n_e^{(j)} into D_k(M) and use D_k(M∖e) = (k+1)s_{k+1}(M∖e) − (m−1−k)s_k(M∖e).
Checked exactly on every instance in `lemmaE_test.py`. ∎

**Lemma A.2 (odd middle).** If |M₀| = 2k+1 then D_k(M₀) = 0 (complement symmetry s_k = s_{k+1}, and C(2k+1,k) = C(2k+1,k+1)).

**Corollary A.3 (induction scheme).** Monotonicity a_k ≥ a_{k+1} holds for all M with |M| ≥ 2k+2 if for every such M
some e ∈ M satisfies Φ_e(M) := (k+1)n_e^{(k+1)} − (m−k−1)n_e^{(k)} − s_k(M) ≤ 0 ("Lemma E"), by descending to
|M₀| = 2k+1. The averaged form Σ_e Φ_e ≤ 0 is the "core inequality" (k+1)Σ_y|C(y)| ≤ m s_k + (m−k−1)Σ_x|C(x)|, and the
per-element form Φ_e ≤ 0 ∀e is "defect monotonicity" (DM). ∎

**Lemma A.4 (equivalent forms of Φ_e ≤ 0).** With M′ = M∖e, m′ = m − 1, v = w_e, I_j := |Σ_j(M′) ∩ (Σ_{j−1}(M′) + v)|
(j-sums of M′ reachable as a (j−1)-sum plus v):
Φ_e ≤ 0 ⟺ (k+1)I_{k+1} − (m′+1−k)I_k ≥ D_{k−1}(M′) ⟺ (k+1)·#{non-v-extendable k-sums of M′} ≤ s_k(M′) + (m′+1−k)·#{non-v-extendable (k−1)-sums of M′}.
For a generic new value v both sides are the monotonicity of M′ at level k−1. ∎

**Lemma S (monotonicity on [k, m/2] ⟹ [S], explicit constant).** If a_t ≤ a_k for all t ∈ [k, m−k] (in particular if
a_j is nonincreasing on [k, m/2], by complement symmetry) and k = αm with h(α) ≤ 1/2 (α ≤ 0.1100), then
a_k ≥ 2^{−d(M)}/3.
*Proof.* |Σ(M)| ≤ Σ_t s_t, so 2^{−d} = |Σ|2^{−m} ≤ Σ_t a_t C(m,t)2^{−m} = E_{t∼Bin(m,1/2)}[a_t] ≤ a_k + P[t ∉ [k, m−k]]
≤ a_k + 2·2^{−m(1−h(α))}, and a_k ≥ 1/C(m,k) ≥ 2^{−m h(α)} ≥ 2^{−m(1−h(α))} when h(α) ≤ 1/2. ∎
With the weak form a_t ≤ P(m)a_k the same proof gives a_k ≥ 2^{−d}/(P(m) + 2), which is all Theorem A′ needs
(C_S enters only the trial count n⁸·C_S·2^{d(M)}, Section T).

**Lemma R (restated for completeness, PROVED in the handoff and in my round-1 notes).** For uniform S (|S| = m/2) and
ℱ(S) = {U : |U ∩ S| = k1, |U∖S| = k2}, E_S[#distinct sums over ℱ(S)]/(C(σ,k1)C(σ,k2)) ≥ a_{k1+k2}(M).

### A.3 Counterexamples (verified exactly by brute force, `dm_violations.py`, `out/dm_violations.txt`)

**Exact monotonicity fails.** Exhaustive sweep over all 496,860 value multisets with values in [−6,6] and m = 4..9:
16 violations, all at m = 8, k = 3 (the middle step k+1 = m/2). Two families:

| multiset (shifted to start at 0) | s_0..s_8 | (m−k)s_k vs (k+1)s_{k+1} | a_3 vs a_4 |
| --- | --- | --- | --- |
| {0,1,1,3,3,4,10,11} (= (−6,−5,−5,−3,−3,−2,4,5)) and 11 relatives | 1,6,14,19,24,19,14,6,1 | 95 < 96 | 19/56 = 0.3393 < 24/70 = 0.3429 |
| {0,2,2,6,6,8,9,11} (= (−6,−4,−4,0,0,2,3,5)) and 3 relatives | 1,6,14,18,23,18,14,6,1 | 90 < 92 | 18/56 = 0.3214 < 23/70 = 0.3286 |

Structure: six small values containing two doubled values, plus two large values; in both families Σ_4 is a full
interval of integers (24 resp. 23 consecutive sums) while Σ_3 has gaps. Every 7-element sub-multiset satisfies
monotonicity in its own range, so the k = 3 chain of Corollary A.3 starts at |M₀| = 7 with D = 0 and fails at the
first step: this is exactly where the handoff's remark "any proof must be tight at the two-valued case" bites, the
two-valued case being the boundary of a region that is in fact slightly crossed.

**DM (per-element) fails** already at m = 7: (−6,−5,−2,−1,0,3,4), k = 2, e the element of weight −1: six 3-sums need
e, no 2-sum needs e, s_2 = 13, so Φ_e = 18 − 0 − 13 = +5 (23 DM-violating multisets in the sweep). Monotonicity
holds for this instance (65 ≥ 57) and the averaged form holds (Σ_e Φ_e = −31).

### A.4 Evidence on the surviving statements (EVIDENCE)

| Sweep (script) | instances | exact monotonicity | max_{t∈[k,m−k]} a_t/a_k, k ≤ m/4 | min a_k2^{d}(m+1), k ≤ m/4 |
| --- | --- | --- | --- | --- |
| all multisets, values in [−3,3], m = 4..12 (`dm_exhaustive.py`) | 50,268 | 0 violations | 1.000 | — |
| all multisets in Z_q, q = 2..7, m = 4..12 | 77,181 | 0 | — | — |
| all multisets, values in [−6,6], m = 4..9 (`dm_violations.py`) | 496,860 | 16 (all m = 8, middle step) | — | — |
| all multisets, values in [−6,6], m = 10 and 11 (`mono_ratio_sweep.py`) | 2,645,370 | 0 (min middle ratio 1.000, min interior ratio 1.126) | 1.000 | 20.9 |
| all multisets, values in [−8,8], m = 8 and 9 (`mono_wide.py`) | 2,778,446 | 130 (all m = 8, middle step, worst ratio 90/92 = 0.978; e.g. (−8,−6,−6,−2,−2,0,1,3)); 0 at m = 9 | 1.000 | — |
| structured cluster+large (the counterexample's shape), m = 10..16 (`mono_wide.py`) | 19,500 | 0 (min middle ratio 1.029) | 1.000 | — |
| all multisets, m = 10 in [−8,8] and m = 12 in [−6,6] (`mono_m10_m12.py`) | 8,015,891 | 0 (min middle ratio exactly 1 at two-valued weights; min interior ratio 1.21 and 1.24) | — | — |
| structured families, m = 16..22 (`c_hunt.py`) | 273 | 0, min ratio 1.000 (two-valued) | — | — |
| finite groups, random, m ≤ 14 (`group_probe.py`) | 12,000 | 0 | — | — |
| Hall's condition, all subsets Y of (k+1)-fibers, small m (`hall_probe.py`) | 1,176 (instance,k) | holds, min slack 0 | — | — |

The pattern: violations of monotonicity exist but (so far) only at m = 8, only at the last step before the middle,
and by at most 2.2 % (ratio ≥ 90/92); exhaustive sweeps at m = 9, 10, 11, 12 over the same or wider value ranges
(about 11 million multisets in all) show none. For k ≤ m/4 the maximum of a_t over t ≥ k is always attained at t = k.
Why m = 8 is special is not understood; the middle step compares s_n with s_{n−1}(1 + 1/n) for m = 2n, and the
counterexamples have a full-interval middle layer over a gapped layer below, a configuration that the small value
ranges tested cannot reproduce at larger m. The [S] quantity
a_k 2^{d(M)}(m+1) never fell below 20 in the exhaustive ranges (and below 4.5 in round 1's random tests).

### A.5 Routes tried tonight and why each failed (kept)

1. *Per-element induction (DM).* Clean, group-free, held in 10,199 family tests and a hill-climb, but is false
   (m = 7). The step inequality is an additive statement about one new value v, not a local property of witnesses:
   x is "v-extendable" iff x + v is a (k+1)-sum, which can happen through a witness unrelated to x's witnesses.
2. *Existence form (Lemma E) and averaged form (core inequality).* Both are exactly as strong as monotonicity itself
   in the sweeps (they fail precisely on the 16 counterexamples), so they are reformulations, not steps.
3. *Per-set and per-fiber charging* (Σ_{g∉A} 1/f(A∪g) ≤ (m−k)/f(A); Σ_{A∈W(x)} … ≤ m−k): fail (three equal weights
   plus generic weights: the fiber x = 2w receives m > m − 2).
4. *Token injection* (y, e ∈ Z_y) ↦ (y − w_e, e) with canonical witnesses: injective, but the load at x is
   Σ_v mult_{Z_{x+v}}(v), which reaches m (three-equal) while the capacity is m − k.
5. *Uniform fractional flows* in the fiber graph (from y: N(y,x)/f(y); from x: N(y,x)/f(x)): the first violates
   capacities (three-equal), the second violates demands (two-valued extremes). Hall's condition itself holds in all
   small tests, so a non-uniform flow exists, but no rule for it was found; and since exact monotonicity is false at
   m = 8, Hall must fail there for Y = everything, i.e. the flow approach can only aim at the weak form.
6. *Induction on value classes with disjoint translates*: the termwise use of the inductive hypothesis is too lossy
   for classes of multiplicity ≥ 2.
7. *Group structure*: monotonicity and DM hold in every finite abelian group tested (m ≤ 14), so the order of the
   integers is irrelevant; the m = 8 counterexample lives in Z as well as in Z_q for large q.

### A.6 Refined conjecture and what remains

**Conjecture M′ (weak monotonicity).** For k ≤ m/4 and every t ∈ [k, m−k], a_t(M) ≤ a_k(M). (Evidence: never violated;
exact monotonicity is only violated at the step k+1 = m/2.) Conjecture M′ implies [S] with constant 3 for
k ≤ 0.11m (Lemma S), hence Theorem A′ and the exponent 0.4873407528. Even a_t ≤ poly(m)·a_k suffices.

What a proof must do: it cannot be an induction whose step is a per-element inequality, and it cannot be tight at
the middle step. The natural remaining tools are (i) a flow/Hall argument for the weak form, where the capacity
m − k can be replaced by (m − k)·poly(m), so that non-uniform rules have room; (ii) the "two-level" structure: the
counterexamples show the middle layer can be a full interval while the layer below has gaps, which suggests
bounding a_t/a_k through the growth of |Σ_t| as a sumset Σ_k + Σ_{t−k}: |Σ_t| ≤ |Σ_k|·|Σ_{t−k}| is too weak, but a
Plünnecke-type or "popular difference" argument on the layer sumsets, with the k-layer as the base, is the right
shape; (iii) for the actual application only k ≤ 0.007m matters, and there the statement a_t ≤ a_k·poly is a
statement about very sparse layers, where the handoff's swap/relation picture (a sparse layer sees each additive
relation with probability ≈ α^j(1−α)^j) should give the expectation version; the lower-tail (support) version is
the open part.

---

## B. The ternary alias step and the certified point

Full section: `SECTION_T_ternary_alias_step.md` (Theorem A′, Lemmas T1–T7 with Base line numbers, the procedure
changes, the expansion rule X⁺ ∩ Y = ∅, X⁻ ⊆ Y, Z = ((X⁺ ∪ Y)∖X⁻) △ F, the trial count n⁸⌈2^{d(M)}⌉ with |Σ(M)|
computed exactly, the distinctness lemma T4 (global, no "bad S" fraction, so Base's δ and (C8) are not needed), and
the complete numerical condition list).

Condition list derived (33 conditions, all certified in `scripts/round2/check_ternary_point.py`,
output `out/ternary_certificate_N4096_8192.txt`):
C1R γ < h(2a)/2 + h(2c)/2; C2R l + (H3(a,c) − γ)μ < τ0; C3 r + (1−γ)μ < τ0; C4R 1 − μ + (H3(a,c) + h(½−a+c) − γ)μ − η < τ0;
C5R/C5L max(H3(a,c), h(½−a+c))μ + ½ − τ0 < τ0; C6 0 < r < τ0, l < τ0; MU1 μ < l; MU2 μ ≤ ½; A4R μ(h(2a′)+2a′) < η with
2a′ ≤ ½ and 1/guard < η − A4; SR a′ ≤ 0.11; A7.1 l, r, μ < τ0 − ε0; A7.3, A7.4; ThmA 1/guard + ζ < ε0; τ0 < ½;
η/2 < τ0 + 20ε; Δ, Γ > 0; a_Γ ≤ ¾; p, q ≥ 1; ρ_c < ρ_f; ρ_f + (18+6p)ε < η; ρ_f + (18+6q)ε < η; log₂M1, log₂M2 < ρ_c.
Not needed (information only, all slack): C8, A5R, the OpenAI caps 3p ≤ 30 and q(4a+3) ≤ 30.

Frozen point (choice: parameters to 10 decimals, κ, p, q and filter coefficients to 8 decimals, τ0 raised by
3·10⁻⁷ and rounded up, ε = ζ = 10⁻⁸, guard 10⁸, ρ_f = η − 1.5·10⁻⁶, ρ_c = ρ_f − 10⁻⁶; `freeze_ternary.py`):

| τ0 | η | μ | a | c | γ | l | κ | p | q_m |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.4873405528 | 0.5159974155 | 0.4746795055 | 0.0035141538 | 0.0035141537 | 0.0603737099 | 0.4840025845 | 1.03462910 | 8.46825883 | 8.27946618 |

**T = τ0 + 20ε = 0.4873407528.** Conditional on [S] (any constant) and on Base's written proof, Subset Sum has a
randomized algorithm in time O(2^{T′n}) for every T′ > 0.4873407528, in particular O(2^{0.4873408n}). Margins:
C1R 9.99·10⁻⁷ (= ε0; it is the one constraint that does not contain τ0, so the τ0 bump leaves it at the optimizer's
10⁻⁶ slack), B3 8.1·10⁻⁷, C2R/C3/C4R 1.30·10⁻⁶, C5R 1.60·10⁻⁶, M1 3.04·10⁻⁶, M2 3.30·10⁻⁶, everything else ≥ 3·10⁻³.
log₂M1 = 0.51599187405865778648, log₂M2 = 0.51599162047014794189 (identical at N = 1024, 4096, 8192; ball radii
< 4·10⁻⁵⁵; evaluator = round-1 `moments_arb.py`, whose control reproduces OpenAI's Appendix A table).
Since a = c to 10 decimals, the right mask has exactly m/2 entries and h(½ − a + c) = 1 exactly.

Choices made in B (noted): (1) the trial count uses the exact |Σ(M)| (cost 2^{μn} < 2^{τ0 n}) instead of Base's
sampled F̂, which removes Lemma A3's estimation step and makes C3 cancel d(M) exactly; (2) Lemma T4 is stated
globally over M (all ≤ 2k′-sparse relations), which is cleaner than Base's "bad S" fraction and makes (C8)/(A5)
unnecessary; (3) [S]'s constant C_S is carried symbolically (it only multiplies the trial count by a polynomial).

---

## C. Counterexample hunt (background)

`c_hunt.py`: m = 16..22, 273 structured instances (two-valued, APs with gaps, ± mixtures, 2- and 3-valued, sumsets,
gadget repeats, geometric + equal, low rank, cluster + generic, generic control): no violation, minimum ratio
exactly 1 at two-valued weights with k = m/2 − 1 (pre-registered prediction held). The decisive counterexamples came
from the exhaustive small-range sweep (A.3), which was not part of C's plan; lesson: for this problem exhaustive
small cases beat structured families, because the violating structure (two doubled values plus two large values)
is not one a human would guess.

## Choices made tonight (log)

1. Pursued the induction route first (A1) because the handoff's identity suggested it; abandoned after the exact
   counterexample at m = 7 (DM) and m = 8 (monotonicity).
2. Ran exhaustive sweeps over value multisets (cheap: the statement depends only on the multiset of values) in
   preference to larger random searches; this is what found the counterexamples.
3. Froze the C19 point with the same recipe as `candidate_base.json` (τ0 + 3·10⁻⁷, 10/8 decimals); did not re-optimize.
4. Wrote Theorem A′ with the exact-|Σ(M)| trial count and the global distinctness lemma (see B).
5. Kept every run to one process and under 3 minutes; the longest (m = 11 exhaustive) took 150 s.
6. Did not touch `paper_v2.md`.

## What I would do next

1. Hunt for monotonicity violations strictly inside the range (k+1 < m/2) and at larger m with the counterexample's
   shape (two doubled small values + two large) scaled up, to learn whether Conjecture M′ (k ≤ m/4) can fail at all.
   If a violation with a_t/a_k ≥ 1 + c appears for k ≤ m/4, the weak form must be re-examined; if none, the shape of
   the violating set (full-interval middle layer) suggests a sumset-growth proof of a_t ≤ poly·a_k.
2. Prove the weak form for k = O(1) first (a_1, a_2 against the middle layers) via Plünnecke/Ruzsa-type growth of
   Σ_t ⊆ Σ_k + Σ_{t−k}, then try to push k to linear size with the swap/relation picture of the handoff.
3. In paper_v2, replace the proposed "cleanest target: monotonicity" by Conjecture M′ and record the m = 8
   counterexamples (and the m = 7 DM counterexample) in the failures log.
4. B is finished modulo [S]; if [S] is proved with an explicit polynomial, only the trial-count constant and the
   cutoff n_* ≥ C_S change.
