# Round-6 pre-registration (independent re-derivation of Base's core; computational checks only)

Discipline as in rounds 2–5. These checks are small (seconds, numpy only, `python -I`), one process at a time. They
support the written re-derivation in `../../BASE_CORE_REDERIVATION.md`; none of them is a proof. Sources: `../../../base_PROOF_0.4877.tex`
(the only copy in the folder; the folder is not a git repository, so the commit 44c34961 could not be verified) and
`../../../openai_tex/sections/*.tex`. My own proofs were written to a scratch file before Base's proof bodies were read;
the comparison was written after.

## R6-C1 `core_checks.py` part A — Lemmas 3.1, 3.2, 3.3 and Corollary D by exhaustive enumeration
Random integer weight multisets on |V| ≤ 9 elements (values in [−3,3], repeats and signs allowed; also generic
weights as a control), all (k,t) with k ≤ t ≤ |V|: compute a_t(V), E_W a_k(V∖W) (all W), E_S a_k(S) (all S), the
good layer of Lemma 3.3, and Corollary D's two sides for all (k,σ,v) satisfying its hypotheses on |M| ≤ 8, by exact
rational arithmetic. Also (F2): d(V) for the weights with the signs of a random subset negated equals d(V).
Prediction: every inequality holds in every case; Lemma 3.1 and 3.2 are equalities for generic weights (all
layer densities 1); Corollary D is never an equality on the random sets but is tight within a factor 2 somewhere;
(F2) holds exactly. Control: the inequality of Lemma 3.1 with the roles of t and k swapped (a_k(V) ≤ E a_t) fails on
some instance (so the check can fail).

## R6-C2 `core_checks.py` part B — one trial of Theorem A, brute force, against the Step-0 characterisation
Tiny instances: n = 8, m = 4 (σ = 2, k = 1), |L| = 2, |R| = 2, weights c_i ∈ [1, 40], prime P ∈ {31, 37, 41, 43},
targets t_s = all values 0..Σc; aliases by brute force. For 300 random trials (F ⊆ M uniform, P′ ∈ {5, 7, 11}
uniform, j′ uniform) implement steps (c)–(g) of Base §5.2 literally (left records, right classes, class records,
matching with the skipped interval, expansion, dictionary) and compare the inserted key set, for every target and
carry, with the prediction "the key of the class of alias I is inserted iff |S| = σ and some k-subset X of S has
b(κ(I∩L)) + b^F(X) ≡ j′ (mod P′)", S = (I∩M)△F. Prediction: exact agreement in all trials; every inserted key is an
alias class (Lemma A1). Control: with the skipped interval removed, some inserted key is an exact-sum class
(not an alias), so the check sees the exclusion.

## R6-C3 `core_checks.py` part C — Lemma B2 (domination) numerically, with the a_Γ ≤ 3/4 control
Random patterns: J = 43 values (U_l, W_l), v = argmax U_l, region of W_v, random z ≥ 0 with the stated z_0
condition, random C; coordinate averages ū_l, w̄_l drawn within 3ε, 4ε of the pattern values (adversarially at the
boundary half the time); check −α U_v ≤ −Δ + z·Ḡ + 6εΣz for sampled patterns. Prediction: holds in all cases at
a_Γ = 0.0619. Control: with a_Γ = 0.9 (so 4a_Γ + 3 > 6) and adversarial errors, the inequality fails for some
instance with z = (z_0, 0, 0, …) and a tight margin (the 6ε accounting needs a_Γ ≤ 3/4).

## R6-C4 `core_checks.py` part D — the two OpenAI moments (float, 4096-node trapezoid)
Compute u, v from OpenAI's filter (6 cosines, κ = 1.0315) and the moments M_1 (p = 8.5) and M_2 (q = 8.3) with
OpenAI's constants. Prediction: log2 M_1, log2 M_2 < 0.5168 (OpenAI Prop. 3.1), to be compared with the ρ_c of the
JoshuaQFEX/paper.md convention; this only checks my reading of u, v, a (the J = 1 reduction is algebraic).

## Outcomes — core_checks.py, out/core_checks.txt (10 s)
C1: Lemma 3.1: 763 cases, 0 failures, 63 equalities (all on the generic instances); Lemma 3.2: 763 cases, 0 failures,
63 equalities (generic); Lemma 3.3: 30 cases, 0 failures; (F2): 0 failures; Corollary D: 462 (w,k,σ,v) cases,
0 failures, smallest ratio lhs/rhs = 2.40 (so never tight within a factor 2 on these sets — the prediction "tight
within a factor 2 somewhere" was NOT met; the pointwise case t < k and the (v+1) factor leave room). Control
(Lemma 3.1 with t and k swapped): 66 failures, as required. All predictions met except the factor-2 tightness.
C2: 300 trials × 8,273 (trial, target) pairs: exact agreement between the literal implementation of §5.2 (c)–(g)
and the characterisation "inserted iff |S| = σ and some k-subset X of S has b(κ(I∩L)) + b^F(X) ≡ j′ (mod P′)";
4,207 inserted keys, 0 soundness failures; control without the skipped interval: 1,256 exact-sum classes inserted.
Predictions met.
C3: random patterns at a_Γ = 0.0619: 0 failures (min margin 0.47 random, 0.60 adversarial signs) — the random test
is far from tight. The pre-registered control was ILL-POSED: a_Γ is not a free parameter (α a_Γ W = Δ needs
a_Γ = Δ/Γ), so "a_Γ = 0.9 with Base's Δ, Γ" is inconsistent and produced 0 failures with margin 1.0. Replaced
(after the first run, recorded here) by the explicit tight instance predicted by the algebra: region ρ_3,
W = Γb_2(1 + 10⁻¹³), U = a_Γ W − 10⁻¹³, z = (1/b_2, 0, 0), worst-sign errors, with (Δ, Γ) varied consistently:
margin = z₀ε(3 − 4a_Γ) exactly — 1.72·10⁻⁸ at Base's point (a_Γ = 0.0619), 0 at a_Γ = 0.75, −1.25·10⁻⁹ at
a_Γ = 0.8, −3.75·10⁻⁹ at a_Γ = 0.9 (FAILS). So the 6εΣz accounting of Lemma B2 is exactly equivalent to
a_Γ ≤ 3/4 on this instance.
C4: OpenAI filter: log2 M_1 = 0.51497, log2 M_2 = 0.51485, both < 0.5168 as claimed; min D = 0.068,
min(D − A) = 0.115, min(D − E) = 0.110 (the entropy order (3.3) holds). Prediction met.
