#!/usr/bin/env python3
"""KP-local preparation, serialized additive commit, receipt recovery and readback."""
import fcntl,hashlib,importlib.util,json,re,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];REF=HERE/'reference';REF.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture'),str(HERE)]
from database import Database,QUESTION_PULL
from core import atomic_json
from edn import dumps,loads,kw
from serve_graph_explorer import database_environment

def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=module('scalar_generator',HERE.with_suffix('.py'))
v=module('scalar_validation',HERE/'validate.py')
p=module('scalar_readback',ROOT/'generate/runs/current/scalar-line-parser.py')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math'))
SOURCE=':application/ca-engine';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
RESULT=ROOT/'.local/learning/inventory/math'/LEARNER/'61d577efef48c48d783d221f54af1b6d40826b5fe698beac9215f584c17a5dfa.result'
PATTERN='[* {:knowledge-point/question-generator [*]} {:knowledge-point/questions '+QUESTION_PULL+'} {:knowledge-point/canonical-example '+QUESTION_PULL+'}]'

def save(name,obj):atomic_json(REF/name,obj)
def inventory(name):
 b=(REF/'learning-binary.txt').read_text().strip()
 r=subprocess.run([b,'math',LEARNER,'/tmp/edb-math/writer.sock'],input=json.dumps({'action':'inventory'}),env=database_environment('math'),capture_output=True,text=True,check=True,timeout=60)
 d=json.loads(r.stdout);assert d['ok'],d;d=d['data'];assert d['lineage']==LINEAGE;save(name,d);return d

def pull(basis,name):
 path=REF/'pull.edn';path.write_text(PATTERN)
 text=DB.command('pull','--file',path,'--entity',g.KP_ID,'--as-of',basis);(REF/name).write_text(text);return loads(text)

def task(q):
 d=p.prompt(q[':question/problem'])
 return d

def same_task(a,b):
 return p.equal(a[0],b[0]) and p.equal(a[1],b[1]) and all(p.equal(x,y) for x,y in zip(a[3],b[3]))

