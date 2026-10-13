from html.parser import HTMLParser
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
rows=json.loads((R/'later-source-candidates.json').read_text());rows.append({'account':'multivariable','directory':str(R.parents[1]/'capture/multivariable/14120884/repairs/source-candidates-v1')})
class Scan(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.tables=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);cs=set(a.get('class','').split());skip=(self.stack and self.stack[-1][1]) or bool(cs & {'questionWidget-choicesTable','selectList','selectListOptions','questionWidget-header','questionHeader','answerDetails','studentAnswer','studentAnswerHeader'}) or tag=='mjx-assistive-mml'
  table_index=None
  if tag=='table' and not skip:
   parent=next((i for t,s,i in reversed(self.stack) if t=='table' and i is not None),None)
   table_index=len(self.tables);self.tables.append({'class':a.get('class'),'nested':parent is not None,'spans':[]})
   if parent is not None:self.tables[parent]['nested']=True
  if tag in ('td','th') and not skip:
   index=next((i for t,s,i in reversed(self.stack) if t=='table' and i is not None),None)
   if index is not None:
    spans={k:v for k,v in a.items() if k in ('rowspan','colspan') and v!='1'}
    if spans:self.tables[index]['spans'].append(spans)
  if tag not in {'br','hr','img','input','meta','link','wbr','col','source','area','base','embed','param','track'}:self.stack.append((tag,skip,table_index))
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:self.stack=self.stack[:i];break
out=[];records=0
for row in rows:
 d=Path(row['directory']).parents[1];c=json.loads((d/'content.json').read_text())
 for q in c.get('questions',[])+c.get('canonical_examples',[]):
  records+=1;source=Path(q.get('html_path',''))
  if not source.is_file():continue
  raw=source.read_text()
  if '<table' not in raw:continue
  s=Scan();s.feed(raw);complex_tables=[x for x in s.tables if x['nested'] or x['spans']]
  if complex_tables:out.append({'account':row['account'],'task_id':d.name,'id':q.get('math_academy_id'),'source':str(source),'source_sha256':hashlib.sha256(raw.encode()).hexdigest(),'tables':complex_tables,'errors':q.get('errors',[])})
result={'records_scanned':records,'complex_authored_table_records':out};(R/'later-complex-table-scan.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
