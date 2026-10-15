"""Serialize scoped additive replenishment, exact requests and receipt readback."""
import copy,fcntl,hashlib,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
import integration as i
import validate as v
HERE=i.HERE;ROOT=i.ROOT;DB=i.DB;KP=i.KP;g=v.g
SOURCE=':application/ca-engine';SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
LEVELS=g.SUPPORTED_LEVELS;OUT=HERE/'reference/replenishment'
JOB=ROOT/'.local/learning/inventory/math'/i.LEARNER/'84242fcb773aa1f20c0eb173b523d8db11fd9380f142d30dd5391dd71938809b'
LOCK=ROOT/'.local/learning/requests/math/api.lock'
def save(p,x):i.save(p,x)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.loads(json.dumps(x,default=str))
def normalized(q):
 if isinstance(q[':question/difficulty'],dict):q=g.clean(q)
 q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
 for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
 return q

def source_unchanged(kp):
 old=g.RAW['record'];now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert str(kp[':knowledge-point/id'])==g.KP_UUID
 for q in old[':knowledge-point/questions']:assert canonical(now[q[':db/id']])==q,'Source changed; reclassify'
 assert canonical(kp[':knowledge-point/canonical-example'])==old[':knowledge-point/canonical-example']

def source_validation():
 rows=[];cases=[]
 for key,q in g.Q.items():
  r=g.generate(g.level_of(key),template=key,parameters=g.default_parameters(key));v.independent(r)
  source=g.clean(q)
  assert all(r['question'][k]==source[k] for k in (':question/problem',':question/worked-solution',':question/difficulty'))
  r['question']=source;v.independent(r)
  cases.append(v.native(r,key));rows.append({'id':q[':db/id'],'source':key,'difficulty':g.level_of(key),'fingerprint':g.fingerprint(source)})
 save(OUT/'source-native-input.json',cases);subprocess.run([str(HERE/'check-engine'),str(OUT/'source-native-input.json'),str(OUT/'source-native-report.json')],check=True)
 save(OUT/'source-inventory-validation.json',{'basis':g.RAW['basis'],'accepted':rows,'excluded':[],'passed':True})

def check(r):
 fp=v.independent(r);m=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
 twin=g.generate(level,m['seed'],m['template'],m['parameters'])
 assert normalized(r['question'])==normalized(twin['question']) and m==twin['generation'],'Instance does not replay'
 return fp

def validated_counts(kp,native_counts,path):
 accepted={x['id'] for x in json.loads((OUT/'source-inventory-validation.json').read_text())['accepted']}
 packages=[]
 for p in OUT.glob('basis-*/generated.json'):packages.extend(json.loads(p.read_text()))
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] in accepted:continue
  for r in packages:
   if str(q[':question/id'])==r['question'][':question/id'] and normalized(q)==normalized(r['question']):check(r);accepted.add(q[':db/id']);break
 byid={q[':db/id']:q for q in kp[':knowledge-point/questions']};available=set(native_counts['available_questions'])&accepted
 counts={l:len({g.fingerprint(byid[e]) for e in available if str(byid[e][':question/difficulty'][':db/ident'])==':question.difficulty/'+l}) for l in LEVELS}
 save(path/'validated-counts.json',{'basis':native_counts['basis'],'counts':counts,'accepted_available_ids':sorted(available),'excluded_unvalidated_ids':sorted(set(native_counts['available_questions'])-accepted),'distinctness':'matrix order, supplied mathematical object and fixed claims; exact null-space RREF; ignores seed, identity and bank order'})
 return counts

