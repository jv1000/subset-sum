"""B1: freeze the C19 floating optimum (ternary masks, conditional on [S]) to exact decimals.
Choice (noted): parameters to 10 decimals, kappa/p/q and filter coefficients to 8 decimals (as candidate_base.json),
tau0 raised by BUMP (default 3e-7, as the Section 8 point: floating 0.4875749036 -> frozen 0.4875752036) and then
rounded UP to 10 decimals; eps = zeta = 1e-8, guard 1e8, rho_f = eta - 1.5e-6, rho_c = rho_f - 1e-6.
Usage: python -I scripts/round2/freeze_ternary.py [BUMP]"""
import json, sys, os
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_EVEN
HERE = os.path.dirname(os.path.abspath(__file__))
c19 = json.load(open(os.path.join(HERE, '..', '..', 'c19.json')))
best = min((o for o in c19['runs'] if o['feasible']), key=lambda o: o['tau0'])
z = best['z']; nt = 16
assert len(z) == 9 + 4 * nt + 1
BUMP = float(sys.argv[1]) if len(sys.argv) > 1 else 3e-7
def dec(x, places, up=False):
    q = Decimal(1).scaleb(-places)
    return str(Decimal(repr(x)).quantize(q, rounding=ROUND_CEILING if up else ROUND_HALF_EVEN))
tau0, eta, mu, a, gam, l, kap, p, q = z[:9]
rc, sc, c = z[9:9+2*nt], z[9+2*nt:9+4*nt], z[-1]
out = {
 "construction": "Base (a-kapila PROOF_0.4877, commit 44c34961) alias step with TERNARY left masks (k1 = a m entries +1 inside S, k2 = c m entries -1 outside S), plain right mask, ONE filter (J = 1). Conditional on [S] (layer density: a_k(M) >= 2^{-d(M)}/poly for k <= 0.11 m) and on Base's written proof.",
 "source": "Fable_round2/c19.json best feasible run (floating tau0 %.10f), frozen by scripts/round2/freeze_ternary.py with tau0 bump %.1e" % (tau0, BUMP),
 "tau0": dec(tau0 + BUMP, 10, up=True), "eta": dec(eta, 10), "mu": dec(mu, 10), "a": dec(a, 10), "c": dec(c, 10),
 "gamma": dec(gam, 10), "l": dec(l, 10), "kappa": dec(kap, 8), "p": dec(p, 8), "q_m": dec(q, 8), "n_terms": nt,
 "rc": [dec(x, 8) for x in rc], "sc": [dec(x, 8) for x in sc],
 "epsilon": "0.00000001", "zeta": "0.00000001", "input_guard_coefficient": "100000000",
 "rho_f_rule": "eta - 1.5e-6", "rho_c_rule": "rho_f - 1e-6",
 "exponent_rule": "T = tau0 + 20 eps; the algorithm runs in O(2^{T' n}) for every T' > T",
 "certificate_format": "rho0: z=(p,0); rho1..rho9: z=(q,0,0) (Base Theorem B with J = 1)"}
json.dump(out, open(os.path.join(HERE, '..', '..', 'candidate_ternary.json'), 'w'), indent=1)
print("frozen tau0 =", out['tau0'], " T =", str(Decimal(out['tau0']) + Decimal('0.0000002')), " (floating tau0 %.10f)" % tau0)
