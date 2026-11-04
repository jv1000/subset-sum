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
