"""Offline replay of captured DOMs and controlled formatting metadata fixtures."""
import hashlib,json,re
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SOURCES=[
 ('bad-definite-integral','reference/mathacademy/question-capture-workers/multivariable/14037313/q-349253-before.json'),
 ('bad-indefinite-integral','reference/mathacademy/question-capture-workers/linear/14038125/q-114289-before.json'),
 ('good-svg-title','reference/mathacademy/question-capture/14009414/example-491.json')]
MML='<mstyle displaystyle="true" scriptlevel="0"><msubsup><mo>∫</mo><mn>0</mn><mn>1</mn></msubsup><mi>x</mi><mtext>d</mtext><mi>x</mi></mstyle>'
def fixture(inner):return '<div id="fixture"><div class="questionWidget-text">Evaluate '+inner+'</div></div>'
def main():
 scripts={name:(ROOT/file).read_text() for name,file in [('legacy','scripts/question_capture/dom.js'),('active','capture/scripts/browser/extract.js')]};cases=[]
 for name,file in SOURCES:
  source=json.loads((ROOT/file).read_text());cases.append({'name':name,'file':file,'html':source['html'],'recorded_problem':source['problem']})
 for name,inner in [
  ('inline-container-with-displaystyle','<mjx-container><mjx-assistive-mml><math>'+MML+'</math></mjx-assistive-mml></mjx-container>'),
  ('display-container','<mjx-container display="true"><mjx-assistive-mml><math display="block">'+MML+'</math></mjx-assistive-mml></mjx-container>'),
  ('native-mathml-display-block','<math display="block">'+MML+'</math>')]:cases.append({'name':name,'html':fixture(inner)})
 output=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page();page.route('**/*',lambda route:route.abort())
  for case in cases:
   page.set_content(case['html']);row={k:v for k,v in case.items() if k!='html'};row['source_sha256']=hashlib.sha256(case['html'].encode()).hexdigest();row['source_style_nodes']=page.evaluate("()=>[...document.querySelectorAll('mstyle[displaystyle]')].map(n=>({displaystyle:n.getAttribute('displaystyle'),scriptlevel:n.getAttribute('scriptlevel'),text:n.textContent.slice(0,100)}))");row['outputs']={}
   for name,script in scripts.items():
    r=page.evaluate('({script})=>{const fn=eval("("+script+")");return fn(document.body.firstElementChild)}',{'script':script});row['outputs'][name]={'problem':r['problem'],'errors':r['errors'],'extractor_sha256':hashlib.sha256(script.encode()).hexdigest()}
   output.append(row)
  browser.close()
 for row in output:
  for name,r in row['outputs'].items():
   if row['name'].startswith('bad-') or row['name'] in ('inline-container-with-displaystyle','native-mathml-display-block'):assert '\\displaystyle' not in r['problem'] and '$$' not in r['problem']
   if row['name']=='good-svg-title':assert '\\displaystyle' in r['problem']
   if row['name']=='display-container':assert '$$' in r['problem']
 (HERE/'reproduction.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n');print(json.dumps([{r['name']:r['outputs']} for r in output],ensure_ascii=False,indent=2))
if __name__=='__main__':main()
