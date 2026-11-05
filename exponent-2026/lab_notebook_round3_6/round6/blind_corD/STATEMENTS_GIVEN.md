# Statements given to the blind agent (Base l.223-232, 240-242, 247-249, 254-258; log is base 2)
Let $w$ be integer weights on a finite index set; equal weights are allowed. For a finite index set $V$ and $j \ge 0$,
put
\[\Sigma_j(V) = \{w(T) : T \subseteq V,\ |T| = j\},\qquad a_j(V) = |\Sigma_j(V)|\Big/\binom{|V|}{j},\]
and $\Sigma(V) = \bigcup_j\Sigma_j(V)$, $d(V) = |V| - \log|\Sigma(V)|$.

\textbf{Lemma 3.1 (covering).} Let $0 \le k \le t \le |V|$, and let $W$ be a uniform $(t-k)$-subset of $V$. Then
$a_t(V) \le \mathbb E_W\, a_k(V\setminus W)$.

\textbf{Lemma 3.2 (sampling).} Let $k \le s \le |V|$, and let $S$ be a uniform $s$-subset of $V$. Then
$\mathbb E_S\, a_k(S) \ge a_k(V)$.

\textbf{Lemma 3.3 (a good layer).} Some $t$ with $2t \le |V|$ has $|\Sigma(V)| \le (|V|+1)\,|\Sigma_t(V)|$. In particular
$a_t(V) \ge 2^{-d(V)}/(|V|+1)$.

\textbf{Corollary D (averaged small layer).} Let $M$ be a finite index set with integer weights. Let $k, \sigma, v$ be
integers with $2k \le \sigma$, $2\sigma \le v + 2k$, $v \le |M|$ and $\binom\sigma k\binom vk \le 2^v$. Let $S$ be a
uniform $\sigma$-subset and $V$ a uniform $v$-subset of $M$. Then
\[\mathbb E_S\, a_k(S) \;\ge\; \frac{\mathbb E_V\, 2^{-d(V)}}{v+1}.\]

