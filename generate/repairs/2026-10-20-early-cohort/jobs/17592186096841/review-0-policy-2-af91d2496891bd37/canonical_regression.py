"""Strict source-coverage regression. Expected to fail on the reviewed package.
The author can adapt construction to an explicit cubic-term slot; the mathematical
assertion and original source target must be retained.
"""
from review import *
r=g.generate_moderate(seed=99173,template='quartic_radio',parameters={'a':3,'b':1,'n':5})
q=r['question']
f=parse(re.search(r'f\(x\)\s*=\s*(.*?)\$',q[':question/problem'])[1].rstrip('.,'))
required=(3*x**4+x**3)**5
assert s.expand(f-required)==0, 'Canonical e-181 cannot replay: generated (3*x^4+x)^5 instead of (3*x^4+x^3)^5; expose the second inner term degree.'
assert s.expand(parse(correct(q)[':answer/value'])-s.diff(required,x))==0
