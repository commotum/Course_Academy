"""Reproduce both capture paths offline from retained source HTML fragments."""
import importlib.util,json,re
from pathlib import Path
from bs4 import BeautifulSoup
import subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
if __name__=='__main__':
 history=module('history_renderer',ROOT/'scripts/import_historical_question_content.py');fmt=module('reproduction_formatter',ROOT/'scripts/question_capture/math_format.py')
 fixtures=json.loads((HERE/'source-fixtures.json').read_text())['fixtures'];reports=[]
 config=json.loads((ROOT/'reference/mathacademy/repairs/2026-10-18-power-lesson/ui/browser-config.json').read_text())
 script=HERE/'extract-offline.cjs'
 script.write_text(r"""const fs=require('fs');
const config=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const fixtures=JSON.parse(fs.readFileSync(process.argv[3],'utf8')).fixtures;
const source=fs.readFileSync(process.argv[4],'utf8');
const {chromium}=require(config.playwright);
(async()=>{const browser=await chromium.launch({headless:true,executablePath:config.browser,args:['--disable-dev-shm-usage']});const page=await browser.newPage();await page.route('**/*',r=>r.abort());const results=[];
for(const f of fixtures){const html=f.kind==='mathml'?f.html:'<div class="mjpage mjpage__block">'+f.html+'</div>';await page.setContent('<div id="fixture"><div class="questionWidget-text">'+html+'</div></div>');results.push(await page.locator('#fixture').evaluate((el,src)=>eval('('+src+'\n)')(el),source));}
await browser.close();fs.writeFileSync(process.argv[5],JSON.stringify(results,null,2));})().catch(e=>{console.error(e);process.exit(1)});
""")
 (HERE/'browser-config.json').write_text(json.dumps(config))
 subprocess.run([config['node'],str(script),str(HERE/'browser-config.json'),str(HERE/'source-fixtures.json'),str(ROOT/'capture/scripts/browser/extract.js'),str(HERE/'raw-extractions.json')],check=True,timeout=45)
 results=json.loads((HERE/'raw-extractions.json').read_text())
 for f,result in zip(fixtures,results):
  raw=result['problem'];normalized=fmt.normalize_prose(raw)
  assert not result['errors'],result['errors'];assert r'\eqalign' not in normalized;assert not re.search(r'&\s*=\s*\\\\',normalized)
  item={'step_id':f['step_id'],'content_id':f['content_id'],'kind':f['kind'],'raw_capture':raw,'current_preparation':normalized,'capture_needs_layout_normalization':raw!=normalized}
  if f['kind']=='mathml':
   legacy=history.Renderer(None).m(BeautifulSoup(f['html'],'html.parser').find('math'));item['historical_python_conversion']=legacy
   assert fmt.normalize_equality_chains(legacy)!=legacy
  reports.append(item)
 (HERE/'reproduction.json').write_text(json.dumps({'passed':True,'fixtures':reports,'database_writes':0},indent=2)+'\n');print('Reproduced',len(reports),'archived formulas; current preparation repairs their equality chains.')
