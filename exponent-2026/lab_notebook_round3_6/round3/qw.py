from itertools import combinations
from fractions import Fraction as F
from math import comb
def Qw(w,k,t):
    m=len(w); idx=range(m)
    wit={}
    for X in combinations(idx,t): wit.setdefault(sum(w[i] for i in X),[]).append(X)
    sk=len({sum(w[i] for i in A) for A in combinations(idx,k)})
    st=len(wit); mu={}
    for y,Xs in wit.items():
        for X in Xs:
            for A in combinations(X,k):
                u=sum(w[i] for i in A); mu[u]=mu.get(u,0)+F(1,st*len(Xs)*comb(t,k))
    cp=sum(p*p for p in mu.values()); at=F(st,comb(m,t)); ak=F(sk,comb(m,k))
    return cp*at*comb(m,k), at/ak
for w,k,t in [((-3,-3,-2,-2,0,0),2,3),((-6,-5,-5,-3,-3,-2,4,5),3,4),((-6,-5,-5,-3,-3,-2,4,5),2,4),((-6,-5,-5,-3,-3,-2,4,5),2,3),((1,2,4,8,16,32,64,128),2,4)]:
    q,r=Qw(w,k,t); print(w,k,t," Q_w=%.4f"%float(q)," a_t/a_k=%.4f"%float(r))
