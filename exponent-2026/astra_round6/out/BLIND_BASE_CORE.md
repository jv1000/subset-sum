# Independent Base core derivation, frozen before opening full proof bodies

EVIDENCE — Read Base statements 230–231, 240–241, 247–248, 254–257, 486–488, 696–698, 737–745; notation/algorithm 122–219, 225–228, 295–297, 303–387, class definitions, A3 conclusions, A4 statement and good-set implication, filter/region definitions 620–647, 663–694, and Appendix B checksum definitions 1030–1105. Exposure exceptions are in REGISTER.md. This is independent reconstruction with disclosed contamination, not a pristine blind experiment.

## Lemmas 3.1–3.3 and Corollary D

PROVED — 3.1. Write N=|V|. For each distinct t-sum choose a representative T. For every (t-k)-subset W of T, record (W,w(T)-w(W)). For fixed W distinct original sums give distinct k-sums on V\W. Hence |Σ_t(V)| C(t,k) ≤ sum_{|W|=t-k}|Σ_k(V\W)|. Divide using C(N,t)C(t,k)=C(N,t-k)C(N-t+k,k). This proves the assertion including k=0 and t=N.

PROVED — 3.2. Choose one k-subset representative for each distinct k-sum of V. A uniform s-subset includes each with probability C(s,k)/C(N,k). Included representatives have distinct values, so E|Σ_k(S)| ≥ |Σ_k(V)|C(s,k)/C(N,k). Divide by C(s,k).

PROVED — 3.3. The union of N+1 layers has size at most (N+1) times the largest layer. Complementation maps j-sums bijectively to (N-j)-sums, so a largest layer may be chosen at t≤N/2. Since C(N,t)≤2^N, a_t≥2^{-d(V)}/(N+1).

PROVED — D. Assume explicitly 0≤k and 0≤σ,v and valid binomial coefficients. First fix a v-set V and choose t≤v/2 with |Σ(V)|≤(v+1)|Σ_t(V)|. If t≥k, apply 3.1 then 3.2 to V\W, whose size v-t+k≥v/2+k≥σ. A uniform σ-subset drawn from the complement of a uniform W is uniform in V; hence E a_k(S_V)≥a_t(V)≥2^{-d(V)}/(v+1). If t<k, then k≤v/2 (from 2k≤σ≤v/2+k), so C(v,t)≤C(v,k). The assumed C(σ,k)C(v,k)≤2^v implies 2^{-d(V)}/(v+1)=|Σ(V)|/[2^v(v+1)]≤C(v,k)/2^v≤1/C(σ,k)≤a_k(S_V). This is exactly where the product hypothesis is used. Average over uniform V and then S_V. The marginal S_V is uniform on M. The t<k step was exposed before this reconstruction.

## A5 reconstructed

PROVED — Fix I and M and draw F uniformly among all subsets of M. Symmetric difference is a bijection, so S=(I∩M)△F is uniform over 2^M; conditional on |S|=σ=m/2, it is uniform among σ-sets. The central-binomial probability is at least 1/(m+1).

PROVED — Put c^I_i=(-1)^{[i∈I]}c_i on M. For i∈S, F and I have opposite membership, so c^F_i=-c^I_i. Thus the distinct left k-mask values under c^F have cardinality |Σ_k(S;c^I)|. The signing is fixed before drawing S and leaves every deficiency unchanged. Applying D gives E a_k(S;c^I)≥E_V 2^{-d(V)}/(v+1)=2^{-g_M}/(v+1), where g_M denotes minus the log of that expectation.

PROVED — Remove bad S. Because 0≤a_k≤1, a bad fraction β removes at most β from the expectation. To retain at least half the lower bound one needs β≤2^{-g_M}/[2(v+1)]. A4 and the LD bound on g_M imply this for large n provided its positive exponential margin dominates the bit-length guard. Goodness means distinct signed c-values remain distinct signed b-values; this part was exposed in the A4 definition read.

