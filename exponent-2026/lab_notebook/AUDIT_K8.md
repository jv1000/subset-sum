# C3 audit: is replacing 17 blocks by K = 8 a legitimate adaptation of the OpenAI 0.49 proof?

2026-11-03, Claude. **Classification: reading audit** of the OpenAI 2026-10-04 LaTeX source
(`References/OpenAI_2026-10-04_subset_sum_latex_source.tgz`, all 8 sections read for parameter uses; aliases.tex,
filtering.tex, checksum.tex read in full; setup.tex lines 100–252 and implementation.tex lines 100–344 in full; the
remaining lines grep-checked). Not a proof-assistant check, not outside review. The numerical appendix (numerical.tex)
certifies the OLD filters only and is not reusable; new filters need a new appendix.

## Verdict
Within this reading, **no constraint is missing from Astra's twelve scalar margins plus the moment-stage conditions**.
The constant 17 appears in exactly two places (aliases.tex l.79 block fit; l.336–352 partition + Markov), and both
generalize verbatim to K. Every other block-size dependence is through mu = m/n, not K. The checksum (Section 4) is
generic in (eta, tau). So the K = 8 point is **scalar-admissible under this reading**; whether the algorithm exists at
that point is decided by the new moments (open) and by an independent re-audit.

## Every use, and its replacement
| Source location | Original | Replacement for general K, mu | Astra margin at K=8 point |
|---|---|---|---|
| aliases l.74 | m = 2 floor(.0567 n/2) | m = 2 floor(mu n/2) | — |
| aliases l.79 | 17 m/2 <= floor(n/2) | K m/2 <= floor(n/2); holds for large n when K mu < 1 | blocks .024 |
| aliases l.82, l.300 | h(.0567)+.0567 < .40 | sum_{j<=m} C(n,j)2^j <= 2^{(h(mu)+mu)n+O(log n)}; needs mu <= 1/2 (entropy bound; terms increase for j < 2n/3) | — (mu=.122) |
| aliases l.308 | eta - .40 - .00001 > 0 | eta > h(mu) + mu + guard | sparse .0129 |
| aliases l.166 (generation) | 2^{m + max(l,r)/2} <= 2^{.3067n} | tau >= mu + 1/4 (max(l,r) <= n/2 + O(1) is K-free) | setup .108 |
| aliases l.206 (list) | .48992n | n/2 + (h(1/4) - 1/2 - gamma) m <= tau n (concavity step is mu-free) | list .00051 |
| aliases l.247 (pairs) | .48988n | n + (2h(1/4) - 1 - gamma) m - eta n + guard <= tau n | pairs .1325 |
| aliases l.336–349 | 17 E d(S) <= .01004 n; 1 - .01004/(17·.0106·.0567) > .005 | K E d(S) <= d0 n (superadditivity, any K disjoint parts); Pr >= 1 - d0/(K d mu) - o(1) > c0 | coverage .00267 |
| aliases l.355, l.397 | .4894 > gamma | (1/2 - d) > gamma (gives B >= 2^{gamma m}) | local_to_prime 1e-5 |
| aliases l.424 | .005/(m+1)·(1/2)·1/(4K0n^2) >= n^-4 | c0 replaces .005; any fixed c0 > 0 works | — |
| setup l.157–219 | .01004, .010025, cap .489985 | d0 > d1 (Chebyshev gap, O(1/n) for any fixed gap); cap >= 1/2 - d1 | prelim_cheb, prelim_cap 2.5e-5 |
| implementation l.138, l.284 | eta/2 = .25886 | eta/2 < leading exponent (trial division) | prime .145 |
| checksum l.180–198 | Gamma = .4622 | Gamma = 2 tau - eta > 0; H_pi in [Delta, tau] then automatic | Gamma .29 |
| checksum l.445, l.458 | 8.5, 8.3, 30 eps | p >= 1, 3p <= 30; q_m >= 1, q_m(4a+3) <= 30 | moment stage (q_m <= 5.337) |
| checksum l.473–491 | 0.5169, decay 2^{-.0007n} | rho_f + 48 eps < eta; decay becomes 2^{-(eta - rho_f - 48eps)n}; absorbs Q_n^2 = 2^{O(sqrt n)} for any positive gap | moment stage (5.2e-7 with rho_f .669999) |
| filtering l.94–123 | 2^.5168 / 2^.5169 | M1, M2 < 2^{rho_c}, rho_c < rho_f, finite-circle lemma for the new trig polynomials | **OPEN** |
| checksum l.263 | union over P frequencies | exp(-2^{2 eps d_j - 1}) · q · 2^{eta n} -> 0 for any eta (d_j = Theta(sqrt n)) | — |

K-free and unaffected: isolation (setup l.22–59), prime-collision lemma, Lemma deficiency / random restrictions,
alias subtraction, word-RAM and arithmetic accounting, fallback.

## Two things to state plainly
1. **The point hits 0.48, it does not beat it.** Leading exponent = max(tau + 20 eps, preliminary cap, mu + 1/4,
   eta/2) = max(.48, .48, .372, .335) = .48 exactly. The final step of the paper (implementation l.339) needs a strict
   gap to absorb 2^{O(sqrt n)} poly. So even a full success gives 2^{(.48+o(1))n}; "O(2^{.48n})" needs a point with
   leading exponent < .48.
2. **The checksum does not need small a.** The old monotonicity premises (Delta <= .02776, a <= .02776/.4622) were
   only for transferring the OLD certificate. With fresh moments, a = .655 is allowed; the only a-dependence is
   q_m(4a+3) <= 30, i.e. q_m <= 5.337. The Base/JoshuaQFEX "A < 1/4" belongs to that other construction, not this one.

## Not covered
Correctness of the original proof itself (taken as given); the numerical appendix; any interaction I misread. A second
reader should re-derive at least the partition step and the preliminary coupling.
