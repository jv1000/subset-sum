# Comparison addendum to the frozen independent proofs

**PROVED — Mathematical verdict: PASS WITH REPAIRS for the requested core, with the inherited paper lemmas taken as named inputs. No fatal mathematical gap was found in Lemmas 3.1–3.3, Corollary D, A5, or the B2 region implication.**

**EVIDENCE — Blindness verdict: qualified.** The initial locator search exposed Corollary D's case split and isolated proof lines before the independent draft. A later definitions read exposed A4's bad-set argument. These are itemized in REGISTER.md and at the start of the frozen proof file. The A5 draft established a polynomial success bound but left the precise n^−6 exponent unfinished before comparison. The exact constant calculation below was completed AFTER reading Base. Thus this deliverable does not claim to satisfy the strongest possible fully blind protocol. The sampling-law, fixed-signing, witness-counting, and B2 region derivations were written before their full proof bodies were read. The preserved draft has not been rewritten to conceal this chronology.

## Completing A5 with explicit constants

PROVED — The frozen draft used the signing (−1)^[i∈I]c_i, whereas Base:498 uses its global negative. On S, the draft's trial weights were the negative of its fixed signing; Base's trial weights equal its fixed signing. Global negation bijects every layer's values, so the layer cardinalities, deficiencies and all inequalities are identical. This is a differing convention, not a flaw.

PROVED — Set H=2^(γm), B=C(σ,k), and B_S equal to the number of distinct left b keys. For any fixed good S, the second moment of residue occupancies satisfies E sum_y z_y²≤B_S+K0n²B_S²/H. By Markov, with probability at least one half it is at most 4K0n² max(B_S,B_S²/H). By Cauchy, the occupied residue count is at least min(B_S,H)/(4K0n²). As P′<2H, the hit probability is at least min(B_S/H,1)/(8K0n²)≥B_S/(8K0n²B). Here the final inequality uses BOTH B_S≤B and B≥H. This provides the explicit polynomial omitted from the first draft. All constants are uniform because η,γ,μ are fixed and differences of b sums have O(n) bits; the original input bit length is absent from this second prime step.

PROVED — Corollary D and the bad-set deletion give E[1_good B_S/B]≥2^(−g_M)/[2(v+1)]. Multiply by 1/(m+1), by the one-half probability of the occupancy bound, and by 1/(8K0n²). The resulting lower bound is

    2^(−g_M) / [32 K0 n²(m+1)(v+1)].

PROVED — Since m,v≤n and (n+1)²≤4n² for n≥1, this is at least 2^(−g_M)/(128K0n^4), hence at least 2^(−g_M)n^−6 whenever n²≥128K0. This exhibits an explicit sufficient asymptotic cutoff for that step. The cutoff is independent of the alias, target, prime and block. Bounded samplers may instead fail; their exponentially small abort event is handled separately. The recovery identity in the frozen proof establishes that each occupied representation reaches the alias's class. All of these probability assertions are for the uncapped ideal execution.

PROVED — Bad-set deletion has two distinct requirements. First the A4 bad-fraction event must itself occur with probability 1−o(1), which requires δ>1/guard. Second its deleted mass 2^(−δn) must be small relative to 2^(−g_M)/(v+1), which requires δ>1/2−τ0+ζ, including room for n^0.6 and log(v+1). Both hold for the supplied Base constants. The independent interval calculations are in BASE_CORE_CONSTANTS.json, produced by base_core_constants.py. This distinguishes loss of prime-event probability from loss of useful layer mass.

## Line-by-line audit of the requested Base passages

EVIDENCE — The table covers each substantive line group in the named proofs; table rows describing agreement are labeled PROVED because the frozen derivation or the explicit completion above supplies the argument. “None” means no gap found in that line group, not a statement that the entire surrounding paper was audited.

