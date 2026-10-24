"""Replace unserved preview banks and register the corrected immutable packages."""
from collections import Counter
import json,os,platform,subprocess,sys
from pathlib import Path
import sympy
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'generate'))
from scripts.generator_publish import Publisher,GeneratorCommitter,StaleBasis,digest,dumps,loads,kw,file_lock,normalized_question,jsonable
from scripts.generator_packages import publish_package,build_manifest,manifest_digest,materialize_package,verify_package
from capture.scripts.storage import atomic_json
from substitution_pedagogy import CASES

def prepare(p,kp,d):
 work=d/'bank-refinement';proof=json.loads((d/'verification.json').read_text());assert not proof.get('bank_refinement_verified')
 assert json.loads((H/'bank-shortcut-verification.json').read_text())['passed']
 assert json.loads((d/'grader-verification.json').read_text())['documented_unresolved_checks']==0
 assert json.loads((H/'render/rendering.json').read_text())['passed']
 manifest=build_manifest(d/'package','generator.py',['generator.py','substitution_pedagogy.py','source-evidence.json','band-contract.json'],dependencies={'python':platform.python_version(),'packages':{'sympy':sympy.__version__}})
 package=publish_package(d/'package','generator.py',manifest['files'],p.config.math_root,dependencies=manifest['dependencies'],expected_digest=manifest_digest(manifest));runtime=work/'runtime'/package.digest
 entry=runtime/'generator.py'if runtime.exists()else materialize_package(package.reference,p.config.math_root,runtime);verify_package(runtime,package.digest)
 records=json.loads((d/'candidate-pool.json').read_text());reproduced=[]
 for band in('easy','moderate','hard'):
  output=subprocess.run([sys.executable,str(entry),'--difficulty',band,'--count','8','--seed','20261024','--format','json'],check=True,capture_output=True,text=True,timeout=60,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});reproduced.extend(json.loads(output.stdout))
 assert reproduced==records
 first=json.loads((d/'publication/preparation.json').read_text());old_radio={r['question'][':question/id']for r in first['records']if r['question'][':question/answer-fields'][0][':answer-field/type']==':answer-field.type/radio'};assert len(old_radio)in(8,24)
 prepared=p.prepare(kp,records,package.reference,package.digest,work,source_snapshot=json.loads((d/'source/source.json').read_text()),assets_directory=d/'package',expected_registered_generator=proof['new_reference'])
 assert prepared['new_questions']==len(old_radio)and prepared['duplicates']==24-len(old_radio)
 before=loads(prepared['before_edn']);questions={str(q[':question/id']):q for q in before[':knowledge-point/questions']}
 assert{str(q[':question/id'])for q in questions.values()if not q.get(':question/math-academy-id')and not q.get(':question/retired')}=={r['uuid']for r in proof['new_questions']}
 ids=[questions[qid][':db/id']for qid in old_radio]
 rows=p.client.query('[:find (pull ?q [:db/id :question/id :question/math-academy-id :question/retired {:task-item/_content [:db/id]} {:knowledge-point/_canonical-example [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',[ids],work,'unserved-before',prepared['basis'])
 assert len(rows)==len(ids)
 batch=loads(prepared['batch_edn'])
 for[q]in rows:
  assert not q.get(':question/math-academy-id')and not q.get(':question/retired')and not q.get(':task-item/_content')and not q.get(':knowledge-point/_canonical-example')
  batch['forms'].append([kw('db/cas'),q[':db/id'],kw('question/retired'),None,True]);batch['assertions'].append([q[':db/id'],kw('question/retired'),True])
 prepared['batch_edn']=dumps(batch);prepared['retired_preview_ids']=ids;prepared['initial_verification']=proof;prepared['all_final_records']=json.loads((d/'accepted-pool.json').read_text());prepared['package_manifest']=manifest
 atomic_json(work/'preparation.json',prepared);committer=GeneratorCommitter(p.config,p.client,work);committer.preview(batch,loads(prepared['snapshot_edn']));request=committer.save_request(batch,loads(prepared['snapshot_edn']),digest(prepared));return prepared,committer,request

def apply(p,kp,d,prepared,committer,request):
 assert request['content_sha256']==digest(prepared)
 receipt=committer.submit(request);proof=committer.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t'];work=d/'bank-refinement';after=p.read_kp(kp,work/'after',basis);before=loads(prepared['before_edn']);questions={str(q[':question/id']):q for q in after[':knowledge-point/questions']};retired=set(prepared['retired_preview_ids'])
 assert len(questions)==len(before[':knowledge-point/questions'])+len(retired)
 for q in before[':knowledge-point/questions']:
  expected=dict(q)
  if q[':db/id']in retired:expected[kw('question/retired')]=True
  assert questions[str(q[':question/id'])]==expected
 final=[]
 for record in prepared['all_final_records']:
  q=questions[record['question'][':question/id']];assert not q.get(':question/retired')and not q.get(':question/math-academy-id');assert normalized_question(q)==normalized_question(record['question']);final.append({'entity':q[':db/id'],'uuid':str(q[':question/id']),'band':record['question'][':question/difficulty'],'template':record['generation']['template']})
 assert len(final)==24 and{q[':db/id']for q in questions.values()if not q.get(':question/math-academy-id')and not q.get(':question/retired')}=={r['entity']for r in final}
 exclude={':knowledge-point/questions',':knowledge-point/question-generator'};assert{k:v for k,v in before.items()if k not in exclude}=={k:v for k,v in after.items()if k not in exclude}
 assert after[':knowledge-point/question-generator'][':question-generator/script']==prepared['generator_path']
 result={**prepared['initial_verification'],'basis_after':basis,'new_questions':final,'new_reference':prepared['generator_path'],'bank_refinement_verified':True,'retired_unserved_preview_questions':sorted(retired),'bank_refinement_request_key':request['request_key'],'bank_refinement_receipt':proof}
 atomic_json(work/'verification.json',result);atomic_json(d/'verification.json',result);committer.retire(request,'verified',result);print(kp,'verified final pool; replaced unserved banks',len(retired),'basis',basis,flush=True)

def main():
 p=Publisher.from_environment(source=':agent/codex')
 for kp in CASES:
  d=H/str(kp);work=d/'bank-refinement';lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock'
  with file_lock(lock),file_lock(Path(p.config.request_directory)/'api.lock'):
   committer=GeneratorCommitter(p.config,p.client,work);request=committer.pending()
   if request:apply(p,kp,d,json.loads((work/'preparation.json').read_text()),committer,request);continue
   if json.loads((d/'verification.json').read_text()).get('bank_refinement_verified'):continue
   for attempt in range(3):
    request=None
    try:
     prepared,committer,request=prepare(p,kp,d);apply(p,kp,d,prepared,committer,request);break
    except StaleBasis:
     if request:committer.retire(request,'rejected_stale_basis',{'reason':'Confirmed stale rejection; reprepare'})
   else:raise RuntimeError('Repeated publication race')
if __name__=='__main__':main()
