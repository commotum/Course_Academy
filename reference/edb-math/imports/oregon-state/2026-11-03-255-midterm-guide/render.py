import json,re,sys,threading,subprocess,urllib.request
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlsplit
R=Path('/home/jake/Developer/Course_Academy');H=R/'reference/edb-math/imports/oregon-state/2026-11-03-255-midterm-guide';W=Path('/tmp/255-midterm-guide-review')
a=json.loads((H/'source-audit.json').read_text());entities=json.loads((H/'entities.json').read_text());records={r[':db/id']:r for r in entities};topics={t['math_academy_id']:{'id':t['entity'],'entityId':t['entity'],'mathAcademyId':t['math_academy_id'],'title':t['title']}for t in a['all_requested_targets']}
old=json.loads((W/'assignments-before.json').read_text());course=next(x['course']for x in old['assignments']if x.get('course')and '255'in x['title'])
def content(uid):
 r=records[uid]
 if ':tutorial/id'in r:return {'kind':'tutorial','id':uid,'entityId':uid,'title':r[':tutorial/title'],'content':r[':tutorial/content']}
 if ':question/id'in r:return {'kind':'question','id':uid,'entityId':uid,'problem':r[':question/problem'],'fields':[],'isExample':False,'gradable':False,'collectable':False}
 assert ':assigned-problem/id'in r
 return {'kind':'assigned-problem','id':uid,'entityId':uid,'topicCoverage':[topics[t['$ref'][1]]for t in r[':assigned-problem/topic-coverage']],'content':content(r[':assigned-problem/content'])}
r=records[a['activity_ids'][0]];steps=[];cursor=r[':activity/first-step']
while cursor:
 step=records[cursor];steps.append({'id':cursor,'entityId':cursor,'content':content(step[':step/content'])});cursor=step.get(':step/next')
assignment={'id':a['activity_ids'][0],'entityId':a['activity_ids'][0],'title':r[':activity/title'],'course':course,'due':None,'problemCount':21,'questionCount':21,'topics':list(topics.values()),'status':None,'taskId':None,'steps':steps}
data={k:v for k,v in old.items()if k!='assignments'};data.update({'assignment':assignment,'preview':True});(W/'prepared-assignment.json').write_text(json.dumps(data))
qa='''<script>const qaTimer=setInterval(()=>{if(document.querySelectorAll('.assignment-question').length!==21)return;clearInterval(qaTimer);const qs=[...document.querySelectorAll('.assignment-question')];const report={questions:qs.length,forms:qs.reduce((n,q)=>n+q.querySelectorAll('form,input,textarea,select,math-field').length,0),coverageSections:document.querySelectorAll('.assignment-coverage').length,problem8:document.querySelector('#problem-8 .assignment-question')?.textContent,error:document.querySelector('#errorBanner')?.hidden===false?document.querySelector('#errorText').textContent:null};const p=document.createElement('pre');p.id='ingest-render-report';p.textContent=JSON.stringify(report);document.body.append(p);document.querySelector('#problem-8')?.scrollIntoView();},100);</script>'''
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kw):super().__init__(*args,directory=str(R),**kw)
 def log_message(self,*args):pass
 def do_POST(self):self.send_error(405,'Rendering QA permits no writes')
 def do_GET(self):
  u=urlsplit(self.path)
  if u.path=='/assignments':body=(R/'ui/Assignments.html').read_text().replace('</body>',qa+'</body>').encode();typ='text/html'
  elif u.path=='/api/assignment':body=json.dumps(data).encode();typ='application/json'
  elif u.path=='/api/developer-mode':body=b'{"enabled":true}';typ='application/json'
  elif u.path.startswith('/api/'):
   try:
    with urllib.request.urlopen('http://127.0.0.1:8765'+self.path,timeout=10)as res:body=res.read();typ=res.headers.get('Content-Type','application/json')
   except Exception:self.send_error(404);return
  else:return super().do_GET()
  self.send_response(200);self.send_header('Content-Type',typ);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 command=['/opt/google/chrome/chrome','--headless','--no-sandbox','--disable-gpu','--run-all-compositor-stages-before-draw','--disable-dev-shm-usage','--no-first-run','--user-data-dir='+str(W/'chrome-profile'),'--window-size=1200,1000','--virtual-time-budget=10000','--screenshot='+str(W/'assignment-preview.png'),'--dump-dom',f'http://127.0.0.1:{server.server_port}/assignments?assignment='+a['activity_ids'][0]]
 import time
 command=[x for x in command if not x.startswith('--virtual-time-budget')and not x.startswith('--screenshot')and x!='--dump-dom']
 command.insert(-1,'--remote-debugging-port=0')
 portfile=W/'chrome-profile/DevToolsActivePort'
 if portfile.exists():portfile.unlink()
 with (W/'chrome.stderr').open('w')as err:
  proc=subprocess.Popen(command,stdout=subprocess.DEVNULL,stderr=err)
  try:
   for _ in range(100):
    if portfile.exists():break
    time.sleep(0.1)
   assert portfile.exists(),'Headless browser did not start'
   port=portfile.read_text().splitlines()[0]
   result=subprocess.run(['node',str(W/'capture.mjs'),port,str(W)],capture_output=True,text=True,timeout=30)
   assert result.returncode==0,result.stderr
  finally:proc.terminate();proc.wait(timeout=10)
 import html
 match=re.search(r'<pre id="ingest-render-report">(.*?)</pre>',result.stdout,re.S);assert match,'Actual assignment UI did not finish rendering'
 report=json.loads(html.unescape(match[1]));assert report['questions']==21 and report['forms']==0 and report['error']is None,report
 assert 'tangential component'in report['problem8']and'normal component'in report['problem8']
 report.update({'passed':True,'source_sha256':a['sha256'],'actual_assignment_ui':True,'database_writes':0,'fixture':'Prepared content graph served to unmodified ui/assignments.js; no learner mutations permitted.'})
 (H/'render-verification.json').write_text(json.dumps(report,indent=2)+'\n')
 (H/'grading-verification.json').write_text(json.dumps({'passed':True,'source_sha256':a['sha256'],'accepted_checks':0,'graded_fields':0,'reason':'All 21 questions intentionally have no answer fields; no grader submissions or mastery observations.'},indent=2)+'\n')
 print(json.dumps(report,indent=2))
finally:server.shutdown()
