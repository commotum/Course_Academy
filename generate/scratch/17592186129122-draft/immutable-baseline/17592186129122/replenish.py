"""Scoped additive inventory preparation, exact EDB commit and readback for period KP."""
import copy, fcntl, hashlib, importlib.util, json, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.storage import atomic_json as save, atomic_text
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database, QUESTION_PULL
from edn import dumps, loads, kw
from serve_graph_explorer import database_environment
# Load reusable independent mathematics reader without running its full suite again.
v=SimpleNamespace(); ns={'__file__':str(HERE/'validate.py')};exec(compile((HERE/'validate.py').read_text().split('\nsources=g.CAPTURE')[0],str(HERE/'validate.py'),'exec'),ns);v=SimpleNamespace(**ns);g=v.g
KP=g.KP['db_id']; LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.CAPTURE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT)); LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'32817af42885d348e2b0c94a43939747edd3ed011be2cd9d1aae3b349aceded1'
OUT=HERE/'reference/replenishment'
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE=max((p for p in (ROOT/'.local/graph-explorer').glob('learning-*') if p.is_file() and p.stat().st_mode&0o111),key=lambda p:p.stat().st_mtime)
QUERY='[:find (pull ?k [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?k :where [?k :knowledge-point/id _]]'
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] (or-join [?q ?l] (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]) (and [?l :learner/activity ?t] [?t :learner-task/status ?s] (or [?s :db/ident :learner-task.status/started] [?s :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(p):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,text=True,capture_output=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']
def read_kp(p,b):
 rows=DB.query(QUERY,[KP],p,'kp',b);assert len(rows)==1 and str(rows[0][0][':knowledge-point/id'])==g.KP['id'];return rows[0][0]
def enum(x):return str(x.get(':db/ident')) if isinstance(x,dict) else str(x)
def ordered(q):
 q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
 for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
 return q
def normalize(q):
 result={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')};result[':question/difficulty']=enum(q[':question/difficulty']);result[':question/answer-fields']=[]
 for f in sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']):
  result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':enum(f[':answer-field/type']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':enum(a[':answer/type']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/value'])})
 return result
def signature(q):
 fs=[]
 for f in q.get(':question/answer-fields',[]):
  fs.append((f[':answer-field/key'],enum(f[':answer-field/type']),f.get(':answer-field/correct',{}).get(':answer/value'),sorted((enum(a[':answer/type']),a[':answer/value']) for a in f.get(':answer-field/choices',[]))))
 return (q[':question/problem'],q.get(':question/worked-solution'),enum(q.get(':question/difficulty')),sorted(fs))
def task(q):
 freq,period,unit,*_=v.prompt_math(q);level=enum(q.get(':question/difficulty')).split('/')[-1];return (level,unit,str(freq))
def check(rec):
 assert rec['knowledge_point']==g.KP and rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only'];v.verify(rec)
 p=rec['generation'];replay=g.generate(rec['question'][':question/difficulty'].split('/')[-1],p['seed'],p['template'],parameters=p['parameters'],profile=p['bank_profile'])
 assert ordered(rec['question'])==ordered(replay['question']);return task(rec['question'])
def native(records,p):
 fixtures=[]
 for i,r in enumerate(records):
  f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
  fixtures.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'independent mathematical key and actual application radio grader'} for a in f[':answer-field/choices']]})
 save(p/'native-input.json',fixtures);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(p/'native-input.json'),str(p/'native-report.json')],check=True)
 report=json.loads((p/'native-report.json').read_text());assert report['accepted_checks']==len(records) and report['rejected_checks']==4*len(records) and not report['documented_unresolved_checks']
def counts(kp,p,b):
 unavailable={r[0] for r in DB.query(USAGE,[KP,LEARNER],p,'unavailable',b)};unavailable.update(r[0] for r in DB.query(USAGE,[KP,LEARNER],p,'historical-unavailable',b,history=True))
 fresh={l:set() for l in g.LEVELS};excluded=[];valid=[]
 for q in kp[':knowledge-point/questions']:
  sid=q.get(':question/math-academy-id');level=enum(q.get(':question/difficulty')).split('/')[-1]
  if level not in fresh or not q.get(':question/answer-fields') or not q.get(':question/worked-solution') or sid=='q-43411':excluded.append({'question':sid or str(q[':question/id']),'reason':'unrated/incomplete or documented false source teaching rule'});continue
  clean=normalize(q);freq,_,unit,*_=v.prompt_math(clean)
  rec={'knowledge_point':g.KP,'question':clean,'generation':{'frequency':str(freq),'unit':unit,'evidence_only':bool(sid),'source_ids':[sid] if sid else [],'template':'source' if sid else 'registered'}};v.verify(rec);valid.append(rec)
  if q[':db/id'] not in unavailable and not q.get(':knowledge-point/_canonical-example'):fresh[level].add(task(q))
 native(valid,p)
 result={'basis':b,'distinct_available':{l:len(s) for l,s in fresh.items()},'shortage':{l:max(0,5-len(s)) for l,s in fresh.items()},'excluded_shown_or_reserved':sorted(unavailable),'excluded_invalid_sources':excluded};save(p/'available-counts.json',result);return result

