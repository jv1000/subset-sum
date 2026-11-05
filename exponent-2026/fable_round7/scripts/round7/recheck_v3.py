"""R7-C1: the frozen ternary point is unchanged, and no condition's numbers moved (Section T v2 -> v3 is text only).
Usage (from Fable_round2): python -I scripts/round7/recheck_v3.py
"""
import sys, os, json, hashlib, subprocess, tempfile, shutil
from decimal import Decimal
HERE = os.path.dirname(os.path.abspath(__file__))
R2 = os.path.join(HERE, '..', 'round2')
JSON = os.path.join(HERE, '..', '..', 'candidate_ternary.json')
SCRIPTS = os.path.join(HERE, '..', '..', '..', 'scripts')          # Fable_review/scripts (moments_arb.py)
sys.path.insert(0, SCRIPTS)
from flint import arb
from moments_arb import S, set_prec
set_prec(200)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
out = []


def P(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    out.append(s)


# 1. sha256
EXPECT = 'ea2f10e89ea5f0073479e1e41cc5e22ffda31a5655966ee3f458e8cff25c422b'
h = hashlib.sha256(open(JSON, 'rb').read()).hexdigest()
P('1. sha256(candidate_ternary.json) =', h, 'MATCH' if h == EXPECT else 'MISMATCH')


# 2. re-run the round-2 certificate and compare with the recorded output
def run_checker(json_path):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    if json_path == JSON:
        script = os.path.join(R2, 'check_ternary_point.py')
    else:
        # the checker reads ../../candidate_ternary.json and ../../../scripts/moments_arb.py relative to itself:
        # rebuild that layout under a temp root
        root = tempfile.mkdtemp(prefix='r7ctrl_')
        d2 = os.path.join(root, 'F', 'scripts', 'round2')
        os.makedirs(d2)
        os.makedirs(os.path.join(root, 'scripts'))
        shutil.copy(os.path.join(R2, 'check_ternary_point.py'), d2)
        shutil.copy(json_path, os.path.join(root, 'F', 'candidate_ternary.json'))
        shutil.copy(os.path.join(SCRIPTS, 'moments_arb.py'), os.path.join(root, 'scripts', 'moments_arb.py'))
        script = os.path.join(d2, 'check_ternary_point.py')
    r = subprocess.run([sys.executable, '-I', script, '4096', '8192'], capture_output=True, text=True, env=env)
    return r.stdout + r.stderr


def cond_lines(txt):
    # the N= lines end with an elapsed-time string "(Ns)": drop it (amendment after the first run, see PREREG_R7.md)
    import re
    return [re.sub(r'\s*\(\d+s\)\s*$', '', l.rstrip()) for l in txt.splitlines()
            if l.startswith(('PASS', 'FAIL', 'info', 'N=', 'eps0'))]


rec = open(os.path.join(R2, 'out', 'ternary_certificate_N4096_8192.txt'), encoding='utf-8').read()
new = run_checker(JSON)
a, b = cond_lines(rec), cond_lines(new)
same = a == b
P('2. checker lines recorded/new:', len(a), len(b), 'IDENTICAL' if same else 'DIFFER')
if not same:
    for x, y in zip(a, b):
        if x != y:
            P('   recorded:', x)
            P('   new     :', y)
npass = sum(l.startswith('PASS') for l in b)
nfail = sum(l.startswith('FAIL') for l in b)
P('   PASS', npass, 'FAIL', nfail, '| final line:', new.strip().splitlines()[-1] if new.strip() else '(no output)')

# 3. Astra's extra scalar checks, arb vs Astra's 35-digit intervals
J = json.load(open(JSON))
t, e, m, a_, c_, g, l = (S(J[k]) for k in ('tau0', 'eta', 'mu', 'a', 'c', 'gamma', 'l'))
eps, z, guard = S(J['epsilon']), S(J['zeta']), S(J['input_guard_coefficient'])
ln2 = arb(2).log()
hh = lambda x: -(x * x.log() + (1 - x) * (1 - x).log()) / ln2
r = 1 - m - l
ap = a_ + c_
half = arb(1) / 2
H3 = -(a_ * a_.log() + c_ * c_.log() + (1 - ap) * (1 - ap).log()) / ln2
hy = hh(half - a_ + c_)
base = {'C1R': (hh(2 * a_) + hh(2 * c_)) / 2 - g, 'C2R': t - l - (H3 - g) * m, 'C3': t - r - (1 - g) * m,
        'C4R': t - (1 - m + (H3 + hy - g) * m - e), 'C5R-left': 2 * t - half - H3 * m,
        'C5R-right': 2 * t - half - hy * m, 'C6-r-positive': r, 'C6-r-upper': t - r, 'C6-l-upper': t - l,
        'MU1': l - m, 'MU2': half - m, 'A4R': e - m * (hh(2 * ap) + 2 * ap), 'A4R-domain': half - 2 * ap}
emin = min(base.values(), key=lambda v: float(v.lower()))
extra = {'preliminary': half - t, 'exact-M-merge': t - m,
         'small-prime-total': 2 * t - half - z - g * m / 2,
         'right-key-sort-total': 2 * t - half - z - r,
         'large-prime-draw': t + 20 * eps - e / 2,
         'cap-margin': emin - 1 / guard - z,
         'A4R-after-guard': base['A4R'] - 1 / guard,
         'small-prime-vs-eps0': 2 * t - half - z - g * m / 2 - emin,
         'right-sort-vs-eps0': 2 * t - half - z - r - emin}
ASTRA = {  # SCALAR_SLACKS.md (Astra, 2025-11-04 22:04)
    'preliminary': ('0.01265944719999999999999999999999999', '0.01265944720000000000000000000000001'),
    'exact-M-merge': ('0.01266104729999999999999999999999999', '0.01266104730000000000000000000000001'),
    'small-prime-total': ('0.46035201421973377277499999999999999', '0.46035201421973377277500000000000001'),
    'right-key-sort-total': ('0.43336318559999999999999999999999999', '0.43336318560000000000000000000000001'),
    'large-prime-draw': ('0.22934204504999999999999999999999999', '0.22934204505000000000000000000000001'),
    'cap-margin': ('0.00000097944610694028886216648638658', '0.00000097944610694028886216648638659'),
    'A4R-after-guard': ('0.45871419888288432306120304859186510', '0.45871419888288432306120304859186511'),
    'small-prime-vs-eps0': ('0.46035101477362683248613783351361341', '0.46035101477362683248613783351361342'),
    'right-sort-vs-eps0': ('0.43336218615389305971113783351361341', '0.43336218615389305971113783351361342')}
P('3. Astra-named scalar checks (arb 200 bits) vs SCALAR_SLACKS.md intervals:')
allin = True
for k, v in extra.items():
    lo, hi = (S(x) for x in ASTRA[k])
    inside = bool(v.lower() >= lo.lower() - S('1e-34')) and bool(v.upper() <= hi.upper() + S('1e-34'))
    pos = bool(v > 0)
    allin &= inside and pos
    P(f'   {k:22s} {v.str(20):40s} {"inside" if inside else "OUTSIDE"} {"positive" if pos else "NOT positive"}')
P('   all inside and positive:', allin)
P('   eps0 (least slack of C1R..A4R-domain, lower end) =', emin.str(8))

# 4. control: tau0 - 2e-6 must FAIL
Jc = dict(J)
Jc['tau0'] = str(Decimal(J['tau0']) - Decimal('0.000002'))
tmpj = os.path.join(tempfile.gettempdir(), 'candidate_ternary_CONTROL.json')
json.dump(Jc, open(tmpj, 'w'), indent=1)
hc = hashlib.sha256(open(tmpj, 'rb').read()).hexdigest()
ctrl = run_checker(tmpj)
cl = cond_lines(ctrl)
cf = [x.split()[1] for x in cl if x.startswith('FAIL')]
P('4. CONTROL tau0-2e-6: sha256', hc[:16] + '...', 'differs' if hc != h else 'SAME(!)', '| FAIL conditions:', cf,
  '| final line:', ctrl.strip().splitlines()[-1] if ctrl.strip() else '(no output)')
ok = (h == EXPECT) and same and nfail == 0 and allin and all(x in cf for x in ('C2R', 'C3', 'C4R')) \
    and 'SOME CONDITION FAILS' in ctrl
P('R7-C1 RESULT:', 'ALL PREDICTIONS MET' if ok else 'SOME PREDICTION NOT MET')
open(os.path.join(HERE, 'out', 'recheck_v3.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
open(os.path.join(HERE, 'out', 'checker_rerun_N4096_8192.txt'), 'w', encoding='utf-8').write(new)
open(os.path.join(HERE, 'out', 'checker_control_tau0_minus_2e-6.txt'), 'w', encoding='utf-8').write(ctrl)
