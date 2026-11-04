# C2 result: the inherited moment hypotheses of the JoshuaQFEX conditional 0.487676 bound

**Date:** 2026-11-01. Prepared by Claude for Jennifer Voitle. Pre-registered in `PREREGISTRATION.md` before any certification run.

## Summary
- **All 430 continuous moment hypotheses are CERTIFIED.** These are the inequalities the repo assumes, with exactly its margins: 0.00025 for ρ0 and ρ1, 4 for ρ2–ρ8, and 17 for ρ9. Route A (python-flint arb) certifies all 430 with rigorous outward-rounded quadrature and strip bounds. Route B (mpmath iv, independently written, different N and strip) also certifies all 430; on 422 of them it agrees with Route A to <5e-13 in log2 margin (ρ0/ρ1: <4e-16). **None is refuted and none is open.**
- **The least margins reproduce Base §8.2 to every printed digit:**
  - ρ0: 0.000253791727569 (filter 28);
  - ρ1: 0.000359513928220 (filter 34);
  - ρ2: 4.15582444577 (filter 3);
  - ρ3: 10.6050665595;
  - ρ4: 17.9665613272.

  ρ5–ρ9 are larger still: 29.0, 45.5, 73.1, 128.2 and 256.8. The tightest case, ρ0, clears the assumed 0.00025 by only 3.79e-6 in log2. That is real but thin.
- **The repo's own conclusion, Proposition "Transferred continuous moments", is also certified directly.** I evaluated its 430 *modified* certificates at the new parameters (τ = 0.48767595, η = 0.51612858), without using the transfer algebra or the coarse |w| ≤ 256 bound. Every new margin exceeds the required 1e-6. The least are 1.3154e-4 (ρ0, filter 28), 2.142e-4 (ρ1, filter 34) and 4.1558 (ρ2). These agree to about 1e-10 with what the transfer identities predict from the old margins and the actual z0, which numerically confirms the transfer lemma's algebra. The paper's uniform worst-case bound m0 = 2.75e-6 is very conservative; the true least new margin is about 48× larger.
- **The arithmetic chain reproduces exactly:**
  - Δ = 0.02845263, Γ = 0.45922332, q = 0.99994190528, K = 1.4283043596e-5, A − A_b = 3.1100802605e-5;
  - the identity A − A_b = K/Γ_b holds exactly in rationals;
  - m0 = 2.7545366640e-6, m1 = 9.7649292937e-5, m2:8 = 3.91036676822, m9 = 13.6690976449;
  - the modified multiplier sum is ≤ 418.3730 < 419, and the remaining mean-square exponent is 9.7468e-7;
  - all 14 alias / side constraints are strict with the true entropy. The least slack is 1.84806927e-8 (C3), versus ζ + guard = 2e-11;
  - τ + 20ε = 0.4876759502 < 0.487676, a gap of 4.98e-8.

  So, **given its premises**, 0.487676 follows from the stated optimisation.

**What this means for the 0.487676 claim.** The numerical premises that the repo lists as unproved continuous inequalities are now rigorously certified twice, by code independent of both the repo and Base's script. The claim is still **conditional**. It inherits these premises from Base and the OpenAI preprint, unverified here:
- the finite-circle convergence (Base Lemma B1 / paper Lemma 3.2);
- the isolation and implementation lemmas;
- the checksum construction and estimator guarantees (Lemma 4.2 and the (4.x) chain);
- the alias coverage and cost arguments;
- the word-RAM operation count.

These are written proofs, not numerical inequalities. They were out of scope for this check.

## Hypotheses checked
`paper.tex` lines 371–386 and `source_facts.json` (`assumed_old_moment_margins`) state H(v,ρ):
  I_b(v,ρ) = ∫_T (2+2cos x) 2^{z·G(x)} dx < 2^{η_b − m_ρ}, η_b = 0.51613,
