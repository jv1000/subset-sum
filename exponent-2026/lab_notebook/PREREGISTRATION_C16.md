# C16: the C4 lever (an extra filtering level), what it can buy at most, and the architecture floor (pre-registration)
**Written 2026-11-03 ~19:05 ET, before any C16 run.** Jennifer: "Yes let's do this".

## Decomposition (algebra, done before modeling, the lesson from C15)
- C4 with η = τ0 + Δ: 2τ0 > (1 − Δ) + μ[(h(a) − γ) + (h(1/2 − a) − 1)].
- **1 − η = log2 of the alias count 2^n/P.** Theorem A inserts every alias class into a dictionary, so any design that
  enumerates alias classes pays at least this. That gives τ0 ≥ (1 − Δ)/2 for this whole architecture (alias
  enumeration + checksum with capacity Δ), whatever the list side does.
- **Overhead μ(h(a) − γ):** left masks range over all of M but only binom(m/2, k) of them represent an alias.
  With γ ≤ h(2a)/2, the overhead is about μ·a (one bit per mask element, because S is half of M).
  h(1/2 − a) − 1 ≈ −2.9a² is negligible.
- **The other side:** C2 + C3 (left records + right class records, with l + r = 1 − μ) give
  τ0 > 1/2 − μ(γ − h(a)/2). This wants larger a (more representations); C4's overhead wants smaller a.
- **C5 alone:** τ0 > (1/2 + μ h(1/2 − a))/2 (right masks × trials, using (LD)).
- So Base's list design is a three-way balance: (C2 + C3) vs C4 + moments vs C5. An "extra filtering level" can only
  attack C4's overhead term.

## Runs (floating; the C14 joint model, filter free)
1. **Closed-form check:** at the C12 point, the three reduced bounds must reproduce τ0 = .4875749 to within 1e-5
   (the binding ones agree).
2. **Value of an ideal extra level:** scale C4's overhead μ[(h(a) − γ) + (h(1/2 − a) − 1)] by ρ ∈ {1, .75, .5, .25, 0}
   and re-optimize. ρ = 1 must reproduce .4875749. This upper-bounds what ANY filtering improvement of C4 buys.
3. **Architecture floor:** τ0 ≥ (1 − Δ_cap(τ))/2, evaluated with our capacity curve.

## Predictions
- ρ = 0 buys at most ~.002 (about μa/2 ≈ .0019). The realized value is smaller, because C5 and C2 + C3 bind next.
  Point prediction: ρ = 0 gives τ0 ≈ .4866 ± .0005.
- The architecture floor is (1 − .0287)/2 ≈ .4856, so 0.48 is unreachable in this architecture: it would need
  Δ_cap ≥ .04 even with zero list overhead. This is consistent with the Lemma 1 cap of ~.0427 on M1 alone.

## C16 results (~19:20 ET); c16.py, c16.json
1. **Closed form reproduces the optimizer** at the C12 point: C2 + C3 → .4875739, C4 → .4875744, C5 → .4875744,
   against the optimizer's τ0 .4875749. All within 1e-6. PASS.
   - Our point (and Base's .4877) is an explicit three-way balance:
     - C2 + C3: τ0 > 1/2 − μ(γ − h(a)/2), wanting more representations;
     - C4 with the moments: 2τ0 > 1 − Δ + overhead, wanting smaller masks;
     - C5: τ0 > (1/2 + μ h(1/2 − a))/2.
2. **Value of an ideal C4 filtering level** (C4 overhead scaled by ρ, everything else re-optimized):

| ρ (fraction of overhead kept) | τ0 | gain vs C12 |
|---|---|---|
| 1 (control) | .4875749 | 0 (PASS) |
| .75 | .4871858 | 3.9e-4 |
| .50 | .4867641 | 8.1e-4 |
| .25 | .4863049 | 1.27e-3 |
| 0 | .4858019 | 1.77e-3 (only C4 and the moments active) |

   - Roughly linear: each 10% of the overhead removed is worth ≈ 1.6–1.8e-4.
3. **Architecture floor:** at ρ = 0, τ0 = (1 − Δ_cap)/2 exactly (Δ_cap = .02840): .485801.
   - Any design that enumerates alias classes modulo a P of ηn bits, with checksum capacity Δ, satisfies τ0 ≥ (1 − Δ)/2.
   - 0.48 needs Δ_cap ≥ .040 even with a perfect list side. The OpenAI-format moments are capped at ~.0427 by Lemma 1
     and reach ~.029 in practice.
4. **What the overhead is (c16 check):** C4's overhead μ[(h(a) − γ) + (h(1/2 − a) − 1)] = .003846 per n equals
   −log2 P(a random left mask and a random right mask are disjoint) = .003845 per n.
   - Finite m = 2000 exact count: .003735. An exact entropy identity at γ = h(2a)/2.
   - **So the C4 overhead is precisely the visited tuples with X ∩ Y ≠ ∅**, which the expansion step tests and discards
     (Lemma A1 needs X ∩ Y = ∅).
   - **The C4 lever, stated precisely:** enumerate only the matching (left record, class member) pairs with disjoint
     masks, in time close to their number. That is a disjointness-filtered join. Fully achieved it is worth 1.77e-3
     (τ0 → .4858); every 10% of the junk avoided is worth ~1.7e-4.
- **Predictions:**
  - "ρ = 0 buys at most ~.0019": HELD (1.77e-3).
  - Point "ρ = 0 → .4866 ± .0005": WRONG. With C4's overhead gone, μ and a move until C2 + C3 and C5 go slack, and τ0
    reaches the architecture floor.
  - "Architecture floor ≈ .4856": HELD (.4858; the capacity at that τ is .02840, not .0287).
- **Hard part (not attempted yet):** general set-disjointness joins are OV-hard. A gain needs structure specific to
  this setting, e.g. small k = am (X has ~0.008m elements), class members sharing a value, or random partitions /
  colour-coding of M per trial that keep the representation count. Each candidate needs its own representation-count
  and coverage check (the C15 lesson).
