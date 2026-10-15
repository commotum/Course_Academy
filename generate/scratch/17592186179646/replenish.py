"""Scoped replenishment, source-preserving commit and exact-basis verification."""
import copy,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys,threading,uuid,shutil
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.storage import atomic_json,atomic_text
sys.path.insert(0,str(HERE))
from db_read import DB,KP,LEARNER,LINEAGE,SOURCE,inventory,read,plain,kw,dumps,loads
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'59868f0fffe5b90204e21b032c12bf05b8a837cd83ce2c0166242cca056d5404'
OUT=ROOT/'reference/generated'/str(KP);OUT.mkdir(parents=True,exist_ok=True)
LOCK=ROOT/'.local/learning/requests/math/api.lock';POOL=ROOT/'generate/scratch/17592186110754/check-pool';ENGINE=v.ENGINE
save=atomic_json
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

from image_library import ImageLibrary
LIBRARY=ImageLibrary(Path('/media/jake/SSD/EDB/math'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def native_checks(records,path):
 path.mkdir(parents=True,exist_ok=True);save(path/'native-input.json',[v.checks(r,r['question'][':question/id']) for r in records])
 if not records:return {}
 result=subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],capture_output=True,text=True,check=True,timeout=55)
 atomic_text(path/'native.log',result.stdout+result.stderr);report=json.loads((path/'native-report.json').read_text());assert report['documented_unresolved_checks']==0;return report

def publish(rec):
 rec=copy.deepcopy(rec);hashes=[]
 for role,original in rec['generation']['assets'].items():
  digest=sha(original);relative=LIBRARY.put_file(original,expected_sha256=digest);assert sha(LIBRARY.math_root/relative)==digest
  for attr in (':question/problem',':question/worked-solution'):rec['question'][attr]=rec['question'][attr].replace(original,relative)
  hashes.append({'role':role,'local':original,'reference':relative,'sha256':digest})
 rec['generation']['published_assets']=hashes;return rec

def validate_instance(rec):
 m=rec['generation'];q=rec['question'];lv=q[':question/difficulty'].split('/')[-1];assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.KP_UUID
 v.inspect(rec);replay=g.generate(lv,seed=m['seed'],template=m['template'],parameters=m['parameters'],profile=m['bank_profile'])
 if m.get('published_assets'):replay=publish(replay)
 assert ordered(replay['question'])==ordered(q),'Question differs from exact replay'
 return g.task_key(m['parameters'])

def source_record(q):
 sid=q.get(':question/math-academy-id')
 if sid in g.SOURCES:
  r=g.generate(g.level_of(q),parameters=g.parameters(q),profile=sid);r['question']=normalize(q);return r
 for path in OUT.glob('basis-*/generated.json'):
  for r in json.loads(path.read_text()):
   if r['question'][':question/id']==str(q[':question/id']):
    assert ordered(r['question'])==normalize(q);return r
 raise ValueError('Unknown existing generated instance: '+str(q[':question/id']))

def counts(kp,b,path):
 pool=available(kp,b,path/'engine-pool');eligible={e for ids in pool['available_ids_by_level'].values() for e in ids}
 rows={lv:[] for lv in LEVELS};excluded=[];checks=[]
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] not in eligible:
   excluded.append({'id':str(q[':question/id']),'source':q.get(':question/math-academy-id'),'reason':'native pool excludes shown, reserved, unrated, canonical or ungradable'});continue
  r=source_record(q);v.inspect(r);checks.append(r);lv=q[':question/difficulty'][':db/ident'].split('/')[-1];rows[lv].append(r)
 native_checks(checks,path/'available-grading')
 distinct={lv:len({g.task_key(g.parameters(r['question'])) for r in rs}) for lv,rs in rows.items()}
 result={'basis':b,'distinct_available':distinct,'remaining_shortage':{lv:max(0,5-distinct[lv]) for lv in LEVELS},'available_ids':{lv:[r['question'][':question/id'] for r in rs] for lv,rs in rows.items()},'excluded':excluded,'native_pool':pool,'distinctness':'same field magnitude and square length, ignoring sign/axis for uniform cancellation; radial coefficient signed and length; ignores bank, seed, identity and order'}
 save(path/'available-counts.json',result);return result

