# Revision of paper.tex in response to Astra's round-8 referee report (R1-R26), 2026-11-05, Claude.
# Every anchor must occur exactly once or nothing is written. Backup: preprint/drafts/paper_before_round8_2026-11-05.tex
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('ANCHOR COUNT %d (want %d): %r' % (n, count, old[:100]))
    s = s.replace(old, new)

def between(start, end, new, keep_end=True):
    """replace text from start (inclusive) up to end (exclusive if keep_end)"""
    global s
    assert s.count(start) == 1, ('start', start[:80], s.count(start))
    i = s.index(start)
    j = s.index(end, i)
    s = s[:i] + new + (s[j:] if keep_end else s[j + len(end):])

# ---------------------------------------------------------------- preamble, title
rep(r"\newtheorem*{theorem*}{Theorem}",
    "\\newtheorem*{theorem*}{Theorem}\n\\newtheorem{theorem}{Theorem}\n\\newtheorem{proposition}{Proposition}\n\\newtheorem{conjecture}{Conjecture}")
rep("pdftitle={A certified 0.48758 for worst-case Subset Sum, and why the alias-checksum architecture stalls near 0.4876}",
    "pdftitle={A certified exponent of 0.48758 for worst-case Subset Sum, and limits of the alias-checksum analysis}")
rep(r"\title{A certified 0.48758 for worst-case Subset Sum, and why the alias--checksum architecture stalls near 0.4876}",
    r"\title{A certified exponent of 0.48758 for worst-case Subset Sum, and limits of the alias--checksum analysis}")
rep(r"\date{Draft, 4 November 2026}", r"\date{Draft, 5 November 2026}")

# ---------------------------------------------------------------- abstract (R1, R12, R23)
between(r"\begin{abstract}", r"\end{abstract}", r"""\begin{abstract}
Worst-case Subset Sum fell below the meet-in-the-middle exponent $1/2$ in October 2026, with OpenAI's $2^{0.49n}$ algorithm and Ye and Li's $2^{(1/2 - 1/450000)n}$. We study the OpenAI approach and its modification by A.~Kapila (``Base''), which reached 0.4877; a retuning of Base by JoshuaQFEX reached 0.487676. Conditional on the written proofs of OpenAI and Base, we give a parameter point with threshold $T = 0.4875754036$: for every fixed $T' > T$, the resulting randomized algorithm runs in time $O(2^{T'n})$ on inputs of polynomial bit length, in particular $O(2^{0.4875755n})$, about $1.0\times10^{-4}$ below JoshuaQFEX. A single asymmetric filter with 16 cosine and 16 sine terms replaces Base's family of 43 filters, and all 33 numerical conditions of Base's proof, including both filtering moments, are certified in interval arithmetic by independent implementations. Within the original OpenAI construction we also certify a 16-block point at 0.4894616 and the 430 moment premises of the JoshuaQFEX bound.

We also study what limits this line of work. We prove a lower bound on the first filtering moment, valid for every filter, which shows that the sufficient conditions of the original OpenAI proof cannot be met at any exponent $\tau \le 0.484$, for any choice of parameters. Base's alias constraints reduce to three closed-form bounds that explain the costs at our point. One of them gives a counting floor: an alias-enumeration phase that faces $2^{(1-\eta-o(1))n}$ alias classes, combined with a checksum of capacity $\Delta$, needs exponent at least $(1 - \Delta)/2$, about 0.4857 at the best capacity we found (about 0.029, not proved optimal). Finally, we isolate a combinatorial statement about subset-sum layers that would give the threshold 0.4873407528, prove special cases of it, and state the remaining open questions.
""", keep_end=True)

# ---------------------------------------------------------------- introduction opening (R1, R12)
between(r"Worst-case Subset Sum fell below the meet-in-the-middle exponent $1/2$ in October 2026. This paper asks",
        r"\subsection*{The problem in brief}",
r"""Worst-case Subset Sum fell below the meet-in-the-middle exponent $1/2$ in October 2026. This paper asks how far one of the two new approaches, OpenAI's, can be pushed: we improve the best exponent in that line of work (Theorem~\ref{thm:main} below), explain what limits it near 0.4876, and state the open problems that would move it further. Two of our results concern the analysis as a whole rather than one parameter point (the terms are explained below). A lower bound on the first filtering moment, valid for every filter, shows that the sufficient conditions of the original OpenAI proof cannot be met at any exponent up to 0.484 (Section~5). And an alias-enumeration phase that faces about $2^{(1-\eta)n}$ alias classes, combined with a checksum of capacity $\Delta$, needs exponent at least $(1 - \Delta)/2$, about 0.4857 at the best capacity found so far (Section~9). We begin with background for readers outside the area.

""")

# ---------------------------------------------------------------- related work (R suggestions)
rep(r"Schroeppel and Shamir~\cite{ss} kept the time and reduced the memory to about $2^{n/4}$.",
    r"Schroeppel and Shamir~\cite{ss} kept the time and reduced the memory to about $2^{n/4}$; Nederlof and W\k{e}grzycki~\cite{nw} gave the first improvement of that memory bound, combining it with the representation technique below.")
rep(r"after their work on average-case subset balancing problems~\cite{cjrs22}.",
    r"after their work on average-case subset balancing problems~\cite{cjrs22}. Earlier, Austrin, Kaski, Koivisto and Nederlof~\cite{akkn} gave faster-than-meet-in-the-middle algorithms for instances whose largest number of subsets with a common sum is either small or very large, a parameter closely related to the deficiency used below.")

# ---------------------------------------------------------------- main theorem up front (R6)
rep(r"Base keeps this architecture but changes the list side (one large shared block with sparse masks) and uses a family of 43 filters.",
r"""Base keeps this architecture but changes the list side (one large shared block with sparse masks) and uses a family of 43 filters.

\subsection*{The main result}
\begin{theorem}[main result]\label{thm:main}
Assume the non-numerical lemmas of the OpenAI paper~\cite{openai} and of Base's written proof~\cite{base}. Then there is a uniform randomized algorithm for Subset Sum in the word-RAM model that halts on every execution and answers correctly with probability at least $2/3$, and, for every fixed $c$ and every fixed $T' > T = 0.4875754036$, uses $O(2^{T'n})$ word operations on every input of $n$ integers whose bit lengths, and that of the target, are at most $n^c$. In particular it runs in time $O(2^{0.4875755n})$.
\end{theorem}
The algorithm is Base's, with a single asymmetric filter (16 cosine and 16 sine terms per density) in place of Base's 43, and with the parameters of Section~8. The theorem rests on two kinds of input: the 33 numerical conditions of Base's proof at these parameters, which we certify in interval arithmetic (Section~8), and the non-numerical lemmas of the two proofs, which we take as given; Section~11 records which of them were re-derived independently.""")

rep(r"0.4875754036 & this paper (Section~8) & Base with one asymmetric filter (16 cosine + 16 sine terms) in place of 43 & certified and refereed; conditional on Base \\",
    r"0.4875754036 & this paper (Theorem~\ref{thm:main}) & Base with one asymmetric filter (16 cosine + 16 sine terms) in place of 43 & numerics certified; conditional on Base \\")
rep(r"Section~9 shows why further progress in this architecture is bounded: at the current checksum capacity no change on the list side can go below about 0.4857.",
    r"Section~9 explains what bounds further progress: with an alias-enumeration phase of the kind used here and the best checksum capacity found so far, no change on the list side can go below about 0.4857.")

