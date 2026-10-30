import json
from pathlib import Path
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;rows=json.loads((H/'candidate-pool.json').read_text())
for page in range(5):
    out=Image.new('RGB',(1500,930),'#eee');draw=ImageDraw.Draw(out)
    for ri,r in enumerate(rows[page*3:page*3+3]):
        for ci,path in enumerate(r['generation']['paths']):
            im=Image.open(path).convert('RGB');im.thumbnail((290,282));out.paste(im,(ci*300+5,ri*310+24))
            draw.text((ci*300+5,ri*310+4),str(page*3+ri+1)+' '+r['generation']['level']+' choice '+str(ci),fill='black')
    out.save(H/f'bank-contact-{page+1}.png')
