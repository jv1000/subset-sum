# A certified 0.48758 for worst-case Subset Sum, and why the alias–checksum architecture stalls near 0.4876 (draft)

Nov 3, 2026 · @MochiKitten

## Status of this draft

Working draft by Jennifer Voitle, Claude (Anthropic) and Astra; we edit it as results come in. Nothing here is submitted, and no novelty claim is made until a literature check is done.

| Result | Status |
| --- | --- |
| Exponent 0.4875754036 (time O(2^{0.4875755n})) in Base's construction with one asymmetric filter, 1.0e-4 below JoshuaQFEX (Section 8) | Rigorous certificate (33 conditions) and two independent referees; conditional on Base's written proof and the OpenAI proof |
| Three closed-form bounds and the floor τ ≥ (1 − Δ)/2 ≈ 0.4857 of the architecture (Section 9) | Exact algebra on Base's constraints; numbers from floating, pre-registered runs |
| Overlap identity for the list overhead; negative results for filter families, ternary masks and colour-coding (Section 9) | Floating, pre-registered; mechanisms identified |
| Lemma 1, a lower bound on the first moment for all densities (Section 5) | Proved; independently refereed; interval-evaluated |
| 0.48 blocked in the OpenAI construction (Section 5) | Rigorous for all parameters given Lemma 1 (with the list and pair bounds it is infeasible for every τ ≤ 0.484); the sharper floor 0.4852 is a floating estimate |
| 16-block point at 0.4894616 in the OpenAI construction (Section 7) | Two independent rigorous certificates; conditional on the OpenAI proof and our block-count audit |
| Joint M1 + M2 capacity about 0.029 (Sections 6, 10) | Floating exploration; no proof yet |
| Certification of the 430 premises of the 0.487676 bound (Section 3) | Two routes plus an outside check (Astra) |

Open questions for the authors:

- how we position this relative to Base and JoshuaQFEX, and whether to contact them before posting;
- how to word the AI disclosure and authorship for the venue we choose;
- checking every reference link and revision.

## Abstract

Worst-case Subset Sum fell below the meet-in-the-middle exponent 1/2 in October 2026, with OpenAI's 2^{0.49n} algorithm and Ye and Li's 2^{(1/2 − 1/450000)n}. Follow-up work on the OpenAI algorithm reached 0.4877 (Base, which modifies the construction) and 0.487676 (JoshuaQFEX, a retuning of Base, conditional). We give a parameter point with exponent 0.4875754036, so running time O(2^{0.4875755n}), about 1.0e-4 below JoshuaQFEX. Inside Base's construction, a single asymmetric filter with 16 cosine and 16 sine terms replaces Base's family of 43 cosine-only filters, and all alias parameters are re-optimized. All 33 numerical conditions, including both filtering moments, are certified in ball arithmetic and were rechecked by two independent referees. Like JoshuaQFEX, the result is conditional on Base's written proof. Within the original OpenAI construction we also certify a 16-block point at 0.4894616.

We then explain why this line of work stalls near 0.4876. Base's alias constraints reduce to three closed-form bounds whose balance reproduces our point to within 1e-6. One of them counts the aliases themselves, which gives the floor τ ≥ (1 − Δ)/2 for any design that enumerates every alias class modulo the checksum prime, where Δ is the checksum's capacity: about 0.4857 at today's capacity of about 0.029, and exponent 0.48 would need Δ ≥ 0.040 even with a perfect list side. The rest of that bound is exactly the share of mask pairs that overlap. Pre-registered experiments show that filter families, ternary masks in the style of Becker–Coron–Joux and colour-coding do not help, each for an identified reason. We prove that the first filtering moment satisfies, for every filter, log2 M1 ≥ 1 + pΔ + (1+p) log2 E\[(1+cos x)^{1/(1+p)}\], which blocks 0.48 in the OpenAI construction. We also independently certify the 430 moment premises of the JoshuaQFEX bound, and we state the open lemmas that would move the exponent.

## 1. Introduction

For fifty years the best worst-case algorithm for Subset Sum was meet-in-the-middle, in time 2^{n/2} (Horowitz–Sahni 1974). In October 2026 two independent works broke that barrier. Ye and Li reached 2^{(1/2 − 1/450000)n} through partial match and exact integer circuits. OpenAI reached 2^{0.49n} by a different route: modular aliases, a capped preliminary search and a filtered Fourier checksum.

The OpenAI exponent comes from fixed numerical parameters, and follow-up work tuned them. Base (a-kapila) claims 0.4877; JoshuaQFEX claims 0.487676, conditional on 430 continuous moment inequalities inherited from Base; Astra's landscape study found a certified point at 0.4897736 and a floor of 0.4895157 for the unchanged 17-block budget.

Lower exponents are faster. Where the results stand:

| Exponent | Work | Construction | Status |
| --- | --- | --- | --- |
| 0.5 | Horowitz–Sahni 1974 | meet in the middle | classical |
| 0.4999977 | Ye–Li | partial match, integer circuits | preprint, proved |
| 0.489995 (stated 0.49) | OpenAI | aliases, preliminary search, filtered checksum | preprint |
| 0.4897736 | Astra's tuning | OpenAI, retuned parameters | numerics certified |
| 0.4894616 | this paper | OpenAI with 16 blocks and asymmetric densities | two certificates; conditional on the OpenAI proof |
| 0.4877 | Base | modified lists (mask density) and 43 filters in 10 regions | claimed; its 430 moment premises certified here |
| 0.487676 | JoshuaQFEX | Base with retuned parameters | conditional on Base |
| 0.4875754036 | this paper (Section 8) | Base with one asymmetric filter (16 cosine + 16 sine terms) in place of 43 | certified and refereed; conditional on Base |

Base changes both the list construction and the estimator. Our analysis of the original construction (Sections 5–7) indicates that both changes are needed to get below about 0.4895. Combining Base's list construction with our asymmetric filter reaches 0.4875754036 (Section 8). Section 9 shows why further progress in this architecture is bounded: at today's checksum capacity no change on the list side can go below about 0.4857.

This paper contributes:

