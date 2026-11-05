# Round 5 report: the round-4 gap closed, the base case k = 1 of YP-Hall, and the window at m = 18–20

Claude Fable 5.1, 4 Nov 2026, working as a collaborator. Discipline as before: every run is pre-registered in
`scripts/round5/PREREG_R5.md` (prediction and control before the run, outcome appended, including the predictions
that failed and one mis-stated reduction caught by its own control); every claim is labelled PROVED, EVIDENCE or
CONJECTURE; dead ends are kept with the reason. `paper_v2.md` was not edited. Scripts in `scripts/round5/`, outputs
in `scripts/round5/out/`; one process at a time; every flow run had a memory guard (edge cap and working-set
abort; peak working set 241 MB); the longest run was 19 minutes; nothing was enumerated above m = 20.
**No case of YP-Hall was proved beyond two explicit k = 1 families** (two-valued instances; one repeated pair among
generic values), so nothing is handed to a referee as a proof of the conjecture; what is handed over is the gap
closed, the base case reduced to an explicit transportation problem on weight classes with its tight sets
identified, two families proved, the exact obstruction, and the exact statement of what an induction k → k + 1
would need.

Notation (ROUND4_REPORT §A.1): near miss ℓ = (X, X′, A, A′), P = A∖A′, Q = A′∖A, B = Q ∩ X ≠ ∅, weight
1/(f(X)f(X′)); target r = (Y, Y*, Y″, D), weight 1/(f(Y)f(Y″)); aggregated nodes (X, A, A′) with supply N(A′)/f(X) and
(Y, Y*, D) with capacity N(D)/f(Y). **Rule YP**: ℓ may charge r iff Y ⊇ P. **Conjecture YP-Hall** (ROUND4 §A.4,
rule name made consistent in Task 0): for t + 2k ≤ m the Hall condition of YP holds, i.e. a fractional charging
map along YP edges exists; it implies Q_w ≤ 1 and hence a_t ≤ a_k on that range.

## Summary table

| Task | Status | Result |
| --- | --- | --- |
| 0. Housekeeping | done | ROUND4_REPORT.md §B (two lines) said "YPQ-Hall" for the lemma the summary and §A.4 call YP-Hall. Both now say **YP-Hall**; a naming note after the conjecture statement in §A.4 states that the conjecture is about the rule YP only (Y ⊇ P = A∖A′, any Y*, any Y″, any admissible D), and that YPQ-Hall (Y ⊇ P or Y ⊇ Q) is the weaker consequence. |
| 1. Close the gap (137 dense m = 8, 9 cases) | **closed**, 0 failures | A collapsed flow (sources merged by P, targets merged by Y; exact, §A.1) runs every dense case in ≤ 70 MB. Validation: agrees with round 4's explicit flow to 10⁻¹⁰ on 302 cases; control (−3,−3,−2,−2,0,0) at (2,3) stays infeasible at 0.900. EVIDENCE: **YP, YPQx and YPQ are feasible on all 137 dense cases and the 3 curated m = 9 instances** round 4 never reached, and on a further 19,278 cases (exhaustive m = 8 in [−3,3], m = 9 in [−2,2], partial m = 10): 0 failures, worst routed fraction 1 − 2·10⁻¹⁰. |
| 2. Base case k = 1 | **not proved in general**; two families proved; obstruction written | PROVED: at k = 1, Q_w ≤ 1 ⟺ Σ_c M_c(M_c − C) ≤ 0 over weight classes c (M_c = mult of the class, C = C(m−1,t−1)); YP-Hall(k = 1) is the Hall condition of "element p (demand S_p) may use the collision sets Y ∋ p (capacity cap(Y))" with explicit S_p, cap(Y), and a violation, if any, occurs at a union of classes; over-represented classes (M_c > C) require the whole class inside a t-set with fewer than n_c witnesses, and without them the inequality is trivial. PROVED: Q_w(t,1) ≤ 1 for every two-valued instance (equality only at (0,0,1,1), t = 2) and for one repeated pair among generic values (equality only at (0,0,g1,g2), t = 2; asymptotically tight as the number of generics grows). EVIDENCE (8,894 cases, m ≤ 9): YP-Hall(k = 1) holds with the tight set equal to the over-represented set in every case where one exists; the explicit proportional map is a valid certificate at k = 1 (max load 0.82). Dead end: "extra coincidences only help" is false (1,264 counterexamples), so no reduction to the profile model. Obstruction and the requirements of the induction step: §B.4–B.5. |
| 3. Hill-climb m = 18, 20 in the window | no violation; one pre-registration flaw found and corrected | EVIDENCE: no Q_w > 1 with k < m/3 at m = 18 or 20 in 46,000 evaluations of a free climb and 39,000 of a palette-only climb (controls: the same climbers find the known violations 1.0236 at (18; 8,9) and 1.0240 at (20; 9,10) within one restart). The free climb (A3) converges to *generic* instances, which sit at Q_w = 1 exactly at every (k,t) — overlooked in the pre-registration ("best ≤ 0.85" failed) — and finds nothing above 1 among single-coincidence perturbations of generic instances (best non-generic 0.9987 at (20; 6,10): one pair among generics, consistent with (F2)). The palette-only climb (A3b: values in [−3,6], 0 or 4 generics fixed) explores the structured region: best 0.713 at (18; 5,6) and 0.705 at (20; 6,7), both few-valued blocks plus 4 generics, the same picture as round 4's 0.70. CONJECTURE sharpened: in the window the supremum of Q_w is 1, attained only by generic instances and approached by one repeated pair among generics; every structured (few-valued) instance is ≤ 0.72. |

