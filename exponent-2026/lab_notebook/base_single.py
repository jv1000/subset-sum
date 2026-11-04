"""C13 diagnostic: each of Base's 43 filters ALONE (J=1, OpenAI two-moment form) at Base's (tau0, eta).
Margin = eta - max(min_p log2 M1, min_q log2 M2). Base's family margin is +0.00025 (Prop. B)."""
import re, numpy as np
from scipy.optimize import minimize_scalar
T = open('/home/claude/ext/maths-proofs/subset-sum/PROOF_0.4877.tex').read()
A = T[T.index('Appendix A. The 43 filters'):T.index('Appendix B. Results used')]
rows = re.findall(r'^(\d+) & ([\d.]+) & ([-\d., ]+) & ([-\d., ]+) \\\\', A, re.M)
print(len(rows), 'filters parsed')
N = 2048; x = np.arange(N)*2*np.pi/N; pref = 2 + 2*np.cos(x); jj = np.arange(1, 9)
def corr(a, b): return np.real(np.fft.ifft(np.fft.fft(a)*np.conj(np.fft.fft(b))))/len(a)
def uv(rc, sc, kap):
    r = np.cos(np.outer(x, jj)) @ rc; s = np.cos(np.outer(x, jj)) @ sc
    F, G = 2.0**r, 2.0**s; Zf, Zg = F.mean(), G.mean(); f, g = F/Zf, G/Zg
    Q = corr(f, g); Bb = (corr(f*r, g) + corr(f, g*s))/Q - np.log2(Zf*Zg); L = np.log2(Q)
    H = np.log2(np.mean(f**kap)*np.mean(g**kap)); return L + (kap-1)*Bb - H, (2-kap)*Bb - 2*L + H
def lm(e): m = e.max(); return m + np.log2(np.mean(pref*2.0**(e - m)))
t, eta = 0.48769, 0.51613; D = eta - t; G = 2*t - eta; aG = D/G
res = []
for v, k, rs, ss in rows:
    u, w = uv(np.array([float(c) for c in rs.split(',')]), np.array([float(c) for c in ss.split(',')]), float(k))
    m1 = minimize_scalar(lambda p: lm(p*(D - u)), bounds=(1, 40), method='bounded')
    m2 = minimize_scalar(lambda q: lm(q*(aG*w - u)), bounds=(1, 40), method='bounded')
    res.append((int(v), eta - m1.fun, eta - m2.fun, m1.x, m2.x))
res.sort(key=lambda r: -min(r[1], r[2]))
for r in res[:6]: print('filter %2d alone: M1 margin %+.5f (p %.2f)  M2 margin %+.5f (q %.2f)' % (r[0], r[1], r[3], r[2], r[4]))
print('best single-filter margin %+.5f  vs family +0.00025' % min(res[0][1], res[0][2]))
