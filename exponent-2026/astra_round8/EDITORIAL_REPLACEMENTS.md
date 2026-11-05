# Suggested publication revision

EVIDENCE — These are proposed edits for Jennifer, not edits to the source. They prioritize a reader who knows exponential-time algorithms but has not read the project notebooks or Base. The conditional nature of the main algorithmic claim must survive every shortening.

## A shorter opening

EVIDENCE — Suggested title: **Certified parameter improvements for worst-case Subset Sum and limits of the alias–checksum analysis**. The existing numerical title is also usable if the abstract immediately states the inherited proof assumptions. “Why the architecture stalls” currently promises a global explanation stronger than the evidence establishes.

EVIDENCE — Suggested abstract (subject to integrating the identified proof repairs):

> We study the alias–checksum approach to worst-case Subset Sum introduced by OpenAI and modified by Kapila. Conditional on the cited non-numerical arguments, we give a certified parameter point with threshold T=0.4875754036: for every fixed T'>T, the resulting uniform randomized algorithm runs in O(2^(T'n)) word operations on inputs of polynomial bit length, with success probability at least 2/3. A single asymmetric filter replaces a family of 43 filters. Independent interval computations certify the required numerical inequalities, including analytic bounds for quadrature errors.
>
> We also prove a lower bound on the first filtering moment, valid for all positive continuous densities. Combined with the list and pair inequalities of the original analysis, it excludes every parameter choice with tau<=0.484 in that budget. Three algebraic bounds explain the active costs at our improved point. A separate operation-count argument gives (1-Delta)/2 as a barrier for an enumeration phase with 2^((1-eta+o(1))n) distinct alias classes; this is not a universal lower bound for Subset Sum or a proved global bound on checksum capacity. Finally, we isolate a small-layer conjecture which would yield threshold 0.4873407528, and give proved special cases and explicit remaining questions.

EVIDENCE — The K16 point and the 430-certificate verification can move to the contribution list; they do not both need full numerical detail in the abstract. Keep the abstract to the main improvement, one proved structural result, and the principal open question.

## Recommended reading order

EVIDENCE — A reader should encounter the following sequence:

1. **Problem, model and main result.** State the input model and the formal conditional main theorem. A compact comparison table should distinguish an exact threshold, a proved ordinary-O exponent, and an experimental estimate.
2. **How the algorithm works.** Introduce the checksum prime, aliases and alias classes, the list/checksum split, and the preliminary search. Define deficiency and the two uses of a shared block. Then explain precisely what changes from OpenAI to Base to this paper.
3. **The new point and its certificate.** Give the Base point first because it is the headline result. State the finite list of sufficient conditions and their dependency map, the moment convention, and the independent certification method. Put full decimal data and certificates in an appendix or a stable artifact.
4. **What the budget permits and obstructs.** Prove Lemma 1 and the all-parameter exclusion, then derive the three reduced bounds. Separate the exact fixed-capacity counting implication from the empirical capacity landscape.
5. **The conditional extension and open problems.** Present the ternary theorem, the exact statement [S], the implication chain, and the fully formulated partial results. Put speculative variational observations after the proved combinatorics, clearly marked as such.
6. **Reproducibility and AI use.** Briefly disclose tools, code independence and prior exposure. Move search histories, repeated referee narratives, and most optimizer diagnostics into the artifact documentation.

EVIDENCE — The K16 audit and the 430 historical certificates are valuable supporting results but currently delay the headline result until page 10. They fit naturally in appendices or a short secondary-results section. There is no need to remove them from the research record.

## Introduce Corollary D before naming it as a dependency

EVIDENCE — Suggested transition before the Base parameter table:

> Partition the coordinates into a shared block M and outside blocks L and R, of sizes approximately mu n, ell n and (1-mu-ell)n. A trial uses a random half S of M and seeks many representations of an alias through k-element subsets of S, with k approximately a|M|. Repetition is useful only if these subsets produce sufficiently many distinct sums. Kapila's Corollary D supplies the required averaged lower bound under explicit size conditions; we restate the version used here next.

