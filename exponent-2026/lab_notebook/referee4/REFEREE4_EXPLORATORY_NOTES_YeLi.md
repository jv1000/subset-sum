# Exploratory notes: Ye–Li's partial-match route and the two open questions

Claude Fable 5.1, 3 Nov 2026. Sources: `2610.10446v1.pdf` (Ye–Li, "Subset Sum via Partial Match", 7 Oct 2026),
`paper.md`, Base, the OpenAI TeX. These are explorations, not refereeing; everything labelled "model" is the
fixed-Δ alias-budget model of `scripts/section9_check.py`. Scripts: `scripts/q_a_breakeven.py`,
`scripts/q_b_layer_density.py`, `scripts/q_b_local_search.py`, `scripts/q_b_sampling_identity.py`; outputs in
`scripts/out/q_*.txt`; the extracted Ye–Li text is `scripts/out/yeli_text.txt`.

## Summary

- (a) Ye–Li is not subject to the floor τ0 ≥ (1 − Δ)/2 because it has none of the floor's ingredients: no modulus
  P, no alias enumeration, no checksum, no Δ. It escapes the floor only in that sense; its exponent 1/2 − ξ/9 with
  ξ ≈ 2.0e-5 is far above 0.4858. Its partial-match step cannot replace or feed Base's alias step: in Base's
  regime the key-matching pairs are already as few as the records (C2 = C3 = C4 at the optimum), so a
  compatibility test has nothing to save; to profit from one, the masks must grow to a ≈ 0.03–0.12, where the
  test would need per-coordinate degree below 0.107 while the Fredman–Volper (OR-optimal) degree is 0.15–0.29,
  and Ye–Li's integer-circuit gain over the OR bound is 4e-5. In the joint model no EXACTZ gain up to 0.05 per
  coordinate improves on the certified point. The combined exponent is the certified 0.4875754 (nothing gained);
  the hypothetical limit, with an ideal compatibility test and the multiplicity problem solved, is the floor
  0.48565 at the certified Δ.
