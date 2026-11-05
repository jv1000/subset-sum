# Fresh referee of Section T — Astra, round 6

**PROVED — Verdict: PASS WITH REPAIRS, conditional on [S] and the inherited Base/OpenAI results, in Base's stated word-RAM model and for each fixed polynomial bound on input bit length.** The frozen decimal point supports every exponent **T′ > 0.4873407528**. This is an exact threshold expression, not a downward-rounded exponent. The unqualified claim for arbitrary bit length does not follow: Base explicitly restricts its exponential-time conclusion to b≤n^c (Base:58–66, 806–810). Restoring that qualification is a repair to the statement, not a numerical change.

**NOT CHECKED — [S] itself is not proved here.** Nor is the supplied commit identifier authenticated against Git. Base's other inherited theorems remain premises where explicitly identified below; this is not a new unconditional Subset Sum theorem.

## Scope, sources and independence

EVIDENCE — Only the supplied A folder was used before this report and BASE_CORE_ASTRA.md were completed. Source abbreviations: T = SECTION_T_v2.md; Base = base_PROOF_0.4877.tex; F = openai_tex/sections/filtering.tex; C = openai_tex/sections/checksum.tex. Line numbers refer to these supplied files. ROUND2_REPORT.md was used for the statements of R and S at 53–62, not as evidence for them. Existing certificate scripts and Base's code appendix were not used. The numerical code in verify_a.py is newly written.

EVIDENCE — BLIND_BASE_CORE.md records the independent probabilistic derivation before the full Base proof bodies were read. REGISTER.md discloses accidental earlier proof-fragment exposure. The blind exercise is therefore qualified, not represented as pristine.

## Complete condition inventory derived from costs and probabilities

PROVED — Set t=τ0, r=1−μ−l, a′=a+c, H=H3(a,c), y=1/2−a+c, Δ=η−t, Γ=2t−η, A=Δ/Γ, and Gd=10^8. Parameters are fixed rationals; ε,ζ>0. The following is a sufficient list for this implementation. Domain inequalities are listed separately from cost inequalities so that no implicit parameter restriction is hidden. Conditions at equality that are intrinsically non-strict need not be made strict in general; the frozen point is interior.

| Status | Requirement | Derivation and source lines |
|---|---|---|
| PROVED | 0<μ≤1/2, 0<l, r>0, a,c≥0, a,c≤1/2, a+c≤1, 0≤y≤1, γ>0 | Partition, feasible disjoint masks, valid right layer and exponential small-prime scale; T:15–19, 44–52; Base:334–359 |
| PROVED | γ < [h(2a)+h(2c)]/2 | Central split representation count B=C(m/2,k1)C(m/2,k2)≥2^(γm) for all large m; floors and Stirling cost O(log m); T:100–110; Base:511–520 |
| PROVED | l+(H−γ)μ<t | Left records after deficiency cancellation; T:134–135; Base:565–567 |
| PROVED | r+(1−γ)μ<t | Right classes times trials; T:136–137; Base:568–570 |
| PROVED | 1−μ+(H+h(y)−γ)μ−η<t | Expanded tuples, including rejected overlap tests; T:138–141; Base:571–584 |
| PROVED | μH+1/2−t<t and μh(y)+1/2−t<t | BOTH mask enumerations repeated through all trials; T:130–131; Base:558–560 |
| PROVED | l<t and r<t | Initial value maps, T:129; Base:556–557 |
| PROVED | μ<l | Concentration compares d(M) with d(L), T:67–73; also implies μ<t for the exact merge |
| PROVED | μ≤1/2 | LD bound on d(M), T:72–73 |
| PROVED | 2a′≤1/2 and η−μ[h(2a′)+2a′]>1/Gd | Count sparse signed relations and absorb input bit length, T:77–86; Base:210–212 |
| PROVED | a′≤0.11 and [S] holds for every signing with ONE uniform polynomial upper bound C_S(m) | Fixed-alias signing followed by witness averaging, T:88–106 |
| PROVED | h(a′)≤1/2 | Needed only for deriving [S] from weak monotonicity via Lemma S; not a separate premise if [S] is assumed directly |
| PROVED | 1/2−t+γμ/2<t | Repeated trial-division cost; T:132; Base:561–562 |
| PROVED | r+1/2−t<t | Repeated sorting of right keys; T:133; Base:563–564 |
| PROVED | ε0>1/Gd+ζ | All alias-work exponents have adequate slack; cap Markov bound, T:125–150; Base:601–605 |
| PROVED | t<1/2 and ζ>0 | Preliminary search threshold is separated from its cap; Base:281–297 |
| PROVED | η/2<t+20ε | Initial large-prime trial division, Base:801–803 |
| PROVED | Δ>0, Γ>0 | Valid checksum digits and α; Base:1078–1083; C:109–133, 163–195 |
| PROVED | κ>0; fixed real trigonometric polynomials, finite harmonics | Positive densities and uniform computability, F:113–175 |
| PROVED | A≤3/4 | Row error (4A+3)ε≤6ε, Base:700–703 |
| PROVED | p≥1, q≥1 | Domination in low and ALL high regions; Base:638–640, 710–715 |
| PROVED | log2 M1, log2 M2<ρ_c<ρ_f | Strict continuous-to-finite transfer, Base:651–659; F:144–155 |
| PROVED | ρ_f+(18+6p)ε<η and ρ_f+(18+6q)ε<η | Positive variance decay after phase averaging, Base:723–733 |
| PROVED | Fixed polynomially many targets; phases independent uniform and independent of table/sample draws | Base:737–745, 750–760; C:287–304 |
| PROVED | Fixed polynomial b≤n^c for the pure O(2^(T′n)) conclusion | Base:58–66, 806–810; otherwise retain model/bit-length dependence and fallback cost |