PROVED — Small prime step. Choose one representative of each of N distinct signed b-values. They have O(n)-bit differences since |b_i|<P, independent of original bit length. For a random P' of scale H=2^{floor(γm)}, the collision probability of each unequal pair is ≤poly(n)/H. If C_p counts ordered equal-residue pairs, E C_p≤N+poly(n)N²/H. Cauchy gives the number R_p of occupied residues ≥N²/C_p. Jensen therefore gives E R_p≥N/[1+poly(n)N/H]. As P'<2H, E(R_p/P')≥min(N,H)/poly(n)H. If B=C(σ,k)≥H and N=a_k B, then min(N,H)/H≥a_k. This yields per-trial success ≥2^{-g_M}/poly(n). To claim the particular power n^{-6} one must explicitly track the prime-collision polynomial and central-layer/product factors; the qualitative argument alone does not establish that exponent.

PROVED — For a chosen residue occupied by a left mask, let Y=S\X. The left/right records match the integer carry. Since I is an alias, the c-total differs from t_s, so the record is visited rather than skipped. Disjointness passes and the class key of I is inserted. Cap failure is a separate global event: a literal “after the trial” assertion assumes the hypothetical uncapped run or no prior cap failure.

NOT CHECKED — Precise n^{-6} and uniform threshold pending comparison. No proof of original checksum Lemma 4.2 has been reconstructed here; it is a named input to the region argument.

## B2 and region reconstruction

PROVED — Let U,W be pattern averages, ū,w̄ true averages. Errors are |U-ū|≤3ε, |W-w̄|≤4ε. A sampled pattern has t=Δ-αU>0. If W≤Γ, α=1 and Δ-U=t. In region ρ0 the first row Δ-ū≥t-3ε, second Γ-w̄≥-4ε, and each choice row ū_v-ū_l≥-6ε. With z0≥1 and nonnegative multipliers, z·G≥t-6εΣz.

PROVED — If W>Γ, α=Γ/W and aΓ W-U=(W/Γ)t. In region Γb_{i-1}<W≤Γb_i the first row aΓ w̄-ū≥b_{i-1}t-(4aΓ+3)ε, lower endpoint row w̄-Γb_{i-1}≥-4ε, upper endpoint row Γb_i-w̄≥-4ε, choice rows ≥-6ε. Thus z0 b_{i-1}≥1 suffices, provided 4aΓ+3≤6. For ρ9 omit the upper row and use b8=15. The universal 6 requires the stated numerical bound on aΓ, rather than positivity alone.

PROVED — For one filter, comparisons disappear. The low-region certificate z=(1,0) gives exponent Δ-u and moment M1=∫M² 2^{Δ-u}. For all W>Γ choose the two rows (aΓ w-u, w-Γ) with z=(1,0): since W/Γ>1 the same domination holds for the whole upper region, and moment M2=∫M² 2^{aΓ w-u}. Thus exactly two certificates suffice if these two moments are <2^η by enough margin. J=1 is one filter, not an additional “family of J=1 filters” with comparisons.

PROVED — On the table-good event the per-pattern conditional variance is ≤N^{-1}Lπ/P² sum_k |J(k)|². Substitute Lπ≤2^{(η-αU+18ε)n}, N≥2^{τn}, and domination -αU≤-Δ+average(zG)+6εΣz. Since τ+Δ=η, the remaining exponent outside the phase product is -2η+18ε+6εΣz (up to O(1/n)). Summing over P frequencies gives another η, while independent uniform phases factor the expectation into the nth power of ∫finite M²2^{zG}. A moment bound ≤2^{η-δ} gives error ≤2^{-(δ-18ε-6εΣz)n+O(1)}. Summing finitely many regions and 2^{O(sqrt n)} patterns and polynomially many targets costs subexponential factors. Markov/Chebyshev gives simultaneous accuracy. No independence across frequencies is required. Exact direct-pattern contributions need no moment bound.

NOT CHECKED — This proves the region/variance implication conditional on Lemma 4.2, caps, precision and finite-circle transfer, not the entire original checksum algorithm from scratch.
