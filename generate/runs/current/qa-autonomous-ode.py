"""Root independent isolation, explicit dependency, stages and owned booleans."""
import sys,re,json,itertools,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','reader');x,y,d=p.x,p.y,p.k
def scalar(text):
 text=text.replace(r'\frac{\text{d}y}{\text{d}x}','k');text=re.sub(r'\{y\}\^\{[′\']\}', 'k',text);return p.scalar(text.strip().rstrip('.,'))
def isolate(text):
 l,r=text.replace('&','').split('=');F=scalar(l)-scalar(r);assert s.Poly(F,d).degree()==1;return s.cancel(-F.subs(d,0)/s.diff(F,d))
n=dict(records=0,equations=0,choices=0,numeric_isolation_rows=0,formal_dependency_rows=0,where_definitions=0,classification_sentences=0,conclusions=0,known_raw_error_rows=0,source_prompts=0,source_solutions=0,source_values=0,source_refs=0)
def check(rec):
 q=rec['question'];g=rec['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];eqs=re.findall(r'- \*\*(?:I|II|III)\.\*\* \$(.*?)\$',prompt);assert len(eqs)==3;negate='**not**' in prompt;selected=[]
 blocks=sol.split('- Equation ')[1:];assert len(blocks)==3
 for i,(equation,block,f) in enumerate(zip(eqs,blocks,q[':question/answer-fields'])):
  rhs=isolate(equation);A=s.simplify(s.diff(rhs,x))==0;roman=('I','II','III')[i];assert block.startswith(roman+' ')
  assert ('is an autonomous differential equation' in block)==A;expected='true' if A!=negate else 'false';choices=f[':answer-field/choices'];assert {z[':answer/value'] for z in choices}=={'false','true'} and f[':answer-field/key']==roman
  actual=next(z[':answer/value'] for z in choices if z[':answer/id']==f[':answer-field/correct'][1]);assert actual==expected
  if expected=='true':selected.append(roman)
  raw_error=g['template']=='q-96702' and g['profile']=='observed_raw' and i==1
  for display in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,re.S):
   for row in display.split(r'\\'):
    row=row.strip().replace('&','')
    if '=f(' in row:
     l,formal=row.split('=');assert scalar(l)==d and ((formal=='f(y)')==A);n['formal_dependency_rows']+=1
    else:
     correct=s.simplify(isolate(row)-rhs)==0
     if not correct:assert raw_error;n['known_raw_error_rows']+=1
     else:n['numeric_isolation_rows']+=1
  for form,value in re.findall(r'where \$(f\([^)]*\))=(.*?)\.\$',block):
   correct=s.simplify(scalar(value)-rhs)==0
   if not correct:assert raw_error;n['known_raw_error_rows']+=1
   else:n['where_definitions']+=1
   assert ((form=='f(y)')==A)
  n['equations']+=1;n['choices']+=2;n['classification_sentences']+=1
 assert sol.endswith('"'+' and '.join(selected)+' only."');n['conclusions']+=1;n['records']+=1
if __name__=='__main__':
 kp=17592186166814;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':db/id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);check(rec);q=rec['question'];o=olds[c['source_id']]
  assert set(q)==set(o) and q[':question/problem']==o[':question/problem'] and q[':question/worked-solution']==o[':question/worked-solution'] and q[':question/difficulty']==o[':question/difficulty'][':db/ident']
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert set(f)==set(of) and f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);correct=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert correct==of[':answer-field/correct'][':answer/value'];n['source_values']+=2;n['source_refs']+=1
  n['source_prompts']+=1;n['source_solutions']+=1
  for params in ({k:2 if v!=2 else 3 for k,v in c['parameters'].items()},):check(g.generate(c['level'],parameters=params,template=c['template'],profile='observed_repaired'))
 for item in json.load(open(D/'review.json')):check(item['record'])
 for level in ('easy','moderate','hard'):
  for seed in range(35):check(g.generate(level,seed=670000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
