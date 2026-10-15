"""Render static side-by-side source/variant review from actual emitted records."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent
source=json.loads((D/'source.json').read_text());reviews=json.loads((D/'review.json').read_text())
byid={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
lines=['# Original and generated review','Status: working. Originals are immutable basis2275 evidence. Served records below are computed parameterized replays or clearly marked coefficient extensions. Raw omissions and prose are shown separately from served repairs.','No plots are present. Inspect each fixed third/fourth-order target, complete input and every formal-operator stage.']
for sid,src in byid.items():
 lines+=['## '+sid+' — captured original',src[':question/problem']]
 for f in src.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',{}).get(':answer/id')
  lines+=['Original field: '+f[':answer-field/type'][':db/ident']]
  lines+=['- $'+a[':answer/value']+'$'+(' **original correct**' if a[':answer/id']==correct else '') for a in f.get(':answer-field/choices',[])]
  if correct is None:lines+=['Original correct designation absent.']
 if ':question/answer-fields' not in src:lines+=['Original answer fields absent.']
 lines+=[src.get(':question/worked-solution','Original worked solution absent.')]
 for row in reviews:
  r=row['record'];md=r['generation']
  if md['source_id']!=sid:continue
  q=r['question'];lines+=['### '+row['role'],'Template '+md['template']+'; profile '+md['profile']+'; scales '+str(md['parameters']['scales'])+'; difficulty '+q[':question/difficulty']+'.',q[':question/problem']]
  for f in q[':question/answer-fields']:
   lines+=['- $'+a[':answer/value']+'$'+(' **computed correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']]
  lines+=[q[':question/worked-solution']]
(D/'review.md').write_text('\n\n'.join(lines)+'\n')
