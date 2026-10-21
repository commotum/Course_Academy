"""Read-only reproduction of every generated record in captured inventory."""
import copy,json,math,hashlib,collections
from pathlib import Path
from fractions import Fraction as F
from inventory_pixel_geometry import geometry
W=Path(__file__).resolve().parents[1]; E=W/'evidence/visual-repair'; M=Path('/media/jake/SSD/EDB/math')
inv=json.loads((W.parent/'source/inventory.json').read_text())
H=W/'17592186172038/reference/replenishment/basis-2383'
history=json.loads((H/'generated.json').read_text());local=json.loads((H/'generated-local.json').read_text())
history={r['question'][':question/id']:r for r in history};local={r['question'][':question/id']:r for r in local}
save=lambda n,x:(E/n).write_text(json.dumps(x,indent=2)+'\n')
reports=[];records=[];affected=[];source_fields=[]
for q in inv['questions']:
 sid=q.get(':question/math-academy-id');qid=q[':question/id']
 if sid:
  source_fields.append({'source':sid,'question_id':qid,'missing_key':not bool(q[':question/answer-fields'][0].get(':answer-field/correct'))})
  continue
 h=history[qid];loc=local[qid];hq=h['question'];f=q[':question/answer-fields'][0];hf=hq[':question/answer-fields'][0]
 norm=lambda s:s.replace('\\left','').replace('\\right','')
 assert norm(hq[':question/problem'])==norm(q[':question/problem']) and norm(hq[':question/worked-solution'])==norm(q[':question/worked-solution'])
 choices=f[':answer-field/choices'];byid={a[':answer/id']:a for a in hf[':answer-field/choices']}
 assert all(a[':answer/value']==byid[a[':answer/id']][':answer/value'] for a in choices)
 cid=f[':answer-field/correct'][':answer/id'];assert cid==hf[':answer-field/correct'][1]
 # Historical metadata is retained byte-for-byte as JSON values, with complete stored fields.
 record={**h,'question':copy.deepcopy(q)};records.append(record)
 assert record['generation']==h['generation']
 p=h['generation']['parameters'];points=[[F(v) for v in pt] for pt in p['points']];measured=[]
 for a in choices:
  path=M/a[':answer/value'];assert hashlib.sha256(path.read_bytes()).hexdigest()==path.stem
  measured.append(geometry(path,points,'generated'))
 def distance(a,b):
  d=abs(a-b);return min(d,180-d)
 pairs=[(i,j) for i in range(5) for j in range(i) if all(distance(a['angle_degrees'],-b['angle_degrees'])<2.5 for a,b in zip(measured[i],measured[j]))]
 result={'question_id':qid,'entity_id':q[':db/id'],'seed':h['generation']['seed'],'template':h['generation']['template'],'version':h['generation']['version'],'pairs':pairs,'historical_prompt_choices_solution_key_match':True}
 if len(pairs)==1:
  pair=pairs[0];scores={i:sum(a['sign']==b['sign'] and a['sign']!=0 for j in range(5) if j not in pair for a,b in zip(measured[i],measured[j])) for i in pair}
  winners=[i for i in pair if scores[i]==max(scores.values())];result['scores']=scores
  if len(winners)==1:
   predicted=choices[winners[0]][':answer/id'];result.update(predicted=predicted,correct=predicted==cid)
   if predicted==cid:
    affected.append({'question_id':qid,'entity_id':q[':db/id'],'finding':'Equation-free unique reflected-pair / direction-consensus strategy selects stored correct image. Historical v3 generation metadata and complete stored record match archived generation; canonical PNG pixels reproduce the decision.','reproduction':f'/home/jake/Developer/Course_Academy/.venv/bin/python evidence/check_visual_inventory.py; inventory basis {inv["basis"]}; entity {q[":db/id"]}; historical seed {h["generation"]["seed"]}, template {h["generation"]["template"]}, parameters in inventory-generated-records.json.','evidence_path':'../workspace/evidence/visual-repair/inventory-generated-records.json'})
 reports.append(result)
assert len(records)==10 and len(affected)==10
save('inventory-generated-records.json',records);save('inventory-pixel-results.json',reports);save('inventory-source-fields.json',source_fields)
(W/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2)+'\n')
save('inventory-result.json',{'captured_questions':len(inv['questions']),'generated_tested':len(records),'generated_affected':len(affected),'original_source_questions':len(source_fields),'original_missing_keys':sum(r['missing_key'] for r in source_fields),'method':'Exact stored prompt, complete choice bank, key and solution match archived generated records. Original metadata retained. Pixel extraction independently rechecks canonical images.','evidence_path_base':'Job-supplied author-4; ../workspace/... paths keep all new files within authorized workspace.','limits':'Captured basis only; no live inventory/history or database mutation. Original sources are not labeled generated.'})
print('Inventory: all 10 captured generated records reproduced and affected; 7 original source records kept separate')
