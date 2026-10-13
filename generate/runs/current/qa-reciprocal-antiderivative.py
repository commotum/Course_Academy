"""Root actual unit reciprocal/power, complete-bank and ordered-solution QA."""
import importlib.util,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186064169'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'power-rule-readback.py','p');g=load(D.with_suffix('.py'),'g');s=p.s
n=dict(records=0,choices=0,whole_banks=0,printed_equalities=0,source_prompts=0,source_solutions=0,source_banks=0,source_values=0,source_absent_designations=0,source_fieldless=0,source_unrated=0,raw_missing_differentials=0)
def integrand(prompt):
 tex=re.search(r'\$([^$]+)\$',prompt).group(1).strip().rstrip('.?')
 if 'f(x)' in tex:tex=tex.split('=',1)[1]
 return p.scalar(tex)
def check(r):
 q=r['question'];gm=r['generation'];raw=gm['evidence_only'];assert gm['eligible_for_learning']==(not raw);f=integrand(q[':question/problem']);primitive=s.integrate(f,p.x);degree=f.as_powers_dict()[p.x];assert degree<0 and degree!=-1
 if not raw:assert '$x>0$' in q[':question/problem']
 for field in q.get(':question/answer-fields',[]):
  vals=[p.scalar(a[':answer/value']) for a in field[':answer-field/choices']];assert all(not p.same_derivative(z,t) for i,z in enumerate(vals) for t in vals[:i]);good=[i for i,z in enumerate(vals) if p.eq(s.diff(z,p.x),f)];assert len(good)==1
  if ':answer-field/correct' in field:assert field[':answer-field/correct'][1]==field[':answer-field/choices'][good[0]][':answer/id']
  if not raw:
   m=degree+1;bank=[primitive+p.C,degree*p.x**m+p.C,p.x**degree/m+p.C,s.diff(f,p.x)+p.C,-primitive+p.C];assert all(sum(p.eq(z,t) for z in vals)==1 for t in bank);n['whole_banks']+=1
  n['choices']+=len(vals)
 sol=q.get(':question/worked-solution')
 if sol:
  for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S):
   rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
   if rows[0].startswith("{F}^{'}"):
    assert len(rows)==3 and rows[0]=="{F}^{'}(x) & =f(x) " and 'F(x) & =' in rows[-1];continue
   for row in rows:
    for part in row.split('& ='):
     part=part.strip()
     if not part or part=='F(x)' or 'f(x)' in part:continue
     if part.startswith(r'\int ') and not part.endswith(r'\,\text{d}x'):
      assert raw and gm['source_references']==['q-29662'];part+=r'\,\text{d}x';n['raw_missing_differentials']+=1
     assert p.same_derivative(p.value(part),primitive),(gm['template'],part,primitive);n['printed_equalities']+=1
  for tex in re.findall(r'(?<!\$)\$(?!\$)([^$]+)\$(?!\$)',sol):
   if '=' in tex and not tex.startswith('n=') and 'F' not in tex and 'f(x)' not in tex:
    parts=tex.rstrip('.').split('=');assert all(p.eq(p.scalar(a),p.scalar(b)) for a,b in zip(parts,parts[1:]));n['printed_equalities']+=len(parts)-1
 n['records']+=1
if __name__=='__main__':
 cases=json.load(open(D/'source-cases.json'));old={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
 for c in cases:
  r=g.generate(c.get('level',c.get('difficulty')),template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(r);q=r['question'];o=old[c['source_id']];assert q[':question/problem']==o[':question/problem'];n['source_prompts']+=1
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in o)
  if ':question/difficulty' not in o:n['source_unrated']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_solutions']+=1
  if ':question/answer-fields' not in o:n['source_fieldless']+=1
  for of,gf in zip(o.get(':question/answer-fields',[]),q.get(':question/answer-fields',[])):
   assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices']);assert ':answer-field/correct' not in gf and ':answer-field/correct' not in of;n['source_banks']+=1;n['source_values']+=len(gf[':answer-field/choices']);n['source_absent_designations']+=1
  params=g.domain(c.get('level',c.get('difficulty')),c['template'])[0];check(g.generate(c.get('level',c.get('difficulty')),template=c['template'],profile=c['bank_profile'],parameters=params))
 tasks={}
 for level in ('easy','moderate','hard'):
  seen=set()
  for template,spec in g.TEMPLATES.items():
   if spec['level']!=level:continue
   for params in g.domain(level,template):
    r=g.generate(level,seed=33,template=template,parameters=params);check(r);seen.add(r['generation']['mathematical_fingerprint']);z=g.generate(level,seed=71,template=template,parameters=params);assert r['question'][':question/id']==z['question'][':question/id']
  tasks[level]=len(seen)
 n['finite_meaningful_tasks']=tasks
 review=json.load(open(D/'review.json'));rows=review if isinstance(review,list) else [r for rows in review.values() for r in rows]
 for r in rows:check(r.get('record',r))
 for level,params in [('easy',{'p':1,'q':1}),('easy',{'p':2,'q':4}),('moderate',{'p':10,'q':1}),('hard',{'p':3,'q':8})]:
  try:g.generate(level,parameters=params)
  except ValueError:pass
  else:raise AssertionError('Workload guard bypassed')
 (R/'qa/17592186064169-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
