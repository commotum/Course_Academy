#!/usr/bin/env python3
import importlib.util,json,copy,hashlib,itertools,re,subprocess,sys
from pathlib import Path
import sympy as S
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;R=D.parents[2]
def mod(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=mod('g',D.with_suffix('.py'));F=mod('f',R/'generate/runs/current/root-source-fidelity.py');MF=mod('mf',R/'scripts/question_capture/math_format.py')
VR=mod('vr',D/'variable-readback.py')
originals,fidelity=F.check(G,G.KP_ID,D)
count={'records':0,'choices':0,'rows':0,'formal_inputs':0};x=G.x
# Independent integration uses direct component rules, never generator CAS target.
def primitive(s):
 e=G.expression(s);a=S.expand(e).coeff(S.sin(x));b=S.expand(e).coeff(S.cos(x));assert G.eq(e,a*S.sin(x)+b*S.cos(x));return -a*S.cos(x)+b*S.sin(x)
def printed(s,h=None):
 s=re.sub(r'\\(?:begin|end)\{aligned\}','',s).replace('&','').strip().rstrip('.,')
 s=s.replace('h(x)',h) if h else s
 def integral(m):count['formal_inputs']+=1;return '('+S.sstr(primitive(m[1]))+')'
 s=re.sub(r'\\int\s*(.*?)(?:\\,)?\\text\{d\}(?:\\theta|x|y)',integral,s)
 return G.expression(s)
def check(r):
 VR.check(r)
 d=r['generation']['domain'];assert d['status']=='established' and d['integrand_domain']=='All real values of the independent variable.' and d['correct_primitive_domain']=='All real values of the independent variable.'
 assert d['integration_constant']['symbol']=='C' and d['integration_constant']['range']=='all real numbers'
 q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert q[':question/difficulty'] in [':question.difficulty/'+l for l in G.SUPPORTED_LEVELS]
 for t in [q[':question/problem'],q[':question/worked-solution'],*[a[':answer/value']for f in q[':question/answer-fields']for a in f[':answer-field/choices']]]:
  assert not any(ord(c)<32 and c not in '\n\t'for c in t)
 MF.validate_generated_record(r)
 prompt=q[':question/problem'];h=None
 if 'h(x)' in prompt:
  h=re.search(r'h\(x\)=(.*?)\$',prompt)[1];prompt=prompt.replace('h(x)',h)
 e=G.integrand(prompt)
 for f in q[':question/answer-fields']:
  vals=[G.expression(a[':answer/value'])for a in f[':answer-field/choices']];ids=[a[':answer/id']for a in f[':answer-field/choices']];ci=ids.index(f[':answer-field/correct'][1])
  assert G.eq(S.diff(vals[ci],x),e)
  for i,v in enumerate(vals):assert (i==ci)==G.eq(S.diff(v,x),e);count['choices']+=1
  for a,b in itertools.combinations(vals,2):assert not G.family_eq(a,b)
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}'in q[':question/problem'] and not vals[ci].has(G.C)
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==2
 for bi,block in enumerate(blocks):
  block=re.sub(r'\\(?:begin|end)\{aligned\}','',block)
  # Authored shared recall has two equations on a single row.
  rows=block.split('\\\\') if '\\qquad'not in block else block.split('\\qquad')
  for row in rows:
   assert '='in row
   left,right=row.split('=',1);lhs=printed(left,h)if left.replace('&','').strip()else None;rhs=printed(right,h)
   if bi==0:assert lhs is not None and G.family_eq(lhs,rhs),(r["generation"]["template"],row,lhs,rhs)
   else:
    assert G.eq(S.diff(rhs,x),e),(r["generation"]["template"],row,rhs,e)
    if lhs is not None:assert G.eq(S.diff(lhs,x),e)
   count['rows']+=1
 # Structure independently enforces real source stages, not only equality.
 main=blocks[1]
 if r['generation']['template']=='grouped':assert main.count('\\int')==5 and main.count('& =')==5
 elif r['generation']['template']in ['cos','sin']:assert main.count('\\int')==2 and main.count('& =')==3
 elif r['generation']['template']=='sum':assert main.count('\\int')==3 and main.count('& =')==3
 count['records']+=1
records=[];families={}
for level in G.SUPPORTED_LEVELS:
 seen=set();fps=set()
 for seed in range(72):
  r=G.generate(level,seed);check(r);seen.add(r['generation']['template']);fps.add(r['generation']['parameter_fingerprint']);records.append(r)
 families[level]={'default_templates':sorted(seen),'sampled_tasks':len(fps)}
for lv,ts in [('easy',['cos','sin','q-113907','q-113908','repaired_h','completed_q-71653']),('moderate',['sum','q-113909','q-2161','completed_q-71654']),('hard',['grouped'])]:
 for t in ts:
  for seed in [5,19]:r=G.generate(lv,seed,template=t);check(r);records.append(r)
