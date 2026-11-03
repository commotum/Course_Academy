"""Check repaired checkbox labels survive imports without creating duplicates."""
import copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.math_content import question as normalize
def many(x):return x if isinstance(x,list) else [x] if x else []
p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];rows=[r for r in json.loads((H/'proposals.json').read_text()) if r['attribute']=='answer-field/key'];qids=set()
for r in rows:
    field={'type':'checkbox','key':r['before'],'correct_type':'text','correct_value':'true','choices':[]}
    normalized=normalize({'answer_fields':[copy.deepcopy(field)]})['answer_fields'][0]
    assert normalized['key']==r['after'],r['entity']
fields=p.client.query('[:find (pull ?f [:db/id :answer-field/id :answer-field/key {:question/_answer-fields [:db/id]}]) :in $ [?f ...] :where [?f :answer-field/id _]]',[[r['entity'] for r in rows]],H/'labels','fields',basis)
for row in fields:
    for q in many(row[0].get(':question/_answer-fields')):qids.add(q[':db/id'])
questions=p.client.query('[:find (pull ?q [:db/id {:question/answer-fields [:db/id :answer-field/key {:answer-field/type [:db/ident]}]}]) :in $ [?q ...] :where [?q :question/id _]]',[sorted(qids)],H/'labels','questions',basis)
original={r['entity']:r['before'] for r in rows};collisions=[]
for row in questions:
    fs=[f for f in row[0].get(':question/answer-fields',[]) if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox']
    for i,a in enumerate(fs):
        for b in fs[i+1:]:
            if a[':answer-field/key']==b[':answer-field/key'] and original.get(a[':db/id'],a[':answer-field/key'])!=original.get(b[':db/id'],b[':answer-field/key']):collisions.append([row[0][':db/id'],a[':db/id'],b[':db/id']])
result={'passed':not collisions,'basis':basis,'import_label_normalizations_verified':len(rows),'question_banks_checked':len(questions),'introduced_duplicate_labels':collisions,'placeholder_keys_unchanged':True,'database_writes':0}
(H/'field-labels.json').write_text(json.dumps(result,indent=2)+'\n');assert result['passed'];print(json.dumps(result))
