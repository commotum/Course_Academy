"""One guarded EDB transaction for all three generators and the repaired lesson pool."""
import importlib.util,copy,uuid
from read import *
from scripts.generator_packages import build_manifest,manifest_digest,publish_package,verify_package
from scripts.integration_batch_policy import validate_delivery_batch
H=HERE
# Reuse the verified primitive serializers and exact state/datom checks.
spec=importlib.util.spec_from_file_location('bounded_commit_helpers',ROOT/'reference/mathacademy/repairs/2026-10-20-log-product-quotient/commit.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
helper.HERE=H;helper.DB=DB
SOURCE=':agent/codex';IDS=[17592186184153,17592186184154,17592186184155]
PATTERN=helper.KP_PATTERN

def prepare():
 directory=H/'content';directory.mkdir(exist_ok=True);assert not(directory/'request.json').exists()
 for name in ('quality-verification.json','algebra-verification.json','ui-verification.json'):assert json.loads((H/name).read_text())['passed']
 identity=DB.status();assert identity['lineage']==json.loads((H/'identity.json').read_text())['lineage']
 state=native(directory/'before',identity['basis'],[('kps',PATTERN,IDS)]);byid={q[':db/id']:q for q in state['kps']};plans={};forms=[]
 qids=[q[':db/id']for kp in byid.values()for q in kp[':knowledge-point/questions']]
 items=DB.query('[:find ?q (pull ?i '+ITEM+') :in $ [?q ...] :where [?i :task-item/content ?q]]',[qids],directory,'items-before',identity['basis']);save('items-at-preparation.json',items)
 allnew=[]
 for kp_id in IDS:
  kp=byid[kp_id];d=H/str(kp_id);initial=json.loads((d/'kp.json').read_text());assert helper.same(kp,initial),('KP changed during review',kp_id)
  additions=json.loads((d/'additions.json').read_text());validate_delivery_batch(additions,kp_id);allnew+=additions
  old=kp[':knowledge-point/question-generator'];m=json.loads((d/'original/generator-package.json').read_text());files=sorted(set(list(m['files'])+['legacy.py','forward.py','integration_batch_policy.py','source-cases.json','scope-contract.json']));manifest=build_manifest(d/'package',m['entrypoint'],files,dependencies=m['dependencies']);digest=manifest_digest(manifest);package=publish_package(d/'package',m['entrypoint'],files,Path(DB.config.math_root),dependencies=m['dependencies'],expected_digest=digest);gid=uuid.uuid5(uuid.UUID(str(kp[':knowledge-point/id'])),'generator-package:'+digest);temp='new-generator-'+str(kp_id)
  forms += [{kw('db/id'):temp,kw('question-generator/id'):gid,kw('question-generator/script'):package.reference},[kw('db/cas'),kp_id,kw('knowledge-point/question-generator'),old[':db/id'],temp],[kw('db/cas'),old[':db/id'],kw('question-generator/script'),old[':question-generator/script'],old[':question-generator/script']]]
  helper.KP=kp_id
  for r in additions:forms+=helper.question_forms(r)
  ledger=json.loads((d/'audit-ledger.json').read_text());withdraw=[r['id']for r in ledger if r['decision']=='withdraw_and_replace']
  for qid in withdraw:forms.append([kw('db/cas'),qid,kw('question/retired'),None,True])
  forms.append([kw('db/ensure'),kp_id,kw('knowledge-point/validate')]);own={q[':db/id']for q in kp[':knowledge-point/questions']}
  plans[str(kp_id)]={'basis':identity['basis'],'lineage':identity['lineage'],'old_generator':old,'generator_uuid':str(gid),'generator_reference':package.reference,'generator_digest':digest,'withdrawn':withdraw,'replacements':additions,'solution_changes':[],'before':{'kp':[kp]},'items_before':[[q,i]for q,i in items if q in own]}
 for kind,values in [('question',[r['question'][':question/id']for r in allnew]),('answer-field',[f[':answer-field/id']for r in allnew for f in r['question'][':question/answer-fields']]),('answer',[a[':answer/id']for r in allnew for f in r['question'][':question/answer-fields']for a in f[':answer-field/choices']])]:
  assert not DB.query(f'[:find ?e :in $ [?id ...] :where [?e :{kind}/id ?id]]',[[uuid.UUID(x)for x in values]],directory,kind+'-identities',identity['basis'])
 (directory/'transaction.edn').write_text(dumps(forms)+'\n');save('content/plan.json',{'identity':identity,'kps':plans,'items_before':items})
 groups=[('kps',PATTERN,IDS),('items',ITEM,sorted({i[':db/id']for q,i in items})),('old-generators','[*]',[p['old_generator'][':db/id']for p in plans.values()])];(directory/'native-pulls.edn').write_text(dumps(groups)+'\n');binary=ROOT/'reference/mathacademy/repairs/2026-10-20-explicit-none/native-preview';p=subprocess.run([str(binary),str(directory),SOURCE],input='PREVIEW\n',env=DB.environment,capture_output=True,text=True,timeout=180);(directory/'preview.stderr').write_text(p.stderr);p.check_returncode();report=loads((directory/'preview.edn').read_text());assert report[':edb/db-before-t']==identity['basis'],'Database advanced; refresh unsubmitted preparation'
 proposed={n:loads((directory/'speculative'/(n+'.edn')).read_text())for n,_,_ in groups};check(plans,proposed,report,False);save('content/proposed.json',proposed)
 request={**identity,'source':SOURCE,'endpoint':str(DB.config.endpoint),'sha256':sha(directory/'transaction.edn'),'request_key':'integration-lesson-quality-v2-'+str(identity['basis'])+'-'+sha(directory/'transaction.edn'),'plan_sha256':sha(directory/'plan.json')};save('content/request.json',request);print(json.dumps({'preview_passed':True,'basis':identity['basis'],'new_questions':len(allnew),'retired':sum(len(p['withdrawn'])for p in plans.values()),'generator_versions':3}),flush=True)

def check(plans,state,report,committed):
 consumed=set();globalids=report[':edb/tempids'];source_id=helper.NAMES[SOURCE];instant_id=helper.NAMES[':db/txInstant']
 assert report[':edb/committed']is committed
 for kpstr,plan in plans.items():
  kp=int(kpstr);helper.KP=kp;ids={**globalids,'new-generator':globalids['new-generator-'+kpstr]};newids={value for key,value in globalids.items()if key.startswith('question-')and any(key=='question-'+r['question'][':question/id']for r in plan['replacements'])}
  for r in plan['replacements']:
   for f in r['question'][':question/answer-fields']:
    newids.add(globalids['field-'+f[':answer-field/id']]);newids.update(globalids['answer-'+a[':answer/id']]for a in f[':answer-field/choices'])
  owned=newids|{kp,ids['new-generator'],plan['old_generator'][':db/id']}|set(plan['withdrawn']);data=[row for row in report[':edb/tx-data']if row[0]in owned or row[1]==instant_id];consumed.update(tuple(row)for row in data)
  local={**report,':edb/tempids':ids,':edb/tx-data':data};helper.check_datoms(plan,local,committed)
  itemids={i[':db/id']for q,i in plan['items_before']};substate={'kp':[next(k for k in state['kps']if k[':db/id']==kp)],'items':[i for i in state['items']if i[':db/id']in itemids],'old-generator':[next(g for g in state['old-generators']if g[':db/id']==plan['old_generator'][':db/id'])]};helper.check_state(plan,substate,local)
 assert consumed=={tuple(row)for row in report[':edb/tx-data']},'Unexpected transaction datoms outside the reviewed KPs'

def commit():
 directory=H/'content';request=json.loads((directory/'request.json').read_text());assert sha(directory/'plan.json')==request['plan_sha256'];plan=json.loads((directory/'plan.json').read_text());report=helper.submit(directory,request);groups=loads((directory/'native-pulls.edn').read_text());after=native(directory/'committed',report[':edb/db-after-t'],groups);check(plan['kps'],after,report,True);save('content/committed.json',after)
 before=native(directory/'historical',request['basis'],groups);assert helper.same(before['kps'],[p['before']['kp'][0]for p in plan['kps'].values()]);assert helper.same(before['items'],[i for q,i in plan['items_before']])
 for p in plan['kps'].values():verify_package(Path(DB.config.math_root)/Path(p['generator_reference']).parent,p['generator_digest'])
 result={'passed':True,'committed':True,'basis_before':request['basis'],'basis_after':report[':edb/db-after-t'],'retired_questions':[q for p in plan['kps'].values()for q in p['withdrawn']],'new_questions':[{ 'kp':int(k),'id':report[':edb/tempids']['question-'+r['question'][':question/id']],'uuid':r['question'][':question/id'],'difficulty':r['question'][':question/difficulty'],'family':r['generation']['family']}for k,p in plan['kps'].items()for r in p['replacements']],'generators':{k:p['generator_reference']for k,p in plan['kps'].items()},'all_existing_keys_answers_and_solutions_unchanged':True,'all_math_academy_sources_unchanged':True,'all_multistep_source_links_unchanged':True,'learner_items_unchanged':len(plan['items_before']),'historical_snapshot_reproduced':True};save('verification.json',result);print(json.dumps({'committed':True,'basis':result['basis_after'],'new_questions':len(result['new_questions']),'retired_questions':result['retired_questions'],'generator_versions':3,'learner_items_preserved':result['learner_items_unchanged']}),flush=True)
if __name__=='__main__':{'prepare':prepare,'commit':commit}[sys.argv[1]]()
