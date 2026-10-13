import json,re
from pathlib import Path
H=Path(__file__).parent
qs=json.load(open(H/'source.json'))['record'][':knowledge-point/questions']
M={}
def slot(n,d=1):return '@'+str(n)+':'+str(d)+'@'
def replace_islands(text,updates):
 i=-1
 def change(m):
  nonlocal i;i+=1;v=m.group()
  for old,new in updates.get(i,[]):
   assert old in v,(i,old,v)
   v=v.replace(old,new)
  return v
 return re.sub(r'\$\$.*?\$\$|\$[^$]*\$',change,text,flags=re.S)
# Every tuple/radius/substitution/conclusion has its own mathematical mask.
P={
'q-40803':{6:[('10',slot(10,2))]},
'q-40806':{1:[('2',slot(2))],3:[('(1,','('+slot(1)+',')],6:[('2',slot(2,2))]},
'q-120455':{6:[('-3',slot(-3)),(r'\sqrt{3}',r'\sqrt{'+slot(3,2)+'}')]},
'q-120468':{1:[('2',slot(2))],3:[('(4,','('+slot(4)+',')],6:[(r'\sqrt{3}',r'\sqrt{'+slot(3,2)+'}'),('-1',slot(-1))]},
'q-276803':{6:[(r'\sqrt{3}',r'\sqrt{'+slot(3,2)+'}'),(',1)',','+slot(1)+')')]},
'q-276807':{6:[('2',slot(2))]},
'q-276838':{1:[('5',slot(5))],3:[('(5,','('+slot(5)+',')],6:[('5',slot(5))]},
'q-40804':{6:[('5',slot(5,2))]},
'q-40826':{1:[('2',slot(2,2))],3:[('(8,','('+slot(8)+',')],6:[('-1',slot(-1))]},
'q-86619':{6:[('3',slot(3))]}}
S={
'q-120455':{3:[('(-3)','('+slot(-3)+')'),(r'\sqrt{3}',r'\sqrt{'+slot(3,2)+'}'),('12',slot(12,2))],5:[('12',slot(12,2))],10:[('12',slot(12,2)),('6\\sqrt',slot(6,2)+r'\sqrt')],13:[('12',slot(12,2)),('=-6','='+slot(-6,2))],15:[('6\\sqrt',slot(6,2)+r'\sqrt'),(',-6',','+slot(-6,2))]},
'q-120468':{2:[(r'\frac{-1}{-\sqrt{3}}',r'\frac{'+slot(-1)+r'}{-\sqrt{'+slot(3,2)+'}}')],6:[('(4,','('+slot(4)+',')],11:[('=4\\cdot','='+slot(4)+r'\cdot')],14:[('=4\\cdot','='+slot(4)+r'\cdot'),('=-4','='+slot(-4))],16:[(',-4',','+slot(-4))]},
'q-276803':{3:[(r'(\sqrt{3})',r'(\sqrt{'+slot(3,2)+'})'),('{1}^{2}','{'+slot(1)+'}^{2}'),(r'\sqrt{4}',r'\sqrt{'+slot(4,2)+'}'),('=2\\end','='+slot(2)+r'\end')],5:[(r'\frac{2}{3}',r'\frac{'+slot(2)+'}{3}')],10:[(r'\frac{2}{3}',r'\frac{'+slot(2)+'}{3}'),(r'=-\frac{\sqrt{3}}{3}',r'=-\frac{\sqrt{'+slot(3,2)+'}}{3}')],13:[(r'\frac{2}{3}',r'\frac{'+slot(2)+'}{3}'),(r'=\frac{1}{3}',r'=\frac{'+slot(1)+'}{3}')],15:[(r'\sqrt{3}',r'\sqrt{'+slot(3,2)+'}'),(r'\frac{1}{3}',r'\frac{'+slot(1)+'}{3}')]},
'q-276807':{3:[('(2\\sqrt','('+slot(2)+r'\sqrt'),('(2)^{2}','('+slot(2)+')^{2}'),('16',slot(16,2)),('=4\\end','='+slot(4)+r'\end')],5:[('2\\cdot 4','2\\cdot '+slot(4)),('(8,','('+slot(8)+',')],10:[('=8','='+slot(8)),('=-4\\sqrt','='+slot(-4)+r'\sqrt')],13:[('=8','='+slot(8)),('=-4','='+slot(-4))],15:[('-4',slot(-4))]},
'q-276838':{2:[(r'\frac{0}{5}',r'\frac{0}{'+slot(5)+'}')],6:[('(5,','('+slot(5)+',')],11:[('=5\\cdot','='+slot(5)+r'\cdot'),(r'\frac{5\sqrt',r'\frac{'+slot(5)+r'\sqrt')],14:[('=5\\cdot','='+slot(5)+r'\cdot'),(r'\frac{5}{2}',r'\frac{'+slot(5)+'}{2}')],16:[(r'\frac{5',r'\frac{'+slot(5))]},
'q-40804':{3:[('5',slot(5,2)),('10',slot(10,2))],5:[('10',slot(10,2))],10:[('=10','='+slot(10,2)),('=-5','='+slot(-5,2))],13:[('=10','='+slot(10,2)),('=-5','='+slot(-5,2))],15:[('-5',slot(-5,2))]},
'q-40826':{2:[(r'\frac{-1}{-1}',r'\frac{'+slot(-1)+'}{'+slot(-1)+'}')],6:[('(8,','('+slot(8)+',')],11:[('=8\\operatorname','='+slot(8)+r'\operatorname'),('=8\\cdot','='+slot(8)+r'\cdot'),('=4\\sqrt','='+slot(4)+r'\sqrt')],14:[('=8\\operatorname','='+slot(8)+r'\operatorname'),('=8\\cdot','='+slot(8)+r'\cdot'),('=4\\sqrt','='+slot(4)+r'\sqrt')],16:[('4\\sqrt',slot(4)+r'\sqrt')]},
'q-86619':{3:[('3\\sqrt',slot(3)+r'\sqrt'),('18',slot(18,2)),('36',slot(36,2)),('=6\\end','='+slot(6)+r'\end')],5:[(r'\frac{6}{2}',r'\frac{'+slot(6)+'}{2}'),('(3,','('+slot(3)+',')],10:[('=3','='+slot(3)),(r'\frac{3\sqrt',r'\frac{'+slot(3)+r'\sqrt')],13:[('=3','='+slot(3)),(r'\frac{3}{2}',r'\frac{'+slot(3)+'}{2}')],15:[(r'\frac{3',r'\frac{'+slot(3))]}}
for q in qs:
 n=q[':question/math-academy-id'];m={'problem':replace_islands(q[':question/problem'],P[n]),'banks':{}}
 if ':question/worked-solution' in q:m['solution']=replace_islands(q[':question/worked-solution'],S[n])
 degree=2 if n in ['q-120455','q-40804'] else 1
 for f in q[':question/answer-fields']:
  # Homogeneous whole-coordinate transformations are evidence recipes only.
  m['banks'][f[':answer-field/key']]=[{'original':a[':answer/value'],'degree':degree} for a in f[':answer-field/choices']]
 M[n]=m
(H/'masks.json').write_text(json.dumps(M,indent=2,ensure_ascii=False))
