import json,re,collections,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/mathml-tables-work';sys.path.insert(0,str(R/'scripts/question_capture'));from math_format import environment,cells
values=json.loads((W/'all-values.json').read_text());meta=json.loads((W/'metadata.json').read_text());out=[];counts=collections.Counter()
for r in values:
 spans=[]
 for m in re.finditer(r'\\begin\{(aligned|matrix|bmatrix|pmatrix|Bmatrix|vmatrix|Vmatrix|array)\}',r['v']):
  bounds=environment(r['v'],m.start())
  if not bounds:continue
  body_start,body_end,end=bounds;body=r['v'][body_start:body_end];columns=None
  if m[1]=='array':
   cm=re.match(r'\s*\{([^{}]*)\}',body)
   if not cm:continue
   columns=cm[1];body=body[cm.end():]
  grid=cells(body)
  if not grid or len(grid)<2:continue
  width=max(map(len,grid));counts[m[1]]+=1
  spans.append({'start':m.start(),'end':end,'body_start':body_start+(cm.end() if m[1]=='array' else 0),'body':body,'env':m[1],'columns':columns,'tex':r['v'][m.start():end],'rows':grid,'width':width})
 if spans:out.append({**r,'spans':spans,'metadata':meta.get(str(r['e']),{})})
(W/'inventory-all.json').write_text(json.dumps(out)+'\n');print('fields',len(out),'spans',sum(len(r['spans']) for r in out),'counts',dict(counts))
