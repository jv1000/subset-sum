"""B2: certificate for candidate_ternary.json (Base's alias step with ternary left masks, conditional on [S]).

Every condition is derived in ROUND2_REPORT.md (Section B) from base_PROOF_0.4877.tex with line numbers; the
ternary changes replace Base's (C1), (C2), (C4), (C5), (C7), (S1)-(S4), Lemma A4/A5's delta by their analogues.
Ball arithmetic at 200 bits; PASS only if the whole ball satisfies the strict inequality.

Usage: python -I scripts/round2/check_ternary_point.py [N ...]   (default 4096 8192)
"""
import sys, json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'scripts'))      # Fable_review/scripts (moments_arb.py)
from flint import arb
from moments_arb import S, set_prec, filter_scores, moments, load_filter

set_prec(200)
A = arb
ln2 = A(2).log()
log2 = lambda t: t.log() / ln2
h = lambda x: -(x * x.log() + (1 - x) * (1 - x).log()) / ln2
def H3(x, y):                                   # ternary entropy of the left masks: fractions x (+1), y (-1), 1-x-y (0)
    z = 1 - x - y
    return -(x * x.log() + y * y.log() + z * z.log()) / ln2

J = json.load(open(os.path.join(HERE, '..', '..', 'candidate_ternary.json')))
tau0, eta, mu, a, c, gam, l = (S(J[k]) for k in ("tau0", "eta", "mu", "a", "c", "gamma", "l"))
kappa, p, q = S(J["kappa"]), S(J["p"]), S(J["q_m"])
eps, zeta, guard = S(J["epsilon"]), S(J["zeta"]), S(J["input_guard_coefficient"])
r = 1 - mu - l
Delta, Gamma = eta - tau0, 2 * tau0 - eta
aG = Delta / Gamma
half = A(1) / 2
ap = a + c                                      # a' = k'/m, k' = k1 + k2
HL = H3(a, c)                                   # log2(#left masks)/m  (multinomial m; k1, k2, rest)
HR = h(half - a + c)                            # log2(#right masks)/m (|Y| = sigma - k1 + k2)
rho_f = eta - S("1.5e-6"); rho_c = rho_f - S("1e-6")
T = tau0 + 20 * eps
A4 = mu * (h(2 * ap) + 2 * ap)                  # log2(#vectors in {-1,0,1}^M with <= 2k' nonzeros)/n

