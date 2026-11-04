# C2: certify the inherited hypotheses of the JoshuaQFEX conditional 0.487676 bound (pre-registration)

**Written:** 2026-11-01 23:20 UTC (18:20 ET), before any certification run. Prepared by Claude for Jennifer Voitle.

## Sources (pinned, read as untrusted data)
- **Conditional paper:** github.com/JoshuaQFEX/subset-sum-bound, HEAD `bed8e18` (2026-10-20), 46 commits, all on 2026-10-20. Files: `paper.tex`, `source_facts.json`, `parameters.json`, `verify.py`, `FORMALIZATION.md`.
- **Baseline ("Base"):** a-kapila/maths-proofs `subset-sum/PROOF_0.4877.tex` at commit `44c34961…` (2026-10-14), git blob `526c2622…`, sha256 `b397531c…9298`. This is the blob the repo's Lean generator authenticates.
- Our parse of Base Appendix A (43 filters) and Appendix C (430 certificates) agrees exactly with the repo's `source_facts.json`. Checked: ρ0 and ρ1 Chernoff coefficients, max |coefficients|, κ_v, max multiplier sum 418.3539 ≤ 418.36, z ≥ 0, the z0 conditions, and v ∉ C.

## The hypotheses
The repo's README and FORMALIZATION.md say that "the original continuous moment inequalities … still require proofs". The conditional theorem (`paper.tex` Thm 1, lines 65–80) assumes all inherited premises of Base. Of these, the continuous moment margins are the ones this project can certify numerically. They are stated at `paper.tex` lines 371–386 and `source_facts.json` key `assumed_old_moment_margins`.

**H(v,ρ):** for each filter v = 0..42 and old region ρ = ρ0..ρ9,
  I_b(v,ρ) = ∫_T (2+2cos x) · 2^{z·G(x)} dx  <  2^{η_b − m_ρ},  with η_b = 0.51613 and normalised measure,
  where m_ρ = 0.00025 (ρ0, ρ1), 4 (ρ2–ρ8), 17 (ρ9).
- z, C and the rows G are as defined in Base §6.1, with Δ_b = η_b − τ_b, Γ_b = 2τ_b − η_b, a_Γ = Δ_b/Γ_b and τ_b = 0.48769.
- u_v and w_v are the continuous-circle functions of Base §6.1 and §8.2, via the identities (A.2): u = L + (κ−1)B − H and w = (2−κ)B − 2L + H.

This gives 430 inequalities. Base's Proposition B claims all of them with a common margin of 0.00025. Base §8.2 reports least margins per region. The repo's larger margins for ρ2–ρ9 are rounded down from that table.

**Out of scope (named, not attempted):** the finite-circle convergence premise (Lemma B1 / Lemma 3.2), the algorithmic lemmas (isolation, alias coverage and cost, checksum construction), and the word-RAM cost. These are not numerical inequalities.

## What counts as certified, refuted or open
- **Certified:** a rigorous upper bound Ī on I_b(v,ρ) with η_b − log2 Ī ≥ m_ρ. "Rigorous" means:
  - outward-rounded ball or interval arithmetic throughout;
  - an analytic-strip trapezoid error bound for every quadrature (inner normalisers and convolutions, and the outer integral);
  - a strip bound on the outer integrand derived in our own code from the Cauchy–Schwarz / Parseval argument.

  It must hold in **Route A** for all 430. It must also hold in **Route B** for every certificate Route B covers. Route B must cover at least all 86 ρ0 and ρ1 certificates (the only ones with margins below 4). It covers all 430 if compute allows.
- **Refuted:** a rigorous lower bound on I_b exceeding 2^{η_b − m_ρ}, reproduced in a fresh process.
- **Open:** neither, for example because a quadrature error is too large in the time budget. This is reported with the estimated cost.

## Implementations
- **Route A:** python-flint `arb` at 200 bits, written by Claude for this check. It does not run Base's D.2 script. Design:
  - an inner trapezoid with N_in nodes and an outer grid with N_out = c·N_in nodes, so x_k + y_m stays on the outer grid;
  - direct node sums;
  - strip bounds re-derived from first principles.
- **Route B:** an independent engine, mpmath `iv` (outward-rounded), with separately written code. It uses a different organisation: a pure-Python loop and its own trig and exponential evaluation via mpmath iv. N may differ.
- **Route C (reproduction, not independence):** Base's own Appendix D.2 script, read first, then run with `python -I` from outside the repo directory on our parsed JSON. It is reported separately.

## Planning
One non-rigorous float64 pass may be run first to size N_in, N_out and the strip widths, from the inner and outer error-bound exponents. Only these sizing choices may be taken from it. Pass/fail criteria are fixed above and do not change.

