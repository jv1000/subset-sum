# A1 pre-registration (induction route), written before running lemmaE_test.py
Prediction: (i) the averaged "core inequality" (k+1) S_{k+1} <= m s_k + (m-k-1) S_k holds on all instances (m<=14),
(ii) "Lemma E" (some e with (k+1) n_e^{k+1} <= s_k + (m-k-1) n_e^{k}) holds on all instances, and (iii) the rule
"e in a value class of maximum multiplicity" works in >= 95% of instances but not all.
Control: generic distinct weights give equality in (i) and in Lemma E for every e (D = 0 everywhere).

## Result of lemmaE_test.py (6562 (instance,k) pairs, m = 6..14, k+1 <= m/2)
- identity D_k(M) = D_k(M\e) - s_k + (k+1) n_e^{k+1} - (m-k-1) n_e^{k}: exact in every case (PROVED anyway).
- core inequality: 0 violations.  Lemma E: 0 violations.  Prediction (i),(ii) HELD.
- Prediction (iii) FAILED in the good direction: every rule works because the inequality holds for EVERY e
  ('all': 0 failures).  New target, stronger and cleaner:
  **Defect monotonicity (DM):  D_k(M) <= D_k(M \ e)  for every e in M, whenever k+1 <= |M|/2.**
  DM + complement symmetry (D_k(M0) = 0 for |M0| = 2k+1) => a_k >= a_{k+1} for all k+1 <= m/2.

# A2 pre-registration (written before dm_evidence.py)
Prediction: DM holds for all k with k+1 <= m/2 at m <= 16 (classes DP) including adversarial hill-climbing on
Phi_e = (k+1) n_e^{k+1} - (m-k-1) n_e^{k} - s_k (maximize), and also for k+1 <= (m+1)/2; it FAILS for some
k > m/2 (where the defect is >= 0 by symmetry and need not be monotone).  Control: generic weights give Phi_e = 0.

## Result of dm_evidence.py
families: 10199 in-range (k+1 <= m/2) tests, 0 violations, max Phi = 0 (generic instances are tight); beyond the middle
8323/11284 violations (as predicted: no DM there).  Hill-climb (m = 10,12,14): max Phi = 0.  Prediction A2 HELD.

# A3 pre-registration (written before group_probe.py)
Question: do monotonicity and DM depend on the integers, or only on the lifting property of sum-equivalence
(A ~ A' => A u g ~ A' u g)?  Test weights in finite abelian groups Z_q (q=2..9) and Z_2^2, Z_2^3, Z_3^2.
Prediction: monotonicity a_k >= a_{k+1} (k+1 <= m/2) still holds in every group (P = .6); DM also (P = .5).
Control: Z_q with q huge reproduces the integer results.

## Result of group_probe.py (A3)
0 violations of monotonicity and of DM in Z_2..Z_9, Z_2^2, Z_2^3, Z_3^2 (1098 tests each) and the Z_{10^6} control.
Prediction HELD (both). Consequence for the proof: it must not use the order of the integers; only the lifting
property A ~ A' => A u g ~ A' u g (and its dual) of sum-equivalence.

# A4 pre-registration (written before hall_probe.py)
Question: does Hall's condition hold for the bipartite graph between (k+1)-fibers (demand k+1) and k-fibers
(capacity m-k)?  G1: y ~ x iff x = y - w_g for some g in U(y) (witness-compatible).  G2: y ~ x iff y - x is a weight value.
Prediction: Hall holds for G2 in all small instances (P = .7); it FAILS for G1 in some structured instance (P = .5),
because the uniform flow already fails per-fiber (three-equal example). Control: generic weights (Hall trivially holds
with the set-level LYM counting).

## Result of hall_probe.py (A4)
1176 (instance,k) pairs, all subsets Y when s_{k+1} <= 18: Hall holds for BOTH G1 and G2, min slack 0 at the two-valued
sharp case. Prediction for G1 FAILED (good direction): a fractional flow from (k+1)-fibers (demand k+1) to k-fibers
(capacity m-k) exists in the witness-compatible graph, although neither uniform flow (per y: N(y,x)/f(y); per x:
N(y,x)/f(x)) satisfies the constraints.

# C pre-registration (written before c_hunt.py)
Monotonicity a_k >= a_{k+1}, k+1 <= m/2, at m = 16..22 on structured families (sumsets, multi-valued, +/- mixtures,
low rank, APs with gaps, geometric, products of small gadgets), numpy enumeration, capped at ~20 minutes.
Prediction: no violation; minimum ratio exactly 1 at two-valued weights with k = m/2 - 1 (and at generic weights).
Control: generic random large weights give ratio exactly 1 at every k.

