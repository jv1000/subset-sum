"""Apply the authorized rev8c follow-up edits; preserve input and record a diff.
Document operations only. Mathematical constants reuse the prior registered audit.
"""
from pathlib import Path
import json, shutil, difflib, hashlib, re

OUT=Path(__file__).resolve().parent
ROOT=OUT/'rev8d'
SRC=Path('D:/AIProjects/SubsetSum/preprint/paper.tex')
A=OUT.parent/'A_paper_and_sources'
original=SRC.read_text(encoding='utf-8-sig')
s=original
changes=[]
def rep(old,new,name):
    global s
    assert s.count(old)==1,(name,s.count(old))
    s=s.replace(old,new)
    changes.append(name)
def par(prefix,new,name):
    start=s.index(prefix); end=s.find('\n\n',start)
    if prefix.startswith(r'\item'):
        stops=[s.find(x,start+len(prefix)) for x in ('\n\\item','\n\\end{itemize}','\n\\end{enumerate}')]
        end=min([end]+[x for x in stops if x>=0])
    assert end>=0
    rep(s[start:end],new,name)
def span(start,end,new,name):
    a=s.index(start); b=s.index(end,a)
    rep(s[a:b],new,name)

rep(r'\date{Draft, 5 November 2026}',r'\date{5 November 2026\\Revision 8d}', 'Identify revision')
span(r'\begin{abstract}',r'\end{abstract}',r'''\begin{abstract}
We study the alias--checksum approach to worst-case Subset Sum introduced by OpenAI and modified by Kapila (``Base''). Here we improve this approach and examine the limits of its current analysis. Conditional on the cited non-numerical proofs, we give a certified parameter point with threshold $T=0.4875754036$: for every fixed $T'>T$, the uniform randomized algorithm uses $O(2^{T'n})$ word operations on inputs of polynomial bit length, with success probability at least $2/3$. In particular, it runs in time $O(2^{0.4875755n})$. A single asymmetric filter replaces Base's family of 43 filters. Independent interval computations certify all required numerical conditions, including both filtering moments and their quadrature errors.

We prove a lower bound on the first filtering moment, valid for all positive continuous densities, that excludes every parameter choice with $\tau\le0.484$ in the original OpenAI proof's sufficient budget. Three algebraic bounds explain the costs at our improved point. Separately, an enumeration phase that inserts at least $2^{(1-\eta-o(1))n}$ alias classes, spending a counted step on each, and uses checksum gap at most $\Delta$ needs exponent at least $(1-\Delta)/2$. This is a conditional operation-count bound; a global upper bound on achievable checksum capacity remains open. Finally, we isolate a small-layer statement that would yield threshold $0.4873407528$, prove combinatorial special cases, and identify the remaining questions.
''','Shorten abstract; precise bridge and scope')
par("Base changes both the list construction and the estimator.",r'''Base changes both the list construction and the estimator. In our tested density families and searches for the original construction (Sections~5--7), the best exponents remain near 0.4895. Combining Base's list construction with our asymmetric filter reaches threshold 0.4875754036 (Section~8). Section~9 distinguishes the costs at that point from a general limitation: under the enumeration and alias-class-count premises of Proposition~\ref{prop:floor}, retaining its checksum gap gives the lower bound $(1-\Delta)/2$.''','Qualify introductory architectural claims')
span('This paper contributes:',r'\subsection*{How to read this paper}',r'''The main contributions are the certified conditional theorem above; a first-moment obstruction for the original sufficient budget and an algebraic analysis of Base's costs; and a precise small-layer conjecture with a conditional ternary improvement and proved special cases. Supporting results include a certified 16-block point for the original OpenAI construction and an independent certification of the 430 moment premises used by the Base/JoshuaQFEX bound.

''','Condense repeated contribution list')
par('Section~2 sets up the model,',r'''Section~2 introduces the model and notation. For the main result, continue to Section~8 (Base's construction, Corollary~D and the certified point), Section~9 (costs and limitations) and Section~10 (the conditional extension and open problems). Section~3 audits the historical Base/JoshuaQFEX certificates; Sections~4--7 analyse the original OpenAI construction and its 16-block improvement. Section~11 gives the methods, verification ledger and AI disclosure. Appendix~\ref{app:T} states the ternary alias step, and Appendix~\ref{app:B} supplies the combinatorial proofs.''','Correct reading guide and distinguish constructions')
# Consolidate the long introductory methods/status material into Section 11.
span(r'\subsection*{How the results were obtained and checked}', '% STATUS-END',r'''\paragraph{Reading the evidence labels.}
``Certified'' describes rigorous numerical inequalities; ``conditional'' describes dependence on the cited algorithmic proofs or an open conjecture. The two labels are compatible. Floating optimization is evidence, not proof. The claim-by-claim ledger in Section~11 separates these categories and records the remaining imported premises.
''','Remove duplicated introductory methods and status summary')
rep('% STATUS-END','', 'Remove obsolete status marker')
rep('The two moments are integrals over the circle with normalized measure.',r'The circle is $\mathbb T=\mathbb R/(2\pi\mathbb Z)$. All means and integrals below use normalized measure $dx/(2\pi)$; the notation $dx$ in circle integrals abbreviates this measure. All logarithms and relative entropies are in bits.','Specify circle and measure')
needle='The pair $(x, w)$ enters through $y - \\theta = x + w$ (correlation, not convolution). With symmetric densities this convention is invisible; with asymmetric ones it matters (Section~7).'
rep(needle,needle+r'''

\paragraph{The filters used in the certificates.}
The coefficient arrays specify log-density polynomials, not densities themselves:
\begin{align*}
r(x)&=\sum_{j=1}^{16}\bigl(r_{c,j}\cos(jx)+r_{s,j}\sin(jx)\bigr),&
s(x)&=\sum_{j=1}^{16}\bigl(s_{c,j}\cos(jx)+s_{s,j}\sin(jx)\bigr),\\
f(x)&=\frac{2^{r(x)}}{\mean 2^r},&g(x)&=\frac{2^{s(x)}}{\mean 2^s}.
\end{align*}
In each candidate file, the first 16 entries of \texttt{rc} are $r_{c,j}$ and the next 16 are $r_{s,j}$, in increasing $j$; \texttt{sc} has the same ordering for $s$. Decimal strings are exact rational inputs. These formulas give strictly positive smooth densities. The scalar right-block fraction $r=1-\mu-l$ used in Base's list analysis is separate from the function $r(x)$.
''','Define filters and coefficient order')
rep(r'Densities $r$, $s$ &',r'Log-density polynomials $r$, $s$ &','Correct filter table label')
rep(r'($P(x) = \mean_w F(x+w)G(w)$)',r'($Q(x) = \mean_w f(x+w)g(w)$)','Use defined correlation notation')
rep(r'\log_2 M_1 = 0.518477576190',r'\log_2 M_1 \approx 0.518477576190','K16 display precision M1')
rep(r'\log_2 M_2 = 0.518477347232',r'\log_2 M_2 \approx 0.518477347232','K16 display precision M2')
par(r'\item \textbf{Reviewer\'s}', '', 'unused') if False else None
par(r"\item \textbf{Reviewer's}",r'\item \textbf{Independent check:} an independently derived condition list and an interval DFT evaluation, including aliasing and tail bounds, give agreement to 16 digits. The provenance and exposure qualifications are recorded in Section~11.','Condense K16 process narrative')
# A local key for Base's certificate-vector notation.
needle=r'\eta_b = 0.51613'+'\n'+r'\end{gather*}'
rep(needle,needle+r'''
Here $z$ is the nonnegative multiplier vector supplied for that filter and region, and $m_\rho$ is the required margin above. To distinguish filter indices from the score $v(x)$, write Base's filter index as $j$. Its score $w_j$ is our second score $v_j$. With $b_0=1$, $b_1=1.25$, $b_2=1.6$, $b_3=2$, $b_4=2.6$, $b_5=3.5$, $b_6=5$, $b_7=8$, $b_8=15$, and a specified comparison set $C$, the rows of $G$ are
\[
\begin{cases}
(\Delta-u_j,\ \Gamma-v_j,\ (u_j-u_h)_{h\in C}),&\rho_0,\\
(a_\Gamma v_j-u_j,\ v_j-\Gamma b_{i-1},\ \Gamma b_i-v_j,\ (u_j-u_h)_{h\in C}),&\rho_i,\ 1\le i\le8,\\
(a_\Gamma v_j-u_j,\ v_j-15\Gamma,\ (u_j-u_h)_{h\in C}),&\rho_9.
\end{cases}
\]
The region fixes a band for the second score's type average. Base's Appendix~C supplies $z$ and $C$ for each row of the certificate inventory; the integral above tests that particular sufficient certificate.
''','Define historical certificate rows')
rep(r'$q(a_\Gamma w - u)$',r'$q(a_\Gamma v - u)$','Consistent high-region score')
rep(r'$a_\Gamma w - u$',r'$a_\Gamma v - u$','Consistent appendix row score')
rep('It is a log power mean of $w$, so it is nonincreasing in $p$; this makes minimizing $\\Phi$ over $p$ rigorous on monotone cells.',r'The function $\Psi$ is a log power mean of $w$ and is nonincreasing in $p$. On a cell $[p_L,p_R]$, $\Phi(p)\ge 1+p_L\Delta+\Psi(p_R)$; this gives rigorous cellwise lower bounds.','Clarify monotone-cell argument')
par("OpenAI's paper proves exponent 0.49.",r'''OpenAI's paper proves exponent 0.49. Section~5 excludes 0.48 for that proof's sufficient conditions, for every parameter choice. The floating exploration below asks a finer question: what limits the best points found within this construction? In the density families and searches tested, joint moment capacity restricts the scalar budget to exponents near 0.4895. Section~8 obtains a lower exponent using Base's modified construction; these searches do not prove that every improvement must use that modification.''','Qualify original-construction landscape')
rep('The binding resource is not the block count but the joint capacity of the two moments:', 'In these searches the binding resource is the joint capacity of the two moments:', 'Scope empirical binding resource')
rep('Two consequences follow.', 'Two observations from these floating searches follow.', 'Label search observations')
par(r'\item \textbf{Fewer blocks alone do not help.}',r'''\item \textbf{Fewer blocks did not help in the tested searches.} With the tested density families and starts, each $K$ from 9 to 13 gave a worse best value than 17 (best 0.48978 at $K=13$). Along the tested continuations toward block size $1/K$ for $K=11,12$, $T$ increased while the moments kept $\Delta$ near 0.0284. These comparisons are not global optima over all densities.''','Qualify fewer-block experiments')
rep('The moments are $\\log_2 M_1 = 0.51626832585128515$ and $\\log_2 M_2 = 0.51626814726466969$, with rigorous error radii below $10^{-20}$; doubling the quadrature resolution changes nothing in 20 digits.',r'The moments are $\log_2 M_1\approx0.51626832585128515$ and $\log_2 M_2\approx0.51626814726466969$, rounded here for display. The full-precision stored balls have rigorous radii below $10^{-20}$; doubled quadrature resolution agrees to 20 digits.','Separate printed rounding from ball radii')
span(r'\textbf{Independent review.}',r'\textbf{A conditional improvement to 0.4873408.}',r'''\textbf{Independent checks and admissibility.} Independently derived condition lists and rigorous moment evaluators confirm the point; Section~11 records their provenance. The checks include Lemma A7 items 1, 3 and 4, S2, S5, the prime draw and $a_\Gamma\le3/4$, required for Base's Lemma B2 row error. Sine terms preserve strict positivity, smoothness and the relative-entropy identities. For the displayed log-density polynomials, summing harmonic amplitudes gives the safe bounds $|r(x)|,|s(x)|<3.21$; every required fixed derivative is bounded explicitly by the corresponding coefficient sum with harmonic powers. Thus the uniform-boundedness argument of OpenAI's Lemma 3.2 applies without an evenness assumption. The stored certificates, rather than rounded displays, carry the numerical error bounds.

''','Condense reviewer narrative and repair uniform bounds')
start='We re-derived each step of Section~T and recomputed every slack and both moments with independent code;'
a=s.index(start); b=s.index('\n\nHere [S]',a)
rep(s[a:b],r'Independent condition extraction and interval quadrature, with analytic error bounds, confirm the frozen point. Section~11 records the proof checks and numerical provenance; Appendix~\ref{app:T} and the accompanying Section~T text state the repaired procedure.','Condense ternary review narrative')
rep(r'$\log_2 M_1 = 0.51599187405865779$, $\log_2 M_2 = 0.51599162047014794$',r'$\log_2 M_1\approx0.51599187405865779$, $\log_2 M_2\approx0.51599162047014794$','Ternary display precision')
rep(r'ours ($10^{-8}$) only raise',r'our choices $\zeta=10^{-8}$ and $\mathrm{guard}=10^8$ only raise','Correct guard typo')
rep(r'$\delta = 0.0698$',r'$\delta\approx0.0698$','Mark rounded delta')
rep(r'\section{Why the exponents stall near 0.4876}',r'\section{Costs and limitations near the certified point}','Scope section heading')
par("This section analyses Base's parameter budget",r'''This section analyses Base's parameter budget at the Section~8 point. The three closed forms are proved algebraic consequences of (C1)--(C8), and Proposition~\ref{prop:floor} is a counting implication under its explicit premises. Evaluation at the frozen point uses its exact decimal parameters. The re-optimizations, sensitivities and negative results are floating evidence from pre-registered experiments C13--C17; they do not establish global optima.''','Separate proved algebra from floating experiments')
par(r'\textbf{Shadow prices.}',r'''\textbf{Local sensitivities (floating evidence).} The following values report the estimated exponent saving per unit relaxation of a constraint near the optimized point, with the filter and other parameters allowed to vary. They describe local sensitivity, not the result of a finite one-bit relaxation:''','Clarify shadow-price interpretation')
par('The list side carries 0.80 of the exponent,',r'''The entries identify the list constraints as the largest local sensitivities. They are not a decomposition of the running-time exponent. Interpreting them as KKT multipliers also requires the constraint normalization and stationarity residuals of the optimization run; the table is used here only as exploratory guidance.''','Remove unsupported KKT normalization claim')
rep("Its value depends on $\\Delta$: at the certified point's $\\Delta = 0.0287$ it is 0.48565, and about 0.029 is the best joint capacity found numerically (Section~6), not a proved maximum.",r'At the frozen point, $\Delta=0.0286969377$ and $(1-\Delta)/2=0.48565153115$ exactly. This evaluation is distinct from the empirical observation that about 0.029 is the best joint capacity found in the searches of Section~6; no global maximum has been proved.','Exact fixed-point floor and empirical ceiling separation')
rep(r'$\mu[(h(a) - \gamma) + (h(1/2 - a) - 1)] = 0.003846$',r'$\mu[(h(a) - \gamma) + (h(1/2 - a) - 1)]\approx0.003846$','Rounded overhead display')
par(r'\textbf{Colour-coding',r'''\textbf{A restricted colour-coding model.} We tested the use of colour-coding~\cite{ayz} that confines left masks to a random region $R$ of size $\rho m$, while $S$ covers half of $R$. For fixed $\rho>0$ and small $a$, the left-mask contribution is $a+a^2/(2\rho\ln2)+O(a^3)$; the right-mask term is $h(1/2-a)-1=-2a^2/\ln2+O(a^4)$. The leading terms favour $\rho=1$. In the tested full-model optimizations, the exponent was worse by $1.4\times10^{-4}$ at $\rho=0.75$, $4.0\times10^{-4}$ at 0.5 and $1.2\times10^{-3}$ at 0.25. These calculations rule out an improvement in those tested configurations, not all uses of colour-coding. They motivate investigating representations that use information about $S$ or a different source of representations.''','Scope colour-coding result')
par(r'\textbf{Summary.} With an alias-enumeration',r'''Under Proposition~\ref{prop:floor}'s enumeration and alias-class-count premises, fixing the checksum gap at our certified value gives the lower bound $0.48565153115$. This leaves less than $1.77\times10^{-3}$ between that floor and the certified threshold. The tested filter families, ternary masks under Base's Corollary~D, and restricted colour-coding model did not remove that distance. The floor is a proved conditional implication; the claims about those searches are floating evidence.''','Repair counting-floor summary')
par(r'\textbf{Beyond the floor of Section~9.}',r'''\textbf{Beyond the fixed-gap counting bound.} Under the enumeration and alias-class-count premises of Proposition~\ref{prop:floor}, retaining the checksum gap of our certified point gives the lower bound $(1-\Delta)/2$. Progress below that bound would require leaving at least one premise, for example by increasing checksum capacity or avoiding full alias-class enumeration. Two narrower questions remain on the list side.''','Carry floor premises into future work')
rep('A construction that knows part of $S$ in advance would remove it; we estimate that this would be worth up to', 'Information about $S$ might reduce that waste; removing it entirely would be worth up to', 'Avoid asserting partial knowledge removes all waste')
needle='the first for $k \\le m/4$, the second by complementation, the last by Lemma~S.'
rep(needle,r'''In Conjecture M$'$, one fixed polynomial $P$ must work for every $m$, every integer weighting, and all integers $0\le k\le0.11m$ and $k\le t\le m-k$; $P$ is independent of the weighting and of $k,t$. The first implication covers $k\le m/4$, the second uses complementation, and the last is Lemma~S.''','State uniform polynomial quantifiers')
# Do not retain an unidentified optimizer's table as evidence about both moments.
a=s.index('At a floating 16-block point of the OpenAI construction'); b=s.index('\n\\begin{enumerate}',a)
rep(s[a:b],r'''The two maximizing densities are generally different. The searches suggest investigating types near the corner $U=\Delta$, $V=\Gamma$, where the sampling boundary meets the case switch, but do not establish equality there for both moment maximizers. A possible route to a joint bound is an ``amplitude costs entropy'' inequality: a lower bound on $\E_\nu v$, valid for every filter pair, in terms of $\E_\nu\lambda$, $\KL(\nu)$ and $\E_\nu u$. We have not proved one.
''','Remove critical-type table pending optimizer provenance')
rep('The SOR iteration, working on unrestricted grid densities, cannot improve it.', 'The tested SOR iteration on unrestricted grid densities did not improve it.', 'Scope SOR evidence')
rep('It is not binding at the current joint optimum, but it would be after any capacity gain.', 'It is not binding at the current best joint point, but may become relevant at larger capacities.', 'Avoid universal rounding-cap forecast')
par(r'\item \textbf{Other domination steps.}',r'''\item \textbf{Other domination steps.} Lemma~1 restricts the sufficient moment format, not Subset Sum. In the experiments, replacing the two affine forms by up to 32 forms $c_0+c_1u+c_2v$, each dominating a strip of patterns in the convex hull of $(u(x),v(x))$, did not improve capacity: the reported values remained 0.02810 for the earlier densities and 0.02906 for the new ones. The active patterns in these runs lay near the case switch $V=\Gamma$. This suggests studying a different sampling/direct split or match-count bound; it does not prove that all refinements of the domination step fail.

For amplitude tilting, define, for fixed densities and multiplier $p$,
\[
\psi(c)=\log_2\int_{\mathbb T}2^{c\lambda(x)+p(\Delta-u(x))}\,dx,
\qquad \lambda(x)=\log_2(2+2\cos x).
\]
Thus $\psi(1)=\log_2 M_1$ and $\psi'(1)=\E_{\nu_1}\lambda$, where $\nu_1$ is the normalized integrand at $c=1$. Also $\partial_p\log_2 M_1=\Delta-\E_{\nu_1}u$. At an interior minimum with respect to $p$, the latter derivative vanishes. This identity alone does not prove a global minimax statement or identify the two moments' maximizing types. In the tested joint optimizations of densities, amplitude tilts, cutoffs and affine certificates, the amplitude coefficient returned to 1. Separate sampling-budget and threshold variations also gave no improvement in the tested model. A rigorous obstruction for these richer estimator families remains open.''','Replace unsupported minimax narrative with defined identities and scoped evidence')
rep('All results here inherit the non-numerical lemmas', 'The algorithmic running-time claims inherit the non-numerical lemmas', 'Scope inherited dependencies')
rep('the layer question below.', 'the layer question discussed above.', 'Correct direction of reference')
# Put methodological explanations once, in Methods.
par('Every experiment was pre-registered before it ran,',r'''The constraints were extracted from the cited proof sources and optimized in floating point. Certification then evaluated the frozen decimal inputs using interval or ball arithmetic, with analytic bounds for both quadratures. Agreement between resolutions is a control, not an error bound. A strict inequality is certified only when its entire enclosure lies on the required side. Floating capacities, sensitivities and negative searches remain evidence rather than global bounds. Experiments were pre-registered with predictions, controls and stopping rules, and negative results were retained. The work was carried out by the author with the AI systems identified below.''','Consolidate methods explanation')
par(r'\item \textbf{Files.}',r'''\item \textbf{Files and versioning.} The accompanying revision-8d verification snapshot contains the three frozen candidate files, independent interval results and verifier sources, the analytic error argument, and \texttt{SECTION\_T\_v3\_rev8d.md}, the complete ternary proof with the work-bound repair used in Appendix~\ref{app:T}. Its \texttt{MANIFEST.json} records SHA-256 hashes, and \texttt{ARTIFACT\_GUIDE.md} maps claims to files and explains coefficient ordering and exact-decimal inputs. The broader experiment record is maintained at \url{https://github.com/jv1000/subset-sum} in \texttt{exponent-2026}. The local verification snapshot covers the three frozen points and the stated independent budget check; it is not a replacement for the historical 430-certificate data or the optimizer and search logs. Those claims retain the evidence status recorded in the ledger.''','Pin local verification snapshot without inventing external release')
rep(r'Lemma~S, Proposition~\ref{prop:p2} and the case $k = 1$ (Section~10)',r'Lemma~S, Proposition~\ref{prop:p2}, the special cases of Proposition~\ref{prop:k1}, and YP-Hall at $k=1,t=2$','Scope ledger special cases')
rep('The value 0.4856 of the floor, the joint capacity near 0.029, the shadow prices and the negative results of Section~9', 'The empirical joint capacity near 0.029, the local sensitivities and the negative results of Section~9', 'Correct floating ledger category')
rep('Exact algebra on Base\'s constraints; the floor under the premise of Proposition~\\ref{prop:floor}',r'Exact algebra on Base\'s constraints; the floor under Proposition~\ref{prop:floor}\'s premises; exact value $0.48565153115$ at the frozen gap'.replace("\\'","'"),'Ledger exact fixed-gap value')
# Keep all section numbers stable; add an agenda without adding a section.
needle=r'\section{Methods, reproducibility and AI collaboration}'
rep(needle,r'''\paragraph{Research priorities.}
The main next steps are to prove or refute [S] in the linear range needed by Theorem~\ref{thm:ternary}; prove a global joint-capacity bound or certify a better filter; reduce list costs by changing a premise of the fixed-gap enumeration bound; and complete the specifically identified inherited proof checks. The general case $k=1,t\ge3$ remains an intermediate combinatorial question, not a substitute for the required linear range.

'''+needle,'Add focused research agenda')
# Make the ancillary name precise everywhere it occurs in main.tex.
s=s.replace(r'\texttt{SECTION\_T\_v3} of this submission',r'\texttt{SECTION\_T\_v3\_rev8d.md} in the accompanying verification snapshot')
needle=r'\textbf{Changes to the procedure.}'
rep(needle,r'''\textbf{Imported notation.} The transformed input weights are $c_i$, and $b_i=c_i\bmod P\in\{0,\ldots,P-1\}$. For a flip set $F\subseteq M$, put $c_i^F=(-1)^{[i\in F]}c_i$ and $b_i^F=(-1)^{[i\in F]}b_i$; a set argument denotes the sum of those signed weights. A left outside-block value class is denoted $\kappa_L$, and $b(\kappa_L)$ is its residue-weight sum. The small-prime residue chosen in a trial is $j'$. Event (LD) is Base's low-deficiency condition after the preliminary search. The full inherited procedure, including the targets and carry indices, is specified in Base, Section~5, and the accompanying Section~T text.

'''+needle,'Define imported ternary notation')
rep(r'$9.99\times10^{-7} = \eps_0$',r'$\eps_0\approx9.99\times10^{-7}$','Avoid equality to rounded ternary slack')
hall=r'''\textbf{YP-Hall at $k=1$, $t=2$.}
We prove the stronger charging statement for every weighting with $m\ge4$.

\emph{Step 1: aggregate sources and targets.} For an element $p$ in an equal-weight class $c$, put
\[
N_c=\sum_{X\ni p}\frac1{f(X)},\qquad
S_p=N_c\sum_{X\ni p}\frac{|X\cap c|-1}{f(X)}.
\]
The first value is independent of the choice of $p\in c$ by symmetry. A near miss with $A=\{p\}$ chooses $p'\ne p$ of the same weight inside $X$, and its free set $X'$ contains $p'$. Summing over $X'$ gives $N_c$, hence the demand $S_p$. All these near misses have exactly the targets based at $Y\ni p$ as neighbours, so aggregation preserves the fractional feasibility problem.

For a fixed target set $Y$, summing over $Y''$ for $D=\{d\}$ gives $N_c$ when $d\in c$. Among the $f(Y)-1$ other witnesses $Y^*$, precisely $n_c-|Y\cap c|$ are obtained by replacing $d$ with an equal-weight element outside $Y$; these are excluded by $D\supseteq Y\setminus Y^*$. Thus the available capacity at $Y$ is
\[
\operatorname{cap}(Y)=\sum_c N_c|Y\cap c|\,
\frac{f(Y)-1-n_c+|Y\cap c|}{f(Y)}.
\]
The aggregated graph joins $p$ to $Y$ exactly when $p\in Y$.

\emph{Step 2: reduce cuts to unions of classes.} For an element set $H$, let
\[
F(H)=\sum_{Y:Y\cap H\ne\varnothing}\operatorname{cap}(Y)-\sum_{p\in H}S_p.
\]
The first term is a weighted coverage function, hence submodular; the second is modular. Moreover $F$ is invariant under permutations within each equal-weight class. Minimizers of a submodular function are closed under unions. The union of all such permutation images of a minimizer is therefore a minimizing union of classes. Consequently a negative Hall cut, if any, has a class-union witness. The same argument applies to the residual graph below, which has the same class symmetries.

\emph{Step 3: use the internal pairs.} Every source at $t=2$ arises from a pair $X=\{p,p'\}$ of equal-weight elements in a class $c$. Write $f_c=f(X)$. The two ordered sources associated with this pair have total demand $2N_c/f_c$, while
\[
\operatorname{cap}(X)=\frac{2N_c(f_c-n_c+1)}{f_c}.
\]
If $f_c\ge n_c$, this capacity pays both sources on their own pair. This condition holds whenever $n_c\ge3$, since $f_c\ge\binom{n_c}{2}\ge n_c$, and when $n_c=2$ and the pair's sum has another witness. Make these assignments independently for every such internal pair. They use no cross-class set. Singleton classes have zero demand. The only residual sources are isolated repeated pairs: classes of size 2 whose internal sum has multiplicity 1. Each element of such a class has remaining demand $N_c$.

\emph{Step 4: pay the residual class-union cuts.} Consider a nonempty union of $q$ isolated repeated-pair classes. If $q\ge2$, each two of these classes $c,d$ have four cross sets. Their common-sum multiplicity is at least 4, so each cross set has capacity at least $(N_c+N_d)/2$. The total capacity of these sets is at least
\[
2\sum_{c<d}(N_c+N_d)=2(q-1)\sum_c N_c\ge2\sum_cN_c,
\]
the demand of the cut.

It remains to consider a cut consisting of one isolated pair $c$. If another repeated class $d$ exists, its $2n_d$ cross sets with $c$ have multiplicity at least $2n_d$. The contribution of $c$ alone to their total capacity is at least
\[
2n_dN_c\left(1-\frac2{2n_d}\right)=2(n_d-1)N_c\ge2N_c.
\]
These cross sets are untouched by Step 3, even if class $d$ was already served there.

Finally suppose the only repeated class is the isolated pair. Shift its value to 0, write the $G=m-2\ge2$ singleton values as $g_i$, and put $N_0=N_c$, $f_i=f(\{0,g_i\})$, and $N_i=\sum_{X\ni g_i}1/f(X)$. There are two cross sets for each $g_i$, and $f_i\ge2$. Since the internal pair has a unique sum,
\[
N_0=1+\sum_i\frac1{f_i}\le\frac{G+2}{2},\qquad
\sum_iN_i=2s-2N_0,\qquad s\ge G+2.
\]
The last inequality was proved in part (i): the sums include 0, all $g_i$, and an additional value. Let $K$ be the total capacity of these cross sets. The capacity formula gives
\begin{align*}
K/2&=N_0(G+2-2N_0)+\sum_iN_i(1-1/f_i)\\
&\ge s+N_0(G+1-2N_0)\\
&\ge s-N_0\ge N_0.
\end{align*}
Thus every residual class-union cut has sufficient capacity. Step 2 implies all residual Hall inequalities, and adjoining the assignments of Step 3 gives the required fractional charging. $\square$
'''
span(r'\textbf{YP-Hall at $k = 1$, $t = 2$.}', '%======================================================================\n\\begin{thebibliography}',hall+'\n','Expand complete Hall proof')

