"""Independent float computation of M1, M2 (numpy FFT, double) + mpmath high precision direct sums.
Convention: Q(x) = mean_w f(x+w) g(w) (paper filtering.tex l.12-20; checksum.tex l.122-153)."""
import json, sys
import numpy as np

def trig(cc, sc, x):
    out = np.zeros_like(x)
    for j in range(len(cc)):
        out += cc[j]*np.cos((j+1)*x)
    for j in range(len(sc)):
        out += sc[j]*np.sin((j+1)*x)
    return out

def uw(rc, rs, sc_, ss, kappa, N, conv="corr"):
    x = 2*np.pi*np.arange(N)/N
    r = trig(rc, rs, x); s = trig(sc_, ss, x)
    F = 2.0**r; G = 2.0**s
    Zf, Zg = F.mean(), G.mean()
    Zfk, Zgk = (F**kappa).mean(), (G**kappa).mean()
    LZ = np.log2(Zf*Zg)
    H = np.log2(Zfk) + np.log2(Zgk) - kappa*LZ
    def corr(a, b):  # c[j] = (1/N) sum_i a[i+j] b[i]
        if conv == "corr":
            return np.real(np.fft.ifft(np.fft.fft(a)*np.conj(np.fft.fft(b))))/len(a)
        else:          # convolution c[j] = (1/N) sum_i a[j-i] b[i]
            return np.real(np.fft.ifft(np.fft.fft(a)*np.fft.fft(b)))/len(a)
    Pc = corr(F, G)
    Yc = corr(F*r, G) + corr(F, G*s)
    L = np.log2(Pc) - LZ
    B = Yc/Pc - LZ
    u = L + (kappa-1)*B - H
    w = (2-kappa)*B - 2*L + H
    D = B - L
    return x, u, w, D

def moments(x, u, w, tau, eta, p, q):
    Delta = eta - tau; Gamma = 2*tau - eta; aG = Delta/Gamma
    m2 = 2 + 2*np.cos(x)
    M1 = np.mean(m2*2.0**(p*(Delta - u)))
    M2 = np.mean(m2*2.0**(q*(aG*w - u)))
    return np.log2(M1), np.log2(M2)

if __name__ == "__main__":
    # sanity: the paper's filter, Prop 3.1: both < 0.5168
    rc = [0.851, 0.466, 0.325, 0.253, 0.224, -0.314]; sc = [1.281, -0.938, 0.731, -0.559, 0.391, 0.110]
    for N in (256, 1024):
        x, u, w, D = uw(rc, [], sc, [], 1.0315, N)
        print("paper filter N=%d: log2 moments" % N, moments(x, u, w, 0.48996, 0.51772, 8.5, 8.3), " (paper: both < 0.5168)")
    Pj = json.load(open(sys.argv[1]))
    f = lambda k: float(Pj[k])
    tau, eta, kappa, p, q = f("tau0"), f("eta"), f("kappa"), f("p"), f("q_m")
    rcoef = [float(t) for t in Pj["rc"]]; scoef = [float(t) for t in Pj["sc"]]
    nt = Pj["n_terms"]
    rc, rs = rcoef[:nt], rcoef[nt:]; sc_, ss = scoef[:nt], scoef[nt:]
    rho_c = eta - 2.5e-6
    for N in (128, 256, 512, 1024, 4096, 16384):
        x, u, w, D = uw(rc, rs, sc_, ss, kappa, N)
        l1, l2 = moments(x, u, w, tau, eta, p, q)
        print(f"N={N:6d}  log2 M1 = {l1:.12f}  log2 M2 = {l2:.12f}  margins vs rho_c: {rho_c-l1:.4e} {rho_c-l2:.4e}")
    x, u, w, D = uw(rc, rs, sc_, ss, kappa, 1024)
    Gamma = 2*tau - eta
    print("W/Gamma range:", (w/Gamma).min(), (w/Gamma).max(), " u range:", u.min(), u.max(), " D min:", D.min())
    # convention sensitivity: convolution instead of correlation, and reflected s
    x, u2, w2, _ = uw(rc, rs, sc_, ss, kappa, 1024, conv="conv")
    print("CONVOLUTION convention (wrong one): ", moments(x, u2, w2, tau, eta, p, q))
    # z-sensitivity: what if band rows / Gamma-w row would matter -- check optimal p,q near given
    x, u, w, D = uw(rc, rs, sc_, ss, kappa, 1024)
    for pp in (p - 0.2, p, p + 0.2):
        print("p=%.4f" % pp, moments(x, u, w, tau, eta, pp, q)[0])
    for qq in (q - 0.2, q, q + 0.2):
        print("q=%.4f" % qq, moments(x, u, w, tau, eta, p, qq)[1])