PROVED — For the stated ε0 bound, the two explicitly added work inequalities must have sufficient slack too. verify_a.py checks the stronger versions with ζ already subtracted and still more than ε0. The exact merge has slack t−μ, which exceeds ε0 here. The sparse-relation guard condition follows from the stronger common ε0 condition, but is checked independently as a control. Thus these are missing explicit checks in the parameter table, not obstructions at the candidate.

PROVED — The domain facts also imply γ<1 via C1R, and μ< t via μ<l<t. No Base S1–S4, C7, C8, v-set sampling, or old bad-half-set δ is required for the ternary coverage argument. Original Base's Corollary D is not a premise of T5; [S]+R replaces it.

## Lemmas T1–T7 and A′

PROVED — T1 (T:57–62): the tests X+∩Y=∅ and X−⊆Y make the signed sum exactly the sum of (X+∪Y)\X−. Symmetric difference with F gives the intended c and b sums. The integer b match fixes a carry; exclusion of the exact c interval excludes true solutions. The key classes partition subsets and their phase contributions factor (Base:391–396). No overcount occurs because the dictionary deduplicates classes.

PROVED — T2 (T:64–65): for a fixed c(A), b(A) has at most n+1 possible values because b(A)=c(A)−P times an integer and 0≤b(A)<nP. On M, c^F(Y)=c(Y△F)−c(F); for fixed c^F(Y), the signed b sum lies between −mP and mP and is congruent modulo P, giving at most 2m+1 possibilities. This is independent of the cardinality of Y. The right-class bound survives ternary left masks unchanged.

PROVED — T3 (T:67–75): M and L have uniform marginals even though disjoint. Exchange-Lipschitz concentration applies to both; no independence between their deficiencies is needed. Monotonicity of the mean deficiency and μ<l yield d(M)−d(L)≤2n^0.6. μ≤1/2 and LD give d(M)≤(1/2−t+ζ)n+n^0.6. The event depends only on the partition, so later averaging over P remains legitimate.

PROVED — T4 (T:77–86): a difference of two k′-subset sums under ONE fixed signing has coefficients in {−1,0,1} and support at most 2k′. There are at most sum_{j≤2k′} C(m,j)2^j such vectors. Entropy and monotonicity on 2a′≤1/2 give exponent μ[h(2a′)+2a′]. F4 supplies poly(n)(b+log n)2^(−ηn) per nonzero relation; the guard consumes 1/Gd in the exponent. The event is simultaneous over all signings and all aliases. One does NOT compare unrelated ternary masks with arbitrary coefficient differences ±2 here: coverage uses the fixed signing c^I on U. Such ±2 coefficients may occur in work accounting, where the general integer collision bound still applies.

