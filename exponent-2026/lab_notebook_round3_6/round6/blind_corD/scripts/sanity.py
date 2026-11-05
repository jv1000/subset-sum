import sys, random, itertools
sys.path.insert(0,'.')
from bf import layers, stats
random.seed(1)
for trial in range(300):
    n = random.randint(0,7)
    ws = [random.randint(-5,5) for _ in range(n)]
    L = layers(ws) if n>0 else None
    if n==0: continue
    A,B,per = stats(ws,L)
    for (mask,s,cnts,tot) in per:
        idx=[i for i in range(n) if mask>>i&1]
        lay=[set() for _ in range(s+1)]
        for r in range(s+1):
            for T in itertools.combinations(idx,r):
                lay[r].add(sum(ws[i] for i in T))
        assert [len(x) for x in lay]==cnts, (ws,mask)
        assert len(set().union(*lay))==tot
print("ok")
