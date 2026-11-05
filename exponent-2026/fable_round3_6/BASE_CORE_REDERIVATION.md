# Independent re-derivation of Base's core: Lemma A5, Corollary D with Lemmas 3.1–3.3, and the region analysis of Theorem B

Claude Fable 5.1, 4 Nov 2026 (round 6). Sources: `../base_PROOF_0.4877.tex` ("Base"; the folder is not a git
repository, so the stated commit 44c34961 could not be verified — this is the only copy present, dated 3 Nov 2026
on disk, title date 12 Oct 2026) and `../openai_tex/sections/*.tex` ("the paper"). Nothing else was used for the
mathematics. Discipline: the statements, definitions and procedure descriptions of Base (§2, §3 statements, §5.1–5.5
non-proof text, §6.1–6.2, the statements of A1–A7, B1–B3, Theorem B) and the paper's §2–4 were read first; my own
proofs were written to a scratch file *before* Base's proof bodies were opened; the comparison below was written
after. One leak to declare: while locating the statements I grepped my own round-3 referee report, whose output
quoted two lines of Base's proof of Corollary D (the case split "t ≥ k / t < k"); my proof of Corollary D uses the
same split, and I cannot rule out that I was primed by it. Everything else was derived blind. Four small
computational checks (seconds, numpy only) were pre-registered in `scripts/round6/PREREG_R6.md` and are reported
in §5; they support the reading of the procedure, not the proofs.

Labels: PROVED = I have a complete written proof below; EVIDENCE = numerical; CONJECTURE = none needed here.
Verdicts on Base's text: **fatal** = the argument as written is wrong and no local fix is known; **repairable** =
wrong or missing step with an evident local fix; **cosmetic** = correct but imprecise, loose, or unlisted.

## Summary

| Part | My proof | Base's proof vs mine | Fatal | Repairable | Cosmetic |
| --- | --- | --- | --- | --- | --- |
| 1. Lemmas 3.1–3.3, Corollary D | PROVED (§1) | same injections and the same two-case coupling; all hypotheses located | 0 | 0 | 2 |
| 2. Lemma A5 (law of S, signing, Corollary D, small prime, recovery) | PROVED (§2), 6 steps | identical step structure; same constants; the one parameter condition not in (C1)–(C8) is stated inline | 0 | 0 | 3 |
| 3. Region analysis of Theorem B (Lemmas B1–B3, J = 1 ⟹ M₁, M₂) | PROVED (§3) | identical; one justification sentence in Lemma B2 is wrong in general although the detailed accounting beneath it is right (needs a_Γ ≤ 3/4) | 0 | 1 | 4 |

