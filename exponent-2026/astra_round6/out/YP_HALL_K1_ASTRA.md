# YP-Hall at k=1 — Astra, round 6

**PROVED — New result in this report: YP-Hall holds for k=1, t=2, for every integer-weight instance with m≥4. Consequently Q_w(2,1)≤1 without any genericity or restriction on additive coincidences.** A proof is given below; finite searches are not its justification.

**NOT CHECKED — A proof or counterexample for all 3≤t≤m/2 was not obtained.** The deliverable gives an exact residual transportation problem isolating the remaining difficulty, a stronger combinatorial sufficient condition, and a precise counterexample to a natural spectral strengthening. The spectral counterexample is NOT a counterexample to YP-Hall or Q_w.

EVIDENCE — Folder B was first opened after REFEREE_SECTION_T.md and BASE_CORE_ASTRA.md were written; the gate is recorded in REGISTER.md. The B reports were used for definitions of near misses, targets, Q_w, and the transportation formulation. Their numerical claims were not imported as evidence. All calculations reported here use newly written yp_k1.py, profile_obstruction.py, and b_examples.py.

## Definitions and independently checked reductions

PROVED — Let classes c consist of equal-weight indices, with sizes n_c. For a t-set X put j_c(X)=|X∩c| and f(X)=#{X′: |X′|=t, w(X′)=w(X)}. Define

    N_c = sum_{X containing p} 1/f(X),  p∈c,
    M_c = n_c N_c = sum_X j_c(X)/f(X),
    C = binom(m−1,t−1),     s_t = number of distinct t-sums.

PROVED — N_c is independent of the choice of p by permuting equal-weight indices. Summing over classes gives sum_c M_c=t s_t. From the definition of the canonical sum-uniform sampling law,

    Q_w(t,1) = sum_c M_c² / (C t s_t),
    Q_w(t,1)≤1  iff  sum_c M_c(M_c−C)≤0.

EVIDENCE — Source definitions: ROUND3_REPORT.md:84–108; ROUND4_REPORT.md:30–38; ROUND5_REPORT.md:80–108. The equalities below are re-derived, not accepted on the reports' authority.

PROVED — For k=1 a near miss is (X,{p},{p′}) with p≠p′ in X of the same weight, after summing out its independent X′. Its supply is N_c/f(X). Its YP neighbors are exactly the targets based at sets Y containing p. Summing over X,p′ gives element demand

    S_p = N_c sum_{X containing p} (j_c(X)−1)/f(X).

PROVED — A target based at Y and marked d∈Y has (f(Y)−1) possible partners Y*, except that partners differing only by replacing d with an equal-weight outside index are disallowed. There are n_c−j_c(Y) excluded partners. Summing out Y″ gives

    cap(Y) = sum_c N_c j_c(Y)[f(Y)−1−n_c+j_c(Y)]/f(Y).

PROVED — Each coefficient is nonnegative: the excluded swaps are distinct members of the fiber other than Y. Summing supply minus capacity gives

    sum_p S_p − sum_Y cap(Y)
      = sum_c N_c sum_X j_c(X)[n_c−f(X)]/f(X)
      = sum_c M_c(M_c−C).

PROVED — YP-Hall asks S(R)≤K(R)=sum_{Y:Y∩R≠∅}cap(Y) for every subset R of indices. It is enough to test unions of repeated classes. Indeed F(R)=K(R)−S(R) is submodular and invariant under permutations within each class. If a negative minimizer exists, both it and every permutation of it minimize F. Submodularity shows their union is also a minimizer. Union over the finite permutation group produces a negative minimizer that is a class union. Removing singleton classes cannot increase F since they have zero demand. This is an argument about a negative minimizer; it need not identify a nonempty minimizer when no violation exists, since the empty set already has value zero.

## Theorem: YP-Hall for k=1, t=2

PROVED — Fix m≥4. Every near miss has X={p,p′} inside a single class c. Write f_c=f(2w_c). Its two oriented sources have total supply 2N_c/f_c at this X. The entire target capacity at the same Y=X is

    cap(X) = 2N_c(f_c−n_c+1)/f_c.

