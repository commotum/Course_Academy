"""Additive quadrilateral inventory using the application's EDB writer and lock."""
from __future__ import annotations
import copy, fcntl, hashlib, importlib.util, json, math, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from serve_graph_explorer import database_environment
from database import Database,StaleBasis
from inventory_jobs import save
from edn import dumps,loads,kw
spec=importlib.util.spec_from_file_location('quadrilateral_validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));LEVELS=('easy','moderate','hard')
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'9ac3d22d9afedaf2f3adc022f2e7aff3823a2373870695a0a211f617cf98bf15'
OUT=HERE/'reference/replenishment';LOCK=ROOT/'.local/learning/requests/math/api.lock';ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
QUERY=(OUT/'source-query.edn').read_text();NATIVE=Path((OUT/'learning-executable.txt').read_text().strip())
USAGE_QUERY='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l] (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
 (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/unlocked] [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?s] [?s :step/content ?q]))]'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(path,b):return DB.query(QUERY,[KP],path,'kp',b)[0][0]
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def norm(q):
 def enum(x):return str(x[':db/ident']) if isinstance(x,dict) else str(x)
 result={k:str(q[k]) for k in (':question/id',':question/problem',':question/worked-solution')}
 result[':question/difficulty']=enum(q[':question/difficulty']);fields=[]
 for f in q[':question/answer-fields']:
  correct=f[':answer-field/correct'];fields.append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':enum(f[':answer-field/type']),':answer-field/correct':[':answer/id',str(correct[':answer/id'])] if isinstance(correct,dict) else correct,':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':enum(a[':answer/type']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])})
 result[':question/answer-fields']=sorted(fields,key=lambda f:f[':answer-field/key']);return result

def fingerprint(p,kind):
 # Exclude level, source-mask, label, seed, precision, bank and identity from the
 # deduplication key: never serve the same supplied mathematical data twice.
 pairs=[(tuple(sorted([p['a'],p['b']])),p['theta'])]
 if kind=='general':pairs.append((tuple(sorted([p['c'],p['d']])),p['phi']))
 return g.digest({'kind':kind,'triangles':sorted(pairs)})

def validate(r):
 m=r['generation'];assert r['knowledge_point']['db_id']==KP and m['eligible_for_learning'] and not m['evidence_only']
 level=r['question'][':question/difficulty'].split('/')[-1];assert level in LEVELS
 replay=g.generate(level,m['seed'],m['template'],parameters=m['parameters'],profile=m['profile'])
 assert norm(replay['question'])==norm(r['question']) and replay['generation']==m
 v.math_check(r);return fingerprint(m['parameters'],g.RECIPES[m['template']]['kind'])

def checks(r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
 if f[':answer-field/type'].endswith('/radio'):
  return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'field-owned complete bank'} for a in f[':answer-field/choices']]
 return [{'submitted':answer,'expected':'accepted','purpose':'canonical rounded numeral'},{'submitted':str(float(answer)+1),'expected':'rejected','purpose':'wrong value'},{'submitted':'2*'+answer+'/2','expected':'rejected','purpose':'documented rounding-form constraint'},{'submitted':'+'+answer,'expected':'rejected','purpose':'documented leading-plus limitation'}]
def native(records,path):
 path.mkdir(parents=True,exist_ok=True);save(path/'input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]);subprocess.run([str(OUT/'check-engine'),str(path/'input.json'),str(path/'report.json')],check=True,timeout=55)

def source_data(q):
 mid=q.get(':question/math-academy-id')
 if mid in g.RECIPES:p=copy.deepcopy(g.RECIPES[mid]['parameters']);kind=g.RECIPES[mid]['kind']
 elif mid=='q-54340':p=dict(a=10,b=6,theta=38,precision=0);kind='para'
 elif mid=='q-54338':p=dict(a=21,b=12,theta=66,precision=0);kind='para'
 else:raise AssertionError('Unclassified current source '+str(mid))
 if mid=='q-72754':p['phi']=36.4
 return p,kind

def scoped(kp,b,unavailable):
 entities={};enums={}
 def enum(x):
  ident=str(x[':db/ident']).lstrip(':')
  if ident not in enums:
   e=len(enums)+1;enums[ident]=e;entities[str(e)]={'db/ident':ident}
  return enums[ident]
 for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
  d={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]};entities[str(q[':db/id'])]=d
  if ':question/difficulty'in q:d['question/difficulty']=enum(q[':question/difficulty'])
  for f in q.get(':question/answer-fields',[]):
   d['question/answer-fields'].append(f[':db/id']);fd={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]};entities[str(f[':db/id'])]=fd
   if ':answer-field/correct'in f:fd['answer-field/correct']=f[':answer-field/correct'][':db/id']
   for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
 entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
 return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(unavailable)}

