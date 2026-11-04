"""Referee check of every scalar condition of Base (PROOF_0.4877.tex) at the candidate JSON, in Arb ball arithmetic."""
from flint import arb, ctx
import json, sys
ctx.prec = 256
P = json.load(open(sys.argv[1]))
Q = lambda x: arb(str(x))
tau0, eta, a, mu, gam, l = (Q(P[k]) for k in ("tau0", "eta", "a", "mu", "gamma", "l"))
eps, zeta = Q(P["epsilon"]), Q(P["zeta"])
guard = Q(P["input_guard_coefficient"])
p, q = Q(P["p"]), Q(P["q_m"])
r = 1 - mu - l
ln2 = arb(2).log()
def h(x): return -(x*x.log() + (1-x)*(1-x).log())/ln2
half = Q("0.5")
log2_3 = arb(3).log()/ln2
Delta = eta - tau0; Gamma = 2*tau0 - eta; aG = Delta/Gamma
rho_f = eta - Q("1.5e-6"); rho_c = rho_f - Q("1e-6")

rows = []  # (name, lhs, rhs, source)  meaning lhs < rhs required
def need(name, lhs, rhs, src): rows.append((name, lhs, rhs, src))

need("C1 gamma < h(2a)/2", gam, h(2*a)/2, "l.165")
need("C2 l+(h(a)-gamma)mu < tau0", l + (h(a)-gam)*mu, tau0, "l.166")
need("C3 r+(1-gamma)mu < tau0", r + (1-gam)*mu, tau0, "l.167")
need("C4 1-mu+(h(a)+h(1/2-a)-gamma)mu-eta < tau0", 1 - mu + (h(a)+h(half-a)-gam)*mu - eta, tau0, "l.168")
need("C5 h(1/2-a)mu+1/2-tau0 < tau0", h(half-a)*mu + half - tau0, tau0, "l.169")
need("C6a 0 < r", arb(0), r, "l.170")
need("C6b r < tau0", r, tau0, "l.170")
need("C6c l < tau0", l, tau0, "l.170")
need("C7 mu(1-2a) < l", mu*(1-2*a), l, "l.171")
need("C8 (mu/2)log3 < eta", mu/2*log2_3, eta, "l.172")
C = {n: (rhs - lhs) for n, lhs, rhs, s in rows}
eps0 = min(C.values(), key=lambda x: float(x.lower()))
# further conditions
need("left masks h(a)mu+1/2-tau0 < tau0 (A7 item 2, D.1)", h(a)*mu + half - tau0, tau0, "l.558, D.1")
need("S1 4a < 1", 4*a, arb(1), "l.185")
need("S2 mu(1-2a) < 1/2", mu*(1-2*a), half, "l.186")
need("S3 h(2a)/2+h(a) < 1-2a", h(2*a)/2 + h(a), 1-2*a, "l.187-188")
need("S5 h(a) < h(1/2-a) (left masks implied by C5)", h(a), h(half-a), "l.837")
need("A5: 1/2-tau0+zeta < delta=(eta-(mu/2)log3)/2", half - tau0 + zeta, (eta - mu/2*log2_3)/2, "l.465,506")
need("A7 item1/6: mu < tau0 - eps0", mu, tau0 - eps0, "l.556,570")
need("A7 item1: mu(1-2a) < tau0-eps0", mu*(1-2*a), tau0 - eps0, "l.556")
need("A7 item1: l < tau0-eps0", l, tau0 - eps0, "l.556")
need("A7 item1: r < tau0-eps0", r, tau0 - eps0, "l.556")
need("A7 item3: 1/2-tau0+zeta+gamma mu/2 < tau0-eps0+zeta", half - tau0 + zeta + gam*mu/2, tau0 - eps0 + zeta, "l.562 (unlisted)")
need("A7 item4: r+1/2-tau0+zeta < tau0-eps0+zeta", r + half - tau0 + zeta, tau0 - eps0 + zeta, "l.564 (unlisted)")
need("A7 item4: l < tau0-eps0+zeta", l, tau0 - eps0 + zeta, "l.564")
need("Thm A cap (l.603): 1/guard + zeta < eps0", 1/guard + zeta, eps0, "l.177,603")
need("Prime P trial division: eta/2 < tau0", eta/2, tau0, "l.801")
need("Delta > 0", arb(0), Delta, "B.3")
need("Gamma > 0", arb(0), Gamma, "B.3")
need("a_Gamma <= 3/4 (row error (4a+3)eps <= 6eps)", aG, Q("0.75"), "l.703")
need("B2 rho0: z0 = p >= 1 (strict here)", arb(1), p + Q("1e-30"), "l.639,711")
need("B2 rho_i: z0 b_{i-1} = q*1 >= 1", arb(1), q + Q("1e-30"), "l.639,715")
cz = 6*max(p, q) if p > q else 6*q
need("B3: (18+c_z)eps < eta-rho_f, c_z=6p", (18 + 6*p)*eps, eta - rho_f, "l.723-733")
need("B3: (18+c_z)eps < eta-rho_f, c_z=6q", (18 + 6*q)*eps, eta - rho_f, "l.723-733")
need("B1 slack rho_c < rho_f", rho_c, rho_f, "l.659")
need("final: tau0+20eps < 0.48767595 (Joshua)", tau0 + 20*eps, Q("0.48767595"), "claim")

ok = True
print(f"{'condition':58s} {'slack (rhs-lhs)':>30s}  src")
for n, lhs, rhs, s in rows:
    sl = rhs - lhs
    good = bool(lhs < rhs)
    ok &= good
    print(f"{('PASS ' if good else 'FAIL ') + n:58s} {sl.str(8):>30s}  {s}")
print("eps0 (least slack C1-C8) =", eps0.str(10))
print("which:", min(C, key=lambda k: float(C[k].lower())))
print("Delta =", Delta.str(12), " Gamma =", Gamma.str(12), " aG =", aG.str(12))
print("delta =", ((eta - mu/2*log2_3)/2).str(10))
print("rho_c =", rho_c.str(14), " rho_f =", rho_f.str(14))
print("T = tau0+20eps =", (tau0 + 20*eps).str(14))
print("B3 decay exponent with c_z=6p:", ((18 + 6*p)*eps - (eta - rho_f)).str(8))
print("ALL PASS" if ok else "SOME FAIL")
