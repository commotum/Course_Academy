"""Contact sheets of existing artifacts for human QA; no image generation/edit."""
import sys,json,re,pathlib
H=pathlib.Path(__file__).resolve().parent;P=json.loads((H/'render-provenance.json').read_text());sys.path[:0]=list(P['dependency_paths'].values())
from PIL import Image,ImageDraw
records=json.loads((H/'review.json').read_text())
for batch in range((len(records)+5)//6):
 selected=records[batch*6:(batch+1)*6];out=Image.new('RGB',(6*270,len(selected)*300),'white');d=ImageDraw.Draw(out)
 for j,r in enumerate(selected):
  q=r['question'];vals=[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]+re.findall(r'!\[\]\((.*?)\)',q[':question/worked-solution'])[-1:]
  for i,v in enumerate(vals):
   p=pathlib.Path(v) if v.startswith('/') else pathlib.Path('/media/jake/SSD/EDB/math')/v;im=Image.open(p).convert('RGBA');white=Image.new('RGBA',im.size,'white');white.alpha_composite(im);white=white.convert('RGB');white.thumbnail((265,270));out.paste(white,(i*270,j*300+25));d.text((i*270+3,j*300+5),r['generation']['bank_profile']+' '+str(r['generation']['parameters']) if i==0 else ('guide' if i==5 else str(i+1)),fill='black')
 out.save(H/('review-sheet-'+str(batch+1)+'.png'))
