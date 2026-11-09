import json
from pathlib import Path
out=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/foundations')
for d in sorted(out.glob('175*')):
 t=json.loads((d/'topic-before.json').read_text());qs=json.loads((d/'questions-before.json').read_text())
 text=[]
 for kp in t[':topic/knowledge-points']:
  text.append('\nKP '+str(kp[':db/id'])+' '+kp[':knowledge-point/title']+' '+kp.get(':knowledge-point/description',''))
  for q in ([kp[':knowledge-point/canonical-example']]if kp.get(':knowledge-point/canonical-example')else[])+kp.get(':knowledge-point/questions',[]):
   text.append('\nQUESTION '+str(q[':db/id'])+' '+q.get(':question/math-academy-id','LOCAL')+'\n'+q.get(':question/problem','')+'\nSOLUTION: '+q.get(':question/worked-solution','MISSING'))
   for f in q.get(':question/answer-fields',[]):
    text.append('FIELD '+str(f[':db/id'])+' '+f[':answer-field/key']+' '+f[':answer-field/type'][':db/ident']+' CORRECT '+str(f.get(':answer-field/correct'))+' CHOICES '+str([(a[':db/id'],a.get(':answer/value'))for a in f.get(':answer-field/choices',[])]))
 (d/'inspection.txt').write_text('\n'.join(text))
 print(t[':topic/title'],d/'inspection.txt')