PROVED — The restatement should define v=m-2k, sigma=m/2 and g=-log2 E_V[2^-d(V)] for a uniform v-subset V of M. Base lines 254–257 require integer k,sigma,v with 2k<=sigma, 2sigma<=v+2k, v<=|M|, and binom(sigma,k)binom(v,k)<=2^v; in this application 2sigma=v+2k. Its conclusion is

    E_{|S|=sigma} [ |Sigma_k(S)| / binom(sigma,k) ] >= 2^-g/(v+1).

EVIDENCE — Follow with two sentences explaining how concentration bounds g by the trial budget and how the small-prime argument converts distinct sums into success probability. Do not make the reader reconstruct this from “productive trials,” an unexplained g, and a source label. The full proof may remain a cited dependency if the theorem is explicitly conditional, but the usable statement belongs in the paper.

## Minimum notation panel

EVIDENCE — Add this before the first constraint table, and give actual definitions rather than only names:

| Notation | Meaning |
|---|---|
| h_2(x) | -x log2 x -(1-x) log2(1-x), with endpoint convention |
| Sigma(B), d(B) | Distinct subset sums of B; d(B)=|B|-log2|Sigma(B)| |
| tau / tau0, T | Internal enumeration budget / final exponent threshold; T includes the stated overhead |
| eta, Delta, Gamma | Prime exponent; eta-tau; 2tau-eta |
| mu, ell, r | Sizes of M,L,R divided by n; r=1-mu-ell in Base |
| a_mask, a_Gamma | Mask density; Delta/Gamma. Do not call both a |
| K, kappa | Number of half-blocks; density power parameter |
| d_local, d0, d1, cap, c0 | Local deficiency cutoff, preliminary-search thresholds, time cap and useful-block probability |
| rho_c, rho_f | Certified continuous moment threshold and finite-circle threshold |
| P, P' | Checksum prime and smaller representation-filtering prime |
| sigma, k, v | Half-block size, mask size, and Corollary D's residual size |

EVIDENCE — The density denoted mu in the Q_w definition should be renamed nu to avoid collision with block size. Use h_2 and a_Gamma consistently. Label every theorem, proposition and conjecture, and replace hand-typed “Section 8,” “Section T,” “Theorem A,” etc. by explicit references identifying whose theorem is meant.

## Replace the variational paragraph with a statement that is exact

PROVED — For a probability density nu on the circle, write lambda=log2(2+2cos x), U=E_nu u and V=E_nu v. The Gibbs variational formula gives

    log2 M1 = sup_nu { E_nu lambda + p(Delta-U) - KL_2(nu||unif) },
    log2 M2 = sup_nu { E_nu lambda + q(a_Gamma V-U) - KL_2(nu||unif) }.

PROVED — These identities quantify over all densities nu. The published domination proof uses the affine expressions as sufficient majorants of a piecewise target on sampled patterns. They do not by themselves establish the manuscript's claimed equivalence to a single condition restricted to sampled types. If that stronger equivalence is retained, define its phi, optimize the multipliers explicitly, and prove the needed duality and boundary assertions.

## A focused future-work ending

EVIDENCE — Suggested final research agenda, ordered by what each answer would change:

1. **Prove [S], or find a counterexample.** State the fixed polynomial loss and the linear range k<=0.11m. Explain that the conditional ternary point needs only k/m about 0.00703. State that k=1,t=2 is settled, that two special families are settled, and that general k=1,t>=3 remains open; those partial results do not settle linear k.
2. **Bound or improve joint checksum capacity.** About 0.029 is a numerical achievement and conjectural ceiling, not a proved optimum. A global inequality linking u and v, or a certified better density pair, would resolve this question.
3. **Reduce enumeration costs.** Specify the fixed-capacity operation-count regime in which (1-Delta)/2 applies. Avoiding full alias enumeration, changing the estimator, or finding a new representation family could escape that regime.
4. **Complete verification of inherited arguments.** List the exact remaining OpenAI/Base dependencies. Distinguish ordinary written proofs from optional formalization; remove the stale claim that the already re-derived Base core has only been read.

EVIDENCE — Continuing this work after publication is entirely compatible with a useful paper now. The publication boundary should be a stable collection of stated, proved or certified results with explicit limitations, not a claim that the research program is finished.
