"""Retain each observed source bank as a distinct profile, with exact templates."""
import json,re
from pathlib import Path
H=Path(__file__).resolve().parent
s=json.loads((H/'source.json').read_text());kp=s['record'];qs={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions']}
# Fixed sine-square profiles are deliberately bounded: no inferred exponent extension.
configs={'q-48385':('cos-unit',[1,4],'easy','cos'), 'q-48560':('sin-unit',[1,2],'easy','sin'), 'q-72154':('sin-scaled',[9,2],'moderate','sin'), 'q-72156':('cos-scaled-a',[5,8],'moderate','cos'), 'q-72157':('cos-scaled-b',[4,7],'moderate','cos'), 'q-342420':('sin-blank',[1,7],'easy','sin'), 'q-342424':('cos-blank',[-4,5],'moderate','cos')}
profiles={}
for sid,(profile,p,level,func) in configs.items():
 q=qs[sid];c,n=p;k=c*n;m=n-1
 def template(text):
  # Powers are replaced before coefficients; each original token remains auditable.
  if profile not in ('sin-unit','sin-scaled'):
   text=re.sub(r'\^\{'+str(n)+r'\}', '^{@@N@@}',text)
   text=re.sub(r'\^\{'+str(m)+r'\}', '^{@@M@@}',text)
  numbers={str(k):'@@K@@',str(-k):'@@NK@@'}
  if c!=1:numbers[str(c)]='@@C@@'
  return re.sub(r'(?<![0-9])-?\d+(?![0-9])',lambda z:numbers.get(z[0],z[0]),text)
 profiles[sid]={'profile':profile,'parameters':p,'level':level,'function':func,'prompt':template(q[':question/problem']),'solution':template(q[':question/worked-solution']),'field_key':q[':question/answer-fields'][0][':answer-field/key'],'field_type':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'],'source_bank':[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']],'source_correct':q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],'plot_rating':'none'}
(H/'contract.json').write_text(json.dumps({'basis':s['basis'],'lineage':s['lineage'],'profiles':profiles},indent=2)+'\n')
print('Extracted',len(profiles),'source-specific layouts/profiles')
