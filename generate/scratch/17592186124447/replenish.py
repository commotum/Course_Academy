"""Scoped additive inventory replenishment through the existing EDB integration."""
import ast, copy, fcntl, hashlib, json, os, subprocess, sys, threading, types, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database, QUESTION_PULL
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning
# Load the existing independent display validators without running their full suite.
p=HERE/'validate.py';a=ast.parse(p.read_text())
a.body=[n for n in a.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('DIR','spec','g','ROOT') for t in n.targets)) or (isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value).startswith('spec.loader.exec_module'))]
v=types.ModuleType('gradient_validator');v.__file__=str(p);exec(compile(a,str(p),'exec'),v.__dict__);g=v.g
KP=g.KP_ID;LEVELS=('easy','moderate','hard')
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.CAPTURE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'162834183d82f134b491a855054f29aab21ef81df6d18625ab790b4bb45e2ba0'
OUT=HERE/'reference/replenishment'
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {:knowledge-point/questions '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
UNAVAILABLE='''[:find ?q :in $ ?learner ?kp :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
 (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
 (and [?l :learner/activity ?t] [?t :learner-task/activity ?a]
 (or [?t :learner-task/status :learner-task.status/started] [?t :learner-task/status :learner-task.status/paused])
 [?a :activity/steps ?step] [?step :step/content ?q]))]'''
SHOWN='''[:find ?q :in $ ?learner [?q ...] :where [?l :learner/id ?learner]
 [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q ?tx true]]'''
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def canon(x):
 if isinstance(x,dict):return {str(k):canon(z) for k,z in x.items() if k!=':db/id' and not str(k).startswith(':knowledge-point/_')}
 if isinstance(x,(list,tuple)):return sorted((canon(z) for z in x),key=lambda z:json.dumps(z,sort_keys=True))
 return str(x) if isinstance(x,uuid.UUID) else x

def validate_sources(kp):
 current={q[':question/math-academy-id']:canon(q) for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
 assert current=={mid:canon(q) for mid,q in g.SOURCES.items()},'Source changed; reopen classification'
 assert canon(kp[':knowledge-point/canonical-example'])==canon(g.RAW[':knowledge-point/canonical-example'])

def inventory(binary,path):
 r=subprocess.run([str(binary),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']

def normalized(q):
 d=copy.deepcopy(q)
 for k in list(d):
  if k not in (':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):del d[k]
 if isinstance(d.get(':question/difficulty'),dict):d[':question/difficulty']=str(d[':question/difficulty'][':db/ident'])
 for f in d[':question/answer-fields']:
  for k in list(f):
   if k not in (':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct'):del f[k]
  if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=str(f[':answer-field/type'][':db/ident'])
  if isinstance(f.get(':answer-field/correct'),dict):f[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
  for ans in f[':answer-field/choices']:
   for k in list(ans):
    if k not in (':answer/id',':answer/type',':answer/value'):del ans[k]
   if isinstance(ans[':answer/type'],dict):ans[':answer/type']=str(ans[':answer/type'][':db/ident'])
 return canon(d)

def fingerprint(q):
 functions=v.functions_from_prompt(q[':question/problem']);F,G=functions.values()
 vs=(g.x,g.y,g.z) if any(g.z in f.free_symbols for f in functions.values()) else (g.x,g.y)
 info='supplied' if '∇' in q[':question/problem'] else 'unsupplied'
 return g.digest({'product':g.s.srepr(g.s.expand(g.s.simplify(F*G))),'variables':list(map(str,vs)),'information':info})

def validate(r):
 assert r['knowledge_point']['db_id']==KP and r['knowledge_point']['id']==g.KP_UUID
 assert r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
 m=r['generation'];q=r['question'];l=q[':question/difficulty'].split('/')[-1]
 assert l in LEVELS and all('$' not in a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])
 replay=g.generate(l,m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile'])
 assert normalized(q)==normalized(replay['question']);v.display_validate(r)
 assert fingerprint(q)==m['mathematical_fingerprint']

def native(records,path):
 rows=[]
 for n,r in enumerate(records):
  f=r['question'][':question/answer-fields'][0];c=f[':answer-field/correct'][1]
  rows.append({'label':str(n),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==c else 'rejected','purpose':'ordered exact gradient'} for a in f[':answer-field/choices']]})
 save(path/'native-input.json',rows)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
 report=json.loads((path/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
 return report

def counts(kp,path,basis,records=()):
 unavailable={r[0] for r in DB.query(UNAVAILABLE,[LEARNER,KP],path,'unavailable',basis)}
 unavailable|={r[0] for r in DB.query(SHOWN,[LEARNER,[q[':db/id'] for q in kp[':knowledge-point/questions']]],path,'historically-shown',basis,history=True)}
 known={r['question'][':question/id']:r for r in records}
 for manifest in OUT.glob('basis-*/generated.json'):
  for r in json.loads(manifest.read_text()):known[r['question'][':question/id']]=r
 used=set();available={l:{} for l in LEVELS};unrated=[];graded=[]
 for q in kp[':knowledge-point/questions']:
  fp=fingerprint(q);used.add(fp)
  if ':question/difficulty' not in q:unrated.append(q[':db/id']);continue
  l=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
  if str(q[':question/id']) in known:
   r=known[str(q[':question/id'])];assert normalized(q)==normalized(r['question']);validate(r)
  else:
   mid=q[':question/math-academy-id'];family=next(f for f,m in g.FAMILIES.items() if m==mid)
   r=g.generate(l,template=family,parameters=v.raw_case(family,mid)['parameters'],profile='source:'+mid)
   v.display_validate(r);assert q[':question/problem']==r['question'][':question/problem']
  if q[':db/id'] not in unavailable:available[l][fp]=str(q[':question/id']);graded.append(r)
 used.add(fingerprint(kp[':knowledge-point/canonical-example']))
 native(graded,path)
 result={'basis':basis,'available_by_level':{l:len(z) for l,z in available.items()},'available_question_ids':{l:sorted(z.values()) for l,z in available.items()},'shown_or_reserved_ids':sorted(unavailable),'unrated_source_questions_excluded':unrated,'distinctness':'Exact reduced product and supplied-information role; independent of seed, identity, choice order and distractor profile.'}
 save(path/'validated-inventory.json',result);return result,used

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
    if gen is None:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_datoms(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])}
    new=set(report[':edb/tempids'].values())
    allowed={':question/'+s for s in ('id','problem','worked-solution','difficulty','answer-fields')}|{':answer-field/'+s for s in ('id','key','type','choices','correct')}|{':answer/'+s for s in ('id','type','value')}|{':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution or retraction'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected existing entity change'

def verify(path,intent,report):
 assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
 check_datoms(report,path/'receipt-check',intent['source_eid'])
 after=report[':edb/db-after-t'];kp=read_kp(path/'readback',after);validate_sources(kp)
 before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items())
 omit={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert {k:z for k,z in before.items() if k not in omit}=={k:z for k,z in kp.items() if k not in omit}
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
 byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
  assert normalized(q)==normalized(r['question']);validate(r)
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 assert not transaction([],kp,intent['generator_id'])
 stock,_=counts(kp,path/'post-inventory',after,records)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':after,'new_questions':len(records),'source_questions_preserved':len(old),'learner_history_unchanged':True,'only_scoped_additive_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_inventory':stock}
 save(path/'verification.json',result);return result

def finish(path,intent,verified,binary):
 inv=inventory(binary,path/'inventory-after.json');kp=read_kp(path/'final-inventory',inv['basis']);validate_sources(kp)
 stock,_=counts(kp,path/'final-inventory',inv['basis']);remaining={l:max(0,5-stock['available_by_level'][l]) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'generator_sha256':sha(HERE.with_suffix('.py')),'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'] if not verified.get('no_changes') else None,'inventory_recheck_basis':inv['basis'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'available_by_level':stock['available_by_level'],'shortage_remaining':remaining,'unsupported_levels':[],'unsupported_levels_filled':False,'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'native-report.json',path/'inventory-after.json',path/'final-inventory/validated-inventory.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'capabilities.json') if p.exists()],'note':'Unrated q-37466 excluded. All historical source and learner facts preserved. Finite candidate domains do not imply unlimited future replenishment.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
 print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_remaining')}),flush=True)

def main():
 OUT.mkdir(parents=True,exist_ok=True);validation=json.loads((HERE/'validation.json').read_text())
 assert validation['passed'] and validation['generator_sha256']==sha(HERE.with_suffix('.py')) and validation['basis']==g.CAPTURE['basis']
 binary=build_learning(ROOT.parent/'EDB');preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if not (path/'commit-intent.json').exists():continue
   intent=json.loads((path/'commit-intent.json').read_text())
   assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE
   assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
   assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
   report=DB._commit(intent,path/'transaction.edn',path);finish(path,intent,verify(path,intent,report),binary);return
  inv=inventory(binary,OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);validate_sources(kp)
  (path/'before.edn').write_text(dumps(kp)+'\n');stock,used=counts(kp,path,b)
  needed={l:max(0,5-stock['available_by_level'][l]) for l in LEVELS}
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
  registered=DB.query('[:find (pull ?g [*]) :in $ ?path :where [?g :question-generator/script ?path]]',[SCRIPT],path,'generator-by-script',b);assert len(registered)<=1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
  collisions=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b)
  assert not collisions or collisions[0][0][':question-generator/script']==SCRIPT
  selected={l:0 for l in LEVELS};records=[];checked=[]
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
  instances=supplied.get('instances',supplied if isinstance(supplied,list) else []) if isinstance(supplied,dict) else supplied
  if isinstance(instances,dict):instances=[instances]
  def consider(r):
   validate(r);checked.append(r);l=r['question'][':question/difficulty'].split('/')[-1];fp=r['generation']['mathematical_fingerprint']
   if selected[l]<needed[l] and fp not in used:records.append(r);used.add(fp);selected[l]+=1
  for r in instances:consider(r)
  for l in LEVELS:
   for n in range(max(needed[l]*12,1)):
    if selected[l]>=needed[l]:break
    consider(g.generate(l,int(JOB.name[:8],16)+n))
  assert all(selected[l]<=needed[l] for l in LEVELS)
  save(path/'generated.json',records)
  if not supplied_path.exists():save(supplied_path,{'request':json.loads(JOB.with_suffix('.json').read_text())['request'],'instances':records,'preparation_basis':b})
  native(checked,path)
  ids=[uuid.UUID(ident) for r in records for ident in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
  if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',b)
  save(path/'preparation.json',{'basis':b,'original_job_basis':1831,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing_by_level':needed,'selected_by_level':selected,'unproduced_by_level':{l:needed[l]-selected[l] for l in LEVELS},'available_before':stock,'source_evidence_unchanged':True,'asset_hashes':[],'plots':'none','supplied_generated_exists':bool(supplied),'instances_validated':len(checked),'generator_sha256':sha(HERE.with_suffix('.py'))})
  forms=transaction(records,kp,gid)
  if not forms:
   verified={'passed':True,'basis_after':b,'new_questions':0,'no_changes':True};save(path/'verification.json',verified);finish(path,{'generator_id':gid},verified,binary);return
  txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
  with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
  proc=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  (path/'preview.edn').write_text(proc.stdout);pr=loads(proc.stdout);assert not pr[':edb/committed'] and pr[':edb/db-before-t']==b
  check_datoms(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'gradient-properties-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path)
  finish(path,intent,verify(path,intent,report),binary)
if __name__=='__main__':main()
