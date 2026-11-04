import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/e6b88fde-407f-5350-a0a8-9cc298e460bb/scratchpad/referee")
import numpy as np, mpmath as mp
from core import closed
for b in [0.05,0.1,0.25,1/3,0.5,0.75,0.9,1,1.5,2,3.7]:
    q=mp.quad(lambda t:(1+mp.cos(t))**b,[0,mp.pi])/mp.pi
    print(f"b={b:.4f} quad={float(q):.15f} closed={closed(b):.15f} diff={float(q)-closed(b):.2e}")
