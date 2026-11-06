"""Figures for the preprint (Claude, 5 Nov 2026). Our values are computed from the frozen candidate files;
other values are the published/printed ones cited in the paper. Labels print exact decimals as in the paper."""
import json, os
from fractions import Fraction as F
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'serif', 'mathtext.fontset': 'cm', 'font.size': 8.5, 'axes.linewidth': 0.6,
                     'pdf.fonttype': 42})
H = os.path.expanduser('~/mnt'); L = H + '/SubsetSum/C3_target_048_Claude'
cb = json.load(open(L + '/candidate_base.json')); ck = json.load(open(L + '/candidate_K16.json'))
ct = json.load(open(H + '/Fable_review/Fable_round2/candidate_ternary.json'))
eps = F(1, 10**8)
Tb = F(str(cb['tau0'])) + 20*eps; Tt = F(str(ct['tau0'])) + 20*eps; Tk = F(str(ck['tau'])) + 20*eps
D = F(str(cb['eta'])) - F(str(cb['tau0'])); floor = (1 - D)/2
assert str(float(Tb))[:12] == '0.4875754036' and float(Tt) == 0.4873407528 and abs(float(Tk) - 0.4894615727) < 1e-12
OUT = os.path.dirname(os.path.abspath(__file__))
C_OUR, C_COND, C_OTH, C_BND = '#1f5fa8', '#7b3fa0', '#555555', '#b03a2e'

# ---------- Figure 1: exponents, one row each ----------
rows = [  # (value, row label, value label, colour)
 (0.489995, 'OpenAI (stated 0.49)', '0.489995', C_OTH),
 (0.4897736, "OpenAI, Astra's tuning", '0.4897736', C_OTH),
 (float(Tk), 'OpenAI, 16 blocks (Theorem 2)', '0.4894616', C_OUR),
 (0.4877, 'Base (claimed)', '0.4877', C_OTH),
 (0.487676, 'JoshuaQFEX', '0.487676', C_OTH),
 (0.4876723, 'Bills', '0.4876723', C_OTH),
 (float(Tb), 'Base + one filter (Theorem 1)', '0.4875754036', C_OUR),
 (float(Tt), 'ternary masks, if [S] (Theorem 3)', '0.4873407528', C_COND),
]
fig, ax = plt.subplots(figsize=(6.3, 2.7))
x0, x1 = 0.4835, 0.4906; n = len(rows)
ax.set_xlim(x0, x1); ax.set_ylim(-0.6, n + 0.75)
ax.axvspan(x0, 0.484, color=C_BND, alpha=0.12, lw=0)
ax.text(0.48412, n + 0.45, 'Lemma 1:\n$\\tau\\leq0.484$ excluded\n(OpenAI budget)', fontsize=6.3, color=C_BND, ha='left', va='top')
ax.axvline(float(floor), color=C_BND, lw=0.9, ls='--')
ax.text(float(floor) + 0.00006, n + 0.45, 'counting floor at our $\\Delta$\n0.48565153\n(Prop. 1, conditional)', fontsize=6.5, color=C_BND, ha='left', va='top')
ax.axvline(0.4895156, color=C_OTH, lw=0.7, ls=':')
ax.text(0.4895156 - 0.00006, n + 0.45, 'floor of the 17-block\nOpenAI budget 0.4895156', fontsize=6.3, color=C_OTH, ha='right', va='top')
for k, (v, lab, vl, c) in enumerate(rows):
    y = n - 1 - k
    ax.plot([x0, v], [y, y], color='#dddddd', lw=0.5, zorder=1)
    ax.plot(v, y, 'o', ms=4, color=c, zorder=3)
    ax.text(v + 0.00007, y, vl, fontsize=6.8, color=c, va='center', ha='left')
ax.set_yticks([n - 1 - k for k in range(n)]); ax.set_yticklabels([r[1] for r in rows], fontsize=7)
for tl, r in zip(ax.get_yticklabels(), rows): tl.set_color(r[3])
ax.tick_params(axis='y', length=0)
[ax.spines[k].set_visible(False) for k in ('left', 'right', 'top')]
ax.set_xticks([0.484, 0.485, 0.486, 0.487, 0.488, 0.489, 0.490])
ax.tick_params(axis='x', labelsize=7.5, length=3, width=0.6)
ax.set_xlabel('running-time exponent (lower is faster)', fontsize=8)
fig.tight_layout(pad=0.3); fig.savefig(OUT + '/fig_exponents.pdf'); fig.savefig(OUT + '/fig_exponents.png', dpi=200)

# ---------- Figure 2: the counting floor against the checksum gap ----------
fig, ax = plt.subplots(figsize=(5.2, 2.6))
xs = [0.025 + i*0.00002 for i in range(1001)]
ax.plot(xs, [(1 - x)/2 for x in xs], color=C_BND, lw=1.1, label='$(1-\\Delta)/2$')
ax.fill_between(xs, [(1 - x)/2 for x in xs], 0.472, color=C_BND, alpha=0.07, lw=0)
ax.text(0.0335, 0.4738, 'not reachable with full alias-class\nenumeration (Proposition 1)', fontsize=7, color=C_BND)
ax.plot(float(D), float(Tb), 'o', color=C_OUR, ms=4.5, zorder=3)
ax.annotate('Theorem 1: $\\Delta = 0.0286969377$,\n$T = 0.4875754036$', (float(D), float(Tb)), xytext=(0.0305, 0.4884),
            fontsize=7, color=C_OUR, arrowprops=dict(arrowstyle='-', lw=0.5, color=C_OUR))
ax.plot([float(D), float(D)], [float(floor), float(Tb)], color=C_OUR, lw=0.8)
ax.text(float(D) + 0.0006, (float(floor) + float(Tb))/2 - 0.0004, '$1.92\\times10^{-3}$', fontsize=7, color=C_OUR)
for d, lab in [(0.030, '0.485 needs $\\Delta\\geq0.030$'), (0.040, '0.48 needs $\\Delta\\geq0.040$')]:
    ax.plot(d, (1 - d)/2, 's', color='k', ms=3)
    ax.text(d + 0.0004, (1 - d)/2 + 0.0003, lab, fontsize=7)
ax.axvline(0.029, color=C_OTH, lw=0.7, ls=':')
ax.text(0.0287, 0.4745, 'best capacity found $\\approx 0.029$', fontsize=6.3, color=C_OTH, rotation=90, ha='right', va='bottom')
ax.axvline(0.0427, color=C_OTH, lw=0.7, ls='--')
ax.text(0.0424, 0.4885, 'Lemma 1:\nfirst-moment\ncapacity $\\leq 0.0427$', fontsize=6.5, color=C_OTH, ha='right', va='top')
ax.set_xlim(0.025, 0.045); ax.set_ylim(0.472, 0.4895)
ax.set_xlabel('checksum gap $\\Delta = \\eta - \\tau_0$', fontsize=8); ax.set_ylabel('exponent', fontsize=8)
ax.tick_params(labelsize=7.5, length=3, width=0.6)
[ax.spines[k].set_visible(False) for k in ('right', 'top')]
fig.tight_layout(pad=0.3); fig.savefig(OUT + '/fig_floor.pdf'); fig.savefig(OUT + '/fig_floor.png', dpi=200)
print('floor', float(floor), 'distance', float(Tb - floor))
