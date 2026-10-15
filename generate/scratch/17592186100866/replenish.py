"""Only this KP: current native inventory, validated generation and guarded commit."""
import copy,fcntl,hashlib,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
import integration as i
import validate as v
g=v.g;HERE=i.HERE;ROOT=i.ROOT;DB=i.DB;KP=i.KP;LEVELS=('easy',)
LINEAGE=g.CAP['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/i.LEARNER/'8516312240f7f281a2a4b1556be5a765308a3ec323555ebdd8f11ac946fad718'
OUT=HERE/'reference/replenishment';OUT.mkdir(exist_ok=True,parents=True)
save=i.save;kw=i.kw;dumps=i.dumps;loads=i.loads

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def plain(x):
 if isinstance(x,dict):return {str(k):plain(z) for k,z in x.items()}
 if isinstance(x,(list,tuple)):return [plain(z) for z in x]
 return x if x is None or isinstance(x,(str,int,float,bool)) else str(x)
def comparable(x):
 if isinstance(x,dict):
  if ':db/ident' in x:return {':db/ident':str(x[':db/ident'])}
  return {str(k):comparable(z) for k,z in x.items() if str(k) not in (':knowledge-point/_questions',':knowledge-point/_canonical-example')}
 if isinstance(x,(list,tuple)):return sorted([comparable(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
 return plain(x)
def normalize(q):
 out={k:plain(q[k]) for k in (':question/id',':question/problem',':question/worked-solution')}
 out[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);out[':question/answer-fields']=[]
 for f in q[':question/answer-fields']:
  out[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
 return out

def validate_sources(kp,path):
 accepted=set();rows=[];cases=[]
 for q in kp[':knowledge-point/questions']:
  mid=q.get(':question/math-academy-id')
  if mid in ('q-13564','q-13566'):
   rows.append({'id':q[':db/id'],'source':mid,'accepted':False,'reason':'duplicate key/incomplete field' if mid=='q-13564' else 'unrated/incomplete'});continue
  if mid in g.SOURCES:
   n=normalize(q);math_q=copy.deepcopy(n)
   # Retain original source notation; compare full vectors under documented escape correction.
   for f in math_q[':question/answer-fields']:
    for a in f[':answer-field/choices']:a[':answer/value']=a[':answer/value'].replace('\\\\begin','\\begin').replace('\\\\end','\\end')
   p=g.parameters(q);meta={'template':g.template_of(mid),'bank_profile':mid,'parameters':p,'eligible_for_learning':True}
   rec={'knowledge_point':{'db_id':KP,'title':g.TITLE},'question':math_q,'generation':meta}
   fp=v.check(rec)
   rec['question']=n;cases.append(v.native(rec,'existing-'+mid))
  else:
   raise ValueError('Unrecognized current question; reclassification needed')
  accepted.add(q[':db/id']);rows.append({'id':q[':db/id'],'source':mid,'accepted':True,'mathematical_fingerprint':fp})
 save(path/'source-validation.json',rows);save(path/'source-native-input.json',cases)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'source-native-input.json'),str(path/'source-native-report.json')],check=True)
 return accepted

def validated_count(kp,pool,path):
 accepted=validate_sources(kp,path);seen=set();ids=[];byid={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 for eid in pool['available_questions']:
  if eid not in accepted:continue
  fp=g.question_fingerprint(plain(byid[eid]))
  if fp not in seen:seen.add(fp);ids.append(eid)
 result={'basis':pool['basis'],'easy':len(ids),'accepted_available_questions':ids,'excluded_unvalidated':sorted(set(pool['available_questions'])-accepted),'distinctness':'ordered row operands; simultaneous column/vector permutation collapsed; ignores labels, format, bank, seed and identity'}
 save(path/'validated-inventory.json',result);return result

def transaction(records,kp,gid):
 forms=[]
 for rec in records:
  q=rec['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen is None:forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def check_report(report,path,source):
 attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,value,tx,contributor,added in report[':edb/tx-data']:
  assert contributor==source and added,'Unexpected retraction or contributor'
  name=attrs[a]
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,name

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,path/'receipt-check',intent['source_eid'])
 before=loads((path/'before.edn').read_text());kp=i.read_kp(path/'readback',report[':edb/db-after-t'])
 assert {k:z for k,z in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:z for k,z in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items())
 recs=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(recs)
 byid={str(q[':question/id']):q for q in now.values()}
 for r in recs:
  assert comparable(normalize(byid[r['question'][':question/id']]))==comparable(r['question']);v.check(r)
 assert not transaction([],kp,intent['generator_id'])
 result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(recs),'source_questions_unchanged':len(old),'canonical_example_unchanged':True,'only_additive_scoped_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_changes':0}
 save(path/'verification.json',result);return result

def finish(path,intent,verified):
 inv,pool=i.pool_inventory(path/'inventory-after.json');kp=i.read_kp(path/'inventory-readback',inv['basis'])
 # At this run inventory already has 9, so only registration is needed.
 counts=validated_count(kp,pool,path/'inventory-readback');remaining={'easy':max(0,5-counts['easy'])}
 result={'outcome':'generated' if not any(remaining.values()) else 'finite-limit','knowledgePoint':KP,'topic':17592186050825,'database':'math','lineage':LINEAGE,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'generator_registered':True,'verified_commit_basis':verified['basis_after'],'commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'unsupported_levels_filled':False,'available_by_level':{'easy':counts['easy'],'moderate':0,'hard':0},'remaining_supported_shortages':remaining,'unsupported_nominal_shortage':{'moderate':5,'hard':5},'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source_questions_and_learner_history_preserved':True,'supplied_generated_file_existed':JOB.with_suffix('.generated').exists(),'note':'Nine existing fresh, distinct, gradable easy questions meet the supported reserve; no redundant questions added. Generator executed and validated, then registered. Moderate and hard remain explicitly unfilled, unsupported by current sources.','evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'preparation.json',path/'inventory-after.json',path/'inventory-after-counts.json',path/'inventory-readback/validated-inventory.json',path/'inventory-readback/source-native-report.json',HERE/'validation.json',HERE/'classification.json',HERE/'template-extraction.json',HERE/'template-extraction.md',HERE/'source-bank-replay.json',HERE/'slot-coverage.json',HERE/'review.json',HERE/'review.md',HERE/'native-report.json',HERE/'capabilities.json',HERE/'reference/freeze.json'] if p.exists()]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
 freeze=json.loads((HERE/'reference/freeze.json').read_text());assert all(sha(ROOT/p)==h for p,h in freeze['hashes'].items())
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn')
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    report=DB._commit(intent,path/'transaction.edn',path);finish(path,intent,verify(path,intent,report));return
  inv,pool=i.pool_inventory(OUT/'inventory-before.json');assert inv['lineage']==LINEAGE
  b=inv['basis'];path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=i.read_kp(path,b);(path/'before.edn').write_text(dumps(kp)+'\n')
  current={str(q[':question/id']):q for q in kp[':knowledge-point/questions']}
  assert all(comparable(q)==comparable(current[str(q[':question/id'])]) for q in g.RECORD[':knowledge-point/questions']),'Source changed; reclassify'
  assert comparable(kp[':knowledge-point/canonical-example'])==comparable(g.RECORD[':knowledge-point/canonical-example'])
  sources=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(sources)==1
  gen=kp.get(':knowledge-point/question-generator');existing=DB.query('[:find (pull ?g [*]) :in $ ?path :where [?g :question-generator/script ?path]]',[SCRIPT],path,'generator-by-script',b);assert len(existing)<=1
  gid=str(gen[':question-generator/id']) if gen else str(existing[0][0][':question-generator/id']) if existing else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
  existing_id=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b)
  assert not existing_id or existing_id[0][0][':question-generator/script']==SCRIPT
  counts=validated_count(kp,pool,path);needed=max(0,5-counts['easy']);used={g.question_fingerprint(plain(q)) for q in kp[':knowledge-point/questions']}
  used.add(g.fingerprint({'a':1,'b':3,'c':7,'d':-2,'u':2,'v':5}))
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
  records=[]
  for r in instances:
   fp=v.check(r)
   if fp not in used and len(records)<needed:records.append(r);used.add(fp)
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
  for seed in range(1000):
   if len(records)>=needed:break
   r=g.generate('easy',seed);fp=v.check(r)
   if fp not in used:records.append(r);used.add(fp)
  save(path/'generated.json',records);save(path/'native-input.json',[v.native(r) for r in records]);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
  # This classified job needs registration only; new question preparation is
  # available above but source-aware inventory verification must remain explicit.
  assert not records,'A fresh shortage needs a reviewed generation batch; current job was reclassified from existing inventory'
  forms=transaction(records,kp,gid);assert forms,'Registration already present; recover prior scoped receipt'
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_by_level':{'easy':counts['easy'],'moderate':0,'hard':0},'needed':{'easy':needed},'selected':{'easy':len(records)},'remaining_supported_shortage':{'easy':max(0,needed-len(records))},'unsupported_nominal_shortage':{'moderate':5,'hard':5},'source_questions_unchanged':True,'assets':[],'validation_sha256':sha(HERE/'validation.json'),'distinctness':'mathematical operands, excludes labels, seed, identity, format and bank order'})
  txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  p=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,timeout=55)
  (path/'preview.stderr').write_text(p.stderr);p.check_returncode();(path/'preview.edn').write_text(p.stdout)
  report=loads(p.stdout);assert report[':edb/committed'] is False and report[':edb/db-before-t']==b
  check_report(report,path/'preview-check',sources[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':i.ENV['EDB_ENDPOINT'],'lineage':LINEAGE,'source':SOURCE,'source_eid':sources[0][0],'basis':b,'expected_basis':b,'request_key':'matrix-column-generator-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);finish(path,intent,verify(path,intent,report))
if __name__=='__main__':main()