# Every supported authored fragment layout receives independent and native QA.
for lv,t in [('easy','sin'),('easy','cos'),('moderate','sum'),('hard','grouped')]:
 for seed in [9,23]:
  r=G.generate(lv,seed,template=t,field_type='blank');check(r);records.append(r)
# Explicit signed arithmetic boundary variants use each public level.
boundary_cases=[]
for lv in G.SUPPORTED_LEVELS:
 for a in [-9,-2,2,9]:
  for b in ([None] if lv=='easy' else [-9,-2,2,9]):
   p={'a':a} if b is None else {'a':a,'b':b}
   try:G.guard(lv,p,['a']if lv=='easy'else['a','b'])
   except ValueError:continue
   ts=['sin','cos']if lv=='easy'else['sum']if lv=='moderate'else['grouped']
   for t in ts:
    r=G.generate(lv,template=t,parameters=p);check(r);records.append(r);boundary_cases.append([lv,t,p])
# Mathematical capacity excludes aliases/banks/seeds and is a finite domain.
dom=[a for a in range(-9,10)if abs(a)>=2]
authored_capacities={'easy':len(dom)*2,'moderate':sum(abs(a)!=abs(b)for a in dom for b in dom),'hard':sum(a*b<0 and abs(a)!=abs(b)for a in dom for b in dom)}
# Original anchor source-stage replay and changed coefficient variation.
changed=[];raw_audit=[]
def audit_raw(r,c):
 VR.check(r)
 q=r['question'];sid=c['source_id'];h='-'+str(r['generation']['parameters']['a'])+r'\sin x' if 'h(x)'in q[':question/problem']else None
 target=-r['generation']['parameters']['a']*S.sin(x) if h else G.integrand(q[':question/problem'])
 assert r['generation']['domain']['status']==('unresolved' if h else 'established')
 row={'source_id':sid,'parameters':r['generation']['parameters'],'choices':0,'pairs':0,'equivalent_wrong_pairs':0,'inferred_missing_key':False,'undefined_h':h is not None,'worked_rows':0}
 for f in q.get(':question/answer-fields',[]):
  vals=[G.expression(a[':answer/value'])for a in f[':answer-field/choices']]
  good=[i for i,v in enumerate(vals)if G.eq(S.diff(v,x),target)];assert len(good)==1,(sid,r["generation"]["parameters"],q[":question/problem"],vals,target)
  if ':answer-field/correct'in f:assert f[':answer-field/choices'][good[0]][':answer/id']==f[':answer-field/correct'][1]
  else:row['inferred_missing_key']=True
  for i,a in enumerate(vals):
   for j,b in enumerate(vals[:i]):
    row['pairs']+=1
    if G.family_eq(a,b):assert sid=='q-17654' and i not in good and j not in good;row['equivalent_wrong_pairs']+=1
  row['choices']+=len(vals)
 if ':question/worked-solution'in q:
  blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==2
  for bi,block in enumerate(blocks):
   block=re.sub(r'\\(?:begin|end)\{aligned\}','',block)
   for st in block.split('\\\\'):
    left,right=st.split('=',1);lhs=printed(left,h)if left.replace('&','').strip()else None;rhs=printed(right,h)
    if bi==0:assert lhs is not None and G.family_eq(lhs,rhs)
    else:
     assert G.eq(S.diff(rhs,x),target),(sid,st,rhs,target)
     if lhs is not None:assert G.eq(S.diff(lhs,x),target)
    row['worked_rows']+=1
 raw_audit.append(row)
for c in json.load(open(D/'source-cases.json')):
 for p in [c['parameters'],{k:([8,7][i] if v!=[8,7][i]else 6)for i,(k,v)in enumerate(c['parameters'].items())}]:
  r=G.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=p);assert not r['generation']['eligible_for_learning'];audit_raw(r,c)
  if p!=c['parameters']:
   q=r['question'];o=originals[c['source_id']]
   assert q.get(':question/worked-solution')!=o.get(':question/worked-solution')or q[':question/problem']!=o[':question/problem']or c['source_id']=='q-2034'
 changed.append(c['source_id'])
# Level guards, collisions, unknown keys/profiles and hard sign boundaries.
negative=[]
for lv,t,p in [('easy','cos',{'a':1}),('easy','sin',{'a':-10}),('moderate','sum',{'a':2,'b':-2}),('hard','grouped',{'a':3,'b':4}),('hard','grouped',{'a':0,'b':-5}),('moderate','q-113909',{'a':3,'b':3})]:
 try:G.generate(lv,template=t,parameters=p)
 except (ValueError,AssertionError):negative.append([lv,t,p])
 else:raise AssertionError('invalid inputs accepted')
