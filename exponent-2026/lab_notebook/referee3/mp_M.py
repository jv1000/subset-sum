"""High-precision (mpmath, 50 digits) direct-sum computation of log2 M1, log2 M2 at two resolutions.
Inner integral Q(x) = mean_w f(x+w) g(w) computed by direct O(N^2) sums (no FFT)."""
import json, sys
import mpmath as mp
mp.mp.dps = 50
Pj = json.load(open(sys.argv[1]))
D_ = lambda k: mp.mpf(Pj[k])
tau, eta, kappa, p, q = D_("tau0"), D_("eta"), D_("kappa"), D_("p"), D_("q_m")
nt = Pj["n_terms"]
rco = [mp.mpf(t) for t in Pj["rc"]]; sco = [mp.mpf(t) for t in Pj["sc"]]
Delta = eta - tau; Gamma = 2*tau - eta; aG = Delta/Gamma
rho_c = eta - mp.mpf("2.5e-6")

def run(N):
    xs = [2*mp.pi*k/N for k in range(N)]
    cosj = [[mp.cos(j*x) for x in xs] for j in range(nt+1)]
    sinj = [[mp.sin(j*x) for x in xs] for j in range(nt+1)]
    r = [sum(rco[j-1]*cosj[j][k] + rco[nt+j-1]*sinj[j][k] for j in range(1, nt+1)) for k in range(N)]
    s = [sum(sco[j-1]*cosj[j][k] + sco[nt+j-1]*sinj[j][k] for j in range(1, nt+1)) for k in range(N)]
    F = [mp.power(2, t) for t in r]; G = [mp.power(2, t) for t in s]
    Zf = mp.fsum(F)/N; Zg = mp.fsum(G)/N
    Zfk = mp.fsum(mp.power(t, kappa) for t in F)/N; Zgk = mp.fsum(mp.power(t, kappa) for t in G)/N
    LZ = mp.log(Zf*Zg, 2); H = mp.log(Zfk, 2) + mp.log(Zgk, 2) - kappa*LZ
    S1 = mp.mpf(0); S2 = mp.mpf(0)
    for k in range(N):
        Pk = mp.mpf(0); Yk = mp.mpf(0)
        for i in range(N):
            t = F[(i+k) % N]*G[i]
            Pk += t; Yk += t*(r[(i+k) % N] + s[i])
        Pk /= N; Yk /= N
        L = mp.log(Pk, 2) - LZ; B = Yk/Pk - LZ
        u = L + (kappa-1)*B - H; w = (2-kappa)*B - 2*L + H
        m2 = 2 + 2*mp.cos(xs[k])
        S1 += m2*mp.power(2, p*(Delta - u)); S2 += m2*mp.power(2, q*(aG*w - u))
    return mp.log(S1/N, 2), mp.log(S2/N, 2)

for N in (96, 160):
    l1, l2 = run(N)
    print(f"N={N}: log2 M1 = {mp.nstr(l1, 20)}  log2 M2 = {mp.nstr(l2, 20)}")
    print(f"        margins vs rho_c: {mp.nstr(rho_c - l1, 12)}  {mp.nstr(rho_c - l2, 12)}")
