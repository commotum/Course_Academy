"""Private basis-2275 chain-rule draft; never changes the registered baseline.

Raw profiles parameterize complete captured components and preserve omissions.
Normal questions retain each observed operative solution, with method-derived
complete banks and explicit conservative easy authorship. No database operations.
"""
import argparse, copy, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186096843
KP_UUID='0a312840-0d35-50bb-94b3-b04778f4efc3'
TITLE='Differentiating a Function Using the Chain Rule and Prime Notation'
HERE=Path(__file__).with_suffix('')
VERSION='2.0.0-draft'
SUPPORTED_LEVELS=('easy','moderate','hard')
import importlib.util
_spec=importlib.util.spec_from_file_location('math_format',HERE.parents[2]/'scripts/question_capture/math_format.py')
math_format=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(math_format)
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION))
x=s.Symbol('x',real=True)
SOURCES={q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
DEFAULTS={'q-11414':{'c':4},'q-48850':{'c':3},'q-107293':{'b':4},'q-342804':{'b':3},'q-342875':{'c':4},'q-342883':{'b':-4},'q-342891':{'c':5},'q-71954':{'b':-7},'q-71956':{'b':2},'authored-square':{'a':2,'b':1}}
LEVELS={'q-11414':'hard','q-48850':'hard','q-107293':'moderate','q-342804':'moderate','q-342875':'hard','q-342883':'hard','q-342891':'hard','q-71954':'moderate','q-71956':'moderate','authored-square':'easy'}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def tex(e):return s.latex(e).replace(r'\log',r'\ln')
def affine(a,b):return f'{a}x{b:+d}'
def parameters_for(m):
    if m=='authored-square':return [{'a':a,'b':b} for a in (-5,-4,-3,-2,2,3,4,5) for b in range(-9,10) if b]
    key=next(iter(DEFAULTS[m]));values=range(1,17) if key=='c' else range(-12,13)
    return [{key:v} for v in values if m!='q-71956' or v!=0]

def model(m,p):
    b=p.get('b');c=p.get('c')
    if m=='authored-square':inner=p['a']*x+b;outer=s.Symbol('g')**2
    elif m=='q-11414':inner=3*x**5-c*x**2;outer=s.Symbol('g')**3
    elif m=='q-48850':inner=2*x**2+c*x;outer=2/s.sqrt(s.Symbol('g'))
    elif m=='q-107293':inner=3*x+b;outer=s.Symbol('g')**5
    elif m=='q-342804':inner=4*x+b;outer=s.Symbol('g')**5
    elif m=='q-71954':inner=8*x+b;outer=s.Symbol('g')**4
    elif m=='q-71956':inner=b-5*x;outer=s.Symbol('g')**3
    elif m=='q-342875':inner=x**5-c*x**4;outer=s.Symbol('g')**2
    elif m=='q-342883':inner=5*x+b;outer=s.sqrt(s.Symbol('g'))
    elif m=='q-342891':inner=2*x**4-x**2+c;outer=1/s.sqrt(s.Symbol('g'))
    else:raise ValueError('Unknown template')
    fun=outer.subs(s.Symbol('g'),inner)
    answer=s.diff(inner,x) if m=='q-342875' else -s.diff(inner,x)/2 if m=='q-342891' else s.diff(fun,x)
    return inner,outer,fun,answer

def transform(t,m,p):
    """Complete component slots; source-specific typography stays intact."""
    b=p.get('b');c=p.get('c')
    if m in ('q-107293','q-342804','q-71954','q-342883'):
        anchors={'q-107293':(3,4),'q-342804':(4,3),'q-71954':(8,-7),'q-342883':(5,-4)}
        a,old=anchors[m];pairs=[(affine(a,old),affine(a,b))]
        if m=='q-71954':pairs.append((affine(16,old),affine(16,b)))
    elif m=='q-71956':pairs=[('2-5x',f'{b}-5x'),('2+5x',f'{b}+5x')]
    elif m=='q-342875':pairs=[('4{x}^{4}',f'{c}'+r'{x}^{4}'),('16{x}^{3}',str(4*c)+r'{x}^{3}')]
    elif m=='q-342891':pairs=[('2{x}^{4}-{x}^{2}+5','2{x}^{4}-{x}^{2}+'+str(c))]
    elif m=='q-11414':pairs=[('3x^{5} - 4x^{2}',f'3x^{{5}} - {c}x^{{2}}'),('15x^{4} - 8x',f'15x^{{4}} - {2*c}x'),('5x^{5} - 8x',f'5x^{{5}} - {2*c}x'),('5x^{4} - 8x',f'5x^{{4}} - {2*c}x'),('-8(',f'-{2*c}(')]
    elif m=='q-48850':pairs=[('2x^{2} + 3x',f'2x^{{2}} + {c}x'),('4x + 3',f'4x + {c}'),('8x + 6',f'8x + {2*c}')]
    else:raise ValueError(m)
    # Simultaneous masks avoid accidental cascading replacements.
    for i,(old,new) in enumerate(pairs):t=t.replace(old,f'@@SLOT{i}@@')
    for i,(old,new) in enumerate(pairs):t=t.replace(f'@@SLOT{i}@@',new)
    return t

def solution(inner,outer):
    """Authored missing solutions use source common ordered prime stages."""
    G=s.Symbol('g');od=s.diff(outer,G);id=s.diff(inner,x);fun=outer.subs(G,inner)
    return (f'Let $g(x)={tex(inner)}$ and $f(g(x))={tex(outer)}.$ \n\nDifferentiating, we have\n\n$$\n'
        +r'\begin{aligned}{f}^{′}(g(x)) & ='+f'({tex(outer)})'+r'^{′}='+tex(od)+r', \\ {g}^{′}(x) & =('+tex(inner)+r')^{′}='+tex(id)+r'.\end{aligned}'
        +'\n$$\n\nThen, using the chain rule, \n\n$$\n'
        +r'\begin{aligned}{f}^{′}(x) & ={f}^{′}(g(x))\cdot {g}^{′}(x) \\  & =('+tex(od)+r')\cdot ('+tex(id)+r') \\  & ='+tex(s.diff(fun,x))+r'.\end{aligned}'+'\n$$')

def domain(m,p):
    if m=='q-342883':return {'real_x':True,'restriction':affine(5,p['b'])+'>0'}
    if m=='q-48850':return {'real_x':True,'restriction':f'2x^2+{p["c"]}x>0'}
    if m=='q-342891':return {'real_x':True,'restriction':'all real x; radicand minimum c-1/8>0'}
    return {'real_x':True,'restriction':'all real x'}

def task_fingerprint(m,p):
    inner,outer,fun,answer=model(m,p)
    shape='inner-derivative-fragment' if m=='q-342875' else 'reciprocal-radical-numerator-fragment' if m=='q-342891' else 'full-derivative'
    # In the reciprocal-radical numerator blank, the varying additive
    # constant never changes the assessed fragment. Do not inflate diversity.
    if m=='q-342891':return digest({'assessed_fragment':s.srepr(answer),'response':shape,'nonconstant_inner':s.srepr(inner-p['c'])})
    return digest({'function':s.srepr(s.expand(fun)),'response':shape,'domain':domain(m,p)})

def normal_values(m,p):
    """Choose complete bank before parameters; all errors use actual components."""
    inner,outer,fun,answer=model(m,p);id=s.diff(inner,x)
    if m=='authored-square':
        a=p['a'];b=p['b'];return [tex(v) for v in (answer,2*inner,a*inner**2,2*a*inner**2,2*a*(a*x-b))],0
    if m=='q-107293':
        # The historical coefficient20 is unresolved; replacement whole bank.
        return [tex(v) for v in (answer,5*inner**4,3*inner**5,3*inner**4,15*inner**5)],0
    if m in ('q-11414','q-48850','q-71954','q-71956'):
        vals=[transform(a[':answer/value'],m,p) for a in SOURCES[m][':question/answer-fields'][0][':answer-field/choices']]
        return vals,0 if m in ('q-11414','q-48850') else 4
    return [transform(SOURCES[m][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'],m,p)],0

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,bank_profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
    if profile is not None and bank_profile is not None and profile!=bank_profile:raise ValueError('Conflicting profile aliases')
    profile=profile or bank_profile
    rng=random.Random(seed)
    if profile and profile.startswith('raw-'):
        pm=profile[4:]
        if template is not None and template!=pm:raise ValueError('Profile/template mismatch')
        template=pm
    eligible=[m for m in LEVELS if LEVELS[m]==level]
    m=template or rng.choice(eligible)
    if m not in eligible:raise ValueError('Template/difficulty mismatch')
    raw=bool(profile and profile.startswith('raw-'))
    canonical_profile='raw-'+m if raw else 'authored-method-bank' if m in ('authored-square','q-107293') else 'source-operation-bank' if m in ('q-11414','q-48850','q-71954','q-71956') else 'source-blank'
    if profile not in (None,canonical_profile,'default'):raise ValueError('Unknown profile')
    if raw and m not in SOURCES:raise ValueError('No observed source for authored template')
    p=copy.deepcopy(parameters) if parameters is not None else rng.choice(parameters_for(m))
    if p not in parameters_for(m) or any(type(v)!=int for v in p.values()):raise ValueError('Outside documented level/template parameter bounds')
    inner,outer,fun,answer=model(m,p)
    if m=='authored-square':
        prompt=f'Given that $f(x)=({affine(p["a"],p["b"])})^{{2}},$ find $f^{{′}}(x).$'
        worked=solution(inner,outer);key='selection';ft=':answer-field.type/radio';values,ci=normal_values(m,p);has_correct=True;has_solution=True;has_grade=True
    else:
        src=SOURCES[m];field=src[':question/answer-fields'][0]
        prompt=transform(src[':question/problem'],m,p);worked=transform(src.get(':question/worked-solution',''),m,p)
        key=field[':answer-field/key'];ft=field[':answer-field/type'][':db/ident']
        has_correct=not raw or ':answer-field/correct' in field;has_solution=not raw or ':question/worked-solution' in src;has_grade=not raw or ':question/difficulty' in src
        if raw:
            values=[transform(a[':answer/value'],m,p) for a in field[':answer-field/choices']]
            ci=next((i for i,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field.get(':answer-field/correct',{}).get(':answer/id')),None)
        else:
            values,ci=normal_values(m,p)
            if not worked:worked=solution(inner,outer)
            if m=='q-342891':prompt=prompt.replace(r'\frac{\text{d}y}{\text{d}x}',r'{f}^{′}(x)')
    if field_type is not None and field_type not in (ft,ft.split('/')[-1]):raise ValueError('Observed answer-field contract cannot change')
    # Complete selected-bank eligibility, independently read back by validator.
    if not raw:
        D=s.diff(inner,x)
        if m=='authored-square':
            a=p['a'];b=p['b'];bank=(answer,2*inner,a*inner**2,2*a*inner**2,2*a*(a*x-b))
        elif m=='q-107293':bank=(answer,5*inner**4,3*inner**5,3*inner**4,15*inner**5)
        elif m=='q-11414':
            c=p['c'];bank=(answer,3*(5*x**5-2*c*x)*inner**2,-2*c*D*inner**2,3*D*inner**3,3*(5*x**4-2*c*x)*inner**2)
        elif m=='q-48850':bank=(answer,D/inner**s.Rational(3,2),-D/(2*inner**s.Rational(3,2)),-D/inner**s.Rational(2,3),-2*D/inner**s.Rational(3,2))
        elif m=='q-71954':bank=(32*(16*x+p['b'])**3,16*inner**3,16*(16*x+p['b'])**3,8*inner**3,answer)
        elif m=='q-71956':bank=(-15*(p['b']+5*x)**2,-15*inner**3,15*(p['b']+5*x)**2,15*inner**2,answer)
        else:bank=(answer,)
        for i,a in enumerate(bank):
            for b in bank[i+1:]:
                delta=s.powdenest(a,force=True)-s.powdenest(b,force=True)
                # A nonzero exact value at an allowed positive-domain point
                # disproves equivalence; simplify only potential equal pairs.
                if any(s.simplify(delta.subs(x,t))!=0 for t in (4,5,6)):continue
                if s.simplify(delta)==0:raise ValueError('Complete bank collision')
    if not raw:
        prompt=math_format.normalize_prose(prompt);worked=math_format.normalize_prose(worked)
        values=[math_format.normalize_tex(v) for v in values]
    fp=task_fingerprint(m,p)
    body={'problem':prompt,'solution':worked if has_solution else None,'difficulty':level if has_grade else None,'field':{'type':ft,'key':key,'values':sorted(values),'correct':values[ci] if has_correct else None},'domain':domain(m,p),'version':VERSION,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__,'parser':'sympy exact expressions; independent nested TeX readback'}}
    content_id=digest(body);uid=lambda text:str(uuid.uuid5(uuid.UUID(KP_UUID),text))
    qid=uid(content_id);fid=uid(qid+'|'+key)
    answers=[{':answer/id':uid(fid+'|'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    # Preserve feedback presence and parameterize if ever supplied by a source.
    if raw:
        for a,old in zip(answers,SOURCES[m][':question/answer-fields'][0][':answer-field/choices']):
            if ':answer/feedback' in old:a[':answer/feedback']=transform(old[':answer/feedback'],m,p)
    correct=answers[ci][':answer/id'] if has_correct else None
    if ft==':answer-field.type/radio':random.Random(seed).shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':ft,':answer-field/choices':answers}
    if has_correct:field[':answer-field/correct']=[':answer/id',correct]
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if has_solution:q[':question/worked-solution']=worked
    if has_grade:q[':question/difficulty']=':question.difficulty/'+level
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'level':level,'seed':seed,'template':m,'profile':canonical_profile,'bank_profile':canonical_profile,'parameters':p,'parameter_fingerprint':fp,'mathematical_fingerprint':fp,'content_identity':content_id,'domain':domain(m,p),'dependencies':body['dependencies'],'source_references':[] if m=='authored-square' else [m],'plots':'none','evidence_only':raw,'eligible_for_learning':not raw,'difficulty_provenance':'authored conservative band' if m=='authored-square' else 'authored hard assignment; raw unrated' if m in ('q-11414','q-48850') else 'observed MA label','source_basis':2275,'source_lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}}
    if not raw:return math_format.validate_generated_record(record)
    for k in (':question/problem',':question/worked-solution'):
        if k in q:math_format.validate_prose(q[k])
    for a in answers:math_format.validate_tex(a[':answer/value'])
    record['generation']['math_format']=math_format.FORMAT_VERSION
    return record

# Easy: authored affine squares; the smallest power-rule/inner-slope workload.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: observed affine cubic, quartic and quintic masks and banks.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: observed radical and polynomial fragment families; legacy completions.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def batch(level,count,seed=0):
    if count<0:raise ValueError('Count must be nonnegative')
    pairs=[(m,p) for m in LEVELS if LEVELS[m]==level for p in parameters_for(m)];random.Random(seed).shuffle(pairs)
    return [generate(level,seed+i,template=m,parameters=p) for i,(m,p) in enumerate(pairs[:count])]
def markdown(rec):
    q=rec['question'];parts=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        correct=f.get(':answer-field/correct',[None,None])[1]
        parts.append('\n'.join(('* ' if a[':answer/id']==correct else '- ')+a[':answer/value'] for a in f.get(':answer-field/choices',[])))
    if ':question/worked-solution' in q:parts.append(q[':question/worked-solution'])
    return '\n\n'.join(parts)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),required=True);p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=('markdown','json'),default='json');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
    levels=SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]
    records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