| Status | Base lines | Comparison | Severity |
|---|---|---|---|
| PROVED | 230–231 | Correct covering statement for legal sizes, including boundary cases. | none |
| PROVED | 233–235 | Same witness choice and injective map as the independent counting proof. The injectivity relies on recovering x from W and the residual sum, not on weights being distinct. | none |
| PROVED | 236–238 | Same incidence count and binomial normalization. | none |
| PROVED | 240–245 | Same representative inclusion probability; all included sums are distinct. | none |
| PROVED | 247–252 | Union bound on layers, then complement symmetry, then C(N,t)≤2^N. | none |
| PROVED | 254–259 | Need legal nonnegative sizes; “integers” alone is too broad if read literally. Binomial/subset notation convention normally supplies this. | cosmetic |
| PROVED | 262–265 | Averaging over W then S′ produces a uniform σ-set in V by permutation symmetry. σ≤v−t+k is exactly the necessary room. | none |
| PROVED | 267–269 | This is precisely the use of C(σ,k)C(v,k)≤2^v. It is not dispensable from THIS proof. For t<k, k≤v/2 guarantees C(v,t)≤C(v,k). | none |
| PROVED | 271–275 | Nested uniform sampling has the correct marginal. Fixed signing must precede the random S; d is sign invariant but a_k need not be. | none |
| PROVED | 486–490 | The success statement should say “uncapped ideal execution,” or explicitly condition on completion of the trial. A prior cap stop otherwise invalidates a literal guarantee. | repairable |
| PROVED | 492–494 | S is uniform in the whole power set, not initially uniform in the middle layer. Conditioning on its size gives uniformity; probability ≥1/(m+1). | none |
| PROVED | 496–499 | Correct signing independent of S. The independent draft's opposite convention is equivalent. | cosmetic convention only |
| PROVED | 501–503 | The stated S1–S3 meet D's hypotheses; g_M is the negative log of the average, not E d(V). | none |
| PROVED | 504–507 | Distinct c sums inject into distinct b sums only on a good S; bounded density allows deletion of bad S at its probability cost. The margin against δ is positive independently of the cited rounded values. | none |
| PROVED | 509–511 | W_S can depend on P and I; it must not depend on P′ or j′. The bit-size bound is O(n) and uniform. | none |
| PROVED | 512–515 | Diagonal occupancy contribution B_S, off-diagonal collision contribution, two cases, then Markov at factor two. Correct. | none |
| PROVED | 516–520 | Cauchy, P′<2H, and BOTH bounds B_S≤B, H≤B give the displayed hit probability. | none |
| PROVED | 522–530 | A matching residue produces complementary Y; carry identity places its class in the integer match group. Alias status ensures it is not in the exact-solution interval. | none |
| PROVED | 532–535 | Product denominator 32K0n²(m+1)(v+1) is correct. The n^−6 weakening has a uniform large-n cutoff as explicitly derived above. | none |
| PROVED | 537–543 | Independence is across trials conditional on fixed P,M,L and Step 3. exp(−n) times poly(n)2^n tends to zero because log_e 2<1. There is no missing extra union over carries. | none, apart from uncapped wording |
| PROVED | 629–643 | Region endpoints, nonnegative multipliers and z0 conditions provide valid affine certificates. The last region has one less row. | none |
| PROVED | 667–675 | The full pattern grid is deterministic. Selecting the best filter is deterministic for each pattern, so no table randomness is conditioned on observed phase outcomes. | none |
| PROVED | 691–694 | Error 3ε for U and 4ε for W follows by summing coordinate errors with their absolute coefficients. | none |
| PROVED | 700–704 | “a_Γ<1” alone is insufficient to conclude every row error≤6ε; the Aw−u row costs (4a_Γ+3)ε. Need a_Γ≤3/4, which both original and frozen ternary constants satisfy. | repairable reasoning shorthand |
| PROVED | 705–708 | Endpoint rows are nonnegative by region membership; choice rows by maximizing U. Nonnegative z permits discarding all but the first row. | none |
| PROVED | 710–711 | Low region: Δ−U>0 and z0≥1. | none |
| PROVED | 713–715 | High region: α=Γ/W<1/b_{i−1}≤z0 and αa_ΓW=Δ. Positivity comes from sampling, not from the entropy-order inequalities alone. | none |
| PROVED | 717 | Combine pattern domination and rounding error exactly as in the independent proof. | none |
| PROVED | 723–725 | Match exponent contributes 18ε; certificate rounding contributes 6εΣz. | none |
| PROVED | 726–728 | Remove the good-event/pattern indicators by a nonnegative pointwise majorant BEFORE using independent original phases. Independence under conditioning is not assumed. | none |
| PROVED | 729–733 | Sum P frequencies, divide by NP, use η−Δ−τ0=0. The claimed Base decay is conservative; independently checked. | none |
| PROVED | 747–753 | Transfer of the table argument requires independent phases and own random draws, exactly as stated. | none |
| PROVED | 754–758 | Cauchy across Q_n patterns gives Q_n² times the per-pattern bound; polynomial target union costs only subexponential factors. | none |
| PROVED | 759–760 | Fixed J makes pattern-description overhead 2^{O(sqrt n)}; precision estimate is inherited from the original paper. | none in region implication |

