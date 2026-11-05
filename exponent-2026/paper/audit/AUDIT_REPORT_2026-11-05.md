# Preprint revision and number audit — 2026-11-05 (Claude)
Master: preprint/paper.tex (backup of the Nov 4 20:49 version: paper_2026-11-04_2049_backup.tex, and its PDF).
New PDF: Voitle_SubsetSum_certified-0.48758_2026-11-05.pdf, 22 pages (was 19), pdflatex x3, 0 errors, no undefined
references; one pre-existing 1pt overfull box in the Introduction table (line ~90, invisible).
Edit script (rerunnable, anchor-checked): drafts/apply_edits_2026-11-05.py.

## What changed
1. Edits 1–5 of drafts/SECTION10_UPDATE_DRAFT.md: Section 9 floating number and wording; Section 10 stale text replaced;
   status and Section 8 "referee pending" removed (A1 passed); Base-core sentence in the status; computational setting
   (randomized, success ≥ 2/3, word-RAM, b ≤ n^c) in Section 2, both theorems, Section 8 caveats and abstract;
   fresh-referee sentence in Section 8.
2. Section 10 restructured: new subsection "The small-layer statement [S] behind the conditional exponent" with a
   status table ([S] ⇐ Lemma S ⇐ M′ ⇐ Q ⇐ YP-Hall; exact monotonicity false; case k = 1), Proposition P2,
   Conjecture Q, Conjecture YP-Hall and a Proposition for k = 1 (incl. Astra's t = 2 theorem with a proof sketch);
   remaining material under "The checksum side and other questions".
3. Verification ledger (end of Section 11, longtable): 13 rows, claim/premise → how checked → status; pointer from
   the Introduction. Use of AI tools and Files updated (Fable rounds 3–6, Astra round 6, blind Corollary D).

## Audit (audit/number_audit.py → number_audit_out.txt)
- 48 numbers with ≥ 4 significant digits matched to source files (candidate_base/K16/ternary.json, cert_base_512.json,
  cert_K16_512x32.json, Astra's SCALAR_SLACKS.md and certificates): all agree to their printed precision.
  Every printed exponent T (0.4875754036 / 0.4875755, 0.4894615727 / 0.4894616, 0.4873407528 / 0.4873408) is exact
  or rounded UP.
- 4 automatic "rounded down" flags, all checked by hand and NOT exponent claims: 0.4894 (a constraint "0.4894 > γ"),
  0.48757 (a pre-registered prediction ± 0.0001), τ0 = 0.4875752 (the parameter τ0, truncated, in a comparison),
  "about 0.48946" (a floating floor estimate).
- 67 numbers come from other sources (literature, landscape study, floating tables of Sections 6 and 9); spot-checked:
  16-block log2 M1/M2 = 0.518477576190/0.518477347232 vs cert_K16 ✓; ρ_c = 0.5184784240 ✓; Astra point 0.4897736 ✓;
  JoshuaQFEX point 0.48767595 ✓.
- FIXED (2 errors found):
  a) Section 10 critical-type table was introduced as "At our certified point"; its values (τ = 0.4898, Δ = 0.02906,
     Γ = 0.46074) are from the floating 16-block joint optimization (c7.json k16_joint, c10_prop.json), not from a
     certified point. Now: "At a floating 16-block point of the OpenAI construction with τ = 0.4898 and Δ = 0.02906".
  b) Astra's 17-block floor was printed 0.4895157; the computed value is 0.48951564024772, so the paper rounded a
     LOWER BOUND UP. Now 0.4895156.
- Optional (not changed; Jennifer's call): gaps are rounded to nearest, which slightly overstates two improvements:
  0.4875754036 vs 0.4873407528 is 2.3465e-4 (printed 2.35e-4); vs Base's 0.48769 is 1.146e-4 (printed 1.15e-4).
  Conservative alternatives: 2.34e-4 / 1.14e-4. (1.005e-4 vs JoshuaQFEX is already conservative; true 1.006e-4.)
- Not covered by the script: numbers with < 4 significant digits (e.g. 8.1e-7, 0.0625), and the bibliography.

## Update ~06:55 ET (Jennifer: use conservative values)
Gaps changed to round DOWN: Section 8 "2.35e-4 below the point above" → 2.34e-4 (true 2.3465e-4); "1.15e-4 below Base's
τ0" → 1.14e-4 (true 1.146e-4); Section 10 "worth about 2.35e-4" → 2.34e-4. Unchanged because already conservative:
3.35e-4 (true 3.3525e-4), 1.005e-4 (true 1.006e-4), and Section 9's floating gap 2.35e-4 (true 2.3515e-4).
Recompiled: 22 pages, 0 errors; audit rerun: 48 matched, the same 4 hand-cleared flags.

## Update ~07:05 ET: structural results moved to the front
Abstract: the floor (1 - Delta)/2 and the Lemma 1 block of 0.48 now come right after the background, before the
parameter point; their later repeats in the second paragraph were trimmed. Introduction: the same two facts in the
opening paragraph, with section pointers. Pre-edit copy: drafts/paper_before_structural_lead_2026-11-05.tex.
Recompiled: 22 pages, 0 errors; audit rerun unchanged.
