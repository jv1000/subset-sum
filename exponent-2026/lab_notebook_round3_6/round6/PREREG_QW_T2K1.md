# Pre-registration: computational check of Astra's new theorem Q_w(2,1) ≤ 1 for all integer weights (m ≥ 4)
Written 2026-11-04 ~22:30 ET by Claude, before the run. Hand check of both of Astra's proofs is in REVIEW_OF_ASTRA_ROUND6_B.md.
Method: Q_w(2,1) from the definition (cp(μ)·a_t·C(m,1), exact fractions) via round3/qw.py's Qw — not Astra's code, not
the M_c formula. Also compute M_c = Σ_X j_c(X)/f(X) directly to test the lemma "singleton M_c ≤ r−1, repeated M_c ≤ r+1".
Scope: exhaustive multisets m = 4..9 in [−4,4]; m = 10 in [−3,3]; 3000 seeded random instances m = 10..14 with mixed
palettes (few-valued, wide, one repeated pair among generics).
Predictions: (1) max Q_w(2,1) = 1 exactly, never > 1; (2) the M_c lemma holds in every case; (3) Q_w = 1 occurs for
generic weights and for a pair (0,0) with G = 2 other values (e.g. (0,0,1,1), (0,0,g1,g2)), and no instance with a
repeated class exceeds it.
Control: (−3,−3,−2,−2,0,0) at (k,t) = (2,3) must give 29/28 (outside the theorem's scope).
Resources: one process, < 10 min.

## Outcome (appended ~22:33 ET; qw_t2k1_check_out.txt, 14 s)
Control 29/28 PASS. 59,408 instances (56,408 exhaustive + 3,000 random): max Q_w(2,1) = 1 exactly, 0 violations;
M_c lemma holds in every case; equality with a repeated class seen only at m = 4 (pair + two other values), as
predicted. All predictions met. Evidence for the theorem; the proof itself was checked by hand (review B).
