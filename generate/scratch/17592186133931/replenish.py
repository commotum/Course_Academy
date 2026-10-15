"""KP-scoped additive replenishment using the application's EDB integration."""
import copy,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));import validate as v;g=v.g
sys.path.insert(0,str(ROOT));from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import database_environment
from inventory_jobs import save
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from database import Database
from edn import dumps,loads,kw
KP=g.KP[':db/id'];LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'b81d2d89e4a3a0407c80c1188e7e401db18ec3453c506580b7f4f45c05cde00c'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY=(HERE/'reference/initial/kp-query.edn').read_text()
NATIVE=ROOT/'.local/graph-explorer/learning-64e7aa312fccadb0';POOL=ROOT/'generate/scratch/17592186110754/check-pool'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(p):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']
def read(p,b):return DB.query(QUERY,[KP],p,'kp',b)[0][0]
def normalize(q):
    return {':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':sorted([{':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])} for f in q[':question/answer-fields']],key=lambda f:f[':answer-field/key'])}

def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q

def scoped(kp,b,seen):
    entities={};enums={}
    def enum(value):
        name=str(value[':db/ident']).lstrip(':')
        if name not in enums:
            e=len(enums)+1;enums[name]=e;entities[str(e)]={'db/ident':name}
        return enums[name]
    for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
        r={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]};entities[str(q[':db/id'])]=r
        if ':question/difficulty' in q:r['question/difficulty']=enum(q[':question/difficulty'])
        for f in q.get(':question/answer-fields',[]):
            r['question/answer-fields'].append(f[':db/id']);field={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]};entities[str(f[':db/id'])]=field
            if ':answer-field/correct'in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
            for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
    entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}

def transaction(records,kp,gid):
    forms=[]
    for r in records:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    else:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,p,source):
    attrs=dict(DB.attributes(p,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution/retraction'
        name=str(attrs[a])
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,name

# Extend the independent arithmetic reader for the newly captured square-root
# source. This changes no generator family or source records.
base_parse=v.parse
def parse(t):
 while r'\sqrt{' in t:
  i=t.index(r'\sqrt{');body,j=v.grouped(t,i+5)
  t=t[:i]+'(('+str(parse(body))+')**(1/2))'+t[j:]
 return base_parse(t)
v.parse=parse

def display(q):
 q=copy.deepcopy(q)
 for k in (':question/problem',':question/worked-solution'):
  q[k]=q.get(k,'').replace(r'\mathbf{F}','F').replace(r'\mathbf{i}','i').replace(r'\mathbf{j}','j').replace(r'\mathbf{k}','k')
 return q

def fingerprint(q):
 F,bounds=v.prompt_data(display(q));D=g.s.simplify(sum(g.s.diff(f,x) for f,x in zip(F,g.VARIABLES)))
 if not D.free_symbols:
  task={'divergence':str(D),'unordered_widths':sorted(str(hi-lo) for lo,hi in bounds),'criterion':'outward_flux'}
 else:task={'F':[g.s.srepr(f) for f in F],'bounds':[[g.s.srepr(x) for x in pair] for pair in bounds],'criterion':'outward_flux'}
 return hashlib.sha256(json.dumps(task,sort_keys=True).encode()).hexdigest()

def validate(r):
 meta=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
 assert level in LEVELS and meta['eligible_for_learning'] and not meta['evidence_only']
 assert r['knowledge_point']['db_id']==KP and r['knowledge_point']['id']==g.KP[':knowledge-point/id']
 replay=g.generate(level,meta['seed'],meta['template'],parameters=meta['parameters'],profile=meta['profile'])
 assert ordered(replay['question'])==ordered(r['question']) and replay['generation']==meta
 v.check_record(r)

def native(records,p):
 p.mkdir(parents=True,exist_ok=True);items=[]
 for i,r in enumerate(records):
  f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected'} for a in f[':answer-field/choices']]
  items.append({'label':str(i),'record':r,'checks':checks})
 save(p/'input.json',items)
 if items:subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(p/'input.json'),str(p/'report.json')],check=True,timeout=55)

