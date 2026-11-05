# Round 4 report: the charging inequality, the window k/m ∈ (1/4, 1/3), and the gadget-product limit

Claude Fable 5.1, 4 Nov 2026, working as a collaborator. Discipline as before: every run is pre-registered in
`scripts/round4/PREREG_R4.md` (prediction and control before the run, outcome appended, including the predictions
that failed); every claim is labelled PROVED, EVIDENCE or CONJECTURE; dead ends are kept with the reason.
`paper_v2.md` was not edited. Scripts in `scripts/round4/`, outputs in `scripts/round4/out/`; one process at a time;
the longest single run was 16 minutes; nothing was enumerated above m = 20. **No proof of Conjecture Q was obtained
for any range of k**, so nothing is handed to a referee; what is handed over is a sharpened conjecture, a candidate
charging lemma that survived every test, and the exact structural reason the simpler charging maps fail.

Notation (ROUND3_REPORT A.1, A.3): a_j = s_j / C(m,j); the canonical second-moment constant
Q_w(t,k) = Σ_u mult_w(u)² / (s_t C(t,k) C(m−k,t−k)) with mult_w(u) = Σ_{A : w(A)=u} N_w(A), N_w(A) = Σ_{X ⊇ A} 1/f_t(X);
Q_w ≤ 1 ⟹ a_t ≤ a_k. Conjecture Q: Q_w ≤ 1 for k ≤ m/4, k < t ≤ m/2. Round 3 reduced Q_w ≤ 1 exactly to the
charging inequality w(L^nm) ≤ w(R′) between near misses and t-level collisions (recalled in §A.1).

## Summary table

| Task | Status | Result |
| --- | --- | --- |
| 1. Charging inequality w(L^nm) ≤ w(R′) for k ≤ m/4 via a fractional map | **not proved**; rule ladder decided | Fourteen locality rules tested as max-flow feasibility on up to 13,661 (instance, k, t) cases with t + 2k ≤ m (exhaustive [−3,3] m = 6, 7, [−4,4] m = 6, samples m = 8, 9, curated m ≤ 10). PROVED (by explicit instances): every rule that keeps the relation (P,Q), even as a sub-relation, fails; the per-relation inequality fails by a factor up to 6.4; the min-cut shows why (§A.3). EVIDENCE: the rule **YP** (charge a near miss (X, A, A′) to every collision Y ∼ Y* with Y ⊇ P = A∖A′, any partner, any D) and its supersets YPQ, YPQx are feasible on every one of the 13,661 cases (0 failures; §A.4). The control (−3,−3,−2,−2,0,0) at (2,3) is infeasible under every rule (routes ≤ 90 %). CONJECTURE (YP-Hall): the Hall condition of YP holds whenever t + 2k ≤ m; it implies Conjecture Q. No closed-form map: the proportional map has load 1.126 on one m = 7 instance. |
| 2. The window k/m ∈ (1/4, 1/3) at m = 16 and 20 | decided for the targeted families | EVIDENCE: no violation with k < m/3 anywhere (exhaustive small m, A0; two-valued and all {0,p,q} splits at m = 12..14, {0,1,c} at m = 15, 16, generic padding, A2; m = 20 targeted, A3). The discriminators (13;4,6), (14;4,7), (16;5,7), (16;5,8) are at 0.67–0.73. Violations occur only at k ≥ m/3, and at m ≥ 12 only at k = m/2 − 1, t = m/2 (≈ 1.03). Honest statement: Conjecture Q can be stated for **k < m/3** with the same evidential standing as for k ≤ m/4; k = m/3 is excluded by (6;2,3). |
| 3. Gadget-product limit (hidden 2^{εk} loss?) | ruled out for products | PROVED (interval layer sets) / EVIDENCE (otherwise): for q → ∞ generic-separated copies of any A5/A0 worst block, R/m ≥ 0.16 at α = 1/4 (≥ 0.28 at α ≤ 0.05) and the M′ exponent E(α,τ) ≤ 0 for all α ≤ 1/4, τ ∈ [α, 1/2]. Exact products: Q_w falls from 1.036 (q = 1) to 0.944 (q = 2) to 0.882 (q = 3) for the m = 6 block, and similarly for every block. Violations are single-block phenomena that products wash out. |

---

## A. Task 1 — the charging inequality

### A.1 Setting (from ROUND3_REPORT A.3 (ii))

Fix w, t ≤ m/2, k < t. A *near miss* is ℓ = (X, X′, A, A′) with |X| = |X′| = t, A ⊆ X, A′ ⊆ X′, |A| = |A′| = k,
w(A) = w(A′), A ≠ A′, and B := (A′∖A) ∩ X ≠ ∅; its weight is 1/(f(X) f(X′)). Write P = A∖A′, Q = A′∖A (the
*relation* of ℓ; w(P) = w(Q), |P| = |Q| = j ≥ 1). A *target* is r = (Y, Y*, Y″, D) with |Y| = |Y*| = |Y″| = t,
w(Y) = w(Y*), Y ≠ Y*, D ⊆ Y ∩ Y″, |D| = k, D ⊉ Y∖Y*; weight 1/(f(Y) f(Y″)). Then Q_w ≤ 1 ⟺ w(L^nm) ≤ w(R′).