conds = []
add = lambda name, cite, slack: conds.append((name, cite, slack))
# --- alias step (Section B of the report; Base line numbers for the unchanged parts) ---
add("C1R  gamma < h(2a)/2 + h(2c)/2  (P' <= C(sigma,k1)C(sigma,k2))", "T5 step 4 (Base l.520-521 with the new representation count)", h(2 * a) / 2 + h(2 * c) / 2 - gam)
add("C2R  l + (H3(a,c) - gamma) mu < tau0", "T6 item 5 (Base l.566-568; trials 2^{d(M)} <= 2^{d(L)+2n^0.6})", tau0 - (l + (HL - gam) * mu))
add("C3   r + (1 - gamma) mu < tau0", "T6 item 6 (Base l.569-572, unchanged)", tau0 - (r + (1 - gam) * mu))
add("C4R  1 - mu + (H3(a,c) + h(1/2-a+c) - gamma) mu - eta < tau0", "T6 item 7 (Base l.573-589)", tau0 - (1 - mu + (HL + HR - gam) * mu - eta))
add("C5R  h(1/2-a+c) mu + 1/2 - tau0 < tau0  (right masks x trials)", "T6 item 2 (Base l.558-560)", tau0 - (HR * mu + half - tau0))
add("C5L  H3(a,c) mu + 1/2 - tau0 < tau0  (left masks x trials)", "T6 item 2", tau0 - (HL * mu + half - tau0))
add("C6a  0 < r", "Base l.166", r)
add("C6b  r < tau0", "Base l.166", tau0 - r)
add("C6c  l < tau0", "Base l.166", tau0 - l)
add("MU1  mu < l  (d(L) >= d(M) - 2n^0.6 whp, replaces C7)", "T3/T6 (Base (F3) l.207-211)", l - mu)
add("MU2  mu <= 1/2 (d(M) <= f(n/2)+n^0.6 under (LD), replaces S2)", "T3 (Base l.283-299)", half - mu)
add("A4R  mu(h(2a') + 2a') < eta  (all <= 2k'-sparse relations survive mod P)", "T4 (Base l.464-482 with 3^sigma -> sum_{j<=2k'} C(m,j)2^j)", eta - A4)
add("A4R' 2a' <= 1/2 (entropy bound for the vector count)", "T4", half - 2 * ap)
add("A4R'' 1/guard < eta - A4  (o(1) under the guard)", "T4", eta - A4 - 1 / guard)
add("SR   k' = a' m <= 0.11 m  (range of [S] via monotonicity)", "Lemma S (report Section A)", S("0.11") - ap)
C = [cd for cd in conds if cd[0][:3] in ("C1R", "C2R", "C3 ", "C4R", "C5R", "C5L", "C6a", "C6b", "C6c", "MU1", "MU2", "A4R")]
eps0 = min((cd[2] for cd in C), key=lambda b: float(b.lower()))
eps0_lo = A(eps0.lower())
print(f"eps0 (least slack of the alias constraints, lower end) = {eps0.str(6)}")
add("A7.1 l < tau0 - eps0", "T6 item 1 (Base l.556-557)", tau0 - eps0_lo - l)
add("A7.1 r < tau0 - eps0", "T6 item 1", tau0 - eps0_lo - r)
add("A7.1 mu < tau0 - eps0  (value maps; exact |Sigma(M)| costs 2^{m-d(M)})", "T3, T6 item 1", tau0 - eps0_lo - mu)
add("A7.3 1/2 - tau0 + gamma mu/2 < tau0 - eps0  (small primes)", "T6 item 3 (Base l.561-563)", tau0 - eps0_lo - (half - tau0 + gam * mu / 2))
add("A7.4 r + 1/2 - tau0 < tau0 - eps0  (sorting keys)", "T6 item 4 (Base l.564-565)", tau0 - eps0_lo - (r + half - tau0))
add("ThmA 1/guard + zeta < eps0", "Theorem A' proof (Base l.605-607)", eps0_lo - (1 / guard + zeta))
add("P    tau0 < 1/2", "Base Prop. P l.281-285", half - tau0)
add("prime draw eta/2 < tau0 + 20 eps", "Base l.795", T - eta / 2)
# --- checksum (unchanged from the Section 8 certificate) ---
add("Delta > 0", "Base l.141", Delta)
add("Gamma > 0", "Base l.142", Gamma)
add("B2   a_Gamma <= 3/4", "Base Lemma B2 l.703-705", A(3) / 4 - aG)
add("B2   p >= 1", "Base l.709-710", p - 1)
add("B2   q >= 1", "Base l.712", q - 1)
add("B1   rho_c < rho_f", "Base Lemma B1 l.651-659", rho_f - rho_c)
add("B3   rho_f + (18 + 6p) eps < eta", "Base Lemma B3 l.719-733", eta - rho_f - (18 + 6 * p) * eps)
add("B3   rho_f + (18 + 6q) eps < eta", "Base Lemma B3", eta - rho_f - (18 + 6 * q) * eps)
info = [("C8 (mu/2) log2 3 < eta  [not needed: A4R replaces Lemma A4; kept for information]", eta - (mu / 2) * (A(3).log() / ln2)),
        ("A5R 1/2 - tau0 + zeta < (eta - A4)/2  [not needed, see T4; information]", (eta - A4) / 2 - (half - tau0 + zeta)),
        ("3p <= 30 [OpenAI-only]", 30 - 3 * p), ("q(4a+3) <= 30 [OpenAI-only]", 30 - q * (4 * aG + 3))]

r_tp, s_tp, kap = load_filter(J)
Ns = [int(x) for x in sys.argv[1:]] or [4096, 8192]
sigma, beta = S("0.3"), S("0.1")
res = {}
for N in Ns:
    t0 = time.time()
    sc = filter_scores(r_tp, s_tp, kappa, N, sigma, beta)
    M1, M2, l1, l2 = moments(sc, kappa, Delta, Gamma, p, q, N, beta)
    res[N] = (l1, l2)
    print(f"N={N}: log2 M1 = {l1.str(20)}   log2 M2 = {l2.str(20)}   ({time.time()-t0:.0f}s)")
N = Ns[-1]; l1, l2 = res[N]
add(f"M1   log2 M1 < rho_c  (N={N})", "Base Prop. B with z=(p,0)", rho_c - l1)
add(f"M2   log2 M2 < rho_c  (N={N})", "Base Prop. B with z=(q,0,0)", rho_c - l2)
if len(Ns) > 1:
    print(f"resolution check: |d log2 M1| <= {abs(res[Ns[0]][0] - l1).str(3)}, |d log2 M2| <= {abs(res[Ns[0]][1] - l2).str(3)}")

print("\n=== conditions for candidate_ternary.json ===")
allok = True
for name, cite, slack in conds:
    ok = bool(slack > 0); allok &= ok
    print(f"{'PASS' if ok else 'FAIL'}  {name:70s} slack {slack.str(6):28s}  [{cite}]")
for name, val in info:
    print(f"info  {name:70s} slack {val.str(6)}")
print(f"\nT = tau0 + 20 eps = {T.str(15)}; Delta = {Delta.str(12)} Gamma = {Gamma.str(12)} a_Gamma = {aG.str(10)} rho_c = {rho_c.str(12)}")
print(f"a' = a + c = {ap.str(10)}; H3(a,c) = {HL.str(10)}; h(1/2-a+c) = {HR.str(10)}; A4 = {A4.str(10)}")
print(f"true ball radii: rad(log2 M1) = {l1.rad().str(3)}, rad(log2 M2) = {l2.rad().str(3)}")
print("ALL CONDITIONS PASS" if allok else "SOME CONDITION FAILS")
