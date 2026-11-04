# C3 result: working backward from 0.48 in the OpenAI 0.49 architecture

2026-11-03, Claude, for Jennifer (continuing Astra's `target_048` handoff). **No 0.48 algorithm is claimed.**
Labels used: RERUN, READING AUDIT, FLOATING (exploration), INTERVAL (outward-rounded enclosure), PROOF (short written
argument; independent referee pending — see Status).

## Headline
1. **Astra's K = 8 scalar point is scalar-admissible but its first moment cannot be met by any filter.**
   PROOF + INTERVAL: for any positive densities f, g and any kappa, log2 M1 >= Phi(p) = 1 + p Delta + g(p) with
   g(p) = (1+p) log2 E[(1+cos x)^{1/(1+p)}]. At Delta = .1900002, min over p in [1,10] of Phi >= **.885370**
   (mpmath iv, 9000 monotone cells), versus the required .669998: **fails by .2154 bits**, for every density family.
2. **The same bound pushes the whole architecture's floor above .48 for every block count tried (K = 1..40; the
   floor rises steadily for K > 11).** FLOATING (grid-based, optimistic closure): adding the M1 bound to the audited
   scalar budget gives a floor of .48543 at K = 8 and a best of **.48516 at K = 11**; without it, K = 8 would allow
   .47903. At K = 17 the bound is not binding (floor .489515, unchanged), consistent with Astra's certified .4897736.
   Note the flip side: K ~ 9–12 floors (~.4852–.4853) sit well below today's .48977, so changing K is still a live
   route to a *smaller* improvement, once M2 and real densities are added.
3. **Reading audit: the 17 -> K replacement itself is legitimate.** 17 appears in two places (block fit; partition +
   Markov), both generalize; every other dependence is through mu. The checksum section is generic in (eta, tau).
   No scalar constraint is missing from Astra's twelve (AUDIT_K8.md).

So within this proof's moment format, 0.48 is blocked by mathematics, not by the search: the pair-count bound forces
Delta = eta - tau > 1 - 2 tau (= .04 at tau = .48), the sparse-prime bound at the needed block size forces
Delta ~ .17, and the M1 bound allows only Delta <= Dmax(tau) ~ .0403 at tau = .48. These cannot hold together.

## Why the M1 bound holds (the Lebesgue / level-set connection)
- Jensen with the probability density K_x: u(x) = ∫ K_x log2[f*(x+w) g*(w) / K_x(w)] <= log2 Q*(x), where
  Q* = f* ⋆ g* is itself a probability density on the circle.
- w = 1 + cos x is a probability density, and M1 = 2^{1 + p Delta} E_w[2^{-p u}] >= 2^{1 + p Delta} E_w[Q*^{-p}].
- Hölder: E_w[Q*^{-p}] >= (E[w^{1/(1+p)}])^{1+p}, with E[w^b] = 2^b Γ(b+1/2)/(√π Γ(b+1)).
- g(p) is a log power mean of w, nonincreasing in p, which makes the interval minimization over p rigorous.
- Near-tight: equality needs kappa = 1 and Q* ∝ w^{1/(1+p)}. So no choice of densities can do much better.

This is the "sharper distributional inequality" Astra's handoff asked about: it bounds the **true** moment (Astra's
claim type iii) from below for all densities at once. Changing Riemann to Lebesgue integration changes nothing; a
distribution-level inequality (Jensen + Hölder against the weight measure w) rejects the candidate outright.