PROVED — If f_c≥n_c, this capacity serves both sources at X, using valid YP edges because both p and p′ belong to X. A class of size at least three automatically has f_c≥binom(n_c,2)≥n_c. A class of size two with f_c≥2 also qualifies. Perform these local assignments independently at each same-class two-set. They use only same-class target sets and cannot conflict across X.

PROVED — The only sources left are classes of size two with f_c=1. Call these isolated pairs. At each of their two elements p the remaining demand is N_c, so the class demand is 2N_c. All cross-class target capacities remain unused. It suffices to prove Hall for this residual system. By class symmetry, test unions U of isolated-pair classes.

PROVED — If U contains q≥2 classes, consider only two-sets Y with one element from each of two distinct classes c,d in U. Each such sum has at least four witnesses, so

    cap(Y) = (N_c+N_d)(1−2/f(Y)) ≥ (N_c+N_d)/2.

PROVED — There are four such sets for each unordered pair c,d. Their total capacity, summed once over unordered class pairs, is at least

    2 sum_{c<d in U}(N_c+N_d)
       = 2(q−1) sum_{c in U}N_c
       ≥ 2 sum_{c in U}N_c,

PROVED — which covers the residual demand of U. These are valid collisions, and every target set used meets U.

PROVED — Now suppose U={c} is one isolated pair, and there is some other repeated class d of size n_d≥2. For a cross set Y={p∈c,q∈d}, the fiber has at least 2n_d witnesses. Thus

    cap(Y) = N_c(1−2/f(Y)) + N_d(1−n_d/f(Y))
            ≥ N_c(1−1/n_d) + N_d/2.

PROVED — Summing its first term alone over the 2n_d cross sets gives at least 2(n_d−1)N_c≥2N_c. This covers the singleton class cut. These cross targets were not consumed by the local assignments, even if class d's sources were already served locally.

PROVED — It remains to handle exactly one repeated class, an isolated pair, with G=m−2≥2 distinct other weights. Shift all weights so the pair is (0,0); shifting preserves every fixed-layer equality. Write the other weights as distinct nonzero g_1,…,g_G, set f_i=f(g_i), and write N_i for each singleton's N. Then f_i≥2 and

    N_0 = 1 + sum_i 1/f_i ≤ (G+2)/2.

PROVED — The initial 1 is the unique pair {0,0}, since isolation means f(0)=1. Let s be the number of distinct two-sums. The G+1 sums 0,g_1,…,g_G occur, and there is at least one more. If G≥3, two g's have the same sign; the two most extreme of that sign sum outside the range of all g's. If G=2 and they have the same sign, the same argument works; if they have opposite signs, g_1+g_2 is neither g_i and cannot be 0 by isolation. Hence s≥G+2.

PROVED — For each i there are two cross target sets {0,g_i}, each of capacity

    N_0(1−2/f_i) + N_i(1−1/f_i).

PROVED — Denote the total capacity of these cross sets by K. Since sum_i N_i=2s−2N_0 and f_i≥2,

    K/2
      = N_0(G+2−2N_0) + sum_i N_i(1−1/f_i)
      ≥ N_0(G+2−2N_0) + s−N_0
      = s + N_0(G+1−2N_0).

PROVED — The right side is at least N_0: this is equivalent to s≥N_0(2N_0−G). If the factor 2N_0−G is negative the claim is immediate; otherwise it is at most 2, and N_0≤(G+2)/2, so the product is at most G+2≤s. Thus K≥2N_0, proving the final Hall cut.

PROVED — Every residual class-union cut is feasible, so the finite weighted Hall theorem gives a residual fractional flow. Together with the local assignments this proves YP-Hall. No assumption on extra additive coincidences was made. The proof implies Q_w(2,1)≤1 via the supply-capacity identity. It uses t=2 essentially: near misses then live in same-class pairs, and local reservations leave all cross-class target sets untouched.

