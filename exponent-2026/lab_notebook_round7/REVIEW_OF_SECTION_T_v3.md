# Claude's check of Section T v2 → v3 (Fable round 7) against Astra's issue register
Written 2026-11-05 ~06:55 ET. Inputs: Fable_review/Fable_round2/{SECTION_T_v3.md, CHANGELOG_T_v2_to_v3.md,
scripts/round7/}, Astra_round6/out/REFEREE_SECTION_T.md. I am not the builder (Fable) or the referee (Astra).

## Verdict: PASS. Every repair (a)–(h) is applied correctly; no number moved; one small repairable precision point.

Integrity: candidate_ternary.json sha256 ea2f10e8… (matches); SECTION_T_v2.md byte-identical to the snapshot 3 copy;
recheck_v3.txt: 40/40 checker lines identical (33 PASS), nine added scalars inside Astra's intervals, control
(τ0 − 2e-6) fails at C2R, C3, C4R, C5R, ThmA, M1, M2 as pre-registered. Elapsed-time amendment is recorded and benign.

| Astra item | v3 | Checked |
|---|---|---|
| (a) scope b ≤ n^c, word-RAM, ≥ 2/3 | Scope v3:223–232, Statement v3:260–266, header | Correct; matches Base l.58–66, 806–810; "O_c(2^{0.4873408n})", never rounded down |
| (b) integer trial count | Step 3 v3:74–83 | Correct: x := C̄_S n⁸ 2^{d} ≥ 1 ⟹ x ≤ T ≤ 2x+1 ≤ 4x; T6 uses T ≥ C_S n⁸ 2^d ⟹ e^{−n²} |
| (c) O(log n) in T bounds | v3:184, items 5, 7 | Correct |
| (d) new table rows | v3:47–53 | Rows match Astra's inventory; slacks recomputed: EM = PP = 0.01266, PD = 0.22934, SP 0.4604, SK 0.4334, CAP 9.79e-7, A4G 0.4587 |
| (e) uncapped ideal execution | Step 6 v3:91–93, T5–T7, A′ proof | Correct; cap charged in A′ by Markov + (CAP) |
| (f) B2 a_Γ ≤ 3/4 | v3:59–65 | Correct: (4a_Γ+3)ε; a_Γ = Δ/Γ = 0.06248; slack 0.6875 |
| (g) cosmetic | T7 citations; strict/non-strict; ρ_9 z = (q,0) | Correct (line pointers spot-checked: l.301–612, l.486–535, l.696–717) |
| (h) cutoffs | v3:268–281, T5 statement | Correct: n³ ≥ 16K₀ ⟹ 16K₀(m+1) ≤ 16K₀n ≤ n⁴; Step 6 constant 16K₀n²(m+1) re-derived; 128K₀ correctly attributed to Base's A5 |

## One repairable precision point (no number changes)
T7 items 1, 3, 4 need the work exponents below τ0 − ε0 + ζ, i.e. (EM), (SP), (SK) with slack ≥ ε0, but the table
states them in the weaker form (< τ0, with ζ) and ε0 (v3:55) is defined over (C1R)–(A4R) only. The script checks the
needed stronger forms (slacks 0.0127, 0.4604, 0.4334, all ≫ ε0 ≈ 1e-6), and v3:55–57 says so; Astra also said these
"must have sufficient slack too". Suggested one-line fix for v3.1 (or the repo README): state (EM) μ < τ0 − ε0,
(SP) ½ − τ0 + ζ + γμ/2 < τ0 − ε0 + ζ, (SK) r + ½ − τ0 + ζ < τ0 − ε0 + ζ in the table (or add them to ε0's list).
Not a defect at the point; only the table's wording.

## Fable's seven qualifications
All reasonable; I agree with each. (1) is fair: v2's Theorem A′ already had poly(n+b+2); only the summary was
unqualified. (2) matches my own correction in the round-7 prompt.