## Region rows, epsilon costs, and the two-moment specialization

PROVED — In the low region the rows are (Δ−u_v, Γ−w_v, (u_v−u_l)_l), with respective error bounds (3,4,6)ε. In an intermediate region they are (A w_v−u_v, w_v−Γb_low, Γb_high−w_v, (u_v−u_l)_l), with errors (4A+3,4,4,6)ε. The last region removes the upper endpoint row. Each comparison error is the sum of two 3ε errors. A≤3/4 is the common sufficient row restriction.

PROVED — With one filter, use z=(p,0) in the first region, z=(q,0,0) in intermediate regions and z=(q,0) in the last. p,q≥1 meet every z0 condition since b_low≥1. The low exponent is p(Δ−u); every high exponent is q(Aw−u). The ten regions therefore use two actual integrands. The frozen blind draft used the special case p=q=1 to demonstrate the reduction; the general multipliers preserve the proof and can greatly improve the moments.

PROVED — Let δ_m=η−ρ_f. For one sampled pattern, after averaging original phases,

    E[1_good |error|²] ≤ 2^{−[δ_m−18ε−6εΣz]n+O(1)}.

PROVED — This follows directly from the conditional variance, the pointwise certificate bound, and product factorization for each fixed frequency. Directly summed patterns have zero ideal error on the good event. Fixed polynomially many targets and 2^{O(sqrt n)} patterns can be union-bounded against any fixed positive decay. No independence between frequencies, patterns, or target errors is needed. At J=1, Σz is p or q.

PROVED — The original table argument itself does not require even filters: tilting a non-star label by K_x gives the three means αA,αE,αD (C:232–258). For the expected pair count, integrate the uniform phase to remove f_*, then the uniform label to remove g_* (C:287–304). Every pattern is included before testing whether a frequency belongs to it. This explains why fixed sine harmonics and deterministic patternwise filter choice preserve the identities.

## Boundaries of this review and retained dead ends

EVIDENCE — The initial attempt to locate statement boundaries with a broad text search was a procedural dead end for pristine blindness: it displayed proof fragments. The exact exposure is preserved rather than erased. A safer protocol would extract theorem text using a parser that suppresses proof bodies before displaying any matches.

EVIDENCE — The frozen A5 reconstruction first used an expectation/Jensen occupied-residue argument. It proves the right inverse-polynomial form, but did not at that stage track the explicit n^−6. The comparison completed the constant accounting using the occupancy second moment. Both versions are retained; neither is claimed to have proved the precise constant before it was written.

PROVED — The attempted generic justification “two coefficients each ≤1 imply error≤6ε” fails for a row combining errors 3ε and 4ε. Its corrected sufficient condition is A≤3/4. This is a real logical repair with no change to either frozen point.

NOT CHECKED — This report does not re-prove the entire original paper's isolation lemma, implementation/address-space analysis, or all of Base's numerical family certificates. It proves and compares the requested probabilistic core and identifies the inherited premises. It also does not prove [S] or any layer-density monotonicity conjecture.

PROVED — Recommended human checks: the uncapped/capped coupling wording, uniformity of the fixed-signing application, correct use of original phase law in the second-moment domination, and the input-bit-length quantifiers when announcing the final exponent. The computations relevant to the ternary candidate and the local Base constants have independently checkable scripts and logs.
