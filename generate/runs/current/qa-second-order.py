"""Root independently reads second-order banks and both integration passes."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186096697;D=R.parents[2]/f'generate/scratch/{K}'
def mod(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=mod('root_second_reader',R/'second-order-readback.py');g=mod('root_second_generator',D.with_suffix('.py'));X=p.X;C=p.C;DC=p.D
T=dict(records=0,choices=0,complete_operation_banks=0,evidence_banks=0,displayed_solution_equalities=0,source_prompts=0,source_values=0,source_solutions=0,present_source_keys=0,missing_source_keys=0)
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def check(r):
 q=r['question'];meta=r['generation'];G,coef=p.forcing(q[':question/problem']);F1=p.primitive(G);F0=p.primitive(F1);assert meta['evidence_only']==(not meta['eligible_for_learning']);actual=[]
 for field in q[':question/answer-fields']:
  vals=[p.answer(a[':answer/value']) for a in field[':answer-field/choices']];assert sum(p.valid(v,G) for v in vals)==1
  for i,v in enumerate(vals):
   for w in vals[:i]:assert not p.equivalent(v,w)
  correct=field.get(':answer-field/correct')
  if correct:assert p.valid(next(v for a,v in zip(field[':answer-field/choices'],vals) if a[':answer/id']==correct[1]),G)
  else:assert meta['evidence_only']
  T['choices']+=len(vals);actual=vals
 if not meta['evidence_only']:
  expected=[F0+C*X+DC,-F0+C*X+DC,F1+C*X+DC,F0+DC,F0+C*X];assert all(sum(p.equivalent(v,w) for w in expected)==1 for v in actual);T['complete_operation_banks']+=1
  if coef==1:assert q[':question/worked-solution'].startswith('Integrating the equation once')
  else:assert q[':question/worked-solution'].startswith('First, we rearrange')
 else:T['evidence_banks']+=1
 phase=0
 for block in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
  if r'\begin{aligned}' not in block:
   left,right=block.split('=',1);assert s.simplify((p.expression(left)-p.expression(right)).subs(p.D2,G))==0;T['displayed_solution_equalities']+=1;continue
  phase+=1;prev=None;rows=block.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(r'\\')
  for row in rows:
   left,right=row.split('=',1);a=p.expression(left) if p.normalize(left) else prev;b=p.expression(right);assert a is not None
   aa=a.subs({p.D2:G,p.D1:F1+C,p.F:F0+C*X+DC});bb=b.subs({p.D2:G,p.D1:F1+C,p.F:F0+C*X+DC});assert s.simplify(s.diff(aa-bb,X))==0,(meta,row,aa,bb);prev=b;T['displayed_solution_equalities']+=1
  if phase==1:assert s.simplify(prev-(F1+C))==0
  elif phase==2:assert p.equivalent(prev,F0+C*X+DC)
 assert phase==2
 T['records']+=1;return q
for case in json.loads((D/'source-cases.json').read_text()):
 r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=check(r);old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];assert q[':question/worked-solution']==old[':question/worked-solution'];T['source_prompts']+=1;T['source_solutions']+=1;assert q[':question/difficulty']==old[':question/difficulty'][':db/ident'];assert len(q[':question/answer-fields'])==len(old[':question/answer-fields'])
 for f,of in zip(q[':question/answer-fields'],old[':question/answer-fields']):
  assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);T['source_values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];T['present_source_keys']+=1
  else:T['missing_source_keys']+=1
 for a in (2,'3/2'):check(g.generate(case['level'],template=case['template'],parameters={'scale':a},profile=case['bank_profile']))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
for item in json.loads((D/'review.json').read_text()):check(item['record'])
for template,level in g.TEMPLATES.items():
 for seed in range(4):check(g.generate(level,7714+seed,template=template))
T['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(T,indent=2)+'\n');print(T)
