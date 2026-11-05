# Draft: Section 10 (and two small Section 8/9) updates for paper.tex
Prepared 2026-11-04 ~21:50 ET by Claude. paper.tex was NOT edited (Jennifer is collecting changes).
Sources: Fable ROUND3/4/5 reports, Claude REVIEW_OF_ROUND3.md, SECTION_T_v2.md, candidate_ternary.json,
ternary_floating_optimum.json. Every number below was copied from those files. The [ASTRA-B] slot is now filled (Astra's t = 2 theorem,
checked in C3_target_048_Claude/round6/REVIEW_OF_ASTRA_ROUND6_B.md). Paper hygiene: no model names, rounds, folders or "tonight" in the TeX.

---------------------------------------------------------------------------------------------------------
## Edit 1 — Section 9, line 430 (ternary paragraph): harmonize with Section 8
The floating optimum is tau0 = 0.48734025 (ternary_floating_optimum.json). Line 430 says 0.4873404, line 444 says
0.4873403; both round upward, but they should match. Proposed:

OLD: In the floating model this reaches $\tau_0 = 0.4873404$, $2.35\times10^{-4}$ below our point, from four of four starts;
NEW: In the floating model this reaches $\tau_0 = 0.4873403$, $2.35\times10^{-4}$ below our point, from four of four starts;

OLD (last sentence): We count this as a negative result and leave the stronger lemma open (Section~10).
NEW: Under Base's Corollary D we therefore count ternary masks as a negative result. Under the stronger statement [S] of
Section~8 they give the conditional theorem stated there ($T = 0.4873407528$); [S] is open (Section~10).

---------------------------------------------------------------------------------------------------------
## Edit 2 — Section 10, item "Corollary D beyond the half-block" (line 444)
Replace everything from "So it suffices that small layers are robust:" to the end of the item with the text below.
(The part before it — the family {U}, the support m/2 + k, the sumset remark, the counting identity — stays.)

