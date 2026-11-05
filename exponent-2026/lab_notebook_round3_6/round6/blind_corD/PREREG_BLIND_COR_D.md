# Pre-registration: blind re-derivation of Base's Corollary D (fresh agent)
Written 2026-11-04 ~21:58 ET by Claude, before launching the agent.
Why: Fable and Astra both saw Base l.260-267 (Corollary D's proof case split) before writing; the t < k branch has not
been re-derived blind. Corollary D is a premise of the CERTIFIED 0.4875754 result.
Protocol: a fresh agent receives ONLY STATEMENTS_GIVEN.md (Base l.223-232, 240-242, 247-249, 254-258: definitions and the
statements of Lemmas 3.1-3.3 and Corollary D, no proof text, no line numbers of proofs, no hint of a case split). It is
told not to open any file on Jennifer's computer and not to look up the Base paper. It may run small exact computations in
its own sandbox. Its report is saved verbatim as BLIND_COROLLARY_D_REPORT.md before Claude compares it with Base.
Predictions (Claude's, sealed here, not given to the agent):
 P1 the agent proves Corollary D from Lemmas 3.1-3.3 (or finds a gap; either outcome is logged);
 P2 the product hypothesis C(σ,k)C(v,k) ≤ 2^v is used, in a regime where the good layer t of Lemma 3.3 lies below k;
 P3 the conditions 2k ≤ σ and 2σ ≤ v + 2k are used to fit σ inside V minus a (t−k)-set.
Control: the agent is asked to exhibit numerically that the conclusion can fail when the product hypothesis is dropped
(or to report that it found no such instance) — a check that it engages with every hypothesis.

## Outcome (appended 2026-11-04 ~22:20 ET; report saved verbatim as BLIND_COROLLARY_D_REPORT.md, extracted
## programmatically from the agent's final message; its scripts in scripts/)
- P1 MET: Lemmas 3.1-3.3 and Corollary D PROVED blind, for every layer t Lemma 3.3 can return.
- P2 MET: the product hypothesis is used only in the branch t < k, exactly as in Base l.267-270.
- P3 MET: 2σ ≤ v + 2k gives σ ≤ |V∖W| = v − t + k in the branch t ≥ k (Base l.263).
- Comparison with Base l.259-273 (read by Claude only after the report was saved): same two-case structure, same
  injections, same averaging step; NO difference in any step or constant. The t < k branch is now confirmed by a
  blind re-derivation.
- Control: no counterexample with the product hypothesis dropped (exhaustive |M| ≤ 10 in [−4,4] and more; ~3.1M
  dropped-hypothesis checks), with a structural reason: in that range some t ∈ [k, ⌊v/2⌋] always satisfies Lemma
  3.3's inequality. EVIDENCE only; whether the hypothesis is removable is open.
- Branch t < k is not vacuous: e.g. (−4,−3,−2,−2,1,1,2,3) has layer sizes 1,6,13,16,15,16,… (Claude rechecked: same
  numbers, |Σ| = 19).
- New cosmetic observations (none affect our results): σ ≤ v and k ≥ 0 are implicit; 2k ≤ σ and 2σ ≤ v + 2k are
  slightly stronger than needed; the product hypothesis can be weakened to C(σ,k)C(v,min(k−1,⌊v/2⌋)) ≤ 2^v;
  integrality of the weights is never used.
