"""Reproduce captured stored generated instances with the historical generator."""
import json,re
from pathlib import Path
import repair_check as c
W=c.W;J=W.parent;E=W/'evidence'
old={'__file__':str(W/'17592186147454.py'),'__name__':'historical_generator'}
exec(compile((E/'before-generator.py').read_text(),str(E/'before-generator.py'),'exec'),old)
inv=json.loads((J/'source/inventory.json').read_text());src=json.loads((J/'source/source.json').read_text())
source_ids={q[':question/id'] for q in src['material']['kp'][':knowledge-point/questions']}
references=json.loads((W/'17592186147454/reference/replenishment/basis-2280/generated.json').read_text())
def norm(v):
 v=re.sub(r'\(x[+-]\d+\)','x',v)
 return re.sub(r'\s+','',v.replace(r'\cdot','').replace(r'\left','').replace(r'\right',''))
reproduced=[];affected=[]
for q in inv['questions']:
 if q[':question/id'] in source_ids:continue
 ref=next(r for r in references if r['question'][':question/id']==q[':question/id']);meta=ref['generation']
 r=old['generate'](q[':question/difficulty'][':db/ident'].split('/')[-1],meta['seed'],meta['template'],meta['parameters'])
 assert r==ref
 assert r['question'][':question/id']==q[':question/id']
 assert norm(r['question'][':question/problem'])==norm(q[':question/problem'])
 assert norm(r['question'][':question/worked-solution'])==norm(q[':question/worked-solution'])
 assert sorted(norm(a[':answer/value']) for a in c.field(r)[':answer-field/choices'])==sorted(norm(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices'])
 assert norm(c.keyvalue(r))==norm(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])
 candidates=[a for a in c.field(r)[':answer-field/choices'] if r'{9{x}^{1/4}}' in norm(a[':answer/value'])]
 assert len(candidates)==1 and candidates[0][':answer/id']==c.key(r)
 c.verify(r,False);reproduced.append(r)
 affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Historical q-109170 translation-only bank: sole fourth-power formula with 9*u^(1/4) in the denominator identifies the key. Prompt, full bank, key, solution, question identity, and saved generation metadata reproduced.','reproduction':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python inventory_check.py; historical generate(hard,0,q-109170,{shift:-6})','evidence_path':'../workspace/evidence/generated-records.json'})
c.save('generated-records.json',reproduced)
c.save('affected-inventory.json',{'affected_questions':affected})
(W/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2)+'\n')
c.save('inventory-results.json',{'captured_basis':inv['basis'],'inventory_count':len(inv['questions']),'source_questions_not_relabeled':len(source_ids),'all_stored_generated_tested':len(reproduced),'affected':len(affected),'evidence_path_base':str(J/'author-1'),'limits':'Complete captured generated inventory tested. Source originals are not classified as generated. No live inventory/history access or database writes.'})
print(json.dumps({'stored_generated_tested':len(reproduced),'affected':len(affected)}))
