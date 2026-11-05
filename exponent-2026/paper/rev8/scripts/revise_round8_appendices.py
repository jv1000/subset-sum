# Appendices A (ternary alias step, from SECTION_T_v3 with the eps0 repair) and B (proofs for Section 10). Claude, 2026-11-05.
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
APP = r"""
%======================================================================
\appendix

\section{The ternary alias step}\label{app:T}

This appendix states the replacement for Base's alias step (Base, Section~5, l.301--612) behind Theorem~\ref{thm:ternary}. The complete proofs, in Base's style and with Base line numbers, are in the ancillary file \texttt{SECTION\_T\_v3} of this submission; everything not restated is as in Base. The result is conditional on [S] and on Base's written proof; the checksum (Base's Section~6 with $J = 1$, as in Section~8) is unchanged.

\textbf{Parameters.} As in Base, with $r = 1 - \mu - l$, $\Delta = \eta - \tau_0$, $\Gamma = 2\tau_0 - \eta$, $a_\Gamma = \Delta/\Gamma$, $\eps = \zeta = 10^{-8}$ and the guard $10^8\lceil\log(b+1)\rceil \le n$. There are two mask fractions, $a$ inside the alias's half-block $S$ and $c$ outside it, with $a' = a + c$; $m = 2\lfloor \mu n/2 \rfloor$, $\sigma = m/2$, $k_1 = \lfloor am \rfloor$, $k_2 = \lfloor cm \rfloor$ and $k' = k_1 + k_2$. Write $H_3(a,c) = -a\log_2 a - c\log_2 c - (1-a-c)\log_2(1-a-c)$.

\textbf{Changes to the procedure.} (1) The trial count is $T = \lceil \bar C_S(m)\, n^8 \lceil 2^m/|\Sigma(M)| \rceil \rceil$, where $|\Sigma(M)|$ is computed exactly by Base's merge procedure and $\bar C_S \ge \max(1, C_S)$ is a fixed polynomial with nonnegative integer coefficients; so $\bar C_S n^8 2^{d(M)} \le T \le 4\bar C_S n^8 2^{d(M)}$. (2) Left records are triples $(\kappa_L, X^+, X^-)$ with $X^+, X^- \subseteq M$ disjoint, $|X^+| = k_1$, $|X^-| = k_2$, and $b(\kappa_L) + b^F(X^+) - b^F(X^-) \equiv j' \pmod{P'}$. (3) Right classes are the sets $Y \subseteq M$ with $|Y| = \sigma - k_1 + k_2$, grouped by $(b^F(Y), c^F(Y))$. (4) A visited member $Y$ is expanded only if $X^+ \cap Y = \emptyset$ and $X^- \subseteq Y$; then $Z = ((X^+ \cup Y)\setminus X^-) \triangle F$ is inserted. (5) Lemmas~T5--T7 below are statements about the \emph{uncapped ideal execution}, the run with Base's time cap removed; reaching the cap is charged separately in Theorem~A$'$.

\textbf{Conditions.} With $\eps_0$ the least slack of (C1R)--(A4R):

\begin{center}
\small
\begin{tabularx}{\linewidth}{>{\raggedright\arraybackslash}p{1.4cm} L >{\raggedright\arraybackslash}p{4.4cm}}
\toprule
& Inequality & Used for \\
\midrule
(C1R) & $\gamma < h(2a)/2 + h(2c)/2$ & enough representations for $P'$ \\
(C2R) & $l + (H_3(a,c) - \gamma)\mu < \tau_0$ & left records \\
(C3) & $r + (1-\gamma)\mu < \tau_0$ & right class records \\
(C4R) & $1 - \mu + (H_3(a,c) + h(\tfrac12 - a + c) - \gamma)\mu - \eta < \tau_0$ & visited tuples \\
(C5R) & $\max(H_3(a,c), h(\tfrac12 - a + c))\mu + \tfrac12 - \tau_0 < \tau_0$ & both mask lists in every trial \\
(C6) & $0 < r < \tau_0$, $l < \tau_0$ & value maps \\
(MU1), (MU2) & $\mu < l$; $\mu \le 1/2$ & deficiency comparison; deficiency bound \\
(A4R) & $\mu(h(2a') + 2a') < \eta$, with $2a' \le 1/2$ & sparse relations survive reduction mod $P$ \\
(SR) & $a' \le 0.11$ & range of [S] obtained from Conjecture M$'$ \\
(EM) & $\mu < \tau_0 - \eps_0$ & exact computation of $|\Sigma(M)|$ \\
(SP) & $\tfrac12 - \tau_0 + \gamma\mu/2 < \tau_0 - \eps_0$ & small-prime trial divisions, all trials \\
(SK) & $r + \tfrac12 - \tau_0 < \tau_0 - \eps_0$ & sorting right keys, all trials \\
(CAP) & $1/\mathrm{guard} + \zeta < \eps_0$ & the cap is reached with probability $o(1)$ \\
(A4G) & $\mu(h(2a') + 2a') + 1/\mathrm{guard} < \eta$ & union bound under the guard \\
(PP), (PD) & $\tau_0 < 1/2$; $\eta/2 < \tau_0 + 20\eps$ & preliminary search; large-prime trial division \\
checksum & $\Delta, \Gamma > 0$; $a_\Gamma \le 3/4$; $p, q \ge 1$; $\rho_c < \rho_f$; $\rho_f + (18 + 6\max(p,q))\eps < \eta$; $\log_2 M_1, \log_2 M_2 < \rho_c$ & Base's Lemmas B1--B3 with $J = 1$ \\
\bottomrule
\end{tabularx}
\end{center}

At the frozen point every condition holds with positive slack (tightest: C1R, $9.99\times10^{-7} = \eps_0$; B3, $8.1\times10^{-7}$); (EM), (SP) and (SK) hold with slacks 0.0127, 0.460 and 0.433, far above $\eps_0$. The condition $a_\Gamma \le 3/4$ is needed because the certificate row $a_\Gamma w - u$ has rounding error $(4a_\Gamma + 3)\eps$, which Base's Lemma~B2 bounds by $6\eps$.

\textbf{Lemma T1} (soundness)\textbf{.} Every key inserted into a dictionary is an alias class of its target.

\textbf{Lemma T2} (right classes)\textbf{.} For fixed $c^F(Y)$ there are at most $2m+1$ possible values of $b^F(Y)$, whatever $|Y|$ is, so Base's right-class bound holds unchanged.

\textbf{Lemma T3} (deficiencies)\textbf{.} With probability $1 - o(1)$ over the partition, $d(M) - d(L) \le 2n^{0.6}$ and $d(M) \le (\tfrac12 - \tau_0 + \zeta)n + n^{0.6}$.

\textbf{Lemma T4} (distinctions survive)\textbf{.} With probability $1 - o(1)$ over $P$, every $\lambda \in \{-1,0,1\}^M$ with at most $2k'$ nonzero entries and $\sum_i \lambda_i c_i \ne 0$ has $P \nmid \sum_i \lambda_i c_i$.

\textbf{Lemma R.} For every signing $w$ of $M$ and a uniform $\sigma$-subset $S$, the family $\mathcal F(S) = \{U \subseteq M : |U \cap S| = k_1,\ |U\setminus S| = k_2\}$ satisfies $\E_S\bigl[|\{w(U) : U \in \mathcal F(S)\}|\big/\bigl(\binom{\sigma}{k_1}\binom{\sigma}{k_2}\bigr)\bigr] \ge a_{k'}(M; w)$. \emph{Proof.} Fix one witness $K_y$ for each distinct $k'$-sum $y$; $S$ admits it, $|K_y \cap S| = k_1$, with probability $\pi = \binom{k'}{k_1}\binom{m-k'}{\sigma - k_1}/\binom{m}{\sigma}$, and admitted witnesses have distinct sums. Double counting pairs $(S, U)$ gives $\binom{m}{k'}\pi = \binom{\sigma}{k_1}\binom{\sigma}{k_2}$. $\square$

\textbf{Lemma T5} (one trial)\textbf{.} In the uncapped ideal execution, on Base's low-deficiency event (LD), under the events of Lemmas T3 and T4, and under [S], a trial for a target and carry inserts the class of a fixed alias with that carry with probability at least $2^{-d(M)}/(16K_0 n^2 (m+1) C_S) \ge 2^{-d(M)}/(C_S n^6)$, where $K_0$ is an absolute constant; the second inequality holds when $n^3 \ge 16K_0$, and the lemma also needs $\lfloor \gamma m\rfloor$ to exceed an absolute constant. [S] enters through Lemma R applied to the signing fixed by the alias.

\textbf{Lemma T6} (coverage)\textbf{.} In the uncapped ideal execution, under the assumptions of Lemma T5, every alias class of every target is inserted, except with probability $o(1)$. (Each miss has probability at most $e^{-n^2}$, since $T \ge C_S n^8 2^{d(M)}$; the constant $C_S$ cancels.)

\textbf{Lemma T7} (work)\textbf{.} Conditioned on the partition and averaged over $P$ and the trials, the uncapped ideal execution takes at most $(b+2)2^{(\tau_0 - \eps_0 + \zeta)n + O(n^{0.6})}$ steps in expectation. Every expanded member is counted, including those that fail the test in step (4).

\textbf{Theorem A$'$.} Under [S], the modified procedure has the properties of Base's Theorem~A for all sufficiently large $n$: on (LD), with $P$ uniform, it returns with probability $1 - o(1)$ values within $1/16$ of the alias phase sums of every target, and on every execution it uses at most $2^{\tau_0 n + 2n^{0.7}}\poly(n + b + 2)$ word operations. Outside the failure events the real run coincides with the uncapped ideal execution. With Theorem~A$'$ in place of Theorem~A, Base's Theorem~1 gives Theorem~\ref{thm:ternary}.

\section{Proofs for Section 10}\label{app:B}

\textbf{The charging reduction.} Let $N(A) = \sum_{X \supseteq A,\,|X| = t} 1/f(X)$ for a $k$-set $A$, and $\mathrm{mult}(u) = \sum_{A:\,w(A) = u} N(A)$. By the definition of $\nu$, $\nu(u) = \mathrm{mult}(u)/(s_t\binom{t}{k})$, so $Q_w \le 1$ if and only if $\sum_u \mathrm{mult}(u)^2 \le s_t \binom{t}{k}\binom{m-k}{t-k}$, that is,
\[\sum_{A \ne A',\ w(A) = w(A')} N(A)N(A') \;\le\; \sum_A N(A)\Bigl(\tbinom{m-k}{t-k} - N(A)\Bigr).\]
The left side is the total weight of the quadruples $(X, X', A, A')$ with $A \subseteq X$, $A' \subseteq X'$, $A \ne A'$, $w(A) = w(A')$, weighted $1/(f(X)f(X'))$; the right side is the total weight of the quadruples $(Y, Y^*, Y'', D)$ with $w(Y^*) = w(Y)$, $Y^* \ne Y$ and $D \subseteq Y \cap Y''$, weighted $1/(f(Y)f(Y''))$. The swap $(X, X', A, A') \mapsto (Y, Y^*, Y'', D) = ((X\setminus A)\cup A',\ X,\ X',\ A')$, defined when $(A' \setminus A) \cap X = \emptyset$, preserves weights and maps those quadruples bijectively onto the quadruples with $D \supseteq Y \setminus Y^*$. Removing both from the two sides leaves exactly the near misses and the targets of Section~10. $\square$

\textbf{The case $k = 1$.} Let $s = s_t$ and $C = \binom{m-1}{t-1}$. For $k = 1$, $\nu$ gives the class $c$ probability $M_c/(ts)$, and $\sum_c M_c = \sum_X t/f(X) = ts$. Hence $Q_w(t,1) = \sum_c M_c^2/(tsC)$, and $Q_w \le 1$ if and only if $\sum_c M_c^2 \le C\sum_c M_c$, which is the stated criterion. Since $\sum_X |X \cap c| = n_c C$, we have $M_c - C = \sum_X |X\cap c|(n_c - f(X))/(n_c f(X))$; the orbit of $X$ under permutations of equal weights lies in its fiber and has at least $n_c$ elements unless $X \supseteq c$, so a positive term needs the whole class in a $t$-set with fewer than $n_c$ witnesses.

\emph{Part (i), $t = 2$.} Let $r$ be the number of classes. A cross profile $\{c, d\}$ ($n_c n_d$ sets, all in one fiber) contributes at most 1 to $M_c$, and the internal profile $\{c, c\}$ at most 2. So $M_c \le r - 1$ for a singleton class and $M_c \le r + 1$ for a repeated one. If no class repeats, $M_c \le m - 1 = C$. If there are two repeated classes or a class of size at least 3, then $r \le m - 2$ and again every $M_c \le C$. Otherwise there is exactly one repeated pair and $m - 2$ singletons, each with $M_i \le m - 2$; if the pair's sum has another witness its internal contribution is at most 1 and $M_0 \le C$. In the remaining case shift the pair to 0. The $G = m - 2 \ge 2$ singleton values are distinct and nonzero, with no opposite pair (it would give a second witness of 0). The 2-sums include $0$ and every singleton value, and one more: the sum of the two values of largest absolute value among those of one sign, if two share a sign; otherwise $G = 2$ and $g_1 + g_2 \notin \{0, g_1, g_2\}$. So $s \ge m$. With $x = M_0 \le m$, the singletons' deficits are at least $\sum_i M_i(C - M_i) \ge \sum_i M_i = 2s - x \ge 2m - x$, and when $x > C$,
$2m - x - x(x - m + 1) = (m - x)(x + 2) \ge 0$. $\square$

\emph{Part (ii), two values.} Normalize the values to 0 and 1, with multiplicities $a \le b$; $m = a + b \ge 2t$, so $b \ge t$. Put $A = \min(a, t)$. There are $A + 1$ distinct $t$-sums, each fiber is one orbit, $M_0 = A(A+1)/2$ and $M_1 = (A+1)(t - A/2)$, and the criterion becomes $(A+1)[A^2 + (2t - A)^2] \le 4Ct$. The left side increases in $A$ (its derivative $6A^2 + (4 - 8t)A + 4t^2 - 4t$ has negative discriminant for $t \ge 2$), so it is at most $2t^2(t+1)$; and $C \ge \binom{2t-1}{t-1} \ge t(t+1)/2$, with equality only at $t = 2$. Equality therefore needs $t = 2$, $m = 4$ and $a = b = 2$. $\square$

\emph{Part (iii), a pair among generic values.} Shift the pair to 0 and let $G = m - 2 \ge 2t - 2$, with $\binom{G}{j} = 0$ outside $0 \le j \le G$. Put $A = \binom{G}{t-2}$ and $B = \binom{G}{t-1}$. Then $M_0 = B + 2A$, each singleton has $M_i = \binom{G-1}{t-1} + \binom{G-1}{t-2} + \binom{G-1}{t-3} \ge B$, $C = A + B$, $M_0 - C = A$ and $C - M_i = \binom{G-1}{t-2}$. Since $G\binom{G-1}{t-2} = (t-1)B$, the criterion reads $M_0 A \le (t-1) B M_i$. Now $A/B = (t-1)/(G - t + 2) \le (t-1)/t$, so $M_0 A \le (t-1)B^2(3t-2)/t^2 \le (t-1)B^2 \le (t-1)BM_i$, using $(t-1)(t-2) \ge 0$. Equality needs $t = 2$ and $G = 2$. $\square$

\textbf{YP-Hall at $k = 1$, $t = 2$.} For $k = 1$ a near miss is $(X, \{p\}, \{p'\})$ with $p \ne p'$ in $X$ of equal weight, and its neighbours under YP are the targets based at sets $Y \ni p$. Summing out the free coordinates, each element $p$ of a class $c$ has demand $S_p = N_c\sum_{X \ni p}(|X \cap c| - 1)/f(X)$, with $N_c = \sum_{X \ni p} 1/f(X)$, and may use the collision sets $Y \ni p$, of capacity $\mathrm{cap}(Y) = \sum_c N_c |Y \cap c|\,(f(Y) - 1 - n_c + |Y \cap c|)/f(Y)$. By submodularity and symmetry it suffices to check Hall's condition on unions of classes. At $t = 2$ every near miss lies on a same-class pair $X = \{p, p'\}$, whose two sources need $2N_c/f_c$, while $\mathrm{cap}(X) = 2N_c(f_c - n_c + 1)/f_c$ ($f_c$ the multiplicity of the pair's sum); this suffices when $f_c \ge n_c$, which holds for classes of size at least 3 and for pairs whose sum is not unique. What remains are pairs with a unique sum, each element needing $N_c$, served from untouched cross-class sets: two or more such pairs use the four cross sets between each two of them (each of capacity at least $(N_c + N_d)/2$); a pair beside another repeated class $d$ uses the $2n_d$ cross sets with $d$; and a pair among $G \ge 2$ singletons uses the sets $\{0, g_i\}$, whose total capacity $K$ satisfies $K/2 \ge s + N_0(G + 1 - 2N_0) \ge N_0$ because $N_0 \le (G+2)/2$ and $s \ge G + 2$. $\square$
"""
anchor = "\n%======================================================================\n\\begin{thebibliography}{99}"
assert s.count(anchor) == 1
s = s.replace(anchor, APP + anchor)
open(P, 'w', encoding='utf-8').write(s)
print('OK appendices', len(s))

