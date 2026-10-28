import json,re
from pathlib import Path
import sympy as S
from texmath import parse
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());Q={q.get(':question/math-academy-id'):q for q in D['questions']};out=[];proofs=[]
def add(q,attr,after,why,proof):
 out.append(dict(entity=q[':db/id'],attribute=attr,before=q.get(attr),after=after,reason=why,evidence={'basis_t':9122,'identity':q.get(':question/math-academy-id'),**proof},confidence='high'))
for ma,power in [('q-2005',''),('q-2022','^{4}')]:
 q=Q[ma];after='Calculate the integral.\n\n$$\n\\int x'+power+r'\,\mathrm{d}x.'+'\n$$';add(q,':question/problem',after,'Restore missing integral command boundary and show standalone calculation in display math.',{'source':f'/home/jake/Developer/MA/DATA/Lessons/308/Source/308.html','source_formula':r'\int x'+power+r'\hspace{0.167em}\text{d}x.','strict_error':'Undefined control sequence '+(r'\intxdx'if not power else r'\intx')})
q=Q['q-133291'];add(q,':question/problem',r"Given $y'(t)=t^2-2$, find $y(t)$, the antiderivative of $y'(t)$."+'\n\n$y(t)=$\n{{field-1}}\n$+C$', 'Author missing shared derivative given explicitly recalled by existing solution.',{'solution_evidence':q[':question/worked-solution'].split('\n\n')[0],'independent_check':'d(t^3/3-2t)/dt=t^2-2'})
for ma,tex,domain in [('q-132983',r'\frac2t-\frac{16t}{2t^2+3}',r'$t\ne0$'),('q-132779',r'\frac1t-\frac{4t}{t^2+3}',r'$t>0$'),('q-133003',r'\frac1{2t}-\frac{3t}{t^2+1}',r'$t>0$')]:
 q=Q[ma];f=q[':question/answer-fields'][0];value=f[':answer-field/correct'][':answer/value'];t=S.Symbol('t',positive=True);expr=parse(tex);argument=parse(value);residual=S.simplify(S.diff(S.log(argument),t)-expr);assert residual==0
 after=f'For {domain}, let $y\u2032(t)={tex}$. Complete the argument $A(t)$ so that\n\n$$\n\\int y\u2032(t)\\,\\mathrm{{d}}t=\\ln(A(t))+K,\n$$\n\nwhere $K$ is an arbitrary constant.\n\n$A(t)=$\n{{{{'+f[':answer-field/key']+'}}}}';after=after.replace('{{{{','{{').replace('}}}}','}}')
 add(q,':question/problem',after,'Author missing shared givens and explicit real-log domain; clarify existing argument-only blank without changing answer values.',{'classification':'Authored standalone givens/domain repair, not source recovery','solution_evidence':q[':question/worked-solution'],'proof':str(residual),'positive_branch':domain,'owned_canonical':value})
 if ma=='q-132779':
  old=q[':question/worked-solution'];new=old.replace(r'\frac{4t}{{t}^{2}+1}',r'\frac{4t}{{t}^{2}+3}');new=new.replace('Using the sum and constant multiple rules,', 'Since $t>0$, we have $\\ln|t|=\\ln t$. Using the sum and constant multiple rules,');assert new!=old
  add(q,':question/worked-solution',new,'Correct source-internal denominator typo and explicitly justify positive-branch logarithm simplification.',{'proof':'Derivative ln(t/(t^2+3)^2)=1/t−4t/(t^2+3), not1/t−4t/(t^2+1). All later source lines and canonical argument use+3.','source_internal_typo':True})
q=Q['q-335056'];after=q[':question/problem'].replace('released from rest with an initial downward velocity','launched downward with an initial velocity');assert after!=q[':question/problem'];add(q,':question/problem',after,'Remove contradictory rest statement while preserving explicitly given4.6m/s initial velocity and matching existing solution/key.',{'proof':'No drag:v′=g, v(0)=4.6 impliesv=gt+4.6; at rest would imply0 and contradict given velocity.','canonical':q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']})
for ma,eq in [('q-317821',r'(2+ye^{xy})\,\mathrm{d}x+(xe^{xy}-2y)\,\mathrm{d}y=0'),('q-320435',r'(2+y^2e^{xy})\,\mathrm{d}x+(xe^{xy}-2y)\,\mathrm{d}y=0')]:
 q=Q[ma];after='Consider the differential equation\n\n$$\n'+eq+'\n$$\n\nTo test whether it is exact, write it as $P(x,y)\\,\\mathrm{d}x+Q(x,y)\\,\\mathrm{d}y=0$. Which partial-derivative equality is the exactness criterion?\n\n{{field-1}}'
 add(q,':question/problem',after,'Clarify captured first-step select task and remove incorrect default option rendered as a given; no uncaptured follow-up banks invented.',{'classification':'Authored first-step scope clarification. Dynamic source capture retained one criterion bank only.','proof':'Exactness criterionP_y=Q_x; completion-solution-proposals contains independently computed derivatives.'})
(H/'extra-context-proposals.json').write_text(json.dumps(out,indent=2));print('extra',len(out))
