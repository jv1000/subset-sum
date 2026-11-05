"""Rebuilt independent check of Fable's round-5 k = 1 families (see PREREG_QW_K1_REBUILD.md).
Q_w from the definition (qw.py's Qw), exact fractions."""
import sys, time
from fractions import Fraction as F
sys.path.insert(0, '.')
import importlib.util
spec = importlib.util.spec_from_file_location('qwmod', 'qw.py')
src = open('qw.py').read().split('\nfor w,k,t in')[0]   # take only the Qw definition, not qw.py's demo loop
ns = {}; exec(src, ns); Qw = ns['Qw']
t0 = time.time()
def gen(G): return tuple(2**i for i in range(G))
print('CONTROL 0')
q, _ = Qw((-3,-3,-2,-2,0,0), 2, 3); print('  (-3,-3,-2,-2,0,0) (2,3): Q_w =', q, '=', float(q))
ok0 = q > 1 and abs(float(q) - 1.0357) < 5e-4
gm = [Qw(gen(m), 1, t)[0] for m in range(4, 13) for t in range(2, m//2 + 1)]
ok0 = ok0 and all(x == 1 for x in gm); print('  generic, k=1: all exactly 1?', all(x == 1 for x in gm)); print('  CONTROL 0', 'PASS' if ok0 else 'FAIL')
if not ok0: sys.exit(1)
print('A  two-valued 0^a 1^b')
mx = F(0); eq = []; n = 0
for m in range(4, 17):
    for a in range(1, m//2 + 1):
        w = (0,)*a + (1,)*(m - a)
        for t in range(2, m//2 + 1):
            q, _ = Qw(w, 1, t); n += 1
            if q > mx: mx = q
            if q >= 1: eq.append((a, m - a, t, q))
print('  cases', n, 'max', mx, 'cases with Q_w >= 1:', eq)
okA = mx == 1 and eq == [(2, 2, 2, F(1))]; print('  A', 'PASS' if okA else 'FAIL')
print('B/C  0^2 + G generic')
okB = True; okC = True; eqB = []; mxB = F(0)
for G in range(2, 13):
    w = (0, 0) + tuple(2**i for i in range(G)); m = G + 2
    for t in range(2, m//2 + 1):
        q, _ = Qw(w, 1, t); mxB = max(mxB, q)
        if q >= 1: eqB.append((G, t, q))
        if t == 2:
            cf = F(G**3 + G**2 + 4*G + 4, G**3 + 2*G**2 + 3*G + 2)
            if q != cf: okC = False; print('  C mismatch G=%d: brute %s closed %s' % (G, q, cf))
okB = mxB == 1 and eqB == [(2, 2, F(1))]
print('  max', mxB, 'cases with Q_w >= 1:', eqB); print('  B', 'PASS' if okB else 'FAIL'); print('  C', 'PASS' if okC else 'FAIL')
print('D  0^n + G generic, n = 3, 4 (evidence)')
mxD = F(0); hit = []
for nz in (3, 4):
    for G in range(1, 15 - nz):
        w = (0,)*nz + tuple(2**i for i in range(G)); m = nz + G
        for t in range(2, m//2 + 1):
            q, _ = Qw(w, 1, t); mxD = max(mxD, q)
            if q >= 1: hit.append((nz, G, t, q))
print('  max', mxD, float(mxD), 'cases with Q_w >= 1:', hit); print('  D', 'PASS' if not hit else 'FAIL (prediction)')
print('elapsed %.1f s' % (time.time() - t0))
