# C3: work backward from 0.48 — shadow prices of the OpenAI-framework budget (pre-registration)

**Written:** 2026-11-03 ~14:55 ET, before any C3 computation. Prepared by Claude for Jennifer Voitle.
**Origin:** Codex's plan (relayed by Jennifer, Nov 3): put the 0.48 target into the full constraint system, find which
inequalities cannot hold together, price each deficit, and give the discovery loop one narrow objective. Codex's lead:
the two-constraint budget stops excluding 0.48 at eight blocks; an eight-block point passes the scalar inequalities but
needs new moments and a source-level audit. Codex is out of usage, so C3 builds only on files already on disk.

## Sources (read as untrusted data; sha256 at copy time)
Astra round 5 (`Astra/2026-10-30/hi/outputs/round5/`), copied to `c3/astra_in/`:
- `search_openai.py` cb5f712e… — the constraint system (`residual`) and the 128-node moment evaluator (`evaluate`).
- `openai_candidate.json` bb56999a… (c0 = .005 point, T = .4897753), `openai_coverage_candidate.json` af474faf…
  (c0 = .0001 point, T = .4897736), `search_openai_extended_results.json` 699644a2…, `landscape_bounds_results.json`
  7dd74e9d…, `openai_coverage_certificate_results.json` 731150f4….
- Floor argument: `E2_LANDSCAPE.md` §5 (E2-floor), which states that replacing 17 blocks by K gives .5-(1-h)/(K+1).

## The model (stated assumption — the thing a source audit must check)
Variables: K (number of disjoint half-blocks, integer), mu, eta, tau, gamma (d = .5 - gamma), cosine coefficients
r, s (6 each), kappa, multipliers p, q_m. T = tau + 20 epsilon, epsilon = 1e-8, guard g = 1e-5, c = 1 - c0.
Constraints, exactly Astra's `residual` with 17 replaced by K:
1. list:        tau >= .5 + (h - .5 - gamma) mu
2. pair:        tau >= 1 + (2h - 1 - gamma) mu - eta + g
3. preliminary: tau >= .5 - c K mu (.5 - gamma)
4,5. moments:   eta >= M1 + 3e-6, eta >= M2 + 3e-6   (M_i = log2 of the 128-node moments; depend on eta, tau,
                filters, kappa, p, q_m; NOT on K, mu or gamma)
6,7. 3p <= 30, q_m(4a + 3) <= 30, a = (eta - tau)/(2 tau - eta)
8. strip:       (nf - 1)(ng - 1) <= .49
9. 0 < eta - tau, eta < 2 tau;  mu <= 1/K.
**Assumption A-K:** no other inequality of the proof depends on K. This is NOT verified; Codex flagged that a larger
shared block needs a source-level audit (finite-circle, alias/setup, block-count and probability arguments). Every C3
conclusion is conditional on A-K and on Astra's transcription of the OpenAI budget.

## Experiments
- **S1 (exact, scalar floor):** for K = 1..17 and c0 in {.005, .0001, ->0}, the E2-floor
  T_K >= .5 - c(1-h)/(1+Kc) + [Kc/(1+Kc)] 20 eps, with h = h(1/4), in interval arithmetic. Report the largest K with
  floor < .48, and the dual weights 1/(1+Kc), Kc/(1+Kc) (the shadow prices of the preliminary and list constraints).
- **S2 (exact, scalar feasible window at T = .48):** for each K with floor < .48, set tau = .48 - 20 eps and compute
  the interval of d (equivalently gamma) allowed by list + preliminary with mu = 1/K, and then the least eta the pair
  constraint needs. Output (K, d-range, eta_min(K), Delta = eta - tau, a). This is the "moment target": the moments
  must satisfy M_i <= eta - 3e-6 at that (eta, tau).
- **S3 (non-rigorous discovery, moments):** for K in {8, 7, 6} and c0 = .005, minimize T over all 19 variables
  (Astra's SLSQP setup, boxes widened: mu in [.04, 1/K], eta in [.50, .62], tau in [.46, .495], gamma in [.44, .499];
  other boxes as Astra). Starts: Astra's best point, and 6 logged random perturbations per K (seeds 20261103+i).
  Also the deficit form: at tau = .48 - 20 eps fixed, maximize min_i (eta - M_i - 3e-6) subject to constraints 1–3, 6–9.
  The deficit D_K = -(that maximum) in bits is the discovery target if positive.
