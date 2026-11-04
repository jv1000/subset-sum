import json, numpy as np, jax, jax.numpy as jnp
jax.config.update('jax_enable_x64', True)
src = open('c8.py').read().split('t1 = time.time()')[0]
exec(src)
for it in [1, 2, 3, 10]:
    f2, g2, lm = sor_minmax(fA, gA, pA, qA, DA, iters=it)
    print(it, 'log2M', [float(t) for t in lm], 'f range', float(jnp.min(f2)), float(jnp.max(f2)), 'nan f', bool(jnp.any(jnp.isnan(f2))), 'nan g', bool(jnp.any(jnp.isnan(g2))))
