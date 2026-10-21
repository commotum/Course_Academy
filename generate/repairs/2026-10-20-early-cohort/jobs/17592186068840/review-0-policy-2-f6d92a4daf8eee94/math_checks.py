import json,sys,re
from pathlib import Path
sys.path.insert(0,'/home/jake/.cache/uv/wheels-v5/pypi/lark/1.2.2-py3-none-any')
import sympy as s
from sympy.parsing.latex import parse_latex
E=Path(__file__).resolve().parent
x,C,K=s.symbols('x C K',real=True)
def parse(t):
 t=t.replace('\u2061','').replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{ln}',r'\ln').replace(r'\operatorname{tan}',r'\tan').replace(r'\operatorname{sec}',r'\sec').replace(r'\operatorname{arcsin}',r'\arcsin')
 v=parse_latex(t,backend='lark');return v.xreplace({z:{'x':x,'C':C,'K':K}.get(z.name,z) for z in v.free_symbols})
rows=json.load(open(E/'independent-records.json'))+json.load(open(E/'batch-records.json'))+json.load(open(E/'counterfactual-records.json'))
report=[]
for i,r in enumerate(rows):
 q=r['question'];p=q[':question/problem']; f=q[':question/answer-fields'][0]
 if not q[':question/difficulty'].endswith('/easy'): continue
 # family inferred from rendered ODE, independent of generation metadata
 m=re.search(r'\(x([+-]\d+)\)',p);shift=int(m[1]) if m else 0;u=x+shift
 if '{y}^{2}+1' in p:
  am=re.search(r'=([2-5])\(',p);a=int(am[1]) if am else 1
  rhs=lambda v:a*(v**2+1);kind='tan'
 elif '3{y}^{2}' in p:rhs=lambda v:2*u/(3*v**2);kind='root3'
 elif '{e}^{-y}' in p:rhs=lambda v:u*s.exp(-v);kind='log'
 elif r'\sqrt[3]{{y}^{2}}' in p:rhs=lambda v:6*u*s.Abs(v)**s.Rational(2,3);kind='cube'
 else:raise ValueError(p)
 results=[]
 for ch in f[':answer-field/choices']:
  v=parse(ch[':answer/value'].split('=',1)[1]);res=s.diff(v,x)-rhs(v)
  # Check exact generic residual; positive-base domain subset suffices to disprove a family.
  residuals=[s.simplify(res.subs({x:-shift+j,C:2,K:2})) for j in [1,2,3]]
  zero=all(z==0 for z in residuals)
  key=ch[':answer/id']==f[':answer-field/correct'][1]
  results.append({'value':ch[':answer/value'],'key':key,'all_exact_residuals_zero':zero,'residuals':[str(z) for z in residuals],'passed':zero==key})
 # Read final worked-solution expression independently (before domain annotation).
 blocks=re.findall(r'\$\$\s*([\s\S]*?)\s*\$\$',q[':question/worked-solution']);last=blocks[-1].strip().rstrip('.')
 if last.startswith('y='):
  sol=parse(last[2:]);correct=parse(next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1]).split('=',1)[1]);solution_match=s.simplify(sol-correct)==0
 else:solution_match=False
 report.append({'index':i,'id':q[':question/id'],'family_inferred_from_prompt':kind,'shift_inferred':shift,'choices':results,'worked_solution_matches':solution_match,'passed':all(c['passed'] for c in results) and solution_match})
(E/'math-results.json').write_text(json.dumps({'method':'Read ODE and final solution from displayed prompt, parse every choice through independent SymPy Lark reader, exact derivative residual at three regular positive-base points (C=2); reject wrong families, not special particular solutions. Negative cube-root branches are source-supported real-root convention; no claim of exhaustive real-domain proof.','command':sys.executable+' math_checks.py','cases':report,'passed':all(r['passed'] for r in report)},indent=2)+'\n')
print('math cases',len(report),'failures',[r['index'] for r in report if not r['passed']])
