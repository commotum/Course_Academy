import copy,json,re,sys,types
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import normalize_tex,environment,cells
parser=types.ModuleType('matrix_scalar');exec((R/'generate/runs/current/vector-math-parser.py').read_text().replace('[tuvxyzijke]','[A-Za-z]'),parser.__dict__);parser.locals_.update({c:s.Symbol(c,real=True)for c in 'abcdfghlmnopqrswABCDEFGHIJKLMNOPQRSTUVWXYZ'})
def scalar(v):return parser.scalar(v.strip().strip('$').replace(r'\dfrac',r'\frac').replace(r'\tfrac',r'\frac'))
def solve(q,unknown):
 p=normalize_tex(q[':question/problem']);match=re.search(r'\\begin\{(?:bmatrix|vmatrix|matrix)\}',p);assert match,(q[':db/id'],'no matrix');span=environment(p,match.start());rows=cells(p[span[0]:span[1]]);assert len(rows)==2 and all(len(row)==2 and all(cell.strip()for cell in row)for row in rows);m=s.Matrix([[scalar(c)for c in row]for row in rows]);det=s.factor(m.det());target=det;equation=None
 if unknown:
  mt=re.search(r'(?:\\text\{det\}|\\det|det)\s*\([^)]*\)\s*=\s*([^$,\n]+)',p);assert mt,(q[':db/id'],p);equation=scalar(mt[1]);variables=list(det.free_symbols);assert len(variables)==1;roots=s.solve(s.Eq(det,equation),variables[0]);assert len(roots)==1,(q[':db/id'],roots);target=roots[0]
 return rows,det,target,equation

def main():
 qs=json.loads((H/('final-questions.json'if(H/'final-questions.json').exists()else'questions.json')).read_text());topic=json.loads((H/'topic.json').read_text());unknown={v[':db/id']for kp in topic[':topic/knowledge-points']if kp[':db/id']==17592186059750 for a in [':knowledge-point/questions',':knowledge-point/canonical-example']for v in(kp[a]if isinstance(kp[a],list)else[kp[a]])};report=[]
 for q in qs:
  rows,det,target,eq=solve(q,q[':db/id']in unknown);r={'entity':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'matrix':rows,'determinant':str(det),'expected':str(target),'determinant_equation':str(eq)if eq is not None else None,'fields':[]}
  for f in q.get(':question/answer-fields',[]):
   matching=[a for a in f[':answer-field/choices']if s.simplify(scalar(a[':answer/value'].split('=')[-1])-target)==0];assert len(matching)==1,(q[':db/id'],'ambiguous or wrong bank');actual=f.get(':answer-field/correct');assert actual is None or actual[':db/id']==matching[0][':db/id'],(q[':db/id'],'wrong correct');r['fields'].append({'field':f[':db/id'],'correct':matching[0][':db/id'],'value':matching[0][':answer/value'],'missing_correct':actual is None})
  report.append(r)
 (H/('final-independent-math.json'if(H/'final-questions.json').exists()else'independent-math.json')).write_text(json.dumps(report,indent=2)+'\n');print('Independent exact determinant and canonical-answer checks passed:',len(report))
if __name__=='__main__':main()
