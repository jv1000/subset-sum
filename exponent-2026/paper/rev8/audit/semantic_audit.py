"""Semantic number audit (v2, Claude 2026-11-05). Each row names a claim in paper.tex by an exact text snippet, the
quantity it states, its true value (computed from the frozen candidate files / certificates), and the rounding
direction the claim must have: 'up' (printed >= true: exponents, upper bounds), 'down' (printed <= true: margins,
lower bounds, floors, gaps claimed as improvements), 'eq' (exact decimal). Replaces the value-only matcher."""
import json, os, sys
from mpmath import mp, mpf, log
mp.dps = 50
H = os.path.expanduser('~/mnt'); L = H + '/SubsetSum/C3_target_048_Claude'
cb = json.load(open(L + '/candidate_base.json')); ct = json.load(open(H + '/Fable_review/Fable_round2/candidate_ternary.json'))
ck = json.load(open(L + '/candidate_K16.json')); cert = json.load(open(L + '/cert_base_512.json'))
e = mpf('1e-8'); Tb = mpf(cb['tau0']) + 20*e; Tt = mpf(ct['tau0']) + 20*e; Tk = mpf(ck['tau']) + 20*e
h = lambda x: -x*log(x, 2) - (1-x)*log(1-x, 2)
Db = mpf(cb['eta']) - mpf(cb['tau0'])
m = cert['margins_lower']
rows = [
 ('exponent T (base)', r'T = 0.4875754036$', '0.4875754036', Tb, 'eq'),
 ('time exponent (base)', r'O(2^{0.4875755n})', '0.4875755', Tb, 'up'),
 ('title', r'certified exponent of 0.48758', '0.48758', Tb, 'up'),
 ('exponent K16', "T' > 0.4894615727", '0.4894615727', Tk, 'eq'),
 ('time exponent K16', r'O(2^{0.4894616 n})', '0.4894616', Tk, 'up'),
 ('exponent ternary', "T' > 0.4873407528", '0.4873407528', Tt, 'eq'),
 ('time exponent ternary', r'O(2^{0.4873408n})', '0.4873408', Tt, 'up'),
 ('gap vs JoshuaQFEX', r'$1.005\times10^{-4}$ below JoshuaQFEX', '1.005e-4', mpf('0.487676') - Tb, 'down'),
 ('gap vs Base tau0', r'$1.14\times10^{-4}$ below Base', '1.14e-4', mpf('0.48769') - Tb, 'down'),
 ('gap ternary vs base', r'This is $2.34\times10^{-4}$ below the point above', '2.34e-4', Tb - Tt, 'down'),
 ('gap ternary vs JQ', r'$3.35\times10^{-4}$ below JoshuaQFEX', '3.35e-4', mpf('0.487676') - Tt, 'down'),
 ('ternary a', r'$a = 0.0035141538$, $c = 0.0035141537$', '0.0035141538', mpf(ct['a']), 'eq'),
 ('ternary c', r'$a = 0.0035141538$, $c = 0.0035141537$', '0.0035141537', mpf(ct['c']), 'eq'),
 ('eps0 lower bound', r'$\eps_0 \ge 1.3156\times10^{-6}$', '1.3156e-6', min(v for k, v in m.items() if k.split()[0] in ('C1','C2','C3','C4','C5','C6','C7','C8')), 'down'),
 ('C4 margin', r'C4 ($1.3156\times10^{-6}$)', '1.3156e-6', m['C4 pairs'], 'down'),
 ('M1 margin', r'$M_1$ ($1.315\times10^{-6}$)', '1.315e-6', m['M1 = rho0 integral < 2^rho_c'], 'down'),
 ('M2 margin', r'$M_2$ ($1.494\times10^{-6}$)', '1.494e-6', m['M2 = rho1..rho9 integrals < 2^rho_c'], 'down'),
 ('B3 margin', r'B3 ($8.1\times10^{-7}$)', '8.1e-7', m['B3: eta - rho_f > (18 + 6 max(p,q)) eps'], 'down'),
 ('S3 left side (must be small)', r"S3's left side $0.12946$", '0.12946', h(2*mpf(cb['a']))/2 + h(mpf(cb['a'])), 'up'),
 ('delta at our point (must be large)', r'$\delta\approx0.0698$', '0.0698', (mpf(cb['eta']) - mpf(cb['mu'])/2*log(3, 2))/2, 'down'),
 ('floor at our Delta', r"$(1-\Delta)/2=0.48565153115$", '0.48565153115', (1 - Db)/2, 'down'),
 ('distance floor to T (rev8e)', r"This leaves $1.92\times10^{-3}$ between that floor", '1.92e-3', Tb - (1 - Db)/2, 'down'),
 ('floor, abstract', r'about 0.4856 at the capacity of our point', '0.4856', (1 - Db)/2, 'down'),
 ('our Delta', r'$\Delta=0.0286969377$', '0.0286969377', Db, 'eq~'),
 ('Psi(1) threshold', r'1 + 2\log_2(2\sqrt2/\pi) \approx 0.697', '0.697', 1 + 2*log(2*mp.sqrt(2)/mp.pi, 2), 'eq~'),
 ('pair-bound coefficient', r'2.6494(1/2 - \tau)', '2.6494', 1/(2*(1 - h(mpf(1)/4))), 'eq~'),
 ('C1 slack times mu', r'about $6.3\times10^{-7}$ at our point', '6.3e-7', mpf(cb['mu'])*(h(2*mpf(cb['a']))/2 - mpf(cb['gamma'])), 'about'),
]
tex = open(H + '/SubsetSum/preprint/paper.tex', encoding='utf-8').read()
bad = 0
for name, snip, printed, true, d in rows:
    present = snip in tex
    p = mpf(printed); ok = {'eq': p == true, 'up': p >= true, 'down': p <= true, 'eq~': abs(p - true) <= abs(true) * mpf('0.002'), 'about': abs(p - true) <= abs(true) * mpf('0.01')}[d]
    flag = 'OK ' if (present and ok) else 'BAD'
    bad += flag == 'BAD'
    print('%s %-34s printed %-13s true %-22s need %-4s %s' % (flag, name, printed, mp.nstr(true, 12), d, '' if present else '(SNIPPET NOT FOUND)'))
print('\n%d rows, %d problems' % (len(rows), bad))
