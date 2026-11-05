"""Output consistency and provenance checks, restricted to Astra_round6."""
import json,hashlib,re
from pathlib import Path
from fractions import Fraction
OUT=Path(__file__).resolve().parent
def endpoints(s):return tuple(Fraction(x.strip()) for x in s.strip('[]').split(','))
def main():
    for name in ['REFEREE_SECTION_T.md','BASE_CORE_ASTRA.md','YP_HALL_K1_ASTRA.md','ROUND6_ASTRA_SUMMARY.md']:
        assert (OUT/name).stat().st_size>1000
    a=json.loads((OUT/'A_certificate_4096.json').read_text());b=json.loads((OUT/'A_certificate_8192.json').read_text())
    for cert in [a,b]:
        assert all(endpoints(s)[0]>0 for s in cert['slacks'].values())
        for k in ['slack_M1','slack_M2']:assert endpoints(cert['moments'][k])[0]>0
    for k in ['log2_M1','log2_M2']:
        x,y=endpoints(a['moments'][k]),endpoints(b['moments'][k]);assert x[0]<=y[0]<=y[1]<=x[1]
    raw=json.loads((OUT.parent/'A_referee_and_base_core'/'candidate_ternary.json').read_text())
    threshold=Fraction(raw['tau0'])+20*Fraction(raw['epsilon']);assert threshold==Fraction('0.4873407528')
    ctrl=json.loads((OUT/'B_CONTROLS.json').read_text())['negative']
    assert Fraction(ctrl['Q'])==Fraction(29,28) and Fraction(ctrl['near_miss_supply'])==30 and Fraction(ctrl['target_capacity'])==27
    assert not json.loads((OUT/'B_SEARCH.json').read_text())['failures']
    rows=['# Scalar slack certificate','','PROVED — Every interval below is an outward enclosure from verify_a.py, rendered by exact integer division of binary endpoints. All lower endpoints are positive. Conditions and source citations are in REFEREE_SECTION_T.md.','','| Status | Check | Slack interval |','|---|---|---|']
    rows+=['| PROVED | '+k+' | '+v+' |' for k,v in a['slacks'].items()]
    (OUT/'SCALAR_SLACKS.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    manifest={}
    for folder in ['A_referee_and_base_core','B_open_only_after_A_is_written']:
        for p in sorted((OUT.parent/folder).rglob('*')):
            if p.is_file():manifest[str(p.relative_to(OUT.parent))]=hashlib.sha256(p.read_bytes()).hexdigest()
    (OUT/'INPUT_SHA256.json').write_text(json.dumps(manifest,indent=2))
    # Compile our source text without emitting bytecode or importing extra modules.
    for p in OUT.glob('*.py'):compile(p.read_text(encoding='utf-8'),str(p),'exec')
    summary=(OUT/'ROUND6_ASTRA_SUMMARY.md').read_text(encoding='utf-8')
    result={'status':'PROVED finite checks passed; provenance hashes do not authenticate the claimed commit','scalar_checks':len(a['slacks']),'moment_grids':[a['n'],b['n']],'exact_threshold_fraction':str(threshold),'summary_whitespace_words':len(summary.split()),'negative_control_Q':ctrl['Q'],'outputs':[p.name for p in sorted(OUT.iterdir()) if p.is_file()]}
    (OUT/'FINAL_CHECK.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
