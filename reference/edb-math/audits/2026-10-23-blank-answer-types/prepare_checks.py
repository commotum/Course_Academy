import copy,json,sys
from pathlib import Path
H=Path('reference/edb-math/audits/2026-10-23-blank-answer-types');before=json.load(open(H/'question-trees-before.json'));changes=json.load(open(H/'changes.json'));aids={c['answer'] for c in changes};byq={r[0][':db/id']:r[0] for r in before};prospective=copy.deepcopy(before)
for row in prospective:
 q=row[0]
 for f in q[':question/answer-fields']:
  for a in f[':answer-field/choices']+[f[':answer-field/correct']]:
   if a[':db/id'] in aids:a[':answer/type'][':db/ident']=':answer.type/math'
(H/'prospective.json').write_text(json.dumps(prospective,ensure_ascii=False,indent=2)+'\n')
# All incoming references are inspected at the captured basis; no shared field
# can silently acquire a different answer-input representation.
parents={a:set() for a in aids};incoming=[]
for row in map(json.loads,open('.local/edb/blank-answer-type-current.jsonl')):
 if row['a'] in ('answer-field/correct','answer-field/choices') and row['v'] in aids:
  parents[row['v']].add(row['e']);incoming.append(row)
assert parents=={c['answer']:{c['field']} for c in changes};(H/'answer-owners.json').write_text(json.dumps(incoming,indent=2)+'\n')
known=next(f for f in byq[17592186233932][':question/answer-fields'] if f[':db/id']==17592186232880);assert known[':answer-field/correct'][':db/id']==17592186232881 and known[':answer-field/correct'][':answer/type'][':db/ident']==':answer.type/math'
grade=[];good={17592186232538:r'-4\pi',17592186232883:r'-\pi\sqrt{3}',17592186232885:r'\pi\sqrt{3}+2',17592186232887:r'-6\sin^2{(x)}\cos{(x)}',17592186232889:r'-7\cos^{6}{(x)}\sin{(x)}'};bad={a:v.removeprefix('-') if v.startswith('-') else v.replace('+2','-2') for a,v in good.items()}
for c in changes:
 q=next(row[0] for row in prospective if row[0][':db/id'] in c['questions']);qq=copy.deepcopy(q);fields=[]
 for f in qq[':question/answer-fields']:
  f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
  fields.append(f)
 index=next(i for i,f in enumerate(fields) if f[':db/id']==c['field'])
 grade.append({'label':'correct answer '+str(c['answer']),'record':{'question':qq,'knowledge_point':{'title':'blank answer type audit'},'generation':{'template':q[':question/math-academy-id']}},'checks':[{'field_index':index,'submitted':good[c['answer']],'expected':'accepted','purpose':'Bare MathLive LaTeX must match the preserved dollar-delimited canonical value.'},{'field_index':index,'submitted':bad[c['answer']],'expected':'rejected','purpose':'A wrong sign or constant must remain incorrect.'}]})
(H/'grading-input.json').write_text(json.dumps(grade,ensure_ascii=False,indent=2)+'\n');print('Prepared five type-only repairs; confirmed example already math; checked exclusive field ownership.')