PROVED — T5 (T:88–118): fix the alias AFTER conditioning on P,M,L. F remains uniform and independent. S=(I∩M)△F is uniform in the power set; the half-layer event has probability C(m,m/2)2^(−m)≥1/(m+1). On S use c^I=+c on I and −c off I; off S the trial signing is −c^I. Thus subtracting the outside mask cancels this second sign flip. Every U with |U∩S|=k1, |U\S|=k2 supplies a valid representation with Y=(S\X+)∪X−. R followed by [S] supplies E B_S/B≥2^(−d(M))/C_S, where B=C(σ,k1)C(σ,k2). T4 ensures this many distinct integer b keys.

PROVED — T5 step 4 in full: the key set W_S lies in (−nP,nP), hence its differences have O(n) bits. It is fixed before drawing P′ and j′. With z_j the residue occupancies, F4 gives E sum z_j²≤B_S+K0 n² B_S²2^(−γm), for an absolute fixed K0≥1. In the cases B_S≤2^(γm) and B_S>2^(γm), Markov gives, with probability ≥1/2, sum z_j²≤4K0 n² max(B_S,B_S²2^(−γm)). Cauchy then yields at least min(B_S,2^(γm))/(4K0 n²) occupied residues. Since P′<2^(1+γm), a random residue hits with probability at least min(B_S2^(−γm),1)/(8K0n²). Finally B_S≤B and B≥2^(γm) imply this is ≥B_S/(8K0n²B). These are the ONLY properties of the binomial denominator used in Base:511–520. Replacing it with the product is valid.

PROVED — T5 recovery follows from the exact identities in T:112–116; alias status ensures the c interval is not skipped. Combining the half-layer probability, the half-probability prime event, and the averaged key fraction gives ≥2^(−d(M))/[16K0 n²(m+1)C_S]≥2^(−d(M))/(C_S n^6) for all sufficiently large n. Interpret this in the hypothetical uncapped run. Actual cap failure is charged separately in A′.

PROVED — T6 (T:120–123): choose an integer polynomial majorant Cbar_S≥max(1,C_S), and use T=ceil(Cbar_S n^8 ceil(2^m/|Σ(M)|)). This avoids computing a logarithm and makes the loop count unambiguous. Then Tp≥n², so failure per alias is ≤exp(−n²). The union over polynomially many targets and at most 2^n aliases is o(1). C_S cancels; the bound is uniform over aliases and carries. No extra factor for carries is needed because each target/subset pair has a unique carry. The inequality exp(−n²)≤exp(−n) is true but wastes most of the slack.

PROVED — T7 (T:125–142): count uncapped elementary steps, conditioned only on the partition event. Initial lists cost 2^(ln), 2^(rn), and 2^(m−d(M))poly(n). Mask listing, prime draws and key sorting have the exponents in the inventory. Left records cancel d(L) against d(M) up to 2n^0.6; right classes cancel d(M) exactly up to polynomial factors. Visits must count ALL expanded members, including those failing the disjointness/subset test. Fix unreduced values x_L,x_R and masks before P, with D=x_L+c^F(X+)−c^F(X−)+x_R+c^F(Y)−t^F. A visited tuple requires nonzero D divisible by P; for each P there are only polynomially many keys sharing each unreduced value. Averaging over j′ supplies at most 1/P′. Averaging over P then supplies the F4 factor, without conditioning on T4. This resolves the apparent P-dependence of keys. The resulting C4R exponent pays for every expanded member. Sorting, matching and dictionary maintenance add polynomial factors.

PROVED — A′ (T:144–155): combine partition failure, T4 failure, coverage failure and cap failure by a union bound. Do not condition the expected-work bound on T4. With b+2≤2^(n/Gd+1) and ε0>1/Gd+ζ, Markov makes the cap probability o(1). Bounded sampler errors are exp(−Ω(n²)) or smaller times an exponential number of draws. Phase accuracy is inherited from Base:608–612. The modified checksum has variance margin as certified below. Base's isolation/subtraction assembly (781–794) then applies. The polynomial bit-length restriction is essential when absorbing poly(n+b) into a strictly larger exponent.

## R, S, and the one-filter checksum

PROVED — R: for every distinct k′-sum choose ONE witness K_y. A random half set S admits it with probability π=C(k′,k1)C(m−k′,σ−k1)/C(m,σ). Included witnesses have different sums. Therefore E distinct admitted sums≥|Σ_k′(M)|π. Double-count pairs (S,U) with |U|=k′ and |U∩S|=k1: C(m,k′)π=C(σ,k1)C(σ,k2). Division proves R. Repeated weights, negative weights and arbitrary fixed signs cause no change.

