# Round-7 scripts

Round 7 applies Astra's repairs to Section T (`../../SECTION_T_v2.md` -> `../../SECTION_T_v3.md`, changes listed in
`../../CHANGELOG_T_v2_to_v3.md`). No number changes. The only computation is `recheck_v3.py` (arb via python-flint,
`python -I`, 25 s), pre-registered in `PREREG_R7.md`; outputs in `out/`:

| File | Content |
| --- | --- |
| `out/recheck_v3.txt` | sha256 of `candidate_ternary.json`; diff of the re-run certificate against the round-2 record; Astra's nine extra scalar checks in arb; the failing control |
| `out/checker_rerun_N4096_8192.txt` | full output of `../round2/check_ternary_point.py 4096 8192` re-run |
| `out/checker_control_tau0_minus_2e-6.txt` | the same checker on the perturbed control point (must fail) |
