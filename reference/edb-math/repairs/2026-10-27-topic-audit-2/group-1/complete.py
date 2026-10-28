"""Stage independently solved completions; never transact or invent existing IDs."""
import json,re,sys
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parents[4]/'scripts'))
from question_capture.math_format import MATH
from texmath import parse
D=json.loads((H/'current.json').read_text()); Q={q[':db/id']:q for q in D['questions']}; byma={q.get(':question/math-academy-id'):q for q in Q.values()}
reports=json.loads((H/'scalar-math-validation.json').read_text()); contexts=json.loads((H/'completion-context.json').read_text())
keys=[];solutions=[];proofs=[];empty=[]
def proposal(e,a,b,c,reason,evidence):return dict(entity=e,attribute=a,before=b,after=c,reason=reason,evidence=evidence,confidence='high')
def add(q,answers,solution,proof):
 evidence={'basis_t':9122,'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'independent_proof':proof,'template_context':'completion-context.json (canonical example and complete nearby KP questions)','source_limit':'Authored completion from existing prompt; no claim that prose is recovered original.'}
 for f in q.get(':question/answer-fields',[]):
  if ':answer-field/correct'in f or f[':db/id']not in answers:continue
  aid=answers[f[':db/id']]; assert aid in {a[':db/id']for a in f.get(':answer-field/choices',[])},(q[':db/id'],aid)
  keys.append(proposal(f[':db/id'],':answer-field/correct',None,aid,'Complete independently solved missing key using uniquely correct existing owned answer.',evidence))
 if solution and not q.get(':question/worked-solution'):solutions.append(proposal(q[':db/id'],':question/worked-solution',None,solution,'Author missing worked solution with explicit calculation and correct existing-bank result.',evidence))
 proofs.append(evidence)
for r in reports:
 if r['status']!='missing-key-derived':continue
 q=Q[r['question']]; expected=r['expected'];kind=r['kind'];x=r['variable'];answers={c['field']:c['matching_answers'][0]for c in r['checks']};f=q[':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices']if a[':db/id']==answers[f[':db/id']]);ans=a[':answer/value'].replace('±',r'\pm')
 if kind=='root-set':
  texes=[m[0][2:-2]if m[0].startswith('$$')else m[0][1:-1]for m in MATH.finditer(q[':question/problem'])];equation=next(t for t in texes if '='in t);left,right=equation.split('=',1);polynomial=S.expand(parse(left)-parse(right));var=next(iter(polynomial.free_symbols));root_values=S.sympify(expected);factored=S.Mul(S.Poly(polynomial,var).LC(),*[var-v for v in sorted(root_values,key=str)],evaluate=False)
  solution='Move every term to the left, combine like terms, and factor:\n\n$$\n'+S.latex(polynomial)+'='+S.latex(factored)+'=0.\n$$\n\nThe zero-product rule gives\n\n$$\n'+ans+'.\n$$\n\nSubstitution in the original equation confirms each listed root.'
 elif kind in ['antiderivative','definite-integral']:
  integrand=r['integrand'];var=S.Symbol(x,positive=True);expr=S.sympify(integrand,locals={x:var});primitive=S.integrate(expr,var)
  solution='Apply the sum and constant multiple rules, using the power rule or the standard trigonometric/exponential antiderivative for each term:\n\n$$\n\\int '+S.latex(expr)+r'\,\mathrm{d}'+x+'='+ans+'.\n$$\n\nDifferentiate the result to check:\n\n$$\n'+r'\frac{\mathrm{d}}{\mathrm{d}'+x+'}\\left('+S.latex(primitive)+'+C\\right)='+S.latex(S.diff(primitive,var))+'.\n$$'
 else:
  var=S.Symbol(x,positive=True);func=S.sympify(r['function'],locals={x:var});der=S.diff(func,var)
  solution='Use the product rule, $(uv)\u2032=u\u2032v+uv\u2032$, and differentiate each factor:\n\n$$\n'+r'\frac{\mathrm{d}}{\mathrm{d}'+x+'}\\left('+S.latex(func)+'\\right)='+S.latex(der)+'.\n$$'
  if kind=='evaluated-derivative':solution+='\n\nSubstituting the given point gives\n\n$$\n'+S.latex(der.subs(var,S.sympify(r['point'])))+'.\n$$'
 add(q,answers,solution,{'method':kind,'expected':expected,'full_bank_check':r['checks'],'branch_limit':r['assumptions']})
