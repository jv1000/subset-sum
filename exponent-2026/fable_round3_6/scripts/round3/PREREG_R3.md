# Round-3 pre-registrations (Conjecture M′: a_t ≤ poly(m)·a_k, t ∈ [k, m−k], k ≤ c·m, c > 0.007)

Each entry: two lines before the run (prediction, control), outcome appended after. Scripts in `scripts/round3/`,
outputs in `scripts/round3/out/`. Harness: `lay3.py` (brute force, m ≤ 16; Dinic max-flow for the Hall tests).
Every run: one process, under 10 minutes.

## R3-A0 `free_bounds.py` — the three loss-bearing bounds that are PROVED (baseline)
(a) entropy: a_k ≥ a_t·C(m−k,t−k)/C(m,t−k); (b) a_t ≤ a_k·max_u f_k(u); (c) a_t ≤ E_B a_k(M∖B), |B| = t−k.
Prediction: all three hold on every instance (they are theorems); (a) is tight (equality) exactly for generic weights;
none of them gives M′ with a poly factor (the loss of (a) is ≈ 2^k at t = m/2; (c) fails as a step by 2^k on two-valued M).
Control: generic weights (a_j = 1 ∀j) give equality in (a) and (b).

## R3-A1 `approx_mono.py` — approximate monotonicity ratio at larger m and wider ranges
Quantity: ρ(M) = max_{j+1 ≤ m/2} a_{j+1}/a_j and, separately, ρ_int(M) = max over j+1 < m/2 (strictly inside);
also μ′(M) = max_{k ≤ m/4} max_{t∈[k,m−k]} a_t/a_k.  Random instances m = 10..14, uniform in [−R,R], R ∈ {10, 20, 40},
and the "cluster + doubles + large" shape of the m = 8 counterexamples, 20,000 instances per (m, R, shape) cap.
Prediction: ρ ≤ 1.03 everywhere; ρ_int = 1 (no interior violation); μ′ = 1 exactly. If a violation with ρ_int > 1
appears, record it and test whether it scales with m.
Control: w = (−6,−5,−5,−3,−3,−2,4,5) gives ρ = 96/95 (must be reproduced by the same code path).

## R3-A2 `cs_rep.py` — direction (ii): second-moment (Cauchy–Schwarz) form of M′ with canonical witnesses
For one witness X_y per t-sum, mult(u) = #{(y, A ⊆ X_y): |A| = k, w(A) = u}; Q(t,k) = Σ_u mult² /(s_t C(t,k) C(m−k,t−k)).
PROVED: s_k ≥ s_t C(m,k)/(C(m,t) Q), so M′ ⟸ Q ≤ poly.  Q = 1 for generic weights (every mult = C(m−k,t−k)).
Witness rules compared: lex-first (natural order), min over 8 random orders, and "min-fiber" (witness containing the
k-sets with the smallest fibers is not canonical; skipped).  Exhaustive multisets in [−3,3] for m ≤ 10 and random m ≤ 13.
Prediction: Q ≤ m for lex-first on every instance with k ≤ m/4, t ≤ m/2; Q grows with the fiber sizes but not
exponentially in m at fixed value range. Control: generic → Q = 1.000 exactly.

## R3-A3 `hall_flow.py` — direction (i): flow/Hall form with poly slack
Graph: y ∈ Σ_t ~ u ∈ Σ_k iff some witness of y contains a k-set of sum u. P*(M; t, k) = least capacity ratio
(× C(m,k)/C(m,t)) under which every t-sum sends one unit; P* ≥ a_t/a_k always, P* = 1 for generic.
Prediction: P* ≤ 1 + 0.03 for every tested instance with k ≤ m/4 (the only known excess is the m = 8 middle step,
96/95); P* = 1 exactly for k ≤ m/4 and t < m/2.  Control: the m = 8 counterexample must give P*(8; 4, 3) ≥ 96/95.

## R3-A4 `sparse_tail.py` — direction (iii): k small, [S] directly against the cube at larger m
Quantity: Λ(M,k) = a_k·2^{d(M)}·(m+1) (≥ 1 is what Lemma S needs with P = 1); also the relation counts Z_k(A) and the
lower tail of the cube's F(T) given A ⊆ T.  Random wide-range and planted-relation instances, m = 14..18, k = 1..3.
Prediction: Λ ≥ 1 everywhere (minimum attained near generic weights, where Λ ≈ m+1); the per-A coupling T ⊇ A loses
a factor ≈ 2^{−|Q|} per relation (so no per-A lower tail can give [S]); the averaged quantity E_A[f_k(A)]/2^d stays ≤ poly.
Control: generic weights give Λ = m+1 exactly and E_A f_k = 1 = 2^d.

### Outcomes R3-A0..A3 (appended after the runs)
- A0 (`out/free_bounds.txt`): 6,435 instances, all three bounds hold, max ratios exactly 1.000 (generic control tight). Loss of
  P2 at t = m/2: 2^{-8.4} for m = 100, k = 11; 2^{-12.2} for k = 25 (≈ 2^{-k} up to poly). As predicted.
- A1 (`out/approx_mono.txt`): control reproduces 96/95. 400,000+ random instances, m = 10..14, uniform and cluster shapes,
  R ∈ {10,20,40}: max ρ = 1.000 (attained trivially at j = 0), ρ_int = 1, μ′ = 1. No violation anywhere. Prediction held;
  note the random generators rarely produce the doubled-values structure of the m = 8 counterexamples (see A6).
