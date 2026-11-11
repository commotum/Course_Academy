import importlib.util,json,sys
from pathlib import Path
import sympy as S
b=Path('/home/jake/Developer/Course_Academy/reference/edb-math/repairs/2026-11-11-normal-independent-practice/package')
sys.path.insert(0,str(b));spec=importlib.util.spec_from_file_location('normal_candidate',b/'generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=S.Symbol('x',real=True);report={'cases':0,'bands':{},'failures':[]};zero=[]
for band in ['easy','moderate','hard']:
 families={}; cases=[]
 for seed in [17,83,291]:
  for r in g.generate_batch(band,12,seed):
   p=r['generation']['parameters'];a,b,c,t=[S.Rational(p[k]) for k in ['a','b','c','point']];fam=r['generation']['template'];families[fam]=families.get(fam,0)+1
   # Independent reconstruction and implicit normal-line identity.
   f={'quadratic':a*x*x+b*x+c,'cubic':a*x**3+b*x+c,'sextic':a*x**6/8-b*x**3/4+c,'root-reciprocal':a/S.sqrt(x)+b/x+c,'reciprocal-powers':a/x+b/x**2+c,'cube-linear':a*S.real_root(x,3)+b*x+c}[fam]
   f0=S.simplify(f.subs(x,t));m=S.simplify(S.diff(f,x).subs(x,t));n=-1/m;intercept=S.simplify(f0-n*t)
   expected={'slope':n,'intercept':intercept,'coefficient':m,'constant':S.simplify(t+m*f0)}
   for field in r['question'][':question/answer-fields']:
    ans=field[':answer-field/choices'][0][':answer/value'];actual=S.sympify(ans.replace('\\frac{','(').replace('}{',')/(').replace('}',')')) if '\\frac' in ans else S.sympify(ans)
    assert S.simplify(actual-expected[field[':answer-field/key']])==0,(band,fam,p,ans,expected)
    if actual==0:zero.append({'band':band,'family':fam,'field':field[':answer-field/key'],'parameters':p})
   assert m!=0 and m.is_finite and f0.is_finite
   assert 'negative reciprocal' not in r['question'][':question/problem'] and "f'(" not in r['question'][':question/problem']
   report['cases']+=1
 report['bands'][band]={'count':36,'families':families}
report['valid_zero_examples']=zero[:10]
report['status']='passed';Path('/tmp/question-audit-20261111/independent-review/normal-math.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
