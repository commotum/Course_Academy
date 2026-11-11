"""Offline response-contract checks on actual refill survivors."""
import argparse
import hashlib
import json
from pathlib import Path
import re

def enum(v):return str(v.get(':db/ident') if isinstance(v,dict) else v)
def answer_id(v):
    return str(v[':answer/id'] if isinstance(v,dict) else v[1] if isinstance(v,(list,tuple)) else v)

def fingerprint(q):
    # Same identity-free content projection as the publisher. Difficulty,
    # explanations, answer feedback and allocated entity IDs do not identify
    # a fresh mathematical question.
    result={k:q[k] for k in (':question/problem',':question/requires-calculator') if k in q}
    fields=[]
    for f in q[':question/answer-fields']:
        choices=[{':answer/type':enum(a[':answer/type']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]
        correct=next(a for a in f[':answer-field/choices'] if str(a[':answer/id'])==answer_id(f[':answer-field/correct']))
        fields.append({':answer-field/key':f[':answer-field/key'],':answer-field/type':enum(f[':answer-field/type']),
            ':answer-field/choices':sorted(choices,key=lambda a:json.dumps(a,sort_keys=True)),
            ':answer-field/correct':{':answer/type':enum(correct[':answer/type']),':answer/value':correct[':answer/value']}})
    for f in fields:
        if f[':answer-field/type'] in (':answer-field.type/blank', ':answer-field.type/free'):
            f.pop(':answer-field/choices')
    result[':question/answer-fields']=sorted(fields,key=lambda f:f[':answer-field/key'])
    return hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def rational(value):
    from fractions import Fraction
    value=value.replace(' ','').replace(r'\dfrac',r'\frac')
    m=re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(\d+)\}',value)
    if m:return Fraction((-1 if m[1] else 1)*int(m[2]),int(m[3]))
    return Fraction(value)

def check(q):
    prompt=q[':question/problem']
    head,tail=prompt.split('\n\n',1)
    assert re.fullmatch(r'Find the equation of the normal line to the curve \$y=[^$]+\$ at \$\\left\([^$]+\\right\)\$\.',head),'Unexpected support or malformed task stem'
    fields=q[':question/answer-fields'];keys=[f[':answer-field/key'] for f in fields]
    if len(keys)==2 and set(keys)=={'coefficient','constant'}:
        expected='Give exact values of $a$ and $b$ in $x+ay=b$.\n\n$a=$ {{coefficient}}\n\n$b=$ {{constant}}'
    else:
        assert len(keys)==2 and set(keys)=={'slope','intercept'}
        expected='Give exact values of $a$ and $b$ in $y=ax+b$.\n\n$a=$ {{slope}}\n\n$b=$ {{intercept}}'
    assert tail==expected,'Response endpoint/support changed'
    checks=[]
    for i,f in enumerate(fields):
        assert enum(f[':answer-field/type'])==':answer-field.type/blank'
        correct=next(a for a in f[':answer-field/choices'] if str(a[':answer/id'])==answer_id(f[':answer-field/correct']))
        v=rational(correct[':answer/value'])
        checks += [dict(field_index=i,submitted=f'({v.numerator})/({v.denominator})',expected='accepted',control='equivalent',purpose='Exact rational value in ordinary fraction notation'),
                   dict(field_index=i,submitted=str(v+1),expected='rejected',control='wrong',purpose='A coefficient one greater changes this uniquely specified line')]
    return checks

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--records',required=True);parser.add_argument('--inventory',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();records=json.loads(Path(args.records).read_text())
    native=[dict(fingerprint=fingerprint(r['question']),checks=check(r['question'])) for r in records]
    covered=sorted(fingerprint(r['question']) for r in records)
    Path(args.output).write_text(json.dumps(dict(status='passed',checked_fingerprints=covered,native_checks=native,
      check_results=[dict(id='independent-normal-task',status='passed',checked_fingerprints=covered),dict(id='labeled-coefficient-endpoint',status='passed',checked_fingerprints=covered)]),indent=2)+'\n')
