# Claude's review of Fable round 3 (ROUND3_REPORT.md draft of 08:59 ET, SECTION_T_v2.md)
Written 2026-11-04 ~09:15 ET. This is a co-author's check, NOT the fresh referee: Astra referees Section T tonight
and should not be shown this file first.

## Section T v2: PASS (pending the fresh referee)
- **C_S fix is correct.**
  - T = C_S(m) n^8 ceil(2^{d(M)}).
  - Lemma T5 loses 1/(C_S n^6); Corollary T6 gives e^{-n^2}.
  - Lemma T7 absorbs C_S into 2^{O(n^0.6)}.
  - No numerical condition changes.
- **Independent recomputation of the numbers** (our code, not Fable's):
  - alias constraints recomputed in mpmath from the T.1 formulas: C1R 9.994e-7 (= eps0), C2R 1.300e-6, C3 1.300e-6,
    C4R 1.300e-6, C5R 1.600e-6, MU1 .00932, MU2 .0253, A4R .4587, SR .1030, all PASS;
  - moments recomputed with OUR certify_base.py: log2 M1 = 0.51599187405865778648, log2 M2 = 0.51599162047014794189.
    These agree with Fable's certificate to all 20 printed digits; margins 3.04e-6 and 3.30e-6.
  - T = 0.4873407528 is unchanged.
- **Notes for v3 / the fresh referee:**
  1. Lemma S needs a_t for t in [k, m-k]. Conjecture Q is stated for t in [k, m/2]. This is enough, by the symmetry
     s_t = s_{m-t} (complements), but say so in one line.
  2. If Conjecture Q (k <= m/4) is proved, it gives a_t <= a_k exactly in the needed range, hence C_S = 3 again,
     legitimately. Worth one sentence.
  3. Not checked by me:
     - Lemma T5 step 4 ("Base l.511-523 verbatim", with C(s,k1)C(s,k2) in place of C(s,k)): the residue-hitting
       argument with a product of binomials;
     - Base's core itself.
     The fresh referee should do both.

## Round 3, part A (Conjecture M')
- **Re-derived by hand, correct:**
  - P2: the injection (y, A) -> (w(A), X_y \ A), then the binomial identity;
  - the Cauchy-Schwarz step s_k >= 1/cp(mu);
  - Q_w >= a_t/a_k.
- **Recomputed Q_w with my own exact-fraction code (qw.py)** on Fable's examples:
  - (-3,-3,-2,-2,0,0) at (2,3): Q_w = 1.0357;
  - the m = 8 counterexample at (3,4): Q_w = 1.0788, a_t/a_k = 1.0105;
  - the same counterexample at k = 2 <= m/4: Q_w = 0.790 and 0.740;
  - generic weights: 1.0000.
  All match the report.
- **Reading:** M' is still open. Conjecture Q (k <= m/4) is a clean, witness-free, sharp target with an exact charging
  reformulation (near misses w(L^nm) <= w(R')). This is genuine progress in the formulation, not a proof.

## Round 3, part C (scoping memo)
- Consistent with C16 and paper Sections 9-10: the floor is (1 - Delta)/2, and Delta is the only lever.
- **New and useful:** the "no per-class operation" ceiling of 0.4522, and D5's explanation of the floor as a variance
  floor.
- D2 agrees with paper Section 10: 0.485 needs Delta >= 0.030, the relaxation bound is 0.0382, the Lemma 1 cap is
  0.0415 at tau = .485, and the format saturates at ~0.029. So 0.485 is not excluded, but it needs a new checksum format.

## Suggested paper changes (after Astra's referee)
- State Conjecture Q as the sharp form of M'.
- Cite P2 as the proved 2^k-lossy version (it is exactly Base's Corollary D barrier).
- Add one paragraph on the variance floor and the 0.4522 ceiling.
