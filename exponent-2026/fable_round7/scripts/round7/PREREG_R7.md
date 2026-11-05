# Round-7 pre-registration (Section T v2 → v3: apply Astra's repairs; no number changes)

Discipline as in rounds 2–6. Round 7 is a text revision. The only computation is the re-check that the frozen
ternary point is unchanged and that no condition's numbers moved, pre-registered here before it is run.

## R7-C1 `recheck_v3.py` — the frozen point is unchanged and every condition's slack is unchanged
1. sha256 of `../../candidate_ternary.json`. Prediction: `ea2f10e89ea5f0073479e1e41cc5e22ffda31a5655966ee3f458e8cff25c422b`
   (the value given in the round-7 request).
2. Re-run `../round2/check_ternary_point.py 4096 8192` (arb, 200 bits) as a subprocess and compare every PASS line and
   every slack string with the recorded `../round2/out/ternary_certificate_N4096_8192.txt`. Prediction: all 33
   conditions PASS with byte-identical slack strings; log₂ M1 = 0.51599187405865778648, log₂ M2 = 0.51599162047014794189.
3. Recompute in arb the scalar slacks of Astra's inventory that are NOT in the round-2 table, under Astra's names and
   formulas (`verify_a.py` lines 55–74): preliminary = ½ − τ0; exact-M-merge = τ0 − μ; small-prime-total =
   2τ0 − ½ − ζ − γμ/2; right-key-sort-total = 2τ0 − ½ − ζ − r; large-prime-draw = τ0 + 20ε − η/2; cap-margin =
   ε0 − 1/guard − ζ; A4R-after-guard = η − μ(h(2a′)+2a′) − 1/guard; small-prime-vs-eps0 and right-sort-vs-eps0.
   Prediction: each arb ball lies inside Astra's 35-digit interval from `SCALAR_SLACKS.md` (copied into the script),
   and all are positive. No condition's numbers move: v3 changes only text.
4. Control (must FAIL): a perturbed copy of the JSON in the system temp folder with τ0 lowered by 2·10⁻⁶ (all else
   equal), run through the same checker. Prediction: C2R, C3 and C4R FAIL (their slacks are 1.30·10⁻⁶ < 2·10⁻⁶), the
   output ends in "SOME CONDITION FAILS", and the sha256 differs. (C5R has slack 1.60·10⁻⁶ against 2τ0, so it also
   fails; C1R does not depend on τ0 and passes.)
Runtime: about 10 s per checker run, one process, memory well under 200 MB.

## Outcomes — recheck_v3.py, out/recheck_v3.txt (two checker runs + control, 25 s total)
First run: predictions 1, 3, 4 met; prediction 2 flagged one differing line, which was the elapsed-time suffix
"(1s)" vs "(0s)" on the N=4096 line, not a number. Amendment (recorded before the second run): the comparison
strips the "(Ns)" suffix. Second run: 1. sha256 MATCH; 2. all 40 recorded condition/moment lines IDENTICAL
(33 PASS, 0 FAIL, "ALL CONDITIONS PASS"; log2 M1 = 0.51599187405865778648, log2 M2 = 0.51599162047014794189 at
N = 4096 and 8192); 3. all nine Astra-named scalars inside Astra's 35-digit intervals and positive (cap-margin
9.7944610694e-7, small-prime-total 0.46035201, right-key-sort-total 0.43336319, A4R-after-guard 0.45871420,
exact-M-merge 0.01266105, preliminary 0.01265945, large-prime-draw 0.22934205); 4. control tau0 - 2e-6: sha256
differs, FAIL at C2R, C3, C4R, C5R and also ThmA (eps0 < 0), M1, M2 (Delta = eta - tau0 grows by 2e-6, so log2 M1
rises by about p*2e-6 = 1.7e-5 > its 3.0e-6 slack), "SOME CONDITION FAILS". All predictions met. EVIDENCE that
no number moved between v2 and v3 (the point and the checker are unchanged; v3 is text only).
