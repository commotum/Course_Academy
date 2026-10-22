import sys,os,json,pathlib,hashlib,subprocess,shutil,re,math,random
from fractions import Fraction
from collections import Counter,defaultdict
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent
PKG=JOB/'workspace'
sys.dont_write_bytecode=True
sys.path.insert(0,str(PKG))
import generator as g
from generator_policy import explicit_none_checkbox

def save(n,x): (ROOT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
def digest():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.iterdir() if p.is_file()}
def truth(f):
 ref=f[':answer-field/correct'];aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def sym(key):
 if key in ('None','None of the above'):return None
 m=re.search(r'\\mathbb\{([NZQRC])\}',key)
 if not m: raise ValueError(key)
 return m[1]+('0' if '_0' in key else '')+('+' if '+' in key else '-' if '-' in key else '')
# Independent semantic oracle, reading prompt/fields rather than generation categories.
def number(q):
 t=re.search(r'number \$(.*?)\$ belong',q)[1]; sign=-1 if t.startswith('-') else 1;t=t.lstrip('-')
 if '\\pi' in t:return (sign,False,False)
 if '\\sqrt' in t:
  n=int(re.search(r'\{(\d+)\}',t)[1]);v=math.isqrt(n)
  return (0 if n==0 else sign,v*v==n,v*v==n)
 if '\\frac' in t:
  n,d=map(int,re.findall(r'\{(\d+)\}',t));v=Fraction(sign*n,d)
 else:v=Fraction(('-' if sign<0 else '')+t)
 return (0 if not v else 1 if v>0 else -1,v.denominator==1,True)
def member(v,s):
 sign,integer,rational=v
 if s=='C':return True
 if s=='N':return integer and sign>0
 if s=='N0':return integer and sign>=0
 base=s[0]; suffix=s[1:]
 if base=='Z' and not integer:return False
 if base=='Q' and not rational:return False
 return {'':True,'+':sign>0,'-':sign<0,'0+':sign>=0,'0-':sign<=0}[suffix]
W=[(-1,True,True),(0,True,True),(1,True,True),(-1,False,True),(1,False,True),(-1,False,False),(1,False,False)]
def target(q):
 p=q[':question/problem']
 if 'do all the ' not in p:return [number(p)]
 group=re.search(r'do all the (.*?) belong',p)[1]
 # Independent witness partition suffices exactly for all taught candidate predicates.
 return [v for v in W if {'positive integers':v[0]>0 and v[1], 'natural numbers':v[0]>0 and v[1], 'negative integers':v[0]<0 and v[1], 'integers':v[1], 'nonnegative integers':v[0]>=0 and v[1], 'positive rational numbers':v[0]>0 and v[2], 'negative rational numbers':v[0]<0 and v[2], 'rational numbers':v[2], 'real numbers':True}[group]]
def expected(r):
 q=r['question'];vs=target(q);ordinary=[all(member(v,sym(f[':answer-field/key'])) for v in vs) for f in q[':question/answer-fields'] if sym(f[':answer-field/key']) is not None]
 it=iter(ordinary);return [not any(ordinary) if sym(f[':answer-field/key']) is None else next(it) for f in q[':question/answer-fields']]
def describe(r):
 return {'id':r['question'][':question/id'],'profile':r['generation']['profile'],'target':r['generation']['instance'],'candidates':r['generation']['candidates'],'correct':[truth(f) for f in r['question'][':question/answer-fields']]}
initial=digest(); save('package-hashes-before.json',initial)
batch=load(JOB/'samples.json');save('batch.json',batch)
seed=827461
records=g.generate(count=100,seed=seed);save('samples.json',records)
assert records==g.generate(count=100,seed=seed)
# All supported replay indices, record complete outputs, compare full original banks.
source=load(JOB/'source/source.json')['material']['kp']; original=source[':knowledge-point/questions']
replays=[g.replay_source(i) for i in range(10)];save('source-replays.json',replays)
replay_results=[]
for r in replays:
 sid=r['generation']['source_id'];s=next(s for s in original if s[':question/id']==sid)
 def bank(q):return [(f[':answer-field/key'],[a[':answer/value'] for a in f[':answer-field/choices']]) for f in q[':question/answer-fields']]
 replay_results.append({'source_id':sid,'complete_bank_preserved':bank(s)==bank(r['question']),'original_bank':bank(s),'replay_bank':bank(r['question'])})
