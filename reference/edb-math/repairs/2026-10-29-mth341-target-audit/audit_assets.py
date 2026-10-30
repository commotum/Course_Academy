"""Resolve every image used in the new audit groups without touching learner state."""
import hashlib,json,re,sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit,parse_qs
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT
class Images(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,t,a):
  if t=='img':self.urls.extend(v for k,v in a if k=='src'and v)
texts={};direct=[]
def visit(v):
 if isinstance(v,list):
  for x in v:visit(x)
 elif isinstance(v,dict):
  eid=v.get(':db/id');typ=v.get(':answer/type',{});isimage=isinstance(typ,dict)and typ.get(':db/ident')==':answer.type/image'
  for a,x in v.items():
   if a in[':question/problem',':question/worked-solution',':tutorial/content',':answer/value',':answer/feedback',':answer-field/key',':multistep/context']and isinstance(x,str)and eid is not None:
    texts[eid,a]=x
    if isimage and a==':answer/value':direct.append((eid,a,x))
   elif isinstance(x,(dict,list)):visit(x)
for name in['group-1','group-2','group-3']:visit(json.loads((H/name/'current.json').read_text()))
refs=list(direct)
for(e,a),text in texts.items():
 parser=Images();parser.feed(text);refs.extend((e,a,url)for url in parser.urls+re.findall(r'!\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)',text))
files={};records=[]
for e,a,url in sorted(set(refs)):
 path=unquote(url)
 if path.startswith('/api/asset?'):path=parse_qs(urlsplit(path).query).get('path',[''])[0]
 if path.startswith('file://'):path=path[7:]
 p=image_path(path,DEFAULT_MATH_ROOT);rec={'entity':e,'attribute':a.lstrip(':'),'reference':url,'resolved':str(p)if p else None,'available':p is not None}
 if p:
  if str(p)not in files:raw=p.read_bytes();files[str(p)]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'extension':p.suffix.lower()}
  rec.update(files[str(p)])
 records.append(rec)
report={'passed':all(r['available']for r in records),'basis_t':json.loads((H/'inventory.json').read_text())['basis_t'],'text_fields':len(texts),'image_references':len(records),'unique_files':len(files),'unavailable':[r for r in records if not r['available']],'records':records,'database_writes':0};D=H/'assets';D.mkdir(exist_ok=True);(D/'inventory.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k not in['records','unavailable']});print('Unavailable',report['unavailable'])
