"""Additive, exact-request inventory replenishment for this KP only."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP;LEVELS=g.SUPPORTED_LEVELS;SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.CAPTURE['lineage'];SOURCE=':application/ca-engine'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'7b89050a9326e46c726997f93ae1f3599b7dd6067aba2660e1d73853e4b22280'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
DB.env=ENV
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7'
QUERY='''[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example [*]} {[:knowledge-point/questions :limit nil] [* {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/correct [* {:answer/type [:db/ident]}]} {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'''
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
 (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
 (and [?l :learner/activity ?t] [?t :learner-task/status ?st]
 (or [?st :db/ident :learner-task.status/started] [?st :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
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
def displayed(q):
 """Read actual printed function, point and direction without generator parameters."""
 t=q[':question/problem']
 pt=re.search(r'point\s+\$A?\((-?\d+),\s*(-?\d+)\)',t);assert pt,'missing point'
 A,B=map(s.Integer,pt.groups())
 if 'The gradient of' in t:
  E=v.vectors(t)[0];F=None
 else:
  expr=re.search(r'[fg]\(x,\s*y\)\s*=\s*([^$]+)',t);assert expr,'missing function'
  assert 'div' not in expr[1], 'source missing prior-part vector field/gradient'
  F=v.math(expr[1]);E=[s.simplify(s.diff(F,z).subs({v.x:A,v.y:B})) for z in (v.x,v.y)]
 if 'towards' in t:
  ep=re.search(r'B\(([^,]+),\s*([^)]+)\)',t);assert ep
  dx,dy=[v.math(z) for z in ep.groups()];dx-=A;dy-=B
 else:
  vt=re.search(r'v\s*=\s*([^$]+)',t);assert vt
  m=re.fullmatch(r'(.*?)i\s*(.*?)j',vt[1].rstrip('.').replace(r'\,',''));assert m
  dx=v.math(m[1] or '1');dy=v.math(m[2] if m[2] not in ('+','-') else m[2]+'1')
 N=s.sqrt(dx*dx+dy*dy);assert N!=0
 C=s.simplify((E[0]*dx+E[1]*dy)/N)
 return F,E,A,B,dx,dy,N,C

def task(q):
 F,E,A,B,dx,dy,N,C=displayed(q)
 data=[s.srepr(s.expand(F)),str(A),str(B)] if F is not None else ['given-gradient',*[s.srepr(z) for z in E]]
 return g.fingerprint(data+[s.srepr(s.simplify(dx/N)),s.srepr(s.simplify(dy/N))])

def native_checks(r):
 f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'entire radio bank'} for a in f[':answer-field/choices']]
 F,E,A,B,dx,dy,N,C=displayed(r['question'])
 return [{'submitted':g.tex(C),'expected':'accepted','purpose':'canonical blank'}, {'submitted':str(C),'expected':'accepted','purpose':'equivalent exact blank'}, {'submitted':g.tex(C+1),'expected':'rejected','purpose':'wrong blank'}]

def validate_bank(q):
 F,E,A,B,dx,dy,N,C=displayed(q)
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 kind=str(f[':answer-field/type'][':db/ident']);answers=f[':answer-field/choices'];vals=[v.math(a[':answer/value']) for a in answers]
 assert len(vals)==(5 if kind.endswith('/radio') else 1)
 assert all(not v.equal(a,b) for i,a in enumerate(vals) for b in vals[i+1:])
 matches=[a for a,z in zip(answers,vals) if v.equal(z,C)]
 assert len(matches)==1 and str(matches[0][':answer/id'])==str(f[':answer-field/correct'][':answer/id'])
 assert q[':question/worked-solution']
 return C

def count(kp,path,basis):
 unavailable={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'usage',basis)}
 rows={l:[] for l in LEVELS};excluded=[];native=[]
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] in unavailable:continue
  try:
   level=str(q[':question/difficulty'][':db/ident']).split('/')[-1];assert level in rows
   validate_bank(q);rows[level].append(q)
   rec={'question':flatten(q),'knowledge_point':{'title':g.REC[':knowledge-point/title']},'generation':{'template':'current-source'}};native.append({'label':str(q[':question/id']),'record':rec,'checks':native_checks(rec)})
  except (AssertionError,KeyError,ValueError,TypeError) as exc:
   excluded.append({'id':str(q[':question/id']),'reason':str(exc)})
 if native:
  save(path/'inventory-native-input.json',native)
  subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'inventory-native-input.json'),str(path/'inventory-native-report.json')],check=True,capture_output=True,text=True)
 result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({task(q) for q in qs}),'available_question_ids':[str(q[':question/id']) for q in qs]} for l,qs in rows.items()},'excluded_shown_or_reserved':sorted(unavailable),'excluded_invalid_or_unrated':excluded}
 save(path/'available-counts.json',result);return result

def flatten(q):
 q=copy.deepcopy(q)
 for k in list(q):
  if k==':db/id' or k.startswith(':knowledge-point/'):q.pop(k)
 q[':question/id']=str(q[':question/id']);q[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
 for f in q[':question/answer-fields']:
  f.pop(':db/id',None);f[':answer-field/id']=str(f[':answer-field/id']);f[':answer-field/type']=str(f[':answer-field/type'][':db/ident']);f[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
  for a in f[':answer-field/choices']:
   a.pop(':db/id',None);a[':answer/id']=str(a[':answer/id']);a[':answer/type']=str(a[':answer/type'][':db/ident'])
 return q

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
 if not gen and kp.get(':knowledge-point/question-generator-reuse'):
  forms.append([kw('db/add'),KP,kw('knowledge-point/question-generator'),[kw('question-generator/id'),uuid.UUID(gid)]])
 elif not gen:
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
def normalize(q):
 q=copy.deepcopy(q)
 for key in list(q):
  if key==':db/id' or key.startswith(':knowledge-point/'):q.pop(key)
 q[':question/id']=str(q[':question/id']);q[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
 for f in q[':question/answer-fields']:
  f.pop(':db/id',None);f[':answer-field/id']=str(f[':answer-field/id']);f[':answer-field/type']=str(f[':answer-field/type'][':db/ident']);f[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
  for a in f[':answer-field/choices']:
   a.pop(':db/id',None);a[':answer/id']=str(a[':answer/id']);a[':answer/type']=str(a[':answer/type'][':db/ident'])
 return canonical(q)
def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_report(report,path/'receipt-check',intent['source_eid'])
 basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis);old=loads((path/'before.edn').read_text());byid={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(canonical(byid[q[':db/id']])==canonical(q) for q in old[':knowledge-point/questions'])
 assert canonical({k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:v for k,v in old.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());questions={str(q[':question/id']):q for q in byid.values()};assert len(byid)==len(old[':knowledge-point/questions'])+len(records)
 for r in records:
  q=questions[r['question'][':question/id']];assert normalize(q)==canonical(r['question']);assert ':question/math-academy-id' not in q;v.check_normal(r)
 assert not transaction([],kp,intent['generator_id'])
 counts=count(kp,path/'readback',basis)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old[':knowledge-point/questions']),'source_and_learner_history_preserved':True,'only_scoped_additive_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':counts}
 save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
 prep=json.loads((path/'preparation.json').read_text());counts=verified['available_counts_after'];remaining={l:max(0,5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'available_counts_before':prep['available_counts'],'available_counts_after':counts,'shortage_remaining':remaining,'unsupported_levels_filled':False,'unsupported_levels':['hard'],'unsupported_shortage':{'hard':5},'capability_exceptions':json.loads((HERE/'capability.json').read_text())['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'native-report.json',path/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'validation-freeze.json',HERE/'slot-validation.json',HERE/'capability.json',HERE/'reference/initial/current-source-validation.json'] if p.exists()]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def main():
 freeze=json.loads((HERE/'validation-freeze.json').read_text());assert freeze['status']=='passed'
 for name,digest in freeze['hashes'].items():assert sha(ROOT/name)==digest,'Validated inputs changed'
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis;path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True)
  kp=read_kp(path,basis);(path/'before.edn').write_text(dumps(kp)+'\n')
  captured=loads((HERE/'reference/initial/kp-record.edn').read_text())
  original={q[':db/id']:q for q in kp[':knowledge-point/questions']}
  assert {q.get(':question/math-academy-id') for q in kp[':knowledge-point/questions'] if q.get(':question/math-academy-id')}=={q.get(':question/math-academy-id') for q in captured[':knowledge-point/questions'] if q.get(':question/math-academy-id')}, 'New source evidence; reclassify'
  assert all(canonical(original[q[':db/id']])==canonical(q) for q in captured[':knowledge-point/questions']), 'Source evidence changed; reclassify'
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');existing=DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-identity',basis)
  gid=str(gen[':question-generator/id']) if gen else str(existing[0][1]) if existing else str(uuid.uuid5(uuid.UUID(g.REC[':knowledge-point/id']),'question-generator'))
  assert len(existing)<=1
  by_uuid=DB.query('[:find ?e ?script :in $ ?id :where [?e :question-generator/id ?id] [?e :question-generator/script ?script]]',[uuid.UUID(gid)],path,'generator-uuid',basis)
  assert not by_uuid or len(by_uuid)==1 and by_uuid[0][1]==SCRIPT,'Generator UUID belongs to another package'
  reg=HERE/'registration.json'
  if reg.exists():assert json.loads(reg.read_text())['id']==gid
  else:save(reg,{'id':gid,'script':SCRIPT})
  if gen:assert gen[':question-generator/script']==SCRIPT
  if not gen and existing:kp[':knowledge-point/question-generator-reuse']=existing[0][0]
  counts=count(kp,path,basis);needed={l:max(0,5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS};used=set()
  for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
   try:used.add(task(q))
   except (AssertionError,ValueError,KeyError):pass
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
  for r in instances:v.check_normal(r);assert r['generation']['eligible_for_learning'] and r['knowledge_point']['db_id']==KP
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
  records=[];added={l:0 for l in LEVELS}
  def consider(r):
   l=r['question'][':question/difficulty'].split('/')[-1];fp=task(r['question'])
   if added[l]<needed[l] and fp not in used:
    v.check_normal(r);records.append(r);used.add(fp);added[l]+=1
  for r in instances:consider(r)
  for l in LEVELS:
   for offset in range(1000):
    if added[l]>=needed[l]:break
    consider(g.generate(l,seed=int(JOB.name[:8],16)+offset,template='exp' if l=='moderate' else None))
  save(path/'bounded-search.json',{'attempt_limit_per_level':1000,'missing':{l:needed[l]-added[l] for l in LEVELS},'exception':'finite search exhausted' if any(added[l]<needed[l] for l in LEVELS) else None})
  ids=[uuid.UUID(i) for r in records for i in [r['question'][':question/id'],r['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]]
  matches=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else [];assert not matches,'Identity collision requires reconciliation'
  save(path/'generated.json',records);save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':native_checks(r)} for r in records])
  subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
  save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':counts,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({task(r['question']) for r in records}),'asset_hashes':[],'source_basis':json.loads((HERE/'reference/initial/inventory.json').read_text())['basis'],'source_evidence_unchanged':True,'generator_id':gid,'generator_path':SCRIPT})
  forms=transaction(records,kp,gid)
  if not forms:
   verified={'passed':True,'basis_after':basis,'new_questions':0,'available_counts_after':counts};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
  txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  preview_result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
  (path/'preview.edn').write_text(preview_result.stdout);pr=loads(preview_result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'directional-derivative-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'generator_version':g.VERSION,'generated_sha256':sha(path/'generated.json'),'validation_freeze_sha256':sha(HERE/'validation-freeze.json'),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent);verified=verify(path,intent,DB._commit(intent,txpath,path));finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
