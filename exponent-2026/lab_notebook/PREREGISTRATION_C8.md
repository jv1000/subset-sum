# C8: the kappa = 1 problem — Euler–Lagrange equations and an SOR solver (pre-registration)
**Written 2026-11-03 ~17:35 ET, before any C8 run.** Jennifer: "Yes please" (Euler–Lagrange at kappa = 1).

## Logged first (a failed guess)
I had guessed from the coefficients that our optimum has g = f shifted by pi. A direct test over all shifts and
reflections finds no such relation: the best match has rms difference .920, against rms(s) = .940. The guess fails.

## The kappa = 1 problem (exact, no relaxation)
Natural logs, normalized measure. Q(x) = ∫ f(x+w) g(w) dw, Phi(x) = ∫ f(x+w) g(w) ln(f(x+w) g(w)) dw,
D(x) = Phi/Q - ln Q (nats), u = ln Q / ln 2, v = D/ln2 - u.
M1 = 2^{p Delta} ∫ 2w Q^{-p} and M2 = ∫ 2w e^{c D} Q^{-s}, with w = 1 + cos x, c = q a, s = q(1+a).
Capacity: max Delta s.t. log2 M1, log2 M2 <= tau + Delta. At fixed (p, q, Delta), the pair minimizes
L = lam ln M1 + (1 - lam) ln M2, with lam chosen so that M1 = M2.

## Euler–Lagrange (first variation in f; g is symmetric)
- dQ(x)/df(y) = g(y-x)
- dD(x)/df(y) = (g(y-x)/Q(x)) [ln(f(y) g(y-x)) - Phi(x)/Q(x)]
- dM1/df(y) = -p 2^{p Delta} ∫ 2w Q^{-p-1} g(y-x) dx
- dM2/df(y) = ∫ 2w e^{cD} Q^{-s-1} g(y-x) [c (ln f(y) + ln g(y-x) - Phi/Q) - s] dx
- Stationarity: lam dM1/M1 + (1-lam) dM2/M2 = mu_f for all y (mu_f is the multiplier of ∫f = 1).
- This is linear in ln f(y): B(y) ln f(y) + A(y) = mu_f, with
  B(y) = (1-lam) c ∫ 2w e^{cD} Q^{-s-1} g(y-x) dx / M2 > 0.
  So the fixed point is ln f(y) = (mu_f - A(y))/B(y). Damped alternating updates of f and g form an SOR iteration.

## Experiments (floating; tau = .4898; N = 1024 grid)
- **C8-A:** kappa = 1 capacity, log-densities as trig polynomials of degree 24 (cos + sin), JAX gradients, SLSQP.
  Starts: our 16+16 optimum (kappa set to 1) and 3 random. Prediction: .0287–.0291 (kappa ≈ 1.03 at the free optimum).
- **C8-B (derivation check):** the hand-written variations above must match JAX gradients of M1, M2 with respect to
  the grid values f(y), g(y). Pass: max relative difference < 1e-6.
- **C8-C:** the EL residual at the C8-A optimum. Report the spread of lam dM1/M1 + (1 - lam) dM2/M2 over y,
  relative to its mean. Small means stationary within the family; any structure shows what the trig family misses.
- **C8-D (SOR, nonparametric):** starting from the C8-A optimum on the grid, run damped SOR on the EL fixed point at
  fixed (p, q). Bisect Delta for capacity. 10 min cap. Prediction: gain < .0005 over C8-A (C5 showed saturation);
  P(gain > .001) = .15.

## Results part 1 (17:50 ET), floating
- C8-A: kappa = 1 capacity .02854, identical from all 4 starts (p 8.725, q 8.550). Prediction ".0287–.0291" missed
  slightly low; the free-kappa optimum (kappa ≈ 1.035) is worth about +.0005.
- C8-B PASS: the hand-written first variations match JAX gradients to 5.3e-16 (relative).
- C8-C: the EL residual at the C8-A optimum has f-weighted relative spread 2.2e-5 (lam .385). The trig optimum
  nearly satisfies the full nonparametric stationarity condition.
- **C8-D FAILURE (bug, logged):** every SOR step returned NaN. The mu bracket ±1e3 overflowed exp((mu - A)/B), so
  the run is void. Kept as c8_v1_nanbug.*. Fix: log-space bracket with logsumexp normalization and clipped
  exponents. A/B/C are not rerun (reused from v1); D is rerun.
- **C8-D second failure (logged):** after the overflow fix the SOR still produced NaN. It DIVERGED: one sweep moved
  log2 M from .518 to (.531, .522), and two sweeps reached (46.6, 50.9). Causes: (1) the start-up rule set lam = .9
  (M1-weighted), which drives the densities toward peaked shapes, the concentration mechanism; (2) step omega = .3
  with no safeguard; the EL fixed point is not a contraction. v2 kept as c8_v2_diverge.py.
- **Fix (before rerunning):** lam starts at the C8-C stationary value .385 and adapts slowly. Each sweep is accepted
  only if max(log2 M1, log2 M2) decreases; otherwise omega is halved (backtracking line search).
- **C8-D result (v3, backtracking SOR):** stable. M1 and M2 are balanced to 6 digits at every Delta, but there is no
  improvement over C8-A. At Delta = .02854: log2 M = .518376 vs eta .518345, with p, q fixed at C8-A's values.
  Capacity gain = 0. Prediction "gain < .0005" HELD.
- **Conclusion (floating, evidence not proof):** the kappa = 1 problem is exact, and its trig-24 optimum (.02854)
  nearly satisfies the full nonparametric EL equations (spread 2.2e-5). A safeguarded nonparametric SOR cannot
  improve it, and 4/4 starts agree. With kappa free the capacity is .0291 (C5).
- **Conjecture:** the joint capacity of the M1+M2 format is ≈ .029 for all densities. By the price list, the
  architecture's floor is then ≈ .48946, essentially the certified .4894616 point (which sits at the
  optimistic-closure floor up to its explicit slack).
- **Still open for rigor:** global optimality (second-order and basin analysis) and a certificate.
