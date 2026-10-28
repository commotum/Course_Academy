import collections,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;ns={'__file__':str(H/'propose_format.py')};exec((H/'propose_format.py').read_text().split('P=[]')[0],ns);neutral=ns['neutral'];diff=json.loads((H/'source-differences.json').read_text());out=[]
for d in diff:
 if d['attribute']=='answer/value':continue
 s=d.get('source');ms=d.get('math',[])
 if not s or len(ms)!=len(s['formulas']):continue
 bad=[]
 for i,(a,b)in enumerate(zip(ms,s['formulas'])):
  if neutral(a)!=neutral(b):bad.append({'i':i,'current':a,'source':b})
 if bad:out.append({'entity':d['entity'],'identity':d['identity'],'attribute':d['attribute'],'path':s['path'],'differences':bad})
(H/'semantic-candidates.json').write_text(json.dumps(out,indent=2)+'\n');print(len(out),'fields',sum(len(x['differences'])for x in out),'formula pairs')
for i,d in enumerate(out):print(i,d['identity'],d['attribute'],[(v['current'][:160],v['source'][:160])for v in d['differences']][:3])
