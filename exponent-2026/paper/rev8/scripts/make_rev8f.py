"""rev8f = rev8e + Li-Ye v2 citation (arXiv 2610.10446v2, 2 Nov 2026; author order Baitian Li, Lixi Ye) (Claude, 5 Nov)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
R = [
 ("(partial match and integer circuits, building on~\\cite{rw})", "(partial match and depth-2 linear circuits, building on~\\cite{rw})"),
 ("& partial match, integer circuits &", "& partial match, depth-2 linear circuits &"),
 ("which hashes representations modulo a random prime but has no alias-enumeration phase and no Fourier checksum",
  "which hashes representations but sifts pseudosolutions by partial-match compatibility tests instead of enumerating aliases (their Section~1.4 compares the two approaches), and has no Fourier checksum"),
 ("from an integer-circuit improvement on a fixed partial-match matrix", "from a depth-2 linear-circuit improvement on a fixed partial-match matrix"),
 ("L.~Ye and B.~Li. Subset Sum via Partial Match. \\href{https://arxiv.org/abs/2610.10446v1}{arXiv:2610.10446v1} [cs.DS], 7 Oct 2026.",
  "B.~Li and L.~Ye. Subset Sum via Partial Match. \\href{https://arxiv.org/abs/2610.10446v2}{arXiv:2610.10446v2} [cs.DS], 7 Oct 2026, revised 2 Nov 2026."),
]
for a, b in R:
    assert t.count(a) == 1, (t.count(a), a[:70]); t = t.replace(a, b)
for a, b in [("Ye and Li", "Li and Ye"), ("Ye--Li", "Li--Ye")]:
    print(a, '->', b, t.count(a)); t = t.replace(a, b)
assert 'Ye and Li' not in t and 'Ye--Li' not in t and 'integer circuit' not in t and '10446v1' not in t
open(dst, 'w', encoding='utf-8').write(t); print('ok')

# ---- figures (appended): run as a second pass: python3 make_rev8f.py --figs in out
