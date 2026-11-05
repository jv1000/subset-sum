import sys, random, time
from math import comb
sys.path.insert(0,'.')
from bf import layers, check_instance
random.seed(11)
t0=time.time(); N=0; mA=None; mD=None; fA=fD=0; nA=nD=0
while time.time()-t0<200:
    n=random.randint(6,10); mode=random.random()
    if mode<0.4: ws=[random.randint(-50,50) for _ in range(n)]
    elif mode<0.7:
        vals=[random.randint(-20,20) for _ in range(random.randint(1,3))]; ws=[random.choice(vals) for _ in range(n)]
    else: ws=[random.choice([0,0,1,2,4,8,16,-1,-5,3]) for _ in range(n)]
    res,_=check_instance(ws); N+=1
    for (k,s,v,p,l,r) in res:
        if v==0: continue
        q=l/r
        if p:
            nA+=1; fA+= l<r
            if mA is None or q<mA[0]: mA=(q,ws,k,s,v)
        else:
            nD+=1; fD+= l<r
            if mD is None or q<mD[0]: mD=(q,ws,k,s,v)
print("random instances",N,"all-hyp checks",nA,"fails",fA,"min",float(mA[0]),mA[1:],"| dropped checks",nD,"fails",fD,"min",float(mD[0]),mD[1:])
