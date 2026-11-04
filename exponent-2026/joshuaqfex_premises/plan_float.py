"""NON-RIGOROUS planning pass (float64): sizes N and strip widths only."""
import json, numpy as np, sys
d = json.load(open(sys.argv[1])); tau, eta = 0.48769, 0.51613
Dl, Gm = eta - tau, 2*tau - eta; aG = Dl/Gm
def absum(c, y): return sum(abs(c[j])*np.cosh((j+1)*y) for j in range(8))
NN = 4096; x = 2*np.pi*np.arange(NN)/NN
def trig(c): return sum(c[j]*np.cos((j+1)*x) for j in range(8))
for hw in (0.1, 0.19, 0.25):  # beta; outer strip half-width = 2*beta
    U, W, Q = [], [], []
    for f in d['filters']:
        r = np.array(list(map(float, f['r_coef']))); s = np.array(list(map(float, f['s_coef']))); k = float(f['kappa'])
        rk, sk = trig(r), trig(s); Zf, Zg = np.mean(2**rk), np.mean(2**sk)
        LZ = np.log2(Zf*Zg); H = np.log2(np.mean(2**(k*rk))) + np.log2(np.mean(2**(k*sk))) - k*LZ
        rb = r*np.cosh(np.arange(1,9)*hw); sb = s*np.cosh(np.arange(1,9)*hw)
        Af = np.mean(2**(2*trig(rb)))/Zf**2; Ag = np.mean(2**(2*trig(sb)))/Zg**2
        q0 = np.sqrt((Af-1)*(Ag-1)); qb = np.sqrt(Af*Ag)*(absum(r,hw)+absum(s,hw)+abs(LZ))
        Bm = qb/(1-q0); ln = -np.log2(1-q0)
        U.append(ln + abs(k-1)*Bm + abs(H)); W.append(2*ln + abs(2-k)*Bm + abs(H)); Q.append(q0)
    worst = 0
    for c in d['certs']:
        z = list(map(float, c['z'])); v = c['v']
        if c['case'] == 'case1': sup = [Dl+U[v], Gm+W[v]]
        else:
            lo = float(c['lo']); sup = [aG*W[v]+U[v], W[v]-Gm*lo] + ([Gm*float(c['hi'])+W[v]] if c['hi'] else [])
        sup += [U[v]+U[l] for l in c['cons']]
        worst = max(worst, sum(a*b for a,b in zip(z, sup)))
    w = 2*hw
    print(f"beta={hw}: max q0={max(Q):.3f} max U*={max(U):.2f} max W*={max(W):.2f} worst B0 exponent (bits)={worst:.0f}"
          f" -> N_out for err<2^-60 rel: {int((worst+64)*np.log(2)/w)+1}")
# inner sizing
for sig in (0.45,):
    R = max(absum(list(map(float,f['r_coef'])),sig)+absum(list(map(float,f['s_coef'])),sig) for f in d['filters'])
    print(f"inner sigma={sig}: max R+S={R:.2f} bits; N_in for err 2^-80: {int((R+np.log2(R)+81)*np.log(2)/sig)+1}")
