#!/usr/bin/env python3
"""Independent displayed-math checks, full replay and native memory-only grading."""
import importlib.util,json,hashlib,re,sys,copy,subprocess,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;R=D.parents[2]
def module(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=module('G',D.with_suffix('.py'));F=module('F',R/'generate/runs/current/root-source-fidelity.py')
originals,fidelity=F.check(G,G.KP_ID,D)

def equal(a,b):
 e=a-b;args={f.args[0] for f in e.atoms(s.Function)};sub={};circles=[]
 for j,v in enumerate(sorted(args,key=str)):
  c,z=s.symbols('cosine'+str(j)+' sine'+str(j));circles.append((c,z));sub.update({s.sin(v):z,s.cos(v):c,s.sec(v):1/c,s.csc(v):1/z,s.tan(v):z/c,s.cot(v):c/z})
 num=s.fraction(s.cancel(e.xreplace(sub)))[0]
 for c,z in circles:
  if num!=0:num=s.rem(num,c*c+z*z-1,c)
 return s.expand(num)==0

def integrate_printed(arg,v):
 e=G.expression(arg);out=0
 for term in s.Add.make_args(s.expand(e)):
  for fn,anti in ((s.sin(v),-s.cos(v)),(s.cos(v),s.sin(v)),(s.sec(v)*s.tan(v),s.sec(v)),(s.csc(v)*s.cot(v),-s.csc(v))):
   c=s.cancel(term/fn)
   if not c.has(v):out+=c*anti;break
  else:raise AssertionError('unsupported printed formal argument '+arg)
 assert equal(s.diff(out,v),e)
 return out

def printed(t):
 t=re.sub(r'\\(?:begin|end)\{aligned\}','',t).replace('&','').strip().rstrip('.,')
 def sub(m):
  variable={'\\theta':'theta'}.get(m[2],m[2]);v=s.Symbol(variable,real=True)
  return '('+s.sstr(integrate_printed(m[1],v))+')'
 t=re.sub(r'\\int\s*(.*?)(?:\\,)?\\text\{d\}(\\theta|x|y)',sub,t)
 return G.expression(t)

C={'records':0,'choice_derivatives':0,'solution_rows':0,'formal_inputs':0,'all_pairs':0}
def check(r):
 q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'}
 for st in (q[':question/problem'],q[':question/worked-solution'],*[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]):
  assert not any(ord(c)<32 and c not in '\n\t' for c in st)
 G.MF.validate_generated_record(r)
 prompt=q[':question/problem'];var='theta' if '\\theta' in prompt else 'y' if '\\text{d}y' in prompt else 'x';v=s.Symbol(var,real=True);e=G.integrand(prompt)
 for f in q[':question/answer-fields']:
  vals=[G.expression(a[':answer/value']) for a in f[':answer-field/choices']];ids=[a[':answer/id'] for a in f[':answer-field/choices']];ci=ids.index(f[':answer-field/correct'][1]);assert len(vals)==5
  assert equal(s.diff(vals[ci],v),e)
  for i,x in enumerate(vals):assert (equal(s.diff(x,v),e))==(i==ci);C['choice_derivatives']+=1
  for a,b in itertools.combinations(vals,2):assert not equal(s.diff(a-b,v),0);C['all_pairs']+=1
 # Each recalled relation and every operative main-chain row is read from the
 # actual prose. Formal integrals are evaluated independently by component.
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==2
 def signature(sol):
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
  return [[(row.count('\\int'),re.findall(r'(?:sin|cos|sec|csc|tan|cot)',row)) for row in re.sub(r'\\(?:begin|end)\{aligned\}','',b).split('\\\\')] for b in blocks]
 k=r['generation']['template'];t=G.RECIPES[k];reference=G.render(t['solution'],t['parameters'])
 if k=='q-113925':reference=reference.replace(r'\operatorname{cos}\operatorname{csc}',r'\operatorname{csc}')
 reference=G.MF.normalize_prose(G.clean(reference))
 assert signature(q[':question/worked-solution'])==signature(reference),'operative source stage removed/reordered'

 for block_index,block in enumerate(blocks):
  clean=re.sub(r'\\(?:begin|end)\{aligned\}','',block)
  rows=clean.split('\\\\');assert len(rows)>=1
  for row in rows:
   if '=' not in row:continue
   left,right=row.split('=',1);lhs=printed(left) if left.replace('&','').strip() else None;rhs=printed(right)
   if block_index==0:
    assert lhs is not None and equal(s.diff(lhs-rhs,v),0)
   else:
    assert equal(s.diff(rhs,v),e)
    if lhs is not None:assert equal(s.diff(lhs,v),e)
   C['solution_rows']+=1;C['formal_inputs']+=row.count('\\int')
 C['records']+=1

records=[]
# All supported family/default coverage and declared slot boundaries.
for lv,banks in G.BANKS.items():
 for k in banks:
  for i in range(4):
   p={a:(G.RATIONALS[(i*7+j)%len(G.RATIONALS)] if lv=='hard' else (2 if k=='q-71659' and i==0 else [1,4,8,12][i])) for j,a in enumerate(G.RECIPES[k]['parameters'])}
   r=G.generate(lv,i,template=k,parameters=p);check(r);records.append(r)
  assert G.generate(lv,44,template=k,parameters=p)['question'][':question/id']==G.generate(lv,77,template=k,parameters=p)['question'][':question/id']
for lv in G.SUPPORTED_LEVELS:
 seen=set()
 for i in range(32):
  r=G.generate(lv,i);check(r);seen.add(r['generation']['template']);records.append(r)
 assert seen==set(G.BANKS[lv]),(lv,seen)
# Explicit parameter scope enforcement.
for lv,k,p in [('easy','q-71659',{'a':1}),('moderate','q-113930',{'a':13,'b':3}),('hard','q-113930',{'a':2,'b':'3/2'}),('hard','q-113930',{'a':'20/3','b':'3/2'})]:
 try:G.generate(lv,template=k,parameters=p)
 except (ValueError,AssertionError):pass
 else:raise AssertionError('invalid explicit input accepted')
# Mutation tests require validator failures without changing generator/shared files.
mutations=[]
anchor=G.generate('moderate',template='q-113930',parameters={'a':3,'b':7})
for purpose,mutate in [
 ('wrong primitive sign',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('=-\\operatorname{csc}', '=\\operatorname{csc}'))),
 ('distributed operator input corruption',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('7\\int', '6\\int'))),
 ('collapsed equal formal stage',lambda q:q.__setitem__(':question/worked-solution',re.sub(r'3\\int \\operatorname\{sec\}.*?\\text\{d\}x\+7\\int \\operatorname\{csc\}.*?\\text\{d\}x',r'3\\operatorname{sec}⁡x-7\\operatorname{csc}⁡x+C',q[':question/worked-solution']))),
 ('C0 control byte',lambda q:q.__setitem__(':question/problem',q[':question/problem']+'\x0c'))]:
 r=copy.deepcopy(anchor);mutate(r['question'])
 assert r!=anchor, 'mutation did not alter content: '+purpose
 try:check(r)
 except Exception:mutations.append(purpose)
 else:raise AssertionError('mutation not rejected '+purpose)
