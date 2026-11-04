"""Claude's independent (mpmath iv) recomputation of Astra's twelve K=8 scalar margins + floors. Formulas typed from RESULT.md."""
import json
from fractions import Fraction as F
from mpmath import iv
iv.prec = 200
def I(x): x = F(x); return iv.mpf(x.numerator) / x.denominator
def H2(x): return -(x*iv.log(x) + (1-x)*iv.log(1-x))/iv.log(2)
h = 2 - I(F(3,4))*iv.log(3)/iv.log(2)
P = dict(K=8, mu='.122', d='.0206', gamma='.47939', tau='.4799998', cap='.48', eta='.67', d0='.02005', d1='.020025', c0='.0001', g='.00001')
K = P['K']; mu, d, gam, tau, cap, eta, d0, d1, c0, g = [I(P[k]) for k in ['mu','d','gamma','tau','cap','eta','d0','d1','c0','g']]
m = dict(blocks=1-K*mu, list=tau-(I('.5')+(h-I('.5')-gam)*mu), pairs=tau-(1+(2*h-1-gam)*mu-eta+g),
         local_to_prime=I('.5')-d-gam, coverage=1-d0/(K*d*mu)-c0, prelim_cheb=d0-d1, prelim_cap=cap-(I('.5')-d1),
         sparse=eta-H2(mu)-mu-g, setup=tau-I('.25')-mu, prime=tau-eta/2, Delta=eta-tau, Gamma=2*tau-eta)
out = {k: [float(v.a), float(v.b), bool(v.a > 0)] for k, v in m.items()}
a = (eta-tau)/(2*tau-eta); out['a'] = float(a.a); out['qm_cap'] = float((30/(4*a+3)).a)
out['T=tau+20eps'] = float((tau+20*I('1e-8')).b)
print(json.dumps(out, indent=1))
