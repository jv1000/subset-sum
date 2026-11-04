"""Interval (arb) evaluation of every scalar inequality the proof needs,
derived independently from setup/aliases/checksum/filtering/implementation.tex,
at the candidate's exact decimal values.  Each check prints the margin as an
arb ball and PASS only if the ball is strictly on the correct side of 0."""
import json
from flint import arb, ctx
ctx.prec = 200

C = json.load(open('/home/claude/c3/candidate_K16.json'))
A = lambda s: arb(s)          # decimal string -> tight ball containing the exact rational
K = arb(C['K']); mu = A(C['mu']); eta = A(C['eta']); tau = A(C['tau'])
gam = A(C['gamma']); eps = A(C['epsilon']); g = A(C['guard'])
c0 = A(C['minimum_useful_probability']); kap = A(C['kappa'])
p = A(C['p']); q = A(C['q_m'])
d = arb('0.5') - gam - arb('1e-8')
d0 = (1 - c0) * K * d * mu * (1 - arb('1e-7'))
d1 = d0 - arb('1e-9')
cap = tau + 20 * eps
rho_f = eta - 48 * eps - arb('5e-7')
rho_c = rho_f - arb('1e-6')
Delta = eta - tau; Gam = 2 * tau - eta; a = Delta / Gam
log2 = lambda x: x.log() / arb(2).log()
h = lambda x: -x * log2(x) - (1 - x) * log2(1 - x)
h14 = h(arb(1) / 4)
T = tau + 20 * eps

rows = []
def chk(name, tex, margin):
    ok = margin > 0           # arb comparison: True only if whole ball > 0
    rows.append((name, ok))
    print('%-34s %-5s margin=%s   [%s]' % (name, 'PASS' if ok else 'FAIL', margin.str(6, radius=True), tex))

print('derived: d=%s d0=%s d1=%s cap=%s' % (d.str(12), d0.str(12), d1.str(12), cap.str(12)))
print('Delta=%s Gamma=%s a=%s rho_f=%s rho_c=%s T=%s\n' % (Delta.str(12), Gam.str(12), a.str(12),
      rho_f.str(12), rho_c.str(12), T.str(12)))

# --- aliases.tex
chk('blocks: 1 - K mu > 0', 'aliases.tex:79 (17m/2<=floor(n/2))', 1 - K * mu)
listexp = arb('0.5') + (h14 - arb('0.5') - gam) * mu
chk('list: tau - list exponent', 'aliases.tex:201-211', tau - listexp)
pairexp = 1 + (2 * h14 - 1 - gam) * mu - eta + g
chk('pairs: tau - pair exponent', 'aliases.tex:244-253 (+guard)', tau - pairexp)
chk('sparse: eta-h(mu)-mu-g', 'aliases.tex:296-309', eta - h(mu) - mu - g)
chk('sparse: mu <= 2/3 (binom sum dom.)', 'aliases.tex:299-301', arb(2) / 3 - mu)
chk('setup: T - (mu+1/4)', 'aliases.tex:163-169', T - (mu + arb('0.25')))
chk('useful blk: (1-c0)K d mu - d0', 'aliases.tex:341-351 Markov', (1 - c0) * K * d * mu - d0)
chk('useful blk limit - c0', 'aliases.tex:349-352', (1 - d0 / (K * d * mu)) - c0)
chk('c0 > 0', 'aliases.tex:424', c0)
chk('B>=2^{gam m}: 1/2-d-gam', 'aliases.tex:354-399', arb('0.5') - d - gam)
chk('d > 0', 'aliases.tex:348', d)
# --- setup.tex
chk('prelim Chebyshev gap d0-d1', 'setup.tex:192-198', d0 - d1)
chk('prelim cap: cap-(1/2-d1)', 'setup.tex:200-206', cap - (arb('0.5') - d1))
# --- checksum.tex
chk('Delta > 0', 'checksum.tex:109,195', Delta)
chk('Gamma > 0', 'checksum.tex:180-189', Gam)
chk('p >= 1', 'checksum.tex:448-449', p - 1)
chk('30 - 3p >= 0', 'checksum.tex:448-449 (3eps pattern err)', 30 - 3 * p)
chk('q_m >= 1 (alpha<=1<=q)', 'checksum.tex:451', q - 1)
chk('30 - q(4a+3) >= 0', 'checksum.tex:458', 30 - q * (4 * a + 3))
chk('err exp: eta-48eps-rho_f', 'checksum.tex:487-495', eta - 48 * eps - rho_f)
# --- filtering.tex
chk('finite slack rho_f-rho_c', 'filtering.tex:116-123,152-155', rho_f - rho_c)
chk('kappa > 0', 'filtering.tex:26', kap)
# --- implementation.tex
chk('trial division: T - eta/2', 'implementation.tex:283-285', T - eta / 2)
chk('cap <= T', 'implementation.tex:273-286', T - cap + arb('1e-30'))
chk('guard g > 0', 'aliases.tex:22-24', g)
print('\nlist exponent  =', listexp.str(15))
print('pair exponent  =', pairexp.str(15))
print('prelim (1/2-d1)=', (arb('0.5') - d1).str(15))
print('T = tau+20eps  =', T.str(15))
print('h(1/4)=', h14.str(15), ' h(mu)+mu=', (h(mu) + mu).str(10))
print('ALL PASS' if all(ok for _, ok in rows) else 'SOME FAIL')
