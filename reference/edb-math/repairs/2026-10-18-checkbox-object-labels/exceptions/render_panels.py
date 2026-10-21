"""Render SVG compositions in Chrome and check exact viewport pixel fidelity."""
import base64,hashlib,io,json,sys
from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
rows=json.loads((HERE/'panel-assets.json').read_text())
OUT=HERE/'rendered-panels';OUT.mkdir(exist_ok=True)
results=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--no-sandbox','--disable-gpu'])
    page=browser.new_page(device_scale_factor=1)
    for row in rows:
        raw=Path(row['svg']).read_bytes();x,y,w,h=row['viewport']
        page.set_viewport_size({'width':max(w,100),'height':max(h,100)})
        page.set_content('<html><body style="margin:0;background:white"><img style="display:block" width="'+str(w)+'" height="'+str(h)+'" src="data:image/svg+xml;base64,'+base64.b64encode(raw).decode()+'"></body></html>')
        page.locator('img').evaluate('(i)=>i.decode()')
        image=page.locator('img').screenshot()
        destination=OUT/f'{row["question_eid"]}-{row["source_label"]}.png';destination.write_bytes(image)
        actual=Image.open(io.BytesIO(image)).convert('RGB')
        original=Image.open(row['source']).convert('RGBA');bg=Image.new('RGBA',original.size,'white');bg.alpha_composite(original)
        expected=bg.convert('RGB').crop((x,y,x+w,y+h))
        diff=ImageChops.difference(actual,expected);bbox=diff.getbbox()
        results.append({'question_eid':row['question_eid'],'source_label':row['source_label'],'rendered':str(destination),'dimensions':[w,h],'exact_pixels':bbox is None,'diff_bbox':bbox,'png_sha256':hashlib.sha256(image).hexdigest()})
    ids=list(dict.fromkeys(row['question_eid']for row in rows))
    for chunk in range(0,len(ids),7):
        content='<html><style>body{margin:12px;font:14px sans-serif}.row{margin:0 0 16px;padding:8px;border:1px solid #aaa}h3{margin:0 0 6px}.imgs{display:flex;gap:20px;align-items:start}.imgs img{max-width:230px;max-height:180px;object-fit:contain}</style><body>'
        for eid in ids[chunk:chunk+7]:
            content+=f'<div class="row"><h3>{eid}</h3><div class="imgs">'
            for result in results:
                if result['question_eid']==eid:
                    b64=base64.b64encode(Path(result['rendered']).read_bytes()).decode();content+=f'<img src="data:image/png;base64,{b64}">'
            content+='</div></div>'
        page.set_viewport_size({'width':1100,'height':1000});page.set_content(content);page.locator('img').evaluate_all('(is)=>Promise.all(is.map(i=>i.decode()))')
        page.screenshot(path=str(OUT/f'overview-{chunk//7+1:02}.png'),full_page=True)
    browser.close()
report={'status':'pass'if all(x['exact_pixels']for x in results)else'fail','images':len(rows),'exact_pixels':sum(x['exact_pixels']for x in results),'results':results}
(HERE/'panel-render-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k!='results'}))
sys.exit(0 if report['status']=='pass'else 1)
