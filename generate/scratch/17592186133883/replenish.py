"""Scoped, locked, receipt-preserving inventory preparation and EDB commit."""
import copy,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.storage import atomic_json,atomic_text
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture'),str(HERE)]
from serve_graph_explorer import database_environment
from database import Database
from edn import dumps,loads,kw
import validate as v
g=v.g;KP=g.KP_ID
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE=':application/ca-engine';SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'5e90a510b0d8c1c8b1cecbb0550368f1c79b32fae842d25c9839a66de8339dc6'
OUT=ROOT/'reference/generated'/str(KP);OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY=(HERE/'source-query.edn').read_text()
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7'
POOL=ROOT/'generate/scratch/17592186110754/check-pool'
RAW=v.RAW['record'];save=atomic_json

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE
 save(path,x['data']);return x['data']
def read_kp(path,basis):
 rows=DB.query(QUERY,[KP],path,'kp',basis);assert len(rows)==1 and str(rows[0][0][':knowledge-point/id'])==g.KP_UUID
 return rows[0][0]
def canonical(x):
 if isinstance(x,dict):return {str(k):canonical(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return sorted((canonical(v) for v in x),key=lambda v:json.dumps(v,sort_keys=True))
 if isinstance(x,uuid.UUID):return str(x)
 return x

def ordered(q):
 q=copy.deepcopy(q)
 q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
 for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
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



def scoped(kp,b,seen):
    entities={};enums={};next_enum=1
    def enum(value):
        nonlocal next_enum
        name=str(value[':db/ident']).lstrip(':')
        if name not in enums:
            enums[name]=next_enum;entities[str(next_enum)]={'db/ident':name};next_enum+=1
        return enums[name]
    def question(q):
        r={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]}
        if ':question/difficulty' in q:r['question/difficulty']=enum(q[':question/difficulty'])
        entities[str(q[':db/id'])]=r
        for f in q.get(':question/answer-fields',[]):
            r['question/answer-fields'].append(f[':db/id'])
            field={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]}
            if ':answer-field/correct' in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
            entities[str(f[':db/id'])]=field
            for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
    entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:question(q)
    return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}

def available(kp,b,path):
    path.mkdir(parents=True,exist_ok=True)
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],path,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],path,'reserved',b)
    seen={row[0] for row in shown+reserved};save(path/'scoped-snapshot.json',scoped(kp,b,seen))
    subprocess.run([str(POOL),str(path/'scoped-snapshot.json'),str(path/'available-counts.json')],check=True,timeout=55,capture_output=True,text=True)
    return json.loads((path/'available-counts.json').read_text())



def fingerprint(q):
 sid=q.get(':question/math-academy-id')
 if sid=='q-41475':return ('triangle-0-2-plus-minus-x/2',sp.srepr(v.X))
 if sid:return ('source-id',sid)
 # Reconcile generated display against this package, not seed/identity alone.
 records=[r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text()) if r['question'][':question/id']==str(q[':question/id'])]
 if records:return v.validate_instance(records[0])
 matches=[]
 for a in g.DOMAIN:
  rec=g.generate('hard',parameters={'a':a})
  if q[':question/problem']==rec['question'][':question/problem']:matches.append(rec)
 assert len(matches)==1,'Unknown authored question needs reconciliation'
 return v.validate_instance(matches[0])

