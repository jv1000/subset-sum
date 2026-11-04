# C9: estimator-side price list, and amplitude-stratified patterns (pre-registration)
**Written 2026-11-03 ~17:20 ET, before any C9 run.** Jennifer: "Yes let's proceed" (estimator-side price list).

## Analytic price list (algebra; to be checked in the write-up)
- **Separate sampling budget tau_s from list budget tau_l.** The MSE exponent is rho - tau_s + tau_l - eta and
  T >= max(tau_s, tau_l). Gain 0.
- **Enumerate more patterns** (sampling only where alpha U < Delta - delta, enumeration budget tau + delta). Both
  moments get cheaper by about (p-1)delta and (q-1)delta bits, worth about delta of capacity, which is about
  .35 delta in T by the price list. The cost is +delta in T. Net loss of about .65 delta.
- **More cases, or the hull domain** for the (U, W) domination: 0 (C6, measured).
- **Larger rounding allowance** (30 eps -> C eps, removes the q_m cap): 0 at today's joint optimum (cap slack); it
  matters only after a capacity gain.
- **Finer score grid** (eps -> 0): at most 20 eps = 2e-7 in T.

## New knob: stratify patterns by amplitude (estimator change)
|J_rho(k)|^2 = prod_i M(x_i)^2 = 2^{n Lambda-bar} exactly, with lambda(x) = log2(2 + 2cos x). Add block averages of
lambda (rounded to eps, like D, A, E) as a 4th pattern coordinate Lambda. The pattern count stays 2^{O(sqrt n)}.
On a pattern, L_pi |J|^2 <= 2^{(eta - alpha U + Lambda + O(eps)) n}. Dominate by an affine form
l = c0 + c1 u + c2 v + c3 lambda with l >= phi(U, W) + Lambda on the pattern's region. The moment becomes
mean_x 2^{l(x)}. The paper is the special case c3 = 1, where 2^{lambda} = 2 + 2cos x. A region's Lambda-range
lets c3 differ from 1. The bottom region (Lambda -> -infinity) needs c3 <= 1. Rounding: 3|c1| + 4|c2| + |c3| + 1 <= 30.

## Experiment C9 (floating; tau = .4898; N = 1023, odd, to avoid x = pi exactly)
Fixed densities (Astra 6-term; our 16+16). Generic (U, W) domain, split at W = Gamma. The Lambda-axis is cut into
k strips on [-L0, 2], plus a bottom strip (-infinity, -L0], with L0 = 8.
- **Control:** k = 1, c3 = 1 must reproduce .02810 / .02906.
- **Runs:** k = 1 with c3 free; k = 2, 4, 8, 16.
- **Prediction (honest uncertainty):** P(any gain > .001) = .35; P(gain > .005) = .1.
- **If there is a gain:** check it on the hull domain, re-optimize densities, price it, and audit the estimator
  change at source level (the pattern definition and the Chebyshev coverage step for the 4th coordinate).

## Results (2026-11-03 ~17:40 ET)
- **C9 generic domain (floating):** Astra densities: control k0 c3=1 .02810; c3 free .02810; k = 2/4/8/16 strips
  .02810 each. Gain 0. Binding strip: Lambda in [-.5, .75] (the typical band), where the optimal form is the paper's
  (c3 = 1).
- **Why, by duality (argument, to be written up):** for a strip at Lambda*, the best tilt minimizes
  (1 - c3) Lambda* + psi(c3), with psi(c3) = log2 mean 2^{c3 lambda - p u} convex. The worst strip maximizes over
  Lambda* <= max lambda = 2. Minimax gives min over c3 <= 1 of [2(1 - c3) + psi(c3)], which improves on c3 = 1 only if
  psi'(1) > 2. That is impossible, since psi'(1) is an average of lambda <= 2. So amplitude stratification gains
  nothing on the generic domain.
- **Escape test on the joint hull (LP over conv{(u, v, lambda)} ∩ sampling region):** a gain needs the largest
  sampling-region amplitude to fall below psi'(1). Astra: psi'(1) .5755 vs max Lambda .668 (region 1) / .693
  (region 2). Ours: .5731 vs .643 / .630. No escape, near miss by .06–.07 in Lambda. By the same minimax argument
  (with 2 replaced by max Lambda), the best tilt is still c3 = 1. Predictions: P(gain > .001) = .35 — no gain.
- **Estimator-side price list (all knobs within the OpenAI checksum design):**
  - separate sampling budget: 0 (algebra)
  - larger enumeration threshold: net loss ≈ .65 delta (algebra)
  - more cases, hull domain: 0 (C6)
  - rounding allowance: 0 now
  - finer eps: <= 2e-7
  - amplitude stratification: 0 (C9, with a duality reason and a near miss of .06 in Lambda)
- **Conclusion:** within this checksum design the moment wall is robust. Getting past ~.4895 needs a different
  variance argument for the estimator (not pointwise domination of a product moment), or an improvement on the list
  or pair side (representations, mixing), or a different route (Ye–Li).