- (b) The "Corollary D beyond the half-block" lemma reduces losslessly to a statement about the whole block:
  E_S a_{k1,k2}(S) ≥ a_k(M), where a_k(M) is the fraction of distinct k-sums of the signed block (proof below,
  exact). So the inside/outside split is not the issue; the lemma is equivalent (up to a 2^{O(k)} factor in the
  other direction) to the **layer-density conjecture** a_k(M) ≥ 2^{−d(M)}/poly(m) for k ≤ m/2. Base's machinery
  proves it with a loss of up to k bits (a_k(M) ≥ 2^{−d(M)} C(m − t + k, k)/((m + 1)C(m, k))), which is more than
  the paper's 10 % tolerance, so the naive route fails exactly as the paper says. I could neither prove the
  lossless form nor find a counterexample: 7832 structured and random instances, hill-climbing at m ≤ 14, and
  30744 tests of the stronger monotonicity a_k ≥ a_t (k < t ≤ m/2) show no violation, with the worst ratio ≥ 4.5.
  My assessment: the lemma is probably true, with d(M) (not g_M) as the exponent, and d(M) is inside the trial
  budget; a proof needs a new idea (monotonicity of layer density would suffice via Base's Lemma 3.3).

---

## (a) Ye–Li versus the alias–checksum architecture

### What Ye–Li does (pages 3–10, 16–17)

Representation technique on a prefix of n/3 coordinates: c = a + b with a ∈ {0,1}, b ∈ {−1,0,1}, using
0 = 0 + 0 = 1 + (−1), 1 = 0 + 1 = 1 + 0 (p. 3). That is the Becker–Coron–Joux ternary representation, the same
one Section 9 of the paper calls "ternary masks". Keys are exact integer sums; a multiply-add-shift hash keeps a
1/N_sum fraction of each list (p. 9), where N_sum is the number of distinct prefix subset sums. The surviving
pairs with equal keys include pseudo-solutions (a + b ∉ {0,1}^n); they are not visited: a keyed partial-match
*counting* algorithm (Definition 2.1) returns the exact number of compatible equal-key pairs in time
|A|2^{δ_L m} + |B|2^{δ_R m}, and bisection recovers one solution. The whole gain is δ_L + δ_R = 1/2 − 2ξ against
the trivial 1/2 (Lemma 1.2), with ξ = 0.0000200 (Proposition 4.2), obtained from a depth-2 integer circuit for
the half-stars partial match matrix (Section 3.5) in the regime of central rows (#1(x) = n/2) and queries with
n/4 zeros and n/4 ones. The dichotomy on N_sum (p. 6, 10) plays the role of the deficiency dichotomy in
OpenAI/Base. Ye–Li's own remark (p. 6): OR circuits cannot beat δ_L + δ_R = 1/2 in this regime; the improvement
is a genuinely integer (inclusion–exclusion) cancellation.

### Why the floor does not apply, and why that does not help

The floor's two premises (paper Section 9) are: one dictionary insertion per alias class modulo a prime of ηn
bits, and a checksum whose budget η − τ_cs is at most the capacity Δ. Ye–Li has neither object: there is no
modulus, aliases are never defined, and the equal-key pseudo-solutions are *counted away* algebraically rather
than listed. So the inequality τ0 ≥ (1 − Δ)/2 says nothing about Ye–Li. But nothing else in Ye–Li gets near the
floor either: 1/2 − ξ/9 = 0.4999978. The two routes attack different wastes:

| | OpenAI/Base | Ye–Li |
| --- | --- | --- |
| representations | masks X ⊆ S (k of σ) and Y = S \ X on a block | a ∈ {0,1}^{n/3}, b ternary with support sn/3 on a prefix |
| filter | small prime P' of γm bits (plus large prime P, Lemma 2.5) | hash to |I|/p ≈ 1/N_sum |
| structured inputs | deficiency dichotomy (preliminary search) + random-prime collision lemma + exact-integer exclusion | N_sum dichotomy (AKKN few-sums procedure) |
| pseudo-pairs | visited and discarded (the C4 overhead, 0.0038n) | counted by an exact integer circuit, never visited |
| gain over 2^{n/2} | 0.0124n: large block, many representations, checksum instead of matching | ξn/9 = 2.2e-6 n |

### Could partial match feed the alias step?

Base's expansion step (g) (Base l.376-379) visits every key-matching (left record, right class record) pair and
tests X ∩ Y = ∅. That is a keyed compatibility test: rows = k-subsets X of the block (sparse, k = am), queries =
(σ − k)-subsets Y, compatible iff X ∩ Y = ∅, i.e. partial match where the query specifies "0" on Y and "∗"
elsewhere: half-stars, but with rows of weight am rather than m/2. Two facts decide the question.

1. **There is nothing to save at Base's point.** At the certified point C2 = C3 = C4 = C5 = τ0 within 1.3e-6
   (`scripts/out/base_point_N4096_8192.txt`): the number of visited pairs equals the number of left records and
   of right class records. Each record is visited O(1) times. A compatibility test can only reduce the pair
   count, never the list sizes; so at a = 0.0082 the brute-force visit is optimal given the lists, and the
   "overhead" of Section 9 lives in the lists (records that represent no alias), not in the pairs. The paper's
   own diagnosis ("removing the waste needs partial knowledge of S or a different source of representations")
   is right for this reason too.
2. **Growing the masks moves the waste into the pairs, but then the needed circuit is out of reach.** In the
   model (`q_a_breakeven.py`), if step (g) could be done at cost |left|2^{δm} + |right|2^{δm} per trial, the
   optimum moves to a ≈ 0.03–0.12 and reaches the floor 0.4856515 for every δ below the break-even
   δ* = 0.107 per block coordinate (2^{0.05n} in total), and nothing is gained for δ above it. What is
   achievable? For this matrix the Fredman–Volper cover (Ye–Li Section 3.2), restricted to rows of weight k,
   has degrees δ_L(b) = h(s) − b·h(s/b), δ_R(b) = (b − s)h(a/(b − s)) with s = 1/2 − a; the balanced optimum is
   0.059 at a = 0.0082, 0.134 at 0.025, 0.182 at 0.04, 0.244 at 0.07, 0.289 at 0.12 — above the break-even
   everywhere the masks are large enough to matter, and worse than brute force where they are not. Tying the
   degree to a in the joint model gives no improvement over the certified point even with an additive EXACTZ
   gain of 0.05 per coordinate, 2500 times Ye–Li's 2e-5 (`scripts/out/q_a_breakeven.txt`, last block).
3. **Multiplicity.** Even an ideal circuit would return multiplicity-weighted sums. Base needs the exact alias
   phase sum, so each alias class must count once; its dictionary deduplicates across the 2^{Ĥ} trials and across
   the ~1 surviving representation per trial. A circuit sums over all (trial, representation) hits. The checksum
   solves the same problem with inverse multiplicities μ_π(k) computed by retesting (OpenAI checksum l.342-357),
   which needs the object in hand; for aliases that costs 2^{γm}T ≈ 2^{0.041n} per class, so inverse-multiplicity
   weighting would cost 2^{(1 − η + 0.041)n} > 2^{τ0 n}. A weighted-count version of step (g) is therefore not
   available without a new deduplication idea. (For disjoint pairs the phase does factorize,
   χ((X ∪ Y) △ F) = χ(F)·Π_{X} ω_i·Π_{Y} ω_i with ω_i = e_P(±φ_i), so the alias phase sum *within one trial* is
   a bilinear form w_L^T M w_R that an EXACTZ circuit could evaluate with complex weights; the obstruction is
   only the cross-trial multiplicity.)
4. **Estimating instead of listing** the alias sum fails for variance reasons: it is a sum of 2^{(1−η)n} unit
   phasors with no product structure, so a sampling estimator with absolute error 1/16 needs about
   2^{2(1−η)n} samples. The checksum escapes this only through the Fourier product form of J_ρ(k).

The reverse direction, OpenAI/Base feeding Ye–Li, has no obvious entry point: Ye–Li's only bottleneck is
δ_L + δ_R, a property of a fixed 0/1 matrix, which modular hashing and Fourier estimation do not touch. The
item "Relation to Ye–Li: whether the two methods compose is open" in the paper's Section 10 can, I think, be
answered negatively at the level of these two constructions: the gains are in different places and neither
machinery addresses the other's bottleneck. A combined exponent, if one insists: the certified 0.4875754 (nothing
to add), with the hypothetical ceiling (1 − Δ)/2 = 0.48565 at the certified Δ if an ideal keyed compatibility
test with δ ≈ 0 and a deduplication scheme existed.

One structural remark worth recording: Ye–Li's "many correct keys" step (p. 8) is a whole-prefix layer argument,
not a half-block one: among the n/6 + 1 support layers of b = c − a, some layer has ≥ N_sum/(n/3 + 2) distinct
keys, where N_sum = |Σ(prefix)|. That is precisely the statement a_t ≥ 2^{−d}/poly for *some* layer t ≤ (size)/2
(Base's Lemma 3.3), used with full support; Ye–Li avoid Base's half-block restriction because they run every
layer s and need only existence, not a prescribed layer. This is the same obstacle as question (b).

---

## (b) "Corollary D beyond the half-block"

### Setting

Base's Lemma A5 (l.486-535) fixes an alias I; the trial's signing on the block satisfies c^F = c^I on
S = (I ∩ M) △ F and c^F = −c^I off S (Step 2). A ternary left mask with +1 on X ⊆ S (|X| = k1) and −1 on
X' ⊆ M \ S (|X'| = k2) therefore has left sum c^F(X) − c^F(X') = c^I(X ∪ X'); the right mask is
Y = (S \ X) ∪ X' and the pair represents S. So the representations of S are the sets U ∈ F(S) := {U ⊆ M :
|U ∩ S| = k1, |U \ S| = k2}, with k := k1 + k2, and coverage (Step 4) needs many distinct values of c^I(U).
The lemma the paper asks for (Section 10): for uniform S, E_S a_{k1,k2}(S) ≥ 2^{−g}/poly(n) with
a_{k1,k2}(S) := |{c^I(U) : U ∈ F(S)}| / (C(σ,k1)C(σ,k2)) and g inside the trial budget.

