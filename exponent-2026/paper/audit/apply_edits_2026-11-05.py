# Applies Edits 1-5 (preprint/drafts/SECTION10_UPDATE_DRAFT.md), the restructured Section 10 [S] subsection and the
# verification ledger to paper.tex. Written 2026-11-05 by Claude. Backup: paper_2026-11-04_2049_backup.tex.
# Every anchor must occur exactly once, or nothing is written.
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'paper.tex'
s = open(P, encoding='utf-8').read()
orig = s

def rep(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit('ANCHOR COUNT %d: %r' % (n, old[:90]))
    s = s.replace(old, new)

# ---------- Edit 5(d): abstract ----------
rep(r"so running time $O(2^{0.4875755n})$",
    r"so randomized running time $O(2^{0.4875755n})$ on inputs of polynomial bit length")

# ---------- intro: pointer to the ledger ----------
rep(r"Floating results are evidence, not proof.",
    r"Floating results are evidence, not proof. Section~11 lists, claim by claim and premise by premise, how each was checked.")

# ---------- Edit 4: certified status, Base core ----------
rep(r"two independent referees; conditional on Base's written proof and the OpenAI proof.",
    r"two independent referees; conditional on Base's written proof and the OpenAI proof. Base's probabilistic core (Lemma A5, Corollary D and the region analysis of its Theorem B) was re-derived independently; one repairable step was found, which our point satisfies (Section~11).")

# ---------- Edit 3: conditional status ----------
rep(r"33 conditions certified in arb; written proof (Section~T) reviewed; [S] unproved; an independent referee of the point is pending.",
    r"33 conditions certified in arb; written proof (Section~T) reviewed and independently refereed; [S] unproved (Section~10 reduces it to a chain of combinatorial statements and records what is proved).")

# ---------- Edit 5(a): computational setting ----------
rep("\\section{The OpenAI architecture and its parameter budget}\n\n",
    "\\section{The OpenAI architecture and its parameter budget}\n\n"
    r"Throughout, running times are for randomized algorithms that answer correctly with probability at least $2/3$, in the word-RAM model of the OpenAI paper, on inputs whose integers and target have bit length $b \le n^c$ for an arbitrary fixed $c$; the constant in the $O(\cdot)$ depends on $c$. This is the setting of the OpenAI and Base theorems, and every bound below inherits it."
    "\n\n")

# ---------- Edit 5(b): theorems ----------
rep(r"With the parameters below, the OpenAI algorithm decides Subset Sum in time",
    r"With the parameters below, the OpenAI algorithm (randomized, word-RAM, inputs of bit length at most $n^c$ for any fixed $c$) decides Subset Sum in time")
rep(r"Subset Sum can be solved in time $O(2^{T' n})$ for every $T' > 0.4873407528$",
    r"Subset Sum can be solved by a randomized word-RAM algorithm, on inputs of bit length at most $n^c$ for any fixed $c$, in time $O(2^{T' n})$ for every $T' > 0.4873407528$")

# ---------- Edit 5(c): Section 8 caveats ----------
rep(r"so the algorithm runs in time $O(2^{T' n})$ for every $T' > T$",
    r"so, in the setting of Section~2, the algorithm runs in time $O(2^{T' n})$ for every $T' > T$")

# ---------- Edit 5(e): fresh referee of the conditional point ----------
rep(r"recomputed every slack and both moments with independent code; the moments agree to 20 digits.",
    r"recomputed every slack and both moments with independent code; the moments agree to 20 digits. A fresh referee, working only from the candidate file, Section~T and the Base and OpenAI sources, derived its own list of conditions with line citations and certified both moments with its own interval code, bounding the quadrature error analytically (a trapezoid bound on a strip of analyticity); its enclosures agree with ours to 35 digits. It found no fatal defect, only expository repairs to Section~T, including the bit-length scope of Section~2.")

# ---------- Edit 3: Section 8 conditional sentence ----------
rep(r"We present it as conditional until [S] is proved and the point has been checked by an independent referee.",
    r"We present it as conditional until [S] is proved.")

# ---------- Edit 1: Section 9 ternary paragraph ----------
rep(r"In the floating model this reaches $\tau_0 = 0.4873404$",
    r"In the floating model this reaches $\tau_0 = 0.4873403$")
rep(r"We count this as a negative result and leave the stronger lemma open (Section~10).",
    r"Under Base's Corollary D we therefore count ternary masks as a negative result. Under the stronger statement [S] of Section~8 they give the conditional theorem stated there ($T = 0.4873407528$); [S] is open (Section~10).")

# ---------- Edit 2: Section 10 item, then the new [S] subsection ----------
start = s.index(r"So it suffices that small layers are robust:")
end = s.index("\n", start)
assert s.count(r"So it suffices that small layers are robust:") == 1
s = s[:start] + r"So it suffices that small layers are robust, which is the statement [S] of Section~8; the subsection below reduces it to a chain of purely combinatorial statements and records what is proved." + s[end:]

S_SUB = r"""\subsection*{The small-layer statement [S] behind the conditional exponent}

The conditional exponent of Section~8 needs [S] only at $k' = k_1 + k_2 \approx 0.0070m$; Section~8 states it for $k \le 0.11m$ because that is the range reached by the reduction below. Base's Corollary D and its size conditions are then not needed, and its cost bounds still hold if $\mu < l$. Write $s_j$ for the number of distinct $j$-subset sums of the block and $a_j = s_j/\binom{m}{j}$. The table lists a chain of statements, each of which would imply the one above it, and the status of each; the paragraphs after it give the definitions and the evidence.

\begin{center}
\small
\begin{tabularx}{\linewidth}{>{\raggedright\arraybackslash}p{2.6cm} L >{\raggedright\arraybackslash}p{4.7cm}}
\toprule
Statement & Content & Status \\
\midrule
{[S]} & $a_k \ge 2^{-d(M)}/C_S(m)$ for every weighting and $k \le 0.11m$ & Open; $a_k\,2^{d(M)} \ge 1.00$ in all 2,655 tested instances ($m = 12$ to $16$) \\
{Lemma S} & M$'$ with constant $P(m)$ implies [S] with $C_S = P + 2$ & Proved \\
{Exact monotonicity} & $a_{k+1} \le a_k$ for $k + 1 \le m/2$ & False (130 counterexamples at $m = 8$, all at the middle step) \\
{Conjecture M$'$} & $a_t \le P(m)\, a_k$ for $t \in [k, m-k]$, $k \le 0.11m$ & Open; proved with a loss of about $2^k$ (Proposition P2) \\
{Conjecture Q} & $Q_w(t,k) \le 1$ for $k \le m/4$; implies M$'$ with $P = 1$ & Open; no violation for $k < m/3$ in about $10^5$ instances; false at $k = m/3$ \\
{YP-Hall} & a Hall condition for $t + 2k \le m$; implies Conjecture Q & Open; feasible in about 35,700 exact flow computations \\
{Case $k = 1$} & $Q_w(t,1) \le 1$ & Proved for $t = 2$ and for two families of weights; open for $t \ge 3$ \\
\bottomrule
\end{tabularx}
\end{center}

\emph{Lemma S.} If $a_t \le P(m)\, a_k$ for all $t \in [k, m-k]$ and $k \le 0.11m$, then [S] holds with $C_S = P + 2$. Indeed $2^{-d(M)} \le \E_{t\sim\mathrm{Bin}(m,1/2)}[a_t]$, since $|\Sigma| \le \sum_t |\Sigma_t|$; the layers inside $[k, m-k]$ contribute at most $P a_k$, and the layers outside carry mass at most $2\cdot 2^{-m(1-h(\alpha))}$ with $\alpha = k/m$, which is at most $2a_k$ because $a_k \ge 1/\binom{m}{k} \ge 2^{-mh(\alpha)}$ and $h(\alpha) \le 1/2$ for $\alpha \le 0.11$.

\emph{Exact monotonicity fails, but only at the middle.} An exhaustive sweep over all value multisets in $[-8, 8]$ at $m = 8$ finds 130 counterexamples to $a_{k+1} \le a_k$, all at the middle step $k + 1 = m/2$, for example $w = (-6, -5, -5, -3, -3, -2, 4, 5)$ with $a_3 = 19/56 < a_4 = 24/70$ (verified independently). Away from the middle the comparison looks exact: in exhaustive sweeps at $m = 9$ to 12 (about 11 million multisets) the maximum of $a_t$ over $t \ge k$ was attained at $t = k$ for every $k \le m/4$. The tight cases are sharp: with half the weights equal to 1 and half to 2, $a_k/a_{k+1} = (m - k)/(k + 2)$, exactly 1 at $k = m/2 - 1$. Monotonicity also has an exact combinatorial form: the map $(y, e) \mapsto (e, y - w_e)$ is a bijection between pairs with $y$ a $(k+1)$-sum and $e$ in the union $U(y)$ of its witness sets, and pairs with $x$ a $k$-sum and $e$ outside the intersection $C(x)$ of its witness sets, so $a_k \ge a_{k+1}$ is equivalent to $\sum_y (|U(y)| - (k+1)) \ge \sum_x (k - |C(x)|)$ (verified on 39 instances).

\begin{proposition*}[P2]
For $k \le t \le m - k$, $s_t\binom{t}{k} \le s_k\binom{m}{t-k}$, that is, $a_t \le a_k\,\binom{m}{t-k}\big/\binom{m-k}{t-k}$.
\end{proposition*}
Fix one witness $X_y$ for each $t$-sum $y$; the map $(y, A) \mapsto (w(A), X_y \setminus A)$ over $k$-subsets $A \subseteq X_y$ is injective. The loss is about $2^k$ at $t = m/2$; it is exactly the support barrier $m/2 + k$ of Base's Corollary D seen as a statement about layers. At $k = 0.007m$ it costs about $0.0033$ in the exponent, fourteen times the ternary gain, so the application needs the comparison essentially without loss. M$'$ is trivial for bounded $k$ ($P = \binom{m}{k}$); its content is $k \to \infty$ with $m$.

\emph{A sharper target.} Draw a $t$-sum $y$ uniformly, a witness $X$ of $y$ uniformly, and a uniform $k$-subset $A \subseteq X$, and let $\mu$ be the law of $w(A)$. By Cauchy--Schwarz $s_k \ge 1/\mathrm{cp}(\mu)$, where $\mathrm{cp}$ is the collision probability, so $Q_w(t,k) := \mathrm{cp}(\mu)\, a_t \binom{m}{k} \le 1$ implies $a_t \le a_k$. Always $Q_w \ge a_t/a_k$, with $Q_w = 1$ for generic weights.

\begin{conjecture*}[Q]
$Q_w(t,k) \le 1$ for all integer weightings, $k \le m/4$ and $k < t \le m/2$.
\end{conjecture*}
With $s_t = s_{m-t}$ this gives $a_t \le a_k$ on all of $[k, m-k]$, hence M$'$ with $P = 1$ and [S] with $C_S = 3$. The range is part of the statement: $Q_w$ exceeds 1 at $k = m/3$ ($w = (-3,-3,-2,-2,0,0)$ at $(k,t) = (2,3)$: $Q_w = 29/28$) and at the middle step ($1.079$ for the $m = 8$ counterexample above). Below $m/3$ we found no violation: exhaustive in $[-3,3]$ for $m \le 10$, about $10^5$ random instances, targeted two- and three-valued families up to $m = 20$, and hill-climbs at $m = 18$ and 20 whose controls recover the known middle-step violations. In these searches the supremum of $Q_w$ for $k < m/3$ is 1, attained by generic weights and approached by a single repeated pair among generic values; every few-valued instance stays below 0.72.

\emph{A charging formulation.} $Q_w \le 1$ is equivalent to a weighted inequality between \emph{near misses} (a $t$-set $X$ and two $k$-sets $A \subseteq X$, $A' \ne A$ with $w(A) = w(A')$ and $A' \setminus A$ meeting $X$) and \emph{collisions} of $t$-sets. Call the rule YP: a near miss may be charged to any collision whose $t$-set contains $A \setminus A'$.

\begin{conjecture*}[YP-Hall]
For $t \le m/2$ and $t + 2k \le m$, the Hall condition of the bipartite charging rule YP holds.
\end{conjecture*}
By max-flow/min-cut it is equivalent to a fractional charging map, and it implies $Q_w \le 1$ on $t + 2k \le m$, which with the symmetry above covers the range $k \le m/4$ of Conjecture~Q. Exact max-flow computations found the rule feasible in every one of about 35,700 (instance, $k$, $t$) cases with $t + 2k \le m$ that we tried (exhaustive in $[-3,3]$ for $m \le 8$ and in $[-2,2]$ for $m = 9$, partial at $m = 10$, and the dense two- and three-valued shapes), while the control $(-3,-3,-2,-2,0,0)$ at $(2,3)$, outside the range, stays infeasible. Rules that keep the relation $(A \setminus A', A' \setminus A)$ fail, and the natural closed-form (proportional) map exceeds load 1 on one instance at $m = 7$, so the certificate is a flow, not a formula.

\begin{proposition*}[the case $k = 1$]
Group the elements into classes of equal weight, with sizes $n_c$, and put $M_c = \sum_X |X \cap c|/f(X)$, the sum over $t$-sets $X$, where $f(X)$ is the number of $t$-sets with the same sum as $X$. Then $Q_w(t,1) \le 1$ if and only if $\sum_c M_c (M_c - C) \le 0$, where $C = \binom{m-1}{t-1}$. The inequality holds
(i) for $t = 2$ and every integer weighting with $m \ge 4$, and so does YP-Hall;
(ii) for every two-valued weighting and every $2 \le t \le m/2$, with equality only at $(0,0,1,1)$, $t = 2$;
(iii) for one repeated pair among generic values and every $2 \le t \le m/2$, with equality only at $(0,0,g_1,g_2)$, $t = 2$.
\end{proposition*}
A class can be over-represented ($M_c > C$) only if the whole class lies in a $t$-set whose sum has fewer than $n_c$ witnesses, so the content of the case $k = 1$ is that such excesses are paid by the deficits of the other classes. For (i), comparing each orbit of class profiles with its fiber gives $M_c \le r - 1$ for a singleton class and $M_c \le r + 1$ for a repeated class, where $r$ is the number of classes. So every $M_c \le m - 1 = C$ unless exactly one pair of weights coincides and its sum is unique; then the pair has $M_0 \le m$, each singleton has $M_i \le m - 2$, there are at least $m$ distinct 2-sums, and the singletons' deficits $\sum_i M_i (C - M_i) \ge \sum_i M_i \ge 2m - M_0$ pay the pair's excess $M_0(M_0 - C)$. Family (iii) is asymptotically tight at $(k,t) = (1,2)$ as the number of generic values grows, so any proof must handle it with no slack. All three parts were also checked by exhaustive computation from the definition of $Q_w$ (for (i), 59,408 instances up to $m = 14$; maximum exactly 1). The case $k = 1$, $t \ge 3$ is open. The obstruction is that the excess of an over-represented class must be paid by deficits on collisions of \emph{different} sums that merely share an element of the class, so no charging that stays inside a fiber or an orbit suffices; an induction from $k$ to $k + 1$ would also need a weighted form of YP-Hall and a separate treatment of near misses with $A \cap A' = \emptyset$.

\subsection*{The checksum side and other questions}

"""
anchor = "\\textbf{A large-deviation form of the moment conditions.}"
assert s.count(anchor) == 1
s = s.replace(anchor, S_SUB + anchor)

# theorem environments for the new statements
rep("\\newtheorem*{theorem*}{Theorem}",
    "\\newtheorem*{theorem*}{Theorem}\n\\newtheorem*{proposition*}{Proposition}\n\\newtheorem*{conjecture*}{Conjecture}")

# ---------- Use of AI tools and Files ----------
rep(r"and Claude Fable 5.1 as the second independent referee and later as a collaborator on the ternary alias step.",
    r"and Claude Fable 5.1 as the second independent referee, as a collaborator on the ternary alias step and on the reduction of [S] (Conjecture~Q, the charging formulation and the families of the case $k = 1$), and for one re-derivation of Base's probabilistic core. Astra also refereed the ternary point and Section~T, gave a second re-derivation of Base's core, and proved part~(i) of the case $k = 1$; a further fresh Claude context re-derived Corollary D from its statement alone.")
rep(r"and the Section~9 experiments C13--C17.",
    r"and the Section~9 experiments C13--C17; the later work (the ternary alias step and its referee reports, the re-derivations of Base's core and the evidence for Section~10) is in \texttt{round2\_fable}, \texttt{fable\_round3\_6}, \texttt{lab\_notebook\_round3\_6} and \texttt{astra\_round6}.")

# ---------- Verification ledger (end of Section 11) ----------
LEDGER = r"""
\subsection*{Verification ledger}
For each claim and each premise, the table records how it was checked. ``Re-derived'' means an independent written proof compared afterwards with the source; ``read'' means checked only by reading.

\begin{center}
\small
\begin{tabularx}{\linewidth}{>{\raggedright\arraybackslash}p{4.3cm} L >{\raggedright\arraybackslash}p{2.5cm}}
\toprule
Claim or premise & How it was checked & Status \\
\midrule
The 33 numerical conditions of the Section~8 point (0.4875754036), including both moments & Ball arithmetic with analytic quadrature error bounds; two independent referees, each deriving the conditions from the \TeX{} and recomputing with its own code & Certified \\
The 16-block point of Section~7 (0.4894615727) & Two independent rigorous certificates; block-count audit & Certified \\
Lemma~1 and the blocking of 0.48 (Section~5) & Written proof; independent referee; interval evaluation & Proved \\
The 430 moment premises of the 0.487676 bound (Section~3) & Ball arithmetic by two routes; outside check & Certified \\
The 33 numerical conditions of the conditional point (0.4873407528) & Ball arithmetic; independent recomputation (moments agree to 20 digits); fresh referee with its own condition list and interval code (35 digits) & Certified \\
The ternary alias step (Section~T) & Written proof in Base's style; co-author review; fresh referee: no fatal defect, expository repairs only & Refereed; needs [S] \\
Base: Lemmas 3.1--3.3 and Corollary D & Two independent re-derivations (each had seen part of Base's proof of Corollary D) and a third from the statements alone, without Base's proof; all agree with Base & Re-derived \\
Base: Lemma A5 and the region analysis of Theorem B & Two independent re-derivations (one had seen Base's bad-set step); one repairable step, Lemma B2's row error, which needs $a_\Gamma \le 3/4$ (ours is about 0.0625) & Re-derived \\
Base: the rest of the proof (preliminary search, alias-step cost accounting, checksum changes) & Read; the referees derived its numerical conditions from the text & Premise \\
OpenAI: isolation, the alias lemmas, alias subtraction, finite-circle convergence, word-RAM accounting & Read & Premise \\
The floor $(1 - \Delta)/2$ and the closed-form bounds (Section~9) & Exact algebra on Base's constraints; numbers from pre-registered floating runs & Floating \\
The joint capacity near 0.029 and the negative results of Section~9 & Pre-registered floating optimization with controls & Floating \\
{[S]} and the chain of Section~10 & Partial proofs; exhaustive, random and adversarial searches with controls & Open \\
\bottomrule
\end{tabularx}
\end{center}
"""
anchor = "\\end{itemize}\n\n%======================================================================\n\\begin{thebibliography}"
assert s.count(anchor) == 1, s.count(anchor)
s = s.replace(anchor, "\\end{itemize}\n" + LEDGER + "\n%======================================================================\n\\begin{thebibliography}")

open(P, 'w', encoding='utf-8').write(s)
print('OK: %d -> %d characters' % (len(orig), len(s)))
