"""Read every displayed source component and derivative into exact expressions."""
import sys,re,json
from functools import lru_cache
from pathlib import Path
sys.path.insert(0,'/tmp/ca-17592186166863-deps')
import sympy as sp
from sympy.parsing.latex import parse_latex
HERE=Path(__file__).resolve().parent
x,y=sp.symbols('x y',real=True)
@lru_cache(maxsize=20000)
def parse(s):
 s=s.strip().rstrip('.,')
 s=s.replace(r'\operatorname{atan}',r'\arctan ').replace('⁡','').replace('∂',r'\partial ').replace(r'\operatorname{ln}',r'\ln').replace(r'\operatorname{arctan}',r'\arctan ')
 for f in ['sin','cos']:s=s.replace(r'\operatorname{'+f+'}', '\\'+f+' ')
 z=parse_latex(s,strict=True)
 z=z.xreplace({a:{'x':x,'y':y,'e':sp.E}.get(str(a),a) for a in z.free_symbols})
 assert z.free_symbols <= {x,y}, ('Unexpected parsed symbol',s,z)
 return z
def pairs(prompt):
 out=[]
 for text in re.findall(r'- \*\*(?:I|II|III)\.\*\* \$(.*?)\$',prompt):
  expr=text.split('=',1)[1]
  p,q=expr.split(r'\,i');q=q.rsplit(r'\,j',1)[0]
  out.append((parse(p),parse(q)))
 assert len(out)==3
 return out
if __name__=='__main__':
 s=json.loads((HERE/'source.json').read_text());rows={}
 for q in s['record'][':knowledge-point/questions']:
  ps=pairs(q[':question/problem']);key=q[':question/math-academy-id'];fields=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']);mask=[]
  for f,(p,t) in zip(fields,ps):
   eq=sp.simplify(sp.diff(p,y)-sp.diff(t,x))==0
   assert f[':answer-field/correct'][':answer/value']==str(eq).lower(),(key,p,t)
   mask.append(eq)
  rows[key]={'source_db_id':q[':db/id'],'pairs':[[str(p),str(t)] for p,t in ps],'truth':mask,'component_tex':[[sp.latex(p),sp.latex(t)] for p,t in ps],'derivatives':[[str(sp.diff(p,y)),str(sp.diff(t,x))] for p,t in ps]}
 (HERE/'source-components.json').write_text(json.dumps(rows,indent=2)+'\n')
 print('All',len(rows),'source triples parsed and checked against exact derivatives and all 33 checkbox keys.')