mutations=[];anchor=G.generate('hard',template='grouped',parameters={'a':-3,'b':7})
for kind in ['wrong primitive','formal factor','operation omission','C0','wrong key']:
 r=copy.deepcopy(anchor);q=r['question'];s=q[':question/worked-solution']
 if kind=='wrong primitive':q[':question/worked-solution']=s.replace('4\\sin x-10\\cos x','4\\sin x+10\\cos x')
 elif kind=='formal factor':q[':question/worked-solution']=s.replace('4\\int','5\\int')
 elif kind=='operation omission':q[':question/worked-solution']=s.replace('\\int (4\\cos x+10\\sin x)\\,\\text{d}x','4\\sin x-10\\cos x')
 elif kind=='C0':q[':question/problem']+='\x0c'
 else:q[':question/answer-fields'][0][':answer-field/correct'][1]=q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']
 assert r!=anchor
 try:check(r)
 except Exception:mutations.append(kind)
 else:raise AssertionError('mutation escaped '+kind)
target_probe=G.generate('easy',template='cos',parameters={'a':-5})
wrong_target=copy.deepcopy(target_probe);wrong_target['question'][':question/problem']=wrong_target['question'][':question/problem'].replace(r'\cos',r'\sin')
try:check(wrong_target)
except Exception:mutations.append('changed sine/cosine target with stale solution')
else:raise AssertionError('stale target mutation escaped')
# Identity independent of seed/profile alias and bank ordering.
for lv,t,p in [('easy','sin',{'a':-9}),('moderate','sum',{'a':-3,'b':7}),('hard','grouped',{'a':-3,'b':7})]:
 a=G.generate(lv,1,template=t,parameters=p);b=G.generate(lv,44,template=t,parameters=p,profile='authored_'+t);assert a['question'][':question/id']==b['question'][':question/id']
def equivalent_entry(v):
 e=G.expression(v);parts=[]
 for fn in ['cos','sin']:
  a=S.expand(e).coeff(getattr(S,fn)(x))
  if a:
   # A genuine unreduced distributive decomposition of one component.
   if not parts:parts.extend(['('+str(a-1)+')'+'\\'+fn+' x','\\'+fn+' x'])
   else:parts.append('('+str(a)+')'+'\\'+fn+' x')
 alt='+'.join(parts)
 assert G.eq(G.expression(alt),e)
 if 'y'in v:alt=alt.replace(' x',' y')
 return alt
engine=[]
for i,r in enumerate(records):
 f=r['question'][':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected','purpose':'actual displayed radio ID'}for a in f[':answer-field/choices']]
 else:
  v=f[':answer-field/choices'][0][':answer/value'];alt=equivalent_entry(v);checks=[{'submitted':v,'expected':'accepted','purpose':'canonical fragment'},{'submitted':alt,'expected':'accepted','purpose':'equivalent unreduced fragment'},{'submitted':v+'+1','expected':'rejected','purpose':'wrong fragment constant'},{'submitted':'-('+v+')','expected':'rejected','purpose':'wrong sign'}]
 engine.append({'label':str(i),'record':r,'checks':checks})
for c in json.load(open(D/'source-cases.json')):
 r=G.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);fs=r['question'].get(':question/answer-fields',[])
 if not fs or ':answer-field/correct'not in fs[0]:continue
 f=fs[0]
 if f[':answer-field/type'].endswith('/radio'):checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected','purpose':'raw source ID, mathematics reported separately'}for a in f[':answer-field/choices']]
 else:
  v=f[':answer-field/choices'][0][':answer/value'];checks=[{'submitted':v,'expected':'accepted','purpose':'raw canonical fragment, undefined prompt ineligible'},{'submitted':equivalent_entry(v),'expected':'accepted','purpose':'raw equivalent fragment'},{'submitted':'-('+v+')','expected':'rejected','purpose':'raw wrong sign'}]
 engine.append({'label':'raw_'+c['source_id'],'record':r,'checks':checks})
(D/'engine-input.json').write_text(json.dumps(engine));subprocess.run([str(R/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
before=json.load(open(D/'registered-baseline-before.json'));base=D.parent/'17592186064178';after={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [base.with_suffix('.py'),*sorted(base.rglob('*'))]if p.is_file()};assert before==after
(D/'registered-baseline-after.json').write_text(json.dumps(after,indent=2))
report={'status':'passed','fidelity':fidelity,'independent_inventory':6,'mathematics':count,'coverage':families,'explicit_boundaries':boundary_cases,'authored_core_capacities':authored_capacities,'raw_mathematical_audit':raw_audit,'changed_source_parameters':changed,'negative_inputs':negative,'mutation_regressions':mutations,'source_limitations':{'q-17654':'Two wrong primitive families differ only by an arbitrary constant; raw evidence ineligible.','q-2033/q-2034':'Missing difficulty,correct designation and solution preserved; inferred keys are not observed matches.','q-71653/q-71654':'Fields absent in raw evidence; completed blanks explicitly authored.','q-167331/q-167785/q-166078':'Undefined h in raw prompt; repaired_h supplies actual integrand from solution, explicitly authored.'},'dependency_versions':{'python':sys.version.split()[0],'sympy':S.__version__},'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'registered_baseline_unchanged':True,'baseline_files':len(after),'database_writes':0,'grader':json.load(open(D/'engine-report.json'))}
(D/'review.json').write_text(json.dumps(records,indent=2,ensure_ascii=False));(D/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k!='grader'},indent=2))
