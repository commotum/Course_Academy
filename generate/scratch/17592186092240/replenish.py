"""Requested-KP-only additive commit, serialized with the application."""
import copy,fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from db_support import DB,KP,read,dumps,loads,kw,plain
sys.path.insert(0,str(ROOT/'scripts'))
from serve_graph_explorer import build_learning,database_environment
from inventory_jobs import save
spec=importlib.util.spec_from_file_location('validate',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';SOURCE=':application/ca-engine'
SCRIPT=str(H.with_suffix('.py').relative_to(ROOT));OUT=H/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'ff60d30ca04b04ca856b8a87c47a3d9796c0303d13a302294801ad90397ffef3'
LOCK=ROOT/'.local/learning/requests/math/api.lock'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):
 if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
 if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
 return str(x) if isinstance(x,uuid.UUID) else x
def inventory(native,path):
 p=subprocess.run([str(native),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=55)
 r=json.loads(p.stdout);assert r['ok'];x=r['data'];assert x['lineage']==LINEAGE;save(path,x);return x
def known_records():
 out={r['question'][':question/id']:r for r in json.loads((H/'source-replay.json').read_text())}
 for path in OUT.glob('basis-*/generated.json'):
  for r in json.loads(path.read_text()):out[r['question'][':question/id']]=r
 return out
KNOWN=known_records()
def fingerprint(q):
 sid=q.get(':question/math-academy-id')
 if sid in g.CONFIG:
  c=g.CONFIG[sid];return g.generate('moderate',0,profile=sid,parameters={'scale':'1','point':c['point']})['generation']['mathematical_key']
 r=KNOWN.get(str(q.get(':question/id')))
 return r['generation']['mathematical_key'] if r else None
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''
def counts(kp,path,basis):
 shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
 reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
 out={level:set() for level in ['easy','moderate','hard']};excluded=[]
 captured=loads((H/'source.edn').read_text());source={q[':db/id']:q for q in captured[':knowledge-point/questions']}
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] in shown|reserved:continue
  sid=q.get(':question/math-academy-id');key=fingerprint(q)
  if key is None:
   excluded.append({'question_id':str(q[':question/id']),'reason':'Excluded source template or unknown generated content; see capability.json'});continue
  if sid in g.CONFIG:
   assert canonical(q)==canonical(source[q[':db/id']]);c=g.CONFIG[sid]
   r=g.generate('moderate',0,profile=sid,parameters={'scale':'1','point':c['point']});v.check(r)
  else:
   r=KNOWN[str(q[':question/id'])];v.check(r);assert normalized(q)==canonical(r['question'])
  level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
  if level in out:out[level].add(key)
 result={'basis':basis,'distinct_available':{l:len(z) for l,z in out.items()},'shown_or_reserved':sorted(shown|reserved),'excluded':excluded};save(path/'available-counts.json',result);return result

def tx(records,kp):
 forms=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:
  assert str(gen[':question-generator/id'])==g.GENERATOR_ID and gen[':question-generator/script']==SCRIPT
 else:
  forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(g.GENERATOR_ID),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def report_checks(report,path,source):
 attrs={eid:str(a) for eid,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':answer/id',':answer/type',':answer/value',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':question-generator/id',':question-generator/script'}
 for e,a,value,t,s,added in report[':edb/tx-data']:
  assert added and s==source, 'Unexpected retraction or attribution'
  name=attrs[a]
  if e==KP:assert name in {':knowledge-point/questions',':knowledge-point/question-generator'}
  elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected non-scoped datom'

def normalized(q):
 x={k:str(q[k]) if k==':question/id' else q[k] for k in [':question/id',':question/problem',':question/worked-solution']};x[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);x[':question/answer-fields']=[]
 for f in q[':question/answer-fields']:
  x[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])]})
 return canonical(x)