CONTEXT=17592186235537
NEW_SOURCE={17592186537908:'sqrt-x',17592186537916:'negative-sine-y'}
def source_audit(q):
 nq=display(q);F,bounds=v.prompt_data(nq);s=g.s
 D=s.simplify(sum(s.diff(f,x) for f,x in zip(F,g.VARIABLES)));value=D
 for x,(lo,hi) in reversed(list(zip(g.VARIABLES,bounds))):value=s.integrate(value,(x,lo,hi))
 value=s.simplify(value);f=q[':question/answer-fields'][0];choices=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(choices)==5 and len(set(choices))==5
 assert s.simplify(parse(f[':answer-field/correct'][':answer/value'])-value)==0
 # Verify the final evaluated flux against the live source's displayed solution.
 bs=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',nq[':question/worked-solution'],re.S)
 final=bs[-1].split(r'\\  & =')[-1].rstrip('.')
 assert s.simplify(parse(final)-value)==0
 if q[':db/id'] not in {*NEW_SOURCE,17592186134139}:
  test={'question':normalize(q),'knowledge_point':{'db_id':KP,'id':g.KP[':knowledge-point/id'],'title':g.KP[':knowledge-point/title']},'generation':{'template':'source','eligible_for_learning':False}}
  v.check_record(test)
 else:
  # Current sources use a different endpoint layout from frozen replay.
  divrows=bs[0].split(r'\\  & =');assert len(divrows)==3
  assert s.simplify(parse(divrows[1])-D)==0 and s.simplify(parse(divrows[2].rstrip('.'))-D)==0
  rows=bs[-1].split(r'\\  & =');rows[0]=rows[0].split('& =',1)[1];rows[-1]=rows[-1].rstrip('.')
  assert all(s.simplify(v.rowvalue(row,bounds)-value)==0 for row in rows)
  repeated,pairs,rv=v.integral_data(rows[1]);assert s.simplify(repeated-D)==0 and [p for x,p in pairs]==bounds
  factors=[v.integral_data(t) for t in v.split_product(rows[2])]
  assert len(factors)==3 and s.simplify(s.prod(t[0] for t in factors)-D)==0
  assert [t[1][0] for t in factors]==list(zip(g.VARIABLES,bounds))
 return {'question':normalize(q),'knowledge_point':{'db_id':KP,'id':g.KP[':knowledge-point/id'],'title':g.KP[':knowledge-point/title']},'generation':{'source_audit':True,'divergence':str(D),'exact_flux':str(value)}}

def counts(kp,b,p):
 p.mkdir(parents=True,exist_ok=True)
 shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
 reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
 seen={row[0] for row in shown+reserved};save(p/'scoped-snapshot.json',scoped(kp,b,seen))
 subprocess.run([str(POOL),str(p/'scoped-snapshot.json'),str(p/'native-pool.json')],capture_output=True,text=True,check=True,timeout=55)
 pool=json.loads((p/'native-pool.json').read_text());available={e for xs in pool['available_ids_by_level'].values() for e in xs}
 known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
 bylevel={l:[] for l in LEVELS};fps={l:set() for l in LEVELS};excluded=[];records=[];audits=[]
 for q in kp[':knowledge-point/questions']:
  if q[':db/id']==CONTEXT:
   excluded.append({'id':q[':db/id'],'reason':'Missing preceding field/region; context-dependent blank remains ineligible.'});continue
  if ':question/math-academy-id' in q:r=source_audit(q);audits.append({'id':q[':db/id'],**r['generation']})
  else:
   r=known[str(q[':question/id'])];validate(r);assert normalize(q)==ordered(r['question'])
  if q[':db/id'] not in available:
   excluded.append({'id':q[':db/id'],'reason':'Native pool excludes shown/reserved/unrated/ungradable questions.'});continue
  l=str(q[':question/difficulty'][':db/ident']).split('/')[-1];assert l in LEVELS
  fp=fingerprint(q);fps[l].add(fp);bylevel[l].append(str(q[':question/id']));records.append(r)
 native(records,p/'grading');save(p/'source-audit.json',audits)
 result={'basis':b,'levels':{l:{'distinct_available_tasks':len(fps[l]),'available_question_ids':bylevel[l]} for l in LEVELS},'excluded':excluded,'native_pool':pool,'deduplication':'fixed field and exact box; constant-divergence width permutations collapsed; seed, choice order and identities excluded'}
 save(p/'counts.json',result);return result