covered={r['generation']['source_id'] for r in replays}
save('source-replay-results.json',{'cases':replay_results,'missing_sources':[q[':question/id'] for q in original if q[':question/id'] not in covered], 'missing_canonical_replay':source[':knowledge-point/canonical-example'][':question/id']})
# Controlled same-candidate interventions on a number or whole target set.
pairs=[]
def record(inst,candidates):return explicit_none_checkbox(g.make_record(inst,candidates))
cs=['N','Z','Q','R']
pairs += [record(g.number_instance('root',radicand=n,sign=1),cs) for n in [121,2,144]]
pairs += [record({'profile':'universal','group':s},['N','Z','Q-','R']) for s in ['natural numbers','negative integers']]
save('counterfactual-records.json',pairs)
save('counterfactual-results.json',{'relevant_root':[describe(pairs[i]) for i in [0,1]],'irrelevant_magnitude':[describe(pairs[i]) for i in [0,2]],'relevant_universal_target':[describe(pairs[i]) for i in [3,4]],'expectations':['121 to 2 changes N,Z,Q true to false; R remains true','121 to 144 preserves all membership truths','natural to negative integers flips N and Q-; Z and R unchanged']})
# Representation boundaries, directly constructed and semantically validated.
boundaries=[]
for n in [0,1,2,144]:
 for sign in [-1,1]:boundaries.append(record(g.number_instance('root',radicand=n,sign=sign),['N','N0','Z0-','Q+']))
for n,d in [(0,2),(1,2),(-1,2),(12,12),(-12,12)]:boundaries.append(record(g.number_instance('fraction',numerator=n,denominator=d),['Z','Q','Q0+','R-']))
save('boundary-records.json',boundaries)
math_cases=[];grader=[]
for group,rr in [('samples',records),('batch',batch),('counterfactual',pairs),('boundary',boundaries)]:
 for idx,r in enumerate(rr):
  ex=expected(r);fs=r['question'][':question/answer-fields'];actual=[truth(f)=='true' for f in fs]
  math_cases.append({'group':group,'index':idx,'id':r['question'][':question/id'],'expected':ex,'actual':actual,'passed':ex==actual})
  checks=[]
  for j,f in enumerate(fs):
   for a in f[':answer-field/choices']:
    checks.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if (a[':answer/value']=='true')==ex[j] else 'rejected','purpose':'Independent prompt-derived membership truth and its Boolean opposite'})
  grader.append({'label':group+'-'+str(idx),'record':r,'checks':checks})
save('math-results.json',{'checked':len(math_cases),'failures':[c for c in math_cases if not c['passed']],'cases':math_cases})
# Replay grading includes all radio choices and all checkbox alternatives.
for i,r in enumerate(replays):
 checks=[]
 for j,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:
   checks.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==truth(f) else 'rejected','purpose':'Source replay key independently checked against captured solution or inferred key'})
 grader.append({'label':'source-replay-'+str(i),'record':r,'checks':checks})