Bottom line: in these three parts I found no gap that changes any constant or any conclusion. The one repairable
item (Lemma B2's "coefficients of absolute value at most 1" justification) is a one-sentence fix and the needed
condition a_Γ ≤ 3/4 holds with slack 0.69 at Base's point. The constants I obtain are the same as Base's wherever
Base states one (2^{−g_M}n^{−6}; 1/(m+1); 2^{−δn} ≤ 2^{−g_M}/(2(v+1)); 6εΣz; (18 + c_z)ε < 2.6·10⁻⁵;
2^{−0.00017n+2}), and Base's δ > 0.0706 is correct at Base's own parameters (δ = 0.070643; the value 0.0698 quoted in
my earlier referee report belongs to the retuned point of `paper.md`, not to Base).

---

## 1. Corollary D and Lemmas 3.1–3.3 (the small-layer bound)

### 1.1 Statements (Base §3)

Integer weights w on a finite index set, repeats allowed. Σ_j(V) = {w(T) : T ⊆ V, |T| = j}, a_j(V) = |Σ_j(V)|/C(|V|,j),
Σ(V) = ∪_j Σ_j(V), d(V) = |V| − log|Σ(V)|.
- Lemma 3.1 (covering): 0 ≤ k ≤ t ≤ |V|, W uniform (t−k)-subset of V ⟹ a_t(V) ≤ E_W a_k(V∖W).
- Lemma 3.2 (sampling): k ≤ s ≤ |V|, S uniform s-subset of V ⟹ E_S a_k(S) ≥ a_k(V).
- Lemma 3.3 (good layer): some t with 2t ≤ |V| has |Σ(V)| ≤ (|V|+1)|Σ_t(V)|; so a_t(V) ≥ 2^{−d(V)}/(|V|+1).
- Corollary D: integers k, σ, v with 2k ≤ σ, 2σ ≤ v + 2k, v ≤ |M|, C(σ,k)C(v,k) ≤ 2^v; S uniform σ-subset, V uniform
  v-subset of M ⟹ E_S a_k(S) ≥ E_V 2^{−d(V)}/(v+1).

### 1.2 My proofs (PROVED)

Identity used twice: for 0 ≤ k ≤ t ≤ N, C(N,t)C(t,k) = C(N,k)C(N−k,t−k) = C(N,t−k)C(N−t+k,k) (count a t-set with a
marked k-subset in three orders).

*Lemma 3.1.* For each σ ∈ Σ_t(V) fix a representative T_σ. For a (t−k)-set W ⊆ T_σ the k-set T_σ∖W ⊆ V∖W has
weight σ − w(W); for fixed W, σ ↦ σ − w(W) is injective, so |Σ_k(V∖W)| ≥ #{σ : W ⊆ T_σ}. Summing over all W,
Σ_W |Σ_k(V∖W)| ≥ |Σ_t(V)| C(t,t−k). Divide by C(N,t−k)C(N−t+k,k) = C(N,t)C(t,k). ∎

*Lemma 3.2.* Fix representatives K_σ (k-sets) for σ ∈ Σ_k(V). |Σ_k(S)| ≥ #{σ : K_σ ⊆ S} and P(K_σ ⊆ S) =
C(N−k,s−k)/C(N,s). So E a_k(S) ≥ |Σ_k(V)| C(N−k,s−k)/(C(N,s)C(s,k)) = |Σ_k(V)|/C(N,k). ∎

*Lemma 3.3.* |Σ(V)| ≤ Σ_j |Σ_j(V)| ≤ (N+1) max_j |Σ_j(V)|; complementation T ↦ V∖T gives |Σ_j| = |Σ_{N−j}|, so
the maximum is at some t ≤ N/2; then a_t(V) ≥ |Σ(V)|/((N+1)2^N) = 2^{−d(V)}/(N+1) because C(N,t) ≤ 2^N. ∎

*Corollary D.* From the hypotheses: k ≤ σ ≤ v and k ≤ v/2. Draw V; let t = t(V) ≤ v/2 be a layer from Lemma 3.3 for
V. Given V let S′ be a uniform σ-subset of V; then S′ is a uniform σ-subset of M, so E_S a_k(S) = E_V E[a_k(S′) | V],
and it suffices to prove E[a_k(S′) | V] ≥ 2^{−d(V)}/(v+1) for each V.
Case t ≥ k: Lemma 3.1 on V with W a uniform (t−k)-subset: a_t(V) ≤ E_W a_k(V∖W), |V∖W| = v − t + k ≥ v/2 + k ≥ σ;
Lemma 3.2 on V∖W with s = σ: a_k(V∖W) ≤ E a_k(S″), S″ a uniform σ-subset of V∖W. Given V, the law of S″ is the
uniform law on σ-subsets of V (for every σ-set S ⊆ V, P(S″ = S) = C(v−σ,t−k)/(C(v,t−k)C(v−t+k,σ)), which does not
depend on S; here t − k is a function of V only), i.e. the law of S′. Hence E[a_k(S′)|V] ≥ a_t(V) ≥ 2^{−d(V)}/(v+1).
Case t < k: t < k ≤ v/2 gives C(v,t) ≤ C(v,k), so 2^{v−d(V)} = |Σ(V)| ≤ (v+1)|Σ_t(V)| ≤ (v+1)C(v,k), hence
2^{−d(V)}/(v+1) ≤ C(v,k)/2^v ≤ 1/C(σ,k) ≤ a_k(S) for every σ-set S (Σ_k(S) ≠ ∅). ∎
Where the hypotheses enter: v ≤ |M| (V exists); 2k ≤ σ (k ≤ s in Lemma 3.2, and k ≤ v/2 in case t < k);
2σ ≤ v + 2k (σ ≤ |V∖W|); C(σ,k)C(v,k) ≤ 2^v (case t < k only). Signs and the values of the weights play no role;
this is why the corollary can later be applied to the signed weights c^I.

### 1.3 Comparison with Base (lines 232–273)

- Lemma 3.1: Base's proof is the same injection (x, W) ↦ (W, x − w(W)), same division by C(|V|,t)C(t,k). Identical.
- Lemma 3.2: same representatives K_x, same probability C(|V|−k,s−k)/C(|V|,s) = C(s,k)/C(|V|,k). Identical.
- Lemma 3.3: same covering and complementation, t = min(j, |V|−j), C(|V|,t) ≤ 2^{|V|}. Identical.
- Corollary D: same two cases, same coupling. Base's proof contains the two facts my proof needs and that a reader
  might miss: (a) for fixed V, "when W is uniform, S′ is a uniform σ-subset of V" (the size of W is fixed once V is
  fixed, so the composite is uniform — Base asserts it; I verified it by the explicit count above); (b) "a uniform
  σ-subset of a uniform v-subset of M is a uniform σ-subset of M". Both are correct and both are stated.
- Base derives k ≤ σ ≤ v and k ≤ v/2 from the hypotheses exactly as I do.

Findings (Part 1):
| # | Item | Class | Note |
| --- | --- | --- | --- |
| 1.1 | Lemma 3.3's "In particular" uses C(|V|,t) ≤ 2^{|V|}, which wastes a factor ≈ 2^{|V|h(t/|V|)}/2^{|V|}; harmless because Corollary D only needs the (v+1) loss, which later costs a polynomial factor in Lemma A5. | cosmetic | no change |
| 1.2 | The hypothesis C(σ,k)C(v,k) ≤ 2^v is used only in the case t < k, where it makes the trivial bound a_k(S) ≥ 1/C(σ,k) dominate; Base's text does not say that this is the only place it enters, and (S3)'s numeric check "h(2a)/2 + h(a) = 0.129 < 1 − 2a" is a loose rounding of 0.1290 (I get 0.12898 at a = 0.0082). | cosmetic | no change |

---

## 2. Lemma A5 (one trial inserts the alias class)

### 2.1 Setting (Base §5.2–5.5, statements only)

Fixed: the partition M, L, R; the keys κ(A) = (c(A), b(A)); the maps Φ_L, Φ_R; the target t_s; an alias I ∈ A_s(P)
with carry q (b(I) = T_{s,q} = (t_s mod P) + qP); the events (LD), E_3 (Lemma A3: F̂ ≥ g_M; under (LD),
g_M ≤ e_M ≤ (1/2 − τ0 + ζ)n + n^{0.6}) and the event of Lemma A4 (at most a 2^{−δn} fraction of the σ-subsets of
M are bad for P, δ = (η − (μ/2)log 3)/2); (5.1): c^F(Z) = c(Z△F) − c(F), b^F(Z) = b(Z△F) − b(F) for Z ⊆ M;
(5.3): on a good S, distinct signed c-sums (any fixed signs) have distinct signed b-sums. A trial for (s,q): F ⊆ M
uniform; P′ a uniform prime in [2^{⌊γm⌋}, 2^{1+⌊γm⌋}); j′ uniform mod P′; T^F = T_{s,q} − b(F), t^F = t_s − c(F);
then the left records (κ_L, X) (|X| = k, b(κ_L) + b^F(X) ≡ j′), the right classes λ(Y) = (b^F(Y), c^F(Y))
(|Y| = σ − k), the right class records (κ_R, λ) (b(κ_R) + b_λ ≡ T^F − j′), matching by the integer b-sum with the
interval of integer c-sum t^F − c(κ_L) − c^F(X) skipped, expansion over the members Y of a visited class with
X ∩ Y = ∅, insertion of (κ_L, κ_R, (X∪Y)△F) into D_s.

**Lemma A5.** Under (LD), E_3 and the event of Lemma A4, one trial for (s,q) inserts the key of the class of I,
(κ(I∩L), κ(I∩R), I∩M), with probability ≥ 2^{−g_M} n^{−6}, the threshold for n independent of I, s, P, M.

### 2.2 My proof (PROVED)

Write A = I∩L, B = I∩R, κ_L = κ(A), κ_R = κ(B), S := (I∩M) △ F ⊆ M.

*Step 0 (what the trial must do — an "iff").* The key of I's class is inserted iff |S| = σ and some k-subset X ⊆ S
has b(κ_L) + b^F(X) ≡ j′ (mod P′).
(⇐) Put Y = S∖X. By (5.1), b^F(X) + b^F(Y) = b^F(S) = b(I∩M) − b(F), so b(κ_L) + b^F(X) + b(κ_R) + b_{λ(Y)} =
b(I) − b(F) = T^F as integers, and the same computation with c gives c(I) − c(F) ≠ t^F because I is an alias.
The left record (κ_L, X) is listed (κ_L is a key of L, residue j′). The class record (κ_R, λ(Y)) is listed: every
(σ−k)-subset of M is a member of a class, and its residue is T^F − j′ by the integer identity. In matching it sits
in the group looked up by the left record and outside the skipped interval, so it is visited; expansion reaches Y,
X ∩ Y = ∅, and inserts (κ_L, κ_R, (X∪Y)△F) = (κ_L, κ_R, I∩M).
(⇒) An insertion of (κ_L, κ_R, Z) with Z = I∩M comes from disjoint X, Y with X ∪ Y = Z△F = S, |X| = k, |Y| = σ−k,
and (κ_L, X) a listed left record, so |S| = σ and the residue condition holds. (Only ⇐ is needed for the bound;
check C2 in §5 confirms the "iff" on 8,273 (trial, target) pairs of a literal implementation.)

*Step 1 (the law of S).* F is uniform on the 2^m subsets of M and Z ↦ Z △ (I∩M) is a bijection of the power set,
so S is uniform on the subsets of M; P(|S| = σ) = C(m,σ)2^{−m} ≥ 1/(m+1); given |S| = σ, S is a uniform σ-subset
of M; and F = S △ (I∩M) is a function of S.

*Step 2 (the signing is fixed by I).* For i ∈ S exactly one of i ∈ I∩M, i ∈ F holds, so (−1)^{[i∈F]} = +1 if
i ∈ I and −1 if i ∉ I. Define c^I_i = c_i (i ∈ I∩M), c^I_i = −c_i (i ∈ M∖I), and b^I likewise: these depend on I
only. For every trial outcome and every X ⊆ S, c^F(X) = c^I(X) and b^F(X) = b^I(X). Hence the left-mask integers
{b(A) + b^I(X) : X ⊆ S, |X| = k} form a translate of {b^I(X)}, with B(S) := |Σ_k(S; b^I)| distinct values; if S is
good, (5.3) with the signs of c^I gives B(S) ≥ |Σ_k(S; c^I)| = a_k(S; c^I) C(σ,k). And d(V; c^I) = d(V; c) for all
V ⊆ M by (F2) (negating the weights on M∖I translates every Σ(V)).

*Step 3 (Corollary D).* Apply Corollary D to the weights c^I on M with (k, σ, v) of §2.2; its hypotheses are
2k ≤ σ and 2σ = v + 2k (S1), v = m − 2k ≤ m, C(σ,k)C(v,k) ≤ 2^v (S3). With S a uniform σ-subset of M:
E_S a_k(S; c^I) ≥ E_V 2^{−d(V)}/(v+1) = 2^{−g_M}/(v+1). Since a_k ≤ 1 and the bad fraction is ≤ 2^{−δn},
E_S[1{S good} a_k(S; c^I)] ≥ 2^{−g_M}/(v+1) − 2^{−δn} ≥ 2^{−g_M}/(2(v+1)) for large n, because by E_3 and (LD),
g_M ≤ (1/2 − τ0 + ζ)n + n^{0.6} and 1/2 − τ0 + ζ = 0.012311 < δ = 0.070643.

*Step 4 (a random small prime keeps a positive fraction of the distinct integers).* Fix a good S with |S| = σ, and
let w_1 < … < w_B be the B = B(S) distinct integers of Step 2 (in (−nP, nP), so differences have < ηn + log n + 3
bits). They depend on P, M, L, I, S only; P′ and j′ are independent of them. For z_a = #{j : w_j ≡ a (mod P′)},
(F4) with L′ = ⌊γm⌋ gives P(P′ | w_i − w_j) ≤ K_0 n² 2^{−γm} (K_0 ≥ 1 absolute, large n), so
E_{P′} Σ_a z_a² ≤ B + K_0 n² B² 2^{−γm} ≤ 2K_0 n² max(B, B² 2^{−γm}). With probability ≥ 1/2 over P′ (Markov),
Σ_a z_a² ≤ 4K_0 n² max(B, B²2^{−γm}), and Cauchy–Schwarz gives #{a : z_a > 0} ≥ B²/Σ z_a² ≥ min(B, 2^{γm})/(4K_0n²).
As P′ < 2^{1+γm} and j′ is uniform: P(j′ hits | S, this P′-event) ≥ min(B 2^{−γm}, 1)/(8K_0 n²) ≥ B/(8K_0 n² C(σ,k)),
using B ≤ C(σ,k) and C(σ,k) ≥ 2^{γm} (S4).

*Step 5 (product).* F, P′, j′ are independent, so
P(key inserted) ≥ (1/(m+1)) · E_S[1{S good} · (1/2) · a_k(S; c^I)/(8K_0n²)] ≥ 2^{−g_M}/(32K_0 n²(m+1)(v+1)) ≥ 2^{−g_M}n^{−6}
for all n with 32K_0 n²(m+1)(v+1) ≤ n^6, together with the large-n conditions of Steps 3–4 (m ≥ 1; ⌊γm⌋ ≥ L_*;
(δ − 0.012311)n ≥ n^{0.6} + 1 + log(2(v+1))). None depends on I, s, P or M. ∎

Inputs: (5.1); the lists (c)–(g); Lemma A4's event and (5.3); (F2); (F4); Corollary D with (S1), (S3); (S4);
Lemma A3(4) with (LD); and the parameter inequality **1/2 − τ0 + ζ < δ**.

### 2.3 Comparison with Base (lines 489–535)

Base's proof has six steps; mine has the same six in a different order (Base's Step 5 is my Step 0). Line by line:
- Base Step 1 = my Step 1 verbatim (bijection, C(m,σ)2^{−m} ≥ 1/(m+1), conditional uniformity, F = S△(I∩M)).
- Base Step 2 = my Step 2: c^I defined identically; "These depend on I but not on S"; the same for b.
- Base Step 3 = my Step 3: Corollary D with (S1)–(S3); (F2); W_S and B_S as my w_j and B(S); "if S is good, (5.3)
  and Step 2 give B_S ≥ |Σ_k(S; c^I)|"; the subtraction of the bad fraction with "by Lemma A3(4),
  2^{−δn} ≤ 2^{−g_M}/(2(v+1)), because 1/2 − τ0 + ζ < 0.013 < δ". Same inequality, same constants.
