# Claude's review of Astra round 6, Part B (YP_HALL_K1_ASTRA.md) and summary
Written 2026-11-04 ~22:35 ET.

## New theorem: YP-Hall (hence Q_w(2,1) ≤ 1) at k = 1, t = 2, all integer weights, m ≥ 4 — CHECKED, correct
Hand check, line by line:
- Reductions (supply S_p, cap(Y), identity Σ S − Σ cap = Σ_c M_c(M_c − C), class-union cuts by submodularity): match
  Fable round 5 (R1)-(R3); re-derived, correct.
- Proof 1 (flow). At t = 2 every near miss lives on a same-class pair X = {p,p′}; total source 2N_c/f_c,
  cap(X) = 2N_c(f_c − n_c + 1)/f_c, so local service works iff f_c ≥ n_c, true for n_c ≥ 3 (f_c ≥ C(n_c,2)) and for
  pairs with f_c ≥ 2. Residual = isolated pairs (n_c = 2, f_c = 1), demand N_c per element, using only untouched
  cross-class sets. Cuts: (i) ≥ 2 isolated pairs: f ≥ 4 on the 4 cross sets per class pair, cap ≥ (N_c+N_d)/2,
  total 2(q−1)Σ N_c ≥ demand; (ii) one isolated pair + another repeated class d: f ≥ 2n_d, first term alone gives
  2(n_d − 1)N_c ≥ 2N_c; (iii) one isolated pair + G ≥ 2 distinct singletons: N_0 = 1 + Σ 1/f_i ≤ (G+2)/2,
  s ≥ G + 2 (extreme same-sign pair, or g1+g2 ∉ {0,g1,g2} by isolation), K/2 ≥ s + N_0(G+1−2N_0) ≥ N_0. All steps
  verified. Correct.
- Proof 2 (direct, no flow). Orbit/fiber bound gives M_c ≤ r − 1 (singleton), ≤ r + 1 (repeated); h = m − r ∈ {0} or
  ≥ 2 ⟹ every M_c ≤ C = m − 1; h = 1 ⟹ one pair, and M_0 > C forces a unique pair sum, then
  Σ_i M_i(C − M_i) ≥ 2s − M_0 ≥ 2(G+2) − M_0 ≥ M_0(M_0 − C) since G+1 < M_0 ≤ G+2. Verified. Correct, and short —
  this is the one to put in the paper.
- Computational check (PREREG_QW_T2K1.md, qw_t2k1_check.py, Claude's code from the definition): 59,408 instances,
  max exactly 1, M_c lemma never fails, control 29/28. Agrees.
- Relevance: this is the base case t = 2 of k = 1 only. The application needs k ≈ 0.007m → ∞, so it does not move [S]
  materially; it is honest progress on the base case and shows the k = 1 obstruction is a t ≥ 3 phenomenon.

## Other Part B content (assessed, not re-proved)
- Residual-Hall (CONJECTURE): after local reservations, every residual source is a full-class low-multiplicity fiber
  (orbit bound: 0 < j_c < n_c ⟹ orbit ≥ n_c) — the orbit step is correct; the conjecture is a sufficient route only.
  The (0,0,1,4,16,64), t = 3 instance (Q = 14/15) shows per-fiber bounds fail; consistent with Fable's B.4 obstruction 2.
- Profile-subfamily inequality (CONJECTURE, weight-free, stronger than Q_w(t,1)): convexity ⟹ vertex reduction is
  correct. 3.6M subset checks, no violation. New route; worth giving to Fable as a target.
- Spectral shortcut fails at n = (2,1,1) with a rational certificate: an obstruction to a proof strategy, not to Q.
- Astra's search: 3,371 actual-weight cases, no failure of Q, YP-Hall, Residual-Hall or Fable's Prop-1.

## Summary file
Consistent with Parts A and B. Its own blindness disclosure matches REGISTER.md. Final check: 43 scalar checks
(SCALAR_SLACKS.md regenerated 03:04 UTC — the C1R..B3 values I compared are unchanged), exact threshold
609175941/1250000000 = 0.4873407528.
