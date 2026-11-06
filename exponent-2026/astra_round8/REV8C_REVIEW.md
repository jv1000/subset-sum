# Review of rev8c against the round-8 recommendations

EVIDENCE — Reviewed for Jennifer on 5 November 2026. Input: `D:/AIProjects/SubsetSum/preprint/Voitle_SubsetSum_certified-0.48758_2026-11-05_rev8c.pdf`, 29 pages. Page numbers below are the printed PDF page numbers. This is a follow-up review of the supplied PDF against my earlier R1–R26 register, not a new blind review or a fresh certification of the external release. I read all pages and inspected rendered contact sheets of all pages. I did not edit the manuscript.

## Assessment

EVIDENCE — **Substantially improved; close to an arXiv-ready conditional research paper after a focused correction pass.** I found no new fatal defect in the headline result. The most serious earlier presentation and logical gaps have been addressed: a formal main theorem appears on page 3; Corollary D is explained and stated with its hypotheses; the counting proposition has an explicit premise; the variational identities are correctly stated over all densities; YP-Hall now has a complete weighted graph; and the missing elementary combinatorial proofs are in Appendix B. These are substantive improvements, not cosmetic ones.

EVIDENCE — I would no longer recommend a wholesale rewrite before posting. I would fix the remaining scope statements, make the filter definition explicit, expand the Hall argument, and freeze the supporting artifacts before calling this the publication version. The typography is conventional and professional. The paper can add value now through its conditional certified improvement, its proved restriction on a precisely specified sufficient budget, and its explicit combinatorial research questions. Completing all future research is not a prerequisite for publishing those results.

EVIDENCE — A venue submission would benefit from a more economical organization: foreground the new theorem and its reusable certificate, and move more historical verification and experiment narrative into supporting material. That is a recommendation about exposition and emphasis, not a finding that the conditional theorem is invalid.

## Necessary corrections and important clarifications

### C1. Carry the counting proposition's premise into its summaries — repairable, important

PROVED — Proposition 1 on page 16 now explicitly assumes an execution/instance with at least `2^((1-eta-o(1))n)` alias classes and an enumeration step that inserts every class. Its argument is valid under that premise. However, the summaries on page 4 ("no change on the list side"), page 17 ("the exponent cannot go below"), and page 18 ("the design itself must change") again read more broadly. Page 1's abstract is better because it explicitly says the enumeration phase faces that many classes.

EVIDENCE — Replace the page-18 sentence with: "Under the enumeration and alias-class-count premises of Proposition 1, retaining the checksum gap of our certified point gives the lower bound (1-Delta)/2. Progress below that bound would require leaving at least one of those premises, for example by increasing checksum capacity or avoiding full alias-class enumeration." Use the same qualification in the other summaries. A bound on an explicitly defined phase is useful; the paper need not turn it into a universal lower bound on the architecture.

PROVED — For the exact frozen point, `Delta = 0.0286969377` and `(1-Delta)/2 = 0.48565153115`, already computed in my prior exact-input audit. This arithmetic is not a floating optimization. Pages 6 and 25 still label the numerical value of the fixed-point floor "Floating", while page 15 says "nothing in this section is certified". Separate (a) the proved conditional counting implication and exact evaluation at the frozen point from (b) the empirical assertion that roughly 0.029 might be globally optimal. The latter remains unproved.

### C2. Remove residual general conclusions from finite experiments — repairable, important

PROVED — Several statements still exceed the scope stated for their supporting evidence:

- Page 4: both Base changes are "needed" below about 0.4895.
- Page 11: "Fewer blocks alone do not help" and "every K from 9 to 13 is worse" without restricting the claim to the tested families and searches.
- Page 17: "Colour-coding does not remove it" and "Removing the waste needs ...", following one particular restricted-mask model.
- Page 22: "Escaping the wall therefore needs a change of the target itself" and "Both moments' tilted means sit at the same critical pattern".

EVIDENCE — Use formulations such as "In the density families and searches tested ...", "This restricted colour-coding model did not improve the bound", and "These experiments suggest investigating a different target or estimator." Keep any genuinely general algebraic statement, but supply its proof and hypotheses separately. The local expansion with an `O(a^3)` remainder on page 17 does not by itself prove a global comparison over every region size rho; either cite the exact model inequality or scope that conclusion to the computed model.

