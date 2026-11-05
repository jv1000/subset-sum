# Jennifer, Nov 5 ~10:30: restore "more than fifty years" and give Ye-Li's exponent as a decimal. Claude.
import sys
P = sys.argv[1]; s = open(P, encoding='utf-8').read()
E = [
 (r"Worst-case Subset Sum fell below the meet-in-the-middle exponent $1/2$ in October 2026, with OpenAI's $2^{0.49n}$ algorithm and Ye and Li's $2^{(1/2 - 1/450000)n}$. We study the OpenAI approach and its modification by A.~Kapila (``Base''), which reached 0.4877; a retuning of Base by JoshuaQFEX reached 0.487676.",
  r"For more than fifty years, since Horowitz and Sahni's meet-in-the-middle algorithm of 1974, the best exponent for worst-case Subset Sum was $1/2$. In October 2026 that barrier fell twice within a week, with OpenAI's $2^{0.49n}$ algorithm and, independently, Ye and Li's $2^{(1/2 - 1/450000)n} \approx 2^{0.4999978n}$, and improvements have followed quickly since: within three weeks A.~Kapila's modification of the OpenAI approach (``Base'') reached 0.4877, and a retuning of Base by JoshuaQFEX reached 0.487676. We study this line of work."),
 (r"Worst-case Subset Sum fell below the meet-in-the-middle exponent $1/2$ in October 2026. This paper asks how far one of the two new approaches, OpenAI's, can be pushed:",
  r"For more than fifty years, from Horowitz and Sahni's meet-in-the-middle algorithm in 1974 until October 2026, the best exponent for worst-case Subset Sum was $1/2$. Then, within a few weeks, OpenAI and, independently, Ye and Li broke that barrier, and several further improvements appeared; the area is moving quickly. This paper asks how far one of the two new approaches, OpenAI's, can be pushed:"),
 (r"Ye and Li~\cite{yeli}, independently and by a different method (partial match and integer circuits, building on~\cite{rw}), proved $1/2 - 1/450000$.",
  r"Ye and Li~\cite{yeli}, independently and by a different method (partial match and integer circuits, building on~\cite{rw}), proved $1/2 - 1/450000 \approx 0.4999978$."),
]
for a, b in E:
    assert s.count(a) == 1, a[:70]; s = s.replace(a, b)
open(P, 'w', encoding='utf-8').write(s); print('ok')

# Nov 5 ~10:50: "why care" sentence in The problem in brief replaced (Jennifer approved). Pre-edit copy drafts/paper_before_why_care_2026-11-05.tex
