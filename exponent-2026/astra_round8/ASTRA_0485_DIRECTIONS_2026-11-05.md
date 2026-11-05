**CONJECTURE — My strongest recommendation is to investigate computing the aliases’ total contribution without listing every alias class.** That attacks the premise behind the paper’s counting floor. I would pair it with a second investigation: estimating the checksum and alias correction together, so their errors can cancel.

I think we need a new algorithmic ingredient, but we may be able to retain substantial parts of the current framework.

**PROVED — The target requires more than removing overlap waste.** Under the paper’s full-enumeration and alias-count premises,
\[
\tau_0\ge \frac{1-\Delta}{2}.
\]
At the frozen capacity, this gives \(0.48565153115\), already above 0.485. These premises and their limitations are recorded in :codex-file-citation{path="D:/AIProjects/SubsetSum/Astra_round8/out/rev8d/Voitle_SubsetSum_certified-0.48758_2026-11-05_rev8d.pdf" purpose="source"}.

My exact rational-arithmetic check confirms that reaching \(\tau_0=0.485\) through full enumeration requires \(\Delta\ge0.030\), even with zero enumeration overhead. The gap from our frozen capacity is exactly \(0.0013030623\). Retaining the current \(T=\tau_0+20\epsilon\), with \(\epsilon=10^{-8}\), raises that necessary capacity to \(0.0300004\) for \(T=0.485\), before other costs and strict slacks.

Here is where I would put the research effort, in priority order.

1. **CONJECTURE — Replace alias reporting with weighted aggregation.**

   The current architecture ultimately needs a quantity—the alias phase sum—to subtract from the checksum. Producing a list of the contributing objects is one way to obtain it. The research question is whether that list is unnecessarily expensive.

   I would formulate a precise replacement problem:

   > Given the representation lists, modular constraints and phase weights, compute the required alias contribution without explicitly producing every compatible alias class.

   Candidate tools are signed matrix factorizations, inclusion–exclusion circuits, and transforms on subsets. Their purpose would be to combine many contributions in one operation while retaining the exact multiplicities and weights.

   **EVIDENCE — There is a relevant precedent.** Ye–Li’s revised paper uses algebraic cancellation in partial-match circuits; it also proves a limitation for the corresponding OR circuits in its regime. Their comparison with OpenAI explicitly distinguishes compatibility testing from enumerating modular pseudosolutions. This makes their *algebraic mechanism* worth examining, even though their published exponent does not itself supply our desired improvement. [Ye–Li, Sections 1.3–1.4](https://arxiv.org/html/2610.10446v2#S1.SS3)

   **NOT CHECKED — Their circuits do not automatically compute our weighted alias correction.** Detecting a compatible pair, summing all compatible pairs, and summing distinct alias classes are different problems. Deduplication could consume the entire saving.

   **First milestone:** derive the exact weighted matrix or tensor that the correction needs, including multiplicities. Then seek a small signed factorization whose construction and evaluation costs beat explicit reporting. A useful first result would be a composition lemma explaining precisely what such a factorization would buy in the full algorithm.

2. **CONJECTURE — Estimate the residual directly, using shared randomness.**

   We currently estimate a large modular checksum and subtract the aliases. Another possibility is to design an estimator for the difference from the outset.

   **PROVED — The elementary reason this can matter** is that, for real-valued estimators,
   \[
   \operatorname{Var}(X-Y)
   =\operatorname{Var}(X)+\operatorname{Var}(Y)
     -2\operatorname{Cov}(X,Y).
   \]
   Bounding the two errors separately can discard a useful covariance term. For complex estimators, the analogous identity uses the real part of the covariance.

   **CONJECTURE — The same troublesome configurations may contribute to both the checksum and correction.** If shared randomness makes those contributions cancel before we bound the error, the residual might admit a better second-moment bound than the existing \(M_1,M_2\) analysis.

   This is the direction in which I would investigate control variates: subtract a cheaply computable random contribution with known expectation, then estimate what remains.

   **First milestone:** construct a toy estimator with three properties: its expectation preserves the true-solution signal; the correction is genuinely cheaper to compute; and its exact residual second moment improves on separate bounds. Only then derive its asymptotic budget.

   **NOT CHECKED — Shared randomness alone gives no improvement.** The covariance must have the right sign and sufficient magnitude uniformly over worst-case inputs. A construction that cancels the true solution along with the aliases is useless.

3. **CONJECTURE — Explore a small amount of dependence between coordinates in the checksum.**

   The current filters are flexible functions, but their use still exploits a coordinatewise structure. Increasing the Fourier degree explores that structure more thoroughly; it does not necessarily escape it.

   I would examine filters on small groups of coordinates, or a small mixture of product filters, and ask:

   > Can dependence distinguish high-amplitude, expensive configurations more efficiently than the current coordinatewise scores?

   **EVIDENCE — The existing searches discourage spending most of our time on additional harmonics or small filter families.** They do not establish that every correlated construction has the same capacity limit.

   **First milestone:** derive the estimator and cost accounting for the smallest nontrivial coupled construction. Charge for normalization, sampling, table generation and evaluation before optimizing its moments. Start with a construction whose normalization can be calculated exactly.

   **NOT CHECKED — A better integral is insufficient.** If the sampling tables lose their efficient structure, the apparent capacity gain may disappear. Also, capacity just above 0.030 would still leave very little room for the list costs. This direction probably needs to combine with an alias-side improvement.

4. **CONJECTURE — Seek a worst-case dichotomy tailored to whichever new primitive succeeds.**

   A promising compression or aggregation method may initially work only when the input has favorable structure. Instead of trying immediately to prove that it works universally, ask whether failure itself exposes another fast algorithm.

   The desired theorem would have the form:

   > Either the instance supports efficient weighted aggregation, or its failure supplies a certificate that enables a different algorithm within the target budget.

   **EVIDENCE — Mixing dichotomies already play this role in representation-based algorithms:** a favorable mixing case supports the main method, while failure is handled separately. [Ye–Li, Section 1.1](https://arxiv.org/html/2610.10446v2#S1.SS1)

   **NOT CHECKED — We do not yet have the right structural statistic or fallback.** A useful dichotomy must be algorithmic: we must find the relevant structure and exploit it cheaply. An existential statement about additive structure would not suffice.

**EVIDENCE — I would keep [S] and YP-Hall as a separate mathematical project.** Proving [S] would validate the ternary improvement and could give a reusable representation lemma. But the present ternary construction has threshold \(0.4873407528\); it does not supply a route to 0.485 by itself. Likewise, the \(k=1\) problem is valuable groundwork, but the algorithm needs control at a layer growing linearly with the block size.

**CONJECTURE — My preferred next research sprint would therefore start with two concrete objects:**

- An exact specification of the **weighted alias-aggregation problem**, with a proposed signed factorization and complete cost accounting.
- An exact **second-moment formula for a jointly randomized checksum-minus-correction estimator**, retaining covariance until the last possible step.

For each, I would preregister a small experiment with explicit enumeration as the control, including repeated weights, highly structured inputs and generic inputs. The first success criterion would be a correct identity and an identifiable asymptotic saving—not an optimizer returning a smaller exponent.

**CONJECTURE — If I had to choose only one question to pursue first, it would be: “Can we subtract the aliases without discovering them individually?”** A positive answer would remove a specific obstruction that our paper identifies, and could make 0.485 a credible target without requiring an entirely new Subset Sum framework.