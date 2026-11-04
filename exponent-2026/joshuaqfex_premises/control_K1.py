"""K1: Route A machinery reproduces Claude's Round 5 rigorous OpenAI-paper moments (paper parameters):
   1.428968434779451821837...  and  1.428847009317706360116...  (moment_cert_claude.py, N=160, beta=.19)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import routeA_flint as R
pad = lambda v: v + ['0'] * (8 - len(v))
d = dict(tau0='0.48996', eta='0.51772',
         filters=[dict(kappa='1.0315', r_coef=pad(["0.851", "0.466", "0.325", "0.253", "0.224", "-0.314"]),
                       s_coef=pad(["1.281", "-0.938", "0.731", "-0.559", "0.391", "0.110"]))])
FD, xs, N, h = R.build(d, 128, 16, R.A('0.1'))
m1, e1, _ = R.certify(d, FD, xs, N, h, dict(v=0, case='case1', cons=[], z=['8.5', '0'], lo=None, hi=None))
m2, e2, _ = R.certify(d, FD, xs, N, h, dict(v=0, case='band', cons=[], z=['8.3', '0'], lo='1', hi=None))
ref1, ref2 = R.A('1.428968434779451821837010784168561896235096441352459340145224751'), R.A('1.428847009317706360116238287982525344685708510877265741754253143')
out = dict(N_out=N, moment1=m1.str(25), moment2=m2.str(25), outer_err=[e1.str(3), e2.str(3)],
           ref_round5=[ref1.str(25), ref2.str(25)], diff=[float(abs(m1 - ref1).upper()), float(abs(m2 - ref2).upper())])
out['pass'] = out['diff'][0] < 1e-10 and out['diff'][1] < 1e-10
print(json.dumps(out, indent=1)); json.dump(out, open(sys.argv[1], 'w'), indent=1)
