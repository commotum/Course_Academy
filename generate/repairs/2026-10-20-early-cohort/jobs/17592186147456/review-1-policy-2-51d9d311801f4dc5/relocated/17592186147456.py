"""Source-backed Bernoulli recognition; decision-first power assignments."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import uuid
import sympy as sp
from generator_policy import nonempty_checkbox

KP_ID = 17592186147456
KP_UUID = 'eef27d2b-6149-5070-b711-f4dcc7db2a03'
VERSION = 'bernoulli-recognition-v2'
DATA = json.loads(Path(__file__).with_name('source-data.json').read_text())
SOURCE_BASIS = DATA['basis']
x, y = sp.symbols('x y', positive=True)
D = sp.Symbol('D')
LABELS = ('I', 'II', 'III')
# (derivative multiplier, supplied left term, supplied right term).
CASES = {
 'q-108911': ('easy', [(1,-sp.sqrt(x)*y,x**3/y), (1,sp.tan(x)*y,-sp.sqrt(x)*y**sp.Rational(3,2)), (1,-sp.log(x)*y**2,y**6)]),
 'q-108913': ('easy', [(1,x**-2*y**3,sp.sin(y)), (1,-sp.exp(x)*y,x**2*y**5), (1,sp.log(x)*y**4,-x*y**3)]),
 'q-108914': ('easy', [(1,sp.sqrt(x)*y,x**2*sp.log(y)), (1,x**2*y**2,x*y**3), (1,x**2*y,sp.sqrt(x)*y**sp.Rational(-1,2))]),
 'q-108916': ('moderate', [(y**2,-x*y**5,y**4), (y,-x*sp.sqrt(y),x**2), (1,sp.log(x)*y,x*sp.log(y))]),
 'q-108918': ('moderate', [(1,-sp.exp(x)*y**2,sp.sqrt(y)), (y**3,sp.log(x)*y**4,sp.sqrt(y)), (y,x*sp.sin(y),sp.cos(y)**2)]),
 'q-108912': ('easy', [(1,x**3*y,-y**sp.Rational(-1,2)), (1,-sp.sin(x)*y,sp.cos(x)*y**2), (1,y,sp.sec(x)/y**2)]),
 'q-108915': ('easy', [(1,sp.sec(x)*y,y**2), (1,-x*y**2,sp.exp(x)*y**6), (1,-x**sp.Rational(3,2)*y,x*sp.cos(y))]),
 'q-108920': ('moderate', [(y**sp.Rational(1,3),sp.sqrt(x)*y**sp.Rational(1,3),y**3), (1,-sp.sec(x)*y,sp.cos(y)), (y,sp.sqrt(x)*y**2,1)]),
}

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), value))

def equations(template, parameters):
    assert template in CASES
    assert set(parameters) in ({'left_scales','right_scales'}, {'left_scales','right_scales','decisions'})
    for values in (parameters['left_scales'],parameters['right_scales']):
        assert len(values)==3 and all(type(n) is int and 1<=n<=5 for n in values)
    eqns=[]
    decisions=parameters.get('decisions')
    if decisions is not None:
        assert len(decisions)==3 and all(type(v) is bool for v in decisions)
        assert tuple(decisions) in decision_cases(template)
    for i,(m,a,b) in enumerate(CASES[template][1]):
        m,a,b=map(sp.sympify,(m,a,b))
        if decisions is not None:
            left,right=monomial(a/m),monomial(b/m)
            if left and right:
                # Keep the other power fixed; change only decisive linearity.
                negative=left[1] if left[1]!=1 else (sp.Integer(2) if right[1]!=2 else sp.Integer(3))
                power=sp.Integer(1) if decisions[i] else negative
                a=sp.simplify(a*y**(power-left[1]))
        eqns.append((m,sp.expand(a*parameters['left_scales'][i]),sp.expand(b*parameters['right_scales'][i])))
    return eqns

def selection_text(flags):
    selected=[label for label,flag in zip(LABELS,flags) if flag]
    if not selected:return 'None of the given equations is a Bernoulli differential equation'
    if len(selected)==1:return selected[0]+' only'
    if len(selected)==2:return ' and '.join(selected)+' only'
    return 'I, II and III'

def decision_cases(template):
    import itertools
    base=CASES[template][1]; profile=DATA['profiles'][template]
    eligible=[bool(monomial(sp.sympify(a)/m) and monomial(sp.sympify(b)/m)) for m,a,b in base]
    return [flags for flags in itertools.product((False,True),repeat=3)
            if all(not flag or ok for flag,ok in zip(flags,eligible))
            and (profile['type']=='checkbox' or selection_text(flags) in profile['bank'])]

def monomial(expr):
    expr=sp.simplify(expr)
    power=expr.as_powers_dict().get(y,sp.Integer(0))
    coefficient=sp.simplify(expr/y**power)
    return (coefficient,power) if not coefficient.has(y) else None

def analyze(equation):
    m,a,b=equation
    left,right=sp.simplify(a/m),sp.simplify(b/m)
    l,r=monomial(left),monomial(right)
    # All observed candidates either have two distinct powers or a nonpower.
    # Either side may supply the linear term; this avoids positional grading.
    if l and r and l[1]!=r[1] and 1 in (l[1],r[1]):
        if l[1]==1: p,q,n=l[0],r[0],r[1]
        else: p,q,n=-r[0],-l[0],l[1]
        return {'correct':True,'p':p,'q':q,'n':n,'left':left,'right':right}
    return {'correct':False,'left':left,'right':right,
            'reason':('The normalized equation contains two different powers of $y$, neither with exponent 1.' if l and r
                      else 'The normalized equation contains a function of $y$ that is not a single power of $y$.')}

def math_text(expr):
    return sp.latex(expr, mul_symbol='dot')

def equation_text(m,a,b):
    m,a,b=map(sp.sympify,(m,a,b))
    derivative="y'" if m==1 else math_text(m)+"y'"
    if a.could_extract_minus_sign():
        return derivative+' - '+math_text(-a)+' = '+math_text(b)
    return derivative+' + '+math_text(a)+' = '+math_text(b)

def fingerprint(eqns):
    # Normalized mathematical objects, ignoring labels/order and whole-equation scaling.
    return digest(sorted(sp.srepr(sp.expand((a-b)/m)) for m,a,b in eqns))

def render_solution(eqns):
    text=['A Bernoulli differential equation has the form',
          "$$\ny'+p(x)y=q(x)y^n.\n$$",
          "With that in mind, let's examine the given options. Work on the stated positive domain, so dividing by powers of $y$ is valid."]
    flags=[]
    for label,eqn in zip(LABELS,eqns):
        m,a,b=eqn;info=analyze(eqn);flags.append(info['correct'])
        prefix=f'- Equation {label} is '+('a Bernoulli differential equation.' if info['correct'] else '*not* a Bernoulli differential equation.')
        if m!=1:
            prefix+=' Dividing by $'+math_text(m)+'$, we get\n\n$$\n'+equation_text(1,info['left'],info['right'])+'\n$$\n\n'
        if info['correct']:
            prefix+=' In this case, we have\n\n$$\np(x)='+math_text(info['p'])+',\\quad q(x)='+math_text(info['q'])+',\\quad n='+math_text(info['n'])+'.\n$$'
        else:
            prefix+=' '+info['reason']
        text.append(prefix)
    selected=[label for label,flag in zip(LABELS,flags) if flag]
    text.append('Therefore, select '+(', '.join(selected)+'.' if selected else 'none of the given equations.'))
    return '\n\n'.join(text)

def generate(level,seed=0,template=None,parameters=None,profile=None,replay=False):
    assert level in ('easy','moderate'), 'Unsupported source-backed difficulty'
    rng=random.Random(seed)
    # The captured None family has an explicit, correctly keyed selectable answer.
    eligible=[t for t,(l,_) in CASES.items() if l==level]
    template=template or rng.choice(eligible)
    assert template in eligible
    bank=DATA['profiles'][template]
    expected_profile='boolean-checkbox' if bank['type']=='checkbox' else template+'-radio'
    assert profile in (None,expected_profile)
    profile=expected_profile
    if parameters is None:
        flags=rng.choice(decision_cases(template))
        parameters={'decisions':list(flags),'left_scales':[rng.randint(1,5) for _ in range(3)],'right_scales':[rng.randint(1,5) for _ in range(3)]}
    eqns=equations(template,parameters)
    problem='Which of the following equations is a Bernoulli differential equation?\n\nWork on intervals where $x>0$ and $y>0$, and where the displayed coefficients are defined.\n\n'
    problem+='\n'.join('- **'+label+'.** $'+equation_text(*eqn)+'$' for label,eqn in zip(LABELS,eqns))
    if bank['type']=='checkbox':problem+='\n\nSelect all that apply.'
    solution=render_solution(eqns)
    fp=fingerprint(eqns);qid=uid('question:'+fp+':'+profile+':'+str(replay));fields=[]
    for label,eqn in zip(LABELS,eqns):
        fid=uid(qid+':field:'+label)
        choices=[{':answer/id':uid(fid+':'+value),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
        correct='true' if analyze(eqn)['correct'] else 'false'
        fields.append({':answer-field/id':fid,':answer-field/key':('$'+equation_text(*eqn)+'$') if replay else label,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+':'+correct)]})
    if bank['type']=='radio':
        fid=uid(qid+':selection'); values=bank['bank']
        choices=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/text',':answer/value':v} for v in values]
        correct=selection_text([analyze(e)['correct'] for e in eqns])
        assert correct in values
        fields=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+':'+correct)]}]
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':DATA['title']},
            'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields},
            'generation':{'version':VERSION,'source_basis':SOURCE_BASIS,'source_template':template,'template':template,'bank_profile':profile,'seed':seed,'parameters':parameters,'parameter_fingerprint':fp,'content_fingerprint':digest({'problem':problem,'solution':solution}),'domain':'x>0, y>0; coefficients defined','eligible_for_learning':True,'sympy_version':sp.__version__}}
    # Replay the one original three-checkbox bank without manufacturing a fourth.
    if replay and not bank['source_none'] and bank['type']=='checkbox':
        record['generation']['evidence_only']=True
    record['generation']['replay']=replay
    return record

def markdown(record):
    q=record['question'];return q[':question/problem']+'\n\n'+q[':question/worked-solution']


generate = nonempty_checkbox(generate, none_label='None of the above')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=('easy','moderate'),required=True);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--template',choices=tuple(CASES));parser.add_argument('--output',type=Path);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('json',),default='json')
    args=parser.parse_args()
    if args.count<1:parser.error('--count must be positive')
    r=[generate(args.difficulty,args.seed+i,args.template) for i in range(args.count)]
    if args.output:
        args.output.write_text(json.dumps(r,indent=2)+'\n')
    else:print(json.dumps(r,indent=2))
