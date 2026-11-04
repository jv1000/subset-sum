# C4 result: where the next improvement has to come from (2026-11-03, Claude; all FLOATING unless noted)

**Question (Jennifer):** a block-count change suggested ~.4852 might be reachable; can we get a real point there?
**Answer:** not by changing K alone. With real filter densities, every K in 9–13 is worse than 17 (best .48978 at
K = 13 vs .4897734 at K = 17); a mu-continuation at K = 11, 12 rises monotonically. The bottleneck is the **second
moment M2**, which caps Delta = eta - tau at ~.028; the K-change pays off only after that cap moves.

| Diagnostic | Result |
|---|---|
| Control: K = 17 from Astra's point | T = .48977344 (Astra certified .4897736) |
| K = 9..13, 7 starts each | .490067 / .489911 / .489860 / .489817 / .489781 (all in the old mu ~ .058 basin) |
| mu-continuation, K = 11, 12 | T increases with mu; Delta pinned at .0284–.0287; infeasible past mu ~ .089 |
| Delta capacity, M1 only (6 terms) | .0396 (Holder ceiling .0427, proved for M1) |
| Delta capacity, M1 + M2 (6 / 12 terms) | .0281 / .0288 (12 terms and a wider box add only .0007) |

**Price list (floor of the audited budget vs M2 capacity, any K):** .0281 -> .48977 (K 17); .032 -> .48840 (K 15);
.036 -> .48703 (K 13); .0396 -> .48579 (K 12). About -0.35 in the exponent per unit of capacity.

**The narrow objective for the discovery loop:** find densities (or a proof variant of the domination step for
W > Gamma) that raise the joint M1+M2 Delta-capacity from .028 toward M1's own .040. Reaching .036 would mean
T ~ .4870; reaching .040, T ~ .4858. A first mathematical sub-question: is there an M2 analogue of the Holder bound
(it would tell us whether .028 is already near the true M2 limit, as the 12-term result hints)?

Caveats: floors are grid-based closures (optimistic: coverage -> 1, eps = 0); the capacity numbers are local
searches; nothing here is certified. The M1 Holder bound (C3) is the only proved ingredient.
