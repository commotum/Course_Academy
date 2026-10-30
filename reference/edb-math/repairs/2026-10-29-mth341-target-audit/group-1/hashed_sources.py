"""Include hashed historical observations in the source audit, never mutate source captures."""
import json,re,sys,collections
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH
s=(H/'audit.py').read_text();ns={'__file__':str(H/'audit.py')};exec(s[:s.index('paths=[]')],ns);parts=ns['parts'];sources=ns['sources'];slim=ns['slim'];records=json.loads((H/'sources.json').read_text());paths=json.loads((H/'hashed-history-sources.json').read_text());seen=set()
for ident,path in paths:
 if path in seen:continue
 seen.add(path);p=R/path;data=json.loads(p.read_text());html=data.get('html')or data.get('raw_html')
 if html:parts(BeautifulSoup(slim(html),'html.parser'),ident,p)
old={(x['identity'],x['attribute'],x['path'],x['html'])for x in records}
for(i,a),vs in sources.items():
 for v in vs:
  if(i,a,v['path'],v['html'])not in old:records.append({'identity':i,'attribute':a,**v})
(H/'sources.json').write_text(json.dumps(records,indent=2)+'\n');print('Source fields',len(records),'hashed observations',len(seen))
