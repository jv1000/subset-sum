"""Exact illustrative obstruction and t=2 proof controls; no floating numbers."""
from fractions import Fraction as F
from pathlib import Path
import json,math
from yp_k1 import calc,general_control
out=Path(__file__).resolve().parent
profiles=[(2,0,0),(1,1,0),(1,0,1),(0,1,1)]
theta=[F(1),F(3,5),F(3,5),F(1,5)]
M=[sum(x*j[c] for x,j in zip(theta,profiles)) for c in range(3)]
lhs=sum(x*x for x in M); spectral_rhs=6*sum(x*x for x in theta); true_rhs=6*sum(theta)
assert lhs>spectral_rhs and lhs<true_rhs
examples=[([0,0,1,4],2),([0,0,1,1],2),([0,0,0,1,4,16],2),([0,0,1,3,9,13],3),([0,0,1,4,16,64],3),([0,0,0,1,4,16],3)]
results={'spectral_obstruction':{'class_sizes':[2,1,1],'m':4,'t':2,'profiles':profiles,'theta':[str(x) for x in theta],'M':[str(x) for x in M],'lhs':str(lhs),'spectral_rhs':str(spectral_rhs),'correct_l1_rhs':str(true_rhs)},'instances':[calc(w,t,True) for w,t in examples]}
for v in results['instances']: assert F(v['Q'])<=1 and F(v['Hall_ratio'])<=1
(out/'B_EXAMPLES.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results['spectral_obstruction'],indent=2))
for v in results['instances']:print(v['weights'],v['t'],'Q',v['Q'],'Hall',v['Hall_ratio'],'local',v['local_ratio'])