def transaction(records,kp,gid):
 forms=[]
 for rec in records:
  q=rec['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen is None:forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def check_report(report,p,source):
 attrs={e:str(a) for e,a in DB.attributes(p,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,value,tx,s,added in report[':edb/tx-data']:
  assert s==source and added,'Unexpected attribution or retraction';name=attrs[a]
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,name

def verify(p,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_report(report,p/'receipt-check',intent['source_eid']);after=report[':edb/db-after-t'];kp=read_kp(p/'readback',after);before=loads((p/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']};assert all(now[e]==q for e,q in old.items())
 assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for rec in records:
  q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q;assert normalize(q)==ordered(rec['question']);check(rec)
 assert not transaction([],kp,intent['generator_id'])
 result={'passed':True,'basis_before':intent['basis'],'basis_after':after,'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in g.LEVELS},'unchanged_source_questions':len(old),'canonical_unchanged':True,'only_scoped_additive_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0};save(p/'verification.json',result);return result

def finish(p,gid,verified):
 available=counts(read_kp(p/'final-counts',verified['basis_after']),p/'final-counts',verified['basis_after']);inv=inventory(p/'inventory-after.json')
 result={'outcome':'generated' if not any(available['shortage'].values()) else 'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'verified_commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'generated_by_level':verified.get('by_level',{}),'supported_levels':list(g.LEVELS),'unsupported_levels':[],'available_counts':available['distinct_available'],'remaining_shortage':available['shortage'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(x.relative_to(ROOT)) for x in (p/'commit-intent.json',p/'transaction.edn',p/'preview.edn',p/'commit.edn',p/'verification.json',p/'preparation.json',p/'inventory-after.json',p/'final-counts/available-counts.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'capabilities.json')]}
 save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
 val=json.loads((HERE/'validation.json').read_text());assert val['status']=='pass';assert all(sha(ROOT/p)==h for p,h in val['hashes'].items())
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Waiting for application lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application lock acquired',flush=True)
  for p in sorted(OUT.glob('basis-*')):
   if (p/'commit-intent.json').exists():
    intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(p/'transaction.edn').read_text() and intent['sha256']==sha(p/'transaction.edn');assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    finish(p,intent['generator_id'],verify(p,intent,DB._commit(intent,p/'transaction.edn',p)));return
  inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(parents=True,exist_ok=True);kp=read_kp(p,b);atomic_text(p/'before.edn',dumps(kp)+'\n')
  expected={q[':question/math-academy-id']:q for q in g.CAPTURE['record'][':knowledge-point/questions']};now={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']};assert all(signature(q)==signature(now[sid]) for sid,q in expected.items()),'Source changed: reclassify'
  available=counts(kp,p,b);gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:question-generator:'+g.KP['id']))
  contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'contributor',b);assert len(contributor)==1
  existing=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],p,'generator-identity',b);assert not existing or len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT
  used={task(q) for q in kp[':knowledge-point/questions']};used.add(('easy',*task(kp[':knowledge-point/canonical-example'])[1:]));records=[];per={l:0 for l in g.LEVELS}
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
  for rec in instances:
   fp=check(rec);level=fp[0]
   if per[level]<available['shortage'][level] and fp not in used:records.append(rec);used.add(fp);per[level]+=1
  save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
  for level in g.LEVELS:
   for i in range(1000):
    if per[level]>=available['shortage'][level]:break
    rec=g.generate(level,int(JOB.name[:8],16)+i);fp=check(rec)
    if fp in used:continue
    records.append(rec);used.add(fp);per[level]+=1
   assert per[level]==available['shortage'][level],('Bounded capability shortage',level)
  for attr,ids in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
   if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(i) for i in ids]],p,attr.replace('/','-')+'-collisions',b),'Identity collision: reconcile'
  native(instances+records,p/'generated-grading');save(p/'generated.json',records);atomic_text(p/'generated.md','\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
  save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_sha256':sha(HERE.with_suffix('.py')),'source_evidence_unchanged':True,'available_counts':available,'new_by_level':per,'assets':[],'distinctness':'level method, angular unit and frequency; excludes amplitude, shifts, trig aliases, bank order, seed and alternative factorizations','validation_sha256':sha(HERE/'validation.json')})
  forms=transaction(records,kp,gid)
  if not forms:finish(p,gid,{'basis_before':b,'basis_after':b,'new_questions':0,'passed':True});return
  tx=dumps(forms)+'\n';txpath=p/'transaction.edn';atomic_text(txpath,tx)
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55);atomic_text(p/'preview.edn',r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',contributor[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'inventory-period-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)};save(p/'commit-intent.json',intent)
  finish(p,gid,verify(p,intent,DB._commit(intent,txpath,p)))
if __name__=='__main__':main()