- Base Step 4 = my Step 4: same bit length ηn + log n + 3, same K_0 n² 2^{−γm}, same second moment, same split at
  B_S ≤ 2^{γm}, same Markov factor 1/2, same Cauchy–Schwarz, same min(B_S, 2^{γm})/(4K_0n²), same hit probability
  min(B_S2^{−γm}, 1)/(8K_0n²) ≥ B_S/(8K_0n²C(σ,k)) with B_S ≤ C(σ,k) and (S4). Identical.
- Base Step 5 = my Step 0 (⇐ direction): same identity b(A) + b^F(X) + b(B) + b^F(Y) = T^F, same alias argument for
  the skipped interval, same expansion. Base does not state the ⇒ direction (not needed).
- Base Step 6 = my Step 5: same product 2^{−g_M}/(32K_0n²(m+1)(v+1)) ≥ 2^{−g_M}n^{−6}.

Findings (Part 2):
| # | Item | Class | Note |
| --- | --- | --- | --- |
| 2.1 | The inequality 1/2 − τ0 + ζ < δ (0.0123 < 0.0706) is a genuine parameter condition of the proof, not among (C1)–(C8) and not in the Arb script of §8.1; Base states it inline in Step 3 with the correct numbers. At a retuned parameter point it must be rechecked (at `paper.md`'s point it is 0.0124 < 0.0698). | cosmetic | add it to the constraint list |
| 2.2 | Base's threshold "for all large n" hides three explicit conditions (L′ = ⌊γm⌋ ≥ L_* for (F4); 32K_0 ≤ n²; (δ − 0.0123)n ≥ n^{0.6} + 1 + log(2(v+1))). All are absolute, as the lemma claims. | cosmetic | no change |
| 2.3 | Step 2's sentence "on S the signed weights equal c^I" is the whole signing argument; Base does not say explicitly that Corollary D's weights must be fixed before S is drawn (the reason c^I rather than c^F is needed), though the §3 Remark says it. | cosmetic | one clause |
| — | Unstated assumptions I looked for and found handled: F uniform over all 2^m subsets (Step 4(a)); the carry q ≤ n − 1 (b(I) ≤ n(P−1)); the class record's residue following from the integer identity; independence of (P′, j′) from S; badness defined via {−1,0,1}-combinations of the unsigned c_i, hence covering c^I; Corollary D's S being the conditional law of (I∩M)△F given |S| = σ. | — | none missing |

Constants: none differ. In particular Base's "δ > 0.0706" is correct at its parameters (η = 0.51613, μ = 0.473:
(μ/2)log 3 = 0.374844, δ = 0.070643).