A *fractional charging map* is a flow from near misses (supply = weight) to targets (capacity = weight) along the
edges of a *locality rule*; the rule is viable on an instance iff the max-flow saturates the supply (Hall's condition
for weighted bipartite graphs). Aggregation: a rule that ignores X′ and Y″ works on the nodes (X, A, A′) with supply
N(A′)/f(X) and (Y, Y*, D) with capacity N(D)/f(Y); this is exact because Σ_{X′ ⊇ A′} 1/f(X′) = N(A′) and likewise for
Y″ (PROVED, trivial). All flows below are on the aggregated graph (Dinic, integer scaling 2^36, tolerance 10⁻⁶).

The harness: `charge_flow.py` (rules S1E, S1P, S1, S2, T, C, V, free), `per_rho.py` (the per-relation inequality),
`charge_flow2.py` (SUPA, SUPD, SUPX, SUP), `charge_flow3.py` (DA, DAA, YA, YAA, YPQ), `charge_flow4.py` /
`charge_flow4b.py` (YP, YPQx, YPQ at scale), `mincut_diag.py` (named Hall violators). Every run has the control
(−3,−3,−2,−2,0,0) at (2,3) (Q_w = 1.0357; must be infeasible under every rule, and is: `free` routes 90 %, the total
supply 30 exceeds the total capacity 27) and the equality case (0,0,g1,g2) at (1,2) (Q_w = 1 exactly; the map must be
tight, and is, with explicit load 1.000). The rule `free` (all edges) agreed with the sign of Q_w − 1 on every one of
the 152 curated instances (enumeration check).

### A.2 The rule ladder (most local → least local) and where each fails

All failures below are on instances with t + 2k ≤ m (the range where Conjecture Q and H2 claim Q_w ≤ 1), so each
failure is a PROVED counterexample to "this rule yields the charging inequality".

| Rule (edges from (X, A, A′) with P, Q, B = Q ∩ X) | Result in range t + 2k ≤ m | Witness (instance, (k,t), routed fraction) |
| --- | --- | --- |
| perD: Y″ = X′, D = A′ (the per-u bound mult_w(u) ≤ C(m−k,t−k)) | FAILS already at k = 1 | (0,0,g1,g2,g3), (1,2): mult(0) = 5 > 4 (hand-checked); per-u ratio up to 1.6 at m = 8 while Q_w < 1 |
| C: X ∈ {Y, Y*} (collision at X itself) | FAILS on 1125/924 (instance,(k,t)) at m = 6 | (−3,−3,−3,−3,0,0), (1,2): 0.333 |
| S1E / S1P / S1: swap-repair Y = (X∖B) ∪ E, E ⊆ M∖(X ∪ Q), Y* = (Y∖P) ∪ Q (D ⊇ E / D ∩ P = ∅ / D free) | FAIL on 264/924 at m = 6, 2076 cases at m = 7, 4599 at m = 8 | (−3,−3,−3,−3,0,0), (1,2): 0.5; explicit proportional map load up to 18 |
| S2: S1 or reversed orientation | FAILS as S1 | same |
| T: repaired Y, any collision partner Y*, any D | FAILS only on the zeros family | (0,0,0,g,g,g,g), (2,3): 0.976 |
| V: any collision at Hamming distance ≤ 2\|B\| from X | FAILS only on the zeros family | same instance, 0.976 (mass must go to distance 4) |
| per-rho: same relation (complete bipartite inside each (P,Q)) | FAILS on 243/924 at m = 6, most at m = 7, 8; ratio S/T up to 6.4 | (0,0,0,0,0,1,1,1), (2,3): S/T = 6.4; (0,0,1,1,1), (1,2): S = 1.5, T = 0.5 (hand) |
| SUPA: Y ⊇ A, Y ∩ Q = ∅, Y* ⊇ A′, Y* ∩ P = ∅ | FAILS on 362/1716 at m = 7 | (−3,−3,−3,−2,−2,−1,0), (2,3): 0.910 |
| SUPD: SUP and D ∩ P = ∅ | FAILS on almost everything with k ≥ 2 | (−3)^7, (2,3): 0.333 |
| SUP / SUPX: relation kept as a sub-relation, P ⊆ Y∖Y*, Q ⊆ Y*∖Y (SUPX: also \|Y∖X\| ≤ \|B\| + \|P\|) | FAIL on 77/1716 at m = 7 and 43/641 at m = 8, all at (2,3), narrowly (98.2–99.6 %) | (−2,−1,−1,0,0,1,2,3), (2,3): 0.982; (−6,−5,−2,−1,0,3,4), (2,3): 0.985 |
| DA / DAA: D = A (or D ∈ {A, A′}), any collision at Y ⊇ D | FAIL on 192/924 at m = 6 | (−3,−3,−3,−2,−1,1), (1,3): 0.5 |
| YA / YAA: Y ⊇ A (or Y ⊇ A or Y ⊇ A′), any Y*, any D | FAIL on 2/1707 at m = 7 | (−3,−3,−3,0,1,2,3) and (−3,−2,−1,0,3,3,3), (2,3): 0.944 |
| **YPQ: Y ⊇ P or Y ⊇ Q, any Y*, any D** | **0 failures** on 13,661 cases (§A.4) | — |
| **YP: Y ⊇ P only** (smaller edge set); YPQx: YPQ with Y ≠ X | **0 failures** on the same 13,661 cases | — |
| free: all edges | feasible iff Q_w ≤ 1 | consistency check |

