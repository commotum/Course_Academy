import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/matrix-layout-2026-10-26';sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import _matrix_layouts,ENV,environment,cells
meta={int(k):v for k,v in json.loads((W/'metadata.json').read_text()).items()};parents={int(k):v for k,v in json.loads((W/'parents.json').read_text()).items()}
def context(e):
 seen=set();todo=[e];out=[]
 for depth in range(7):
  nxt=[]
  for x in todo:
   if x in seen:continue
   seen.add(x);m=meta.get(x,{})
   if any(a in m for a in ['topic/title','knowledge-point/title','question/math-academy-id','tutorial/math-academy-id']):out.append({'entity':x,**{a:v for a,v in m.items()if not a.endswith('/script')}})
   nxt.extend(p for p,a in parents.get(x,[]))
  todo=nxt
 return out
blocks=[];shapes=collections.Counter();topics=set();suspect=[]
for d in json.loads((H/'candidates.json').read_text()):
 ctx=context(d['e']);topics|={str(x['topic/math-academy-id'])for x in ctx if'topic/math-academy-id'in x}
 for m in ENV.finditer(d['v']):
  if m[1]!='begin'or m[2]not in ('aligned','matrix'):continue
  b=environment(d['v'],m.start())
  if not b:continue
  l=re.search(r'(?:\\left\s*)?([\[|(])\s*$',d['v'][:m.start()]);r=re.match(r'\s*(?:\\right\s*)?([\]|)])',d['v'][b[2]:])
  if not l or not r:continue
  old=d['v'][l.start():b[2]+r.end()];new=_matrix_layouts(old)
  if new==old:continue
  grid=cells(d['v'][b[0]:b[1]]);width=max(map(len,grid));shape=(l[1],m[2],len(grid),tuple(map(len,grid)));shapes[str(shape)]+=1
  z={'e':d['e'],'a':d['a'],'old':old,'new':new,'rows':grid,'left_context':d['v'][max(0,l.start()-100):l.start()],'right_context':d['v'][b[2]+r.end():b[2]+r.end()+80],'context':ctx,'span':[l.start(),b[2]+r.end()]};blocks.append(z)
  if len(grid)==1 or width==1 or any(not c.strip() for row in grid for c in row)or re.search(r'\\(?:text|underbrace|overbrace|cdots|vdots|ddots|hline|multicolumn|hdotsfor)|[=<>]|\\(?:to|Rightarrow|approx|leq|geq)',old):suspect.append(z)
(H/'blocks.json').write_text(json.dumps(blocks,indent=2)+'\n');(H/'individual-review-candidates.json').write_text(json.dumps(suspect,indent=2)+'\n')
print('fields',len(json.loads((H/'candidates.json').read_text())),'blocks',len(blocks),'topics',len(topics),'extra-review',len(suspect));print('shapes',json.dumps(shapes,indent=2))
for r in suspect[:55]:print(r['e'],r['a'],[x.get('topic/title')for x in r['context']if'topic/title'in x],r['old'][:700])
print('RESIDUALS')
for d in json.loads((H/'residual.json').read_text()):print(d['e'],d['a'],repr(d.get('left','')),repr(d.get('right','')),d.get('tex',d.get('v',''))[:850])
