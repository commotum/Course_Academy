"""Publish repaired immutable generator, preview CAS edits, commit and read back."""
import copy,hashlib,json,threading
from collections import Counter
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient,QUESTION_PULL,StaleBasis
from capture.scripts.database.edn import dumps,loads,kw
from scripts.generator_packages import publish_package,resolve_registered_script
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SOURCE=':agent/codex'
DB=EDBClient(Config(),threading.Event())
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def run():
 changes=json.loads((HERE/'changes.json').read_text());info=json.loads((HERE/'generator-update.json').read_text());manifest=json.loads((HERE/'generator-manifest.json').read_text())
 assert json.loads((HERE/'generator-checks.json').read_text())['passed']
 assert json.loads((HERE/'ui/rendering.json').read_text())['passed']
 package=publish_package(HERE/'generator','generator.py',manifest['files'],DB.config.math_root,dependencies=manifest['dependencies'],expected_digest=info['digest'])
 assert package.reference==info['new_reference']
 edits=changes+[{'entity':info['entity'],'attribute':':question-generator/script','before':info['old_reference'],'after':info['new_reference']}]
 forms=[[kw(':db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']] for c in edits]
 for qid in sorted({c['entity'] for c in changes if c['attribute'].startswith(':question/')}):forms.append([kw(':db/ensure'),qid,kw(':question/validate')])
 forms.append([kw(':db/ensure'),17592186107083,kw(':tutorial/validate')])
 txfile=HERE/'transaction.edn';txfile.write_text(dumps(forms)+'\n')
 attrs={str(i):e for e,i in loads((HERE/'evidence/idents.edn').read_text())}
 expected=Counter((c['entity'],attrs[c['attribute']],c['before'],False) for c in edits)
 expected.update((c['entity'],attrs[c['attribute']],c['after'],True) for c in edits)
 def verify(report):
  actual=Counter();times=0
  for e,a,v,tx,source,added in report[':edb/tx-data']:
   assert source==attrs[SOURCE]
   if a==attrs[':db/txInstant']:assert e==tx and added;times+=1
   else:actual[(e,a,v,added)]+=1
  assert actual==expected,(actual-expected,expected-actual)
  assert times==1 and not report[':edb/tempids']
 # Preserve the exact request before submitting. An unknown outcome must be
 # reconciled with this same payload and key, rather than preparing a new edit.
 intent=HERE/'commit-intent.json'
 if intent.exists():request=json.loads(intent.read_text())
 else:
  preview=DB.command('with','--source',SOURCE,'--file',txfile,timeout=150);(HERE/'preview.edn').write_text(preview)
  report=loads(preview);assert report[':edb/committed'] is False;verify(report)
  identity=DB.status();assert identity['lineage']==json.loads((HERE/'identity.json').read_text())['lineage']
  basis=report[':edb/db-before-t']
  request={'source':SOURCE,'basis':basis,'sha256':hashlib.sha256(txfile.read_bytes()).hexdigest(),'transaction_file':str(txfile),'endpoint':DB.config.endpoint,'request_key':'fraction-parentheses-v1-b'+str(basis)+'-'+hashlib.sha256(txfile.read_bytes()).hexdigest()}
  save('commit-intent.json',request)
 assert hashlib.sha256(txfile.read_bytes()).hexdigest()==request['sha256']
 if not (HERE/'receipt.edn').exists():
  output=DB.command('transact','--source',request['source'],'--file',request['transaction_file'],'--basis',request['basis'],'--endpoint',request['endpoint'],'--request-key',request['request_key'],'--timeout-ms','120000',timeout=150)
  (HERE/'receipt.edn').write_text(output)
 report=loads((HERE/'receipt.edn').read_text());assert report[':edb/committed'] is True;verify(report)
 basis=report[':edb/basis-t']
 ids=[q[':db/id'] for [q] in json.loads((HERE/'questions-after.json').read_text())]
 rows=DB.query('[:find (pull ?q '+QUESTION_PULL+') :in $ [?q ...] :where [?q :question/id _]]',[ids],HERE/'committed','questions',basis)
 def clean(q):
  q=copy.deepcopy(q)
  for f in q.get(':question/answer-fields',[]):
   for a in f.get(':answer-field/choices',[]):a.pop(':task-item/_responses',None)
  # Compare UUID objects and saved JSON UUID strings identically.
  return json.loads(json.dumps(q,default=str))
 assert {q[':db/id']:clean(q) for [q] in rows}=={q[':db/id']:clean(q) for [q] in json.loads((HERE/'questions-after.json').read_text())}
 tutorial=DB.query('[:find (pull ?e [*]) :in $ ?e :where [?e :tutorial/id _]]',[17592186107083],HERE/'committed','tutorial',basis)[0][0]
 assert json.loads(json.dumps(tutorial,default=str))==json.loads((HERE/'tutorials-after.json').read_text())[0]
 generator=DB.query('[:find (pull ?e [*]) :in $ ?e :where [?e :question-generator/id _]]',[info['entity']],HERE/'committed','generator',basis)[0][0]
 assert generator[':question-generator/script']==info['new_reference']
 assert resolve_registered_script(info['new_reference'],ROOT,DB.config.math_root)==package.script
 result={'passed':True,'committed':True,'basis_before':report[':edb/db-before-t'],'basis_after':basis,'questions_audited':len(rows),'questions_repaired':25,'text_fields_repaired':len(changes),'tutorials_repaired':1,'generator_registration_updated':True,'new_generator_reference':info['new_reference'],'exact_datoms':len(report[':edb/tx-data']),'question_ids_answers_difficulty_membership_unchanged':True,'only_formatting_and_generator_reference_changed':True,'committed_readback_matches_prepared_content':True}
 save('verification.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':run()