# contributions
rep(r"\item A certified and refereed point at 0.4875754036 (time $O(2^{0.4875755n})$) in Base's construction with a single asymmetric filter, $1.0\times10^{-4}$ below JoshuaQFEX (Section~8).",
    r"\item A certified point at 0.4875754036 (time $O(2^{0.4875755n})$) in Base's construction with a single asymmetric filter, $1.0\times10^{-4}$ below JoshuaQFEX (Theorem~\ref{thm:main}, Section~8).")
rep(r"\item An explanation of the values near 0.4876: three closed-form bounds, the floor $(1 - \Delta)/2 \approx 0.4857$ of the architecture, the identification of the remaining list overhead as overlapping mask pairs, and pre-registered negative results for filter families, ternary masks and colour-coding (Section~9).",
    r"\item An analysis of the costs near 0.4876: three closed-form bounds, a counting floor $(1 - \Delta)/2$ for the alias-enumeration phase (about 0.4857 at the best capacity found), the identification of most of the remaining list overhead with overlapping mask pairs, and pre-registered negative results for filter families, ternary masks and colour-coding (Section~9).")
rep(r"\item A lower bound on the first filtering moment valid for all densities, which blocks exponent 0.48 in the OpenAI construction (Section~5).",
    r"\item A lower bound on the first filtering moment valid for all densities, which shows that the sufficient conditions of the OpenAI proof cannot be met at any $\tau \le 0.484$ (Section~5).")
rep(r"\item Precise open problems: a joint bound on the moment capacity, Corollary D beyond the half-block, and designs that avoid enumerating every alias class (Section~10).",
    r"""\item Precise open problems: a joint bound on the moment capacity, designs that avoid enumerating every alias class, and the small-layer statement [S] behind a conditional 0.4873408, with proved special cases (Section~10, Appendices~\ref{app:T} and~\ref{app:B}).
\end{enumerate}

\subsection*{How to read this paper}
Section~2 sets up the model, the notation and the parameter budget of the OpenAI proof. A reader interested mainly in the main result can go from there to Section~8, which gives the new point and its certificate, then to Section~9 (what limits the exponent) and Section~10 (open problems, including the conditional improvement). Sections~3--7 concern the original OpenAI construction: the premises of the 0.487676 bound (Section~3), the block count (Section~4), Lemma~1 and the exclusion of 0.48 (Section~5), the capacity of the checksum (Section~6) and a certified 16-block point (Section~7). Section~11 describes the methods and the use of AI tools, and records, claim by claim, how each result was checked. Appendix~\ref{app:T} states the ternary alias step behind the conditional result; Appendix~\ref{app:B} gives the proofs for Section~10.
\begin{enumerate}[label={}, leftmargin=0pt]""")
# the line above re-opens an empty enumerate so the original \end{enumerate} still closes something; remove that trick:
rep("\n\\begin{enumerate}[label={}, leftmargin=0pt]\n\\end{enumerate}", "\n")

# how obtained (R21)
rep(r"\item \textbf{Independent review.} Each main claim was rechecked by a reviewer that saw only the claim's inputs and the source papers, never our code, and that derived the conditions and recomputed the numbers on its own (Section~11).",
    r"\item \textbf{Independent review.} Each main claim was rechecked by a reviewer: a separate AI agent run in a fresh context, given the claim's inputs and the source papers but not our code, which derived the conditions and recomputed the numbers on its own. These are computational and mathematical cross-checks, not external peer review; where a reviewer had seen related material earlier, Section~11 says so.")
rep(r"Every claim in the paper is labelled as proved, certified, conditional or floating, and the paragraph below summarizes the labels.",
    r"Every claim in the paper is labelled as proved, certified, conditional or floating, and the paragraph below summarizes the labels; ``certified'' and ``conditional'' are compatible, since a certified inequality can be a premise of a conditional theorem.")

# status block (R20)
between("% STATUS-BEGIN", "% STATUS-END", r"""% STATUS-BEGIN
\subsection*{Status of the results}
\textbf{Certified numerics in conditional theorems.} Theorem~\ref{thm:main}, the exponent 0.4875754036 (time $O(2^{0.4875755n})$), $1.0\times10^{-4}$ below JoshuaQFEX (Section~8): all 33 numerical conditions certified in interval arithmetic by independent implementations; conditional on Base's written proof and the OpenAI paper. Base's probabilistic core (Lemma A5, Corollary D and the region analysis of its Theorem B) was re-derived independently; one repairable step was found, which our point satisfies (Section~11). Theorem~\ref{thm:k16}, the 16-block point at 0.4894616 in the OpenAI construction (Section~7): independent certificates; conditional on the OpenAI proof and our block-count audit (Section~4). The 430 moment premises of the 0.487676 bound (Section~3): certified by two routes.

\textbf{Proved.} Lemma~1 (Section~5) and its consequence that the sufficient conditions of the OpenAI proof fail for every $\tau \le 0.484$ and every multiplier $p \in [1, 10]$ (checked in interval arithmetic). The three closed-form bounds of Section~9, which are exact algebra on Base's constraints, and the counting floor (Proposition~\ref{prop:floor}) under its stated premise. Lemma~S, Proposition~\ref{prop:p2} and the special cases of Proposition~\ref{prop:k1} in Section~10 (proofs in Appendix~\ref{app:B}).

\textbf{Conditional on an open statement.} Theorem~\ref{thm:ternary}, the exponent 0.4873407528 (time $O(2^{0.4873408n})$) with ternary left masks (Sections~8, 10, Appendix~\ref{app:T}): 33 conditions certified; the ternary alias step reviewed and independently checked; it needs the statement [S], which is open.

\textbf{Floating.} The value 0.4857 of the counting floor, which uses the best joint checksum capacity found (about 0.029, not proved optimal); the shadow prices and the negative results for filter families, ternary masks under Base's Corollary D and colour-coding (Section~9); the joint capacity itself (Sections~6, 10); and the sharper 0.4852 floor of Section~5.
""")

