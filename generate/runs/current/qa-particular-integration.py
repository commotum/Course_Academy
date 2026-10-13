"""Root proof of actual particular functions, supplied fragments and condition rows."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186096699;D=R.parents[2]/f'generate/scratch/{K}'
def mod(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=mod('root_particular_reader',R/'particular-integration-readback.py');g=mod('root_particular_generator',D.with_suffix('.py'));X=p.X;C=p.C
T=dict(records=0,choices=0,whole_operation_banks=0,evidence_banks=0,displayed_solution_equalities=0,initial_condition_equalities=0,documented_source_error_rows=0,source_prompts=0,source_values=0,source_solutions=0,present_source_keys=0,missing_source_keys=0,source_attribute_omissions=0)
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']};tasks={l:set() for l in ('easy','moderate','hard')}
def check(r):
 q=r['question'];meta=r['generation'];G,t,v,name=p.problem(q[':question/problem']);vals,full=p.responses(q,name);valid=lambda z:p.equal(p.derivative(z),G,t) and p.equal(z.subs(X,t),v,t);assert sum(valid(z) for z in full)==1;assert meta['evidence_only']==(not meta['eligible_for_learning']);field=q[':question/answer-fields'][0];ref=field.get(':answer-field/correct')
 if ref:assert valid(next(z for a,z in zip(field[':answer-field/choices'],full) if a[':answer/id']==ref[1]))
 else:assert meta['evidence_only'] and ':question/difficulty' not in q and ':question/worked-solution' not in q
 for i,z in enumerate(vals):
  for w in vals[:i]:assert not p.equal(z,w,t)
 P=p.primitive(G);constant=s.simplify(v-P.subs(X,t));F=s.simplify(P+constant)
 if not meta['evidence_only']:
  assert q[':question/worked-solution'].startswith('The derivative is already isolated');level=q[':question/difficulty'].split('/')[-1];tasks[level].add(s.srepr(G)+'|'+str(t)+'|'+str(v))
  if field[':answer-field/type'].endswith('radio'):
   expected=[F,P]+[h+v-h.subs(X,t) for h in (-P,G,P/2)];assert len(vals)==5 and all(sum(p.equal(z,w,t) for w in expected)==1 for z in vals);T['whole_operation_banks']+=1
 else:T['evidence_banks']+=1
 sol=q.get(':question/worked-solution')
 if sol:
  # Check actual variable roles before normalization, retaining only documented
  # raw teaching-label errors; repaired and default records may not contain them.
  for m in re.finditer(r'(f\(x\)|g\(x\)|(?<![A-Za-z])y)\s*(?:&\s*)?=',sol):
   expected_name='y' if name=='y' else name+'(x)'
   if m[1]!=expected_name:assert meta['profile']=='observed_raw' and meta['template'] in ('q-119045','q-50044')
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);last_aligned=max(i for i,b in enumerate(blocks) if r'\begin{aligned}' in b);submatch=re.search(r'Let \$u=(.*?)\.\$',sol);sub=p.expression(submatch[1]) if submatch else None
  def resolve(z):
   if sub is not None:z=z.subs(p.SUB,sub)
   return p.interval(z.subs({p.DF:G,p.F:F,C:constant}),t)
  for i,b in enumerate(blocks):
   if r'\begin{aligned}' not in b:
    left,right=b.split('=',1);a=p.expression(left);z=p.expression(right)
    if a==p.F:assert valid(z)
    else:assert p.equal(resolve(a),resolve(z),t)
    T['displayed_solution_equalities']+=1;continue
   prev=None
   for row in b.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(r'\\'):
    if meta['profile']=='observed_raw' and meta['template']=='q-50044' and r'6(\frac{{x}^{3}}{3})\,\text{d}x' in row:T['documented_source_error_rows']+=1;prev=p.F;continue
    left,right=row.split('=',1);a=p.expression(left) if p.normalize(left) else prev;z=p.expression(right);assert a is not None;aa=resolve(a);zz=resolve(z)
    if i==last_aligned:assert p.equal(aa,zz,t),(meta,row,aa,zz);T['initial_condition_equalities']+=1
    else:assert p.equal(p.derivative(aa-zz),0,t),(meta,row,aa,zz)
    prev=z;T['displayed_solution_equalities']+=1
  # Every prose condition uses the actual given point, including changed targets.
  for m in re.finditer(r'[fgy]\(([-\d]+)\)\s*=\s*(-?\d+)',sol):assert s.Integer(m[1])==t and s.Integer(m[2])==v
 T['records']+=1;T['choices']+=len(vals);return q
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];T['source_prompts']+=1
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
  assert (key in q)==(key in old)
  if key not in old:T['source_attribute_omissions']+=1
 if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution'];T['source_solutions']+=1
 f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0];assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert len(f[':answer-field/choices'])==len(of[':answer-field/choices']);actual=p.responses(q,p.problem(q[':question/problem'])[3])[0];original=p.responses(old,p.problem(old[':question/problem'])[3])[0];t=p.problem(old[':question/problem'])[1];assert all(sum(p.equal(z,w,t) for w in actual)==1 for z in original);T['source_values']+=len(original);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
 if ':answer-field/correct' in of:
  cv=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);ov=of[':answer-field/correct'][':answer/value'];assert p.equal(p.expression(cv.split('=')[-1]),p.expression(ov.split('=')[-1]),t);T['present_source_keys']+=1
 else:T['missing_source_keys']+=1
 b=int(case['parameters']['target'])
 for target in (b+2,b-3):
  for profile in ('observed_raw','observed_repaired'):check(g.generate(case['level'],template=case['template'],parameters={'target':target},profile=profile))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
review=json.loads((D/'review.json').read_text())
for item in review['originals']:
 for r in (item['raw'],item['repaired']):check(r)
for r in review['observed_variants']:check(r)
for rs in review['authored_variants'].values():
 for r in rs:check(r)
T['meaningful_printed_tasks']={l:len(v) for l,v in tasks.items()};assert min(T['meaningful_printed_tasks'].values())>=6;T['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(T,indent=2)+'\n');print(T)
