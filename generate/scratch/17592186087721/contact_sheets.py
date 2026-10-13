"""Review thumbnails only; original/generated mathematical assets are unchanged."""
import sys,json,re
from pathlib import Path
sys.path.insert(0,'/home/jake/.cache/uv/wheels-v5/pypi/pillow/12.3.0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64')
from PIL import Image,ImageDraw
P=Path(__file__).parent
for idx,r in enumerate(json.loads((P/'review.json').read_text())):
 f=r['question'][':question/answer-fields'][0];choices=sorted(f[':answer-field/choices'],key=lambda a:Path(a[':answer/value']).name)
 sol=re.findall(r'!\[\]\((.*?)\)',r['question'][':question/worked-solution'])[-1]
 paths=[a[':answer/value'] for a in choices]+[sol];can=Image.new('RGB',(1800,340),'white');d=ImageDraw.Draw(can)
 for i,path in enumerate(paths):
  im=Image.open(path);im.thumbnail((295,295));can.paste(im,(i*300,35));d.text((i*300+3,3),('correct' if i<5 and choices[i][':answer/id']==f[':answer-field/correct'][1] else 'solution' if i==5 else str(i)),fill='black')
 can.save(P/f'generated-{idx:02}.png')
