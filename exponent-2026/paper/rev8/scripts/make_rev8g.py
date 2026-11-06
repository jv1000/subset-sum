"""rev8g = rev8f + Y. Bills (yannouli) 0.4876723 citation, comparison and Section 3 overlap; repository/companion
wording instead of "arXiv ancillary file"; date line 6 Nov (Claude, 6 Nov 2026). Exact, asserted replacements."""
import sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
R = [
 # date
 (r"\date{Draft, 5 November 2026}", r"\date{Draft, 6 November 2026}"),
 # abstract
 (r"reached 0.4877, and a retuning of Base by JoshuaQFEX reached 0.487676. Here we push",
  r"reached 0.4877, a retuning of Base by JoshuaQFEX reached 0.487676, and a refinement by Y.~Bills reached 0.4876723. Here we push"),
 # history bullet
 (r"JoshuaQFEX~\cite{joshua} retuned Base's parameters to 0.487676, conditional on 430 numerical inequalities.",
  r"JoshuaQFEX~\cite{joshua} retuned Base's parameters to 0.487676, conditional on 430 numerical inequalities, and Bills~\cite{bills} reached 0.4876723 by moving a certificate boundary of Base's filter~3."),
 # table
 (r"& claimed; its 430 moment premises certified here \\",
  r"& claimed; its 430 moment premises certified here and in~\cite{bills} \\"),
 (r"0.487676 & JoshuaQFEX~\cite{joshua} & Base with retuned parameters & conditional on Base \\",
  "0.487676 & JoshuaQFEX~\\cite{joshua} & Base with retuned parameters & conditional on Base \\\\\n"
  r"0.4876723 & Bills~\cite{bills} & Base with a moved certificate boundary for filter 3 & conditional on Base; previous best \\"),
 # contributions
 (r"an independent certification of the 430 moment premises used by the Base/JoshuaQFEX bound.",
  r"an independent certification of the 430 moment premises used by the Base and JoshuaQFEX bounds (Bills~\cite{bills} certifies the same 430 inequalities independently)."),
 # Section 3: new paragraph after the opening one
 (r"clears its assumed margin 0.00025 by $3.79\times10^{-6}$ in $\log_2$.",
  "clears its assumed margin 0.00025 by $3.79\\times10^{-6}$ in $\\log_2$.\n\n"
  r"Bills~\cite{bills} (verification supplement, 22 Oct 2026) independently reports validated enclosures for the same 430 original inequalities, including the stronger middle-region and tail thresholds, using FLINT/Arb ball arithmetic with analytic integration-error bounds, a method close to our Route~A below. Our two routes therefore give a further independent confirmation of that result; we have not compared the two sets of enclosures digit by digit."),
 # Section 8 title and opening
 (r"\section{Below JoshuaQFEX: Base's construction with one asymmetric filter}",
  r"\section{Below the earlier bounds: Base's construction with one asymmetric filter}"),
 (r"JoshuaQFEX retunes Base's parameters to 0.487676.",
  r"JoshuaQFEX retunes Base's parameters to 0.487676, and Bills~\cite{bills} reaches 0.4876723 by stopping filter 3's low certificate at a moved sampling boundary and extending the next certificate downward. Both keep Base's 43 filters; the point below replaces them by a single filter."),
 # Section 8 ternary: companion instead of ancillary; distance to Bills
 (r"its complete proofs are in the ancillary file and the repository (``Section~T'')",
  r"its complete proofs are in the companion file \path{SECTION_T_v3.pdf} and the repository (``Section~T'')"),
 (r"This is $2.34\times10^{-4}$ below the point above and $3.35\times10^{-4}$ below JoshuaQFEX.",
  r"This is $2.34\times10^{-4}$ below the point above, $3.315\times10^{-4}$ below Bills and $3.35\times10^{-4}$ below JoshuaQFEX."),
 # Status and caveats
 (r"$T$ is $1.005\times10^{-4}$ below JoshuaQFEX and $1.14\times10^{-4}$ below Base's $\tau_0$. It is conditional on Base's written proof (its alias-step cost accounting, Lemma A5 and its checksum changes) and on the OpenAI paper, exactly as JoshuaQFEX is.",
  r"$T$ is $9.689\times10^{-5}$ below Bills (0.4876723), $1.005\times10^{-4}$ below JoshuaQFEX and $1.14\times10^{-4}$ below Base's $\tau_0$. It is conditional on Base's written proof (its alias-step cost accounting, Lemma A5 and its checksum changes) and on the OpenAI paper, exactly as JoshuaQFEX and Bills are."),
 # open problem: non-numerical premises
 (r"The OpenAI repository formalizes several of its other results, but not this one.",
  r"The OpenAI repository formalizes several of its other results, but not this one. Bills~\cite{bills} supplies written arguments for several inherited steps (score estimates, effective finite-circle approximation, isolation and aspects of alias handling) and Lean-checked components of the certificate analysis; we have not reviewed them, and they may already cover part of this task."),
 # Files item
 (r"The broader experiment record is maintained at \url{https://github.com/jv1000/subset-sum} in \texttt{exponent-2026}.",
  r"The broader experiment record is maintained in the folder \texttt{exponent-2026} of the repository \url{https://github.com/jv1000/subset-sum}."),
 # ledger
 (r"The 430 moment premises of the 0.487676 bound (Section~3) & Ball arithmetic by two routes; outside check & Certified \\",
  r"The 430 moment premises of the 0.487676 bound (Section~3) & Ball arithmetic by two routes; outside check; also certified independently in~\cite{bills} & Certified \\"),
 # Appendix A
 (r"distributed with this paper (on arXiv as an ancillary file); everything",
  r"distributed with this paper and in the repository \url{https://github.com/jv1000/subset-sum} (folder \texttt{exponent-2026}); everything"),
 # bibliography
 (r"commit bed8e18, 20 Oct 2026.",
  "commit bed8e18, 20 Oct 2026.\n\n\\bibitem{bills}\n"
  r"Y.~Bills (yannouli). subset-sum-conditional-refinement, \url{https://github.com/yannouli/subset-sum-conditional-refinement}, v1.0.0, 21 Oct 2026, and v1.1.0 (verification supplement), commit 590bb68, 22 Oct 2026."),
]
for a, b in R:
    assert t.count(a) == 1, (t.count(a), a[:80]); t = t.replace(a, b)
assert 'ancillary' not in t and 'Below JoshuaQFEX' not in t and t.count(r'\bibitem{bills}') == 1
open(dst, 'w', encoding='utf-8').write(t); print('ok,', len(R), 'replacements')

# Second pass (applied to paper.tex after the first build showed half of page 3 blank: the added row pushed the
# non-floating results table to page 4). Trimmed the new table cells so the table grows by one line only:
#   Base status  -> "claimed; 430 premises certified here and in~\cite{bills}"
#   Bills row    -> "0.4876723 & Bills~\cite{bills} & Base, filter-3 boundary moved & conditional on Base"
# Appendix A wording then changed to: "distributed with this paper and also kept in the folder \\texttt{exponent-2026} of the repository \\url{https://github.com/jv1000/subset-sum}; everything" (avoids a URL break after 'j').
# (A [t] float was tried and rejected: it collided with the notation table and overfilled page 5.)
