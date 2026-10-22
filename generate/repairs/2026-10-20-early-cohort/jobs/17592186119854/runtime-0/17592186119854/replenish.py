"""Scoped inventory and serialized, recoverable additive EDB submission."""
import copy,fcntl,hashlib,importlib.util,json,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.storage import atomic_json,atomic_text
sys.path[:0]=[str(HERE),str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from snapshot import DB,LEARNER,KP
from edn import dumps,loads,kw
import validate as v
g=v.g;KP_UUID=g.KP_UUID;SOURCE=':application/ca-engine';LINEAGE=g.SOURCE['lineage']
LEVELS=('moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'541891bf952eaf5e92c5aba4ce13e31ae69ba599b5661e84beabac7ae7c5b0c9'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
NATIVE=ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e';POOL=ROOT/'generate/scratch/17592186110754/check-pool';ENGINE=ROOT/'generate/runs/current/check-engine'
QUERY=(HERE/'source-query.edn').read_text();save=atomic_json

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,text=True,capture_output=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def read_kp(path,basis):
 rows=DB.query(QUERY,[KP],path,'kp',basis);assert len(rows)==1 and str(rows[0][0][':knowledge-point/id'])==KP_UUID;return rows[0][0]

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

def counts(kp,path,basis):
 pool=available(kp,basis,path/'engine-pool');eligible={e for ids in pool['available_ids_by_level'].values() for e in ids};rows={l:[] for l in LEVELS};checks=[];excluded=[]
 for q in kp[':knowledge-point/questions']:
  sid=q.get(':question/math-academy-id')
  if q[':db/id'] not in eligible:
   excluded.append({'source_id':sid,'reason':'native pool excludes shown/reserved/unrated/incomplete/canonical'});continue
  if sid=='q-74032':
   excluded.append({'source_id':sid,'reason':'original intermediate row-swap matrix has incorrect RHS -1; preserved unchanged; exclude from validated reserve'});continue
  if sid in g.CASES:
   A,b=g.parse(q);rec=g.generate(g.level(sid),0,sid,{'b':list(map(int,b))});v.check(rec)
   f=q[':question/answer-fields'][0];nf=rec['question'][':question/answer-fields'][0]
   expected={(a[':answer/type'],a[':answer/value'],a[':answer/id']==nf[':answer-field/correct'][1]) for a in nf[':answer-field/choices']}
   actual={(str(a[':answer/type'][':db/ident']),a[':answer/value'],a[':answer/id']==f[':answer-field/correct'][':answer/id']) for a in f[':answer-field/choices']};assert actual==expected
   # Actual field-owned source answer IDs, not only regenerated IDs, are graded.
   rec=copy.deepcopy(rec);rec['question']=normalize(q)
  else:
   rec=next(r for file in OUT.glob('basis-*/generated.json') for r in json.loads(file.read_text()) if r['question'][':question/id']==str(q[':question/id']));v.check(rec);assert normalize(q)==ordered(rec['question'])
  checks.append(v.native(str(q[':question/id']),rec));l=str(q[':question/difficulty'][':db/ident']).split('/')[-1];rows[l].append(q)
 save(path/'grading-input.json',checks);subprocess.run([str(ENGINE),str(path/'grading-input.json'),str(path/'grading-report.json')],check=True,capture_output=True,text=True,timeout=55)
 result={'basis':basis,'distinct_available':{l:len({g.fingerprint(q[':question/math-academy-id'],list(g.parse(q)[1])) for q in qs}) for l,qs in rows.items()},'available_ids':{l:[str(q[':question/id']) for q in qs] for l,qs in rows.items()},'excluded':excluded,'native_pool':pool}
 result['remaining_shortage']={'easy':5,**{l:max(0,5-result['distinct_available'][l]) for l in LEVELS}}
 save(path/'available-counts.json',result);return result

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_report(report,path/'receipt-check',intent['source_eid'])
 after=report[':edb/db-after-t'];kp=read_kp(path/'readback',after);before=loads((path/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items())
 exclude={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in kp.items() if k not in exclude}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
 for rec in records:
  q=next(q for q in now.values() if str(q[':question/id'])==rec['question'][':question/id']);assert normalize(q)==ordered(rec['question']);v.check(rec)
 assert not transaction([],kp,intent['generator_id'])
 c=counts(kp,path/'readback',after)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':after,'new_questions':len(records),'source_questions_unchanged':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'datoms_only_scoped_additions':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
 save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
 c=verified['available_counts_after'];result={'outcome':'unsupported' if not any(c['remaining_shortage'][l] for l in LEVELS) else 'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'verified_commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':['easy'],'unsupported_levels_filled':False,'available_counts_after':{'easy':0,**c['distinct_available']},'remaining_shortage':c['remaining_shortage'],'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'note':'Moderate/hard reserves already satisfied after excluding incomplete q-34243 and faulty intermediate solution q-74032. Registered and executed a validated generator; no surplus questions inserted. Easy remains unsupported in this bounded package. Source records and history preserved.','evidence':[str(p.relative_to(ROOT)) for p in [path/'preparation.json',path/'supplied-status.json',path/'generated.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'verification.json',path/'readback/available-counts.json',path/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'validation.json',HERE/'source-replay.json',HERE/'slot-coverage.json',HERE/'native-grading.json',HERE/'capabilities.json'] if p.exists()]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_counts_after','remaining_shortage')}),flush=True)

def main():
 val=json.loads((HERE/'validation.json').read_text());assert val['passed'];assert all(sha(ROOT/p)==h for p,h in val['hashes'].items())
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Acquired application api.lock',flush=True)
  for path in sorted(OUT.glob('basis-*')):
   if not (path/'commit-intent.json').exists():continue
   intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
   assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
   assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
   verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b;path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
  kp=read_kp(path,b);atomic_text(path/'before.edn',dumps(kp)+'\n')
  captured=loads((HERE/'reference/initial/source.edn').read_text())[0][0]
  assert kp==captured,'Source or registration changed since capture: reclassify/reconcile before committing'
  c=counts(kp,path/'current-inventory',b);print(json.dumps(c['distinct_available']),flush=True)
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
  existing=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
  assert not existing or len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT
  byscript=DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-script',b)
  assert not byscript or len(byscript)==1 and str(byscript[0][1])==gid
  contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
  supplied=JOB.with_suffix('.generated');payload=json.loads(supplied.read_text()) if supplied.exists() else {};instances=payload.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
  for rec in instances:v.check(rec)
  save(path/'supplied-status.json',{'exists':supplied.exists(),'validated_instances':len(instances),'generator_error':payload.get('generatorError')})
  records=[];used={g.fingerprint(sid,list(g.parse(q)[1])) for sid,q in g.CASES.items()};added={l:0 for l in LEVELS}
  for l in LEVELS:
   candidates=[r for r in instances if r['question'][':question/difficulty']==':question.difficulty/'+l]+g.batch(l,25,int(JOB.name[:8],16))
   for rec in candidates:
    v.check(rec);fp=rec['generation']['mathematical_fingerprint']
    if added[l]<c['remaining_shortage'][l] and fp not in used:records.append(rec);used.add(fp);added[l]+=1
   assert added[l]==c['remaining_shortage'][l], 'Bounded capacity insufficient; document finite limit before submission'
  save(path/'generated.json',records)
  checks=[v.native('prepared-'+str(i),r) for i,r in enumerate(instances+records)];save(path/'grading-input.json',checks)
  subprocess.run([str(ENGINE),str(path/'grading-input.json'),str(path/'grading-report.json')],check=True,capture_output=True,text=True,timeout=55)
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'new_by_level':added,'assets':[],'generator_sha256':sha(HERE.with_suffix('.py')),'source_basis':g.SOURCE['basis'],'source_unchanged':True,'unsupported_levels':['easy'],'unsupported_levels_filled':False,'generator_executed_after_current_inventory_check':True})
  forms=transaction(records,kp,gid)
  if not forms:
   verified={'basis_before':b,'basis_after':b,'new_questions':0,'available_counts_after':c,'passed':True,'repeat_preparation_content_changes':0};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
  txpath=path/'transaction.edn';tx=dumps(forms)+'\n';atomic_text(txpath,tx)
  pr=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  atomic_text(path/'preview.edn',pr.stdout);pr=loads(pr.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
  check_report(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'three-coefficients-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
  save(path/'commit-intent.json',intent)
  verified=verify(path,intent,DB._commit(intent,txpath,path));finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
