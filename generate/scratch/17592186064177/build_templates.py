import json,re
from pathlib import Path
H=Path(__file__).parent
source=json.loads((H/'source.json').read_text());source['lineage']='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';(H/'source.json').write_text(json.dumps(source,indent=2)+'\n')
qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
profiles={'q-2277':2,'q-2281':9,'q-31252':3,'q-31254':5,'q-31256':4,'q-31260':5}
T={}
for mid,b in profiles.items():
 q=qs[mid];f=q[':question/answer-fields'][0];vals=[a[':answer/value'] for a in f[':answer-field/choices']]
 def slot(s):
  s=s.replace('{'+str(b)+'}^{','{@@B@@}^{')
  s=s.replace('ln\u2061'+str(b),'ln\u2061@@B@@')
  s=s.replace(r'\operatorname{ln}'+ '\u2061'+str(b),r'\operatorname{ln}'+'\u2061@@B@@')
  if mid=='q-31254':s=s.replace('{e}^{5x}','{e}^{@@B@@x}')
  if mid=='q-31260':s=s.replace('{e}^{5x}','{e}^{@@B@@x}')
  return s
 T[mid]={'difficulty':q[':question/difficulty'][':db/ident'].split('/')[-1],'parameters':{'base':b},'prompt':slot(q[':question/problem']),'solution':slot(q[':question/worked-solution']),'choices':[slot(s) for s in vals],'correct_index':vals.index(f[':answer-field/correct'][':answer/value']),'field_key':f[':answer-field/key'],'source_id':mid,'plot_rating':'none','policy':'Vary only the positive nonunit exponential base, its matched logarithm, and the explicitly mapped e-exponent in q-31254/q-31260. All other literals and polynomial exponents stay fixed. Wrong-choice expressions are observed parameterized patterns; psychological interpretations unresolved.'}
(H/'templates.json').write_text(json.dumps(T,indent=2)+'\n')