---

## 3. The region analysis of Theorem B

### 3.1 Objects (Base §6.1–6.2, the paper §4)

J = 43 filters; for a pattern π and every filter l the rounded block averages D_{l,π}, A_{l,π}, E_{l,π} (each within
ε of the true averages; D ≥ 0, A, E ≤ D), U_{l,π} = A + E − D, W_{l,π} = 2D − A − E; v = v*(π) the least maximiser of
U_{l,π}; α_π = 1 if W_{v,π} ≤ Γ else Γ/W_{v,π}; sampled iff α_π U_{v,π} < Δ (else summed directly). Regions by
W = W_{v,π}: ρ_0: W ≤ Γ; ρ_i: Γb_{i−1} < W ≤ Γb_i (b_0 = 1, …, b_8 = 15, b_9 = ∞). Certificate for (v, ρ): z ≥ 0,
C ⊆ {0..42}∖{v}, rows G as in §6.1, and the condition z_0 ≥ 1 (ρ_0), z_0 b_{i−1} ≥ 1 (ρ_i), 15z_0 ≥ 1 (ρ_9);
Proposition B: ∫ M² 2^{z·G} < 2^{η−0.00025}; Lemma B1: the finite-circle average is < 2^{η−0.0002} for P ≥ P_0.
For a frequency k with coordinates x_i = x_i(k): ū_l, w̄_l the averages of u_l, w_l, and (6.1):
|U_{l,π} − ū_l| ≤ 3ε, |W_{l,π} − w̄_l| ≤ 4ε (three, resp. four, ε-accurate block averages).