# ---------------------------------------------------------------- Section 2: notation panel (R5, R24)
rep(r"This is the setting of the OpenAI and Base theorems, and every bound below inherits it.",
r"""This is the setting of the OpenAI and Base theorems, and every bound below inherits it.

\textbf{Notation.} The symbols used throughout are collected here; each is explained again where it is first used.

\begin{center}
\small
\begin{tabularx}{\linewidth}{>{\raggedright\arraybackslash}p{4.4cm} L}
\toprule
Symbol & Meaning \\
\midrule
$n$; $b$ & number of input integers; largest bit length of the input integers and the target \\
$h(x) = -x\log_2 x - (1-x)\log_2(1-x)$ & binary entropy, with $h(0) = h(1) = 0$ \\
$\Sigma(B)$, $\Sigma_j(B)$ & the distinct subset sums of a set $B$ of input positions; those of its $j$-element subsets \\
$d(B) = |B| - \log_2|\Sigma(B)|$ & deficiency of $B$ (0 when all subset sums of $B$ are distinct) \\
$a_j(B) = |\Sigma_j(B)|/\binom{|B|}{j}$ & fraction of distinct values among the $j$-subset sums of $B$ \\
$P$, $\eta$ & the random checksum prime, of about $\eta n$ bits \\
alias; alias class & a subset whose sum agrees with the target modulo $P$ without being a solution; subsets that the list side cannot tell apart (in Base: equal on the shared block, with the same sums on each outside block) form a class, and a class consists of aliases entirely or not at all \\
$\tau$ ($\tau_0$ in Base); $T$ & exponent of the enumeration budget; final exponent threshold, the largest of the terms in the running-time formula below \\
$\Delta = \eta - \tau$, $\Gamma = 2\tau - \eta$, $a_\Gamma = \Delta/\Gamma$ & the checksum gap, its complement and their ratio \\
$M_1$, $M_2$; $p$, $q_m$ ($q$ in Base); $\kappa$ & the two filtering moments; their multipliers; the power applied to the densities \\
$\rho_c < \rho_f$ & the certified moment threshold and its finite-circle counterpart \\
OpenAI: $K$, $\mu = m/n$, $\gamma$, $d$, $d_0$, $d_1$, $c_0$, cap & number of disjoint half-blocks, block size, rate of the smaller modulus, local deficiency cutoff, preliminary-search thresholds, probability of a useful block, time cap \\
Base: $M, L, R$; $\mu$, $l$, $r = 1 - \mu - l$; $a$; $P'$; $\sigma = m/2$, $k \approx am$ & shared block and outside blocks; their sizes divided by $n$; mask density; the second, smaller random prime that filters representations (of rate $\gamma$); half-block size and mask size \\
$\eps$, $\zeta$; $g_0$; guard & small slack constants ($\eps = \zeta = 10^{-8}$ in Section~8); the guard margin $g_0 = 10^{-5}$ of the OpenAI budget; Base's input-length guard ($10^8$) \\
\bottomrule
\end{tabularx}
\end{center}""")
rep(r"$K$ the number of disjoint half-blocks (17 in the paper), $\eps = 10^{-8}$ and guard $g = 10^{-5}$.",
    r"$K$ the number of disjoint half-blocks (17 in the paper), $\eps = 10^{-8}$ and guard margin $g_0 = 10^{-5}$.")
rep(r"Visited pairs & $\tau \ge 1 + (2h(1/4) - 1 - \gamma)\mu - \eta + g$ & aliases l.244--253 \\",
    r"Visited pairs & $\tau \ge 1 + (2h(1/4) - 1 - \gamma)\mu - \eta + g_0$ & aliases l.244--253 \\")
rep(r"Sparse distinctions & $\eta > h(\mu) + \mu + g$ & aliases l.296--309 \\",
    r"Sparse distinctions & $\eta > h(\mu) + \mu + g_0$ & aliases l.296--309 \\")
rep(r"Domination, case 2 & $1 \le q_m$, $q_m(4a + 3) \le 30$, $a = \Delta/\Gamma$ & checksum l.451--458 \\",
    r"Domination, case 2 & $1 \le q_m$, $q_m(4a_\Gamma + 3) \le 30$, $a_\Gamma = \Delta/\Gamma$ & checksum l.451--458 \\")
rep(r"M_2 = \int_{\mathbb T} (2+2\cos x)\, 2^{\,q_m(a\, v(x) - u(x))}\, dx",
    r"M_2 = \int_{\mathbb T} (2+2\cos x)\, 2^{\,q_m(a_\Gamma v(x) - u(x))}\, dx")

# ---------------------------------------------------------------- Section 4 (R13, R21)
rep(r"The constant 17 enters the OpenAI proof in two places, and both hold verbatim for any $K$ with $K\mu < 1$.",
    r"The constant 17 enters the OpenAI proof in two places, and both hold verbatim for any integer $K \ge 1$ with $K\mu < 1$ (the replacements below also need $\mu \le 1/2$, the range of the sparse-distinction count).")
rep(r"an independent referee re-derived the full constraint list from the \TeX{} and found nothing missing.",
    r"an independent reviewer re-derived the full constraint list from the \TeX{} and found nothing missing.")

# ---------------------------------------------------------------- Section 5 (R11, R12)
rep(r"\textbf{Tightness.} Equality in step 1 needs $\kappa = 1$, and in step 3 needs $Q^*$ proportional to $w^{1/(1+p)}$. Densities with $g$ sharply peaked and $f$ proportional to $w^{1/(1+p)}$ approach the bound, with gaps down to $5.8\times10^{-7}$ in $\log_2$; at $\kappa = 1.1$ a fixed positive gap remains. The function $g(p) = (1+p) \log_2 \E[w^{1/(1+p)}]$ is a log power mean of $w$, so it is nonincreasing in $p$; this makes minimizing $\Phi$ over $p$ rigorous on monotone cells.",
    r"\textbf{Tightness.} Equality in step 1 holds when the ratio $f^*(x+w)\,g^*(w)/K_x(w)$ is constant in $w$ under $K_x$ (for example when $\kappa = 1$, or when $f = g = 1$), and equality in step 3 needs $Q^*$ proportional to $w^{1/(1+p)}$. Densities with $g$ sharply peaked and $f$ proportional to $w^{1/(1+p)}$ approach the bound, with gaps down to $5.8\times10^{-7}$ in $\log_2$; in the family we tested, a positive gap remains at $\kappa = 1.1$. Write $\Psi(p) = (1+p) \log_2 \E[w^{1/(1+p)}]$, so that $\Phi(p) = 1 + p\Delta + \Psi(p)$. It is a log power mean of $w$, so it is nonincreasing in $p$; this makes minimizing $\Phi$ over $p$ rigorous on monotone cells.")
rep(r"(a referee counterexample at $P = 4$ has gap $-0.154$;", r"(a reviewer's counterexample at $P = 4$ has gap $-0.154$;")
between(r"\textbf{Consequence 2: 0.48 is out of reach.}", r"\textbf{Verification.} An independent referee checked each step",
r"""\textbf{Consequence 2: the OpenAI budget cannot reach 0.48.} The sufficient conditions of the OpenAI proof include the $M_1$ condition with a multiplier $p \in [1, 10]$ (the rounding cap $3p \le 30$). Writing $\eta = \tau + \Delta$, Lemma~1 turns that condition into $(p - 1)\Delta < \tau - 1 - \Psi(p)$. At $p = 1$ this reads $\tau > 1 + \Psi(1) = 1 + 2\log_2(2\sqrt2/\pi) \approx 0.697$, which fails; for $p \in (1, 10]$ it forces $\Delta < D_{\max}(\tau)$ = max over $p$ of $(\tau - 1 - \Psi(p))/(p - 1)$, about 0.0403 at $\tau = 0.48$. The list bound forces $\mu \ge (1/2 - \tau)/(\gamma + 1/2 - h(1/4))$, and the pair bound with $\gamma < 1/2$ then forces $\Delta \ge 2.6494(1/2 - \tau) + g_0$, about 0.053 at $\tau = 0.48$. These constraints are jointly infeasible for every $\tau \le 0.484$, every $p \in [1, 10]$ and every $K$ (checked in interval arithmetic by two independent reviewers), so the sufficient conditions of the OpenAI proof cannot be met at exponent 0.48 for any choice of parameters. This is a statement about that proof's budget, not a lower bound for every algorithm built on related ideas. Combining Lemma~1 with the full scalar budget gives a sharper floor near 0.4852 ($K = 11$), but only as a floating, grid-based estimate.

""")
rep(r"\textbf{Verification.} An independent referee checked each step of the proof",
    r"\textbf{Verification.} An independent reviewer checked each step of the proof")

