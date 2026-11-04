# C12: going below JoshuaQFEX 0.487676 inside Base's construction (pre-registration)
**Written 2026-11-03 ~18:15 ET, before any C12 run.** Jennifer: "can we get to joshuaQFEX to understand what they did
then try to go below."

## What they did (read from the cloned repos; reading, not verification)
- **JoshuaQFEX** (subset-sum-bound @ bed8e18): retunes Base's (tau, eta) to (.48767595, .51612858) and transfers the
  430 certificates via a transfer lemma; displayed exponent .487676. Lean formalization of the finite data.
  Conditional on Base's continuous moments (certified by us in C2) and on the written lemmas.
- **Base** (a-kapila/maths-proofs, PROOF_0.4877.tex @ 44c34961). Relative to OpenAI it:
  - uses ONE large block |M| ≈ .473n with sparse masks (a = .0082);
  - returns alias PHASE SUMS (no listing), with trials repeated about 2^{F-hat} times;
  - replaces the 17-block Markov step by an averaged small-layer Corollary D;
  - uses alias constraints C1–C8 on (tau0, eta, mu, a, gamma, l), tight to 5.4e-6 (C4);
  - uses a checksum with J = 43 filters, each 8 cosine terms (symmetric) with kappa_v in [1.024, 1.064]. The pattern
    chooses the filter maximizing U; certificates live in 10 W-regions with comparison rows u_v - u_l.
  - Budget: tau0 = eta - Delta with Delta = .02844 certified at eta = .51613 (margin .00025).
  - Base §8.4: "At tau0 = 0.4876 the cutting-plane search for filters stalls at a log2 margin of -0.0015.
    Further progress needs a new idea."
- **Our new ideas the Base search never tried:** asymmetric (sine) terms and more harmonics. On a single filter they
  added about +.001 of capacity (C5).

## C12-A (floating): price of moment capacity in Base's budget
- **Model:** minimize tau0 over (eta, mu, a, gamma, l) subject to (C1)–(C8), all strict with slack >= 1e-6, and
  eta - tau0 <= Delta_cap(tau0).
- **Capacity:** Delta_cap(tau0) = .02844 + s (tau0 - .48769) + delta. The slope s = .166 is estimated from our
  single-filter data (.0281 at .4898, .02747 at .486).
- **Control:** delta = 0 must return tau0 ≈ .48769 (Base) or slightly lower (JoshuaQFEX found .48767595 by retuning).
- **Runs:** delta in {.0005, .001, .0015, .002}. Report tau0*(delta), and the slope dT/d delta.
- **Prediction:** the slope is between -.3 and -.6; delta = .001 gives tau0 about .4874 ± .0002, i.e. below .487676.

## C12-B (next, only if A is favourable)
Measure the capacity at tau0 ≈ .4874 of (i) one asymmetric 16+16 filter and (ii) a small asymmetric family with
Base's region/comparison certificate format. Then freeze, certify and referee as in C5.

## C12-A result (18:20 ET), floating
- Control (delta = 0): tau0* = .4876826 (JoshuaQFEX .48767595, Base .48769). PASS within 7e-6; the slack model
  (1e-6) explains the difference.
- delta .0005 / .001 / .0015 / .002 -> tau0* .4874876 / .4872929 / .4870983 / .4869039. **Price -0.389 per unit of
  capacity.** Prediction "slope -.3 to -.6, delta = .001 -> ~.4874" HELD (.48729).

## C12-B plan (pre-registered here before running)
- With J = 1 filter, Base's Theorem B reduces exactly to OpenAI's checksum (the two moments M1, M2).
- Full joint floating optimization: minimize tau0 over Base's alias parameters (eta, mu, a, gamma, l), one filter
  (16 cos + 16 sin each for r and s, box 4, kappa in [.5, 2]) and p, q. Constraints: C1–C8 (slack 1e-6) and
  log2 M1, M2 <= eta - 3e-6, with 3p <= 30 and q(4a_Gamma + 3) <= 30.
- Starts: our 16+16 densities and Base's alias point; 3 perturbed. N = 512, rechecked at 1024.
- **Prediction:** a single asymmetric filter reaches tau0 ≈ .48757 ± .0001 (capacity about +.0003 over Base's
  43-filter family at that tau). P(T < .487676) = .65.