### 3.2 Why there are regions, and what a certificate row buys (my reading)

The paper dominates −α_π U_π by one of two functions of the coordinate values: 8.5(Δ − u) when W_π ≤ Γ (α = 1,
U < Δ) and 8.3(a v − u) when W_π > Γ (then α a W = Δ, so −αU = −Δ + α(aW − U) ≤ −Δ + 8.3(aW − U) because
0 < aW − U and α ≤ 1 ≤ 8.3), and then replaces U, W by ū, w̄ at a fixed cost 30ε. Base keeps the split ρ_0 versus
ρ_1 ∪ … ∪ ρ_9, makes the multiplier a free z_0 subject only to z_0 ≥ α (which is what z_0 ≥ 1, z_0 b_{i−1} ≥ 1 say,
since α < 1/b_{i−1} in ρ_i), and adds nonnegative multiples of three kinds of rows that are nonnegative *on the
pattern* up to O(ε): Γ − W (in ρ_0), the band rows W − Γb_{i−1} and Γb_i − W (in ρ_i), and U_{v,π} − U_{l,π} for
other filters l (v maximises U). Each added row costs at most 6εz_t in the final slack, and the regions exist
precisely so that the band rows are available: the finer the bands, the more of the integrand's mass at
w(x) ∉ (Γb_{i−1}, Γb_i] can be suppressed by 2^{z_1(w−Γb_{i−1})+z_2(Γb_i−w)}. Base's §8.2 table shows which
regions bind: ρ_0 (margin 0.00025379) and ρ_1 (0.00036) are tight; ρ_2 has margin 4.2 and ρ_3, …, ρ_9 ≥ 10.6
(log₂ units), so at Base's point the eight upper bands are pure slack and the whole difficulty sits at W ≈ Γ.

