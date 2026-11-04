# Referee report on `paper.md` (draft of 3 Nov 2026)

Referee: Claude Fable 5.1, 3 Nov 2026. Sources used: `paper.md`, `candidate_base.json`, `candidate_K16.json`,
`base_PROOF_0.4877.tex` ("Base"), `openai_tex/sections/*.tex` ("OpenAI"). Nothing outside this folder was used.
All rigorous numbers below are python-flint 0.9.0 arb balls at 200 bits; a condition passes only if the whole ball
satisfies the strict inequality. Scripts are in `scripts/`, outputs in `scripts/out/`; see `scripts/README.md`.

Summary of verdicts

| Item | Verdict | One line |
| --- | --- | --- |
| 1. The 0.4875754 point (Section 8) | PASS, conditional on Base's and OpenAI's written proofs; two wording fixes required | 33 conditions derived from the TeX all hold; log2 M1 = 0.51626832585128515, log2 M2 = 0.51626814726466969 (true ball radius below 4e-55), margins 1.3155e-6 and 1.4940e-6; the claimed exponent 0.4875754 is 3.6e-9 *below* the proved bound τ0 + 20ε = 0.4875754036 and must be rounded up |
| 2. The 0.4894616 point (Section 7) | PASS, conditional on the OpenAI proof and the block-count audit, which I confirm | 17 enters the OpenAI proof only at aliases.tex l.79 and l.336-352; 22 conditions all hold; moments agree with the paper to 20 digits; the orientation claims (3.28 on reflection) are confirmed |
| 3. Lemma 1 (Section 5) | PASS | every step is correct; 495 adversarial/random instances, minimum gap +2.8e-6; rigorous min Φ = 0.8853701728 at the eight-block point; Dmax(0.48) ≤ 0.0403365; the paper under-claims: 0.48 is rigorously blocked in the OpenAI construction, not only at the eight-block point |
| 4a. Three closed-form bounds | PASS | exact algebra on C2+C3, C4, C5; the text's numbers refer to the floating optimum τ0 = 0.4875749, not to the frozen point 0.4875752036 |
| 4b. Floor τ0 ≥ (1 − Δ)/2 | PASS as a conditional model statement; generality stated below | valid for any design that inserts every alias class and uses a checksum with η − τ_cs ≤ Δ at the same modulus; the quoted 0.4858 uses Δ = 0.0284 while the certified point has Δ = 0.0287, giving 0.48565 |
| 4c. Overhead = −log2 Pr[disjoint masks] | PASS | exact finite identity C(m,σ)C(σ,k) = C(m,k)C(m−k,σ−k); 0.0038460 vs 0.0038454 reproduced |
| 4d. Colour-coding formula a + a²/(2ρ ln 2) | UNCLEAR (formula incomplete, conclusion correct) | it is the expansion of the left-mask part only; the full overhead has an extra ρ-independent term −2a²/ln 2, four times larger at a = 0.0082; "ρ = 1 is best" and the penalties 1.4e-4 / 4.0e-4 / 1.2e-3 are confirmed (1.5e-4 / 4.2e-4 / 1.2e-3 in my model) |

---

## Item 1. The 0.4875754 point (Section 8, `candidate_base.json`)

### 1.1 Conditions derived from the text

Base's Theorem 1 (l.58-66) gives time 2^{(τ0+20ε)n + O(n^0.7)} poly, so the exponent is T = τ0 + 20ε. The
proof needs the following numerical facts; the "slack" column is the amount by which the strict inequality holds
at the exact decimals of the JSON (arb lower end). Script: `scripts/check_base_point.py`, output
`scripts/out/base_point_N4096_8192.txt`.

