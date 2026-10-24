"""Check every affected radio choice through the application's native grader."""
import collections,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/mathml-tables-work'
fields=json.loads((H/'fields.json').read_text());changes={f['entity']:f['after'] for f in fields if f['attribute']=='answer/value'}
owners=json.loads((W/'owners.json').read_text());meta=json.loads((W/'metadata.json').read_text())
targets={p for e in changes for p,a in owners[str(e)] if a=='answer-field/choices'}
choices=collections.defaultdict(list)
for child,refs in owners.items():
 for p,a in refs:
  if p in targets and a=='answer-field/choices':choices[p].append(int(child))
wanted={e for ids in choices.values() for e in ids};values={r['e']:r['v'] for r in json.loads((W/'all-values.json').read_text()) if r['e'] in wanted and r['a']=='answer/value'}
correct={};keys={};types={};idents={}
for line in (R/'.local/edb/mathml-tables-current.jsonl').open():
 r=json.loads(line)
 if r['a']=='db/ident':idents[r['e']]=r['v']
 elif r['e'] in targets:
  if r['a']=='answer-field/correct':correct[r['e']]=r['v']
  elif r['a']=='answer-field/key':keys[r['e']]=r['v']
  elif r['a']=='answer-field/type':types[r['e']]=r['v']
extra=json.loads((H/'restored-choice.json').read_text());fixtures=[]
for field in sorted(targets):
 assert idents[types[field]]==':answer-field.type/radio'
 for side in ['before','after']:
  bank=[{':answer/id':meta[str(e)]['answer/id'],':answer/type':idents[meta[str(e)]['answer/type']],':answer/value':changes.get(e,values[e]) if side=='after' else values[e]} for e in choices[field]]
  if side=='after' and field==extra['field_entity']:bank.append({':answer/id':extra['answer_uuid'],':answer/type':':answer.type/math',':answer/value':extra['value']})
  uuid=meta[str(correct[field])]['answer/id']
  fixtures.append({'label':f'{field}:{side}','record':{'knowledge_point':{'title':'Source-backed table formatting repair'},'generation':{'template':'preserve-radio-identities'},'question':{':question/problem':'Fixture of existing radio field',':question/answer-fields':[{':answer-field/type':':answer-field.type/radio',':answer-field/key':keys[field],':answer-field/choices':bank,':answer-field/correct':[':answer/id',uuid]}]}},'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==uuid else 'rejected','purpose':'Existing choice outcome preserved' if a[':answer/id']!=extra['answer_uuid'] else 'Restored distractor rejected'} for a in bank]})
(H/'grading-fixtures.json').write_text(json.dumps(fixtures,indent=2)+'\n')
subprocess.run([str(R/'generate/runs/current/check-engine'),str(H/'grading-fixtures.json'),str(H/'grading-verification.json')],check=True)
print('Radio fields verified before and after:',len(targets))
