import json,pathlib,re
from PIL import Image,ImageDraw
root=pathlib.Path.cwd();job=root.parent
qs=json.load(open(job/'source/inventory.json'))['questions'];qs=[q for q in qs if ':question/math-academy-id' not in q]
out=Image.new('RGB',(1250,len(qs)*270),'white');d=ImageDraw.Draw(out);meta=[]
for i,q in enumerate(qs):
 d.text((2,i*270),f"{i+1}: {q[':db/id']} {q[':question/id']} {q[':question/difficulty']}",fill='black');f=q[':question/answer-fields'][0]
 row={'row':i+1,'entity':q[':db/id'],'id':q[':question/id'],'prompt':q[':question/problem'],'opening':q[':question/worked-solution'].split('\n\n')[0],'correct':f.get(':answer-field/correct'),'choices':[]}
 for j,a in enumerate(f[':answer-field/choices']):
  p=pathlib.Path('/media/jake/SSD/EDB/math')/a[':answer/value'];im=Image.open(p).convert('RGB');im.thumbnail((245,245));out.paste(im,(250*j,i*270+25));d.text((250*j+5,i*270+15),str(j+1),fill='black');row['choices'].append({'position':j+1,'id':a[':answer/id'],'asset':a[':answer/value']})
 meta.append(row)
out.save(root/'inventory-banks.png');(root/'inventory-observations.json').write_text(json.dumps(meta,indent=2))
print('prepared',len(meta),'non-MA inventory banks')
