"""Quick double-precision independent evaluation of M1, M2 (sanity check).
Definitions follow filtering.tex / numerical.tex:
  P(x) = mean_w F(x+w) G(w),  Y(x) = mean_w F(x+w)G(w)(r(x+w)+s(w))
"""
import json, sys
import numpy as np

C = json.load(open('/home/claude/c3/candidate_K16.json'))
rc = np.array([float(t) for t in C['rc']]); sc = np.array([float(t) for t in C['sc']])
kap = float(C['kappa']); p = float(C['p']); q = float(C['q_m'])
eta = float(C['eta']); tau = float(C['tau']); eps = 1e-8
Delta = eta - tau; Gam = 2*tau - eta; a = Delta/Gam
rho_f = eta - 48*eps - 5e-7; rho_c = rho_f - 1e-6
J = np.arange(1, 17)

def trig(c, x):
    return np.cos(np.outer(x, J)) @ c[:16] + np.sin(np.outer(x, J)) @ c[16:]

def moments(Nout, Nin=None, conv='corr'):
    if Nin is None: Nin = Nout
    assert Nin % Nout == 0
    w = 2*np.pi*np.arange(Nin)/Nin
    r = trig(rc, w); s = trig(sc, w)
    F = 2.0**r; G = 2.0**s
    Zf = F.mean(); Zg = G.mean()
    Zfk = (F**kap).mean(); Zgk = (G**kap).mean()
    # correlation P_j = mean_i F[i+j] G[i]  via FFT: ifft(fft(F) * conj(fft(G)))
    if conv == 'corr':
        Gc = G; Gsc = G*s
    else:  # convolution F(x-w)G(w) == corr with G(-w)
        idx = (-np.arange(Nin)) % Nin
        Gc = G[idx]; Gsc = (G*s)[idx]
    fF = np.fft.fft(F); fFr = np.fft.fft(F*r)
    fG = np.fft.fft(Gc); fGs = np.fft.fft(Gsc)
    Pj = np.real(np.fft.ifft(fF*np.conj(fG)))/Nin
    Yj = np.real(np.fft.ifft(fFr*np.conj(fG) + fF*np.conj(fGs)))/Nin
    step = Nin//Nout
    Pj = Pj[::step]; Yj = Yj[::step]
    x = 2*np.pi*np.arange(Nout)/Nout
    lz = np.log2(Zf) + np.log2(Zg)
    L = np.log2(Pj) - lz
    B = Yj/Pj - lz
    H = np.log2(Zfk) + np.log2(Zgk) - kap*lz
    u = L + (kap-1)*B - H
    v = (2-kap)*B - 2*L + H
    D = B - L
    M2w = 2 + 2*np.cos(x)
    M1 = np.mean(M2w*2.0**(p*(Delta-u)))
    M2 = np.mean(M2w*2.0**(q*(a*v-u)))
    return dict(M1=M1, M2=M2, l1=np.log2(M1), l2=np.log2(M2),
                Pmin=Pj.min(), Pmax=Pj.max(), Dmin=D.min(), H=H, Zf=Zf, Zg=Zg,
                umin=u.min(), umax=u.max(), vmin=v.min(), vmax=v.max(),
                fracsample1=np.mean(u < Delta))

for N in (256, 512, 1024, 2048):
    m = moments(N, 4096)
    print(N, 'log2M1=%.10f log2M2=%.10f  rho_c=%.10f  marg1=%.3e marg2=%.3e' %
          (m['l1'], m['l2'], rho_c, rho_c-m['l1'], rho_c-m['l2']))
m = moments(2048, 4096)
print({k: m[k] for k in ('Pmin','Pmax','Dmin','H','Zf','Zg','umin','umax','vmin','vmax')})
mc = moments(2048, 4096, conv='conv')
print('convolution convention instead: log2M1=%.8f log2M2=%.8f' % (mc['l1'], mc['l2']))
print('Delta,Gamma,a', Delta, Gam, a, 'rho_c', rho_c)
