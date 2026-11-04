# Claude's review of Fable's Section T and the round-2 summary (2026-11-04, ~07:10 ET)

## A. Exact monotonicity: FALSE (verified independently)
- w = (−6, −5, −5, −3, −3, −2, 4, 5), m = 8: |Σ_3| = 19, |Σ_4| = 24, so a_3 = .3393 < a_4 = .3429 (a 1% violation,
  at the middle step).
- In this instance every a_k/2^{−d} is ≥ 2.71 (d = 3).
- **Lesson logged:** our adversarial searches at m = 16–20 missed what Fable's exhaustive sweep at m = 8 found.
  Prefer exhaustive small cases.
- **The needed approximate target M′ is untouched:** a_t ≤ poly·a_k on [k, m−k], k ≤ 0.11m. Fable's sweep (m = 9–12,
  about 11M multisets): max_{t ≥ k} a_t is attained at t = k for all k ≤ m/4.

## B. Section T: SOUND, with one required correction
Each step was re-derived:
- T1 soundness: X⁻ ⊆ Y and X⁺ ∩ Y = ∅ make the sum additive over (X⁺ ∪ Y) \ X⁻. ✓
- T5 step 3: −b^F(X⁻) = +b^I(X⁻) off S, so the keys are b(A) + b^I(U), U ∈ F(S). ✓
- T5 step 5: b^F(Y) = b^I(S \ X⁺) − b^I(X⁻); the total is b(A) + b^I(S) + b(B) = T^F; Z = S Δ F = I ∩ M. ✓
- T4: count Σ_{j≤2k′} C(m,j)2^j ≤ 2^{(h(2a′)+2a′)m} for 2a′ ≤ 1/2; global, so there is no bad-S term. ✓
- T3: |L| > m and f nondecreasing give d(L) ≥ d(M) − 2n^.6; m ≤ n/2 and (LD) give d(M) ≤ (1/2 − τ0 + ζ)n + n^.6. ✓
- T7 items 1–8: the exact |Σ(M)| costs 2^{m−d(M)} ≤ 2^{μn} < 2^{τ0 n}; for right classes T·2^{m−d(M)} cancels exactly;
  the visit count is as in Base with H3 and h(1/2 − a + c). ✓
- Slacks recomputed independently at the frozen decimals (floating): C1R 9.99e-7, C2R/C3/C4R 1.30e-6, C5R 1.60e-6,
  MU1 9.3e-3, A4R .459, prime .229. All match Fable's arb certificate.
- **REQUIRED FIX:** Corollary T6 uses C_S = 3 (from exact monotonicity, now false). Under M′, C_S = poly(m).
  Set T = C_S·n⁸·⌈2^{d(M)}⌉ (with a fixed polynomial), otherwise (1 − 2^{−d}/(C_S n^6))^T is not ≤ e^{−n}. The
  exponent is unchanged.

## Status
- **CONDITIONAL theorem** (on [S], Base's written proof, the OpenAI paper): T = 0.4873407528, O(2^{0.4873408n}).
- Recorded in the paper (rev 73): Section 8 paragraph and status-table row, labelled conditional.
- **Before any claim:** [S] must be proved, and a FRESH referee (Astra tonight or a new Fable session, not this Fable)
  must check candidate_ternary.json and Section T.
- **Still to receive from the laptop:** ROUND2_REPORT.md, candidate_ternary.json, the certificate output and
  scripts/round2 (Fable's folder is not reachable from this session).
