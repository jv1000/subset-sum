# C14: shadow prices of Base's list-side (alias) constraints at our C12 point (pre-registration)
**Written 2026-11-03 ~18:10 ET, before any C14 run.** Jennifer: "Yes let's go for it".

## Why
- At the C12 point, C1–C5 and both moments are active together; C13 showed the filter side is nearly exhausted.
- The price of each active constraint (exponent saved per bit of loosening) says which part of Base's alias procedure
  is worth redesigning.

## What each constraint counts (Base §2.2 and §5, l.165–172 and 557–584)
- **C1** γ < h(2a)/2: the small prime P′ (γ|M| bits) must not exceed the variety of left masks of S.
- **C2** l + (h(a) − γ)μ < τ0: left records, i.e. keys of L × left masks / P′.
- **C3** r + (1 − γ)μ < τ0: right class records, i.e. keys of R × mask classes / P′.
- **C4** 1 − μ + (h(a) + h(1/2 − a) − γ)μ − η < τ0: matching visits, i.e. pairs looked at per trial (alias count
  times splits / P′).
- **C5** h(1/2 − a)μ + 1/2 − τ0 < τ0: right masks per trial times the number of trials 2^{F̂} (F̂ ≤ 1/2 − τ0 + ζ by
  the preliminary search).
- **Moments:** log2 M1, M2 < η (the checksum).

## Method
- Model: the C12 joint model (s12.py: alias parameters + one 16+16 filter + p, q; N = 512).
- For each constraint i (C1, C2, C3, C4, C5, and the moment pair together), loosen its slack by δ ∈ {2e-4, 5e-4}.
  Re-minimize τ0 from the C12 optimum.
- **Price** π_i = −dτ0/dδ, by finite differences, checked for linearity across the two δ.
- **Control:** δ = 0 must return .4875749.
- **Consistency check:** the KKT condition implies Σ_i π_i · (∂g_i/∂τ0) = 1, where the τ0-coefficient of C2, C3, C4
  and the moments is 1 and that of C5 is 2. So the prices must split the unit of exponent among the constraints
  (within ~5%).
- **Also:** loosen ALL of C1–C5 by δ jointly, which gives the total list-side price.

## Predictions
- C4 (matching visits) and the moments carry the most weight.
- The list-side total (C1–C5 jointly) is between .4 and .8 per unit; the moments get the rest.
- C1 (P′ vs mask variety) has a positive price but is not the largest.

## C14 result (~18:20 ET), floating; c14.py, c14.json
- Control: δ = 0 gives .48757490. PASS. All runs are feasible, and prices are linear (δ = 2e-4 and 5e-4 agree to 1e-4).

| Constraint (what it counts) | Price: τ0 saved per bit loosened |
|---|---|
| C4 matching visits | **0.389** |
| C1 P′ size vs left-mask variety h(2a)/2 | **0.258** |
| C2 left records | 0.077 |
| C3 right classes | 0.077 (identical to C2: they trade through l vs r) |
| C5 right masks × trials | 0.001 (not binding in practice) |
| moments, per bit of log2 M | 0.051 (≈ 0.43 per unit of τ-coefficient, since ∂/∂τ0 is p ≈ 8.5) |
| ALL of C1–C5 jointly | 0.801 (= the sum of the individual prices, so additive) |

- **Mistake logged (pre-registered check):**
  - The KKT identity used τ0-coefficient 1 for the moment rows; it is p = 8.46 (M1) and 9.31 (M2), by autodiff.
  - The check as written gave 0.595. Corrected, it gives Σ π_i ∂g_i/∂τ0 = 0.544 (list side) + 0.431 to 0.474
    (moments; the split between M1 and M2 is not separated) = 0.975 to 1.018, which brackets 1. PASS after the fix.
- **Predictions:**
  - "C4 and the moments carry most weight": HELD. C4 is the largest single price; the moments carry about 0.45 of the
    unit through their τ0 coefficient.
  - "List-side total between .4 and .8 per unit": HELD, at the edge (0.80).
  - "C1 positive, not the largest": HELD (0.258, second).
- **Reading:**
  - Two constraints set the price: matching visits (C4) and the P′ ceiling (C1).
  - Saving 0.001 bits in both would buy 0.00065 of exponent, 6.5× what the whole C13 filter family bought.
  - **C1 comes from the representation count:** S = (I∩M) Δ F has |S| = σ = m/2. Its left masks X (|X| = k = am) take
    binom(σ, k) ≈ 2^{(m/2) h(2a)} values, and P′ cannot exceed that.
  - **C4 is the number of candidate pairs** that agree modulo P′·P but are not real aliases.
  - Both are the classic levers of the representation technique (Howgrave-Graham–Joux; Becker–Coron–Joux), which
    Base adapts to the worst case. The natural redesigns:
    - (a) richer masks (more representations per alias raise C1's ceiling, e.g. ternary {−1, 0, 1} masks as in BCJ);
    - (b) an extra filtering level (a second small prime) to cut C4's visits.
  - Each needs its own worst-case proof (Base's Corollary D and deficiency accounting). Price them in floating
    arithmetic first.
