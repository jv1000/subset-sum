"""Own round-8 audit. Exact decimal inputs; directed intervals for entropy.
Prediction/controls: REGISTER R8-NUM. Run python audit_numbers.py.
"""
import json
from fractions import Fraction as F
from pathlib import Path
from interval_core import I, iv, entropy as h, lg, textiv, lower, scalars
OUT=Path(__file__).resolve().parent
SRC=OUT.parent/'A_paper_and_sources'/'candidates'
def exact(x):
    # All requested exact outputs terminate in base ten.
    sign='-' if x<0 else ''; x=abs(x); n,d=x.numerator,x.denominator
    k=0
    while 10**k%d: k+=1
    n*=10**k//d
    s=str(n).zfill(k+1)
    return sign+(s[:-k]+'.'+s[-k:] if k else s)
def base(d):
    t,e,m,a,g,l,eps,z=[d[k] for k in ('tau0','eta','mu','a','gamma','l','epsilon','zeta')]
    r=1-m-l; delta=e-t; gam=2*t-e; ag=delta/gam
    c={'C1':h(2*a)/2-g,'C2':t-l-(h(a)-g)*m,
       'C3':t-r-(1-g)*m,'C4':t-1+m-(h(a)+h(I('.5')-a)-g)*m+e,
       'C5':2*t-I('.5')-h(I('.5')-a)*m,
       'C6-r-positive':r,'C6-r-upper':t-r,'C6-l-upper':t-l,
       'C7':l-m*(1-2*a),'C8':e-m*lg(3)/2}
    emin=min(lower(x) for x in c.values())
    c.update({'S1':1-4*a,'S2-half':I('.5')-m*(1-2*a),
       'S3-conservative':1-2*a-h(2*a)/2-h(a),
       'left-mask-cost':2*t-I('.5')-h(a)*m,
       'merge-M':t-m,'preliminary':I('.5')-t,
       'A5-threshold':(e-m*lg(3)/2)/2-(I('.5')-t+z),
       'small-prime-total':2*t-I('.5')-z-g*m/2,
       'right-key-sort-total':2*t-I('.5')-z-r,
       'cap':emin-1/d['input_guard_coefficient']-z,
       'prime-draw':t+20*eps-e/2,'Delta':delta,'Gamma':gam,
       'p-lower':d['p']-1,'q-lower':d['q_m']-1,
       '3p':30-3*d['p'],'qcap':30-d['q_m']*(4*ag+3),
       'row-error':I('.75')-ag,'B3-p':I('.0000015')-(18+6*d['p'])*eps,
       'B3-q':I('.0000015')-(18+6*d['q_m'])*eps})
    return c,{'T':t+20*eps,'r':r,'Delta':delta,'Gamma':gam,'a_Gamma':ag,
      'epsilon0_lower':emin,'A5-delta':(e-m*lg(3)/2)/2,
      'S3-entropy-LHS':h(2*a)/2+h(a),'rho_f':e-I('.0000015'),'rho_c':e-I('.0000025'),
      'alias-floor':(1-delta)/2,
      'bound-i':I('.5')-m*(g-h(a)/2),
      'bound-ii':(1-delta+m*(h(a)-g+h(I('.5')-a)-1))/2,
      'bound-iii':(I('.5')+m*h(I('.5')-a))/2,
      'true-disjoint-overhead':m*(h(a)+h(I('.5')-a)-1-h(2*a)/2),
      'C4-overhead':m*(h(a)+h(I('.5')-a)-1-g),
      'representation-slack-extra':m*(h(2*a)/2-g)}