def validate_batch(records):
 checks=[];counts=[]
 for r in records:
  n=v.validate_record(r);q=r['question'];d=task(q);c,answer=p.stages(q[':question/worked-solution'],d,with_value=True)
  f=q[':question/answer-fields'][0];correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert p.equal(p.scalar(correct[':answer/value']),answer)
  checks.append({'label':q[':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'full field-owned radio bank'} for a in f[':answer-field/choices']]})
  counts.append({'question':q[':question/id'],'printed_stage_checks':n,'independent_readback':c})
 save('selected-engine-input.json',checks)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(REF/'selected-engine-input.json'),str(REF/'selected-engine-report.json')],check=True,capture_output=True,text=True)
 save('selected-validation.json',{'passed':True,'records':counts,'native_checks':5*len(records),'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'sympy':g.sp.__version__})

def typed(v,key=None):
 if isinstance(v,dict):return {kw(k):typed(x,k) for k,x in v.items()}
 if isinstance(v,list):return [typed(x) for x in v]
 if isinstance(v,str) and v.startswith(':'):return kw(v)
 if isinstance(v,str) and re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}',v):return uuid.UUID(v)
 return v

def forms_for(records,gid):
 forms=[]
 for r in records:
  q=r['question'];qref='q-'+q[':question/id'];t=typed(q);t[kw('db/id')]=qref
  for f,tf in zip(q[':question/answer-fields'],t[kw('question/answer-fields')]):
   tf[kw('db/id')]='f-'+f[':answer-field/id']
   for a,ta in zip(f[':answer-field/choices'],tf[kw('answer-field/choices')]):ta[kw('db/id')]='a-'+a[':answer/id']
   tf[kw('answer-field/correct')]='a-'+f[':answer-field/correct'][1]
  forms += [t,[kw('db/add'),g.KP_ID,kw('knowledge-point/questions'),qref],[kw('db/ensure'),qref,kw('question/validate')]]
  for f in q[':question/answer-fields']:
   forms.append([kw('db/ensure'),'f-'+f[':answer-field/id'],kw('answer-field/validate')])
   forms += [[kw('db/ensure'),'a-'+a[':answer/id'],kw('answer/validate')] for a in f[':answer-field/choices']]
 forms += [{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),g.KP_ID,kw('knowledge-point/question-generator'),'generator'],[kw('db/ensure'),g.KP_ID,kw('knowledge-point/validate')]]
 return forms

def verify(intent,receipt):
 assert receipt[':edb/committed'] is True;assert receipt[':edb/db-before-t']==intent['basis'];after=receipt[':edb/db-after-t']
 attrs=dict(DB.attributes(REF/'verification',after))
 allowed={'question/id','question/problem','question/worked-solution','question/difficulty','question/answer-fields','answer-field/id','answer-field/key','answer-field/type','answer-field/choices','answer-field/correct','answer/id','answer/type','answer/value','knowledge-point/questions','knowledge-point/question-generator','question-generator/id','question-generator/script','db/txInstant'}
 for row in receipt[':edb/tx-data']:
  a=str(attrs[row[1]])[1:];assert a in allowed,(a,row);assert row[-1] is True and row[-2]==intent['source_entity'],row
  if a.startswith('knowledge-point/'):assert row[0]==g.KP_ID
 old=loads((REF/'before.edn').read_text());now=pull(after,'readback.edn')
 oldq={str(q[':question/id']):q for q in old[':knowledge-point/questions']};newq={str(q[':question/id']):q for q in now[':knowledge-point/questions']}
 assert all(newq[k]==q for k,q in oldq.items());assert old[':knowledge-point/canonical-example']==now[':knowledge-point/canonical-example']
 assert set(newq)==set(oldq)|{r['question'][':question/id'] for r in intent['records']}
 reg=now[':knowledge-point/question-generator'];assert str(reg[':question-generator/id'])==intent['generator_id'] and reg[':question-generator/script']==SCRIPT
 for r in intent['records']:
  q=r['question'];a=newq[q[':question/id']];assert ':question/math-academy-id' not in a
  for k in (':question/problem',':question/worked-solution'):assert a[k]==q[k]
  assert a[':question/difficulty'][':db/ident']==q[':question/difficulty'];assert len(a[':question/answer-fields'])==len(q[':question/answer-fields'])
  for f,af in zip(q[':question/answer-fields'],a[':question/answer-fields']):
   assert str(af[':answer-field/id'])==f[':answer-field/id'] and af[':answer-field/key']==f[':answer-field/key'] and af[':answer-field/type'][':db/ident']==f[':answer-field/type']
   assert str(af[':answer-field/correct'][':answer/id'])==f[':answer-field/correct'][1]
   expected={x[':answer/id']:(x[':answer/type'],x[':answer/value']) for x in f[':answer-field/choices']};actual={str(x[':answer/id']):(x[':answer/type'][':db/ident'],x[':answer/value']) for x in af[':answer-field/choices']};assert actual==expected
 inv=inventory('inventory-after.json');jobs=[j for j in inv['jobs'] if j['knowledgePoint']==g.KP_ID];assert not jobs,jobs
 assert all(any(same_task(task(r['question']),task(q)) for q in newq.values()) for r in intent['records'])
 generated={l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in intent['records']) for l in ('easy','moderate','hard')}
 out={'outcome':'generated','knowledgePoint':g.KP_ID,'topic':17592186048645,'database':'math','lineage':LINEAGE,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'verified_commit_basis':after,'commit_basis_before':intent['basis'],'generated':generated,'available':{l:5 for l in generated},'remaining_shortages':jobs,'capability_exceptions':[],'source_questions_and_history_preserved':True,'learner_or_engine_facts_changed':False,'repeat_preparation_content_changes':0,'evidence':[str((REF/n).relative_to(ROOT)) for n in ('preparation.json','selected-validation.json','selected-engine-report.json','transaction.edn','preview.edn','commit-intent.json','commit.edn','readback.edn','inventory-after.json')]}
 save('verification.json',out);atomic_json(RESULT,out);print(json.dumps(out,indent=2))

