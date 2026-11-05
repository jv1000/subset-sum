"""R8-BLOCK. Directed interval proof over all p in [1,10], not sampling."""
import json,time
from pathlib import Path
from interval_core import I,iv,lg,entropy,lower,upper,textiv
OUT=Path(__file__).resolve().parent
def g(p):
    b=1/(1+p)
    return (1+p)*(b+lg(iv.gamma(b+I('.5')))-lg(iv.pi)/2-lg(iv.gamma(b+1)))
def main():
    start=time.monotonic(); h=entropy(I('.25')); C=I('.5')/(1-h)
    tau=I('.484'); guard=I('.00001'); D=C*(I('.5')-tau)+guard
    # Controls: b=1/2 gives exact elementary expression; b=1 gives integral 1.
    ctrl=2*lg(2*iv.sqrt(2)/iv.pi)
    assert not (upper(ctrl)<lower(g(I(1))) or upper(g(I(1)))<lower(ctrl))
    assert 0 in g(I(0))
    # g is nonincreasing by monotonicity of power means. At each cell use g(p_right).
    bounds=[]
    for j in range(9000):
        pL=I(1)+I(j)/1000; pR=I(1)+I(j+1)/1000
        bound=1-tau+(pL-1)*D+g(pR)
        assert lower(bound)>0
        bounds.append(lower(bound))
    out={'status':'PROVED for the stated continuous-circle sufficient budget and p in [1,10]',
      'tau_upper':'.484','p_interval':['1','10'],'cells':9000,
      'Delta_min':textiv(D),'coefficient_C':textiv(C),
      'minimum_cell_lower_bound':textiv(min(bounds)),
      'p_equals_1_margin':textiv(1-tau+g(I(1))),
      'controls':'PASS: elementary p=1 gamma identity and p=0 normalization',
      'elapsed_seconds_evidence':time.monotonic()-start}
    (OUT/'blocking.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
