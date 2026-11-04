"""Rigorous upper bounds for the continuous filtering moments M1, M2 (arb).

Method (independent of the author's code):
 1. Fourier coefficients of F=2^r, G=2^s, F r, G s, F^kap, G^kap from an
    Ndft-point acb DFT of ball values.  Aliasing error for |k|<=Ndft/2:
       |hat_N(k)-hat(k)| <= S(sig1) * 2 e^{-(Ndft-|k|) sig1}/(1-e^{-Ndft sig1})
    where S(sig1) bounds |func| on |Im z|=sig1, using
       Re r(t+iy) <= |r(t+iy)| <= A_r(sig1) := sum_j cosh(j sig1) sqrt(a_j^2+b_j^2).
    Tail: |hat(k)| <= S(sig1) e^{-|k| sig1}.
 2. Exact P(x)=sum_k c_k e^{ikx}, c_k = Fhat(k) Ghat(-k);
    Y(x)=sum_k d_k e^{ikx}, d_k = (Fr)hat(k) Ghat(-k) + Fhat(k) (Gs)hat(-k).
    Truncate at |k|<=Kc with rigorous tail; evaluate at the outer nodes by
    inverse acb DFT.  This encloses the TRUE P(x_j), Y(x_j), Zf, Zg, Zfk, Zgk.
 3. Node integrands h1, h2 as balls; T_N(h) as a ball.
 4. Outer trapezoid error <= 2 B0/(e^{N sig_o}-1), B0 = sup |h| on |Im z|<=sig_o'
    (sig_o' > sig_o), bounded via: for z in the strip, nearest node x_j,
    |P(z)-P(x_j)| <= sum_k |c_k| (e^{|k| rho}-1), rho = sig_o' + pi/N;
    hence Re P(z) >= P_lo > 0 (principal log analytic, no winding),
    |Y(z)| <= Y_hi; then crude bounds on Re(Delta-u), Re(a v-u).
Usage: python3 -I rigorous_moments.py N_out
"""
import json, sys
from flint import arb, acb, ctx
ctx.prec = 160

C = json.load(open('/home/claude/c3/candidate_K16.json'))
rc = [arb(t) for t in C['rc']]; sc = [arb(t) for t in C['sc']]
kap = arb(C['kappa']); p = arb(C['p']); q = arb(C['q_m'])
eta = arb(C['eta']); tau = arb(C['tau']); eps = arb('1e-8')
Delta = eta - tau; Gam = 2 * tau - eta; a = Delta / Gam
rho_f = eta - 48 * eps - arb('5e-7'); rho_c = rho_f - arb('1e-6')
LN2 = arb(2).log()
def log2(x): return x.log() / LN2
def pow2(x): return (x * LN2).exp()

Nout = int(sys.argv[1]) if len(sys.argv) > 1 else 1024
Ndft = 2048
Kc = 400
assert 2 * Kc + 1 <= Nout or Nout >= 1024
sig1 = arb('0.5')

def amp(c):
    return [((c[j] ** 2 + c[16 + j] ** 2).sqrt()) for j in range(16)]
def Abound(c, sig):
    return sum((amp(c)[j - 1] * (j * sig).cosh() for j in range(1, 17)), arb(0))

Ar1 = Abound(rc, sig1); As1 = Abound(sc, sig1)
# sup bounds on |Im z| = sig1 (upper ends)
S_F = pow2(Ar1); S_G = pow2(As1)
S_Fr = S_F * Ar1; S_Gs = S_G * As1
S_Fk = pow2(kap * Ar1); S_Gk = pow2(kap * As1)
print('A_r(0.5)=%s A_s(0.5)=%s' % (Ar1.str(6), As1.str(6)))

pi = arb.pi()
def trig_vals(c, Nn):
    out = []
    for i in range(Nn):
        t = 2 * pi * i / Nn
        v = arb(0)
        for j in range(1, 17):
            v += c[j - 1] * (j * t).cos() + c[15 + j] * (j * t).sin()
        out.append(v)
    return out
r = trig_vals(rc, Ndft); s = trig_vals(sc, Ndft)
F = [pow2(x) for x in r]; G = [pow2(x) for x in s]
Fr = [F[i] * r[i] for i in range(Ndft)]; Gs = [G[i] * s[i] for i in range(Ndft)]
Fk = [pow2(kap * x) for x in r]; Gk = [pow2(kap * x) for x in s]

def coeffs(vals, S):
    """Return function k -> acb ball containing the TRUE Fourier coefficient."""
    X = acb.dft([acb(v) for v in vals])
    e = (-sig1 * Ndft).exp()
    out = {}
    for k in range(-Kc, Kc + 1):
        alias = S * 2 * (-(Ndft - abs(k)) * sig1).exp() / (1 - e)
        c = X[k % Ndft] / Ndft
        out[k] = acb(c.real.union(c.real) + arb(0, alias.upper()), c.imag + arb(0, alias.upper()))
    return out
cF = coeffs(F, S_F); cG = coeffs(G, S_G); cFr = coeffs(Fr, S_Fr); cGs = coeffs(Gs, S_Gs)
cFk = coeffs(Fk, S_Fk); cGk = coeffs(Gk, S_Gk)
Zf = cF[0].real; Zg = cG[0].real; Zfk = cFk[0].real; Zgk = cGk[0].real
lz = log2(Zf) + log2(Zg)
H = log2(Zfk) + log2(Zgk) - kap * lz
print('Zf=%s Zg=%s Zfk=%s Zgk=%s H=%s' % (Zf.str(15), Zg.str(15), Zfk.str(15), Zgk.str(15), H.str(15)))

