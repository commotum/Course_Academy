#!/usr/bin/env python3
"""Independent implicit directional-derivative checks of visible easy choices."""
import json,pathlib,sys
sys.dont_write_bytecode=True
W=pathlib.Path(__file__).resolve().parents[1];E=W/'evidence'
sys.path.insert(0,str(W/'checks'))
from check_shortcuts import visible,field
import sympy as s
x,y,C=s.symbols('x y C',real=True,nonzero=True)
rows=[]
for r in json.loads((E/'census-records.json').read_text()):
    t,a,cs=visible(r);f=field(r);zero_ids=[];witnesses=[]
    for choice,implied in zip(f[':answer-field/choices'],cs):
        if t=='cube_root':
            H=y**3/x**3-3*implied*s.log(s.Abs(x))-C
            rhs=(a*x**3+y**3)/(x*y**2)
        elif t=='affine':
            H=(y+implied*x)/x**2-C
            rhs=(a*x+2*y)/x
        else:
            H=y/x-implied*s.log(s.Abs(x))-C
            rhs=(a*x+y)/x
        residual=s.simplify(s.diff(H,x)+s.diff(H,y)*rhs)
        if residual==0:zero_ids.append(choice[':answer/id'])
        else:
            # Every candidate family passes through either nonsingular point for some C.
            assert residual.subs({x:2,y:5})!=0
            assert residual.subs({x:-2,y:-5})!=0
        witnesses.append({'choice':choice[':answer/value'],'implicit_family':str(H),'directional_derivative':str(residual),'zero':residual==0})
    assert zero_ids==[f[':answer-field/correct'][1]]
    rows.append({'question_id':r['question'][':question/id'],'visible_family':t,'visible_a':a,'choices':witnesses,'unique_correct':True})
(E/'math.json').write_text(json.dumps({'passed':True,'sympy_validation_version':s.__version__,'method':'Parse visible ODE and choice coefficients, express each choice as H(x,y,C)=0 and compute H_x+H_y*f(x,y). Exactly the keyed candidate has zero derivative. Nonzero residuals are witnessed at both positive and negative nonsingular points. No generator components or generation metadata used.','domain':'Real x,y nonzero for cubic; x nonzero for other families. log(abs(x)) differentiates to 1/x on either interval. Cubic is represented implicitly so real negative cube roots are included.','records':54,'choices':270,'results':rows},indent=2)+'\n')
print('Independent symbolic math passed: 54 ODEs, 270 candidates, exactly one correct per record.')