PROVED — Page 21 now correctly calls the critical-type values approximate and reports their discrepancy from the corner. Page 22's exact-sounding common-corner assertion therefore reintroduces part of R16. Say whether it refers to the same run, a different run, or a limiting conjecture. Specify which of the two moment maximizers the page-21 table describes; the two Gibbs tilts need not be the same probability density.

### C3. Define the actual filters and finish the notation cleanup — repairable, important for reuse

PROVED — Page 8 defines the moments using positive densities f and g. Page 12 instead lists "Densities r, s" with cosine and sine coefficients, without explaining their relationship to f and g. The paper needs the construction, not just a JSON filename.

PROVED — In the convention used by the already audited candidates, write the trigonometric polynomials explicitly, for example

    r(x) = sum_{j=1}^{16} (r_c,j cos(jx) + r_s,j sin(jx)),
    s(x) = sum_{j=1}^{16} (s_c,j cos(jx) + s_s,j sin(jx)),
    f(x) = 2^{r(x)} / mean(2^r),
    g(x) = 2^{s(x)} / mean(2^s).

EVIDENCE — Define the coefficient ordering and exact-decimal interpretation in the artifact guide. Call r and s log-density polynomials, not densities. State once that the circle is R/(2 pi Z), integrals use normalized measure dx/(2 pi), and logarithms/KL are in bits. This makes the cosine arguments and normalization unambiguous.

PROVED — Other remaining notation problems are small but real: page 13 uses `q(a_Gamma w-u)` after defining the score as v; page 22 switches from V to W without a definition; `psi'(1)` there has no definition of psi; the nearby capital Psi from Lemma 1 is a different function. Page 8's Section 3 introduces z and G(x) without a usable description of their entries, and page 25 introduces b_F, c_F and LD by inheritance from Base rather than local explanation.

EVIDENCE — Use v and V consistently, define the amplitude-tilted log-partition function before differentiating it, and either give a brief region-row key in Section 3 or move its source-dependent formula to a technical appendix. Appendix A may rely on Base, but add a compact notation key for its imported symbols. Also give Conjecture M' its full quantifiers: one polynomial P, independent of the weighting and of k, valid uniformly in the stated range. Its table entry currently leaves that uniformity implicit.

### C4. Expand the Hall proof enough to be independently usable — repairable, proof exposition

EVIDENCE — Appendix B now contains the missing arguments for Q at k=1,t=2 and for the two families. On rereading, the charging reduction, the Q criterion, and those three proofs are coherent. The t=2 Hall argument also follows the earlier construction, but page 28 compresses several nontrivial steps into a single paragraph. That is the most important place to spend additional explanatory space.

EVIDENCE — Break it into four steps: aggregate demands and capacities; reduce cuts to unions of equal-weight classes; satisfy the non-isolated classes with their internal collision sets; handle the remaining isolated pairs using cross-class sets. In particular, explain why the first allocations leave the later capacity unused, why the three remaining cases exhaust the cuts, and why a source subset may be replaced by the whole aggregated source at an element.

PROVED — The symmetry/submodularity sentence can be justified as follows. For a set H of elements define the deficit `F(H)=capacity(N(H))-demand(H)`. Coverage capacity is submodular and demand is modular. The function is invariant under permutations within each equal-weight class. Minimizers of a submodular function are closed under unions; taking the union of all class-permutation images of a minimizing set therefore yields a minimizer that is a union of classes. A negative cut would consequently have a class-union witness. State this argument, rather than only naming symmetry and submodularity.

PROVED — In the final isolated-pair case, define `f_i=f({0,g_i})` and `N_i` explicitly. Then display the missing calculation:

    K/2 = N_0 (G+2-2N_0) + sum_i N_i(1-1/f_i)
        >= s + N_0(G+1-2N_0)
        >= N_0.

Here `f_i>=2`, `sum_i N_i=2s-2N_0`, `N_0<= (G+2)/2`, and `s>=G+2`. These facts explain both inequalities. Likewise write the total capacity bound for a pair next to another repeated class, instead of merely naming the cross sets. This is a completion of exposition of the existing proof, not a new conjectural ingredient.

