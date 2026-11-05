import sys, itertools, random
from math import comb
from fractions import Fraction
sys.path.insert(0,'.')
from bf import layers, stats
random.seed(3)
c1=c2=c3=0; min31=None; min32=None
insts=[]
for n in range(1,8):
    for ws in itertools.combinations_with_replacement(range(-3,4),n): insts.append(list(ws))
for _ in range(300):
    n=random.randint(1,8); insts.append([random.randint(-30,30) for _ in range(n)])
for ws in insts:
    n=len(ws); L=layers(ws); A,B,per=stats(ws,L)
    cnt={m:(s,c,t) for (m,s,c,t) in per}
    full=(1<<n)-1
    # treat V = full set (lemmas are statements about a single V)
    s,c,tot=cnt[full]
    for t in range(n+1):
        for k in range(t+1):
            Ws=[m for m in range(1<<n) if bin(m).count('1')==t-k]
            rhs=sum(Fraction(cnt[full^W][1][k],comb(n-(t-k),k)) for W in Ws)/len(Ws)
            lhs=Fraction(c[t],comb(n,t)); c1+=1
            assert lhs<=rhs,(ws,t,k)
            r=rhs/lhs; min31=r if min31 is None or r<min31 else min31
    for k in range(n+1):
        for sz in range(k,n+1):
            Ss=[m for m in range(1<<n) if bin(m).count('1')==sz]
            e=sum(Fraction(cnt[S][1][k],comb(sz,k)) for S in Ss)/len(Ss)
            assert e>=Fraction(c[k],comb(n,k)),(ws,k,sz); c2+=1
    # 3.3
    ok=any(2*t<=n and tot<=(n+1)*c[t] for t in range(n+1)); assert ok; c3+=1
    t=max(range(n//2+1),key=lambda j:c[j])
    assert Fraction(c[t],comb(n,t))>=Fraction(tot,2**n*(n+1))
print("instances",len(insts),"3.1 checks",c1,"min ratio",min31,"3.2 checks",c2,"3.3 checks",c3)
