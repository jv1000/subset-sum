import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/e6b88fde-407f-5350-a0a8-9cc298e460bb/scratchpad/referee")
import numpy as np
from scipy.optimize import minimize
from core import *
rng=np.random.default_rng(7)
N=256; x=2*np.pi*np.arange(N)/N
def gap(theta,deg,p,Delta,kfix=None):
    cf=np.clip(theta[:2*deg],-2.5,2.5).reshape(deg,2); cg=np.clip(theta[2*deg:4*deg],-2.5,2.5).reshape(deg,2)
    kappa=kfix if kfix else 0.5+1.5/(1+np.exp(-theta[-1]))
    u=quantities(trig(cf,x),trig(cg,x),kappa)[0]
    return log2M1(u,Delta,p,x)-Phi(p,Delta)
best=[]
for trial in range(16):
    deg=int(rng.integers(1,7)); p=float(rng.choice([0.5,1,2,5,10])); Delta=float(rng.uniform(0,0.3))
    kfix=None if trial%2 else 1.0
    th0=rng.uniform(-1,1,4*deg+1)
    r=minimize(gap,th0,args=(deg,p,Delta,kfix),method='Nelder-Mead',options={'maxiter':3000,'xatol':1e-6,'fatol':1e-9})
    th=r.x; cf=np.clip(th[:2*deg],-2.5,2.5).reshape(deg,2); cg=np.clip(th[2*deg:4*deg],-2.5,2.5).reshape(deg,2)
    kappa=kfix if kfix else 0.5+1.5/(1+np.exp(-th[-1]))
    x2=2*np.pi*np.arange(1024)/1024
    g1024=log2M1(quantities(trig(cf,x2),trig(cg,x2),kappa)[0],Delta,p,x2)-Phi(p,Delta)
    print(f"deg={deg} p={p} Delta={Delta:.3f} kappa={kappa:.4f} min gap N256={r.fun:.6f} N1024={g1024:.6f}")