### C5. Fix the precision language and the unexplained 3.20 bound — repairable

PROVED — Page 14 prints moment values to roughly 17 decimal places and immediately says their rigorous error radii are below `10^-20`; the second review gives a radius below `4*10^-55` next to the same short displays. Those error radii must refer to the full-precision stored balls, not to the displayed decimal centers. For example, the previous independent enclosure of log2 M2 is

    [0.51626814726466968639, 0.51626814726466968640],

which does not contain the printed value `0.51626814726466969` within radius `10^-20`.

EVIDENCE — Use approximation signs and say "values rounded for display; the full-precision certificate balls have radii ...". Alternatively print outward-rounded interval endpoints. The passing margins are unaffected.

PROVED — Page 14 says the uniform and derivative bounds "change from 2.433 and 4.010 to 3.20". In the supplied OpenAI `filtering.tex`, lines 134–159, 2.433 and 4.010 are bounds for |r| and |s|, with derivative bounds discussed separately. My earlier coefficient-amplitude audit gave an upper bound approximately 3.20263022124 for the new s polynomial by summing harmonic amplitudes.

NOT CHECKED — That amplitude sum does not disprove a sharper supremum bound of 3.20; I have not certified or refuted that sharper bound. Either supply its actual certificate, or use the already safe 3.21 bound for |r| and |s| and state separately that each needed fixed derivative has a finite explicit coefficient bound. Do not describe one number as a bound for all derivatives. This is not evidence of a failure of the asymptotic finite-circle argument.

### C6. Pin the release and verify that the claimed export repairs reached it — repairable, reproducibility

EVIDENCE — Page 24 is much better than an "available on request" statement: it names the repository, manifests and a Section T ancillary file. It still does not identify which exact release/commit/manifest belongs to this PDF. Add a release identifier or immutable archive citation, the precise ancillary filename and format, and a short claim-to-input/verifier/output map. A reader should not have to search several notebook directories to find the certificate for Theorem 1.

NOT CHECKED — I reviewed the supplied PDF, not a newly published repository release or an attached ancillary file. The PDF's statement that exports use directed rounding is not verification that the earlier Base C8 lower-bound export, K16 M2 upper-bound export, and underflowed outer-error field were repaired. The page-9 sentence is also in Section 3, whereas those two previously defective exports concern Sections 7 and 8. Before release, check the actual decimal strings and their directions against the full balls, preserve nonzero analytic error bounds, and include the corrected rho9 metadata and ternary conditions in the frozen package. No rerun of all experiments is implied by this recommendation.

EVIDENCE — Section T should preferably be a readable PDF or a compiled appendix as well as its editable source. Novel proof details can live in ancillary material, but must accompany the version being cited. The PDF alone contains statements of T1–T7, not their complete proofs.

### C7. Correct a handful of status, history and measurement statements — repairable, local

PROVED — Page 5 says Sections 3–7 concern the original OpenAI construction, then lists Section 3's 0.487676 certification. That result concerns the Base/Joshua construction. Replace the sentence with a description that separates the retrospective certificate audit from the original-OpenAI analysis. Likewise page 1's "Within the original OpenAI construction ... and the 430 moment premises" groups two different constructions; split it into two sentences.

PROVED — Page 15 says "The constants zeta and the input guard ... ours (10^-8)" although the table gives the input guard as `10^8`. Write `zeta=10^-8` and `guard=10^8` explicitly. This is an explanatory typo, not a change to the candidate.

EVIDENCE — Page 15 describes shadow prices as loosening each constraint "by one bit" and reoptimizing. KKT multipliers describe local derivatives per unit of relaxation, not an arbitrary finite one-bit perturbation. State whether these are multipliers or small-step finite differences, and give the step-size/control in the artifact. On page 16, "the list side carries 0.80 of the exponent" should mean a local sensitivity share, not a literal decomposition of the running-time exponent.

PROVED — The page-25 ledger says "Lemma S, Proposition 2 and the case k=1 ... Proved". General k=1,t>=3 remains open; change this to "the special cases of Proposition 3 and YP-Hall at k=1,t=2". Similarly, page 22's "All results here inherit ..." should say "The algorithmic running-time claims inherit ..."; Lemma 1 and the elementary combinatorial statements are not contingent on all of Base's algorithmic lemmas.

