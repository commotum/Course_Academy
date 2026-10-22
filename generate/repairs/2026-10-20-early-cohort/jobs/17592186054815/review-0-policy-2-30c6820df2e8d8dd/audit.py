import sys
sys.dont_write_bytecode=True
import json, pathlib, random, hashlib, subprocess, shutil, re, platform
from fractions import Fraction
from math import isqrt
from collections import Counter,defaultdict
E=pathlib.Path(__file__).resolve().parent
J=E.parent; W=J/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy'); PY=str(REPO/'.venv/bin/python')
sys.path.insert(0,str(W));import generator as g

def save(n,d): (E/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in W.iterdir() if p.is_file()}
save('package-hashes-before.json',hashes())
source=json.load(open(J/'source/source.json'));orig=source['material']['kp'][':knowledge-point/questions']
batch=json.load(open(J/'samples.json'));save('batch-records.json',batch)
# Oracle reads visible TeX and target; does not use generator membership/classification metadata.
def value(tex):
 t=tex.replace('$','').replace(' ','').replace('The number','')
 sg=-1 if t.startswith('-') else 1;t=t.lstrip('-')
 if '\\pi' in t:return sg,False,False,'pi:'+t
 m=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',t)
 if m:
  a=int(m[1] or 1);b=int(m[2]);r=isqrt(b)**2==b
  return sg,r,r,('rat:'+str(Fraction(sg*a*isqrt(b)))) if r else f'root:{sg*a}:{b}'
 m=re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',t)
 v=Fraction(sg*int(m[1]),int(m[2])) if m else Fraction(('-' if sg<0 else '')+t)
 return (v>0)-(v<0),True,v.denominator==1,'rat:'+str(v)
def target(q):
 p=q[':question/problem'];m=re.search(r'\\mathbb\{([ZQR])\}(_0)?\^\{([+-])\}',p)
 if not m:raise ValueError(p)
 return m[1], bool(m[2]),m[3]
def oracle(r):
 q=r['question'];base,zero,sg=target(q);truth=[];ordinary=[]
 for f in q[':question/answer-fields']:
  if f[':answer-field/key']=='None of the above':continue
  s,rat,integer,_=value(f[':answer-field/key']);ordinary.append((s==0 and zero) or (s==(-1 if sg=='-' else 1) and (base=='R' or rat) and (base!='Z' or integer)))
 j=0
 for f in q[':question/answer-fields']:
  if f[':answer-field/key']=='None of the above':truth.append(not any(ordinary))
  else:truth.append(ordinary[j]);j+=1
 return truth
def stored(r):
 return [next(a[':answer/value']=='true' for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]) for f in r['question'][':question/answer-fields']]
fresh=g.batch('easy',64,829317);save('fresh-records.json',fresh)
controlled=[]
for t in g.TARGETS:
 for mask in range(16):
  _,ns,_=g.sample(random.Random(9327+mask),t,mask);controlled.append(g.generate(t,ns,seed=9327+mask,index=mask))
save('controlled-records.json',controlled)
ns=[g.number('integer',0),g.number('sqrt',1,2),g.number('fraction',1,2),g.number('integer',-3)]
pairs=[g.generate('Q0+',ns,seed=101),g.generate('R0+',ns,seed=102)]
ns2=list(ns);ns2[2]=g.number('fraction',3,4);pairs.append(g.generate('Q0+',ns2,seed=103))
ns3=list(ns);ns3[0]=g.number('integer',1);pairs.append(g.generate('Q0+',ns3,seed=104))
save('counterfactual-records.json',pairs)
allrecords=batch+fresh+controlled+pairs
fail=[]
for i,r in enumerate(allrecords):
 if oracle(r)!=stored(r):fail.append({'index':i,'id':r['question'][':question/id'],'expected':oracle(r),'stored':stored(r)})
save('math-checks.json',{'command':f'{PY} -B {E}/audit.py','oracle':'parse visible rendered-input TeX using Fraction and integer square tests; classify independently of generation metadata','checked':len(allrecords),'failures':fail,'counterfactual_truths':[oracle(r) for r in pairs]})
# Native grader every true/false choice with expected outcome from oracle.
cases=[]
for i,r in enumerate(allrecords):
 checks=[]
 for j,(f,truth) in enumerate(zip(r['question'][':question/answer-fields'],oracle(r))):
  for a in f[':answer-field/choices']:
   checks.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if (a[':answer/value']=='true')==truth else 'rejected','purpose':'independent class/sign/zero membership; both checked and unchecked learner states'})
 cases.append({'label':f'independent-{i}','record':r,'checks':checks})
save('grader-input.json',cases)
# Coverage + cue scores by target using complete-response success; random independent 4-item subset baseline 1/16.
def metrics(rs):
 groups=defaultdict(list)
 for r in rs:groups[r['generation']['profile']].append(r)
 return {'count':len(rs),'groups':{t:{'count':len(rr),'masks':dict(Counter(str(sum(1<<i for i,b in enumerate(oracle(r)[:4]) if b)) for r in rr)),'choose_first_only':sum(oracle(r)[:4]==[True,False,False,False] for r in rr),'choose_last_only':sum(oracle(r)[:4]==[False,False,False,True] for r in rr),'choose_none':sum(not any(oracle(r)[:4]) for r in rr),'choose_all':sum(all(oracle(r)[:4]) for r in rr)} for t,rr in groups.items()}}
