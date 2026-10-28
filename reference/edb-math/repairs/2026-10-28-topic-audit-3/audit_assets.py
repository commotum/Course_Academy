import hashlib,json,re,sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit,parse_qs
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT
from migrate_learner_history import connection
class Images(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,t,a):
  if t=='img':self.urls +=[v for k,v in a if k=='src' and v]
D=H/'assets';D.mkdir(exist_ok=True);db=connection();image_id=db.query('[:find ?e :where [?e :db/ident :answer.type/image]]',[],D,'image-enum',json.loads((H/'basis.json').read_text())['basis_t'])[0][0];texts={};direct=[]
attrs={':question/problem',':question/worked-solution',':tutorial/content',':answer/value',':answer/feedback',':answer-field/key',':multistep/context'}
def visit(v):
 if isinstance(v,list):
  for n in v:visit(n)
 elif isinstance(v,dict):
  e=v.get(':db/id');typ=v.get(':answer/type');image=typ==':answer.type/image' or isinstance(typ,dict)and (typ.get(':db/id')==image_id or typ.get(':db/ident')==':answer.type/image')
  for a,s in v.items():
   if a in attrs and isinstance(s,str)and e is not None:
    texts[e,a]=s
    if a==':answer/value'and image:direct.append((e,a,s))
   elif isinstance(s,(dict,list)):visit(s)
for g,f in [('group-1','current.json'),('group-2','current.json'),('group-3','snapshot.json')]:visit(json.loads((H/g/f).read_text()))
visit(json.loads((H/'scoped-contexts.json').read_text()))
refs=[]
for(e,a),s in texts.items():
 parser=Images();parser.feed(s)
 urls=parser.urls+re.findall(r'!\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)',s)
 refs +=[(e,a,u)for u in urls]
refs+=direct;records=[];files={}
for e,a,url in sorted(set(refs)):
 path=unquote(url)
 if path.startswith('/api/asset?'):path=parse_qs(urlsplit(path).query).get('path',[''])[0]
 if path.startswith('file://'):path=path[7:]
 local=image_path(path,DEFAULT_MATH_ROOT)
 rec={'entity':e,'attribute':a.lstrip(':'),'reference':url,'resolved':str(local)if local else None,'available':local is not None}
 if local:
  if str(local)not in files:
   raw=local.read_bytes();files[str(local)]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'extension':local.suffix.lower()}
  rec.update(files[str(local)])
 records.append(rec)
report={'basis_t':json.loads((H/'basis.json').read_text())['basis_t'],'snapshot_text_attributes':len(texts),'image_reference_occurrences':len(records),'unique_resolved_files':len(files),'unavailable':[r for r in records if not r['available']],'records':records};(D/'inventory.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k not in ['records','unavailable']});print('Unavailable',len(report['unavailable']));
for r in report['unavailable']:print(r)
