# Mathematical checks supplementing the referee report

PROVED — The arguments below are direct derivations in this review. They establish specified local claims, not the whole imported OpenAI/Base algorithm. I previously worked on the k=1,t=2 case in round 6; that argument is not an independent rediscovery.

## The three reduced bounds and the overlap term

PROVED — Put r=1-mu-ell and Delta=eta-tau0. Adding Base C2 and C3 gives 2tau0>1+mu(h(a)-2gamma), which is bound (i). Substituting eta=tau0+Delta into C4 gives bound (ii). Rearranging C5 gives bound (iii). These are necessary consequences of the sufficient scalar conditions, not three equivalent replacements for the entire condition list.

PROVED — For independent uniform masks A,B of sizes k and sigma-k in an m-element block, sigma=m/2,

    Pr[A cap B is empty]
      = binom(m-k,sigma-k)/binom(m,sigma-k)
      = binom(m,sigma) binom(sigma,k) /
        [binom(m,k) binom(m,sigma-k)].

Stirling's formula, k=am+O(1), gives negative log probability divided by n:

    mu [ h(a)+h(1/2-a)-1-h(2a)/2 ] + O(log n/n).

The C4 overhead is instead

    mu [ h(a)+h(1/2-a)-1-gamma ].

PROVED — Their difference is mu[h(2a)/2-gamma], strictly positive at the certified point. It exceeds 0.00000062544652673151 there. Thus the overhead equals overlap loss only at the limiting representation rate gamma=h(2a)/2. The current paper both mentions that limit and nevertheless calls the two expressions exactly equal at its frozen point; the latter wording should be corrected.

## What the counting floor proves

PROVED — If an enumeration phase really emits A_n distinct classes, it costs at least A_n output operations. Under the additional premise log2 A_n/n >=1-eta-o(1), and checksum relation eta-tau<=Delta, one obtains

    tau >=1-eta >=1-tau-Delta,
    tau >=(1-Delta)/2.

PROVED — Distinct subset sums alone do not imply the missing premise for each target residue. For a fixed prime P, weights P,2P,4P,... have distinct subset sums, but a target congruent to 1 modulo P has no aliases. Conversely, powers of two give consecutive subset sums and nearly uniform residue counts, illustrating how to prove the output count for a specified enumeration instance. Neither observation alone proves that every full algorithm, including its preprocessing, must reach such a costly phase. The main text should state the operational assumptions or provide that additional worst-case argument.

NOT CHECKED — A global upper bound of approximately 0.029 for checksum capacity has not been proved in this review or in the manuscript's displayed arguments. A fixed-capacity counting implication cannot promote the best numerically achieved capacity into a universal algorithmic floor.

## Lemma S, P2, and the Q implication

PROVED — For Sigma_j the set of j-subset sums, write a_j=|Sigma_j|/binom(m,j). Then

    2^-d(M) = |union_j Sigma_j|/2^m
             <= sum_j binom(m,j)a_j/2^m.

If a_j<=P(m)a_k on [k,m-k], the interior is at most P(m)a_k. The binomial tail bound gives at most 2*2^-m(1-h(k/m)) outside. For h(k/m)<=1/2, this is at most 2*2^-mh(k/m)<=2a_k, since a_k>=1/binom(m,k)>=2^-mh(k/m). Thus C_S=P+2 works. At k=0 the empty tail can be handled directly.

PROVED — To prove P2, choose one witness X_y for each t-sum y. The map (y,A) to (w(A),X_y minus A), for A a k-subset of X_y, is injective: the image determines y, hence its chosen witness X_y, hence A. Counting gives s_t binom(t,k)<=s_k binom(m,t-k), and the stated ratio follows.

PROVED — In the Q definition the sampled k-sum distribution is supported on s_k values. Therefore cp>=1/s_k and Q>=a_t/a_k. Q<=1 implies a_t<=a_k. Complementation a_t=a_(m-t) extends the range from t<=m/2 to [k,m-k]. For k<=m/4, t<=m/2 implies t+2k<=m, so a correctly formulated YP-Hall theorem in that domain would cover the Q conjecture. A theorem only for k=1 does not prove the general Q conjecture.

## The k=1 class criterion

