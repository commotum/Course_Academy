"""Normal sampling must retain source-supported opposite-role equal frequencies."""
import json
import sympy as s
import generator as g
import legacy
class ControlledRNG:
    def __init__(self): self.roles=iter(['sin','cos'])
    def choice(self,values): return next(self.roles) if values==['sin','cos'] else values[0]
    def randint(self,a,b): return 0
p=g.parameters('trig',ControlledRNG())
assert p['m']==p['n'] and p['fx']!=p['fy']
for A,B in [(1,1),(2,2),(2,3)]:
    q=g.build('moderate','trig',p|dict(A=A,B=B),412)['question']
    f=q[':question/answer-fields'][0]
    answer=next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
    speed=legacy.parse_tex(answer).function
    assert s.trigsimp(speed**2-((A*p['m'])**2*s.cos(p['m']*g.T)**2+(B*p['n'])**2*s.sin(p['n']*g.T)**2))==0
    if A==B:
        assert s.simplify(speed-A*p['m'])==0
        assert 'The squared coefficients match' in q[':question/worked-solution']
        options=[legacy.parse_tex(c[':answer/value']).function for c in f[':answer-field/choices']]
        assert sum(not v.has(g.T) for v in options)>=2
        assert sum(v.is_Integer is True for v in options)>=2
print(json.dumps({'passed':True,'equal_frequency_cases':3}))