### Reduction (exact)

**Lemma R.** For any integer weights w on M, uniform σ-subset S, and any k1 ≤ σ, k2 ≤ m − σ,
E_S a_{k1,k2}(S) ≥ a_k(M) := |Σ_k(M)|/C(m,k).

Proof. For each distinct k-sum y of M fix a k-set K_y with w(K_y) = y. If |K_y ∩ S| = k1 then K_y ∈ F(S) and
y ∈ Σ(F(S)). Hence E_S|Σ(F(S))| ≥ |Σ_k(M)|·p with p = Pr_S[|K_y ∩ S| = k1] = C(k,k1)C(m−k, σ−k1)/C(m,σ). The
identity C(m,k)C(k,k1)C(m−k,σ−k1) = C(m,σ)C(σ,k1)C(m−σ,k2) (both sides count triples (U, S) with
|U ∩ S| = k1) gives p·C(m,k) = C(σ,k1)C(σ,k2) when m − σ = σ, so E_S a_{k1,k2}(S) ≥ a_k(M). ∎
(Brute-force check on 12 random instances: `scripts/out/q_b_sampling_identity.txt`.)

Conversely Σ(F(S)) ⊆ Σ_k(M), so a_{k1,k2}(S) ≤ a_k(M)·C(m,k)/(C(σ,k1)C(σ,k2)) ≤ a_k(M)·2^{k}/C(k,k1). The
needed lemma is therefore equivalent, up to 2^{O(k)} (which is exactly the scale at stake), to a lower bound on
the k-layer density of the whole signed block. The inside/outside split of the representations is irrelevant.

