import json,functools,http.server,threading,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path('/home/jake/Developer/Course_Academy');base=root/'reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic';after='--after'in sys.argv
fixture=(root/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
try:
 with sync_playwright()as p:
  browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1100,'height':950})
  def route(r):
   if r.request.url==origin+'/fixture':r.fulfill(body=fixture,content_type='text/html')
   elif r.request.url.startswith(origin+'/'):r.continue_()
   else:r.abort()
  page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready')
  for d in sorted(base.glob('175*')):
   qs=json.loads((d/('questions-after.json'if after else'questions.json')).read_text());out=d/('visual-after'if after else'visual-before');out.mkdir(exist_ok=True);reports=[]
   for width in [1100,390]:
    page.set_viewport_size({'width':width,'height':950})
    for q in qs:
     result=page.evaluate('''async q=>{
      MathJax.typesetClear([content]);content.replaceChildren();const article=document.createElement('article');article.className='lesson-content';const card=document.createElement('div');card.className='content-card';article.append(card);content.append(article);
      const label=document.createElement('h3');label.textContent=q[':question/math-academy-id'];card.append(label);
      card.append(render(q[':question/problem'],'prose'));
      for(const f of q[':question/answer-fields']||[]){const choices=document.createElement('div');choices.className='answer-options';for(const a of f[':answer-field/choices']||[]){let value=a[':answer/value'];const bare=a[':answer/type'][':db/ident']===':answer.type/math';choices.append(render(bare?'$'+value+'$':value,'prose'));}card.append(choices);}
      if(q[':question/worked-solution'])card.append(render(q[':question/worked-solution'],'prose'));
      await MathJax.typesetPromise([content]);await document.fonts.ready;
      return {errors:[...content.querySelectorAll('[data-mjx-error]')].map(n=>n.getAttribute('data-mjx-error')),mathBlocks:content.querySelectorAll('mjx-container').length,rawMarkers:content.textContent.includes('{{'),cardWidth:card.clientWidth,cardScrollWidth:card.scrollWidth,bodyScrollWidth:document.body.scrollWidth,images:[...content.querySelectorAll('img')].map(i=>({src:i.src,loaded:i.complete&&i.naturalWidth>0})),svgCount:content.querySelectorAll('svg').length,height:card.offsetHeight};
     }''',q)
     reports.append({'entity':q[':db/id'],'mid':q[':question/math-academy-id'],'width':width,**result})
     if width==1100 and (q[':question/math-academy-id'].startswith('e-')or q[':question/math-academy-id']in ['q-64884','q-64716','q-7814','q-93910','q-7893']):page.locator('.content-card').screenshot(path=str(out/(q[':question/math-academy-id']+'.png')))
   for l in json.loads((d/('lessons-after.json'if after else'lessons.json')).read_text()):
    for step in l[0][':activity/steps']:
     c=step[':step/content']
     if ':tutorial/content'not in c:continue
     for width in [1100,390]:
      page.set_viewport_size({'width':width,'height':950});q={':question/math-academy-id':'tutorial-'+str(c[':db/id']),':question/problem':c[':tutorial/content']};result=page.evaluate('''async q=>{MathJax.typesetClear([content]);content.replaceChildren();const card=document.createElement('div');card.className='content-card';card.append(render(q[':question/problem'],'prose'));content.append(card);await MathJax.typesetPromise([content]);await document.fonts.ready;return{errors:[...content.querySelectorAll('[data-mjx-error]')].map(n=>n.getAttribute('data-mjx-error')),mathBlocks:content.querySelectorAll('mjx-container').length,cardWidth:card.clientWidth,cardScrollWidth:card.scrollWidth};}''',q);reports.append({'entity':c[':db/id'],'width':width,'tutorial':True,**result});page.locator('.content-card').screenshot(path=str(out/(q[':question/math-academy-id']+'-'+str(width)+'.png')))
   (d/('layout-after.json'if after else'layout-before.json')).write_text(json.dumps(reports,indent=2));print(d.name,len(reports),flush=True)
  browser.close()
finally:server.shutdown();server.server_close()
