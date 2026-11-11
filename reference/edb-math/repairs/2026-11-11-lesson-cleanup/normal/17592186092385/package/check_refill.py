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


from normal_math import extract,parse,key_value,s

def check(record):
 q=record['question'];prompt=q[':question/problem'];meta=record['generation'];kp=record['knowledge_point']['db_id'];provenance=json.loads(Path(__file__).with_name('source-provenance.json').read_text())
 fields=q[':question/answer-fields']
 if kp==17592186092384:
  assert re.fullmatch(r"Find the slope \$m'\$ of the normal line to the curve\n\n\$\$\ny=[^$\n]+\n\$\$\n\nat the point \$[^$]+\$\. Give an exact answer\.\n\n\$m'=\$\n\{\{field-1\}\}",prompt),'Unexpected pre-answer support or response endpoint'
  assert [f[':answer-field/key'] for f in fields]==['field-1']
  contract=provenance['bands'][meta['template']];refs=meta['source_refs']
 else:
  assert kp==17592186092385
  assert re.fullmatch(r'Find where the normal line to the curve \$y=[^$]+\$ at the point (?:\$[^$]+\$|with \$x\$-coordinate \$[^$]+\$) intersects the \$[xy]\$-axis\.\n\nThe intersection is \$\(\$\{\{field-1\}\}\$,\$ \{\{field-2\}\}\$\)\$\. Give exact values\.',prompt),'Unexpected pre-answer support or response endpoint'
  assert [f[':answer-field/key'] for f in fields]==['field-1','field-2']
  contract=provenance['families'][meta['template']];refs=meta['source_references']
 assert refs==contract['source_refs'] and meta['source_inference']==contract['reason'],'Source contract differs'
 assert not set(map(str,refs))&set(provenance['forbidden_source_refs']),'Retired/incomplete source resurfaced'
 f,x,y,m,n,b=extract(q);expected=[n] if kp==17592186092384 else ([s.simplify(-b/n),s.Integer(0)] if '$x$-axis' in prompt else [s.Integer(0),b]);checks=[]
 for i,(field,wanted) in enumerate(zip(fields,expected)):
  assert enum(field[':answer-field/type'])==':answer-field.type/blank','Radio banks must not replace the exact scalar/coordinate response'
  observed=parse(key_value(field));assert s.simplify(observed-wanted)==0,'Displayed function/point disagrees with key'
  assert wanted.is_Rational;v=s.Rational(wanted)
  checks += [dict(field_index=i,submitted=f'({v.p})/({v.q})',expected='accepted',control='equivalent',purpose='Independent exact calculus in ordinary rational notation'),dict(field_index=i,submitted=str(v+1),expected='rejected',control='wrong',purpose='Offset changes the uniquely requested normal endpoint')]
 return checks

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--records',required=True);parser.add_argument('--inventory',required=True);parser.add_argument('--output',required=True);args=parser.parse_args();records=json.loads(Path(args.records).read_text());native=[dict(fingerprint=fingerprint(r['question']),checks=check(r)) for r in records];covered=sorted(fingerprint(r['question']) for r in records)
 Path(args.output).write_text(json.dumps(dict(status='passed',checked_fingerprints=covered,native_checks=native,check_results=[dict(id=i,status='passed',checked_fingerprints=covered) for i in ['independent-normal-work','exact-normal-endpoint','eligible-source-lineage']]),indent=2)+'\n')