rep(r'p{2.3cm} >{\raggedright\arraybackslash}p{2.6cm} L L',r'p{2.2cm} >{\raggedright\arraybackslash}p{2.7cm} L L','Fit comparison-table label')
rep('\nchecksum &', '\nB1--B3 &', 'Fit appendix condition label')
s=s.replace(r'\texttt{SECTION\_T\_v3\_rev8d.md}',r'\path{SECTION_T_v3_rev8d.md}')
s=s.replace(r'\texttt{MANIFEST.json}',r'\path{MANIFEST.json}')
s=s.replace(r'\texttt{ARTIFACT\_GUIDE.md}',r'\path{ARTIFACT_GUIDE.md}')
s=s.replace(r'and \path{ARTIFACT_GUIDE.md} maps claims to files',r'and the accompanying artifact guide maps claims to files')
s=s.replace('For amplitude tilting, define, for fixed densities and multiplier $p$,','For amplitude tilting, define, for fixed densities and multiplier $p$, and for $c$ near 1,')
rep(r'Round~5 landscape (\texttt{E2\_LANDSCAPE.md}) and the 0.48 constraint audit (\texttt{target\_048}), Nov 2026.',r'Round~5 landscape and 0.48 constraint audit, Nov 2026. Files \path{E2_LANDSCAPE.md} and \path{target_048}.','Allow bibliography filenames to wrap')

