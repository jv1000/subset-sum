"""R8-COMB: exact, small combinatorial controls. No general inference."""
from itertools import combinations,combinations_with_replacement
from collections import defaultdict
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json,time
OUT=Path(__file__).resolve().parent
def layer(w,t):
    z=defaultdict(list)
    for X in combinations(range(len(w)),t): z[sum(w[i] for i in X)].append(X)
    return z
def Q(w,t,k):
    fiber=layer(w,t); s=len(fiber); mu=defaultdict(F)
    for witnesses in fiber.values():
        for X in witnesses:
            for A in combinations(X,k): mu[sum(w[i] for i in A)]+=F(1,s*len(witnesses)*comb(t,k))
    assert sum(mu.values())==1
    at=F(s,comb(len(w),t)); ak=F(len(layer(w,k)),comb(len(w),k))
    value=sum(x*x for x in mu.values())*at*comb(len(w),k)
    assert value>=at/ak
    return value,at,ak
def main():
    start=time.monotonic(); out={}
    w=(-6,-5,-5,-3,-3,-2,4,5)
    out['middle_counterexample']={str(t):str(F(len(layer(w,t)),comb(len(w),t))) for t in (3,4)}
    assert out['middle_counterexample']=={'3':'19/56','4':'12/35'}
    q,at,ak=Q((-3,-3,-2,-2,0,0),3,2); assert q==F(29,28)
    out['excluded_k2_case']={'Q':str(q),'a_t':str(at),'a_k':str(ak),'status':'Must remain outside YP-Hall domain: t+2k=7>m=6'}
    out['few_valued_counterexample_to_072']=str(Q((0,0,1,1),2,1)[0]); assert Q((0,0,1,1),2,1)[0]==1
    for m in range(4,10):
        for t in range(2,m//2+1): assert Q(tuple(2**i for i in range(m)),t,1)[0]==1
    count=0
    for m in range(4,10):
        for w in combinations_with_replacement(range(-2,3),m):
            assert Q(w,2,1)[0]<=1; count+=1
    family_count=0
    for m in range(4,10):
        for t in range(2,m//2+1):
            for a in range(1,m//2+1):
                assert Q((0,)*a+(1,)*(m-a),t,1)[0]<=1; family_count+=1
            assert Q((0,0)+tuple(2**j for j in range(m-2)),t,1)[0]<=1; family_count+=1
    out.update({'status':'PROVED for exact enumerated cases only; general theorems require proofs',
      'k1_t2_instances':count,'two_special_family_instances':family_count,
      'generic_controls':'PASS','elapsed_seconds_evidence':time.monotonic()-start})
    (OUT/'combinatorics.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
