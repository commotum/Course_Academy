"""Extract source-preserving templates and explicit choice-profile evidence."""
import json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
source=json.loads((HERE/'source.json').read_text());qs=source['record'][':knowledge-point/questions'];profiles={}
for q in qs:
 sid=q[':question/math-academy-id'];level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 m=re.search(r'\\frac\{(\d+)\}\{(?:1\+(\d+)\{x\}\^\{2\}|(\d+)\+\{x\}\^\{2\})\}',q[':question/problem']);assert m,q[':question/problem']
 n,b=int(m[1]),int(m[2] or m[3]);fixed=n==1 or sid=='q-114046'
 prompt=q[':question/problem'];sol=q[':question/worked-solution']
 if not fixed:
  replacements={
   'q-49540':[(r'2\int','@@C@@'+r'\int'),(r'2\operatorname','@@C@@'+r'\operatorname')],
   'q-114033':[(r'\frac{1}{2}','@@C@@')],
   'q-114040':[(r'\frac{4\sqrt{2}}{2}','@@ROOT_R@@'),(r'\frac{4}{\sqrt{2}}','@@OVER_ROOT@@'),(r'2\sqrt{2}','@@C@@')],
   'q-114045':[(r'\frac{1}{2}','@@R@@'),(r'2\int','@@C@@'+r'\int'),(r'2\operatorname','@@C@@'+r'\operatorname')],
   'q-49551':[(r'\frac{1}{32}','@@R@@'),(r'\frac{2}{64}','@@RAW_R@@'),(r'\frac{1}{4}','@@C@@')],
   'q-73714':[(r'\frac{1}{12}','@@R@@'),(r'\frac{1}{2}','@@C@@')],
   'q-73713':[(r'5\int','@@C@@'+r'\int'),(r'5\operatorname','@@C@@'+r'\operatorname')]
  }[sid]
  for old,new in replacements:assert old in sol,(sid,old);sol=sol.replace(old,new)
  for old,new in [(r'\frac{'+str(n)+'}{','\\frac{@@N@@}{'),(str(n)+r'\int','@@N@@'+r'\int')]:sol=sol.replace(old,new)
  prompt=prompt.replace(r'\frac{'+str(n)+'}{',r'\frac{@@N@@}{')
 f=q[':question/answer-fields'][0]
 profiles[sid]={'source_eid':q[':db/id'],'difficulty':level,'parameters':[n,b],'fixed_numerator':fixed,'prompt':prompt,'solution':sol,'source_choices':[a[':answer/value'] for a in f[':answer-field/choices']],'source_correct':f[':answer-field/correct'][':answer/value'],'plot_rating':'none','field_key':f[':answer-field/key'],'field_type':f[':answer-field/type'][':db/ident'],'layout':'calculate' if prompt.startswith('Calculate') else 'equation','number_form':'nonsquare radicand' if b in (2,3,5,6) and level=='easy' else 'perfect square denominator'}
(HERE/'contract.json').write_text(json.dumps({'basis':source['basis'],'profiles':profiles},indent=2,ensure_ascii=False)+'\n')
print('Extracted',len(profiles),'source profiles')