ROOT.mkdir(exist_ok=True)
(ROOT/'source_rev8c.tex').write_text(original,encoding='utf-8')
(ROOT/'main.tex').write_text(s,encoding='utf-8')
(ROOT/'changes.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='rev8c/paper.tex',tofile='rev8d/main.tex')),encoding='utf-8')
(ROOT/'edit_log.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
verification=ROOT/'verification'; verification.mkdir(exist_ok=True)
candidates=verification/'candidates'; candidates.mkdir(exist_ok=True)
for name in ('base','K16','ternary'):
    data=json.loads((A/'candidates'/f'candidate_{name}.json').read_text(encoding='utf-8-sig'))
    # Freeze algorithmic input strings; exclude stale optimizer-derived display metadata.
    data.pop('floating_margins',None); data.pop('floating_T',None)
    if 'certificate_format' in data: data['certificate_format']='rho0: z=(p,0); rho1..rho8: z=(q,0,0); rho9: z=(q,0)'
    (candidates/f'candidate_{name}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
for name in ['interval_core.py','audit_numbers.py','verify_moments.py','verify_blocking.py','check_combinatorics.py','numbers.json','moments_base_4096.json','moments_K16_4096.json','moments_ternary_4096.json','blocking.json','combinatorics.json','NUMERICAL_METHOD.md','MATHEMATICAL_NOTES.md']:
    shutil.copy2(OUT/name,verification/name)
p=verification/'audit_numbers.py'
p.write_text(p.read_text(encoding='utf-8').replace("SRC=OUT.parent/'A_paper_and_sources'/'candidates'", "SRC=OUT/'candidates'"),encoding='utf-8')
t=(A/'SECTION_T_v3.md').read_text(encoding='utf-8-sig')
t=t.replace('# Section T (v3).','# Section T (v3, revision 8d).',1)
t=t.replace('| (EM) | μ < τ0 |','| (EM) | μ < τ0 − ε0 |')
t=t.replace('| (SP) | ½ − τ0 + ζ + γμ/2 < τ0 |','| (SP) | ½ − τ0 + γμ/2 < τ0 − ε0 |')
t=t.replace('| (SK) | r + ½ − τ0 + ζ < τ0 |','| (SK) | r + ½ − τ0 < τ0 − ε0 |')
old='The script checks (SP) and (SK) in the stronger form with ε0 subtracted in place of ζ\n(slacks 0.4604 and 0.4334); Astra\'s inventory states them with ζ, as above. (EM), (PP), (PD) were implicit in v2.'
assert old in t
t=t.replace(old,'Revision 8d requires (EM), (SP) and (SK) with the explicit ε0 slack needed by T7, as in the paper appendix. The frozen point already satisfies these stronger requirements; no input parameter is changed. The ζ term from the trial count is retained in T7\'s overall exponent. (EM), (PP), (PD) were implicit in v2.')
t=t.replace('v3 (round 7):', 'Revision-8d note: the historical candidate hash below identifies the original JSON, including its metadata. The accompanying snapshot preserves every numerical input and corrects or omits obsolete display metadata; use MANIFEST.json for its file hashes.\n\nv3 (round 7):',1)
(verification/'SECTION_T_v3_rev8d.md').write_text(t,encoding='utf-8')
print(json.dumps({'edits':len(changes),'source':str(SRC),'revised':str(ROOT/'main.tex'),'snapshot':str(verification)},indent=2))
