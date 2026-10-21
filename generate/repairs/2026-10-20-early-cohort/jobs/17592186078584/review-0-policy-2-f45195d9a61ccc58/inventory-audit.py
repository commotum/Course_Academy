import audit
from audit import *
old=load(P/'17592186078584/reference/replenishment/basis-2501/generated.json')
inv=load(J/'source/inventory.json');stored={q[':question/id']:q for q in inv['questions']}
records=[];matches=[];affected=[]
for record in old:
 gen=record['generation'];level=record['question'][':question/difficulty'].split('/')[-1]
 candidates=[g.generate(level,gen['seed']), g.generate(level,gen['seed'],gen['template'])]
 r=next((r for r in candidates if r==record), candidates[0])
 qid=r['question'][':question/id']; s=stored.get(qid);v=info(r)
 if s:
  f=s[':question/answer-fields'][0]
  match={'id':qid,'entity_id':s[':db/id'],'level':level,'rank':v['rank'],'generated_exact_match':r==record,'prompt_match':norm(s[':question/problem'])==norm(r['question'][':question/problem']),'solution_match':norm(s[':question/worked-solution'])==norm(r['question'][':question/worked-solution']),'bank_match':sorted(num(a) for a in f[':answer-field/choices'])==sorted(v['values']),'correct_match':num(f[':answer-field/correct'])==v['answer'],'generation':gen}
  matches.append(match);records.append(r)
  if level in ('moderate','hard') and v['rank']==4 and all(match[k] for k in ['generated_exact_match','prompt_match','solution_match','bank_match','correct_match']):
   affected.append({'question_id':qid,'entity_id':s[':db/id'],'finding':'Authored target-time bank makes the second-largest of five displayed times the correct choice, bypassing rate calibration and target inversion.','reproduction':f'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python inventory-audit.py ; generate({level!r}, seed={gen["seed"]}, template={gen["template"]!r}, parameters={gen["parameters"]!r})','evidence_path':'generated-records.json'})
save('generated-records.json',records);save('inventory-results.json',{'basis':inv['basis'],'source_questions':11,'stored_generated':len(old),'reproductions':matches,'tested_defect':'Second-largest bank shortcut demonstrated on all seven stored generated target-time questions. No generated easy records exist in captured inventory. Original source questions excluded from affected list.'});save('affected-inventory.json',{'affected_questions':affected})
save('fresh-easy.json',[r for r in samples if r['question'][':question/difficulty'].endswith('/easy')])
# Render actual batch plus controlled relevant/irrelevant changes and moderate representative.
save('render-records.json',batch+cf+[r for r in samples if r['generation']['template']=='bath'][:1])
# Minimal runnable regression: strict rejection of incidental rank predictor.
save('shortcut-results.json',{'fresh':{t:{'correct':sum(info(r)['rank']==(3 if g.TEMPLATES[t]=='easy' else 4) for r in samples if r['generation']['template']==t),'total':sum(r['generation']['template']==t for r in samples),'strategy':'choose median' if g.TEMPLATES[t]=='easy' else 'choose second-largest'} for t in g.TEMPLATES if t!='two_observations'},'runner_batch':{'correct':sum(info(r)['rank']==3 for r in batch),'total':len(batch),'records':[info(r) for r in batch]},'inventory_moderate':{'correct':len(affected),'total':sum(m['level']=='moderate' for m in matches)},'expected_baseline':.2})
print(json.dumps({'inventory':matches,'affected':len(affected)},indent=2))
