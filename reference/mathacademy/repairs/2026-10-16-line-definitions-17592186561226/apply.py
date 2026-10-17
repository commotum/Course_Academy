"""Apply the requested single-question layout edit with CAS and native verification."""
import copy,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
from scripts.database.edn import loads,dumps,kw
from scripts.database.preview import native_executable
HERE=Path(__file__).resolve().parent;PRIOR=HERE.parent/'2026-10-16-system-equations-display'
spec=importlib.util.spec_from_file_location('prior_read',PRIOR/'read.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
DB=m.DB;SOURCE=':agent/gpt-6.1-sol-high';QID=17592186561226
snapshot=loads((HERE/'snapshot.edn').read_text());change=json.loads((HERE/'change.json').read_text())
def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2,default=str)+'\n')
def check(report):
 datoms=report[':edb/tx-data'];assert len(datoms)==3 and not report[':edb/tempids']
 assert all(d[4]==17592186045436 for d in datoms)
 edits=[(e,a,v,add) for e,a,v,tx,s,add in datoms if a!=50]
 assert sorted(edits)==sorted([(QID,1071,change['before'],False),(QID,1071,change['after'],True)])

if not (HERE/'intent.json').exists():
 assert json.loads((HERE/'ui/summary.json').read_text())['passed']
 assert json.loads((HERE/'ui/summary.json').read_text())['changes_sha256']==hashlib.sha256((HERE/'change.json').read_bytes()).hexdigest()
 forms=[[kw(':db/cas'),QID,kw(':question/problem'),change['before'],change['after']], [kw(':db/ensure'),QID,kw(':question/validate')]]
 (HERE/'transaction.edn').write_text(dumps(forms)+'\n')
 groups=[['question',m.QUESTION,[QID]],['items',m.ITEM,[item[':db/id'] for [item] in snapshot['items']]]]
 (HERE/'native-pulls.edn').write_text(dumps(groups)+'\n')
 files=['reference/mathacademy/repairs/2026-10-16-system-equations-display/native/preview.rs','capture/scripts/database/preview.py','engine/edb/answer_fields.rs','engine/edb/configuration.rs','engine/edb/progress.rs']
 binary=native_executable(DB.config,DB.stop_event,files,'systems-preview')
 identity=DB.status();assert identity['lineage']==snapshot['lineage']
 result=subprocess.run([str(binary),str(HERE),SOURCE,str(identity['basis'])],env=DB.environment,capture_output=True,text=True,timeout=120)
 (HERE/'preview.stderr').write_text(result.stderr);result.check_returncode();(HERE/'preview.edn').write_text(result.stdout);check(loads(result.stdout))
 assert loads((HERE/'preview-question-before.edn').read_text())==[snapshot['question']]
 expected=copy.deepcopy(snapshot['question']);expected[':question/problem']=change['after']
 assert loads((HERE/'preview-question-after.edn').read_text())==[expected]
 assert loads((HERE/'preview-items-before.edn').read_text())==loads((HERE/'preview-items-after.edn').read_text())
 digest=hashlib.sha256((HERE/'transaction.edn').read_bytes()).hexdigest()
 intent={'basis':identity['basis'],'source':SOURCE,'lineage':identity['lineage'],'sha256':digest,'request_key':f'line-layout-{QID}-{identity["basis"]}-{digest}'}
 save('intent.json',intent)
intent=json.loads((HERE/'intent.json').read_text());assert intent['sha256']==hashlib.sha256((HERE/'transaction.edn').read_bytes()).hexdigest()
if not (HERE/'receipt.edn').exists():
 receipt=DB.command('transact','--source',intent['source'],'--file',HERE/'transaction.edn','--basis',intent['basis'],'--endpoint',DB.config.endpoint,'--request-key',intent['request_key'],'--timeout-ms','120000',timeout=150)
 (HERE/'receipt.edn').write_text(receipt)
report=loads((HERE/'receipt.edn').read_text());assert report[':edb/committed'];check(report)
for group,pattern,ids in loads((HERE/'native-pulls.edn').read_text()):
 rows=DB.query('[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e _ _]]',[ids],HERE/'committed',group,report[':edb/basis-t']) if ids else []
 assert {r[0][':db/id']:r[0] for r in rows}=={e[':db/id']:e for e in loads((HERE/f'preview-{group}-after.edn').read_text())}
save('verification.json',{'passed':True,'committed':True,'question':QID,'basis_before':intent['basis'],'basis_after':report[':edb/basis-t'],'only_prompt_changed':True,'answers_difficulty_solution_and_saved_state_preserved':True,'exact_readback':True})
print((HERE/'verification.json').read_text())
