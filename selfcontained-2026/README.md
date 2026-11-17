# A self-contained proof of the exponent threshold 0.4875754036 for worst-case Subset Sum

Supplement to the manuscript of Jennifer Voitle, November 2026.

The manuscript proves that Subset Sum on `n` integers of polynomial bit length is decided by a randomized
word-RAM algorithm in time `O(2^(T'n))` for every fixed `T' > T = 0.4875754036`. The same threshold was reported
earlier, conditionally on lemmas of two other preprints, in *A certified exponent of 0.48758 for worst-case
Subset Sum, and limits of the alias–checksum analysis* (hexagon:2611.00178), whose supplement is the folder
`exponent-2026` of this repository. This manuscript proves those lemmas in its own text.

**Status.** The manuscript has been reviewed and audited by a second AI system with the sources open. It has not
been refereed by a human. Section 13 of the manuscript gives the verification status of every statement.

## What is here

| Path | Contents |
|---|---|
| `Voitle_SubsetSum_selfcontained_2026-11.pdf`, `.tex` | The manuscript |
| `certificates/candidate_base.json` | The parameter point and the 64 filter coefficients (also printed in Appendix A) |
| `certificates/certify_selfcontained.py` | The certificate; its margins carry the premise labels of the manuscript |
| `certificates/certify_c5.py` | The moment computation, imported by the script above; its error bounds are justified by Lemma 11.1 |
| `certificates/cert_selfcontained_512.json` | Stored output of the certificate |
| `requirements.txt` | The one Python dependency |
| `LICENSE` | MIT License, for the certificate files |

The files under `certificates/` are part of the proof: they verify the numerical premises listed in Section 1.4
of the manuscript.

## Licence

The files under `certificates/` and `requirements.txt` are released under the MIT License (see `LICENSE`): anyone
may run, copy, modify and redistribute them. The manuscript (`.pdf` and `.tex`) is not covered by that licence;
its copyright remains with the author.

## Reproducing the certificate

The numerical premises are the inequalities (E0), (C1)–(C8), (N1)–(N14), (M1), (M2). They are verified in ball
arithmetic (Arb, through python-flint) by one script.

Requirements: Python 3.12 and python-flint 0.9.0.

```
pip install -r requirements.txt
cd certificates
python certify_selfcontained.py candidate_base.json 512 32 0.1 0.25 > my_run.json
```

The run takes about ten seconds. It exits with status 0 only if all 39 premise lines, the 8 auxiliary bounds and
the 12 facts of exact decimal arithmetic hold. `my_run.json` should agree with the stored output
`cert_selfcontained_512.json` in every field except the two that record the run itself: the running time
(`params.seconds`) and the Python version (`params.python`).

The arguments are the number of inner quadrature nodes (512), the ratio of outer to inner nodes (32), `beta`
(the outer strip has half-width `2*beta`) and the inner strip half-width `sigma`. The working precision is
200 bits. Section 11 of the manuscript explains the method and matches each line of the output to a premise.

One limit, stated in Section 11.2: every run of this certificate uses the same moment code, `certify_c5.py`.
The independently written implementations of the moments are those reported in the earlier paper.