EVIDENCE — Use an approximately-equal sign for rounded derived values such as delta=0.0698 on page 15. Keep the exact threshold T separate from an ordinary-O exponent in comparisons; using Base's internal tau0 as a benchmark is clearly labelled here, but comparing final published running-time exponents is easier for readers.

## Readability and flow

EVIDENCE — **The Corollary D problem has been fixed.** Page 13 gives the reason it is needed, a usable statement including the binomial hypothesis, the application parameters, g_M, and the link to repeated trials. A reader no longer has to know the project's private shorthand to understand its role. An early forward reference in the status summary is acceptable because it is identified as a Base dependency and explained later.

EVIDENCE — **The introduction is still too repetitive.** It now lasts into page 6 and presents the results through an abstract, opening motivation, theorem, comparison table, seven-item contribution list, reading guide, methodology list and another status summary. Page 5 largely duplicates Section 11. I would retain the accessible problem/history explanation, algorithm outline, theorem, a compact comparison table and a short reading guide; move the long methods list to Section 11 and merge the page-6 status summary with the final ledger.

EVIDENCE — **The main numerical result remains delayed in the body.** The theorem on page 3 solves the biggest problem, but the parameter point is not developed until pages 13–15. An effective order would be: overview and notation; Base's construction, Corollary D and the new point; first-moment obstruction and closed-form budget analysis; conditional ternary extension and open problems; methods and appendices. The K16 result can remain a secondary section, while the 430-certificate audit fits well in an appendix. This reordering is optional for arXiv, more desirable for a venue paper.

EVIDENCE — **Reduce process narrative, preserve accountability.** Pages 12, 14 and 15 repeatedly describe separate reviewers and how many digits agree. One compact result-oriented certificate paragraph plus the Section 11 ledger would be more professional and easier to follow. Keep the explicit AI disclosure, the prior-exposure qualifications and the author's responsibility statement. Internal independent implementations are useful evidence, and the revision now correctly distinguishes them from external peer review.

EVIDENCE — **Shorten the abstract.** The historical chronology and secondary numerical achievements crowd out the central message. Lead with the certified conditional improvement, the proved first-moment budget obstruction, and the small-layer open question. Keep detailed history in the introduction. The current title is usable: its exponent is safely rounded upward and the abstract immediately states the inherited assumptions.

EVIDENCE — **Expand definitions at their real points of use.** The page-7 notation panel helps substantially, but naming a symbol there does not replace defining a source-specific expression later. The remaining filter, region-vector and amplitude-tilt issues in C3 are the next high-value fixes.

EVIDENCE — **The future-work boundary is now clear.** The paper explicitly leaves [S], general k=1,t>=3, global joint capacity and the remaining imported proof verification open; it also says the small-k results do not settle the linear k needed by the ternary theorem. Preserve that paragraph. A final short research agenda would make the ending more memorable: (1) prove or refute [S] in the needed linear range; (2) bound or exceed joint capacity; (3) reduce enumeration costs outside Proposition 1's premises; (4) complete the specifically named inherited proof checks. These are genuine next problems, not admissions that the published contribution must wait.

## The pending bridge sentence

EVIDENCE — Jennifer's proposed "Here we push this line of work further and examine what limits it" is more purposeful than "We study this line of work." I would make the object of the limitation precise:

> Here we improve this approach and examine the limits of its current analysis.

EVIDENCE — Alternatively: "Here we improve the certified parameters of this approach and investigate what limits further progress within its current analysis." If either replaces the bridge in the abstract, remove or rewrite the start of the next paragraph ("We also study what limits this line of work") to avoid immediate repetition. The bridge was already marked as pending by Jennifer and is not counted as an unaddressed defect.

## R1–R26 disposition

EVIDENCE — "Addressed in PDF" concerns the supplied text, not confirmation of an external file change. "Partial" identifies a remaining item above. The following is a comparison with the previous issue register, not a newly expanded numerical certification.

