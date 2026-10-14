"""Replenish only this KP, with mathematical deduplication and guarded EDB writes."""
import copy, fcntl, hashlib, importlib.util, json, os, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database, QUESTION_PULL, StaleBasis
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('validator',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.m
KP=g.KP_ID; LEVELS=('easy','moderate','hard'); SOURCE=':application/ca-engine';LINEAGE=g.SOURCE['lineage']
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'3427a3f3eb72f6258a1950053d0da3226962d97d8a5eb0e2f8c538791fdb63d4'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE=max((ROOT/'.local/graph-explorer').glob('learning-*'),key=lambda p:p.stat().st_mtime_ns)
PATTERN='[* {:knowledge-point/question-generator [*]} {:knowledge-point/questions '+QUESTION_PULL+'} {:knowledge-point/canonical-example '+QUESTION_PULL+'}]'
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
(or-join [?q ?l]
(and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
(and [?l :learner/activity ?t] [?t :learner-task/status ?status]
(or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
[?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}\n',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def pull(path,basis):
 p=path/'kp-pattern.edn';p.write_text(PATTERN);t=DB.command('pull','--file',p,'--entity',KP,'--as-of',basis);(path/'kp.edn').write_text(t);return loads(t)
def normalize(q):
 out={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
 out[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);out[':question/answer-fields']=[]
 for f in q[':question/answer-fields']:
  out[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']}for a in f[':answer-field/choices']]})
 return ordered(out)
def ordered(q):
 q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
 for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
 return q
def fingerprint(q):
 math=v.MATH.search(q[':question/problem'])[0];poly=v.sp.cancel(v.equation(math)/v.Z)
 assert v.sp.degree(poly,v.X)==2
 # A root set is one factoring task even if base, scalar, field, bank or rearrangement changes.
 return tuple(str(r) for r in sorted(v.sp.solve(poly,v.X)))
def independent(r):
 v.actual_display(r)
 again=g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=r['generation']['seed'],template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile'])
 assert ordered(again['question'])==ordered(r['question']) and again['generation']==r['generation']
 # Seed replay exercises the sampler too; explicit parameter replay can consume
 # a different amount of randomness before the incidental option shuffle.
 sampled=g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=r['generation']['seed'])
 if sampled['generation']['template']==r['generation']['template'] and sampled['generation']['parameters']==r['generation']['parameters'] and sampled['generation']['profile']==r['generation']['profile']:
  assert sampled==r
 for f in r['question'][':question/answer-fields']:
  uuid.UUID(f[':answer-field/id'])
  for a in f[':answer-field/choices']:uuid.UUID(a[':answer/id'])
def grade(records,path,name):
 save(path/(name+'-input.json'),[v.fixtures(r,r['question'][':question/id'])for r in records])
 subprocess.run([str(HERE/'check-current-engine'),str(path/(name+'-input.json')),str(path/(name+'-report.json'))],check=True)
def counts(kp,path,basis):
 unavailable={r[0]for r in DB.query(USAGE,[KP,LEARNER],path,'unavailable',basis)}
 cases={c['source_id']:c for c in json.loads((HERE/'source-cases.json').read_text())};rows={l:[]for l in LEVELS};excluded=[];native=[]
 saved={r['question'][':question/id']:r for p in OUT.glob('basis-*/generated.json')for r in json.loads(p.read_text())}
 for q in kp[':knowledge-point/questions']:
  sid=q.get(':question/math-academy-id');lev=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]
  if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):continue
  if lev not in LEVELS:excluded.append({'source':sid,'reason':'Unrated original remains excluded and unchanged'});continue
  if sid=='q-264791':excluded.append({'source':sid,'reason':'Documented trailing plus in original solution; original preserved'});continue
  if sid in cases:
   c=cases[sid];r=g.generate(c['level'],seed=7,template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])
   r['question']=normalize(q);v.actual_display(r)
  else:
   r=saved[str(q[':question/id'])];assert normalize(q)==ordered(r['question']);independent(r)
  rows[lev].append(q);native.append(r)
 grade(native,path,'available-native')
 result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({fingerprint(q)for q in qs}),'question_ids':[str(q[':question/id'])for q in qs]}for l,qs in rows.items()},'unavailable_ids':sorted(unavailable),'excluded':excluded}
 save(path/'counts.json',result);return result

