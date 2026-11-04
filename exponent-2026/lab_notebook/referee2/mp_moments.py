"""High-precision floating evaluation (mpmath) of M1, M2.
Outer nodes x_j = 2 pi j/N (N = 1024, 2048), inner trapezoid on the same grid
(so x_j + w_i is a grid point) -- inner integrand is entire, so N inner nodes
is overwhelmingly adequate (checked by also running N_in = 2N for N = 1024).
Usage: python3 -I mp_moments.py N [Nin]"""
import json, sys
import mpmath as mp
mp.mp.dps = 30

C = json.load(open('/home/claude/c3/candidate_K16.json'))
rc = [mp.mpf(t) for t in C['rc']]; sc = [mp.mpf(t) for t in C['sc']]
kap = mp.mpf(C['kappa']); p = mp.mpf(C['p']); q = mp.mpf(C['q_m'])
eta = mp.mpf(C['eta']); tau = mp.mpf(C['tau']); eps = mp.mpf('1e-8')
Delta = eta - tau; Gam = 2*tau - eta; a = Delta/Gam
rho_f = eta - 48*eps - mp.mpf('5e-7'); rho_c = rho_f - mp.mpf('1e-6')

N = int(sys.argv[1]); Nin = int(sys.argv[2]) if len(sys.argv) > 2 else N
assert Nin % N == 0
step = Nin // N
tw = 2*mp.pi/Nin
def trig(c, i):
    t = tw*i
    return mp.fsum(c[j-1]*mp.cos(j*t) + c[15+j]*mp.sin(j*t) for j in range(1, 17))
r = [trig(rc, i) for i in range(Nin)]
s = [trig(sc, i) for i in range(Nin)]
F = [mp.power(2, x) for x in r]; G = [mp.power(2, x) for x in s]
Fr = [F[i]*r[i] for i in range(Nin)]; Gs = [G[i]*s[i] for i in range(Nin)]
Zf = mp.fsum(F)/Nin; Zg = mp.fsum(G)/Nin
Zfk = mp.fsum(mp.power(2, kap*x) for x in r)/Nin
Zgk = mp.fsum(mp.power(2, kap*x) for x in s)/Nin
lz = mp.log(Zf, 2) + mp.log(Zg, 2)
H = mp.log(Zfk, 2) + mp.log(Zgk, 2) - kap*lz
S1 = []; S2 = []
for j in range(N):
    sh = j*step
    Fs = F[sh:] + F[:sh]; Frs = Fr[sh:] + Fr[:sh]      # F(x_j + w_i)
    P = mp.fdot(Fs, G)/Nin
    Y = (mp.fdot(Frs, G) + mp.fdot(Fs, Gs))/Nin
    L = mp.log(P, 2) - lz
    B = Y/P - lz
    u = L + (kap-1)*B - H
    v = (2-kap)*B - 2*L + H
    w2 = 2 + 2*mp.cos(2*mp.pi*j/N)
    S1.append(w2*mp.power(2, p*(Delta-u)))
    S2.append(w2*mp.power(2, q*(a*v-u)))
M1 = mp.fsum(S1)/N; M2 = mp.fsum(S2)/N
l1 = mp.log(M1, 2); l2 = mp.log(M2, 2)
print('N=%d Nin=%d' % (N, Nin))
print('Zf=%s Zg=%s H=%s' % (mp.nstr(Zf, 20), mp.nstr(Zg, 20), mp.nstr(H, 20)))
print('M1=%s log2M1=%s' % (mp.nstr(M1, 22), mp.nstr(l1, 22)))
print('M2=%s log2M2=%s' % (mp.nstr(M2, 22), mp.nstr(l2, 22)))
print('rho_c=%s  margin1=%s  margin2=%s' % (mp.nstr(rho_c, 15), mp.nstr(rho_c-l1, 12), mp.nstr(rho_c-l2, 12)))
