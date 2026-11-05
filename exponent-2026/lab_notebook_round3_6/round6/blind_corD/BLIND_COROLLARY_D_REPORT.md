# Blind referee report: Lemmas 3.1–3.3 and Corollary D (Subset Sum paper)

## Summary verdict

- **Lemma 3.1 (covering): PROVED.** A short injection argument works.
- **Lemma 3.2 (sampling): PROVED.** A short double-counting argument works.
- **Lemma 3.3 (good layer): PROVED,** including the "in particular" clause.
- **Corollary D: PROVED** for every layer t that Lemma 3.3 can supply. The proof has two branches:
  - **Branch A, t ≥ k:** uses Lemmas 3.1 and 3.2 and the hypothesis 2σ ≤ v + 2k.
  - **Branch B, t < k:** uses the trivial bound a_k ≥ 1/C(σ,k) and the product hypothesis C(σ,k)C(v,k) ≤ 2^v.
- **Branch B really happens.** Lemma 3.3 only promises "some t". For example, if all weights are equal, t = 0 is a valid output. Even the largest layer can sit below ⌊v/2⌋: the weights (−4,−3,−2,−2,1,1,2,3) have layer sizes 1,6,13,16,15,16,… . So a proof that assumes t ≥ k, or t = ⌊v/2⌋, without a case split would have a gap.
- **Control (product hypothesis dropped): no counterexample found** in the search scope below (EVIDENCE). In that scope, every v-subset V had some t in [k, ⌊v/2⌋] satisfying Lemma 3.3's inequality, so the product hypothesis was never actually needed. Whether it can be removed in general is NOT CHECKED (open).
- **Brute force with all hypotheses: 0 failures** (EVIDENCE). For v ≥ 1 the smallest LHS/RHS ratio was exactly 2. At v = 0 the two sides are equal (both 1).

## Proofs

Notation: n = |V|. A t-subset is a subset with t elements. Binomial identities used:
- (I1) C(n, t−k)·C(n−t+k, k) = C(n,t)·C(t,k)
- (I2) C(n,s)·C(s,k) = C(n,k)·C(n−k, s−k)

Both count the same pairs of disjoint labelled subsets in two ways.

### Lemma 3.1 — PROVED

Assume 0 ≤ k ≤ t ≤ n.

1. Expand the right-hand side as a sum over all (t−k)-subsets W:
   E_W a_k(V∖W) = Σ_W |Σ_k(V∖W)| / (C(n,t−k)·C(n−t+k,k)).
   By (I1) the denominator is C(n,t)·C(t,k).
2. So the lemma is equivalent to: Σ_W |Σ_k(V∖W)| ≥ C(t,k)·|Σ_t(V)|.
3. For each value s in Σ_t(V), fix one t-set T_s with w(T_s) = s.
4. Each split T_s = W ⊔ U with |W| = t−k gives a pair (W, s − w(W)). Here s − w(W) = w(U), and U is a k-subset of V∖W, so this value lies in Σ_k(V∖W).
5. The map from (s, W) to (W, s − w(W)) is injective: from the image, W is read off directly, and then s = (s − w(W)) + w(W).
6. The domain has C(t,k)·|Σ_t(V)| elements, so the claim follows.

Only the group law is used (subtraction is well-defined), so integrality of the weights is not needed.

### Lemma 3.2 — PROVED

Assume 0 ≤ k ≤ s ≤ n.

1. Expand: E_S a_k(S) = Σ_S |Σ_k(S)| / (C(n,s)·C(s,k)).
2. By (I2) the lemma is equivalent to: Σ_S |Σ_k(S)| ≥ C(n−k, s−k)·|Σ_k(V)|.
3. For each value x in Σ_k(V), fix a k-set U_x with w(U_x) = x.
4. Every s-set S containing U_x has x in Σ_k(S). There are C(n−k, s−k) such sets S.
5. The pairs (S, x) are distinct for distinct x, which gives the inequality.

