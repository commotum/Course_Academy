"""Independent identity checks for the two incomplete source items."""
import json
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

root=Path(__file__).resolve().parent
records=json.loads((root/'source-replay-records.json').read_text())
x,y,p=s.symbols('x y p',positive=True)
reports=[]
for i,r in enumerate(records[:2]):
    expressions=[]
    for c in r['question'][':question/answer-fields'][0][':answer-field/choices']:
        tex=c[':answer/value']
        text=tex.replace('\\log_{2}','L2').replace('\\log','L').replace('{','(').replace('}',')')
        v=parse_expr(text,local_dict={'L':s.log,'L2':lambda z:s.log(z)/s.log(2),'x':x,'y':y,'p':p},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
        expressions.append((tex,v))
    expected=s.log(5)+3*s.log(p) if i==0 else s.log(x**3*y**2)/s.log(2)
    expected=s.expand_log(expected,force=True)
    result=[]
    for tex,v in expressions:
        same=s.simplify(s.expand_log(v,force=True)-expected)==0
        witness=s.N((v-expected).subs({p:2,x:3,y:5}),40)
        if not same:assert abs(witness)>s.Rational(1,10**10)
        result.append({'tex':tex,'expression':str(v),'identity':same,'difference_at_positive_witness':str(witness)})
    assert sum(c['identity'] for c in result)==1
    reports.append({'source':r['generation']['source_question_id'],'exact_expected':str(expected),'choices':result})
(root/'source-symbolic-math.json').write_text(json.dumps({'command':'/home/jake/Developer/Course_Academy/.venv/bin/python -B source-symbolic-math.py','sympy':s.__version__,'witness':{'p':2,'x':3,'y':5},'cases':reports},indent=2)+'\n')
print('Both incomplete source identities and all wrong-choice witnesses passed.')
