# Round-6 scripts

Round 6 is a written re-derivation (`../../BASE_CORE_REDERIVATION.md`) of three parts of `../../../base_PROOF_0.4877.tex`
(Lemma A5; Lemmas 3.1–3.3 and Corollary D; the region analysis of Theorem B). The only computation is
`core_checks.py` (numpy only, `python -I`, 10 s), pre-registered in `PREREG_R6.md`; output in `out/core_checks.txt`.

| Part | What it checks |
| --- | --- |
| A | Lemmas 3.1, 3.2, 3.3 and Corollary D by exhaustive enumeration (exact rationals) on random small weight multisets; (F2); a control that must fail |
| B | one trial of Theorem A's procedure (Base §5.2 (c)–(g)) implemented literally on tiny instances, against the characterisation "the class key of alias I is inserted iff \|S\| = σ and some k-subset X of S has b(κ(I∩L)) + b^F(X) ≡ j′ (mod P′)"; soundness; a control without the skipped interval |
| C | Lemma B2 (domination) on random patterns and on the explicit tight instance whose margin is z₀ε(3 − 4a_Γ) |
| D | OpenAI's two filtering moments with its own filter (float trapezoid) |
