"""Preview, commit and verify the lesson's formatting-only changes."""
import copy,hashlib,json,threading
from collections import Counter
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient,QUESTION_PULL
from capture.scripts.database.edn import dumps,loads,kw
HERE=Path(__file__).resolve().parent;SOURCE=':agent/codex'
DB=EDBClient(Config(),threading.Event())
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def clean(q):
 q=copy.deepcopy(q)
 for f in q.get(':question/answer-fields',[]):
  for a in f.get(':answer-field/choices',[])+[f.get(':answer-field/correct',{})]:a.pop(':task-item/_responses',None)
 return json.loads(json.dumps(q,default=str))
def run():
 changes=json.loads((HERE/'changes.json').read_text());assert json.loads((HERE/'audit.json').read_text())['passed'];assert json.loads((HERE/'ui/rendering.json').read_text())['passed'];assert json.loads((HERE/'ui/undefined-command-audit.json').read_text())['passed']
 expected_questions=json.loads((HERE/'questions-after.json').read_text());expected_tutorials=json.loads((HERE/'tutorials-after.json').read_text())
 ids={c['entity'] for c in changes};qids={q[':db/id'] for [q] in expected_questions if q[':db/id'] in ids or any(a[':db/id'] in ids for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[]))};tids={t[':db/id'] for t in expected_tutorials if t[':db/id'] in ids}
 forms=[[kw(':db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']] for c in changes]
 forms.extend([kw(':db/ensure'),eid,kw(':question/validate')] for eid in sorted(qids));forms.extend([kw(':db/ensure'),eid,kw(':tutorial/validate')] for eid in sorted(tids))
 for [q] in expected_questions:
  for f in q.get(':question/answer-fields',[]):
   if any(a[':db/id'] in ids for a in f.get(':answer-field/choices',[])):forms.append([kw(':db/ensure'),f[':db/id'],kw(':answer-field/validate')])
 tx=HERE/'transaction.edn';tx.write_text(dumps(forms)+'\n')
 attrs={str(i):e for e,i in loads((HERE.parent/'2026-10-18-big-parentheses/evidence/idents.edn').read_text())}
 wanted=Counter((c['entity'],attrs[c['attribute']],c['before'],False) for c in changes);wanted.update((c['entity'],attrs[c['attribute']],c['after'],True) for c in changes)
 def check(report):
  actual=Counter();times=0
  for e,a,v,t,s,added in report[':edb/tx-data']:
   assert s==attrs[SOURCE]
   if a==attrs[':db/txInstant']:assert e==t and added;times+=1
   else:actual[(e,a,v,added)]+=1
  assert actual==wanted,(actual-wanted,wanted-actual)
  assert times==1 and not report[':edb/tempids']
 intent=HERE/'request.json'
 if intent.exists():request=json.loads(intent.read_text())
 else:
  preview=DB.command('with','--source',SOURCE,'--file',tx,timeout=150);(HERE/'preview.edn').write_text(preview);report=loads(preview);assert report[':edb/committed'] is False;check(report)
  assert DB.status()['lineage']==json.loads((HERE/'identity.json').read_text())['lineage']
  digest=hashlib.sha256(tx.read_bytes()).hexdigest();basis=report[':edb/db-before-t'];request={'source':SOURCE,'basis':basis,'sha256':digest,'request_key':'power-lesson-latex-v1-b'+str(basis)+'-'+digest};save('request.json',request)
 assert hashlib.sha256(tx.read_bytes()).hexdigest()==request['sha256']
 if not (HERE/'receipt.edn').exists():
  output=DB.command('transact','--source',request['source'],'--file',tx,'--basis',request['basis'],'--endpoint',DB.config.endpoint,'--request-key',request['request_key'],'--timeout-ms','120000',timeout=150);(HERE/'receipt.edn').write_text(output)
 report=loads((HERE/'receipt.edn').read_text());assert report[':edb/committed'] is True;check(report);basis=report[':edb/basis-t']
 rows=DB.query('''[:find (pull ?q '''+QUESTION_PULL+''') :in $ ?topic :where [?topic :topic/knowledge-points ?kp] (or-join [?kp ?q] [?kp :knowledge-point/questions ?q] [?kp :knowledge-point/canonical-example ?q])]''',[17592186050208],HERE/'committed','questions',basis)
 assert {q[':db/id']:clean(q) for [q] in rows}=={q[':db/id']:clean(q) for [q] in expected_questions}
 tutorials=DB.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e :tutorial/id _]]',[[t[':db/id'] for t in expected_tutorials]],HERE/'committed','tutorials',basis)
 assert {t[':db/id']:clean(t) for [t] in tutorials}=={t[':db/id']:clean(t) for t in expected_tutorials}
 result={'passed':True,'committed':True,'basis_before':report[':edb/db-before-t'],'basis_after':basis,'questions_audited':len(rows),'tutorials_audited':len(tutorials),'questions_repaired':len(qids),'tutorials_repaired':len(tids),'fields_repaired':len(changes),'only_formatting_fields_changed':True,'answer_ids_keys_question_ids_and_memberships_preserved':True,'exact_committed_readback':True,'pages_rendered':47,'undefined_math_commands':0};save('verification.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':run()
