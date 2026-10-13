import json
from pathlib import Path
H=Path(__file__).resolve().parent
src=json.loads((H/'source.json').read_text());q=src['record'];profiles={}
# n, sign, source constant, numerator coefficient, denominator power.
specs={'q-2389':(3,1,7,3,'1/2','x'),'q-113726':(5,-1,3,7,'6','x'),'q-113728':(3,-1,1,2,'1/2','x'),'q-12502':(2,1,5,1,'10','x'),'q-49560':(5,1,1,10,'1/2','s'),'q-49561':(4,-1,1,4,'5','y'),'q-49575':(2,-1,9,1,'5','x'),'q-49634':(2,1,1,3,'1/2','x'),'q-113727':(6,-1,2,1,'1/2','x')}
lines=[]
for old in q[':knowledge-point/questions']:
 sid=old[':question/math-academy-id'];lines+=['## '+sid,old[':question/problem'],old.get(':question/worked-solution','Missing worked solution')]
 for a in old[':question/answer-fields'][0][':answer-field/choices']:lines.append(a[':answer/value'])
 if sid not in specs:continue
 n,sign,b,k,p,var=specs[sid];base='{'+var+'}^{'+str(n)+'}';patterns=[base+'+'+str(b) if sign==1 else str(b)+'-'+base]
 if sid=='q-49560':patterns.append('{s}^{4}+1')
 def template(text):
  for pattern in patterns:text=text.replace(pattern,pattern.replace(str(b) if sign==1 else str(b)+'-', '@@B@@' if sign==1 else '@@B@@-',1) if sign==-1 else pattern[:-len(str(b))]+'@@B@@')
  return text
 f=old[':question/answer-fields'][0];correct=f[':answer-field/correct'][':answer/value'];values=[correct]+[a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/value']!=correct]
 profiles[sid]={'parameters':[b],'n':n,'sign':sign,'k':k,'power':p,'variable':var,'level':old[':question/difficulty'][':db/ident'].split('/')[-1],'prompt':template(old[':question/problem']),'solution':template(old[':question/worked-solution']),'bank':[template(a) for a in values],'source_uuid':old[':question/id']}
(H/'contract.json').write_text(json.dumps({'basis':src['basis'],'lineage':src['lineage'],'profiles':profiles},indent=2)+'\n')
(H/'source-questions.md').write_text('\n\n'.join(lines)+'\n')