| # | Condition | Where it is used | Slack |
| --- | --- | --- | --- |
| C1 | γ < h(2a)/2 | Base l.161; (S4) l.188; Lemma A5 step 4 l.520-521 | 1.31606e-6 |
| C2 | l + (h(a) − γ)μ < τ0 | l.162; Lemma A7 item 5 l.566-568 | 1.31570e-6 |
| C3 | r + (1 − γ)μ < τ0, r = 1 − μ − l | l.163; A7 item 6 l.569-572 | 1.31577e-6 |
| C4 | 1 − μ + (h(a) + h(1/2 − a) − γ)μ − η < τ0 | l.164; A7 item 7 l.573-589 | 1.31567e-6 |
| C5 | h(1/2 − a)μ + 1/2 − τ0 < τ0 | l.165; A7 item 2 l.558-560 | 1.31577e-6 |
| C6 | 0 < r < τ0, l < τ0 | l.166; A7 item 1 | 0.0411 / 0.4465 / 0.00394 |
| C7 | μ(1 − 2a) < l | l.167; (S2) l.185; A3(3) | 0.0162 |
| C8 | (μ/2) log2 3 < η | l.168; δ > 0 l.464 | 0.1397 |
| S1 | a ≤ 1/4 | l.184 | 0.2418 |
| S2 | μ(1 − 2a) ≤ 1/2 | l.185 | 0.0326 |
| S3 | h(2a)/2 + h(a) < 1 − 2a | l.186-187 | 0.854 (Base's printed 0.129 becomes 0.1308 at this point) |
| A7.1 | l, r, μ(1 − 2a) < τ0 − ε0 | l.556-557 | 0.00394 / 0.4465 / 0.0202 |
| A7.3 | 1/2 − τ0 + γμ/2 < τ0 − ε0 | l.561-563 | 0.4608 |
| A7.4 | r + 1/2 − τ0 < τ0 − ε0 | l.564-565 | 0.4340 |
| A7.6 | μ < τ0 − ε0 | l.569-572 | 0.0123 |
| ThmA | 1/guard + ζ < ε0 (guard 10^8 so b + 2 ≤ 2^{n/10^8 + 1}) | l.605-607 | 1.29567e-6 (ε0 = 1.31567e-6, least slack of C1-C8, l.172) |
| A5 | 1/2 − τ0 + ζ < δ = (η − (μ/2)log2 3)/2 | l.508-509 (Base writes "0.013 < δ") | 0.0574 (δ = 0.069826; Base's "δ > 0.0706" must be updated) |
| P | τ0 < 1/2 | l.281-285 | 0.0124 |
| prime | η/2 < τ0 + 20ε | l.795 | 0.2294 |
| chk | Δ > 0, Γ > 0 | l.141-142 | 0.0287 / 0.4589 |
| B2 | a_Γ ≤ 3/4 (row error (4a_Γ + 3)ε ≤ 6ε) | Lemma B2 l.703-705 | 0.6875 |
| B2 | z0 = p ≥ 1 (region ρ0) | l.709-710 | 7.459 |
| B2 | z0 = q ≥ 1 (regions ρ_i: z0 b_{i−1} ≥ 1, b_0 = 1) | l.712 | 7.270 |
| B1 | ρ_c < ρ_f | Lemma B1 l.651-659; OpenAI filtering l.152-155 | 1.0e-6 |
| B3 | ρ_f + (18 + 6p)ε < η | Lemma B3 l.719-733 with c_z = 6Σz = 6p | 8.12459e-7 |
| B3 | ρ_f + (18 + 6q)ε < η | same, c_z = 6q | 8.23791e-7 |
| M1 | log2 ∫(2+2cos x) 2^{p(Δ−u)} < ρ_c | Prop. B l.645-649 with z = (p, 0) | 1.31545e-6 |
| M2 | log2 ∫(2+2cos x) 2^{q(a_Γ v−u)} < ρ_c | Prop. B with z = (q, 0, 0) | 1.49404e-6 |

Not needed under Base: the OpenAI caps 3p ≤ 30 (checksum l.443-449) and q(4a+3) ≤ 30 (l.458) are replaced in Base
by the 6εΣz_t accounting of Lemma B2; they hold anyway (slacks 4.62 and 3.12). The paper lists them in its margins,
which is harmless but should be labelled as not required.

All 33 conditions hold; the four tightest are C1-C5 at 1.316e-6, the B3 bookkeeping at 8.1e-7 and the moments at
1.3e-6 / 1.5e-6, matching the paper's stated margins to four digits.

### 1.2 The moments

Method (`scripts/moments_arb.py`): OpenAI Appendix A generalized to N nodes and to sine terms. Inner integrals
(normalizers, P and Y at the nodes) are N-node trapezoid sums with the analytic-strip error 2B0/(e^{Nσ} − 1)
(numerical.tex l.198-241), B0 from |r(z)| ≤ Σ_j(|c_j| + |s_j|)cosh(jσ). Outer integrals use the strip of
half-width 2β with |Q − 1| ≤ q0 < 1 from the contour split, Cauchy–Schwarz and Parseval monotonicity
(numerical.tex l.265-298); with sine terms Re r(w + iy) = Σ(c_j cos jw + s_j sin jw)cosh(jy), so the identity
∫|f(· + iy)|² = Z_f^{-2}∫2^{2 r_y} and the monotonicity argument (which only needs f real) carry over verbatim.

Controls: (a) on OpenAI's own filter at N = 64 the code reproduces every printed entry of numerical.tex Table 1 and
the normalizers (Z_f = 1.1963625, X_0 = 1.71479, X'_0 = 1.72487, X_31 = 0.27604, …) and gives M1 = 1.42897 <
2^{0.5168} (`scripts/out/control_openai.txt`); (b) an independent double-precision implementation on a direct
N×N grid, computing u, v from the definition of D, A, E rather than from the P/Y identities, agrees to 12 digits
(`scripts/float_crosscheck.py`).

Results for `candidate_base.json` (σ = 0.3, β = 0.1, q0 = 0.37084):

| N | log2 M1 | log2 M2 | outer quadrature error |
| --- | --- | --- | --- |
| 1024 | 0.51626832585128515044 | 0.51626814726466968639 | 2.6e-85 |
| 4096 | same to 20 digits | same | 1e-340 |
| 8192 | same to 20 digits | same | 1e-700 |

True ball radii below 4e-55 at N = 8192 (5e-56 at N = 1024) (the ± shown by arb's `str(d)` is print truncation, not the ball). The values
agree with the paper's to all 17 printed digits. Changing the strips to (σ, β) = (0.45, 0.12), (0.2, 0.05),
(0.3, 0.14) changes nothing in 18 digits (`scripts/out/sensitivity_and_bounds.txt`).

### 1.3 The correlation convention

The convention Q(x) = mean_w f(x + w)g(w) is the one in the TeX: filtering.tex l.11-13 defines x = y − z,
w = z − θ, y − θ = x + w; l.19-20 defines Q and K_x with f(x + w)g(w); checksum.tex l.149-154 scores the high digit
by log f_*(y_i − θ) and the low digit by log g_*(z_i − θ); l.235-244 changes the law of w = z_i − θ to K_{x_i(k)}
and uses y_i − θ = x_i(k) + w. Base restates the same (B.2 l.1030-1034). It is the cyclic cross-correlation
P_j = (1/N)Σ_i F_{i+j}G_i (numerical.tex l.43), as implemented in Base's script and in mine. Experiment
(rigorous, N = 1024, on the K16 point): reflecting either density gives log2 M1 = 3.2778, swapping f and g or
sending x → −x leaves 0.5184775762 unchanged, exactly as Section 7 says.

### 1.4 Is J = 1 with sine terms a legitimate instance?

Yes. Base's Theorem B (l.737-763) and its certificate format (l.624-643) allow any J ≥ 1 and any multiplier
vectors z ≥ 0 with z0 ≥ 1 in ρ0 and z0 b_{i−1} ≥ 1 in ρ_i. With J = 1 the sets C are empty, so the rows are
(Δ − u, Γ − w) and (a_Γ w − u, w − Γb_{i−1}, Γb_i − w); z = (p, 0) and (q, 0, 0) make all ten certificates the two
integrals M1 and M2, Lemma B2 holds with Σz_t = p or q, and Lemma B3's exponent becomes
ρ_f − η + (18 + 6 max(p, q))ε, which is the B3 condition above. The filter choice v*(π) (l.676) is trivial.
Sine terms: Base invokes OpenAI Lemma 3.2 through (F7) l.212-214, "uses only that r and s are fixed trigonometric
polynomials". I checked the proof of Lemma 3.2 (filtering.tex l.133-176): it uses only (i) uniform bounds on |r|,
|s| from the coefficient sums (l.137) and (ii) derivative bounds for the Riemann-sum estimate (l.144-146). Both
hold for cos+sin polynomials (sharper bound Σ_j √(c_j² + s_j²) = 3.195 / 3.203, which is the paper's "3.20";
the plain absolute sums are 3.63 / 3.60). Nothing in the checksum section, the pattern grid or the joint moment
(4.14) uses evenness of f or g; the only place symmetry was used is the j ↔ 64 − j shortcut of OpenAI's Table 1,
which the new certificate replaces. Verdict: legitimate.

### 1.5 Issues to fix before posting

1. **Exponent rounding (must fix).** The proved bound is T = τ0 + 20ε = 0.4875754036, so the algorithm runs in
   O(2^{T'n}) for every T' > 0.4875754036. The headline "0.4875754" (abstract, Section 1 table, Section 8 status
   line, contribution 1) is below T by 3.6e-9 and is therefore not a theorem. Say 0.4875755, or state the bound as
   Section 7 does ("every T' > 0.4875754036, in particular O(2^{0.4875755 n})"). The title's 0.48758 is fine.
2. **Cutoff.** With ζ = 1e-8 Base's Proposition P needs n > 1/ζ = 1e8 and its Chebyshev term 4/(ζ²n) is o(1)
   only for n ≫ 4e16; the guard 10^8 needs n ≥ 10^8 ⌈log(b + 1)⌉. "Only raise the cutoff" is true, but the
   cutoff is of order 1e17 and the draft should say so.
3. Section 8 and Section 9 quote τ0 = 0.4875749 (the floating optimum) while the certified point is
   0.4875752036; use one value, or label the first as the floating optimum.
4. Base constants that change at this point and should be listed in the write-up: δ = 0.069826 (Base says
   > 0.0706), S3's 0.129 → 0.1308, ε0 = 1.3157e-6 (Base 5.37e-6), the guard constant 10^8, c_z = 6p ≈ 50.8
   (Base ≤ 2511), and the B3 error exponent 8.1e-7 (Base 0.00017).
5. Label the 3p ≤ 30 and q(4a + 3) ≤ 30 lines of the certificate as OpenAI-only and not required under Base.

---

## Item 2. The 0.4894616 point (Section 7, `candidate_K16.json`)

### 2.1 Block-count audit (Section 4)

I searched every numeric constant in the OpenAI TeX. The constant 17 appears only at aliases.tex l.79
(17m/2 ≤ ⌊n/2⌋) and l.336-352 (partition of a uniform ⌊n/2⌋-set into 17 disjoint m/2-sets, superadditivity,
Markov). Both generalize verbatim to K with Kμ < 1; the product at l.420-426 needs only a fixed c0 > 0. All other
block-size dependence is through m (l.74) and the constants 0.0567 (l.74, 82, 166, 300), 0.4894/0.48925 (l.75,
355, 367, 397), 0.01004/0.010025/0.0106/0.005 (setup l.157-219, aliases l.50, 344-352, 424), and in the
checksum 8.5/8.3/0.5168/0.5169/30ε/48ε/−0.0007 (checksum l.443-500, filtering l.90-123). Section 4 is correct.
Two remarks: (i) because m = 2⌊μn/2⌋ ≤ μn, the Markov bound 1 − d0 n/(K d m) is *at most* 1 − d0/(Kdμ) at
finite n, so the limiting inequality must be strict, which the paper's (1 − 1e-7) factor provides; (ii) the
preliminary cap must satisfy cap > 1/2 − d1 strictly (setup l.200-205 carries a +1/2), not "≥" as in the
Section 2 table; the point has strict margin.

### 2.2 Conditions (script `scripts/check_k16_point.py`, output `scripts/out/k16_point_N4096_8192.txt`)

| Condition | Source | Slack |
| --- | --- | --- |
| Kμ < 1 | aliases l.79, 336-339 | 0.0506 |
| 1/2 + (h(1/4) − 1/2 − γ)μ < τ | l.201-211 | 8.48245e-7 |
| 1 + (2h(1/4) − 1 − γ)μ − η + g < τ (g = 1e-5 guard, l.22-25) | l.244-253 | 8.48261e-7 |
| h(μ) + μ + g < η; μ ≤ 1/2 | l.297-308 | 0.1343; 0.4407 |
| μ + 1/4 < T | l.162-169 | 0.1801 |
| 1/2 − d > γ | l.355, 367, 397 | 1.0e-8 |
| 1 − d0/(K d μ) > c0 > 0 | l.346-352 | 9.999e-8; c0 = 1e-4 |
| d1 < d0; cap > 1/2 − d1 | setup l.192-205 | 1.0e-9; 8.48262e-7 |
| η/2 < T | implementation l.283-285 | 0.2302 |
| Δ > 0, Γ > 0 | checksum l.180-199 | 0.0290; 0.4604 |
| p ≥ 1, 3p ≤ 30 | checksum l.443-449 | 7.385; 4.844 |
| q ≥ 1, q(4a + 3) ≤ 30 | l.450-458 | 7.196; 3.347 |
| ρ_f + 48ε < η; ρ_c < ρ_f | l.487-495; filtering l.113-155 | 5.0e-7; 1.0e-6 |
| log2 M1 < ρ_c; log2 M2 < ρ_c | filtering l.90-103 | 8.47810e-7; 1.07677e-6 |

T = τ + 20ε = cap = 0.4894615727. Moments (σ = 0.3, β = 0.1, q0 = 0.37164, paper 0.372):
log2 M1 = 0.51847757618968867873, log2 M2 = 0.51847734723194144144, identical at N = 1024, 4096, 8192, true ball
radii below 4e-55, equal to the paper's values to all printed digits. Verdict PASS, conditional on the OpenAI proof.
As in item 1, the thin slacks (1e-8, 1e-9, 1e-7) make the cutoff astronomically large: Chebyshev with
d0 − d1 = 1e-9 gives failure probability 1e18/n, and B ≥ 2^{γm} needs 2^{1e-8 m} ≥ m + 1, i.e. n ≳ 1e11. The
theorem is unaffected, but the paper should state the order of n_*.

---

## Item 3. Lemma 1 (Section 5) — PASS

Proof check. Step 1: u = E_K log2[f_*(x+w)g_*(w)/K_x(w)] ≤ log2 E_K[·] = log2 Q_*(x) by Jensen; ∫Q_* = 1 by
Fubini and shift invariance, Q_* > 0. Step 2: ∫(1 + cos x)dx = 1 so w = 1 + cos x is a density; M1 =
2^{1+pΔ}E_w[2^{−pu}] ≥ 2^{1+pΔ}E_w[Q_*^{−p}] needs only p > 0. Step 3: Hölder with exponents 1 + p and (1 + p)/p
gives ∫w^{1/(1+p)} ≤ (∫wQ_*^{−p})^{1/(1+p)}(∫Q_*)^{p/(1+p)}; the zero of w at π is harmless. The closed form
∫(1 + cos x)^b = 2^bΓ(b + 1/2)/(√πΓ(b + 1)) follows from (1 + cos x) = 2cos²(x/2) and the Beta integral; checked
by quadrature to 1e-22 (`scripts/out/lemma1.txt`, Part A). The hypotheses "Δ ≥ 0" is not needed (Δ enters
linearly), κ is arbitrary, and p > 0 is needed. The monotonicity of g(p) (log of a power mean of w with exponent
1/(1 + p)) is correct.

Numerics (Part B, floating, u from the definition of D, A, E): the two candidate filters give gaps +0.0559 and
+0.0560; 495 instances including near-tight ones (f ∝ (1 + cos x)^{1/(1+p)}, g a von Mises bump with concentration
up to 2000, κ ∈ {0.7, 1, 1.035, 1.3}, p ∈ [0.3, 20]), lopsided, multimodal and 300 random 16+16-term asymmetric
filters: minimum gap +2.8e-6 at the near-tight case, no violation.

Consequence 1 (rigorous, Part C): with Δ = 0.1900002, Φ(p) ≥ 0.8853701728 for all p ∈ [1, 10] (minimum near
p = 1.157), exactly the paper's 0.885370, against the 0.669998 required. Consequence 2 (Part D): Dmax(0.48) ≤
0.0403365 (paper "about 0.0403"). Finite circle (Part E): at P = 4, p = 1 the discrete average is smaller and the
gap is −0.1539, as the paper says.

Under-claim. The status table says "0.48 blocked in the OpenAI construction: follows from Lemma 1 at the eight-block
point; the all-K floor is a floating estimate". The blocking is rigorous for every parameter choice, not only that
point: the list bound (l.201-211) forces μ ≥ (1/2 − τ)/(γ + 1/2 − h(1/4)), the pair bound (l.244-253) with
γ < 1/2 − d < 1/2 then forces Δ ≥ 2.64941(1/2 − τ) + g, and Lemma 1 forces Δ ≤ Dmax(τ). In arb these are
contradictory for every τ ≤ 0.484 (at τ = 0.48: needed Δ ≥ 0.0530 versus Dmax ≤ 0.0403). So "0.48 is out of
reach in the OpenAI construction" is a theorem given Lemma 1; only the sharper 0.4852 floor is floating. The
sentence "the sparse-distinction bound forces Δ of about 0.17" is not reproducible from the stated steps (list
bound gives μ ≥ 0.106, then η > h(μ) + μ gives Δ > 0.114); it does not matter for the conclusion.

---

## Item 4. Section 9

### 4a. Three closed-form bounds — PASS

(i) is (C2 + C3)/2 with l + r = 1 − μ; (ii) is C4 with η = τ0 + Δ; (iii) is C5. The identities hold exactly in arb
(`scripts/out/section9.txt`, Part 1). At the frozen point the right sides are 0.4875738879, 0.4875745458,
0.4875745457 against τ0 = 0.4875752036 (gaps 1.32e-6, 6.6e-7, 6.6e-7). The paper's 0.4875739 / 0.4875744 /
0.4875744 "against τ0 = 0.4875749" and its "1e-6 slack" refer to the floating optimum; (ii) and (iii) are the
binding pair, (i) sits 6.6e-7 lower, so "explicit three-way balance" is a slight overstatement for the frozen
point. My own fixed-Δ alias-budget model (Part 4) reproduces the point: optimum 0.4875741 at μ = 0.47524,
a = 0.0082373, γ = 0.0605803, l = 0.483636, and at JoshuaQFEX's Δ = 0.02845263 returns 0.48767593 against
JoshuaQFEX's 0.48767595.

### 4b. The floor τ0 ≥ (1 − Δ)/2 — PASS, with its generality made explicit

The argument: for inputs with distinct subset sums (the worst case the bound must cover), every alias class is
a single alias and there are ≈ 2^n/P ≥ 2^{(1 − η)n − 1} of them per target; Base's Theorem A inserts each into a
dictionary (Step 4(g) l.376-379) and counts the insertion (Step 6 l.380-383), so τ0 ≥ 1 − η. The checksum costs
2^{τ_cs n} with η − τ_cs ≤ Δ, so τ0 ≥ τ_cs ≥ η − Δ. Adding gives 2τ0 ≥ 1 − Δ. It is valid exactly in this
generality: (1) any algorithm whose work includes one operation per alias class modulo a prime of ηn bits, on
worst-case inputs; (2) a checksum at the same modulus whose certified budget η − τ_cs is at most Δ; (3) Δ is a
model quantity (the capacity of the moment format at that τ), floating, about 0.029. It says nothing about
designs that do not enumerate all alias classes, that subtract aliases through a different estimator, that use a
different modulus for the two halves, or whose checksum is not of the moment form; the paper's Section 10 lists
these. Numerical nit: at the certified point Δ = 0.0286969, so (1 − Δ)/2 = 0.48565; the text's 0.4858 uses
Δ ≈ 0.0284 (the table's 0.4858019 corresponds to Δ = 0.0283962). State which Δ the floor is quoted at. My
model's overhead-removal table at the point's Δ is 0.4875741 / 0.4871563 / 0.4867011 / 0.4862020 / 0.4856515,
reaching (1 − Δ)/2 exactly at full removal; the paper's values differ by up to 1.5e-4 because its model
re-optimizes the filter (Δ moves), which should be said next to the table.

### 4c. The overhead equals −log2 Pr[disjoint masks] — PASS

Exact identity for finite m: Pr[X ∩ Y = ∅] = C(m − k, σ − k)/C(m, σ − k) = C(m, σ)C(σ, k)/(C(m, k)C(m, σ − k)),
verified in exact rationals; the entropy limit of −(1/m)log2 Pr is h(a) + h(1/2 − a) − 1 − h(2a)/2, which is
the C4 overhead with γ = h(2a)/2 (C1 tight). At the point: overhead 0.0038460 (γ as given), 0.0038454
(γ = h(2a)/2), finite m = 1e7 gives 0.0038454; aμ = 0.0039150 ("about one bit per left-mask element"). All match.

### 4d. Colour-coding formula — UNCLEAR as written, conclusion correct

With left masks confined to R, |R| = ρm, C1 becomes γ ≤ (ρ/2)h(2a/ρ) and h(a) becomes ρh(a/ρ) in C2 and C4.
The overhead is then ρh(a/ρ) − (ρ/2)h(2a/ρ) + h(1/2 − a) − 1. The expansion of the first two terms is
a + a²/(2ρ ln 2) + O(a³), which is the paper's formula; but h(1/2 − a) − 1 = −2a²/ln 2 + O(a⁴) is missing. At
a = 0.0082 the missing term (−1.96e-4 per m) is four times the ρ-dependent term (4.9e-5/ρ); the stated formula
gives 0.008287 against the true 0.008091 at ρ = 1 (`scripts/out/section9.txt`, Part 3). Since the missing term
does not depend on ρ, "smallest at ρ = 1" is right, and my fixed-Δ model gives penalties +1.5e-4, +4.2e-4, +1.2e-3
at ρ = 0.75, 0.5, 0.25 (paper 1.4e-4, 4.0e-4, 1.2e-3). Either call the formula the left-mask part, or add the term.

### 4e. Other Section 9 numbers (information)

My fixed-Δ model gives dτ0/dΔ = −0.417 (paper −0.39 with the filter re-optimized) and shadow prices
C4 0.417, C1 0.276, C2 0.082, C3 0.082, C5 0.001 (paper 0.389 / 0.258 / 0.077 / 0.077 / 0.001). Same ordering
and sizes; the paper's are 7 % lower because its filter absorbs part of each relaxation. Not certified; consistent.

---

## Conditions missed, overclaims, and required changes

Missed conditions: none that would change a verdict. For item 2 the Section 2 table should make two inequalities
strict (cap > 1/2 − d1; the Markov inequality in the limit), and for item 1 the certificate should mark the two
OpenAI caps as not required. The list of 33 conditions above is what I derive; the paper's "34" presumably counts
one of mine twice or includes S5 (always true).

Overclaims or imprecise wording:
1. "0.4875754" as the exponent (abstract, Section 1 table, Section 8, contribution 1): the proved exponent is
   0.4875754036, so the claim must be 0.4875755 or "every T' > 0.4875754036". Required change.
2. "Three-way balance" and the quoted bounds/τ0 in Section 9 refer to the floating optimum 0.4875749, not the frozen
   point. Say so, or recompute at the frozen point (0.4875739 / 0.4875745 / 0.4875745 against 0.4875752).
3. The colour-coding expansion is for the left-mask part only (4d).
4. The floor's 0.4858 uses Δ = 0.0284 while the certified point has Δ = 0.0287 (floor 0.48565).
5. "Thin slacks only make the cutoff astronomically large": true, but give the order (n_* ≳ 1e17 for the Base point,
   ≳ 1e18 for the K16 point from Chebyshev with d0 − d1 = 1e-9).
6. Status table, Section 5: "0.48 blocked ... follows from Lemma 1 at the eight-block point" under-claims; the
   three-constraint argument above makes it rigorous for all parameters.
7. Base constants that the write-up must update (δ, S3's 0.129, ε0, guard, c_z, the B3 exponent): the paper says
   "several"; list them.

Not checked here (outside items 1-4): Section 3's 430 JoshuaQFEX premises, the floating Sections 6 and 10, and the
non-numerical parts of Base (Theorem A accounting, Lemma A5, Corollary D) and of OpenAI, on which both results
remain conditional.

## Scripts

| Script | What it does | Output |
| --- | --- | --- |
| `scripts/moments_arb.py` | rigorous M1/M2 evaluator (arb); run alone for the OpenAI Table 1 control | `out/control_openai.txt` |
| `scripts/check_base_point.py [N...]` | item 1: all conditions + moments for `candidate_base.json` | `out/base_point_N4096_8192.txt` |
| `scripts/check_k16_point.py [N...]` | item 2: all conditions + moments + orientation experiments | `out/k16_point_N4096_8192.txt` |
| `scripts/float_crosscheck.py` | independent double-precision grid evaluation of both moments | `out/float_crosscheck.txt` |
| `scripts/lemma1_check.py` | item 3: closed form, adversarial tests, rigorous Φ minimum, Dmax, three-constraint floor, P = 4 | `out/lemma1.txt`, `out/lemma1_partB.txt` |
| `scripts/section9_check.py` | item 4: Base control, three bounds, overlap identity, colour-coding, floor, fixed-Δ model | `out/section9.txt`, `out/section9_part4.txt` |
| (inline, recorded) | strip sensitivity and coefficient bounds | `out/sensitivity_and_bounds.txt` |
