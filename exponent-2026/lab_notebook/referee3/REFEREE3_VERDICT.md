# Referee 3 verdict on candidate_base.json (2026-11-03, ~22:40 UTC)
Independent agent. It read only candidate_base.json, Base's PROOF_0.4877.tex and the OpenAI paper's TeX.

**Verdict: the claim survives.**
- Every numerical premise holds at the JSON decimals.
- The adaptation has no fatal issue.
- Base's text needs constants updated, and the D.2 script must be rewritten to handle sine terms.

## Conditions derived, with Base line numbers
- **Alias:** C1–C8 (l.165–172); ε0 = least slack (l.176).
- **Sizes:** S1–S5 (l.185–191).
- **Lemma A5** (l.465, 506): 1/2 − τ0 + ζ < δ.
- **Lemma A7:**
  - item 1 (l.556): l, r, μ(1−2a) < τ0 − ε0;
  - items 1 and 6 (l.570): μ < τ0 − ε0;
  - **item 3 (l.562): 1/2 − τ0 + ζ + γμ/2 < τ0 − ε0 + ζ** — missing from Claude's list;
  - **item 4 (l.564): r + 1/2 − τ0 + ζ < τ0 − ε0 + ζ** — missing from Claude's list.
- **Theorem A cap** (l.177, 603): 1/guard + ζ < ε0.
- **Prime draw** (l.801): η/2 < τ0.
- **Theorem B:** Δ, Γ > 0.
  - Lemma B2: row error 6ε needs a_Γ ≤ 3/4; z0 ≥ 1; z0·b_{i−1} ≥ 1.
  - Lemma B3: (18 + c_z)ε < η − ρ_f.
  - Lemma B1: ρ_c < ρ_f.

## Evaluation (cond.py, arb at 256 bits)
- All conditions pass. ε0 = 1.315670e-6, with C4 tightest.
- δ = .0698258, against 1/2 − τ0 + ζ = .012425.
- B3 slack 8.12e-7.
- The candidate's "floating_margins" for C2–C5 are about 5e-11 optimistic, because they were computed at the unrounded τ0. This is harmless.

## Moments (correlation convention, full circle)
- float_M.py (FFT, N = 128–16384) and mp_M.py (50 digits, N = 96 and 160) agree.
- rig_M.py (arb with analytic-strip bounds; sine terms bounded by Σ√(a² + b²)cosh(jy)):
  - log2 M1 ∈ [0.5162683258512851504 ± 4e-26];
  - log2 M2 ∈ [0.5162681472646696864 ± 4e-26];
  - margins against ρ_c: 1.3154487e-6 and 1.4940353e-6.
- **Sanity checks:**
  - The convolution convention would give log2M ≈ 3.28, so the convention matters, and correlation is the correct one (filtering.tex l.12–13).
  - p and q are at a local optimum.

## Legitimacy
- **ζ = 1e-8 and guard 10^8:** these only raise the cutoff n_*. Prop. P still gives O(1/n). Free choices in Base.
- **J = 1 is an instance of Theorem B:**
  - v* = 0 trivially.
  - ρ0 uses z = (p, 0); ρ1–9 use z = (q, 0, 0), or (q, 0) for ρ9.
  - Band rows have weight 0, so one integral serves each family.
- **Sine terms:**
  - Lemma 3.2 (filtering.tex l.133–176) uses only uniform and derivative bounds. The constants 2.433 and 4.010 become 3.20.
  - The entropy order, the pattern grid, the joint moment (4.14) and uniform x_i(k) do not use evenness.

## Text changes needed in a write-up (none fatal)
- **Wrong as written at the new parameters:**
  - l.466 "δ > 0.0706" → .06983;
  - l.176 ε0 ≥ 5.37e-6 → 1.3157e-6.
- **Constants:**
  - l.646 and l.653 → 2^{ρ_c} and 2^{ρ_f};
  - l.720 and l.756 → 2^{−8.1e-7·n};
  - l.723: c_z → 6p ≈ 50.75;
  - l.733 → 6.9e-7 < 1.5e-6;
  - l.862: q0 → 0.562;
  - l.66 and l.808: exponent → T;
  - ζ and the guard at l.80, 149, 177, 193, 603, 770.
- **Rewrite for sine terms:**
  - the filter definition (l.620–627);
  - the cosine-only statements (l.1038–1040);
  - D.2's trig_nodes and abs_sum (cosine only). rig_M.py replaces D.2.