# A5 pre-registration (written before dm_exhaustive.py)
DM depends only on the multiset of values. Check DM and monotonicity EXHAUSTIVELY over all value multisets with
(a) integer values in [-3,3], m = 4..12; (b) values in Z_q, q = 2..7, m = 4..12; (c) integer values in [-6,6], m = 4..9.
Prediction: zero violations in all three; the number of tight cases (max_e Phi_e = 0) is a sizeable fraction (>= 20%).
Control: generic-like instances (all values distinct, e.g. {-3,..,3} itself at m = 7) must be tight at every k.

## Result of dm_exhaustive.py / dm_violations.py (A5/A6): COUNTEREXAMPLES
- [-3,3], m<=12 and Z_q (q<=7), m<=12: 0 violations of anything (prediction held there).
- [-6,6], m<=9 (496860 multisets): DM (per-element) FAILS in 23 instances (first: (-6,-5,-2,-1,0,3,4), k=2, e of
  weight -1: Phi = 3*6 - 4*0 - 13 = +5), and EXACT MONOTONICITY a_k >= a_{k+1} FAILS in 16 instances, all at m = 8,
  k = 3 = m/2 - 1 (the middle step): e.g. w = (-6,-5,-5,-3,-3,-2,4,5): s = (1,6,14,19,24,19,14,6,1), 5*19 = 95 < 4*24 = 96,
  a_3 = 19/56 < a_4 = 24/70.  Verified by brute force (itertools).  Prediction A5 FAILED.
- Lesson logged: the earlier "0 violations" (10199 family tests, hill-climb, m<=16) were not adversarial enough; the
  counterexamples need 2-3 repeated values plus 2 large values, and show up only in an exhaustive sweep.
- Consequence: the induction route (DM) is dead; exact monotonicity is dead at the middle step; the weak form
  a_t <= poly(m) a_k (t in [k, m-k]) is what remains and is what [S] needs.

# A7 pre-registration (written before mono_ratio_sweep.py)
Exhaustive [-6,6] at m = 10 and 11 (and random cluster+large instances m = 10..14), tracking
 r_mid = min a_{m/2-1}/a_{m/2} (middle step, even m), r_int = min over interior steps k+1 < m/2 of a_k/a_{k+1},
 R = max over k <= m/4, t in [k, m-k] of a_t/a_k, and the [S] quantity q = min over k <= m/4 of a_k 2^{d(M)} (m+1).
Prediction: r_int = 1 (no interior violation, P = .6); r_mid < 1 again with ratio >= 0.97; R <= 1.05; q >= 1.

## Result of mono_ratio_sweep.py (A7)
[-6,6] exhaustive at m = 10 (646646) and m = 11 (1998724): NO violations; min middle ratio 1.0 (two-valued), min
interior ratio 1.126; max a_t/a_k over t in [k, m-k], k <= m/4: exactly 1.0; min a_k 2^d (m+1) = 20.9.
Random cluster+large m = 10..14: nothing. Prediction A7: r_int = 1 held, r_mid < 1 FAILED (no middle violation at m = 10),
R <= 1.05 held (R = 1), q >= 1 held.

# A8 pre-registration (written before mono_wide.py)
(1) Exhaustive m = 8 and 9 in [-8,8]: prediction: middle-step violations at m = 8 with min ratio >= 0.97; at m = 9
(no exact middle) no violation (P = .6). (2) Structured random search m = 10..16, values = cluster in [0,8] with
repeats + 2..4 large values in [12,40]: prediction: violations only at the middle step k+1 = m/2 for even m, ratio
>= 0.97; max_t a_t/a_k = 1 for k <= m/4.  Control: two-valued gives middle ratio exactly 1.

## Result of mono_wide.py (A8)
[-8,8] exhaustive: m = 8: 735471 multisets, 130 violations, all at k = 3 (middle), min ratio 90/92 = 0.97826
(e.g. (-8,-6,-6,-2,-2,0,1,3), s = 1,6,14,18,23,...); m = 9: 2042975 multisets, 0 violations. Structured cluster+large
m = 10..16: 0 violations, max a_t/a_k (k <= m/4) = 1.000. Prediction A8 HELD (both parts).

# A9 pre-registration (written before mono_m10_m12.py)
Exhaustive middle-step check at m = 10 in [-8,8] (C(26,10) = 5.3M) and m = 12 in [-6,6] (C(24,12) = 2.7M), sizes only.
Prediction: violations exist at m = 10 or 12 at the middle step with ratio >= 0.97 (P = .5); none strictly inside
(P = .85). Control: two-valued gives ratio exactly 1 at the middle.

## Result of mono_m10_m12.py (A9)
m = 10 in [-8,8] (5311735 multisets): 0 violations, min middle ratio 1.0 (two-valued), min interior 1.21.
m = 12 in [-6,6] (2704156): 0 violations, min middle ratio 1.0, min interior 1.24.
Prediction "violations at m = 10 or 12" FAILED (none); "none strictly inside" HELD. All known violations are at m = 8.
