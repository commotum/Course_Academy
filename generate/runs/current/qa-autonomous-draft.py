"""Root readback: actual variable binding, whole ODEs, stages and owned Boolean fields."""
import sys,re,json,itertools,hashlib,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;REPO=R.parents[2];K=17592186166814;D=REPO/f'generate/scratch/{K}-draft'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
P=load(R/'ode-scalar-parser.py','root_scalar');F=load(R/'root-source-fidelity.py','root_fidelity');G=load(D.with_suffix('.py'),'root_generator')
x,y,d=P.x,P.y,P.k
N=dict(records=0,equations=0,values=0,numeric_isolation_rows=0,formal_dependency_rows=0,where_definitions=0,classification_sentences=0,conclusions=0,known_raw_error_rows=0,definition_bindings=0,permutation_aliases=0)
def check(rec):
 q=rec['question'];meta=rec['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];decl=re.search(r'Let \$(\w)=(\w)\((\w)\)\$\.',prompt)
 iv,dv=(decl[3],decl[1]) if decl else ('x','y')
 if decl:assert decl[1]==decl[2] and iv!=dv
 def scalar(text):
  text=text.strip().rstrip('.,').replace(r'\frac{\text{d}'+dv+r'}{\text{d}'+iv+'}','k')
  text=re.sub(r'\{'+dv+r"\}\^\{[′']\}",'k',text).replace(dv+"'",'k')
  assert r'\text{d}' not in text and "'" not in text and '′' not in text
  names={iv:'x',dv:'y'}
  text=re.sub(r'\\operatorname\{[A-Za-z]+\}|\\[A-Za-z]+|[A-Za-z]|.',lambda m:names.get(m[0],m[0]),text,flags=re.S)
  result=P.scalar(text)
  assert result.free_symbols<={x,y,d}
  return result
 def isolate(text):
  left,right=text.replace('&','').split('=');res=scalar(left)-scalar(right)
  assert s.Poly(res,d).degree()==1
  coefficient=s.diff(res,d);assert coefficient!=0
  return s.cancel(-res.subs(d,0)/coefficient)
 # Check the actual instructional definition binds dependent function/independent derivative.
 opening=sol.replace('′',"'").split('\n\nWith',1)[0]
 assert 'f('+dv+')' in opening and r'\text{d}'+dv in opening and r'\text{d}'+iv in opening
 assert '{'+dv+"}^{'}=f("+dv+')' in opening or dv+"'=f("+dv+')' in opening
 N['definition_bindings']+=1
 eqs=re.findall(r'- \*\*(I|II|III)\.\*\* \$(.*?)\$',prompt);assert [z[0] for z in eqs]==['I','II','III']
 blocks=sol.split('- Equation ')[1:];assert len(blocks)==3
 fields={f[':answer-field/key']:f for f in q[':question/answer-fields']};assert set(fields)=={'I','II','III'}
 negate='**not**' in prompt;selected=[]
 for (roman,equation),block in zip(eqs,blocks):
  assert block.startswith(roman+' ');rhs=isolate(equation);A=s.simplify(s.diff(rhs,x))==0
  assert ('is an autonomous differential equation.' in block.replace('*',''))==A
  assert bool(re.search(r'is not (?:an )?autonomous',block.replace('*','')))==(not A),(meta['template'],roman,A,block)
  f=fields[roman];choices=f[':answer-field/choices'];assert len(choices)==2 and {a[':answer/value'] for a in choices}=={'true','false'}
  expected='true' if A!=negate else 'false';assert next(a[':answer/value'] for a in choices if a[':answer/id']==f[':answer-field/correct'][1])==expected
  if expected=='true':selected.append(roman)
  rawerror=meta['template']=='q-96702' and meta['profile']=='observed_raw' and roman=='II'
  for display in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,re.S):
   for row in display.split(r'\\'):
    row=row.strip().replace('&','')
    if '=f(' in row:
     left,formal=row.split('=');assert scalar(left)==d;assert formal.strip() in (('f('+dv+')',) if A else ('f('+iv+','+dv+')',)+(('f('+iv+')',) if not rhs.has(y) else ())),(meta['template'],roman,formal,A);N['formal_dependency_rows']+=1
    else:
     good=s.simplify(isolate(row)-rhs)==0
     if not good:assert rawerror;N['known_raw_error_rows']+=1
     else:N['numeric_isolation_rows']+=1
  for formal,value in re.findall(r'where \$(f\([^)]*\))=(.*?)\.\$',block):
   good=s.simplify(scalar(value)-rhs)==0
   if not good:assert rawerror;N['known_raw_error_rows']+=1
   else:N['where_definitions']+=1
   assert formal in (('f('+dv+')',) if A else ('f('+iv+','+dv+')',)+(('f('+iv+')',) if not rhs.has(y) else ()))
  N['equations']+=1;N['values']+=2;N['classification_sentences']+=1
 assert sol.endswith('"'+' and '.join(selected)+' only."');N['conclusions']+=1;N['records']+=1
originals,source=F.check(G,K,D)
for c in json.load(open(D/'source-cases.json')):
 check(G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']))
 for binding in [('t','u'),('s','v'),('t','y')]:
  for notation in ('leibniz','prime'):
   params={k:(3 if v==2 else 2) if k.startswith('n') and k[1:].isdigit() else v for k,v in c['parameters'].items()};params.update(independent=binding[0],dependent=binding[1],notation=notation)
   check(G.generate(c['level'],template=c['template'],parameters=params,profile='observed_repaired'))
for level in ('easy','moderate','hard'):
 for seed in range(32):check(G.generate(level,seed=88000+seed))
 for binding in [('x','y'),('t','u'),('s','v'),('t','y')]:
  for notation in ('leibniz','prime'):
   rec=G.generate(level,seed=500);params=dict(rec['generation']['parameters']);params.update(independent=binding[0],dependent=binding[1],notation=notation)
   first=G.generate(level,parameters=params);check(first)
   for kinds in itertools.permutations(params['kinds']):
    again=G.generate(level,parameters={**params,'kinds':list(kinds)},seed=12)
    assert again['question'][':question/id']==first['question'][':question/id'] and again['generation']['mathematical_fingerprint']==first['generation']['mathematical_fingerprint'];N['permutation_aliases']+=1
report=dict(status='passed',source=source,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0)
(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