### 3.3 Lemma B2 (domination), my proof (PROVED)

Let π be sampled, v = v*(π), U = U_{v,π}, W = W_{v,π}, Ḡ = (1/n)Σ_i G(x_i).
*ρ_0.* α = 1, U < Δ. Ḡ_0 = Δ − ū_v ≥ (Δ − U) − 3ε; Ḡ_1 = Γ − w̄_v ≥ (Γ − W) − 4ε ≥ −4ε; Ḡ_l = ū_v − ū_l ≥
(U_{v,π} − U_{l,π}) − 6ε ≥ −6ε. With z ≥ 0: z·Ḡ ≥ z_0(Δ − U) − 6εΣ_t z_t, so
−Δ + z·Ḡ + 6εΣz ≥ −Δ + z_0(Δ − U) ≥ −Δ + (Δ − U) = −U = −αU, using z_0 ≥ 1 and Δ − U > 0.
*ρ_i (1 ≤ i ≤ 8).* W > Γb_{i−1} ≥ Γ, so α = Γ/W < 1/b_{i−1} ≤ 1 and Δ = α a_Γ W; sampled means a_ΓW − U > 0 and
−αU = −Δ + α(a_ΓW − U). Rows: Ḡ_0 = a_Γw̄_v − ū_v ≥ (a_ΓW − U) − (4a_Γ + 3)ε; Ḡ_1 = w̄_v − Γb_{i−1} ≥ −4ε;
Ḡ_2 = Γb_i − w̄_v ≥ −4ε; Ḡ_l ≥ −6ε. So z·Ḡ ≥ z_0(a_ΓW − U) − 6εΣz **provided 4a_Γ + 3 ≤ 6, i.e. a_Γ ≤ 3/4**,
and then −Δ + z·Ḡ + 6εΣz ≥ −Δ + z_0(a_ΓW − U) ≥ −Δ + α(a_ΓW − U) = −αU because z_0 ≥ 1/b_{i−1} > α.
*ρ_9.* As ρ_i without the upper band row; α < 1/15 ≤ z_0. ∎
(The tie rule for v*(π) is irrelevant; only "v maximises U_{·,π}" is used. The band rows use the region of the
pattern value W_{v,π}, with the 4ε accuracy paying for the true average.) Check C3 (§5): on the explicit tight
instance the margin is exactly z_0ε(3 − 4a_Γ), positive at a_Γ = 0.0619, zero at 3/4, negative at 0.8.

### 3.4 From domination to the error bound (Lemma B3, Theorem B) — my derivation (PROVED given the paper's §4)

For a sampled π and a frequency k of pattern π, on the event G of Lemma 4.2(iii):
L_π|J_ρ(k)|² ≤ 2^{(η−αU+18ε)n} Π_i M(x_i)² ≤ 2^{(η−Δ+18ε+6εΣz)n} Π_i M(x_i)² 2^{z·G(x_i)}, by (4.11), (4.4) and
Lemma B2. The right side does not involve π or G. For fixed k the x_i(k) = φ_i + kb_i are independent uniform
residues, so its expectation is ≤ 2^{(η−Δ+18ε+6εΣz)n} 2^{(η−0.0002)n} (Lemma B1). Inserting into the conditional
mean-square error (1/N)(L_π/P²)Σ_{k: pattern π}|J_ρ(k)|² of the N-sample estimator and summing over k < P:
E[1_G|E_{π,ρ}|²] ≤ 2^{(2η−Δ+18ε+6εΣz−0.0002)n}/(NP) ≤ 2^{(18ε+6εΣz−0.0002)n+2} (N ≥ 2^{τ0 n}, P ≥ 2^{ηn−2},
η − Δ = τ0). With Σz ≤ 418.36: 18ε + 6εΣz ≤ 2.53·10⁻⁵, exponent ≤ −0.000174n + 2 ≤ −0.00017n + 2. Direct
patterns are exact on G with L_π ≤ 2^{(τ0+18ε)n} ≤ C_n. Cauchy–Schwarz over Q_n = 2^{O(√n)} patterns, Markov and
the union over ≤ n^d targets give error ≤ 1/16 with probability 1 − o(1), as in the paper's §4.4; §4.5 (caps,
precision, 2^{(τ0+20ε)n+O(√n)}poly time) is unchanged except that a pattern costs 3Jq block averages. ∎
What the family changes in Lemma 4.2 and why it is harmless: (i) coverage of k uses the tables of its own pattern,
built with the filter v*(π) whose block averages the pattern records; (ii)–(iii) use (4.5), (4.8)–(4.9) with the
chosen filter's values, the normalisation of f_{*,v}, g_{*,v} on the finite circle (Lemma B1) and the joint moment
E 2^{S_h+S_ℓ} = 1, all per pattern with one filter; Q_n stays 2^{O(√n)} because J is fixed; (6.1) holds for every l
because the pattern rounds every filter's averages.