- A2 (`out/cs_rep.txt`): control Q = 1.000 (generic). Exhaustive [−3,3] m = 6..10 and random m = 11..13: Q_lex ≤ 1 in every
  case with k ≤ m/4, and Q_lex is within a few % of a_t/a_k (so the second-moment form is essentially tight, not lossy).
  Stronger than predicted (predicted Q ≤ m). The middle step (k = m/2 − 1) was not in the sweep; at the m = 8
  counterexample Q(4,3) ≥ 96/95 is forced. New target: R3-A5.
- A3 (`out/hall_flow.txt`): controls OK (generic P* = 1.000; counterexample P*(8;4,3) = 1.0107 ≥ 96/95). All sweeps:
  P* = a_t/a_k to within the 1e-3 search tolerance, i.e. Hall's condition holds with the best possible constant on every
  instance: the flow form is equivalent to M′, not a strengthening. Prediction (P* ≤ 1.03, = 1 inside) held.

## R3-A4 `sparse_tail.py` — see above (launched after A3).

## R3-A5 `cs_w.py` — the canonical (witness-free) second-moment form and its reduction
Q_w(t,k) := s_t C(t,k)·P_{π⊗π}[w(A) = w(A′)] / C(m−k,t−k), π = (uniform y ∈ Σ_t, uniform witness X of y, uniform k-subset
A ⊆ X). PROVED: Q_w ≤ E_rule[Q] for random witness rules (convexity) and Q_w ≤ P ⟹ M′ with P (Cauchy–Schwarz on the
support). PROVED tonight: Q_w ≤ 1 ⟺ w(L^{nm}) ≤ w(R′) where L^{nm} = {(X,X′,A ⊆ X,A′ ⊆ X′): w(A)=w(A′), A′∖A meets X},
weight 1/(f_t(X)f_t(X′)), and R′ = {(Y,Y*,Y″,D): w(Y*)=w(Y), Y* ≠ Y, D ⊆ Y∩Y″, |D| = k, D ⊉ Y∖Y*}, weight 1/(f_t(Y)f_t(Y″))
(the swap injection Φ_1 matches the non-near-miss part of L exactly onto {D ⊇ Y∖Y*}).
Prediction: Q_w ≤ 1 for all k ≤ m/4, t ∈ (k, m/2]; Q_w > 1 only at the middle step (k = m/2−1) and only on the m = 8
counterexample families; the ratio w(L^{nm})/w(R′) equals the sign of Q_w − 1 (consistency) and stays ≤ 1 inside.
Control: generic weights give Q_w = 1 with L = R = ∅ (0 = 0); the m = 8 counterexample gives Q_w(4,3) ≥ 96/95.

## R3-A6 `hill.py` — adversarial search for interior violations and for large Q_w at k ≤ m/4
Hill-climb (random restarts, single-coordinate moves, values in [−R,R], R ≤ 12) maximising (a) ρ_int (interior
monotonicity ratio), (b) ρ at the middle step, (c) max_{k ≤ m/4, t} Q_w, at m = 9..13, seeded with the m = 8
counterexample padded by random values.
Prediction: (a) stays 1.000 (no interior violation); (b) finds ρ > 1 at m = 8 only (ratio ≤ 1.03) and nothing at m ≥ 9;
(c) max Q_w ≤ 1.000. Control: the m = 8 seed itself gives ρ = 96/95.

### Outcomes R3-A4..A6 (appended after the runs)
- A4 (`out/sparse_tail.txt`): controls OK (generic Λ = 13.0 = m+1; m = 8 counterexample Λ = 54/36/24 for k = 1/2/3). 2,655
  instances, m = 12..16, k ≤ m/4: min Λ = 13.2/14.2/15.2/16.3/17.3 (m = 12..16), i.e. a_k·2^d ≥ 1.0 always, minimum at the
  near-generic planted-relation instances (E f_k/2^d = 0.98); max tail = 0.033 ≪ 1 (tail ≤ 1 suffices for [S] with
  constant m+1). Near-miss lemma P5: 0 failures. Predictions held.
- A5 (`out/cs_w.txt`): controls OK (generic Q_w = 1 with L = R′ = 0; counterexample Q_w(4,3) = 1.0788 ≥ 96/95, and
  w(L^nm) = 179.7 > w(R′) = 141.9 there, consistent with the reduction). Exhaustive [−3,3] m = 6..10 (m = 10 cut at 150 s,
  7,636 of 8,008 multisets), 59,233 random m = 8 in [−6,6], random m = 11, 12: **0 violations of Q_w ≤ 1 with k ≤ m/4**.
  Q_w > 1 occurs for k ≥ m/3 even where a_t ≤ a_k holds: (m,k,t) = (6,2,3) 1.0357 (a_t/a_k = 0.875), (8,3,4) 1.0300 at
  (−3,−3,−3,−2,−2,−2,1,1), (10,4,5) 1.0286, (12,4,6) 1.0114 (a_t/a_k = 0.882), (12,5,6) 1.0173. So the prediction "Q_w > 1
  only at the middle step" was wrong: the correct cut is k ≤ m/4 (holds) versus k ≥ m/3 (fails by ≤ 8 %). In every case
  Q_w − a_t/a_k ≤ 0.1, i.e. the second-moment form is nearly tight.
- A6 (`out/hill.txt`): control reproduces 96/95. Hill-climb m = 8..13 (182–468 restarts each): max r_int = 1.000 at m = 8
  only (0.92, 0.86, 0.76, 0.81, 0.75 at m = 9..13); max r_mid = 1.0222 at m = 8 (the known worst, 92/90) and ≤ 1.000 at
  m ≥ 9 (1.000 = two-valued). Max Q_w (k ≤ m/4) = 0.839/0.749/0.693 at m = 9/10/11 (below the generic value 1, which is
  unreachable in [−8,8] at these m). Predictions held.
