# C11 notes: critical-type route to the joint bound (2026-11-03 ~18:05 ET; theory notes, not an experiment)
- **Donsker–Varadhan:** log2 mean 2^h = max_t (E_t h - KL(t || U)). So each moment condition is equivalent to:
  every type t whose pattern (E_t u, E_t v) lies in the sampling set S satisfies E_t[lambda] + phi - KL(t) <= eta.
  Maximizing over t under linear constraints on (E_t u, E_t v) is dual to minimizing over affine forms, so the
  reformulation is exact. It is not a shortcut: a proof must still cover all densities.
- **Corner equations** at the certified point (M1 tilt at optimal p; c10_prop.json):
  - E_t u = .02906 = Delta;
  - E_t v = .46036 ≈ Gamma = .46074;
  - E_t D = .48942 ≈ tau;
  - E_t lambda - KL = .518821 = log2 M1 ≈ eta = .51886.
- **Missing lemma ("amplitude costs entropy"):** a lower bound on E_t[v], over all densities (f, g, kappa) and
  types t, in terms of (E_t lambda, KL(t), E_t u). With it, the critical type certifies infeasibility above the
  bound. The pointwise relaxation (C5-B) and the Bhattacharyya relaxation (C7) are two weak versions of it
  (capacities .0426 and .0382). The truth is ≈ .029.
- **Status:** OPEN. Written into paper Section 8, item 1.
- **Also noted:** Base (0.4877) changes both the list construction (mask density a; alias constraints C1–C8) and the
  estimator (43 filters in 10 regions), consistent with our diagnosis that both walls must move. Next lead: test
  whether 16 blocks or asymmetric densities transfer to Base. That needs Base's TeX, which is not on the laptop
  (C2 kept only the parsed data). The repo page was not reachable from this session.
