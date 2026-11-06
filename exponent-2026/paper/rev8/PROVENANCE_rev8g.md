# Provenance of revision 8g (Claude, 6 Nov 2026)

Made from rev8f (`drafts/paper_before_rev8g_2026-11-06.tex`, sha256 ae596962…) by
`drafts/make_rev8g.py` (17 exact, asserted replacements) plus the layout pass recorded at the end of that script.
All theorem/proposition/lemma/conjecture statements are unchanged. Exponents and certificates are unchanged.

| Version | Source | PDF | Made by |
|---|---|---|---|
| rev8g (current master) | paper.tex (sha256 18899a6e…e9bd) | Voitle_SubsetSum_certified-0.48758_2026-11-06_rev8g.pdf (4fdc8cab…), 30 pages | drafts/make_rev8g.py on rev8f |

rev8f -> rev8g (Jennifer's decisions, 6 Nov):
1. Cite Y. Bills (yannouli), subset-sum-conditional-refinement, conditional 0.4876723 (v1.0.0, 21 Oct; v1.1.0 verification
   supplement, commit 590bb68, 22 Oct), listed as Claimed/rank 1 on Big O Speedrun on 21 Oct. New \bibitem{bills} [13].
   Mentioned in: abstract, history bullet, results table (new row; Base status now "430 premises certified here and in [13]"),
   contributions paragraph, Section 3 (new paragraph: Bills's 430 enclosures, FLINT/Arb, close to Route A; not compared digit by
   digit), Section 8 opening (mechanism: filter 3's low certificate stops at a moved sampling boundary; both refinements keep
   Base's 43 filters), Status and caveats, ternary paragraph, open problem "Verifying the non-numerical premises" (Bills's written
   arguments and Lean components, not reviewed by us), verification ledger.
2. New distances (displayed 0.4876723, truncated): T is 9.689e-5 below Bills; Theorem 3 is 3.315e-4 below Bills.
   (Earlier chat estimates 9.69e-5 / 3.32e-4 were rounded up; the paper prints the truncated values, as for 1.005e-4.)
3. Section 8 title "Below JoshuaQFEX: ..." -> "Below the earlier bounds: ...".
4. "arXiv ancillary file" removed: Section 8 ternary paragraph -> "companion file SECTION_T_v3.pdf"; Appendix A -> "distributed with
   this paper and also kept in the folder exponent-2026 of the repository https://github.com/jv1000/subset-sum"; Files item reworded
   to the same folder/repository form.
5. Date line -> "Draft, 6 November 2026".
6. Figure 1: Bills row added (grey) in figures/make_figures.py; figures regenerated.

Checks: semantic_audit.py 29/29 OK (two new rows for the Bills distances) -> audit/semantic_audit_out_rev8g.txt; number_audit
same 4 benign flags as rev8f, new unmatched values are only 0.4876723, 9.689e-5, 3.315e-4 -> audit/number_audit_out_rev8g.txt;
pdflatex clean (no warnings); link annotations checked; pages 3-4 inspected (audit/render8g/s-03.png, s-04.png).
arXiv bundle: arxiv/arxiv_submission_2026-11-06_rev8g.zip (0ae4ff8f…), same layout as the 5 Nov bundle (anc/SECTION_T_v3.pdf kept as an ancillary file).
Not changed: to_send/ (still rev8e, the version emailed 5 Nov) and the 5 Nov arXiv bundle.
