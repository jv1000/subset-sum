# Round-3 scripts

Run from `Fable_round2/` with `python -I scripts/round3/<name>.py`. Python 3.12 + numpy (no scipy: the max-flow is a
hand-written Dinic in `lay3.py`). One process at a time; the longest script takes 8 minutes. Pre-registrations and
outcomes: `PREREG_R3.md`. Outputs in `out/` (`.txt` = results, `.log` = full stdout).

| Script | Purpose | Output |
| --- | --- | --- |
| `lay3.py` | brute-force layers/fibers (m ≤ 16), lex witnesses, multiplicity Q, shadow graph, Dinic flow, instance generators | library |
| `free_bounds.py` | A0: the PROVED bounds P2/P3/P4 as a harness check | `out/free_bounds.txt` |
| `approx_mono.py` | A1: monotonicity ratios (middle step included), interior ratio, μ′ at m = 10..14, random | `out/approx_mono.txt` |
| `cs_rep.py` | A2: witness-rule second-moment constant Q_lex, k ≤ m/4 | `out/cs_rep.txt` |
| `hall_flow.py` | A3: flow constant P* of the shadow graph (binary search on capacity) | `out/hall_flow.txt` |
| `sparse_tail.py` | A4: a_k 2^d (m+1), tail condition, near-miss lemma P5, m = 12..16 | `out/sparse_tail.txt` |
| `cs_w.py` | A5: canonical Q_w, its reduction w(L^nm) vs w(R′), all k < t ≤ m/2, counterexamples first | `out/cs_w.txt` |
| `hill.py` | A6: hill-climb for interior/middle violations and for large Q_w (k ≤ m/4) | `out/hill.txt` |
| `floor_designs.py` | Task 3: fixed-Δ model pricing of the floor-breaking designs | `out/floor_designs.txt` |
| `make_section_t_v2.py` | Task 2: generates `SECTION_T_v2.md` from Section T by asserted exact-match substitutions | `../../SECTION_T_v2.md` |

Smallest instance where the canonical second-moment constant exceeds 1 (k = m/3, monotonicity still holds):
`w = (−3,−3,−2,−2,0,0)`, (k,t) = (2,3): Q_w = 1.0357, a_3/a_2 = 0.875. Smallest with k ≤ m/4: none found.
