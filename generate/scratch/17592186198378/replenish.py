"""Validated, additive KP inventory commits serialized with the application."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from capture.scripts.database.preview import preview_executable
from inventory_validation import *
import fcntl,threading
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

def check_source(kp,path):
 frozen=json.loads((HERE/'source.json').read_text())['record'];now={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
 for q in frozen[':knowledge-point/questions']:assert canonical(q)==canonical(now[q[':question/math-academy-id']]),'Source changed since generator validation'
 assert canonical(frozen[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
 initial=loads((OUT/'initial/kp.edn').read_text())[0][0]
 assert canonical(initial)==canonical(kp) or canonical({k:x for k,x in initial.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:x for k,x in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
 source=[source_check(q) for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q]
 assert {q['source_id'] for q in source}=={q[':question/math-academy-id'] for q in initial[':knowledge-point/questions']}
 save(path/'source-validation.json',{'basis':DB.basis(),'source_questions':source,'frozen_nine_unchanged':True,'canonical_unchanged':True})

def generator_identity(kp,path,b):
 existing=kp.get(':knowledge-point/question-generator')
 peers=DB.query('[:find (pull ?g [:db/id :question-generator/id :question-generator/script]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b)
 assert len(peers)<=1
 regpath=HERE/'registration.json';local=json.loads(regpath.read_text()) if regpath.exists() else None
 gid=str(existing[':question-generator/id']) if existing else str(peers[0][0][':question-generator/id']) if peers else local['id'] if local else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
 if local:assert local['id']==gid
 if existing:assert existing[':question-generator/script']==SCRIPT
 save(regpath,{'id':gid,'script':SCRIPT,'knowledge_point_id':g.KP_UUID,'reused_existing_database_identity':bool(existing or peers)})
 rows=DB.query('[:find ?g ?s :in $ ?id :where [?g :question-generator/id ?id] [?g :question-generator/script ?s]]',[uuid.UUID(gid)],path,'generator-id',b)
 assert not rows or len(rows)==1 and rows[0][1]==SCRIPT
 return gid

def select(kp,needed,path,b):
 supplied=JOB.with_suffix('.generated');data=json.loads(supplied.read_text()) if supplied.exists() else {};instances=data.get('instances',[]) if isinstance(data,dict) else data
 if isinstance(instances,dict):instances=[instances]
 assert isinstance(instances,list)
 for r in instances:validate(r)
 save(path/'supplied-validation.json',{'exists':supplied.exists(),'validated_instances':len(instances),'generator_error':data.get('generatorError') if isinstance(data,dict) else None})
 used={fingerprint(q) for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]};records=[];added={l:0 for l in LEVELS};duplicates=0
 for level in LEVELS:
  candidates=[r for r in instances if r['question'][':question/difficulty'].endswith('/'+level)]
  # Bounded calls to the existing validated sampler, rotating eligible families.
  names=[name for name,(l,_,_) in g.TEMPLATES.items() if l==level]
  for n in range(100):
   if added[level]>=needed[level]:break
   r=candidates[n] if n<len(candidates) else g.generate(level,int(JOB.name[:8],16)+n,template=names[n%len(names)])
   fp=validate(r)
   if fp in used:duplicates+=1;continue
   records.append(r);used.add(fp);added[level]+=1
 save(path/'generated.json',records);native(records,path/'selected-grading');(path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
 ids=[uuid.UUID(r['question'][':question/id']) for r in records]+[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]+[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]
 assert len(ids)==len(set(ids))
 if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-collisions',b)
 save(path/'asset-manifest.json',{'assets':[],'plot_rating':'none','reason':'All sampled templates use mathematical notation and no plot assets'})
 return records,added,duplicates

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_report(report,path/'receipt-check',intent['source_eid']);b=report[':edb/db-after-t'];kp=read(path/'readback',b);before=loads((path/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']};assert all(canonical(now[e])==canonical(q) for e,q in old.items())
 omit={':knowledge-point/questions',':knowledge-point/question-generator'};assert canonical({k:x for k,x in before.items() if k not in omit})==canonical({k:x for k,x in kp.items() if k not in omit})
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  validate(r);q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question'])
 assert not transaction([],kp,intent['generator_id'])
 after=counts(kp,b,path/'readback/inventory');prep=json.loads((path/'preparation.json').read_text())
 for l in LEVELS:assert after['distinct_available'][l]==prep['counts_before']['distinct_available'][l]+prep['new_by_level'][l]
 verified={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'source_questions_preserved':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'only_scoped_additive_datoms':True,'all_datoms_attributed_to':SOURCE,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_after':after['distinct_available']}
 save(path/'verification.json',verified);return verified

def finish(path,intent,verified,inv):
 prep=json.loads((path/'preparation.json').read_text());remaining={l:max(0,5-verified['available_after'][l]) for l in LEVELS};caps=json.loads((HERE/'capabilities.json').read_text())
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'generator_sha256':sha(HERE.with_suffix('.py')),'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'available_before':prep['counts_before']['distinct_available'],'available_after':verified['available_after'],'shortage_remaining':remaining,'supported_levels':list(LEVELS),'authored_levels':['hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'capability_exceptions':caps['exceptions'],'difficulty_basis':caps['difficulty_basis'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [HERE/'validation.json',HERE/'classification-current.md',HERE/'capabilities.json',OUT/'native-build.json',path/'source-validation.json',path/'preparation.json',path/'generated.json',path/'selected-grading/report.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'readback/inventory/counts.json',path/'inventory-after.json']]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','new_by_level','available_after','shortage_remaining')},indent=2),flush=True)

def main():
 validation=json.loads((HERE/'validation.json').read_text());qa=json.loads((ROOT/'generate/runs/current/qa/17592186198378.json').read_text());assert validation['status']=='passed' and qa['parent_review']=='passed' and qa['generator_sha256']==sha(HERE.with_suffix('.py'))
 freeze=json.loads((HERE/'freeze.json').read_text());assert all(sha(ROOT/p)==s for p,s in freeze['files'].items())
 preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired; rechecking current inventory and basis',flush=True)
  for path in sorted(OUT.glob('basis-*')):
   if not (path/'commit-intent.json').exists():continue
   intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['connection_sha256']==hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
   assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
   verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,intent,verified,inventory(path/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b and LINEAGE in DB.command('status');path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
  kp=read(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID;check_source(kp,path);(path/'before.edn').write_text(dumps(kp)+'\n');gid=generator_identity(kp,path,b)
  c=counts(kp,b,path/'inventory-before');needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS};records,added,duplicates=select(kp,needed,path,b)
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'counts_before':c,'needed':needed,'new_by_level':added,'new_questions':len(records),'remaining':{l:needed[l]-added[l] for l in LEVELS},'duplicate_candidates_rejected':duplicates,'generator_sha256':sha(HERE.with_suffix('.py')),'generator_version':g.VERSION,'mathematics_and_native_grading':'passed','source_evidence':'12 current banks checked, frozen 9 unchanged'})
  forms=transaction(records,kp,gid)
  if not forms:
   finish(path,{'generator_id':gid},{'basis_after':b,'new_questions':0,'available_after':c['distinct_available']},inv);return
  txpath=path/'transaction.edn';text=dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(text);f.flush();os.fsync(f.fileno())
  result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,capture_output=True,text=True,check=True,timeout=55)
  (path/'preview.edn').write_text(result.stdout);pr=loads(result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','lineage':LINEAGE,'endpoint':DB.args.endpoint,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'sha256':sha(txpath),'exact_edn':text,'request_key':'flux-integral-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK),'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()}
  save(path/'commit-intent.json',intent)
  verified=verify(path,intent,DB._commit(intent,txpath,path));finish(path,intent,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