for each filter v = 0..42 and region ρ0..ρ9. The rows G and multipliers z are from Base §6.1 and Appendix C, and the 43 filters from Base Appendix A. We parsed the pinned Base TeX (blob `526c2622`, the one the repo's Lean generator authenticates). Our parse agrees exactly with every value the repo transcribed: z0 for ρ0 and ρ1, κ, max |coefficient|, Σz ≤ 418.36, and the z0 conditions.

## Method
Each Route computes the following.
- **Node values:** u_v(x_k) and w_v(x_k) from the convolution identities (Base §8.2 / OpenAI App. A), with inner trapezoid error bounds 2M/(e^{σN}−1) on the strip σ = 0.45. The integrands are entire.
- **Outer strip bounds:** U* ≥ |Re u| and W* ≥ |Re w| on |Im z| < 2β. These are derived in our own code from the contour split ±iy/2, Cauchy–Schwarz and Parseval monotonicity: q0 = sqrt((nf−1)(ng−1)) < 1, |Re L| ≤ −log2(1−q0), and the |B| bound.
- **The certificate:** the outer trapezoid of (2+2cos x)·2^{z·G}, plus 2M/(e^{2βN}−1), where M bounds the integrand on the strip.

| | Route A | Route B |
|---|---|---|
| Engine | python-flint arb, 200 bits | mpmath iv, 128 bits |
| Inner / outer nodes | 256 / 8192 | 192 / 6144 |
| Outer strip half-width 2β | 0.20 | 0.18 |
| \|B\| bound form | (sqrt(nf ng)(R_β+S_β) + (1+q0)\|LZ\|)/(1−q0) | sqrt(nf ng)(R_β+S_β+\|LZ\|)/(1−q0) |
| Max q0 / U* / W* | 0.393 / 1.65 / 18.1 | 0.379 / 1.60 / 17.3 |
| Max outer error | 1.8e-218 | 3.5e-6 (filter 41, ρ2; see note) |
| Max inner error (P, Y) | 1.3e-42, 3.3e-41 | — |

Base's own script uses N = 8192 nodes for both quadratures, 2β = 0.38 and arb_poly cyclic correlations. Our routes use a decoupled inner subgrid and direct node sums.

## Controls (all passed)
- **K1:** Route A's machinery reproduces Claude's Round 5 rigorous OpenAI-paper moments, 1.428968434779451822 and 1.428847009317706360. The differences are 7.8e-20 and 1.2e-19 (`K1.json`).
- **K2 (rejections):**
  - (a) H(28,ρ0) against a false requirement of 0.0003 is rejected; the margin's upper end is 0.000253792.
  - (b) The same certificate with Δ_b raised by 0.001 is rejected against 0.00025; its margin is −0.0082.
- **K3:** Route A at doubled N (512 / 16384) for all 86 ρ0 and ρ1 certificates. Every lower margin is identical to 15 significant digits.

## Observations
- **Route B outer error for filter 41.** Route B uses the narrower strip (0.18) and fewer nodes (6144). For filter 41's band certificates ρ2–ρ9, which have large multipliers, its outer quadrature error is not negligible: 3.5e-6 against I ≈ 0.063 at ρ2, and 2.3e-15 against I ≈ 2.5e-14 at ρ6. This lowers its *certified* margins by up to 0.14 in log2 (for example ρ6: 45.72 versus Route A's 45.85). Every one still exceeds the requirement of 4 by more than 6, and the Route B enclosures contain Route A's. This is looser quadrature, not a disagreement.
- **Six ρ0 certificates are literally the same integral.** These are filters 28, 32, 34, 37, 38 and 39, all at margin 0.000253791727569. Each uses z0 = 8.46 and z1 = 0, with comparison multipliers that form the same symmetric combination over the group {28, 32, 34, 37, 38, 39}. This is not an artefact.
- **ρ9 tail:** the paper's transfer uses |w| ≤ 256. Direct evaluation gives a ρ9 new margin of 256.8196 versus 256.8190 from the transfer, so the coarse bound costs essentially nothing.

## Route C (reproduction, not independence)
Base's own Appendix D.2 script, run unmodified on our parsed JSON with N = 8192, β = 0.19: **ALL 430 PASS**, worst log2 margin [0.00025379 ± 1.7e-9] at filter 28 ρ0, max q0 0.676. This reproduces Base §8.2. Route C is not independent evidence; it confirms that the published script and data do what Base says.

## Files
- `PREREGISTRATION.md`;
- `parse_baseline.py` and `baseline_data.json` (the parsed Base data, with sha256 of the TeX);
- `routeA_flint.py` and `routeA_8192.json`;
- `routeA_16384_tight.json` (K3);
- `routeB_mpmath_iv.py` and `routeB.json`;
- `direct_new_certs.py` and `direct_new.json`;
- `arithmetic_chain.py` and `arithmetic_chain.json`;
- `control_K1.py` and `K1.json`;
- `plan_float.py` (the non-rigorous sizing pass);
- `routeC_base_D2.log`.

To reproduce: `pip install python-flint==0.9.0 mpmath`, then run with `python3 -I`. Route A takes about 2 min, direct about 3 min, and Route B about 45 min, on 2 cores.

## Caveats and mistakes logged
- **Not a formal proof.** These are interval-arithmetic certificates with standard analytic-strip quadrature bounds. The quadrature lemma (Trefethen–Weideman 2014, Thm 3.2) and the strip derivation are written arguments.
- **Not fully independent of Base.** Both routes are Claude-written. Route A shares the arb engine, though not the code, with Base's script. Route B is a different engine. This is not outside review.
- **Scope:** the non-numerical inherited premises listed above are untouched.
- **Mistakes:**
  - A syntax error in the first draft of `arithmetic_chain.py` was fixed before its first output.
  - A shell `cd` inside a backgrounded command group briefly made logs look missing. No computation was affected.

