"""Validate and replenish only Calculating the Determinant of a 3x3 Matrix, with durable EDB receipts."""
import argparse,copy,fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path[:0]=[str(ROOT),str(H),str(ROOT/'scripts')]
from capture.scripts.database.preview import preview_executable
from db_support import DB,ENV,KP,read,dumps,loads,kw,plain
from inventory_jobs import save
spec=importlib.util.spec_from_file_location('determinant_validation',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(H.with_suffix('.py').relative_to(ROOT));OUT=H/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'3c4c1e3ac7b0bef5d0bf5895f73d117caed55ec14e5e050560fdf54b04906b37'
LOCK=ROOT/'.local/learning/requests/math/api.lock';LEVELS=('easy','moderate','hard')
ENGINE=OUT/'check-engine'
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?s] (or [?s :db/ident :learner-task.status/started] [?s :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):
 if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
 if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
 return str(x) if isinstance(x,uuid.UUID) else x
def source_shape(x):
 if isinstance(x,str):
  import re
  return re.sub(r'\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',lambda m:r'\begin{bmatrix}'+m[1]+r'\end{bmatrix}',x,flags=re.S)
 if isinstance(x,dict):return {str(k):source_shape(z) for k,z in x.items() if not (':db/ident' in x and str(k)==':db/id')}
 if isinstance(x,(list,tuple)):return sorted([source_shape(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
 return str(x) if isinstance(x,uuid.UUID) else x
def inventory(path):
 native=Path((OUT/'native-learning-path.txt').read_text())
 p=subprocess.run([str(native),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,text=True,capture_output=True,check=True,timeout=55)
 r=json.loads(p.stdout);assert r['ok'];data=r['data'];assert data['lineage']==LINEAGE;save(path,data);return data

def question_record(q):
 x={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
 x[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);x[':question/answer-fields']=[]
 for f in sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']):
  x[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])]})
 return x

def matrix_entries(q):
 import re
 for text in (q[':question/problem'], q.get(':question/worked-solution','')):
  match=re.search(r'\\begin\{(?:aligned|vmatrix|bmatrix)\}(.*?)\\end\{(?:aligned|vmatrix|bmatrix)\}',text,re.S)
  if match:
   values=list(map(int,re.findall(r'-?\d+',match[1])))
   if len(values)==9:return values
 raise ValueError('No complete printed 3x3 matrix')
def fingerprint(q):
 # Only matrix entries establish a fresh determinant task; ignore labels,
 # formatting, answer shape/bank, seed, identities and difficulty.
 return g.digest({'matrix':matrix_entries(q)})

def validate(r):
 assert r['knowledge_point']['db_id']==KP and r['knowledge_point']['id']==g.KP_UUID
 v.check_record(r);md=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
 replay=g.generate(level,md['seed'],template=md['template'],profile=md['bank_profile'],parameters=md['parameters'])
 assert canonical(replay['question'])==canonical(r['question']), 'Generated content differs from deterministic replay'
 return fingerprint(r['question'])

def original_record(q):
 cases=json.loads((H/'source-cases.json').read_text())
 case=next(c for c in cases if c['source_id']==q[':question/math-academy-id'])
 r=g.generate(case['level'],template=case['template'],profile=case['bank_profile'],parameters=case['parameters'])
 v.check_record(r)
 actual=question_record(q);expected=v.independent_det(matrix_entries(actual))
 assert matrix_entries(actual)==case['parameters']['matrix']
 assert all(row==expected for row in v.arithmetic_solution_values(actual[':question/worked-solution'])), 'Erroneous source worked row; preserved and excluded'
 for a,b in zip(actual[':question/answer-fields'],r['question'][':question/answer-fields']):
  assert a[':answer-field/type']==b[':answer-field/type'] and a[':answer-field/key']==b[':answer-field/key']
  assert sorted(int(z[':answer/value']) for z in a[':answer-field/choices'])==sorted(int(z[':answer/value']) for z in b[':answer-field/choices'])
  assert next(int(z[':answer/value']) for z in a[':answer-field/choices'] if z[':answer/id']==a[':answer-field/correct'][1])==expected
 r['question']=actual;return r

def grade(records,path):
 path.mkdir(parents=True,exist_ok=True);items=[]
 for r in records:
  checks=[]
  expected=v.independent_det(matrix_entries(r['question']))
  for i,f in enumerate(r['question'][':question/answer-fields']):
   if f[':answer-field/type'].endswith('/radio'):
    checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'All actual displayed choices'} for a in f[':answer-field/choices'])
   else:
    checks.extend({'field_index':i,'submitted':value,'expected':outcome,'purpose':purpose} for value,outcome,purpose in [(str(expected),'accepted','Canonical integer'),(str(expected)+' + 0','accepted','Equivalent expression'),(str(expected+1),'rejected','Wrong integer')])
  items.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
 save(path/'native-input.json',items)
 subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],check=True,timeout=55)
 report=json.loads((path/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
 assert report['accepted_checks']+report['rejected_checks']==sum(len(item['checks']) for item in items)
 return report

def refresh(kp,path,basis):
 assert str(kp[':knowledge-point/id'])==g.KP_UUID
 captured=json.loads((H/'source.json').read_text())['record'];old={q[':db/id']:q for q in captured[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(source_shape(q)==source_shape(now[e]) for e,q in old.items()), 'Source changed; reclassification required'
 assert source_shape(captured[':knowledge-point/canonical-example'])==source_shape(kp[':knowledge-point/canonical-example'])
 save(path/'source-refresh.json',{'passed':True,'basis':basis,'captured_basis':g.SOURCE['basis'],'practice_questions_preserved':len(old),'equivalent_bracket_notation_changes':[q[':question/math-academy-id'] for e,q in old.items() if canonical(q)!=canonical(now[e]) and q[':question/problem']!=now[e][':question/problem']],'canonical_unchanged':True,'comparison':'Exact content except equivalent [aligned] to bmatrix notation and optional enum db IDs'})

def counts(kp,path,basis):
 shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
 shown.update(r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'currently-shown',basis))
 reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
 canonical_id=kp[':knowledge-point/canonical-example'][':db/id'];pool={l:set() for l in LEVELS};records=[];excluded=[]
 known={r['question'][':question/id']:r for p in OUT.glob('basis-*/generated.json') for r in json.loads(p.read_text())}
 for q in kp[':knowledge-point/questions']:
  level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
  if q[':db/id'] in shown|reserved|{canonical_id} or level not in LEVELS:
   excluded.append({'id':q[':db/id'],'reason':'Shown, reserved, canonical or unrated'});continue
  if ':question/math-academy-id' in q:
   try:r=original_record(q)
   except (AssertionError, KeyError, ValueError) as e:
    excluded.append({'id':q[':db/id'],'reason':'Source invalid or incomplete: '+str(e)});continue
  else:
   r=copy.deepcopy(known[str(q[':question/id'])]);assert canonical(r['question'])==canonical(question_record(q));validate(r)
  records.append(r);pool[level].add(fingerprint(q))
 grade(records,path)
 result={'basis':basis,'distinct_available':{l:len(z) for l,z in pool.items()},'shown':sorted(shown),'reserved':sorted(reserved),'excluded':excluded,'deduplication':'exact matrix entries, excluding names, UUIDs, answer shapes/banks, seed, order and difficulty','validation':'Independent rendered determinant/cofactor/key check plus actual native grader'}
 save(path/'available-counts.json',result);return result

def prepare():
 inv=inventory(OUT/'inventory-prepare.json');b=inv['basis'];kp=read(b,OUT/'prepare');refresh(kp,OUT/'prepare',b);c=counts(kp,OUT/'prepare',b)
 supplied=JOB.with_suffix('.generated');raw=json.loads(supplied.read_text()) if supplied.exists() else {};instances=raw.get('instances',[]) if isinstance(raw,dict) else raw
 if isinstance(instances,dict):instances=[instances]
 used={fingerprint(q) for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]};records=[];rejected=[]
 needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS}
 for r in instances:
  fp=validate(r);l=r['question'][':question/difficulty'].split('/')[-1]
  if fp in used or needed[l]==0:rejected.append({'id':r['question'][':question/id'],'reason':'duplicate matrix or reserve already adequate'});continue
  records.append(r);used.add(fp);needed[l]-=1
 for l in LEVELS:
  if not needed[l]:continue
  run=subprocess.run([str(ROOT/'.venv/bin/python'),str(H.with_suffix('.py')),'--difficulty',l,'--count',str(needed[l]+10),'--seed',str(int(JOB.name[:8],16)),'--format','json'],text=True,capture_output=True,check=True,timeout=180)
  for r in json.loads(run.stdout):
   fp=validate(r)
   if fp in used:continue
   records.append(r);used.add(fp);needed[l]-=1
   if needed[l]==0:break
 grade(records,OUT/'candidates')
 save(OUT/'candidates.json',records)
 save(OUT/'candidate-validation.json',{'passed':True,'basis':b,'generator_sha256':sha(H.with_suffix('.py')),'available_before':c,'new_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'supplied_generated_file_exists':supplied.exists(),'supplied_validated':len(instances),'supplied_rejected':rejected,'distinct_matrices':len(records),'bounded_remaining':needed,'hard_evidence':'Existing validated authored dense integer arithmetic extension, magnitudes 4..12; no original hard calibration','native_grader_sha256':sha(ENGINE)})
 print(json.dumps({'basis':b,'available':c['distinct_available'],'candidates':len(records),'remaining':needed}),flush=True)

def tx(records,kp,gid):
 forms=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 else:forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def report_checks(report,path,source):
 attrs={eid:str(a) for eid,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':answer/id',':answer/type',':answer/value',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':question-generator/id',':question-generator/script'}
 for e,a,value,t,s,added in report[':edb/tx-data']:
  assert added and s==source,'Unexpected retraction or attribution';name=attrs[a]
  if e==KP:assert name in {':knowledge-point/questions',':knowledge-point/question-generator'}
  elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected out-of-scope datom'

def verify(report,path,intent):
 assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis'];b=report[':edb/db-after-t'];report_checks(report,path/'receipt-check',intent['source_eid'])
 before=loads((path/'before.edn').read_text());after=read(b,path/'readback');old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in after[':knowledge-point/questions']}
 assert all(canonical(q)==canonical(now[e]) for e,q in old.items())
 excluded={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert canonical({k:z for k,z in before.items() if k not in excluded})==canonical({k:z for k,z in after.items() if k not in excluded})
 gen=after[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q;assert canonical(question_record(q))==canonical(r['question']);validate(r)
 assert not tx([],after,intent['generator_id']);grade(records,path/'readback');c=counts(after,path/'readback-counts',b)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'new_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'distinct_available_after':c['distinct_available'],'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'no_retractions':True,'only_requested_kp_additive_content':True,'source':SOURCE,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
 save(path/'verification.json',result);return result

def finish(path,verified,inv,gid):
 remaining={l:max(0,5-verified['distinct_available_after'][l]) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'topic':17592186048146,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'new_by_level':verified['new_by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'available_after':verified['distinct_available_after'],'shortage_remaining':remaining,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source_questions_and_learner_history_preserved':True,'application_contributor':SOURCE,'capability_evidence':{'easy':'Observed integer determinant scope','moderate':'Validated authored dense signed integer scope, magnitudes 2..8; no source moderate calibration','hard':'Validated authored dense signed integer scope, magnitudes 4..12; no source hard calibration','deduplication':'Distinct exact matrices; no claim-only, name-only, identity, seed or order variations counted'},'evidence':[str(p.relative_to(ROOT)) for p in [H/'validation.json',H/'classification.md',H/'template-extraction.md',OUT/'native-build.json',OUT/'candidate-validation.json',path/'preparation.json',path/'transaction.edn',path/'commit-intent.json',path/'preview.edn',path/'commit.edn',path/'verification.json',path/'inventory-after.json']]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def commit():
 val=json.loads((H/'validation.json').read_text());assert val['status']=='passed' and val['generator_sha256']==sha(H.with_suffix('.py'))
 assert json.loads((OUT/'candidate-validation.json').read_text())['generator_sha256']==sha(H.with_suffix('.py'))
 candidates=json.loads((OUT/'candidates.json').read_text())
 for r in candidates:validate(r)
 preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint and intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(report,path,intent);finish(path,verified,inventory(path/'inventory-after.json'),intent['generator_id']);return
  inv=inventory(OUT/'inventory-locked.json');b=inv['basis'];assert DB.basis()==b and LINEAGE in DB.command('status')
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read(b,path);refresh(kp,path,b);(path/'before.edn').write_text(dumps(kp)+'\n')
  existing=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'existing-generator',b)
  gen=kp.get(':knowledge-point/question-generator');assert len(existing)<=1
  gid=str(gen[':question-generator/id']) if gen else str(existing[0][0][':question-generator/id']) if existing else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
  save(H/'capabilities.json',{'generator_id':gid,'script':SCRIPT,'version':g.VERSION,'supported_levels':list(LEVELS),'unsupported_levels':[],'hard_calibration':'Authored dense integer arithmetic extension, magnitudes 4..12; no source hard calibration','validation':'validation.json','finite_limit':None})
  if gen:assert gen[':question-generator/script']==SCRIPT
  c=counts(kp,path,b);needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS};used={fingerprint(q) for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]};records=[];added={l:0 for l in LEVELS}
  for r in candidates:
   l=r['question'][':question/difficulty'].split('/')[-1];fp=validate(r)
   if added[l]<needed[l] and fp not in used:records.append(r);used.add(fp);added[l]+=1
  assert added==needed,'Live shortage exceeds candidates; return to preparation'
  ids=[uuid.UUID(s) for r in records for s in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
  if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',b)
  identity=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
  assert not identity or len(identity)==1 and identity[0][0][':question-generator/script']==SCRIPT
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
  save(path/'generated.json',records);grade(records,path)
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_sha256':sha(H.with_suffix('.py')),'available_before':c,'new_by_level':added,'supported_shortage_remaining':{l:needed[l]-added[l] for l in LEVELS},'assets':[],'source_unchanged':True,'candidate_validation':str((OUT/'candidate-validation.json').relative_to(ROOT))})
  forms=tx(records,kp,gid)
  if not forms:
   verified={'basis_before':b,'basis_after':b,'new_questions':0,'new_by_level':added,'distinct_available_after':c['distinct_available'],'no_changes':True};save(path/'verification.json',verified);finish(path,verified,inv,gid);return
  txpath=path/'transaction.edn';text=dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(text);f.flush();os.fsync(f.fileno())
  result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=55)
  (path/'preview.edn').write_text(result.stdout);pr=loads(result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;report_checks(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','lineage':LINEAGE,'endpoint':DB.args.endpoint,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'sha256':sha(txpath),'exact_edn':text,'request_key':'determinant-3x3-'+str(b)+'-'+sha(txpath),'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(H.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()}
  save(path/'commit-intent.json',intent)
  report=DB._commit(intent,txpath,path);verified=verify(report,path,intent);finish(path,verified,inventory(path/'inventory-after.json'),gid)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','commit']);args=parser.parse_args()
 (prepare if args.action=='prepare' else commit)()