def k16(d):
    t,e,m,g,eps=[d[k] for k in ('tau','eta','mu','gamma','epsilon')]
    K=16; c0=I('.0001'); dd=I('.5')-g-I('1e-8')
    d0=(1-c0)*K*dd*m*(1-I('1e-7')); d1=d0-I('1e-9'); cap=t+20*eps
    D=e-t; G=2*t-e; ag=D/G
    s={'blocks':1-K*m,'list':t-I('.5')-(h(I('.25'))-I('.5')-g)*m,
       'pairs':t-1-(2*h(I('.25'))-1-g)*m+e-d['guard'],
       'sparse':e-h(m)-m-d['guard'],'setup':cap-m-I('.25'),
       'prime':cap-e/2,'prelim-cap':cap-I('.5')+d1,
       'local-deficiency':I('.5')-dd-g,'probability':1-d0/(K*dd*m)-c0,
       'd0-d1':d0-d1,'Delta':D,'Gamma':G,'3p':30-3*d['p'],
       'qcap':30-d['q_m']*(4*ag+3),'p-lower':d['p']-1,'q-lower':d['q_m']-1,
       'rho-f-gap':I('5e-7'),'rho-c-gap':I('1e-6')}
    return s,{'T':cap,'d':dd,'d0':d0,'d1':d1,'Delta':D,'Gamma':G,'a_Gamma':ag,
      'rho_f':e-48*eps-I('5e-7'),'rho_c':e-48*eps-I('1.5e-6')}
def load(name):
    raw=json.loads((SRC/f'candidate_{name}.json').read_text())
    d={k:I(v) for k,v in raw.items() if isinstance(v,str) and k in
       ('tau0','tau','eta','mu','a','c','gamma','l','epsilon','zeta','input_guard_coefficient','kappa','p','q_m','guard')}
    return raw,d
def main():
    results={}; Ts={}
    for name in ('base','K16','ternary'):
        raw,d=load(name); ss,der=(base(d) if name=='base' else k16(d) if name=='K16' else scalars(d))
        assert all(lower(v)>0 for v in ss.values())
        T=F(raw.get('tau0',raw.get('tau')))+20*F(raw['epsilon']); Ts[name]=T
        rounded={'base':'0.4875755','K16':'0.4894616','ternary':'0.4873408'}[name]
        assert F(rounded)>T
        results[name]={'exact_T':exact(T),'valid_strict_upward_exponent':rounded,
          'slacks':{k:textiv(v) for k,v in ss.items()},'derived':{k:textiv(v) for k,v in der.items()}}
        results[name]['exact_decimal_parameters']={k:v for k,v in raw.items() if k in d}
        results[name]['uniform_trigonometric_bounds']={side:textiv(sum(iv.sqrt(I(raw[side][j])**2+I(raw[side][16+j])**2) for j in range(16))) for side in ('rc','sc')}
    results['exact_gaps']={'Joshua-minus-base':exact(F('.487676')-Ts['base']),
        'Base-printed-minus-base':exact(F('.4877')-Ts['base']),
        'Base-tau0-minus-base':exact(F('.48769')-Ts['base']),
        'base-minus-ternary':exact(Ts['base']-Ts['ternary']),
        'Joshua-minus-ternary':exact(F('.487676')-Ts['ternary']),
        'OpenAI-.489995-minus-K16':exact(F('.489995')-Ts['K16'])}
    # Printed three-way equalities in section 10: these discrepancies are exact.
    results['critical_type_table_exact_discrepancies']={
      'v-minus-Gamma':exact(F('.46036')-F('.46074')),
      'D-minus-tau':exact(F('.48942')-F('.4898')),
      'moment-minus-eta':exact(F('.51882')-(F('.4898')+F('.02906')))}
    results['status']='PROVED: directed interval scalar checks; exact decimal arithmetic for exponents and differences. Experimental optimizer outputs not recomputed.'
    results['YeLi_exact_exponent_fraction']=str(F(1,2)-F(1,450000))
    assert F('.4999978')>F(1,2)-F(1,450000)
    (OUT/'numbers.json').write_text(json.dumps(results,indent=2))
    print(json.dumps({k:v['exact_T'] for k,v in results.items() if isinstance(v,dict) and 'exact_T' in v},indent=2))
    print(json.dumps(results['exact_gaps'],indent=2)); print('All scalar controls and positive slacks PASS')
if __name__=='__main__': main()