Reading the ladder. (i) Anything that fixes D (perD, DA, DAA) or fixes the collision to sit at X (C) is hopeless.
(ii) The natural "repair" map (swap B for fresh elements E outside X ∪ Q, keep the relation) fails for the two-valued
instances: on (0,0,1,1,1) at (1,2) the near misses with relation (z1 → z2) weigh 1.5 but the collisions with that
relation have capacity 0.5; the missing 1.0 sits only in collisions with the *larger* relation ({z1,e},{z2,e′}).
This kills every same-relation rule (T, V, per-rho). (iii) Allowing larger relations that *contain* (P,Q) (SUP)
almost works, but fails on a thin set of instances at (2,3) — the min-cut in §A.3 shows the failure is structural,
not numerical. (iv) Keying on the k-sets A, A′ (YAA) fails on two instances; keying on the *relation halves* P, Q
(YPQ) has not failed.

### A.3 The structural obstruction (min-cut diagnosis, `mincut_diag.py`)

On (−2,−1,−1,0,0,1,2,3) at (2,3) under SUP the Hall violator is four near misses at X = {−2,−1,−1} (the unique
3-set with sum −4, so f(X) = 1, so these near misses are heavy: N(A′)/f(X) = 1.065 each for the two with X = {−2,−1,−1})
with A = P = {−1,−1}, A′ = Q = {−2,0} (two choices of the 0). Their SUP-neighbourhood is the sixteen targets
Y = {−1,−1,e} ∼ Y* = {−2,0,e}, e ∈ {0′,1,2,3}, whose sums have f(Y) = 5, 7, 9, 9 witnesses, so each target's capacity
N(D)/f(Y) is 0.10–0.19: total supply 2.556 against total capacity 2.015. On (−6,−5,−2,−1,0,3,4) at (2,3): twelve
unique-sum sources (f(X) = 1, supply 2.2 each, 26.40 in all) against 36 supporting targets with f(Y) = 3 or 5 (25.55).

The obstruction in words: a k-level relation (P,Q) seen by a t-set X whose sum is *unique* produces heavy near misses,
but every t-level collision that *contains* that relation lives at sums with *many* witnesses, which dilutes the
capacity 1/f(Y). The extra mass has to be charged to collisions whose relation is unrelated to (P,Q) — e.g.
{−2,−1,3} ∼ {−1,0,1} — i.e. to collisions that merely contain P or Q as a subset but realise the collision through a
different balanced pair. That is exactly what YPQ allows and SUP forbids. It also says what a proof must do: it must
not be relation-local; it must compare the number of balanced relations of level ≤ k seen by unique-sum t-sets with the
number of t-level collisions through P, with the 1/f weights — the same "witness-count" tension as in the
round-3 near-miss lemma P5. (iv) in §A.2 is the positive side of the same picture: keying only on P = A∖A′, the part
of the k-set that the near miss removes, never failed.

### A.4 The surviving rules YP ⊂ YPQ (EVIDENCE, and the proposed lemma)

Rule YPQ: the near miss (X, A, A′) with P = A∖A′, Q = A′∖A may charge any target (Y, Y*, D) with Y ⊇ P or Y ⊇ Q
(Y* any collision partner of Y, D any admissible k-subset of Y). Results in range t + 2k ≤ m:

| Test set | cases | YPQ failures | worst routed | explicit proportional map, max load |
| --- | --- | --- | --- | --- |
| curated m = 7..10 (counterexamples, A0/A5 worst cases, two-valued, zeros + generic, shapes) | 54 + 49 | 0 | 1.000 | 0.874 ((−3,−3,−2,−2,0,1,1) at (2,3)) |
| exhaustive [−3,3] m = 6 (924 multisets, 1834 cases) and m = 7 (1716, 5146); [−4,4] m = 6 (3003, 5838); sample m = 8 (547 cases, 33 dense cases skipped by the memory guard); sample m = 9, k ≤ 2 (296 cases, 104 skipped) — `charge_flow4b.py`, 13 min | 13,661 | 0 | 1.000 (to 10⁻⁹) | 1.126 ((−3,−3,−2,−2,0,3,3) at (2,3)); 0.96 at m = 8, 0.55 at m = 9 |
| charge_flow3 (independent run, same rule) m = 6, 7, 8 | 2,707 | 0 | — | — |