### Lemma 3.3 — PROVED

1. Taking complements maps j-subsets to (n−j)-subsets, so Σ_j(V) = w(V) − Σ_{n−j}(V). Hence |Σ_j| = |Σ_{n−j}|.
2. |Σ(V)| ≤ Σ_{j=0..n} |Σ_j| ≤ (n+1)·max_j |Σ_j|.
3. Let j* be a maximizer and set t = min(j*, n−j*). Then 2t ≤ n and |Σ_t| = |Σ_{j*}|, so |Σ(V)| ≤ (n+1)|Σ_t|.
4. For the "in particular" clause: 2^{−d(V)} = |Σ(V)|/2^n. Using C(n,t) ≤ 2^n,
   a_t(V) = |Σ_t|/C(n,t) ≥ |Σ(V)| / ((n+1)·C(n,t)) ≥ |Σ(V)| / ((n+1)·2^n).

Σ(V) always contains 0, so d(V) is defined. When V is empty, t = 0 and the statement holds with equality.

### Corollary D — PROVED

Write m = |M|. Assume k ≥ 0 (implicit in the statement).

**Step 0: derived facts.**
- From 2k ≤ σ and 2σ ≤ v + 2k: σ ≤ v/2 + k ≤ v/2 + σ/2, so **σ ≤ v**.
- Hence k ≤ σ/2 ≤ v/2, so **k ≤ ⌊v/2⌋**.
- With v ≤ m, all the random sets in the statement exist.

**Step 1: per-V claim.** Fix a v-subset V. Let S_V be a uniform σ-subset of V. Let t = t(V) be any t supplied by Lemma 3.3 (any rule that picks t from V will do). Then 2t ≤ v and |Σ(V)| ≤ (v+1)|Σ_t(V)|.

**Claim:** E[a_k(S_V)] ≥ 2^{−d(V)}/(v+1).

**Branch A (t ≥ k).**
1. Lemma 3.1 applies because 0 ≤ k ≤ t ≤ v: a_t(V) ≤ E_W a_k(V∖W), where W is a uniform (t−k)-subset of V.
2. For each W, |V∖W| = v − t + k ≥ v − ⌊v/2⌋ + k = ⌈v/2⌉ + k. The hypothesis 2σ ≤ v + 2k gives σ ≤ v/2 + k ≤ ⌈v/2⌉ + k. So k ≤ σ ≤ |V∖W|.
3. Lemma 3.2 then gives a_k(V∖W) ≤ E[a_k(S′)], where S′ is a uniform σ-subset of V∖W.
4. **Marginal law.** In the two-stage draw (W, then S′), a fixed σ-subset S₀ of V comes up exactly when W is disjoint from S₀. There are C(v−σ, t−k) such W, and each (W, S₀) pair has probability 1/(C(v,t−k)·C(v−t+k,σ)). This does not depend on S₀, so S′ has the law of S_V.
5. Combining with the "in particular" part of Lemma 3.3: 2^{−d(V)}/(v+1) ≤ a_t(V) ≤ E[a_k(S_V)].

**Branch B (t < k).**
1. Every σ-subset S has Σ_k(S) non-empty (because k ≤ σ), so a_k(S) ≥ 1/C(σ,k), and therefore E[a_k(S_V)] ≥ 1/C(σ,k).
2. |Σ(V)| ≤ (v+1)|Σ_t(V)| ≤ (v+1)·C(v,t).
3. Since t < k ≤ v/2, the binomial C(v,·) is increasing on [0, ⌊v/2⌋], so C(v,t) ≤ C(v,k).
4. Therefore 2^{−d(V)}/(v+1) = |Σ(V)| / ((v+1)·2^v) ≤ C(v,k)/2^v ≤ 1/C(σ,k) ≤ E[a_k(S_V)]. The third inequality is the product hypothesis.

**Step 2: averaging.** Draw V uniformly among v-subsets of M, then S_V uniformly among σ-subsets of V. For any σ-subset S₀ of M:

