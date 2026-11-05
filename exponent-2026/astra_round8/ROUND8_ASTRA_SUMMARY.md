# Round 8 — for Jennifer

**EVIDENCE — Verdict: MAJOR REVISION, with a sound-looking numerical core.** I would revise this version before posting it as the finished arXiv paper or submitting it to a venue. The prose and PDF look professional, and the work has value. The main problems are scope, missing definitions/proofs, and the order of explanation—not a failed headline numerical certificate. Continuing the research after publication is appropriate; the paper need not solve every open question first.

**PROVED — My own computations confirm all three frozen exponent thresholds and both moments for each candidate**, with interval arithmetic and analytic quadrature error bounds. The headline threshold is exactly **0.4875754036**, safely giving the displayed exponent **0.4875755** under the stated inherited assumptions. I also independently proved the stated proof-budget exclusion for every tau<=0.484 and p in [1,10]. No fatal defect in the headline point was found.

**EVIDENCE — The essential publication repairs are:**

- Narrow the abstract's architectural claim. The algebraic floor needs an explicit large-alias-count premise; capacity near 0.029 is achieved numerically, not proved globally optimal.
- Introduce the model and notation before the constraint tables. Restate Corollary D with its hypotheses, explain how it pays for trials, and bring the main Base theorem forward from page 10.
- Fully define YP-Hall and include the claimed partial proofs. I supplied direct proofs for Q at k=1,t=2 and for the two special families. The stronger Hall proof still needs to appear in the submission.
- Repair the undefined variational target and unsupported equivalence, inconsistent critical-type table, stale verification paragraph, and small parameter/slack errors.
- Separate proved statements, certified inequalities, inherited assumptions and experimental observations. Move most review-process narration to methods and publish a stable artifact manifest.

**PROVED — B agrees with my moment enclosures but does not remove these concerns.** Two JSON fields labelled as directed bounds are rounded the wrong way; their ball enclosures and passing decisions survive. These exports need correction before reuse. The initial report was saved and hashed before B was opened, and its after-B section records the comparison separately.

**EVIDENCE — The future-work boundary should be explicit:** general k=1,t>=3 remains open; the application needs [S] at linear k, not merely k=1; joint checksum capacity is not globally bounded near 0.029; and the remaining imported OpenAI/Base lemmas should be named individually.

**NOT CHECKED —** I did not rerun every historical optimizer, the 430-certificate suite, or the large flow sweeps. Their provenance and exactness need artifact support. A human expert should especially inspect the architectural lower-bound quantifiers, the variational necessity claim, the complete Hall formulation/proof, and the remaining imported algorithmic dependencies.

**EVIDENCE — Start with REFEREE_PAPER.md** for the line-cited issue register and after-B comparison. **EDITORIAL_REPLACEMENTS.md** gives a shorter abstract, revised reading order, Corollary D introduction and future-work ending. NUMERICAL_METHOD.md and MATHEMATICAL_NOTES.md contain the supporting calculations and proofs. Everything is in this out directory. My round-6 exposure is disclosed; this was not a wholly blind review.
