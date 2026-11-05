# Revision in response to Astra's round-8 referee report — 2026-11-05 (Claude)
Master: preprint/paper.tex → Voitle_SubsetSum_certified-0.48758_2026-11-05_rev8.pdf (28 pages, 0 errors, no undefined
references; two overfull boxes under 1.1 pt). Pre-revision copy: drafts/paper_before_round8_2026-11-05.tex.
Rerunnable, anchor-checked edit scripts: drafts/revise_round8.py, then drafts/revise_round8_appendices.py.
Jennifer's decisions: hold emails until this revision is done; title keeps the number, softened ending.

| Astra | What changed |
|---|---|
| R1 floor scope | Abstract, intro, contributions, Section 9: counting floor is now Proposition 1 with an explicit premise (≥ 2^{(1−η−o(1))n} alias classes; one counted step per class; checksum at the same modulus); counterexample P, 2P, 4P… stated; "not a lower bound for Subset Sum". Floor value now from our point's Δ = 0.0287: 0.48565 → printed 0.4856 (rounded down; the old "0.4857 at capacity 0.029" did not compute). |
| R2 variational claim | Replaced by the two exact Gibbs formulas over all densities; the "equivalent to one condition on sampled types" sentence removed (also in item 4). |
| R3 YP-Hall definition | Full definitions of near misses and targets (sets, weights), the rule YP, and Conjecture 3 (YP-Hall) as a Hall inequality; reduction Q ⇔ (near-miss weight ≤ target weight) proved in Appendix B (swap bijection). |
| R4 k = 1 proofs | Proposition 3 now states only the Q inequality for (i)–(iii), equality "up to affine change and permutation", "generic" defined; proofs of (i), (ii), (iii) in Appendix B (Astra's notes, checked line by line by Claude); YP-Hall at t = 2 proof sketch with demands/capacities in Appendix B. |
| R5 notation, Corollary D | Notation panel at the start of Section 2 (h, Σ, d, a_j, alias class, τ/T, Δ, Γ, a_Γ, moments, OpenAI and Base parameters, ε, ζ, g0, guard). Section 8 restates Corollary D with its hypotheses and explains how it pays for trials (σ = m/2, v = m − 2k, g_M, Base's sampled trial count, Lemma A5's 2^{−g_M} n^{−6}). |
| R6 main theorem first | Theorem 1 (main result) in the Introduction with model, success probability, every execution, fixed c, every T′ > T; Theorems 2, 3 numbered; reading guide "How to read this paper". |
| R7 ρ9 vector | Section 8: ρ0 (p,0), ρ1–ρ8 (q,0,0), ρ9 (q,0); "exactly" → "reduce to". candidate_base.json metadata NOT edited (frozen, in snapshots); noted here as an erratum. |
| R8 a ≠ c; trial count | a = 0.0035141538, c = 0.0035141537; "explicit integer trial count of order C_S n^8 2^{d(M)}". |
| R9 S3, ε0 | S3 left side 0.12946 (true 0.1294547, rounded up since it must be small); ε0 ≥ 1.3156e-6; C4 margin 1.3156e-6. |
| R10 C4 vs overlap | "equals/exactly" replaced by the decomposition: differ by μ(h(2a)/2 − γ) ≈ 6.3e-7. |
| R11 Lemma 1 equality | Equality condition stated correctly (ratio constant under K_x; e.g. κ = 1 or f = g = 1); κ = 1.1 gap restricted to the tested family; g(p) renamed Ψ(p). |
| R12 0.48 scope | "sufficient conditions of the OpenAI proof cannot be met at any τ ≤ 0.484", p ∈ [1,10], p = 1 handled (1 + Ψ(1) ≈ 0.697); "not a lower bound for every algorithm". |
| R13 K domain | Section 4: integer K ≥ 1, Kμ < 1, μ ≤ 1/2. |
| R14 chain, 0.72 | Chain YP-Hall ⇒ Q ⇒ M′ ⇒ [S] displayed; table reordered with partial results; "fails at the middle step … held in our tests"; 0.72 claim restricted to the m = 18, 20 hill-climbs, (0,0,1,1) counterexample to the general claim stated. |
| R15 "exact" flows | "Max-flow computations in floating point (routed fraction ≥ 1 − 10^{−9})"; table says "floating-point flow computations". |
| R16 critical-type table | "Equals" → "Compare with", with values; "agree to within 4e-4; not certified"; "all budgets bind at one type" removed. |
| R17 overclaims | Domination experiments: "in our experiments … did not help"; interior-optimum qualification (boundary p = 1, 10 not covered); indicator densities v = KL(f) + KL(g) − 2u, equal-entropy assumption stated. |
| R18 stale dependency list | Item 5 names the remaining OpenAI and Base dependencies; Base core re-derived; Lean described as a further project. |
| R19 Ye–Li | "hashes representations modulo a random prime but has no alias-enumeration phase and no Fourier checksum". |
| R20 labels | Status split into: certified numerics in conditional theorems / proved / conditional on an open statement / floating; ledger rows split accordingly (counting floor "Proved", its value "Floating"). |
| R21 "referees" | Defined as separate AI agents in fresh contexts, internal cross-checks, exposure noted; all "referee" wording → "reviewer/review" (0 left). |
| R22 artifacts | Methods: release fixed by SHA-256 manifests + OpenTimestamps (TIMESTAMP.md); Section T proofs as ancillary file; Astra bib entry "included in the repository". TODO before posting: put E2_LANDSCAPE.md and target_048 reports and an experiment inventory in the public repo; add SECTION_T_v3 as arXiv ancillary file. |
| R23 length/order | Abstract shortened and reorganized; reading guide added. NOT done: moving Sections 3–7 to appendices (would renumber every hard-coded cross-reference); the reading guide serves the same purpose. |
| R24 notation collisions | a_Γ for Δ/Γ, ν for the k-sum law, g0 for the OpenAI guard margin, g_M in Corollary D, Ψ(p) in Lemma 1; theorems/propositions/conjectures numbered. Left: v (score) vs v (Corollary D residual size), each defined where used. |
| R25 provenance | Methods: floating results are evidence; repository to list script/inputs/output of each (inventory TODO, see R22). |
| R26 ε0 / SP, SK | Appendix A states (EM), (SP), (SK) with the ε0 margin that Lemma T7 uses. SECTION_T_v3.md itself still has the weaker wording (v3.1 for Fable, or keep the appendix as authoritative). |
| After-B: exports | New file C3_target_048_Claude/cert_exports_directed_2026-11-05.json (script export_directed_2026-11-05.py): outward-rounded margins, moment enclosures, recomputed outer quadrature errors (~1e-1419, 1e-1416), note on the vs_Base field. Originals unchanged. |
| After-B: audit | New semantic audit (audit/semantic_audit.py): 26 claims checked against the quantity they describe with the required rounding direction; 26/26 OK. |
| Related work | Added Austrin–Kaski–Koivisto–Nederlof (STACS 2016) and Nederlof–Węgrzycki (STOC 2021) to the history. |