### What Base's tools give, and the loss

Base's Lemma 3.3 gives a layer t ≤ m/2 with a_t(M) ≥ 2^{−d(M)}/(m+1); the covering Lemma 3.1 gives
a_t(M) ≤ E_W a_k(M \ W) for W a uniform (t − k)-subset; and Σ_k(M \ W) ⊆ Σ_k(M). Hence

  a_k(M) ≥ 2^{−d(M)} · C(m − t + k, k) / ((m + 1) C(m, k)) ≥ 2^{−d(M) − k}/(m + 1),

the last step for t = m/2. (By (F2) d is signing-invariant, so d(M; c^I) = d(M).) The loss is the factor
C(m−t+k,k)/C(m,k) ≈ 2^{−k}, which is the "support m/2 + k" limit the paper identifies; it exceeds the 10 %
tolerance (in the paper's ternary optimum, k ≈ 0.008n of loss against a tolerance of about 0.003n). The exponent
d(M) itself is fine for the budget: under (LD) and (F3), d(M) ≤ f(m) + n^{0.6} ≤ (1/2 − τ0 + ζ)n + n^{0.6}, and
d(L) ≥ d(M) − 2n^{0.6} because |L| > m and f is nondecreasing, so a trial count 2^{d(M)} (computable exactly in
2^{m − d(M)} ≤ 2^{μn} time by the merge procedure) keeps every item of Lemma A7 unchanged. So the paper's
"g at most d(L), d(M) and (1/2 − τ0 + ζ)n" is the right budget and the whole question is:

**Layer-density conjecture [S].** For any multiset of m integers and 0 ≤ k ≤ m/2,
|Σ_k(M)| ≥ C(m,k)·|Σ(M)|·2^{−m}/poly(m), i.e. a_k(M) ≥ 2^{−d(M)}/poly(m).

Equivalently (μ_k := C(m,k)/|Σ_k| the mean multiplicity of a k-sum, μ_all := 2^m/|Σ| the mean multiplicity of a
subset sum): μ_k ≤ poly(m)·μ_all. Since |Σ| ≤ Σ_t |Σ_t| gives μ_all ≥ 1/E_{t∼Bin(m,1/2)}[1/μ_t], [S] follows
from **monotonicity** a_k ≥ a_t/poly for k < t ≤ m/2, which with Lemma 3.3 would prove the ternary lemma
losslessly with g = d(M).

### Evidence

- `q_b_layer_density.py`: 7832 (weights, k) instances, m ≤ 14, structured (equal classes, APs, powers, mixtures,
  cyclic types, squares) and random in [1..R]; restricted to instances where a_k ≥ 1/C(m,k) does not already
  imply the claim. Minimum of a_k 2^{d(M)}(m+1): 4.48 (a random instance). No violation.
- `q_b_local_search.py`: hill-climbing over weights (copy, perturb, sum-of-two moves) to minimize the same ratio
  for m ∈ {10,12,14}, k ∈ {1..4}: minima 4.9–31, the smallest at all-equal weights with k = m/2 − 1. Monotonicity
  a_k ≥ a_t for k < t ≤ m/2: 30744 pairs, zero violations, minimum ratio exactly 1.
- Heuristic: a layer-k collision (X, X') with w(X) = w(X') propagates to collisions (X ∪ Y, X' ∪ Y) for every
  Y ⊆ M \ (X ∪ X'), so layer collisions are "amplified" into the full subset-sum structure; in every explicit
  family I computed (j equal weights plus generic: a_k ≈ (1 − j/m)^k against 2^{−d} ≈ 2^{−j}; t equal classes;
  APs plus generic) a_k exceeds 2^{−d(M)} by an exponential margin. The examples where Base's Corollary D is
  lossy by 2^{k} (random half of an AP has 2^{k} times the k-layer density of the whole AP) are examples where
  d(M) is of order m, so they do not threaten [S].
- The Base-style form with E_V 2^{−d(V)} over v = m − 2k subsets in place of 2^{−d(M)} is false for the whole
  block in the degenerate corner (all-equal weights, v small), where Base's hypothesis (S3) C(σ,k)C(v,k) ≤ 2^v
  fails; the correct hypothesis for the whole-block version is C(m,k)C(v,k) ≤ 2^v, and in the regime of
  interest (k ≈ 0.04m) that holds comfortably.

### What I could not do

Prove [S] or monotonicity in general. The natural double-counting (pairs (x, W) ↦ x − w(W) from layer t to
layer k) loses the factor C(m−t+k,k)/C(m,k) in the fibre bound and I see no way to tighten it without using the
structure of the collisions. The paper's proposed route (a sumset argument "a sum of two pieces collapses only
if both are structured") is, by Lemma R, not needed: there are no two pieces, only the k-layer of one signed
multiset. If anyone wants to attack it, monotonicity of the layer density on [0, m/2] is the cleanest target;
its exact form (no poly loss) held in every test. A disproof would have to exhibit weights whose k-layer
collides at rate 2^{−c} with c ≫ d(M) + log m while the full subset-sum map has deficiency only d(M); the
propagation heuristic suggests c ≤ O(k·d(M)/m) + O(log m), i.e. [S] with large room, in which case the
ternary-mask gain of 2.35e-4 in Section 9 would be real, subject to the rest of Base's accounting.

## Files

| Script | Purpose | Output |
| --- | --- | --- |
| `scripts/q_a_breakeven.py` | break-even circuit degree, FV degrees in the sparse-row regime, joint model with EXACTZ gain | `scripts/out/q_a_breakeven.txt` |
| `scripts/q_b_sampling_identity.py` | brute-force check of Lemma R and the counting identity | `scripts/out/q_b_sampling_identity.txt` |
| `scripts/q_b_layer_density.py` | structured and random search for violations of [S] and of the Base-style form | `scripts/out/q_b_layer_density.txt` |
| `scripts/q_b_local_search.py` | hill-climbing minimization of the [S] ratio; monotonicity test | `scripts/out/q_b_local_search.txt` |
| `scripts/out/yeli_text.txt` | text extracted from `2610.10446v1.pdf` with page markers | |
