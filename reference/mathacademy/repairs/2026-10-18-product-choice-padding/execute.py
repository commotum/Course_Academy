"""Publish the repaired generator and apply guarded choice-only EDB edits."""
import copy,hashlib,json,threading
from collections import Counter
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient,QUESTION_PULL
from capture.scripts.database.edn import dumps,loads,kw
from scripts.generator_packages import publish_package,resolve_registered_script
from .prepare import clean_answer,Exact,PHANTOM
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SOURCE=':agent/codex'
DB=EDBClient(Config(),threading.Event())
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def run():
 changes=json.loads((HERE/'changes.json').read_text());info=json.loads((HERE/'generator-update.json').read_text());manifest=json.loads((HERE/'generator-manifest.json').read_text())
 assert json.loads((HERE/'generator-checks.json').read_text())['passed']
 assert json.loads((HERE/'ui/rendering.json').read_text())['passed']
 for c in changes:
  assert c['after']==clean_answer(c['before'])==clean_answer(c['after'])
  assert Exact(PHANTOM.sub('',c['before'])).value()==Exact(c['after']).value()
 package=publish_package(HERE/'generator','generator.py',manifest['files'],DB.config.math_root,dependencies=manifest['dependencies'],expected_digest=info['digest']);assert package.reference==info['new_reference']
 edits=changes+[{'entity':info['entity'],'attribute':':question-generator/script','before':info['old_reference'],'after':info['new_reference']}]
 forms=[[kw(':db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']] for c in edits]
 for qid in sorted({c['question'] for c in changes}):forms.append([kw(':db/ensure'),qid,kw(':question/validate')])
 before=loads((HERE/'all-questions.edn').read_text())
 for [q] in before:
  if q[':db/id'] in {c['question'] for c in changes}:
   for f in q[':question/answer-fields']:forms.append([kw(':db/ensure'),f[':db/id'],kw(':answer-field/validate')])
 txfile=HERE/'transaction.edn';txfile.write_text(dumps(forms)+'\n')
 attrs={str(i):e for e,i in loads((HERE.parent/'2026-10-18-big-parentheses/evidence/idents.edn').read_text())}
 expected=Counter((c['entity'],attrs[c['attribute']],c['before'],False) for c in edits);expected.update((c['entity'],attrs[c['attribute']],c['after'],True) for c in edits)
 def check_report(report):
  actual=Counter();times=0
  for e,a,v,tx,source,added in report[':edb/tx-data']:
   assert source==attrs[SOURCE]
   if a==attrs[':db/txInstant']:assert e==tx and added;times+=1
   else:actual[(e,a,v,added)]+=1
  assert actual==expected,(actual-expected,expected-actual)
  assert times==1 and not report[':edb/tempids']
 intent=HERE/'commit-intent.json'
 if intent.exists():request=json.loads(intent.read_text())
 else:
  preview=DB.command('with','--source',SOURCE,'--file',txfile,timeout=150);(HERE/'preview.edn').write_text(preview)
  report=loads(preview);assert report[':edb/committed'] is False;check_report(report)
  identity=DB.status();assert identity['lineage']==json.loads((HERE/'identity.json').read_text())['lineage']
  basis=report[':edb/db-before-t'];digest=hashlib.sha256(txfile.read_bytes()).hexdigest()
  request={'source':SOURCE,'basis':basis,'sha256':digest,'transaction_file':str(txfile),'endpoint':DB.config.endpoint,'request_key':'product-choice-padding-v1-b'+str(basis)+'-'+digest};save('commit-intent.json',request)
 assert hashlib.sha256(txfile.read_bytes()).hexdigest()==request['sha256']
 if not (HERE/'receipt.edn').exists():
  output=DB.command('transact','--source',request['source'],'--file',request['transaction_file'],'--basis',request['basis'],'--endpoint',request['endpoint'],'--request-key',request['request_key'],'--timeout-ms','120000',timeout=150);(HERE/'receipt.edn').write_text(output)
 report=loads((HERE/'receipt.edn').read_text());assert report[':edb/committed'] is True;check_report(report);basis=report[':edb/basis-t']
 rows=DB.query('''[:find (pull ?q '''+QUESTION_PULL+''') :in $ ?topic :where [?topic :topic/knowledge-points ?kp] (or-join [?kp ?q] [?kp :knowledge-point/questions ?q] [?kp :knowledge-point/canonical-example ?q])]''',[17592186049861],HERE/'committed','all-questions',basis)
 def clean(q):
  q=copy.deepcopy(q)
  for f in q.get(':question/answer-fields',[]):
   for a in f.get(':answer-field/choices',[]):a.pop(':task-item/_responses',None)
  return json.loads(json.dumps(q,default=str))
 desired=json.loads((HERE/'all-questions-after.json').read_text());assert {q[':db/id']:clean(q) for [q] in rows}=={q[':db/id']:clean(q) for [q] in desired}
 assert '\\phantom' not in json.dumps(rows,default=str)
 generator=DB.query('[:find (pull ?e [*]) :in $ ?e :where [?e :question-generator/id _]]',[info['entity']],HERE/'committed','generator',basis)[0][0];assert generator[':question-generator/script']==info['new_reference'];resolve_registered_script(info['new_reference'],ROOT,DB.config.math_root)
 result={'passed':True,'committed':True,'basis_before':report[':edb/db-before-t'],'basis_after':basis,'questions_audited':len(rows),'questions_repaired':5,'choices_repaired':len(changes),'generator_updated':info['new_reference'],'draft_generators_patched':len(info['workspaces']),'exact_mathematical_values_preserved':True,'question_choice_and_correct_answer_ids_preserved':True,'native_question_and_answer_field_validation_passed':True,'exact_committed_readback':True,'remaining_phantom_choices':0,'only_choice_text_and_generator_reference_changed':True,'datoms':len(report[':edb/tx-data'])};save('verification.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':run()
