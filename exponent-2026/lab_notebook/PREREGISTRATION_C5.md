# C5: the M2 question (pre-registration)
**Written 2026-11-03 ~15:30 ET, before any C5 run.** Jennifer: "please start the M2 question."
Background (C4, floating): at tau = .4898 the joint M1+M2 Delta-capacity is .0281 (6 cosine terms) / .0288 (12 terms);
M1 alone reaches .0396 (proved Hölder ceiling .0427). Price: about -0.35 exponent per unit capacity.

## C5-A (floating exploration): family limit or true limit?
Capacity(tau) = max Delta s.t. log2 M1, log2 M2 <= tau + Delta - 3e-6, 1 <= p <= 10, 1 <= q_m, q_m(4a+3) <= 30,
a = Delta/(tau - Delta). tau = .4898 throughout.
- **A0 control:** degree-6 cosine-only family, kappa in [.85, 1.3], N = 512: must reproduce .0281 +- .0003.
- **A1:** M2 only (M1 dropped), degree-6 cosine family. Is M2 alone the limit, or is it the joint constraint?
- **A2:** M1+M2 with log-densities r, s = sum_{j<=n} (c_j cos jx + d_j sin jx), n in {6, 16, 32}, coefficient box
  [-4, 4], kappa in [.5, 2], N = 512 (best point rechecked at N = 1024). Starts: Astra's best (sines 0), plus 3
  perturbed (rng 20261103+seed, noise .1 on all coefficients). SLSQP, maxiter 600; 10 min cap per case.
- Record at each optimum: binding constraints, kappa, p, q_m, whether q_m's rounding cap binds, and the strip
  quantity (nf-1)(ng-1) (dropped as a constraint here; it only matters for later certification).

## Predictions
- A0 reproduces. A1 (M2 only) capacity > .040 (M2 alone is weak: its Hölder-type bound is only log2 M2 >= 1 + g(q_m)).
- A2: n = 32 asymmetric densities gain < .003 over .0288. P(A2 capacity > .033) = 0.2.
- If A2 stays below .032, the binding object is the JOINT M1+M2 tradeoff and C5-B (a proof) is the right next step.
  If A2 exceeds .035, the density family is the bottleneck and the discovery loop should target densities.

