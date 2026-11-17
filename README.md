# subset-sum

Jennifer Voitle's research on worst-case Subset Sum.

## Two papers, one exponent

| Paper | What it establishes | Files |
|---|---|---|
| **A self-contained proof of the exponent threshold 0.4875754036 for worst-case Subset Sum** (preprint, November 2026) | The threshold *T = 0.4875754036* as a theorem with a complete written proof. Every non-numerical lemma is proved in the paper itself, so the result assumes no statement of another preprint. | [`selfcontained-2026/`](selfcontained-2026/) |
| **A certified exponent of 0.48758 for worst-case Subset Sum, and limits of the alias–checksum analysis** (6 November 2026; hexagon:2611.00178) | The same threshold, **conditionally** on the non-numerical lemmas of the OpenAI paper and of A. Kapila's proof. Also: limits of the analysis, and a further conditional exponent. | [`Voitle_SubsetSum_certified-0.48758_2026-11-06_rev8g.pdf`](Voitle_SubsetSum_certified-0.48758_2026-11-06_rev8g.pdf), [`exponent-2026/`](exponent-2026/) |

The self-contained paper is the later one. It does not lower the exponent: it removes the condition under which
the earlier paper stated it. Its numerical premises are certified in ball arithmetic. It has been reviewed and
audited by a second AI system with the sources open; Section 13 of the paper gives the verification status of every
statement. **Neither paper has been refereed.**

## The earlier paper: status (6 November 2026)

**Paper:** [`Voitle_SubsetSum_certified-0.48758_2026-11-06_rev8g.pdf`](Voitle_SubsetSum_certified-0.48758_2026-11-06_rev8g.pdf)
(draft, 6 November 2026; source [`exponent-2026/paper/rev8/paper_2026-11-06_rev8g.tex`](exponent-2026/paper/rev8/paper_2026-11-06_rev8g.tex)).
Companion proof of the ternary alias step: [`SECTION_T_v3.pdf`](SECTION_T_v3.pdf).
Not peer reviewed. This section describes that paper as it stood on 6 November; the lemmas it assumes are proved
in the self-contained paper.

