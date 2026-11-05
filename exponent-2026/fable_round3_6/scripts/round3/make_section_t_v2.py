"""Task 2: SECTION_T_v2.md = Section T aligned with ROUND2_REPORT: [S] with a polynomial constant C_S = C_S(m),
trial count C_S n^8 ceil(2^{d(M)}); the remark 'C_S = 3 if [S] comes from monotonicity' removed (exact monotonicity
is false, ROUND2_REPORT A.3). Every replacement must match exactly once."""
import io
src = io.open('SECTION_T_ternary_alias_step.md', encoding='utf-8').read()
R = [
 ("The result is **conditional on [S]** (Section A of\n`ROUND2_REPORT.md`) **and on Base's written proof**",
  "The result is **conditional on [S]** (Section A of\n`ROUND2_REPORT.md`: a_{k′}(M; w) ≥ 2^{−d(M)}/C_S(m) for every signing w, k′ ≤ 0.11m, with C_S(m) a fixed polynomial;\nunder Conjecture M′ of ROUND2_REPORT A.6, C_S(m) = P(m) + 2 by Lemma S) **and on Base's written proof**"),
 ("| (SR) | a′ ≤ 0.11 | range of [S] as proved from monotonicity (Lemma S) |",
  "| (SR) | a′ ≤ 0.11 | range of [S] as derived from Conjecture M′ (Lemma S, h(a′) ≤ ½) |"),
 ("Put T := n⁸ ⌈2^{d(M)}⌉. (Base's sampled F̂ is not used.)",
  "Put T := C_S(m)·n⁸ ⌈2^{d(M)}⌉, where C_S(m) ≤ n^{c_S} is the polynomial of [S]. (Base's sampled F̂ is not used.)"),
 ("Assume (LD), ℰ₃, the event of Lemma T4, and [S] with\nconstant C_S (a_{k′}(M; w) ≥ 2^{−d(M)}/C_S for every signing w of M, k′ ≤ 0.11m).",
  "Assume (LD), ℰ₃, the event of Lemma T4, and [S] with\npolynomial constant C_S = C_S(m) (a_{k′}(M; w) ≥ 2^{−d(M)}/C_S(m) for every signing w of M, k′ ≤ 0.11m)."),
 ("every alias class of every target is in its dictionary: T = n⁸⌈2^{d(M)}⌉ ≥ n⁸2^{d(M)} trials miss a fixed class with\nprobability ≤ (1 − 2^{−d(M)}/(C_S n^6))^T ≤ e^{−n²/C_S} ≤ e^{−n} for n ≥ C_S, and there are ≤ (nN₀+1)2^n pairs. ∎",
  "every alias class of every target is in its dictionary: T = C_S n⁸⌈2^{d(M)}⌉ ≥ C_S n⁸ 2^{d(M)} trials miss a fixed class with\nprobability ≤ (1 − 2^{−d(M)}/(C_S n^6))^T ≤ e^{−n²} ≤ e^{−n}, and there are ≤ (nN₀+1)2^n pairs. (The constant C_S cancels:\nthe trial count carries it.) ∎"),
 ("*Proof.* T ≤ 2n⁸2^{d(M)}; polynomial factors go into 2^{O(n^{0.6})}.",
  "*Proof.* T ≤ 2C_S(m)n⁸2^{d(M)} ≤ 2n^{8+c_S}2^{d(M)}; polynomial factors (including C_S(m)) go into 2^{O(n^{0.6})}."),
 ("**Theorem A′.** Under [S] with constant C_S, the procedure",
  "**Theorem A′.** Under [S] with polynomial constant C_S(m), the procedure"),
 ("for n of order 10¹⁷; Corollary T6 needs n ≥ C_S (C_S = 3 if [S] comes from monotonicity, Lemma S).",
  "for n of order 10¹⁷; Corollary T6 has no further cutoff (the polynomial C_S(m) is absorbed into the trial count and into\n2^{O(n^{0.6})}). Exact layer-density monotonicity is false (ROUND2_REPORT A.3, m = 8), so [S] is taken from Conjecture M′\n(a_t ≤ P(m)·a_k for t ∈ [k, m−k], k ≤ 0.11m) through Lemma S, which gives C_S(m) = P(m) + 2."),
]
out = src
for a, b in R:
    assert out.count(a) == 1, a[:60]
    out = out.replace(a, b)
out = out.replace("# Section T. Alias phase sums with ternary left masks (Theorem A′)",
                  "# Section T (v2). Alias phase sums with ternary left masks (Theorem A′)\n\nv2 (round 3): [S] carries a polynomial constant C_S(m) (Conjecture M′ + Lemma S); the trial count is C_S(m)·n⁸⌈2^{d(M)}⌉;\nthe remark \"C_S = 3 if [S] comes from monotonicity\" is withdrawn (exact monotonicity is false, ROUND2_REPORT A.3).\nNo numerical condition changes; the certificate `candidate_ternary.json` is unaffected.", 1)
io.open('SECTION_T_v2.md', 'w', encoding='utf-8').write(out)
print("written SECTION_T_v2.md", len(out.splitlines()), "lines")