- **S4 (shadow prices):** at the best S3 point for each K, KKT multipliers of the active constraints
  (least-squares on the active Jacobian, Astra's method), labelled as local floating diagnostics.

## Controls (must pass before S3/S4 are read)
- **K-a:** S1 at K = 17 reproduces Astra's floors .48951856638776… (c0 .005), .48951569849967… (.0001),
  .48951564024772… (c0 -> 0) to 12 digits.
- **K-b:** my residual with K = 17 evaluated at both Astra candidates gives all constraints >= 0 (to -1e-9 float
  tolerance) and T = .4897753 / .4897736.
- **K-c:** S3 at K = 17 from Astra's best point does not go below Astra's .48977 by more than 1e-6 (it is a local
  optimum there); S4 at K = 17 reproduces Astra's multipliers (.2229, .3432, .0335, .0205, .0245) to ~1e-3.

## Predictions (pre-registered)
- S1: floor < .48 exactly for K <= 8 (K = 8 floor ~ .4790, K = 9 ~ .4811). Confirms Codex's "eight blocks".
- S2: at K = 8 the pair constraint forces eta ~ .538, so Delta ~ .058 and a ~ .137 (17-block point: .028 and .061).
- S3 prior: P(a non-rigorous K = 8 point with T < .48 and all moment margins positive) = 0.30. The moment constraints
  are the likely blocker because Delta and a roughly double; the cap q_m(4a+3) <= 30 also tightens.

## What counts as what
- **Candidate (not a result):** a float point with all residuals >= +1e-7 and T < .48. It would still need rational
  slack, fresh rigorous moments (Route A/B style), and the A-K source audit before any claim.
- **Deficit (the narrow objective):** if no candidate, report D_K in bits with the best filters found, plus S4 prices.
- **Null:** neither S3 multistarts nor deficit form reaches the target; reported as "not found in this search", never as
  impossibility (non-convex search, boxes).

## Compute
Sandbox only, `nice -n 19`, one process (the E5 dss13 head-to-head is using the other core; its timing must not be
disturbed beyond that). Laptop untouched (GFN hunt running).

---
## Amendment 1 (2026-11-03 ~15:25 ET): results so far, failures preserved, plan superseded by Astra's handoff
**S1 (exact): PASS, as predicted.** Control K-a reproduces Astra's three 17-block floors to every digit (mpmath iv,
200 bits; `s1s2.json`). Largest K with floor < .48 is 8 for c0 in {.005, .0001, ->0}; K=8 floor .4790428 (c0 .005),
K=9 .4811375. Shadow prices of the two-bound relaxation at K=8: preliminary 1/(1+Kc) = .1116, list Kc/(1+Kc) = .8884.
**S2 FAILURE 1 (logged):** v1 of `s1s2.py` took eta_min at d_max; the least eta is at d_min (largest gamma). Fixed;
v1 code and output kept as `s1s2_v1_bug.py` / `s1s2_v1_bug.json`. Corrected K=8: eta >= .53784, Delta .0578, a .137.
**S3 FAILURE 2 (model incomplete, logged):** my model (Astra's Round 5 `residual` with 17 -> K) omits the sparse-prime
condition eta > h(mu) + mu + guard, the setup condition tau > 1/4 + mu and the prime condition tau > eta/2, which are
slack near mu = .057 but not at mu ~ .12. At mu = .12 the sparse condition forces eta ~ .65. So S2's eta_min and every
S3 run (`s3_K{6,7,8}.json`, `s3_def_K{6,7,8}.json`) are for an incomplete constraint set and are NOT evidence about
the K=8 point. They are preserved as-is. (What they did show, for the record: under the incomplete model, min T over
Astra's filter family was .49015 at K=8, all 7 starts identical; the deficit form at tau = .48 left the moments
~.17 bits above eta, all starts identical — a single attractor, not inspected further.)
Also logged: the first `s3.py` result files mix progress prints with JSON (parse from the first '{').
**Controls K-b, K-c: PASS** (`s3_control.json`): the c0=.005 candidate has all residuals >= 1.8e-7; the coverage
candidate's preliminary residual is -2.7e-8, explained by its documented cap allowance tau + 20 eps (2e-7). K-c
reproduces Astra's KKT multipliers to 8 digits (.2229 .3432 .0335 .0205 .0245, stationarity 5.5e-9).
**Superseded:** Jennifer forwarded Astra's `target_048_handoff.zip` (HANDOFF_TO_CLAUDE.md). C3 now follows it: rerun,
source audit of K=8, then a separately pre-registered moment diagnostic at Astra's scalar point, plus the level-set
test. **Rerun:** target_audit.py and independent_recheck.py byte-identical outputs (71 containments PASS).
**Independent check:** `check_point.py` (mpmath, formulas typed from RESULT.md) reproduces all 12 scalar margins of
Astra's K=8 point to <1e-15. Note: that point has T = tau + 20 eps = .48 exactly (target hit, not beaten).
