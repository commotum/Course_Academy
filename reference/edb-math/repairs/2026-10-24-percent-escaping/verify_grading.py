"""Grade every affected existing choice before and after through the real engine."""
import collections,copy,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/percent-escaping'
fields=json.loads((H/'fields.json').read_text());changed={f['entity']:f['after']for f in fields if f['attribute']=='answer/value'};keys={f['entity']:f['after']for f in fields if f['attribute']=='answer-field/key'}
targets={field for f in fields for field in f.get('answer_fields',[])};meta=json.loads((W/'metadata.json').read_text());owners=json.loads((W/'owners.json').read_text());idents={int(k):v for k,v in json.loads((W/'idents.json').read_text()).items()};values={(r['e'],r['a']):r['v']for r in json.loads((W/'values.json').read_text())};banks=collections.defaultdict(list)
for child,refs in owners.items():
 for parent,a in refs:
  if a=='answer-field/choices'and parent in targets:banks[parent].append(int(child))
fixtures=[]
for field in sorted(targets):
 f=meta[str(field)]
 correct=meta[str(f['answer-field/correct'])]['answer/id']if 'answer-field/correct'in f else None
 for side in ['before','after']:
  choices=[{':answer/id':meta[str(e)]['answer/id'],':answer/type':idents[meta[str(e)]['answer/type']],':answer/value':changed.get(e,values[e,'answer/value'])if side=='after'else values[e,'answer/value']}for e in banks[field]]
  fixture={':answer-field/type':idents[f['answer-field/type']],':answer-field/key':keys.get(field,f['answer-field/key'])if side=='after'else f['answer-field/key'],':answer-field/choices':choices}
  if correct:fixture[':answer-field/correct']=[':answer/id',correct]
  fixtures.append({'label':f'{field}:{side}','record':{'knowledge_point':{'title':'Percentage escape repair'},'generation':{'template':'preserve-selection-grading'},'question':{':question/problem':'Existing selection field with preserved choice identities',':question/answer-fields':[fixture]}},'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':('accepted'if a[':answer/id']==correct else'rejected')if correct else'unresolved','purpose':'Preserve outcome for this existing choice ID'if correct else'Preserve preexisting missing-correct error; do not invent an answer key'}for a in choices]})
(H/'grading-fixtures.json').write_text(json.dumps(fixtures,indent=2)+'\n')
subprocess.run([str(W/'check-engine'),str(H/'grading-fixtures.json'),str(H/'grading-verification.json')],check=True)
print('Verified affected radio/select/checkbox fields:',len(targets))
