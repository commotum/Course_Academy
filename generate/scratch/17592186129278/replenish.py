"""Scoped additive replenishment; exact requests survive unknown outcomes."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, image_path
from math_format import validate_generated_record
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'60c1b8f81e8cb256743ce9b90a4977cafdb145d2ac3a309fe0f9baa652827483'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
ENV=database_environment('math');MATH_ROOT=Path(ENV['EDB_MATH_ROOT'])
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7';ENGINE=HERE/'reference/check-engine'
QUERY=(HERE/'reference/initial/kp-query.edn').read_text()
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
 (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
 (and [?l :learner/activity ?t] [?t :learner-task/status ?st]
 (or [?st :db/ident :learner-task.status/started] [?st :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
SOURCE_ISSUES={17592186367694:'Source worked solution omits the squared sine term in Cartesian substitution; preserve original and exclude from validated reserve.',17592186411857:'Source worked solution has a mismatched parenthesis in its endpoint evaluation; preserve original and exclude from validated reserve.'}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(value):
 if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
 if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
 if isinstance(value,uuid.UUID):return str(value)
 return value

def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
 obj=json.loads(r.stdout);assert obj['ok'] and obj['data']['lineage']==LINEAGE;save(path,obj['data']);return obj['data']
def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'All field-owned radio choices'} for a in f[':answer-field/choices']]
def native_check(records,path,prefix):
 save(path/(prefix+'-input.json'),[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records])
 subprocess.run([str(ENGINE),str(path/(prefix+'-input.json')),str(path/(prefix+'-report.json'))],check=True)
 assert json.loads((path/(prefix+'-report.json')).read_text())['documented_unresolved_checks']==0

def normalize(q):
 q=copy.deepcopy(q)
 for key in list(q):
  if key==':db/id' or key.startswith(':knowledge-point/'):q.pop(key)
 q[':question/id']=str(q[':question/id'])
 if ':question/difficulty' in q:q[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
 for f in q[':question/answer-fields']:
  f.pop(':db/id',None);f[':answer-field/id']=str(f[':answer-field/id']);f[':answer-field/type']=str(f[':answer-field/type'][':db/ident'])
  if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
  for a in f[':answer-field/choices']:
   a.pop(':db/id',None);a[':answer/id']=str(a[':answer/id']);a[':answer/type']=str(a[':answer/type'][':db/ident'])
 return q

def math_key(e):
 e=sp.sympify(e)
 if e.is_Pow and not e.exp.is_Integer:return ['power',math_key(e.base),str(e.exp)]
 return str(sp.expand(sp.expand(sp.expand_trig(e)).subs(sp.sin(g.t)**2,1-sp.cos(g.t)**2)))

def fingerprint(F,bounds):
 return g.digest({'assessed':math_key(F),'bounds':[math_key(e) for e in bounds]})

def model_fingerprint(f,p):
 m=g.model(f,p)
 return fingerprint(m['F'],[m[k] for k in ('R','a','d','low','high')])

def rendered_fingerprint(q):
 problem=q[':question/problem']
 cart=g.parse_tex(re.search(r'\\iiint_R (.*?)\\,\\mathrm\{d\}V',problem).group(1))
 n=sp.Integer(re.search(r'cylinder \$x\^2\+y\^2=(\d+)\$',problem).group(1))
 low,high=map(g.parse_tex,re.search(r'surfaces \$z=(.*?)\$ and \$z=(.*?)\.\$',problem).groups())
 replacement={g.x:g.r*sp.cos(g.t),g.y:g.r*sp.sin(g.t)}
 F=sp.trigsimp(cart.subs(replacement,simultaneous=True)*g.r)
 low,high=(sp.trigsimp(e.subs(replacement,simultaneous=True)) for e in (low,high))
 a,d=(0,sp.pi/2) if 'for $x\\ge 0,$ $y\\ge 0$' in problem else (-sp.pi/2,sp.pi/2) if 'for $x\\ge 0$' in problem else (0,sp.pi) if 'for $y\\ge 0$' in problem else (0,2*sp.pi)
 return fingerprint(F,(sp.sqrt(n),a,d,low,high))

def task(q):
 sid=q.get(':db/id')
 if sid in g.SOURCES:
  f=next(f for f,(_,s,_) in g.SPECS.items() if s==sid)
  return model_fingerprint(f,g.SPECS[f][2])
 return rendered_fingerprint(q)

def unpublish(r):
 r=copy.deepcopy(r)
 for a in r.get('generation',{}).get('assets',[]):
  assert sha(MATH_ROOT/a['path'])==a['sha256']
  r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(a['path'],a['local_path'])
 return r

def validate(r):
 assert r['knowledge_point']['db_id']==KP and r['knowledge_point']['id']==g.KP[':knowledge-point/id']
 meta=r['generation'];assert meta['eligible_for_learning'] and not meta['evidence_only'] and meta['profile']=='method_bank'
 assert r['question'][':question/difficulty']==':question.difficulty/'+meta['level']
 g.eligible(meta['template'],meta['parameters'])
 v.displayed_math(r);validate_generated_record(r)
 expected=g.generate(meta['level'],seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
 assert canonical(unpublish(r)['question'])==canonical(expected['question']),'Output differs from deterministic validated generator'
 assert rendered_fingerprint(r['question'])==model_fingerprint(meta['template'],meta['parameters'])
 assert meta['mathematical_fingerprint']==expected['generation']['mathematical_fingerprint']
 return r

def record_for(q):
 if q[':db/id'] in g.SOURCES:
  original=g.SOURCES[q[':db/id']];assert canonical(q)==canonical(original),'Source changed; reclassify'
  f=next(f for f,(_,sid,_) in g.SPECS.items() if sid==q[':db/id']);_,_,p=g.SPECS[f]
  r={'knowledge_point':{'db_id':KP,'id':g.KP[':knowledge-point/id'],'title':g.KP[':knowledge-point/title']},'question':normalize(q),'generation':{'template':f}}
  field=r['question'][':question/answer-fields'][0];values=[g.parse_tex(a[':answer/value']) for a in field[':answer-field/choices']]
  actual=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
  v.eq(g.parse_tex(actual),g.stages(f,**p)[-1]);assert all(sp.simplify(a-b)!=0 for i,a in enumerate(values) for b in values[:i])
  assert q.get(':question/worked-solution')
  return r
 candidates=[r for file in OUT.glob('basis-*/generated.json') for r in json.loads(file.read_text())]
 r=next(copy.deepcopy(r) for r in candidates if r['question'][':question/id']==str(q[':question/id']))
 assert canonical(normalize(q))==canonical(r['question']);validate(r);return r

def count(kp,path,basis):
 unavailable={row[0] for row in DB.query(USAGE,[KP,LEARNER],path,'usage',basis)}
 unavailable.update(row[0] for row in DB.query(USAGE,[KP,LEARNER],path,'usage-history',basis,history=True))
 rows={l:[] for l in LEVELS};excluded=[];records=[]
 for q in kp[':knowledge-point/questions']:
  level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
  if q[':db/id'] in unavailable:reason='Previously shown or reserved, including retained history'
  elif level not in LEVELS:reason='Unrated: excluded from difficulty-weighted validated reserve'
  elif q[':db/id'] in SOURCE_ISSUES:reason=SOURCE_ISSUES[q[':db/id']]
  else:
   r=record_for(q);records.append(r);rows[level].append(q);continue
  excluded.append({'db_id':q[':db/id'],'reason':reason})
 native_check(records,path,'inventory-grade')
 result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({task(q) for q in qs}),'available_question_ids':[str(q[':question/id']) for q in qs]} for l,qs in rows.items()},'excluded_shown_or_reserved':sorted(unavailable),'excluded_questions':excluded}
 save(path/'available-counts.json',result);return result

def source_check(kp):
 before={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 for q in g.KP[':knowledge-point/questions']:assert canonical(before[q[':db/id']])==canonical(q),'Source changed; reclassify'
 assert canonical(kp[':knowledge-point/canonical-example'])==canonical(g.KP[':knowledge-point/canonical-example'])
 assert str(kp[':knowledge-point/id'])==g.KP[':knowledge-point/id']

def generate_candidates(kp,counts,path):
 needed={l:max(0,5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS}
 supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
 instances=supplied.get('instances',[]);assert isinstance(instances,list)
 for r in instances:validate(r)
 save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
 used={task(q) for q in kp[':knowledge-point/questions']};records=[];added={l:0 for l in LEVELS}
 def consider(r):
  l=r['generation']['level'];fp=rendered_fingerprint(r['question'])
  if added[l]<needed[l] and fp not in used:
   validate(r);records.append(r);used.add(fp);added[l]+=1
 for r in instances:consider(r)
 for l in LEVELS:
  for offset in range(1000):
   if added[l]>=needed[l]:break
   consider(g.generate(l,seed=int(JOB.name[:8],16)+offset))
 save(path/'candidates.json',records);native_check(records,path,'native')
 save(path/'generation.json',{'basis':counts['basis'],'missing_by_level':needed,'new_by_level':added,'finite_shortages':{l:needed[l]-added[l] for l in LEVELS},'source_solution_exclusions':SOURCE_ISSUES})
 return records

def publish(records,path):
 library=ImageLibrary(MATH_ROOT,HERE);records=copy.deepcopy(records)
 for r in records:
  q=r['question'];local=q[':question/worked-solution'];q[':question/worked-solution']=library.text(local)
  refs=re.findall(r'!\[.*?\]\((.*?)\)',local)
  r['generation']['assets']=[{'local_path':a,**library.saved[a]} for a in refs]
  for a in r['generation']['assets']:
   assert sha(Path(a['local_path']))==a['sha256']==sha(MATH_ROOT/a['path'])
   assert image_path(a['path'],MATH_ROOT)==(MATH_ROOT/a['path']).resolve()
  validate(r)
 save(path/'assets.json',library.saved);return records

def transaction(records,kp,gid):
 forms=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if not gen:
  forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def check_report(report,path,source):
 attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,value,tx,src,added in report[':edb/tx-data']:
  assert src==source and added,'Unexpected source or retraction'
  name=attrs[a]
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected existing entity or attribute'

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_report(report,path/'receipt-check',intent['source_eid'])
 basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis);old=loads((path/'before.edn').read_text());byid={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(canonical(byid[q[':db/id']])==canonical(q) for q in old[':knowledge-point/questions'])
 assert canonical({k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:v for k,v in old.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());questions={str(q[':question/id']):q for q in byid.values()};assert len(byid)==len(old[':knowledge-point/questions'])+len(records)
 for r in records:
  q=questions[r['question'][':question/id']];assert canonical(normalize(q))==canonical(r['question']);assert ':question/math-academy-id' not in q;validate(r)
 assert not transaction([],kp,intent['generator_id'])
 counts=count(kp,path/'readback',basis)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old[':knowledge-point/questions']),'source_and_learner_history_preserved':True,'only_scoped_additive_content_datoms':True,'generator_registration_verified':True,'asset_bytes_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':counts}
 save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
 prep=json.loads((path/'preparation.json').read_text());counts=verified['available_counts_after'];remaining={l:max(0,5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified.get('basis_after') if verified.get('committed',True) else None,'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'available_counts_before':prep['available_counts'],'available_counts_after':counts,'shortage_remaining':remaining,'unsupported_levels_filled':False,'capability_exceptions':[],'source_errors_excluded':SOURCE_ISSUES,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'native-report.json',path/'assets.json',path/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'validation-freeze.json'] if p.exists()]}
 if any(remaining.values()):result['capability_exceptions']=[{'difficulty':l,'status':'finite-limit','shortage_remaining':remaining[l],'reason':'Bounded 1000-seed search of declared supported domains exhausted without distinct valid candidates','domain_evidence':str((HERE/'validation.json').relative_to(ROOT))} for l in LEVELS if remaining[l]]
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','new_by_level','shortage_remaining')}),flush=True)

def prepare():
 path=OUT/'pre-generation';path.mkdir(exist_ok=True)
 inv=inventory(path/'inventory.json');basis=inv['basis'];kp=read_kp(path,basis);source_check(kp)
 counts=count(kp,path,basis);records=generate_candidates(kp,counts,path)
 (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
 print(json.dumps({'basis':basis,'available':{l:counts['levels'][l]['distinct_available_tasks'] for l in LEVELS},'new_questions':len(records),'generation':json.loads((path/'generation.json').read_text())}),flush=True)

def main():
 if '--prepare' in sys.argv:prepare();return
 freeze=json.loads((HERE/'validation-freeze.json').read_text());assert freeze['status']=='passed'
 for name,digest in freeze['hashes'].items():assert sha(ROOT/name)==digest,'Validated inputs changed'
 preview=preview_executable(SimpleNamespace(math_root=MATH_ROOT,repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    inventory(path/'recovery-inventory.json')
    verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-under-lock.json');basis=inv['basis'];assert DB.basis()==basis;path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True)
  kp=read_kp(path,basis);source_check(kp);(path/'before.edn').write_text(dumps(kp)+'\n')
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');existing=DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-identity',basis)
  assert len(existing)<=1
  gid=str(gen[':question-generator/id']) if gen else str(existing[0][1]) if existing else str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'question-generator'))
  if gen:assert gen[':question-generator/script']==SCRIPT and (not existing or existing[0][0]==gen[':db/id'])
  byid=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-uuid',basis)
  if byid:assert byid[0][0].get(':question-generator/script',SCRIPT)==SCRIPT
  counts=count(kp,path,basis);needed={l:max(0,5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS}
  candidates=json.loads((OUT/'pre-generation/candidates.json').read_text());used={task(q) for q in kp[':knowledge-point/questions']};records=[];added={l:0 for l in LEVELS}
  for r in candidates:
   validate(r);l=r['generation']['level'];fp=rendered_fingerprint(r['question'])
   if added[l]<needed[l] and fp not in used:records.append(r);used.add(fp);added[l]+=1
  # A changed basis can require additional candidates. Recheck and validate them here.
  for l in LEVELS:
   for offset in range(1000):
    if added[l]>=needed[l]:break
    r=g.generate(l,seed=int(JOB.name[:8],16)+1000+offset);fp=rendered_fingerprint(r['question'])
    if fp not in used:validate(r);records.append(r);used.add(fp);added[l]+=1
  ids=[uuid.UUID(i) for r in records for i in [r['question'][':question/id'],r['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]]
  matches=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else [];assert not matches,'Identity collision requires reconciliation'
  records=publish(records,path);save(path/'generated.json',records);native_check(records,path,'native')
  save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':counts,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({rendered_fingerprint(r['question']) for r in records}),'asset_hashes':json.loads((path/'assets.json').read_text()),'source_basis':g.SOURCE['basis'],'source_evidence_unchanged':True,'generator_id':gid,'generator_path':SCRIPT,'lock':str(ROOT/'.local/learning/requests/math/api.lock'),'shortage_remaining':{l:max(0,needed[l]-added[l]) for l in LEVELS}})
  forms=transaction(records,kp,gid)
  if not forms:
   verified={'passed':True,'committed':False,'basis_after':basis,'new_questions':0,'available_counts_after':counts};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
  txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  assert DB.basis()==basis,'Basis changed while api.lock held; return to preparation'
  preview_result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
  (path/'preview.edn').write_text(preview_result.stdout);pr=loads(preview_result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'cylindrical-evaluation-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent);verified=verify(path,intent,DB._commit(intent,txpath,path));finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
