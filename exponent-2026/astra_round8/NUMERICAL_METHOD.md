# Independent numerical audit: method and limits

PROVED — All decimal candidate parameters used in this audit are parsed from their string fields, not from `floating_T` or `floating_margins`. `audit_numbers.py` uses exact rational arithmetic for exponents and differences and directed intervals for logarithms and entropy. `verify_moments.py` uses my own FFT and analytic error estimates, originally written in round 6 and copied into `interval_core.py`. No supplied verifier or B script was used. The numerical conclusions trust Python integer arithmetic and mpmath's interval elementary functions; this is a rigorous numerical certificate, not a formally verified implementation.

## Exact exponent accounting

PROVED — The following are exact decimal thresholds, followed by safe strictly larger exponents for ordinary big-O bounds on polynomial-bit inputs:

| Candidate | Exact threshold T | Safe displayed exponent |
|---|---:|---:|
| Base, one filter | 0.4875754036 | 0.4875755 |
| OpenAI, K=16 | 0.4894615727 | 0.4894616 |
| Ternary, additionally assuming [S] | 0.4873407528 | 0.4873408 |

PROVED — The exact improvements are: Joshua's quoted 0.487676 minus the Base candidate, 0.0001005964; Base candidate minus ternary, 0.0002346508; Joshua minus ternary, 0.0003352472. Thus the paper's conservative gaps 1.005e-4, 2.34e-4 and 3.35e-4 do not overstate these differences. The difference from Base's quoted final exponent 0.4877 is 0.0001245964; from its internal tau0=0.48769 it is 0.0001145964. These two comparisons must not be conflated.

## Moment formula and orientation

PROVED — Write F=2^r, G=2^s, with normalized circle measure, and

    C(x) = mean_w F(x+w)G(w),
    H(x) = mean_w F(x+w)G(w)(r(x+w)+s(w)),
    K = log2(mean 2^(kappa r)) + log2(mean 2^(kappa s)).

The score functions simplify exactly to

    D = H/C - log2 C,
    u = (kappa-1) H/C + log2 C - K,
    v = (2-kappa) H/C - 2 log2 C + K.

PROVED — The code computes C and H with correlation, not convolution: Fourier index j of the first factor multiplies index -j of the second. The independent eight-entry, asymmetric integer control checks every output against the defining finite sum. This matters because the frozen densities contain sine terms. The zero-filter control gives u=v=D=0, and binary entropy at 1/2 encloses 1.

## Analytic quadrature bounds

PROVED — For a trigonometric polynomial r, let c_j=|r_cos,j|+|r_sin,j|. For strip half-width s put

    R=sum c_j,  R_s=sum c_j cosh(js),
    A=sum c_j(cosh(js)-1),  B=sum c_j sinh(js).

For z=x+iy, |y|<=s, |Re r(z+w)-r(x+w)|<=A, |Im r(z+w)|<=B and |r(z+w)|<=R_s. Define S and S_s similarly for the second polynomial. On the outer strip, only the first factor is shifted into the complex plane. With theta=(ln 2)B<pi/2, C(z) stays in the sector |arg C|<=theta and is nonzero. In particular

    |H(z)/C(z)| <= 2^(2A)(R_s+S)/cos(theta) = H_b,
    |log2 C(z)| <= R+S+A-log2 cos(theta)+B = L_b.

The analytic logarithm is therefore well defined. Since |K|<=kappa(R+S)=K_b, bounds for the two scores are

    U_b=|kappa-1|H_b+L_b+K_b,
    V_b=|2-kappa|H_b+2L_b+K_b.

PROVED — The N-point periodic trapezoidal rule for a function analytic on |Im z|<=s and bounded by B_0 there has error at most 2B_0/(exp(sN)-1), from summing its Fourier-coefficient bounds at nonzero multiples of N. Apply this with outer s=0.04 and

    B_1=(2+2cosh s) 2^[p(Delta+U_b)],
    B_2=(2+2cosh s) 2^[q(a_Gamma V_b+U_b)].

PROVED — For the inner quadratures take s_i=0.1; shifting w moves both polynomial arguments. Bounds for the integrands C,H,Z_r,Z_s are respectively

    2^(R_i+S_i),  2^(R_i+S_i)(R_i+S_i),
    2^(kappa R_i),  2^(kappa S_i).

