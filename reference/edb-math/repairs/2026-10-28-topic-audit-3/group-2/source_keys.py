import json,sys,re
from pathlib import Path
from bs4 import BeautifulSoup
from propose_controls import norm
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
s=(H/'import_historical_question_content.py').read_text();ns={'__file__':str(R/'scripts/import_historical_question_content.py')};exec(compile(s.split('def prepare():')[0],str(H/'import_historical_question_content.py'),'exec'),ns)
Q={q.get(':question/math-academy-id'):q for q in json.loads((H/'current.json').read_text())['questions']};out=[];fails=[]
for source in json.loads((H/'sources.json').read_text()):
 if source['attribute']!='question/problem'or not source['path'].endswith('-after.json')or'selectList'not in source['html']:continue
 q=Q[source['identity']];r=ns['Renderer'](None)
 try:text=r.text(BeautifulSoup(source['html'],'html.parser'),True)
 except Exception as ex:fails.append({'identity':source['identity'],'source':source['path'],'error':str(ex)});continue
 for sf in r.fields:
  if sf['type']!='select':continue
  fs=[f for f in q[':question/answer-fields']if f[':answer-field/key']==sf['key']]
  if len(fs)!=1:continue
  f=fs[0];matches=[a for a in f[':answer-field/choices']if norm(a[':answer/value'])==norm(sf['correct_value'])]
  old=f.get(':answer-field/correct',{})
  if old and norm(old[':answer/value'])==norm(sf['correct_value']):continue
  if not matches:fails.append({'identity':source['identity'],'source':source['path'],'field':f[':db/id'],'error':'correct source value absent from existing bank','source_value':sf['correct_value']});continue
  target=matches[0]
  out.append({'entity':f[':db/id'],'attribute':'answer-field/correct','before':old.get(':db/id'),'after':target[':db/id'],'reason':'Recover source-observed verified correct selection mapped by exact DOM control index; independently verify mathematical role before approval','evidence':{'question':q[':db/id'],'identity':source['identity'],'source':source['path'],'key':sf['key'],'source_value':sf['correct_value'],'before_value':old.get(':answer/value'),'after_value':target[':answer/value'],'problem':text},'confidence':'pending-independent-math'})
(H/'source-key-candidates.json').write_text(json.dumps(out,indent=2)+'\n');(H/'source-key-failures.json').write_text(json.dumps(fails,indent=2)+'\n');print('wrong source keys',len(out),'errors',len(fails))
for x in out:print(x['evidence']['identity'],x['evidence']['key'],x['evidence']['before_value'],'->',x['evidence']['after_value'])