save('coverage.json',{'fresh':metrics(fresh),'controlled':metrics(controlled),'batch':metrics(batch),'notes':'Each cue is scored as a complete selected subset, not an isolated box. All masks are deliberate independent controlled boundaries, not a claim about finite random balance.'})
replay=g.replay_sources();save('replay-records.json',replay)
rep={}
for r in replay:
 for sid in r['generation']['source_question_ids']:rep[sid]=r
norm=lambda x:re.sub(r'\s+','',x)
source_results=[]
for q in orig:
 sid=q[':question/id'];r=rep.get(sid)
 if not r:source_results.append({'source_id':sid,'status':'omitted','type':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'],'complete_bank':[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]});continue
 old={norm(f[':answer-field/key']):f for f in q[':question/answer-fields']};new={norm(f[':answer-field/key']):f for f in r['question'][':question/answer-fields']}
 fields=[]
 for k,f in old.items():
  nf=new.get(k);expected=f.get(':answer-field/correct',{}).get(':answer/value')
  av=next((a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]),None) if nf else None
  fields.append({'key':k,'present':nf is not None,'bank_equal':bool(nf) and sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in nf[':answer-field/choices']),'expected':expected,'actual':av,'correct':expected==av})
 source_results.append({'source_id':sid,'fields':fields,'status':'passed' if all(f['correct'] and f['bank_equal'] for f in fields) and len(old)==len(new) else 'failed','new_extra_keys':list(set(new)-set(old))})
errors=[]
for t in ['Z0+','Q0-']:
 try:g.generate(t,[g.number('integer',-5),g.number('integer',0),g.number('sqrt',1,3),g.number('fraction',1,3)])
 except Exception as ex:errors.append({'target':t,'exception':type(ex).__name__,'message':str(ex)})
# Radio source at supported Q0+ target still cannot replay through checkbox construction.
q=next(q for q in orig if q[':question/id']=='c620ed83-c013-5ff0-8983-14697bd50f1b')
try:g.generate('Q0+',[g.number('integer',0),g.number('sqrt',1,20),g.number('sqrt',-1,25),g.number('fraction',1,2)],replay=q)
except Exception as ex:errors.append({'source_id':q[':question/id'],'exception':type(ex).__name__,'message':str(ex)})
save('source-replay-checks.json',{'source_cases':source_results,'explicit_reproduction':errors,'canonical':'canonical four entries not exposed by replay interface; Q- same-method variations covered','limitations':'Source q-181542 lacks key/solution, so exact solution comparison is unavailable; omitted fully keyed radio q-80337/q-104686 have no such gap.'})
# Actual CLI deterministic/relocation/negative inputs, all copies written under evidence.
rel=E/'relocated';rel.mkdir(exist_ok=True)
for p in W.iterdir():
 if p.is_file():shutil.copy2(p,rel/p.name)
def run(args,root=W):return subprocess.run([PY,'-B',str(root/'generator.py')]+args,capture_output=True,text=True,cwd=E)
a=run(['--seed','711923','--count','5']);b=run(['--seed','711923','--count','5']);c=run(['--seed','711923','--count','5'],rel)
neg=[]
for args in [['--difficulty','hard'],['--count','-1'],['--count','0']]:
 rr=run(args);neg.append({'args':args,'returncode':rr.returncode,'stdout':rr.stdout,'stderr':rr.stderr})
save('packaging-checks.json',{'python_actual':platform.python_version(),'manifest':json.load(open(W/'package.json')),'deterministic':a.returncode==b.returncode==0 and a.stdout==b.stdout,'relocatable':a.stdout==c.stdout and c.returncode==0,'negative_and_boundary_cli':neg,'outputs':'JSON stdout only; no assets; no declared third-party dependencies','package_before':hashes()})
# Inspect captured inventory for demonstrated missing-radio-family weakness: generated records differ from missing practice capability.
inv=json.load(open(J/'source/inventory.json'))
save('inventory-review.json',{'basis':inv['basis'],'questions':len(inv['questions']),'source_ids':[q[':question/id'] for q in orig],'generated_candidates':[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'keys':list(q)} for q in inv['questions'] if q[':question/id'] not in {z[':question/id'] for z in orig}],'finding_applicability':'Omission of source families is a generator coverage defect, not an erroneous stored item. No generated stored question demonstrated affected. Original source radio questions are not marked generated.'})
save('affected-inventory.json',{'affected_questions':[]})
save('render-records.json',pairs+[controlled[0],batch[0],replay[0]])
(E/'session-state.md').write_text('Source analysis verified before package reads. Independent audit.py completed: 153 generated math checks; 80 controlled masks; 64 fresh seeded records; exact five runner records retained; native grader input prepared. Source replay omits three radio sources; explicit unsupported target and radio replay errors retained. No repair history/preflight/preparation present. Next: delivery filters, native grader, actual UI screenshots, decision report.\n')
print(json.dumps({'math_records':len(allrecords),'math_failures':len(fail),'source_status':Counter(r['status'] for r in source_results),'explicit_errors':errors,'coverage':metrics(batch)},indent=2))