---

## Task 0 — housekeeping (done)

ROUND4_REPORT.md: lines in §B that said "the proposed lemma (YPQ-Hall)" and "a proof route (YPQ-Hall restricted to
t + 2k ≤ m)" now say YP-Hall; a *Naming note (round 5)* paragraph was inserted after the conjecture statement in
§A.4 saying precisely: the conjecture is about the rule **YP** (a near miss (X, A, A′) may charge a target
(Y, Y*, Y″, D) iff Y ⊇ P = A∖A′; any partner Y*, any Y″, any admissible D), and YPQ-Hall is the weaker statement
implied by it. Nothing else in the round-4 report was changed.

## A. Task 1 — the gap closed

### A.1 Method: the collapsed flow (PROVED exact)

In the aggregated charging network the neighbourhood of a source (X, A, A′) under YP depends only on P (under YPQ
only on (P, Q); under YPQx on (P, Q) and on whether Y = X), and the neighbourhood of a target (Y, Y*, D) depends
only on Y. Merging sources with identical neighbourhoods (supplies added) and targets with identical neighbourhoods
(capacities added, cap(Y) = Σ_{(Y*,D)} N(D)/f(Y)) does not change the max-flow value (the middle edges have infinite
capacity; any flow on the merged network splits back, and conversely). The merged network has at most
#{P} × #{collision sets Y} edges — a few thousand where round 4's explicit network had up to 4·10⁷ — so the dense
cases fit in tens of MB. `flow5.py` also extracts the Hall violator of an infeasible case from the residual graph
(merged source classes and collision sets in the cut, with supply and capacity), so a counterexample would have been
reported with its min-cut; none occurred. Memory guard: a case is skipped if the merged edge count exceeds 3·10⁶ and
the run aborts above a 1500 MB working set (peak observed: 241 MB, at m = 10).

Controls (A1): on 302 random (instance, k, t) cases at m = 6, 7 the collapsed flow agrees with round 4's explicit
flow (`charge_flow4.Inst4`) to 1.1·10⁻¹⁰ for all three rules; (−3,−3,−2,−2,0,0) at (2,3) routes 0.9000 under YP,
YPQx, YPQ (supply 30 vs capacity 27, infeasible as required); (0,0,g1,g2) at (1,2) is tight (supply = capacity = 4).

### A.2 Results (EVIDENCE)

The 137 cases are regenerated exactly (same generator seed and draw order as round 4's `charge_flow4b.py`; the
counts 33 at m = 8 and 104 at m = 9, and the 843 tested cases, match).

| Set | cases | YP / YPQx / YPQ failures | worst YP routed | note |
| --- | --- | --- | --- | --- |
| the 137 guard-skipped dense cases (m = 8: 33; m = 9, k ≤ 2: 104) | 137 | 0 / 0 / 0 | 1 − 3·10⁻¹² | e.g. (0,0,0,0,2,2,2,2) at (2,4), (−2,0,0,0,0,1,1,1,1) at (2,4); 13 s in all |
| curated m = 9 instances never reached in round 4: (0,0,0,1,1,1,2,2,2), (−3,−3,−2,−1,0,1,2,3,3), (−2,−2,−1,−1,0,0,1,1,2) at k = 2, t = 3, 4 | 6 | 0 / 0 / 0 | 1 | the instance that killed round 4's run routes 1 with 1568 sources |
| A1b: exhaustive m = 8 in [−3,3] (all 3003 multisets), all t + 2k ≤ m | 15,015 | 0 / 0 / 0 | 1 − 2·10⁻¹⁰ | tight cases are the all-equal instances at (1,2) |
| A1b: exhaustive m = 9 in [−2,2] (all 715 multisets) | 3,575 | 0 / 0 / 0 | 1 − 2·10⁻¹⁰ | |
| A1b: m = 10 in [−2,2], 86/1001 multisets (time cap), k ≤ 3 | 688 | 0 / 0 / 0 | 1 − 2·10⁻¹⁰ | 5 cases at (2,5) over the edge cap for YPQx only (YP, YPQ ran, feasible) |

