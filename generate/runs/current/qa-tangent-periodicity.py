"""Root supplied tangent value, actual shifted target and every equality stage."""
import importlib.util,json,re,sys,hashlib,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186176050;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','period_parent');x,N,T=p.x,p.z,p.t
def normalize(raw):return raw.replace('tan⁡',r'\tan ').replace(r'\operatorname{tan}⁡',r'\tan ').replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
def scalar(raw):
 raw=re.sub(r'\\[A-Za-z]+|n',lambda m:m[0] if m[0].startswith('\\') else 'z',raw);return p.scalar(raw.strip().rstrip('.,'))
def eq(a,b):return s.simplify(a-b)==0
def reduce_tangent(raw,value,expected_shift=None):
 raw=normalize(raw);shifts=[]
 def replace(m):
  arg=scalar(m[1]);assert s.diff(arg,x)==1;delta=s.expand((arg-x)/s.pi);assert not delta.has(x) and s.diff(delta,N,2)==0
  if delta.has(N):assert delta.coeff(N).is_integer and delta.subs(N,0).is_integer
  else:assert delta.is_integer
  shifts.append(delta);return '('+s.latex(value)+')'
 raw=re.sub(r'\\tan\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)',replace,raw)
 raw=re.sub(r'\\tan\s*x',lambda m:'('+s.latex(value)+')',raw)
 if expected_shift is not None:assert shifts and shifts[-1]==expected_shift
 return scalar(raw)
C={key:0 for key in ('records','actual_given_values','actual_targets','source_prompts','source_solutions','source_fields','source_values','source_refs','source_missing_refs','source_missing_ratings','solution_equalities','prose_values','prose_shifts','complete_choices','whole_method_banks','identity_period_links')}
def check(rec):
 q=rec['question'];prompt=normalize(q[':question/problem']);ins=re.findall(r'\$(.*?)\$',prompt,re.S);given=scalar(re.search(r'\\tan\s*x\s*=\s*(.*?)\$',prompt)[1]);target=ins[-1];args=re.findall(r'\\tan\s*\((.*?)\)',target);assert len(args)==1;shift=s.simplify((scalar(args[0])-x)/s.pi);assert shift.is_Integer and shift!=0
 template=rec['generation']['template'];target_affine=re.sub(r'\\tan\s*\((.*?)\)','t',target);expression=scalar(target_affine);a=s.diff(expression,T);b=expression.subs(T,0);assert not a.free_symbols and not b.free_symbols and eq(expression,a*T+b);answer=a*given+b
 assert eq(reduce_tangent(target,given,shift),answer);C['actual_given_values']+=1;C['actual_targets']+=1
 f=q[':question/answer-fields'][0];values=[scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(values)==5 and all(not eq(a,b) for a,b in itertools.combinations(values,2));hits=[z[':answer/id'] for z,val in zip(f[':answer-field/choices'],values) if eq(val,answer)];assert len(hits)==1
 if ':answer-field/correct' in f:assert hits==[f[':answer-field/correct'][1]]
 else:assert rec['generation']['evidence_only']
 if not rec['generation']['evidence_only']:
  if template.startswith('direct'):wanted=[given,1/given,-given,-1/given,given+shift*s.pi]
  elif template=='add':wanted=[answer,given,b,-given+b,given+shift*s.pi+b]
  elif template=='scale':wanted=[answer,given,given/a,-answer,a*(given+shift*s.pi)]
  else:wanted=[answer,a*given,a*given-b,a+b*given,a*(given+shift*s.pi)+b]
  assert all(sum(eq(val,z) for z in wanted)==1 for val in values);C['whole_method_banks']+=1
 sol=normalize(q.get(':question/worked-solution',''))
 if sol:
  n=re.search(r'Substituting \$n=(.*?)\$',sol);assert n and scalar(n[1])==shift;C['prose_shifts']+=1
  for raw in re.findall(r'\$(.*?)\$',sol,re.S):
   if '$' in raw or '=' not in raw or r'\tan' not in raw or raw.strip().startswith('y='):continue
   parts=raw.strip().rstrip('.,').split('=');results=[reduce_tangent(part,given) for part in parts];assert all(eq(z,results[0]) for z in results),(raw,results);C['prose_values']+=1
  for block in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
   for row in normalize(block).split(r'\\'):
    parts=row.strip().rstrip('.,').split('=');assert len(parts)>=2;results=[reduce_tangent(part,given) for part in parts];assert all(eq(z,results[0]) for z in results),(row,results);C['solution_equalities']+=len(parts)-1
    if r'\tan' in row:C['identity_period_links']+=len(parts)-1
 C['records']+=1;C['complete_choices']+=5
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_periodicity');old={q[':question/math-academy-id']:q for q in json.load(open(R/f'sources/{K}.json'))['record'][':knowledge-point/questions']}
 for case in json.load(open(D/'source-cases.json')):
  rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=rec['question'];o=old[case.get('math_academy_id',case['source_id'])];check(rec)
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (key in q)==(key in o)
  assert q[':question/problem']==o[':question/problem'];C['source_prompts']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];C['source_solutions']+=1
  C['source_missing_ratings']+=int(':question/difficulty' not in o)
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);C['source_fields']+=1;C['source_values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];C['source_refs']+=1
   else:C['source_missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for level,families in g.TEMPLATES.items():
  for family in families:
   for seed in (791,792,793):records.append(g.generate(level,seed=seed,template=family))
 for rec in records:check(rec)
 out=dict(status='passed',readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
