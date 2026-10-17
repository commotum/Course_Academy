"""Guarded display-only repair with exact native preview, receipt and readback."""
import copy,hashlib,json,subprocess,sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from read import HERE,ROOT,DB,QUESTION,ITEM
from scripts.database.edn import loads,dumps,kw
from scripts.database.preview import native_executable
SOURCE=':agent/gpt-6.1-sol-high'
snapshot=loads((HERE/'snapshot.edn').read_text())
changes=json.loads((HERE/'changes.json').read_text())
attrs=dict(snapshot['schema']);attrids={str(v):k for k,v in attrs.items()}
sourceid=attrids[SOURCE]
qids=sorted({c['entity'] for c in changes if c['attribute'].startswith(':question/')})
tids=sorted({c['entity'] for c in changes if c['attribute'].startswith(':tutorial/')})
original={e[':db/id']:e for g in ('questions','tutorials') for [e] in snapshot[g]}
by_id=lambda rows:{e[':db/id']:e for e in rows}
def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def report_check(report):
 expected=Counter((c['entity'],attrids[c['attribute']],c['before'],False) for c in changes)
 expected.update((c['entity'],attrids[c['attribute']],c['after'],True) for c in changes)
 actual=Counter();times=0
 for e,a,v,tx,source,added in report[':edb/tx-data']:
  assert source==sourceid
  if a==attrids[':db/txInstant']:
   assert e==tx and added;times+=1
  else:actual[(e,a,v,added)]+=1
 assert actual==expected and times==1 and not report[':edb/tempids']
 assert len(report[':edb/tx-data'])==355

def prepare_preview():
 assert not (HERE/'commit-intent.json').exists()
 forms=[[kw(':db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']] for c in changes]
 forms.extend([[kw(':db/ensure'),i,kw(':question/validate')] for i in qids])
 forms.extend([[kw(':db/ensure'),i,kw(':tutorial/validate')] for i in tids])
 (HERE/'transaction.edn').write_text(dumps(forms)+'\n')
 files=['reference/mathacademy/repairs/2026-10-16-system-equations-display/native/preview.rs',
   'capture/scripts/database/preview.py','engine/edb/answer_fields.rs','engine/edb/configuration.rs','engine/edb/progress.rs']
 executable=native_executable(DB.config,DB.stop_event,files,'systems-preview')
 save('native/build.json',json.loads(executable.with_suffix('.json').read_text())|{'executable':str(executable)})
 identity=DB.status();assert identity['lineage']==snapshot['lineage'];basis=identity['basis']
 items=DB.query('[:find ?q (pull ?item '+ITEM+') :in $ [?q ...] :where [?item :task-item/content ?q]]',[qids],HERE/'refresh','items',basis)
 groups=[['questions',QUESTION,qids],['tutorials','[*]',tids],['items',ITEM,[v[':db/id'] for q,v in items]]]
 (HERE/'native-pulls.edn').write_text(dumps(groups)+'\n')
 result=subprocess.run([str(executable),str(HERE),SOURCE,str(basis)],env=DB.environment,capture_output=True,text=True,timeout=150)
 (HERE/'preview.stderr').write_text(result.stderr);result.check_returncode()
 (HERE/'preview.edn').write_text(result.stdout);report=loads(result.stdout);report_check(report)
 for group in ('questions','tutorials'):
  before=by_id(loads((HERE/f'preview-{group}-before.edn').read_text()))
  after=by_id(loads((HERE/f'preview-{group}-after.edn').read_text()))
  for eid,e in before.items():assert e==original[eid],('Content dependencies changed',eid)
  expected=copy.deepcopy(before)
  for c in changes:
   if c['entity'] in expected:expected[c['entity']][c['attribute']]=c['after']
  assert expected==after
 assert loads((HERE/'preview-items-before.edn').read_text())==loads((HERE/'preview-items-after.edn').read_text())
 digest=hashlib.sha256((HERE/'transaction.edn').read_bytes()).hexdigest()
 request={'source':SOURCE,'basis':basis,'lineage':identity['lineage'],'sha256':digest,
  'transaction_file':str(HERE/'transaction.edn'),'endpoint':str(DB.config.endpoint),
  'request_key':'systems-display-v1-b'+str(basis)+'-'+digest}
 save('prepared-request.json',request)
 save('preview-verification.json',{'passed':True,'committed':False,'basis':basis,'fields':177,'questions':108,'tutorials':2,'datoms':355,'native_entity_validation':True,'exact_math_preservation':True,'unchanged_answers_difficulties_memberships':True,'saved_task_items_unchanged':len(items),'exact_change_scope':True})
 print('Native preview passed at basis',basis,flush=True)
 return request

if '--preview-only' in sys.argv:
 prepare_preview();sys.exit(0)
if not (HERE/'commit-intent.json').exists():
 # Re-preview at the current basis immediately before retaining the request.
 request=prepare_preview()
 assert json.loads((HERE/'ui/preview/summary.json').read_text())['passed']
 save('commit-intent.json',request)
else:request=json.loads((HERE/'commit-intent.json').read_text())
assert hashlib.sha256(Path(request['transaction_file']).read_bytes()).hexdigest()==request['sha256']
if not (HERE/'receipt.edn').exists():
 output=DB.command('transact','--source',request['source'],'--file',request['transaction_file'],
  '--basis',request['basis'],'--endpoint',request['endpoint'],'--request-key',request['request_key'],'--timeout-ms','120000',timeout=150)
 (HERE/'receipt.edn').write_text(output)
report=loads((HERE/'receipt.edn').read_text());assert report[':edb/committed'] is True;report_check(report)
basis=report[':edb/basis-t'];fields=[]
for group,pattern,ids in loads((HERE/'native-pulls.edn').read_text()):
 def batch(groupids):return DB.query('[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e _ _]]',[groupids],HERE/'committed',group+'-'+str(groupids[0]),basis)
 with ThreadPoolExecutor(max_workers=3) as pool:rows=[r[0] for group_result in pool.map(batch,[ids[i:i+20] for i in range(0,len(ids),20)]) for r in group_result]
 assert by_id(rows)==by_id(loads((HERE/f'preview-{group}-after.edn').read_text())),group
 for e in rows:
  for c in changes:
   if c['entity']==e[':db/id']:fields.append({'entity':c['entity'],'attribute':c['attribute'],'value':e[c['attribute']]})
assert len(fields)==177
save('committed-fields.json',fields)
save('verification.json',{'passed':True,'committed':True,'basis_before':request['basis'],'basis_after':basis,'lineage':request['lineage'],'source':SOURCE,'request_key':request['request_key'],'transaction_sha256':request['sha256'],'fields':177,'questions':108,'tutorials':2,'datoms':355,'native_validation_passed':True,'exact_committed_readback':True,'answers_difficulties_memberships_preserved':True,'saved_learner_state_preserved':True,'change_scope_verified':True})
print('Committed and verified display repair at basis',basis,flush=True)