def counts(kp,b,path):
 unavailable={row[0] for hist in (False,True) for row in DB.query(USAGE_QUERY,[KP,LEARNER],path,'history' if hist else 'current',b,history=hist)}
 save(path/'snapshot.json',scoped(kp,b,unavailable));subprocess.run([str(OUT/'check-pool'),str(path/'snapshot.json'),str(path/'pool.json')],check=True,capture_output=True,text=True,timeout=55)
 pool=json.loads((path/'pool.json').read_text());ids={e for xs in pool['available_ids_by_level'].values() for e in xs};levels={l:set() for l in LEVELS};records=[];excluded=[]
 known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] not in ids:excluded.append({'id':str(q[':question/id']),'reason':'native pool excludes shown/reserved/unrated/ungradable'});continue
  l=str(q[':question/difficulty'][':db/ident']).split('/')[-1];r=known.get(str(q[':question/id']))
  if r is not None:fp=validate(r)
  else:
   p,kind=source_data(q);_,_,area=g.calculations(p,kind);expected=g.rounded(area,p['precision']);f=q[':question/answer-fields'][0];actual=f[':answer-field/correct'][':answer/value']
   if expected!=actual:
    excluded.append({'id':str(q[':question/id']),'reason':'current source mathematical answer differs','expected':expected,'actual':actual});continue
   assert sum(float(a[':answer/value'])==float(expected) for a in f[':answer-field/choices'])==1
   fp=fingerprint(p,kind);r={'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':norm(q),'generation':{'template':q[':question/math-academy-id']}}
  levels[l].add(fp);r=copy.deepcopy(r);r['question']=norm(q);records.append(r)
 native(records,path/'grading');result={'basis':b,'distinct_available':{l:len(levels[l]) for l in LEVELS},'excluded':excluded,'native_pool':pool,'deduplication':'unordered side pairs and component triangles; ignores all cosmetic identities and level'};save(path/'counts.json',result);return result

def transaction(records,kp,gid):
 forms=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 else:forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def check_report(report,path,source):
 attrs=dict(DB.attributes(path,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values());allowed={':question/'+x for x in ('id','problem','worked-solution','difficulty','answer-fields')}|{':answer-field/'+x for x in ('id','key','type','choices','correct')}|{':answer/'+x for x in ('id','type','value')}|{':question-generator/id',':question-generator/script'}
 for e,a,value,tx,s,added in report[':edb/tx-data']:
  assert s==source and added,'unexpected attribution/retraction';name=str(attrs[a])
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed

def publish(records,path):
 lib=ImageLibrary(Path(ENV['EDB_MATH_ROOT']),HERE);published=copy.deepcopy(records)
 for r in published:
  for key in (':question/problem',':question/worked-solution'):
   r['question'][key]=re.sub(r'!\[\]\(([^)]+)\)',lambda m:'![]('+lib.resolve(m[1])+')',r['question'][key])
 for item in lib.saved.values():assert sha(Path(ENV['EDB_MATH_ROOT'])/item['path'])==item['sha256']
 save(path/'asset-manifest.json',lib.saved);return published

def verify(path,intent,report):
 assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis'];check_report(report,path/'receipt-check',intent['source_eid']);b=report[':edb/db-after-t'];kp=read(path/'readback',b);old=loads((path/'before.edn').read_text());now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[q[':db/id']]==q for q in old[':knowledge-point/questions']);skip={':knowledge-point/questions',':knowledge-point/question-generator'};assert {k:v for k,v in old.items() if k not in skip}=={k:v for k,v in kp.items() if k not in skip}
 records=json.loads((path/'generated.json').read_text());published=json.loads((path/'database-generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old[':knowledge-point/questions'])+len(records)
 for raw,pub in zip(records,published):
  validate(raw);q=byid[pub['question'][':question/id']];assert ':question/math-academy-id'not in q and norm(q)==norm(pub['question'])
 for item in json.loads((path/'asset-manifest.json').read_text()).values():assert sha(Path(ENV['EDB_MATH_ROOT'])/item['path'])==item['sha256']
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 assert not transaction([],kp,intent['generator_id']);after=counts(kp,b,path/'readback/inventory');result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'source_questions_unchanged':len(old[':knowledge-point/questions']),'canonical_example_unchanged':True,'learner_history_unchanged':True,'additive_scoped_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_after':after};save(path/'verification.json',result);return result

def finish(path,verified,inv):
 prep=json.loads((path/'preparation.json').read_text());after=verified['available_after']['distinct_available'];remaining={l:max(0,5-after[l]) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':json.loads((HERE/'registration.json').read_text())['id'],'verified_commit_basis':verified['basis_after'],'lineage':LINEAGE,'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'available_before':prep['available_before']['distinct_available'],'available_after':after,'shortage_remaining':remaining,'supported_levels':list(LEVELS),'authored_levels':['easy','hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'capability_exceptions':json.loads((HERE/'capabilities.json').read_text()),'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'preparation.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'asset-manifest.json',path/'generated.json',path/'inventory-after.json',OUT/'current-native-build.json',OUT/'current-replay-native-report.json',HERE/'freeze.json',HERE/'validation.json',HERE/'classification-current.md'] if p.exists()]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','new_questions','new_by_level','verified_commit_basis','available_after','shortage_remaining')},indent=2),flush=True)

