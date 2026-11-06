# Astra round 6: exposure and computation register

EVIDENCE — Scope: only A_referee_and_base_core has been opened. B remains unopened. No external mathematical sources or other project folders have been opened. Python package availability was inspected through the interpreter without opening package source folders.

EVIDENCE — Blindness limitation: the initial locator search matched more than headings. Before independent proofs I saw Base lines 260, 262–267 (the Corollary D case split), 274–275 (fixed signing), 501 (Corollary D application), 541 (trial amplification), 655–656 (finite-circle convergence), 723 (the constant 6 sum z). A later definitions read exposed lines 473–482 (A4 union bound and good-set implication) and the identity at 339. I also read algorithm prose 310–315 and the statement/definition material listed in BLIND_BASE_CORE.md. Thus Corollary D is not fully blind; A5's bad-set substep is not fully blind. No A5 full proof or B2 proof body was read before the blind file was written.

NOT CHECKED — The supplied commit label 44c34961 is provenance supplied by the user, not independently authenticated against a repository.

## Experiment R0: environment only (registered retrospectively, not a mathematical computation)
EVIDENCE — Python 3.12; mpmath, numpy and scipy available; python-flint unavailable. No mathematical numbers were computed. Directory and source-line counts are navigation metadata.

## Experiment A-N1 (pre-registration, before implementation/run)
CONJECTURE — The frozen candidate satisfies the stated scalar strict inequalities and both continuous moment bounds. The weakest scalar/moment slack may require more precision than printed values.
PROVED — Control design: exact decimal parameters; outward interval elementary functions; inner and outer quadrature must carry analytic error bounds, not convergence alone. Check entropy at 1/2 equals 1, constant filters have D=A=E=0, and compare nested resolutions as a diagnostic only. Any unresolved bound is NOT CHECKED, never rounded into a pass.
EVIDENCE — Resource cap: one foreground Python computation at a time, single numerical-library thread, hard planned runtime below 30 minutes, arrays kept modest. Scripts and results remain in out.

## Experiment A-C1 (pre-registration)
CONJECTURE — Small exhaustive instances satisfy the three layer lemmas and Corollary D under their written hypotheses.
PROVED — Controls: exact integer subset sums and rational probabilities, include repeated/zero/negative weights, test only legal sizes, preserve any failure. This is evidence only, not a substitute for the proofs. Do not run if the analytic proof makes the computation unnecessary.

EVIDENCE — A-N1 bounds-only outcome: all independently derived scalar slacks and controls passed. For N=4096, the analytic outer errors are enclosed by 4.5410e-31 and 3.58264684e-27. This validates the planned grid before the moment run. No candidate moments have yet been computed by this script.

## Experiment A-N2 (pre-registration, full interval moments)
CONJECTURE — At N=4096, 50 decimal interval digits, both log moments will be below rho_c. Expected values from untrusted source were already seen; this is independent code, not blind numerical prediction. Controls are exact asymmetric circular correlation, zero-filter scores, entropy at one half, positive convolution denominators, and imaginary FFT residuals enclosing zero. Inner strip 0.1, outer strip 0.04; absolute quadrature bounds computed before run. One process, expected a few minutes, maximum 30 minutes. If successful, N=8192 is a resolution diagnostic and independent error-bound check under the same preregistration.

PROVED — A-N2 outcome: N=4096 certificate passed. log2 M1 is in [0.51599187405865778647641245720363800, 0.51599187405865778647641245720455427]; log2 M2 is in [0.51599162047014794189115095280871168, 0.51599162047014794189115096003773423]. Rigorous positive margins are saved in A_certificate_4096.json. EVIDENCE — elapsed time was under 8 seconds. Proceeding to the pre-registered N=8192 diagnostic.

PROVED — A-N2 resolution outcome: N=8192 also passed; its moment enclosures are contained in the N=4096 enclosures. EVIDENCE — runtime under 20 seconds. No additional moment runs are needed.

EVIDENCE — A-C1 was not run: the representative-counting proofs establish the small-layer assertions directly, so a finite sweep would add little to this referee exercise.

## Experiment A-B1 (pre-registration)
CONJECTURE — Base's original constants have the margins used in bad-set removal and B2/B3. Controls: exact decimal interval inputs, explicitly subtract the asserted B3 decay and the guard contribution. This is a short scalar computation only, using newly written base_core_constants.py; no original certificate code is run.

PROVED — A-B1 outcome: all local Base constants passed; BASE_CORE_CONSTANTS.json contains outward enclosures. The row-error restriction and bad-set-removal margin hold.

EVIDENCE — Part A gate: REFEREE_SECTION_T.md and BASE_CORE_ASTRA.md are now written, including the scalar/moment certificate, analytic quadrature error proof, independent proofs, exposure disclosure, and line-by-line comparison. B has not yet been opened. The mathematical A verdict is PASS WITH REPAIRS; blind-protocol limitations are expressly recorded. All A computation runs were sequential and under 30 minutes.

