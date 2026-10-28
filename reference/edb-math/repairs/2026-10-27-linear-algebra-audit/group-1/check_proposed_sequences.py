import collections,json,re,sys
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import ENV,environment,cells
D=json.loads((H/'proposed.json').read_text());topicbyq={q:t for t,k,q in D['links']};topics={t['entity']:t for t in D['topics']}
p=R/'reference/edb-math/repairs/2026-10-27-lesson-1171/audit_math.py';ns={'__file__':str(p)};s=p.read_text();ns.update(globals());exec(compile(s[s.index('def scalar'):s.index('for q in Q:')],str(p),'exec'),ns,ns);scalar=ns['scalar']
def grids(t):
 out=[]
 for m in ENV.finditer(t):
  if m.groups()[0]!='begin'or m[2]not in ['bmatrix','pmatrix','vmatrix','matrix','array']:continue
  span=environment(t,m.start())
  if not span:continue
  body=t[span[0]:span[1]];col=None
  if m[2]=='array':
   spec=re.match(r'\{([clr|]+)\}',body)
   if not spec:continue
   col=spec[1];body=body[spec.end():]
  g=cells(body)
  if not g or len({len(r)for r in g})!=1:continue
  try:mat=S.Matrix([[scalar(c)for c in r]for r in g])
  except Exception:continue
  if any(x.free_symbols for x in mat):continue
  out.append({'span':[m.start(),span[2]],'env':m[2],'columns':col,'cells':g,'matrix':mat})
 return out
out=[]
for q in D['questions']:
 sol=q.get(':question/worked-solution','');gs=grids(sol);groups=collections.defaultdict(list)
 for i,g in enumerate(gs):
  if (g['columns']and '|'in g['columns'])or (topics[topicbyq[q[':db/id']]]['ma_id']==1855 and g['matrix'].cols>1):groups[g['matrix'].shape].append((i,g))
 for shape,group in groups.items():
  if len(group)<2:continue
  base=group[0][1]['matrix'].rref()[0]
  for i,g in group:
   actual=g['matrix'].rref()[0];match=actual==base
   out.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'topic':topics[topicbyq[q[':db/id']]]['ma_id'],'matrix_index':i,'shape':list(shape),'row_equivalent_to_first':match,'cells':g['cells'],'span':g['span'],'rref':str(actual),'first_rref':str(base)})
(H/'proposed-matrix-sequence-validation.json').write_text(json.dumps(out,indent=2));print('checked',len(out),'sequences',len(set(r['entity']for r in out)),'non-equivalent',[(r['source'],r['matrix_index'],r['cells'])for r in out if not r['row_equivalent_to_first']])
