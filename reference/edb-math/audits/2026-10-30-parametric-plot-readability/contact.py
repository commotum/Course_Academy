import json,re
from pathlib import Path
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;MATH=Path('/media/jake/SSD/EDB/math');k=json.loads((H/'kp.json').read_text())
imports=[q for q in k[':knowledge-point/questions'] if q.get(':question/math-academy-id')]
def sheet(rows,name,cols=2):
 w,h=440,360;out=Image.new('RGB',(cols*w,((len(rows)+cols-1)//cols)*h),'#eee');d=ImageDraw.Draw(out)
 for n,(label,path) in enumerate(rows):
  im=Image.open(MATH/path).convert('RGB');im.thumbnail((420,326));x=(n%cols)*w;y=(n//cols)*h
  d.text((x+8,y+8),label,fill='black');out.paste(im,(x+10+(420-im.width)//2,y+28+(326-im.height)//2))
 out.save(H/name)
for page in range(4):
 rows=[]
 for q in imports[page*4:(page+1)*4]:
  f=q[':question/answer-fields'][0];rows.append((q[':question/math-academy-id']+' CHOICE',f[':answer-field/correct'][':answer/value']))
  path=re.findall(r'images/[^)\s]+',q[':question/worked-solution'])[-1];rows.append((q[':question/math-academy-id']+' SOLUTION',path))
 sheet(rows,f'sources-{page+1}.png')
for eid in (17592186535273,17592186088027,17592186393320,17592186281377):
 q=next(q for q in k[':knowledge-point/questions'] if q[':db/id']==eid);f=q[':question/answer-fields'][0]
 rows=[(str(eid)+' '+str(n+1)+(' CORRECT' if a[':db/id']==f[':answer-field/correct'][':db/id'] else ''),a[':answer/value']) for n,a in enumerate(f[':answer-field/choices'])]
 sheet(rows,f'bank-{eid}.png',3)
print('Created four source comparison sheets and four complete answer-bank sheets')