# Each manual entry has an independent explicit derivation; no key is inferred from a duplicate bank.
manual={
'q-74903':([17592186123936],r'For $x\ne0$, cancel $x$ to obtain $(2y^2+xy)/(x^2+y^2)$. Along $y=0$ the value is $0$, whereas along $y=x$ it is $3/2$. The two path limits differ, so the limit does not exist.'),
'q-74954':([17592186123949],r'Rationalize the denominator: $(x-y)/(\sqrt{x}-\sqrt{y})=\sqrt{x}+\sqrt{y}$ wherever the original expression is defined. By continuity, the limit is $2+2=4$.'),
'q-50099':([17592186171019],r'Substitute each marked point into $y\u2032=2-xy$. The slopes at $(-1,2)$, $(1,3)$, and $(0,-2)$ are respectively $4,-1,2$. Select the diagram with a steep positive segment on the left, a negative segment at $(1,3)$, and a positive segment at $(0,-2)$.'),
'q-80494':([17592186171226],r'Substitute each marked point into $y\u2032=x^2-2y$. The slopes at $(1,2)$, $(-1,-1)$, and $(2,-2)$ are respectively $-3,3,8$. Select the diagram with those signed segment slopes.'),
'q-96477':([17592186171473],r'Compare segments across each horizontal row. In the selected diagram every segment in a row has the same slope, so the slope depends only on $y$. It therefore cannot represent the stated dependence on both $x$ and $y$.'),
'q-334032':([17592186113631],r'Downward is positive. Gravity is $80g$ and drag is $-kv$. Newton\u2019s law gives $80v\u2032=80g-kv$, hence $v\u2032+(k/80)v=g$.'),
'q-334034':([17592186113636],r'Downward is positive, so $72v\u2032=72g-18v$. Divide by $72$ to obtain $v\u2032+\frac14v=g$.'),
'q-334056':([17592186113642,17592186113651,17592186113655],r'Newton\u2019s law gives $v\u2032+(k/12)v=9.8$. Using $v=9$ and $v\u2032=6.8$ yields $6.8+9k/12=9.8$, so $k=4\,\mathrm{kg/s}$. Substitution gives $v\u2032+\frac13v=g$.'),
'q-334536':([17592186113659],r'With negligible drag, gravity is the only force. Newton\u2019s law is $mv\u2032=mg$, so $v\u2032=g$.'),
'q-317664':([17592186144297],r'Write the equation as $(2+ye^{xy})\,\mathrm{d}x+(xe^{xy}-2y)\,\mathrm{d}y=0$. A potential is $F=e^{xy}-y^2+2x$, since $F_x=2+ye^{xy}$ and $F_y=xe^{xy}-2y$. Thus $e^{xy}-y^2+2x=c$.'),
'q-317821':([17592186144300],r'The exactness criterion is $P_y=Q_x$. Here $P=2+ye^{xy}$ and $Q=xe^{xy}-2y$, so both partial derivatives equal $e^{xy}+xye^{xy}$. Thus the equation is exact.'),
'q-320435':([17592186144316],r'The exactness criterion is $P_y=Q_x$. Here $P_y=(2y+xy^2)e^{xy}$, whereas $Q_x=(1+xy)e^{xy}$. They are not identically equal, so the equation is not exact.'),
'q-64180':([17592186146467],r'Exactness requires $P_y=Q_x$. Since $Q=2y+x$, we have $Q_x=1$. For candidates I, II, III, $P_y$ is respectively $1,1,0$. Therefore I and II only are possible.'),
'q-136634':([17592186174390],r'Cosine has period $2\pi$ and is even. Therefore $\cos(-x+16\pi)=\cos(-x)=\cos x=-11/24$.'),
'q-65176':([17592186175416],r'Cosine has period $2\pi$, so $\cos(x-6\pi)=\cos x$. Hence $4\cos(x-6\pi)-1=4(\sqrt3/2)-1=2\sqrt3-1$.'),
'q-65179':([17592186175424],r'The shift $10\pi$ is five full periods, so $\cos(x+10\pi)=\cos x=-1/\sqrt3$.'),
'q-118386':([17592186177220],r'At one half-life $H$, $e^{-0.53319H}=1/2$. Thus $H=\ln2/0.53319=1.3000\ldots\,\mathrm{s}$, which rounds to $1.3\,\mathrm{s}$.'),
'q-118600':([17592186177228],r'Exponential decay gives $M(t)=M_0\,2^{-t/H}$. At the stated time, $t/H=1.5$, so $M=100\,2^{-1.5}=35.3553\ldots\,\mathrm{pg}$, or $35.36\,\mathrm{pg}$.'),
'q-118730':([17592186177233],r'The remaining fraction is $0.15=2^{-t/717000}$. Taking logarithms gives $t=717000\ln(1/0.15)/\ln2=1962404\ldots$ years, approximately $1$ million $962$ thousand years.'),
'q-15574':([17592186178145],r'The remaining fraction is $6.25/200=1/32=(1/2)^5$. Five half-lives have elapsed, so $t=5(15.2)=76\,\mathrm{s}$.'),
'q-15575':([17592186178153],r'At the half-life, $e^{-0.001k}=1/2$. Therefore $k=\ln2/0.001=693.147\ldots\,\mathrm{s}^{-1}$, which is $693$ to three significant figures.'),
'q-336439':([17592186228337],r'Substitute $t=0$ into the stated model $Q(t)=\alpha+\beta e^{-kt}$. Since $e^0=1$ and the initial salt mass is $6\,\mathrm{kg}$, $\alpha+\beta=Q(0)=6$.'),
'q-336499':([17592186228346],r'The volume is $V(t)=120+(9-6)t=120+3t$. Overflow begins when $V=210$, so $t=30\,\mathrm{min}$. Mass balance gives $Q\u2032=4.5-6Q/(120+3t)$. Its solution satisfying $Q(0)=30$ is $Q=\frac12(120+3t)-30(120/(120+3t))^2$. At $t=30$, $Q=95.204\ldots\,\mathrm{lb}$, hence $95.2\,\mathrm{lb}$.'),
'q-339392':([17592186228571],r'The volume stays $900\,\mathrm{L}$. The salt inflow is $0.02(30)=0.6\,\mathrm{kg/min}$ and outflow is $30Q/900=Q/30$. Thus $Q\u2032+Q/30=0.6$. With $Q(0)=10$, $Q(t)=18-8e^{-t/30}$. Consequently $Q(6)=11.4501\ldots\,\mathrm{kg}$, or $11.45\,\mathrm{kg}$.'),
}
for ma,(aids,solution)in manual.items():
 q=byma[ma];answers={}
 for aid in aids:
  fs=[f for f in q[':question/answer-fields']if aid in{a[':db/id']for a in f.get(':answer-field/choices',[])}];assert len(fs)==1;(f,)=fs;answers[f[':db/id']]=aid
 add(q,answers,solution.replace(r'\u2032','′').replace(r'\u2019','’'),{'calculation':solution,'bank_cardinality':len(aids),'image_check':'All five retained diagram choices visually inspected'if ma in['q-50099','q-80494','q-96477']else None})
