"""White-composited QA contact sheets; no plot mathematics or resampling."""
import json,subprocess,sys,re
from pathlib import Path
D=Path(__file__).resolve().parent
# Reuse the renderer's read-only cached dependency setup.
code=(D/'render.py').read_text().split("if sys.argv[1]=='montage':")[0]
exec(code)
if sys.argv[1]=='canonical':
 source=json.loads((D/'source.json').read_text())['record'][':knowledge-point/canonical-example']
 refs=re.findall(r'!\[.*?\]\((.*?)\)',source[':question/problem']+source[':question/worked-solution'])
 canvas=Image.new('RGB',(1600,750),'white');draw=ImageDraw.Draw(canvas)
 for i,ref in enumerate(refs):
  im=Image.open(Path('/media/jake/SSD/EDB/math')/ref).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);im=bg.convert('RGB');im.thumbnail((770,700));canvas.paste(im,(i*800+(790-im.width)//2,35));draw.text((i*800+10,5),'e-6818 '+('prompt' if i==0 else 'solution'),fill='black')
 canvas.save(D/'canonical-montage.png')
else:
 records=json.loads((D/'engine-input.json').read_text());unique={}
 for item in records:
  r=item['record'];g=r['generation'];key=g['plot_assets']['prompt'];unique.setdefault(key,(item['label'],g['parameters'],g['plot_assets']))
 entries=list(unique.values())
 (D/'plot-contact-index.json').write_text(json.dumps(entries,indent=2)+'\n')
 for page in range((len(entries)+5)//6):
  canvas=Image.new('RGB',(1600,1800),'white');draw=ImageDraw.Draw(canvas)
  for row,(label,p,assets) in enumerate(entries[page*6:page*6+6]):
   for col,role in enumerate(('prompt','solution')):
    im=Image.open(assets[role]).convert('RGB');im.thumbnail((770,265));canvas.paste(im,(col*800+(790-im.width)//2,row*300+30));draw.text((col*800+5,row*300+5),label+' '+role+' '+str(p),fill='black')
  canvas.save(D/f'generated-montage-{page}.png')
 print(len(entries),'unique generated plot pairs',page+1,'contact sheets')
