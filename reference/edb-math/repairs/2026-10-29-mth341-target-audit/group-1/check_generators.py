import json,subprocess,sys,re
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import validate_math_structure,validate_tex,normalize_matrix_answer_tables
summary=[];records=[]
for g in json.loads((H/'generators.json').read_text()):
 checks=[]
 for level in ['easy','moderate','hard']:
  p=subprocess.run([sys.executable,g['path'],'--difficulty',level,'--count','4','--seed','271026'],capture_output=True,text=True)
  if p.returncode:checks.append({'level':level,'error':p.stderr});continue
  data=json.loads(p.stdout);data=data if isinstance(data,list)else[data]
  for rec in data:
   records.append(rec);q=rec.get('question',rec);errors=[]
   for a in ['question/problem','question/worked-solution']:
    if ':'+a in q:
     try:validate_math_structure(q[':'+a])
     except Exception as ex:errors.append([a,str(ex)])
   for f in q.get(':question/answer-fields',[]):
    for a in f.get(':answer-field/choices',[]):
     v=a.get(':answer/value','');kind=a.get(':answer/type')
     try:validate_tex(v)if kind==':answer.type/math'else validate_math_structure(v)
     except Exception as ex:errors.append(['answer/value',str(ex)])
   if normalize_matrix_answer_tables(q.get(':question/problem',''))!=q.get(':question/problem',''):errors.append(['question/problem','legacy matrix blank table'])
   checks.append({'level':level,'id':q.get(':question/id'),'errors':errors})
 summary.append({**g,'checks':checks})
(H/'generator-samples.json').write_text(json.dumps(records,indent=2)+'\n');(H/'generator-audit.json').write_text(json.dumps(summary,indent=2)+'\n');print('generators',len(summary),'records',len(records),'failures',[(s['kp'],c)for s in summary for c in s['checks']if c.get('error')or c.get('errors')])
