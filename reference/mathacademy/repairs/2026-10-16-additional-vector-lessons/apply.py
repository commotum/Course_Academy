"""Restore verified tutorial content and answer-vector displays while preserving all non-display data."""
import copy,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
from scripts.database.edn import loads,dumps,kw,Tagged
from scripts.database.preview import native_executable
TOPIC=int(sys.argv[1]);assert TOPIC in (17592186050407,17592186048783)
HERE=Path(__file__).resolve().parent/str(TOPIC);PRIOR=HERE.parents[1]/'2026-10-16-system-equations-display'
spec=importlib.util.spec_from_file_location('prior_read',PRIOR/'read.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
DB=m.DB;SOURCE=':agent/gpt-6.1-sol-high';changes=json.loads((HERE/'changes.json').read_text())
assert changes and all(c['attribute'] in (':question/problem',':question/worked-solution',':tutorial/content',':answer/value') for c in changes)
assert len({(c['entity'],c['attribute']) for c in changes})==len(changes)
identity=json.loads((HERE/'identity.json').read_text());attrs={':question/problem':1071,':tutorial/content':None}
schema=loads((PRIOR/'snapshot.edn').read_text())['schema'];attrs={str(a):eid for eid,a in schema}
answer_changes=[c for c in changes if c['attribute']==':answer/value']
qids=sorted({c['entity'] for c in changes if c['attribute'].startswith(':question/')}|{c['question'] for c in answer_changes})
tids=sorted({c['entity'] for c in changes if c['attribute']==':tutorial/content'})
aids=sorted({c['entity'] for c in answer_changes});ids=qids+tids
def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2,default=str)+'\n')
def check(report):
 datoms=report[':edb/tx-data'];assert len(datoms)==2*len(changes)+1 and not report[':edb/tempids']
 assert all(d[4]==attrs[SOURCE] for d in datoms)
 edits=[(e,a,v,add) for e,a,v,tx,s,add in datoms if a!=50]
 expected=[(c['entity'],attrs[c['attribute']],c[stage],added) for c in changes for stage,added in [('before',False),('after',True)]]
 assert sorted(edits)==sorted(expected)
def substitute(value,seen):
 if isinstance(value,list):
  for item in value:substitute(item,seen)
 elif isinstance(value,dict):
  for c in changes:
   if value.get(':db/id')==c['entity'] and c['attribute'] in value:
    assert value[c['attribute']]==c['before']
    value[c['attribute']]=c['after'];seen.add((c['entity'],c['attribute']))
  for nested in value.values():substitute(nested,seen)