c = {k: cF[k] * cG[-k] for k in range(-Kc, Kc + 1)}
dd = {k: cFr[k] * cG[-k] + cF[k] * cGs[-k] for k in range(-Kc, Kc + 1)}
# tails |k|>Kc : |c_k| <= S_F S_G e^{-2|k| sig1};  |d_k| <= (S_Fr S_G + S_F S_Gs) e^{-2|k| sig1}
TP = S_F * S_G; TY = S_Fr * S_G + S_F * S_Gs
def tail(T, rho):  # sum_{|k|>Kc} T e^{-|k|(2 sig1 - rho)}
    b = 2 * sig1 - rho
    assert b > 0
    return 2 * T * (-(Kc + 1) * b).exp() / (1 - (-b).exp())
tP0 = tail(TP, arb(0)); tY0 = tail(TY, arb(0))
print('tail P =%s  tail Y=%s' % (tP0.str(3), tY0.str(3)))

# exact node values via inverse DFT of length Nout
def eval_nodes(cc, t0):
    vec = [acb(0)] * Nout
    for k, v in cc.items():
        vec[k % Nout] += v
    X = acb.dft(vec, inverse=True)  # = (1/N) sum vec_k e^{+2 pi i k j/N}
    return [(X[j] * Nout).real + arb(0, t0.upper()) for j in range(Nout)]
Pn = eval_nodes(c, tP0); Yn = eval_nodes(dd, tY0)
S1 = arb(0); S2 = arb(0)
cB = a * (2 - kap) - (kap - 1)
for j in range(Nout):
    P = Pn[j]; Y = Yn[j]
    L = log2(P) - lz
    B = Y / P - lz
    u = L + (kap - 1) * B - H
    v = (2 - kap) * B - 2 * L + H
    w2 = 2 + 2 * (2 * pi * j / Nout).cos()
    # at x=pi, w2 is an interval around 0 -- force nonnegativity
    w2 = arb(0).union(w2) if w2.contains(0) else w2
    if w2.contains(0):
        w2 = arb(w2.upper() / 2, w2.upper() / 2)
    S1 += w2 * pow2(p * (Delta - u))
    S2 += w2 * pow2(q * (a * v - u))
T1 = S1 / Nout; T2 = S2 / Nout
Pmin = min(x.lower() for x in Pn); Pmax = max(x.upper() for x in Pn)
Yabs = max(max(abs(x.lower()), abs(x.upper())) for x in Yn)
print('node P in [%s, %s], max|Y| <= %s' % (arb(Pmin).str(8), arb(Pmax).str(8), arb(Yabs).str(8)))

# strip bound
best = None
for so_s in ['0.02', '0.04', '0.06', '0.08', '0.1', '0.15', '0.2']:
    so = arb(so_s); sop = so * arb('1.01')
    rho = sop + pi / Nout
    dP = sum(((abs(c[k])) * ((abs(k) * rho).exp() - 1) for k in range(-Kc, Kc + 1)), arb(0)) + tail(TP, rho)
    dY = sum(((abs(dd[k])) * ((abs(k) * rho).exp() - 1) for k in range(-Kc, Kc + 1)), arb(0)) + tail(TY, rho)
    Plo = arb(Pmin) - dP
    if not (Plo > 0):
        print('sig_o=%s: P may vanish on strip (Plo=%s)' % (so_s, Plo.str(5)))
        continue
    Yhi = arb(Yabs) + dY
    ReLlo = log2(Plo) - lz           # Re L >= this
    absB = Yhi / Plo + abs(lz)       # |B| <= this
    wmax = 2 + 2 * sop.cosh()
    e1 = p * (Delta - ReLlo + (kap - 1) * absB + H)
    e2 = q * ((1 + 2 * a) * (-ReLlo) + abs(cB) * absB + (1 + a) * abs(H))
    B01 = wmax * pow2(e1); B02 = wmax * pow2(e2)
    err1 = 2 * B01 / ((Nout * so).exp() - 1); err2 = 2 * B02 / ((Nout * so).exp() - 1)
    print('sig_o=%s: dP=%s Plo=%s Yhi=%s log2B0=(%s,%s) err=(%s,%s)' % (
        so_s, dP.str(4), Plo.str(4), Yhi.str(4), log2(B01).str(4), log2(B02).str(4), err1.str(3), err2.str(3)))
    if best is None or (err1 + err2).upper() < best[0]:
        best = ((err1 + err2).upper(), err1, err2, so_s)
_, err1, err2, so_s = best
M1u = T1.upper() + err1.upper(); M2u = T2.upper() + err2.upper()
print('\nN_out=%d  using sig_o=%s' % (Nout, so_s))
print('T_N(h1) = %s' % T1.str(20, radius=True))
print('T_N(h2) = %s' % T2.str(20, radius=True))
l1 = log2(arb(M1u)); l2 = log2(arb(M2u))
print('rigorous M1 <= %s  log2 <= %s  rho_c - log2M1 >= %s  %s' % (arb(M1u).str(16), l1.upper(), (rho_c - l1).lower(),
      'PASS' if rho_c - l1 > 0 else 'FAIL'))
print('rigorous M2 <= %s  log2 <= %s  rho_c - log2M2 >= %s  %s' % (arb(M2u).str(16), l2.upper(), (rho_c - l2).lower(),
      'PASS' if rho_c - l2 > 0 else 'FAIL'))
# also lower ends (to show the margin is real, not an artefact)
print('log2 T_N(h1) lower = %s, log2 T_N(h2) lower = %s' % (log2(arb(T1.lower())).str(16), log2(arb(T2.lower())).str(16)))
