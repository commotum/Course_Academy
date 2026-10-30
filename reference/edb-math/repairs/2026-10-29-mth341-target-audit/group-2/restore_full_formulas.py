import ast,collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path[:0]=[str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-26-mixed-math-titles')]
from reconstruct import SourceRenderer,reconstruct
from question_capture.math_format import MATH,ENV,environment,cells,normalize_source_tex
oldpath=R/'reference/edb-math/repairs/2026-10-29-q17592186604616/full-review/restore_colors.py';code=ast.parse(oldpath.read_text());exec(compile(ast.Module(body=[n for n in code.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),str(oldpath),'exec'))
base=canonical
def canonical(v):
 v=v.replace(r'\det','det');v=re.sub(r'\\begin\{array\}\s*\{[^{}]+\}',r'\\begin{matrix}',v);v=v.replace(r'\end{array}',r'\end{matrix}').replace('bmatrix','matrix');v=re.sub(r'\\(?:phantom)\{[^{}]*\}','',v);v=base(v);return re.sub(r'[\[\]|]','',v)
S=json.loads((H/'current.json').read_text());objs={q[':question/math-academy-id']:q for q in S['questions']};objs.update({'tutorial:'+str(c[':tutorial/math-academy-id']):c for c in S['contents']if ':tutorial/content'in c});srcs=collections.defaultdict(list)
for r in json.loads((H/'source-inventory.json').read_text()):srcs[r['identity'],r['attribute']].append(r)
changes={(p['entity'],':'+p['attribute']):p['after']for name in['decoration-proposals','layout-proposals','completion-proposals']for p in json.loads((H/(name+'.json')).read_text())};proposals=[];evidence=[]
for(mid,attr),rows in srcs.items():
 o=objs[mid];old=changes.get((o[':db/id'],':'+attr),o.get(':'+attr,''))
 if not old:continue
 sf=collections.defaultdict(list)
 for r in rows:
  try:fs=source_formulas(r['html'])
  except Exception:continue
  for v in fs:
   if any(s in v for s in[r'\mathbf',r'\mathbfit',r'\mathit',r'\mathrm',r'\color',r'\bbox']):sf[canonical(v)].append((v,r['path']))
 edits=[]
 for m in MATH.finditer(old):
  edge=2 if m[0].startswith(('$$',r'\(',r'\['))else 1;v=m[0][edge:-edge];matches=sf.get(canonical(v),[])
  if not matches:continue
  unique={x[0]for x in matches}
  # Conflicting source decoration variants are retained for explicit review.
  if len(unique)!=1:continue
  new=matches[0][0]
  if new!=v:edits.append((m.start()+edge,m.end()-edge,new,matches[0][1]))
 new=old
 for a,b,v,p in reversed(edits):new=new[:a]+v+new[b:]
 if new!=old:
  proposals.append({'entity':o[':db/id'],'attribute':attr,'before':old,'after':new,'reason':'Restore complete archived formula fonts and emphasis only after matching every normalized mathematical token; this also preserves source augmented-matrix separators.'});evidence.append({'entity':o[':db/id'],'identity':mid,'attribute':attr,'restored_formulas':len(edits),'sources':sorted({p for a,b,v,p in edits})})
(H/'full-formula-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n');(H/'full-formula-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print('Full formula source restorations',len(proposals),'formulas',sum(r['restored_formulas']for r in evidence))