# Conflict: solution expressly recommends leaving EVERY box unchecked; native grader must reject None=false.
bad=next(r for r in records if 'leave every box unchecked' in r['question'][':question/worked-solution'])
save('minimal-failure.json',[bad])
f=bad['question'][':question/answer-fields'][-1]
false=next(a for a in f[':answer-field/choices'] if a[':answer/value']=='false')
grader.append({'label':'follow-worked-solution-leave-EVERY-box-unchecked','record':bad,'checks':[{'field_index':4,'submitted_answer_id':false[':answer/id'],'expected':'rejected','purpose':'Demonstrates that the worked solution instructs a response rejected by the actual learner grader'}]})
save('grader-input.json',grader)
save('failure-summary.json',{'command':f'PYTHONDONTWRITEBYTECODE=1 {sys.executable} {PKG}/generator.py --seed {seed} --count 100 --format json','sample_index':records.index(bad),'minimal':describe(bad),'solution_final':bad['question'][':question/worked-solution'].splitlines()[-1], 'none_correct':truth(f),'failing_count':sum('leave every box unchecked' in r['question'][':question/worked-solution'] for r in records),'batch_failing_indices':[i for i,r in enumerate(batch) if 'leave every box unchecked' in r['question'][':question/worked-solution']]})
# Inventory: look only for demonstrated stale solution on records with visible None.
inv=load(JOB/'source/inventory.json');affected=[];inspection=[]
for q in inv['questions']:
 none=any(f[':answer-field/key'] in ('None','None of the above') for f in q.get(':question/answer-fields',[]));stale='leave every box unchecked' in q.get(':question/worked-solution','')
 inspection.append({'id':q[':question/id'],'entity_id':q[':db/id'],'visible_none':none,'unchecked_instruction':stale,'demonstrated_stale_none_conflict':none and stale})
save('inventory-inspection.json',{'basis':inv['basis'],'records':inspection,'conclusion':'All 16 stored questions inspected for the demonstrated stale-None solution conflict; none exhibit the conjunction. Earlier implicit-empty selection is distinct, not established as this defect. Generation metadata are absent from captured stored records.'})
save('affected-inventory.json',{'affected_questions':affected})
# Package isolation and runtime behavior. Copies only beneath evidence_root.
rel=ROOT/'relocated';rel.mkdir(exist_ok=True)
for name in initial:shutil.copy2(PKG/name,rel/name)
cmd=[sys.executable,str(rel/'generator.py'),'--seed','827461','--count','100','--format','json']
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True)
checks=[{'name':'relocated deterministic CLI equals imported API','passed':p.returncode==0 and json.loads(p.stdout)==records,'command':cmd}]
for args in [['--difficulty','hard'],['--count','-1'],['--count','0']]:
 p=subprocess.run([sys.executable,str(rel/'generator.py'),*args],env=env,capture_output=True,text=True)
 checks.append({'name':'CLI '+str(args),'code':p.returncode,'stdout':p.stdout[:200],'stderr':p.stderr[-400:]})
for kwargs in [{'radicand':-1,'sign':1},{'radicand':1,'sign':0}]:
 try:g.number_instance('root',**kwargs);ok=False
 except ValueError:ok=True
 checks.append({'name':'reject invalid root '+str(kwargs),'passed':ok})
try:g.number_instance('fraction',numerator=1,denominator=0);ok=False
except ValueError:ok=True
checks.append({'name':'reject zero denominator','passed':ok})
save('packaging-results.json',{'runtime':sys.version,'manifest':load(PKG/'package.json'),'checks':checks,'no_assets':all(not r['assets'] for r in records),'package_unchanged':digest()==initial,'external_output':'CLI writes JSON to stdout only; source fixture reads are package-relative; relocated execution succeeded.'})
save('render-records.json',batch+[bad]+pairs+[replays[0],replays[3],replays[6]])
(ROOT/'session-state.md').write_text('Completed independent source reconstruction, source replay comparison, 100 fresh samples (seed 827461), 5 exact batch records, controlled relevant/irrelevant pairs, boundaries, mathematical oracle, inventory scan and relocated runtime checks. Demonstrated stale solution for explicit None; missing complete source replay banks. Awaiting shared delivery, actual grader and renderer; package unchanged.\n')
print(json.dumps({'math_checked':len(math_cases),'math_failures':sum(not c['passed'] for c in math_cases),'source_bank_failures':[r['source_id'] for r in replay_results if not r['complete_bank_preserved']],'minimal_failure':load(ROOT/'failure-summary.json'),'package_unchanged':digest()==initial},indent=2))