### 3.5 Why J = 1 reduces the ten certificates to M₁ and M₂ (PROVED, algebraic)

With one filter C = ∅ and the rows are (Δ − u, Γ − w) in ρ_0, (a_Γw − u, w − Γb_{i−1}, Γb_i − w) in ρ_1..ρ_8 and
(a_Γw − u, w − 15Γ) in ρ_9. Choosing z = (p, 0) with p ≥ 1 in ρ_0 and z = (q, 0, 0) (or (q, 0)) with q ≥ 1 in every
ρ_i (then z_0b_{i−1} ≥ q ≥ 1 and 15z_0 ≥ 1 automatically; ρ_1 with b_0 = 1 is the binding case) makes the ten
inequalities of Proposition B the two inequalities
M₁ = ∫ M² 2^{p(Δ−u)} < 2^{η−0.00025}, M₂ = ∫ M² 2^{q(a_Γw−u)} < 2^{η−0.00025},
i.e. the paper's Proposition 3.1 with (p, q) in place of (8.5, 8.3) and with Base's margin and Base's (Δ, Γ, a_Γ).
This is a *sufficient* choice: the band multipliers may still be used with J = 1, so Base's format is at least as
strong as (M₁, M₂) for a single filter. Side conditions that survive the reduction: p ≥ 1 and q ≥ 1 (Lemma B2);
a_Γ ≤ 3/4 (the 6ε accounting); and B3's slack (18 + 6p)ε, (18 + 6q)ε must stay below the margin that B1 transfers
to the finite circle. The paper's own conditions 3p ≤ 30 and q(4a + 3) ≤ 30 are the same accounting with a fixed
30ε in place of 6εΣz; with a_Γ = 0.0619 and p, q ≈ 8.3–8.5 both versions hold.

### 3.6 Comparison with Base (lines 655–761)

- Lemma B1 (655–659): Riemann-sum transfer from (F7) with the slack 0.00025 → 0.0002; P_0 absolute because there are
  finitely many pairs. Same as my reading; nothing to add.
- Lemma B2 (699–718): identical structure (G^π rows nonnegative for t ≥ 1 by the region and the maximality of v;
  z·Ḡ ≥ z_0G^π_0 − 6εΣz; then the two cases with z_0 ≥ 1 and z_0 ≥ 1/b_{i−1} > α). One sentence differs from
  what is true: "Each row is affine in at most two of these quantities, with coefficients of absolute value at most 1
  (a_Γ < 1). By (6.1), |Ḡ_t − G^π_t| ≤ 6ε for every row" — coefficients ≤ 1 only give 4ε + 3ε = 7ε for a row in both
  u and w, so the sentence does not prove 6ε; the next sentence's detailed list (3ε, 4ε, 6ε, (4a_Γ+3)ε, 4ε, 4ε) does,
  and it needs a_Γ ≤ 3/4, which holds (0.0619) but is not stated as a condition anywhere.
- Lemma B3 (722–734): identical to §3.4 (c_z = 6Σz ≤ 2511, (18 + c_z)ε < 2.6·10⁻⁵, 2^{−0.00017n+2}; references
  (4.11), (4.4), (4.20), (4.25)).
- Theorem B (746–761): a delegation to the paper's §4 with the three listed changes; the three bullets cover exactly
  the points in my §3.4; the pattern cost "3Jq approximate block averages" is noted.

