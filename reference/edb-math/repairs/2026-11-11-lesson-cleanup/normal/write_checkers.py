from pathlib import Path
import json
H=Path('/home/jake/Developer/Course_Academy/reference/edb-math/repairs/2026-11-11-lesson-cleanup/normal')
base=Path('/media/jake/SSD/EDB/math/generators/2d/2dad35d505965ce58f224701b7f4ca5db306cc23475610593ecb06f7f76b9908/check_refill.py').read_text().split('def rational(value):')[0]
code=r'''
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
'''
for kp in [17592186092384,17592186092385]:
 D=H/str(kp);P=D/'package';prov=json.loads((P/'source-provenance.json').read_text());source=json.loads((D/'source/source.json').read_text());prov['forbidden_source_refs']=sorted({str(row[k]) for row in source['material']['source_eligibility']['excluded_questions'] for k in [':db/id',':question/id',':question/math-academy-id'] if k in row});(P/'source-provenance.json').write_text(json.dumps(prov,indent=2)+'\n');(P/'check_refill.py').write_text(base+code)
