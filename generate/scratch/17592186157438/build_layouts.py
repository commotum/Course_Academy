"""One-time extraction of whole mathematical components, not token substitution."""
import json,re,shutil
from pathlib import Path
HERE=Path(__file__).parent
SNAPSHOT=HERE.parent.parent/'runs/current/sources/17592186157438.json'
raw=json.loads(SNAPSHOT.read_text());qs=raw['record'][':knowledge-point/questions']
(HERE/'source.json').write_text(json.dumps(raw,indent=2)+'\n')
lesson=json.loads(Path('/home/jake/Developer/MA/DATA/Lessons/2979/Source/2979.json').read_text())
widgets=[i for i in lesson['lesson']['items'] if i.get('question_id') in ['237949','88417','88472']]
(HERE/'original-widgets.json').write_text(json.dumps({'path':'/home/jake/Developer/MA/DATA/Lessons/2979/Source/2979.json','widgets':widgets,'q88472':'not present in original snapshot; no widget layout recovered'},indent=2)+'\n')
for name in ['06-question-88417.png','07-question-237949.png']:shutil.copyfile('/home/jake/Developer/MA/DATA/Lessons/2979/Source/Sections/'+name,HERE/name)
math_re=re.compile(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^$]*\$')
layouts={}
for q in qs:
 sid=q[':question/math-academy-id']
 # Replace the entire assessed equation (first math span only).
 prompt=q[':question/problem'];m=math_re.search(prompt)
 if sid=='q-237949':equation='<<EQ_SPACED>>'
 elif sid=='q-88417':equation='<<EQ_SPACED>>'+('?' if m[0].endswith('?$') else '')
 else:equation='<<EQ>>'+('?' if m[0].endswith('?$') else '')
 prompt=prompt[:m.start()]+'$'+equation+'$'+prompt[m.end():]
 sol=q.get(':question/worked-solution');masked=None
 if sol:
  spans=list(math_re.finditer(sol));changes={0:'$$\n<<ALIGNED>>\n$$',4:r'$$'+'\n'+r'<<POLY>>=0\,\text{and}\,<<E>>=0.'+'\n$$',5:'$<<POLY>>=0$',6:'$$\n<<FACTOR_STAGE>>\n$$',7:'$x=<<ROOTS>>.$'}
  offset=1 if sid in ['q-264786','q-264787','q-88474'] else 0
  if offset:changes[8]='$<<G>>=0$'
  changes[8+offset]='$<<E>>=0$';changes[9+offset]='$<<E>>$'
  if ':answer-field.type/blank' in str(q.get(':question/answer-fields',[])):
   changes[11+offset]='$$\nx=<<R1>>'+r'\,\text{and}\,x=<<R2>>.'+'\n$$'
  else:
   changes[11+offset]='$x=<<ROOTS>>,$';changes[12+offset]='$<<PRODUCT>>.$'
  masked=sol
  for i in sorted(changes,reverse=True):
   m=spans[i];masked=masked[:m.start()]+changes[i]+masked[m.end():]
 layouts[sid]={'prompt':prompt,'solution':masked,'repair':'Remove trailing + from first rearrangement row' if sid=='q-264791' else None}
(HERE/'layouts.json').write_text(json.dumps(layouts,indent=2)+'\n')
rows=[
 ('q-237949','quadratic_unrated_blank',dict(g=1,p=3,q=1,r=1,s=-2,base='e',u=1,v=5),'blank','moderate'),
 ('q-88417','difference_rational_product',dict(g=1,p=2,q=5,r=2,s=-5,base='e',u=1,v=0),'observed:q-88417','easy'),
 ('q-88472','quadratic_right_const_linear_product',dict(g=1,p=2,q=3,r=2,s=-1,base='e',u=5,v=0),'authored:product-errors','moderate'),
 ('q-100797','quadratic_right_linear_const_product',dict(g=1,p=5,q=2,r=1,s=-3,base=8,u=1,v=0),'observed:q-100797','moderate'),
 ('q-264786','difference_integer_blank',dict(g=2,p=1,q=5,r=1,s=-5,base=3,u=2,v=-5),'blank','easy'),
 ('q-264787','difference_integer_blank',dict(g=4,p=1,q=6,r=1,s=-6,base=5,u=1,v=-4),'blank','easy'),
 ('q-264788','difference_rational_blank',dict(g=1,p=3,q=8,r=3,s=-8,base='e',u=1,v=3),'blank','easy'),
 ('q-264791','quadratic_left_const_negative_blank',dict(g=1,p=3,q=2,r=1,s=3,base=7,u=1,v=0),'blank','moderate'),
 ('q-264793','quadratic_left_const_positive_blank',dict(g=1,p=4,q=-1,r=1,s=-6,base='e',u=2,v=0),'blank','moderate'),
 ('q-88473','reverse_quadratic_product',dict(g=1,p=3,q=7,r=1,s=-1,base=6,u=1,v=-2),'observed:q-88473','moderate'),
 ('q-88474','quadratic_left_const_product',dict(g=3,p=1,q=3,r=1,s=-5,base=5,u=1,v=0),'observed:q-88474','moderate'),
 ('q-110803','difference_unit_product',dict(g=1,p=1,q=1,r=1,s=-1,base=10,u=-1,v=2),'observed:q-110803','easy'),
]
cases=[{'source_id':sid,'template':t,'parameters':p,'bank_profile':prof,'level':level,'authored_level_assignment':sid in ['q-237949','q-88417']} for sid,t,p,prof,level in rows]
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