The code inflates each discrete inner integral by its analytic error before dividing or taking logarithms, checks positive real denominators, then inflates the final outer sums. Thus FFT rounding and both levels of discretization are enclosed; agreement of two meshes is not being used as an error proof. All computation used N=4096 and 50 interval decimal digits. Exported endpoints are rounded outward by exact integer division of the binary endpoints.

## Certified results

PROVED — These shorter intervals are widened outward from the machine-readable results; all comparisons below are strict:

| Candidate | log2 M1 enclosure | log2 M2 enclosure | rho_c |
|---|---|---|---:|
| Base | [0.51626832585128515043, 0.51626832585128515044] | [0.51626814726466968639, 0.51626814726466968640] | 0.5162696413 |
| K16 | [0.51847757618968867872, 0.51847757618968867873] | [0.51847734723194144144, 0.51847734723194144145] | 0.5184784240 |
| Ternary | [0.51599187405865778647, 0.51599187405865778648] | [0.51599162047014794189, 0.51599162047014794190] | 0.5159949155 |

PROVED — For the Base point the moment slacks exceed 1.3154487148e-6 and 1.4940353303e-6. Its least C1–C8 slack is C4, enclosed by [1.31567023384168025906847261644e-6, 1.31567023384168025906847261645e-6]. A safe concise lower bound is 1.3156e-6, not 1.3157e-6. The B3 margin is at least 8.12458704e-7. Exact scalar outputs, including the other two candidates, are in `numbers.json`.

PROVED — The frozen Base point has Delta=0.0286969377, hence (1-Delta)/2=0.48565153115. Its three reduced scalar bounds are enclosed by [0.48757388786628705556,0.48757388786628705557], [0.48757454576488307915,0.48757454576488307916], and [0.48757454571492742019,0.48757454571492742020]. These are lower bounds, not running-time exponents.

## All-parameter obstruction in the stated budget

PROVED — Let h=h_2(1/4), g_0=10^-5 denote the guard, and G(p)=(1+p)log2 mean(1+cos x)^(1/(1+p)). If tau<1/2 is feasible, the list inequality implies gamma+1/2-h>0 and

    mu >= (1/2-tau)/(gamma+1/2-h)
        >= (1/2-tau)/(1-h),

because gamma<1/2. The pair inequality then gives

    Delta >= 1-2tau+(2h-3/2)mu+g_0
          >= C(1/2-tau)+g_0,
    C=1/[2(1-h)].

Here 2h-3/2>0. The first-moment certificate requires log2 M1<eta=tau+Delta. Lemma 1 instead gives the necessary condition

    0 > 1-tau+(p-1)Delta+G(p)
      >= 1-tau+(p-1)[C(1/2-tau)+g_0]+G(p).

PROVED — For p>=1 this last expression decreases as tau increases. Therefore it suffices to prove positivity at tau=0.484. Also G is nonincreasing by monotonicity of power means. On each cell [p_L,p_R] of length 0.001 in [1,10], use the rigorous lower bound

    1-0.484+(p_L-1)Delta_min+G(p_R).

`verify_blocking.py` evaluates G through the gamma-function formula in Lemma 1 using directed intervals. All 9,000 cell lower bounds are positive; the minimum exceeds 0.00461138323631. The p=1 endpoint is treated directly (no division by p-1), and has margin greater than 0.21300774105536. Its elementary gamma identity and the p=0 normalization are controls. This proves infeasibility for all tau<=0.484 and p in [1,10], independently of K. It does not prove a lower bound for algorithms outside these sufficient inequalities.

## Limits and reproducibility

EVIDENCE — Each numerical run took seconds, not minutes; all ran sequentially. Commands are `python audit_numbers.py`, `python verify_blocking.py`, and `python verify_moments.py --candidate NAME --n 4096`, with NAME base, K16 or ternary. Scripts set no multiprocessing. Dependencies are Python and mpmath; the separate document-inspection scripts use PyMuPDF and Pillow. The copied interval module is a library here; its old standalone round-6 entry point is not used.

NOT CHECKED — This audit does not rerun all 430 historical certificates, optimizer searches, shadow prices, negative-result experiments, large multiset sweeps or flow sweeps. Those are not reproducible from the candidate files alone. Their manuscript values should be tied to versioned inputs and output records, not treated as freshly established by this audit.
