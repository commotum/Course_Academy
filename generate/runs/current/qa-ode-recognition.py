"""Root actual one-function ODE statement, full-bank and formal-stage readback."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186100888'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','p');g=load(D.with_suffix('.py'),'g');x=s.Symbol('x',positive=True);y=p.y
n=dict(records=0,choices=0,whole_statement_banks=0,formal_derivative_inputs=0,printed_equalities=0,printed_inequalities=0,source_prompts=0,source_solutions=0,source_banks=0,source_values=0,source_designations=0)
def scalar(t):return p.scalar(t.strip().rstrip('.,').replace(r'\,✓','').replace(r'\,\times','').replace(r'\times','')).subs(p.x,x)
def equal(a,b):return s.simplify(a-b)==0
def subset(t):return frozenset(re.findall(r'\b(?:III|II|I)\b',t))
def check(r):
 q=r['question'];gm=r['generation'];assert gm['eligible_for_learning'] == (not gm['evidence_only']);prompt=q[':question/problem'];sol=q[':question/worked-solution']
 rhs=scalar(re.search(r'\$\$\s*\{y\}\^\{′\}=(.*?)\s*\$\$',prompt,re.S).group(1).split(',')[0]);f=scalar(re.search(r'Let \$f\(x\)=(.*?)\$',prompt,re.S).group(1));claim=scalar(re.search(r'\$\{f\}\^\{′\}\(x\)=(.*?)\$',prompt,re.S).group(1));d=s.diff(f,x);sub=rhs.subs(y,f);i=equal(d,claim);ii=equal(d,sub);good=frozenset((['I'] if i else [])+(['II','III'] if ii else []))
 field=q[':question/answer-fields'][0];bank=field[':answer-field/choices'];assert len(bank)==5;subsets=[subset(z[':answer/value']) for z in bank];assert len(set(subsets))==5 and subsets.count(good)==1;correct=next(z[':answer/value'] for z in bank if z[':answer/id']==field[':answer-field/correct'][1]);assert subset(correct)==good;n['choices']+=5;n['whole_statement_banks']+=1
 for number,b in [('I',i),('II',ii),('III',ii)]:assert f'Statement {number} is '+('true' if b else 'false')+'.' in sol
 assert 'correct answer is "'+correct+'."' in sol
 blocks=re.findall(r'\$\$\s*\\begin\{aligned\}(.*?)\\end\{aligned\}\s*\$\$',sol,re.S);assert len(blocks)==2
 for index,row in enumerate(blocks[0].split(r'\\')):
  row=row.strip();left,right=row.split('&',1);right=right.strip()
  if index==0:
   assert right.startswith('=');formal=right[1:].strip();m=re.fullmatch(r"\{?\((.*)\)\}?\^\{′\}",formal);assert m,formal;assert equal(scalar(m[1]),f);n['formal_derivative_inputs']+=1
  elif right.startswith(r'\ne'):
   assert not i and equal(scalar(right[3:]),claim);n['printed_inequalities']+=1
  else:assert right.startswith('=') and equal(scalar(right[1:]),d);n['printed_equalities']+=1
 for index,row in enumerate(blocks[1].split(r'\\')):
  left,right=row.strip().split('&',1);right=right.strip();tentative=right.startswith(r'\overset{?}{=}');unequal=right.startswith(r'\ne');right=right[len(r'\overset{?}{=}'):] if tentative else right[3:] if unequal else right[1:]
  if index==0:assert tentative and equal(scalar(right),rhs);continue
  assert equal(scalar(left),d);assert equal(scalar(right),sub),(gm['template'],row,sub)
  if not tentative:assert unequal==(not ii);n['printed_inequalities' if unequal else 'printed_equalities']+=1
  else:n['printed_equalities']+=1
 prose=re.search(r'Substituting \$y=(.*?)\$ and \$\{y\}\^\{′\}=(.*?)\$',sol,re.S);assert prose and equal(scalar(prose[1]),f) and equal(scalar(prose[2]),d)
 if not gm['evidence_only']:
  assert 'interval' in sol
  if gm['template']=='affine_log':assert 'on $' in prompt and '>0.$' in prompt
  if gm['template'] in ('log_all','log_scaled'):assert '>0' in prompt
 n['records']+=1
if __name__=='__main__':
 cases=json.load(open(D/'source-cases.json'));old={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
 for c in cases:
  r=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(r);q=r['question'];o=old[c['source_id']];assert q[':question/problem']==o[':question/problem'];assert q[':question/worked-solution']==o[':question/worked-solution'];assert q[':question/difficulty']==o[':question/difficulty'][':db/ident'];n['source_prompts']+=1;n['source_solutions']+=1
  for of,gf in zip(o[':question/answer-fields'],q[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices']);assert of[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);n['source_banks']+=1;n['source_values']+=len(gf[':answer-field/choices']);n['source_designations']+=1
 for template,level in g.LEVELS.items():
  for seed in range(7):
   r=g.generate(level,seed+9100,template=template);check(r);z=g.generate(level,seed+9900,template=template,profile=r['generation']['bank_profile'],parameters=r['generation']['parameters']);assert r['question'][':question/id']==z['question'][':question/id'];check(g.generate(level,seed+9100,template=template,parameters=r['generation']['parameters'],profile='authored'))
 for a in (-4,2):
  for claim in (True,False):
   for solution in (True,False):check(g.generate('hard',template='affine_log',parameters={'a':a,'b':3,'c':-2,'claim':claim,'solution':solution}))
 for r in json.load(open(D/'review.json')):check(r.get('record',r))
 for level,template,params in [('moderate','power_moderate',{'a':-6,'n':2}),('hard','affine_log',{'a':2,'b':1,'c':1,'claim':True,'solution':True}),('easy','sin_none',{'k':1})]:
  try:g.generate(level,template=template,parameters=params)
  except ValueError:pass
  else:raise AssertionError('Workload guard bypassed')
 (R/'qa/17592186100888-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
