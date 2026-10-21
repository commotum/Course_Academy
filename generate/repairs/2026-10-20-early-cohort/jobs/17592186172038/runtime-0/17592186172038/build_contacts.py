import sys,json
from pathlib import Path
sys.path.insert(0,'/home/jake/.cache/uv/archive-v0/4-AemGpMwlNQVMB0M4sW_')
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];rs=json.load(open(HERE/'review.json'))+json.load(open(HERE/'source-replays.json'))
for batch in range((len(rs)+5)//6):
 selected=rs[batch*6:batch*6+6];board=Image.new('RGB',(1500,len(selected)*330),'white');d=ImageDraw.Draw(board)
 for j,r in enumerate(selected):
  d.text((10,j*330+3),f'{r["question"][":question/difficulty"]} {r["generation"]["template"]} {r["generation"]["bank_profile"]}',fill='black')
  for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']):
   im=Image.open(ROOT/a[':answer/value']);im.thumbnail((295,295));board.paste(im,(i*300,j*330+25))
 board.save(HERE/f'generated-contact-{batch}.png')