# ---------------------------------------------------------------- Section 6
rep(r"Lemma~1 already rules out 0.48 for every choice of parameters (Section~5), and the analysis below shows why:",
    r"Lemma~1 already shows that the proof's sufficient conditions cannot be met at 0.48 for any choice of parameters (Section~5), and the analysis below shows why:")
rep(r"At $\tau = 0.4898$ that capacity is about 0.029, whatever density family we try (floating exploration).",
    r"At $\tau = 0.4898$ that capacity is about 0.029 in every density family we tried (floating exploration).")
rep(r"6 cosines & $M_2$ only & 0.03226 & rounding cap $q_m(4a+3) \le 30$ \\",
    r"6 cosines & $M_2$ only & 0.03226 & rounding cap $q_m(4a_\Gamma+3) \le 30$ \\")

# ---------------------------------------------------------------- Section 7 (numbered theorem)
rep(r"""\begin{theorem*}[conditional on the OpenAI proof and Section~4]
With the parameters below""", r"""\begin{theorem}[conditional on the OpenAI proof and Section~4]\label{thm:k16}
With the parameters below""")
rep(r"""in particular $O(2^{0.4894616 n})$.
\end{theorem*}""", r"""in particular $O(2^{0.4894616 n})$.
\end{theorem}""")
rep(r"\item \textbf{Referee's} (independent agent; saw only the parameter file and the TeX):",
    r"\item \textbf{Reviewer's} (independent agent; saw only the parameter file and the TeX):")

# ---------------------------------------------------------------- Section 8 first paragraph + Corollary D (R5)
between(r"Base changes both halves of the OpenAI algorithm. On the list side it uses one large shared block",
        r"\textbf{Observation.} With a family of $J = 1$ filters",
r"""Base changes both halves of the OpenAI algorithm. On the list side it partitions the input into a shared block $M$ of about $0.475n$ positions and two outside blocks $L$ and $R$, uses sparse masks of density $a \approx 0.008$, returns alias phase sums instead of alias lists, and replaces the 17-block Markov step by an averaged small-layer bound, Base's Corollary~D. On the checksum side it uses a family of 43 filters, each with 8 cosine terms, certified in 10 regions of the pattern space. Base reports that its filter search stalls near 0.4876 and that ``further progress needs a new idea.'' JoshuaQFEX retunes Base's parameters to 0.487676.

\textbf{Why Corollary D is needed.} A trial of Base's alias step uses a random half $S$ of $M$ and looks for representations of an alias through $k$-element subsets of $S$, with $k \approx am$. Repeating trials helps only if these subsets produce enough distinct sums, and Corollary D supplies the averaged lower bound:

\begin{quote}
\textbf{Corollary D} (Base, l.254--257). Let $k, \sigma, v$ be nonnegative integers with $2k \le \sigma$, $2\sigma \le v + 2k$, $v \le |M|$ and $\binom{\sigma}{k}\binom{v}{k} \le 2^v$. Let $S$ be a uniform $\sigma$-subset and $V$ a uniform $v$-subset of $M$. Then $\E_S\, a_k(S) \ge \E_V\, 2^{-d(V)}/(v+1)$.
\end{quote}

In the alias step $\sigma = m/2$ and $v = m - 2k$, so $2\sigma = v + 2k$; write $g_M = -\log_2 \E_V 2^{-d(V)}$. So a random half-block has, on average, at least a $2^{-g_M}/(v+1)$ fraction of distinct $k$-subset sums. Base estimates $2^{g_M}$ by sampling and runs about $n^7\, 2^{g_M + O(n^{0.6})}$ trials. Each trial finds the class of a given alias with probability at least $2^{-g_M} n^{-6}$ (Base's Lemma A5), using the second prime $P'$ to keep many of the distinct sums in one residue class, so every alias class is found with high probability; Base's deficiency bounds keep the number of trials within the time budget. The numerical side conditions this needs are among Base's (C1)--(C8) and (S1)--(S5), certified below.

""")
rep(r"region $\rho_0$ uses the multiplier vector $z = (p, 0)$ and regions $\rho_1$--$\rho_9$ use $z = (q, 0, 0)$, so the 10 certificates are exactly $M_1$ and $M_2$.",
    r"region $\rho_0$ uses the multiplier vector $z = (p, 0)$, the bounded regions $\rho_1$--$\rho_8$ use $z = (q, 0, 0)$ and the unbounded region $\rho_9$, which has one row fewer, uses $z = (q, 0)$; all high regions share the exponent $q(a_\Gamma w - u)$, so the 10 certificates reduce to $M_1$ and $M_2$.")
rep(r"The tightest margins are B3 ($8.1\times10^{-7}$), $M_1$ ($1.315\times10^{-6}$), C4 ($1.316\times10^{-6}$) and $M_2$ ($1.494\times10^{-6}$).",
    r"The tightest margins are B3 ($8.1\times10^{-7}$), $M_1$ ($1.315\times10^{-6}$), C4 ($1.3156\times10^{-6}$) and $M_2$ ($1.494\times10^{-6}$).")
rep(r"\textbf{Independent referee.} A separate agent that saw only", r"\textbf{Independent review.} A separate agent that saw only")
rep(r"\textbf{Second referee.} A further independent review,", r"\textbf{Second review.} A further independent review,")
rep(r"A full replacement for Base's alias step in Base's style (soundness, counts, a trial count computed exactly as $C_S\, n^8\, 2^{d(M)}$, a global distinctness lemma in place of Base's $\delta$, coverage through the counting identity of Section~10, and the cost items, with Base line numbers) is in the repository as Section~T.",
    r"A full replacement for Base's alias step in Base's style (soundness, counts, an explicit integer trial count of order $C_S\, n^8\, 2^{d(M)}$, a global distinctness lemma in place of Base's $\delta$, coverage through the counting identity of Section~10, and the cost items, with Base line numbers) is stated in Appendix~\ref{app:T}; its complete proofs are in the ancillary file and the repository (``Section~T'').")
rep(r"$a = c = 0.0035141538$,", r"$a = 0.0035141538$, $c = 0.0035141537$,")
rep(r"A fresh referee, working only from the candidate file, Section~T and the Base and OpenAI sources,",
    r"A fresh reviewer, working only from the candidate file, Section~T and the Base and OpenAI sources,")
rep(r"""\begin{theorem*}[conditional on {[S]}, on Base's written proof and on the OpenAI paper]""",
    r"""\begin{theorem}[conditional on {[S]}, on Base's written proof and on the OpenAI paper]\label{thm:ternary}""")
rep(r"""in particular in time $O(2^{0.4873408n})$.
\end{theorem*}""", r"""in particular in time $O(2^{0.4873408n})$.
\end{theorem}""")
rep(r"\textbf{Status and caveats.} The proved exponent is $T = \tau_0 + 20\eps = 0.4875754036$,",
    r"\textbf{Status and caveats.} The exponent of Theorem~\ref{thm:main} is $T = \tau_0 + 20\eps = 0.4875754036$,")
rep(r"S3's 0.129 $\to$ 0.1308, $\eps_0 = 1.3157\times10^{-6}$ (Base $5.37\times10^{-6}$)",
    r"S3's left side $0.12945$ (Base: 0.129), $\eps_0 \ge 1.3156\times10^{-6}$ (Base $5.37\times10^{-6}$)")