PROVED — S: assume a_t≤P(m)a_k for k≤t≤m−k. The union of layers gives 2^(−d)≤E_{T~Bin(m,1/2)}a_T≤P(m)a_k+Pr(T<k or T>m−k). With α=k/m≤1/2, the tail is ≤2·2^(−m(1−h(α))). Also a_k≥1/C(m,k)≥2^(−mh(α)). When h(α)≤1/2 the tail is at most 2a_k. Hence a_k≥2^(−d)/(P(m)+2). At k=0 the outside tail is empty. Apply this separately to every signing. No monotonicity conjecture is being proved here; only the implication is proved. The wording of M′ differs between T:185 and ROUND2:129–131, but the weak polynomial hypothesis suffices in either case.

PROVED — With J=1, comparisons between filters disappear. Region ρ0 has z=(p,0), and each bounded upper region has z=(q,0,0). The unbounded last region has the TWO-entry vector (q,0), not a three-entry vector. Their exponent functions are p(Δ−u) and q(Aw−u). Since each high-region b_{i−1}≥1, q≥1 satisfies z0 b_{i−1}≥1. This yields exactly M1=∫(2+2cos x)2^{p(Δ−u)} and M2=∫(2+2cos x)2^{q(Aw−u)}. Sines need no symmetry argument: F:133–175 uses bounded smooth functions and positivity, and the normalization/joint-moment arguments C:272–304 use uniform shifts and independent phases, not evenness.

PROVED — The rounding errors are 3ε for u, 4ε for w, 6ε for a filter comparison, and (4A+3)ε for Aw−u. Thus A≤3/4 makes every row error ≤6ε. Multipliers p,q lead to costs 6pε and 6qε. After the 18ε table-count allowance, the per-pattern variance decays at rates η−ρ_f−(18+6p)ε and η−ρ_f−(18+6q)ε. Both are positive. These replace Base's fixed decimal B3 decay rate; it must not be copied literally.

## Independent interval certificate and quadrature proof

PROVED — The exact decimal JSON is parsed into directed intervals at 50 decimal digits. verify_a.py implements its own radix-two interval FFT; it does not call a supplied certifier or a floating FFT. It forms real trigonometric samples through an interval inverse transform and checks correlation orientation against an asymmetric exact integer control. Arithmetic-library correctness is a dependency, as with any ball certificate; this is not a formally verified implementation of mpmath itself.

PROVED — Define F=2^r, G=2^s, C(x)=∫F(x+w)G(w), H(x)=∫F(x+w)G(w)(r(x+w)+s(w)), and K=log2∫2^(κr)+log2∫2^(κs), with normalized circle measure. Direct cancellation of normalizers in the definitions gives

    D = H/C − log2 C,
    u = (κ−1)H/C + log2 C − K,
    w = (2−κ)H/C − 2log2 C + K.

PROVED — These identities avoid separately subtracting several noisy normalizers. Discrete correlations give C and H on the grid. For any 2π-periodic analytic function bounded by B on |Im z|≤s, the normalized N-point trapezoid error is at most 2B/(exp(sN)−1): shift the contour of each Fourier coefficient to bound it by B exp(−s|j|), then sum coefficients at nonzero multiples of N. This supplies a genuine truncation bound, not a grid-stability assumption.

PROVED — Here is the complete strip argument used by the code. Write R_j=|r_cos,j|+|r_sin,j| and similarly S_j. Let R=sum R_j, S=sum S_j, R_s=sum R_j cosh(js), A_s=sum R_j(cosh(js)−1), B_s=sum R_j sinh(js), θ=(ln 2)B_s. For z=x+iy, |y|≤s, the real part of r(z+w) differs from r(x+w) by at most A_s and its imaginary part has magnitude at most B_s. Consequently C(z) lies in the sector |arg C|≤θ and

    2^(−A_s) cos θ · C(x) ≤ |C(z)| ≤ 2^(A_s) C(x).

PROVED — The code certifies θ<π/2. Thus the principal log is analytic throughout this strip, and periodic, because the sector is in the right half-plane. Also 2^(−R−S)≤C(x)≤2^(R+S). It follows that

    |H/C| ≤ 2^(2A_s)(R_s+S)/cos θ = H_b,
    |log2 C| ≤ R+S+A_s−log2 cos θ+B_s = L_b,
    |K| ≤ κ(R+S) = K_b.

