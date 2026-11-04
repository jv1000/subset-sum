# C13: a family of asymmetric filters in Base's format (pre-registration)
**Written 2026-11-03 ~17:55 ET, before any C13 run.** Jennifer: "Yes please" (to running a small family of
asymmetric filters in Base's multi-filter format).

## What Base's family format allows (read from PROOF_0.4877.tex §6, l.616–760)
- A pattern π records block averages for every filter v and picks v* = argmax_v U_{v,π}.
- For each (filter v, region ρ), a certificate z ≥ 0 multiplies these rows:
  - ρ0: (Δ − u_v, Γ − w_v, (u_v − u_l)_{l∈C});
  - ρ_i: (a_Γ w_v − u_v, band rows, (u_v − u_l)_{l∈C}).
- Conditions: z0 ≥ 1 (ρ0) and z0 b_{i−1} ≥ 1 (ρ_i). The integral is ∫(2+2cos x) 2^{z·G(x)} < 2^{ρ_c}.
- **Why this can help:** the comparison rows u_v − u_l are ≥ 0 on every pattern that chooses v. So v's certificate can
  ignore frequency types on which another filter has the larger U. Those types are then handled by filter l, and are
  direct-summed when U_l ≥ Δ.
- In the large-deviation picture, the critical type of filter v (its tilt, E_t u_v = Δ) stops binding if some other filter
  has E_t u_l > Δ there.
- C12 used J = 1, where the comparison rows are empty. C6 showed that band and region refinements alone gain nothing for
  J = 1, so any gain must come from the comparison rows.

## Model (floating)
- **Variables:**
  - Base's alias parameters (t, η, μ, a, γ, l);
  - J filters, each with 16 cosine + 16 sine coefficients per density (box 4) and its own κ_v ∈ [.5, 2];
  - per filter, two certificates:
    - "low": z = (p_v, z1_v ≥ 0 on Γ − w_v, y_{v,l} ≥ 0);
    - "high": z = (q_v, z1'_v ≥ 0 on w_v − Γ, y'_{v,l} ≥ 0), used for all of ρ1..ρ9.
- **Validity of the high certificate for every ρ_i:**
  - q_v ≥ 1 ≥ 1/b_{i−1};
  - w_v − Γ ≥ w_v − Γb_{i−1}, so the row we use dominates Base's band row for each i (the band row Γb_i − w_v gets weight 0);
  - the integral with Base's row is therefore no larger.
- **Constraints:**
  - C1–C8 with slack 1e-6;
  - all 2J moments ≤ η − 3e-6;
  - Σz ≤ 20 per certificate. This replaces OpenAI's 3p ≤ 30 rounding cap, since in Base the rounding cost is
    (18 + 6Σz)ε. With ε = 1e-8 and η − ρ_f = 1.5e-6, B3 needs Σz < 22.
- **Grid:** N = 512 grid; the best point is rechecked at N = 1024.

## Runs
- **Control:** J = 1 must reproduce C12's τ0 = .4875749 (within 2e-7). Note that the cap changes from 3p ≤ 30 to Σz ≤ 20,
  and p ≈ 8.46 satisfies both.
- **J = 2 and J = 3**, four starts each. Extra filters start from our filter:
  - shifted by c ∈ {±0.3, ±0.6} (r(x+c), s(x+c));
  - reflected (x → −x);
  - plus noise .05.
- Comparison weights start at 0, so each start begins as J independent single-filter certificates.

## Prediction (before running)
- J = 2 gain in τ0 versus J = 1: P(> 2e-5) = .5; P(> 1e-4) = .2.
- Reason for caution: Base's 43 filters at 8 cosines reached a capacity close to what one of our 16+16 filters gives
  alone. So families may add less than more harmonics did.
- If there is a gain, then freeze, certify in arb (all 2J certificates, with Base's full region rows written out), and
  referee as in C12.

## Amendment 1 (~18:10 ET), before changing the starts
- **Control (J = 1):** τ0 .4875749, +3.6e-9 vs C12. PASS.
- **J = 2, v1 starts (comparison weights y = 0; filter 2 = shifted or reflected copy + noise):** 3 of 3 finished starts
  returned exactly the J = 1 value. Filter 1's comparison weights stayed at 0. The J = 3 run was stopped.
  Log kept: s13_J2_v1_zero_y_starts.log.
- **Diagnosis (degenerate start, not evidence):**
  - At y = 0, filter 1's binding certificate does not depend on filter 2's coefficients, so the gradient gives filter 2
    no reason to move.
  - d log M / d y = E_t[u_1 − u_2] at the tilt t. This is > 0 when filter 2 is worse on filter 1's critical type, so
    y stays at its bound.
- **Diagnostic (base_single.py):** each of Base's 43 filters alone, at Base's (τ0, η):
  - best single filter (#32) margin −0.00039, next #28 −0.00075;
  - the family's certified margin is +0.00025.
  - So Base's family is worth about +0.0006 bits of moment margin over its best member. That is the scale to expect.
- **Changed starts (v2):**
  1. y initialized to 0.5 in all certificates;
  2. filter 2 also started from Base's filters #32 and #28 (8 cosine terms, sine and harmonics 9–16 zero) as well as
     from shifted copies of ours;
  3. a phase-0 step that holds the alias parameters at C12's point and maximizes the minimum moment margin over the
     filters and weights, then runs the full τ0 minimization from there.
- **Prediction unchanged.**

## C13 result (~18:35 ET): small gain, below the pre-registered thresholds. Not worth certifying.
- **v2 full runs (s13b.py; logs s13b_J1/J2/J3.log; s13v2_J*_N512.json):**
  - J = 1 control: .4875749.
  - J = 2 best .4875717 (−3.25e-6), from the reflection start. The optimizer's filter 2 is the MIRROR of filter 1
    (x → −x) to within 1.6e-3 in every coefficient, with comparison weights 4.22 (low) and 3.68 (high).
  - J = 3 best .4875717 (same pair; the third filter unused).
  - Other starts (Base #32, Base #28, shifted copies) stayed at the J = 1 value.
- **Phase-0 margin at C12's alias point** (max-min moment margin in bits; J = 1 value 3.0e-6):
  - J = 2: 12 random diverse second filters (s13c.py) give 5/12 → 6.684e-5 (the mirror pair), 1/12 → 9.3e-6 and
    6/12 → 3.0e-6.
  - J = 3: mirror pair + a random third filter (s13d.py, 6 starts) gives at best 7.144e-5, i.e. +4.6e-6 over the pair.
- **Conversion to τ0:** about 0.05 τ0 per bit of margin. So J = 2 gives −3.3e-6 and J = 3 about −3.5e-6.
- **Prediction check:** "P(gain > 2e-5) = .5; P(> 1e-4) = .2". Outcome 3.3e-6, below both thresholds.
- **Interpretation:**
  - Base's cosine-only family gains about 6.4e-4 bits over its best member, from the diversity of different filters.
  - Our single asymmetric filter already beats that family. A family on top of it adds only ~7e-5 bits, almost all
    from pairing the filter with its mirror image, which covers the mirror of its own critical type.
  - Asymmetry and family diversity buy largely the same thing.
- **Decision:** do not freeze or certify a 3e-6 improvement now. Logged as a known small option (mirror pair:
  T ≈ .4875722). The filter side of Base's checksum is close to exhausted at this budget. Remaining levers are
  structural: the alias/list side (C1–C5 are all active) or a new variance argument.
