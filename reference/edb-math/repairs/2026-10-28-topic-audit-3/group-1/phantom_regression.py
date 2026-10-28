import importlib.util,json,sys,re
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));P=H/'phantom-patch'
spec=importlib.util.spec_from_file_location('staged_historical',P/'import_historical_question_content.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
raw=(H/'visual-review/q-162407-source.html').read_text();source=BeautifulSoup(raw,'html.parser');math=next(m for m in source.find_all('math')if m.find('mphantom'));(H/'visual-review/q-162407-mathml.html').write_text(str(math))
assert not source.select('.selectList,.freeResponseTextbox,input,select')
fixtures=[('decorated',raw),('bare',(H.parent/'group-2/q12457-authentic-source.html').read_text())]
out={'basis_t':9837,'question':17592186134135,'response_frame':'one existing radio field selection; no input in formula','fixtures':[]}
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page()
 for name,html in fixtures:
  soup=BeautifulSoup(html,'html.parser');rr=mod.Renderer(None);historic=rr.render(soup)
  page.set_content('<div id="fixture"><div class="questionText">'+html+'</div></div>');item={'name':name,'historical':historic,'historical_errors':rr.errors}
  for label,path in [('dom',P/'dom.js'),('capture',R/'capture/scripts/browser/extract.js')]:item[label]=page.eval_on_selector('#fixture',path.read_text())
  for label,text in [('historical',historic),('dom',item['dom']['problem']),('capture',item['capture']['problem'])]:
   if name=='decorated':assert r'\phantom{AAAAA}'in text and 'border:'in text,(name,label,text)
   else:assert '-6a'not in text.replace(' ','')and '6a'in text.replace(' ',''),(name,label,text)
  assert not rr.errors,(name,rr.errors)
  assert not item['dom']['errors'],item['dom']['errors'];assert not item['capture']['errors'],item['capture']['errors']
  out['fixtures'].append(item)
 b.close()
(H/'decorated-phantom-regression.json').write_text(json.dumps(out,indent=2)+'\n');print('Both authentic fixtures pass all three paths; hidden bbox width retained and bare minus remains invisible.')