def transaction(records,kp,gid):
 forms=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id']for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id']for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 else:forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id']for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def check_report(report,path,source):
 attrs={eid:str(a)for eid,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,value,tx,s,added in report[':edb/tx-data']:
  assert s==source and added,'Unexpected attribution or retraction'
  if e==KP:assert attrs[a] in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif attrs[a]!=':db/txInstant':assert e in new and attrs[a] in allowed,'Unexpected content or learner mutation'

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,path/'receipt-check',intent['source_eid']);basis=report[':edb/db-after-t'];(path/'readback').mkdir(exist_ok=True);kp=pull(path/'readback',basis)
 before=loads((path/'kp.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items())
 assert {k:x for k,x in before.items()if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:x for k,x in kp.items()if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:assert normalize(byid[r['question'][':question/id']])==ordered(r['question']);independent(r)
 assert not transaction([],kp,intent['generator_id'])
 c=counts(kp,path/'readback',basis)
 verified={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'source_questions_preserved':len(old),'only_scoped_additive_datoms':True,'learner_history_preserved':True,'generator_registration_verified':True,'repeat_preparation_changes':0,'counts':c};save(path/'verification.json',verified);return verified

def finish(path,intent,verified):
 inv=inventory(path/'inventory-after.json');records=json.loads((path/'generated.json').read_text());missing={l:max(0,5-verified['counts']['levels'][l]['distinct_available_tasks'])for l in LEVELS}
 result={'outcome':'finite-limit' if any(missing.values())else 'generated','knowledgePoint':KP,'topic':17592186048423,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'verified_commit_basis':verified['basis_after'],'commit_basis_before':intent['basis'],'lineage':LINEAGE,'generated':{l:sum(r['question'][':question/difficulty'].endswith('/'+l)for r in records)for l in LEVELS},'supported_levels':list(LEVELS),'hard_authored':True,'available_after':{l:verified['counts']['levels'][l]['distinct_available_tasks']for l in LEVELS},'shortage_remaining':missing,'capability_exceptions':[],'unrated_originals_preserved':True,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs']if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT))for p in (path/'preparation.json',path/'generated.json',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'reference/engine-build.json')]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2))

def main():
 validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass' and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
 # Recheck inventory before any new sampling; this read never mutates learner state.
 inventory(OUT/'initial-inventory.json')
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a')as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  status=DB.command('status');assert 'lineage='+LINEAGE in status;(OUT/'locked-status.txt').write_text(status)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
    report=DB._commit(intent,path/'transaction.edn',path);finish(path,intent,verify(path,intent,report));return
  inv=inventory(OUT/'locked-inventory.json');basis=inv['basis'];assert DB.basis()==basis
  path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=pull(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
  captured=json.loads((HERE/'source.json').read_text())['record'];current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
  for q in captured[':knowledge-point/questions']:assert current[q[':question/math-academy-id']][':question/problem']==q[':question/problem'],'Source prompt changed: reclassify'
  c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks'])for l in LEVELS}
  used={fingerprint(q)for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
  suppliedpath=JOB.with_suffix('.generated');supplied=json.loads(suppliedpath.read_text())if suppliedpath.exists()else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
  for r in instances:independent(r)
  save(path/'supplied-status.json',{'exists':suppliedpath.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
  records=[];added={l:0 for l in LEVELS}
  for r in instances:
   l=r['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(r['question'])
   if added[l]<needed[l] and fp not in used:records.append(r);used.add(fp);added[l]+=1
  for l in LEVELS:
   for i in range(250):
    if added[l]>=needed[l]:break
    r=g.generate(l,seed=int(JOB.name[:8],16)+i);fp=fingerprint(r['question'])
    if fp in used:continue
    independent(r);records.append(r);used.add(fp);added[l]+=1
  assert added==needed,'Bounded distinct sampling failed; document explicit remaining shortage'
  grade(records,path,'generated-native');save(path/'generated.json',records)
  (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r)for r in records))
  ids=[uuid.UUID(item[':'+kind+'/id'])for r in records for kind,item in [('question',r['question'])]+[('answer-field',f)for f in r['question'][':question/answer-fields']]+[('answer',a)for f in r['question'][':question/answer-fields']for a in f[':answer-field/choices']]]
  if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identities',basis)
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id'])if gen else g.uid('course-academy:question-generator:'+str(KP))
  if not gen:assert not DB.query('[:find ?e :in $ ?id :where [?e :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
  save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'counts_before':c,'needed':needed,'added':added,'deduplication':'Distinct real root sets across all originals and canonical example; seed, identity, options, base, scalar and response shape excluded','asset_hashes':[],'generator_sha256':sha(HERE.with_suffix('.py')),'source_basis':1356,'hard_scope':validation['authored_hard']})
  txpath=path/'transaction.edn';tx=dumps(transaction(records,kp,gid))+'\n'
  with txpath.open('w')as f:f.write(tx);f.flush();os.fsync(f.fileno())
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,check=True,capture_output=True,text=True,timeout=55);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
  assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'sha256':sha(txpath),'exact_edn':tx,'request_key':'ca-kp-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'generator_id':gid,'generator_path':SCRIPT,'question_uuids':[r['question'][':question/id']for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);finish(path,intent,verify(path,intent,report))
if __name__=='__main__':main()
