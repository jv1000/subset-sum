# Round-5 scripts

Run from `Fable_round2/` with `python -I scripts/round5/<name>.py`. Python 3.12 + numpy only (max-flow: the Dinic of
`../round3/lay3.py`; near-miss / target enumeration: `Inst` of `../round4/charge_flow.py`; fast Q_w: `../round4/lay4.py`).
One process at a time; the longest run is 19 minutes; nothing is enumerated above m = 20. Every flow run has a memory
guard (edge cap 3·10⁶ per case, abort above a 1500 MB working set). Pre-registrations and outcomes (including the
predictions that failed): `PREREG_R5.md`. Outputs in `out/` (`.txt` = results, `.log` = full stdout).
Report: `../../ROUND5_REPORT.md`.

| Script | Purpose | Output |
| --- | --- | --- |
| `flow5.py` | library: collapsed (sparse) YP / YPQx / YPQ flow — sources merged by P (YP), (P,Q) (YPQ) or (P,Q,X) (YPQx), targets merged by Y; memory guard; named Hall violator from the residual graph | library |
| `charge_flow5.py` | A1: validation of the collapsed flow against the dense flow (302 cases), controls, the 137 dense m = 8, 9 cases skipped in round 4 and the 3 curated m = 9 instances | `out/charge_flow5.txt` |
| `charge_flow5b.py` | A1b: exhaustive m = 8 [−3,3], m = 9 [−2,2], partial m = 10 [−2,2], all t + 2k ≤ m | `out/charge_flow5b.txt` |
| `k1_hall.py` | A2: k = 1 — checks of the reductions (R1)–(R4), Hall slack over unions of classes and over all subsets, tight sets vs over-represented classes, proportional map, profile-model comparison | `out/k1_hall.txt` |
| `k1_families.py` | A2b: exact check of the two k = 1 families with closed forms (two-valued; one class + generics) | `out/k1_families.txt` |
| `hill5.py` | A3: hill-climb at m = 18, 20 in the window k < m/3, with the (m/2−1, m/2) control | `out/hill5.txt` |
| `hill5b.py` | A3b: the same climb with g ∈ {0, 4} generic entries fixed and all other values in [−3,6] (cannot reach a generic instance) | `out/hill5b.txt` |

Rule names: **YP** = the near miss (X, A, A′) may charge any target (Y, Y*, D) with Y ⊇ P = A∖A′; YPQ = Y ⊇ P or
Y ⊇ Q (Q = A′∖A); YPQx = YPQ and Y ≠ X; free = all edges (feasible iff Q_w ≤ 1). The conjecture under test
(YP-Hall) is about YP.