Controls: (6;2,3) routes 0.900 under YP, YPQx and YPQ (infeasible, as it must be); the equality case is tight
(load 1.000); the two YAA failures are YPQ-feasible (0.953 load). The variants also never failed: **YP** (only
Y ⊇ P, i.e. the collision must contain the part of A that A′ lacks; a strictly smaller edge set) and **YPQx** (Y ≠ X)
have 0 failures on the same 13,661 cases, against the pre-registered prediction that YP would fail somewhere. So the
surviving candidate is the smaller rule YP. The explicit proportional map is *not* always a valid certificate
(load 1.126 at m = 7), so the certificate is the flow, not a closed-form map. Caveat: the memory guard skipped the
densest m = 8, 9 cases (many repeated values, e.g. (0,0,0,0,2,2,2,2) at (2,4)); those are two-valued shapes whose
smaller analogues all passed, but they are untested at m = 8, 9.

**CONJECTURE (YP-Hall).** For every w, every t ≤ m/2 and k < t with t + 2k ≤ m, and every set S of near misses,
w(S) ≤ w({targets (Y, Y*, Y″, D) : Y ⊇ P(ℓ) for some ℓ ∈ S}), P(ℓ) = A∖A′.
(The weaker YPQ-Hall, with "Y ⊇ P or Y ⊇ Q", is implied.) By max-flow/min-cut it is equivalent to the existence
of a fractional charging map along YP edges, and it implies Q_w ≤ 1, hence a_t ≤ a_k, on the whole range t + 2k ≤ m
(which contains Conjecture Q's range k ≤ m/4).
*Naming note (round 5, 4 Nov 2026).* The conjecture is about the rule **YP** only: a near miss (X, A, A′) may charge a
target (Y, Y*, Y″, D) iff Y ⊇ P = A∖A′ (any partner Y*, any Y″, any admissible D). Two lines in §B previously called the
same lemma "YPQ-Hall"; they now say YP-Hall. YPQ-Hall (Y ⊇ P or Y ⊇ Q) is the weaker statement implied by it and is not
the conjecture.

Status: EVIDENCE only. What was tried toward a proof, and where it stops (kept as dead ends, §D): (a) the explicit
proportional map (each near miss spreads its weight over its targets proportionally to capacity) is a valid
certificate whenever its max load is ≤ 1 — it is not always (load 1.126 on (−3,−3,−2,−2,0,3,3) at (2,3)), so no
closed-form map was found; (b) a per-P decomposition (sum over near misses with
a fixed P versus targets with Y ⊇ P) is the natural inductive statement; it is the |P| = k, Q-free analogue of P5 and I
could not close it, because the weights 1/f(X) on the source side and 1/f(Y) on the target side are not comparable
set-by-set (the min-cut above is precisely a counterexample to the set-by-set version with the relation kept).

### A.5 Working hypothesis H2 and the role of t + 2k ≤ m

Pre-registered before any round-4 run: **H2: Q_w ≤ 1 whenever t + 2k ≤ m**. It was suggested by the repair step
needing |E| = |B| ≤ k fresh elements outside X ∪ Q (m − t − k ≥ k) and by the exact equality cases at t + 2k = m
(Q_w = 1 for (0,0,g1,g2) and (0,0,1,1) at (1,2); both hand-verified, PROVED). All round-4 data are consistent with
H2 (no violation with t + 2k ≤ m in ≈ 60,000 exhaustive multisets at m ≤ 10 and all the m = 12..20 families), and
the boundary t + 2k = m is where the largest in-range values sit (0.9556 at (7;2,3), 0.8970 at (8;2,4), 0.8458 at
(8;2,4) in [−3,3], 0.8286 at (10;3,4)). But H2 is *not* the sharp boundary of Q_w ≤ 1: the cases with t + 2k = m + 1
or m + 2 and k < m/3 are all comfortably below 1 (§B), so the repair-step heuristic is a sufficient-looking condition,
not the true shape of the safe region. Since t ≥ k + 1, H2's region {t + 2k ≤ m} is contained in {k < m/3}; the
larger region {k < m/3} (H3) is also unviolated. See §B.4.

---

## B. Task 2 — the window k/m ∈ (1/4, 1/3)

### B.1 Exact small-m map (A0, `window_small.py`, exhaustive, no cap)

Max Q_w over all multisets, by (k,t); VIOL marks > 1.

| range | (m; k, t) with t + 2k ≤ m: max Q_w | (m; k, t) with t + 2k > m: max Q_w |
| --- | --- | --- |
| [−3,3] m = 6 | (1,2) 0.850, (1,3) 0.867 | **(2,3) 1.0357** |
| [−3,3] m = 7 | (2,3) 0.9385 (boundary) | — |
| [−3,3] m = 8 | (2,3) 0.833, (2,4) 0.846 (boundary) | **(3,4) 1.0300** |
| [−3,3] m = 9 | (2,3) 0.752, (2,4) 0.687 | (3,4) 0.9298 (k = m/3) |
| [−3,3] m = 10 | (3,4) 0.8286 (boundary), (2,5) 0.550 | (3,5) 0.855, **(4,5) 1.0286** |
| [−4,4] m = 6, 7, 8 | (7;2,3) 0.9556, (8;2,4) 0.8970 | (6;2,3) 1.0357, (8;3,4) 1.0300 |
| [−5,5] m = 6, 7 | (7;2,3) 0.9556 | (6;2,3) 1.0417 ((−5,−4,−2,−1,3,4): a_3 = a_2) |

Every violation has k ≥ m/3; the only one at k = m/3 exactly is m = 6. At m = 9 the k = m/3 case (3,4) is 0.93.

### B.2 m = 12..16, targeted families (A2, `window.py`, 99 s)

Families (affine-normalised; the layer structure is invariant under w ↦ αw + β): two-valued {0,1} with every
split; every multiplicity split of {0,1,2}, {0,1,3}, {0,1,4}, {0,1,5}, {0,2,3}, {0,2,5}, {0,3,4}, {0,3,5}, {0,4,5} at
m = 12, 13, 14; two-valued and {0,1,c}, c ≤ 5, at m = 15, 16; the worst shapes of m − 1, m − 2 padded with generic
elements. (k,t) from k = ⌊m/4⌋ − 1 to ⌈m/3⌉ + 1, all t ≤ m/2. Controls: generic m = 12 gives 1.000000 at all ten
pairs; the second control failed *as a control* (the m = 8 violation shape scaled to (6,6,4) at m = 16, (6,8) gives
0.771, not > 1), which is itself informative: proportional scaling does not preserve a violation.

| (m; k, t) | k/m | t + 2k − m | max Q_w | worst shape | H1 / H2 / H3 |
| --- | --- | --- | --- | --- | --- |
| (12; 3, 6) | 0.250 | 0 | 0.520 | 0⁴1⁴5⁴ | safe / safe / safe |
| (12; 4, 5) | 0.333 | +1 | 0.833 | 0⁴2⁴5⁴ | open / open / open |
| (12; 4, 6) | 0.333 | +2 | 0.837 | 0⁴1⁴5⁴ | open / open / open |
| (12; 5, 6) | 0.417 | +4 | **1.0301** | 0⁴1⁴5⁴ | open / open / open |
| (13; 4, 5) | 0.308 | 0 | 0.754 | 0⁴1⁴5⁵ | open / safe / safe |
| (13; 4, 6) | 0.308 | +1 | 0.732 (pad) | 0⁴1⁴5⁴g | open / open / safe |
| (14; 4, 6) | 0.286 | 0 | 0.658 (pad) | | open / safe / safe |
| (14; 4, 7) | 0.286 | +1 | 0.696 (pad) | 0⁴2⁴5⁴gg | open / open / safe |
| (14; 5, 7) | 0.357 | +3 | 0.927 (pad) | | open / open / open |
| (14; 6, 7) | 0.429 | +5 | **1.0304** (pad), 1.0268 | 0⁴1⁴5⁴gg | open / open / open |
| (15; 4, 7) | 0.267 | 0 | 0.547 (pad) | | open / safe / safe |
| (15; 5, 6) | 0.333 | +1 | 0.805 (pad) | 0⁵4⁴5⁴gg | open / open / open |
| (16; 4, 8) | 0.250 | 0 | 0.456 (pad) | | safe / safe / safe |
| (16; 5, 6) | 0.312 | 0 | 0.748 (pad) | 0⁵1⁴5⁵gg | open / safe / safe |
| (16; 5, 7) | 0.312 | +1 | 0.672 (pad) | | open / open / safe |
| (16; 5, 8) | 0.312 | +2 | 0.714 (pad) | | open / open / safe |
| (16; 6, 7) | 0.375 | +3 | 0.877 (pad) | | open / open / open |
| (16; 6, 8) | 0.375 | +4 | 0.930 (pad) | 0⁵4⁴5⁵gg | open / open / open |
| (16; 7, 8) | 0.438 | +6 | **1.0278** (pad), 1.0230 | 0⁵1⁴5⁵gg | open / open / open |

The pre-registered prediction "some Q_w > 1 strictly inside the window" was NOT met: the window is clear by a wide
margin (max 0.754), and so are all the H1/H2 discriminators. The k/m = 0.375 cases, where m = 8 violates, are at
0.93 by m = 16. All violations at m ≥ 12 sit at k = m/2 − 1, t = m/2 and are ≈ 1.03 (the two-valued-plus-5 shapes).

### B.3 m = 20, targeted (A3, `window20.py`, 26 min)

Families: two-valued (all 10 splits); {0,1,5}, {0,1,4}, {0,1,2} splits with every part ≥ 3 (60, 44, 35 instances
before the time caps); {0,2,5}, {0,4,5} with parts ≥ 4 (26 each); the shape (−3,−3,−3,−2,−2,−2,1,1) and the A0
m = 10 worst shape scaled to m = 20 (6 instances); the worst {0,1,c} shapes with 2 or 4 elements replaced by generic
ones (12). (k,t): k = 5 (t = 6..10), k = 6 (7..10), k = 7 (8..10), k = 8 (9, 10), k = 9 (10). Controls: generic
m = 20 gives 1.000000 at (5,6), (6,8), (7,10); the second control (all-equal weights at (9,10), which I predicted > 1)
gave 0.909 — a wrong control prediction, recorded.

| (20; k, t) | k/m | t + 2k − m | max Q_w over all families | family of the maximiser | H1 / H2 / H3 |
| --- | --- | --- | --- | --- | --- |
| (5, 6) | 0.25 | 0 | 0.606 | 0⁶1⁴5⁶ + 4 generic | safe / safe / safe |
| (5, 10) | 0.25 | −4 (t + 2k = m) | 0.397 | same | safe / safe / safe |
| (6, 7) | 0.30 | +1 | 0.695 | same | open / safe / safe |
| (6, 8) | 0.30 | 0 | 0.577 | same | open / safe / safe |
| (6, 9) | 0.30 | +1 | 0.556 | same | open / open / safe |
| (6, 10) | 0.30 | +2 | 0.612 | same | open / open / safe |
| (7, 8) | 0.35 | +2 | 0.793 | same | open / open / open |
| (7, 9) | 0.35 | +3 | 0.749 | same | open / open / open |
| (7, 10) | 0.35 | +4 | 0.820 | same | open / open / open |
| (8, 9) | 0.40 | +5 | 0.902 | same | open / open / open |
| (8, 10) | 0.40 | +6 | 0.970 | same | open / open / open |
| (9, 10) | 0.45 | +8 | **1.0240** | same; also 1.0168 for 0⁸1⁴5⁸, 1.0129 for 0⁷2⁴5⁹, 1.000 for 0¹⁰1¹⁰ | open / open / open |

The pre-registered prediction (k = 6: t = 9, 10 some > 1; k = 7: t = 9, 10 > 1) was NOT met: at m = 20 nothing
below k = 9 reaches 1. The window k/m ∈ (1/4, 1/3) at m = 20 has max Q_w = 0.695 (at (6,7), with generic padding
adding ≈ 0.07 over the pure {0,1,5} shapes). The H2 discriminators (20; 6, 9) and (20; 6, 10) are at 0.56 and 0.61.
Generic padding consistently raises Q_w by 0.05–0.1 relative to the pure three-valued shapes and is where every
family's maximiser sits, so a hill-climb seeded there is the right next probe (§F).

### B.4 Verdict: how far Conjecture Q can honestly be stated

- **k ≤ m/4 (Conjecture Q as stated):** EVIDENCE, unchanged in kind, strengthened in quantity: no violation in any
  exhaustive or targeted set at m ≤ 20; the largest in-range value is 0.9556 at (7;2,3) and the values decrease with m.
- **k < m/3 (H3):** the same evidential standing. No violation with k < m/3 anywhere in rounds 3–4 (≈ 100,000
  instances of round 3, the exhaustive sets of A0, the families of A2/A3). The discriminating cases that would have
  separated it from H1 or H2 are all ≤ 0.73 at m = 13..16 and ≤ 0.70 at m = 20.
- **k = m/3:** false at m = 6 ((−3,−3,−2,−2,0,0), 1.0357); unviolated at m = 9, 12, 15 (0.93, 0.84, 0.81).
- **H2 (t + 2k ≤ m):** unviolated and is the region where the proposed lemma (YP-Hall) is formulated; it is not the
  sharp boundary (the cases t + 2k = m + 1, m + 2 with k < m/3 are ≤ 0.93).

So the honest statement is: *Conjecture Q may be stated for k < m/3* (EVIDENCE), with k ≤ m/4 as the range needed
by the application and as the only range for which a proof route (YP-Hall restricted to t + 2k ≤ m) is formulated.
What this does NOT give: a proof for any k, and a reason why 1/3 (rather than, say, 0.4 at large m) is the threshold.
The m ≥ 12 data suggest the true threshold moves toward 1/2 as m grows (violations only at k = m/2 − 1), which would
be consistent with Q_w ≤ 1 for all k ≤ cm, c < 1/2, for large m — a CONJECTURE I state but did not test beyond m = 20.

---

## C. Task 3 — the gadget-product limit (A4, `gadget_limit.py`, 9 s)

Setting. M = q generic-separated copies of a block B of b elements (block i scaled by 1000^i), m = qb, k = αm,
t = τm. Let V = Σ(B) be the set of block sums and lo(v), hi(v) the least and greatest layer of B containing v.
With distinct tuples of block sums giving distinct sums, s_k is the number of tuples (v_1, …, v_q) ∈ V^q admitting
a representation of total size k. If every layer set {j : v ∈ Σ_j(B)} is an interval, this is Σ_i lo(v_i) ≤ k ≤
Σ_i hi(v_i), and a standard large-deviation count gives (PROVED for interval layer sets; for the blocks with
non-interval layer sets the same formula is EVIDENCE, confirmed by the exact q = 2, 3 values)

  (log2 s_k)/m → H*(αb)/b, with H*(A) = max{ H(π) : π on V, E_π lo ≤ A ≤ E_π hi } (bits),
  R/m := lim (log2 a_k + d)/m = H*(αb)/b − h(α) + 1 − (log2 |V|)/b,
  E(α,τ) := lim (log2 a_t − log2 a_k)/m = [H*(τb)/b − h(τ)] − [H*(αb)/b − h(α)].

H* is computed by its convex dual (two Lagrange multipliers, nested golden-section minimisation; no scipy).
Controls: the generic block gives R/m = 0 and E = 0 at every (α,τ) to 10⁻⁴ (as it must: every subset sum distinct);
the all-equal block gives R/m = 1 − h(α) > 0 and E < 0.

| block B | \|V\| | R/m at α = 1/4 | R/m at α = 0.0074 | max_{α ≤ 1/4, τ ∈ [α,1/2]} E(α,τ) |
| --- | --- | --- | --- | --- |
| generic (control) | 64 | 0.000 | 0.000 | 0.000 |
| all-equal 1⁶ (control) | 7 | 0.1165 | 0.5133 | 0.000 (only at τ = α) |
| A5 m = 6 worst (−3,−3,−2,−2,0,0) | 9 | 0.1659 | 0.4601 | 0.000 |
| A5 m = 8 worst (−3³,−2³,1²) | 18 | 0.1617 | 0.4684 | 0.000 |
| A0 m = 10 worst (−3³,−2⁴,2³) | 22 | 0.1791 | 0.5413 | 0.000 |
| A0 [−5,5] m = 6 worst (−5,−4,−2,−1,3,4) | 20 | 0.1623 | 0.2796 | 0.000 |
| m = 8 counterexample 1 (−6,−5,−5,−3,−3,−2,4,5) | 32 | 0.1683 | 0.3718 | 0.000 |
| m = 8 counterexample 2 (−8,−6,−6,−2,−2,0,1,3) | 29 | 0.1673 | 0.3877 | 0.000 |
| m = 7 counterexample (−6,−5,−2,−1,0,3,4) | 22 | 0.1775 | 0.3612 | 0.000 |
| zeros + generic 0⁵g³ | 8 | 0.1887 | 0.6145 | 0.000 |
| two-valued 0⁴1⁴ | 5 | 0.1887 | 0.6879 | 0.000 |
| two-valued 0²1⁶ | 7 | 0.1656 | 0.6272 | 0.000 |

E(α,τ) is strictly negative for every τ > α (e.g. E(1/4, 1/2) = −0.166 for the m = 6 block, −0.162 for the m = 8
block), i.e. a_t/a_k decays like 2^{−cm} on products with c ≥ 0.05 at τ = 0.3 and c ≥ 0.16 at τ = 1/2; and R/m is
bounded away from 0, i.e. a_k 2^d grows exponentially. **There is no hidden 2^{εk} loss on products of the worst
gadgets**: M′ holds on them with room to spare in the limit, and Lemma R's quantity is exponentially positive.

Exact products (brute force, m ≤ 20), Q_w at the scaled (k,t):

| block | q = 1 | q = 2 | q = 3 |
| --- | --- | --- | --- |
| A5 m = 6 worst, (2q, 3q) | **1.0357** (a_t/a_k 0.875) | 0.944 (0.761) | 0.882 (0.591) |
| A5 m = 8 worst, (3q, 4q) | **1.0300** (0.889) | 0.882 (0.724) | — |
| m = 8 counterexample 1, (3q, 4q) | **1.0788** (1.011) | 0.857 (0.712) | — |
| zeros + generic 0⁵g³, (3q, 4q) | 0.950 (0.800) | 0.867 (0.622) | — |
| A0 m = 10 worst, (4q, 5q) | **1.0286** (0.897) | 0.937 (0.773) | — |

At k ≤ m/4 on the products everything is far below 1 (max 0.756 at (12; 3,4) for the m = 6 block; 0.672 at
(16; 4,5) for counterexample 1; 0.322 at (20; 4,6) for the m = 10 block). The pre-registered "some product with
Q_w > 1 at the scaled (k,t)" was NOT observed; the violation is a one-block phenomenon and products dilute it.

---

## D. Dead ends (kept, with the reason)

1. **Per-u bound** mult_w(u) ≤ C(m−k,t−k): false at k = 1 ((0,0,g1,g2,g3): mult(0) = 5 > 4) although Q_w < 1 there.
2. **Swap-repair maps S1/S1E/S1P/S2** (keep the relation, replace B by fresh E): fail on 264/924 instances at m = 6;
   explicit map load up to 18. Reason: two-valued instances need collisions with larger relations.
3. **Collision-at-X (C)** and **Hamming-vicinity (V)**: C hopeless; V fails on (0,0,0,g,g,g,g) at (2,3) because the mass
   of the all-zero X must reach collisions at Hamming distance 4.
4. **Per-relation inequality** S(ρ) ≤ T(ρ): false by a factor 6.4; the |P|-aggregated version also false (3.33).
5. **Sub-relation rules SUP/SUPX/SUPA/SUPD**: SUP fails narrowly (98 %) on a thin set at (2,3); min-cut shows the
   structural reason (unique-sum t-sets vs many-witness collisions), so no tolerance or reweighting fixes it.
6. **k-set keyed rules DA/DAA/YA/YAA**: DA/DAA fail widely; YAA fails on exactly two m = 7 instances (94.4 %).
7. **Proportional scaling as a control**: the m = 8 violation shape scaled ×2 to m = 16 is at 0.771; violations do not
   scale, consistent with the gadget-product result. (Recorded because it was a pre-registered control that failed.)
   Likewise the m = 20 control "all-equal weights at (9,10) > 1" gave 0.909: the (9,10) violations need three values.
8. **H2 as the sharp boundary**: the heuristic "repair needs m − t − k ≥ k" produces a region that is unviolated but
   strictly inside the unviolated region; the true boundary is at least k < m/3 and apparently moves up with m.
9. **The first charge_flow4 run** died of MemoryError on the m = 9 instance (0,0,0,1,1,1,2,2,2) at (2,3) (dense YPQ
   adjacency inside the max-flow); rerun with an edge-count guard (`charge_flow4b.py`), recorded in PREREG.

## E. Labels

PROVED: the aggregation identity; the exact equality cases Q_w = 1 at (4;1,2) for (0,0,g1,g2) and (0,0,1,1); the
failure of every relation-preserving rule and of the per-relation inequality (explicit instances, hand-checked for
(0,0,1,1,1)); the maximum-entropy limit formula for products of blocks with interval layer sets; the generic control
values.
EVIDENCE: Conjecture Q for k ≤ m/4 and for k < m/3 (no violation at m ≤ 20 in every exhaustive/targeted set); the
YP / YPQ rules' feasibility on every one of 13,661 cases tested; the product-limit values for blocks with non-interval layer sets (exact
q = 2, 3 agree in trend); the decrease of Q_w under products.
CONJECTURE: YP-Hall (§A.4); Q_w ≤ 1 for k < m/3; the threshold k/m moving to 1/2 for large m.
NOT OBTAINED: any proof of Conjecture Q.

