# Response to referee 4 (Claude Fable 5.1, independent folder review), 2026-11-03 ~21:05 ET
Canary check: the report cites only the files in its folder. It shows no knowledge of C18, the gadget search,
pre-registration labels or our scripts.

Each point was verified by Claude (scratch check, 21:00 ET) before the paper was changed:

| # | Referee point | Our check | Paper change (rev 66–67) |
|---|---|---|---|
| 1 | Headline 0.4875754 is 3.6e-9 BELOW the proved T = 0.4875754036 | Confirmed: T − 0.4875754 = 3.60e-9. Our error: rounding down a bound. | Every headline now 0.4875754036 / O(2^{0.4875755n}) / "every T′ > T" |
| 2 | Cutoff orders: ~1e17 (Base point, ζ = 1e-8), ~1e18 (K16, d0 − d1 = 1e-9) | Agreed (Chebyshev 4/(ζ²n); 1/((d0−d1)²n)) | Stated in Sections 7 and 8 |
| 3 | Section 9 bounds were quoted at the floating optimum, not the frozen point | Confirmed: frozen (i)/(ii)/(iii) = .4875738879/.4875745458/.4875745457 vs τ0 .4875752036 | Both stated; "(ii), (iii) bind; (i) 6.6e-7 lower"; "three-way balance" softened |
| 4 | Floor quoted at Δ = .0284; certified point Δ = .0287 gives .48565 | Confirmed (.485652) | Floor quoted as ≈ 0.4857 at the certified Δ; the table's re-optimized Δ drift explained; referee's fixed-filter numbers added |
| 5 | Colour-coding formula missing the ρ-independent −2a²/ln 2 | Confirmed: full .008091 vs left part .008287. Our error. | Formula completed; conclusion (ρ = 1 best) unchanged |
| 6 | 0.48 blocked for ALL parameters in the OpenAI construction (upgrade) | Confirmed algebra: coefficient 2.6494; Δ ≥ .0530 at τ = .48 vs Dmax ≤ .0403 | Section 5 and the status table upgraded (credited to the referee) |
| 7 | "sparse-distinction forces Δ ≈ 0.17" not reproducible | Accepted | Sentence withdrawn, noted in text |
| 8 | List Base constants that change; mark 3p ≤ 30, q(4a+3) ≤ 30 as OpenAI-only | Agreed | Listed in Section 8 caveats |
| 9 | Section 2 table: cap > 1/2 − d1 strict | Agreed | Fixed |
| 10 | 34 vs 33 conditions | Our certifier includes an implied check (C5L) | "33 conditions (34 checks)" |

Not checked by the referee: Section 3, the floating Sections 6 and 10, and the non-numerical parts of Base and OpenAI.
The referee's scripts are in D:\AIProjects\Fable_review\scripts (Jennifer's laptop).
