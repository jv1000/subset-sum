"""Search the stronger, additive-structure-free profile relaxation."""
from fractions import Fraction
import itertools,math,json,time,random
from pathlib import Path
out=Path(__file__).resolve().parent
def profiles(ns,t):return [j for j in itertools.product(*(range(n+1) for n in ns)) if sum(j)==t]
def partitions(n,lo=1):
    if n==0:yield []
    for i in range(lo,n+1):
        for p in partitions(n-i,i):yield [i]+p
def main():
    start=time.monotonic(); checked=0; maxratio=Fraction(0); best=None; exact_cases=0
    rng=random.Random(60411)
    for m in range(4,13):
      for ns in partitions(m):
       if max(ns)==1:continue
       for t in range(2,m//2+1):
        js=profiles(ns,t); den=t*math.comb(m-1,t-1); r=len(ns); p=len(js)
        if p>300:continue
        if p<=16:
            exact_cases+=1; z=[0]*r;s=0;old=0
            for mask in range(1,1<<p):
                gray=mask^(mask>>1);diff=gray^old;i=diff.bit_length()-1;sign=1 if gray&diff else -1
                s+=sign;z=[a+sign*b for a,b in zip(z,js[i])];old=gray
                val=sum(a*a for a in z)
                checked+=1
                if val>den*s:
                    result={'status':'PROVED finite profile-relaxation counterexample; not an integer-weight counterexample','m':m,'t':t,'class_sizes':ns,'profiles':[js[i] for i in range(p) if gray>>i&1],'M':z,'s':s,'C':math.comb(m-1,t-1),'ratio':str(Fraction(val,den*s)),'checked':checked}
                    (out/'PROFILE_OBSTRUCTION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return
        else:
            for _ in range(10):
                chosen=[rng.randrange(2) for _ in js];z=[sum(bit*j[c] for bit,j in zip(chosen,js)) for c in range(r)];s=sum(chosen)
                for steps in range(5*p):
                    i=rng.randrange(p);sign=1-2*chosen[i];v=[a+sign*b for a,b in zip(z,js[i])]
                    delta=sum(a*a for a in v)-sum(a*a for a in z)-den*sign
                    if delta>0:chosen[i]^=1;z=v;s+=sign
                if s and sum(a*a for a in z)>den*s:
                    result={'status':'PROVED finite profile-relaxation counterexample; not an integer-weight counterexample','m':m,'t':t,'class_sizes':ns,'profiles':[j for j,bit in zip(js,chosen) if bit],'M':z,'s':s,'C':math.comb(m-1,t-1),'ratio':str(Fraction(sum(a*a for a in z),den*s)),'checked':checked}
                    (out/'PROFILE_OBSTRUCTION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return
        if time.monotonic()-start>45:
            result={'status':'EVIDENCE only; no obstruction found before time cap','exact_profile_families':exact_cases,'subset_checks':checked,'elapsed':time.monotonic()-start}
            (out/'PROFILE_OBSTRUCTION.json').write_text(json.dumps(result,indent=2));print(result);return
    result={'status':'EVIDENCE only; no obstruction found in completed prescribed search','exact_profile_families':exact_cases,'subset_checks':checked,'elapsed':time.monotonic()-start}
    (out/'PROFILE_OBSTRUCTION.json').write_text(json.dumps(result,indent=2));print(result)
if __name__=='__main__':main()