def verify(p,intent,report):
 assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis'];check_report(report,p/'receipt-check',intent['source_eid'])
 b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items());exclude={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in kp.items() if k not in exclude}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);validate(r)
 assert not transaction([],kp,intent['generator_id'])
 after=counts(kp,b,p/'readback');result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':after};save(p/'verification.json',result);return result

def finish(p,gid,verified,inv):
 after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'shortage_remaining':remaining,'available_counts_after':{l:after['levels'][l]['distinct_available_tasks'] for l in LEVELS},'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_exceptions':{'context_source':CONTEXT,'reason':'Missing prior-part premise; excluded from validated available counts and generation.','new_source_profiles':{'ids':list(NEW_SOURCE),'generation_supported':False,'reason':'Newly captured radical and negative-sine families are classified and mathematically audited as original practice; parameterized bank intentions are not established. Existing ten-family moderate sampler suffices for reserve.'},'finite_sampler_by_level':{'easy':32,'moderate':4715,'hard':100}},'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'reference/current-source-classification.md',HERE/'freeze.json'] if f.exists()]}
 save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','available_counts_after','shortage_remaining')}),flush=True)

def main():
 report=json.loads((HERE/'validation.json').read_text());assert report['status']=='pass_with_documented_ineligible_source_context'
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 save(HERE/'freeze.json',{'generator_version':g.VERSION,'sha256':{str(f.relative_to(ROOT)):sha(f) for f in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json']},'validation':str((HERE/'validation.json').relative_to(ROOT))})
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
  for p in sorted(OUT.glob('basis-*')):
   if not (p/'commit-intent.json').exists():continue
   intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
   assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
   verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b)
  captured=loads((HERE/'reference/initial/kp.edn').read_text())[0][0];assert kp==captured,'Source or generator changed since current-source audit'
  (p/'before.edn').write_text(dumps(kp)+'\n');source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'question-generator'))
  existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
  if existing:
   assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
  save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
  c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS};print(json.dumps({'basis':b,'missing':needed}),flush=True)
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied;instances=[instances] if isinstance(instances,dict) else instances
  for r in instances:validate(r)
  save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
  used={fingerprint(q) for q in kp[':knowledge-point/questions'] if q[':db/id']!=CONTEXT};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
  records=[];added={l:0 for l in LEVELS}
  for l in LEVELS:
   for r in instances:
    if added[l]>=needed[l]:break
    if r['question'][':question/difficulty']!=':question.difficulty/'+l:continue
    fp=fingerprint(r['question'])
    if fp not in used:validate(r);records.append(r);used.add(fp);added[l]+=1
   for seed in range(1000):
    if added[l]>=needed[l]:break
    r=g.generate(l,int(JOB.name[:8],16)+seed);fp=fingerprint(r['question'])
    if fp in used:continue
    validate(r);records.append(r);used.add(fp);added[l]+=1
  ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
  if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
  save(p/'generated.json',records);(p/'generated.md').write_text('\n\n---\n\n'.join(map(g.markdown,records)));native(records,p/'selected-grading')
  save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len(records),'asset_hashes':[],'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True,'finite_shortages':{l:needed[l]-added[l] for l in LEVELS if needed[l]>added[l]}})
  forms=transaction(records,kp,gid)
  if not forms:
   verified={'passed':True,'basis_after':b,'new_questions':0,'available_counts_after':c};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
  tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=55);(p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'closed-flux-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(p/'commit-intent.json',intent)
  verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()
