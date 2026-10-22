import sys,json,pathlib
E=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(E/'deps'))
import sympy as s
from sympy.parsing.latex import parse_latex
x,C=s.symbols('x C',positive=True);n=4;p=1/x;q=1/x**2
source=json.load(open(E.parent/'source/source.json'));question=next(v for v in source['material']['kp'][':knowledge-point/questions'] if v[':question/math-academy-id']=='q-106074')
def residual(Y):
 z=s.powdenest(Y**(-3),force=True);return s.simplify(s.diff(z,x)-3*z/x+3/x**2)
correct=(4*x/(C*x**4+3))**s.Rational(1,3);assert residual(correct)==0
out=[]
for a in question[':question/answer-fields'][0][':answer-field/choices']:
 expr=parse_latex(a[':answer/value'].split('=',1)[1]);expr=expr.xreplace({v:{'x':x,'C':C}.get(str(v),v) for v in expr.free_symbols});res=residual(expr);assert res!=0;out.append({'choice':a[':answer/value'],'linear_residual':str(res)})
(E/'source-gap-results.json').write_text(json.dumps({'source_id':question[':question/id'],'derived_equation':'z\' - 3z/x = -3/x^2, z=y^(-3)','general_solution':'y=(4x/(C*x^4+3))^(1/3)','derived_residual':0,'source_bank':out,'conclusion':'All five captured choices are invalid general-solution families. Exclusion pending source correction is defensible.'},indent=2)+'\n')
a=json.load(open(E/'source-analysis.json'));a['gaps'][0]='caf692da-64e7-571b-8ecf-524b4723203b lacks correct answer and worked solution: independent derivation gives y=(4x/(C*x^4+3))^(1/3), not any captured choice; see source-gap-results.json. An initial arithmetic slip in this account was corrected by the exact residual check.'
(E/'source-analysis.json').write_text(json.dumps(a,indent=2)+'\n')
