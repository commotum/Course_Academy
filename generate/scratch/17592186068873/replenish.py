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
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'72d38c4c71dd7c14a5ed123774cd7ad0b7a6e86609ea0b191ac771dd515fd7ed'
GENERATOR_ID=str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
LEVELS=['easy','moderate','hard']
LOCK=ROOT/'.local/learning/requests/math/api.lock'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):
 if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
 if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
 return str(x) if isinstance(x,uuid.UUID) else x
def inventory(native,path):
 p=subprocess.run([str(native),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=55)
 r=json.loads(p.stdout);assert r['ok'];x=r['data'];assert x['lineage']==LINEAGE;save(path,x);return x
def fingerprint(q):
 import re
 p=re.search(r'\$([^$]*)\$',q[':question/problem'])[1].split('=')[0].strip()
 e=v.parse(p);symbol=list(e.free_symbols)[0];poly=v.sp.Poly(e,symbol);a=poly.nth(1)/2
 outer=re.search(r'\)([+-])(\d+)$',p.replace(' ','').replace('{','').replace('}',''))
 assert outer and a>0 and a.is_Integer
 sign=1 if outer[1]=='+' else -1;k=int(outer[2]);assert poly.nth(0)-sign*k==a*a
 return g.digest([int(a),k,sign])  # Ignore aliases, formatting, bank/profile, and response format.

def engine_item(label,r):
 checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete bank grading'} for a in f[':answer-field/choices'])
  else:
   answer=f[':answer-field/choices'][0][':answer/value'];val=v.parse(answer)
   equivalent='1*('+answer+')' if f[':answer-field/key']=='field-1' else str(val)+'/2+'+str(val)+'/2'
   checks.extend({'field_index':fi,'submitted':entry,'expected':ex,'purpose':purpose} for entry,ex,purpose in [(answer,'accepted','canonical fragment'),(equivalent,'accepted','equivalent fragment'),(str(val+1),'rejected','incorrect fragment')])
 return {'label':label,'record':r,'checks':checks}

def validate_current(q):
 # Source IDs determine masks for originals; new instances must fit one validated solution family.
 nq=normalized(q);level=nq[':question/difficulty'].rsplit('/',1)[1]
 source=q.get(':question/math-academy-id')
 templates=[source] if source in g.CONFIG else ([sid for sid,c in g.CONFIG.items() if c[0]==level] if level!='hard' else ['hard_radio','hard_blank'])
 for sid in templates:
  rec={'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':nq,'generation':{'template':sid}}
  try:v.check(rec)
  except (AssertionError,ValueError,KeyError,TypeError):continue
  return rec
 raise ValueError('No validated source-shaped solution/answer family')

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
 # Retained presentation history must be available to establish freshness.
 retention=DB.query('[:find ?i :in $ [?i ...] :where [?a :db/ident ?i] [?a :db/noHistory true]]',[[kw(x) for x in ['task-item/content','learner-task/items','learner/activity']]],path,'history-retention',basis)
 assert not retention,'Freshness cannot be established after history loss'
 out={level:set() for level in LEVELS};excluded=[];payload=[]
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] in shown|reserved:continue
  level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
  if level not in out:excluded.append({'question':str(q[':question/id']),'reason':'unclassified'});continue
  try:
   rec=validate_current(q);key=fingerprint(q)
  except (AssertionError,ValueError,KeyError,TypeError) as error:excluded.append({'question':str(q[':question/id']),'reason':str(error) or type(error).__name__});continue
  out[level].add(key);payload.append(engine_item(str(q[':question/id']),rec))
 save(path/'available-native-input.json',payload)
 subprocess.run([str(H/'check-engine'),str(path/'available-native-input.json'),str(path/'available-native-report.json')],check=True)
 assert json.loads((path/'available-native-report.json').read_text())['documented_unresolved_checks']==0
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
  assert str(gen[':question-generator/id'])==GENERATOR_ID and gen[':question-generator/script']==SCRIPT
 else:
  forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(GENERATOR_ID),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
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
 return x
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
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q;assert canonical(normalized(q))==canonical(r['question']);assert fingerprint(q)==fingerprint(r['question']);v.check(r)
 assert not tx([],after), 'Repeat preparation must be a content no-op'
 c=counts(after,path/'readback',b)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'distinct_available_after':c['distinct_available'],'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'no_retractions':True,'only_requested_kp_additive_content':True,'source':SOURCE,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
 save(path/'verification.json',result);return result