Findings (Part 3):
| # | Item | Class | Note |
| --- | --- | --- | --- |
| 3.1 | Lemma B2's justification "coefficients of absolute value at most 1 ⟹ 6ε per row" is false in general (it gives 7ε); the detailed error list beneath it is correct and requires a_Γ ≤ 3/4, an unstated assumption. | **repairable** | replace the sentence by "row 0 in ρ_i has error (4a_Γ + 3)ε ≤ 6ε since a_Γ ≤ 3/4; all other rows ≤ 6ε", and add a_Γ ≤ 3/4 to the checked constraints (slack 0.69) |
| 3.2 | Proposition B's margin 0.00025 is met in ρ_0 by only 3.8·10⁻⁶ (least margin 0.00025379, filter 28); Lemma B1 then needs the finite-circle loss below 0.00005, which (F7) gives only "for P ≥ P_0" with P_0 unspecified. The algorithm's P has ≈ ηn bits, so this is fine for large n, but the proof's n-threshold is not effective. | cosmetic | same status as the paper's own Lemma 3.2 |
| 3.3 | Theorem B's proof is by reference ("the paper's proof applies with these changes"); the three bullets are the right three places, and I found no fourth. The sentence "Lemma 4.2 holds for this construction with U_π := U_{v*(π),π}" at line 684 carries the whole weight; the justification given (parts (ii)–(iii) use only (4.5), (4.8), (4.9), the normalisation and (4.14)) is correct. | cosmetic | no change |
| 3.4 | The J = 1 reduction (`paper.md` §8's "Observation") is correct as a sufficient certificate; it should be stated as "implied by M₁, M₂ (p, q ≥ 1)", not "exactly M₁ and M₂", since the band and filter rows are dropped, not shown to be useless. | cosmetic | wording in `paper.md` |
| 3.5 | Base's regions ρ_2..ρ_9 contribute nothing at Base's point (margins ≥ 4.2); the construction would be unchanged with three regions (W ≤ Γ, Γ < W ≤ 1.25Γ, W > 1.25Γ). A design remark, not a gap. | cosmetic | none |

Constants compared: 6εΣz (Base) versus 30ε (the paper): Base's is the sharper, parametric version; both are
consistent. 2.6·10⁻⁵ (Base) versus my 2.53·10⁻⁵: same bound. −0.00017n + 2: same. No constant differs.

---

## 4. What I did not re-derive (scope boundary)

Lemmas A1–A4, A6–A7 and Theorem A's cost accounting (§5.7), Proposition B's 430 numerical inequalities (certified
in my round-3 report), the paper's §4 (used as a black box through (4.4), (4.5), (4.8)–(4.9), (4.11), (4.14),
(4.19)–(4.21), (4.25)), and (F3)–(F7). Lemma A5 depends on A3(4) and A4, whose proofs I read for the comparison
only; both looked correct on reading (A4: 3^σ ≤ 2^{(μ/2)log3·n}, (F4), Markov, the guard) but were not re-derived.

## 5. The computational checks (EVIDENCE; `scripts/round6/core_checks.py`, 10 s; outcomes in `PREREG_R6.md`)

| Check | Result |
| --- | --- |
| C1 Lemmas 3.1, 3.2, 3.3, Corollary D, (F2) by exact enumeration on random small weight multisets (signs and repeats) | 763 + 763 + 30 + 462 cases, 0 failures; equalities in 3.1/3.2 only on generic instances; Corollary D's smallest ratio 2.40 (never tight here; pre-registered "tight within a factor 2 somewhere" not met); the control (3.1 with t, k swapped) fails 66 times, as it must |
| C2 One trial of §5.2 (c)–(g) implemented literally (n = 8, m = 4, k = 1, σ = 2) versus the Step-0 "iff" | 8,273 (trial, target) pairs: exact agreement; 4,207 inserted keys, all alias classes (Lemma A1); the control without the skipped interval inserts 1,256 exact-sum classes |
| C3 Lemma B2 | random patterns: 0 failures but margins ≥ 0.47 (not informative); the pre-registered control was ill-posed (a_Γ is not free: α a_Γ W = Δ forces a_Γ = Δ/Γ) and was replaced by the explicit tight instance ρ_3, W = Γb_2(1+10⁻¹³), U = a_ΓW − 10⁻¹³, z = (1/b_2, 0, 0), worst-sign errors: margin = z_0ε(3 − 4a_Γ) exactly (1.72·10⁻⁸ at Base's point; 0 at a_Γ = 3/4; −1.25·10⁻⁹ at 0.8; −3.75·10⁻⁹ at 0.9) |
| C4 The paper's M₁, M₂ with its own filter (float) | log₂ M₁ = 0.51497, log₂ M₂ = 0.51485 < 0.5168; D ≥ 0.068, D − A ≥ 0.115, D − E ≥ 0.110 |

## 6. Labels

PROVED (own proofs, §1–§3): Lemmas 3.1–3.3, Corollary D; Lemma A5 with the Step-0 characterisation; Lemma B2;
Lemma B3 and the reduction of Theorem B to the paper's §4 given Lemma B1 and Proposition B; the J = 1 reduction.
EVIDENCE: the four checks of §5. CONJECTURE: none. NOT VERIFIED: the commit hash; Proposition B's 430 inequalities
and Lemma B1's P_0 (outside scope); A3, A4, A6, A7.