def verify(report,path,intent):
 assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis'];b=report[':edb/db-after-t'];report_checks(report,path/'receipt-check',intent['source_eid'])
 before=loads((path/'before.edn').read_text());after=DB.query('[:find (pull ?k '+__import__('db_support').PATTERN+') :in $ ?k :where [?k :knowledge-point/id _]]',[KP],path/'readback','kp',b)[0][0]
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in after[':knowledge-point/questions']}
 assert all(canonical(q)==canonical(now[e]) for e,q in old.items())
 excluded={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert canonical({k:z for k,z in before.items() if k not in excluded})==canonical({k:z for k,z in after.items() if k not in excluded})
 gen=after[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q;assert normalized(q)==canonical(r['question']);assert fingerprint(q)==r['generation']['mathematical_key'];v.check(r)
 assert not tx([],after), 'Repeat preparation must be a content no-op'
 c=counts(after,path/'readback',b)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'distinct_available_after':c['distinct_available'],'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'no_retractions':True,'only_requested_kp_additive_content':True,'source':SOURCE,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
 save(path/'verification.json',result);return result

def finish(path,verified,inv):
 caps=json.loads((H/'capability.json').read_text());remaining={l:max(0,5-verified['distinct_available_after'][l]) for l in ['easy','moderate','hard']}
 result={'outcome':'finite-limit' if remaining['moderate'] else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':g.GENERATOR_ID,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':['moderate'],'available_after':verified['distinct_available_after'],'shortage_remaining':remaining,'capability_exceptions':caps['unsupported_levels'],'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [H/'validation.json',H/'classification.md',H/'template-extraction.md',H/'source-components.json',H/'source-bank-replay.json',H/'engine-report.json',H/'capability.json',path/'preparation.json',path/'transaction.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json'] if p.exists()],'note':'Moderate supported blank-template reserve verified. Easy/hard unsupported with nominal shortage five each. Radio profiles and incomplete/context-dependent originals excluded from this bounded generator; all originals and learner history preserved.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
 val=json.loads((H/'validation.json').read_text());assert val['passed'] and val['generator_sha256']==sha(H.with_suffix('.py')) and val['contract_sha256']==sha(H/'contract.json') and val['engine_sha256']==sha(H/'check-engine') and val['validation_sha256']==sha(H/'validate.py') and val['source_sha256']==sha(H/'source.edn')
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event());native=build_learning(ROOT.parent/'EDB')
 with LOCK.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  # Recover exact saved submission before any fresh planning or identity work.
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint and intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest() and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(report,path,intent);finish(path,verified,inventory(native,path/'inventory-after.json'));return
  inv=inventory(native,OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b and LINEAGE in DB.command('status')
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
  kp=read(b,'locked-source');assert str(kp[':knowledge-point/id'])==str(g.NAMESPACE)
  captured=loads((H/'source.edn').read_text());original={q[':db/id']:q for q in captured[':knowledge-point/questions']};current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
  assert all(canonical(q)==canonical(current[e]) for e,q in original.items()),'Source evidence changed; reclassify'
  assert canonical(captured[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
  (path/'before.edn').write_text(dumps(kp)+'\n')
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
  reg=kp.get(':knowledge-point/question-generator')
  if reg:assert str(reg[':question-generator/id'])==g.GENERATOR_ID and reg[':question-generator/script']==SCRIPT,'Existing identity requires reconciliation'
  counts_before=counts(kp,path,b);jobs={j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP};needed={l:max(0,5-counts_before['distinct_available'][l],jobs.get(l,{}).get('missing',0)) for l in ['moderate']}
  protocol=subprocess.run([str(ROOT/'.venv/bin/python'),str(H.with_suffix('.py')),'--difficulty','moderate','--count','1','--seed','421019372','--format','json'],capture_output=True,text=True,check=True)
  protocol_records=json.loads(protocol.stdout)
  for r in protocol_records:v.check(r)
  save(path/'generator-execution.json',{'command':[str(ROOT/'.venv/bin/python'),SCRIPT,'--difficulty','moderate','--count','1','--seed','421019372','--format','json'],'instances':protocol_records})
  used={fingerprint(q) for q in kp[':knowledge-point/questions']};records=[]
  historical=DB.query('[:find ?id :in $ ?kp :where [?kp :knowledge-point/questions ?q] [?q :question/id ?id]]',[KP],path,'historical-question-ids',b,history=True)
  historical_ids={str(row[0]) for row in historical}
  for qid,r in KNOWN.items():
   if qid in historical_ids:used.add(r['generation']['mathematical_key'])
  supplied=json.loads(JOB.with_suffix('.generated').read_text()) if JOB.with_suffix('.generated').exists() else {};instances=supplied.get('instances',[])
  if isinstance(instances,dict):instances=[instances]
  rejected=[]
  for r in instances:
   level=r['question'][':question/difficulty'].split('/')[-1]
   if level not in needed:rejected.append({'question':r['question'][':question/id'],'reason':'Unsupported level'});continue
   v.check(r);p=r['generation'];assert r==g.generate(level,p['seed'],profile=p['profile'],parameters=p['parameters'])
   key=p['mathematical_key']
   if needed[level]>0 and key not in used and r['question'][':question/id'] not in historical_ids:records.append(r);used.add(key);needed[level]-=1
  # Execute registered protocol for each currently missing supported band.
  generated_counts={l:0 for l in needed}
  for r in records:generated_counts[r['question'][':question/difficulty'].split('/')[-1]]+=1
  for level in needed:
   if not needed[level]:continue
   result=subprocess.run([str(ROOT/'.venv/bin/python'),str(H.with_suffix('.py')),'--difficulty',level,'--count',str(min(len(g.candidates(level)),needed[level]+len(used)+5)),'--seed','421019372','--format','json'],capture_output=True,text=True,check=True)
   for r in json.loads(result.stdout):
    v.check(r);key=r['generation']['mathematical_key']
    if key in used or r['question'][':question/id'] in historical_ids:continue
    records.append(r);used.add(key);needed[level]-=1;generated_counts[level]+=1
    if needed[level]==0:break
   # A bounded exhausted sampler leaves its explicit shortage in preparation/outcome.
  for attr,key,ids in [('question/id','q',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id','f',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id','a',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
   if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[ids],path,'identity-'+key,b),'Existing identity requires reconciliation'
  gid=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(g.GENERATOR_ID)],path,'generator-identity',b);assert not gid or len(gid)==1 and gid[0][0][':question-generator/script']==SCRIPT
  save(path/'generated.json',records);KNOWN.update({r['question'][':question/id']:r for r in records});save(path/'native-input.json',[v.engine_item(r['question'][':question/id'],r) for r in records])
  subprocess.run([str(H/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
  assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_evidence_unchanged':True,'available_before':counts_before,'new_by_level':generated_counts,'new_questions':len(records),'supported_shortage_remaining':needed,'supplied_generated_file_exists':JOB.with_suffix('.generated').exists(),'supplied_rejected':rejected,'distinct_mathematical_tasks':len({r['generation']['mathematical_key'] for r in records}),'generator_version':g.VERSION,'generator_sha256':sha(H.with_suffix('.py')),'asset_hashes':[]})
  forms=tx(records,kp)
  if not forms:
   finish(path,{'basis_after':b,'new_questions':0,'distinct_available_after':counts_before['distinct_available']},inv);return
  txpath=path/'transaction.edn';text=dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(text);f.flush();os.fsync(f.fileno())
  result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  (path/'preview.edn').write_text(result.stdout);pr=loads(result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;report_checks(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','lineage':LINEAGE,'endpoint':DB.args.endpoint,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'sha256':sha(txpath),'exact_edn':text,'request_key':'normal-line-replenish-'+str(b)+'-'+sha(txpath),'generator_id':g.GENERATOR_ID,'generator_path':SCRIPT,'generator_sha256':sha(H.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()}
  (path/'generator-at-commit.py').write_bytes(H.with_suffix('.py').read_bytes());(path/'contract-at-commit.json').write_bytes((H/'contract.json').read_bytes())
  save(path/'commit-intent.json',intent)
  report=DB._commit(intent,txpath,path);verified=verify(report,path,intent);finish(path,verified,inventory(native,path/'inventory-after.json'))
if __name__=='__main__':main()
