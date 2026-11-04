# C15: BCJ-style ternary masks in Base's alias step, priced in floating arithmetic (pre-registration)
**Written 2026-11-03 ~18:30 ET, before any C15 run.** Jennifer: "Yes please let's try".
C14 showed the list side's levers are C4 (matching visits, price .389) and C1 (P′ vs representations, .258).

## Base's mechanism (read from §3, §5.2–5.7)
- An alias I gives S = (I∩M) Δ F with |S| = σ = m/2.
- A left mask X ⊂ M (|X| = k = am) and a right mask Y (|Y| = σ − k) represent it when X ⊔ Y = S. There are
  binom(σ, k) representations.
- P′ = 2^{γm} keeps 1/P′ of them; coverage needs P′ ≤ binom(σ, k) (S4, giving C1: γ < h(2a)/2).
- On S the signed weights equal a fixed signing c^I (Lemma A5, step 2). Corollary D bounds the average fraction of
  distinct k-subset sums of S below by 2^{−g_M}/(v+1) with v = m − 2k. The trial count 2^{F̂} ≥ 2^{g_M} compensates,
  and F̂ ≤ d(L) or d(M) is paid by the key counts (C2, C3, C4).
- **Sign fact (derived here, checked by hand):** on M \ S the trial's signed weights are c^F = −c^I. So a mask element
  outside S carries the opposite of the alias's own signing.

## Ternary variant T (BCJ-style)
- Representations x = X + Y as coefficient vectors on M, with X, Y ∈ {−1, 0, +1}^M:
  - on S: as in Base (k of S in X, σ − k in Y);
  - on M \ S: e pairs (X = +1, Y = −1) and e′ pairs (X = −1, Y = +1).
- Fractions: b = e/m, c = e′/m.
- **Representations:** binom(σ, k) · multinom(m/2; e, e′, rest), i.e. the exponent per m is h(2a)/2 + H3(2b, 2c)/2,
  where H3 is the 3-way entropy.
- **Left masks:** k + e plus-ones and e′ minus-ones, giving H3(a + b, c). **Right masks:** σ − k + e′ plus-ones and
  e minus-ones, giving H3(1/2 − a + c, b).