P(S_V = S₀) = C(m−σ, v−σ) / (C(m,v)·C(v,σ)) = 1/C(m,σ).

So S_V has the law of S, and E_S a_k(S) = E_V E[a_k(S_V)] ≥ E_V 2^{−d(V)}/(v+1).

Notes on the probability space:
- The statement gives S and V no joint law, and none is needed: the conclusion compares two separate expectations. The coupling is built inside the proof.
- t(V) is a fixed function of V, so mixing the two branches across different V is harmless.
- Everything lives on finite uniform spaces.

## Hypothesis usage table

| Hypothesis | Where used | Necessary for this proof? |
|---|---|---|
| 2k ≤ σ | (a) With 2σ ≤ v + 2k, gives σ ≤ v, so S_V exists. (b) Gives k ≤ σ: needed in Lemma 3.2 and for Σ_k(S) ≠ ∅ in Branch B. (c) Gives k ≤ v/2, so C(v,t) ≤ C(v,k) in Branch B. | Stronger than needed. The proof only uses k ≤ σ ≤ v and 2k ≤ v + 1 (the last one covers (c), since t ≤ min(k−1, ⌊v/2⌋)). |
| 2σ ≤ v + 2k | Branch A, to get σ ≤ \|V∖W\| = v − t + k for every t ≤ ⌊v/2⌋. Also used in step (a) above. | Slightly stronger than needed for odd v: σ ≤ ⌈v/2⌉ + k, i.e. 2σ ≤ v + 2k + 1, suffices. |
| v ≤ \|M\| | So that V exists; together with σ ≤ v, so that S exists. | Yes (definitional). |
| C(σ,k)·C(v,k) ≤ 2^v | Branch B only, in the form C(σ,k)·C(v,t) ≤ 2^v for t < k. | Only for V where Lemma 3.3's t is below k. It can be weakened to C(σ,k)·C(v, min(k−1, ⌊v/2⌋)) ≤ 2^v, and it is not needed at all when k = 0. Whether it can be dropped entirely is open. |
| Integer weights | Not used. | No. All arguments work for weights in any abelian group (e.g. real weights). |
| Nonnegativity of weights | Not used. | No. |
| k, σ, v nonnegative integers (implicit) | k ≥ 0 is needed for Σ_k and C(·,k) to be defined. v = 0 is allowed: then σ = k = 0 and the statement holds with equality. | k ≥ 0 is implicit and should be stated. |
| log base 2, d(V) defined | 0 is always in Σ(V), so \|Σ(V)\| ≥ 1. | Automatic. |

## Computational checks

**Method.**
- Exact subset-sum layers Σ_j for every sub-multiset, computed by a bitset dynamic program. This was validated against naive enumeration on 300 random instances with n ≤ 7 and weights in [−5,5]; all matched.
- All comparisons use exact rational arithmetic (`Fraction`).
- Corollary D is permutation-invariant, so instances are multisets: sorted tuples, which include repeats, zeros and negatives.
- For each instance, every admissible (k, σ, v) with v ≤ |M| is checked. "All hyps" means the product hypothesis holds. "Dropped" means 2k ≤ σ, 2σ ≤ v + 2k and v ≤ |M| hold but the product hypothesis fails.
- Checks with v = 0 are excluded from the ratio minima (they give equality, ratio 1).

**Lemmas 3.1–3.3 (EVIDENCE, in addition to the proofs).**
- 3,731 instances: all multisets of size ≤ 7 with weights in [−3,3], plus 300 random instances of size ≤ 8 with weights in [−30,30].
- 107,355 checks of Lemma 3.1, 107,355 of Lemma 3.2, and 3,731 of Lemma 3.3.
- 0 failures. Equality occurs in Lemma 3.1 (smallest ratio 1).

**Corollary D, exhaustive (EVIDENCE).**