rep(r"The OpenAI rounding caps $3p \le 30$ and $q(4a + 3) \le 30$ are not required under Base,",
    r"The OpenAI rounding caps $3p \le 30$ and $q(4a_\Gamma + 3) \le 30$ are not required under Base,")

# ---------------------------------------------------------------- Section 9 floor (R1) and overhead (R10)
between(r"\textbf{The floor of the architecture.} In (ii), $1 - \eta$ is", r"The floor is attained in the model when the overhead in (ii) is removed.",
r"""\textbf{The counting floor.} In (ii), $1 - \eta$ is $\log_2$ of $2^n/P$, the typical number of aliases of a target. This gives a floor for the alias-enumeration phase, under an explicit premise.

\begin{proposition}[counting floor]\label{prop:floor}
Consider an alias step that inserts every alias class of each target, spends at least one counted step on each class it inserts, and is combined with a checksum at the same modulus whose capacity is $\Delta$, so that $\eta - \tau_0 \le \Delta$. If for some input and target there are at least $2^{(1-\eta-o(1))n}$ alias classes, then $\tau_0 \ge 1 - \eta - o(1) \ge 1 - \tau_0 - \Delta - o(1)$, that is, $\tau_0 \ge (1-\Delta)/2 - o(1)$.
\end{proposition}

The premise concerns the input; the method does not supply it. Distinct subset sums alone do not imply it: the weights $P, 2P, 4P, \dots$ have distinct subset sums but no aliases of a target $\equiv 1 \pmod P$. Inputs whose subset sums spread nearly evenly over the residues modulo $P$, as one expects for typical random inputs, have about $2^{(1-\eta)n}$ aliases per target, each its own class when the subset sums are distinct. The proposition says nothing about designs that do not enumerate every alias class, that use different moduli, or whose checksum is not of the moment form, and it is not a lower bound for Subset Sum. Its value depends on $\Delta$: at the certified point's $\Delta = 0.0287$ it is 0.48565, and about 0.029 is the best joint capacity found numerically (Section~6), not a proved maximum. Exponent 0.48 would need $\Delta \ge 0.040$ even with no list overhead at all; Lemma~1 caps the first moment's capacity near that value. """, keep_end=True)
rep(r"with the filter held fixed, the second referee's model gives", r"with the filter held fixed, the second reviewer's model gives")
rep(r"It equals $-\log_2$ of the probability that a uniform left mask of $k$ elements and a uniform right mask of $\sigma - k$ elements of the block are disjoint, 0.003845 per $n$; at $\gamma = h(2a)/2$ the two entropy expressions agree. So the overhead is exactly the visited tuples with overlapping masks, which the expansion step tests and discards.",
    r"The probability that a uniform left mask of $k$ elements and a uniform right mask of $\sigma - k$ elements of the block are disjoint has $-\log_2$ equal to $\mu[h(a) + h(1/2 - a) - 1 - h(2a)/2]\,n + O(\log n)$, 0.003845 per $n$. The two differ by $\mu(h(2a)/2 - \gamma)$, which is $\mu$ times the slack of C1, about $6.3\times10^{-7}$ at our point; they agree in the limit $\gamma = h(2a)/2$. So, up to that slack, the overhead is the visited tuples with overlapping masks, which the expansion step tests and discards.")
rep(r"Under the stronger statement [S] of Section~8 they give the conditional theorem stated there ($T = 0.4873407528$); [S] is open (Section~10).",
    r"Under the stronger statement [S] of Section~8 they give Theorem~\ref{thm:ternary} ($T = 0.4873407528$); [S] is open (Section~10).")
rep(r"\textbf{Summary.} At the current checksum capacity this architecture cannot go below about 0.4857,",
    r"\textbf{Summary.} With an alias-enumeration phase of this kind and the best checksum capacity found (about 0.029), the exponent cannot go below about 0.4857 (Proposition~\ref{prop:floor}),")

# ---------------------------------------------------------------- Section 10 (R3, R4, R14, R15, R24)
rep(r"\textbf{Beyond the floor of Section~9.} Below about 0.4857 the architecture itself must change:",
    r"\textbf{Beyond the floor of Section~9.} Below about 0.4857 the design itself must change:")
rep(r"Is the average fraction of distinct sums $w(U)$ at least $2^{-g}/\poly(n)$, with $g$ inside the trial budget",
    r"Is the average fraction of distinct sums $w(U)$ at least $2^{-g_M}/\poly(n)$, with $g_M$ inside the trial budget")

