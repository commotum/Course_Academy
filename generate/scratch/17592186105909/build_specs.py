"""Extract complete-component formatting masks and audited observed bank ratios."""
import json,re
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent
src=json.loads((H/'source.json').read_text())['record']
def readval(t):
 m=re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',t)
 return sp.Rational(m[1],m[2]) if m else sp.Rational(t)
specs={}
for q in src[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];p=[list(map(int,z.replace(' ','').split(','))) for z in re.findall(r'[ABCD]\(([-\d, ]+)\)',q[':question/problem'])]
 vectors=[[x-y for x,y in zip(z,p[0])] for z in p[1:]];volume=abs(sp.Matrix(vectors).det());f=q[':question/answer-fields'][0]
 mask=q[':question/problem']
 for name in 'ABCD':mask=re.sub(name+r'\(([-\d, ]+)\)',name+'(@'+name+'@)',mask)
 sol=q.get(':question/worked-solution');s={'points':p,'vectors':vectors,'prompt_mask':mask,'kind':f[':answer-field/type'][':db/ident'].split('/')[-1],'key':f[':answer-field/key'],'ratios':[str(readval(a[':answer/value'])/volume) for a in f[':answer-field/choices']],'has_difficulty':':question/difficulty' in q,'has_correct':':answer-field/correct' in f,'has_solution':sol is not None}
 s['spacing']=[[x for x in re.findall(r'[ABCD]\(([-\d, ]+)\)',q[':question/problem'])][i].split(',') for i in range(4)]
 if sol:
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);s['prose_mask']=sol
  for i,b in enumerate(blocks):s['prose_mask']=s['prose_mask'].replace(b,'@block'+str(i)+'@',1)
  rows=blocks[0].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
  s['basis_units']=[]
  for i in range(3):
   s['basis_units'].append([[bool(re.search(r'(?<!\d)1'+letter,rows[i*4+j])) for letter in 'ijk'] for j in [1,2]])
  s['subtraction_units']={}
  for i in range(3):
   expression=rows[i*4+1].split('=',1)[1].strip();parts=re.fullmatch(r'\((.*?)\)-\((.*?)\)',expression).groups()
   s['subtraction_units'][str(i)]=[[bool(re.search(r'(?<!\d)1'+letter,part)) for letter in 'ijk'] for part in parts]
  # Preserve the scalar term stage catalog and optional row count.
  outer=blocks[1].split(r' \\  & =')
  # First matrix has row separators but not the continuation prefix.
  arithmetic=outer[2:-1]
  s['arithmetic_row_count']=len(arithmetic)
  s['absolute_spacing']=r'\,' in blocks[2]
  s['final_det_period']=outer[-1].endswith(r'.\end{aligned}')
  s['arithmetic_source']=arithmetic
 specs[sid]=s
(H/'specs.json').write_text(json.dumps(specs,indent=2,ensure_ascii=False)+'\n')
r=json.load(open('/home/jake/Developer/MA/DATA/Lessons/1287/Source/1287.json'))
(H/'authoritative-widget.json').write_text(json.dumps([i for i in r['lesson']['items'] if i['item_type']=='question' and str(i.get('question_id')) in ('20138','128472')],indent=2,ensure_ascii=False)+'\n')
