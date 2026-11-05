# Review of Astra's rev8d (Claude, 5 Nov 2026). Astra wrote rev8d; this is the non-author check.

Inputs: REV8D_SOURCE_AND_VERIFICATION.zip (unpacked outside the preprint folder). Its source_rev8c.tex == preprint/paper.tex (cmp).

PROVED (mechanical)
- All 3 theorems, 3 propositions, 1 lemma, 2 conjectures: verbatim identical to rev8c.
- Frozen candidates: no numeric field changed (base, K16, ternary); only floating display metadata removed.
- semantic_audit on rev8d: 22/26 OK; the 4 "snippet not found" claims were reworded and checked by hand
  (T=0.4875754036 eq; delta ~0.0698 down; Delta=0.0286969377 exact; (1-Delta)/2=0.48565153115 exact).
- number_audit: same 4 flagged "rounded down" contexts as rev8c (all non-exponent uses, reviewed before).
- 28 pages; PDF in preprint/ is byte-identical to the one in the zip.

ERROR introduced in rev8d (Section 9, last paragraph)
- "This leaves less than 1.77e-3 between that floor and the certified threshold." False:
  0.4875754036 - 0.48565153115 = 1.9238e-3. 1.77e-3 is the C4 overhead in the re-optimising table
  (0.4875749 -> 0.4858019). Suggested: "This leaves 1.92e-3 between that floor and the certified threshold;
  removing all of the C4 overhead in the model of the table recovers about 1.77e-3 of it."

CHECKED BY HAND
- Section T rev8d vs Fable's v3 (sha bf75bf98...): only change is (EM),(SP),(SK) stated with the explicit eps0
  slack (my round-7 nit). Correct: T7 needs each item <= tau0 - eps0 + zeta, and the trial count contributes
  zeta, so SP: 1/2 - tau0 + gamma*mu/2 < tau0 - eps0 is exactly what is needed; EM, SK likewise. Slacks 0.0127,
  0.460, 0.433.
- Appendix A: imported-notation paragraph added; row "checksum" -> "B1--B3"; a_Gamma w - u -> a_Gamma v - u,
  consistent with the paper's v(x) (and frees w for the signing in Lemma R). Pointer now says
  "SECTION_T_v3_rev8d.md in the accompanying verification snapshot" -> needs the arXiv anc/ wording.
- Expanded YP-Hall proof (k=1, t=2), Steps 1-4: checked line by line, correct. Optional tightening in Step 2/4:
  say that classes with zero residual demand can be dropped from a minimising cut (they only add neighbours).

EDITORIAL CHANGES FOR JENNIFER TO DECIDE
- Abstract no longer opens with the fifty-years sentence (moved to the first line of the Introduction);
  Ye-Li, Kapila and JoshuaQFEX chronology removed from the abstract (still in history + table).
- Bridge sentence: Astra used "Here we improve this approach and examine the limits of its current analysis."
  Jennifer approved "Here we push this line of work further and examine what limits it." (PENDING_EDITS.md)
- Section 9 retitled "Costs and limitations near the certified point" (was "Why the exponents stall near 0.4876").
- Critical-type table removed (acceptable: it was the floating 16-block point and lacked run provenance).