- **Constraints of the model** (b = c = 0 gives back Base's C1–C8 exactly):
  - C1′ γ < h(2a)/2 + H3(2b, 2c)/2.
  - C2′ l + (H3(a + b, c) − γ)μ < τ0.
  - C3′ r + (1 + h(b) − γ)μ < τ0. Right classes are values c(Y+ΔF) − c(Y−ΔF), at most |Σ(M)| · binom(m, bm).
  - C4′ 1 − μ + (H3(a + b, c) + H3(1/2 − a + c, b) − γ)μ − η < τ0.
  - C5′ max(H3(a + b, c), H3(1/2 − a + c, b)) μ + 1/2 − τ0 < τ0.
  - C6 unchanged.
  - C7′ μ(1 − 2(a + b + c)) < l. Conjectural: the Corollary D analogue's v is taken as m − 2|X|.
  - S3′ h(2a)/2 + H3(2b, 2c)/2 + h(a + b + c) < 1 − 2(a + b + c). Conjectural analogue.
  - C8′ (μ/2) log2 3 + μ(h(4(b + c))/2 + 2(b + c) log2 5) < η, and A5′ 1/2 − τ0 + ζ < δ′ = (η − LHS)/2.
    This is the Lemma A4 analogue: the differences of two ternary patterns on M \ S have at most 2(b + c)m nonzeros
    in {−2..2}.
  - The moments are as in C12 (one 16+16 filter, jointly optimized).
- **What would need a new proof (explicitly not claimed):**
  - a Corollary D analogue for the two-part layer (X ∩ S of size k, X \ S a signed pattern), i.e. a lower bound on
    the average fraction of distinct values of c^I(X1) − c^I(O+) + c^I(O−) by 2^{−g}/poly;
  - the coverage step 4 with the larger representation count;
  - the right-class bound.

  C15 only prices the idea, assuming these analogues hold with the same exponents.

## Runs
- **Control:** b = c = 0 fixed must reproduce .4875749.
- **T1:** c = 0, b free (one-sided pairs). **T2:** b and c free (full BCJ).
- 4 starts each (b, c ∈ {.0005, .002, .005}).

## Prediction (before running)
- Rough first-order count for small b: the representation gain h(2b)/2 ≈ b log2(1/2b) is offset by the extra mask entropy
  in C4′, which grows on BOTH sides (left by ~b log2((1−a)/a), right by ~b log2(1/b)).
- So T1 likely gives no gain; P(T1 gain > 1e-5) = .25.
- T2 adds representations through the second pair type. P(T2 gain > 1e-5) = .35; P(T2 gain > 1e-4) = .12.
- A NULL here would say the representation lever needs more than richer masks (e.g. a second level, the C4 lever),
  which would be C16.

## C15 result (~18:50 ET): NULL under Base's proof technique; a precise open lemma would be worth 2.35e-4
- **Control:** b = c = 0 gives .48757490. PASS.
- **T1** (pairs X = +1, Y = −1): b → 0 from all 4 starts. No gain. Prediction HELD.
- **T2** (both pair types): all 4 starts give τ0 = .4873404 (−2.35e-4 vs C12), with b = 0 and c = .00351 and the inside
  fraction a moving to .00351.
  - The optimum does not add representations. It splits Base's total γ ≈ .0604 evenly between inside S (k) and outside
    S (−1 entries of the left mask).
  - That lowers the left-mask entropy (.0674 vs h(.0082) = .0689) and makes the right mask exactly m/2.
  - Hand check (c15 recompute): C2 to C5 all = .487338 < τ0.
  - Prediction "P(T2 gain > 1e-4) = .12" was wrong-way surprised **in the model**. See below for why the model is invalid.
- **Sensitivity (c15_theta.py):** losing a fraction θ of the outside-S representations, paid in trials:
  - θ = .1 already gives NO gain (τ0 back to .4875749, c → 0).
  - Linear estimate: the gain vanishes at θ ≈ .02. The gain needs an essentially lossless lemma.
- **Why the model is invalid (found on analysis, before claiming anything):**
  - Base's Corollary D requires 2σ_T ≤ v + 2k′ with v ≤ |M|, where σ_T is the size of the set the representations
    live in and k′ is the mask size.
  - Its proof goes down from a good layer t ≤ v/2 to layer k′ through Lemma 3.1 covering, leaving a set of size
    v − t + k′ ≥ v/2 + k′.
  - Representations of the two-part family live in T = S ∪ O (O ⊂ M \ S). So |O| = σ_T − m/2 ≤ k′.
  - My C7′ took v′ = m − 2|X|, which is inconsistent with this. **Mistake logged.**
- **With |O| ≤ k′ (the honest model T3), ternary masks are dominated.**
  - Representations: binom(m/2, k1) · binom(k1 + k2, k2). Left masks: H3(a, c) = h(a + c) + (a + c) h(c/(a + c)).
  - Against Base's own masks of size a′ = a + c:
    - (left masks − representations) is h(a + c) − h(2a)/2 for T3 vs h(a + c) − h(2a + 2c)/2 for Base, so Base is better;
    - right masks: h(1/2 − a + c) ≥ h(1/2 − a − c), so Base is better;
    - C3 and C5: Base is better (larger γ, smaller right masks);
    - C7: T3 needs v = m (μ < l), Base needs v = m − 2k′.
  - So T3 is no better in every constraint. **No gain with the current lemma.**
- **Signs (useful later):** on M \ S the trial's signed weights are −c^I. A left mask's −1 on O′ ⊂ M \ S therefore
  contributes c^F(X) = c^I(X1) + c^I(O′) = c^I(X1 ∪ O′). The two-part family is a family of plain (k1 + k2)-subset sums
  of the fixed signing c^I, constrained to |U ∩ S| = k1. Within T, E_S[fraction of distinct values] ≥ a_{k′}(T) exactly
  (counting identity binom(v,σ) binom(σ,k1) binom(v−σ,k2) = binom(v,k′) binom(k′,k1) binom(v−k′,σ−k1)).
- **The open lemma that would be worth 2.35e-4 ("Corollary D beyond the half-block"):**
  > For a uniform σ-subset S of M (σ = m/2) and the family {U : |U ∩ S| = k1, |U \ S| = k2}, the average fraction of
  > distinct values of w(U) is at least 2^{−g}/poly(n), with g within the trial budget (≤ d(L), d(M) and
  > (1/2 − τ0 + ζ)n), losing at most ~2% of the outside representation exponent.

  Base's proof cannot give this. The barrier is the middle good layer t ≈ v/2 in Lemma 3.3. A sumset-type argument
  (Σ_{k1}(S) + Σ_{k2}(M \ S) is large unless both parts are structured, and structure means deficiency) is the natural
  attempt.
- **Next lever (C16 candidate):** the C4 lever (an extra filtering level). The C14 price is .389. It does not touch
  Corollary D.
