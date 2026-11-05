"""Astra's independent interval certificate. No supplied numerical code used.
Run from this directory: python verify_a.py --n 4096
Only mpmath's directed interval primitives are trusted; FFT is written here.
"""
import os
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
import json, argparse, time
from pathlib import Path
from mpmath import iv, mp
ROOT=Path(__file__).resolve().parent
iv.dps=50
mp.dps=65
I=iv.mpf
LN2=iv.ln(2)
def lg(x): return iv.ln(x)/LN2
def pow2(x): return iv.exp(LN2*x)
def upper(x): return I(x.b)
def lower(x): return I(x.a)
def inflate(x,e): return x+I([-upper(e),upper(e)])
def textiv(x):
    # Decimal rendering OUTWARD by EXACT INTEGER division of binary endpoints.
    # Do not multiply an endpoint in rounded floating arithmetic before floor.
    places=35; scale=10**places
    def endpoint(t,up):
        sign,man,exponent,_=t
        num=(-man if sign else man)*scale
        if exponent>=0: num <<= exponent; den=1
        else: den=1<<(-exponent)
        z=-((-num)//den) if up else num//den
        prefix='-' if z<0 else ''; z=abs(z)
        whole,frac=divmod(z,scale)
        return prefix+str(whole)+'.'+str(frac).zfill(places)
    return '['+endpoint(x._mpi_[0],False)+', '+endpoint(x._mpi_[1],True)+']'
def entropy(x): return -x*lg(x)-(1-x)*lg(1-x)
def load():
    raw=json.loads((ROOT.parent/'A_referee_and_base_core'/'candidate_ternary.json').read_text())
    return {k:I(v) for k,v in raw.items() if k in ['tau0','eta','mu','a','c','gamma','l','kappa','p','q_m','epsilon','zeta','input_guard_coefficient']}, [I(x) for x in raw['rc']], [I(x) for x in raw['sc']]
def scalars(d):
    t,e,m,a,c,g,l,k,p,q,eps,z,guard=[d[x] for x in ['tau0','eta','mu','a','c','gamma','l','kappa','p','q_m','epsilon','zeta','input_guard_coefficient']]
    r=1-m-l; ap=a+c; D=e-t; G=2*t-e; ag=D/G
    H=-a*lg(a)-c*lg(c)-(1-ap)*lg(1-ap); hy=entropy(I('.5')-a+c)
    sl={
      'C1R':(entropy(2*a)+entropy(2*c))/2-g,
      'C2R':t-l-(H-g)*m,
      'C3':t-r-(1-g)*m,
      'C4R':t-(1-m+(H+hy-g)*m-e),
      'C5R-left':2*t-I('.5')-H*m,
      'C5R-right':2*t-I('.5')-hy*m,
      'C6-r-positive':r,'C6-r-upper':t-r,'C6-l-upper':t-l,
      'MU1':l-m,'MU2':I('.5')-m,
      'A4R':e-m*(entropy(2*ap)+2*ap),
      'A4R-domain':I('.5')-2*ap,'SR':I('.11')-ap,
      'SR-entropy':I('.5')-entropy(ap),
      'preliminary':I('.5')-t,
      'exact-M-merge':t-m,
      'small-prime-total':2*t-I('.5')-z-g*m/2,
      'right-key-sort-total':2*t-I('.5')-z-r,
      'large-prime-draw':t+20*eps-e/2,
      'Delta':D,'Gamma':G,'row-error':I('.75')-ag,
      'p':p-1,'q':q-1,'kappa':k,
      'rho-gap':I('.000001'),
      'B3-p':I('.0000015')-(18+6*p)*eps,
      'B3-q':I('.0000015')-(18+6*q)*eps,
      'a-positive':a,'c-positive':c,'gamma-positive':g,
      'mask-domain-inside':I('.5')-a,'mask-domain-outside':I('.5')-c,
      'right-mask-lower':I('.5')-a+c,'right-mask-upper':I('.5')+a-c,
      'mu-positive':m,'l-positive':l,'eta-positive':e}
    keys=['C1R','C2R','C3','C4R','C5R-left','C5R-right','C6-r-positive','C6-r-upper','C6-l-upper','MU1','MU2','A4R','A4R-domain']
    emin=min(lower(sl[x]) for x in keys)
    sl['cap-margin']=emin-1/guard-z
    sl['A4R-after-guard']=sl['A4R']-1/guard
    sl['small-prime-vs-eps0']=sl['small-prime-total']-emin
    sl['right-sort-vs-eps0']=sl['right-key-sort-total']-emin
    return sl, {'T':t+20*eps,'r':r,'a_prime':ap,'Delta':D,'Gamma':G,'a_Gamma':ag,'H3':H,'hY':hy,'epsilon0_lower':emin,'rho_f':e-I('.0000015'),'rho_c':e-I('.0000025')}
def fft(a,inverse=False):
    n=len(a); a=list(a); j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit: j^=bit; bit>>=1
        j^=bit
        if i<j: a[i],a[j]=a[j],a[i]
    size=2
    while size<=n:
        ws=[]
        for j in range(size//2):
            ang=2*iv.pi*j/size*(1 if inverse else -1)
            ws.append(iv.mpc(iv.cos(ang),iv.sin(ang)))
        for start in range(0,n,size):
            for j,w in enumerate(ws):
                u=a[start+j]; v=a[start+j+size//2]*w
                a[start+j]=u+v; a[start+j+size//2]=u-v
        size*=2
    return [x/n for x in a] if inverse else a
def samples(coeff,n):
    # Evaluate via inverse FFT of the exact trigonometric coefficient array.
    a=[iv.mpc(0) for _ in range(n)]; h=len(coeff)//2
    for j in range(1,h+1):
        a[j]=iv.mpc(coeff[j-1],-coeff[h+j-1])*n/2
        a[n-j]=iv.mpc(coeff[j-1],coeff[h+j-1])*n/2
    return [x.real for x in fft(a,True)]
def bound_sums(coeff,s):
    h=len(coeff)//2; amps=[abs(coeff[j])+abs(coeff[h+j]) for j in range(h)]
    ch=[(iv.exp((j+1)*s)+iv.exp(-(j+1)*s))/2 for j in range(h)]
    sh=[(iv.exp((j+1)*s)-iv.exp(-(j+1)*s))/2 for j in range(h)]
    return sum(amps),sum(a*c for a,c in zip(amps,ch)),sum(a*(c-1) for a,c in zip(amps,ch)),sum(a*b for a,b in zip(amps,sh))
def errors(d,rc,sc,n):
    s=I('.04'); si=I('.1'); k=d['kappa']; p=d['p']; q=d['q_m']
    R,Rs,A,B=bound_sums(rc,s); S,Ss,_,_=bound_sums(sc,s)
    theta=LN2*B
    assert upper(theta)<lower(iv.pi/2)
    cost=iv.cos(theta)
    Hb=pow2(2*A)/cost*(Rs+S)
    Lb=R+S+A-lg(cost)+B
    Kb=k*(R+S)
    Ub=abs(k-1)*Hb+Lb+Kb
    Wb=abs(2-k)*Hb+2*Lb+Kb
    delta=d['eta']-d['tau0']; ag=delta/(2*d['tau0']-d['eta'])
    cosh=(iv.exp(s)+iv.exp(-s))/2
    outer1=2*(2+2*cosh)*pow2(p*(delta+Ub))/(iv.exp(s*n)-1)
    outer2=2*(2+2*cosh)*pow2(q*(ag*Wb+Ub))/(iv.exp(s*n)-1)
    _,Ri,_,_=bound_sums(rc,si); _,Si,_,_=bound_sums(sc,si)
    factor=2/(iv.exp(si*n)-1)
    ec=factor*pow2(Ri+Si)
    eh=ec*(Ri+Si)
    ef=factor*pow2(k*Ri); eg=factor*pow2(k*Si)
    return {'strip_outer':s,'strip_inner':si,'theta':theta,'H_strip_bound':Hb,'logC_strip_bound':Lb,'u_strip_bound':Ub,'w_strip_bound':Wb,'inner_C':ec,'inner_H':eh,'inner_Zr':ef,'inner_Zs':eg,'outer_M1':outer1,'outer_M2':outer2}
def controls():
    assert 1 in entropy(I('.5'))
    # Verify FFT correlation orientation on a deliberately asymmetric exact input.
    f=[I(x) for x in [1,2,0,4,3,1,5,2]]; g=[I(x) for x in [2,0,1,3,1,4,2,0]]
    fh=fft(f); gh=fft(g)
    got=fft([fh[j]*gh[(-j)%8] for j in range(8)],True)
    for k in range(8):
        expected=sum(f[(j+k)%8]*g[j] for j in range(8))
        assert expected.a in got[k].real and expected.b in got[k].real
        assert 0 in got[k].imag
    r=s=I(0); C=I(1); H=I(0); K=lg(1)+lg(1)
    assert 0 in (H/C-lg(C)) and 0 in K
    return 'PASS: entropy, asymmetric exact correlation, zero-filter D=A=E=0'
def main():
    arg=argparse.ArgumentParser(); arg.add_argument('--n',type=int,default=4096); arg.add_argument('--bounds-only',action='store_true'); opt=arg.parse_args()
    start=time.monotonic(); n=opt.n; assert n>64 and n&(n-1)==0
    d,rc,sc=load(); sl,derived=scalars(d); err=errors(d,rc,sc,n)
    result={'status':'PROVED by interval certificate conditional on mpmath interval primitives and the analytic bounds in REFEREE_SECTION_T.md','n':n,'iv_dps':iv.dps,'slacks':{x:textiv(v) for x,v in sl.items()},'derived':{x:textiv(v) for x,v in derived.items()},'errors':{x:textiv(v) for x,v in err.items()},'controls':controls()}
    assert all(lower(v)>0 for v in sl.values())
    print('scalar checks and controls PASS; error bounds',result['errors'],flush=True)
    if opt.bounds_only:
        (ROOT/f'A_bounds_{n}.json').write_text(json.dumps(result,indent=2)); return
    assert upper(err['outer_M1'])<I('1e-12') and upper(err['outer_M2'])<I('1e-12')
    r=samples(rc,n); s=samples(sc,n); print('samples ready',flush=True)
    F=[pow2(x) for x in r]; G=[pow2(x) for x in s]
    k=d['kappa']; Zr=inflate(sum(pow2(k*x) for x in r)/n,err['inner_Zr']); Zs=inflate(sum(pow2(k*x) for x in s)/n,err['inner_Zs']); K=lg(Zr)+lg(Zs)
    f=fft(F); g=fft(G); fr=fft([x*y for x,y in zip(F,r)]); gs=fft([x*y for x,y in zip(G,s)])
    cv=fft([f[j]*g[(-j)%n] for j in range(n)],True)
    hv=fft([fr[j]*g[(-j)%n]+f[j]*gs[(-j)%n] for j in range(n)],True)
    print('interval convolutions ready',flush=True)
    M1=I(0); M2=I(0); ag=derived['a_Gamma']; delta=derived['Delta']
    for j in range(n):
        assert 0 in cv[j].imag and 0 in hv[j].imag
        C=inflate(cv[j].real/n,err['inner_C']); H=inflate(hv[j].real/n,err['inner_H'])
        assert lower(C)>0
        h=H/C; L=lg(C); u=(k-1)*h+L-K; w=(2-k)*h-2*L+K
        weight=2+2*iv.cos(2*iv.pi*j/n)
        M1+=weight*pow2(d['p']*(delta-u))/n
        M2+=weight*pow2(d['q_m']*(ag*w-u))/n
    M1=inflate(M1,err['outer_M1']); M2=inflate(M2,err['outer_M2'])
    result['moments']={'log2_M1':textiv(lg(M1)),'log2_M2':textiv(lg(M2)),'slack_M1':textiv(derived['rho_c']-lg(M1)),'slack_M2':textiv(derived['rho_c']-lg(M2))}
    assert upper(lg(M1))<lower(derived['rho_c']) and upper(lg(M2))<lower(derived['rho_c'])
    result['elapsed_seconds_evidence']=time.monotonic()-start
    (ROOT/f'A_certificate_{n}.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result['moments'],indent=2),flush=True)
    print('PASS in',result['elapsed_seconds_evidence'],'seconds',flush=True)
if __name__=='__main__': main()
