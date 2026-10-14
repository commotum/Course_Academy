"""Root reflected arguments, complete oddness banks and all arithmetic stages."""
import importlib.util,json,re,sys,hashlib,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186176058;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','odd_parent');X,T=p.x,p.t
def normalize(raw,variable):
 raw=raw.replace('tan⁡',r'\tan ').replace(r'\operatorname{tan}⁡',r'\tan ').replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
 if variable!='x':raw=re.sub(r'\\[A-Za-z]+|'+variable,lambda m:m[0] if m[0].startswith('\\') else 'x',raw)
 return raw
def scalar(raw):return p.scalar(raw.strip().rstrip('.,'))
def eq(a,b):return s.simplify(a-b)==0
def reduced(raw,value):
 def replace(m):
  arg=scalar(m[1]);coefficient=s.diff(arg,X);shift=s.simplify((arg-coefficient*X)/s.pi);assert coefficient in (-1,1) and shift.is_Integer
  return '('+s.latex(coefficient*value)+')'
 raw=re.sub(r'\\tan\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)',replace,raw);raw=re.sub(r'\\tan\s*x',lambda m:'('+s.latex(value)+')',raw);return scalar(raw)
C={key:0 for key in ('records','given_values','reflected_arguments','solution_equalities','prose_equalities','choices','whole_banks','source_prompts','source_solutions','source_values','source_refs','source_missing_refs','source_missing_ratings','canonical_shift_alias_regressions')}
def check(rec):
 q=rec['question'];prompt=q[':question/problem'].replace('tan⁡',r'\tan ');m=re.search(r'\\tan\s*([axt])\s*=\s*(.*?)\$',prompt);assert m;variable=m[1];value=scalar(m[2]);prompt=normalize(prompt,variable);target=re.findall(r'\$(.*?)\$',prompt,re.S)[-1].strip().rstrip('=');arg=re.search(r'\\tan\s*\((.*?)\)',target)[1];angle=scalar(arg);assert s.diff(angle,X)==-1;shift=s.simplify((angle+X)/s.pi);assert shift.is_Integer
 affine=scalar(re.sub(r'\\tan\s*\((.*?)\)','t',target));c=s.diff(affine,T);b=affine.subs(T,0);assert not c.free_symbols and not b.free_symbols and eq(affine,c*T+b);answer=-c*value+b
 assert eq(reduced(target,value),answer);C['given_values']+=1;C['reflected_arguments']+=1;f=q[':question/answer-fields'][0];values=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5 and all(not eq(a,b) for a,b in itertools.combinations(values,2));hits=[a[':answer/id'] for a,val in zip(f[':answer-field/choices'],values) if eq(val,answer)];assert len(hits)==1
 if ':answer-field/correct' in f:assert hits==[f[':answer-field/correct'][1]]
 else:assert rec['generation']['evidence_only']
 profile=rec['generation']['profile'];template=rec['generation']['template']
 if profile=='reciprocal_zero':wanted=[-value,value,1/value,0,-1/value]
 elif profile=='numerator_omission':wanted=[value,1/value,-value,-1/value,-s.Rational(1,value.q)]
 elif profile in ('output_shift','raw_unrated'):wanted=[-value+shift*s.pi,value+shift*s.pi,-value,0,value]
 elif profile=='affine_operations':wanted=[answer,c*value+b,-c*value-b,-value+b,-c*value]
 elif profile=='integer_observed':wanted=[answer,0,c*value+b,-(c*value+b),b]
 else:wanted=None
 if wanted is not None:assert all(sum(eq(val,z) for z in wanted)==1 for val in values);C['whole_banks']+=1
 sol=normalize(q.get(':question/worked-solution',''),variable)
 for block in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
  previous=None
  for row in block.split(r'\\'):
   parts=[part.strip() for part in row.strip().rstrip('.,').split('=')];assert len(parts)>=2
   results=[reduced(part,value) for part in parts if part]
   if parts[0]=='':assert previous is not None;results.insert(0,previous)
   assert all(eq(z,results[0]) for z in results),(template,row,results);previous=results[-1];C['solution_equalities']+=len(results)-1
 inline=re.sub(r'\$\$.*?\$\$','',sol,flags=re.S)
 for raw in re.findall(r'\$(.*?)\$',inline,re.S):
  if '=' not in raw or raw.startswith('y='):continue
  parts=raw.strip().rstrip('.,').split('=');assert all(eq(reduced(z,value),reduced(parts[0],value)) for z in parts);C['prose_equalities']+=1
 if not rec['generation']['evidence_only']:
  level=q[':question/difficulty'].rsplit('/',1)[1]
  if level=='easy':assert shift==0 and c==1 and b==0
  elif level=='moderate':assert shift!=0 and c==1 and b==0
  else:assert shift!=0 and 0<c<1 and c.is_Rational and c.q<=8 and value.is_Integer and value<=-2 and b>0
 C['records']+=1;C['choices']+=5
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_oddness');old={q[':db/id']:q for q in json.load(open(R/f'sources/{K}.json'))['record'][':knowledge-point/questions']}
 for case in json.load(open(D/'source-cases.json')):
  rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=rec['question'];o=old[case['source_id']];check(rec)
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (key in q)==(key in o)
  assert q[':question/problem']==o[':question/problem'];C['source_prompts']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];C['source_solutions']+=1
  C['source_missing_ratings']+=int(':question/difficulty' not in o)
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);C['source_values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];C['source_refs']+=1
   else:C['source_missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for family,level in g.TEMPLATES.items():
  for seed in (801,802,803):records.append(g.generate(level,seed=seed,template=family))
 for rec in records:check(rec)
 for template in ('shifted','affine_integer','affine_fraction'):
  rec=g.generate(g.TEMPLATES[template],seed=804,template=template);params=dict(rec['generation']['parameters']);params['n']=7 if params['n']!=7 else 3;other=g.generate(g.TEMPLATES[template],template=template,parameters=params);assert other['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint'] and other['question'][':question/id']!=rec['question'][':question/id'];C['canonical_shift_alias_regressions']+=1
 out=dict(status='passed',readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