between(r"\subsection*{The small-layer statement [S] behind the conditional exponent}", r"\subsection*{The checksum side and other questions}",
r"""\subsection*{The small-layer statement [S] behind the conditional exponent}

Theorem~\ref{thm:ternary} needs [S] only at $k' = k_1 + k_2 \approx 0.0070m$; Section~8 states it for $k \le 0.11m$ because that is the range reached by the reduction below. Base's Corollary D and its size conditions are then not needed, and its cost bounds still hold if $\mu < l$. Write $s_j$ for the number of distinct $j$-subset sums of the block and $a_j = s_j/\binom{m}{j}$, and call a weighting \emph{generic} if, for each $j$, all its $j$-subset sums are distinct. The statements below are linked by
\[
\text{YP-Hall} \;\Rightarrow\; \text{Conj.~Q} \;\Rightarrow\; \text{Conj.~M}' \ (P = 1) \;\Rightarrow\; \text{[S]} \ (C_S = 3),
\]
the first for $k \le m/4$, the second by complementation, the last by Lemma~S. The table gives the status of each link and of the partial results; proofs are in Appendix~\ref{app:B}.

\begin{center}
\small
\begin{tabularx}{\linewidth}{>{\raggedright\arraybackslash}p{2.6cm} L >{\raggedright\arraybackslash}p{4.7cm}}
\toprule
Statement & Content & Status \\
\midrule
{[S]} & $a_k \ge 2^{-d(M)}/C_S(m)$ for every weighting and $k \le 0.11m$ & Open; $a_k\,2^{d(M)} \ge 1.00$ in all 2,655 tested instances ($m = 12$ to $16$) \\
{Lemma S} & M$'$ with constant $P(m)$ implies [S] with $C_S = P + 2$ & Proved \\
{Conjecture M$'$} & $a_t \le P(m)\, a_k$ for $t \in [k, m-k]$, $k \le 0.11m$ & Open; proved with a loss of about $2^k$ (Proposition~\ref{prop:p2}) \\
{Conjecture Q} & $Q_w(t,k) \le 1$ for $k \le m/4$; implies M$'$ with $P = 1$ & Open; no violation for $k < m/3$ in our searches; false at $k = m/3$ \\
{YP-Hall} & a Hall condition for $t + 2k \le m$; implies Conjecture Q & Open; feasible in about 35,700 floating-point flow computations \\
{Case $k = 1$ of Q} & $Q_w(t,1) \le 1$ & Proved for $t = 2$ and for two families of weights (Proposition~\ref{prop:k1}); open for $t \ge 3$ \\
{Exact monotonicity} & $a_{k+1} \le a_k$ for $k + 1 \le m/2$ & False at the middle step (130 counterexamples at $m = 8$); not needed \\
\bottomrule
\end{tabularx}
\end{center}

\emph{Lemma S.} If $a_t \le P(m)\, a_k$ for all $t \in [k, m-k]$ and $k \le 0.11m$, then [S] holds with $C_S = P + 2$. Indeed $2^{-d(M)} \le \E_{t\sim\mathrm{Bin}(m,1/2)}[a_t]$, since $|\Sigma| \le \sum_t |\Sigma_t|$; the layers inside $[k, m-k]$ contribute at most $P a_k$, and the layers outside carry mass at most $2\cdot 2^{-m(1-h(\alpha))}$ with $\alpha = k/m$, which is at most $2a_k$ because $a_k \ge 1/\binom{m}{k} \ge 2^{-mh(\alpha)}$ and $h(\alpha) \le 1/2$ for $\alpha \le 0.11$. (At $k = 0$ there are no outside layers.)

\emph{Exact monotonicity fails at the middle step.} An exhaustive sweep over all value multisets in $[-8, 8]$ at $m = 8$ finds 130 counterexamples to $a_{k+1} \le a_k$, all at the middle step $k + 1 = m/2$, for example $w = (-6, -5, -5, -3, -3, -2, 4, 5)$ with $a_3 = 19/56 < a_4 = 24/70$ (verified independently). Away from the middle the comparison held in our tests: in exhaustive sweeps at $m = 9$ to 12 (about 11 million multisets) the maximum of $a_t$ over $t \ge k$ was attained at $t = k$ for every $k \le m/4$. The tight cases are sharp: with half the weights equal to 1 and half to 2, $a_k/a_{k+1} = (m - k)/(k + 2)$, exactly 1 at $k = m/2 - 1$. Monotonicity also has an exact combinatorial form: the map $(y, e) \mapsto (e, y - w_e)$ is a bijection between pairs with $y$ a $(k+1)$-sum and $e$ in the union $U(y)$ of its witness sets, and pairs with $x$ a $k$-sum and $e$ outside the intersection $C(x)$ of its witness sets, so $a_k \ge a_{k+1}$ is equivalent to $\sum_y (|U(y)| - (k+1)) \ge \sum_x (k - |C(x)|)$ (verified on 39 instances).

\begin{proposition}[P2]\label{prop:p2}
For $k \le t \le m - k$, $s_t\binom{t}{k} \le s_k\binom{m}{t-k}$, that is, $a_t \le a_k\,\binom{m}{t-k}\big/\binom{m-k}{t-k}$.
\end{proposition}
Fix one witness $X_y$ for each $t$-sum $y$; the map $(y, A) \mapsto (w(A), X_y \setminus A)$ over $k$-subsets $A \subseteq X_y$ is injective, because the image determines $y$, hence $X_y$, hence $A$. The loss is about $2^k$ at $t = m/2$; it is exactly the support barrier $m/2 + k$ of Base's Corollary D seen as a statement about layers. At $k = 0.007m$ it costs about $0.0033$ in the exponent, fourteen times the ternary gain, so the application needs the comparison essentially without loss. M$'$ is trivial for bounded $k$ ($P = \binom{m}{k}$); its content is $k \to \infty$ with $m$.

\emph{A sharper target.} Draw a $t$-sum $y$ uniformly, a witness $X$ of $y$ uniformly, and a uniform $k$-subset $A \subseteq X$, and let $\nu$ be the law of $w(A)$. Since $\nu$ is supported on the $s_k$ values of $\Sigma_k$, Cauchy--Schwarz gives $s_k \ge 1/\mathrm{cp}(\nu)$, where $\mathrm{cp}$ is the collision probability, so $Q_w(t,k) := \mathrm{cp}(\nu)\, a_t \binom{m}{k} \le 1$ implies $a_t \le a_k$. Always $Q_w \ge a_t/a_k$, with $Q_w = 1$ for generic weights.

\begin{conjecture}[Q]\label{conj:Q}
$Q_w(t,k) \le 1$ for all integer weightings, $k \le m/4$ and $k < t \le m/2$.
\end{conjecture}
With $s_t = s_{m-t}$ this gives $a_t \le a_k$ on all of $[k, m-k]$, hence M$'$ with $P = 1$ and [S] with $C_S = 3$. The range is part of the statement: $Q_w$ exceeds 1 at $k = m/3$ ($w = (-3,-3,-2,-2,0,0)$ at $(k,t) = (2,3)$: $Q_w = 29/28$) and at the middle step ($1.079$ for the $m = 8$ counterexample above). Below $m/3$ we found no violation: exhaustive in $[-3,3]$ for $m \le 10$, about $10^5$ random instances, targeted two- and three-valued families up to $m = 20$, and hill-climbs at $m = 18$ and 20 whose controls recover the known middle-step violations. In these searches the supremum of $Q_w$ for $k < m/3$ is 1, attained by generic weights and approached by a single repeated pair among generic values. The few-valued instances found by the hill-climbs at $m = 18$ and 20 stay below 0.72, but small few-valued instances can reach 1, for example $(0,0,1,1)$ at $(k,t) = (1,2)$.

\emph{A charging formulation.} For a $t$-set $X$ let $f(X)$ be the number of $t$-sets with the same sum. A \emph{near miss} is a quadruple $\ell = (X, X', A, A')$ of $t$-sets $X, X'$ and $k$-sets $A \subseteq X$, $A' \subseteq X'$ with $A \ne A'$, $w(A) = w(A')$ and $(A' \setminus A) \cap X \ne \emptyset$; its weight is $1/(f(X)f(X'))$. A \emph{target} is a quadruple $r = (Y, Y^*, Y'', D)$ of $t$-sets $Y \ne Y^*$ with $w(Y) = w(Y^*)$, a $t$-set $Y''$ and a $k$-set $D \subseteq Y \cap Y''$ with $D \not\supseteq Y \setminus Y^*$; its weight is $1/(f(Y)f(Y''))$. Then $Q_w(t,k) \le 1$ if and only if the total weight of the near misses is at most the total weight of the targets (Appendix~\ref{app:B}). The charging rule YP allows a near miss $\ell$ to be charged to a target $r$ exactly when $Y \supseteq A \setminus A'$, whatever $Y^*$, $Y''$ and $D$ are.

\begin{conjecture}[YP-Hall]\label{conj:yp}
For $t \le m/2$ and $t + 2k \le m$, every set $\mathcal S$ of near misses satisfies $w(\mathcal S) \le w(N(\mathcal S))$, where $N(\mathcal S)$ is the set of targets that some member of $\mathcal S$ may be charged to under YP.
\end{conjecture}
By the max-flow/min-cut theorem this is equivalent to a fractional charging of all near misses within the target weights, and taking $\mathcal S$ to be all near misses gives $Q_w \le 1$ on $t + 2k \le m$, which with the symmetry above covers the range $k \le m/4$ of Conjecture~\ref{conj:Q}. Max-flow computations in floating point (routed fraction at least $1 - 10^{-9}$ in every feasible case) found the rule feasible in every one of about 35,700 (instance, $k$, $t$) cases with $t + 2k \le m$ that we tried (exhaustive in $[-3,3]$ for $m \le 8$ and in $[-2,2]$ for $m = 9$, partial at $m = 10$, and the dense two- and three-valued shapes), while the control $(-3,-3,-2,-2,0,0)$ at $(2,3)$, outside the range, stays infeasible (it routes 0.90). Rules that keep the relation $(A \setminus A', A' \setminus A)$ fail, and the natural closed-form (proportional) map exceeds load 1 on one instance at $m = 7$, so the certificate is a flow, not a formula.

\begin{proposition}[the case $k = 1$]\label{prop:k1}
Group the elements into classes of equal weight, with sizes $n_c$, and put $M_c = \sum_X |X \cap c|/f(X)$, the sum over $t$-sets $X$. Then $Q_w(t,1) \le 1$ if and only if $\sum_c M_c (M_c - C) \le 0$, where $C = \binom{m-1}{t-1}$. This inequality holds
(i) for $t = 2$ and every integer weighting with $m \ge 4$;
(ii) for every weighting with two distinct values and every $2 \le t \le m/2$, with equality only for $(0,0,1,1)$ at $t = 2$;
(iii) for a repeated pair among values that are generic in the sense that, at layer $t$, the only equal $t$-sums come from exchanging the pair, for every $2 \le t \le m/2$, with equality only for $(0,0,g_1,g_2)$ at $t = 2$.
Equality cases are up to an affine change of the weights and a permutation.
\end{proposition}
A class can be over-represented ($M_c > C$) only if the whole class lies in a $t$-set whose sum has fewer than $n_c$ witnesses, so the content of the case $k = 1$ is that such excesses are paid by the deficits of the other classes. For $t = 2$ the stronger charging statement also holds (YP-Hall at $k = 1$, $t = 2$; Appendix~\ref{app:B}). Family (iii) is asymptotically tight at $(k,t) = (1,2)$ as the number of generic values grows, so any proof must handle it with no slack. All three parts were also checked by exhaustive computation from the definition of $Q_w$ (for (i), 59,408 instances up to $m = 14$; maximum exactly 1). The case $k = 1$, $t \ge 3$ is open. The obstruction is that the excess of an over-represented class must be paid by deficits on collisions of \emph{different} sums that merely share an element of the class, so no charging that stays inside a fiber or an orbit suffices; an induction from $k$ to $k + 1$ would also need a weighted form of YP-Hall and a separate treatment of near misses with $A \cap A' = \emptyset$. These small-$k$ results do not by themselves settle the linear range $k \approx 0.007m$ that Theorem~\ref{thm:ternary} needs.

""")

