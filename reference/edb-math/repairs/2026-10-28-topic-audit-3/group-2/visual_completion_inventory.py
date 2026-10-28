import json,re,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[4]/'scripts'));from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT
out=[]
for q in json.loads((H/'incomplete.json').read_text()):
 for i,path in enumerate(re.findall(r'!\[[^]]*\]\(([^)]+)\)',q[':question/problem'])):
  p=image_path(path,DEFAULT_MATH_ROOT)
  if p:out.append({'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'role':'prompt '+str(i),'path':str(p)})
 for f in q.get(':question/answer-fields',[]):
  for a in f.get(':answer-field/choices',[]):
   if a[':answer/type'][':db/ident']==':answer.type/image':
    p=image_path(a[':answer/value'],DEFAULT_MATH_ROOT)
    if p:out.append({'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'role':'choice '+str(a[':db/id']),'path':str(p)})
(H/'completion-visual-index.json').write_text(json.dumps(out,indent=2)+'\n');font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
for offset in range(0,len(out),6):
 sheet=Image.new('RGB',(1080,840),'#eeeeee');draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(out[offset:offset+6]):
  xx=(i%3)*360;yy=(i//3)*420;draw.text((xx+6,yy+4),r['identity']+' '+r['role'],font=font,fill='black');im=Image.open(r['path']).convert('RGBA');im.thumbnail((345,380));base=Image.new('RGBA',im.size,'white');base.alpha_composite(im);sheet.paste(base.convert('RGB'),(xx+(360-im.width)//2,yy+35+(380-im.height)//2))
 sheet.save(H/('completion-visual-'+str(offset//6)+'.png'))
print('figures',len(out),'pages',(len(out)+5)//6)
