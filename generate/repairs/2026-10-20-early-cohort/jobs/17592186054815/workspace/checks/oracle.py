"""Independent witness: read public prompt/keys, never generation metadata."""
import re
from fractions import Fraction
from math import isqrt

ROMANS = ('I','II','III','IV')
def enum(x): return x.get(':db/ident') if isinstance(x,dict) else x

def parse_value(text):
    t = re.search(r'\$([^$]+)\$',text)[1] if '$' in text else text
    t = re.sub(r'\s+','',t).split('=',1)[0]
    sg = -1 if t.startswith('-') else 1
    t = t.lstrip('-')
    if '\\pi' in t: return sg,False,False
    m = re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',t)
    if m:
        a,b = int(m[1] or 1),int(m[2]); rational = isqrt(b)**2 == b
        return sg,rational,rational
    m = re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',t)
    v = Fraction(sg*int(m[1]),int(m[2])) if m else sg*Fraction(t)
    return (v>0)-(v<0),True,v.denominator == 1

def target(question):
    p = question[':question/problem'].split('?',1)[0]
    base = re.search(r'(?:\\mathbb\{)?([ZQR])',p)[1]
    return base, bool(re.search(r'_\{?0',p)), '+' if '+' in p else '-'

def membership(text,t):
    base,zero,sign = t
    sg,rat,integer = parse_value(text)
    if sg == 0: return zero
    return sg == (1 if sign=='+' else -1) and (base=='R' or rat) and (base!='Z' or integer)

def subset(text):
    if text=='None': return 0
    return sum(1<<ROMANS.index(r) for r in re.findall(r'\b(?:IV|III|II|I)\b',text))

def entries(q):
    if enum(q[':question/answer-fields'][0][':answer-field/type'])==':answer-field.type/radio':
        return re.findall(r'(?m)^(?:IV|III|II|I|[1-4])\.\s*(\$[^$]+\$)',q[':question/problem'])
    return [f[':answer-field/key'] for f in q[':question/answer-fields'] if f[':answer-field/key'] not in ('None','None of the above')]

def mask(record):
    q = record['question']; es=entries(q)
    assert len(es)==4,es
    return sum(1<<i for i,e in enumerate(es) if membership(e,target(q)))

def expected_values(record):
    q=record['question'];m=mask(record)
    if enum(q[':question/answer-fields'][0][':answer-field/type'])==':answer-field.type/radio':
        choices=q[':question/answer-fields'][0][':answer-field/choices']
        values=[a[':answer/value'] for a in choices if subset(a[':answer/value'])==m]
        assert len(values)==1,(m,values)
        assert len(set(subset(a[':answer/value']) for a in choices))==len(choices)
        return values
    return [str(not bool(m)).lower() if f[':answer-field/key'] in ('None','None of the above') else str(membership(f[':answer-field/key'],target(q))).lower() for f in q[':question/answer-fields']]

def correct_value(field):
    ref=field[':answer-field/correct']; aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
    return next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==aid)

def verify(record, solutions=True):
    q=record['question']; expected=expected_values(record)
    assert [correct_value(f) for f in q[':question/answer-fields']]==expected,q[':question/id']
    if solutions and not record['generation'].get('bank_profile')=='captured':
        bullets=[s for s in q[':question/worked-solution'].split('\n\n') if s.startswith('- ')]
        assert len(bullets)==4
        for i,b in enumerate(bullets):
            assert membership(b,target(q))==('does *not* belong' not in b),(i,b)
    return expected