def counts(kp,b,path):
 pool=available(kp,b,path/'native-pool');eligible=set(pool['available_ids_by_level'].get('hard',[]))
 good=[];excluded=[];records=[]
 for q in kp[':knowledge-point/questions']:
  sid=q.get(':question/math-academy-id')
  if q[':db/id'] not in eligible:
   excluded.append({'id':str(q[':question/id']),'source':sid,'reason':'native pool excludes shown, reserved, unrated, canonical or ungradable content'});continue
  if sid in v.EXCLUDED:
   excluded.append({'id':str(q[':question/id']),'source':sid,'reason':v.EXCLUDED[sid]});continue
  if sid in v.VALID_SOURCES:
   rec=v.normalize(q);v.math_bank(rec['question'],v.source_answer(sid))
  else:
   matches=[r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text()) if r['question'][':question/id']==str(q[':question/id'])]
   assert len(matches)==1,'Unreconciled generated record';rec=matches[0];v.validate_instance(rec)
   assert ordered(v.normalize(q)['question'])==ordered(rec['question'])
  good.append(q);records.append(rec)
 v.native(records,path/'actual-grader')
 n=len({fingerprint(q) for q in good})
 result={'basis':b,'supported_levels':['hard'],'unsupported_levels':['moderate','easy'],'distinct_available':{'hard':n,'moderate':0,'easy':0},'remaining_shortage':{'hard':max(0,5-n),'moderate':5,'easy':5},'available_ids':[str(q[':question/id']) for q in good],'excluded':excluded,'native_pool':pool}
 save(path/'available-counts.json',result);return result

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,path/'receipt-audit',intent['source_eid'])
 b=report[':edb/db-after-t'];kp=read_kp(path/'readback',b);before=loads((path/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};new={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(new[e]==q for e,q in old.items())
 omit={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert {k:v for k,v in before.items() if k not in omit}=={k:v for k,v in kp.items() if k not in omit}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 recs=json.loads((path/'generated.json').read_text());assert len(new)==len(old)+len(recs)
 byid={str(q[':question/id']):q for q in new.values()}
 for rec in recs:
  v.validate_instance(rec);q=byid[rec['question'][':question/id']]
  assert ':question/math-academy-id' not in q and ordered(v.normalize(q)['question'])==ordered(rec['question'])
 v.native(recs,path/'readback-grading')
 assert not transaction([],kp,intent['generator_id'])
 c=counts(kp,b,path/'readback-inventory')
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(recs),'original_practice_questions_preserved':len(old),'canonical_example_preserved':True,'only_additive_scoped_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_changes':0,'available_counts_after':c}
 save(path/'verification.json',result);return result

def finish(path,intent,verified,inv):
 c=verified['available_counts_after'];prep=json.loads((path/'preparation.json').read_text())
 result={'outcome':'generated' if c['remaining_shortage']['hard']==0 else 'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'verified_commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'registration_only':verified['new_questions']==0,'supported_levels':['hard'],'unsupported_levels':['moderate','easy'],'unsupported_levels_filled':False,'available_counts_before':prep['available_counts']['distinct_available'],'available_counts_after':c['distinct_available'],'remaining_shortage':c['remaining_shortage'],'capability_exceptions':prep['capability_exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (HERE/'classification.md',HERE/'template-extraction.md',HERE/'source-fidelity.json',HERE/'validation.json',HERE/'registration.json',path/'preparation.json',path/'generated.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'readback-inventory/available-counts.json',path/'inventory-after.json')],'note':'Hard target checked using validated fresh source questions and any needed distinct variants. Easy/moderate are unsupported in this source-bounded version and remain explicit shortages. Future evidence can reopen those bands.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
 validation=json.loads((HERE/'validation.json').read_text());assert validation['passed'] and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
 assert validation['grader_executable_sha256']==sha(v.ENGINE)
 # Exercise exactly the scheduler CLI contract, including its system interpreter.
 cli=subprocess.run(['/usr/bin/python3',str(HERE.with_suffix('.py')),'--difficulty','hard','--count','3','--seed','117','--format','json'],text=True,capture_output=True,check=True,timeout=55)
 cli_records=json.loads(cli.stdout)
 for rec in cli_records:v.validate_instance(rec)
 save(OUT/'scheduler-cli-preview.json',cli_records)
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Acquiring application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
  status=DB.command('status');assert 'lineage='+LINEAGE in status
  for path in sorted(OUT.glob('basis-*')):
   if not (path/'commit-intent.json').exists():continue
   intent=json.loads((path/'commit-intent.json').read_text())
   assert intent['lineage']==LINEAGE and intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
   assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
   assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
   verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,intent,verified,inventory(path/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);atomic_text(path/'before.edn',dumps(kp)+'\n')
  original={q[':question/math-academy-id']:q for q in RAW[':knowledge-point/questions']}
  current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
  assert all(canonical(original[s])==canonical(current[s]) for s in original),'Source changed; reclassify'
  assert canonical(kp[':knowledge-point/canonical-example'])==canonical(RAW[':knowledge-point/canonical-example'])
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator')
  rows=DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-script',b);assert len(rows)<=1
  registration=HERE/'registration.json';saved=json.loads(registration.read_text())['id'] if registration.exists() else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
  gid=str(gen[':question-generator/id']) if gen else str(rows[0][1]) if rows else saved
  matching=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
  assert not matching or len(matching)==1 and matching[0][0][':question-generator/script']==SCRIPT
  save(registration,{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or matching),'generator_sha256':sha(HERE.with_suffix('.py'))})
  c=counts(kp,b,path/'current-inventory');needed=c['remaining_shortage']['hard'];print(json.dumps({'basis':b,'validated_available':c['distinct_available'],'needed_hard':needed}),flush=True)
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};supplied=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
  supplied=[supplied] if isinstance(supplied,dict) else supplied
  for rec in supplied:v.validate_instance(rec)
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(supplied)})
  used={fingerprint(q) for q in kp[':knowledge-point/questions']};recs=[]
  # Exhaust the known domain once; no seed, choice shuffle or identity duplicates.
  for rec in supplied+[g.generate('hard',parameters={'a':a}) for a in g.DOMAIN]:
   key=v.validate_instance(rec)
   if len(recs)>=needed:break
   if key in used:continue
   recs.append(rec);used.add(key)
  ids=[uuid.UUID(u) for rec in recs for u in [rec['question'][':question/id']]+[f[':answer-field/id'] for f in rec['question'][':question/answer-fields']]+[a[':answer/id'] for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
  assert len(ids)==len(set(ids))
  collisions=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-collisions',b) if ids else []
  assert not collisions
  save(path/'generated.json',recs);atomic_text(path/'generated.md','\n\n---\n\n'.join(map(g.markdown,recs)))
  v.native(recs,path/'prepared-grading')
  exceptions=[{'level':l,'requested':5,'produced':0,'remaining':5,'filled':False,'reason':'No observed source progression establishes this difficulty. Outside bounded hard generator capability; not a claim of global mathematical impossibility. Reopen on new source evidence.'} for l in ('moderate','easy')]
  if len(recs)<needed:exceptions.append({'level':'hard','requested':needed,'produced':len(recs),'remaining':needed-len(recs),'filled':False,'reason':'Exhausted complete 12-value validated coefficient domain after mathematical deduplication.'})
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'available_counts':c,'source':SOURCE,'needed_hard':needed,'new_hard':len(recs),'capability_exceptions':exceptions,'generator_sha256':sha(HERE.with_suffix('.py')),'source_capture_basis':v.RAW['basis'],'assets':[validation['asset']],'source_questions_preserved':True,'native_pool_sha256':sha(POOL),'native_inventory_sha256':sha(NATIVE)})
  forms=transaction(recs,kp,gid)
  if not forms:
   raise ValueError('No changes: existing registration should have retained receipt; reconcile before fresh request')
  txpath=path/'transaction.edn';tx=dumps(forms)+'\n';atomic_text(txpath,tx)
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  atomic_text(path/'preview.edn',r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
  check_report(pr,path/'preview-audit',source[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'greens-evaluate-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in recs],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
  save(path/'commit-intent.json',intent)
  verified=verify(path,intent,DB._commit(intent,txpath,path));finish(path,intent,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
