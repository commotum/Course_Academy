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
    result[':question/answer-fields']=sorted(fields,key=lambda f:f[':answer-field/key'])
    return hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def check(q):
    fields=q[':question/answer-fields'];assert len(fields)==3,'Expected three independently selectable statements'
    assert len({f[':answer-field/key'] for f in fields})==3
    assert 'If none apply, leave all boxes unchecked.' in q[':question/problem']
    assert not re.search(r'(?m)^\s*(?:III|II|I)\.\s',q[':question/problem'])
    owned=set()
    for f in fields:
        assert enum(f[':answer-field/type'])==':answer-field.type/checkbox'
        key=f[':answer-field/key']
        # These packages have a bounded statement grammar; generic labels,
        # empty captions and variants of None cannot stand in for an object.
        statement_patterns=[
            r'\$[^$]+=\\mathbf\{0\}\$(?:\.| only if \$[^$]+=0\$\.)',
            r'The set \$[^$]+\$ is linearly (?:in)?dependent\.',
            r'The vectors \$[^$]+\$ are linearly (?:in)?dependent\.',
            r'The equation \$[^$]+\$ has (?:only the solution \$[^$]+\$|infinitely many solutions with coefficients not all zero)\.',
            r'At least one of \$[^$]+\$ is a free variable in row echelon form\.',
            r'Every column of the coefficient matrix contains a pivot in row echelon form\.',
        ]
        assert isinstance(key,str) and any(re.fullmatch(pattern,key) for pattern in statement_patterns),'Expected a complete reviewed statement'
        bank=f[':answer-field/choices']
        assert len(bank)==2 and {(enum(a[':answer/type']),a[':answer/value']) for a in bank}=={(':answer.type/text','true'),(':answer.type/text','false')}
        ids={str(a[':answer/id']) for a in bank}
        assert len(ids)==2 and not owned.intersection(ids)
        assert answer_id(f[':answer-field/correct']) in ids
        owned.update(ids)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--records',required=True);parser.add_argument('--inventory',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();records=json.loads(Path(args.records).read_text())
    for r in records:check(r['question'])
    covered=sorted(fingerprint(r['question']) for r in records)
    Path(args.output).write_text(json.dumps(dict(status='passed',checked_fingerprints=covered,
      check_results=[dict(id='statement-checkboxes',status='passed',checked_fingerprints=covered)]),indent=2)+'\n')