The `free` rule (supply ≤ capacity, i.e. Q_w ≤ 1) never failed either. With round 4's 13,661 + 2,707 cases, YP is now
feasible on every one of ≈ 35,700 (instance, k, t) cases with t + 2k ≤ m that have been tried, including the dense
two- and three-valued shapes that were the most likely place for a counterexample. The round-4 caveat is closed.

## B. Task 2 — the base case k = 1 of YP-Hall

### B.1 What YP-Hall says at k = 1 (PROVED reductions; each checked numerically to 10⁻¹³ in A2)

Fix w and 2 ≤ t ≤ m/2. Group the elements into *classes* c of equal weight, n_c = |c|, r = #classes. For a t-set X
write j_c(X) = |X ∩ c| and f(X) for the number of t-sets with the same sum. For p ∈ c put N_p = Σ_{X ∋ p} 1/f(X);
N_p is constant on classes (a transposition of two equal weights preserves every sum), call it N_c, and
M_c := n_c N_c = Σ_X j_c(X)/f(X) = mult_w(w_c). Write C := C(m−1, t−1) = #{t-sets through a fixed element}.

**(R1)** Q_w(t,1) = Σ_c M_c² / (t s_t C) and Σ_c M_c = t s_t (Σ_X t/f(X) = t · #sums). Hence
  **Q_w(t,1) ≤ 1 ⟺ Σ_c M_c (M_c − C) ≤ 0** ⟺ the M-weighted mean of M_c is at most C.
Probabilistic form: with ξ(c) = M_c/(t s_t) — the probability that a uniformly random element of a *sum-uniform*
random t-set (a t-sum chosen uniformly, then a t-set with that sum uniformly) lies in class c —
Q_w(t,1) ≤ 1 ⟺ Σ_c ξ(c)² ≤ 1/(m a_t): the collision probability of the class of a sum-uniform t-set is at most
1/(m a_t). Since Σ_c ξ(c)² ≥ 1/r this contains a_t ≤ r/m = a_1 (M′ at k = 1), as it must.

**(R2) The k = 1 charging problem.** A near miss at k = 1 is (X, {p}, {p′}) with p ≠ p′ ∈ X, w_p = w_{p′}
(B = {p′} ∩ X ≠ ∅ forces p′ ∈ X), aggregated supply N_c/f(X). The total supply at p (class c) is
  S_p = N_c Σ_{X ∋ p} (j_c(X) − 1)/f(X),
zero for singleton classes. A target is (Y, Y*, {d}): w(Y) = w(Y*), Y ≠ Y*, d ∈ Y, Y∖Y* ≠ {d}, capacity N_d/f(Y).
Merging the targets of one collision set Y, and using #{Y* : Y∖Y* = {d}} = #{d′ ~ d, d′ ∉ Y} = n_{c(d)} − j_{c(d)}(Y):
  cap(Y) = Σ_c N_c j_c(Y) (f(Y) − 1 − n_c + j_c(Y)) / f(Y),   every term ≥ 0 by (R4).
Identity: Σ_p S_p − Σ_Y cap(Y) = Σ_c N_c Σ_X j_c(X)(n_c − f(X))/f(X) = Σ_c N_c (n_c M_c − n_c C) = Σ_c M_c (M_c − C),
using Σ_X j_c(X) = n_c C. So at k = 1 the round-3 reduction "Q_w ≤ 1 ⟺ supply ≤ capacity" is a one-line identity.

**(R3) YP-Hall at k = 1 is a transportation problem on classes.** The YP neighbourhood of (X, {p}, {p′}) is
{targets with Y ∋ p}: it depends on p only. So YP-Hall(k = 1) says: *element p has demand S_p and may use the
collision sets Y ∋ p, of capacity cap(Y)*; for every R ⊆ [m],
  S(R) := Σ_{p∈R} S_p ≤ K(R) := Σ_{Y collision set, Y ∩ R ≠ ∅} cap(Y).
F(R) = K(R) − S(R) is submodular (coverage minus modular) and invariant under G = Π_c Sym(c). If F(R) < 0 for some
R, take a minimiser R; gR is one too, F(R ∪ gR) ≤ 2F(R) − F(R ∩ gR) ≤ F(R), so R ∪ gR is a minimiser, and iterating,
the union of the classes that R meets is a minimiser. Hence
  **YP-Hall(k = 1) ⟺ for every set U of classes of size ≥ 2: Σ_{c∈U} n_c S_c ≤ Σ_{Y : Σ_{c∈U} j_c(Y) ≥ 1} cap(Y)**
(singletons add no supply). Caution, learned from the control in A2: this is a statement about *violations*; the
*minimum* of F over all R is in general attained at a single element, not at a class (e.g. (−2,−2,0,2,2,3), t = 3:
40 at one element of the pair, 50 for the pair). The pre-registration stated the stronger, false version; the
correct one above is all that is needed.

**(R4) Where the excess comes from.** C = Σ_X j_c(X)/n_c, so
  M_c − C = Σ_X j_c(X) (n_c − f(X)) / (n_c f(X)).
The orbit G·X lies in the fiber of X, so f(X) ≥ Π_c C(n_c, j_c(X)), and C(n, j) ≥ n for 1 ≤ j ≤ n − 1. So a positive
term needs j_c(X) = n_c and f(X) < n_c: **a class is over-represented (M_c > C) only if the whole class sits inside
some t-set whose sum has fewer than n_c witnesses**; in particular n_c ≤ t, and singletons are never over-represented.
Corollary (PROVED): if no class is over-represented, Σ_c M_c² ≤ C Σ_c M_c = C t s_t, i.e. Q_w(t,1) ≤ 1. The whole
content of Conjecture Q at k = 1 is therefore the compensation of the over-represented classes by the others, and
YP-Hall(k = 1) asks for that compensation to be available on the collision sets that meet them.

### B.2 Two families PROVED at k = 1 (A2b checks the closed forms exactly up to m = 40)

**(F1) Two-valued instances w = 0^a 1^b, a ≤ b, 2 ≤ t ≤ m/2.** The fibers are the orbits j = j_0(X) ∈ [0, min(a,t)]
(t ≤ m/2 ≤ b), s = min(a,t) + 1, f = C(a,j)C(b,t−j), N_0 = (1/a)Σ_j j, so M_0 = Σ_j j and M_1 = t s − M_0.
If a ≥ t: M_0 = M_1 = t(t+1)/2 and Σ M² ≤ C t s ⟺ t(t+1)/2 ≤ C(m−1,t−1), true for m ≥ 2t since
C(2t−1,t−1) ≥ t(t+1)/2 (induction on t: the left ratio 2(2t+1)/(t+1) dominates the right ratio (t+2)/t for t ≥ 1),
with equality iff a = b = t = 2 — the known equality case (0,0,1,1). If a < t: M_0 = a(a+1)/2,
M_1 = (a+1)(2t−a)/2, the inequality reads (a+1)(a² + (2t−a)²)/4 ≤ C(m−1,t−1) t, and since a ≤ t − 1 the left is
≤ t(4t² − 4t + 2)/4 while C(2t−1,t−1) ≥ t² − t + 1/2 for t ≥ 2, strictly. ∎
**Q_w(t,1) ≤ 1 for every two-valued instance and every 2 ≤ t ≤ m/2, with equality only at (0,0,1,1), t = 2.**
(4,940 cases with a + b ≤ 40 checked exactly: 0 violations, the single equality case.)

**(F2) One repeated class plus generic values, w = 0^n g_1 … g_G, m = n + G, 2 ≤ t ≤ m/2.** Two t-sets have the
same sum iff they have the same generic part, so with u_j = C(G, t−j), 0 ≤ j ≤ min(n,t): s = Σ u_j, f = C(n,j),
M_0 = Σ_j j u_j, and each generic class has M_g = Σ_j C(G−1, t−1−j) =: N_g. The inequality is
M_0² + G N_g² ≤ C t s, i.e. M_0 (M_0 − C) ≤ G N_g (C − N_g). For n = 2: M_0 − C = C(G,t−2), C − N_g = C(G−1,t−2),
G C(G−1,t−2) = (t−1) C(G,t−1), and the claim is (C(G,t−1) + 2C(G,t−2)) C(G,t−2) ≤ (t−1) C(G,t−1) N_g. At t = 2 it
is G + 2 ≤ G², true for G ≥ 2 with equality at G = 2 (the equality case (0,0,g1,g2)); for t ≥ 3, G ≥ 2t − 2 gives
C(G,t−2) ≤ C(G,t−1)(t−1)/t, the left is ≤ C(G,t−1)²(t−1)(3t−2)/t² and the right ≥ (t−1)C(G,t−1)². ∎
**Q_w(t,1) ≤ 1 for one pair of equal values among generic values, all t ≤ m/2; equality only at (0,0,g1,g2).**
For n ≥ 3 the same reduction gives an explicit binomial inequality, checked exactly for all n + G ≤ 40 (9,329 cases,
0 violations, the single equality case), not proved. Observation worth keeping (PROVED by the formula): at n = 2,
t = 2 the ratio Σ M²/(C t s) = (G³ + G² + 4G + 4)/(G³ + 2G² + 3G + 2) = 1 − (G−2)(G+1)/((G+1)(G²+G+2)) → 1 as
G → ∞ (0.976 at m = 40): **a single repeated pair among generic weights is asymptotically tight for Conjecture Q at
(k,t) = (1,2)**; the excess of the pair, M_0 − C = 1, comes from the one t-set {0,0′} (f = 1 < n = 2) and is matched
by the deficits C − N_g = 1 of the generics, each sitting on the two-element fibers {0,g} ~ {0′,g}.

### B.3 The data at k = 1 (A2: 8,894 cases, m = 6, 7 exhaustive in [−3,3], m = 8, 9 exhaustive in [−2,2], all t ≤ m/2)

| quantity | m = 6 | m = 7 | m = 8 | m = 9 |
| --- | --- | --- | --- | --- |
| Hall failures (min over class unions < 0; Dinic YP flow < 1) | 0 | 0 | 0 | 0 |
| cases with an over-represented class (O ≠ ∅) | 192 | 14 | 0 | 0 |
| of those, tight set U* = O exactly | 192 | 14 | — | — |
| max over U of S(U)/K(U) (Hall ratio) | 0.545 | 0.385 | 0.286 | 0.207 |
| max load of the explicit proportional map (p → Y ∋ p ∝ cap(Y)) | 0.818 | 0.574 | 0.361 | 0.288 |
| max Q_w(t,1) | 0.867 | 0.786 | 0.643 | 0.563 |
| cases with slack(w) < slack(profile model of the same class sizes) | 9 | 349 | 677 | 1229 |

Readings. (i) YP-Hall holds at k = 1 on every case (EVIDENCE), with much room: the Hall ratio is ≤ 0.55 and
decreases with m; the tight cases are two classes of size 2 at t = m/2 (e.g. (−1,−1,1,2,3,3), t = 3: U* = both
pairs, ratio 6/11). (ii) **Whenever an over-represented class exists, the tight set is exactly the set of
over-represented classes** (206/206; sharper than the pre-registered "contains"). In [−2,2] at m = 8, 9 no class is
over-represented at all — too many coincidences — so there the inequality is the trivial corollary of (R4). (iii) The
explicit proportional map is a valid certificate at k = 1 in every case (max load 0.82; it fails at k = 2, load
1.126, reproduced as a control). So at k = 1 the natural candidate for a *closed-form* proof is
  **Prop-1 (CONJECTURE):** for every collision set Y, Σ_{p∈Y} S_p / K_p ≤ 1, where K_p = Σ_{Y′ ∋ p, collision} cap(Y′),
which implies YP-Hall(k = 1). Its per-element strengthening t S_p ≤ K_p is false (at (0,0,g1,g2), t = 2: S_0 = 2,
K_0 = 2), so Prop-1 genuinely needs the singletons in Y, which contribute 0 to the sum. (iv) The pre-registered
hypothesis "extra coincidences only help at k = 1" (the profile model with generic class values is extremal for its
class sizes) is FALSE: 1,264 counterexamples, e.g. (−3,0,0,0,0,3), t = 2 (slack 13.59 vs 16 for 0⁴g²). So Conjecture Q
at k = 1 does not reduce to the combinatorial profile inequality Σ_c J_c² ≤ C t s₀; merging fibers changes
Σ_c M_c(M_c − C) in both directions.

### B.4 Why the general k = 1 case does not close (the exact obstruction)

What has to be proved is, by (R3), for every union U of classes of size ≥ 2:
  Σ_{c∈U} N_c Σ_X j_c(X)(j_c(X) − 1)/f(X) ≤ Σ_{Y meets U} Σ_{c′} N_{c′} j_{c′}(Y)(f(Y) − 1 − n_{c′} + j_{c′}(Y))/f(Y),
and the data say the binding U is the set O of over-represented classes. By (R4) the left side exceeds the
own-class part of the right side exactly by Σ_{c∈U} N_c Σ_{X ⊇ c, f(X) < n_c} n_c (n_c − f(X))/f(X): the excess is
produced by whole classes sitting in t-sets with few witnesses (in the tight families, in a unique-sum t-set,
f(X) = 1). It has to be paid by the *other* classes' terms on collision sets Y that merely contain an element of c:
for a singleton class {q} that term is N_q (f(Y) − 1)/f(Y), and Σ_{Y ∋ q} N_q(f(Y) − 1)/f(Y) = N_q (C − N_q) is
exactly N_q times the deficit of q. So the inequality is a transfer: the excess of the over-represented classes
against the deficits of the under-represented ones, restricted to the collision sets through O. The three facts that
block a proof are:
1. **No local inequality.** The only general lower bound on f is the orbit bound f(X) ≥ Π_c C(n_c, j_c(X)); it is
   tight precisely in the profile model, and the profile model is *not* extremal (B.3 (iv)), so one cannot replace f
   by the orbit size and prove a combinatorial statement — the sign of the correction is instance-dependent.
2. **The transfer is not fiber-local or orbit-local.** In (F2) the pair's excess lives on the fiber of {0,0′} while
   the compensating deficits live on the fibers {0,g} ~ {0′,g}, g generic — different sums, related only through
   the element 0. Any charging that stays within a fiber, an orbit, or a relation fails (this is the k = 1 shadow of
   the round-4 min-cut obstruction: unique-sum t-sets versus many-witness collisions).
3. **The certificate is not closed-form in general.** The proportional map works on all 8,894 cases (B.3 (iii)) but
   its validity, Prop-1, is itself a sum over the elements of each collision set Y of ratios S_p/K_p whose numerators
   and denominators are sums over different t-sets through p; I found no inequality that bounds it except in (F1)
   and (F2), where the fibers are explicit.
What *is* available: the full reduction (R1)–(R4), the exact tight-set structure (U* = O), the two proved families,
and a one-parameter family that is asymptotically tight ((0,0,g^G), t = 2), which any proof must handle with no
slack to spare. The statement to prove next is Prop-1 at k = 1 for instances with a single over-represented class
(a pair) and arbitrary other classes — the smallest case beyond (F2) that is not covered.

### B.5 What an induction k → k + 1 would need (PROVED bookkeeping, no proof)

Let ℓ = (X, X′, A, A′) be a level-(k+1) near miss with i = |A ∩ A′| ≥ 1. For each a ∈ A ∩ A′, (X, X′, A∖a, A′∖a) is a
level-k near miss with the same P, Q, the same t-sets and the same weight 1/(f(X)f(X′)), and the YP condition
Y ⊇ P is unchanged. Conversely a level-k near miss ℓ₀ lifts in λ(ℓ₀) := |(X ∩ X′) ∖ (A₀ ∪ A₀′)| ways, each lift having
|A₀ ∩ A₀′| + 1 parents. A level-k target r₀ = (Y, Y*, Y″, D₀) lifts by d ∈ (Y ∩ Y″)∖D₀ unless (Y∖Y*)∖D₀ = {d}, i.e. in
μ(r₀) := |Y ∩ Y″| − k − [|(Y∖Y*)∖D₀| = 1] ways, each lift having k + 1 parents. Hence the level-(k+1) YP-Hall
condition is equivalent to: for every set S of level-(k+1) near misses,
  w(S ∩ {A ∩ A′ = ∅}) + Σ_{ℓ₀ ∈ S↓} w(ℓ₀) λ(ℓ₀)/(|A₀∩A₀′| + 1) ≤ Σ_{r₀ ∈ N_YP(S)↓} w(r₀) μ(r₀)/(k + 1),
where S↓, N↓ are the level-k projections. So the induction needs two things that YP-Hall at level k does not give:
(I1) a *weighted* YP-Hall at level k with the intersection-size weights λ(ℓ₀) on near misses and μ(r₀) on targets —
these depend on |X ∩ X′| and |Y ∩ Y″|, so the weights are no longer products 1/(f(X)f(X′)) and the aggregation over X′
and Y″ that made every level computable (ROUND4 §A.1) is lost; and (I2) a separate treatment of the new near misses
with A ∩ A′ = ∅, i.e. |P| = |Q| = k + 1 — exactly the full-relation near misses that the round-4 min-cut showed must be
charged to collisions through an unrelated balanced pair. At k = 1 → 2, (I2) is the whole of the (−3,−3,−2,−2,0,3,3)
difficulty (there the proportional certificate already fails), so the base case, even if proved via Prop-1, would
not propagate without a new idea for (I2).

## C. Task 3 — hill-climb at m = 18, 20 in the window k < m/3

Two runs (A3 `hill5.py`, A3b `hill5b.py`), single-coordinate hill-climbs with random restarts, objective the max of
Q_w over the pairs (k, k+1) with the two largest k in the window ((4,5), (5,6) at m = 18; (5,6), (6,7) at m = 20),
the full window pair list evaluated for the top instances; seeds: the generic-padded {0,1,5} shapes of round 4 and
random starts. Controls: the same climbers restricted to (m/2 − 1, m/2) must find the known violations — they do,
1.0236 at (18; 8,9) and 1.0240 at (20; 9,10) (round 4's maximiser 0⁶1⁴5⁶ + 4g), within one restart.

**A3 (free moves: any value in [−3,6] or a fresh generic value).** 38,431 evaluations at m = 18, 7,842 at m = 20.
No Q_w > 1. The pre-registered prediction "best ≤ 0.85" failed for a reason the pre-registration overlooked:
generic weights give Q_w = 1 exactly at every (k,t), so a climber that accepts non-decreasing moves drifts from every
seed to a generic instance ((−2,1,3,5) + 14g at m = 18, (0,1,3,5) + 16g at m = 20: 1.0000 at every window pair) and
then wanders among generic instances. What this run does establish (EVIDENCE): no single-coordinate perturbation of
a generic instance exceeds 1 in the window at m = 18, 20; the best non-generic instances are a single repeated pair
among generics ((0,1,1,3,6) + 15g at m = 20: 0.9987 at (6,10), 0.96–0.98 at the other window pairs), exactly the
asymptotically tight family (F2) of §B.2. Round 4's window maxima (0.70) were lower only because its families
excluded near-generic instances.

**A3b (palette only: g ∈ {0, 4} generic entries fixed, every other value in [−3,6], so the instance carries ≥ 4
coincidences and cannot become generic).** 15,934 + 16,648 evaluations at m = 18, 3,472 + 3,379 at m = 20.

| m | g | best Q_w (pair) | maximiser | full window list of the maximiser |
| --- | --- | --- | --- | --- |
| 18 | 0 | 0.610 (5,6) | 0⁶ 1⁵ 6⁷ | (4,5) 0.50, (4,6..9) ≤ 0.30, (5,7..9) ≤ 0.44 |
| 18 | 4 | 0.713 (5,6) | (−3)⁵ 0² 5² 6⁵ + 4g | (4,5) 0.63, (4,9) 0.45, (5,9) 0.67 |
| 20 | 0 | 0.625 (6,7) | (−2)⁷ 1⁵ 4 5⁷ | (5,6) 0.52, (6,10) 0.38 |
| 20 | 4 | 0.705 (6,7) | (−3)⁶ 2 5⁴ 6⁵ + 4g | (5,6) 0.62, (6,10) 0.64 |

No Q_w > 1; the predictions "no violation", "best < 1, with g = 4, at the largest allowed k with t = k + 1" and
"g = 0 best ≤ 0.90" were met; the sub-prediction "the maximiser is as near-generic as the palette allows" failed:
every maximiser is three- or four-valued (large classes plus the generics), because additional distinct small values
bring arithmetic coincidences (0 + 6 = 1 + 5, …) that lower Q_w.

Verdict for the window (EVIDENCE, m = 18, 20): the supremum of Q_w over k < m/3 is 1, attained only by generic
instances and approached from below by one repeated pair among generic values; structured instances stay ≤ 0.72
(≈ 0.70 in round 4); violations remain confined to k = m/2 − 1, t = m/2. The honest statement of Conjecture Q for
k < m/3 is therefore "Q_w ≤ 1 with equality exactly for generic weights", and any proof must be tight at the generic
instance and asymptotically tight on (0,0,g^G) at (1,2).

## D. Dead ends (kept, with the reason)

1. **"The minimum of the Hall slack over all R is attained at a union of classes"** (pre-registered as (R3)): false;
   the lattice argument needs F(∅) ≥ min, i.e. a violation. Caught by the all-subsets control in A2 on every case.
   The corrected statement (violations occur at unions of classes) is what the reduction needs.
2. **Profile-model extremality** ("extra coincidences only help at k = 1"): false, 1,264 counterexamples at m ≤ 9.
   This closes the route "prove the combinatorial inequality Σ_c J_c² ≤ C t s₀ on compositions, then monotonicity".
3. **Per-element bound t S_p ≤ K_p** as a proof of the proportional certificate: false at the equality case
   (0,0,g1,g2) — the certificate needs the zero-supply singletons inside Y.
4. **Own-class capacity** (charging the excess of class c only to the c-terms of cap(Y)): impossible by (R4) — the
   own-class terms cancel the supply exactly up to the positive excess, which must come from other classes.
5. **Fiber-local or orbit-local charging at k = 1**: the k = 1 shadow of the round-4 obstruction; the excess and its
   compensation live on different sums ((F2)).
6. **The free hill-climb as a window test**: its objective is maximised by generic instances (Q_w = 1 at every (k,t)),
   so it cannot explore the structured region; kept because it shows single-coincidence perturbations of generic
   instances do not exceed 1. Replaced by the palette-only climb.

## E. Labels

PROVED: the collapsed-flow identity (A.1); the k = 1 reductions (R1)–(R4) and the corollary "no over-represented
class ⟹ Q_w(t,1) ≤ 1"; Q_w(t,1) ≤ 1 for all two-valued instances (F1) and for one repeated pair among generic
values (F2, n = 2), with their equality cases; the asymptotic tightness of (0,0,g^G) at (1,2); the lifting
bookkeeping of B.5.
EVIDENCE: YP-Hall on all 137 dense cases, the 3 curated m = 9 instances and 19,278 further cases (0 failures);
YP-Hall at k = 1 on 8,894 cases with U* = O; the proportional certificate at k = 1 (max load 0.82); (F2) for
n ≥ 3 up to m = 40; no Q_w > 1 in the window at m = 18, 20 in 85,000 climb evaluations, structured instances ≤ 0.72.
CONJECTURE: YP-Hall (unchanged); Prop-1 at k = 1; in the window the supremum of Q_w is 1, attained only by generic instances (Q_w = 1 exactly) and approached by one pair among generics.
NOT OBTAINED: a proof of YP-Hall or of Conjecture Q at k = 1 in general.

## F. Next steps (in order of expected value)

1. Prove Prop-1 (hence YP-Hall) at k = 1 for instances with exactly one over-represented class, which by (R4) is a
   class of size n ≤ t contained in a few-witness t-set; start with n = 2 (a pair) and arbitrary other classes — the
   smallest open case beyond (F2), and the asymptotically tight one.
2. Compute, at k = 1, the Hall ratio and U* on targeted families with several over-represented classes (two or
   three pairs among generics, m ≤ 12) to see whether U* = O persists and how the ratio approaches 1; this decides
   whether the k = 1 proof can be organised class-by-class.
3. For (I2) of B.5, test at k = 2 whether the full-relation near misses (A ∩ A′ = ∅) alone satisfy a YP-Hall
   condition against the targets *not* used by the lifted level-1 near misses (a decomposition of the k = 2 flow);
   if they do, the induction has a chance; if not, write the min-cut.
4. The window is settled as far as hill-climbing can settle it; a further test with value would be the two-pair and
   three-pair families among generics at m = 14–20, k = 1, 2 (where (F2) says the single pair is asymptotically
   tight) to see whether several pairs can push Q_w above 1 at small k — the only structured candidates left.
5. Do not spend more compute on the gap or on dense m ≤ 10 cases: Task 1 is settled for m ≤ 9 in the tested ranges.

## G. Files

`ROUND5_REPORT.md` (this file); `scripts/round5/PREREG_R5.md` (all pre-registrations and outcomes, including the failed
predictions and the mis-stated reduction); `scripts/round5/README.md`; `scripts/round5/flow5.py` (collapsed flow,
memory guard, Hall violator); `charge_flow5.py`, `charge_flow5b.py` (Task 1); `k1_hall.py`, `k1_families.py`
(Task 2); `hill5.py` (Task 3). Outputs in `scripts/round5/out/`. ROUND4_REPORT.md edited only as described in Task 0.
