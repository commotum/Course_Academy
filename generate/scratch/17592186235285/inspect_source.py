import sys,re,json
from pathlib import Path
cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
for name in ('pillow',):
 paths=[p for p in (cache/name).iterdir() if p.is_dir() and 'cp310' in p.name and 'manylinux' in p.name]
 sys.path.insert(0,str(sorted(paths)[-1]))
from PIL import Image,ImageDraw
H=Path(__file__).parent
s=json.loads((H/'source.json').read_text())['record'];qs=s[':knowledge-point/questions']
for start in (0,5,10):
 out=Image.new('RGB',(1400,1250),'white');d=ImageDraw.Draw(out)
 for i,q in enumerate(qs[start:start+5]):
  d.text((5,i*250+4),q[':question/math-academy-id'],fill='black')
  for j,key in enumerate([':question/problem',':question/worked-solution']):
   p=re.findall(r'!\[\]\((.*?)\)',q[key])[0];im=Image.open('/media/jake/SSD/EDB/math/'+p).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);bg=bg.convert('RGB');bg.thumbnail((660,220));out.paste(bg,(40+j*690,i*250+25))
 out.save(H/f'source-diagrams-{start}.png')
# Canonical all embedded math + diagrams and relevant linked tutorial diagrams.
refs=re.findall(r'!\[\]\((.*?)\)',s[':knowledge-point/canonical-example'][':question/problem']+'\n'+s[':knowledge-point/canonical-example'][':question/worked-solution'])
out=Image.new('RGB',(1600,1100),'white');d=ImageDraw.Draw(out)
for i,p in enumerate(refs):
 im=Image.open('/media/jake/SSD/EDB/math/'+p).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);bg=bg.convert('RGB');bg.thumbnail((380,160));x=i%4*400;y=i//4*180;out.paste(bg,(x,y+20));d.text((x,y),str(i)+' '+p.split('/')[-1][:8],fill='black')
out.save(H/'canonical-all.png')
