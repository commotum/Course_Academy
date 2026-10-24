import json,re,collections,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'));from math_format import environment,cells
SNAP=R/'.local/edb/mathml-tables-current.jsonl'
attrs={'tutorial/content','question/problem','question/worked-solution','multistep/context','answer/feedback','answer-field/feedback','assigned-problem/instructions','answer/value'}
values={};meta=collections.defaultdict(dict);owners=collections.defaultdict(set)
for line in SNAP.open():
 r=json.loads(line);e,a,v=r['e'],r['a'],r['v']
 if a in attrs and isinstance(v,str):values[e,a]=r
 if a in ['tutorial/math-academy-id','question/math-academy-id','topic/math-academy-id','topic/title','knowledge-point/title','knowledge-point/canonical-example','knowledge-point/question-generator','question-generator/script','answer/type','answer/id','question/id','tutorial/id']:meta[e][a]=v
 if a in ['topic/knowledge-points','knowledge-point/questions','question/answer-fields','answer-field/choices','activity/steps','step/content']:owners[v].add((e,a))
counts=collections.Counter();out=[]
for (e,a),r in values.items():
 spans=[]
 for m in re.finditer(r'\\begin\{(aligned|matrix|bmatrix|pmatrix|Bmatrix|vmatrix|Vmatrix|array)\}',r['v']):
  bounds=environment(r['v'],m.start())
  if not bounds:continue
  body_start,body_end,end=bounds;body=r['v'][body_start:body_end];grid=cells(body)
  if not grid or len(grid)<2:continue
  width=max(map(len,grid));counts[m[1]]+=1
  if m[1]=='aligned':spans.append({'start':m.start(),'end':end,'tex':r['v'][m.start():end],'rows':grid,'width':width})
 if spans:out.append({**r,'spans':spans,'metadata':meta[e]})
(H/'inventory.json').write_text(json.dumps(out,indent=2)+'\n');(H/'metadata.json').write_text(json.dumps(meta)+'\n');(H/'owners.json').write_text(json.dumps({str(k):list(v) for k,v in owners.items()})+'\n');(H/'all-values.json').write_text(json.dumps(list(values.values()))+'\n')
report={'basis_t':json.loads(SNAP.with_suffix('.manifest.json').read_text())['basis_t'],'fields_scanned':len(values),'aligned_fields':len(out),'aligned_tables':sum(len(r['spans']) for r in out),'environment_counts':dict(counts),'attributes':dict(collections.Counter(r['a'] for r in out))};(H/'inventory-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
print('x/u tables',sum(bool(re.match(r'\\begin\{aligned\}\s*x\s*&',s['tex'])) for r in out for s in r['spans']))
