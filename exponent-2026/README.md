# Worst-case Subset Sum below 0.4876: a certified exponent and the floor of the alias–checksum architecture

**Authors:** Jennifer Voitle, with Claude (Anthropic) and Astra (an OpenAI-based assistant).
**Status:** working research record, frozen 2026-11-04. Not peer reviewed. The paper draft is in `paper/paper.md`.

## Results in this snapshot

| Result | Status | Where |
|---|---|---|
| Exponent **T = 0.4875754036**: Subset Sum in time O(2^{T′n}) for every T′ > T (in particular O(2^{0.4875755 n})). This is Base's construction (a-kapila, PROOF_0.4877.tex @ 44c34961) with ONE asymmetric filter (16 cosine + 16 sine terms) in place of Base's 43 cosine-only filters. | All 33 numerical conditions, including both filtering moments, certified in ball arithmetic (python-flint arb); checked by two independent referees. **Conditional, like JoshuaQFEX's 0.487676, on Base's written proof and on the OpenAI paper.** | paper §8; `lab_notebook/candidate_base.json`, `certify_base.py`, `cert_base_256_v2.json`, `PREREGISTRATION_C12.md`, `referee3/`, `referee4/` |
| Exponent **0.4894615727** inside the original OpenAI construction (16 half-blocks, asymmetric densities). | Two independent rigorous certificates and a referee; conditional on the OpenAI proof and the block-count audit. | paper §4, §7; `lab_notebook/candidate_K16.json`, `cert_K16_*.json`, `referee2/` |
| **Lemma 1**: a lower bound on the first filtering moment for all densities. With the list and pair bounds, exponent 0.48 is impossible in the OpenAI construction for every parameter choice. | Proved; refereed; interval-evaluated. | paper §5; `lab_notebook/holder_*.py`, `RESULT_C3.md`, `referee/` |
| **Why the exponents stall near 0.4876.** Three closed-form bounds; the floor τ ≥ (1 − Δ)/2 ≈ 0.4857 for any design that enumerates every alias class modulo the checksum prime; the remaining list overhead is exactly the share of overlapping mask pairs; filter families, ternary masks and colour-coding do not help under Base's lemmas. | Exact algebra plus floating, pre-registered experiments (C13–C17). | paper §9 |
| Independent certification of the 430 moment premises of the JoshuaQFEX bound. | Two routes plus an outside check. | paper §3; `joshuaqfex_premises/` |
| **Open:** ternary masks would give **τ0 ≈ 0.48734** if small slices of a weighted cube have no larger average fiber than the whole cube (equivalently, if layer densities are monotone). | Reduction proved; strong numerical evidence; NOT proved. | paper §10; `open_lemma/LEMMA_R_HANDOFF.md` |

## Method
- Every experiment was pre-registered before it ran (`lab_notebook/PREREGISTRATION_*.md`), with predictions, controls
  and kill rules.
- Failures and mistakes are kept and logged next to their corrections.
- Certified claims have at least two independent implementations. Independent referees saw only the claim's inputs
  and the source papers, never the authors' code.
- The second full review (referee 4) was by Claude Fable 5.1 working in a separate folder. Its report, our
  point-by-point response and its exploratory notes on Ye–Li are in `lab_notebook/referee4/`. Its own scripts are
  held separately and will be added.

## Not included
The source papers are not redistributed. Read them at their origins:
- OpenAI, "Subset Sum in time O(2^{0.49n})" (4 Oct 2026);
- Ye and Li, "Subset Sum via Partial Match", arXiv:2610.10446;
- a-kapila/maths-proofs (Base), commit 44c34961;
- JoshuaQFEX/subset-sum-bound, bed8e18.

## Verifying the main claim
```
pip install python-flint numpy
cd lab_notebook
python3 -I certify_base.py candidate_base.json        # prints all margins; all_pass must be true
```

## Integrity
`MANIFEST.sha256` lists the SHA-256 of every file in this folder. Its own SHA-256 is the fingerprint of this
snapshot, and is timestamped publicly (see `TIMESTAMP.md`).
