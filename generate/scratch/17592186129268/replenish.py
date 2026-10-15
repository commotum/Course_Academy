"""KP-scoped additive shifted-cylinder replenishment; retained basis-guarded EDB requests."""
import copy,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
from capture.scripts.storage import atomic_json as save,atomic_text
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from serve_graph_explorer import database_environment,build_learning
spec=importlib.util.spec_from_file_location('shifted_validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;KP_UUID=g.SOURCE[':knowledge-point/id'];LEVELS=('easy','moderate','hard')
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.CAPTURE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'4b75e710b9471121a59515d0decd72065358b9b81f6e773575ed61158f11f93c'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
NATIVE=build_learning(ROOT.parent/'EDB');QUERY=(HERE/'source-query.edn').read_text()
MATH=Path(DB.env['EDB_MATH_ROOT']);ENGINE=ROOT/'generate/runs/current/check-engine'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

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

def source_shape(current, captured):
    # Source projections did not include all optional reverse refs or enum entity IDs.
    if isinstance(captured,dict):
        assert set(captured)<=set(current), 'Captured fact disappeared'
        return {k:source_shape(current[k],v) for k,v in captured.items()}
    if isinstance(captured,list):
        if captured and isinstance(captured[0],dict) and ':db/id' in captured[0]:
            byid={v[':db/id']:v for v in current}
            assert len(current)==len(captured)
            return canonical([source_shape(byid[v[':db/id']],v) for v in captured])
        return canonical(current)
    return canonical(current)

USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''


def read_kp(path,basis):
 rows=DB.query(QUERY,[[KP]],path,'kp',basis);assert len(rows)==1
 kp=rows[0][0];assert str(kp[':knowledge-point/id'])==KP_UUID;return kp

def localize(rec):
 rec=copy.deepcopy(rec);lib=ImageLibrary(MATH,HERE);q=rec['question']
 for key in (':question/problem',':question/worked-solution'):
  def replace(m):
   raw=m[1]
   if raw.startswith('images/'):
    data=(MATH/raw).read_bytes();assert hashlib.sha256(data).hexdigest()==Path(raw).stem;return m[0]
   data=Path(raw).read_bytes();rel=lib.store(data,raw);assert (MATH/rel).read_bytes()==data
   return '![]('+rel+')'
  q[key]=re.sub(r'!\[\]\(([^)]+)\)',replace,q[key])
 return rec,lib.saved

def fingerprint(q):
 # Read mathematical task from prompt. Disregard shared vertical translations,
 # seeds, choice banks, answer identities, and image references.
 prompt=q[':question/problem'];region=prompt.split('$$')[1]
 circ=region.split(r'\,:\,')[1].split(r'\le ')[0];rhs=region.split(r'\le ')[1].split(',')[0]
 height=region.split(r',\,')[-1].split(r'\}')[0];lo,hi=height.split(r'\le z\le ')
 f=prompt.split('$$')[3].split('{∭}_{R}')[1].split(r'\,\text{d}V')[0]
 condition=re.findall(r',([xy]\\(?:le|ge) 0)',region)
 return g.digest([str(v.s.expand(v.expr(circ)-v.expr(rhs))),str(v.s.expand(v.expr(hi)-v.expr(lo))),str(v.expr(f)),condition])

def validate_instance(rec):
 meta=rec['generation'];assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==KP_UUID
 v.verify(rec);level=rec['question'][':question/difficulty'].split('/')[-1]
 replay=g.generate(level,meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
 replay,_=localize(replay);assert ordered(replay['question'])==ordered(rec['question'])
 assert replay['generation']==meta
 return fingerprint(rec['question'])

def grade(records,path):
 path.mkdir(parents=True,exist_ok=True)
 save(path/'native-input.json',[v.native_item(r['question'][':question/id'],r) for r in records])
 subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],check=True,timeout=55)
 report=json.loads((path/'native-report.json').read_text())
 assert report['documented_unresolved_checks']==0 and report['accepted_checks']==len(records) and report['rejected_checks']==4*len(records)