1. A certified and refereed point at 0.4875754036 (time O(2^{0.4875755n})) in Base's construction with a single asymmetric filter, 1.0e-4 below JoshuaQFEX (Section 8).
2. An explanation of the values near 0.4876: three closed-form bounds, the floor (1 − Δ)/2 ≈ 0.4857 of the architecture, the identification of the remaining list overhead as overlapping mask pairs, and pre-registered negative results for filter families, ternary masks and colour-coding (Section 9).
3. A lower bound on the first filtering moment valid for all densities, which blocks exponent 0.48 in the OpenAI construction (Section 5).
4. A source-level audit showing that the block count 17 can be any K (Section 4), and a certified 16-block point at 0.4894616 with asymmetric densities (Section 7).
5. A backward analysis from 0.48 that prices each constraint of the OpenAI budget (Section 6).
6. An independent rigorous certification of the 430 moment premises of the 0.487676 bound (Section 3).
7. Precise open problems: a joint bound on the moment capacity, Corollary D beyond the half-block, and designs that avoid enumerating every alias class (Section 10).

## 2. The OpenAI architecture and its parameter budget

The algorithm's running time is 2^{(T+o(1))n} with T = max(tau + 20 eps, cap, mu + 1/4, eta/2). A parameter point is valid when the inequalities below hold. Here eta n is the bit length of a random prime P, tau n the list and enumeration budget, mu = m/n the shared block size, gamma the smaller-modulus rate, d the local deficiency, K the number of disjoint half-blocks (17 in the paper), eps = 1e-8 and guard g = 1e-5.

| Constraint | Inequality | Source (TeX) |
| --- | --- | --- |
| Block fit | K mu < 1 | aliases l.79 |
| Filtered list | tau >= 1/2 + (h(1/4) - 1/2 - gamma) mu | aliases l.201–211 |
| Visited pairs | tau >= 1 + (2h(1/4) - 1 - gamma) mu - eta + g | aliases l.244–253 |
| Sparse distinctions | eta > h(mu) + mu + g | aliases l.296–309 |
| Setup work | T >= mu + 1/4 | aliases l.163–169 |
| Many weights | 1/2 - d > gamma | aliases l.354–399 |
| Useful block (Markov) | 1 - d0/(K d mu) > c0 > 0 | aliases l.336–352 |
| Preliminary search | d1 < d0, cap > 1/2 - d1 (strict) | setup l.157–219 |
| Trial division | T > eta/2 | implementation l.283–285 |
| Checksum balance | Delta = eta - tau > 0, Gamma = 2tau - eta > 0 | checksum l.180–199 |
| Domination, case 1 | 1 <= p, 3p <= 30 | checksum l.443–449 |
| Domination, case 2 | 1 <= q\_m, q\_m(4a + 3) <= 30, a = Delta/Gamma | checksum l.451–458 |
| Error decay | rho\_c < rho\_f < eta - 48 eps | checksum l.487–495; filtering l.116–155 |
| Filtering moments | M1, M2 < 2^{rho\_c} | filtering l.90–103 |

The two moments are integrals over the circle with normalized measure. For positive densities f, g and kappa > 0, with K\_x(w) = f(x+w)g(w)/Q(x) and Q(x) = mean\_w f(x+w)g(w), the paper's scores are u = A + E - D and v = 2D - A - E, where D = KL(K\_x || uniform), A = E\_K log2 f\*(x+w), E = E\_K log2 g\*(w), and f\* = f^kappa / mean f^kappa (likewise g\*).

```latex
M_1 = \int_{\mathbb T} (2+2\cos x)\, 2^{\,p(\Delta - u(x))}\, dx, \qquad M_2 = \int_{\mathbb T} (2+2\cos x)\, 2^{\,q_m(a\, v(x) - u(x))}\, dx
```

The pair (x, w) enters through y - theta = x + w (correlation, not convolution). With symmetric densities this convention is invisible; with asymmetric ones it matters (Section 7).

## 3. Certifying the premises of the conditional 0.487676 bound

All 430 continuous moment inequalities that the JoshuaQFEX bound assumes hold, certified twice. The tightest, filter 28 in region rho0, clears its assumed margin 0.00025 by 3.79e-6 in log2.

Each inequality has the form below, for filters v = 0..42 and regions rho0..rho9, with required margins 0.00025 (rho0, rho1), 4 (rho2–rho8) and 17 (rho9).

```latex
I_b(v,\rho) = \int_{\mathbb T} (2+2\cos x)\, 2^{\,z\cdot G(x)}\, dx \;<\; 2^{\,\eta_b - m_\rho}, \qquad \eta_b = 0.51613
```

- **Route A:** python-flint arb at 200 bits; analytic-strip trapezoid error bounds for the inner and outer quadratures; a strip bound on the integrand from a contour split, Cauchy–Schwarz and Parseval monotonicity. Outer error 1.8e-218.
- **Route B:** an independently written mpmath interval implementation with different node counts and strip widths. It agrees with Route A to < 5e-13 in log2 margin on 422 of 430 inequalities; the remaining 8 have looser but still passing enclosures.
- **Least margins** reproduce Base §8.2 to every printed digit: 0.000253791727569 (rho0), 0.000359513928220 (rho1), 4.15582444577 (rho2).
- **The paper's own transferred certificates**, evaluated directly at tau = 0.48767595 and eta = 0.51612858, all exceed the required 1e-6; the least is 1.3154e-4, about 48 times the paper's uniform worst case.
- **Controls:** reproduction of earlier rigorous moments to 1e-19; rejection of a false threshold and of a perturbed Delta; doubled resolution identical to 15 digits.
- **Correction credited to Astra:** our first export wrote rounded-to-nearest decimals labelled as bounds. All exports now use directed rounding, verified in interval arithmetic; no certification decision changed.

The bound remains conditional on non-numerical premises we did not check: finite-circle convergence, the isolation and alias lemmas, and the word-RAM accounting.

## 4. Changing the block count

The constant 17 enters the OpenAI proof in exactly two places, and both hold verbatim for any K with K mu < 1. Every other dependence on block size runs through mu = m/n, and the checksum section is generic in (eta, tau).

1. **Block fit (aliases l.79).** The paper needs 17 m/2 <= floor(n/2); in general K m/2 <= floor(n/2), which holds for large n when K mu < 1.
2. **Partition and Markov (aliases l.336–352).** A uniform floor(n/2)-set is partitioned into K disjoint sets of size m/2, each with the law of S. Superadditivity and nonnegativity of deficiency give K E d(S) <= d0 n. Markov then gives Pr\[d(S) <= d m\] >= 1 - d0/(K d mu) - o(1), which must exceed a fixed c0 > 0. The later product c0/(m+1) · 1/2 · 1/(4 K0 n^2) >= n^-4 holds for any fixed c0 > 0.

