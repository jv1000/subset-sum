# Snapshot fingerprint

Snapshot: 2026-11-04 (frozen ~02:20 US Eastern).
Fingerprint = SHA-256 of `MANIFEST.sha256`:

    27b60d586aa3f8187e337d5fc2d87ca4a55c6caeaa6495248915da3656ed7023

To verify: `sha256sum -c MANIFEST.sha256` (every line OK), then `sha256sum MANIFEST.sha256` must print the
fingerprint above.

Public timestamp record: MANIFEST.sha256.ots

---

# Snapshot 2 fingerprint

Snapshot 2: 2026-11-04 (frozen ~07:50 US Eastern). Adds the conditional ternary result (Fable round 2: Section T,
candidate_ternary.json and its certificate, the exact-monotonicity counterexample), Claude's review of Section T, and
the paper at revision 73. No snapshot-1 file was changed, so snapshot 1 still verifies.
Fingerprint = SHA-256 of `MANIFEST_2.sha256`:

    8928009bf61a82752d0b2538d2b2231029fd2fe14310a6b1ceda9e247e1c2956

To verify: `sha256sum -c MANIFEST_2.sha256`, then `sha256sum MANIFEST_2.sha256`.

Public timestamp record: MANIFEST_2.sha256.ots

---

# Snapshot 3 fingerprint

Snapshot 3: 2026-11-04 (frozen ~22:40 US Eastern). Adds Fable rounds 3–6 (Conjecture Q, P2, YP-Hall evidence, k = 1
families, Section T v2, independent re-derivation of Base's core) with scripts; Claude's reviews (round 3, round 6),
the rebuilt k = 1 family check, the blind re-derivation of Corollary D and the check of Astra's t = 2 theorem; Astra
round 6 (fresh referee of Section T v2 and the ternary point, Base-core re-derivation, YP-Hall at k = 1, t = 2); and
the LaTeX preprint (paper.tex and PDF of 2026-11-04). No snapshot-1 or snapshot-2 file was changed, so both still verify.
Fingerprint = SHA-256 of `MANIFEST_3.sha256`:

    2c00b258515a5fa1c214430ffa65e23de5ab87a228ed764b9106e560d46a27d4

To verify: `sha256sum -c MANIFEST_3.sha256`, then `sha256sum MANIFEST_3.sha256`.

Public timestamp record: MANIFEST_3.sha256.ots

---

# Snapshot 4 fingerprint

Snapshot 4: 2026-11-05 (frozen ~07:10 US Eastern). Adds Section T v3 (fresh referee's repairs applied; no number
changed) with its changelog and round-7 re-check scripts; Claude's check of the v2 → v3 diff; and the revised preprint
of 2026-11-05 (paper_2026-11-05.tex and PDF: computational scope stated, Section 10 restructured around [S],
verification ledger, structural results first, conservative gaps) with its number audit and edit script. Files only
added; no file of snapshots 1–3 was changed, so all three still verify.
Fingerprint = SHA-256 of `MANIFEST_4.sha256`:

    d156aa10cb74074ab209668ddff005097cf3e7bdd49f109b100d1de41bf3e198

To verify: `sha256sum -c MANIFEST_4.sha256`, then `sha256sum MANIFEST_4.sha256`.

Public timestamp record: MANIFEST_4.sha256.ots
