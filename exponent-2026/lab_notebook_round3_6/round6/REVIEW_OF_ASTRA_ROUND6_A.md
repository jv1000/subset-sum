# Claude's review of Astra round 6, Part A (A1 referee, A2 base core), and comparison with Fable round 6
Written 2026-11-04 ~22:10 ET. Inputs: Astra_round6/out/{REGISTER, REFEREE_SECTION_T, SCALAR_SLACKS, A_certificate_4096/8192,
BLIND_BASE_CORE, BASE_CORE_ASTRA, BASE_CORE_COMPARISON, BASE_CORE_CONSTANTS}.md/json; Fable_review/Fable_round2/
BASE_CORE_REDERIVATION.md (identical to the local copy). Astra's Part B and summary were not yet written; this review
does not cover them. Neither Astra nor Fable has seen this file.

## A1 — fresh referee of Section T v2 + candidate_ternary.json: PASS WITH REPAIRS (accepted)
- Verdict as written by Astra: every T' > 0.4873407528, conditional on [S] and inherited Base/OpenAI results, in the
  word-RAM model, for inputs with b ≤ n^c. No fatal defect; no numerical change.
- Independent own constraint list (26 rows with Base/T line citations), own interval FFT certifier with an ANALYTIC
  trapezoid error bound (strip s = 0.04 outer, 0.1 inner), not a grid-stability argument. This is stronger than our
  certificates' convergence evidence and is worth one sentence in the paper's methods.
- Cross-check against ours (Claude round 3 + paper Section 8):
  - log2 M1: Astra [0.515991874058657786476412457204096, …] vs ours 0.51599187405865778648 (20 digits): AGREE.
  - log2 M2: Astra 0.515991620470147941891150956 vs ours 0.51599162047014794189: AGREE.
  - Scalars: C1R 9.99446e-7, C2R 1.30035e-6, C3 1.30006e-6, C4R 1.30035e-6, C5R 1.6001e-6, MU1 .009323, MU2 .025320,
    A4R .458714, SR .102972 — all agree with REVIEW_OF_ROUND3.md. Tightest margin B3-p = 8.119e-7 = paper's 8.1e-7.
  - Astra adds checks we did not list: small-prime-total, right-key-sort-total, cap-margin, A4R-after-guard (all pass
    with ample slack). Its point "these were missing explicit checks, not obstructions" is correct.
- Repairs requested (all to Section T's text, none to numbers): add b ≤ n^c / word-RAM scope; integer polynomial
  majorant for C_S and outer ceiling in the trial count; restore C_S n^8 factor in T:134/141 as +O(log n); add the
  small-prime and right-key-sort checks to the table; "uncapped ideal execution" wording in T5/T6; A ≤ 3/4 in B2;
  several cosmetic line pointers. I checked the b ≤ n^c point against the sources: Base Thm 1 (l.58-66, 806-810) and
  OpenAI main.tex l.47 ("on polynomial-bit inputs in a word-RAM model") both have it. CONFIRMED.
- **Consequence for the PAPER (not only Section T):** paper.tex never says "randomized" and states no model or
  bit-length scope in either theorem (Section 7 l.276, Section 8 l.362), in the certified-result paragraph of Section 8,
  or in the abstract. Needs the qualifier everywhere a time bound is claimed. Draft wording in
  preprint/drafts/SECTION10_UPDATE_DRAFT.md, Edit 5.
- Referee requirement for the conditional result: MET (fresh referee, PASS with expository repairs). It remains
  conditional on [S].

## A2 — Base core: Astra vs Fable (blind to each other), compared
| Item | Fable round 6 | Astra round 6 | Agreement |
|---|---|---|---|
| Lemmas 3.1–3.3 | PROVED, same injections; 2 cosmetic | PROVED, same injection/incidence count | AGREE |
| Corollary D | PROVED; hypothesis C(σ,k)C(v,k) ≤ 2^v used only at t < k | PROVED; same observation ("precisely the use … not dispensable") | AGREE, but NOT blind on the t < k branch: BOTH saw Base l.260-267 first |
| Fixed signing before S | cosmetic note (2.3) | noted (271-275) | AGREE |
| Lemma A5 | PROVED, same constants; δ condition 1/2−τ0+ζ < δ not in (C1)-(C8) | PROVED, explicit constant 32K0 n²(m+1)(v+1) → n^-6 for n² ≥ 128K0; two δ requirements separated | AGREE; Astra's A5 bad-set substep partly exposed (l.473-482) |
| A5 "uncapped ideal execution" | not flagged | repairable wording | Astra adds; I agree (cap failure is charged separately in A′) |
| Lemma B2 row error | REPAIRABLE: "6ε per row" false in general (7ε); needs a_Γ ≤ 3/4 | REPAIRABLE: Aw−u row costs (4A+3)ε; needs A ≤ 3/4 | **AGREE, found independently** — the strongest concordance in the exercise |
| B3 decay | Base 0.00017 (ours 8.1e-7 at our point) | actual 1.7472e-4 ≥ claimed 0.00017 at Base's point | AGREE |
| δ at Base's point | > 0.0706 correct | [0.0706432, …] | AGREE (ours 0.0698 at our point, Fable) |
| J = 1 reduction | "implied by M1, M2" wording | last region z = (q,0), not (q,0,0) | compatible cosmetic notes |
| Prop B ρ0 margin 3.8e-6 at Base's point | cosmetic (non-effective n threshold) | not mentioned | Fable only; affects Base's point, not ours |
- **Verdict:** two independent reconstructions, no fatal gap, one shared repairable item (B2) that our certified point
  satisfies (A = a_Γ = Δ/Γ ≈ 0.0625 at both points; B2 row margin 0.6875 at the ternary point per SCALAR_SLACKS).
- **Scope caveat that must travel with any claim:** neither reconstruction of Corollary D's t < k branch was blind,
  and Astra's A5 bad-set step was partly exposed. Base's Corollary D is a premise of the CERTIFIED 0.4875754 result
  (not of the conditional one, where [S] + R replaces it). If the paper mentions these re-derivations it must say so.

## Not covered here
Astra Part B (YP-Hall k = 1) and ROUND6_ASTRA_SUMMARY.md: pending at time of writing.

## Addendum 22:20 ET — blind Corollary D check done (round6/blind_corD/)
A fresh agent given only Base's statements (no proof text) proved Lemmas 3.1-3.3 and Corollary D, including the t < k
branch, with the product hypothesis used exactly where Base uses it. Compared with Base l.259-273 afterwards: identical.
The exposure caveat above is therefore RESOLVED for Corollary D: there is now one fully blind re-derivation plus two
partly exposed ones, all agreeing. (A5's bad-set substep remains re-derived only with partial exposure by Astra, and
by Fable without that exposure.)
