# C6: more than two cases in the checksum's domination step (pre-registration)
**Written 2026-11-03 ~16:50 ET, before any C6 run.** Jennifer: "let's pursue your top pick with more than 2 cases."
Classification: floating exploration. Any claim needs a source-level write-up, rigorous hull and moment enclosures,
and a referee.

## The proof step (checksum.tex l.434-481)
For a sampled pattern (U, W) (alpha U < Delta, alpha = min(1, Gamma/W)) the proof needs an exponent form R with
  -alpha U <= -Delta + R(ubar, vbar) + rounding,
and then bounds E prod_i M(x_i)^2 2^{R(x_i)} by (mean (2+2cos x) 2^{R(x)})^n. R must be AFFINE in (u, v) for the
product step. The paper uses two forms: R1 = p(Delta - u) when W <= Gamma, R2 = q_m(a v - u) when W > Gamma.

## The generalization (analysis only; the algorithm is unchanged)
- **Target:** phi(U, W) = Delta - alpha(W) U on the sampling set S = {alpha(W) U < Delta}.
- **Cover:** any finite family of affine forms l_r = c0 + c1 u + c2 v with assigned pattern regions R_r covering S,
  l_r >= phi on R_r, and moments M_r = mean (2+2cos x) 2^{l_r(x)} < 2^{rho_c}. Rounding: |ubar - U| <= 3 eps and
  |vbar - W| <= 4 eps, so 3|c1| + 4|c2| <= 30 keeps the 30 eps allowance.
- **Domain lever:** the domination is needed only at real frequencies, whose (ubar, vbar) are averages of the
  points (u(x_i), v(x_i)). They lie in H = conv{(u(x), v(x)) : x in T}. The paper effectively covers the larger
  generic region W >= 0, U >= -W.
- **Regions:** k strips in W, cut at quantiles of W over H ∩ S, with Gamma always a cut.

## Experiments (tau = .4898, rho = tau + Delta - 3e-6, densities fixed per run, N = 1024)
- **D0 control:** the paper's forms (p in [1,10], q_m in [1, cap]) and the generic domain. Reproduce the
  fixed-density capacity: Astra 6-term ~.0281, our 16+16 ~.0290.
- **D1:** 2 regions (split at Gamma), full affine (c0, c1, c2) per region, generic domain.
- **D2:** 2 regions, full affine, hull domain H.
- **D3:** k = 4, 8, 32 strips, full affine, hull domain H.
- Capacity is found by bisection on Delta. Each region is a convex program: minimize log2 M_l subject to linear
  dominance constraints at sampled points of the region, an 80x80 grid plus hull vertices plus boundary points.

## Predictions
- D0 reproduces within .0003.
- D1 adds little (< .001): on the generic domain the vertex (U, W) = (-W, W) and the boundary U -> Delta force the
  paper's shapes.
- D2/D3 help more. P(D3 capacity >= .032 for the 16+16 densities) = 0.35. P(any gain > .001) = 0.6.

## If capacity rises
Re-optimize densities and scalars jointly with the best scheme (as in s5.py), freeze, certify, referee, price.

## Results (2026-11-03 ~17:10 ET), floating
| Scheme | Astra 6-term | Our 16+16 |
|---|---|---|
| D0 paper forms, generic (control) | .02810 | .02906 |
| D1 2 affine forms, generic | .02810 | .02906 |
| D2 2 affine forms, hull | .02810 | .02906 |
| D3 4 / 8 / 32 affine forms, hull | .02810 / .02810 / .02810 | .02906 / .02906 / .02906 |
- D0 control PASS (reproduces .0281 and the C5 value .0291). Prediction D1 "adds < .001" HELD (adds 0).
  Prediction "D2/D3 help more", P(gain > .001) = .6: FAILED — gain is exactly zero.
- **Why:** the score hull is a thin band (v in [.386, .628] Astra; [.382, .601] ours). Only the strips adjacent to the
  case switch W = Gamma bind (log2 M = eta there); all other strips have slack (.50, .025, -1.2 bits) or are empty.
  The binding slice is W = Gamma, where alpha = 1 and the target is Delta - U for both cases; any number of affine
  forms must still dominate that one slice, and the paper's p(Delta - u) is already the best affine form there.
- **Conclusion:** the moment wall is not an artefact of the two-case proof. It sits at the case boundary
  W = Gamma. Escaping it needs a change of the target itself (the estimator: alpha, the sampling/direct split, or
  the match-count bound L_pi <= 2^{(eta - alpha U)n}), not more cases. A "slice lemma" (a Hölder-type lower bound
  for affine forms dominating Delta - U on the hull slice at W = Gamma) is the natural candidate for the joint bound.