## C12-B result (18:35 ET), floating
- 4/4 starts: tau0 = .4875749, T = .4875751 (eps = 1e-8), which is 1.01e-4 below JoshuaQFEX .48767595.
  Delta .02870, eta .51627, mu .4752, kappa 1.035. Active constraints: C1–C5, M1, M2.
- Prediction ".48757 ± .0001; P(T < .487676) = .65" HELD.
- Resolution check: the same point at N = 512 / 1024 / 2048 has all margins equal to ~1e-14.
- **Additional constraint found while reading Base:** Lemma A5 step 3 needs 1/2 - tau0 + zeta < delta
  = (eta - (mu/2) log2 3)/2. At the point: .0124 < .0698.
- **Base's free constants:** eps, zeta and the input guard; JoshuaQFEX used 1e-11. Freeze with eps = 1e-8 (T = tau0 + 2e-7),
  zeta = 1e-8, guard 10^8 (b <= 2^{n/10^8}), requiring least alias slack eps0 > zeta + 1e-8.
- **Certificate format with J = 1:** rho0 uses z = (p, 0) with p >= 1; rho1..rho9 use z = (q, 0, 0) with q b_{i-1} >= 1.
  So the 10 certificates are two integrals, M1 and M2.
  Lemma B3 needs m_f > (18 + 6 max(p, q)) eps ≈ 6.9e-7. Freeze rule: rho_f = eta - 1.5e-6, rho_c = rho_f - 1e-6.

## C12-C: freeze and rigorous certificate (18:45 ET)
- Pre-registered pass rule (same as C5): every ball margin > 0, including both moments with quadrature errors;
  doubled resolution agrees; an independent referee confirms.
- freeze_base.py -> candidate_base.json: tau0 .4875752036, T = tau0 + 2e-7 = .4875754036; eta .5162721413,
  mu .4752421539, a .0082379228, gamma .0605824120, l .4836347962, kappa 1.03465831, p 8.45902160, q_m 8.27015425,
  64 coefficients (16 cos + 16 sin each), zeta 1e-8, guard 10^8.
- certify_base.py (arb 200 bits; moments via certify_c5.build/moments): **all 25 margins positive**.
  - C1–C5 about 1.3157e-6 each; eps0 1.3157e-6 > zeta + 1/guard.
  - A5 delta condition .0574; S3 .854; B3 8.1e-7.
  - M1 1.3154e-6 and M2 1.4940e-6 below 2^{rho_c}.
  - log2 M1 = .51626832585 and log2 M2 = .51626814726 (radius < 3e-21). Inner errors ~1e-27.
  - Doubled resolution (N_in 512, sigma .25) identical to 20 digits.
- **T = .4875754036: 1.005e-4 below JoshuaQFEX (.48767595), 1.15e-4 below Base's tau0 .48769**, with ONE filter
  in place of 43.
- Status: CERTIFIED-C (Claude). Independent referee launched (reads only the candidate, Base TeX and OpenAI TeX).
  Conditional, like Base and JoshuaQFEX, on Base's written proof (Theorem A cost accounting, Lemma A5, the checksum
  changes) and on the OpenAI paper.

## C12-C referee verdict (2026-11-03 ~17:40 ET): CONFIRMED (full report: referee3/REFEREE3_VERDICT.md)
- **Independent referee 3** (sources only):
  - Every numerical premise holds at the JSON decimals.
  - Its own rigorous M1 and M2 (rig_M.py) agree with ours to 20 digits.
  - J = 1 and sine terms are legitimate instances of Base's Theorem B and the paper's Lemma 3.2.
  - No fatal issue.
- **Mistake logged:** Claude's certificate omitted several conditions that the referee derived:
  - Lemma A7 items 1, 3 and 4 (l.556–564);
  - S2 and S5;
  - the prime draw η/2 < τ0;
  - the B2 row-error condition a_Γ ≤ 3/4.

  They were added to certify_base.py and rerun (cert_base_256_v2.json): **all 34 margins positive**. The new ones are slack. The tightest margins are unchanged: B3 8.1e-7, eps0 cap 1.30e-6, M1 1.315e-6, C4 1.316e-6.
- **Text changes needed for a write-up** (constants, the δ > .0706 claim, sine-term filter definition, D.2 script): listed in the verdict.
- **Status: CERTIFIED + REFEREED.** T = 0.4875754036, 1.005e-4 below JoshuaQFEX. Like Base and JoshuaQFEX, it is conditional on Base's written proof and on the OpenAI paper.
