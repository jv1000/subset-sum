# Round 8 exposure and computation register

EVIDENCE — Instructions read first from PROMPT_for_Astra_round8.md. B remains unopened. Only A and the explicitly permitted own round-6 work may inform the initial report. The PDF skill was read for inspection workflow; it contributes no mathematical conclusions. All generated files will remain in this out directory.

EVIDENCE — Prior exposure: in round 6 I reviewed Section T v2 and Base probabilistic core, reconstructed the small-layer and region arguments, independently computed the ternary point, and proved YP-Hall for k=1,t=2. I also read the round-3/4/5 definitions and reports after the round-6 A gate. The initial round-6 statement locator exposed proof fragments, especially Corollary D; the round-6 blind exercise was qualified. I remember those conclusions and cannot offer independence from them. For round 8 I will check the current text rather than import their correctness. No round-8 B content has been seen.

## R8-NUM — pre-registration
EVIDENCE — Expected result: exact rational recomputation should reproduce candidate exponents; rounded gaps may expose small discrepancies. Control: compute T independently from its components and check every claimed rounded-up exponent is at least the exact threshold, while improvement gaps rounded down never exceed the exact difference. Parse decimals exactly. All non-candidate experimental numbers will be explicitly marked NOT CHECKED unless independently recomputed or supported by an inspected artifact.

## R8-MOM — pre-registration
EVIDENCE — Expected result: the base one-filter candidate should satisfy both moments and its numerical conditions. Reuse only my own round-6 interval evaluator, adapted to a candidate path and fresh output location. Controls: asymmetric exact FFT correlation, entropy at one half, zero-filter scores, positive denominators, and full analytic quadrature error bounds. Start N=4096 at 50 interval decimal digits; double only if needed for a meaningful diagnostic or bound. One numerical process, modest arrays, abort rather than exceed 30 minutes.

## R8-BLOCK — pre-registration
EVIDENCE — Expected result: the claimed exclusion of tau≤0.484 survives when Lemma 1 is combined with list/pair inequalities and p in [1,10]. Control: handle p=1 separately; use monotonicity in tau and directed interval bounds on p cells, not an optimization sample. Also test the p-range dependence and distinguish feasibility of the stated sufficient budget from an algorithmic lower bound. Any uncovered parameter range is NOT CHECKED.

## R8-DOC — pre-registration
EVIDENCE — PDF extraction/rendering and source inventories are navigation/layout checks, not numerical theorem certificates. Inspect the rendered paper, cross-check definitions before first use, citation coverage, theorem quantifiers, status ledger and output consistency. Preserve any failed computation and its reason. No files outside out will be modified.

## R8-NUM / R8-MOM — outcomes
PROVED — audit_numbers.py passed all its scalar inequalities for the three frozen candidates. Exact thresholds are 0.4875754036, 0.4894615727, 0.4873407528. The stored floating_T and floating_margins fields in candidate_base.json are stale relative to its exact decimal strings; they were not used. Exact gaps are in numbers.json.

PROVED — verify_moments.py --candidate base --n 4096 passed at 50 interval decimal digits, with analytic inner and outer quadrature bounds. log2 M1 is enclosed in [0.51626832585128515043776256214358221, 0.51626832585128515043776256214440031]; log2 M2 in [0.51626814726466968639116654011059812, 0.51626814726466968639116654653486855]. Both are strictly below rho_c = 0.5162696413. Controls passed. EVIDENCE — elapsed mathematical run about 7.5 seconds; one process. No doubling needed.

## R8-BLOCK / R8-DOC — outcomes
PROVED — verify_blocking.py establishes the exclusion for the stated continuous-circle budget at every tau <= 0.484 and every p in [1,10]. The minimum directed cell lower bound is >0.00461138 on 9,000 cells; p=1 is handled separately. EVIDENCE — run about 1.6 seconds. This is an infeasibility certificate for the sufficient proof budget, not a lower bound on all algorithms.

EVIDENCE — All 22 supplied PDF pages were extracted and visually inspected in six contact sheets. The layout is generally clean; the long abstract, dense unnumbered propositions, small status tables, and excessive process narration weaken usability. Mathematical source line references will be used for exact fixes. No missing glyphs or conspicuous clipped text were seen at contact-sheet resolution; fine typographic perfection is not certified.

## R8-COMB — pre-registration
EVIDENCE — Prediction: the published m=8 monotonicity counterexample and excluded m=6,k=2,t=3 example reproduce exactly; k=1,t=2 and the two stated special families pass small exact tests. Control: generic powers-of-two weights give Q=1; compute the witness distribution with exact Fraction arithmetic, including all index-distinct subsets. Test (0,0,1,1),t=2 against the sentence claiming every few-valued case is below 0.72. No inference from small tests to the general conjecture. One sequential process, bounded enumeration m<=9; retain all outputs.

## R8-SOURCE — pre-registration
EVIDENCE — Extract the supplied source PDF opening statements and relevant theorem passages; verify historical exponents with exact fractions. This is a document/source audit, not a recertification of those algorithms. Joshua's pinned README/statement may be read; no outside optimizer or referee code will be used.