```latex
So it suffices that small layers are robust, which is the statement [S] of Section~8. The application uses it only at $k' = k_1 + k_2 \approx 0.0070m$; Section~8 states it for $k \le 0.11m$ because that is the range reached by the reduction below. Base's Corollary D and its size conditions are then not needed, and its cost bounds still hold if $\mu < l$. Under [S] the frozen point of Section~8, with $k_1 = k_2 \approx 0.0035m$, gives the conditional exponent $T = 0.4873407528$. Directly, [S] holds with margin in every structured family we tested ($a_k\,2^{d(M)} \ge 1.00$ in all 2,655 instances with $m = 12$ to $16$), and an adversarial search found no counterexample, but it is not proved. In expectation it holds with a large margin, because a small layer sees every additive relation less often than the half-cube does. A swap argument reduces it to a lower-tail concentration bound for a sum of mixed cylinder events (bits required to be 1 on one set and 0 on another), to which the standard Janson inequality does not directly apply.

\emph{From [S] to layer comparison.} Write $s_j$ for the number of distinct $j$-subset sums and $a_j = s_j/\binom{m}{j}$. It suffices to compare layers: if $a_t \le P(m)\, a_k$ for all $t \in [k, m-k]$ and $k \le 0.11m$ (Conjecture M$'$), then [S] holds with $C_S = P + 2$, because $2^{-d(M)} \le \E_{t\sim\mathrm{Bin}(m,1/2)}[a_t]$ (since $|\Sigma| \le \sum_t |\Sigma_t|$) and the layers outside $[k, m - k]$ carry mass at most about $2^{-m(1-h(\alpha))}$, which $a_k \ge 1/\binom{m}{k}$ absorbs when $\alpha \le 0.11$. Exact monotonicity $a_k \ge a_{k+1}$ is false: an exhaustive sweep over all value multisets in $[-8, 8]$ at $m = 8$ finds 130 counterexamples, all at the middle step $k + 1 = m/2$, for example $w = (-6, -5, -5, -3, -3, -2, 4, 5)$ with $a_3 = 19/56 < a_4 = 24/70$ (verified independently). Away from the middle the comparison looks exact: in exhaustive sweeps at $m = 9$ to 12 (about 11 million multisets) the maximum of $a_t$ over $t \ge k$ was attained at $t = k$ for every $k \le m/4$. The tight cases are sharp: with half the weights equal to 1 and half to 2, $a_k/a_{k+1} = (m - k)/(k + 2)$, exactly 1 at $k = m/2 - 1$.

\emph{What is proved.} M$'$ holds with an exponential loss: for $k \le t \le m - k$,
\[ s_t \binom{t}{k} \le s_k \binom{m}{t-k}, \qquad\text{that is,}\qquad a_t \le a_k \,\binom{m}{t-k}\Big/\binom{m-k}{t-k}. \]
(Fix one witness $X_y$ for each $t$-sum $y$; the map $(y, A) \mapsto (w(A), X_y \setminus A)$ over $k$-subsets $A \subseteq X_y$ is injective.) The loss is about $2^k$ at $t = m/2$, which is exactly the support barrier $m/2 + k$ of Base's Corollary D seen as a statement about layers; at $k = 0.007m$ it costs about $0.0033$ in the exponent, fourteen times the ternary gain, so the application needs the comparison essentially without loss. M$'$ is trivial for bounded $k$ ($P = \binom{m}{k}$); its content is $k \to \infty$ with $m$.

\emph{A sharper target.} Draw a $t$-sum $y$ uniformly, a witness $X$ of $y$ uniformly, and a uniform $k$-subset $A \subseteq X$, and let $\mu$ be the law of $w(A)$. By Cauchy--Schwarz $s_k \ge 1/\mathrm{cp}(\mu)$, where $\mathrm{cp}$ is the collision probability, so
\[ Q_w(t,k) := \mathrm{cp}(\mu)\, a_t \binom{m}{k} \le 1 \quad\Longrightarrow\quad a_t \le a_k . \]
Always $Q_w \ge a_t/a_k$, with $Q_w = 1$ for generic weights. \textbf{Conjecture Q.} $Q_w(t,k) \le 1$ for $k \le m/4$ and $k < t \le m/2$. With $s_t = s_{m-t}$ this gives $a_t \le a_k$ on all of $[k, m-k]$, hence M$'$ with $P = 1$ and [S] with $C_S = 3$. The range is part of the statement: $Q_w$ exceeds 1 at $k = m/3$ ($w = (-3,-3,-2,-2,0,0)$ at $(k,t) = (2,3)$: $Q_w = 1.036$) and at the middle step ($1.079$ for the $m = 8$ counterexample above). Below $m/3$ we found no violation: exhaustive in $[-3,3]$ for $m \le 10$, about $10^5$ random instances, targeted two- and three-valued families up to $m = 20$, and hill-climbs at $m = 18$ and 20 whose controls recover the known middle-step violations. In these searches the supremum of $Q_w$ for $k < m/3$ is 1, attained by generic weights and approached by a single repeated pair among generic values; every few-valued instance stays below 0.72.

\emph{A charging formulation.} $Q_w \le 1$ is equivalent to a weighted inequality between \emph{near misses} (a $t$-set $X$ and two $k$-sets $A \subseteq X$, $A' \ne A$ with $w(A) = w(A')$ and $A' \setminus A$ meeting $X$) and \emph{collisions} of $t$-sets. We conjecture that the charging can be made local: a near miss may be charged to any collision whose $t$-set contains $P = A \setminus A'$. \textbf{Conjecture YP-Hall.} For $t \le m/2$ and $t + 2k \le m$ the Hall condition of this bipartite charging rule holds. By max-flow/min-cut it is equivalent to a fractional charging map, and it implies $Q_w \le 1$ on $t + 2k \le m$, which with the symmetry above covers Conjecture Q's range $k \le m/4$. Exact max-flow computations found the rule feasible in every one of about 35,700 (instance, $k$, $t$) cases with $t + 2k \le m$ that we tried (exhaustive in $[-3,3]$ for $m \le 8$ and in $[-2,2]$ for $m = 9$, partial at $m = 10$, and the dense two- and three-valued shapes), while the control $(-3,-3,-2,-2,0,0)$ at $(2,3)$, outside the range, stays infeasible. Rules that keep the relation $(A \setminus A', A' \setminus A)$ fail, and the natural closed-form (proportional) map exceeds load 1 on one instance at $m = 7$, so the certificate is a flow, not a formula.

\emph{The case $k = 1$.} Group the elements into classes of equal weight $c$ of size $n_c$, and put $M_c = \sum_X |X \cap c|/f(X)$, the sum over $t$-sets $X$, where $f(X)$ is the number of $t$-sets with the same sum as $X$. Then $Q_w(t,1) \le 1$ is equivalent to $\sum_c M_c (M_c - C) \le 0$ with $C = \binom{m-1}{t-1}$. A class can be over-represented ($M_c > C$) only if the whole class lies in a $t$-set whose sum has fewer than $n_c$ witnesses; if no class is over-represented the inequality holds. We prove it for every two-valued instance (equality only at $(0,0,1,1)$, $t = 2$) and for one repeated pair among generic values (equality only at $(0,0,g_1,g_2)$, $t = 2$, and asymptotically tight as the number of generic values grows). For $t = 2$ it holds for all weights, and so does the Hall condition of the charging rule: a class can be over-represented only if it is a pair whose sum is unique, and that excess is then paid by the deficits of the singletons. The general case $k = 1$, $t \ge 3$, is open; the obstruction is that the excess of an over-represented class must be paid by deficits on collisions of \emph{different} sums that merely share an element of the class, so no fiber-local or orbit-local charging suffices. An induction from $k$ to $k+1$ would need a weighted form of YP-Hall at level $k$ and a separate treatment of near misses with $A \cap A' = \emptyset$.
```

