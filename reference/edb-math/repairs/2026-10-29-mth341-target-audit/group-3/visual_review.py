import json,re,base64,html
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;S=json.loads((H/'current.json').read_text());root=Path('/media/jake/SSD/EDB/math');cards=[];manifest=[]
for q in S['questions']:
 attrs=[q[':question/problem']]+[f[':answer-field/key']for f in q.get(':question/answer-fields',[])];images=[m[1]for a in attrs for m in re.finditer(r'!\[[^\]]*\]\(([^)]*)\)',a)]
 if not images:continue
 imgs=[]
 for asset in images:
  p=root/asset;assert p.is_file(),p;mime='image/svg+xml'if p.suffix=='.svg'else'image/png';imgs.append('<img src="data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()+'">')
 answers=[f[':answer-field/key']+'='+next((a[':answer/value']for a in f[':answer-field/choices']if a[':db/id']==f.get(':answer-field/correct',{}).get(':db/id')),'MISSING')for f in q.get(':question/answer-fields',[])];answers=[re.sub(r'!\[[^\]]*\]\([^)]+\)','diagram',a)for a in answers]
 cards.append('<article><b>'+str(q[':db/id'])+' '+q.get(':question/math-academy-id','')+'</b><div class="imgs">'+''.join(imgs)+'</div><small>'+html.escape('; '.join(answers))+'</small></article>');manifest.append({'entity':q[':db/id'],'images':images,'sheet':len(cards)//9 if len(cards)%9==0 else len(cards)//9+1})
with sync_playwright()as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1500,'height':1400},device_scale_factor=1)
 for i in range(0,len(cards),9):
  page.set_content('<html><style>body{margin:0;font:14px sans-serif}.grid{display:grid;grid-template-columns:repeat(3,500px)}article{border:1px solid #888;padding:8px;box-sizing:border-box;height:440px;overflow:hidden}.imgs{display:flex;align-items:center;justify-content:center;height:350px}.imgs img{max-width:100%;max-height:345px;min-width:0;object-fit:contain}small{font-size:11px}</style><div class="grid">'+''.join(cards[i:i+9])+'</div></html>');page.screenshot(path=str(H/('visual-sheet-'+str(i//9+1)+'.png')),full_page=True)
 browser.close()
(H/'visual-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Visual sheets',len(range(0,len(cards),9)),'questions',len(cards))