PROVED — R8-COMB reproduced 19/56 < 24/70 and Q=29/28 for the excluded (m,k,t)=(6,2,3) case. Exact k=1,t=2 tests passed on 1,946 multisets; 52 special-family cases passed. These are only finite controls. The few-valued example (0,0,1,1),t=2 gives Q=1, so the unqualified prose bound <0.72 is false.

EVIDENCE — R8-SOURCE first extraction stopped on Windows console cp1252 encoding (Unicode minus), after writing the first source text. No mathematical failure. Fixed console output to UTF-8 before retrying; this failed route is retained here.

## R8-MOM extension — pre-registration
EVIDENCE — The base run finished in seconds with ample error margin. To check the paper's printed moment values for the other frozen inputs, run the identical own-code certificate sequentially on K16 and ternary at N=4096, 50 interval decimal digits. Prediction: both pass; compare against the exact frozen strings, not stale floating metadata. Controls and analytic error bounds unchanged. No optimization, no parameter changes, no parallel execution.

EVIDENCE — R8-SOURCE extraction succeeded after the console fix. OpenAI's supplied theorem states the polynomial-bit randomized word-RAM scope and intermediate exponent 0.489995; Ye–Li's supplied Theorem 4.1 states the exact exponent 1/2-1/450000, and its algorithm explicitly uses modular filtering. CJRS's abstract confirms the polynomial-factor improvement and average-case references. NOT CHECKED — both permitted attempts to retrieve Joshua's pinned README failed (web cache miss); its exact historical claim remains attributed to the package rather than independently source-verified.

## R8-MOM extension and final A outcomes
PROVED — Both additional moment runs passed with the same controls and analytic error bounds. K16 log2 moments are enclosed around 0.518477576189688678728610148076 and 0.518477347231941441440656955406; ternary around 0.515991874058657786476412457204 and 0.515991620470147941891150956423. Full outward endpoints are in moments_K16_4096.json and moments_ternary_4096.json. These interior summary decimals are not upper bounds. EVIDENCE — each run took about 7.5–7.8 seconds, sequentially.

PROVED — The scalar audit was extended, within R8-NUM, to include Base's small-prime total, right-key-sort total, bad-set threshold, and coefficient triangle bounds. All added inequalities pass. The coefficient amplitude sums certify the convenient uniform bound 3.21 for both Base polynomials; the paper's smaller 3.20 is not being independently certified by that particular triangle bound. All mathematical calculations used own scripts.

EVIDENCE — A long document-write tool call had a JavaScript quoting/syntax error before execution; no file was changed by that call. Retried successfully with a literal patch. This was a document operation, not a failed mathematical test.

## A-to-B gate
EVIDENCE — REFEREE_PAPER.md, NUMERICAL_METHOD.md, MATHEMATICAL_NOTES.md and EDITORIAL_REPLACEMENTS.md are now written. Initial verdict: major revision; no fatal defect found in the headline frozen point. The pre-B report is being copied and hashed before any access to B. The final summary will be written only after the B comparison.

## B opened after the saved-report gate
EVIDENCE — Read the nine files in B only after the initial report and pre-B hash were saved. B confirms the candidate values and the remaining Section T precision repair. It does not supply the original 35,700 flow witnesses or the floating critical-type source run.

## R8-BEXPORT — pre-registration
EVIDENCE — Prediction: the B certificates' ball strings overlap my independent intervals, but some JSON scalar fields named lower/upper may be ordinary nearest-rounded displays. Control: parse JSON numbers as exact decimal strings/rationals, compare to the full outward intervals from my own code, and distinguish harmless display agreement from a valid directed bound. Include an exact gap recomputation. This is read-only comparison, not a rerun of others' code.

## R8-BEXPORT — outcome
PROVED — The four B moment ball strings overlap the own-code intervals. Two claimed directed scalar exports are invalid: Base C8 lower is above the rigorous upper endpoint; K16 M2 upper is below the rigorous lower endpoint. Exact comparisons are in B_export_comparison.json. The Base gap field compares tau0 rather than final T (difference 20 epsilon). These are export/label repairs, not failed candidate inequalities. No other reviewers' code was run.

EVIDENCE — After-B comparison appended to REFEREE_PAPER.md, preserving the pre-B report. Verdict remains major revision. The original 35,700 flow witnesses, original critical-type experiment and full 430-certificate raw outputs are absent from B, so those reruns remain NOT CHECKED. B's existing proof reports were read and assessed as documentary evidence, with their attribution retained.

## Final review checks
EVIDENCE — The preserved pre-B report still has SHA256 31A25263F863C971EFA1EFE527B50A8103BCAB73785B90400D854727B331A15D. The current report appends the B comparison without changing that initial record. Required reports and all own scripts/results are present under out; source files were not edited. No numerical process was run in parallel, and all actual numerical runs were far below 30 minutes. No long-running shared job was inspected or modified. The one-page ROUND8_ASTRA_SUMMARY.md is the final document to be written.

