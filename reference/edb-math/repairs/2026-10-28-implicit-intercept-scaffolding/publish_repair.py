import json,sys,fcntl,time,copy
from pathlib import Path
R=Path('/home/jake/Developer/Course_Academy');E=R/'reference/edb-math/repairs/2026-10-28-implicit-intercept-scaffolding';P=E/'package';sys.path.insert(0,str(R/'scripts'))
from generator_publish import Publisher,jsonable,normalized_question,StaleBasis
from generator_packages import publish_package,manifest_digest,resolve_registered_script
from generator_pipeline import source_identity,digest
from generator_approval import make_approval,approved_band
from generator_review import validate_review,REVIEW_POLICY_VERSION
from generator_pool_repair import repair_pool
from inventory_jobs import save

def read(p):return json.loads(Path(p).read_text())
def write(p,v):save(Path(p),v)
p=Publisher.from_environment();K=17592186054847;inv=R/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051';oldref='generators/04/04d24c7ca12e603e1125a2bf8982efca603e11cefe57f689c75a5af7c3aa8cde/generator.py'
with (inv/f'kp-{K}.lock').open('a') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 report=read(E/'final-result.json');binding=read(E/'final-binding.json');validate_review(report,E,binding)
 st=p.client.status();kp=p.read_kp(K,E/'live-before',st['basis']);write(E/'live-before.json',jsonable(kp));registered=kp[':knowledge-point/question-generator'][':question-generator/script']
 manifest=read(E/'package-manifest.json');package=publish_package(P,'generator.py',list(manifest['files']),p.config.math_root,dependencies=manifest['dependencies'],expected_digest=binding['package_hash'])
 if registered not in {oldref,package.reference}:raise ValueError('Another generator has been registered; inspect it before proceeding')
 affected=[q for q in kp[':knowledge-point/questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired') and ('Use $' in q[':question/problem'] or 'differentiation has been started' in q[':question/problem'])]
 origin=R/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051/28dc3a4c48de2aaa8bc007595dab2ce8ce98b08057bd6d6908229e02eaa0e645.pipeline/3'
 samples=read(origin/'samples-easy.json')+read(inv/'0c46ca03112909b2ce32e25075988b16791a7a76b2a56f84a95553c528ef5ef8.pipeline/1/samples.json');published=read(origin/'investigation/published-exemplars.json');proof=[];rows=[]
 for q in affected:
  live=normalized_question(q,identity=False);matches=[r for r in samples if normalized_question(r['question'],identity=False)==live]
  if matches:
   r=copy.deepcopy(matches[0]);r['generation']['publication_proof']='Exact prompt/solution/answer comparison to database record; owned identities remapped by publisher.';r['question']=jsonable(q)
  else:
   assert any(str(x[':question/id'])==str(q[':question/id']) and normalized_question(x,identity=False)==live for x in published),'Missing original generated record evidence'
   r={'question':jsonable(q),'generation':{'mode':'published-investigation-exemplar','source':':agent/codex','published_record':str(origin/'investigation/published-exemplars.json'),'provenance_query':'provenance.json'}}
  proof.append(r);rows.append({'entity_id':q[':db/id'],'question_id':str(q[':question/id']),'finding':'Added derivative, point-slope formula/setup, or axis-zero reminder removes independently required work.','reproduction':q[':question/problem'],'evidence_path':'affected-generated-records.json'})
 write(E/'affected-generated-records.json',proof);write(E/'affected-inventory.json',{'affected_questions':rows})
 # Install clean runtime and five fresh independent-practice questions first.
 publication=E/'publication'
 for attempt in range(3):
  try:
   if not (publication/'request.json').exists():p.prepare(K,read(E/'final-easy.json'),package.reference,package.digest,publication,source_snapshot=read(E/'source/source.json'),assets_directory=P,expected_registered_generator=registered)
   receipt=p.publish(publication);break
  except StaleBasis:
   if attempt==2:raise
 else:raise RuntimeError('Publication did not finish')
 retirement=repair_pool(p,K,[E/'affected-inventory.json'],E/'retirement');assert not retirement['unresolved'],retirement
 # Bind the checked package to current instructional evidence, not stale old approval.
 fresh=p.extract_source(K,E/'registered-source');identity={**source_identity(fresh),'package_sha256':package.digest,'registration':package.reference}
 approval=make_approval(identity,report,binding,str(E/'final-result.json'),receipt,'easy',REVIEW_POLICY_VERSION,publication_batch_hash=binding['batch_hash'])
 for band in ['easy','moderate','hard']:approved_band(approval,identity,band,REVIEW_POLICY_VERSION)
 approval_path=p.config.math_root/'generators/approvals'/package.digest/f'{K}.json';approval_path.parent.mkdir(parents=True,exist_ok=True)
 with approval_path.with_suffix('.lock').open('a') as al:
  fcntl.flock(al,fcntl.LOCK_EX);write(approval_path,approval)
 # Supersede the pending review of the old package while holding the same KP lock.
 with (inv/'jobs.lock').open('a') as jl:
  fcntl.flock(jl,fcntl.LOCK_EX)
  for path in inv.glob('*.json'):
   job=read(path);request=job.get('request',{})
   if request.get('knowledgePoint')!=K or request.get('jobKind','build')!='build':continue
   if job.get('state')=='running':raise ValueError('Unexpected live job despite held KP lock')
   write(E/('superseded-'+path.name),job)
   write(path,{**job,'state':'verified','request':{**request,'script':package.reference},'completedAt':time.time(),'verifiedBasis':receipt['basis_after'],'error':None,'exitCode':0,'manualRepair':str(E),'outcome':{'outcome':'generated','generator':package.reference,'verified_package':package.reference,'verified_bands':['easy','moderate','hard'],'publication':receipt,'evidence':str(E/'final-result.json')}})
 after_st=p.client.status();after=p.read_kp(K,E/'live-after',after_st['basis']);write(E/'live-after.json',jsonable(after))
 assert after[':knowledge-point/question-generator'][':question-generator/script']==package.reference
 now={q[':db/id']:q for q in after[':knowledge-point/questions']}
 for q in kp[':knowledge-point/questions']:
  actual=copy.deepcopy(now[q[':db/id']]);before=copy.deepcopy(q)
  if q[':db/id'] in {r['entity_id'] for r in rows}:assert actual.pop(':question/retired') is True
  assert actual==before,'Existing question content/history must not change'
 assert not any(not q.get(':question/math-academy-id') and not q.get(':question/retired') and ('Use $' in q[':question/problem'] or 'differentiation has been started' in q[':question/problem']) for q in now.values())
 result={'passed':True,'basis':after_st['basis'],'registration':package.reference,'new_questions':receipt['new_questions'],'retired':retirement['retired'],'approval_bands':list(approval['bands']),'existing_question_content_unchanged':True,'active_hinted_generated_questions':0};write(E/'live-verification.json',result);print(json.dumps(result))
