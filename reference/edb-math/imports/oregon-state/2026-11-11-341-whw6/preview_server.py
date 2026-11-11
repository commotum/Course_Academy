import json,urllib.request
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlsplit,parse_qs
R=Path('/home/jake/Developer/Course_Academy');H=R/'reference/edb-math/imports/oregon-state/2026-11-11-341-whw6'
a=json.loads((H/'source-audit.json').read_text());records={r[':db/id']:r for r in json.loads((H/'entities.json').read_text())};topics={t['math_academy_id']:{'id':t['entity'],'entityId':t['entity'],'mathAcademyId':t['math_academy_id'],'title':t['title']}for t in a['all_requested_targets']}
with urllib.request.urlopen('http://127.0.0.1:8765/api/assignments',timeout=20)as res:old=json.load(res)
courses={code:next(x['course']for x in old['assignments']if x.get('course')and code in x['title'])for code in ['341']}
def answer(uid):
 r=records[uid];return {'id':uid,'entityId':uid,'type':r[':answer/type'].split('/')[-1],'value':r[':answer/value']}
def steps(uid,prefix):
 r=records[uid];out=[];cursor=r[':'+prefix+'/first-step']
 while cursor:
  st=records[cursor];out.append({'id':cursor,'entityId':cursor,'content':content(st[':step/content'])});cursor=st.get(':step/next')
 return out
def content(uid):
 r=records[uid];b={'id':uid,'entityId':uid}
 if ':tutorial/id'in r:return dict(b,kind='tutorial',title=r[':tutorial/title'],content=r[':tutorial/content'])
 if ':multistep/id'in r:return dict(b,kind='multistep',context=r.get(':multistep/context',''),steps=steps(uid,'multistep'))
 if ':question/id'in r:
  fs=[]
  for fid in r[':question/answer-fields']:
   f=records[fid];ans=answer(f[':answer-field/correct']);fs.append({'id':fid,'entityId':fid,'key':f[':answer-field/key'],'type':f[':answer-field/type'].split('/')[-1],'answerType':ans['type'],'choices':[answer(aid)for aid in f[':answer-field/choices']]if f[':answer-field/type'].endswith('/checkbox')else[],'correctAnswer':ans})
  return dict(b,kind='question',problem=r[':question/problem'],fields=fs,isExample=False,gradable=any(f['type']!='free'for f in fs),collectable=True,solution=r.get(':question/worked-solution',''))
 assert ':assigned-problem/id'in r
 return dict(b,kind='assigned-problem',topicCoverage=[topics[t['$ref'][1]]for t in r[':assigned-problem/topic-coverage']],content=content(r[':assigned-problem/content']))
pages={}
for activity in a['activities']:
 uid=activity['activity_id'];r=records[uid];course=activity['source'].split('/')[1];ps=activity['problems'];used={t for p in ps for t in p['topics']}
 assignment={'id':uid,'entityId':uid,'title':r[':activity/title'],'course':courses[course],'due':r[':activity/due']['$inst'],'problemCount':len(ps),'questionCount':sum(len(p['quizzes'])for p in ps),'topics':[topics[t]for t in used],'status':None,'taskId':None,'steps':steps(uid,'activity')}
 pages[uid]={**{k:v for k,v in old.items()if k!='assignments'},'assignment':assignment,'preview':True}
Path('/tmp/ingest-whw6/prepared-assignments.json').write_text(json.dumps(pages))
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kw):super().__init__(*args,directory=str(R),**kw)
 def log_message(self,*args):pass
 def do_POST(self):self.send_error(405,'Read-only import preview')
 def do_GET(self):
  u=urlsplit(self.path)
  if u.path=='/assignments':body=(R/'ui/Assignments.html').read_bytes();typ='text/html'
  elif u.path=='/api/assignment':body=json.dumps(pages[parse_qs(u.query)['assignment'][0]]).encode();typ='application/json'
  elif u.path=='/api/developer-mode':body=b'{"enabled":true}';typ='application/json'
  elif u.path.startswith('/api/'):
   try:
    with urllib.request.urlopen('http://127.0.0.1:8765'+self.path,timeout=15)as res:body=res.read();typ=res.headers.get('Content-Type','application/json')
   except Exception:self.send_error(404);return
  else:return super().do_GET()
  self.send_response(200);self.send_header('Content-Type',typ);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
server=ThreadingHTTPServer(('127.0.0.1',8778),Handler);print('Read-only QA pages:',flush=True)
for uid,d in pages.items():print(d['assignment']['title'],d['assignment']['questionCount'],'http://127.0.0.1:8778/assignments?assignment='+uid,flush=True)
server.serve_forever()
