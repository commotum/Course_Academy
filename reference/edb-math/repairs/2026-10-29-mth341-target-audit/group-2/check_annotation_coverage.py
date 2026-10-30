import ast,json,re,sys
import sympy as sp
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from algebra import matrices,scalar,symbols
code=ast.parse((H/'family_audit.py').read_text());exec(compile(ast.Module(body=[n for n in code.body if isinstance(n,ast.FunctionDef)and n.name in['normalized_ops','operation']],type_ignores=[]),'helpers','exec'))
S=json.loads((H/'proposed-snapshot.json').read_text());topic={q:t for t,k,q in S['links']};checks=[];unparsed=[]
for q in S['questions']:
 if topic[q[':db/id']]not in[17592186048920,17592186050900]:continue
 for attr in[':question/problem',':question/worked-solution']:
  text=q[attr];ms=matrices(text)
  for u,v in zip(ms,ms[1:]):
   if u['matrix'].shape!=v['matrix'].shape:continue
   between=text[u['end']:v['start']];n=normalized_ops(between)
   if not re.search(r'R_\d+\s*&?\s*(?::=|↔|\\leftrightarrow)',n):continue
   b,op=operation(between,u['matrix'])
   if b is None:unparsed.append({'question':q[':db/id'],'attribute':attr,'annotation':between})
   else:checks.append({'question':q[':db/id'],'attribute':attr,'literal_operation':op,'exact_next_matrix_matches':b==v['matrix']})
assert not unparsed,unparsed;assert all(r['exact_next_matrix_matches']for r in checks),[r for r in checks if not r['exact_next_matrix_matches']]
(H/'annotation-coverage-verification.json').write_text(json.dumps({'passed':True,'literal_annotation_checks':len(checks),'checks':checks,'unparsed_annotations':unparsed},indent=2)+'\n');print('Every',len(checks),'literal annotation parsed and matched its exact next matrix')
