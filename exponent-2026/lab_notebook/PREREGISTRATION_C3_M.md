# C3-M: exploratory moment diagnostic at Astra's K=8 scalar point (pre-registration)
**Written 2026-11-03 ~15:55 ET, before any moment evaluation at the K=8 point.** Follows HANDOFF_TO_CLAUDE.md §2 and
AUDIT_K8.md (reading audit: no missing scalar constraint found). **Classification: floating exploration. Nothing here
is a certificate.** A success would go to rigorous quadrature (Route A/B style) plus a fresh full constraint audit.

## Fixed scalar point (Astra, target_048/PREREGISTRATION.md)
eta = .67, tau = .4799998, Delta = .1900002, Gamma = .2899996, a = Delta/Gamma = .655174007136...
Targets: rho_c = .669998 (need log2 M1, log2 M2 < rho_c), rho_f = .669999. Admissible multipliers: 1 <= p <= 10,
1 <= q_m <= 30/(4a+3) = 5.3374172607.

## Evaluator (independent of Astra's code)
`moments_c3.py`: my own direct-sum implementation of the handoff definitions (O(N^2) correlations, no FFT), N = 128
and 256 nodes; 512 only if 128 vs 256 log-moments differ by > 1e-6. Positivity: F, G > 0 by construction; P(x) is
checked > 0 and any nonpositive value aborts (no clipping).

## Controls (must pass first)
- **MC0:** at Astra's certified coverage point (openai_coverage_candidate.json: eta .51787037, tau .4897734, p, q_m,
  r, s, kappa as given) my log2 M1, log2 M2 agree with Astra's `evaluate` to < 1e-10 and are below .5178685.
- **MC1:** Jensen lower bound (below) <= computed log-moment at every evaluated point (sanity).

## Experiments
- **D1:** old densities and kappa, p = 8, q_m = 5, at the K=8 point. Report log2 M1, log2 M2 at 128 and 256 nodes.
  Prediction: both fail, M1 by >= 1 bit (old filters have E_w[u] ~ .09, far below the .223 the Jensen bound needs).
- **D2 (bounded search):** minimize max(log2 M1 - rho_c, log2 M2 - rho_c) over r, s (6 each, box [-2.5, 2.5]),
  kappa in [.85, 1.3], p in [1, 10], q_m in [1, 5.33741726], by SLSQP on the epigraph form (128 nodes). Starts: 8
  deterministic — seed 0 old densities (p=8, q=5); seeds 1–7 old densities + N(0, .12 (seeds 1–3) or .35 (4–7))
  perturbations, rng 20261103+seed, kappa ~ U(.95,1.15), p ~ U(6,9.5), q_m ~ U(3,5.3). Stop: 120 s wall total
  (checked between starts; a start in progress may finish) or all 8 starts. Best point re-evaluated at 256 nodes.
- **J (rigorous, analytic):** with w = (1+cos x) a probability density, Jensen gives log2 M1 >= 1 + p(Delta - E_w u)
  and log2 M2 >= 1 + q_m(a E_w v - E_w u). Hence M_i < 2^rho_c requires E_w u > Delta + (1 - rho_c)/p >= .223 and
  E_w[u - a v] > (1 - rho_c)/q_m >= .0618. Report E_w u, E_w v at every point. (The inequality is proved; the E_w
  values are floating.)

## Prior
P(D2 finds max excess < 0) = 0.10.

## Reporting
Every start is saved with its objective, both log-moments, E_w u, E_w v, parameters. A failure is reported as "not
found in this bounded search", never as impossibility. No overnight expansion without Jennifer.

---
## Results (appended 2026-11-03 ~16:10 ET; nothing above edited)
- **MC0 PASS:** my direct-sum evaluator matches Astra's FFT `evaluate` to 7.5e-15 (log2 M1 .51786600, log2 M2
  .51786586 at the certified coverage point; both < .5178685). MC1 PASS at every evaluated point.
- **D1 (prediction held):** log2 M1 = 1.81516, log2 M2 = 1.93761 at both 128 and 256 nodes (512 not needed).
  E_w u = .1196 (my pre-registered guess ".09" was low; the conclusion is unchanged).
- **D2:** 8/8 starts done in 6 s; all converge to max excess +.33951 bits (log2 M1 = log2 M2 = 1.00951,
  kappa 1.2687, p = q_m = 1 at their lower bounds, r = s ≈ (1.152, -.113, .009, ...)). Bounded-search failure.
  Prior P(success) = .10; outcome: no success.
- **New, not pre-registered (labelled as such):** the Jensen bound in J was strengthened, after D2, to a bound over
  ALL densities (Jensen against K_x, then Hölder against w): log2 M1 >= 1 + p Delta + (1+p) log2 E[w^{1/(1+p)}].
  Interval evaluation (`holder_cert.py`): >= .885370 at Delta = .1900002 for all p in [1,10]. This rejects the K=8
  point for every density family, not just the searched one. Referee check pending. The budget-wide floor
  exploration that uses it (`holder_floor.py`) is floating and grid-based.
