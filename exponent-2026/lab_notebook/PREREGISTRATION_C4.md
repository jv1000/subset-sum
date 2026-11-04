# C4: a concrete point below .48977 by changing the block count (pre-registration)

**Written 2026-11-03 ~15:15 ET, before any C4 run.** Jennifer: ".4852 would be an improvement worth our while."
**Classification of the search: floating exploration.** Any claim needs C4b (rational slack, rigorous moments,
interval scalar recheck, independent referee) and remains conditional on the OpenAI paper's own correctness and on
the reading audit AUDIT_K8.md.

## Constraint system (full; fixes C3's incomplete S3 model)
Variables mu, eta, tau, gamma, r(6), s(6), kappa, p, q_m; K fixed per run. T = tau + 20 eps, eps = 1e-8, g = 1e-5,
coverage c0 = .0001 (c = .9999). Closure form with d = .5 - gamma (rational slack restored in C4b):
list, pair, preliminary (tau >= .5 - c K mu d), sparse (eta >= h(mu) + mu + g), setup (tau >= 1/4 + mu),
prime (tau >= eta/2), blocks (mu <= 1/K), moments (eta - 3e-6 >= log2 M1, log2 M2 at 128 nodes),
1 <= p, 3p <= 30, 1 <= q_m, q_m(4a+3) <= 30, strip (nf-1)(ng-1) <= .49 (Astra's certifiability heuristic),
0 < Delta, Gamma > 0. Moment evaluator: Astra's FFT `evaluate` (matched to my direct-sum code to 7.5e-15, C3 MC0).

## Runs
- **Control C4-0:** K = 17 from Astra's best point must stay at T ~ .48977 (within 1e-6) and all residuals >= -1e-9.
- **Main:** K = 9..13. Start from Astra's best densities; scalars initialized at mu = .97/K, eta = h(mu)+mu+.002,
  tau = .4875, gamma = .48; plus 6 perturbed starts per K (rng 20261103+seed; coefficient noise .12/.35; kappa,
  p, q_m uniform as in C3). SLSQP, ftol 1e-13, maxiter 1500. Report best T per K, all residuals, KKT multipliers.
- Best point is re-evaluated at 256 nodes; the M1 Hölder bound is checked against it (must hold).

## Predictions
- Holder floor (M1 only, closure) is .48516 at K = 11; M2 and real densities raise it. Prediction: best T in
  [.4855, .4880], at K in {10, 11, 12}. P(best T < .48977 - 1e-4) = 0.75. P(best T < .4860) = 0.25.

## Kill / success
Success for C4a: residuals all >= +1e-8 at a point with T < .4897 (i.e. clearly below the current .4897736).
Otherwise report the bounded-search null with the best T per K.

## Amendment 1 (15:30 ET): first C4 runs, then a mu-continuation
- Control C4-0 PASS: K=17 -> T .48977344 (Astra .4897736), min residual -5e-14.
- K=9..13 (7 starts each): best T .490067 / .489911 / .489860 / .489817 / .489781. Every best point sits at
  mu ~ .058 (Astra's old basin) with the block cap slack, so smaller K only weakens the preliminary bound. This is a
  local-search artifact relative to the floor analysis, which uses mu near 1/K.
- Added (before running it): **mu-continuation** for K = 11, 12: fix mu on a grid from .058 to 1/K - 1e-6 (25 steps),
  minimize T over the other 18 variables, warm-starting from the previous step. Report T(mu) and the moment
  margins. Prediction: T(mu) has an interior minimum; P(min over the grid < .48977) = 0.4 (lowered from .75 after
  seeing the basin result).

## Amendment 2 (15:45 ET): continuation result, and a moment-capacity diagnostic (pre-registered here)
- **Continuation (K = 11, 12):** T rises monotonically with mu (K=11: .48986 at mu .0586 -> .49146 at .0882; infeasible
  beyond ~.089 by sparse); Delta stays pinned at .0284–.0287 by both moments. Prediction "interior minimum" FAILED; no
  point below .48977. So, with real 6-term densities, changing K does not help: the binding resource is how large a
  Delta the filters can support, not the block count. The M1-only Holder floor (.4852) assumed Delta up to ~.04.
- **Capacity diagnostic C4-cap (floating):** at fixed tau in {.4898, .4860}, maximize Delta subject to
  log2 M_i <= tau + Delta - 3e-6 (i in a chosen set), multiplier caps, positivity; densities with n_c cosine terms,
  coefficient box [-2.5, 2.5] (and [-4, 4] for n_c = 12). Cases: {M1 only, n_c = 6}, {M1+M2, n_c = 6}, {M1+M2, n_c = 12},
  {M1+M2, n_c = 12, box 4}. 6 starts each, 300 s total cap. Compare with the Holder M1 capacity Dmax(tau).
  Predictions: M1-only capacity ~.035–.040 (near Holder); M1+M2 n_c = 6 ~.0284 (reproduces); n_c = 12 adds < .002.

## Amendment 3 (16:00 ET): capacity results (all floating)
- C4-cap at tau .4898 / .486: M1 only (6 terms) .03959 / .03866 (kappa -> 1, p ~ 5.1; Holder ceiling .04268 / .04175);
  M1+M2 6 terms .0281 / .02747; M1+M2 12 terms .02876 / .02813, identical with box 4. Predictions: M1-only "~.035–.040"
  HELD; "M1+M2 ~.0284" HELD; "12 terms adds < .002" HELD (+.0007).
- cap_price.py: floor T vs Delta_cap (closure, grid): .0281 -> .489769 (K 17; reproduces Astra's .48977 basin), .032 ->
  .488403 (K 15), .036 -> .487033 (K 13), .0396 -> .485791 (K 12), .0427 -> .484747 (K 11). Shadow price of capacity
  ~ -0.35 exponent per unit Delta. The best K drops only as capacity rises.
- C4a success criterion NOT met (no point below .4897). Conclusion: the narrow objective is M2 capacity.
