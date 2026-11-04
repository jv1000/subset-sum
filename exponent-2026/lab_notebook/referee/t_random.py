import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/e6b88fde-407f-5350-a0a8-9cc298e460bb/scratchpad/referee")
import numpy as np
from core import *
rng=np.random.default_rng(20261103)
def inst(N,cf,cg,kappa):
    x=2*np.pi*np.arange(N)/N
    return x,quantities(trig(cf,x),trig(cg,x),kappa)
rows=[]
for it in range(300):
    df,dg=rng.integers(1,7,2)
    amp=rng.choice([0.3,1.0,2.5])
    cf=rng.uniform(-amp,amp,(df,2)); cg=rng.uniform(-amp,amp,(dg,2))
    if it%10==0: cf[:]=0; cf[0,0]=2.5*df  # extra peaked
    kappa=rng.uniform(0.5,2); p=rng.uniform(0.5,10); Delta=rng.uniform(0,0.3)
    res={}
    for N in (256,512):
        x,(u,v,lQ,lQs)=inst(N,cf,cg,kappa)
        res[N]=(log2M1(u,Delta,p,x),(u-lQs).max(),abs(np.mean(2**lQs)-1))
    gap=res[256][0]-Phi(p,Delta)
    rows.append((gap,res[512][0]-res[256][0],res[256][1],res[256][2],it,kappa,p,Delta,cf,cg))
rows.sort(key=lambda r:r[0])
print("n=",len(rows)," min gap=",rows[0][0])
print("max Jensen violation u-log2Q* =",max(r[2] for r in rows)," max |avg Q* -1|=",max(r[3] for r in rows))
print("max |M1(512)-M1(256)| over all:",max(abs(r[1]) for r in rows))
for r in rows[:5]:
    print(f"gap={r[0]:.6f} conv512-256={r[1]:.2e} it={r[4]} kappa={r[5]:.4f} p={r[6]:.4f} Delta={r[7]:.4f}\n cf={np.round(r[8],4).tolist()}\n cg={np.round(r[9],4).tolist()}")
