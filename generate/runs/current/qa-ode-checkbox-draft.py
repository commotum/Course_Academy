"""Root actual ODE verification; current three independent Boolean field contract."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186100888;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);sys.modules[name]=m;z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_ode_checkbox_parser');g=load(D.with_suffix('.py'),'root_ode_checkbox_generator');F=load(R/'root-source-fidelity.py','root_ode_checkbox_fidelity');originals,fidelity=F.check(g,K,D);x=s.Symbol('x',positive=True);y=p.y
n=dict(records=0,boolean_fields=0,values=0,whole_statement_banks=0,formal_derivative_inputs=0,printed_equalities=0,printed_inequalities=0,domain_guards=0,prose_references=0,verdicts=0,conclusions=0)
def scalar(t):return p.scalar(t.strip().rstrip('.,').replace(r'\,✓','').replace(r'\,\times','').replace(r'\times','')).subs(p.x,x)
def equal(a,b):return s.simplify(a-b)==0
def subset(t):return frozenset(re.findall(r'\b(?:III|II|I)\b',t))
def check(r):
 q=r['question'];gm=r['generation'];assert gm['eligible_for_learning'] == (not gm['evidence_only']);prompt=q[':question/problem'];sol=q[':question/worked-solution']
 rhs=scalar(re.search(r'\$\$\s*\{y\}\^\{′\}=(.*?)\s*\$\$',prompt,re.S)[1].split(',')[0]);f=scalar(re.search(r'Let \$f\(x\)=(.*?)\$',prompt,re.S)[1]);claim=scalar(re.search(r'\$\{f\}\^\{′\}\(x\)=(.*?)\$',prompt,re.S)[1]);d=s.diff(f,x);sub=rhs.subs(y,f);i=equal(d,claim);ii=equal(d,sub);bits={'I':i,'II':ii,'III':ii};good=frozenset(k for k,v in bits.items() if v)
 assert len(q[':question/answer-fields'])==3 and {v[':answer-field/key'] for v in q[':question/answer-fields']}==set(bits)
 for field in q[':question/answer-fields']:
  assert field[':answer-field/type']==':answer-field.type/checkbox';bank=field[':answer-field/choices'];assert len(bank)==2 and sorted(a[':answer/value'] for a in bank)==['false','true'] and all(a[':answer/type']==':answer.type/text' for a in bank)
  correct=next(a[':answer/value'] for a in bank if a[':answer/id']==field[':answer-field/correct'][1]);assert correct==str(bits[field[':answer-field/key']]).lower();n['boolean_fields']+=1;n['values']+=2
 n['whole_statement_banks']+=1
 for number,b in bits.items():assert f'Statement {number} is '+('true' if b else 'false')+'.' in sol;n['verdicts']+=1
 ending=re.search(r'Therefore, the correct answer is "(.*?)\."',sol);assert ending and subset(ending[1])==good;n['conclusions']+=1
 blocks=re.findall(r'\$\$\s*\\begin\{aligned\}(.*?)\\end\{aligned\}\s*\$\$',sol,re.S);assert len(blocks)==2
 for index,row in enumerate(blocks[0].split(r'\\')):
  row=row.strip();left,right=row.split('&',1);right=right.strip()
  if index==0:
   assert left.strip()==r'{f}^{′}(x)' and right.startswith('=');formal=right[1:].strip();m=re.fullmatch(r"\{?\((.*)\)\}?\^\{′\}",formal);assert m,formal;assert equal(scalar(m[1]),f);n['formal_derivative_inputs']+=1
  elif right.startswith(r'\ne'):
   assert not i and equal(scalar(right[3:]),claim);n['printed_inequalities']+=1
  else:assert right.startswith('=') and equal(scalar(right[1:]),d);n['printed_equalities']+=1
 for index,row in enumerate(blocks[1].split(r'\\')):
  left,right=row.strip().split('&',1);right=right.strip();tentative=right.startswith(r'\overset{?}{=}');unequal=right.startswith(r'\ne');right=right[len(r'\overset{?}{=}'):] if tentative else right[3:] if unequal else right[1:]
  if index==0:assert left.strip()==r'{y}^{′}' and tentative and equal(scalar(right),rhs);continue
  assert equal(scalar(left),d);assert equal(scalar(right),sub),(gm['template'],row,sub)
  if not tentative:assert unequal==(not ii);n['printed_inequalities' if unequal else 'printed_equalities']+=1
  else:n['printed_equalities']+=1
 prose=re.search(r'Substituting \$y=(.*?)\$ and \$\{y\}\^\{′\}=(.*?)\$',sol,re.S);assert prose and equal(scalar(prose[1]),f) and equal(scalar(prose[2]),d);n['prose_references']+=2
 conclusion=re.search(r'the function \$y=(.*?)\$ is (not )?a solution',sol);assert conclusion and equal(scalar(conclusion[1]),f) and bool(conclusion[2])==(not ii);n['prose_references']+=1
 if not gm['evidence_only']:
  assert 'interval where the function is defined and the equation is valid' in sol and 'all values of $x$ in the equation\'s domain' not in sol
  domain=gm['domain'];t=gm['template']
  if t=='affine_log':
   v=re.search(r'on \$(.*?)>0\.\$',prompt);assert v;z=scalar(v[1]);assert equal(z,gm['parameters']['b']*x+gm['parameters']['c']) and equal(scalar(domain.removesuffix('>0')),z);assert f==gm['parameters']['a']*s.log(z)
  elif t in ('log_all','log_scaled'):
   z=x+gm['parameters'].get('h',0);v=re.search(r'interval \$(.*?)>0,\$',prompt);assert v and equal(scalar(v[1]),z) and equal(scalar(domain.removesuffix('>0')),z)
  elif t in ('power_easy','power_moderate','inverse_none'):assert domain=='x != 0'
  else:assert domain=='all real x'
  n['domain_guards']+=1
 n['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for c in json.loads((D/'source-cases.json').read_text()):check(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']))
for template,level in g.LEVELS.items():
 for seed in (49,157,409):check(g.generate(level,seed,template=template))
for a in (-4,2):
 for claim in (True,False):
  for solution in (True,False):check(g.generate('hard',template='affine_log',parameters={'a':a,'b':3,'c':-2,'claim':claim,'solution':solution}))
for a in (-9,-2):
 for nn in (2,5):
  try:r=g.generate('moderate',template='power_moderate',parameters={'a':a,'n':nn})
  except ValueError:assert (a,nn)==(-2,2)
  else:check(r)
result=dict(status='passed',source=fidelity,readback=n,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
