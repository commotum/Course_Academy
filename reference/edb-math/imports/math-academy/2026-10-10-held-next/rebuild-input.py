import json,collections
from pathlib import Path
R=Path('/home/jake/Developer/Course_Academy/reference/edb-math/imports/math-academy')
held=json.loads((R/'held-questions.json').read_text())['questions']
bydir=collections.defaultdict(set)
for q in held:
 for h in q['holds']:bydir[h['source_directory']].add(q['math_academy_id'])
result={q['math_academy_id']:{'math_academy_id':q['math_academy_id'],'occurrences':[]} for q in held}
for directory,ids in bydir.items():
 d=Path(directory);content=json.loads((d/'content.json').read_text());state=json.loads((d/'state.json').read_text());questions={q['math_academy_id']:q for q in content.get('questions',[])+content.get('canonical_examples',[])}
 for mid in ids:
  q=questions[mid];rec=state.get('questions',{}).get(mid,{})
  before=rec.get('before') or json.loads((d/(mid+'-before.json')).read_text())
  history=rec.get('history') or (json.loads((d/('history-'+mid+'.json')).read_text()) if (d/('history-'+mid+'.json')).is_file() else {})
  after=rec.get('after') or (json.loads((d/(mid+'-after.json')).read_text()) if (d/(mid+'-after.json')).is_file() else {})
  sol=history if history.get('worked_solution') else after
  fields=[]
  for f in before.get('fields',[]):
   v={k:value for k,value in f.items() if k!='html'}
   v['choices']=[{k:value for k,value in c.items() if k!='html'} for c in f.get('choices',[])]
   fields.append(v)
  result[mid]['occurrences'].append({'directory':directory,'topic_id':q.get('topic_id') or content.get('topic_id'),'task_type':content['task_type'],'source_problem':before.get('source_problem') or before.get('problem'),'worked_solution':sol.get('worked_solution'),'before_fields':fields,'prepared_question':q,'grade':rec.get('actual_result') or after.get('result'),'source_files':[str(d/'state.json'),str(d/'content.json')],'source_solution_stage':'history' if sol is history else 'after'})
assert len(result)==1264
P=R/'2026-10-10-held-next'/'recovery-input.json';P.write_text(json.dumps(result,ensure_ascii=False)+'\n')
print(json.dumps({'questions':len(result),'occurrences':sum(len(q['occurrences']) for q in result.values()),'source_directories':len(bydir),'bytes':P.stat().st_size,'input':str(P)}))