## Rev8c follow-up — scope and pre-registration
EVIDENCE — Jennifer supplied the specific rev8c PDF in the preprint directory and requested review against the round-8 comments. This supersedes the pending request to implement revisions. No manuscript authoring occurred before the change of scope. Read only the supplied revision, existing review outputs, and already authorized sources as needed; write review outputs under out.

EVIDENCE — Prediction: rev8c resolves most local corrections but may retain publication/dependency or exposition gaps. Control: assess each R1–R26 against actual PDF text and page images, distinguish fixed/partial/not checked, and do not assume that an author response establishes correctness. Extraction/rendering are document operations; any new mathematical computation will receive a separate pre-registration. No optimizer or historical certificate reruns are planned.

EVIDENCE — The first attempt to save this pre-registration was denied because the turn-scoped folder grant had ended after the new user message. No file was changed. A fresh narrowly scoped grant was obtained, and the operation was retried.

## Rev8c follow-up — outcome

EVIDENCE — Read the entire 29-page supplied rev8c PDF via own extraction script and inspected rendered contact sheets of every page. Compared the actual text with every prior R1–R26 item. Saved `REV8C_REVIEW.md`, with page-specific remaining corrections, a disposition matrix, readability recommendations and the pending bridge wording. No manuscript changes were made. The result is substantially improved and close to an arXiv-ready conditional paper after focused corrections; no new fatal defect in the headline result was identified.

PROVED — No new mathematical computation was run. Numerical values cited in the follow-up come from the previously preregistered own-code exact/interval audit. Extraction/rendering were document operations. Checks used the PDF text and visuals, not an assumption that the author's revision claims establish correctness.

NOT CHECKED — A new external repository release, updated machine-readable certificate exports and the currently promised Section T ancillary were not supplied or authenticated in this follow-up. The review explicitly preserves that distinction. Historical 430-certificate runs, optimizations and exhaustive flow/sweep counts were not rerun.

## Rev8d implementation — pre-registration

EVIDENCE — Jennifer authorized implementing the rev8c follow-up edits. Starting source: preprint/paper.tex, timestamp matching rev8c. Work and deliverables remain in out/rev8d; preserve the original. Prediction: textual repairs and expanded Hall proof do not change frozen parameters or theorem thresholds. Controls: compare exact parameter strings, preserve all theorem conclusions, verify reference resolution and LaTeX diagnostics, inspect rendered pages, and map each follow-up item to a change or a documented pending input. Compile one process at a time with modest memory; no mathematical search or moment rerun is planned. Reuse previously certified own-code bounds with their provenance; freeze local copies and hashes, without claiming an external release was authenticated. Removed unsupported table/provenance details stay in the source snapshot and change record. No outside research folders will be used.

## Rev8d implementation — outcome

PROVED — The final document checks pass: exactly three formal theorem statements are verbatim unchanged, frozen candidate scalar/coefficient inputs are unchanged, internal reference labels resolve without duplicates, and LaTeX environments balance. The preserved source now matches the original input byte for byte (SHA-256 743e38dae1a516cb5e3ec39d658a422ef0f7f7db377a76de3ca2e63f2a2b0d31). An earlier snapshot had only LF-to-CRLF normalization; text equality was verified before restoring the exact bytes. No original manuscript was edited.

EVIDENCE — Implemented the follow-up review in a 28-page revision, with an expanded Hall proof, clearer scope/definitions, shorter introductory material, explicit research priorities, and a local verification snapshot. Every final page was inspected in rendered contact sheets. The final TeX log has no undefined-reference, missing-character, underfull-box or overfull-box warnings. Tectonic prints a Fontconfig configuration notice but renders successfully with bundled fonts. Numerical results are the earlier registered own-code results, not new mathematical runs.

EVIDENCE — Retained failed routes: the built-in compiler required unfinished Windows sandbox setup; WSL returned E_ACCESSDENIED; standard Windows TeX installations were unavailable. A portable official Tectonic 0.17.0 build, obtained with network permission, compiled successfully with its cache confined to this output directory. Earlier edit/check assertions required adjustment before passing; they did not change mathematical inputs. A final QA rerun was initially denied after a continuation expired the turn-scoped write grant; after the narrow grant was restored, it passed. Documentation corrected an inaccurate description of error-string formatting: errors use outward interval strings with positive upper endpoints, not necessarily scientific notation.

NOT CHECKED — No historical optimization, full flow sweep, 430-certificate rerun, or external release authentication was performed. The pending-items file identifies the release/provenance inputs and the optional evidence needed to restore removed assertions. These limits are carried into the manuscript and artifact guide.

## Rev8d packaging — pre-registration

EVIDENCE — Prediction: the selected source/PDF/verification files form a self-contained local snapshot with matching hashes. Control: generate SHA-256 manifests, test ZIP integrity, and compare every archived file's bytes to its local source. Exclude compiler/cache files and the local-only QA script; include its document-check report. This is a document-integrity operation, not a numerical experiment.

## Rev8d packaging — outcome

PROVED — The 30-file source/PDF/verification archive passed ZIP integrity and byte-for-byte SHA-256 comparison for every entry. The final PDF is 234,587 bytes. This outcome is added to the register snapshot by one final package refresh with the same integrity controls; the release manifest records the delivered file hashes.