def finish(path,verification,inv):
 prep=json.loads((path/'preparation.json').read_text());after=verification['available_counts_after']
 result={'outcome':'generated' if all(after['distinct_available'][lv]>=5 for lv in g.SUPPORTED) else 'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':verification['generator_id'],'lineage':LINEAGE,'verified_commit_basis':verification['basis_after'],'verified_commit_basis_before':verification['basis_before'],'new_questions':verification['new_questions'],'new_by_level':verification['new_by_level'],'available_counts_before':prep['available_counts']['distinct_available'],'available_counts_after':after['distinct_available'],'supported_levels':list(g.SUPPORTED),'unsupported_levels':['hard'],'unsupported_levels_filled':False,'remaining_shortage':after['remaining_shortage'],'capability_exceptions':prep['capability_exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'source-replay.json',HERE/'validation.json',HERE/'visual-review.json',HERE/'registration.json',path/'preparation.json',path/'generated.json',path/'asset-hashes.json',path/'native-report.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json') if p.exists()],'note':'Hard remains short by five and is unsupported within this evidence-bounded generator; no claim of impossible mathematics. Unrated incomplete source q-127199 remains unchanged and excluded.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2),flush=True)

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_report(report,path/'receipt-check',intent['source_eid'])
 b=report[':edb/db-after-t'];kp=read(path/'readback',b);before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items()),'Source question mutation'
 omitted={':knowledge-point/questions',':knowledge-point/question-generator'};assert {k:x for k,x in before.items() if k not in omitted}=={k:x for k,x in kp.items() if k not in omitted}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);validate_instance(r)
 native_checks(records,path/'readback-grading');assert not transaction([],kp,intent['generator_id']);c=counts(kp,b,path/'readback')
 ver={'passed':True,'basis_before':intent['basis'],'basis_after':b,'generator_id':intent['generator_id'],'new_questions':len(records),'new_by_level':{lv:sum(r['question'][':question/difficulty']==':question.difficulty/'+lv for r in records) for lv in LEVELS},'source_questions_unchanged':len(old),'canonical_unchanged':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
 save(path/'verification.json',ver);return ver

def main():
 validation=json.loads((HERE/'validation.json').read_text());assert validation['passed'] and validation['generator_sha256']==sha(HERE.with_suffix('.py')) and validation['source_sha256']==sha(HERE/'source.json') and validation['engine_sha256']==sha(ENGINE)
 assert json.loads((HERE/'visual-review.json').read_text())['passed']
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Waiting for api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('api.lock acquired',flush=True)
  for path in sorted(OUT.glob('basis-*')):
   if not (path/'commit-intent.json').exists():continue
   intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
   assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn') and intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
   ver=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,ver,inventory(path/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read(path,b);atomic_text(path/'before.edn',dumps(kp)+'\n')
  assert plain(kp)==g.RAW,'Captured source changed; reclassify before writing'
  contributors=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributors)==1
  gen=kp.get(':knowledge-point/question-generator');by_script=DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-script',b);assert len(by_script)<=1
  registration=HERE/'registration.json';saved=json.loads(registration.read_text())['id'] if registration.exists() else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
  gid=str(gen[':question-generator/id']) if gen else str(by_script[0][1]) if by_script else saved
  matched=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b);assert not matched or len(matched)==1 and matched[0][0][':question-generator/script']==SCRIPT
  save(registration,{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or by_script or registration.exists()),'generator_sha256':sha(HERE.with_suffix('.py'))})
  c=counts(kp,b,path/'current-inventory');needed={lv:c['remaining_shortage'][lv] for lv in g.SUPPORTED};print(json.dumps({'basis':b,'available':c['distinct_available'],'generate':needed}),flush=True)
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances;assert isinstance(instances,list)
  for r in instances:validate_instance(r)
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
  used={g.task_key(g.parameters(q)) for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]};records=[];added={lv:0 for lv in LEVELS};attempts={lv:0 for lv in g.SUPPORTED}
  for r in instances:
   lv=r['question'][':question/difficulty'].split('/')[-1];fp=validate_instance(r)
   if added[lv]<needed[lv] and fp not in used:records.append(publish(r));used.add(fp);added[lv]+=1
  for lv in g.SUPPORTED:
   for i in range(256):
    if added[lv]>=needed[lv]:break
    attempts[lv]+=1;r=g.generate(lv,seed=int(JOB.name[:8],16)+i);fp=validate_instance(r)
    if fp in used:continue
    records.append(publish(r));used.add(fp);added[lv]+=1
  for r in records:validate_instance(r)
  identities=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
  assert len(identities)==len(set(identities))
  collisions=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[identities],path,'content-identities',b) if identities else [];assert not collisions
  exceptions=[{'level':'hard','status':'unsupported','requested':5,'produced':0,'remaining':5,'filled':False,'scope':'source-faithful bounded package','evidence':'11 source practice questions: four easy, six moderate, one incomplete unrated radial instance; no additional hard method supported. Larger coefficients alone are not a new difficulty. New source evidence reopens classification.'}]
  exceptions.extend({'level':lv,'status':'finite-limit','reason':'256 bounded sampling attempts exhausted; not a proof of mathematical exhaustion','requested':needed[lv],'produced':added[lv],'remaining':needed[lv]-added[lv],'filled':False} for lv in g.SUPPORTED if added[lv]<needed[lv])
  save(path/'generated.json',records);save(path/'asset-hashes.json',[a for r in records for a in r['generation'].get('published_assets',[])])
  atomic_text(path/'generated.md','\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+r['question'][':question/worked-solution'] for r in records)+'\n')
  native_checks(records,path);save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'new_by_level':added,'sampling_attempts':attempts,'capability_exceptions':exceptions,'generator_sha256':sha(HERE.with_suffix('.py')),'all_selected_instances_mathematically_validated':True,'all_selected_instances_actual_grader_validated':True,'source_evidence_unchanged':True,'source_basis':g.CAPTURE['basis']})
  forms=transaction(records,kp,gid);txpath=path/'transaction.edn';tx=dumps(forms)+'\n';atomic_text(txpath,tx)
  if '--prepare-only' in sys.argv:
   print(json.dumps({'prepared':True,'basis':b,'new_by_level':added,'path':str(path)}),flush=True);return
  if not forms:raise ValueError('No changes; reconcile with saved receipt')
  result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  atomic_text(path/'preview.edn',result.stdout);pr=loads(result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,path/'preview-check',contributors[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributors[0][0],'basis':b,'expected_basis':b,'request_key':'square-flux-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
  save(path/'commit-intent.json',intent);ver=verify(path,intent,DB._commit(intent,txpath,path));finish(path,ver,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
