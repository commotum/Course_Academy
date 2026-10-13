"""Parent verifies axis, required coordinate, complete banks and both blank sides."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186110602;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
p=module('parent_axis',R/'axis-line-parser.py');g=module('parent_axis_generator',D.with_suffix('.py'))
counts=dict(source_questions=0,source_banks=0,source_values=0,source_designations=0,missing_fields_derived=0,source_prompts=0,source_solutions=0,printed_instances=0,radio_equations=0,blank_equations=0,orientation_claims=0,coordinate_claims=0,equation_conclusions=0)
def check(record):
 q=record['question'];reference,point,axis,value=p.read(q[':question/problem']);fs=q[':question/answer-fields'];expected=axis-value
 if fs[0][':answer-field/type'].endswith('/radio'):
  assert len(fs)==1 and len(fs[0][':answer-field/choices'])==5
  bank=fs[0][':answer-field/choices'];values=[p.equation(a[':answer/value']) for a in bank]
  assert [a[':answer/id'] for a,v in zip(bank,values) if p.p.equivalent(v,expected)]==[fs[0][':answer-field/correct'][1]]
  assert all(not p.p.equivalent(v,w) for n,v in enumerate(values) for w in values[:n]);counts['radio_equations']+=5
 else:
  assert len(fs)==2
  fields={f[':answer-field/key']:f for f in fs};parts=[]
  for key in ('field-1','field-2'):
   f=fields[key];assert len(f[':answer-field/choices'])==1
   selected=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);parts.append(p.math(selected))
  assert p.p.equivalent(parts[0]-parts[1],expected)
  # Primitive integer standard form keeps each independently graded fragment
  # canonical; full-equation proportionality alone would hide mismatched sides.
  assert s.simplify(parts[0]-value.q*axis)==0 and parts[1]==value.p
  counts['blank_equations']+=1
 for key,n in p.check_solution(q[':question/worked-solution'],reference,point,axis,value).items():counts[key]+=n
 for raw in re.findall(r'In standard form, this is \$(.*?)\$',q[':question/worked-solution']):assert p.p.equivalent(p.equation(raw),expected)
 counts['printed_instances']+=1
 return reference,point,axis,value
def mask(text):return re.sub(r'\s+',' ',p.p.MATH.sub('$MATH$',text)).strip()
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];old=sources[sid];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile')));a=check(r);b=p.read(old[':question/problem']);assert p.p.equivalent(a[0],b[0]) and a[1:]==b[1:]
 assert mask(old[':question/problem'])==mask(r['question'][':question/problem']);counts['source_prompts']+=1
 oldsol=old.get(':question/worked-solution')
 if oldsol:
  assert mask(oldsol)==mask(r['question'][':question/worked-solution']);assert p.check_solution(oldsol,*b)==p.check_solution(r['question'][':question/worked-solution'],*a);counts['source_solutions']+=1
 for field in old[':question/answer-fields']:
  if not field.get(':answer-field/choices'):counts['missing_fields_derived']+=1;continue
  nf=next(f for f in r['question'][':question/answer-fields'] if f[':answer-field/key']==field[':answer-field/key']);remaining=[p.equation(v[':answer/value']) for v in nf[':answer-field/choices']]
  for answer in field[':answer-field/choices']:
   v=p.equation(answer[':answer/value']);matches=[i for i,w in enumerate(remaining) if p.p.equivalent(v,w)];assert len(matches)==1;(remaining.pop(matches[0]));counts['source_values']+=1
  assert not remaining;counts['source_banks']+=1
  chosen=next(v[':answer/value'] for v in nf[':answer-field/choices'] if v[':answer/id']==nf[':answer-field/correct'][1]);assert p.p.equivalent(p.equation(chosen),p.equation(field[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
 counts['source_questions']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for record in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(record)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