def main():
 assert json.loads((HERE/'validation.json').read_text())['passed']
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT),threading.Event())
 # Recover the identical saved request before deciding on any new content.
 intentpath=REF/'commit-intent.json';txpath=REF/'transaction.edn';receiptpath=REF/'commit.edn'
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  status=DB.command('status');assert 'lineage='+LINEAGE in status;(REF/'locked-status.txt').write_text(status)
  if intentpath.exists():
   intent=json.loads(intentpath.read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE
   assert txpath.read_text()==intent['exact_edn'] and hashlib.sha256(txpath.read_bytes()).hexdigest()==intent['sha256']
  else:
   inv=inventory('inventory-locked-before.json');basis=inv['basis'];assert DB.basis()==basis
   old=pull(basis,'before.edn');jobs=[j for j in inv['jobs'] if j['knowledgePoint']==g.KP_ID];missing={l:next((j['missing'] for j in jobs if j['difficulty']==l),0) for l in ('easy','moderate','hard')}
   if any(j['difficulty']=='unclassified' for j in jobs):missing['easy']=5
   assert missing=={'easy':5,'moderate':2,'hard':1},missing
   # Every candidate changes the displayed mathematical task, not just its bank.
   specs=[('easy','easy_linear',{'m':m,'c':c,'b':b}) for m,c,b in [(2,1,3),(3,2,4),(4,3,5),(5,4,6),(6,5,7)]]+[('moderate','line_product',{'b':'2'}),('moderate','line_polynomial',{'b':'2'}),('hard','exponential',{'n':4})]
   records=[g.generate(l,seed=52158+i,template=t,parameters=p) for i,(l,t,p) in enumerate(specs)]
   tasks=[task(q) for q in old[':knowledge-point/questions']]+[task(old[':knowledge-point/canonical-example'])]
   for r in records:
    d=task(r['question']);assert not any(same_task(d,x) for x in tasks),'Duplicate mathematical task';tasks.append(d)
   validate_batch(records);save('generated.json',records);(REF/'generated.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records))
   source=DB.query('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]',[kw(SOURCE)],REF,'contributor',basis);assert len(source)==1
   reg=old.get(':knowledge-point/question-generator');gid=str(reg[':question-generator/id']) if reg else g.GENERATOR_ID
   if reg:assert reg.get(':question-generator/script') in (None,SCRIPT)
   txpath.write_text(dumps(forms_for(records,gid))+'\n');sha=hashlib.sha256(txpath.read_bytes()).hexdigest()
   save('preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'missing':missing,'records':records,'plots':[],'source_records_preserved':True,'duplicate_mathematical_tasks':0})
   r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=60);(REF/'preview.edn').write_text(r.stdout);assert loads(r.stdout)[':edb/db-before-t']==basis
   intent={'database':'math','endpoint':'/tmp/edb-math/writer.sock','lineage':LINEAGE,'basis':basis,'sha256':sha,'exact_edn':txpath.read_text(),'source':SOURCE,'source_entity':source[0][0],'request_key':'ca-kp-17592186152158-'+str(basis)+'-'+sha,'generator_id':gid,'records':records};save('commit-intent.json',intent)
  if receiptpath.exists() and loads(receiptpath.read_text()).get(':edb/committed') is True:receipt=loads(receiptpath.read_text())
  else:
   text=DB.command('transact','--file',txpath,'--endpoint',intent['endpoint'],'--source',intent['source'],'--request-key',intent['request_key'],'--basis',intent['basis'],'--timeout-ms',55000);receiptpath.write_text(text);receipt=loads(text)
  verify(intent,receipt)
if __name__=='__main__':main()