## Independent check of Q_w(2,1) without using the flow theorem

PROVED — Let r be the number of classes and h=m−r. A singleton class has M_c≤r−1; a repeated class has M_c≤r+1. To see this, enumerate two-element class profiles: a cross profile contributes at most one to M_c, and a double-c profile contributes at most two. Each orbit's size divided by its entire fiber size is at most one.

PROVED — If h=0, M_c≤m−1=C for every class. If h≥2, r+1≤m−1=C, so again every class has M_c≤C. Only h=1, one repeated pair and G=m−2 singletons, remains. If M_0≤C the result is immediate. If M_0>C=G+1, the pair sum must be unique: a nonunique pair sum contributes at most one instead of two, forcing M_0≤G+1. By the argument above, s≥G+2, M_0≤G+2, and every singleton M_i≤G. Therefore

    sum_i M_i(C−M_i) ≥ sum_i M_i = 2s−M_0 ≥ 2(G+2)−M_0.

PROVED — Since M_0>G+1 and M_0≤G+2,

    M_0(M_0−C) − [2(G+2)−M_0]
      = M_0(M_0−G)−2(G+2) ≤ 0.

PROVED — Hence the repeated pair's excess is paid by singleton deficits. This second proof checks the numerical conclusion independently of the detailed transportation construction.

## Exact remaining obstruction for t≥3: residual full-class demands

PROVED — At any t, the sum of source demands based at X and with removed element in class c is

    L_c(X)=N_c j_c(X)(j_c(X)−1)/f(X).

PROVED — The part of cap(X) whose mark d belongs to c is

    R_c(X)=N_c j_c(X)[f(X)−1−n_c+j_c(X)]/f(X).

PROVED — All these source nodes can use all these target nodes under YP at Y=X. Reserve min(L_c(X),R_c(X)) for them and split it evenly among the j_c(X) present source elements. Different (X,c) reservations use disjoint marked target groups. The residual demand, for each p in c, is

    E_p=N_c sum_{X containing p} (n_c−f(X))_+/f(X),

PROVED — and the remaining capacity at Y is

    B(Y)=sum_c N_c j_c(Y)(f(Y)−n_c)_+/f(Y).

PROVED — If n_c−f(X)>0 and j_c(X)>0, then j_c(X)=n_c: the class-permutation orbit has at least binom(n_c,j_c(X))≥n_c elements whenever 0<j_c(X)<n_c. Thus every residual source is a full-class, low-multiplicity fiber. This is a precise concentration of the unresolved demand, not an assertion that only globally over-represented classes can have residual sources.

CONJECTURE — Residual-Hall: for every union U of repeated classes,

    sum_{c in U} sum_{p in c} E_p
      ≤ sum_{Y: Y meets U} B(Y).

PROVED — Residual-Hall is sufficient for YP-Hall by extending the local reservations. It has NOT been shown necessary; a different feasible YP flow could reroute capacity already reserved locally. Any failure of Residual-Hall would therefore be an obstruction to this construction, not automatically an obstruction to YP-Hall. The same submodularity argument reduces its cuts to class unions.

PROVED — The missing step is a bound on these cross-fiber residual cuts. A naive per-fiber bound is false: with w=(0,0,1,4,16,64), t=3, each set consisting of the zero pair and one other element has f=1 and positive residual supply, while its own target capacity is zero. Exact enumeration gives Q=14/15 and class Hall ratio 2/3; the instance is feasible only by moving mass to other fibers. B_EXAMPLES.json includes every target and capacity, so this obstruction is inspectable rather than qualitative.

## A stronger combinatorial route and an exact failed spectral shortcut

PROVED — Let J(n,t) be all vectors j=(j_c) with 0≤j_c≤n_c, integral, and sum j_c=t. Each profile has orbit size O_j=prod_c binom(n_c,j_c). All of its subsets share a sum, with full fiber size f_j≥O_j. Put θ_j=O_j/f_j∈(0,1]. Then

    s_t=sum_j θ_j,       M=sum_j θ_j j.