def prepare(preview):
 for path in sorted(OUT.glob('basis-*')):
  if not (path/'commit-intent.json').exists():continue
  intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['connection_sha256']==hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest();assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
  inventory(path/'recovery-inventory.json');verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,verified,inventory(path/'inventory-after.json'));return
 inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b;path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
 captured=loads((OUT/'initial/kp.edn').read_text())[0][0];assert kp==captured,'Current source changed; reclassify first'
 (path/'before.edn').write_text(dumps(kp)+'\n');c=counts(kp,b,path/'inventory-before');needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS};print(json.dumps({'basis':b,'available':c['distinct_available'],'needed':needed}),flush=True)
 source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
 gen=kp.get(':knowledge-point/question-generator');existing=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-script',b)
 identity=json.loads((HERE/'registration.json').read_text()) if (HERE/'registration.json').exists() else {}
 gid=str(gen[':question-generator/id']) if gen else str(existing[0][0][':question-generator/id']) if existing else identity.get('id',str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator')))
 collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-id',b)
 assert len(existing)<=1 and (not collision or collision[0][0][':question-generator/script']==SCRIPT)
 save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing or identity)})
 supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
 for r in instances:validate(r)
 save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
 used=set()
 for q in kp[':knowledge-point/questions']:
  if q.get(':question/math-academy-id'):p,kind=source_data(q);used.add(fingerprint(p,kind))
  else:raise AssertionError('Unreconciled existing generated content')
 # Canonical diagram: 42,35 at B36 degrees; 20,18 at D80 degrees.
 used.add(fingerprint(dict(a=42,b=35,theta=36,c=20,d=18,phi=80,precision=1),'general'))
 records=[];added={l:0 for l in LEVELS};rejected=[]
 for l in LEVELS:
  for candidate in [r for r in instances if r['question'][':question/difficulty'].endswith('/'+l)]:
   fp=validate(candidate)
   if added[l]<needed[l] and fp not in used:records.append(candidate);used.add(fp);added[l]+=1
  for i in range(1000):
   if added[l]>=needed[l]:break
   r=g.generate(l,int(JOB.name[:8],16)+i);fp=validate(r)
   if fp in used:rejected.append({'level':l,'seed':r['generation']['seed'],'reason':'duplicate mathematical task'});continue
   records.append(r);used.add(fp);added[l]+=1
 save(path/'generated.json',records);(path/'generated.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n');native(records,path/'selected-grading')
 published=publish(records,path);save(path/'database-generated.json',published);native(published,path/'published-grading')
 ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
 assert len(ids)==len(set(ids))
 if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'new-identities',b)
 save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_before':c,'needed':needed,'new_by_level':added,'finite_shortages':{l:needed[l]-added[l] for l in LEVELS if needed[l]>added[l]},'duplicate_candidates_rejected':rejected,'generator_sha256':sha(HERE.with_suffix('.py')),'mathematics_validated':True,'actual_grader_validated':True,'new_questions':len(records)})
 forms=transaction(published,kp,gid)
 if not forms:
  verified={'basis_after':b,'new_questions':0,'available_after':c};save(path/'verification.json',verified);finish(path,verified,inv);return
 tx=dumps(forms)+'\n';txpath=path/'transaction.edn'
 with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
 result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,capture_output=True,text=True,check=True,timeout=55);(path/'preview.edn').write_text(result.stdout);pr=loads(result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
 if '--prepare-only' in sys.argv:
  print(json.dumps({'prepared_at_basis':b,'new_by_level':added,'preview_passed':True,'path':str(path)}),flush=True);return
 intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'quadrilateral-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK)};save(path/'commit-intent.json',intent)
 verified=verify(path,intent,DB._commit(intent,txpath,path));finish(path,verified,inventory(path/'inventory-after.json'))

def main():
 frozen=json.loads((HERE/'freeze.json').read_text());assert all(sha(ROOT/rel)==digest for rel,digest in frozen['files'].items());assert json.loads((HERE/'validation.json').read_text())['status']=='pass'
 subprocess.run([str(OUT/'check-engine'),str(HERE/'engine-input.json'),str(OUT/'current-replay-native-report.json')],check=True,timeout=55)
 preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired; checking fresh basis',flush=True)
  prepare(preview)
if __name__=='__main__':main()
