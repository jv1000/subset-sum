import sys, random, time
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
src=open(sys.argv[1]).read().split('\nfor w,k,t in')[0]; ns={}; exec(src,ns); Qw=ns['Qw']
t0=time.time()
q,_=Qw((-3,-3,-2,-2,0,0),2,3); print('control (2,3):',q); assert q==F(29,28)
def Mlemma(w):
    m=len(w); fib={}
    for X in combinations(range(m),2): fib.setdefault(w[X[0]]+w[X[1]],[]).append(X)
    vals=sorted(set(w)); r=len(vals); M={v:F(0) for v in vals}
    for Xs in fib.values():
        for X in Xs:
            for i in X: M[w[i]]+=F(1,len(Xs))
    return all(M[v] <= (r+1 if w.count(v)>=2 else r-1) for v in vals)
mx=F(0); n=0; eq=[]; bad=[]
def test(w):
    global mx,n
    q,_=Qw(w,1,2); n+=1
    if q>mx: mx=q
    if q==1 and len(set(w))<len(w) and len(eq)<12: eq.append(w)
    if q>1 or not Mlemma(w): bad.append((w,q))
for m in range(4,10):
    for w in combinations_with_replacement(range(-4,5),m): test(w)
for w in combinations_with_replacement(range(-3,4),10): test(w)
print('exhaustive cases',n,'max',mx,'bad',bad[:5])
rnd=random.Random(20261104)
for i in range(3000):
    m=rnd.randint(10,14); kind=i%3
    if kind==0: w=tuple(rnd.randint(-3,3) for _ in range(m))
    elif kind==1: w=tuple(rnd.randint(-10**6,10**6) for _ in range(m))
    else: w=(0,0)+tuple(rnd.sample(range(1,10**6),m-2))
    test(tuple(sorted(w)))
print('total cases',n,'max',mx,'violations/lemma failures',len(bad),bad[:5])
print('Q=1 with a repeated class (first few):',eq)
print('elapsed %.0f s'%(time.time()-t0))
