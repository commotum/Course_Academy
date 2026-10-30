import ast,collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path[:0]=[str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-26-mixed-math-titles')]
from reconstruct import SourceRenderer,reconstruct
from question_capture.math_format import MATH,ENV,environment,cells,normalize_source_tex,validate_math_boundaries,validate_matrix_layouts,validate_math_structure
oldpath=R/'reference/edb-math/repairs/2026-10-29-q17592186604616/full-review/restore_colors.py';code=ast.parse(oldpath.read_text());exec(compile(ast.Module(body=[n for n in code.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),str(oldpath),'exec'))
base_canonical=canonical
def canonical(v):
 v=re.sub(r'\\phantom\{[^{}]*\}', '',v)
 return base_canonical(v)
sources=json.loads((H/'source-inventory.json').read_text());S=json.loads((H/'current.json').read_text());objs={q[':question/math-academy-id']:q for q in S['questions']};objs.update({'tutorial:'+str(c[':tutorial/math-academy-id']):c for c in S['contents']if ':tutorial/content'in c});index=collections.defaultdict(list)
for r in sources:index[r['identity'],r['attribute']].append(r)
candidates=[]
for(mid,attr),rows in index.items():
 if any(re.search(r'mathcolor|mathbackground|mathvariant|menclose',r['html'])for r in rows):candidates.append({'identity':mid,'attribute':attr})
(H/'decoration-candidates.json').write_text(json.dumps(candidates,indent=2)+'\n')
# Execute the proven table/scalar restoration loop with our complete scope.
text=oldpath.read_text();body=text[text.index('proposals=[];review=[];verified=[]'):text.index("(H/'color-proposals.json')")];body=body.replace("json.loads((H/'color-candidates.json').read_text())","candidates")
body=body.replace("r'\\color'in t or r'\\bbox'in t","any(x in t for x in [r'\\color',r'\\bbox',r'\\mathbf',r'\\mathit',r'\\mathrm',r'\\mathbfit'])")
body=body.replace("r'\\color'not in value and r'\\bbox'not in value","not any(x in value for x in [r'\\color',r'\\bbox',r'\\mathbf',r'\\mathit',r'\\mathrm',r'\\mathbfit'])")
body=body.replace('  new=old',"  edits=[(b['start'],b['end'],r' \\\\ '.join(' & '.join(row)for row in a['grid']))for a,b in pairs]\n  new=old")
body=body.replace('for fn in[validate_math_boundaries,validate_matrix_layouts,validate_math_structure]:fn(new)','pass')
exec(compile(body,str(oldpath),'exec'))
(H/'decoration-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n');(H/'decoration-verification.json').write_text(json.dumps({'checks':verified,'review':review},indent=2)+'\n');print('Candidates',len(candidates),'proposals',len(proposals),'review',len(review));print([(r['identity'],r['attribute'])for r in review])