PROVED — Let s=s_t, C=binom(m-1,t-1), and M_c=sum_X |X cap c|/f(X). Then sum_c M_c=t s and the weight-class distribution is M_c/(ts). Consequently

    Q = [m/(t^2 s binom(m,t))] sum_c M_c^2,
    Q<=1 iff sum_c M_c(M_c-C)<=0.

This establishes the displayed equivalence in the proposition.

### Part (i), the Q inequality at t=2

PROVED — Let r be the number of equal-weight classes. A cross-class profile c,d contributes at most 1 to M_c, because it has n_c n_d witnesses and its sum fiber has at least that size. An internal profile contributes at most 2. Thus M_c<=r-1 for singletons and M_c<=r+1 for repeated classes.

PROVED — If there are at least two repeated pairs, or a class of size at least three, r<=m-2, so every M_c<=m-1=C. The remaining problematic case is one repeated pair and otherwise singleton classes. If the pair's internal sum has another witness its internal contribution is at most 1, again giving M_c<=C. Otherwise shift its value to zero. There are G=m-2 distinct nonzero singleton values, with no opposite pair (which would give another zero-sum witness). The distinct two-sums include zero and all G singleton values, and at least one further sum: use the two largest positive values or two smallest negative values when available; the only remaining case has two singleton values of opposite signs, whose nonzero sum is different from both. Hence s>=G+2=m.

PROVED — Write x=M_pair<=m. Singleton classes have M_i<=m-2. Their total deficit is at least sum_i M_i=2s-x>=2m-x. When x>C, x lies in (m-1,m], and

    2m-x - x(x-m+1) = (m-x)(x+2) >=0.

They therefore pay the pair's excess. This proves Q<=1. It does not by itself prove the stronger YP-Hall assertion; that requires the charging construction, absent from the current paper's sketch.

### Part (ii), two distinct weight values

PROVED — Suppose the multiplicities are a<=b, a+b=m>=2t, so b>=t. After affine normalization the values are 0 and 1. Let A=min(a,t). There are A+1 different t-sums, with class totals

    M_0=A(A+1)/2,
    M_1=(A+1)(t-A/2).

The class criterion becomes

    (A+1)[A^2+(2t-A)^2] <=4Ct.

PROVED — For t>=2 the left side is strictly increasing as a real function of A: its derivative is 6A^2+(4-8t)A+4t^2-4t, which has negative discriminant and positive leading coefficient. Since A<=t, it is at most 2t^2(t+1). Also C>=binom(2t-1,t-1)>=t(t+1)/2. The last inequality holds at t=2 and follows inductively, with strictness thereafter, from the ratio 2(2t+1)/(t+1). Equality therefore requires t=2,m=4,a=b=2. This proves the stated family, provided equality is described up to affine change of weights and permutation.

### Part (iii), a repeated pair among generic singleton values

PROVED — Interpret “generic” as: at the fixed layer t, the only equal sums come from exchanging the repeated pair. This is the property needed for the counting argument; distinct singleton weights alone do not suffice. Shift the repeated value to zero and let G=m-2. Adopt binom(G,j)=0 outside 0<=j<=G. Put

    A=binom(G,t-2), B=binom(G,t-1),
    M_0=B+2A,
    M_i=binom(G-1,t-1)+binom(G-1,t-2)+binom(G-1,t-3),
    C=B+A.

Here M_0 is the repeated class total and M_i is the common singleton total. Pascal's identity gives M_i>=B and C-M_i=binom(G-1,t-2). Consequently the total excess is

    M_0 A - G M_i binom(G-1,t-2)
      = M_0 A - (t-1)B M_i.

PROVED — Since G>=2t-2,

    A/B=(t-1)/(G-t+2) <=(t-1)/t,
    M_0 A <= (t-1)B^2(3t-2)/t^2
            <=(t-1)B^2 <=(t-1)B M_i.

Equality requires t=2,G=2. This proves the family and its affine-normalized equality case. For t>=3 the inequality is strict.

EVIDENCE — These short proofs would make parts (ii) and (iii) publishable without relying on exhaustive tests. The Hall proof for part (i) still needs to be incorporated from its original proof artifact, with complete demands, capacities and admissible edges.
