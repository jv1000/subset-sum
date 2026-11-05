# Section T (v3.1). Alias phase sums with ternary left masks (Theorem A′)

*Companion file to J. Voitle, "A certified exponent of 0.48758 for worst-case Subset Sum, and limits of the alias–checksum analysis" (draft, 5 November 2026). It gives the complete proofs of the ternary alias step stated in Appendix A of the paper, behind Theorem 3 (conditional on [S] and on Base's written proof). File names cited below refer to the project repository and its verification snapshot.*

v3.1 (5 November 2026): (EM), (SP) and (SK) are stated with the explicit ε0 slack; no number changes. The historical candidate hash below identifies the original JSON, including its metadata. The accompanying snapshot preserves every numerical input and corrects or omits obsolete display metadata; use MANIFEST.json for its file hashes.

v3 (round 7): applies the repairs of Astra's fresh referee report (`REFEREE_SECTION_T.md`, verdict PASS WITH REPAIRS).
All changes are to the text; no number changes. The frozen point `candidate_ternary.json` (sha256
ea2f10e89ea5f0073479e1e41cc5e22ffda31a5655966ee3f458e8cff25c422b) and all 33 certified conditions are unchanged
(`scripts/round7/out/recheck_v3.txt`). The changes: Base's scope (word-RAM model, success ≥ 2/3, b ≤ n^c) is
restored in the statement; the trial count is an explicit integer; the trial bound in Lemma T7 carries its
O(log n); the parameter table lists every condition Astra's inventory derives, including the small-prime and
right-key-sort totals and the cap margin; Lemmas T5–T6 are stated for the uncapped ideal execution; Lemma B2's
a_Γ ≤ ¾ is explained; the cutoffs are made explicit; cosmetic items. The diff is listed in `CHANGELOG_T_v2_to_v3.md`.

v2 (round 3): [S] carries a polynomial constant C_S(m) (Conjecture M′ + Lemma S); the remark "C_S = 3 if [S] comes
from monotonicity" is withdrawn (exact monotonicity is false, ROUND2_REPORT A.3).

Written in the style of Base (`base_PROOF_0.4877.tex`, cited by line number as "Base l.…"). It replaces Base's
Section 5 (l.301–612). Everything not restated is as in Base. The result is **conditional on [S]** (Section A of
`ROUND2_REPORT.md`: a_{k′}(M; w) ≥ 2^{−d(M)}/C_S(m) for every signing w, k′ ≤ 0.11m, with C_S(m) a fixed polynomial;
under Conjecture M′ of ROUND2_REPORT A.6, C_S(m) = P(m) + 2 by Lemma S) **and on Base's written proof**; the checksum
(Base Section 6 with J = 1, as in paper_v2 Section 8) is unchanged.

## T.1 Parameters and constraints

Parameters τ0, η, μ, γ, l as in Base l.136–156, with r = 1 − μ − l, Δ = η − τ0, Γ = 2τ0 − η, a_Γ = Δ/Γ,
ε = ζ = 10⁻⁸, guard 10⁸⌈log(b+1)⌉ ≤ n (Base l.193–194 with 10⁶ → 10⁸; it implies b + 2 ≤ 2^{n/10⁸+1}). New: two
mask fractions a (inside) and c (outside), with a′ := a + c. Sizes: m = 2⌊μn/2⌋, σ = m/2, k1 = ⌊am⌋, k2 = ⌊cm⌋,
k′ = k1 + k2, |L| = ⌊ln⌋, |R| = n − m − |L|. Write H3(a,c) = −a log a − c log c − (1−a−c) log(1−a−c) (so the number of
left masks is 2^{H3(a,c)m + O(log n)}) and h for binary entropy.

Constraints. All are certified in `scripts/round2/check_ternary_point.py` (arb, 200 bits) and, independently, in
Astra's `verify_a.py` (`SCALAR_SLACKS.md`, 50 decimal digits). The inequalities marked "<" are strict; (MU2), (SR),
the domain condition 2a′ ≤ ½ of (A4R), a_Γ ≤ ¾ and p, q ≥ 1 are non-strict by nature. At the certified point every
condition has positive slack, so the distinction does not matter there. Work bounds are proved in Lemma T7
("T7 item k" below); coverage in Lemma T5.

| | Inequality | Used in |
| --- | --- | --- |
| (C1R) | γ < h(2a)/2 + h(2c)/2 | T5 step 4: 2^{γm} ≤ C(σ,k1)C(σ,k2) for large n |
| (C2R) | l + (H3(a,c) − γ)μ < τ0 | T7 item 5: left records |
| (C3) | r + (1 − γ)μ < τ0 | T7 item 6: right class records (Base l.167) |
| (C4R) | 1 − μ + (H3(a,c) + h(½ − a + c) − γ)μ − η < τ0 | T7 item 7: visited tuples |
| (C5R) | max(H3(a,c), h(½ − a + c))μ + ½ − τ0 < τ0 | T7 item 2: both mask lists per trial × trials |
| (C6) | 0 < r < τ0, l < τ0 | T7 item 1: value maps (Base l.170) |
| (MU1) | μ < l | T3/T7: d(L) ≥ d(M) − 2n^{0.6} w.h.p. (replaces Base's (C7)) |
| (MU2) | μ ≤ ½ | T3: d(M) ≤ f(⌊n/2⌋) + n^{0.6} under (LD) (replaces (S2)) |
| (A4R) | μ(h(2a′) + 2a′) < η, with the domain condition 2a′ ≤ ½ | T4: all ≤2k′-sparse relations survive reduction mod P |
| (SR) | a′ ≤ 0.11 | range of [S] as derived from Conjecture M′ (Lemma S needs h(a′) ≤ ½); not a separate premise when [S] is assumed directly |
| (EM) | μ < τ0 − ε0 | T7 item 1: the exact |Σ(M)| merge costs 2^{m−d(M)}poly ≤ 2^{μn}poly (follows from (MU1), (C6)) |
| (SP) | ½ − τ0 + γμ/2 < τ0 − ε0 | T7 item 3: small-prime trial division, totalled over all trials ("small-prime-total") |
| (SK) | r + ½ − τ0 < τ0 − ε0 | T7 item 4: sorting the right keys by residue, totalled over all trials ("right-key-sort-total") |
| (CAP) | 1/guard + ζ < ε0 | Theorem A′: the cap is reached with probability o(1) ("cap-margin") |
| (A4G) | μ(h(2a′) + 2a′) + 1/guard < η | T4: the union bound is o(1) under the guard ("A4R-after-guard") |
| (PP) | τ0 < ½ | Base Proposition P (l.281–297): the preliminary threshold is separated from its cap |
| (PD) | η/2 < τ0 + 20ε | Base l.801: trial division for the large prime |

ε0 := least slack of (C1R)–(C6), (MU1), (MU2), (A4R) including its domain condition; at the certified point it is the
(C1R) slack, 9.994·10⁻⁷. v3.1 requires (EM), (SP) and (SK) with the explicit ε0 slack needed by T7, as in the paper appendix. The frozen point already satisfies these stronger requirements; no input parameter is changed. The ζ term from the trial count is retained in T7's overall exponent. (EM), (PP), (PD) were implicit in v2.

Checksum conditions (paper_v2 Section 8, Base Section 6 with J = 1): Δ > 0, Γ > 0; a_Γ ≤ ¾; p, q ≥ 1; ρ_c < ρ_f;
ρ_f + (18 + 6p)ε < η and ρ_f + (18 + 6q)ε < η (Lemma B3's decay rate, which replaces Base's fixed −0.00017);
log₂ M1 < ρ_c and log₂ M2 < ρ_c. On a_Γ ≤ ¾: in Lemma B2 (Base l.696–717) the row a_Γ w_v − u_v of the certificate
has rounding error (4a_Γ + 3)ε by (6.1) (l.694: |U − ū| ≤ 3ε, |W − w̄| ≤ 4ε), and the accounting 6εΣ_t z_t of the lemma
needs 4a_Γ + 3 ≤ 6, i.e. a_Γ ≤ ¾. Base l.702 justifies the 6ε by "coefficients of absolute value at most 1 (a_Γ < 1)",
which alone gives only 7ε; the detailed list on l.703 is correct and is what the lemma uses. Here a_Γ = 0.06248, slack
0.6875. The J = 1 certificates: region ρ_0 has z = (p, 0) with exponent p(Δ − u); the bounded regions ρ_1–ρ_8 have
z = (q, 0, 0) and the unbounded region ρ_9 has the two-entry vector z = (q, 0) (its G has one band row, l.640), all
with exponent q(a_Γ w − u); so the ten certificates are the two integrals M1 and M2. Base's (S1)–(S4), (C7), (C8) and
Lemma A4's δ are **not used**.

## T.2 The procedure

As Base l.332–383 with these changes.

- **Step 3 (trial count).** Compute |Σ(M)| exactly by the merge procedure of Proposition 2.4 (Base l.1015–1022),
  without a cap; cost 2^{m − d(M)} poly ≤ 2^{μn} poly. Fix once and for all a polynomial C̄_S with nonnegative integer
  coefficients and C̄_S(m) ≥ max(1, C_S(m)) for every m, where C_S is the polynomial of [S]; so C̄_S(m) ≤ n^{c_S} for a
  constant c_S. Put
  T := ⌈ C̄_S(m) · n⁸ · ⌈2^m / |Σ(M)|⌉ ⌉.
  The inner ceiling is of the exact rational 2^m/|Σ(M)| = 2^{d(M)} (d(M) itself is never computed); the outer ceiling
  is redundant when C̄_S has integer coefficients and is kept so that T is an integer for any majorant. Since
  2^{d(M)} ≤ ⌈2^{d(M)}⌉ < 2^{d(M)} + 1 ≤ 2·2^{d(M)},
  C̄_S(m) n⁸ 2^{d(M)} ≤ T ≤ 4 C̄_S(m) n⁸ 2^{d(M)}.
  (Base's sampled F̂, l.349–353, is not used.)
- **Step 4(c) (left records).** All triples (κ_L, X⁺, X⁻) with κ_L a key of L, X⁺, X⁻ ⊆ M disjoint, |X⁺| = k1,
  |X⁻| = k2, and b(κ_L) + b^F(X⁺) − b^F(X⁻) ≡ j′ (mod P′).
- **Step 4(d) (right classes).** All Y ⊆ M with |Y| = σ − k1 + k2, grouped by λ(Y) = (b^F(Y), c^F(Y)).
- **Step 4(f) (matching).** For a left record, the group with b(κ_R) + b_λ = T^F − b(κ_L) − b^F(X⁺) + b^F(X⁻), skipping
  the interval c(κ_R) + c_λ = t^F − c(κ_L) − c^F(X⁺) + c^F(X⁻).
- **Step 4(g) (expansion).** For each visited (κ_R, λ) and member Y: test X⁺ ∩ Y = ∅ and X⁻ ⊆ Y. If both hold, put
  Z := ((X⁺ ∪ Y) ∖ X⁻) △ F and insert (κ_L, κ_R, Z) into 𝒟_s unless present.
- **Step 6 (cap).** As Base l.379–382, with the count of steps including the exact |Σ(M)| computation. The cap is a
  property of the real run; Lemmas T5–T7 below are statements about the *uncapped ideal execution*, the run with the
  cap removed, and the real run's early stop at the cap is charged separately in Theorem A′.

## T.3 Lemmas

**Lemma T1 (soundness; Base Lemma A1, l.398–405).** Every key inserted into 𝒟_s is an alias class of t_s.

*Proof.* Let X⁺ ∩ Y = ∅ and X⁻ ⊆ Y, Z = ((X⁺ ∪ Y) ∖ X⁻) △ F. Since the sum over a disjoint union is additive and
X⁻ ⊆ Y, b^F(X⁺) − b^F(X⁻) + b^F(Y) = b^F((X⁺ ∪ Y) ∖ X⁻) = b(Z) − b(F) by (5.1) (Base l.338), and likewise for c.
The group condition then gives b(A) + b(Z) − b(F) + b(B) = T^F, so b(I) = T_{s,q} for I = A ∪ Z ∪ B, and the skipped
interval gives c(I) ≠ t_s. The rest is Base's argument. ∎

**Lemma T2 (counts; Base Lemma A2, l.411–422).** Unchanged: L has at most (n+1)2^{|L|−d(L)} keys; every trial has at
most (2m+1)2^{m−d(M)} right classes (c^F(Y) = c(Y △ F) − c(F) ∈ Σ(M) − c(F), independent of |Y|).

**Lemma T3 (trial count and deficiencies).** With probability 1 − o(1) over M and L: (i) d(L) ≥ d(M) − 2n^{0.6};
(ii) under (LD), d(M) ≤ (½ − τ0 + ζ)n + n^{0.6}.

*Proof.* M is a uniform m-subset of [n] and L a uniform |L|-subset; (F3) (Base l.206–209) gives
|d(M) − f(m)| ≤ n^{0.6} and |d(L) − f(|L|)| ≤ n^{0.6} except with probability 4e^{−n^{0.2}/2}. Since |L| > m by (MU1)
and f is nondecreasing, d(L) ≥ f(|L|) − n^{0.6} ≥ f(m) − n^{0.6} ≥ d(M) − 2n^{0.6}. For (ii), m ≤ ⌊n/2⌋ by (MU2), so
f(m) ≤ f(⌊n/2⌋) ≤ (½ − τ0 + ζ)n under (LD) (Base l.295–297). ∎

Let ℰ₃ be this event; it depends only on M and L.

**Lemma T4 (distinctions survive reduction; replaces Base Lemma A4, l.468–476).** With probability 1 − o(1) over
P, every λ ∈ {−1,0,1}^M with at most 2k′ nonzero entries and Σλ_i c_i ≠ 0 has P ∤ Σλ_i c_i.

*Proof.* There are at most Σ_{j≤2k′} C(m,j)2^j ≤ 2^{(h(2a′)+2a′)m + O(log n)} such vectors (2a′ ≤ ½). Each nonzero
sum has absolute value below 2^{b+O(log n)}, so by (F4) (Base l.210–212) with L′ = ⌊ηn⌋ it is divisible by P with
probability at most poly(n)(b + log n)2^{−ηn}. A union bound gives poly(n)(b + log n)2^{−(η − μ(h(2a′)+2a′))n}. Under
the guard, b + log n ≤ 2^{n/10⁸ + 2}, so this is at most poly(n)2^{−(η − μ(h(2a′)+2a′) − 1/10⁸)n} = o(1) by (A4G). ∎

On this event, for any U, U′ ⊆ M with |U|, |U′| ≤ k′ and any signs ε_i: Σ_U ε_i c_i ≠ Σ_{U′} ε_i c_i implies
Σ_U ε_i b_i ≠ Σ_{U′} ε_i b_i (the difference is such a λ; Base's argument at l.478–482).

**Lemma T5 (one trial; replaces Base Lemma A5, l.486–535).** Consider the uncapped ideal execution. Assume (LD), ℰ₃,
the event of Lemma T4, and [S] with polynomial constant C_S = C_S(m) (a_{k′}(M; w) ≥ 2^{−d(M)}/C_S(m) for every
signing w of M, k′ ≤ 0.11m). Fix s, an alias I ∈ 𝒜_s(P) with carry q, and one trial for (s,q). The trial inserts the
key of the class of I with probability at least
2^{−d(M)} / (16 K₀ n² (m+1) C_S) ≥ 2^{−d(M)} / (C_S n⁶),
where K₀ ≥ 1 is the absolute constant of (F4) in Base l.511–512, and the second inequality holds whenever
16K₀(m+1) ≤ n⁴, in particular (as m + 1 ≤ n) for all n with n³ ≥ 16K₀. The lemma also needs ⌊γm⌋ ≥ L_* for (F4).
Neither threshold depends on I, s, P or M.

*Proof.* Steps 1–2 as Base (l.492–499): with probability ≥ 1/(m+1), S := (I ∩ M) △ F has |S| = σ, and then S is a
uniform σ-subset of M; on S the trial's signed weights are c^I (c^I_i = c_i on I ∩ M, −c_i off I), and on M ∖ S
they are −c^I.

*Step 3 (representations).* For X⁺ ⊆ S, |X⁺| = k1, and X⁻ ⊆ M ∖ S, |X⁻| = k2, put U = X⁺ ∪ X⁻ and
Y = (S ∖ X⁺) ∪ X⁻. The left record's reduced weight is b(A) + b^F(X⁺) − b^F(X⁻) = b(A) + b^I(U) (the sign flip off S
cancels the −1 entries). So the family of left keys is {b(A) + b^I(U) : U ∈ ℱ(S)} with
ℱ(S) = {U ⊆ M : |U ∩ S| = k1, |U ∖ S| = k2}, and |ℱ(S)| = C(σ,k1)C(σ,k2).

*Step 3′ (many distinct keys).* Lemma R (paper_v2 Section 10; proof: for each distinct k′-sum y of (M, c^I) fix a
witness K_y; Pr_S[|K_y ∩ S| = k1] = C(k′,k1)C(m−k′, σ−k1)/C(m,σ), and C(m,k′)C(k′,k1)C(m−k′,σ−k1) =
C(m,σ)C(σ,k1)C(σ,k2)) gives E_S[|{c^I(U) : U ∈ ℱ(S)}|/(C(σ,k1)C(σ,k2))] ≥ a_{k′}(M; c^I). By (F2) (Base l.204–205)
d(M; c^I) = d(M), so [S] gives ≥ 2^{−d(M)}/C_S. By Lemma T4 the reduced keys b(A) + b^I(U) are distinct whenever the
c^I(U) are, so B_S := #distinct left keys satisfies E_S[B_S/(C(σ,k1)C(σ,k2))] ≥ 2^{−d(M)}/C_S. (No "bad S" term:
Lemma T4 is global.)

*Step 4 (the small prime keeps many residues).* Base l.509–520 verbatim with C(σ,k) replaced by C(σ,k1)C(σ,k2):
the key set lies in (−nP, nP) and is fixed before P′, j′ are drawn; (F4) with L′ = ⌊γm⌋ gives
E_{P′} Σ_y z_y² ≤ B_S + K₀n²B_S²2^{−γm}; Markov and Cauchy–Schwarz give, with probability ≥ ½ over P′, at least
min(B_S, 2^{γm})/(4K₀n²) occupied residues, so a uniform j′ hits an occupied residue with probability ≥
min(B_S 2^{−γm}, 1)/(8K₀n²) ≥ B_S/(8K₀n² C(σ,k1)C(σ,k2)), using B_S ≤ C(σ,k1)C(σ,k2) and 2^{γm} ≤ C(σ,k1)C(σ,k2),
which (C1R) gives for all large n (the floors in k1, k2 and the Stirling factors cost O(log m) in the exponent).

*Step 5 (a hit is recovered).* If j′ ≡ b(A) + b^I(U) for U = X⁺ ∪ X⁻ ∈ ℱ(S), the left record (κ(A), X⁺, X⁻) is listed.
With Y = (S ∖ X⁺) ∪ X⁻: b^F(Y) = b^I(S ∖ X⁺) − b^I(X⁻), so b(A) + b^I(U) + b^F(Y) + b(B) = b(A) + b^I(S) + b(B) =
b(A) + b(I ∩ M) − b(F) + b(B) = T^F (by (5.1) with Z = S, S △ F = I ∩ M). The class record (κ(B), λ(Y)) is listed and
visited (unreduced sum c(I) − c(F) ≠ t^F as I is an alias); X⁺ ∩ Y = ∅ and X⁻ ⊆ Y hold, and Z = ((X⁺ ∪ Y) ∖ X⁻) △ F =
S △ F = I ∩ M, so the key (κ(A), κ(B), I ∩ M) is inserted. In the uncapped ideal execution every listed record is
processed, so this insertion happens.

*Step 6.* Multiply: (1/(m+1))·(½)·E_S[B_S/(8K₀n²C(σ,k1)C(σ,k2))] ≥ 2^{−d(M)}/(16K₀n²(m+1)C_S), and
16K₀n²(m+1) ≤ n⁶ when 16K₀(m+1) ≤ n⁴. ∎

**Corollary T6 (coverage; Base Corollary A6, l.537–543).** In the uncapped ideal execution, under the assumptions of
Lemma T5 and for n above its thresholds, except with probability o(1) every alias class of every target is in its
dictionary at the end of Step 4.

*Proof.* Condition on P, φ, M, L. The T trials for a pair (s,q) are independent, and T ≥ C̄_S(m) n⁸ 2^{d(M)} ≥
C_S n⁸ 2^{d(M)} by Step 3. By Lemma T5 all of them miss a fixed alias class with carry q with probability at most
(1 − 2^{−d(M)}/(C_S n⁶))^T ≤ exp(−T·2^{−d(M)}/(C_S n⁶)) ≤ e^{−n²}. (The constant C_S cancels: the trial count
carries it. Each target/subset pair has a unique carry, so no factor for carries is needed.) There are at most
(nN₀+1)2^n pairs of a target and a subset, and (nN₀+1)2^n e^{−n²} = o(1), with a threshold depending only on N₀. ∎

**Lemma T7 (expected work; Base Lemma A7, l.547–589).** Assume (LD) and ℰ₃; condition on M, L; average over P and
the trials; the phases are arbitrary. The uncapped ideal execution takes in expectation at most
(b+2)2^{(τ0 − ε0 + ζ)n + O(n^{0.6})} steps.

*Proof.* T ≤ 4C̄_S(m)n⁸2^{d(M)} ≤ 2^{d(M) + O(log n)} by Step 3; with T3(i), T ≤ 2^{d(L) + 2n^{0.6} + O(log n)}; with
T3(ii), T ≤ 2^{(½−τ0+ζ)n + O(n^{0.6})}. There are O(n³) pairs (s,q). Polynomial factors (including C̄_S(m) ≤ n^{c_S})
go into 2^{O(n^{0.6})}.
1. *Value maps and Step 3:* 2^{|L|} + 2^{|R|} + 2^{m − d(M)}poly: exponents l, r, μ < τ0 − ε0 by (C6), (MU1) and (EM).
2. *Masks:* per trial ≤ 2^{H3(a,c)m + O(log n)} + 2^{h(½−a+c)m + 1} (both lists, every trial); times
   T ≤ 2^{(½−τ0+ζ)n + O(n^{0.6})}: exponent max(H3, h(½−a+c))μ + ½ − τ0 + ζ < τ0 − ε0 + ζ by (C5R).
3. *Small primes:* n³2^{γm/2+1} divisions per trial; total 2^{(½ − τ0 + ζ + γμ/2)n + O(n^{0.6})}; below the bound by (SP).
4. *Sorting keys by residue:* (n+1)(2^{|L|−d(L)} + 2^{|R|}) per trial; total ≤ 2^{ln + O(n^{0.6})} + 2^{(r + ½ − τ0 + ζ)n + O(n^{0.6})}
   (T3); below the bound by (C6) and (SK).
5. *Left records:* (n+1)2^{|L|−d(L)}·2^{H3(a,c)m + O(log n)}·2^{1−γm} per trial in expectation (for fixed choices other
   than j′, a triple is listed with probability 1/P′ ≤ 2^{1−γm}); T ≤ 2^{d(L) + 2n^{0.6} + O(log n)} (T3(i)); total
   2^{(l + (H3(a,c) − γ)μ)n + O(n^{0.6})}. Use (C2R).
6. *Right class records:* (n+1)2^{|R|}(2m+1)2^{m−d(M)}2^{1−γm} per trial; T ≤ 2^{d(M)+O(log n)} cancels d(M)
   exactly: 2^{(r + (1−γ)μ)n + O(n^{0.6})}. Use (C3). Listing the classes themselves costs 2^{m + O(log n)}; use (EM).
7. *Visits and expansions:* count every expanded member, including those failing the test X⁺ ∩ Y = ∅, X⁻ ⊆ Y. Fix
   unreduced values x_L ∈ Σ(L), x_R ∈ Σ(R) and masks X⁺, X⁻, Y before P, and put
   D = x_L + c^F(X⁺) − c^F(X⁻) + x_R + c^F(Y) − t^F, independent of P. A visited tuple (κ_L, X⁺, X⁻, κ_R, Y) with
   c(κ_L) = x_L, c(κ_R) = x_R needs D ≠ 0 (the exact interval is skipped), P | D (the reduced weights add to
   T^F ≡ t^F mod P), and the two small-prime conditions, which given everything else hold for at most one residue j′.
   By (F4), Pr_P[P | D] ≤ poly(n)(b + log n)2^{−ηn} as |D| < 2^{b+O(log n)}; by Lemma T2 at most (n+1)² key pairs share
   (x_L, x_R). Per trial ≤ poly(n)(b + log n)2^{|L|−d(L)+|R|−d(R)}·2^{H3(a,c)m}·2^{h(½−a+c)m}·2^{−ηn−γm}; with d(R) ≥ 0
   and T ≤ 2^{d(L)+2n^{0.6}+O(log n)}: (b + log n)2^{(1 − μ + (H3(a,c) + h(½−a+c) − γ)μ − η)n + O(n^{0.6})}. Use (C4R).
   This averages over P without conditioning on the event of Lemma T4; only coverage uses that event.
8. *Matching, dictionaries, output:* polynomial per record, tuple and key. ∎

**Theorem A′.** Under [S] with polynomial constant C_S(m), the procedure of T.2 has the properties of Base's
Theorem A (l.319–330) with the constants of T.1, for all sufficiently large n: on (LD), with P uniform and φ arbitrary,
it returns with probability 1 − o(1) values Â_s within 1/16 of Σ_{I∈𝒜_s(P)} χ(I) for every s; on every execution it
uses at most 2^{τ0 n + 2n^{0.7}} poly(n+b+2) word operations.

*Proof.* As Base Section 5.8 (l.593–612). Part 2 is the cap. For part 1, the failure events, combined by a union bound:
ℰ₃ fails with probability o(1) (T3); Lemma T4's event fails with probability o(1) (M is independent of P); given both,
some alias class is missed in the uncapped ideal execution with probability o(1) (T6); the cap is reached, which by
Markov's inequality and Lemma T7 (not conditioned on T4's event) has probability
o(1) + (b+2)2^{(τ0−ε0+ζ)n+O(n^{0.6})}/2^{τ0 n + n^{0.7}} = o(1), because b + 2 ≤ 2^{n/10⁸+1} and 10⁻⁸ + ζ < ε0 (CAP);
a bounded sampler fails with probability 2^{O(n)}(2^{−n³} + e^{−c₀n²}) = o(1). Outside these events the real run
coincides with the uncapped ideal execution, 𝒟_s contains every alias class (T6) and nothing else (T1), and the output
precision is as in Base (l.608–612). ∎

**Scope.** With Theorem A′ in place of Theorem A, Base's Theorem 1 (l.765–810) gives, in Base's word-RAM model (word
length (1.1) of the paper), a uniform randomized algorithm that halts on every execution, answers correctly with
probability at least 2/3 for every input with n ≥ 2 (exact fallback below the cutoff n_* and when the guard fails),
and on every execution with n ≥ n_* that passes the guard uses at most
2^{(τ0 + 20ε)n + 2n^{0.7}} poly(n + b + 2)
word operations. For each fixed positive integer c, every input with n ≥ N_c and b ≤ n^c passes the guard, and the
factor 2^{2n^{0.7}}poly(n + n^c + 2) is absorbed by any fixed T′ > τ0 + 20ε; the address-space argument of Base l.809–810
applies unchanged. This gives O_{c,T′}(2^{T′n}) word operations for every T′ > T := τ0 + 20ε. The pure exponential
bound is claimed only in that range (b ≤ n^c for a fixed c); for larger b, only the displayed bound with its
poly(n + b + 2) factor and the exact fallback are claimed, as in Base l.58–66 and 806–810.

## T.4 The certified point (`candidate_ternary.json`)

| Parameter | Value |
| --- | --- |
| τ0 | 0.4873405528 |
| η | 0.5159974155 |
| μ | 0.4746795055 |
| a, c | 0.0035141538, 0.0035141537 (a′ = 0.0070283075) |
| γ | 0.0603737099 |
| l | 0.4840025845 |
| κ, p, q_m | 1.03462910, 8.46825883, 8.27946618 |
| filter | 16 cosine + 16 sine terms per density, 8 decimals (in the JSON) |
| ε, ζ, guard | 10⁻⁸, 10⁻⁸, 10⁸ |
| ρ_f, ρ_c | η − 1.5·10⁻⁶, ρ_f − 10⁻⁶ |
| **T = τ0 + 20ε** | **0.4873407528** |

All 33 conditions of `scripts/round2/check_ternary_point.py` pass in arb at 200 bits
(`scripts/round2/out/ternary_certificate_N4096_8192.txt`, re-run unchanged in round 7). Tightest:
C1R 9.99·10⁻⁷ (= ε0), B3 8.1·10⁻⁷, C2R/C3/C4R 1.30·10⁻⁶, C5R 1.60·10⁻⁶, M1 3.04·10⁻⁶, M2 3.30·10⁻⁶.
The conditions added to the table in v3 have slacks (SP) 0.4604, (SK) 0.4334, (CAP) 9.79·10⁻⁷, (A4G) 0.4587,
(EM) 0.01266, (PP) 0.01266, (PD) 0.2293 (`scripts/round7/out/recheck_v3.txt`); they agree with Astra's independent
50-digit intervals (`SCALAR_SLACKS.md`), which also certify both moments with an independently written interval FFT:
log₂ M1 = 0.51599187405865778648, log₂ M2 = 0.51599162047014794189, ball radii below 4·10⁻⁵⁵, identical at
N = 1024, 4096, 8192 here and at N = 4096, 8192 in Astra's certificate. The point is 2.3465·10⁻⁴ below the certified
Section 8 point (T = 0.4875754036) and 3.352·10⁻⁴ below JoshuaQFEX.

**Statement.** *Conditional on [S] and on Base's written proof*: there is a uniform randomized algorithm for Subset
Sum in Base's word-RAM model that halts on every execution and answers correctly with probability at least 2/3 on
every input with n ≥ 2, and, for every fixed positive integer c and every fixed T′ > T = 0.4873407528, processes every
input with n ≥ N_{c,T′} and b ≤ n^c in at most C_{c,T′}·2^{T′n} word operations on every outcome of its random choices;
in particular O_c(2^{0.4873408n}) for b ≤ n^c. (Not 0.48734: that is below T. The threshold is the exact decimal
T = τ0 + 20ε; no exponent is rounded down.) For inputs with b above every fixed polynomial in n, only the bound
2^{Tn + 2n^{0.7}}poly(n + b + 2) under the guard, and the exact fallback otherwise, are claimed.

**Cutoffs.** The o(1) terms depend only on n (and on the fixed constants of Base and of [S]), so a fixed cutoff n_*
exists; it is not numeric, and several thresholds enter it:
- Base's preliminary search: ζ = 10⁻⁸ makes Proposition P need n > 10⁸ and its Chebyshev term 4/(ζ²n) small only
  for n of order 10¹⁷ (as for the Section 8 point).
- Lemma T5: (F4) needs ⌊γm⌋ ≥ L_*, and the bound 2^{−d(M)}/(C_S n⁶) needs 16K₀(m+1) ≤ n⁴, which holds for
  n³ ≥ 16K₀ since m + 1 ≤ n; K₀ and L_* are the absolute constants of (F4). The polynomial C_S(m) of [S] is absorbed
  into the trial count (Step 3) and into 2^{O(n^{0.6})} (Lemma T7), and cancels in Corollary T6, so no threshold
  depends on C_S; but the thresholds above remain. (The analogous cutoff for Base's own Lemma A5 is
  32K₀n²(m+1)(v+1) ≤ n⁶, a different inequality; it is not used here.)
- Corollary T6: (nN₀+1)2^n e^{−n²} ≤ 1/n, a threshold depending on N₀.
- Theorem A′: the cap probability (b+2)2^{(τ0−ε0+ζ)n+O(n^{0.6})−τ0n−n^{0.7}} is o(1) once the exponent
  −(ε0 − ζ − 10⁻⁸)n − n^{0.7} + O(n^{0.6}) + 1 is negative; (CAP) gives ε0 − ζ − 10⁻⁸ = 9.79·10⁻⁷ > 0, and the threshold
  depends on the O(n^{0.6}) constants of Lemma T7 and (F3). Separately, the absorption of 2^{2n^{0.7}}poly(n + n^c)
  into 2^{(T′−T)n} has its own threshold N_{c,T′}.
Exact layer-density monotonicity is false (ROUND2_REPORT A.3, m = 8), so [S] is taken from Conjecture M′
(a_t ≤ P(m)·a_k for t ∈ [k, m−k], k ≤ 0.11m) through Lemma S, which gives C_S(m) = P(m) + 2.