| \|M\| | weights | multisets | checks, all hyps | fails | checks, product dropped | fails |
|---|---|---|---|---|---|---|
| 1 | [−4,4] | 9 | 9 | 0 | 0 | — |
| 2 | [−4,4] | 45 | 180 | 0 | 0 | — |
| 3 | [−4,4] | 165 | 1,155 | 0 | 0 | — |
| 4 | [−4,4] | 495 | 5,940 | 0 | 495 | 0 |
| 5 | [−4,4] | 1,287 | 21,879 | 0 | 2,574 | 0 |
| 6 | [−4,4] | 3,003 | 72,072 | 0 | 15,015 | 0 |
| 7 | [−4,4] | 6,435 | 205,920 | 0 | 45,045 | 0 |
| 8 | [−4,4] | 12,870 | 540,540 | 0 | 154,440 | 0 |
| 8 | [−3,3] | 3,003 | 126,126 | 0 | 36,036 | 0 |
| 9 | [−4,4] | 24,310 | 1,288,430 | 0 | 388,960 | 0 |
| 9 | [−3,3] | 5,005 | 265,265 | 0 | 80,080 | 0 |
| 10 | [−4,4] | 43,758 | 2,975,544 | 0 | 962,676 | 0 |
| 10 | [−3,3] | 8,008 | 544,544 | 0 | 176,176 | 0 |
| 10 | [−2,2] | 1,001 | 68,068 | 0 | 22,022 | 0 |

- **Smallest LHS/RHS ratio with all hypotheses (v ≥ 1):** exactly 2. It occurs at k = σ = 0, v = 1 whenever weights are nonzero (LHS 1, RHS 2/4).
- **Smallest ratio with the product hypothesis dropped:** exactly 8/3. It occurs at all-equal weights with (k,σ,v) = (2,4,4) (LHS 1/6, RHS 5/80).
- **Parameter triples where the product hypothesis fails (|M| ≤ 10):**
  - first one: (k,σ,v) = (2,4,4)
  - the full list for |M| = 10: (2,4,4), (2,4,5), (2,4,6), (2,5,6), (3,6,6), (2,5,7), (3,6,7), (2,5,8), (2,6,8), (3,6,8), (3,7,8), (4,8,8), (2,6,9), (3,6,9), (3,7,9), (4,8,9), (3,6,10), (3,7,10), (3,8,10), (4,8,10), (4,9,10), (5,10,10).

**Corollary D, random (EVIDENCE).**
- 176,090 instances with |M| from 6 to 10. Mixed weight models: uniform in [−50,50]; 1–3 distinct values in [−20,20] with heavy repeats; values drawn from {0,1,2,4,8,16,−1,−5,3}.
- 7,706,084 checks with all hypotheses: 0 failures, smallest ratio 2.
- 2,180,853 checks with the product hypothesis dropped: 0 failures, smallest ratio 8/3.

**Control result: no counterexample found** with the product hypothesis dropped, within the scope above. The structural reason, which explains why none was found:
- Every multiset V with |V| ≤ 10 and weights in [−4,4] (92,377 of them), or |V| ≤ 11 in [−3,3] (31,823), or |V| ≤ 8 in [−6,6] (203,489) was checked.
- In every one, for every admissible k, some t in [k, ⌊v/2⌋] satisfies |Σ(V)| ≤ (v+1)|Σ_t(V)|.
- So a proof that picks the largest valid t never needs Branch B in this range.

**Branch B is not vacuous** if t is taken as whatever Lemma 3.3 returns, e.g. the smallest maximizer:
- (V, k) pairs with that t < k: 31,972 for [−4,4] with |V| ≤ 10. Of these, 469 have some σ for which all hypotheses hold, e.g. V = {−4,−4}, k = 1, t = 0.
- The layer sizes |Σ_j| are not always non-decreasing on [0, v/2]:
  - |V| ≤ 10, weights in [−4,4]: 4 such multisets at size 8 and 42 at size 10. Example: (−4,−3,−2,−2,1,1,2,3) has layer sizes 1,6,13,16,15,16,13,6,1 and |Σ| = 19.
  - |V| ≤ 8, weights in [−6,6]: 36 such multisets at size 8.
  - |V| = 16: (8,56,58,−10,−52,−14,−12,−6,27,42,43,−29,−45,21,−8,−42) has |Σ_7| = 415 > |Σ_8| = 414 and |Σ| = 446. Confirmed by naive enumeration.
  - In both examples t = ⌊v/2⌋ still satisfies Lemma 3.3's inequality.

