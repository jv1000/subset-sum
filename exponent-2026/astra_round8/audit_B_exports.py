"""Post-gate B comparison; exact rational parsing, own interval references."""
import json,re
from fractions import Fraction as F
from pathlib import Path
OUT=Path(__file__).resolve().parent
B=OUT.parent/'B_open_only_after_A_is_written'
def read(p): return json.loads(p.read_text(),parse_float=F)
def interval(s):
    a,b=s.strip('[]').split(','); return F(a.strip()),F(b.strip())
def ball(s):
    a,b=s.strip('[]').split('+/-'); a=F(a.strip()); b=F(b.strip()); return a-b,a+b
def main():
    own=read(OUT/'numbers.json'); bc=read(B/'cert_base_512.json'); kc=read(B/'cert_K16_512x32.json')
    out={'ball_comparisons':{},'proved_bad_bound_exports':[]}
    for name,record in [('base',bc),('K16',kc)]:
        mom=read(OUT/f'moments_{name}_4096.json')['moments']
        for j in (1,2):
            oi=interval(mom[f'log2_M{j}'])
            bs=record[f'log2M{j}'] if name=='base' else record['moments'][j-1]['log2_ball']
            bi=ball(bs)
            assert bi[0]<=oi[1] and oi[0]<=bi[1]
            out['ball_comparisons'][f'{name}_M{j}']='PASS: enclosures overlap; independently established moment inequality survives'
    # Demonstrable violations: compare against the opposite endpoint of our enclosure.
    lo,hi=interval(own['base']['slacks']['C8'])
    x=bc['margins_lower']['C8 (mu/2)log3 < eta']
    assert x>hi
    out['proved_bad_bound_exports'].append({'file':'cert_base_512.json','field':'margins_lower/C8','display':str(x),'issue':'claimed lower bound is above independent upper endpoint','own_interval':own['base']['slacks']['C8']})
    lo,hi=interval(read(OUT/'moments_K16_4096.json')['moments']['log2_M2'])
    x=kc['moments'][1]['log2_upper']; assert x<lo
    out['proved_bad_bound_exports'].append({'file':'cert_K16_512x32.json','field':'moments/1/log2_upper','display':str(x),'issue':'claimed upper bound is below independent lower endpoint','own_interval':read(OUT/'moments_K16_4096.json')['moments']['log2_M2']})
    truegap=F('.48769')-F(own['base']['exact_T'])
    stated=bc['vs_Base_0_48769']
    assert stated-truegap==F('0.0000002')
    out['base_gap_field']={'reported':str(stated),'true_T_gap':str(truegap),'difference':str(stated-truegap),'interpretation':'reported field compares internal tau0, not final threshold T'}
    out['status']='PROVED: these two exported bounds are invalid as directed decimal bounds; ball comparisons pass. Not a failure of the mathematical candidate.'
    (OUT/'B_export_comparison.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
