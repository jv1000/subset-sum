"""Independent checks of the fixed Base constants used in A5 and B2/B3."""
import json
from pathlib import Path
from verify_a import I, lg, textiv, lower
out=Path(__file__).resolve().parent
t=I('.48769'); eta=I('.51613'); mu=I('.473'); zeta=I('.000001')
delta=(eta-mu*lg(3)/2)/2
vals={'A4_delta':delta,'bad_set_removal_margin':delta-(I('.5')-t+zeta),
      'A4_guard_margin':delta-I('.000001'),
      'B2_row_margin':I('.75')-(eta-t)/(2*t-eta),
      'B3_rounding_cost':(18+6*I('418.36'))*I('.00000001'),
      'B3_actual_decay':I('.0002')-(18+6*I('418.36'))*I('.00000001'),
      'B3_claimed_decay_margin':I('.0002')-(18+6*I('418.36'))*I('.00000001')-I('.00017')}
assert all(lower(x)>0 for x in vals.values())
(out/'BASE_CORE_CONSTANTS.json').write_text(json.dumps({k:textiv(v) for k,v in vals.items()},indent=2))
print(json.dumps({k:textiv(v) for k,v in vals.items()},indent=2))