CONJECTURE — The following stronger, weight-independent inequality would prove Q_w(t,1) in general:

    ||sum_{j in F} j||_2² ≤ t*binom(m−1,t−1)*|F|
    for every subfamily F of J(n,t), when 2≤t≤m/2.

PROVED — This subset inequality would imply the same inequality for every θ∈[0,1]^J, including the actual fiber coefficients: the function ||sum θ_j j||²−tC sum θ_j is convex, and its maximum on the cube is attained at a vertex. Equivalently, independently select profiles with probabilities θ_j and apply Jensen plus the subset bound. This route drops all additive consistency between different profile sums, so it is stronger than the original problem; failure of it would not disprove Q_w.

PROVED — A tempting sufficient spectral estimate DOES fail already at m=4,t=2,n=(2,1,1). The profiles are (2,0,0),(1,1,0),(1,0,1),(0,1,1). For θ=(1,3/5,3/5,1/5),

    M=(16/5,4/5,4/5),
    ||M||²=288/25 > 264/25 = tC sum θ_j².

PROVED — The correct desired right side is tC sum θ_j=72/5, which exceeds 288/25. Thus the profile matrix is not an l2 contraction at the required constant. The l1 budget and the box constraint θ≤1 cannot be discarded. This is an exact obstruction to a natural proof strategy, with rational certificate in B_EXAMPLES.json; it is explicitly not an integer-weight counterexample.

## Computations, controls, and dead ends

| Status | Experiment | Result |
|---|---|---|
| PROVED | Required negative control, w=(−3,−3,−2,−2,0,0), k=2,t=3 | Q=29/28; near-miss supply 30; target capacity 27; even unrestricted routing reaches at most 9/10. It is not charged. Direct exact enumeration, B_CONTROLS.json. |
| PROVED | Equality controls, (0,0,1,4) and (0,0,1,1), k=1,t=2 | Q=1 and exact class-union Hall ratio=1. |
| PROVED | Generic powers-of-ten control | Q=1, no repeated-class source demand. |
| EVIDENCE | Actual-weight search | 3371 cases; no Q, YP-Hall, Residual-Hall, or Prop-1 failure. Every tested cut and ratio used exact rational arithmetic. B_SEARCH.json. |
| EVIDENCE | Stronger profile-subfamily search | 503 small profile families exhaustively checked, 3,627,047 nonempty subset checks; additional larger families received deterministic seeded local search. No violation found. PROFILE_OBSTRUCTION.json. This does not prove the conjecture. |
| PROVED | Spectral-shortcut control | The rational strict inequality above fails the stronger l2 estimate while satisfying the desired l1 inequality. |

EVIDENCE — The actual-weight generator exhausts m=4,…,8 on the five-value palette {−2,−1,0,1,2}, with 2≤t≤m/2, then runs the stated curated cases and 600 fixed-seed random/structured cases up to m=12. These are finite tests only; full generator details are in yp_k1.py. Its run finished in under 16 seconds, before the 110-second cutoff. The profile experiment finished in under ten seconds, before its 45-second cutoff. No computation used parallel numerical processes.

EVIDENCE — Retained dead ends: (1) local same-fiber charging is obstructed by unique full-class sets; (2) the spectral contraction is false by the exact example; (3) the stronger residual-flow test did not produce the predicted possible obstruction, so it remains only a sufficient conjectural route; (4) the profile search found no obstruction and supplies evidence, not a proof; (5) its initial success branch failed to save counters, so the unchanged search was rerun after fixing that logging branch. All predictions and outcomes are preserved in REGISTER.md.

NOT CHECKED — Neither the uniform-in-t theorem nor an actual k=1 counterexample has been obtained. In particular the forbidden k=2 instance cannot be promoted into a k=1 counterexample, and the t=2 proof does not extend automatically: for t≥3 a target set can contain several classes' local sources, so reservations can consume capacity needed by another class. A human expert should examine the Residual-Hall inequality and the profile-subfamily conjecture as distinct potential routes.