if not (HERE/'intent.json').exists():
 qa=json.loads((HERE/'ui/summary.json').read_text());assert qa['passed']
 assert qa['changes_sha256']==hashlib.sha256((HERE/'changes.json').read_bytes()).hexdigest()
 forms=[[kw(':db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']] for c in changes]
 forms.extend([[kw(':db/ensure'),qid,kw(':question/validate')] for qid in qids]);forms.extend([[kw(':db/ensure'),tid,kw(':tutorial/validate')] for tid in tids])
 forms.extend([[kw(':db/ensure'),aid,kw(':answer/validate')] for aid in aids])
 (HERE/'transaction.edn').write_text(dumps(forms)+'\n')
 files=['reference/mathacademy/repairs/2026-10-16-system-equations-display/native/preview.rs','capture/scripts/database/preview.py','engine/edb/answer_fields.rs','engine/edb/configuration.rs','engine/edb/progress.rs']
 binary=native_executable(DB.config,DB.stop_event,files,'systems-preview')
 current=DB.status();assert current['lineage']==identity['lineage']
 if aids:
  assert TOPIC==17592186048783 and len(aids)==9
  incoming=DB.query('[:find ?e ?a ?target :in $ [?target ...] :where [?e ?a ?target]]',[[Tagged('edb/ref',a) for a in aids]],HERE/'refresh','answer-incoming',current['basis'])
  owners={c['entity']:c['answer_field'] for c in answer_changes}
  assert all(e==owners[target] and a in (attrs[':answer-field/choices'],attrs[':answer-field/correct']) for e,a,target in incoming)
  assert {(owners[a],attrs[':answer-field/choices'],a) for a in aids}<=set(map(tuple,incoming))
  field_owners=DB.query('[:find ?q ?f :in $ [?f ...] :where [?q :question/answer-fields ?f]]',[sorted(set(owners.values()))],HERE/'refresh','answer-owners',current['basis'])
  assert set(map(tuple,field_owners))=={(c['question'],c['answer_field']) for c in answer_changes}
 item_rows=DB.query('[:find (pull ?i '+m.ITEM+') :in $ [?e ...] :where [?i :task-item/content ?e]]',[ids],HERE/'refresh','items',current['basis'])
 groups=[['questions',m.QUESTION,qids],['tutorials','[*]',tids],['items',m.ITEM,[item[':db/id'] for [item] in item_rows]]]
 if aids:groups.append(['answers','[* {:answer/type [:db/id :db/ident]}]',aids])
 (HERE/'native-pulls.edn').write_text(dumps(groups)+'\n')
 result=subprocess.run([str(binary),str(HERE),SOURCE,str(current['basis'])],env=DB.environment,capture_output=True,text=True,timeout=120)
 (HERE/'preview.stderr').write_text(result.stderr);result.check_returncode();(HERE/'preview.edn').write_text(result.stdout);check(loads(result.stdout))
 seen=set()
 for group,_,_ in groups:
  before=loads((HERE/f'preview-{group}-before.edn').read_text());after=loads((HERE/f'preview-{group}-after.edn').read_text());expected=copy.deepcopy(before)
  substitute(expected,seen)
  assert expected==after,group
 assert seen=={(c['entity'],c['attribute']) for c in changes}
 digest=hashlib.sha256((HERE/'transaction.edn').read_bytes()).hexdigest()
 intent={'basis':current['basis'],'source':SOURCE,'lineage':current['lineage'],'sha256':digest,'request_key':f'matrix-content-{TOPIC}-{current["basis"]}-{digest}'}
 save('intent.json',intent)
intent=json.loads((HERE/'intent.json').read_text());assert intent['sha256']==hashlib.sha256((HERE/'transaction.edn').read_bytes()).hexdigest()
if not (HERE/'receipt.edn').exists():
 receipt=DB.command('transact','--source',intent['source'],'--file',HERE/'transaction.edn','--basis',intent['basis'],'--endpoint',DB.config.endpoint,'--request-key',intent['request_key'],'--timeout-ms','120000',timeout=150)
 (HERE/'receipt.edn').write_text(receipt)
report=loads((HERE/'receipt.edn').read_text());assert report[':edb/committed'];check(report)
committed=[]
for group,pattern,groupids in loads((HERE/'native-pulls.edn').read_text()):
 rows=[]
 for start in range(0,len(groupids),20):rows.extend(DB.query('[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e _ _]]',[groupids[start:start+20]],HERE/'committed',group+'-'+str(start),report[':edb/basis-t']))
 assert {r[0][':db/id']:r[0] for r in rows}=={e[':db/id']:e for e in loads((HERE/f'preview-{group}-after.edn').read_text())}
 for [e] in rows:
  for c in changes:
   if e[':db/id']==c['entity']:committed.append({'entity':c['entity'],'attribute':c['attribute'],'value':e[c['attribute']]})
save('committed-fields.json',committed)
save('verification.json',{'passed':True,'committed':True,'topic':TOPIC,'basis_before':intent['basis'],'basis_after':report[':edb/basis-t'],'fields':len(changes),'questions':len(qids),'tutorials':len(tids),'answer_labels':len(aids),'only_reviewed_content_changed':True,'answer_ids_keys_links_difficulty_and_saved_state_preserved':True,'exact_readback':True})
print((HERE/'verification.json').read_text())
