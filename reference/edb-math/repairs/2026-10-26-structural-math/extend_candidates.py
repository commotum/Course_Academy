import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/structural-math-2026-10-26';sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import ENV,environment,cells
out=[];existing=json.loads((H/'table-candidates.json').read_text());keys={(d['e'],d['a'],d['span'][0])for d in existing}
for d in json.loads((W/'values.json').read_text()):
 v=d['v']
 for m in ENV.finditer(v):
  if m[1]!='begin'or m[2]not in ('bmatrix','pmatrix','vmatrix','matrix'):continue
  b=environment(v,m.start());g=cells(v[b[0]:b[1]])if b else None
  if not g:continue
  non_square=m[2]=='vmatrix'and(len(g)!=max(map(len,g)))
  relations=any(re.search(r'(?<!\\)[=<>]',c)for row in g for c in row)
  if(non_square or relations)and(d['e'],d['a'],m.start())not in keys:
   out.append({'e':d['e'],'a':d['a'],'env':m[2],'span':[m.start(),b[2]],'rows':g,'ragged':len({len(r)for r in g})>1,'non_square_determinant':non_square,'relation_in_matrix_cell':relations,'left':v[max(0,m.start()-90):m.start()],'right':v[b[2]:b[2]+90]})
(H/'additional-matrix-candidates.json').write_text(json.dumps(out,indent=2)+'\n');(H/'table-candidates.json').write_text(json.dumps(existing+out,indent=2)+'\n');print('additional',len(out),'fields',len({(d['e'],d['a'])for d in out}));print(collections.Counter((d['env'],len(d['rows']),max(map(len,d['rows'])))for d in out))
for d in out[:22]:print(d['e'],d['a'],str(d['rows'])[:450])
