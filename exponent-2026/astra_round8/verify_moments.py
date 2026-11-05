"""R8-MOM: third independent base certificate, own round-6 interval FFT reused.
Analytic error derivation is given in NUMERICAL_METHOD.md. No supplied verifier used.
"""
import time,json,argparse
from audit_numbers import load,base,k16,OUT
from interval_core import I,iv,lg,pow2,lower,upper,textiv,inflate,errors,controls,samples,fft,scalars
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--candidate',default='base',choices=['base','K16','ternary']); ap.add_argument('--n',type=int,default=4096); args=ap.parse_args()
    start=time.monotonic(); n=args.n; assert n>64 and n&(n-1)==0
    raw,d=load(args.candidate)
    if 'tau0' not in d: d['tau0']=d['tau']
    rc=[I(x) for x in raw['rc']]; sc=[I(x) for x in raw['sc']]
    sl,der=base(d) if args.candidate=='base' else k16(d) if args.candidate=='K16' else scalars(d)
    er=errors(d,rc,sc,n)
    result={'status':'PROVED conditional on interval primitives and analytic bounds in NUMERICAL_METHOD.md','candidate':args.candidate,'N':n,'interval_decimal_precision':iv.dps,
      'controls':controls(),'error_bounds':{k:textiv(v) for k,v in er.items()}}
    assert all(lower(v)>0 for v in sl.values())
    assert upper(er['outer_M1'])<I('1e-12') and upper(er['outer_M2'])<I('1e-12')
    r=samples(rc,n); s=samples(sc,n); F=[pow2(x) for x in r]; G=[pow2(x) for x in s]; k=d['kappa']
    Zr=inflate(sum(pow2(k*x) for x in r)/n,er['inner_Zr']); Zs=inflate(sum(pow2(k*x) for x in s)/n,er['inner_Zs']); K=lg(Zr)+lg(Zs)
    f=fft(F); g=fft(G); fr=fft([x*y for x,y in zip(F,r)]); gs=fft([x*y for x,y in zip(G,s)])
    cv=fft([f[j]*g[(-j)%n] for j in range(n)],True)
    hv=fft([fr[j]*g[(-j)%n]+f[j]*gs[(-j)%n] for j in range(n)],True)
    M1=I(0); M2=I(0)
    for j in range(n):
        assert 0 in cv[j].imag and 0 in hv[j].imag
        C=inflate(cv[j].real/n,er['inner_C']); H=inflate(hv[j].real/n,er['inner_H']); assert lower(C)>0
        hh=H/C; L=lg(C); u=(k-1)*hh+L-K; v=(2-k)*hh-2*L+K
        weight=2+2*iv.cos(2*iv.pi*j/n)
        M1+=weight*pow2(d['p']*(der['Delta']-u))/n
        M2+=weight*pow2(d['q_m']*(der['a_Gamma']*v-u))/n
    M1=inflate(M1,er['outer_M1']); M2=inflate(M2,er['outer_M2'])
    result['moments']={'log2_M1':textiv(lg(M1)),'log2_M2':textiv(lg(M2)),
      'slack_M1':textiv(der['rho_c']-lg(M1)),'slack_M2':textiv(der['rho_c']-lg(M2))}
    assert upper(lg(M1))<lower(der['rho_c']) and upper(lg(M2))<lower(der['rho_c'])
    result['elapsed_seconds_evidence']=time.monotonic()-start
    (OUT/f'moments_{args.candidate}_{n}.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
