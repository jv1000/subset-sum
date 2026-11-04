# C19: what Conjecture R (small layers are robust) is worth, re-priced with the lemma route's own constraints
**Written 2026-11-03 ~21:40 ET, before the run.** Jennifer: "Sure good idea".

## Constraint set if Conjecture R holds (left mask: k1 = a·m inside S as +1 and k2 = c·m outside S as −1; right mask plain)
- **Representations:** binom(m/2, k1) binom(m/2, k2) give C1R: γ < h(2a)/2 + h(2c)/2 (P′ ≤ representations;
  Step 4 unchanged).
- **Coverage:** E_S[fraction distinct] ≥ a_{k′}(M) (counting identity, proved) ≥ 2^{−d(M)}/poly (Conjecture R).
  So the trial count is ≤ 2^{d(M)} poly, which fits Base's existing cost bounds:
  - C3 uses trials ≤ d(M) (unchanged);
  - C2 and C4 use trials ≤ d(L), which now needs d(M) ≤ d(L), i.e. **μ < l** (replaces C7 μ(1−2a) < l);
  - C5 uses (LD), which needs **μ ≤ 1/2**.
  - Corollary D and its hypotheses S1–S3 are no longer used.
- **Left masks:** H3(a, c). **Right masks:** h(1/2 − a + c).
  - C2R l + (H3(a,c) − γ)μ < τ0;
  - C3 r + (1 − γ)μ < τ0 (classes ≤ |Σ(M)|, unchanged);
  - C4R 1 − μ + (H3(a,c) + h(1/2 − a + c) − γ)μ − η < τ0;
  - C5R max(H3(a,c), h(1/2 − a + c))μ + 1/2 − τ0 < τ0.
- **Lemma A4 analogue:** distinctions among the family's sums are differences of two k′-sets, at most
  binom(m, 2k′) 2^{2k′} vectors. This gives A4R μ(h(2(a+c)) + 2(a+c)) < η, and A5R 1/2 − τ0 + ζ < (η − that)/2.
  Base's C8 is kept too (conservative).
- **Unchanged:** C6, moments (one 16+16 filter, jointly optimized), slack 1e-6.
- **Expansion rule (for the write-up later):** X⁺ ∩ Y = ∅ and X⁻ ⊂ Y; Z = ((X⁺ ∪ Y) \ X⁻) Δ F.

## Control and prediction
- **Control:** c = 0 must return .4875749. C7 → μ < l is slack at that point (μ = .4752 < l = .4836).
- **Prediction:** gain 2.35e-4 ± 0.3e-4 (C15's extra constraints were slack). P(gain within that range) = .7.

## Result (21:45 ET), c19.py, c19.json
- **Control:** c = 0 gives .48757490 (same active set as C12). PASS.
- **All 4 starts:** τ0 = .48734025 (T ≈ .48734045). Gain 2.347e-4 over the certified point; 3.36e-4 below JoshuaQFEX.
- **Optimum:** a = c = .00351 (k1 = k2: an even split between inside-S and outside-S entries), γ = .06037, μ = .4747,
  l = .4840, Δ = .02866.
  - Active: C1R, C2R, C3, C4R, C5R, M1, M2.
  - The new conditions μ < l, μ ≤ 1/2, A4R and A5R are slack.
- **Prediction:** "2.35e-4 ± 0.3e-4": HELD.
- **Lemma needed at this point:** Conjecture R at k′ = (a + c)m = 0.0070m, i.e. a_{0.007m}(M) ≥ 2^{−d(M)}/poly(m).