| Prior issue | Follow-up status | Rev8c location / remaining action |
|---|---|---|
| R1 counting floor | Partial | Proposition 1 repaired, p16; carry its premises into p4/17/18 summaries (C1). |
| R2 variational equivalence | Addressed in PDF | Exact all-density formulas, p21; related experimental claims still need C2. |
| R3 YP graph | Addressed in PDF | Complete sources, targets, weights and adjacency, p20; charging reduction p27. |
| R4 missing partial proofs | Substantially addressed | Q proofs and Hall construction p27–28; expand Hall details (C4). |
| R5 notation / Corollary D | Substantially addressed | Notation p7, full Corollary D p13; remaining filter/tilt notation C3. |
| R6 main theorem / proof appendix | Substantially addressed | Theorem 1 p3; Appendix A p25–27; ancillary release not checked (C6). |
| R7 rho9 multiplier | Addressed in PDF | Correct two-entry vector p13; exported metadata not checked. |
| R8 ternary a,c / trial count | Addressed in PDF | Different exact a,c p14; rounded integer count and majorant p25. |
| R9 S3 / epsilon0 | Addressed in PDF | Safe S3 display and epsilon0 lower bound p15; candidate metadata not checked. |
| R10 overlap overhead | Addressed in PDF | Slack difference and limiting equality stated p17. |
| R11 Jensen equality | Addressed in PDF | Correct equality condition and uniform-density example p10. |
| R12 exclusion scope / p=1 | Addressed in PDF | Explicit proof-budget scope, multiplier range and endpoint p10. |
| R13 all-K domain | Addressed in PDF | Integer K, mu<=1/2 and coupling caveat p9. |
| R14 implication chain / few values | Addressed in PDF | Valid arrows p18; side results and scoped tests p19–20. |
| R15 "exact" flow checks | Claim corrected; data NOT CHECKED | Floating arithmetic and tolerance stated p20. |
| R16 critical-type table | Partial | "Compare with", approximate discrepancies and run description p21; p22 still claims common corner. |
| R17 universal experiment claims | Partial | Interior and equal-entropy qualifications fixed p22; C2 remains. |
| R18 remaining dependencies | Addressed in PDF | Specific remaining lemmas p22–25; restrict "all results" per C7. |
| R19 Ye–Li modulus | Addressed in PDF | Modular hashing acknowledged p23. |
| R20 evidence labels | Partial | Useful ledger p24–25; fixed floor and k=1 labels still need C1/C7. |
| R21 review independence / exposure | Substantially addressed | Explicit internal-AI qualification and exposure ledger p23–24; shorten repeated narrative. |
| R22 frozen artifacts | Partial / NOT CHECKED externally | Repository and ancillary promised p24; pin exact release and verify contents (C6). |
| R23 story / repetition | Partial | Main theorem moved early; long introduction and process narrative remain. |
| R24 notation / numbering | Substantially addressed | Numbered results and a_Gamma, nu, g_M; remaining issues C3. |
| R25 experiment inventory | NOT CHECKED externally | PDF says scripts/inputs/outputs are listed; no release audited in this follow-up. |
| R26 epsilon0 in ternary work bounds | Addressed in PDF | EM/SP/SK explicitly subtract epsilon0, p26. Ensure ancillary agrees. |

NOT CHECKED — After-B directed-export repairs are separate from R1–R26: no new export files were supplied with this PDF. I therefore do not mark them verified.

## Review limits and recommended expert checks

PROVED — No new mathematical computation was run for this follow-up. Numerical references above come from my earlier own-code interval/exact audit, with unchanged displayed frozen parameters. PDF extraction and rendering were document operations using `review_rev8c.py`, not new mathematical experiments. The previously verified headline threshold and moments remain supported by those existing certificates.

NOT CHECKED — I did not re-run the 430 historical inequalities, the optimizer searches, large sweep counts or max-flow instances; authenticate a new public release; inspect newly revised JSON files; verify every bibliographic detail; or prove all imported algorithms from scratch. A PDF claim that a release has been repaired is distinct from checking that release. This follow-up is not blind: it uses my previous reports and mathematical work.

EVIDENCE — The most useful human expert checks are the interpretation and scope of the inherited algorithmic theorem, the finite-circle/admissibility argument for asymmetric filters, the expanded Hall reduction including its cut aggregation, and correspondence between Appendix A and the exact released Section T. None requires resolving [S] or proving the global capacity conjecture before the conditional paper can be useful.
