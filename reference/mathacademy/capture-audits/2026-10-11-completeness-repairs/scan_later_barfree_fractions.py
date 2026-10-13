from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,re
R=Path(__file__).resolve().parent;rows=json.loads((R/'later-source-candidates.json').read_text());rows.append({'account':'multivariable','directory':str(R.parents[1]/'capture/multivariable/14120884/repairs/source-candidates-v1')})
class Scan(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.matches=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);cs=set(a.get('class','').split());part=self.stack[-1][1] if self.stack else 'problem'
  if cs & {'questionExplanation','questionWidget-explanation','exampleExplanation'}:part='solution'
  elif cs & {'choiceText','questionWidget-choiceText','selectList','selectListOption','questionWidget-choicesTable'}:part='fields'
  if tag=='mfrac' and re.fullmatch(r'[+-]?0(?:\.0*)?(?:px|em|ex|pt|%|in|cm|mm|rem|ch)?',a.get('linethickness','').strip(),re.I):self.matches.append({'part':part,'attributes':a})
  if tag not in {'br','hr','img','input','meta','link','wbr','col','source','area','base','embed','param','track'}:self.stack.append((tag,part))
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:self.stack=self.stack[:i];break
out=[];source_records=0;seen=set()
for row in rows:
 d=Path(row['directory']).parents[1];state=json.loads((d/'checkpoint.json').read_text());records=[x['question'] for x in state.get('presentations',{}).values() if x.get('question')]+[x['question'] for x in state.get('steps',[]) if x.get('question')]+state.get('history',{}).get('questions',[])+state.get('history',{}).get('canonical_examples',[])
 for q in records:
  source=Path(q.get('html_path',''))
  if not source.is_file() or str(source) in seen:continue
  seen.add(str(source));source_records+=1;raw=source.read_text()
  if 'linethickness' not in raw:continue
  s=Scan();s.feed(raw)
  if s.matches:out.append({'account':row['account'],'task_id':d.name,'id':q.get('math_academy_id'),'dom_id':q.get('dom_id'),'source':str(source),'source_sha256':hashlib.sha256(raw.encode()).hexdigest(),'zero_thickness_fractions':s.matches})
result={'source_records_scanned':source_records,'affected_source_records':out};(R/'later-barfree-fraction-scan.json').write_text(json.dumps(result,indent=2)+'\n');print({'source_records_scanned':source_records,'affected':[{k:v for k,v in x.items() if k not in ['source','source_sha256','zero_thickness_fractions']}|{'count':len(x['zero_thickness_fractions'])} for x in out]})