---------------------------------------------------------------------------------------------------------
## Edit 3 — Status (line 121): READY (Astra's A1 = PASS WITH REPAIRS, all expository; reviewed in C3_target_048_Claude/round6/REVIEW_OF_ASTRA_ROUND6_A.md)
OLD: 33 conditions certified in arb; written proof (Section~T) reviewed; [S] unproved; an independent referee of the point is pending.
NEW: 33 conditions certified in arb; written proof (Section~T) reviewed and independently refereed; [S] unproved (Section~10 reduces it to Conjecture Q and gives the evidence).
Also Section 8, line 366: "We present it as conditional until [S] is proved and the point has been checked by an
independent referee." -> "We present it as conditional until [S] is proved." (A1 has passed, so this applies now.)

## Edit 4 — Status, Base-core re-derivations (optional; wording must reflect the exposure)
Both independent re-derivations of Base's core saw the Corollary D case split (Base l.260-267) before writing, and
Astra also saw the A4/A5 good-set lines (473-482); a third, fully blind re-derivation of Corollary D was then done
(C3_target_048_Claude/round6/blind_corD). Honest wording if used:
"Base's Lemmas 3.1--3.3, Corollary D and Lemma A5 were re-derived in two independent written reconstructions, which
found one repairable step (Lemma B2's per-row error bound; the stated list holds under $a_\Gamma \le 3/4$, which our
certificate checks) and no gap affecting our point. A third reconstruction of Corollary D, from the statements alone
without sight of Base's proof, agrees with Base's argument step for step."
(Comparison done: the two reconstructions agree item by item and found the B2 issue independently; see
REVIEW_OF_ASTRA_ROUND6_A.md. The wording above is accurate as it stands.)

---------------------------------------------------------------------------------------------------------
## Edit 5 — computational model and bit-length scope (from Astra's A1; CONFIRMED against the sources)
OpenAI (main.tex l.47): "worst-case running time O(2^{0.49n}) on polynomial-bit inputs in a word-RAM model".
Base Theorem 1 (l.58-66): randomized, correct with probability ≥ 2/3, word-RAM, "every input with n ≥ N_c and b ≤ n^c".
paper.tex never says "randomized" and gives no model or bit-length scope in any theorem. Proposed:

(a) Section 2, first paragraph (or a footnote at the first time bound in the Introduction), one sentence:
```latex
Throughout, running times are for randomized algorithms that answer correctly with probability at least $2/3$, in the word-RAM model of the OpenAI paper, on inputs whose integers and target have bit length $b \le n^c$ for an arbitrary fixed $c$; the constant in the $O(\cdot)$ depends on $c$. This is the setting of the OpenAI and Base theorems, and every bound below inherits it.
```
(b) Section 7 theorem (l.276) and Section 8 theorem (l.362): after "decides Subset Sum" / "Subset Sum can be solved",
insert "(randomized, word-RAM, inputs of bit length at most $n^c$ for any fixed $c$)".
(c) Section 8 "Status and caveats" (l.368): after "so the algorithm runs in time $O(2^{T' n})$" insert
"in the setting of Section~2".
(d) Abstract, first result sentence: "so running time $O(2^{0.4875755n})$" -> "so randomized running time
$O(2^{0.4875755n})$ on polynomial-bit inputs".
(e) Section 8, conditional paragraph (after "the moments agree to 20 digits.", l.358): add
```latex
A fresh referee, working only from the candidate file, Section~T and the Base and OpenAI sources, derived its own list of conditions with line citations and certified both moments with its own interval code, bounding the quadrature error analytically (a trapezoid bound on a strip of analyticity) rather than by comparing resolutions; its enclosures agree with ours to 35 digits. It found no fatal defect, only expository repairs to Section~T, including the bit-length scope above.
```
