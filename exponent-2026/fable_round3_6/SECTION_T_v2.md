# Section T (v2). Alias phase sums with ternary left masks (Theorem A′)

v2 (round 3): [S] carries a polynomial constant C_S(m) (Conjecture M′ + Lemma S); the trial count is C_S(m)·n⁸⌈2^{d(M)}⌉;
the remark "C_S = 3 if [S] comes from monotonicity" is withdrawn (exact monotonicity is false, ROUND2_REPORT A.3).
No numerical condition changes; the certificate `candidate_ternary.json` is unaffected.

Written in the style of Base (`base_PROOF_0.4877.tex`, cited by line number as "Base l.…"). It replaces Base's
Section 5 (l.301-614). Everything not restated is as in Base. The result is **conditional on [S]** (Section A of
`ROUND2_REPORT.md`: a_{k′}(M; w) ≥ 2^{−d(M)}/C_S(m) for every signing w, k′ ≤ 0.11m, with C_S(m) a fixed polynomial;
under Conjecture M′ of ROUND2_REPORT A.6, C_S(m) = P(m) + 2 by Lemma S) **and on Base's written proof**; the checksum (Base Section 6 with J = 1, as in paper_v2 Section 8)
is unchanged.

## T.1 Parameters and constraints

Parameters τ0, η, μ, γ, l as in Base l.136-152, with r = 1 − μ − l, Δ = η − τ0, Γ = 2τ0 − η, ε = ζ = 10⁻⁸, guard
10⁸⌈log(b+1)⌉ ≤ n (Base l.192-194 with 10⁶ → 10⁸). New: two mask fractions a (inside) and c (outside), with
a′ := a + c. Sizes: m = 2⌊μn/2⌋, σ = m/2, k1 = ⌊am⌋, k2 = ⌊cm⌋, k′ = k1 + k2, |L| = ⌊ln⌋, |R| = n − m − |L|.
Write H3(a,c) = −a log a − c log c − (1−a−c) log(1−a−c) (so the number of left masks is 2^{H3(a,c)m + O(log n)}) and
h for binary entropy.

Constraints (all strict; certified in `scripts/round2/check_ternary_point.py`):

| | Inequality | Used in |
| --- | --- | --- |
| (C1R) | γ < h(2a)/2 + h(2c)/2 | T5 step 4: P′ ≤ C(σ,k1)C(σ,k2) |
| (C2R) | l + (H3(a,c) − γ)μ < τ0 | T6 item 5: left records |
| (C3) | r + (1 − γ)μ < τ0 | T6 item 6: right class records (Base l.163) |
| (C4R) | 1 − μ + (H3(a,c) + h(½ − a + c) − γ)μ − η < τ0 | T6 item 7: visited tuples |
| (C5R) | max(H3(a,c), h(½ − a + c))μ + ½ − τ0 < τ0 | T6 item 2: masks listed per trial × trials |
| (C6) | 0 < r < τ0, l < τ0 | T6 item 1 (Base l.166) |
| (MU1) | μ < l | T3/T6: d(L) ≥ d(M) − 2n^{0.6} w.h.p. (replaces C7) |
| (MU2) | μ ≤ ½ | T3: d(M) ≤ f(⌊n/2⌋) + n^{0.6} under (LD) (replaces S2) |
| (A4R) | μ(h(2a′) + 2a′) < η, 2a′ ≤ ½ | T4: all ≤2k′-sparse relations survive reduction mod P |
| (SR) | a′ ≤ 0.11 | range of [S] as derived from Conjecture M′ (Lemma S, h(a′) ≤ ½) |

ε0 := least slack of (C1R)-(C6), (MU1), (MU2), (A4R). Also 1/guard + ζ < ε0 (T7), η/2 < τ0 + 20ε (prime draw),
τ0 < ½ (Proposition P), and the checksum conditions of paper_v2 Section 8 (Δ, Γ > 0, a_Γ ≤ ¾, p, q ≥ 1, ρ_c < ρ_f,
ρ_f + (18 + 6 max(p,q))ε < η, log₂ M1, log₂ M2 < ρ_c). Base's (S1)-(S4), (C7), (C8) and Lemma A4's δ are **not used**.

