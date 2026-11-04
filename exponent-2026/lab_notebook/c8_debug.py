import json, numpy as np, jax, jax.numpy as jnp
jax.config.update('jax_enable_x64', True)
import importlib.util
src = open('c8.py').read().split('# ---------------- C8-D')[0]
src = src.replace("resA = json.load(open('c8_v1_nanbug.json'))['C8A']", "resA = json.load(open('c8_v1_nanbug.json'))['C8A']")
exec(src)
f, g = fA, gA; p, q, Dl = pA, qA, DA
a = Dl/(TAU - Dl); c, s = q*a, q*(1 + a); Q, Phi, D = QPhiD(f, g)
conv = lambda h, k_: jnp.real(jnp.fft.ifft(jnp.fft.fft(h)*jnp.fft.fft(k_)))/N
Mx = M_lin(f, g, p, q, Dl); lam = .385
e = 2*w*jnp.exp(c*D)*Q**(-s-1)
Bc = (1 - lam)*c*conv(e, g)/Mx[1]
Ar = lam*conv(-p*2**(p*Dl)*2*w*Q**(-p-1), g)/Mx[0] + (1 - lam)*(c*conv(e, g*jnp.log(g)) - c*conv(e*Phi/Q, g) - s*conv(e, g))/Mx[1]
print('f range', float(f.min()), float(f.max()), 'Q range', float(Q.min()), float(Q.max()))
print('Bc range', float(Bc.min()), float(Bc.max()), 'Ar range', float(Ar.min()), float(Ar.max()))
print('any nan', bool(jnp.any(jnp.isnan(Bc))), bool(jnp.any(jnp.isnan(Ar))))
# implied fixed point vs current ln f: residual should be constant mu
mu_est = Ar + Bc*jnp.log(f)
print('mu implied by current f: mean', float(jnp.mean(f*mu_est)), 'rel spread', float(jnp.std(mu_est)/abs(jnp.mean(mu_est))))