**Main result (Theorem 1).** Assume the non-numerical lemmas of the OpenAI paper and of Base's written proof.
Then there is a uniform randomized algorithm for Subset Sum in the word-RAM model that halts on every execution and
answers correctly with probability at least 2/3, and, for every fixed *c* and every fixed *T′ > T = 0.4875754036*,
uses O(2^{T′n}) word operations on every input of *n* integers whose bit lengths, and that of the target, are at most
*n^c*. In particular it runs in time **O(2^{0.4875755 n})**.
Statement: [lines 77–79 of the paper source](exponent-2026/paper/rev8/paper_2026-11-06_rev8g.tex#L77-L79).

The algorithm is Base's (A. Kapila) with a single asymmetric filter (16 cosine + 16 sine terms per density) in place of
Base's family of 43 cosine-only filters, at new parameters. *T* is 9.689 × 10⁻⁵ below the best bound previously
listed, Y. Bills's conditional 0.4876723 (21 Oct 2026), and 1.005 × 10⁻⁴ below J. Wharton's conditional 0.487676.

| | What | How it was checked |
|---|---|---|
| **Certified** | All 33 numerical conditions of Base's proof at our parameters, including both filtering moments and their quadrature errors. Tightest margins: B3 8.1 × 10⁻⁷, *M*₁ 1.315 × 10⁻⁶, C4 1.3156 × 10⁻⁶, *M*₂ 1.494 × 10⁻⁶. | Ball arithmetic (python-flint arb, 200 bits) with analytic quadrature-error bounds; at least two independent implementations; doubled resolution agrees to 20 digits. |
| **Conditional** | The non-numerical lemmas of the OpenAI paper (isolation, alias lemmas, alias subtraction, finite-circle convergence, word-RAM accounting) and of Base's written proof — the same premises as the 0.487676 and 0.4876723 bounds. | Base's probabilistic core (Lemma A5, Corollary D, the region analysis of its Theorem B) was re-derived independently. Base's preliminary search, alias-step cost accounting and checksum changes, and the OpenAI lemmas, were read but not re-derived. |
| **Not claimed** | An unconditional theorem; Lean verification; peer review. | — |
| **Open (not part of the claim)** | Theorem 3: exponent 0.4873407528 (time O(2^{0.4873408 n})) with ternary masks. Its numerics are certified, but it also needs the open combinatorial statement [S] ("small slices are robust"). | Paper §8, §10 and Appendix A; `SECTION_T_v3.pdf`. |

Also in the paper: a certified point at 0.4894616 inside the original OpenAI construction (16 blocks); a lower bound
on the first filtering moment for every filter, which rules out the original OpenAI proof's sufficient conditions up to
exponent 0.484; the counting floor (1 − Δ)/2 for designs that enumerate every alias class; and an independent
certification of the 430 moment premises of the Base/Wharton bound (also certified independently by Bills).

## Verify the numerical claims yourself

Self-contained paper (about ten seconds; Python 3.12 and python-flint 0.9.0):

```
pip install -r selfcontained-2026/requirements.txt
cd selfcontained-2026/certificates
python certify_selfcontained.py candidate_base.json 512 32 0.1 0.25 > my_run.json
```

The run exits with status 0 only if every premise holds, and `my_run.json` should equal the stored
`cert_selfcontained_512.json` except for the running time and the Python version. Details are in
[`selfcontained-2026/README.md`](selfcontained-2026/README.md).

Earlier paper:

```
pip install python-flint numpy
cd exponent-2026/lab_notebook
python3 -I certify_base.py candidate_base.json      # prints every margin; "all_pass" must be true
```

This takes a few seconds and prints `"T_upper": 0.4875754036`. The independent implementations, referee reports and
pre-registrations are in `exponent-2026/` (start with `exponent-2026/paper/rev8/` and `exponent-2026/lab_notebook/`).

## Priority and integrity

`exponent-2026/` is a frozen research record in five snapshots. Each snapshot's `MANIFEST_k.sha256` lists the SHA-256
of every file, and the fingerprint of each manifest is timestamped with OpenTimestamps (`*.ots`; see
`exponent-2026/TIMESTAMP.md`). Snapshot 1, frozen 4 November 2026 at about 02:20 US Eastern, already contains the
certified parameter point `lab_notebook/candidate_base.json`.

Files are only ever added, never edited, after they are fingerprinted, so every snapshot still verifies
(`cd exponent-2026 && sha256sum -c MANIFEST_5.sha256`). For that reason `exponent-2026/README.md` still describes the
state of 4 November; this page is the current summary. The folder `selfcontained-2026/` was added on 17 November
2026 and is not part of those snapshots.

## Folders

| Folder | What |
|---|---|
| `selfcontained-2026/` | The self-contained paper (PDF and LaTeX source) and its certificate: the parameter point, two scripts and their stored output. |
| `exponent-2026/` | The research record: lab notebooks, pre-registrations, independent referee reports and their scripts, certificates, and every revision of the paper (`paper/rev8/` holds the current one). |
| `references/` | Links to, and SHA-256 fingerprints of, the papers this work builds on. They are not redistributed. |

## Credits and AI collaboration

The construction builds on OpenAI, *Subset Sum in time O(2^{0.49n})* (4 Oct 2026), and on A. Kapila's modification
("Base", [a-kapila/maths-proofs](https://github.com/a-kapila/maths-proofs), commit 44c34961). Related refinements:
J. Wharton ([JoshuaQFEX/subset-sum-bound](https://github.com/JoshuaQFEX/subset-sum-bound)) and Y. Bills
([yannouli/subset-sum-conditional-refinement](https://github.com/yannouli/subset-sum-conditional-refinement)).
An independent route below 1/2: B. Li and L. Ye, *Subset Sum via Partial Match*, arXiv:2610.10446.

The research was carried out by Jennifer Voitle with AI systems: Claude (Anthropic), including Claude Fable 5.1 as an
independent reviewer, and Astra (an OpenAI-based assistant). Their contributions are described in Section 11 of the
earlier paper. For the self-contained paper the systems were Claude Fable 5.2 (Anthropic) and GPT-6 Astra (OpenAI);
Sections 1.2 and 13 of that paper say what each did. They are credited in the text, not as authors. The author takes full responsibility for the content.

Questions and corrections are welcome as GitHub issues on this repository.
