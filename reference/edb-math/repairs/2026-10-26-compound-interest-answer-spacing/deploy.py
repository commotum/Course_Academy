"""Publish hint-free packages and replace only the hinted full calculations."""
from collections import Counter
import json,os,platform,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,GeneratorCommitter,StaleBasis,digest,dumps,loads,kw,file_lock,normalized_question,jsonable
from scripts.generator_packages import publish_package,build_manifest,manifest_digest,materialize_package,verify_package
from capture.scripts.storage import atomic_json

def prepare(p,item,d):
 kp=item['kp'];work=d/'publication';assert json.loads((d/'generator-verification.json').read_text())['passed'];assert json.loads((H/'grader-verification.json').read_text())['documented_unresolved_checks']==0;assert json.loads((H/'render/rendering.json').read_text())['passed']
 files=[*item['files'],'rounded_finance.py']
 manifest=build_manifest(d/'package','generator.py',files,dependencies={'python':platform.python_version(),'packages':{}});package=publish_package(d/'package','generator.py',files,p.config.math_root,dependencies=manifest['dependencies'],expected_digest=manifest_digest(manifest));runtime=work/'runtime'/package.digest
 entry=runtime/'generator.py'if runtime.exists()else materialize_package(package.reference,p.config.math_root,runtime);verify_package(runtime,package.digest)
 records=json.loads((d/'candidate-pool.json').read_text())
 out=subprocess.run([sys.executable,str(entry),'--difficulty','moderate','--count','5','--seed','20261026','--format','json'],check=True,capture_output=True,text=True,timeout=60,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 assert json.loads(out.stdout)==json.loads((d/'fresh-samples.json').read_text())

 prepared=p.prepare(kp,records,package.reference,package.digest,work,source_snapshot=json.loads((d/'fresh-source/source.json').read_text()),assets_directory=d/'package',expected_registered_generator=item['registered_generator']);assert prepared['new_questions']+prepared['duplicates']==5 and prepared['new_questions']>=0
 before=loads(prepared['before_edn']);captured=json.loads((d/'before.json').read_text());active=[q for q in before[':knowledge-point/questions']if not q.get(':question/math-academy-id')and not q.get(':question/retired')]
 assert{q[':db/id']for q in active}=={q[':db/id']for q in captured[':knowledge-point/questions']if not q.get(':question/math-academy-id')and not q.get(':question/retired')}
 from scripts.generator_publish import content_fingerprint
 final_fps={content_fingerprint(r['question'])for r in records}
 retirement=[q for q in active if content_fingerprint(q)not in final_fps];assert len(retirement)==prepared['new_questions'];ids=[q[':db/id']for q in retirement]
 rows=p.client.query('[:find (pull ?q [:db/id :question/id :question/math-academy-id :question/retired {:task-item/_content [:db/id]} {:knowledge-point/_canonical-example [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',[ids],work,'retirements-before',prepared['basis']);assert len(rows)==prepared['new_questions']
 batch=loads(prepared['batch_edn'])
 for[q]in rows:
  assert not q.get(':question/math-academy-id')and not q.get(':knowledge-point/_canonical-example')and not q.get(':question/retired')
  old=q.get(':question/retired');batch['forms'].append([kw('db/cas'),q[':db/id'],kw('question/retired'),old,True]);batch['assertions'].append([q[':db/id'],kw('question/retired'),True])
  if old is False:batch['retractions'].append([q[':db/id'],kw('question/retired'),False])
 prepared['batch_edn']=dumps(batch);prepared['retirements']=jsonable([r[0]for r in rows]);prepared['all_final_records']=json.loads((d/'accepted-pool.json').read_text());prepared['package_manifest']=manifest;atomic_json(work/'preparation.json',prepared)
 committer=GeneratorCommitter(p.config,p.client,work);committer.preview(batch,loads(prepared['snapshot_edn']));request=committer.save_request(batch,loads(prepared['snapshot_edn']),digest(prepared));return prepared,committer,request

def apply(p,item,d,prepared,committer,request):
 assert request['content_sha256']==digest(prepared);receipt=committer.submit(request);proof=committer.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t'];work=d/'publication';kp=item['kp'];after=p.read_kp(kp,work/'after',basis);before=loads(prepared['before_edn']);questions={str(q[':question/id']):q for q in after[':knowledge-point/questions']};retired={q[':db/id']for q in prepared['retirements']};assert len(questions)==len(before[':knowledge-point/questions'])+prepared['new_questions']
 for q in before[':knowledge-point/questions']:
  expected=dict(q)
  if q[':db/id']in retired:expected[kw('question/retired')]=True
  assert questions[str(q[':question/id'])]==expected,('Existing content changed',q[':db/id'])
 final=[]
 for record in prepared['all_final_records']:
  q=questions[record['question'][':question/id']];assert not q.get(':question/retired')and not q.get(':question/math-academy-id');assert normalized_question(q)==normalized_question(record['question']);final.append({'entity':q[':db/id'],'uuid':str(q[':question/id']),'band':record['question'][':question/difficulty'],'family':record['generation'].get('family',record['generation'].get('template'))})
 assert len(final)==5 and{q[':db/id']for q in questions.values()if not q.get(':question/math-academy-id')and not q.get(':question/retired')}=={r['entity']for r in final}
 for q in questions.values():
  if q[':db/id']in{r['entity']for r in final}:assert'You may use $'not in q[':question/problem']and'Endpoint values:'not in q[':question/problem']
 exclude={':knowledge-point/questions',':knowledge-point/question-generator'};assert{k:v for k,v in before.items()if k not in exclude}=={k:v for k,v in after.items()if k not in exclude};reg=after[':knowledge-point/question-generator'];assert reg[':question-generator/script']==prepared['generator_path']
 rows=p.client.query('[:find (pull ?q [:db/id :question/retired {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/retired true]]',[sorted(retired)],work,'retirements-after',basis);assert len(rows)==prepared['new_questions']
 for[q]in rows:
  old=next(r for r in prepared['retirements']if r[':db/id']==q[':db/id']);assert jsonable(q.get(':task-item/_content'))==old.get(':task-item/_content')
 original_questions=[q for q in before[':knowledge-point/questions']if q[':db/id']in retired]
 old_ids=sorted(q[':db/id']for q in original_questions)
 old_entities={q[':db/id']for q in before[':knowledge-point/questions']}
 new_ids=sorted(r['entity']for r in final if r['entity']not in old_entities)
 assert len(old_ids)==len(new_ids)
 replacement_map=[{'old':a,'new':b}for a,b in zip(old_ids,new_ids)]

 result={'passed':True,'committed':True,'basis_after':basis,'new_reference':prepared['generator_path'],'new_questions':final,'new_question_entities':[r['entity']for r in final if r['entity']not in{q[':db/id']for q in before[':knowledge-point/questions']}],'retired_questions':sorted(retired),'replacements':replacement_map,'unchanged_full_questions':prepared['duplicates'],'imported_questions_preserved':sum(bool(q.get(':question/math-academy-id'))for q in before[':knowledge-point/questions']),'canonical_preserved':True,'old_question_and_answer_content_preserved':True,'saved_attempt_references_preserved':True,'request_key':request['request_key'],**proof}
 atomic_json(work/'verification.json',result);atomic_json(d/'verification.json',result);committer.retire(request,'verified',result);print(kp,'registered; replaced',prepared['new_questions'],'and preserved',prepared['duplicates'],'full calculations; basis',basis,flush=True)

def main():
 p=Publisher.from_environment(source=':agent/codex')
 for item in json.loads((H/'capture.json').read_text())['knowledge_points']:
  kp=item['kp'];d=H/str(kp);work=d/'publication';lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock'
  with file_lock(lock),file_lock(Path(p.config.request_directory)/'api.lock'):
   committer=GeneratorCommitter(p.config,p.client,work);request=committer.pending()
   if request:apply(p,item,d,json.loads((work/'preparation.json').read_text()),committer,request);continue
   if(d/'verification.json').exists():continue
   for attempt in range(3):
    request=None
    try:
     prepared,committer,request=prepare(p,item,d);apply(p,item,d,prepared,committer,request);break
    except StaleBasis:
     if request:committer.retire(request,'rejected_stale_basis',{'reason':'Confirmed stale rejection; reprepare'})
   else:raise RuntimeError('Repeated publication race; evidence preserved')
if __name__=='__main__':main()