# Missing banks are a separate reviewable authoring request, never masquerading as existing entities.
new=[('q-218567',r'\pm\frac25',r'$25y^2=4$ gives $y^2=4/25$, so $y=\pm2/5$.'),('q-218603',r'\pm5\sqrt2',r'$z^2=53-3=50$, hence $z=\pm\sqrt{50}=\pm5\sqrt2$.'),('q-334539','41.8',r'Without drag, $v(t)=2.6+9.8t$, so $v(4)=41.8\,\mathrm{m/s}$.'),('q-334550',r'49(1-e^{-t/5})',r'$k=25(9.8-7.4)/12=5$. Thus $v\u2032+v/5=9.8$ and $v(0)=0$, giving $v(t)=49(1-e^{-t/5})$.'),('q-334572','39.2',r'At terminal velocity, $0=mg-kv$, so $v=20(9.8)/5=39.2\,\mathrm{m/s}$.'),('q-334770','1.2+gt',r'With negligible drag, $v\u2032=g$. Integrating and using $v(0)=1.2$ gives $v(t)=1.2+gt$.'),('q-335190',r'49-44e^{-t/5}',r'$k=30(9.8-8.2)/8=6$. The ODE is $v\u2032+v/5=9.8$, whose solution with $v(0)=5$ is $v(t)=49-44e^{-t/5}$.'),('q-353607','6.3',r'The remaining fraction satisfies $0.70=2^{-t/12.3}$. Therefore $t=12.3\ln(0.70)/\ln(0.5)=6.3292\ldots$ years, or $6.3$ years to one decimal place.')]
for ma,value,solution in new:
 q=byma[ma];f=q[':question/answer-fields'][0];assert not f.get(':answer-field/choices');empty.append({'question':q[':db/id'],'field':f[':db/id'],'field_identity':f[':answer-field/id'],'answer_type':':answer.type/math','expected_value':value,'worked_solution':solution.replace(r'\u2032','′'),'basis_t':9122,'reason':'No existing owned answer bank; new answer identity/allocation requires parent consolidation. Independently solved from prompt.','template_context':'completion-context.json'})
(H/'key-proposals.json').write_text(json.dumps(keys,indent=2));(H/'completion-solution-proposals.json').write_text(json.dumps(solutions,indent=2));(H/'completion-proofs.json').write_text(json.dumps(proofs,indent=2));(H/'missing-bank-authoring.json').write_text(json.dumps(empty,indent=2))
print('keys',len(keys),'solutions',len(solutions),'missingbanks',len(empty))
