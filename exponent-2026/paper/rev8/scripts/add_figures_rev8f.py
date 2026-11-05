"""Insert the two figures (figures/make_figures.py) into rev8f (Claude, 5 Nov 2026)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
F1 = r"""
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_exponents.pdf}
\caption{Exponents discussed in this paper (lower is faster). Blue: this paper; purple: conditional on the open statement [S]; grey: other work. Theorems~1 and~2 have certified numerics and are conditional on the cited written proofs; Base's 0.4877 is its own claim. The dashed line is the counting floor of Proposition~\ref{prop:floor} at the checksum gap of Theorem~\ref{thm:main}, which applies to designs that enumerate every alias class; the dotted line is the floor of the 17-block OpenAI budget found in~\cite{astra}; the shaded band is excluded for the original OpenAI proof's budget by Lemma~1. Meet in the middle (0.5) and Li--Ye (0.4999978) lie off the scale.}
\label{fig:exponents}
\end{figure}
"""
F2 = r"""
\begin{figure}[t]
\centering
\includegraphics[width=0.82\linewidth]{figures/fig_floor.pdf}
\caption{The counting floor $(1-\Delta)/2$ of Proposition~\ref{prop:floor} against the checksum gap $\Delta$, under its enumeration and alias-class-count premises. The point of Theorem~\ref{thm:main} lies $1.92\times10^{-3}$ above the floor at its own gap. Reaching 0.485 with full enumeration needs $\Delta \ge 0.030$, and 0.48 needs $\Delta \ge 0.040$. The dotted line marks the best joint capacity found in our searches (about 0.029, floating evidence; Section~6); the dashed line is the bound on first-moment capacity from Lemma~1 (0.0427).}
\label{fig:floor}
\end{figure}
"""
R = [
 (r"\usepackage{xurl}", "\\usepackage{xurl}\n\\usepackage{graphicx}"),
 ("The table lists the exponents discussed in this paper; lower is faster.",
  "The table and Figure~\\ref{fig:exponents} list the exponents discussed in this paper; lower is faster."),
 ("\\bottomrule\n\\end{tabularx}\n\\end{center}\n\nBase changes both the list construction",
  "\\bottomrule\n\\end{tabularx}\n\\end{center}\n" + F1 + "\nBase changes both the list construction"),
 ("$(1-\\Delta)/2=0.48565153115$ exactly.", "$(1-\\Delta)/2=0.48565153115$ exactly; Figure~\\ref{fig:floor} shows the floor as a function of $\\Delta$."),
 ("\\textbf{What the overhead is.}", F2.strip() + "\n\n\\textbf{What the overhead is.}"),
]
for a, b in R:
    assert t.count(a) == 1, (t.count(a), a[:70]); t = t.replace(a, b)
open(dst, 'w', encoding='utf-8').write(t); print('ok')