## What to report, and to whom (draft only — NOT sent)
**To:** Joshua Wharton, as a GitHub issue on JoshuaQFEX/subset-sum-bound or by email. Optionally cc the Base author (a-kapila/maths-proofs), since this independently confirms Base Proposition B.

> Subject: Independent interval certification of the 430 inherited moment inequalities (and your transferred certificates)
>
> Hi Joshua, we independently re-certified the continuous moment inequalities your paper takes as premises (Base Prop. B with your per-region margins 0.00025/0.00025/4/17). We used two separately written interval-arithmetic implementations (python-flint arb; mpmath iv), with analytic-strip trapezoid bounds and our own strip estimates. All 430 hold. The least margins match Base §8.2 to the printed digits (0.00025379 at filter 28, ρ0). We also directly certified your 430 modified certificates at τ = 0.48767595, η = 0.51612858. The least new log2 margin is 1.315e-4 (ρ0, filter 28), well above your 1e-6 requirement, and agrees with your transfer identities to about 1e-10. Your scalar chain (m0…m9, alias slacks 1.848e-8, the 4.98e-8 exponent gap) reproduces exactly. This does not address the finite-circle convergence, the algorithmic lemmas or the word-RAM accounting, which remain conditional as you state. An independent check (separate implementation for the three tightest certificates, full same-code rerun, exact-rational scalar audit) agrees; exported bounds use directed rounding. Scripts and outputs are available on request. — Jennifer Voitle (with Claude)

Whether, when and how to send this is Jennifer's decision.

## CORRECTION (2026-11-02): exported bounds now directed; certification unchanged

**What Astra's outside check found (round 6, `C2_outside_check/`).** Route A wrote its "lower" and "upper" fields with
`.lower().str(k, radius=False)` / `.upper().str(k, radius=False)`. That renders a *rounded-to-nearest* decimal, which can
land on the wrong side of the true bound in the last digit. Example: the rho1 / filter 34 lower margin was exported as
0.000359513928219633, but the true margin is 0.00035951392821963265…, so the safe lower bound is …219632. Route B
(`str(mpf)`) and `direct_new_certs.py` used the same pattern. Astra did not rerun those two; Claude found them in the same
code review.

**What was affected.**
- **Not affected:** every certified/not-certified decision. Those comparisons were always made inside Arb or mpmath
  interval arithmetic, and all margins exceed their requirements by far more than 1e-15.
- **Affected:** the exported decimal strings, used as bounds by a machine consumer. In particular, the optional
  per-certificate transfer in `arithmetic_chain.py` read `log2_margin_lower` as an exact rational. The uniform transfer,
  which uses the paper's assumed margins, was unaffected.

**Fix.**
- All three scripts now export directed bounds: lower bounds are rounded down and upper bounds rounded up, and each
  decimal is then verified in interval arithmetic to lie on the safe side (the last digit steps if not).
- Route A and the direct-new script also export full midpoint ± radius balls (`margin_ball`, `integral_ball`).
- **No quadrature or comparison logic changed.**

**Reruns (all from fresh processes):**
- Route A: 430/430 certified, 100 s.
- Route B: 430/430 certified, 1020 s.
- Directly certified new certificates: 430/430, least new margin ≥ 0.000131537178744.
- `arithmetic_chain.py`, per-certificate transfer now fed only directed lower bounds: all > 1e-6.

**Audit.**
- 0 violations: every directed lower bound lies below, and every directed upper bound above, both Claude's ball and
  Astra's independently exported ball (`routeA_with_balls.json`) for all 430 certificates.
- 190 lower and 240 upper legacy strings moved by one unit in the last digit.
- Tightest margins are unchanged in substance: rho0 / filter 28 ≥ 0.000253791727568901; rho1 / filter 34
  ≥ 0.000359513928219632 (was printed …633).

**Use these files:**
- `routeA_8192_directed.json`, `routeB_directed.json`, `direct_new_directed.json`, `arithmetic_chain_directed.json`;
- or Astra's `routeA_with_balls.json`.

The v1 files are kept in `legacy_v1/` for provenance only; treat their decimal "bounds" as display values.

**Outside review status.**
- Astra independently enclosed the three tightest certificates (rho0 f28, rho1 f34, rho2 f3) with its own code and got
  the same values.
- Astra reran Route A (430/430, every non-timing field equal), K1 and the arithmetic chain, and checked the scalar chain
  with exact rationals (tau + 20 eps = 0.4876759502; gap 4.98e-8).
- Astra's parser matched all 43 filters / 430 rows against the pinned Base TeX.
- **Mistake logged (Claude):** "lower bound" labels were attached to rounded displays. Credit to Astra for catching it.
- The 0.487676 claim remains conditional on the non-numerical premises listed above.