def transaction(records,kp,gid):
 k=i.kw;forms=[]
 for rec in records:
  q=rec['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:forms.append({k('db/id'):a[':answer/id'],k('answer/id'):uuid.UUID(a[':answer/id']),k('answer/type'):k(a[':answer/type']),k('answer/value'):a[':answer/value'],k('db/ensure'):k('answer/validate')})
   forms.append({k('db/id'):f[':answer-field/id'],k('answer-field/id'):uuid.UUID(f[':answer-field/id']),k('answer-field/key'):f[':answer-field/key'],k('answer-field/type'):k(f[':answer-field/type']),k('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],k('answer-field/correct'):f[':answer-field/correct'][1],k('db/ensure'):k('answer-field/validate')})
  forms.append({k('db/id'):q[':question/id'],k('question/id'):uuid.UUID(q[':question/id']),k('question/problem'):q[':question/problem'],k('question/worked-solution'):q[':question/worked-solution'],k('question/difficulty'):k(q[':question/difficulty']),k('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],k('db/ensure'):k('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 else:forms += [{k('db/id'):'generator',k('question-generator/id'):uuid.UUID(gid),k('question-generator/script'):SCRIPT},[k('db/add'),KP,k('knowledge-point/question-generator'),'generator']]
 if records:forms.append({k('db/id'):KP,k('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([k('db/ensure'),KP,k('knowledge-point/validate')])
 return forms

def check_datoms(report,path,source):
 attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,val,tx,s,added in report[':edb/tx-data']:
  assert s==source and added,'Unexpected attribution or retraction'
  name=attrs[a]
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,name

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_datoms(report,path/'receipt-check',intent['source_eid']);basis=report[':edb/db-after-t'];kp=i.read_kp(path/'readback',basis)
 before=i.loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items())
 assert {k:x for k,x in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:x for k,x in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalized(q)==normalized(r['question']);check(r)
 assert not transaction([],kp,intent['generator_id'])
 verified={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
 save(path/'verification.json',verified);return verified

def finish(path,intent,verified,binary):
 inv,native=i.inventory(binary,path/'inventory-after.json');kp=i.read_kp(path/'inventory-readback',inv['basis']);available=validated_counts(kp,native,path/'inventory-readback');remaining={l:max(0,5-available[l]) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','database':'math','knowledgePoint':KP,'topic':17592186048978,'lineage':i.LINEAGE,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'generator_registered':True,'verified_commit_basis':verified['basis_after'],'commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':['easy'],'unsupported_levels_filled':False,'unsupported_nominal_shortage':{'easy':5},'available_by_level':{'easy':0,**available},'remaining_supported_shortages':remaining,'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],'inventory_recheck_basis':inv['basis'],'source_questions_and_learner_history_preserved':True,'supplied_generated_file_existed':JOB.with_suffix('.generated').exists(),'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'note':'Current validated inventory already meets moderate and hard targets; registration required no new question content. Easy has no supported source backbone and remains unfilled.','evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'preparation.json',path/'inventory-after.json',path/'inventory-after-counts.json',path/'inventory-readback/validated-counts.json',OUT/'source-inventory-validation.json',OUT/'source-native-report.json',HERE/'validation.json',HERE/'classification.json',HERE/'template-extraction.json',HERE/'template-extraction.md',HERE/'review.json',HERE/'review.md',HERE/'native-report.json',HERE/'native-build.json',HERE/'capabilities.json'] if p.exists()]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ['outcome','verified_commit_basis','new_questions','available_by_level','remaining_supported_shortages']}),flush=True)

def main():
 OUT.mkdir(parents=True,exist_ok=True);validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass'
 for name,digest in validation['hashes'].items():assert sha(ROOT/name)==digest,name
 source_validation();binary=i.build_learning(ROOT.parent/'EDB')
 preview=i.preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if not (path/'commit-intent.json').exists():continue
   intent=json.loads((path/'commit-intent.json').read_text())
   assert intent['database']=='math' and intent['lineage']==i.LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint
   assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
   assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
   report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent,verified,binary);return
  inv,native=i.inventory(binary,OUT/'inventory-before.json');b=inv['basis'];path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
  for name in ('inventory-before.json','inventory-before-counts.json'):(path/name).write_bytes((OUT/name).read_bytes())
  kp=i.read_kp(path,b);source_unchanged(kp);(path/'before.edn').write_text(i.dumps(kp)+'\n')
  contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
  byscript=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b);assert len(byscript)<=1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(byscript[0][0][':question-generator/id']) if byscript else g.GENERATOR_UUID
  assert gid==g.GENERATOR_UUID,'Existing identity requires reconciliation'
  collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b)
  assert not collision or len(collision)==1 and collision[0][0][':question-generator/script']==SCRIPT
  available=validated_counts(kp,native,path);needed={l:max(0,5-available[l]) for l in LEVELS};selected={l:0 for l in LEVELS};used={g.fingerprint(q) for q in kp[':knowledge-point/questions']};records=[]
  supplied=JOB.with_suffix('.generated');data=json.loads(supplied.read_text()) if supplied.exists() else {};instances=data.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
  def select(r):
   fp=check(r);level=r['question'][':question/difficulty'].split('/')[-1]
   if fp in used or selected[level]>=needed[level]:return False
   records.append(r);selected[level]+=1;used.add(fp);return True
  supplied_report=[{'id':r['question'][':question/id'],'validated':True,'selected':select(r)} for r in instances]
  for level in LEVELS:
   if needed[level]:
    for r in g.batch(level,200,1930):
     select(r)
     if selected[level]>=needed[level]:break
  save(path/'supplied-validation.json',{'exists':supplied.exists(),'instances':supplied_report,'generatorError':data.get('generatorError')})
  ids=[uuid.UUID(r['question'][':question/id']) for r in records]+[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]+[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]
  clashes=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',b) if ids else [];assert not clashes
  save(path/'generated.json',records)
  if records:
   save(path/'native-input.json',[v.native(r,r['question'][':question/id']) for r in records]);subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
  save(path/'preparation.json',{'basis':b,'lineage':i.LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'generator_id':gid,'generator_path':SCRIPT,'available_by_level':available,'needed_by_level':needed,'selected_by_level':selected,'unfilled_by_level':{l:needed[l]-selected[l] for l in LEVELS},'unsupported_levels':{'easy':'No easy source backbone; nominal shortage 5 remains'},'asset_hashes':[],'source_evidence_unchanged':True,'validation_sha256':sha(HERE/'validation.json'),'lock':str(LOCK)})
  forms=transaction(records,kp,gid)
  if not forms:
   verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True};save(path/'verification.json',verified);finish(path,{'generator_id':gid},verified,binary);return
  txpath=path/'transaction.edn';tx=i.dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  (path/'preview.edn').write_text(r.stdout);pr=i.loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
  check_datoms(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':i.LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'rank-nullity-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
  save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,intent,verified,binary)
if __name__=='__main__':main()
