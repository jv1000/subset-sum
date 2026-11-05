# Round-4 scripts

Run from `Fable_round2/` with `python -I scripts/round4/<name>.py`. Python 3.12 + numpy only (the max-flow is the
hand-written Dinic from `../round3/lay3.py`). One process at a time; the longest script takes 16 minutes; nothing is
enumerated above m = 20. Pre-registrations and outcomes (including the predictions that failed): `PREREG_R4.md`.
Outputs in `out/` (`.txt` = results, `.log` = full stdout). Report: `../../ROUND4_REPORT.md`.

| Script | Purpose | Output |
| --- | --- | --- |
| `lay4.py` | library: subset sums by doubling (m ≤ 20), layer data, fast chunked Q_w with per-u ratio, generic padding, generic-separated products | library |
| `window_small.py` | A0: exact window at small m (exhaustive [−3,3] m = 6..10, [−4,4] m = 6..8, [−5,5] m = 6, 7) | `out/window_small.txt` |
| `charge_flow.py` | A1: aggregated near-miss/target enumeration (`Inst`), locality rules S1E/S1P/S1/S2/T/C/V/free as max-flow, explicit proportional map | `out/charge_flow.txt` |
| `per_rho.py` | A1b: the per-relation inequality S(ρ) ≤ T(ρ) and its \|P\|-aggregated version | `out/per_rho.txt` |
| `charge_flow2.py` | A1c: sub-relation rules SUPA/SUPD/SUPX/SUP | `out/charge_flow2.txt` |
| `mincut_diag.py` | Hall violator (residual reachability after Dinic) with named elements, for SUP on two instances | `out/mincut_diag.txt` |
| `charge_flow3.py` | A1d: k-set keyed rules DA/DAA/YA/YAA and the relation-half rule YPQ | `out/charge_flow3.txt` |
| `charge_flow4.py` | A1e: YP/YPQx/YPQ on the curated list (died of MemoryError before the exhaustive part; kept) | `out/charge_flow4.txt` |
| `charge_flow4b.py` | A1e-b: the exhaustive/sampled part of A1e with an edge-count guard | `out/charge_flow4b.txt` |
| `window.py` | A2: window k/m ∈ (1/4, 1/3) at m = 12..16, two-valued + {0,p,q} splits + generic padding | `out/window.txt` |
| `window20.py` | A3: window at m = 20, targeted families | `out/window20.txt` |
| `gadget_limit.py` | A4: product-limit R/m and E(α,τ) by the maximum-entropy formula (own 2-D dual minimiser), exact products q ≤ 3 | `out/gadget_limit.txt` |

Rule names (edges from a near miss (X, A, A′), P = A∖A′, Q = A′∖A, B = Q ∩ X, to a target (Y, Y*, D)):
S1 = swap-repair Y = (X∖B) ∪ E, Y* = (Y∖P) ∪ Q; T = repaired Y with any partner; C = collision at X; V = Hamming
vicinity 2|B|; SUP = P ⊆ Y∖Y*, Q ⊆ Y*∖Y; DA = D = A; YA = Y ⊇ A; YAA = Y ⊇ A or A′; **YP = Y ⊇ P** and
**YPQ = Y ⊇ P or Y ⊇ Q** (the only rules with no failure, 13,661 cases); free = all edges (feasible iff Q_w ≤ 1).
