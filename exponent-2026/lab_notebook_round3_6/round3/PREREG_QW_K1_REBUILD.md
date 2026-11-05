# Pre-registration: rebuild of the independent k = 1 family check (qw_k1_check.py)
Written 2026-11-04 ~21:55 ET by Claude, BEFORE writing or running the script.

## Why
The handoff and status doc cite `qw_k1_check.py` (Claude's independent check of Fable's round-5 families F1, F2) as
being in this folder. It is not on disk: it lived only in an earlier session's cloud sandbox. The check is rebuilt
here so the record can be rerun. Logged as a record-keeping mistake.

## Method (independent of Fable's code and closed forms)
Q_w(t,1) computed straight from the definition, cp(μ)·a_t·C(m,1), with exact fractions, using the Qw() routine of
`qw.py` in this folder (Claude's own, written before round 5). No use of Fable's M_c formula except in check C below,
where the formula is the thing under test.

## Checks and predictions
- CONTROL 0: (−3,−3,−2,−2,0,0) at (k,t) = (2,3) gives Q_w = 1.0357… (> 1); generic weights (powers of 2) give
  exactly 1 at every k = 1, t. If either fails, stop: the evaluator is wrong.
- A (F1, two-valued, 0^a 1^b, 1 ≤ a ≤ b, a + b ≤ 16, all 2 ≤ t ≤ m/2): PREDICT max Q_w(t,1) = 1 exactly, attained only
  at (a,b,t) = (2,2,2); every other case < 1.
- B (F2, 0^2 plus G generic values = powers of 2, 2 ≤ G ≤ 12, all 2 ≤ t ≤ m/2): PREDICT Q_w ≤ 1, equality only at
  G = 2, t = 2.
- C (Fable's closed form at n = 2, t = 2): PREDICT brute force equals (G³+G²+4G+4)/(G³+2G²+3G+2) exactly for
  G = 2..12.
- D (evidence only, beyond the proved families: 0^n plus G generic, n = 3, 4, n + G ≤ 14): PREDICT Q_w ≤ 1, no equality.
## Resources
One process, 2-core VM (not the laptop's GFN hunt), expected < 2 min, hard stop 10 min.

## Outcome (appended 2026-11-04 ~21:58 ET, after the run; output in qw_k1_check_out.txt, 7.2 s)
- CONTROL 0 PASS: (−3,−3,−2,−2,0,0) at (2,3) gives 29/28 = 1.0357; generic weights give exactly 1 (k = 1, m = 4..12).
- A PASS: 280 two-valued cases (m ≤ 16); max exactly 1, only at (a,b,t) = (2,2,2).
- B PASS: 0^2 + G generic, G = 2..12; max exactly 1, only at G = 2, t = 2.
- C PASS: Fable's closed form (G³+G²+4G+4)/(G³+2G²+3G+2) matches the brute force exactly for G = 2..12.
- D PASS (evidence): n = 3, 4 zeros plus generics, n + G ≤ 14: max 750/871 = 0.861, no case ≥ 1.
All predictions met. This is a computational check of the two proved families on small sizes, not a proof.