## F. Next steps (in order of expected value)

1. Attack YP-Hall at k = 1 (then P = A = {p}, a single element, and the rule says: charge the near miss at X ∋ p to
   the collisions through p), where the near misses and targets are explicit: the inequality becomes a statement about
   the multiplicities of equal weights and the 1/f weights of t-sets through a fixed element, and a proof there would
   be the base case of an induction on k. The per-u bound is false at k = 1, so even this base case is non-trivial.
2. If (1) works, induction on k through the "larger relation contains (P,Q)" structure that the two-valued hand
   computation exhibits (the missing 1.0 of (0,0,1,1,1) at (1,2) is carried exactly by the level-2 relations).
3. Close the memory gap: run YP on the dense m = 8, 9 cases skipped by the guard with a sparse-adjacency flow
   (edges per source enumerated on demand), 10 minutes.
4. A cheap sharpening of the window: hill-climb at m = 18, 20 restricted to k ∈ {6, 7, 8} seeded with the
   0^a1^b5^c + generic shapes (every m = 20 maximiser has generic padding), round-3 `hill.py` style, 10 min, to test
   the CONJECTURE that violations stay at k = m/2 − 1.
5. Do not spend more compute on products: Task 3 is settled in the limit.

## G. Files

`ROUND4_REPORT.md` (this file); `scripts/round4/PREREG_R4.md` (all pre-registrations and outcomes, including the failed
predictions); `scripts/round4/README.md` (script table); `scripts/round4/lay4.py` (library: fast Q_w, products,
generic padding); `window_small.py`, `window.py`, `window20.py` (Task 2); `charge_flow.py`, `per_rho.py`,
`charge_flow2.py`, `charge_flow3.py`, `charge_flow4.py`, `charge_flow4b.py`, `mincut_diag.py` (Task 1);
`gadget_limit.py` (Task 3). Outputs in `scripts/round4/out/` (`.txt` results, `.log` full stdout).
