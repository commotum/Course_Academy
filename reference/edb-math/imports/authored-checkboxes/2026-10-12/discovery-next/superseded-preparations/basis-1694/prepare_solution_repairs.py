"""Prepare and speculatively validate separate definite solution corrections; never submit."""
import hashlib,importlib.util,json,subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('migration',OUT/'prepare.py');migration=importlib.util.module_from_spec(spec);spec.loader.exec_module(migration)
edb=migration.edb
plan=json.loads((OUT/'plan.json').read_text());snapshot=edb.loads((OUT/'snapshot.edn').read_text());qs={q[':db/id']:q for q, in snapshot['questions']}
directory=OUT/'optional-solution-repairs';directory.mkdir(exist_ok=True)
assert not list(directory.glob('commit*')),'Do not rebuild submitted solution corrections'
rows=json.loads((OUT/'resolutions.json').read_text())['questions'];changes=[];forms=[]
for row in rows:
 proposed=None;reason=[]
 for issue in row.get('content_repairs',[]):
  if issue.get('required_for_consistent_solution'):
   assert row.get('proposed_worked_solution'),row['id'];proposed=row['proposed_worked_solution'];reason.append(issue['description'])
  if issue.get('attribute')==':question/worked-solution':proposed=issue['after'];reason.append(issue['reason'])
 if proposed is None:continue
 q=qs[row['id']];before=q[':question/worked-solution'];assert proposed!=before
 forms.extend([[edb.kw('db/cas'),row['id'],edb.kw('question/worked-solution'),before,proposed],{edb.kw('db/id'):row['id'],edb.kw('db/ensure'):edb.kw('question/validate')}])
 changes.append({'id':row['id'],'ma_id':row['ma_id'],'solution_before':before,'solution_after':proposed,'reason':reason})
image_repairs=json.loads((OUT/'reviews/image-solution-repairs.json').read_text())['questions']
for repair in image_repairs:
 assert repair['id']not in {change['id']for change in changes}
 q=qs[repair['id']];before=q[':question/worked-solution'];after=repair['after']
 assert before==repair['before']and before!=after
 assert q[':question/math-academy-id']==repair['ma_id']
 forms.extend([[edb.kw('db/cas'),repair['id'],edb.kw('question/worked-solution'),before,after],{edb.kw('db/id'):repair['id'],edb.kw('db/ensure'):edb.kw('question/validate')}])
 changes.append({'id':repair['id'],'ma_id':repair['ma_id'],'solution_before':before,'solution_after':after,'reason':[repair['reason']],'proof':repair['proof'],'evidence':'reviews/image-solution-repairs.json'})
path=directory/'transaction.edn';path.write_text('[\n'+'\n'.join(' '+edb.dumps(form)for form in forms)+'\n]\n');sha=hashlib.sha256(path.read_bytes()).hexdigest()
basis=plan['basis']+len(plan['batches'])
counts={'questions':len(changes),'new_checkbox_fields':0,'new_boolean_answers':0,'saved_responses_mapped':0}
manifest={'state':'optional_prepared_not_submitted','basis':basis,'captured_basis':plan['basis'],'source':edb.SOURCE,'transaction_sha256':sha,'counts':counts,'questions':changes,'retained_original_entities':[],'changes_correct_keys':False,'requires_all_conversion_batches_first':True}
(directory/'plan.json').write_text(json.dumps(manifest,indent=2)+'\n')
request={'state':'prepared_not_submitted','database':'math','lineage':plan['lineage'],'source':edb.SOURCE,'basis':basis,'must_use_basis_guard':True,'request_key':f'discovery-next-solution-repairs-v1-{basis}-{sha}','sha256':sha,'transaction_file':str(path),'requires_all_conversion_batches_first':True}
(directory/'prepared-request.json').write_text(json.dumps(request,indent=2)+'\n')
source=OUT/'solution-preview.rs';binary=OUT/'solution-preview'
from capture.scripts.database.preview import _library
from types import SimpleNamespace
library=_library(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math')))
inputs=[source,library,migration.ROOT/'engine/edb/answer_fields.rs',migration.ROOT/'engine/edb/configuration.rs',migration.ROOT/'engine/edb/progress.rs']
hashes={str(p):migration.digest(p)for p in inputs}
command=['rustc','--edition=2024','-O',str(source),'--extern','edb_core='+str(library),'-L','dependency='+str(library.parent),'-o',str(binary)]
subprocess.run(command,check=True)
assert hashes=={str(p):migration.digest(p)for p in inputs}
build={'command':command,'inputs':hashes,'source_sha256':migration.digest(source),'library':str(library),'library_sha256':migration.digest(library),'binary_sha256':migration.digest(binary),'database_writes':0}
(directory/'native-build.json').write_text(json.dumps(build,indent=2)+'\n')
result=subprocess.run([str(binary),str(OUT),edb.SOURCE,str(len(plan['batches'])),str(plan['basis'])],env=edb.DB.env,check=True,capture_output=True,text=True,timeout=180)
(directory/'preview.log').write_text(result.stdout)
verification=migration.verify_report(directory,edb.loads((directory/'preview.edn').read_text()),snapshot)
verification['checks']=['Application-native validators passed','Exact worked-solution CAS assertions/retractions and every datom source checked','Only reviewed worked solutions and the transaction instant changed; answer keys, fields, prompts, ratings, memberships and learner state unchanged']
(directory/'preview.json').write_text(json.dumps(verification,indent=2)+'\n')
print(json.dumps({'optional_solutions_prepared_and_previewed':len(changes),'basis_guard':basis,'database_writes':0}))