# ---------------------------------------------------------------- variational paragraph (R2, R16, R17)
between(r"\textbf{A large-deviation form of the moment conditions.}", r"\begin{enumerate}" + "\n" + r"\item \textbf{A joint moment bound.}",
r"""\textbf{The moment conditions as optimizations over types.} For a probability density $\nu$ on the circle write $\lambda = \log_2(2+2\cos x)$, $U = \E_\nu u$ and $V = \E_\nu v$. The Gibbs variational formula gives, exactly,
\begin{gather*}
\log_2 M_1 = \sup_\nu \bigl\{\E_\nu \lambda + p(\Delta - U) - \KL(\nu \,\|\, \mathrm{unif})\bigr\}, \\
\log_2 M_2 = \sup_\nu \bigl\{\E_\nu \lambda + q_m(a_\Gamma V - U) - \KL(\nu \,\|\, \mathrm{unif})\bigr\},
\end{gather*}
with $\KL$ in bits. So each moment condition says that no frequency type $\nu$ is too favourable: amplitude plus multiplier term minus rarity stays below $\rho_c$. These identities quantify over all densities; they do not by themselves reduce the two moment conditions to a single condition on the sampled types. At a floating 16-block point of the OpenAI construction with $\tau = 0.4898$ and $\Delta = 0.02906$, the maximizing types sit close to one corner, where the sampling boundary $U = \Delta$ meets the case switch $V = \Gamma$:

\begin{center}
\small
\begin{tabular}{lll}
\toprule
Quantity at the maximizing type & Value & Compare with \\
\midrule
$\E_\nu[u]$ & 0.02906 & $\Delta = 0.02906$ \\
$\E_\nu[v]$ & 0.46036 & $\Gamma = 0.46074$ \\
$\E_\nu[u + v] = \E_\nu[D]$ & 0.48942 & $\tau = 0.4898$ \\
$\E_\nu[\lambda] - \KL(\nu)$ & 0.51882 & $\eta = 0.51886$ \\
\bottomrule
\end{tabular}
\end{center}

The values come from one floating optimization and agree with the comparison column to within $4\times10^{-4}$; they are not certified. They suggest that the missing ingredient for a joint bound is an ``amplitude costs entropy'' inequality: a lower bound on $\E_\nu[v]$, valid for every density pair, in terms of $\E_\nu[\lambda]$, $\KL(\nu)$ and $\E_\nu[u]$. We have not proved one.

""", keep_end=True)
rep(r"For indicator-like densities $v = 2(\KL(f) - u)$, so $M_2$ acts as a second $M_1$-type constraint with gap $2a \KL(f)/(1+2a)$:",
    r"For indicator-like densities $v = \KL(f) + \KL(g) - 2u$, which is $2(\KL(f) - u)$ when $f$ and $g$ have equal entropy; then $M_2$ acts as a second $M_1$-type constraint with gap $2a_\Gamma \KL(f)/(1+2a_\Gamma)$:")
rep(r"By the price list in Section~6, the architecture's floor would then be about 0.48946,",
    r"By the price list in Section~6, the floor of the OpenAI budget would then be about 0.48946,")
rep(r"\item \textbf{The rounding caps.} On its own, $M_2$ is limited by $q_m(4a+3) \le 30$,",
    r"\item \textbf{The rounding caps.} On its own, $M_2$ is limited by $q_m(4a_\Gamma+3) \le 30$,")
rep(r"More cases in the domination step do not help: with up to 32 general affine forms",
    r"In our experiments more cases in the domination step did not help: with up to 32 general affine forms")
rep(r"and the paper's $p(\Delta - u)$ is already the best affine form on that slice.",
    r"and in our computations the paper's $p(\Delta - u)$ was already the best affine form on that slice.")
rep(r"None of the estimator variations we modelled within this checksum design helps.",
    r"None of the estimator variations we modelled within this checksum design helped.")
rep(r"That can never happen at the optimal multiplier. There $d \log M_1/dp = \Delta - \E_t[u] = 0$ under the moment's own tilt $t$, so the tilted mean is a realizable sampling pattern",
    r"This cannot happen at an interior optimal multiplier: there $d \log_2 M_1/dp = \Delta - \E_\nu[u] = 0$ under the moment's own tilt $\nu$, so the tilted mean is a realizable sampling pattern")
rep(r"A joint optimization of densities, tilts, cutoffs and the LP-dual certificates confirms this, returning $c_3 = 1$ from every start.",
    r"(A boundary optimum, $p = 1$ or $p = 10$, is not covered by this argument.) A joint optimization of densities, tilts, cutoffs and the LP-dual certificates agrees, returning $c_3 = 1$ from every start.")
rep(r"By the Donsker--Varadhan formula the moment conditions are equivalent to one statement about frequency types: every type $t$ that would be sampled must satisfy $\E_t[\lambda] + \varphi - \KL(t \,\|\, \mathrm{uniform}) \le \eta$, that is, amplitude plus target minus rarity is at most the budget. Proving the joint bound then means exhibiting one violating type for any given densities, for example the critical type.",
    r"Proving a joint bound would mean showing that, for every density pair, some type $\nu$ violates one of the two variational inequalities above.")