def finish(path,verified,inv):
 remaining={l:max(0,5-verified['distinct_available_after'][l]) for l in LEVELS}
 caps=json.loads((H/'capabilities.json').read_text())
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'topic':17592186050372,'generator_path':SCRIPT,'generator_id':GENERATOR_ID,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'supported_levels':LEVELS,'available_after':verified['distinct_available_after'],'shortage_remaining':remaining,'capability_exceptions':caps['exceptions'],'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [H/'validation.json',H/'engine-build.json',H/'current-engine-validation.json',H/'classification.md',H/'template-extraction.md',H/'capabilities.json',H/'freeze.json',path/'preparation.json',path/'generated.json',path/'transaction.edn',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'verification.json',path/'inventory-after.json',path/'native-report.json'] if p.exists()],'note':'Existing isolated-square generator reused. Hard is an explicit validated authored square-recognition extension (a=11..15), not an observed source band. Deduplication ignores variable, response format, source layout, bank, seed and choice order. All three supported reserves verified; incomplete unrated originals remain unchanged and the legacy unclassified job may remain.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
 global GENERATOR_ID
 val=json.loads((H/'validation.json').read_text());assert val['status']=='pass'
 frozen=json.loads((H/'freeze.json').read_text());assert all(sha(ROOT/name)==digest for name,digest in frozen['sha256'].items())
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event());native=build_learning(ROOT.parent/'EDB')
 with LOCK.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  # Recover exact saved submission before any fresh planning or identity work.
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());GENERATOR_ID=intent['generator_id'];assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(report,path,intent);finish(path,verified,inventory(native,path/'inventory-after.json'));return
  inv=inventory(native,OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b and LINEAGE in DB.command('status')
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
  kp=read(b,'locked-source');assert str(kp[':knowledge-point/id'])==g.KP_UUID
  captured=g.SOURCE['record']
  def strip_ids(x):
   if isinstance(x,dict):return {str(k):strip_ids(z) for k,z in x.items() if str(k)!=':db/id'}
   if isinstance(x,(list,tuple)):return sorted([strip_ids(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
   return str(x) if isinstance(x,uuid.UUID) else x
  original={q[':question/math-academy-id']:q for q in captured[':knowledge-point/questions']};current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
  assert all(strip_ids(q)==strip_ids(current[sid]) for sid,q in original.items()),'Source evidence changed; reclassify'
  assert strip_ids(captured[':knowledge-point/canonical-example'])==strip_ids(kp[':knowledge-point/canonical-example'])
  (path/'before.edn').write_text(dumps(kp)+'\n')
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
  reg=kp.get(':knowledge-point/question-generator')
  orphans=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b)
  assert len(orphans)<=1
  if reg:GENERATOR_ID=str(reg[':question-generator/id'])
  elif orphans:GENERATOR_ID=str(orphans[0][0][':question-generator/id'])
  if reg:assert str(reg[':question-generator/id'])==GENERATOR_ID and reg[':question-generator/script']==SCRIPT,'Existing identity requires reconciliation'
  counts_before=counts(kp,path,b);jobs={j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP};needed={l:max(0,5-counts_before['distinct_available'][l],jobs.get(l,{}).get('missing',0)) for l in LEVELS}
  used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']));records=[]
  supplied=json.loads(JOB.with_suffix('.generated').read_text()) if JOB.with_suffix('.generated').exists() else {};instances=supplied.get('instances',[])
  if isinstance(instances,dict):instances=[instances]
  rejected=[]
  for r in instances:
   level=r['question'][':question/difficulty'].split('/')[-1]
   if level not in needed:rejected.append({'question':r['question'][':question/id'],'reason':'Unsupported level'});continue
   v.check(r);p=r['generation'];assert r==g.generate(level,p['seed'],template=p['template'],profile=p['bank_profile'],parameters=p['parameters'])
   assert p['eligible_for_learning'] and not p['evidence_only']
   key=fingerprint(r['question'])
   if needed[level]>0 and key not in used:records.append(r);used.add(key);needed[level]-=1
  # Execute registered protocol for each currently missing supported band.
  generated_counts={l:0 for l in needed}
  for r in records:generated_counts[r['question'][':question/difficulty'].split('/')[-1]]+=1
  for level in needed:
   if not needed[level]:continue
   result=subprocess.run([str(ROOT/'.venv/bin/python'),str(H.with_suffix('.py')),'--difficulty',level,'--count',str(needed[level]+len(used)+5),'--seed','421019372','--format','json'],capture_output=True,text=True,check=True)
   for r in json.loads(result.stdout):
    v.check(r);assert r['generation']['eligible_for_learning'];key=fingerprint(r['question'])
    if key in used:continue
    records.append(r);used.add(key);needed[level]-=1;generated_counts[level]+=1
    if needed[level]==0:break
   # Any bounded sampler shortage remains explicit in the outcome.
  for attr,key,ids in [('question/id','q',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id','f',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id','a',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
   if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[ids],path,'identity-'+key,b),'Existing identity requires reconciliation'
  gid=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(GENERATOR_ID)],path,'generator-identity',b);assert not gid or len(gid)==1 and gid[0][0][':question-generator/script']==SCRIPT
  save(path/'generated.json',records);save(path/'native-input.json',[engine_item(r['question'][':question/id'],r) for r in records])
  subprocess.run([str(H/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
  assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_evidence_unchanged':True,'available_before':counts_before,'new_by_level':generated_counts,'new_questions':len(records),'supported_shortage_remaining':needed,'supplied_generated_file_exists':JOB.with_suffix('.generated').exists(),'supplied_rejected':rejected,'distinct_mathematical_tasks':len({fingerprint(r['question']) for r in records}),'generator_version':g.VERSION,'generator_sha256':sha(H.with_suffix('.py')),'asset_hashes':[]})
  if '--prepare-only' in sys.argv:
   print(json.dumps({'preparation':str(path),'basis':b,'new_by_level':generated_counts}),flush=True);return
  forms=tx(records,kp)
  if not forms:
   verified={'basis_before':b,'basis_after':b,'new_questions':0,'distinct_available_after':counts_before['distinct_available'],'passed':True,'repeat_preparation_content_changes':0};save(path/'verification.json',verified);finish(path,verified,inv);return
  txpath=path/'transaction.edn';text=dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(text);f.flush();os.fsync(f.fileno())
  result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  (path/'preview.edn').write_text(result.stdout);pr=loads(result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;report_checks(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','lineage':LINEAGE,'endpoint':DB.args.endpoint,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'sha256':sha(txpath),'exact_edn':text,'request_key':'isolated-square-replenishment-'+str(b)+'-'+sha(txpath),'generator_id':GENERATOR_ID,'generator_path':SCRIPT,'generator_sha256':sha(H.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()}
  save(path/'commit-intent.json',intent)
  report=DB._commit(intent,txpath,path);verified=verify(report,path,intent);finish(path,verified,inventory(native,path/'inventory-after.json'))
if __name__=='__main__':main()
