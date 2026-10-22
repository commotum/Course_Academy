from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
for dirname,prefix in [('render','render-first'),('render-delivered','render-contact')]:
 files=sorted((root/dirname).glob('question-*.png'))
 for start in range(0,len(files),6):
  sub=files[start:start+6]
  out=Image.new('RGB',(1410,740*((len(sub)+2)//3)),'#222222')
  for i,p in enumerate(sub):
   im=Image.open(p).convert('RGB');top=im.crop((int(im.width*.2),90,int(im.width*.83),min(im.height,1000)))
   top.thumbnail((450,700));canvas=Image.new('RGB',(470,740),'#222222');canvas.paste(top,((470-top.width)//2,30));ImageDraw.Draw(canvas).text((10,10),p.name,fill='white')
   out.paste(canvas,((i%3)*470,(i//3)*740))
  out.save(root/f'{prefix}-{start}.png')
