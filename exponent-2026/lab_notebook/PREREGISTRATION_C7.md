# C7: toward a joint M1+M2 bound — the concentration mechanism and a Bhattacharyya relaxation (pre-registration)
**Written 2026-11-03 ~17:00 ET, before any C7 run.** Jennifer: "Yes please" (the slice lemma).
Background: C6 showed the binding patterns sit at W = Gamma, where the optimal forms are the paper's own. So a slice
lemma for one form reduces to Lemma 1 (capacity .0427). The joint limit (~.029) must come from the SAME densities
serving M1 and M2.

## Mechanism (hypothesis)
Lemma 1 is tight only for concentrated densities. Concentration makes K_x concentrated, so D(x) = KL(K_x || U) and
v = (D - A) + (D - E) are large. M2 carries 2^{q a v}, so it blows up.

## Provable coupling (sketch, all kappa; to be checked)
With a := f*, b := g* (normalized powers), K_x(w) = f(x+w)g(w)/Q(x) and K*_x(w) = a(x+w) b(w)/Q*(x):
- (i) u = log2 Q*(x) - KL(K_x || K*_x) <= log2 Q*(x), with Q* = a ⋆ b (correlation), a probability density.
- (ii) v = KL(K_x || a(x+.)) + KL(K_x || b) >= min over densities k of [KL(k || a(x+.)) + KL(k || b)]
  = -2 log2 BC(x), where BC(x) = mean_w sqrt(a(x+w) b(w)), attained at k ∝ sqrt(ab).
- Hence M1 >= M1' := 2^{1 + p Delta} mean_w Q*^{-p} and M2 >= M2' := 2 mean_w BC^{-2 q a} Q*^{-q}
  (w = 1 + cos x; q a >= 0).
- kappa disappears: the relaxation is a problem over ONE pair of densities (a, b). Its capacity is a valid upper
  bound on the true joint capacity, provided the optimization over (a, b) is global (it is not, in this exploratory
  run). It lies at or below Lemma 1's .0427 automatically.

## Experiments (floating; tau = .4898)
- **C7-A (mechanism):** at the M1-only optimum densities (C4-cap, kappa -> 1), evaluate M2 at its best admissible
  q_m and report mean_w v, mean_w D. At the joint optimum (our 16+16), report the same.
- **C7-B0 (validity control):** at our 16+16 densities and at Astra's, M1' <= M1 and M2' <= M2 (inequality check).
- **C7-B (relaxed capacity):** maximize Delta over (log2 a, log2 b) = trig polynomials of degree 24 (cos + sin,
  box [-6, 6]), p in [1, 10], q_m in [1, 30/(4a+3)], with exact JAX gradients, N = 1024. Starts: f*, g* of our
  16+16 optimum and of Astra's; 4 random. Rechecked at N = 2048.

## Predictions
- C7-A: at the M1-only densities, log2 M2 exceeds eta by > 0.1 bit, with mean_w v well above Gamma.
- C7-B0 holds (it must; a failure means an error in the derivation).
- C7-B capacity lies in [.0291, .0427]. P(< .035) = 0.45. If it lands near .029–.032, the coupling captures the
  mechanism and the rigorous route is a dual certificate for this two-density problem.

## Results (2026-11-03 ~17:15 ET), floating
- **C7-A mechanism CONFIRMED:**
  - At the M1-only optimum (kappa 1.0001, p 5.07, Delta .03959), log2 M1 = .52938 (= eta), but the best admissible
    q_m = 1 gives log2 M2 = 1.0163, which is .487 bit above eta.
  - There, E_w v = 2.18 and E_w D = 2.37, against Gamma = .450 (v ranges over [1.95, 3.64]).
  - At the joint optima, E_w v = .423 (ours) and .427 (Astra's), close to Gamma.
  - Prediction "M2 > eta by > .1 bit, E_w v >> Gamma" HELD.
- **C7-B0 validity PASS:** relaxed <= true at all three points. Ours: M1' .51502 <= .51882, M2' .41116 <= .51866.
  Astra's: .51461 <= .51789, .41462 <= .51788. M1-only point: .52938 <= .52938, .95975 <= 1.01627.
- **C7-B relaxed capacity:**
  - Starts k16 / astra / rand0–3: .03822 / .03766 / .03814 / .03823 / .03815 / .03821; best **.03823**.
  - The optimum sits at p ≈ 6.09, q ≈ 5.78.
  - Prediction P(< .035) = .45: not met; the result lies in the predicted bracket [.0291, .0427].
- **Interpretation:** K_x ∝ (a b)^{1/kappa}, so the Bhattacharyya minimizer k ∝ sqrt(ab) is what kappa = 2 produces.
  The relaxation lets u use kappa = 1 (Jensen tight) and v use kappa = 2 (Bhattacharyya tight) at once. The true
  problem uses ONE kappa; that single-kappa coupling accounts for .0382 -> .029.
- **Bracket on the joint capacity at tau = .4898:**
  - .029: achieved by nonparametric search (lower estimate);
  - <= .0382: relaxation, floating, nonconvex search, not certified;
  - <= .0427: Lemma 1, rigorous.
  - Via the price list: T >= ~.4864 (relaxation, if made rigorous) or T >= ~.4847 (Lemma 1), against the achieved
    .4894616. All of these are floating floors.
- **Next:** a rigorous version needs either global optimality for the two-density problem, or an inequality that
  keeps the kappa coupling. One route: at kappa = 1 the problem in (a, b) is exact (u = log2 Q, v = E_K log2(ab) - 2u);
  study its Euler–Lagrange equations, then perturb in kappa.
