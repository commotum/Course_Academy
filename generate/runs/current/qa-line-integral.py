"""Parent checks complete banks, actual field/potential/path and every endpoint stage."""
import argparse,importlib.util,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('parent_line_oracle',R/'line-integral-parser.py')
ap=argparse.ArgumentParser();ap.add_argument('kp',type=int);K=ap.parse_args().kp;assert K in (17592186133878,17592186133879,17592186133890)
D=R.parents[2]/f'generate/scratch/{K}';g=module('parent_line_generator_'+str(K),D.with_suffix('.py'))
counts=dict(source_banks=0,source_values=0,source_designations=0,source_prompt_math=0,source_prose_layouts=0,source_solution_repairs=0,printed_instances=0,endpoint_vectors=0,endpoint_prose=0,gradient_components=0,cross_partials=0,final_rows=0)
def objects(q):
 if K==17592186133878:return (*p.supplied(q[':question/problem']),None)
 if K==17592186133879:return p.missing(q[':question/problem'],q[':question/worked-solution'])
 return p.cartesian(q[':question/problem'],q[':question/worked-solution'])
def check(r):
 q=r['question'];f,path,d,F=objects(q);A,B,fa,fb,I=p.endpoints(f,path,d)
 for field in q[':question/answer-fields']:
  assert field[':answer-field/type']==':answer-field.type/radio';values=[p.math(a[':answer/value']) for a in field[':answer-field/choices']];assert len(values)==5
  assert all(not p.equal(v,w) for i,v in enumerate(values) for w in values[:i])
  assert [a[':answer/id'] for a,v in zip(field[':answer-field/choices'],values) if p.equal(v,I)]==[field[':answer-field/correct'][1]]
 for key,value in p.stages(q[':question/worked-solution'],f,path,d,F).items():counts[key]+=value
 if K==17592186133878 and q[':question/difficulty'].endswith('/hard'):
  assert len(path)==3 and p.equal(path[0],s.exp(p.p.t)) and p.equal(path[2],s.exp(-p.p.t));h=s.simplify(path[1]-p.p.t);assert h in (1,2,3) and d[0]==0 and d[1] in (1,2)
  terms=s.Add.make_args(s.expand(f));assert len(terms)==2 and all(term.subs(dict(zip((p.p.x,p.p.y,p.p.z),point)),simultaneous=True)!=0 for term in terms for point in (A,B))
 counts['printed_instances']+=1;return f,path,d,F
def mask(text):return re.sub(r'\s+',' ',p.MATH.sub('$MATH$',text)).strip()
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case.get('math_academy_id',case['source_id']);q=qs[sid];r=g.generate(case.get('level',case.get('difficulty')),template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);f,path,d,F=check(r)
 old=dict(q)
 for key in (':question/problem',':question/worked-solution'):
  if sid=='q-99008':old[key]=old[key].replace('f(r(\\pi ))','f(r(\\frac{\\pi }{2}))')
  if sid=='q-104637':old[key]=old[key].replace('f((r(','f(r(')
  if sid=='q-104747':old[key]=old[key].replace('$(0,0)$','$(0,2)$')
  if sid=='q-104764':old[key]=old[key].replace('f(0,e)','f(0,-e)')
  if sid=='q-39749':
   old[key]=old[key].replace('f(0,0)','f(0,-1)').replace('{0}^{2}\\cdot 0','{0}^{2}\\cdot (-1)')
 of,op,od,oF=objects(old);assert p.equal(of,f) and len(op)==len(path) and all(p.equal(a,b) for a,b in zip(op,path)) and od==d
 if F is not None:assert all(p.equal(a,b) for a,b in zip(oF,F))
 counts['source_prompt_math']+=1
 for key in (':question/problem',':question/worked-solution'):assert mask(old[key])==mask(r['question'][key]),(sid,key);counts['source_prose_layouts']+=1
 # Same full stage roles and counts; all evaluated equalities independently checked.
 old_stages=p.stages(old[':question/worked-solution'],of,op,od,oF);new_stages=p.stages(r['question'][':question/worked-solution'],f,path,d,F);assert old_stages==new_stages,(sid,old_stages,new_stages)
 if sid in ('q-99008','q-104637','q-104747','q-104764','q-39749'):counts['source_solution_repairs']+=1
 new={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}
 for field in q[':question/answer-fields']:
  nf=new[field[':answer-field/key']];remaining=[p.math(a[':answer/value']) for a in nf[':answer-field/choices']]
  for answer in field[':answer-field/choices']:
   indices=[n for n,value in enumerate(remaining) if p.equal(value,p.math(answer[':answer/value']))];assert len(indices)==1,(sid,answer,remaining);remaining.pop(indices[0]);counts['source_values']+=1
  assert not remaining;counts['source_banks']+=1
  selected=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert p.equal(p.math(selected),p.math(field[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
