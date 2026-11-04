"""Parse Appendix A (filters) and Appendix C (certificates) of the pinned baseline TeX into exact-decimal JSON."""
import json, re, sys, hashlib
tex_path, out = sys.argv[1], sys.argv[2]
raw = open(tex_path, 'rb').read(); tex = raw.decode()
lines = tex.splitlines()
def section(start_pat, end_pat):
    i = next(k for k, l in enumerate(lines) if start_pat in l)
    j = next(k for k in range(i + 1, len(lines)) if end_pat in lines[k])
    return lines[i:j]
A = section('section*{Appendix A. The 43 filters}', 'section*{Appendix B')
filters = []
for l in A:
    m = re.match(r'^(\d+) & ([\d.]+) & ([^&]+) & ([^\\]+)\\\\', l.strip())
    if m:
        v = int(m.group(1)); assert v == len(filters)
        r = [x.strip() for x in m.group(3).split(',')]; s = [x.strip() for x in m.group(4).split(',')]
        assert len(r) == 8 and len(s) == 8
        filters.append(dict(kappa=m.group(2), r_coef=r, s_coef=s))
assert len(filters) == 43
Csec = section('section*{Appendix C.', 'section*{Appendix D')
B = ['1', '1.25', '1.6', '2', '2.6', '3.5', '5', '8', '15', None]
certs = []
for l in Csec:
    m = re.match(r'^(\d+) & \$\\rho_\{(\d)\}\$ & ([^&]*) & ([^\\]+)\\\\', l.strip())
    if m:
        v, i = int(m.group(1)), int(m.group(2))
        cons = [int(x) for x in m.group(3).replace(' ', '').split(',') if x != '']
        z = [x.strip() for x in m.group(4).split(',')]
        c = dict(v=v, region=i, cons=cons, z=z)
        if i == 0: c.update(case='case1', lo=None, hi=None); nrows = 2
        else: c.update(case='band', lo=B[i - 1], hi=B[i]); nrows = 3 if B[i] is not None else 2
        assert len(z) == nrows + len(cons), (v, i, len(z), nrows, cons)
        certs.append(c)
assert len(certs) == 430
assert sorted((c['v'], c['region']) for c in certs) == [(v, i) for v in range(43) for i in range(10)]
json.dump(dict(source_sha256=hashlib.sha256(raw).hexdigest(), tau0='0.48769', eta='0.51613',
               filters=filters, certs=certs), open(out, 'w'), indent=1)
print('parsed', len(filters), 'filters', len(certs), 'certs; tex sha256', hashlib.sha256(raw).hexdigest())
