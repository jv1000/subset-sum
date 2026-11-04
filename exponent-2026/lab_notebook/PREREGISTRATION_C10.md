# C10: joint optimization with amplitude-grouped patterns (pre-registration)
**Written 2026-11-03 ~17:25 ET, before any C10 run.** Jennifer: "Yes please run it."

## Scheme (per region i = 1: W <= Gamma, form R1 = p(Delta - u); i = 2: W > Gamma, form R2 = q(a v - u))
- **Patterns** carry Lambda (the block average of lambda = log2(2 + 2cos x)) as a 4th coordinate.
- **Cutoff:** choose Lambda_c,i with NO realizable sampling pattern of region i above it. Realizable means a point of
  conv{(u, v, lambda)(x)}.
- **Region sets:** region 1 is {U <= Delta, W <= Gamma}; region 2 is {U - aW <= 0, W >= Gamma}.
- **LP-dual certificate of the cutoff:** y >= 0 and z with lambda(x) <= z + y·A(x) for all x, and
  z + y·b <= Lambda_c,i. Here A(x) = (u, v) and b = (Delta, Gamma) for region 1;
  A(x) = (u - a v, -v) and b = (0, -Gamma) for region 2.
- **Below the cutoff:** l = (1 - c3)Lambda_c + R_i + c3 lambda with 0 <= c3 <= 1 dominates (Delta - alpha U) + Lambda,
  because (1 - c3)(Lambda_c - Lambda) >= 0.
- **Moment:** log2 M_i' = (1 - c3_i)Lambda_c,i + log2 mean (2 + 2cos x)^{c3_i} 2^{R_i(x)}.
  c3 = 1 recovers the paper exactly (the cutoff term vanishes).
- **Rounding:** 3p + c3 + 1 <= 30 and q(4a + 3) + c3 + 1 <= 30.

## Run (floating; tau = .4898; N = 512 grid, best point rechecked at N = 1024)
- Maximize Delta over: densities (16 cos + 16 sin each, box 4), kappa in [.5, 2], p, q, c3_1, c3_2, Lambda_c,1,
  Lambda_c,2, and the duals (y, z) per region. SLSQP with JAX Jacobians.
- Starts: our 16+16 optimum (c3 = 1, Lambda_c = max lambda = 2, a feasible dual), plus 3 perturbations.
- **Control:** with c3 fixed at 1 the capacity must reproduce .0291 (within .0003).

## Prediction
P(capacity gain > .001 over .0291) = .3; P(gain > .003) = .1.

## If there is a gain
1. Recheck at N = 1024 and with a finer hull (N = 4096 curve points for the LP).
2. Price it in T, then do a source-level audit of the 4th pattern coordinate (computing Lambda per frequency; the
   pattern count stays 2^{O(sqrt n)}).
3. Certify rigorously; this needs a continuous-curve hull bound, not grid points.

## Amendment 1 (17:35 ET): first run, then tight-dual starts (added before running them)
- Control (c3 = 1): .02908, which reproduces. All 4 free starts returned c3 = 1, Lambda_c ≈ 2, gain 2e-12.
- Likely local: d m / d c3 = -Lambda_c + psi'(1), so a c3 < 1 tilt only pays once Lambda_c < psi'(1) ≈ .57, while
  the starts used the trivial dual (y = 0, z = 2).
- Added: 4 starts with Lambda_c set to the LP hull maximum at the start densities, (y, z) from the LP dual solution,
  and c3 in {.9, .7, .5, .3}.
- **Tight-dual starts:** for c3 in {.9, .7, .5, .3}, every run returned c3 = (1, 1), cutoffs .637–.721, capacity
  .02908. NULL. Prediction P(gain > .001) = .3: no gain.
- **Why (proposition; numerical check c10_prop.py):** at the M1-optimal p, d log M1/dp = Delta - E_t[u] = 0, where E_t
  is the tilt (2+2cos x) 2^{p(Delta-u)}. So the tilted mean pattern lies exactly on the sampling boundary U = Delta.
  Its amplitude is E_t[lambda] = psi'(1). Its rarity is KL(t || U) = .055 bits << eta, so such frequencies occur.
  The hull therefore always reaches amplitude psi'(1) in the sampling closure, and the C9 minimax argument forces
  c3 = 1.
  - Check at our point: E_t u - Delta = -2.7e-9, E_t v = .46036 <= Gamma = .46074, psi' = .5735.
  - M2 analogue: on its boundary to 2e-9, W = .46050 (2.4e-4 below Gamma).
- **Critical pattern:** both tilted means sit at (U, W) ≈ (Delta, Gamma), the corner where the sampling boundary meets
  the case switch. This is consistent with C6's binding slice.
- **Large-deviation form (Donsker–Varadhan):** log2 mean 2^h = max_t (E_t h - KL(t || U)). The moment conditions are
  equivalent to: every frequency type t whose pattern (E_t u, E_t v) lies in the sampling set S satisfies
  E_t[lambda] + phi(E_t u, E_t v) - KL(t || U) <= eta (amplitude + pattern target - rarity <= budget).
  This also matches a direct Sanov count of the MSE. Proof route for the joint bound: for any (f, g, kappa), exhibit
  one type t (e.g. the critical type) that violates it once Delta exceeds the conjectured ≈ .029.
