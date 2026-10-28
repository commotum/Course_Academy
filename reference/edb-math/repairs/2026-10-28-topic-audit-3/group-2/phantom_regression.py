import json,sys
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from import_historical_question_content import Renderer
sources=json.loads((H/'sources.json').read_text());s=next(s for s in sources if s['identity']=='q-12457'and s['attribute']=='question/problem');html=s['html'];(H/'q12457-authentic-source.html').write_text('<div id="fixture"><div class="questionText">'+html+'</div></div>')
root=BeautifulSoup(html,'html.parser');m=root.find('math');assert m.find('mphantom');(H/'q12457-authentic-mathml.html').write_text(str(m));rr=Renderer(487);historical=rr.render(root);out={'basis':9837,'question':17592186073998,'math_academy_id':'q-12457','original_path':s['path'],'source_mathml':str(m),'source_formula':s['formulas'],'historical_renderer':historical,'errors':rr.errors,'source_history_limit':'The current retained source explicitly marks the minus as mphantom. Old stored import made it visible; retained old implementation provenance has not been reconstructed, so no attribution to a particular old textContent call is asserted.'}
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page();page.set_content((H/'q12457-authentic-source.html').read_text())
 for name,path in [('dom','scripts/question_capture/dom.js'),('capture','capture/scripts/browser/extract.js')]:out[name]=page.eval_on_selector('#fixture',(R/path).read_text())
 b.close()
for name,value in [('historical',historical),('dom',out['dom']['problem']),('capture',out['capture']['problem'])]:
 assert '-6a'not in value.replace(' ','')and'6a'in value.replace(' ',''),(name,value)
(H/'q12457-phantom-regression.json').write_text(json.dumps(out,indent=2)+'\n');print('All3 current extraction paths keep6a positive; source mphantom retained as evidence.')