## Experiment B-K1 (pre-registration)
CONJECTURE — Exact Hall checks will not find an actual k=1 violation in the prescribed small/structured sample. A stronger local-cancellation construction may fail: use same-Y capacity by class to cancel min(local supply, local capacity), then ask whether the remaining excess can be transported along YP. Prediction: either a small explicit obstruction to that stronger construction, or a useful sufficient residual inequality. Prop-1 is also checked, with no general proof presumed.
PROVED — Controls required before search: the forbidden (-3,-3,-2,-2,0,0), (k,t)=(2,3) must have Q>1 and total supply>capacity; (0,0,1,4), (1,2) must give Q=1 and Hall ratio 1; powers-of-ten generic weights must give Q=1. All subset sums, occupancies, cuts and capacities use exact integers/Fractions. Enumerate all unions of repeated classes, not an approximate max-flow solver. A separate direct near-miss/target enumerator verifies the k=2 negative control. One process, no threads, arrays only one small instance at a time. Search stops after 110 seconds; if truncated, report actual case count and do not call the planned grid exhaustive.

EVIDENCE — B-K1 outcome: all 3371 actual-weight cases passed exact Q, all class-union Hall checks, Prop-1, and the stronger residual local-cancellation test. Controls passed, including the infeasible k=2 control. Runtime under 16 seconds. No general proof follows from these checks; local cancellation remains a conjectural sufficient route.

## Experiment B-PROFILE (pre-registration)
CONJECTURE — The much stronger relaxation that allows an arbitrary subfamily of multiplicity profiles may fail the quadratic inequality. Prediction uncertain: this drops additive consistency and may reveal a precise missing constraint. For profile j of size t, test ||sum_F j||²≤t*C(m−1,t−1)*|F|. This relaxation contains every actual fiber system as fractional profile coefficients θ∈[0,1]; convexity makes subset indicators the extreme tests. Controls: exact integer arithmetic and direct ratio; any violating subset is only a counterexample to the relaxation, never to Q_w without realizable weights. Enumerate when at most 16 profiles; otherwise a fixed-seed local search, at most 45 seconds, one process. Retain negative/unfinished result as a dead end.

EVIDENCE — B-PROFILE completed its prescribed search without finding a counterexample (under 10 seconds), but the success branch printed only “finished” and failed to save its counters. This is a logging defect, not a mathematical failure. The next run fixes only that output branch and repeats the same registered deterministic search to preserve the actual coverage.

## Experiment B-EXAMPLES (pre-registration)
PROVED — Analytic prediction: the ordinary spectral contraction J J^T ≤ t*C(m−1,t−1) I is false for the profile incidence matrix with capacities (2,1,1), t=2. Test the exact coefficient vector (1,3/5,3/5,1/5); it should violate the l2-right-side strengthening while satisfying the correct l1 bound. This is an obstruction to a spectral proof, not to Q_w. Compute full rational tables for the stated t=2 equality controls and two t=3 one-pair examples, plus a triple class. Controls: all actual examples must satisfy exact Q and Hall; the forbidden k=2 example remains separately recorded and is never routed by a claimed k=1 map.

PROVED — B-EXAMPLES outcome: the spectral strengthening fails exactly (288/25 > 264/25), while the true l1 right side is 72/5. All actual-weight examples pass Q and Hall. The forbidden control has Q=29/28, supply 30, capacity 27, and free routed fraction 9/10. EVIDENCE — The corrected profile log records 503 exhaustive profile families and 3,627,047 exact subset checks, plus the prescribed larger-family local searches, without a violation.

## Final certificate rendering repair (pre-registration)
PROVED — Code review identified a rigor risk in decimal output formatting: multiplying an endpoint in finite-precision arithmetic before applying floor/ceiling could theoretically cross a decimal boundary. The numerical interval calculation itself is unchanged. Replace formatting with exact integer division of the binary endpoint mantissa/exponent, then rerun both registered grids and Base scalar checks. Prediction: the displayed enclosing endpoints agree at the reported precision; all strict tests remain positive. This rerun is justified by the new formatting concern, not by an attempt to improve a failed certificate.

PROVED — Certificate rendering repair outcome: both N=4096 and N=8192 passed again; their reported enclosures are unchanged, now rendered with exact outward integer division. Base constants also passed. The earlier formatting risk is closed.

## Final consistency check (pre-registration)
CONJECTURE — Both grids' outward enclosures nest, all scalar and moment lower margins are positive, the exact rational exponent is 0.4873407528, and the forbidden control is exactly 29/28 with supply 30 and capacity 27. Check report existence, source syntax and summary length; regenerate the scalar table from the final certificate. Record SHA-256 hashes only of the supplied A/B files within Astra_round6. Hashing is provenance metadata, not authentication of the supplied commit label. No further mathematical search is planned.

PROVED — Final consistency outcome: all checks passed. There are 43 positive scalar checks; both moment grids pass and their enclosures nest. The exact threshold is 609175941/1250000000 = 0.4873407528. The forbidden control is 29/28 with supply 30 and capacity 27. EVIDENCE — The summary has 482 whitespace-delimited words. Input hashes, report presence and script syntax are recorded in FINAL_CHECK.json and INPUT_SHA256.json. All four requested reports and all original scripts are present in out. NOT CHECKED — The general k=1 theorem for t≥3 remains unresolved; the reports expressly distinguish the new t=2 proof and proof-strategy obstructions from a general solution.