## C5-B (mathematics): a joint lower bound
Starting identities (kappa = 1; check general kappa separately): with alpha = D - A = KL(K_x || f*(x+.)),
beta = D - E = KL(K_x || g*): u = D - alpha - beta, v = alpha + beta, so a v - u = (1+a)(alpha + beta) - D.
Mutual-information identities under the joint law of (X' ~ f, W ~ g): E_Q[u] = KL(Q), E_Q[D] = KL(f) + KL(g) - KL(Q).
Goal: an inequality bounding max(M1, M2) from below in terms of Delta (and p, q_m), proved, interval-evaluated,
numerically stress-tested against A2's best points, then refereed. No claim before that.

## Amendment 1 (15:50 ET): A0–A2 results; random-start check added before running it
- A0 control: .02810, 4/4 starts (reproduces). A1 (M2 only): .03226, binding = the q_m rounding cap q_m(4a+3) <= 30,
  not the integral. Prediction ">.040" FAILED; reason: M2 alone is limited by the 30 eps bookkeeping allowance.
- A2 (both, cos+sin, box 4, kappa [.5,2]): n=6 .02841, n=16 .02864, n=32 .02864; binding M1+M2; q cap slack
  (2.6–3.7). Prediction "gain < .003" HELD.
- Added: START=random, 6 starts per case from random coefficients (rng 777+seed, decaying 1/j), for n = 16 both
  cos-only and cos+sin, to test whether Astra's basin is special. Same caps.

## Amendment 2 (16:05 ET): random starts, and a first full-constraint candidate (floating)
- Random starts (n = 16): cos-only .02900 (6 starts: .02886 .02897 .02880 .02831 .02831 .02900); cos+sin .02908
  (.02900 .02900 .02908 .02908 .02891 .02864). Capacity saturates near .029 across families: consistent with a
  structural limit of the M1+M2 format (local-search caveat). -> C5-B (a proof) remains the way to settle it.
- s5.py (full constraints, cos+sin n = 16 densities from the best random start), floating, N = 512:
  K = 17: T .4895157 (= the 17-block floor; moments no longer binding); **K = 16: T .4894611**; K = 15: .4894858.
  Control: K = 17 with Astra's 6-term densities reproduces .4897734.
- K = 16 point: mu .059335, Delta .02902, gamma .488898, kappa 1.03489, p 8.3852, q_m 8.1957; max |coef| .97;
  Astra's strip proxy (nf-1)(ng-1) = .314 at beta .19 (< .49). This is a CANDIDATE for C5-cert, not a result.

## Amendment 3 (16:30 ET): C5-cert — frozen K=16 point and Claude's rigorous certificate
- **Pre-registered here before running certify_c5.py on the candidate:** pass = every interval margin > 0, including
  log2 M1, log2 M2 < rho_c with all quadrature errors; controls = Astra's 6-term certified point below .5178685, and a
  Delta + .001 perturbation rejected; consistency = doubled inner resolution agrees.
- freeze.py -> candidate_K16.json: T = .4894615727 (tau .4894613727 + 20 eps), mu .0593373017, eta .5184804040,
  gamma .4888978551, kappa 1.03489429, p 8.38520435, q_m 8.19573911, 64 density coefficients (8 decimals).
- certify_c5.py (python-flint arb 200 bits; inner trapezoid strip sigma .3, N_in 256; outer N 8192, strip 2beta = .2):
  control PASS (Astra point log2 M <= .5178662 < .5178685), K2 rejection PASS; candidate: q0 .3716, U* 1.336, W* 19.28,
  inner errors ~1e-27, outer < 1e-300; log2 M1 = .51847757619 (+/- < 1e-20), log2 M2 = .51847734723; all 20 interval
  margins > 0 (least: prelim_cheb 1e-9 and local_to_prime 1e-8 by construction; M1 8.478e-7; list/pairs/prelim_cap
  8.48e-7). Doubled resolution (N_in 512, sigma .25): identical to 20 digits.
- Status: Claude-certified only. Independent referee (fresh context; reads only the candidate JSON and the OpenAI TeX)
  launched. The proof-adaptation itself (K = 16, c0 = .0001, sine terms, cap = tau + 20 eps) rests on AUDIT_K8.md.

## Amendment 4 (17:05 ET): referee verdict
Independent referee (fresh context; read only candidate_K16.json and the TeX) CONFIRMS the K = 16 point: own
constraint derivation (no missing or violated constraint), own rigorous moment certificate matching ours to 16
digits. Flags: orientation convention must be explicit (reflection gives log2 M ~ 3.28); the exponent is to be stated
as O(2^{T'n}) for any T' > .4894615727; the JSON floating margins are ~1e-10 optimistic vs the published decimals.

## Amendment 5 (17:20 ET): C5-B candidate joint bound — pre-registered before computing it
Claim to test (proof sketch, all kappa): (i) u <= log2 Q*(x), Q* = f*⋆g* a probability density (Jensen, as in the M1
lemma); (ii) v = (D-A)+(D-E) >= 0 and u + v = D >= 0, so v >= max(0, -u). Hence with Q := 2^u (so mean Q <= 1):
  M1 >= 2^{1+p Delta} mean_w Q^{-p},   M2 >= 2 mean_w h(Q),  h(Q) = max(Q^{-q}, Q^{-q(1+a)}),
with w = 1+cos x. The relaxed problem inf_{Q > 0, mean Q <= 1} max(M1', M2') is convex; weak duality gives, for any
lambda in [0,1], nu >= 0: max(M1,M2) >= 2 mean_x psi(w(x)) - 2 nu, psi(w) = inf_Q [w(lambda 2^{p Delta} Q^{-p}
+ (1-lambda) h(Q)) + nu Q]. Joint capacity bound: largest Delta at which some admissible (p, q_m) has relaxed value
<= 2^{tau+Delta}. Prediction: strictly below the M1-only .0427 at tau = .4898; P(< .035) = 0.4. It must stay >= the
empirical .0291 (else the derivation is wrong). Numerical first (floating); a rigorous version only if it is useful.
- **Result (17:35 ET), floating:** joint.py (dual grid version) was too slow and was stopped with no output. joint2.py
  (primal, free profile u on an odd grid, exact gradients): relaxed joint capacity .04241 (N = 255), .04258 (N = 511),
  6/6 starts identical, at p ≈ 5.03, q ≈ 6.50 — essentially the M1-only Hölder ceiling .0427. **Prediction FAILED**
  (P(< .035) was .4). The pointwise relation v >= max(0, -u) does not bind: lowering q and reshaping u avoids the M2
  blow-up. Conclusion: a useful joint bound must use the convolution structure linking u and v through the same f, g
  (e.g. at kappa = 1, v = E_K[log2 f(x+w)g(w)] - 2u), not pointwise (u, v) relations. C5-B remains OPEN.
