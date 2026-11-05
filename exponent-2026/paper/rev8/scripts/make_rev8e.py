"""rev8e = Astra's rev8d + Jennifer's 5 Nov 15:17 decisions (Claude). Exact replacements, each must match once."""
import os, sys
H = os.path.expanduser('~')
src = sys.argv[1]; dst = sys.argv[2]
t = open(src, encoding='utf-8').read()
R = [
 # date line
 (r"\date{5 November 2026\\Revision 8d}", r"\date{Draft, 5 November 2026}"),
 # abstract opening + Jennifer's bridge
 (r"We study the alias--checksum approach to worst-case Subset Sum introduced by OpenAI and modified by Kapila (``Base''). Here we improve this approach and examine the limits of its current analysis. Conditional",
  r"For more than fifty years, since Horowitz and Sahni's meet-in-the-middle algorithm of 1974, the best exponent for worst-case Subset Sum was $1/2$. In October 2026 that barrier fell twice within a week, with OpenAI's $2^{0.49n}$ algorithm and, independently, Ye and Li's $2^{(1/2 - 1/450000)n} \approx 2^{0.4999978n}$, and improvements have followed quickly since: within three weeks A.~Kapila's modification of the OpenAI approach (``Base'') reached 0.4877, and a retuning of Base by JoshuaQFEX reached 0.487676. Here we push this line of work further and examine what limits it. Conditional"),
 # Section 9 title restored
 (r"\section{Costs and limitations near the certified point}", r"\section{Why the exponents stall near 0.4876}"),
 (r"Section~9 (costs and limitations)", r"Section~9 (why the exponents stall)"),
 # Astra's error: distance floor -> threshold is 1.92e-3, not < 1.77e-3
 (r"This leaves less than $1.77\times10^{-3}$ between that floor and the certified threshold.",
  r"This leaves $1.92\times10^{-3}$ between that floor and the certified threshold; removing all of the C4 overhead in the model of the table above recovers about $1.77\times10^{-3}$ of it."),
 # Section T pointer -> companion PDF / arXiv ancillary file
 (r"are in the ancillary file \path{SECTION_T_v3_rev8d.md} in the accompanying verification snapshot;",
  r"are in the companion file \path{SECTION_T_v3.pdf}, distributed with this paper (on arXiv as an ancillary file);"),
 (r"The accompanying revision-8d verification snapshot contains", r"The accompanying verification snapshot contains"),
 (r"and \path{SECTION_T_v3_rev8d.md}, the complete ternary proof", r"and the companion file \path{SECTION_T_v3.pdf}, the complete ternary proof"),
]
for a, b in R:
    n = t.count(a)
    assert n == 1, (n, a[:80])
    t = t.replace(a, b)
assert 'rev8d' not in t.replace('rev8d.pdf',''), [l for l in t.splitlines() if 'rev8d' in l]
open(dst, 'w', encoding='utf-8').write(t)
print('ok', len(R), 'edits')
