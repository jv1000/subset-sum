"""Rigorous (Arb) upper bounds for log2 M1, log2 M2 with analytic-strip trapezoid error bounds, written independently.
Handles cos+sin trig polynomials:  |a cos jz + b sin jz| <= sqrt(a^2+b^2) cosh(j Im z),
Re(a cos j(t+iy) + b sin j(t+iy)) = cosh(jy)(a cos jt + b sin jt).
Usage: python3 -I rig_M.py cand.json N sigma beta"""
from flint import arb, arb_poly, ctx
import json, sys, time
ctx.prec = 256
A = arb
Pj = json.load(open(sys.argv[1]))
N = int(sys.argv[2]); sig = A(sys.argv[3]); beta = A(sys.argv[4])
tau, eta, kappa, p, q = (A(Pj[k]) for k in ("tau0", "eta", "kappa", "p", "q_m"))
nt = Pj["n_terms"]
rco = [A(t) for t in Pj["rc"]]; sco = [A(t) for t in Pj["sc"]]
Delta = eta - tau; Gamma = 2*tau - eta; aG = Delta/Gamma
rho_c = eta - A("2.5e-6"); rho_f = eta - A("1.5e-6")
ln2 = A(2).log(); pi = A.pi()
pow2 = lambda t: (t*ln2).exp()
log2 = lambda t: t.log()/ln2
def terr(B0, width): return 2*B0/((A(N)*width).exp() - 1)
def widen(x, e): return x + A(0, e.upper())
xs = [2*pi*k/N for k in range(N)]
C = [[(A(j)*x).cos() for x in xs] for j in range(nt+1)]
S = [[(A(j)*x).sin() for x in xs] for j in range(nt+1)]
def nodes(c, scale=None):
    sc = scale or [A(1)]*(nt+1)
    return [sum(sc[j]*(c[j-1]*C[j][k] + c[nt+j-1]*S[j][k]) for j in range(1, nt+1)) for k in range(N)]
def amp(c, y):  # sup over |Im z|<=y of |trig poly|
    return sum((c[j-1]**2 + c[nt+j-1]**2).sqrt()*(A(j)*y).cosh() for j in range(1, nt+1))
mean = lambda v: sum(v)/N
def corr(a, b):  # c[j] = (1/N) sum_i a[(i+j) mod N] b[i]
    pa = arb_poly(a); bb = [A(0)]*(N+1)
    for i in range(N): bb[N-i] = b[i]
    pr = pa*arb_poly(bb)
    co = [pr[t] for t in range(2*N+1)]
    return [(co[N+j] + co[j])/N for j in range(N)]

t0 = time.time()
r = nodes(rco); s = nodes(sco)
F = [pow2(t) for t in r]; G = [pow2(t) for t in s]
Rr, Rs = amp(rco, sig), amp(sco, sig)
print("Rr(sig), Rs(sig) =", Rr.str(6), Rs.str(6))
Zf = widen(mean(F), terr(pow2(Rr), sig)); Zg = widen(mean(G), terr(pow2(Rs), sig))
Zfk = widen(mean([pow2(kappa*t) for t in r]), terr(pow2(kappa*Rr), sig))
Zgk = widen(mean([pow2(kappa*t) for t in s]), terr(pow2(kappa*Rs), sig))
LZ = log2(Zf*Zg); H = log2(Zfk) + log2(Zgk) - kappa*LZ
eP = terr(pow2(Rr + Rs), sig); eY = terr(pow2(Rr + Rs)*(Rr + Rs), sig)
print("inner trapezoid errors eP, eY:", eP.str(3), eY.str(3))
Pc = corr(F, G)
Y1 = corr([F[k]*r[k] for k in range(N)], G); Y2 = corr(F, [G[k]*s[k] for k in range(N)])
u, w = [], []
for k in range(N):
    Pk = widen(Pc[k], eP); Yk = widen(Y1[k] + Y2[k], eY)
    L = log2(Pk) - LZ; B = Yk/Pk - LZ
    u.append(L + (kappa-1)*B - H); w.append((2-kappa)*B - 2*L + H)
print("max node ball radius u:", max(float(t.rad()) for t in u), " w:", max(float(t.rad()) for t in w))
# outer strip
cb = [(A(j)*beta).cosh() for j in range(nt+1)]
rb = nodes(rco, cb); sb = nodes(sco, cb)
rcb = [rco[j]*cb[(j % nt)+1] for j in range(2*nt)]; scb = [sco[j]*cb[(j % nt)+1] for j in range(2*nt)]
Ir = widen(mean([pow2(2*t) for t in rb]), terr(pow2(2*amp(rcb, sig)), sig))
Is = widen(mean([pow2(2*t) for t in sb]), terr(pow2(2*amp(scb, sig)), sig))
Af, Ag = Ir/(Zf*Zf), Is/(Zg*Zg)
q0 = ((Af-1)*(Ag-1)).sqrt()
print("Af, Ag, q0 =", Af.str(6), Ag.str(6), q0.str(6))
assert q0 < 1
qb = (Af*Ag).sqrt()*(amp(rco, beta) + amp(sco, beta) + abs(LZ))
Bmax = qb/(1-q0); lneg = -log2(1-q0)
Ustar = lneg + abs(kappa-1)*Bmax + abs(H); Wstar = 2*lneg + abs(2-kappa)*Bmax + abs(H)
print("U*, W* =", Ustar.str(6), Wstar.str(6))
m2 = [2 + 2*x.cos() for x in xs]; M2s = 2 + 2*(2*beta).cosh()
T1 = mean([m2[k]*pow2(p*(Delta - u[k])) for k in range(N)])
T2 = mean([m2[k]*pow2(q*(aG*w[k] - u[k])) for k in range(N)])
e1 = terr(M2s*pow2(p*(Delta + Ustar)), 2*beta); e2 = terr(M2s*pow2(q*(aG*Wstar + Ustar)), 2*beta)
print("outer trapezoid errors:", e1.str(3), e2.str(3))
I1 = widen(T1, e1); I2 = widen(T2, e2)
for nm, I in (("M1", I1), ("M2", I2)):
    lg = log2(I)
    print(f"log2 {nm} in {lg.str(25)}; upper {lg.upper().str(15)}; margin vs rho_c lower = {(rho_c - lg).lower().str(8)};"
          f" {'PASS' if bool(lg < rho_c) else 'FAIL'} (< rho_c), {'PASS' if bool(lg < rho_f) else 'FAIL'} (< rho_f)")
print(f"time {time.time()-t0:.1f}s")
