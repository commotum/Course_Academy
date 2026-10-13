"""Inspect generated E/M/H prompt/solution plots, two instances at each level."""
import sys,json
from pathlib import Path
cache=Path('/home/jake/.cache/uv/wheels-v5/pypi/pillow');sys.path.insert(0,str(sorted(p for p in cache.iterdir() if p.is_dir() and 'cp310' in p.name and 'manylinux' in p.name)[-1]))
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;records=json.loads((H/'contact-input.json').read_text())
out=Image.new('RGB',(1600,1380),'white');d=ImageDraw.Draw(out)
for row,level in enumerate(('easy','moderate','hard')):
 rs=[r for r in records if r['question'][':question/difficulty'].endswith('/'+level)]
 for sample,r in enumerate(rs):
  p=r['generation']['parameters'];base=f'{level}, example{sample+1}, r={p["r"]}, k={p["k"]}'
  for j,role in enumerate(('prompt','solution')):
   x=(sample*2+j)*400;y=row*460;d.text((x+10,y+8),base+' / '+role,fill='black')
   im=Image.open(r['generation']['plot_assets'][role]).convert('RGB');im.thumbnail((395,425));out.paste(im,(x+2,y+28))
out.save(H/'generated-levels-contact.png')
