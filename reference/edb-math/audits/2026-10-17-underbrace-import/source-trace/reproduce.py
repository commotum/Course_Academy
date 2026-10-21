import sys
sys.dont_write_bytecode=True
import importlib.util,json,hashlib,subprocess,datetime
from pathlib import Path
from bs4 import BeautifulSoup
R=Path('/home/jake/Developer/Course_Academy');O=Path('/tmp/underbrace-import-trace-agent')
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
archived=Path('/home/jake/Developer/MA/DATA/Lessons/280/Source/280.html')
newer=R/'reference/mathacademy/question-capture/13931643/tutorial-2620.html'
raw=BeautifulSoup(archived.read_text(),'html.parser').select_one('#step-12325')
math=next(m for m in raw.select('math') if '⏟' in m.get_text())
(O/'original-mathml.xml').write_text(math.prettify())
(O/'archived-source-step.html').write_text(str(raw))
newersoup=BeautifulSoup(newer.read_text(),'html.parser');newermath=next(m for m in newersoup.select('math') if '⏟' in m.get_text())
(O/'newer-source-mathml.xml').write_text(newermath.prettify())
lj=load('underbrace_lesson_json',Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py'))
md=load('underbrace_md',Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/5-MD/md.py'))
normalized=lj.mathml_to_text(math)
archived_json=json.loads(archived.with_suffix('.json').read_text());step=next(x for x in archived_json['lesson']['items'] if x.get('content_id')=='2620')
(O/'original-normalized-json-step.json').write_text(json.dumps(step,ensure_ascii=False,indent=2)+'\n')
rendered='\n'.join(md.render_tutorial_step(step,md.MarkdownContext(image_resolver=None)))
(O/'archived-json-rendered.md').write_text(rendered+'\n')
rows=json.loads((R/'reference/edb-math/imports/math-academy/newer-captures/tutorials.json').read_text())['occurrences'];row=next(x for x in rows if x.get('math_academy_id')==2620)
(O/'newer-import-row.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
result={'original':{'html_path':str(archived),'sha256':hashlib.sha256(archived.read_bytes()).hexdigest(),'source_mathml':str(math),'converter_output':normalized,'normalized_output_exactly_in_json':normalized in step['sections'][2]['readable_text'],'markdown_output':rendered},'newer':{'html_path':str(newer),'sha256':hashlib.sha256(newer.read_bytes()).hexdigest(),'file_mtime_utc':datetime.datetime.fromtimestamp(row['file_mtime_ns']/1e9,datetime.timezone.utc).isoformat(),'import_content':row['content'],'import_errors':row['errors']},'current_converters':{},'historical_converters':{}}
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
 context=browser.new_context();context.route('**/*',lambda route:route.abort());p=context.new_page()
 p.set_content('<div id="steps"><div class="step" id="fixture"><div class="questionWidget-text">'+str(newermath)+'</div></div></div>')
 formula='$$\n'+row['content'].split('$$\n')[3].split('\n$$')[0]+'\n$$' if False else None
 for name,path in [('question_capture','scripts/question_capture/dom.js'),('capture','capture/scripts/browser/extract.js')]:
  extracted=p.locator('#fixture').evaluate((R/path).read_text()); result['current_converters'][name]={'problem':extracted['problem'],'errors':extracted['errors'],'exact_formula_in_import':extracted['problem'].strip('$\n') in row['content']}
 for commit in ['cf225949d5','ce3d56f1c0','c6b4ab597c']:
  src=subprocess.check_output(['git','show',commit+':scripts/question_capture/dom.js'],cwd=R,text=True)
  extracted=p.locator('#fixture').evaluate(src);result['historical_converters'][commit]={'problem':extracted['problem'],'errors':extracted['errors'],'exact_formula_in_import':extracted['problem'].strip('$\n') in row['content']}
 browser.close()
(O/'reproduction.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'normalized_output_exactly_in_json':result['original']['normalized_output_exactly_in_json'],'source_munder_braces':len([m for m in math.select('munder') if len(m.find_all(recursive=False))>=2 and m.find_all(recursive=False)[1].get_text()=='⏟']),'newer':{'file_mtime_utc':result['newer']['file_mtime_utc'],'import_errors':row['errors']},'current':result['current_converters'],'historical':result['historical_converters']},ensure_ascii=False,indent=2))