## What was run
| Item | Label | Result |
|---|---|---|
| target_audit.py, independent_recheck.py | RERUN | byte-identical outputs; 71 containments pass |
| check_point.py (my mpmath code, formulas from RESULT.md) | independent recomputation | all 12 margins agree to < 1e-15; T = .48 exactly |
| s1s2.py: two-bound floor by K | INTERVAL | K-a reproduces Astra's floors; largest K below .48 is 8 |
| AUDIT_K8.md | READING AUDIT | adaptation legitimate; no missing scalar constraint |
| moments_c3.py MC0 | control | my direct-sum evaluator = Astra's FFT evaluator to 7.5e-15 at the certified point |
| D1: old densities, p = 8, q_m = 5 | FLOATING | log2 M1 = 1.815, log2 M2 = 1.938 (128 = 256 nodes) |
| D2: bounded search, 8 starts, 6 s | FLOATING | all starts -> max excess +.3395 bits (log2 M ~ 1.0095, kappa 1.269, p = q_m = 1) |
| holder_cert.py | INTERVAL (of the proved bound) | min Phi >= .885370 > .669998 |
| holder_floor.py | FLOATING | floors by K as above |

## Failures preserved
- My first model (Astra's Round 5 residual with 17 -> K) lacked the sparse-prime, setup and prime conditions; its
  S2/S3 outputs are kept but are not evidence (PREREGISTRATION_C3.md, Amendment 1).
- s1s2.py v1 took eta_min at the wrong end of the d interval (fixed; v1 kept).
- An overly slow first holder_floor.py was stopped and rewritten (closed form for Dmax); no result came from it.
- The E5 dss13 head-to-head (separate project) was stopped by a time limit and restarted; its rerun shares the
  sandbox with this work, so its timing carries a ~15% contamination note.

## Limitations
- The obstruction concerns this proof's **sufficient** moment format (M1 with weight M² and one multiplier, p >= 1),
  not subset-sum algorithms in general. An estimator or domination step that avoids M1, or a different list/pair
  analysis, could escape it.
- The floor-by-K numbers are grid-based floating estimates; a grid can miss feasible points, so they could be
  slightly too high. A dual-style argument or interval sweep is needed before quoting them as bounds.
- The PROOF is short and written by Claude; an independent referee check is running (see Status).
- Layer-cake arc certification (Astra's suggested test) was not run: Route A's quadrature error is already ~1e-218,
  so it cannot tighten an existing upper bound appreciably; its only remaining value is cost (claim type i).

## Next smallest discriminating experiment
Turn holder_floor.py into a rigorous statement: for each K, an interval sweep over (mu, d) with the closed-form Dmax,
proving "no point of the closure with M1-feasibility has T < .4851". Then ask whether M2's analogous bound
(log2 M2 >= 1 + g(q_m), plus the v term) raises it further. If a sub-.4897 target is wanted, K ~ 11 is where to look.

## Status
**Referee check of the PROOF (independent agent, fresh context, own code; scripts in `referee/`): CONFIRMED.**
- Each step was checked: the Jensen direction, Q* integrating to 1, the Hölder exponents. The closed form for
  E[w^b] matches quadrature to ~1e-15.
- 300 random instances (degree 1–6, coefficients ±2.5, peaked cases included, N = 256 and 512) plus 16 adversarial
  Nelder–Mead searches: the minimum gap log2 M1 − Phi was +0.10686 (random) and +0.0009 (adversarial). No
  counterexample.
- (a) Monotonicity of g: confirmed. (b) The true minimum at Delta = .1900002 is .885560 at p ≈ 1.1578. Our
  interval value .885370 is a valid lower bound below it.
- **(c) Correction: the finite circle needs the discrete constant.** On Z/PZ the argument goes through with the
  DISCRETE average of w^{1/(1+p)}. For even P that average is smaller than the continuous closed form, so the closed
  form alone is false there. Referee counterexample: P = 4, gap −0.154. The shortfall shrinks fast: −2.3e-6 at
  P = 1024 for p = 1, roughly like P^{-1-2/(1+p)}. Consequence here: none.
  - The proof's premise (Prop. "Filtering moments") is the continuous inequality, and the continuous bound rejects
    it.
  - The algorithm's P = 2^{eta n} makes the discrete correction negligible against a .215-bit margin.
  - Any statement about finite moments must quote the discrete constant.
- **Tightness:** the bound is nearly attained only at kappa = 1. Gaps fall to ~5e-7 with g sharply peaked and
  f ∝ w^{1/(1+p)}. At kappa ≠ 1 a fixed positive gap remains.
