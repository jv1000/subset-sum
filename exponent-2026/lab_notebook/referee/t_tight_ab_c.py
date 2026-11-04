import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/e6b88fde-407f-5350-a0a8-9cc298e460bb/scratchpad/referee")
import numpy as np
from scipy.optimize import minimize_scalar
from core import *
print("== Tightness (continuous, kappa=1, g ~ delta, f ~ w^{1/(1+p)}+eps) ==")
for p in (0.5,1,3,10):
  b=1/(1+p)
  for N,c,eps in ((1024,300,1e-3),(4096,3000,1e-5),(8192,20000,1e-7)):
    x=2*np.pi*np.arange(N)/N
    lf=np.log((1+np.cos(x))**b+eps); lg=c*(np.cos(x)-1)
    for kappa in (1.0,1.1):
        u=quantities(lf,lg,kappa)[0]
        print(f" p={p} N={N} conc={c} eps={eps} kappa={kappa}: gap={log2M1(u,0.19,p,x)-Phi(p,0.19):.3e}")
print("== (a) g(p)=(1+p)log2 avg w^{1/(1+p)} monotone ==")
ps=np.linspace(1e-3,200,200001); gp=(1+ps)*np.log2(closed(1/(1+ps)))
print(" max increment:",np.diff(gp).max()," g(0+)=",gp[0]," g(200)=",gp[-1]," (limit -1)")
print("== (b) Delta=0.1900002 ==")
D=0.1900002
r=minimize_scalar(lambda p:Phi(p,D),bounds=(1,10),method='bounded',options={'xatol':1e-12})
pg=np.linspace(1,10,90001); print(f" argmin p={r.x:.6f} min Phi={r.fun:.6f}  grid min={Phi(pg,D).min():.6f}  Phi(1)={Phi(1,D):.6f} Phi(10)={Phi(10,D):.6f}")
print("== (c) discrete Z/PZ: avg_P w^b vs continuous closed form ==")
def davg(P):
    k=np.arange(P); return lambda b: np.mean(np.maximum(1+np.cos(2*np.pi*k/P),0)**b)
for P in (3,4,5,6,8,16,17,64,65,256,1024,1025,4096):
    for p in (1,5):
        b=1/(1+p); print(f" P={P} p={p}: avg_P={davg(P)(b):.10f} closed={closed(b):.10f} PhiP-Phi={Phi(p,0,davg(P))-Phi(p,0):+.3e}")
print("== (c) discrete near-tight instances vs Phi(closed form) ==")
for P in (4,6,8,16,64,256,1024):
  for p in (1,5):
    b=1/(1+p); k=np.arange(P); x=2*np.pi*k/P
    lf=np.log(np.maximum(1+np.cos(x),0)**b+1e-12); lg=np.where(k==0,0.0,-40.0)
    u=quantities(lf,lg,1.0)[0]
    L=log2M1(u,0.19,p,x)
    print(f" P={P} p={p}: log2M1-Phi_closed={L-Phi(p,0.19):+.3e}   log2M1-Phi_discrete={L-Phi(p,0.19,davg(P)):+.3e}")
