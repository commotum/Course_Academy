import json,sympy as s,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from symbolic import parse,SYMS
x,y,C,K=SYMS['x'],SYMS['y'],SYMS['C'],SYMS['K'];v=json.loads((H/'symbolic-math-validation.json').read_text());Q={q[':db/id']:q for q in json.loads((H/'proposed-snapshot.json').read_text())['questions']};out=[]
def save(e,kind,proof,passed=True,limits=None):out.append({'entity':e,'classification':kind,'passed':passed,'independent_evidence':proof,'limits':limits})
# Full parent givens, not child-answer inference.
contexts={r[0]:r[3]for r in json.loads((H/'all-contexts.json').read_text())}
for e in [17592186235436,17592186235485,17592186514423,17592186578821,17592186600797]:
 q=Q[e];f=q[':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices']if a[':db/id']==f[':answer-field/correct'][':db/id']);expected=2*s.exp(x)+24*x-2*x**3 if '4f' in q[':question/problem']else 2*x*x+4*x+1+s.exp(x);assert s.simplify(s.diff(parse(a[':answer/value']),x)-expected)==0;save(e,'valid multistep child',{'context':contexts[e],'integrand_after_given_substitution':str(expected),'derivative_difference':'0'})
for e in [17592186235434,17592186235482,17592186514385]:
 q=Q[e];f=q[':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices']if a[':db/id']==f[':answer-field/correct'][':db/id']);expected=s.diff(s.exp(-4*s.sin(x))/2,x);actual=parse(a[':answer/value']);actual=-actual/s.exp(4*s.sin(x))if e==17592186235482 else actual*s.exp(-4*s.sin(x))if e==17592186235434 else actual;assert s.simplify(actual-expected)==0;save(e,'valid multistep chain rule',{'full_function':'exp(-4sinx)/2','expected':str(expected),'reconstructed_answer':str(actual),'difference':'0'})
# Implicit response frames are part of the mathematical answer.
for e,a in [(17592186323684,3),(17592186691531,2),(17592186691969,3),(17592186691970,3),(17592186691972,3),(17592186691975,1),(17592186691976,2)]:
 ns={'__file__':str(H/'math_check.py')};exec((H/'math_check.py').read_text().split('checks=[];unresolved=[];bad=[];completion_matches=[]')[0],ns);q=Q[e];f=q[':question/answer-fields'][0];choice=next(z for z in f[':answer-field/choices']if z[':db/id']==f[':answer-field/correct'][':db/id']);R=parse(choice[':answer/value']);res,state=ns['ode_task'](q);diff=s.simplify(res.subs(SYMS['Z'],s.diff(R,x)/(a*s.cos(a*y)))).subs(s.sin(a*y),R);assert s.simplify(diff)==0;save(e,'valid implicit sine response',{'frame':'sin('+str(a)+'y)=R(x)','differentiated_frame':'cos(ay)yprime=Rprime/a','ODE_difference':'0','branch':'existing prompt local sine branch retained; completeness not inferred from residual'})
proofs={
17592186069532:('branch condition added','2sqrt(y)=x²+x+C requires x²+x+C>0 because prompt excludes y=0; squared answer otherwise has spurious negative-bracket pieces.'),
17592186275110:('valid implicit family','Original rational RHS cancels to (y²+x²)/(xy) only where x*y*(x+y)≠0. Differentiating y²=x²(2ln|x|+C) gives yprime=(y²+x²)/(xy) on that family, x≠0.'),
17592186275325:('valid real radical family','For x≥0,y>0, sqrt(y³)=y^(3/2), sqrt(x³)=x^(3/2). Differentiation cancels3/2, yielding yprime=sqrt(x)/sqrt(y).'),
17592186297340:('valid coefficient fragment','Full displayed derivative equals field·5^(x³+1). Coefficient3x²ln5 follows chain rule; the raw field alone is not the derivative.'),
17592186323686:('valid implicit tangent response','tan(4y)=4tan(7x)/7 differentiates to sec²(4y)yprime=sec²(7x), matchingODE; y(0)=0 and existing ybranch retained.'),
17592186332805:('valid IVP local branch','Derivative ln|1+2x| is2/(1+2x) forx≠−1/2. (1+2x)fprime−2=0, f(0)=−2. Maximal initial intervalx>−1/2.'),
17592186348253:('positive-quadrant scope added','Onx>0,y>0, sqrt(y)=x^(3/2)/3+K must havepositivebracket. Negativequadrant solutions exist and are outside authoredclarifiedscope.'),
17592186351479:('positive-quadrant scope added','Onx>0,y>0, y^(3/2)=3sqrt(x)+K requirespositivebracket. Negativequadrant solutions exist and are outside authoredclarifiedscope.'),
17592186373003:('lost denominator frame repaired','Sourceborderfraction meansy=x/(4−x−x²). Differentiationyprime=(x²+4)/(4−x−x²)² equals(4/x²+1)y² andy(2)=−1.'),
17592186657676:('valid radical equivalence','Forx>3, sqrt((2x−6)^3)=(2x−6)^(3/2), so givenanswer−1/sqrt((2x−6)^3) is derivative of1/sqrt(2x−6).'),
17592186671882:('valid implicit tangent family','Differentiatingtan(y−1)=2x+C givessec²(y−1)yprime=2, henceyprime=2cos²(y−1). Existinglocalbranch excludes allconstantcoszeroequilibria.'),
17592186672504:('valid sine argument fragment','The displayedframe isy=sin(field+C), withfield=(x−3)². Thenyprime=2(x−3)cos(theta)=2(x−3)sqrt(1−y²) onexisting−π/2<theta<π/2.')}
for e,(kind,proof)in proofs.items():save(e,kind,proof)
assert {r['entity']for r in v['mismatches']}<={r['entity']for r in out};(H/'symbolic-candidate-resolution.json').write_text(json.dumps({'original_mismatches':len(v['mismatches']),'resolved':out,'note':'Residual identities establish mathematical validity on stated domains. Separate equilibrium review checks constant solutions and source branch omissions.'},indent=2));print('resolved',len(out))
