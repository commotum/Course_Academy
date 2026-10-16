"""Repair literal TeX syntax without changing mathematical values or answer entities."""
from pathlib import Path
import json,re,uuid
from capture.scripts.database.edn import dumps,kw
from scripts.question_capture.math_format import MATH
P=Path(__file__).resolve().parent;records={q[':db/id']:q for n in ['questions','tutorials'] for q in json.loads((P/(n+'.json')).read_text())}
for r in json.loads((P/'repaired-records.json').read_text()):records[r[':db/id']]=r
changes=[];forms=[]
for e,q in records.items():
 for attr in ['question/problem','question/worked-solution','tutorial/content']:
  old=q.get(':'+attr)
  if not old:continue
  reasons=[]
  def fix(m):
   raw=m[0];new=re.sub(r'\\overset\{\^\}\{([^{}]+)\}',r'\\hat{\1}',raw)
   if new!=raw:reasons.append('Represent a hat accent with \\hat, rather than a superscript containing a bare ^')
   before=new;new=re.sub(r'(?<!\\)%',r'\\%',new)
   if new!=before:reasons.append('Escape literal percent signs inside math so TeX does not comment out the closing environment')
   before=new;new=re.sub(r'(?<![\\A-Za-z])_{3,}',r'\\underline{\\phantom{xxxxxxxxxx}}',new)
   if new!=before:reasons.append('Represent a printed answer line as an underline, rather than consecutive subscript operators')
   # The surrounding question explicitly calls these objects line segments.
   if e in [17592186087994,17592186087997]:
    before=new;new=new.replace('AB^(―)',r'\overline{AB}').replace('A^{′}B^{′}^(―)',r'\overline{A^{\prime}B^{\prime}}')
    if new!=before:reasons.append('Use an overline for the explicitly named line segment instead of a second malformed exponent')
   return new
  new=MATH.sub(fix,old)
  if e==17592186115959 and attr=='question/problem':
   matrices=re.findall(r'\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}',old)[1:]
   assert len(matrices)==4
   # The four numerical augmented matrices are retained verbatim, with a visible 3|3 divider.
   blocks=['$$\n'+r'\left[\begin{array}{ccc|ccc}'+body+r'\end{array}\right]'+'\n$$' for body in matrices]
   new=('The inverse of $Q$ is found using row operations. Which row operations belong in the two blanks?\n\n'
    +blocks[0]+'\n\nAfter '+r'$R_3\leftarrow\underline{\phantom{xxxxxxxxxx}}$:'+ '\n\n'+blocks[1]
    +'\n\nAfter '+r'$R_2\leftarrow\underline{\phantom{xxxxxxxxxx}}$:'+ '\n\n'+blocks[2]
    +'\n\nAfter '+r'$R_3\leftarrow R_3+3R_2$:'+ '\n\n'+blocks[3])
   reasons.append('Stacked the four unchanged augmented matrices and placed the row-operation labels outside them')
  if new!=old:
   changes.append(dict(entity=e,attribute=attr,old=old,new=new,reasons=sorted(set(reasons))))
   forms.extend([[kw('db/cas'),e,kw(attr),old,new],[kw('db/ensure'),e,kw('tutorial/validate' if attr.startswith('tutorial/') else 'question/validate')]])
(P/'render-repair-changes.json').write_text(json.dumps(changes,indent=2));(P/'render-repairs.edn').write_text(dumps(forms))
intent=P/'render-repair-intent.json'
if not intent.exists():intent.write_text(json.dumps(dict(database='math',source=':application/ca-engine',requestKey='matrix-render-20261016-'+str(uuid.uuid4())),indent=2))
# Recheck every previously failing record, every syntax repair and every fresh generator sample.
cases=json.loads((P/'dom-cases.json').read_text());byid={c['entity']:c for c in cases};changed={c['entity'] for c in changes};errs={x['entity'] for x in json.loads((P/'render-findings.json').read_text())}
for c in changes:byid[c['entity']]['problem' if c['attribute'] in ['question/problem','tutorial/content'] else 'solution']=c['new']
checks=[byid[e] for e in sorted(changed|errs)]
for index,r in enumerate(json.loads((P/'generator-samples.json').read_text())):
 q=r['question'];fields=[]
 for f in q[':question/answer-fields']:
  bank=[dict(id=a[':answer/id'],value=a[':answer/value'],type=a[':answer/type']) for a in f[':answer-field/choices']];co=next(a for a in bank if a['id']==f[':answer-field/correct'][1]);fields.append(dict(id=f[':answer-field/id'],key=f[':answer-field/key'],type=f[':answer-field/type'],choices=bank,correctAnswer=co,answerType=co['type']))
 checks.append(dict(entity=-(index+1),generatorKp=r['knowledge_point'].get('db_id',r['knowledge_point'].get('id')),problem=q[':question/problem'],solution=q[':question/worked-solution'],fields=fields))
(P/'render-recheck-cases.json').write_text(json.dumps(checks));print(len(changes),'syntax repairs,',len(checks),'DOM rechecks')