# All correct and incorrect radio IDs exercise native engine selection, not CAS.
engine=[]
for i,r in enumerate(records):
 f=r['question'][':question/answer-fields'][0]
 engine.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all radio IDs'} for a in f[':answer-field/choices']]})
(D/'engine-input.json').write_text(json.dumps(engine));subprocess.run([str(R/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
# Raw source error detection and exact presence are fidelity, never claimed as
# mathematical correctness. Missing keys/fields remain missing in public replay.
raw_errors={'q-113920':'sec(x) cot(x) equals csc(x); duplicate correct antiderivative','q-113925':'extra cos in distributed integral input','q-2038':'one wrong option uses x rather than theta','q-2042':'missing difficulty/solution/correct; ordinary decoded single-backslash TeX','q-2044':'missing difficulty/solution/correct; ordinary decoded single-backslash TeX','q-113923':'answer fields absent','q-71657':'answer fields absent'}
# Original observed raw profile variation remains a real coefficient recipe.
for c in json.load(open(D/'source-cases.json')):
 if c['parameters']:
  p={k:11 if v!=11 else 10 for k,v in c['parameters'].items()};r=G.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=p);assert r['question'][':question/problem']!=originals[c['source_id']][':question/problem']
normal_originals=[G.generate(G.RECIPES[k]['level'],template=k,parameters=G.RECIPES[k]['parameters']) for k in G.BANKS['easy']+G.BANKS['moderate']]
for r in normal_originals:check(r)
# Preserve complete registered script/evidence path set and every file hash.
before=json.load(open(D/'registered-baseline-before.json'));base=D.parent/'17592186064179';paths=[base.with_suffix('.py'),*sorted(p for p in base.rglob('*') if p.is_file())];after={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};assert before==after
(D/'registered-baseline-after.json').write_text(json.dumps(after,indent=2)+'\n')
tasks={}
for lv in G.SUPPORTED_LEVELS:
 fps=set();domains={}
 for k in G.BANKS[lv]:
  slots=list(G.RECIPES[k]['parameters']);dom=G.RATIONALS if lv=='hard' else range(2 if k=='q-71659' else 1,13);domains[k]=len(dom)**len(slots)
  for vals in itertools.product(dom,repeat=len(slots)):
   e=G.integrand(G.render(G.RECIPES[k]['prompt'],dict(zip(slots,vals))));v=s.Symbol(G.RECIPES[k]['variable'],real=True);fps.add(s.srepr(s.expand(e.subs(v,s.Symbol('x',real=True)))))
 tasks[lv]={'unique_assessed_tasks':len(fps),'profile_instances':domains}
report={'status':'passed','bounded_meaningful_inventory':tasks,'fidelity':fidelity,'independent_inventory':4,'mathematics':C,'mutation_regressions':mutations,'raw_source_errors':raw_errors,'presentation_byte_audit':{k:{'prompt_adjacent_backslash_pairs':q[':question/problem'].count('\\\\'),'answer_literal_unicode_escapes':sum(a[':answer/value'].count('\\u2061') for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[]))} for k,q in originals.items()},'source_repairs_separate':{'q-113920':'one ambiguous choice replaced with integrand','q-113925':'stray cos removed from first distributed integral; fields authored'},'authored_levels':['hard'],'eligible_default_profiles':G.BANKS,'dependency_versions':{'python':sys.version.split()[0],'sympy':s.__version__},'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'registered_baseline_files':len(after),'registered_baseline_unchanged':True,'database_writes':0,'grader':json.load(open(D/'engine-report.json'))}
raw_review=[]
for c in json.load(open(D/'source-cases.json')):
 for p in (c['parameters'],{k:11 if v!=11 else 10 for k,v in c['parameters'].items()}):raw_review.append(G.generate(c['level'],template=c['template'],parameters=p,profile=c['bank_profile']))
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(D/'review.json').write_text(json.dumps(raw_review+records+normal_originals,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='grader'},indent=2))
