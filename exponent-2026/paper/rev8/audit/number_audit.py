"""Number audit of paper.tex against the frozen candidate files and certificates (Claude, 2026-11-05).
Every decimal with >= 4 significant digits in paper.tex is matched to a source value; matches report the rounding
direction. Exponent-like values (T, tau0, the 'time' exponents) printed BELOW their source are flagged as errors."""
import json, re, sys
from decimal import Decimal as D, getcontext
getcontext().prec = 50
S = '/sessions'  # placeholder
import os
H = os.path.expanduser('~/mnt'); L = H + '/SubsetSum/C3_target_048_Claude'
truth = {}
def add(name, v):
    try: truth[name] = D(str(v).strip('[').split('+/-')[0].strip())
    except Exception: pass
for tag, f in [('base', L + '/candidate_base.json'), ('K16', L + '/candidate_K16.json'),
               ('tern', H + '/Fable_review/Fable_round2/candidate_ternary.json')]:
    d = json.load(open(f))
    for k, v in d.items():
        if isinstance(v, (str, int, float)): add(tag + '.' + k, v)
cb = json.load(open(L + '/cert_base_512.json'))
add('base.log2M1', cb['log2M1']); add('base.log2M2', cb['log2M2'])
for k, v in cb['margins_lower'].items(): add('base.margin.' + k, v)
ck = json.load(open(L + '/cert_K16_512x32.json'))
for k, v in ck['margins_lower'].items(): add('K16.margin.' + k, v)
def walk(o, p):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, p + '.' + k)
    elif isinstance(o, (str, int, float)): add(p, o)
walk(ck, 'K16cert')
add('tern.log2M1', '0.515991874058657786476412457204096'); add('tern.log2M2', '0.515991620470147941891150956423223')
eps = D('1e-8')
add('T.base', truth['base.tau0'] + 20*eps); add('T.tern', truth['tern.tau0'] + 20*eps); add('T.K16', truth['K16.tau'] + 20*eps)
add('JoshuaQFEX', '0.487676'); add('Base.tau0', '0.48769')
add('gap.base_vs_JQ', D('0.487676') - truth['T.base']); add('gap.base_vs_Base', D('0.48769') - truth['T.base'])
add('gap.tern_vs_base', truth['T.base'] - truth['T.tern']); add('gap.tern_vs_JQ', D('0.487676') - truth['T.tern'])
add('tern.floating_tau0', '0.48734025273556014')
for line in open(H + '/SubsetSum/Astra_round6/out/SCALAR_SLACKS.md', encoding='utf-8'):
    m = re.match(r'\| PROVED \| (\S+) \| \[([0-9.]+),', line)
    if m: add('tern.slack.' + m.group(1), m.group(2))
EXPONENTISH = ('T.', 'base.tau0', 'tern.tau0', 'K16.tau', 'base.floating_T', 'K16.floating_T')

tex = open(H + '/SubsetSum/preprint/paper.tex', encoding='utf-8').read()
body = tex[tex.index('\\begin{document}'):tex.index('\\begin{thebibliography}')]
num = re.compile(r'(?<![\d.])(\d+\.\d+)(?:\s*\\times\s*10\^\{(-?\d+)\})?')
rows = []; seen = {}
for m in num.finditer(body):
    s, e = m.group(1), m.group(2)
    x = D(s) * (D(10) ** int(e) if e else 1)
    sig = len(s.replace('.', '').lstrip('0'))
    if sig < 4: continue
    dec = D(10) ** (-(len(s.split('.')[1])) + (int(e) if e else 0))
    best = None
    cands = [(abs(x - v), (0 if k.startswith('T.') else 1), k, v) for k, v in truth.items() if v != 0 and abs(x - v) < dec * D('1.0000001')]
    if cands:
        cands.sort(key=lambda c: (c[1], c[0]) if c[0] <= dec * D('0.5000001') else (2, c[0]))
        _, _, k, v = cands[0]; best = (k, v, 'nearest')
    ctx = body[max(0, m.start()-50):m.end()+20].replace('\n', ' ')
    key = (s, e)
    if key in seen: seen[key] += 1; continue
    seen[key] = 1
    rows.append((s + ('e' + e if e else ''), best, ctx))
bad = []; unmatched = []
for s, best, ctx in rows:
    if best is None: unmatched.append((s, ctx)); continue
    k, v, how = best
    if how == 'nearest':
        x = D(s.split('e')[0]) * (D(10) ** int(s.split('e')[1]) if 'e' in s else 1)
        how = 'exact' if x == v else ('up' if x > v else 'down')
    flag = ''
    if how == 'down' and k.startswith(EXPONENTISH): flag = '  <== EXPONENT ROUNDED DOWN'
    if how == 'up' and k.startswith('gap.'): flag = '  (gap rounded up: overstates the improvement slightly)'
    print('%-22s %-26s %-6s%s' % (s, k, how, flag)); (print('      ctx: ...' + ctx + '...') if (k.startswith(EXPONENTISH) or flag) else None)
    if flag.startswith('  <=='): bad.append(s)
print('\nUNMATCHED (need a human/source check):')
for s, ctx in unmatched: print('  %-16s ...%s...' % (s, ctx))
print('\nmatched %d, unmatched %d, exponent-rounded-down %d' % (len(rows) - len(unmatched), len(unmatched), len(bad)))
