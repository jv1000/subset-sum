# C17: colour-coding the left masks (pre-registration + result)
**Written 2026-11-03 ~19:35 ET.** Jennifer: "I would love color coding."

## Idea and algebra (before the run)
- Per trial, draw a random region R ⊂ M with |R| = ρm. Left masks live in R (X ⊂ R, |X| = k), and right masks are
  grouped by (value, Y ∩ R), so overlaps can only occur inside R.
- **But:** S = (I∩M) Δ F is a uniform half of M, so S ∩ R is still a uniform half of R.
  - Representations: binom(ρm/2, k), i.e. (ρ/2) h(2a/ρ) per m.
  - Left masks: ρ h(a/ρ).
  - Overhead (masks − representations) = a + a²/(2ρ ln 2) + O(a³), checked numerically. That is about **1 bit per
    mask element for every ρ**, smallest at ρ = 1 (the whole block).
- The overlap junk is the price of guessing which block elements lie in S. Colouring cannot remove it, because S
  covers half of every region.
- The other colouring (X ⊂ R, Y ⊂ M \ R) forces X = S ∩ R: there is one representation, so γ = 0, and it is worse.
- **Prediction:** NULL; the optimum is ρ = 1 (Base). P(gain > 1e-6) = .03.

## Run: c17.py (the C14 joint model with ρ fixed)
- Constraints: C1 γ < (ρ/2) h(2a/ρ); C2 and C4 with left-mask entropy ρ h(a/ρ); right side unchanged.

## Result (~19:40 ET): NULL, as predicted
| ρ | τ0 | change vs C12 |
|---|---|---|
| 1 (control = Base) | .4875749 | 0 |
| .75 | .4877164 | +1.4e-4 (worse) |
| .5 | .4879723 | +4.0e-4 |
| .25 | .4887278 | +1.2e-3 |
| .1 | .4933881 | +5.8e-3 |

- Monotone: colouring only loses representations.
- **Conclusion:** the C4 junk (1 bit per left-mask element) is intrinsic to representations drawn from a uniform half
  S. Removing it needs partial knowledge of S, or a different source of representations, not a filter on the masks.
  The 1.77e-3 of C16 is therefore not available to filtering tricks of this kind.