**Scripts** (scratchpad):
- /tmp/claude-0/-home-claude/1081a3db-b67e-507d-81e3-94e8009d81b7/scratchpad/bf.py
- /tmp/claude-0/-home-claude/1081a3db-b67e-507d-81e3-94e8009d81b7/scratchpad/run_main.py
- /tmp/claude-0/-home-claude/1081a3db-b67e-507d-81e3-94e8009d81b7/scratchpad/rnd.py
- /tmp/claude-0/-home-claude/1081a3db-b67e-507d-81e3-94e8009d81b7/scratchpad/lem.py
- /tmp/claude-0/-home-claude/1081a3db-b67e-507d-81e3-94e8009d81b7/scratchpad/branch.py
- /tmp/claude-0/-home-claude/1081a3db-b67e-507d-81e3-94e8009d81b7/scratchpad/sanity.py

## Issues

1. **Case split required.** Corollary D's proof must handle a Lemma 3.3 layer t < k: ties, equal weights and layer sizes that rise then dip all make it happen. A proof that silently assumes t ≥ k, or t = ⌊v/2⌋, is incomplete. Branch B above fills that case with the product hypothesis. (I have not seen the paper's proof; this flags what to look for.)
2. **σ ≤ v is implied but not stated.** It follows from 2k ≤ σ and 2σ ≤ v + 2k. It is worth stating because S is drawn from M, not from V.
3. **2k ≤ σ is stronger than needed.** The proof only needs k ≤ σ ≤ v and 2k ≤ v + 1.
4. **2σ ≤ v + 2k is slightly stronger than needed for odd v.** 2σ ≤ v + 2k + 1 suffices.
5. **The product hypothesis is used only in Branch B** and can be weakened to C(σ,k)·C(v, min(k−1, ⌊v/2⌋)) ≤ 2^v (none needed when k = 0). The search suggests it may be removable altogether (EVIDENCE only). That would follow from a lemma saying some t in [k, ⌊v/2⌋] always satisfies Lemma 3.3's inequality, e.g. |Σ(V)| ≤ (v+1)|Σ_{⌊v/2⌋}(V)|. I did not prove such a lemma.
6. **Integer weights are unnecessary.** All statements hold for weights in any abelian group.
7. **Implicit assumptions:** k ≥ 0 in Lemmas 3.1, 3.2 and Corollary D; all parameters are nonnegative integers.
8. **Notation.** "E_V 2^{−d(V)}/(v+1)" can be read two ways, but both readings are equal because v is constant. The phrase "S and V" in Corollary D needs no joint law; saying so would avoid confusion.
9. **Sharpness.** Equality holds at v = 0. For v ≥ 1 the observed slack is at least a factor of 2. Lemma 3.3's "in particular" step uses C(n,t) ≤ 2^n, which loses up to a factor of about √n.

## What I did not check

- Whether Corollary D holds without the product hypothesis in general. No counterexample was found for |M| ≤ 10, but there is no proof.
- Whether some t in [k, ⌊v/2⌋] always satisfies Lemma 3.3's inequality (verified only within the scope above).
- How the paper uses Corollary D downstream: parameter choices, and whether its proof covers Branch B.
- Instances with |M| > 10 for Corollary D. Only the two layer-size examples above (|V| = 8 and 16) were looked at for larger sizes.
- Random searches have a random seed and limited coverage; only the exhaustive rows are complete for their ranges.
- No file on the user's computer, no web source, and no proof from the paper was consulted.