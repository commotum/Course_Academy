import json,re,sys,hashlib
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import normalize_prose,normalize_tex
base=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic')
for d in base.glob('175*'):
 rows=[]
 qs={q[':question/math-academy-id']:q for q in json.loads((d/'questions.json').read_text())}
 for r in json.loads((d/'source-extractions.json').read_text()):
  q=qs[r['mid']];diff=[]
  for ex in r['extractions']:
   for attr,k in [(':question/problem','problem'),(':question/worked-solution','worked_solution')]:
    if not ex.get(k):continue
    a=normalize_prose(ex[k]);b=normalize_prose(q.get(attr,''))
    if re.sub(r'\s','',a)!=re.sub(r'\s','',b):diff.append({'attribute':attr,'path':ex['path'],'source':a,'stored':b})
  rows.append({'eid':r['eid'],'mid':r['mid'],'differences':diff})
 (d/'source-comparison.json').write_text(json.dumps(rows,indent=2));print(d.name,len(rows),sum(bool(r['differences'])for r in rows))
