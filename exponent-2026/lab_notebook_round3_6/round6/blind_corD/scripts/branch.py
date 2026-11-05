import sys, itertools, time
from math import comb
sys.path.insert(0,'.')
from monolib import full_layers, bad
# Every V of size v with weights in [lo,hi] is itself a multiset in the enumeration, so enumerate multisets directly.
for (lo,hi,nmax) in [(-4,4,10),(-3,3,11),(-6,6,8)]:
    t0=time.time(); tot=0; nonmono={}; argmax_below_half=0; ex=None
    branchA=0; branchA_prod=0; noGood=0; noGood_prod=0; exA=None
    for v in range(1,nmax+1):
        for ws in itertools.combinations_with_replacement(range(lo,hi+1),v):
            tot+=1
            c=full_layers(list(ws))
            # union size
            n=v; mn=min(0,min(ws)); off=-n*mn; lay=[1<<off]
            for w in ws:
                new=lay+[0]
                for j in range(len(lay),0,-1):
                    y=lay[j-1]; y=(y<<w) if w>=0 else (y>>(-w)); new[j]|=y
                lay=new
            u=0
            for b in lay: u|=b
            U=u.bit_count()
            if bad(c) is not None:
                nonmono[v]=nonmono.get(v,0)+1
                if ex is None: ex=(ws,c,U)
            h=v//2
            tstar=max(range(h+1),key=lambda j:(c[j],-j))  # smallest maximizer
            if tstar<h: argmax_below_half+=1
            good=[t for t in range(h+1) if U<=(v+1)*c[t]]
            for k in range(0,h+1):
                prod_any=any(comb(s,k)*comb(v,k)<=2**v for s in range(2*k,v+1) if 2*s<=v+2*k)
                adm=any(2*s<=v+2*k for s in range(2*k,v+1))
                if not adm: continue
                if tstar<k:
                    branchA+=1
                    if prod_any: branchA_prod+=1; exA=exA or (ws,k,c)
                if not any(t>=k for t in good):
                    noGood+=1
                    if prod_any: noGood_prod+=1
    print(f"weights [{lo},{hi}], |V|<=({nmax}): multisets={tot}; non-monotone-on-[0,v/2] by size={nonmono}; first={ex}; "
          f"V with smallest 3.3-maximizer t<floor(v/2): {argmax_below_half}; "
          f"(V,k) admissible with maximizer t<k: {branchA} (of which some sigma satisfies product hyp: {branchA_prod}, ex {exA}); "
          f"(V,k) admissible with NO t in [k,v/2] satisfying 3.3: {noGood} (with product: {noGood_prod}); {time.time()-t0:.1f}s",flush=True)