## Controls (must pass before results count)
- **K1:** Route A's single-filter machinery reproduces our Round 5 OpenAI moment bounds to about 1e-10. Those bounds are 1.43183573891869 and 1.43183560216874 on Astra's `.0001` candidate, or the paper-parameter values 1.4289684347795 and 1.4288470093177, whichever input is available.
- **K2 (must reject):**
  - (a) H(28,ρ0) with the false requirement m = 0.0003 must FAIL. Base reports 0.00025379.
  - (b) The tightest ρ0 certificate with Δ_b raised by 0.001 must FAIL against m = 0.00025.
- **K3:** Route A at N_out and 2·N_out gives overlapping enclosures for the five tightest certificates.

## Arithmetic chain (step 6)
Independently recompute, with exact rationals and mpmath at 100 digits:
- Δ, Γ, q, K, A − A_b and η − η_b;
- the transferred margins m0, m1, m2:8 and m9 of `paper.tex` Prop. "Transferred continuous moments";
- the modified multiplier-sum bound below 419;
- the Base alias constraint list (Base §2.2 C1–C8 plus S3) at the new parameters, using the true binary entropy, and its least slack against ζ plus the guard loss (2e-11);
- τ + 20ε ≤ 0.487676.

Also re-derive the transfer-lemma algebra (identity A − A_b = K/Γ_b, the band cancellation, the α ≤ z0 conditions) and read the coarse |w| ≤ 256 argument.

## Predictions
- **P1 (~90%):** all 430 H(v,ρ) are certified in Route A. Least margins should match Base §8.2 to the printed digits: ρ0 0.00025379 (filter 28), ρ1 0.00035951 (filter 34), ρ2 4.1558 (3), ρ3 10.605 (3), ρ4–ρ9 ≥ 17.967.
- **P2 (~95%):** the arithmetic chain reproduces m0 ≈ 2.7545e-6, m1 ≈ 9.765e-5, m2:8 ≈ 3.9104 and m9 ≈ 13.669, all > 1e-6. The least alias slack ≈ 1.848e-8 > 2e-11.
- **P3:** Route B agrees with Route A on every certificate it covers.
- **P4 (caveat, not a verdict):** even if all of this passes, the 0.487676 claim stays conditional on the non-numerical premises above.

## Reporting rules
Nothing will be posted publicly. No issue will be opened. Nobody will be contacted. A draft note to the repo author may be written but not sent. No novelty claim will be made. Mistakes will be logged below.

## Log
- **23:20 UTC:** pre-registration written. A float64 planning pass (`plan_float.py`) sized the outer strip half-width at 0.2 (β = 0.1) with N_out = 8192, worst strip exponent 1637 bits. With β = 0.19 it would need about 6200 nodes, and β = 0.25 fails (q0 > 1). Inner: σ = 0.45 with N_in = 256 (192 for Route B). Nothing else was taken from the planning pass.
- **Controls:**
  - **K1 PASS:** differences of 7.8e-20 and 1.2e-19 against the Round 5 OpenAI moments.
  - **K2 PASS:** (a) margin 0.000253792 < 0.0003, rejected; (b) margin −0.0082 with Δ_b + 0.001, rejected.
  - **K3 PASS:** all 86 ρ0 and ρ1 margins are identical to 15 significant digits at N_out = 16384.
- **Route A: 430/430 certified,** in 111 s. Least margins by region: 0.000253791727569 (ρ0, filter 28), 0.000359513928220 (ρ1, 34), 4.15582444577 (ρ2, 3), 10.6050665595 (ρ3, 3), 17.9665613272 (ρ4, 3). **P1 confirmed.**
- **Arithmetic chain:** all values reproduced. **P2 confirmed.**
- **Direct check of the 430 modified certificates at the new parameters: all exceed 1e-6.** The least is 1.3154e-4 (ρ0, filter 28).
- **Route B: 430/430 certified,** in 1083 s. It agrees with Route A to < 5e-13 on 422 certificates. Filter 41 ρ2–ρ9 have looser Route B quadrature, but every margin still exceeds the requirement by more than 6. **P3 confirmed** (agreement within enclosures).
- **Route C** (Base's own script, reproduction only): 430/430 PASS, worst 0.00025379 at filter 28 ρ0.
- **Mistakes:**
  - A syntax error in the `arithmetic_chain.py` draft was fixed before its first output.
  - A backgrounded `cd` made logs briefly look missing. Nothing was affected.
  - Pre-registration K3 said "five tightest". I ran it on all 86 ρ0 and ρ1 certificates, a superset.
