# Section T: changes from v2 to v3 (round 7)

Source of the repairs: Astra's fresh referee report `D:\AIProjects\SubsetSum\Astra_round6\out\REFEREE_SECTION_T.md`
(issue register, l.123–139; condition inventory, l.13–47). Line numbers "v2:" refer to `SECTION_T_v2.md`, "v3:" to
`SECTION_T_v3.md`. **No number changes**: `candidate_ternary.json` has sha256
ea2f10e89ea5f0073479e1e41cc5e22ffda31a5655966ee3f458e8cff25c422b (as given), the round-2 certificate re-run is
byte-identical in all 40 condition and moment lines (33 PASS, 0 FAIL), and the nine scalars Astra added lie inside
Astra's 50-digit intervals (`scripts/round7/out/recheck_v3.txt`, pre-registered in `scripts/round7/PREREG_R7.md` with
a failing control). v2 is kept unchanged.

## Astra's issue register → v3

| # | Astra's issue (severity) | v2 | v3 change |
| --- | --- | --- | --- |
| 1 | Statement omits b ≤ n^c and the word-RAM scope (repairable; fatal to an unrestricted reading) | v2:154–155, 179–180 | v3:223–232 new paragraph **Scope**: Base's model (word length (1.1)), halts on every execution, success ≥ 2/3 for n ≥ 2, the intermediate bound 2^{(τ0+20ε)n+2n^{0.7}}poly(n+b+2) on executions passing the guard, and O_{c,T′}(2^{T′n}) only for n ≥ N_c, b ≤ n^c (Base l.58–66, 806–810). v3:260–266 the **Statement** restated with these quantifiers; for b above every fixed polynomial only the poly(n+b+2) bound and the exact fallback are claimed. Header v3:3–10 says so. |
| 2 | Trial count uses a possibly non-integer, unspecified polynomial factor (repairable) | v2:3, 45, 121, 128 | v3:74–83 Step 3: fix once an integer-coefficient polynomial majorant C̄_S ≥ max(1, C_S), and T := ⌈C̄_S(m)·n⁸·⌈2^m/|Σ(M)|⌉⌉ with the inner ceiling of the exact rational 2^m/|Σ(M)| = 2^{d(M)} (d(M) never computed); bounds C̄_S n⁸ 2^{d(M)} ≤ T ≤ 4C̄_S n⁸ 2^{d(M)}. Corollary T6 (v3:174–176) uses T ≥ C̄_S n⁸ 2^{d(M)} ≥ C_S n⁸ 2^{d(M)}; Lemma T7 (v3:184) uses T ≤ 4C̄_S n⁸ 2^{d(M)}. The header's "T = C_S n⁸⌈2^{d(M)}⌉" (v2:3) is gone. |
| 3 | T:134, 141 write T ≤ 2^{d(L)+2n^{0.6}}, dropping C_S n⁸ and the ceiling (repairable) | v2:134, 141 | v3:184 "T ≤ 2^{d(M)+O(log n)}; with T3(i), T ≤ 2^{d(L)+2n^{0.6}+O(log n)}"; v3:194 (item 5) and v3:205 (item 7) use T ≤ 2^{d(L)+2n^{0.6}+O(log n)}. Work exponents unchanged. |
| 4 | Explicit small-prime and right-key-sort checks missing from the table (repairable) | v2:23–38 (table), 132–133 | v3:47–53 new table rows (EM) μ < τ0, (SP) ½ − τ0 + ζ + γμ/2 < τ0 ("small-prime-total"), (SK) r + ½ − τ0 + ζ < τ0 ("right-key-sort-total"), (CAP) 1/guard + ζ < ε0 ("cap-margin"), (A4G) μ(h(2a′)+2a′) + 1/guard < η ("A4R-after-guard"), (PP) τ0 < ½, (PD) η/2 < τ0 + 20ε, with Astra's inequalities and names; v3:55–57 notes that the round-2 script checks (SP), (SK) in the stronger form with ε0 in place of ζ. T7 items 3–4 (v3:190–192) now cite (SP), (SK); T4 (v3:122–124) cites (A4G); Theorem A′ (v3:216) cites (CAP). Slacks listed at v3:253–255. |
| 5 | T5/T6 and Base A5/A6 should refer to the uncapped ideal execution (repairable) | v2:88–91, 120–123 | v3:91–93 Step 6 defines the uncapped ideal execution and says the cap is charged in Theorem A′; Lemma T5 (v3:128), its Step 5 (v3:163–164), Corollary T6 (v3:170–172) and Lemma T7 (v3:180–182) are stated for it; Theorem A′'s proof (v3:214–221) says the real run coincides with it outside the failure events. Base's A5/A6 steps cited there are read the same way (Base's text cannot be edited here). |
| 6 | Base B2 l.702 invokes a_Γ < 1, which does not give 4a_Γ + 3 ≤ 6; use a_Γ ≤ ¾ (repairable) | v2:37 (condition present, no reasoning) | v3:59–65: the row a_Γ w − u has error (4a_Γ + 3)ε by (6.1); the 6εΣz accounting needs a_Γ ≤ ¾; Base's "coefficients ≤ 1 (a_Γ < 1)" alone gives 7ε, the detailed list at l.703 is what the lemma uses; a_Γ = 0.06248, slack 0.6875. |
| 7a | T:25–31 cite "T6 items" for work bounds; those are in T7 (cosmetic) | v2:25–30 | v3:37–44 cite "T7 item k"; v3:33–34 says work bounds are in T7, coverage in T5. |
| 7b | Base line pointers drifted (cosmetic) | v2:8, 15, 27, 30, 42, 57, 60, 70, 77, 93, 108, 120, 125, 148, 154 | Rechecked against `base_PROOF_0.4877.tex` and corrected: §5 l.301–612 (v3:16); parameters l.136–156 and guard l.193–194 (v3:23–24); (C3) l.167, (C6) l.170 (v3:39, 42); procedure l.332–383 (v3:72); Lemma A1 l.398–405 (v3:97); (5.1) l.338 (v3:100); (F3) l.206–209 (v3:110); (F4) l.210–212 (v3:121); (F2) l.204–205 (v3:149); Lemma A4 l.468–476 (v3:117); Steps 1–2 l.492–499 (v3:137); Step 4 l.509–520 (v3:153); K₀ at l.511–512 (v3:133); Corollary A6 l.537–543 (v3:170); Lemma A7 l.547–589 (v3:180); §5.8 l.593–612 (v3:214); precision l.608–612 (v3:220); Theorem 1 l.765–810 and address space l.809–810 (v3:223, 230); Lemma B2 l.696–717, (6.1) l.694, ρ_9's G l.640 (v3:61–66); Step 6 cap l.379–382 (v3:91); Base's F̂ l.349–353 (v3:83); large-prime trial division l.801 (v3:53). |
| 7c | T:21 "all strict" while MU2, SR and domain restrictions are non-strict (cosmetic) | v2:21 | v3:29–33: "<" strict; (MU2), (SR), 2a′ ≤ ½, a_Γ ≤ ¾, p, q ≥ 1 non-strict by nature; all have positive slack at the point. |
| 7d | Last checksum region needs z = (q, 0), not (q, 0, 0) (cosmetic) | v2:37, 174 (implicit) | v3:65–68: ρ_0 has z = (p, 0); ρ_1–ρ_8 have z = (q, 0, 0); ρ_9 has the two-entry z = (q, 0) (its G has one band row, Base l.640); all high regions share the exponent q(a_Γ w − u), so the ten certificates are M1 and M2. |
| 8 | T:183 "no further cutoff" (repairable exposition) | v2:182–185 | v3:268–281 **Cutoffs**: C_S still cancels, but T5's bound needs ⌊γm⌋ ≥ L_* (for (F4)) and 16K₀(m+1) ≤ n⁴ (so 2^{−d(M)}/[16K₀n²(m+1)C_S] ≥ 2^{−d(M)}/(C_S n⁶)), which holds for n³ ≥ 16K₀ since m + 1 ≤ n; T6 needs (nN₀+1)2^n e^{−n²} ≤ 1/n; the cap has its threshold from (CAP) and the O(n^{0.6}) constants; absorption into 2^{(T′−T)n} has its own N_{c,T′}; the preliminary-search thresholds stay. Lemma T5's statement (v3:131–135) carries the explicit form 2^{−d(M)}/(16K₀n²(m+1)C_S) and both thresholds. |
| 9 | NOT CHECKED: [S], OpenAI's full theorem, Base's 430 moments, commit provenance | — | No change: v3 remains conditional on [S] and on Base's written proof (v3:15–19). The commit 44c34961 is still unverifiable here (the folder is not a git repository). |

## Other changes taken from Astra's inventory and lemma paragraphs

| v3 | Change |
| --- | --- |
| v3:41 | (C5R) "both mask lists per trial × trials" (Astra's inventory l.24: both enumerations repeated through all trials); T7 item 2 (v3:188) says "both lists, every trial". |
| v3:37, 155–158 | (C1R) is used as 2^{γm} ≤ C(σ,k1)C(σ,k2) "for large n", with the floors and Stirling factors costing O(log m) (Astra l.20). |
| v3:122–124 | Lemma T4's proof makes the guard step explicit: b + log n ≤ 2^{n/10⁸+2} and (A4G). |
| v3:176–177 | Corollary T6 keeps e^{−n²} (the weakening to e^{−n} at v2:122 is dropped) and notes the unique carry per target/subset pair (Astra l.65). |
| v3:198–206 | T7 item 7 states that every expanded member is counted, including those failing the X⁺ ∩ Y = ∅, X⁻ ⊆ Y test, and that the averaging over P does not condition on T4's event (Astra l.67; Base l.591). |
| v3:193 | T7 item 5 states the 1/P′ ≤ 2^{1−γm} listing probability (Base l.565–566) that v2 used silently. |
| v3:209–212 | Theorem A′ says "for all sufficiently large n" and "P uniform, φ arbitrary", as Base l.319–330. |
| v3:250–258 | T.4 cites Astra's independent certificate (`SCALAR_SLACKS.md`, `A_certificate_4096.json`, own interval FFT) as a second verification of both moments and of all scalars. |

## Points of disagreement or qualification (none changes the repairs)

1. **Severity of issue 1.** Astra calls the missing scope "fatal to an unrestricted reading". The repair is applied in
   full. For the record: v2's Theorem A′ (v2:144–146) and the running-time sentence (v2:154–155) already carried the
   poly(n + b + 2) factor and cited Base's Theorem 1; the unqualified claim was confined to the summary Statement
   (v2:179–180). So the proof was never unrestricted, only its summary.
2. **T5's cutoff.** The round-7 request attributes to Astra the cutoff n² ≥ 128K₀; it is the analogue for Base's own
   Lemma A5 (32K₀n²(m+1)(v+1) ≤ n⁶). It is not T5's and is not used. T5's own cutoff is 16K₀(m+1) ≤ n⁴, i.e.
   n³ ≥ 16K₀ (v3:131–135, 272–276).
3. **(SP), (SK) with ζ or with ε0.** Astra's inventory (l.31–32) states them with ζ subtracted; the round-2 script
   checks the stronger forms with ε0 subtracted (slacks 0.4604, 0.4334 either way). v3 states Astra's form in the
   table and notes the script's form (v3:55–57). No change to the script.
4. **(SR) and h(a′) ≤ ½.** Astra (l.30) says h(a′) ≤ ½ is needed only to derive [S] from Conjecture M′ through
   Lemma S and is not a premise when [S] is assumed directly. Agreed; (SR)'s "Used in" column says so (v3:46).
   (SR) stays in the table because the conditional result is stated through Conjecture M′ at v3:282–283.
5. **Outer ceiling in T.** With an integer-coefficient majorant C̄_S the outer ceiling is redundant; it is kept, as
   requested, so that T is an integer for any majorant (v3:79–81).
6. **e^{−n²} ≤ e^{−n}.** Astra (l.65) notes this weakening wastes slack but is correct. v3 drops it rather than
   keeping it; nothing depends on the choice.
7. **Base's Lemma B2 wording.** The defect at Base l.702 is in Base's text, which is not edited here; v2 already
   imposed a_Γ ≤ ¾ (v2:37). v3 adds the reason (v3:59–65). This matches BASE_CORE_REDERIVATION.md finding 3.1.

## Labels

- PROVED (relative to the cited sources): every change above is a textual repair of a statement, a bound or a
  citation; the proofs of T1–T7 and A′ are otherwise those of v2.
- EVIDENCE: no number moved (`scripts/round7/out/recheck_v3.txt`: sha256 match, 33/33 PASS byte-identical, nine
  extra scalars inside Astra's intervals, control fails as predicted).
- CONJECTURE: [S] (Conjecture M′ through Lemma S) remains the conditional premise; nothing in v3 changes its status.