def counts(kp,path,basis):
 path.mkdir(parents=True,exist_ok=True)
 shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
 reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
 saved={r['question'][':question/id']:r for p in OUT.glob('basis-*/generated.json') for r in json.loads(p.read_text())}
 available={l:set() for l in LEVELS};excluded=[];gradable=[];used=set()
 for q in kp[':knowledge-point/questions']:
  sid=q.get(':question/math-academy-id')
  if sid:
   t=next(t for t,z in g.TEMPLATES.items() if z[1]==sid);level,_,params=g.TEMPLATES[t]
   sample=g.generate(level,template=t,parameters=params,profile='observed:'+sid)
   used.add(fingerprint(localize(g.generate(level,template=t,parameters=params if t!='lower_zinverse' else {**params,'C':params['a']+1},profile='authored:method'))[0]['question']))
   if sid!='q-161637':
    excluded.append({'source':sid,'reason':'Unrated/incomplete, ambiguous full bank, or non-real source domain; retained unchanged'});continue
   assert g.eligible(g.source_banks(t,params)[0])[0]
   assert sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in sample['question'][':question/answer-fields'][0][':answer-field/choices'])
   assert next(a[':answer/value'] for a in sample['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==sample['question'][':question/answer-fields'][0][':answer-field/correct'][1])==q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
   rec={'question':normalize(q)};fp=fingerprint(localize(g.generate(level,template=t,parameters=params))[0]['question'])
  else:
   rec=saved[str(q[':question/id'])];assert ordered(normalize(q))==ordered(rec['question'])
   fp=validate_instance(rec);level=rec['generation']['level'];used.add(fp)
  gradable.append(rec)
  if q[':db/id'] not in shown|reserved:available[level].add(fp)
 if gradable:grade(gradable,path/'inventory-grading')
 stock={'basis':basis,'distinct_available':{l:len(z) for l,z in available.items()},'shown_ids':sorted(shown),'reserved_ids':sorted(reserved),'excluded_source_questions':excluded,'validated_questions':len(gradable)}
 save(path/'available-counts.json',stock);return stock,used

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,path/'receipt-check',intent['source_eid'])
 kp=read_kp(path/'readback',report[':edb/db-after-t']);before=loads((path/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(canonical(now[e])==canonical(q) for e,q in old.items())
 assert canonical({k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
 byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
  assert normalize(q)==ordered(r['question']);validate_instance(r)
  for raw in re.findall(r'!\[\]\(([^)]+)\)',q[':question/worked-solution']):assert hashlib.sha256((MATH/raw).read_bytes()).hexdigest()==Path(raw).stem
 assert not transaction([],kp,intent['generator_id'])
 result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{l:sum(r['generation']['level']==l for r in records) for l in LEVELS},'source_questions_unchanged':len(old),'canonical_unchanged':True,'learner_history_unchanged':True,'attribution_verified':True,'repeat_preparation_content_changes':0}
 save(path/'verification.json',result);return result

def finish(path,gid,verified):
 inv=inventory(path/'inventory-after.json');kp=read_kp(path/'current-inventory',inv['basis']);stock,_=counts(kp,path/'current-inventory',inv['basis'])
 missing={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS}
 result={'outcome':'finite-limit' if any(missing.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'verified_commit_basis':verified.get('basis_after'),'verified_commit_basis_before':verified.get('basis_before'),'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'available_by_level':stock['distinct_available'],'shortage_by_level':missing,'supported_levels':list(LEVELS),'authored_levels':['easy','moderate:lower_xy'],'unsupported_levels':[],'unsupported_levels_filled':False,'lineage':LINEAGE,'inventory_recheck_basis':inv['basis'],'capability_exceptions':json.loads((path/'preparation.json').read_text())['capability_exceptions'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'validation.json',HERE/'freeze.json']+list(path.glob('*')) if p.is_file()],'note':'Five flawed raw banks excluded from validated reserves, sources and learner history preserved. Authored repaired banks independently validated and actual native grading passed. api.lock held through basis recheck, guarded submission and exact-basis readback.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2),flush=True)

def main():
 assert json.loads((HERE/'validation.json').read_text())['status']=='passed'
 preview=preview_executable(SimpleNamespace(math_root=MATH,repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text())
    assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
    assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified);return
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b and LINEAGE in DB.command('status')
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b)
  current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
  for q in g.SOURCE[':knowledge-point/questions']:assert source_shape(current[q[':db/id']],q)==canonical(q),'Source evidence changed; reclassify'
  assert source_shape(kp[':knowledge-point/canonical-example'],g.SOURCE[':knowledge-point/canonical-example'])==canonical(g.SOURCE[':knowledge-point/canonical-example'])
  atomic_text(path/'before.edn',dumps(kp)+'\n')
  contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
  gen=kp.get(':knowledge-point/question-generator');byscript=DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-script',b);assert len(byscript)<=1
  gid=str(gen[':question-generator/id']) if gen else str(byscript[0][1]) if byscript else str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
  if gen:assert gen[':question-generator/script']==SCRIPT
  stock,used=counts(kp,path,b);needed={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS}
  records=[];selected={l:0 for l in LEVELS};assets={};attempts={l:0 for l in LEVELS}
  def select(rec):
   rec,a=localize(rec);fp=validate_instance(rec);level=rec['generation']['level']
   if selected[level]<needed[level] and fp not in used:records.append(rec);used.add(fp);selected[level]+=1;assets.update(a)
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
  if isinstance(instances,dict):instances=[instances]
  for rec in instances:select(rec)
  for level in LEVELS:
   for seed in range(20261014129268,20261014129328):
    if selected[level]>=needed[level]:break
    attempts[level]+=1;select(g.generate(level,seed))
  exceptions=[{'level':l,'type':'bounded-sampling-limit','attempt_budget':60,'missing':needed[l]-selected[l],'filled':False} for l in LEVELS if selected[l]<needed[l]]
  for attr,label,ids in [('question/id','q',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id','f',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id','a',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
   if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[ids],path,'identity-'+label,b),'Existing identity needs reconciliation'
  save(path/'generated.json',records)
  if records:grade(records,path)
  atomic_text(path/'review.md','\n\n---\n\n'.join(g.markdown(r) for r in records))
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'available_before':stock,'needed':needed,'selected':selected,'attempts':attempts,'capability_exceptions':exceptions,'assets':assets,'supplied_generated_exists':supplied_path.exists(),'supplied_instances_validated':len(instances),'distinct_tasks':len({fingerprint(r['question']) for r in records}),'source_evidence_unchanged':True})
  save(HERE/'freeze.json',{'generator_id':gid,'generator_path':SCRIPT,'version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'validation_sha256':sha(HERE/'validation.json'),'source_basis':g.CAPTURE['basis'],'rechecked_basis':b})
  forms=transaction(records,kp,gid)
  if not forms:
   verified={'passed':True,'new_questions':0,'by_level':selected,'basis_after':None};save(path/'verification.json',verified);finish(path,gid,verified);return
  txpath=path/'transaction.edn';tx=dumps(forms)+'\n';atomic_text(txpath,tx)
  p=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  atomic_text(path/'preview.edn',p.stdout);pr=loads(p.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
  check_report(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'shifted-cylinder-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
  save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified)

if __name__=='__main__':main()
