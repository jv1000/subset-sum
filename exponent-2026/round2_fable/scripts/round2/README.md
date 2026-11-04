# Round-2 scripts

Run from `Fable_round2/` with `python -I scripts/round2/<name>.py`. Requirements: Python 3.12, numpy, python-flint 0.9
(for the certificate, which imports `../../scripts/moments_arb.py` from round 1). Each run is one process and takes at
most a few minutes; the exhaustive sweeps are capped. Pre-registrations and outcomes: `PREREG_A1.md`.

| Script | Purpose | Output |
| --- | --- | --- |
| `layers.py` | exact layer sizes s_j and core counts n_e^{(j)} via value classes (DP over compositions) | library |
| `lemmaE_test.py` | A1: removal identity, core inequality, Lemma E, rules for e (families, m ≤ 14) | `out/lemmaE_test.txt` |
| `dm_evidence.py` | A2: defect monotonicity on families + hill-climb (m ≤ 16) | `out/dm_evidence.txt` |
| `group_probe.py` | A3: monotonicity/DM over finite abelian groups | `out/group_probe.txt` |
| `hall_probe.py` | A4: brute-force Hall's condition on the fiber graphs | `out/hall_probe.txt` |
| `dm_exhaustive.py` | A5: exhaustive DM/monotonicity over value multisets ([−3,3] m ≤ 12; Z_q; [−6,6] m ≤ 9) | `out/dm_exhaustive.txt` |
| `dm_violations.py` | A6: lists the violations, verifies each by brute force, tests averaged/existence forms | `out/dm_violations.txt` |
| `mono_ratio_sweep.py` | A7: exhaustive [−6,6] at m = 10, 11; ratios, max a_t/a_k, [S] quantity | `out/mono_ratio_sweep.txt` |
| `mono_wide.py` | A8: exhaustive [−8,8] at m = 8, 9; structured cluster+large m = 10..16 | `out/mono_wide.txt` |
| `mono_m10_m12.py` | A9: exhaustive m = 10 in [−8,8], m = 12 in [−6,6] | `out/mono_m10_m12.txt` |
| `c_hunt.py` | C: structured families m = 16..22 (numpy) | `out/c_hunt.txt` |
| `freeze_ternary.py` | B1: freeze the C19 optimum to `../../candidate_ternary.json` | prints T |
| `check_ternary_point.py [N ...]` | B2: certificate (33 conditions + both moments in arb) | `out/ternary_certificate_N4096_8192.txt` |

Smallest counterexample to exact monotonicity (brute-force check in one line):
`python -I -c "import itertools;w=[-6,-5,-5,-3,-3,-2,4,5];s=[len({sum(w[i] for i in A) for A in itertools.combinations(range(8),k)}) for k in range(9)];print(s, 5*s[3], 4*s[4])"`
gives `[1, 6, 14, 19, 24, 19, 14, 6, 1] 95 96`.