# --- wording: remaining "referee" (R21), applied after the appendices
s = open(P, encoding='utf-8').read()
for a, b in [(r"with its certificates and referee reports, and the Section~9 experiments", r"with its certificates and review reports, and the Section~9 experiments"),
             (r"the ternary alias step and its referee reports,", r"the ternary alias step and its review reports,"),
             (r"& Read; the referees derived its numerical conditions from the text &", r"& Read; the reviewers derived its numerical conditions from the text &")]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(P, 'w', encoding='utf-8').write(s)
print('OK wording')

# --- the floor value: computed from our point's Delta = 0.0286969 (floor 0.4856515), rounded DOWN (it is a floor)
s = open(P, encoding='utf-8').read()
for a, b in [
 (r"about 0.4857 at the best capacity we found (about 0.029, not proved optimal).",
  r"about 0.4856 at the capacity of our point ($\Delta \approx 0.0287$; the best joint capacity found in any construction is about 0.029, not proved optimal)."),
 (r"about 0.4857 at the best capacity found so far (Section~9).", r"about 0.4856 at the capacity of our point (Section~9)."),
 (r"with an alias-enumeration phase of the kind used here and the best checksum capacity found so far, no change on the list side can go below about 0.4857.",
  r"with an alias-enumeration phase of the kind used here and the checksum capacity of our point, no change on the list side can go below about 0.4856."),
 (r"(about 0.4857 at the best capacity found)", r"(about 0.4856 at the capacity of our point)"),
 (r"\textbf{Floating.} The value 0.4857 of the counting floor, which uses the best joint checksum capacity found (about 0.029, not proved optimal);",
  r"\textbf{Floating.} The value 0.4856 of the counting floor, which uses the checksum capacity of our point ($\Delta \approx 0.0287$; the best joint capacity found is about 0.029, not proved optimal);"),
 (r"With an alias-enumeration phase of this kind and the best checksum capacity found (about 0.029), the exponent cannot go below about 0.4857 (Proposition~\ref{prop:floor}),",
  r"With an alias-enumeration phase of this kind and the checksum capacity of our point ($\Delta \approx 0.0287$), the exponent cannot go below about 0.4856 (Proposition~\ref{prop:floor}),"),
 (r"Below about 0.4857 the design itself must change:", r"Below about 0.4856 the design itself must change:"),
 (r"The value 0.4857 of the floor, the joint capacity near 0.029,", r"The value 0.4856 of the floor, the joint capacity near 0.029,"),
 (r"S3's left side $0.12945$ (Base: 0.129)", r"S3's left side $0.12946$ (Base: 0.129)"),
]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
assert '0.4857 ' not in s and '0.4857.' not in s and '0.4857,' not in s
open(P, 'w', encoding='utf-8').write(s)
print('OK floor values')
