"""Parent verifies displayed exponential factoring, ordered roots and complete banks."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=int(sys.argv[1]) if len(sys.argv)>1 else 17592186157437;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
p=module('parent_exponential_math',R/'exponential-factor-parser.py');g=module('parent_exponential_generator',D.with_suffix('.py'))
counts=dict(source_questions=0,source_fields=0,source_values=0,source_designations=0,source_missing_designations=0,source_prompts=0,source_solutions=0,source_solution_repairs=0,source_fieldless=0,source_missing_values=0,printed_instances=0,bank_values=0,factor_equations=0,solution_roots=0,positive_exponential_claims=0,product_claims=0)
def check(record):
 q=record['question'];values=p.read(q[':question/problem']);F,E,P,roots=values;fs=q[':question/answer-fields'];blanks=fs[0][':answer-field/type'].endswith('/blank');assert len(fs)==(2 if blanks else 1)
 for field in fs:
  bank=field[':answer-field/choices'];expected=roots[int(field[':answer-field/key'].split('-')[-1])-1] if blanks else roots[0]*roots[1]
  assert len(bank)==(1 if blanks else 5);v=[p.math(a[':answer/value']) for a in bank];assert all(not p.equal(a,b) for i,a in enumerate(v) for b in v[:i])
  assert [a[':answer/id'] for a,z in zip(bank,v) if p.equal(z,expected)]==[field[':answer-field/correct'][1]]
  counts['bank_values']+=len(bank)
 for k,v in p.stages(q[':question/worked-solution'],*values).items():counts[k]+=v
 counts['printed_instances']+=1;return values
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];old=qs[sid];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);F,E,P,roots=check(r);oF,oE,oP,ors=p.read(old[':question/problem']);assert p.equal(F,oF) and p.equal(E,oE) and p.equal(P,oP) and roots==ors
 assert old[':question/problem']==r['question'][':question/problem'];counts['source_prompts']+=1
 if old.get(':question/worked-solution'):
  raw=old[':question/worked-solution'];expected=raw.replace(' {7}^{x}+ & =0',' {7}^{x} & =0') if sid=='q-264791' else raw
  assert expected==r['question'][':question/worked-solution'],sid;assert p.stages(expected,oF,oE,oP,ors)==p.stages(r['question'][':question/worked-solution'],F,E,P,roots);counts['source_solutions']+=1
  if raw!=expected:counts['source_solution_repairs']+=1
 nf={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}
 if not old.get(':question/answer-fields'):counts['source_fieldless']+=1
 for f in old.get(':question/answer-fields',[]):
  got=nf[f[':answer-field/key']];remaining=[p.math(a[':answer/value']) for a in got[':answer-field/choices']]
  if not f.get(':answer-field/choices'):counts['source_missing_values']+=len(remaining);remaining=[]
  for answer in f.get(':answer-field/choices',[]):
   v=p.math(answer[':answer/value']);indices=[i for i,z in enumerate(remaining) if p.equal(z,v)];assert len(indices)==1,(sid,answer,remaining);remaining.pop(indices[0]);counts['source_values']+=1
  assert not remaining;counts['source_fields']+=1
  if f.get(':answer-field/correct'):
   value=next(a[':answer/value'] for a in got[':answer-field/choices'] if a[':answer/id']==got[':answer-field/correct'][1]);assert p.equal(p.math(value),p.math(f[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
  else:counts['source_missing_designations']+=1
 counts['source_questions']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
