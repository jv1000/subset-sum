"""Exact independent subset enumeration, Hall cuts, and local-cancellation test."""
import itertools as it, math, json, random, time, argparse
from fractions import Fraction as Q
from collections import defaultdict, Counter
from pathlib import Path
OUT=Path(__file__).resolve().parent
def calc(weights,t,details=False):
    m=len(weights); values=sorted(set(weights)); groups=[[i for i,x in enumerate(weights) if x==v] for v in values]
    ns=list(map(len,groups)); ci={p:c for c,g in enumerate(groups) for p in g}
    sets=[]; freq=Counter()
    for X in it.combinations(range(m),t):
        y=sum(weights[i] for i in X); counts=[0]*len(groups)
        for i in X: counts[ci[i]]+=1
        sets.append((X,y,counts)); freq[y]+=1
    M=[Q(0) for _ in groups]
    for X,y,j in sets:
        for c in range(len(groups)): M[c]+=Q(j[c],freq[y])
    N=[M[c]/ns[c] for c in range(len(groups))]; C=math.comb(m-1,t-1)
    S=[Q(0) for _ in groups]; L=[Q(0) for _ in groups]; targets=[]
    K=[Q(0) for _ in groups]; localK=[Q(0) for _ in groups]
    for X,y,j in sets:
        f=freq[y]; cap=Q(0); residual=Q(0)
        for c,n in enumerate(ns):
            S[c]+=N[c]*Q(j[c]*(j[c]-1),f)
            L[c]+=N[c]*Q(j[c]*max(n-f,0),f)
            cap+=N[c]*Q(j[c]*(f-1-n+j[c]),f)
            residual+=N[c]*Q(j[c]*max(f-n,0),f)
        assert cap>=0 and residual>=0
        mask=sum(1<<c for c,v in enumerate(j) if v)
        targets.append((mask,cap,residual,X,y,j,f))
        for c in range(len(groups)):
            K[c]+=cap*Q(j[c],ns[c]); localK[c]+=residual*Q(j[c],ns[c])
    q=sum(v*v for v in M)/(t*len(freq)*C)
    assert sum(S)-sum(row[1] for row in targets)==sum(v*(v-C) for v in M)
    repeated=[c for c,n in enumerate(ns) if n>1]
    worst=Q(0); worst_local=Q(0); cut=None; localcut=None
    for choices in it.product([0,1],repeat=len(repeated)):
        U=[c for c,b in zip(repeated,choices) if b]
        if not U: continue
        mask=sum(1<<c for c in U); ss=sum(S[c] for c in U); ll=sum(L[c] for c in U)
        cap=sum(row[1] for row in targets if mask&row[0]); res=sum(row[2] for row in targets if mask&row[0])
        rat=ss/cap if cap else (Q(0) if not ss else Q(10**10))
        rl=ll/res if res else (Q(0) if not ll else Q(10**10))
        if rat>worst: worst=rat;cut={'values':[values[c] for c in U],'supply':str(ss),'capacity':str(cap)}
        if rl>worst_local: worst_local=rl;localcut={'values':[values[c] for c in U],'supply':str(ll),'capacity':str(res)}
    prop=Q(0); propX=None
    for mask,cap,res,X,y,j,f in targets:
        if not cap: continue
        v=sum(Q(j[c],ns[c])*S[c]/K[c] for c in repeated if K[c])
        if v>prop: prop=v;propX=[weights[i] for i in X]
    result={'weights':weights,'t':t,'s_t':len(freq),'C':C,'Q':str(q),'Hall_ratio':str(worst),'Hall_cut':cut,'local_ratio':str(worst_local),'local_cut':localcut,'Prop1_load':str(prop),'Prop1_Y':propX,'classes':[{'value':values[c],'n':ns[c],'M':str(M[c]),'N':str(N[c]),'S_class':str(S[c]),'L_class':str(L[c]),'K_element':str(K[c])} for c in range(len(groups))]}
    if details: result['targets']=[{'X':list(X),'weights':[weights[i] for i in X],'sum':y,'j':j,'f':f,'cap':str(cap),'residual_cap':str(res)} for mask,cap,res,X,y,j,f in targets]
    return result