The remaining replacements are mechanical: 0.0567 becomes mu throughout, so the sparse-distinction count becomes 2^{(h(mu)+mu)n} (valid for mu <= 1/2), the setup bound becomes T >= mu + 1/4, and 0.4894 > gamma becomes 1/2 - d > gamma. In the checksum, the fixed 0.5168/0.5169 thresholds become rho\_c < rho\_f < eta - 48 eps, and the error decay 2^{-0.0007n} becomes 2^{-(eta - rho\_f - 48 eps)n}, which still absorbs the 2^{O(sqrt n)} pattern count.

The constraints that do not depend on K are isolation, the prime-collision lemma, the deficiency lemmas, alias subtraction and the word-RAM accounting. The old moment certificate does not transfer: new densities need a new numerical appendix (Section 7).

Status: a reading audit by Claude, and an independent re-derivation of the full constraint list from the TeX by a referee agent that found nothing missing. A human reader should re-derive the partition step and the preliminary coupling.

## 5. A lower bound on the first moment for all densities

**Lemma 1.** For all strictly positive continuous densities f, g on the circle, every kappa > 0, Delta >= 0 and p > 0:

```latex
\log_2 M_1 \;\ge\; \Phi(p) := 1 + p\,\Delta + (1+p)\log_2 \int_{\mathbb T} (1+\cos x)^{1/(1+p)}\,dx, \qquad \int_{\mathbb T} (1+\cos x)^b\,dx = \frac{2^b\,\Gamma(b+\tfrac12)}{\sqrt{\pi}\;\Gamma(b+1)}
```

*Proof.*

1. **Jensen.** Since K\_x is a probability density in w, u(x) = E\_K log2\[f\*(x+w) g\*(w) / K\_x(w)\] <= log2 Q\*(x), where Q\*(x) = mean\_w f\*(x+w) g\*(w). By shift invariance Q\* is itself a probability density on the circle.
2. **Rewrite.** With w(x) = 1 + cos x, also a probability density, M1 = 2^{1+p Delta} E\_w\[2^{-p u}\] >= 2^{1+p Delta} E\_w\[Q\*^{-p}\].
3. **Hölder.** Write w^{1/(1+p)} = (w Q\*^{-p})^{1/(1+p)} Q\*^{p/(1+p)} and use exponents 1+p and (1+p)/p. Since mean Q\* = 1, E\[w^{1/(1+p)}\] <= (E\_w\[Q\*^{-p}\])^{1/(1+p)}, which is the claim. ∎

**Tightness.** Equality in step 1 needs kappa = 1, and in step 3 needs Q\* proportional to w^{1/(1+p)}. Densities with g sharply peaked and f proportional to w^{1/(1+p)} approach the bound, with gaps down to 5.8e-7 in log2; at kappa = 1.1 a fixed positive gap remains. The function g(p) = (1+p) log2 E\[w^{1/(1+p)}\] is a log power mean of w, so it is nonincreasing in p; this makes minimizing Phi over p rigorous on monotone cells.

**Finite circle.** On Z/PZ the same argument holds with the discrete average of w^{1/(1+p)}. For even P that average is smaller than the closed form, so the closed form alone is false there (a referee counterexample at P = 4 has gap -0.154; the gap shrinks roughly like P^{-1-2/(1+p)}). The algorithm uses P \~ 2^{eta n}, so the correction is negligible, and the paper's premise is the continuous inequality anyway.

**Consequence 1: the eight-block point fails.** Astra's eight-block scalar point (eta = 0.67, Delta = 0.1900002) passes all twelve scalar inequalities. Lemma 1 gives log2 M1 >= 0.885370 for every p in \[1, 10\] (interval-evaluated on 9000 monotone cells), against the 0.669998 required: a shortfall of 0.215 bits for every possible filter.

**Consequence 2: 0.48 is out of reach.** Writing eta = tau + Delta, the M1 constraint forces Delta <= Dmax(tau) = max over p in (1, 10\] of (tau - 1 - g(p))/(p - 1), about 0.0403 at tau = 0.48. The list bound forces mu ≥ (1/2 - tau)/(gamma + 1/2 - h(1/4)), and the pair bound with gamma < 1/2 then forces Delta ≥ 2.6494(1/2 - tau) + g, about 0.053 at tau = 0.48. These three constraints are jointly infeasible for every tau ≤ 0.484 and every K (checked in interval arithmetic by the second referee), so 0.48 is out of reach in the OpenAI construction for all parameters, given Lemma 1. Combining Lemma 1 with the full scalar budget gives a sharper floor near 0.4852 (K = 11), but only as a floating, grid-based estimate. An earlier draft said the sparse-distinction bound forces Delta of about 0.17; that does not follow from the stated steps and is withdrawn.

Status: proof by Claude; refereed by an independent agent, which checked each step and found no counterexample in 300 random and 16 adversarial instances (minimum gaps +0.107 and +0.0009).

## 6. Working backward from 0.48 in the OpenAI construction

The binding resource is not the block count but the joint capacity of the two moments: the largest Delta = eta - tau at which some densities keep both M1 and M2 below 2^eta. At tau = 0.4898 that capacity is about 0.029, whatever density family we try (floating exploration).

