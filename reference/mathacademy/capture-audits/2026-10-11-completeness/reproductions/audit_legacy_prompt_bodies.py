import json
from pathlib import Path
from bs4 import BeautifulSoup
root=Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture');findings=[]
for path in sorted(root.glob('[0-9]*/content.json')):
 c=json.loads(path.read_text());d=path.parent;s=json.loads((d/'state.json').read_text()) if (d/'state.json').is_file() else {}
 for q in c.get('questions',[]):
  mid=q['math_academy_id'];before=s.get('questions',{}).get(mid,{}).get('before')
  if not before:
   f=d/(mid+'-before.json');before=json.loads(f.read_text()) if f.is_file() else {}
  html=before.get('html','')
  if 'questionWidget-body' not in html:continue
  dom=BeautifulSoup(html,'html.parser');body=dom.select_one('.questionWidget-body')
  if body and body.get_text(strip=True) and not body.find_parent(class_='questionWidget-text'):
   findings.append({'task_id':d.name,'id':mid,'body_text':body.get_text(' ',strip=True),'problem':q.get('problem'),
                    'field_count':len(q.get('answer_fields',[])),'placeholder_count':str(q.get('problem','')).count('{{field-'),
                    'source_file':str(d/(mid+'-before.json'))})
Path('/tmp/legacy-prompt-body-findings.json').write_text(json.dumps({'findings':findings},indent=2)+'\n');print('LEGACY LIVE BODY FINDINGS',len(findings),flush=True)
