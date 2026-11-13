import json,sys,subprocess,hashlib,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,loads
A=json.loads((H/'audit.json').read_text());forms=loads((H/'entities.edn').read_text());records={e[':db/id']:e for e in forms};digest=hashlib.sha256((H/'transaction.edn').read_bytes()).hexdigest();assert digest==A['sha256']
def save(n,v):(H/n).write_text(json.dumps(v,default=str,indent=2)+'\n')
db=connection();run=subprocess.run([str(R/'.local/edb/f26-missing-2026-10-21/preview'),str(H/'transaction.edn')],env=db.env,capture_output=True,text=True,timeout=120);(H/'preview.log').write_text(run.stdout+run.stderr);assert run.returncode==0,(run.stdout,run.stderr)
save('native-preview.json',{'passed':True,'sha256':digest,'basis':int((H/'preview-basis.txt').read_text()),'committed':False});print(run.stdout.strip(),flush=True)
assert len([e for e in forms if ':question/id'in e])==A['topic_count']
assert all(':question/answer-fields'not in e and ':question/worked-solution'not in e for e in forms if ':question/id'in e)
assert all(not any(k in e for k in [':answer/id',':answer-field/id'])for e in forms)
topics={t['id']:{'id':t['uuid'],'entityId':t['id'],'title':t['title']}for t in A['topics']}
def content(uid):
 e=records[uid];base={'id':uid,'entityId':uid}
 if ':tutorial/id'in e:return dict(base,kind='tutorial',title=e[':tutorial/title'],content=e[':tutorial/content'])
 if ':question/id'in e:return dict(base,kind='question',problem=e[':question/problem'],fields=[],isExample=False,gradable=False,collectable=False)
 return dict(base,kind='assigned-problem',topicCoverage=[topics[x]for x in e[':assigned-problem/topic-coverage']],content=content(e[':assigned-problem/content']))
uid=A['activity_uuid'];a=records[uid];cursor=a[':activity/first-step'];steps=[]
while cursor:
 e=records[cursor];steps.append({'id':cursor,'entityId':cursor,'content':content(e[':step/content'])});cursor=e.get(':step/next')
origin='http://127.0.0.1:8765'
with urllib.request.urlopen(origin+'/api/assignment?assignment='+A['guide_uuid'])as r:source=json.load(r)
assignment={'id':uid,'entityId':uid,'title':A['title'],'course':source['assignment']['course'],'due':A['due'],'problemCount':A['topic_count'],'questionCount':A['topic_count'],'topics':list(topics.values()),'status':None,'taskId':None,'steps':steps}
preview={**source,'assignment':assignment,'preview':True};save('preview-page.json',preview)
with sync_playwright()as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1200,'height':950});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 def route(r):
  if r.request.method not in ['GET','HEAD']:r.abort()
  elif '/api/assignment?'in r.request.url:r.fulfill(content_type='application/json',body=json.dumps(preview))
  else:r.continue_()
 page.route('**/*',route);page.goto(origin+'/assignments?assignment='+uid);page.wait_for_function('(n)=>document.querySelectorAll(".assignment-problem").length===n',arg=A['topic_count'])
 assert page.locator('.assignment-problem textarea,.assignment-problem input,.assignment-problem math-field,.assignment-problem select').count()==0
 bodylinks=page.locator('.assignment-problem a').evaluate_all('(xs)=>xs.filter(x=>x.textContent==="Open topic").map(x=>x.getAttribute("href"))')
 assert bodylinks==[origin+'/topic?topic='+t['uuid']for t in A['topics']],(len(bodylinks),bodylinks[:4],[origin+'/topic?topic='+t['uuid']for t in A['topics'][:4]],page.locator('.assignment-problem').nth(0).inner_text()[:800])
 assert page.locator('.assignment-coverage').count()==A['topic_count'];assert not errors,errors
 page.screenshot(path=str(H/'preview.png'));browser.close()
save('ui-verification.json',{'passed':True,'sha256':digest,'fieldless_questions':A['topic_count'],'topic_links_in_order':True,'no_answer_controls':True,'no_writes':True});print('Actual UI verified:',A['topic_count'],'fieldless study items with ordered topic links')