rep(r"\item \textbf{Verifying the non-numerical premises.} All results here inherit the non-numerical lemmas of the OpenAI paper (isolation, the alias lemmas, alias subtraction, the word-RAM accounting) and, from Section~8 on, Base's probabilistic core (its Lemma A5, Corollary D and the region analysis of its Theorem B). These have so far been checked only by reading. An independent written re-derivation, or a formal proof in a proof assistant such as Lean, would remove that conditionality; the OpenAI repository formalizes several of its other results, but not this one.",
    r"\item \textbf{Verifying the non-numerical premises.} All results here inherit the non-numerical lemmas of the OpenAI paper (isolation, the alias lemmas, alias subtraction, finite-circle convergence and the word-RAM accounting) and, from Section~8 on, the parts of Base's proof that we have not re-derived: the preliminary search, the alias-step cost accounting and the checksum changes. (Base's probabilistic core, Lemma A5, Corollary D and the region analysis of its Theorem B, was re-derived independently; Section~11.) Written re-derivations of the remaining parts would remove most of that dependence; a formal proof in a proof assistant such as Lean would be a further verification project. The OpenAI repository formalizes several of its other results, but not this one.")
rep(r"The floor of Section~9 does not apply to Ye and Li's algorithm, which has no modulus, aliases or checksum;",
    r"The counting floor of Section~9 does not apply to Ye and Li's algorithm, which hashes representations modulo a random prime but has no alias-enumeration phase and no Fourier checksum;")
rep(r"An exploratory analysis by our second referee indicates", r"An exploratory analysis by a second reviewer indicates")

# ---------------------------------------------------------------- Methods (R21, R22, R25)
rep(r"\item \textbf{Independence.} Each certified claim has at least two implementations. Independent referees were fresh agent contexts that saw only the claim's inputs and the source TeX, never the author's code.",
    r"\item \textbf{Independence.} Each certified claim has at least two implementations. Independent reviewers were separate AI agents run in fresh contexts; they were given the claim's inputs and the source \TeX, not the author's code. Some had worked on related parts of the project earlier; where that exposure could matter, the ledger below says so. These reviews are internal cross-checks, not external peer review.")
rep(r"including those found by the referees,", r"including those found by the reviewers,")
rep(r"and Claude Fable 5.1 as the second independent referee,", r"and Claude Fable 5.1 as the second independent reviewer,")
rep(r"Astra also refereed the ternary point and Section~T, gave a second re-derivation of Base's core, and proved part~(i) of the case $k = 1$; a further fresh Claude context re-derived Corollary D from its statement alone. Independent referees were fresh AI agent contexts that saw only the claim's inputs and the source papers.",
    r"Astra also reviewed the ternary point and Section~T, gave a second re-derivation of Base's core, proved part~(i) of Proposition~\ref{prop:k1} and the case $t = 2$ of YP-Hall at $k = 1$, supplied the proofs of parts (ii) and (iii) given in Appendix~\ref{app:B}, and reviewed the whole manuscript, with a further independent interval certificate of the moments of all three parameter points; a further fresh Claude context re-derived Corollary D from its statement alone.")
rep(r"and \texttt{astra\_round6}.",
    r"""and \texttt{astra\_round6}. Each release of the repository is fixed by SHA-256 manifests whose fingerprints, with OpenTimestamps proofs, are listed in \texttt{TIMESTAMP.md}. The complete proofs summarized in Appendix~\ref{app:T} are in the ancillary file \texttt{SECTION\_T\_v3} of this submission. Floating results (optimizer capacities, shadow prices, sweep counts and the negative results) are evidence only; the repository lists the script, inputs and output of each.""")

# ledger rows
rep(r"The 33 numerical conditions of the Section~8 point (0.4875754036), including both moments & Ball arithmetic with analytic quadrature error bounds; two independent referees, each deriving the conditions from the \TeX{} and recomputing with its own code & Certified \\",
    r"The 33 numerical conditions of the Section~8 point (0.4875754036), including both moments & Ball arithmetic with analytic quadrature error bounds; two independent reviews, each deriving the conditions from the \TeX{} and recomputing with its own code; a third independent interval certificate of both moments & Certified \\")
rep(r"The 16-block point of Section~7 (0.4894615727) & Two independent rigorous certificates; block-count audit & Certified \\",
    r"The 16-block point of Section~7 (0.4894615727) & Independent rigorous certificates of the conditions and moments; block-count audit & Certified \\")
rep(r"Lemma~1 and the blocking of 0.48 (Section~5) & Written proof; independent referee; interval evaluation & Proved \\",
    r"Lemma~1 and the exclusion of $\tau \le 0.484$ in the OpenAI budget (Section~5) & Written proof; independent review; interval evaluation by two reviewers (every $\tau \le 0.484$, every $p \in [1,10]$) & Proved \\")
rep(r"The 33 numerical conditions of the conditional point (0.4873407528) & Ball arithmetic; independent recomputation (moments agree to 20 digits); fresh referee with its own condition list and interval code (35 digits) & Certified \\",
    r"The 33 numerical conditions of the conditional point (0.4873407528) & Ball arithmetic; independent recomputation (moments agree to 20 digits); fresh reviewer with its own condition list and interval code (35 digits) & Certified \\")
rep(r"The ternary alias step (Section~T) & Written proof in Base's style; co-author review; fresh referee: no fatal defect, expository repairs only & Refereed; needs [S] \\",
    r"The ternary alias step (Appendix~\ref{app:T}) & Written proof in Base's style; co-author review; fresh reviewer: no fatal defect, expository repairs only, all applied & Reviewed; needs [S] \\")
rep(r"The floor $(1 - \Delta)/2$ and the closed-form bounds (Section~9) & Exact algebra on Base's constraints; numbers from pre-registered floating runs & Floating \\",
    r"The closed-form bounds and the counting floor (Section~9) & Exact algebra on Base's constraints; the floor under the premise of Proposition~\ref{prop:floor} & Proved \\" + "\n" +
    r"Lemma~S, Proposition~\ref{prop:p2} and the case $k = 1$ (Section~10) & Written proofs (Appendix~\ref{app:B}); exhaustive checks from the definitions & Proved \\")
rep(r"The joint capacity near 0.029 and the negative results of Section~9 & Pre-registered floating optimization with controls & Floating \\",
    r"The value 0.4857 of the floor, the joint capacity near 0.029, the shadow prices and the negative results of Section~9 & Pre-registered floating optimization with controls & Floating \\")

# ---------------------------------------------------------------- bibliography
rep(r"Round~5 landscape (\texttt{E2\_LANDSCAPE.md}) and the 0.48 constraint audit (\texttt{target\_048}), Nov 2026. Internal reports, available on request.",
    r"Round~5 landscape (\texttt{E2\_LANDSCAPE.md}) and the 0.48 constraint audit (\texttt{target\_048}), Nov 2026. Included in the repository (Section~11).")
rep(r"""\bibitem{yeli}""", r"""\bibitem{akkn}
P.~Austrin, P.~Kaski, M.~Koivisto and J.~Nederlof. Dense Subset Sum may be the hardest. In \emph{STACS 2016}. \href{https://arxiv.org/abs/1508.06019}{arXiv:1508.06019} [cs.DS].

\bibitem{nw}
J.~Nederlof and K.~W\k{e}grzycki. Improving Schroeppel and Shamir's algorithm for Subset Sum via orthogonal vectors. In \emph{STOC 2021}. \href{https://arxiv.org/abs/2010.08576}{arXiv:2010.08576} [cs.DS].

\bibitem{yeli}""")

open(P, 'w', encoding='utf-8').write(s)
print('OK', len(s))
