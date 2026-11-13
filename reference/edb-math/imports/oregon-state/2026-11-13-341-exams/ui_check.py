import json,sys,urllib.request,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4];a=json.loads((H/'source-audit.json').read_text());records={e[':db/id']:e for e in json.loads((H/'entities.json').read_text())};base='http://127.0.0.1:8765'
with urllib.request.urlopen(base+'/api/assignment?assignment=67a9d64d-9f6b-5276-b3ba-06d503c39c11')as res:source=json.load(res)
topics={t['math_academy_id']:{'id':t['entity'],'entityId':t['entity'],'mathAcademyId':t['math_academy_id'],'title':t['title']}for t in a['all_requested_targets']}
def answer(uid):
 e=records[uid];return {'id':uid,'entityId':uid,'type':e[':answer/type'].split('/')[-1],'value':e[':answer/value'],'feedback':e.get(':answer/feedback','')}
pages={}
for act in a['activities']:
 itemmap={e[':task-item/content']:e for e in records.values()if ':task-item/id'in e}
 def content(uid):
  e=records[uid];b={'id':uid,'entityId':uid}
  if ':tutorial/id'in e:return dict(b,kind='tutorial',title=e[':tutorial/title'],content=e[':tutorial/content'])
  if ':assigned-problem/id'in e:return dict(b,kind='assigned-problem',topicCoverage=[topics[t['$ref'][1]]for t in e[':assigned-problem/topic-coverage']],content=content(e[':assigned-problem/content']))
  item=itemmap[uid];fs=[]
  for fid in e[':question/answer-fields']:
   f=records[fid];kind=f[':answer-field/type'].split('/')[-1];response=next(x for x in item[':task-item/responses']if x in f[':answer-field/choices']);resp={**answer(response),'choiceId':response}
   fs.append({'id':fid,'entityId':fid,'key':f[':answer-field/key'],'type':kind,'answerType':records[f[':answer-field/correct']][':answer/type'].split('/')[-1],'choices':[answer(x)for x in f[':answer-field/choices']]if kind=='radio'else[],'correctAnswer':answer(f[':answer-field/correct']),'response':resp})
  return dict(b,kind='question',problem=e[':question/problem'],fields=fs,isExample=False,gradable=all(f['type']!='free'for f in fs),collectable=True,status=item[':task-item/status'].split('/')[-1],itemId=item[':db/id'],solution=e.get(':question/worked-solution',''))
 uid=act['activity_id'];e=records[uid];steps=[];cursor=e[':activity/first-step']
 while cursor:
  st=records[cursor];steps.append({'id':cursor,'entityId':cursor,'content':content(st[':step/content'])});cursor=st.get(':step/next')
 assignment={'id':uid,'entityId':uid,'title':e[':activity/title'],'course':source['assignment']['course'],'due':act['due'],'problemCount':len(act['problems']),'questionCount':len(act['problems']),'topics':list(topics.values()),'status':'completed','taskId':act['task_uuid'],'steps':steps}
 pages[uid]={**source,'assignment':assignment,'preview':True}
with sync_playwright()as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1200,'height':950});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 def route(r):
  if r.request.method not in['GET','HEAD']:r.abort()
  elif '/api/assignment?'in r.request.url:
   from urllib.parse import urlsplit,parse_qs
   uid=parse_qs(urlsplit(r.request.url).query)['assignment'][0];r.fulfill(content_type='application/json',body=json.dumps(pages[uid]))
  else:r.continue_()
 page.route('**/*',route);reports=[]
 for act in a['activities']:
  uid=act['activity_id'];page.goto(base+'/assignments?assignment='+uid);page.wait_for_function('(n)=>document.querySelectorAll(".assignment-problem").length===n',arg=len(act['problems']))
  expected=[records[r][':answer/value']for x in act['historical_responses']for r in x['response_answer_ids']if records[r][':answer/type']==':answer.type/text'and any(records[f][':answer-field/type']==':answer-field.type/free'for f in records[x['question_uuid']][':question/answer-fields'])]
  got=page.locator('.assignment-problem textarea').evaluate_all('(xs)=>xs.map(x=>x.value)');assert got==expected,(got,expected)
  radio_expected=sum(records[f][':answer-field/type']==':answer-field.type/radio'for x in act['historical_responses']for f in records[x['question_uuid']][':question/answer-fields'])
  assert page.locator('.assignment-problem input[type=radio]:checked').count()==radio_expected
  assert not errors,errors;page.locator('.assignment-problem').nth(2).screenshot(path=str(H/('preview-'+uid+'.png')));reports.append({'activity':uid,'questions':len(act['problems']),'original_written_responses':len(got),'selected_radio_responses':radio_expected,'passed':True})
 browser.close()
(H/'ui-verification.json').write_text(json.dumps({'passed':True,'sha256':a['sha256'],'activities':reports,'no_writes':True},indent=2)+'\n');print(json.dumps(reports))
