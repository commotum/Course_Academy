import json,re,sys
from pathlib import Path
from PIL import Image,ImageDraw
sys.path.insert(0,'scripts');from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT
H=Path(__file__).resolve().parent;qs=json.loads((H/'ellipse-other-records.json').read_text());qs=[q for q in qs if 'Cartesian'not in q[':question/problem']and'Consider the ellipse'not in q[':question/problem']];rows=[];w=1400;ch=340;out=Image.new('RGB',(w,((len(qs)+3)//4)*ch),'white');draw=ImageDraw.Draw(out)
for i,q in enumerate(qs):
 p=image_path(re.search(r'!\[.*?\]\(([^)]+)\)',q[':question/problem'])[1],DEFAULT_MATH_ROOT);im=Image.open(p).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);im=bg.convert('RGB');im.thumbnail((340,300));x=(i%4)*350;y=(i//4)*ch;out.paste(im,(x+(350-im.width)//2,y+30));draw.text((x+5,y+5),str(i)+' '+str(q[':db/id'])+' '+str(q.get(':question/math-academy-id')),(0,0,0));rows.append({'index':i,'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'image':str(p)})
out.save(H/'ellipse-arc-contact.png');(H/'ellipse-arc-image-index.json').write_text(json.dumps(rows,indent=2));print(len(rows))