| Density family | Moments imposed | Capacity (Delta) | What binds |
| --- | --- | --- | --- |
| 6 cosines (Astra's family) | M1 and M2 | 0.02810 | both moments |
| 6 cos + 6 sin, kappa in \[0.5, 2\] | M1 and M2 | 0.02841 | both moments |
| 16 or 32 cos + sin, Astra-basin starts | M1 and M2 | 0.02864 | both moments |
| 16 cos + 16 sin, random starts | M1 and M2 | 0.02908 | both moments |
| 6 cosines | M2 only | 0.03226 | rounding cap q\_m(4a+3) <= 30 |
| 6 cosines | M1 only | 0.0396 | M1 (Lemma 1 ceiling 0.0427) |

Two consequences follow.

- **Fewer blocks alone do not help.** With real densities, every K from 9 to 13 is worse than 17 (best 0.48978 at K = 13). A continuation that grows the block toward 1/K at K = 11 and 12 raises T monotonically, because the moments pin Delta near 0.0284 and the pair bound then charges for every extra unit of mu.
- **Each unit of capacity is worth about 0.35 in the exponent.** The floor of the audited budget, optimized over K, falls as capacity rises (floating, optimistic closure):

| Joint capacity Delta | Floor on T | Best K |
| --- | --- | --- |
| 0.0281 (today's 6-term family) | 0.48977 | 17 |
| 0.032 | 0.48840 | 15 |
| 0.036 | 0.48703 | 13 |
| 0.0396 (M1's own capacity) | 0.48579 | 12 |

At today's capacity this reproduces Astra's certified basin, which is the control. A further 0.001 of capacity, which richer asymmetric densities do supply, already moves the best K from 17 to 16; Section 7 certifies that point.

## 7. A certified 16-block point at 0.4894616

**Theorem (conditional on the OpenAI proof and Section 4).** With the parameters below, the OpenAI algorithm decides Subset Sum in time O(2^{T' n}) for every T' > 0.4894615727, in particular O(2^{0.4894616 n}).

| Parameter | Value | Replaces |
| --- | --- | --- |
| Half-blocks K | 16 | 17 |
| Block size mu | 0.0593373017 | 0.0567 |
| eta | 0.5184804040 | 0.51772 |
| tau | 0.4894613727 | 0.48996 |
| gamma | 0.4888978551 | 0.48925 |
| kappa | 1.03489429 | 1.0315 |
| p, q\_m | 8.38520435, 8.19573911 | 8.5, 8.3 |
| Densities r, s | 16 cosine + 16 sine terms each (64 coefficients, 8 decimals) | 6 cosine terms |
| Coverage constant c0 | 0.0001 | 0.005 |
| d, d0, d1 | 1/2 - gamma - 1e-8; (1-c0)K d mu (1-1e-7); d0 - 1e-9 | 0.0106, 0.01004, 0.010025 |
| cap; rho\_f; rho\_c | tau + 20 eps; eta - 48 eps - 5e-7; rho\_f - 1e-6 | 0.489985; 0.5169; 0.5168 |

The exact coefficients are in candidate\_K16.json; an appendix will list them.

**Certificates.**

- **Ours** (python-flint arb, 200 bits): inner trapezoid with N\_in = 256 on a strip of half-width 0.3, outer N = 8192 on a strip of half-width 0.2. q0 = 0.372, so log2 Q is analytic on the strip. Quadrature errors are below 1e-27. Result: log2 M1 = 0.518477576190 and log2 M2 = 0.518477347232, against rho\_c = 0.5184784240. All 20 interval margins are positive; the moment margins are 8.48e-7 and 1.08e-6. Doubled resolution agrees to 20 digits.
- **Referee's** (independent agent; saw only the parameter file and the TeX): its own constraint list with line citations, nothing missing; its own rigorous moment bound by an exact-ball DFT with aliasing and tail bounds. It agrees with ours to 16 digits.
- **Controls:** the same certifier passes Astra's certified 17-block point below its own threshold and rejects that point with Delta raised by 0.001.

**Conventions the result depends on.**

- **Orientation.** The densities are asymmetric, so the correlation convention y - theta = x + w (P(x) = mean\_w F(x+w)G(w)) is load-bearing. Reflecting one density gives log2 M \~ 3.28, a catastrophic failure. Swapping f and g, or x -> -x, is harmless because the weight is even.
- **Admissibility.** filtering.tex l.16 allows any strictly positive continuous densities; nothing in the proof uses symmetry. The old numerical appendix used the j <-> 64-j symmetry and is replaced by either certifier.
- **Thin slacks.** Several margins are 1e-9 to 1e-6. They only make the cutoff n\_\* astronomically large: Chebyshev with d0 - d1 = 1e-9 makes the preliminary-search bound meaningful only for n of order 1e18 or more. Nothing fails asymptotically.

At mu = 0.0593 > 1/17, seventeen blocks would not fit: the gain comes from trading one block for a larger shared block, which the extra moment capacity of the new densities pays for.

## 8. Below JoshuaQFEX: Base's construction with one asymmetric filter

Base changes both halves of the OpenAI algorithm. On the list side it uses one large shared block (about 0.475n) with sparse masks of density a ≈ 0.008, returns alias phase sums instead of alias lists, and replaces the 17-block Markov step by an averaged small-layer bound. On the checksum side it uses a family of 43 filters, each with 8 cosine terms, certified in 10 regions of the pattern space. Base reports that its filter search stalls near 0.4876 and that "further progress needs a new idea." JoshuaQFEX retunes Base's parameters to 0.487676.

**Observation.** With a family of J = 1 filters, Base's Theorem B certificates collapse to OpenAI's two moments: region ρ0 uses the multiplier vector z = (p, 0) and regions ρ1–ρ9 use z = (q, 0, 0), so the 10 certificates are exactly M1 and M2. Our asymmetric filters (Section 7) therefore drop into Base's construction unchanged, and Base's 43-filter family has to compete with one filter that carries sine terms and 16 harmonics.

**Price, then optimization.** In Base's alias budget each +0.001 of moment capacity lowers τ0 by about 0.00039 (control: zero extra capacity recovers 0.4876826, within 7e-6 of JoshuaQFEX). We then optimized Base's alias parameters (η, μ, a, γ, l), one filter (16 cosine + 16 sine terms per density, and κ) and the multipliers p, q jointly, under all of Base's alias constraints and both moment constraints. Four of four starts reached τ0 = 0.4875749, matching the pre-registered prediction 0.48757 ± 0.0001.

**The frozen point** (exact decimals, in candidate\_base.json):

| Parameter | Value |
| --- | --- |
| τ0 | 0.4875752036 |
| η | 0.5162721413 |
| μ | 0.4752421539 |
| a | 0.0082379228 |
| γ | 0.0605824120 |
| l | 0.4836347962 |
| κ, p, q\_m | 1.03465831, 8.45902160, 8.27015425 |
| ε, ζ, input guard | 1e-8, 1e-8, 10^8 |
| ρ\_f, ρ\_c | η − 1.5e-6, ρ\_f − 1e-6 |
| exponent T = τ0 + 20ε | 0.4875754036 |

**Certificate.** All 33 conditions (34 checks; our certifier also tests an implied one) were checked in ball arithmetic (python-flint arb, 200 bits) and all margins are positive: Base's alias constraints C1–C8, the size conditions S1–S5, Lemma A5 (1/2 − τ0 + ζ < δ), the Lemma A7 conditions, the Theorem A cap 1/guard + ζ < ε0, the prime draw η/2 < τ0, the Lemma B1–B3 bookkeeping, and both moments. The tightest margins are B3 (8.1e-7), M1 (1.315e-6), C4 (1.316e-6) and M2 (1.494e-6). The moments are log2 M1 = 0.51626832585128515 and log2 M2 = 0.51626814726466969, with rigorous error radii below 1e-20; doubling the quadrature resolution changes nothing in 20 digits.

**Independent referee.** A separate agent that saw only the candidate file and the Base and OpenAI sources derived every condition from the text with line citations, recomputed both moments with its own rigorous code (agreement to 20 digits), and checked that J = 1 and sine terms are legitimate: Lemma 3.2 of the OpenAI paper uses only uniform and derivative bounds, which change from 2.433 and 4.010 to 3.20, and nothing in the entropy order, the pattern grid or the joint moment uses evenness. Its verdict: the claim survives, with no fatal issue. It also found conditions our first certificate had not listed (Lemma A7 items 1, 3 and 4, S2, S5, the prime draw, and the row-error condition a\_Γ ≤ 3/4); we added them, and all are slack.

**Second referee.** A further independent review by Claude Fable 5.1, working only from this paper, the two parameter files and the Base and OpenAI sources, derived 33 conditions from the TeX with line citations and found all of them to hold in arb at 200 bits. Its own moment evaluator reproduces the OpenAI paper's Appendix A table to every printed digit and gives log2 M1 = 0.51626832585128515 and log2 M2 = 0.51626814726466969 (ball radius below 4e-55), unchanged across resolutions and strip widths; an independent floating implementation agrees to 12 digits. It also passed the 16-block point of Section 7, Lemma 1 and the algebra of Section 9. Its corrections are incorporated in this revision: the exponent is now stated as 0.4875754036 rather than rounded down, the cutoff n\_\* is quantified, the colour-coding expansion is completed, and the floor is quoted at the certified point's Δ.

**Status and caveats.** The proved exponent is T = τ0 + 20ε = 0.4875754036, so the algorithm runs in time O(2^{T′n}) for every T′ > T, in particular O(2^{0.4875755n}); T is 1.005e-4 below JoshuaQFEX and 1.15e-4 below Base's τ0. It is conditional on Base's written proof (its alias-step cost accounting, Lemma A5 and its checksum changes) and on the OpenAI paper, exactly as JoshuaQFEX is. The constants ζ and the input guard are free in Base; ours (1e-8) only raise the cutoff n beyond which the bound applies: Base's Proposition P then needs n > 10^8, and its Chebyshev term 4/(ζ²n) is small only for n of order 10^17. A write-up must update these of Base's stated constants: δ = 0.0698 (Base: > 0.0706; still far above the 0.0124 it is compared with), S3's 0.129 → 0.1308, ε0 = 1.3157e-6 (Base 5.37e-6), the guard constant 10^8, c\_z = 6p ≈ 50.8 (Base ≤ 2511) and the B3 error exponent 8.1e-7 (Base 0.00017). The OpenAI rounding caps 3p ≤ 30 and q(4a + 3) ≤ 30 are not required under Base, whose Lemma B2 accounts for rounding through 6εΣz; they hold anyway. A write-up must also rewrite its filter definition and verification script for sine terms; the referee's list is in the repository.

## 9. Why the exponents stall near 0.4876

This section analyses Base's parameter budget at our Section 8 point. The closed forms are exact algebra on Base's constraints (C1)–(C8). The numbers come from floating, pre-registered runs (our experiments C13–C17); nothing in this section is certified.

**Shadow prices.** Loosening each constraint by one bit and re-optimizing every parameter, filter included, gives the exponent saved per bit:

| Constraint | What it counts | Exponent saved per bit |
| --- | --- | --- |
| C4 | matching visits | 0.389 |
| C1 | small prime P′ against the number of representations | 0.258 |
| C2 | left records | 0.077 |
| C3 | right class records | 0.077 |
| C5 | right masks times trials | 0.001 |
| M1, M2 | checksum moments, per bit of log2 M | 0.051 |

The list side carries 0.80 of the exponent, and the prices add. Weighted by each constraint's coefficient of τ0 (p ≈ 8.5 for the moments), they sum to 1 within 2.5%, as the Karush–Kuhn–Tucker conditions require.

**Three closed-form bounds.** Write η = τ0 + Δ, where Δ is the gap the checksum allows, and use l + r = 1 − μ. Adding C2 and C3, and rearranging C4 and C5, gives

- (i) τ0 > 1/2 − μ(γ − h(a)/2), from left records times right classes, where more representations help;
- (ii) 2τ0 > 1 − Δ + μ\[(h(a) − γ) + (h(1/2 − a) − 1)\], from the matching visits together with the checksum, where smaller masks help;
- (iii) τ0 > (1/2 + μ h(1/2 − a))/2, from the right masks times the number of trials.

At the floating optimum behind our Section 8 point the three right sides are 0.4875739, 0.4875744 and 0.4875744, against τ0 = 0.4875749 (the gap is the 1e-6 slack we imposed). At the frozen, certified point they are 0.4875739, 0.4875745 and 0.4875745 against τ0 = 0.4875752: (ii) and (iii) bind, and (i) sits 6.6e-7 lower. Our point and Base's are therefore a balance of these bounds. Bound (i) wants a larger mask fraction a, because γ ≤ h(2a)/2 grows faster than h(a)/2; bound (ii) wants a smaller one; bound (iii) holds the block size μ in place.

**The floor of the architecture.** In (ii), 1 − η is log2 of the number of aliases, 2^n/P, for generic inputs, and Theorem A inserts every alias class into a dictionary. Hence any design that enumerates the alias classes modulo a prime of ηn bits and certifies the rest with a checksum of capacity Δ (so η − τ0 ≤ Δ) has τ0 ≥ 1 − η ≥ 1 − τ0 − Δ, that is

**τ0 ≥ (1 − Δ)/2.**

Precisely: for inputs with distinct subset sums every alias class is a single alias, there are about 2^{(1−η)n} of them per target, and Theorem A spends at least one counted step on each; the checksum at the same modulus costs 2^{τn} with η − τ ≤ Δ. The statement says nothing about designs that do not enumerate every alias class, that use different moduli, or whose checksum is not of the moment form. At the certified point's Δ = 0.0287 the floor is 0.48565. Exponent 0.48 would need Δ ≥ 0.040 even with no list overhead at all; Lemma 1 caps the first moment's capacity near that value, and the joint capacity reached in practice is about 0.029. The floor is attained in the model when the overhead in (ii) is removed. The table re-optimizes the filter at each step, so Δ drifts to 0.0284 and the floor it reaches is 0.4858; with the filter held fixed, the second referee's model gives 0.4875741, 0.4871563, 0.4867011, 0.4862020 and 0.4856515.

| Share of the C4 overhead removed | τ0 |
| --- | --- |
| none (Section 8 point) | 0.4875749 |
| 25% | 0.4871858 |
| 50% | 0.4867641 |
| 75% | 0.4863049 |
| all | 0.4858019 = (1 − Δ)/2 |

**What the overhead is.** The rest of (ii) is μ\[(h(a) − γ) + (h(1/2 − a) − 1)\] = 0.003846 per n at our point. It equals −log2 of the probability that a uniform left mask of k elements and a uniform right mask of σ − k elements of the block are disjoint, 0.003845 per n; at γ = h(2a)/2 the two entropy expressions agree. So the overhead is exactly the visited tuples with overlapping masks, which the expansion step tests and discards. It costs about one bit per left-mask element, because each element of a left mask lies in the alias's half-block S with probability 1/2.

**Colour-coding does not remove it.** Confining the left masks to a random region R of the block with |R| = ρm leaves S covering half of R. The left-mask part of the overhead becomes a + a²/(2ρ ln 2) + O(a³); the right-mask part, h(1/2 − a) − 1 = −2a²/ln 2 + O(a⁴), does not depend on ρ. So the total (0.00809 per element of the block at ρ = 1) is smallest at ρ = 1. In the full model every ρ < 1 is worse: by 1.4e-4 at ρ = 0.75, 4.0e-4 at 0.5 and 1.2e-3 at 0.25. Removing the waste needs partial knowledge of S or a different source of representations, not a filter on the masks.

**Ternary masks need a stronger Corollary D.** Following Becker, Coron and Joux, let the left mask also carry −1 entries outside S. On the block outside S the trial's signed weights are the negatives of the alias's own signing, so these entries add plain subset sums of that signing. In the floating model this reaches τ0 = 0.4873404, 2.35e-4 below our point, from four of four starts; the optimum splits Base's representations evenly between inside and outside S. The model assumes that Base's Corollary D holds for this two-part family essentially without loss. Losing 10% of the outside representations removes the gain entirely, and the break-even is about 2%. Base's proof descends from a good layer t ≤ v/2 by covering, which limits the support of the representations to m/2 + k. Under that limit a ternary mask with fractions (a, c) is no better, in every constraint, than Base's own mask with fraction a + c. We count this as a negative result and leave the stronger lemma open (Section 10).

**Filter families add almost nothing.** We tested families of two and three asymmetric filters in Base's format, with its comparison rows u\_v − u\_l. Base's own family is worth about 6.4e-4 bits of moment margin over its best single filter, which sets the scale. On top of our filter, the best two-filter family the optimizer found pairs the filter with its mirror image x → −x, which covers the mirror of the filter's own critical type: 6.7e-5 bits of margin, lowering the exponent by only 3.3e-6. Twelve random second filters reach either that pair or nothing, and a third filter adds 4.6e-6 bits. Asymmetry and family diversity seem to buy largely the same thing. We did not certify the 3e-6 improvement.

**Summary.** At today's checksum capacity this architecture cannot go below about 0.4857, the list side can contribute at most 1.77e-3 of the remaining distance, and the obvious tools for that contribution (more filters, ternary masks, colour-coding) do not supply it. Each of these conclusions is a pre-registered experiment with a control that reproduced the Section 8 point.

## 10. Open problems

The main open problem is a proved upper bound on the joint M1+M2 capacity: a lemma turning "about 0.029 in every family we tried" into a theorem, or a family that beats it.

**Beyond the floor of Section 9.** Below about 0.4857 the architecture itself must change: either the checksum capacity rises (which is the joint bound question above, read in reverse), or the algorithm stops enumerating every alias class. Two narrower questions remain on the list side.

- *Corollary D beyond the half-block.* Let S be a uniform half of the block and consider the family {U : |U ∩ S| = k1, |U \\ S| = k2}. Is the average fraction of distinct sums w(U) at least 2^{−g}/poly(n), with g inside the trial budget (at most d(L), d(M) and (1/2 − τ0 + ζ)n)? Within the support m/2 + k this follows from Base's proof. Beyond it, a sumset argument is the natural attempt: a sum of two pieces can collapse only if both pieces are structured, and structure costs deficiency. Essentially lossless, the lemma is worth about 2.35e-4 through ternary masks. A cleaner sufficient statement exists. On the block outside S the trial's signed weights are the negatives of the alias's own signing, so the family's sums are plain k′-subset sums (k′ = k1 + k2) of one fixed signing, and a counting identity gives E\_S\[fraction of distinct sums\] ≥ a\_{k′}(M), the fraction of distinct k′-subset sums of the whole block. So it suffices that small layers are robust: a\_k(M) ≥ 2^{−d(M)}/poly(m) for k ≤ 0.01m. Base's Corollary D and its size conditions are then not needed, and its cost bounds still hold if μ < l. Under that statement the full model gives τ0 = 0.4873403, 2.35e-4 below the Section 8 point, with k1 = k2 = 0.0035m (floating, pre-registered). In expectation the statement holds with a large margin, because a small layer sees every additive relation less often than the half-cube does. A swap argument reduces it to a lower-tail concentration bound for a sum of mixed cylinder events (bits required to be 1 on one set and 0 on another), to which the standard Janson inequality does not directly apply. The statement holds with margin in every structured family we tested, and an adversarial search found no counterexample, but it is not proved. Our second referee reached the same reduction independently and proposed a cleaner target: monotonicity of the layer density, a\_k(M) ≥ a\_{k+1}(M) for k + 1 ≤ m/2. It suffices because 2^{−d(M)} ≤ E\_{t∼Bin(m,1/2)}\[a\_t\] (since |Σ| ≤ Σ\_t |Σ\_t|), and the layers outside \[k, m − k\] carry mass at most about 2^{−m(1−h(α))}, which a\_k ≥ 1/C(m,k) absorbs when α ≤ 0.11. Monotonicity held exactly in 30744 tests at m ≤ 14 (referee) and in exhaustive adversarial tests at m = 16, 18 and 20 (ours). It is sharp: with half the weights equal to 1 and half to 2, a\_k/a\_{k+1} = (m − k)/(k + 2), which is exactly 1 at k = m/2 − 1. Monotonicity also has an exact combinatorial form. The map (y, e) ↦ (e, y − w\_e) is a bijection between pairs with y a (k+1)-sum and e in the union U(y) of its witness sets, and pairs with x a k-sum and e outside the intersection C(x) of its witness sets. Hence Σ\_y |U(y)| = Σ\_x (m − |C(x)|), and a\_k ≥ a\_{k+1} is equivalent to Σ\_y (|U(y)| − (k+1)) ≥ Σ\_x (k − |C(x)|): the union-excess of the (k+1)-sums is at least the core-deficit of the k-sums (verified on 39 instances).
- *A different source of representations.* The overlap waste of Section 9 is intrinsic to representations drawn from a uniform half S. A construction that knows part of S in advance would remove it, worth up to 1.77e-3.

**A large-deviation form of the moment conditions.** By the Donsker–Varadhan variational formula, log2 mean 2^h = max over densities t of (E\_t h - KL(t || uniform)). Each moment condition therefore says that every frequency type t (a distribution of coordinates on the circle) whose pattern (E\_t u, E\_t v) would be sampled satisfies

```latex
\mathbb E_t[\lambda] + \varphi(\mathbb E_t u, \mathbb E_t v) - \mathrm{KL}(t \,\|\, \mathrm{unif}) \le \eta, \qquad \lambda(x) = \log_2(2+2\cos x)
```

that is, amplitude plus target minus rarity is at most the budget. This is exact; maximizing over types under linear constraints returns the affine-form moments by duality. At our certified point the binding type satisfies four corner equations at once:

| Quantity at the critical type | Value | Equals |
| --- | --- | --- |
| E\_t\[u\] | 0.02906 | Delta |
| E\_t\[v\] | 0.46036 | Gamma (0.46074) |
| E\_t\[u + v\] = E\_t\[D\] | 0.48942 | tau (0.4898) |
| E\_t\[lambda\] - KL(t) | 0.51882 | log2 M1, which is eta at capacity |

All the checksum's budgets bind at one type, the corner where the sampling boundary meets the case switch. The missing ingredient for the joint bound is an "amplitude costs entropy" inequality: a lower bound on E\_t\[v\], valid for every density pair, in terms of E\_t\[lambda\], KL(t) and E\_t\[u\]. With it, the critical type would certify that every Delta above the bound fails.

1. **A joint moment bound.** Lemma 1 alone allows Delta up to 0.0427. A natural first attempt fails: the pointwise relations u <= log2 Q\* and v >= max(0, -u) (from v = (D-A) + (D-E) >= 0 and u + v = D >= 0) define a convex relaxation whose capacity is 0.0426, no better than Lemma 1. A useful bound must use how u and v arise from the same pair (f, g). The mechanism is concentration: at the densities that are best for M1 alone, the entropy cost is large (E\_w v = 2.18 against Gamma = 0.45) and log2 M2 exceeds eta by 0.49 bit. A coupled relaxation helps. Writing a = f\*, b = g\*, Rényi monotonicity gives v >= -2 log2 BC(x), where BC(x) = mean\_w sqrt(a(x+w) b(w)) is the Bhattacharyya overlap. Together with u <= log2 (a ⋆ b), this gives lower bounds M1' and M2' on the moments in terms of one density pair, for every kappa. Their joint capacity is 0.0382 (floating; six starts agree to 0.0006). So the joint capacity at tau = 0.4898 is bracketed: about 0.029 is achieved, at most 0.0382 follows from the relaxation if its optimization is global, and at most 0.0427 is proved. The remaining gap has a clean source: the relaxation lets u use kappa = 1 and v use kappa = 2 (whose kernel is proportional to sqrt(ab)), while the algorithm must use a single kappa. Making the 0.0382 rigorous needs a global certificate for this two-density problem, or an inequality that keeps the single-kappa coupling. At kappa = 1 the problem is exact, and we derived its Euler–Lagrange equations; they agree with automatic differentiation to 5e-16. The equations are linear in ln f(y), so they rearrange into a fixed point, which a safeguarded relaxation (SOR) iteration can solve. Three pieces of evidence agree. The best kappa = 1 pair in a 24-term family has capacity 0.02854, the same from four starts. It satisfies the full nonparametric equations up to a relative residual of 2.2e-5. The SOR iteration, working on unrestricted grid densities, cannot improve it. Freeing kappa adds about 0.0005, giving 0.0291. We therefore conjecture that the joint capacity of this moment format is about 0.029 for all densities. By the price list in Section 6, the architecture's floor would then be about 0.48946, essentially the point certified in Section 7. At kappa = 1, v = E\_K\[log2 f(x+w)g(w)\] - 2u exactly. For indicator-like densities v = 2(KL(f) - u), so M2 acts as a second M1-type constraint with gap 2a KL(f)/(1+2a): peaked densities help M1 but raise KL(f), which hurts M2.
2. **The rounding caps.** On its own, M2 is limited by q\_m(4a+3) <= 30, a 30 eps rounding allowance in the checksum's domination step. Enlarging that allowance costs only O(eps) in the error exponent. It is not binding at the joint optimum today, but it would be after any capacity gain.
3. **A rigorous all-K floor.** The 0.4852 floor of Section 5 and the price list of Section 6 come from grid searches over the scalar budget. Interval sweeps, or dual certificates, would make them bounds.
4. **Other domination steps.** Lemma 1 bounds this proof's sufficient moment format, not Subset Sum. More cases in the domination step do not help. We replaced the paper's two exponent forms with up to 32 general affine forms c0 + c1 u + c2 v, each dominating its own strip of patterns, and restricted the patterns to the convex hull of the score curve (u(x), v(x)), which is all that real frequencies can reach. The capacity was unchanged in every case, at 0.02810 for Astra's densities and 0.02906 for ours. The binding patterns sit at the case switch W = Gamma, where the target is Delta - U for both cases, and the paper's p(Delta - u) is already the best affine form on that slice. Escaping the wall therefore needs a change of the target itself: the choice of alpha, the sampling/direct split, or the match-count bound L\_pi <= 2^{(eta - alpha U)n}. A Hölder-type lower bound for affine forms on the slice W = Gamma (a "slice lemma") is the natural route to the joint bound of item 1. The estimator knobs we can model inside this checksum design all fail. A separate sampling budget gains nothing, because the error exponent is rho - tau\_s + tau\_l - eta while T is the larger of the two budgets. Enlarging the enumeration threshold by delta makes both moments cheaper by about 7.4 delta bits but costs delta in T, a net loss. Stratifying patterns by amplitude Lambda (the block average of log2(2+2cos x)) adds a free tilt c3 on that coordinate. A minimax argument shows it can beat the paper's c3 = 1 only if the largest amplitude reachable in the sampling region falls below psi'(1), the average amplitude of M1's dominant contributors. That can never happen at the optimal multiplier. There d log M1/dp = Delta - E\_t\[u\] = 0 under the moment's own tilt t, so the tilted mean is a realizable sampling pattern (rarity 0.055 bits, far below eta) whose amplitude is exactly psi'(1). A joint optimization of densities, tilts, cutoffs and the LP-dual certificates confirms this, returning c3 = 1 from every start. Both moments' tilted means sit at the same critical pattern (U, W) = (Delta, Gamma), the corner where the sampling boundary meets the case switch. By the Donsker–Varadhan formula the moment conditions are equivalent to one statement about frequency types: every type t that would be sampled must satisfy E\_t\[lambda\] + phi - KL(t || uniform) <= eta, that is, amplitude plus target minus rarity is at most the budget. Proving the joint bound then means exhibiting one violating type for any given densities, for example the critical type. Getting past about 0.4895 otherwise needs a different variance argument, a list or pair improvement, or a different route.
5. **Relation to Ye–Li.** The floor of Section 9 does not apply to Ye and Li's algorithm, which has no modulus, aliases or checksum; but its own gain is only about 2.2e-6 n, from an integer-circuit improvement on a fixed partial-match matrix. An exploratory analysis by our second referee indicates that the two methods do not compose at the level of these constructions. At our Section 8 point the left records, right records and visited pairs are equally numerous, so a partial-match compatibility test has nothing to save; it would pay only with much larger masks (a ≈ 0.03–0.12), where it would need a per-coordinate cost below 0.107, while the best known (Fredman–Volper) cover for that sparse-row matrix costs 0.13–0.29 and Ye–Li's improvement over it is 4e-5. A circuit would also return multiplicity-weighted sums, whereas Theorem A needs each alias class counted once across trials. Interestingly, Ye and Li use the same ternary representation as Section 9's ternary masks, and their "many correct keys" step is the existence half (Base's Lemma 3.3) of the layer question below.

## 11. Methods, reproducibility and AI collaboration

Every experiment was pre-registered before it ran, with predictions, controls and kill rules, and every failure was kept. The work was done by Jennifer Voitle with two AI systems: Claude (Anthropic) and Astra (an OpenAI-based assistant).

- **Labels.** Each claim is marked as a rerun, reading audit, floating exploration, interval certificate or proof. Floating results are never presented as certified.
- **Independence.** Each certified claim has at least two implementations. Independent referees were fresh agent contexts that saw only the claim's inputs and the source TeX, never the authors' code.
- **Failures kept, for example:** an incomplete first constraint model; an off-by-one in a feasibility window; a wrong prediction that M2 alone would be weak; the failed convex relaxation of Section 10; conditions missing from our first certificate of the Section 8 point, found by the referee (all slack); a unit error in a pre-registered consistency check of the shadow prices; a ternary-mask model that first assumed an unsupported form of Corollary D; degenerate starts in the first filter-family runs; and, caught by the second referee, a headline exponent rounded 3.6e-9 below the proved bound and an incomplete colour-coding expansion. Each is logged with its correction.
- **Who did what.**
  - Jennifer Voitle: direction, review and submission decisions.
  - Astra: the landscape study, the 17-block floor, the 0.48 constraint audit and outside checks of Section 3.
  - Claude: the certifications, the block-count audit, Lemma 1, the 16-block point, the Section 8 point and the analysis of Section 9. The independent referees were fresh Claude agents; the second full review was by Claude Fable 5.1, working only from the paper, the parameter files and the source TeX.
- **Files.** The scripts, inputs, outputs and pre-registrations are in the project folders C2\_JoshuaQFEX\_conditional and C3\_target\_048\_Claude; the Section 8 point is candidate\_base.json with its certificate and referee report, and Section 9 is experiments C13–C17. They will be released with the paper.

## References

Taken from our project notes and the OpenAI source; each link and revision still needs checking before posting.

1. OpenAI. Subset Sum in time O(2^{0.49n}). Preprint, 4 Oct 2026; LaTeX source in our References folder; github.com/openai/math (preprints).
2. Ye and Li. Subset Sum via Partial Match. [arXiv:2610.10446](https://arxiv.org/abs/2610.10446), 7 Oct 2026.
3. a-kapila. PROOF\_0.4877.tex, github.com/a-kapila/maths-proofs, commit 44c34961 (14 Oct 2026). Cited as Base.
4. JoshuaQFEX (Joshua Wharton). subset-sum-bound, github.com/JoshuaQFEX/subset-sum-bound, HEAD bed8e18 (20 Oct 2026).
5. Horowitz and Sahni. Computing partitions with applications to the knapsack problem. J. ACM 21 (1974).
6. Trefethen and Weideman. The exponentially convergent trapezoidal rule. SIAM Review 56 (2014), Theorem 3.2.
7. Rosser and Schoenfeld. Approximate formulas for some functions of prime numbers. Illinois J. Math. 6 (1962).
8. Astra. Round 5 landscape (E2\_LANDSCAPE.md) and the 0.48 constraint audit (target\_048), Nov 2026; internal reports.
9. Howgrave-Graham and Joux. New generic algorithms for hard knapsacks. EUROCRYPT 2010.
10. Becker, Coron and Joux. Improved generic algorithms for hard knapsacks. EUROCRYPT 2011.
11. Alon, Yuster and Zwick. Color-coding. J. ACM 42 (1995).
