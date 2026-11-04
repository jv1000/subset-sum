# C5 result: the M2 question, and a certified-by-Claude point at 0.48946 (2026-11-03)

Labels: FLOATING (exploration), CERTIFIED-C (rigorous ball arithmetic, Claude's code), REFEREE (independent agent;
status at the end), OPEN.

## 1. Is the M1+M2 capacity a family limit or a true limit? (FLOATING)
Joint Delta-capacity at tau = .4898 (largest Delta with both moments < 2^eta):

| Density family | Capacity |
|---|---|
| 6 cosines (control, Astra's family) | .02810 |
| 6 cos + 6 sin, box 4, kappa in [.5, 2] | .02841 |
| 16 cos + 16 sin / 32 cos + 32 sin (Astra-basin starts) | .02864 / .02864 |
| 16 cos, random starts | .02900 |
| **16 cos + 16 sin, random starts** | **.02908** |
| M2 alone (6 cos) | .03226, limited by the rounding cap q_m(4a+3) <= 30 |
| M1 alone (6 cos) | .0396 (proved Hölder ceiling .0427) |

Capacity saturates near .029 whatever the family. So the limit looks structural to the M1+M2 moment format; the extra
freedom (asymmetric densities, more terms) buys about +.001.

## 2. That +.001 is worth having: a K = 16 point at T = .4894615727 (CERTIFIED-C; REFEREE: CONFIRMED)
- Full constraint search with the best 16+16-term densities: K = 17 reaches .4895157 (the 17-block floor itself; the
  moments stop binding), **K = 16 reaches .4894611**, K = 15 .4894858. Control: K = 17 with Astra's 6-term densities
  reproduces .4897734.
- Frozen with explicit slack as exact decimals (`candidate_K16.json`): K = 16, mu .0593373017, eta .5184804040,
  tau .4894613727, gamma .4888978551, kappa 1.03489429, p 8.38520435, q_m 8.19573911, 64 coefficients.
- `certify_c5.py` (python-flint arb, 200 bits; trapezoid strip bounds; Route A strip argument extended to sine terms):
  log2 M1 = .518477576190, log2 M2 = .518477347232 (radii < 1e-20; quadrature errors < 1e-27), against
  rho_c = .5184786...; **all 20 interval margins positive** (moment margins 8.48e-7 and 1.08e-6).
  Controls: Astra's certified point passes its own threshold; a Delta + .001 perturbation is rejected; doubled inner
  resolution agrees to 20 digits.
- **Leading exponent .4894615727, 3.12e-4 below Astra's certified .4897736**, and below the unchanged-17-block floor
  .4895157 (because it uses 16 blocks).
- Conditional, like everything in this line: on the OpenAI paper's own proof, on the K-generalization (AUDIT_K8.md),
  on c0 = .0001 (Astra's documented useful-block variant), and on asymmetric densities being admissible (filtering.tex
  allows any strictly positive continuous densities). As for the paper's own point, the bound is 2^{(T+o(1))n}.

## 3. Why ~.029? (OPEN; a lead, not a proof)
- At kappa = 1, v = E_K[log2(f(x+w) g(w))] - 2u exactly, with u = log2 Q.
- For indicator-like densities (f = g = uniform on a set of measure s), v = 2(KL(f) - u) exactly. Then M2 acts like a
  second M1-type constraint with effective gap 2a·KL(f)/(1 + 2a) and multiplier q_m(1 + 2a). Peaked densities help M1
  (large u) but raise KL(f), which hurts M2. That tension is what a joint bound would have to capture.
- A proved joint lower bound would turn ".029 looks structural" into a theorem, and it would be the natural partner to
  the M1 Hölder lemma in the paper.

## Referee verdict on the K = 16 point (independent agent; it read only candidate_K16.json and the OpenAI TeX)
**Could not break it.** Scripts are in `referee2/`.
- **Constraint list:** derived independently from the TeX, every line cited. No missing or violated constraint. It
  also checked the conditions that hold by construction: the Markov step, B >= 2^{gamma m}, the Chebyshev gap, the
  error exponent and the finite-circle slack. All margins are positive in arb.
- **Moments, its own rigorous certifier:** exact-ball DFT with aliasing and tail bounds; strip of half-width .2 with
  Re P >= .706. log2 M1 <= .5184775761896887 and log2 M2 <= .5184773472319414, at N = 1024 and 2048. This matches
  certify_c5.py exactly. Floating checks at N = 128 to 4096 agree.
- **Points the paper must state:**
  - **Orientation convention.** With asymmetric densities the point passes under the paper's correlation convention
    (y − θ = x + w, P(x) = mean_w F(x+w)G(w)). Reflecting one density (convolution) gives log2 M ≈ 3.28, a
    catastrophic failure. Swapping f and g, or x -> −x, is harmless.
  - **Lost symmetry.** The appendix's j <-> 64−j symmetry no longer holds, so the numerical appendix must be replaced
    (the referee's or our certifier works).
  - **Exponent statement.** What is proved is O(2^{T'n}) for every T' > .4894615727, e.g. 2^{.4894616 n}, not
    literally 2^{.4894615727 n}: the 2^{O(sqrt n)} poly factors need a strict gap.
  - **Thin slacks.** They only push the cutoff n_* astronomically high; nothing breaks asymptotically.
  - **K = 16 is a genuine tradeoff.** mu = .0593 > 1/17, so 17 blocks are infeasible at this mu.
- **Minor:** the floating_margins in the JSON are ~3e-11 (scalar) and ~2.6e-10 (moments) larger than at the
  published decimals, because they were computed before the final rounding. The interval margins from both
  certifiers are the authoritative ones.

## Next
1. Write the K = 16 adaptation at source level for the paper, with the orientation convention explicit. The
   numerical appendix is replaced by the two certifiers.
2. The joint M1+M2 bound (section 3), and only then larger searches.
