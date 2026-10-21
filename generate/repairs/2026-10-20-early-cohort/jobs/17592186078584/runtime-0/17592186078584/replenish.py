"""Additive, locked inventory replenishment for the inhibited-decay KP only."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment,build_learning
from capture.scripts.database.preview import preview_executable
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=17592186078584
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE=g.SNAPSHOT['lineage']
SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'23fd0480b509386d94cc097bb298278bfc3910ba1f666739d995f86497aac5ad'
OUT=HERE/'reference/replenishment'
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
QUERY=(HERE/'reference/source-query.edn').read_text()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def normalize(q):
    result = {k: str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f: f[':answer-field/key']):
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a:a[':answer/value'])})
    return result

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'], kw('answer/id'):uuid.UUID(a[':answer/id']), kw('answer/type'):kw(a[':answer/type']), kw('answer/value'):a[':answer/value'], kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'], kw('answer-field/id'):uuid.UUID(f[':answer-field/id']), kw('answer-field/key'):f[':answer-field/key'], kw('answer-field/type'):kw(f[':answer-field/type']), kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'):f[':answer-field/correct'][1], kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'], kw('question/id'):uuid.UUID(q[':question/id']), kw('question/problem'):q[':question/problem'], kw('question/worked-solution'):q[':question/worked-solution'], kw('question/difficulty'):kw(q[':question/difficulty']), kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'):kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(gid), kw('question-generator/script'):SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'):KP, kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms

def check_report(report, path, source):
    attrs = {e:str(a) for e,a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name

def canonical(x):
    if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
    if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
    return str(x) if isinstance(x,uuid.UUID) else x

USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''

def source_record(q):
 sid=q[':question/math-academy-id'];temp,p=g.ORIGINALS[sid]
 rec=g.generate(g.TEMPLATES[temp],template=temp,parameters=p,profile=sid)
 # A current source must still match its complete captured bank, key and prose.
 f=q[':question/answer-fields'][0];rf=rec['question'][':question/answer-fields'][0]
 assert q[':question/problem']==rec['question'][':question/problem']
 assert q[':question/worked-solution']==rec['question'][':question/worked-solution']
 assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
 assert f[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
 v.validate(rec);return rec

def grade(records,path):
 path.mkdir(parents=True,exist_ok=True);items=[]
 for r in records:
  f=r['question'][':question/answer-fields'][0]
  items.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned radio choice with independently verified mathematics'} for a in f[':answer-field/choices']]})
 save(path/'input.json',items)
 subprocess.run([str(HERE/'check-engine'),str(path/'input.json'),str(path/'report.json')],check=True)
 assert json.loads((path/'report.json').read_text())['documented_unresolved_checks']==0

def counts(kp,path,basis):
 shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
 reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
 pools={l:set() for l in g.LEVELS};exposed=set();all_records=[];excluded=[];entries=[]
 for q in kp[':knowledge-point/questions']:
  sid=q.get(':question/math-academy-id')
  if sid:
   rec=source_record(q)
  else:
   # Reconstruct the actual printed givens before deriving its task identity.
   rec=next((r for r in GENERATED if r['question'][':question/id']==str(q[':question/id'])),None)
   assert rec is not None,'Unknown generated record: reconcile before generating'
   assert normalize(q)==ordered(rec['question']);v.validate(rec)
  fp=rec['generation']['mathematical_fingerprint'];level=rec['question'][':question/difficulty'].split('/')[-1]
  all_records.append(rec)
  if q[':db/id'] in shown|reserved:exposed.add(fp)
  if sid=='q-107122':
   excluded.append({'question':sid,'reason':'Three Fahrenheit/Celsius solution-label contradictions; preserved unchanged'});continue
  entries.append((q,level,fp))
 for q,l,fp in entries:
  if q[':db/id'] not in shown|reserved and not q.get(':knowledge-point/_canonical-example') and fp not in exposed:pools[l].add(fp)
 grade(all_records,path/'inventory-grading')
 result={'basis':basis,'distinct_available':{l:len(pools[l]) for l in g.LEVELS},'shown_ids':sorted(shown),'reserved_ids':sorted(reserved),'excluded':excluded,'all_task_fingerprints':[r['generation']['mathematical_fingerprint'] for r in all_records]}
 save(path/'available-counts.json',result);return result

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,path/'receipt-check',intent['source_eid'])
 b=report[':edb/db-after-t'];kp=read_kp(path/'readback',b);before=loads((path/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(canonical(now[e])==canonical(q) for e,q in old.items())
 assert canonical({k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q;assert normalize(q)==ordered(r['question']);v.validate(r)
 assert not transaction([],kp,intent['generator_id'])
 stock=counts(kp,path/'readback',b)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'source_questions_preserved':len(old),'canonical_example_preserved':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'attribution_verified':SOURCE,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts':stock}
 save(path/'verification.json',result);return result

def finish(path,intent,verified):
 inv=inventory(path/'inventory-after.json');kp=read_kp(path/'current-inventory',inv['basis']);stock=counts(kp,path/'current-inventory',inv['basis'])
 remaining={l:max(0,5-stock['distinct_available'][l]) for l in g.LEVELS}
 assert not any(remaining.values()),'Supported shortage remains; do not report filled'
 result={'outcome':'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'verified_commit_basis':verified['basis_after'],'lineage':LINEAGE,'new_questions':verified['new_questions'],'supported_levels':list(g.LEVELS),'unsupported_levels':[],'shortage_remaining':remaining,'available_counts':stock['distinct_available'],'excluded_source_questions':stock['excluded'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'preparation.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'generated.json',path/'generated-grading/report.json',path/'inventory-after.json',HERE/'validation.json',HERE/'native-report.json',HERE/'classification.md',HERE/'frozen-hashes.json') if p.exists()]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2))

GENERATED=[]
def main():
 global NATIVE,GENERATED
 assert json.loads((HERE/'validation.json').read_text())['status']=='pass'
 assert all(sha(ROOT/name)==digest for name,digest in json.loads((HERE/'frozen-hashes.json').read_text()).items())
 NATIVE=build_learning(ROOT.parent/'EDB')
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 # Recovery always uses the original saved request, never newly generated intent.
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  assert LINEAGE in DB.command('status')
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
    assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    GENERATED=json.loads((path/'generated.json').read_text());report=DB._commit(intent,path/'transaction.edn',path);finish(path,intent,verify(path,intent,report));return
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP[':knowledge-point/id']
  old={q[':db/id']:q for q in kp[':knowledge-point/questions']};assert len(old)==len(g.KP[':knowledge-point/questions'])
  assert all(canonical(old[q[':db/id']])==canonical(q) for q in g.KP[':knowledge-point/questions']),'Source changed; reclassify'
  assert canonical(kp[':knowledge-point/canonical-example'])==canonical(g.KP[':knowledge-point/canonical-example'])
  (path/'before.edn').write_text(dumps(kp)+'\n')
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
  reg=kp.get(':knowledge-point/question-generator');gid=str(reg[':question-generator/id']) if reg else str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'course-academy-generator'))
  matches=DB.query('[:find ?e ?script :in $ ?id :where [?e :question-generator/id ?id] [?e :question-generator/script ?script]]',[uuid.UUID(gid)],path,'generator-identity',b);assert not matches or reg and len(matches)==1 and matches[0][1]==SCRIPT
  stock=counts(kp,path,b);needed={l:max(0,5-stock['distinct_available'][l]) for l in g.LEVELS}
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
  for r in instances:v.validate(r)
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
  # Public CLI, complete banks, no option-only or seed-only duplicates.
  run=subprocess.run([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--count','8','--seed',str(int(JOB.name[:8],16)),'--format','json'],capture_output=True,text=True,check=True)
  candidates=instances+json.loads(run.stdout);save(path/'local-preview.json',candidates)
  used=set(stock['all_task_fingerprints']);used.add(g.fingerprint({'level':'easy','parameters':{'ambient':23,'initial':80,'rate':'1/4','time':4,'unit':'C'}}));records=[];new={l:0 for l in g.LEVELS}
  for r in candidates:
   v.validate(r);l=r['question'][':question/difficulty'].split('/')[-1];fp=r['generation']['mathematical_fingerprint']
   if new[l]<needed[l] and fp not in used:records.append(r);new[l]+=1;used.add(fp)
  assert new==needed,'Bounded candidate count cannot meet shortage'
  GENERATED=records;save(path/'generated.json',records);grade(records,path/'generated-grading')
  (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
  for attr,ids in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
   if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(x) for x in ids]],path/'identity-check',attr.replace('/','-'),b),'Identity collision'
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':stock,'needed':needed,'new_by_level':new,'distinct_tasks':len(records),'generator_id':gid,'generator_path':SCRIPT,'asset_hashes':[],'no_source_or_history_mutations':True})
  txpath=path/'transaction.edn';tx=dumps(transaction(records,kp,gid))+'\n'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout)
  pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'inhibited-decay-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);finish(path,intent,verify(path,intent,report))
if __name__=='__main__':main()

