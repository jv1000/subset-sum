import json, numpy as np, jax, jax.numpy as jnp
jax.config.update('jax_enable_x64', True)
src = open('s12.py').read().split("cand = json.load")[0]
best = json.load(open('s12_N512.json'))['best']; z = jnp.array(best['z'])
for NN in (512, 1024, 2048):
    g = {}; exec(src.replace("N = int(sys.argv[1]) if len(sys.argv) > 1 else 512", f"N = {NN}"), g)
    c = np.asarray(g['cons'](z)); print(NN, 'min constraint', c.min(), ' M1 margin', c[10], ' M2 margin', c[11], ' C4 slack', c[3])
