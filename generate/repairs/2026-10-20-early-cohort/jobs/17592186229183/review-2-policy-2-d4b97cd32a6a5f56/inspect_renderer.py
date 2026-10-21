from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;out=R/'render-inspection';out.mkdir(exist_ok=True)
files=sorted((R/'render').glob('question-*.png'));assert len(files)==27
# Remaining six unchanged source contexts plus complete worked-solution middle.
for i in [0,10,12,16,17,21,22,23,24,25,26]:
 im=Image.open(files[i]);w,h=im.size
 for tag,y,hh in [('top',0,1500),('middle',h//2-600,1200),('bottom',h-950,950)]:
  im.crop((0,max(0,y),w,min(h,y+hh))).save(out/f'case-{i+1:02}-{tag}.png')
for tag in ['top','bottom']:
 sheet=Image.new('RGB',(1500,1200),'#ddd')
 for j,i in enumerate(range(21,27)):
  im=Image.open(files[i]);w,h=im.size;im=im.crop((0,0,w,min(h,1500))) if tag=='top' else im.crop((0,max(0,h-950),w,h));im.thumbnail((480,560));sheet.paste(im,((j%3)*500,(j//3)*600+25));ImageDraw.Draw(sheet).text(((j%3)*500+10,(j//3)*600+5),f'UI record {i+1}',fill='black')
 sheet.save(out/f'remaining-{tag}.png')
print('27 actual screenshots retained; additional inspection crops created')