def general_control(w,k,t):
    m=len(w); ts=list(it.combinations(range(m),t)); ks=list(it.combinations(range(m),k))
    fs=Counter(sum(w[i] for i in X) for X in ts); N={A:sum((Q(1,fs[sum(w[i] for i in X)]) for X in ts if set(A)<=set(X)),Q(0)) for A in ks}
    mult=defaultdict(Q)
    for A in ks: mult[sum(w[i] for i in A)]+=N[A]
    denominator=len(fs)*math.comb(t,k)*math.comb(m-k,t-k)
    q=sum(x*x for x in mult.values())/denominator
    supply=Q(0);cap=Q(0)
    for X in ts:
        f=fs[sum(w[i] for i in X)]
        for A in it.combinations(X,k):
            for Ap in ks:
                if Ap!=A and sum(w[i] for i in A)==sum(w[i] for i in Ap) and (set(Ap)-set(A))&set(X): supply+=N[Ap]/f
        for Xp in ts:
            if Xp==X or sum(w[i] for i in Xp)!=sum(w[i] for i in X): continue
            for D in it.combinations(X,k):
                if not set(X)-set(Xp)<=set(D): cap+=N[D]/f
    assert supply-cap==(q-1)*denominator
    return {'weights':w,'k':k,'t':t,'Q':str(q),'near_miss_supply':str(supply),'target_capacity':str(cap),'free_routed_fraction':str(min(Q(1),cap/supply))}
def run():
    start=time.monotonic(); rng=random.Random(600411); count=0; failures=[]; localfails=[]; propfails=[]; maxq=(Q(0),None); maxprop=(Q(0),None)
    control=general_control([-3,-3,-2,-2,0,0],2,3)
    assert Q(control['Q'])>1 and Q(control['near_miss_supply'])>Q(control['target_capacity'])
    eq=calc([0,0,1,4],2,True); assert Q(eq['Q'])==1 and Q(eq['Hall_ratio'])==1
    generic=calc([1,10,100,1000,10000,100000],3); assert Q(generic['Q'])==1
    (OUT/'B_CONTROLS.json').write_text(json.dumps({'negative':control,'equality':eq,'generic':generic},indent=2))
    def cases():
        for m in range(4,9):
            for w in it.combinations_with_replacement(range(-2,3),m):
                for t in range(2,m//2+1): yield list(w),t
        curated=[[0,0,1,3,9,13],[0,0,1,1,5,25],[0,0,1,1,4,4,16,64],[0,0,0,1,4,16,64,256]]
        for w in curated:
            for t in range(2,len(w)//2+1):yield w,t
        for trial in range(600):
            m=rng.randrange(6,13); t=rng.randrange(2,m//2+1)
            if trial%2:
                r=rng.randrange((m+1)//2,m); base=[10**i for i in range(r)]
                w=base+[base[rng.randrange(r)] for _ in range(m-r)]
                if trial%3==0:
                    a,b,c=rng.sample(range(m-1),3);w[-1]=w[a]+w[b]-w[c]
            else: w=[rng.randrange(-m,m+1) for _ in range(m)]
            yield sorted(w),t
    for w,t in cases():
        if time.monotonic()-start>110: break
        v=calc(w,t);count+=1
        if Q(v['Q'])>maxq[0]:maxq=Q(v['Q']),v
        if Q(v['Prop1_load'])>maxprop[0]:maxprop=Q(v['Prop1_load']),v
        if Q(v['Q'])>1 or Q(v['Hall_ratio'])>1:failures.append(v)
        if Q(v['local_ratio'])>1 and len(localfails)<4:localfails.append(calc(w,t,True))
        if Q(v['Prop1_load'])>1 and len(propfails)<4:propfails.append(calc(w,t,True))
    result={'status':'EVIDENCE for general conjectures; exact rational finite-instance certificates','cases':count,'elapsed_seconds':time.monotonic()-start,'failures':failures,'local_cancellation_failures':localfails,'proportional_failures':propfails,'max_Q':maxq[1],'max_Prop1':maxprop[1]}
    (OUT/'B_SEARCH.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ['max_Q','max_Prop1','local_cancellation_failures','proportional_failures']},indent=2))
    print('local cancellation failures:',len(localfails),'proportional failures:',len(propfails),flush=True)
    if localfails:print(json.dumps({k:v for k,v in localfails[0].items() if k!='targets'},indent=2))
if __name__=='__main__':run()
