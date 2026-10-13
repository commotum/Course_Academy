"""Generate contact sheets from completed exact-instance Matplotlib assets.

Uses system Python/Pillow only for compositing existing rendered PNGs, not for
creating/editing mathematical plots. Mathematical images come from renderer.py.
"""
import json
from pathlib import Path
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent
R=json.loads((H/'review.json').read_text());assets=[]
for record in R['generated_variants']:
 for role in ('prompt','solution'):
  assets.append((record['generation']['template']+' seed '+str(record['generation']['seed'])+' '+role,record['generation']['plots'][role]['path']))
for page in range(0,len(assets),8):
 im=Image.new('RGB',(1200,1800),'white');draw=ImageDraw.Draw(im)
 for i,(label,path) in enumerate(assets[page:page+8]):
  pic=Image.open(path);pic.thumbnail((570,405));x=(i%2)*600;y=(i//2)*450;im.paste(pic,(x,y+30));draw.text((x+5,y+8),label,fill='black')
 im.save(H/f'generated-contact-{page//8}.png')
print(len(assets),'generated plots in',len(range(0,len(assets),8)),'contact sheets')
