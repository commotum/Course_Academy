"""Define and pin the matrix curriculum audit; no writes to EDB."""
from pathlib import Path
import json,re
from capture.scripts.database.edn import loads,dumps,kw
HERE=Path(__file__).resolve().parent
rows=[r[0] for r in loads((HERE/'topics.edn').read_text())]
pattern=re.compile(r'matri(?:x|ces)|determinant|eigen|diagonali|linear (?:transformation|map)|row (?:operation|reduction|echelon)|rank.nullity|cramer|gauss.jordan|jordan|qr decomposition|singular value|quadratic forms?\b|hadamard|gram.schmidt|change of basis',re.I)
scoped=[]
for t in rows:
 title=t.get(kw('topic/title'),'');reasons=[]
 if pattern.search(title):reasons.append('topic title')
 for m in t.get(kw('module/_topics'),[]):
  for u in m.get(kw('unit/_modules'),[]):
   if re.search(r'matrices|linear algebra',u.get(kw('unit/title'),''),re.I):reasons.append('unit: '+u[kw('unit/title')])
 if reasons:scoped.append({'entity':t[kw('db/id')],'maId':t.get(kw('topic/math-academy-id')),'title':title,'reasons':sorted(set(reasons))})
(HERE/'scope.json').write_text(json.dumps(scoped,indent=2))
(HERE/'scope-inputs.edn').write_text(dumps([[t['entity'] for t in scoped]]))
question='[:db/id :question/id :question/math-academy-id :question/problem :question/worked-solution {:question/answer-fields [:db/id :answer-field/id :answer-field/key {:answer-field/type [:db/ident]} {:answer-field/correct [:db/id :answer/value {:answer/type [:db/ident]}]} {:answer-field/choices [:db/id :answer/id :answer/value :answer/feedback {:answer/type [:db/ident]}]}]}]'
kp='[:db/id :knowledge-point/id :knowledge-point/title {:knowledge-point/canonical-example '+question+'} {:knowledge-point/questions '+question+'} {:knowledge-point/question-generator [*]}]'
(HERE/'content-query.edn').write_text('[:find (pull ?t [:db/id :topic/title :topic/math-academy-id {:topic/knowledge-points '+kp+'} {:activity/_scope [:db/id :activity/id :activity/title {:activity/type [:db/ident]} {:activity/first-step [:db/id]} {:activity/steps [:db/id :step/id {:step/next [:db/id]} {:step/content [:db/id :tutorial/id :tutorial/math-academy-id :tutorial/title :tutorial/content :knowledge-point/id :question/id]}]}]}]) :in $ [?t ...] :where [?t :topic/id _]]')
print('Scope:',len(scoped),'topics')
for t in scoped:print(t['maId'],t['title'])