## T.2 The procedure

As Base l.332-387 with these changes.

- **Step 3 (trial count).** Compute |Σ(M)| exactly by the merge procedure of Proposition 2.4 (Base l.1015-1022), i.e.
  d(M) = m − log|Σ(M)|. Cost 2^{m − d(M)} poly ≤ 2^{μn} poly. Put T := C_S(m)·n⁸ ⌈2^{d(M)}⌉, where C_S(m) ≤ n^{c_S} is the polynomial of [S]. (Base's sampled F̂ is not used.)
- **Step 4(c) (left records).** All triples (κ_L, X⁺, X⁻) with κ_L a key of L, X⁺, X⁻ ⊆ M disjoint, |X⁺| = k1,
  |X⁻| = k2, and b(κ_L) + b^F(X⁺) − b^F(X⁻) ≡ j′ (mod P′).
- **Step 4(d) (right classes).** All Y ⊆ M with |Y| = σ − k1 + k2, grouped by λ(Y) = (b^F(Y), c^F(Y)).
- **Step 4(f) (matching).** For a left record, the group with b(κ_R) + b_λ = T^F − b(κ_L) − b^F(X⁺) + b^F(X⁻), skipping
  the interval c(κ_R) + c_λ = t^F − c(κ_L) − c^F(X⁺) + c^F(X⁻).
- **Step 4(g) (expansion).** For each visited (κ_R, λ) and member Y: test X⁺ ∩ Y = ∅ and X⁻ ⊆ Y. If both hold, put
  Z := ((X⁺ ∪ Y) ∖ X⁻) △ F and insert (κ_L, κ_R, Z) into 𝒟_s unless present.
- **Step 6 (cap).** As Base, with the count of steps including the exact |Σ(M)| computation.

## T.3 Lemmas

**Lemma T1 (soundness; Base Lemma A1, l.398-409).** Every key inserted into 𝒟_s is an alias class of t_s.

*Proof.* Let X⁺ ∩ Y = ∅ and X⁻ ⊆ Y, Z = ((X⁺ ∪ Y) ∖ X⁻) △ F. Since the sum over a disjoint union is additive and
X⁻ ⊆ Y, b^F(X⁺) − b^F(X⁻) + b^F(Y) = b^F((X⁺ ∪ Y) ∖ X⁻) = b(Z) − b(F) by (5.1) (Base l.335-337), and likewise for c.
The group condition then gives b(A) + b(Z) − b(F) + b(B) = T^F, so b(I) = T_{s,q} for I = A ∪ Z ∪ B, and the skipped
interval gives c(I) ≠ t_s. The rest is Base's argument. ∎

**Lemma T2 (counts; Base Lemma A2, l.411-422).** Unchanged: L has at most (n+1)2^{|L|−d(L)} keys; every trial has at
most (2m+1)2^{m−d(M)} right classes (c^F(Y) = c(Y △ F) − c(F) ∈ Σ(M) − c(F), independent of |Y|).

**Lemma T3 (trial count and deficiencies).** With probability 1 − o(1) over M and L: (i) d(L) ≥ d(M) − 2n^{0.6};
(ii) under (LD), d(M) ≤ (½ − τ0 + ζ)n + n^{0.6}.

*Proof.* M is a uniform m-subset of [n] and L a uniform |L|-subset; (F3) (Base l.207-211) gives
|d(M) − f(m)| ≤ n^{0.6} and |d(L) − f(|L|)| ≤ n^{0.6} except with probability 4e^{−n^{0.2}/2}. Since |L| > m by (MU1)
and f is nondecreasing, d(L) ≥ f(|L|) − n^{0.6} ≥ f(m) − n^{0.6} ≥ d(M) − 2n^{0.6}. For (ii), m ≤ ⌊n/2⌋ by (MU2), so
f(m) ≤ f(⌊n/2⌋) ≤ (½ − τ0 + ζ)n under (LD) (Base l.295-297). ∎

Let ℰ₃ be this event; it depends only on M and L.

**Lemma T4 (distinctions survive reduction; replaces Base Lemma A4, l.468-482).** With probability 1 − o(1) over
P, every λ ∈ {−1,0,1}^M with at most 2k′ nonzero entries and Σλ_i c_i ≠ 0 has P ∤ Σλ_i c_i.

*Proof.* There are at most Σ_{j≤2k′} C(m,j)2^j ≤ 2^{(h(2a′)+2a′)m + O(log n)} such vectors (2a′ ≤ ½). Each nonzero
sum has absolute value below 2^{b+O(log n)}, so by (F4) with L′ = ⌊ηn⌋ it is divisible by P with probability at most
poly(n)(b + log n)2^{−ηn}. A union bound gives poly(n)(b + log n)2^{−(η − μ(h(2a′)+2a′))n}, which is o(1) under the
guard by (A4R). ∎

On this event, for any U, U′ ⊆ M with |U|, |U′| ≤ k′ and any signs ε_i: Σ_U ε_i c_i ≠ Σ_{U′} ε_i c_i implies
Σ_U ε_i b_i ≠ Σ_{U′} ε_i b_i (the difference is such a λ; Base's argument at l.478-482).

**Lemma T5 (one trial; replaces Base Lemma A5, l.486-535).** Assume (LD), ℰ₃, the event of Lemma T4, and [S] with
polynomial constant C_S = C_S(m) (a_{k′}(M; w) ≥ 2^{−d(M)}/C_S(m) for every signing w of M, k′ ≤ 0.11m). Fix s, an alias I ∈ 𝒜_s(P) with
carry q, and one trial for (s,q). The trial inserts the key of the class of I with probability at least
2^{−d(M)}/(C_S n^6).

*Proof.* Steps 1-2 as Base (l.493-503): with probability ≥ 1/(m+1), S := (I ∩ M) △ F has |S| = σ, and then S is a
uniform σ-subset of M; on S the trial's signed weights are c^I (c^I_i = c_i on I ∩ M, −c_i off I), and on M ∖ S
they are −c^I.

*Step 3 (representations).* For X⁺ ⊆ S, |X⁺| = k1, and X⁻ ⊆ M ∖ S, |X⁻| = k2, put U = X⁺ ∪ X⁻ and
Y = (S ∖ X⁺) ∪ X⁻. The left record's reduced weight is b(A) + b^F(X⁺) − b^F(X⁻) = b(A) + b^I(U) (the sign flip off S
cancels the −1 entries). So the family of left keys is {b(A) + b^I(U) : U ∈ ℱ(S)} with
ℱ(S) = {U ⊆ M : |U ∩ S| = k1, |U ∖ S| = k2}, and |ℱ(S)| = C(σ,k1)C(σ,k2).

*Step 3′ (many distinct keys).* Lemma R (paper_v2 Section 10; proof: for each distinct k′-sum y of (M, c^I) fix a
witness K_y; Pr_S[|K_y ∩ S| = k1] = C(k′,k1)C(m−k′, σ−k1)/C(m,σ), and C(m,k′)C(k′,k1)C(m−k′,σ−k1) =
C(m,σ)C(σ,k1)C(σ,k2)) gives E_S[|{c^I(U) : U ∈ ℱ(S)}|/(C(σ,k1)C(σ,k2))] ≥ a_{k′}(M; c^I). By (F2) d(M; c^I) = d(M),
so [S] gives ≥ 2^{−d(M)}/C_S. By Lemma T4 the reduced keys b(A) + b^I(U) are distinct whenever the c^I(U) are, so
B_S := #distinct left keys satisfies E_S[B_S/(C(σ,k1)C(σ,k2))] ≥ 2^{−d(M)}/C_S. (No "bad S" term: Lemma T4 is global.)

*Step 4 (the small prime keeps many residues).* Base l.511-523 verbatim with C(σ,k) replaced by C(σ,k1)C(σ,k2):
with probability ≥ ½ over P′, a uniform j′ hits an occupied residue with probability ≥
min(B_S 2^{−γm}, 1)/(8K₀n²) ≥ B_S/(8K₀n² C(σ,k1)C(σ,k2)), using 2^{γm} ≤ C(σ,k1)C(σ,k2) (C1R).

*Step 5 (a hit is recovered).* If j′ ≡ b(A) + b^I(U) for U = X⁺ ∪ X⁻ ∈ ℱ(S), the left record (κ(A), X⁺, X⁻) is listed.
With Y = (S ∖ X⁺) ∪ X⁻: b^F(Y) = b^I(S ∖ X⁺) − b^I(X⁻), so b(A) + b^I(U) + b^F(Y) + b(B) = b(A) + b^I(S) + b(B) =
b(A) + b(I ∩ M) − b(F) + b(B) = T^F (by (5.1) with Z = S, S △ F = I ∩ M). The class record (κ(B), λ(Y)) is listed and
visited (unreduced sum c(I) − c(F) ≠ t^F as I is an alias); X⁺ ∩ Y = ∅ and X⁻ ⊆ Y hold, and Z = ((X⁺ ∪ Y) ∖ X⁻) △ F =
S △ F = I ∩ M, so the key (κ(A), κ(B), I ∩ M) is inserted.

*Step 6.* Multiply: (1/(m+1))·(½)·E_S[B_S/(8K₀n²C(σ,k1)C(σ,k2))] ≥ 2^{−d(M)}/(16K₀n²(m+1)C_S) ≥ 2^{−d(M)}/(C_S n^6). ∎

**Corollary T6 (coverage; Base Corollary A6, l.537-545).** Under the same assumptions, except with probability o(1)
every alias class of every target is in its dictionary: T = C_S n⁸⌈2^{d(M)}⌉ ≥ C_S n⁸ 2^{d(M)} trials miss a fixed class with
probability ≤ (1 − 2^{−d(M)}/(C_S n^6))^T ≤ e^{−n²} ≤ e^{−n}, and there are ≤ (nN₀+1)2^n pairs. (The constant C_S cancels:
the trial count carries it.) ∎

**Lemma T7 (expected work; Base Lemma A7, l.547-591).** Assume (LD) and ℰ₃; condition on M, L; average over P and
the trials. The uncapped procedure takes at most (b+2)2^{(τ0 − ε0 + ζ)n + O(n^{0.6})} steps.

*Proof.* T ≤ 2C_S(m)n⁸2^{d(M)} ≤ 2n^{8+c_S}2^{d(M)}; polynomial factors (including C_S(m)) go into 2^{O(n^{0.6})}.
1. *Value maps and Step 3:* 2^{|L|} + 2^{|R|} + 2^{m − d(M)}poly: exponents l, r, μ < τ0 − ε0 by (C6) and (MU1).
2. *Masks:* per trial ≤ 2^{H3(a,c)m} + 2^{h(½−a+c)m + 1}; times T ≤ 2^{d(M)+O(log n)} ≤ 2^{(½−τ0+ζ)n + O(n^{0.6})}
   (T3(ii)): exponent max(H3, h(½−a+c))μ + ½ − τ0 + ζ < τ0 − ε0 + ζ by (C5R).
3. *Small primes:* n³2^{γm/2+1} per trial: (½ − τ0 + ζ + γμ/2)n, far below.
4. *Sorting keys:* (n+1)(2^{|L|−d(L)} + 2^{|R|})T ≤ 2^{ln + O(n^{0.6})} + 2^{(r + ½ − τ0 + ζ)n + O(n^{0.6})} (T3).
5. *Left records:* (n+1)2^{|L|−d(L)}·2^{H3(a,c)m}·2^{1−γm} per trial; T ≤ 2^{d(L) + 2n^{0.6}} (T3(i)); total
   2^{(l + (H3(a,c) − γ)μ)n + O(n^{0.6})}. Use (C2R).
6. *Right class records:* (n+1)2^{|R|}(2m+1)2^{m−d(M)}2^{1−γm} per trial; T = 2^{d(M)+O(log n)} cancels d(M)
   exactly: 2^{(r + (1−γ)μ)n + O(n^{0.6})}. Use (C3). Listing the classes themselves costs 2^{m + O(log n)}; use μ < τ0 − ε0.
7. *Visits and expansions:* for a tuple (κ_L, X⁺, X⁻, κ_R, Y) put D = x_L + c^F(X⁺) − c^F(X⁻) + x_R + c^F(Y) − t^F,
   independent of P; a visit needs D ≠ 0, P | D (probability poly(n)(b + log n)2^{−ηn} by (F4)) and the small-prime
   conditions (one residue j′). Per trial ≤ poly(n)(b + log n)2^{|L|−d(L)+|R|−d(R)}·2^{H3(a,c)m}·2^{h(½−a+c)m}·2^{−ηn−γm};
   with d(R) ≥ 0 and T ≤ 2^{d(L)+2n^{0.6}}: (b + log n)2^{(1 − μ + (H3(a,c) + h(½−a+c) − γ)μ − η)n + O(n^{0.6})}. Use (C4R).
8. *Matching, dictionaries, output:* polynomial per record, tuple and key. ∎

**Theorem A′.** Under [S] with polynomial constant C_S(m), the procedure of T.2 has the properties of Base's Theorem A (l.319-330)
with the constants of T.1: on (LD) it returns, with probability 1 − o(1), Â_s within 1/16 of Σ_{I∈𝒜_s(P)} χ(I) for
every s; on every execution it uses at most 2^{τ0 n + 2n^{0.7}} poly(n+b+2) word operations.

*Proof.* As Base Section 5.8 (l.593-614): ℰ₃ fails with probability o(1) (T3); Lemma T4's event fails with
probability o(1); coverage fails with probability o(1) (T6); the cap is reached with probability
o(1) + (b+2)2^{(τ0−ε0+ζ)n+O(n^{0.6})}/2^{τ0 n + n^{0.7}} = o(1) because b + 2 ≤ 2^{n/10⁸+1} and 10^{−8} + ζ < ε0;
bounded samplers fail with probability 2^{O(n)}(2^{−n³} + e^{−c₀n²}). Soundness is Lemma T1; the output precision is
as in Base. ∎

With Theorem A′ in place of Theorem A, Base's Theorem 1 (l.765-812) gives running time
2^{(τ0 + 20ε)n + 2n^{0.7}}poly(n + b + 2), i.e. O(2^{T′n}) for every T′ > T := τ0 + 20ε.

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

All 33 conditions pass in arb at 200 bits (`scripts/round2/out/ternary_certificate_N4096_8192.txt`). Tightest:
C1R 9.99·10⁻⁷ (= ε0), B3 8.1·10⁻⁷, C2R/C3/C4R 1.30·10⁻⁶, C5R 1.60·10⁻⁶, M1 3.04·10⁻⁶, M2 3.30·10⁻⁶.
log₂ M1 = 0.51599187405865778648, log₂ M2 = 0.51599162047014794189, ball radii below 4·10⁻⁵⁵, identical at
N = 1024, 4096, 8192. The point is 2.3465·10⁻⁴ below the certified Section 8 point (T = 0.4875754036) and
3.352·10⁻⁴ below JoshuaQFEX.

**Statement.** *Conditional on [S] and on Base's written proof*, Subset Sum has a randomized algorithm running in time
O(2^{T′n}) for every T′ > 0.4873407528, in particular O(2^{0.4873408n}). (Not 0.48734: that is below T.)

Cutoff: as for the Section 8 point, ζ = 10⁻⁸ makes Base's Proposition P need n > 10⁸ and its Chebyshev term small only
for n of order 10¹⁷; Corollary T6 has no further cutoff (the polynomial C_S(m) is absorbed into the trial count and into
2^{O(n^{0.6})}). Exact layer-density monotonicity is false (ROUND2_REPORT A.3, m = 8), so [S] is taken from Conjecture M′
(a_t ≤ P(m)·a_k for t ∈ [k, m−k], k ≤ 0.11m) through Lemma S, which gives C_S(m) = P(m) + 2.