PROVED — Hence U_b=|κ−1|H_b+L_b+K_b bounds |u|, and W_b=|2−κ|H_b+2L_b+K_b bounds |w|. The outer integrands are bounded by (2+2cosh s) times 2^[p(Δ+U_b)] and 2^[q(AW_b+U_b)]. The script applies the trapezoid bound to each with s=0.04. For real outer nodes, use inner strip s_i=0.1: C-integrand bound is 2^(R_si+S_si), H-integrand bound is (R_si+S_si) times that, and the two normalizer bounds are 2^(κR_si), 2^(κS_si). Inner errors are added to each interval BEFORE division or logarithms; outer errors are added AFTER the outer sum. Positive denominators are checked at every node.

PROVED — At N=4096 the absolute outer errors are at most 4.5410·10^−31 and 3.58264684·10^−27. With all arithmetic and inner errors included:

    log2 M1 ∈ [0.51599187405865778647641245720363800,
               0.51599187405865778647641245720455427]
    log2 M2 ∈ [0.51599162047014794189115095280871168,
               0.51599162047014794189115096003773423].

PROVED — N=8192 independently tightens these enclosures to

    log2 M1 ∈ [0.51599187405865778647641245720409613,
               0.51599187405865778647641245720409614]
    log2 M2 ∈ [0.51599162047014794189115095642322295,
               0.51599162047014794189115095642322296].

PROVED — The 4096 certificate alone proves the moment inequalities; the second run is a diagnostic, not the source of the error bound. Full outward scalar and moment intervals are in A_certificate_4096.json and A_certificate_8192.json. SCALAR_SLACKS.md lists every scalar check, generated from the former result. No exponent is inferred by rounding a floating optimizer output.

EVIDENCE — Both runs were sequential, single-process, small-array computations; elapsed times were under 8 and 20 seconds. No search or optimizer was run. REGISTER.md records predictions and outcomes.

## Issue register and precise repairs

| Status | Severity | Issue and resolution |
|---|---|---|
| PROVED | repairable; fatal to an unrestricted reading | T:154–180 omits b≤n^c and the word-RAM scope. Add Base's quantifiers. The pure exponent does not follow for arbitrary b from a bound containing poly(n+b) and a guard fallback. |
| PROVED | repairable | T:45, 121 uses a potentially noninteger/unspecified polynomial trial factor. Hardcode an integer polynomial majorant and take an outer ceiling; evaluate 2^d as the exact rational 2^m/|Σ(M)|. |
| PROVED | repairable | T:134 and 141 write T≤2^{d(L)+2n^0.6}, dropping C_S n^8 and the factor from the ceiling. Replace by 2^{d(L)+2n^0.6+O(log n)}. Work exponents are unchanged. |
| PROVED | repairable | T:129–137 needs explicit small-prime and right-key-sort checks. They pass with ample slack; their precise inequalities are in the inventory and code. |
| PROVED | repairable | T5/T6 and Base A5/A6 should explicitly refer to the uncapped ideal execution. A real run can stop earlier at its cap. The separate cap-failure argument repairs the theorem. |
| PROVED | repairable | Base B2:702 invokes A<1 but that alone does not ensure 4A+3≤6. Use A≤3/4. T:37 already includes the correct strengthening, and this point passes. |
| PROVED | cosmetic | T:25–31 cite T6 “items” for work bounds; those are in T7. Several Base line pointers have drifted. |
| PROVED | cosmetic | T:21 says “all strict” while MU2, SR and domain restrictions are naturally non-strict. At this point they have positive slack anyway. |
| PROVED | cosmetic | The last checksum region requires z=(q,0), unlike bounded regions' (q,0,0). A redundant zero is harmless only if the corresponding row is explicitly omitted. |
| PROVED | repairable exposition | T:183 says coverage has “no further cutoff.” The cancellation of C_S is correct, but the success lower bound still needs a sufficiently large n depending on the fixed collision constant; the cap and polynomial absorption have their own thresholds. |
| NOT CHECKED | premise, not a discovered flaw | [S], the complete underlying OpenAI theorem, original 430 Base moments, and historical commit provenance are not newly certified by this review. The J=1 moments needed here ARE independently certified. |

PROVED — After these repairs there is no fatal defect in the ternary replacement found by this review. The exact headline threshold remains 0.4873407528 under the stated conditional/model scope.
