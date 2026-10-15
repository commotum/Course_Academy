#!/usr/bin/env python3
"""Partial derivatives as difference-quotient limits, local draft only.

Observed families use extracted parameterized prompt/solution/bank masks, never
completed source records. `observed` preserves raw attribute omissions; it is
ineligible evidence. `method` retains each family's three operative stages and
repairs f(x) to f(x,y), old limit typography, and the missing root-product key.
Hard is authored: form the same quotient at a supplied point without evaluating
it by a derivative rule. No EDB or registered numeric script is imported/written.
"""
import sys
sys.dont_write_bytecode=True
import argparse,hashlib,importlib.util,json,random,re,uuid
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parents[2]
ASSETS=Path(__file__).with_suffix('')
spec=importlib.util.spec_from_file_location('kp124643_math_format',ASSETS/'reference/math_format.py');mf=importlib.util.module_from_spec(spec);spec.loader.exec_module(mf)
VERSION='partial-quotient-v1'
KP={'db_id':17592186124643,'id':'59c3f441-0499-575c-af10-b597d61e6e35','title':'Partial Derivatives as Limits of Difference Quotients'}
TEMPLATES={r['template']:r for r in json.loads((ASSETS/'templates.json').read_text())}
LEVELS=('easy','moderate','hard')
DOMAINS={'monomial':{'a':range(1,10),'n':range(2,6)},'root_product':{},'exponential_linear':{'b':range(2,10),'c':range(2,10)},'log_linear':{'c':range(2,10)},'rational':{'p':range(2,6),'q':range(2,6),'a':range(1,10)},'exponential_product':{'b':range(2,10)},'cube_root':{'p':range(2,6)},'log_product':{'a':range(2,10)},'variable_power_exponent':{},'variable_power_base':{},'cosine':{'p':range(2,6)},'sine_product':{}}

def uid(*parts):return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(parts,ensure_ascii=False,sort_keys=True,separators=(',',':'))))
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def guard(value):
    if any(ord(c)<32 and c not in '\n\t' for c in value):raise ValueError('C0 control character in learner content')
    return value

def swap_variables(text):
    def letters(value):
        return re.sub(r'\\[A-Za-z]+|[xy]',lambda m:m[0] if m[0].startswith('\\') else {'x':'y','y':'x'}[m[0]],value)
    def math(value):
        # A coordinate swap in the expression also swaps argument roles;
        # always retain the public ordered function signature f(x,y).
        calls=[]
        def protect(m):
            parts=m[1].split(',')
            replacement='f('+','.join(letters(p.strip()) for p in reversed(parts))+')' if len(parts)==2 else letters(m[0])
            calls.append(replacement);return 'CALLSLOT'+str(len(calls)-1)+'END'
        value=re.sub(r'f\(([^()]*)\)',protect,value)
        value=letters(value)
        for i,call in enumerate(calls):value=value.replace('CALLSLOT'+str(i)+'END',call)
        return value
    return mf.MATH.sub(lambda m:math(m[0]),text) if '$' in text else math(text)

def fill(mask,parameters):
    for key,value in parameters.items():
        if key!='swap':mask=mask.replace('@@'+key+'@@',str(value))
    if '@@' in mask:raise ValueError('Unfilled parameter slot')
    return swap_variables(mask) if parameters.get('swap') else mask

def typography(text):
    text=text.replace('∂',r'\partial ').replace('⁡','').replace('{lim}',r'\lim')
    text=text.replace('lim_(h → 0)',r'\lim_{h\to 0}')
    return text

def tex(text):return guard(mf.normalize_tex(typography(text)))
def prose(text):return guard(mf.normalize_prose(typography(text)))
def raw_prose(text):return guard(mf.normalize_prose(text))
def raw_tex(text):return guard(mf.normalize_tex(text))

def parameters_for(template,rng,parameters):
    spec=TEMPLATES[template];domain=DOMAINS[template]
    if parameters is None:return {k:rng.choice(list(v)) for k,v in domain.items()}|{'swap':rng.choice([False,True])}
    p=dict(parameters)
    if set(p)-set(domain)-{'swap'}:raise ValueError('Unknown parameter')
    if set(domain)-set(p):raise ValueError('Missing mathematical parameter')
    p.setdefault('swap',False)
    if type(p['swap']) is not bool:raise ValueError('swap must be boolean')
    for k,v in domain.items():
        if type(p[k]) is not int or p[k] not in v:raise ValueError('Parameter outside workload bounds: '+k)
    return p

def symbolic_parts(template,p):
    """Only used for canonical fingerprints; independent validator reads TeX."""
    x,y=S.symbols('x y',real=True)
    if template=='monomial':v=p['a']*x**p['n']*y
    elif template=='root_product':v=x*S.sqrt(y)
    elif template=='exponential_linear':v=p['b']**(x+p['c']*y)
    elif template=='log_linear':v=S.log(x+p['c']*y)
    elif template=='rational':v=x**p['p']/(y+p['a'])**p['q']
    elif template=='exponential_product':v=p['b']**(x*y)
    elif template=='cube_root':v=(x**p['p']-y)**S.Rational(1,3)
    elif template=='log_product':v=S.log(p['a']*x*y)
    elif template.startswith('variable_power'):v=x**y
    elif template=='cosine':v=S.cos(x-y**p['p'])
    elif template=='sine_product':v=S.sin(x*y)
    else:raise ValueError('Unknown family')
    t=TEMPLATES[template]['target']
    if p['swap']:v=v.xreplace({x:y,y:x});t={'x':'y','y':'x'}[t]
    return v,t

def standard_content(template,p,profile):
    sp=TEMPLATES[template];raw=profile=='observed'
    normp=raw_prose if raw else prose;normt=raw_tex if raw else tex
    prompt=normp(fill(sp['prompt_mask'],p));solution=normp(fill(sp['solution_mask'],p)) if sp['source_solution_present'] else None
    values=[normt(fill(s,p)) for s in sp['bank_masks']]
    target={'x':'y','y':'x'}[sp['target']] if p['swap'] else sp['target'];held={'x':'y','y':'x'}[target]
    if not raw:
        if solution:solution=solution.replace('$f(x)=','$f(x,y)=').replace('$f(y)=','$f(x,y)=')
        if template=='root_product':
            expr=fill(r'x\sqrt{y}',p);shift=fill(r'x\sqrt{y+h}',p)
            pair='x,y+h' if target=='y' else 'x+h,y'
            definition=tex(r'\lim_{h\to 0}(\frac{f('+pair+r')-f(x,y)}{h})')
            solution=prose('The derivative of $f$ with respect to $'+target+'$ is given by the limit \n\n$$\n'+r'\frac{\partial f}{\partial '+target+'}='+definition+'.\n$$\n\nSince $f(x,y)='+expr+',$  we have that \n\n$$\nf('+pair+')='+shift+'.\n$$\n\nTherefore,\n\n$$\n'+r'\frac{\partial f}{\partial '+target+'}='+values[sp['correct_index']]+'.\n$$')
        if template=='exponential_linear':
            # Replace the unexplained yy source option with a complete authored
            # held-coordinate increment recipe; the raw bank stays public.
            b,c=p['b'],p['c'];expr=r'{'+str(b)+r'}^{x+'+str(c)+r'(y+h)}';base=r'{'+str(b)+r'}^{x+'+str(c)+r'y}'
            values[3]=tex(fill(r'\lim_{h\to 0}(\frac{'+expr+'-'+base+r'}{h})',{'swap':p['swap']}))
        solution=prose(solution+'\n\nHere $h\\ne 0$ before taking the limit, and $'+held+'$ is held constant.')
    return prompt,solution,values,target,held

# Shared field-owned record assembly. Choice order is not content identity.
def assemble(level,seed,template,p,profile,prompt,solution,values,correct_index,target,held,raw=False,mathkey=None):
    if len(values)!=5 or len(set(values))!=5:raise ValueError('Whole bank rejected: repeated displayed option')
    content={'version':VERSION,'level':level if not raw or TEMPLATES[template]['source_difficulty_present'] else None,'prompt':prompt,'solution':solution,'bank':sorted(values),'correct':values[correct_index] if not raw or TEMPLATES[template]['source_correct_present'] else None,'profile':profile}
    qid=uid('question',KP['id'],content);fid=uid(qid,'field','selection')
    answers=[{':answer/id':uid(fid,'answer',value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if not raw or TEMPLATES[template]['source_correct_present']:field[':answer-field/correct']=[':answer/id',answers[correct_index][':answer/id']]
    random.Random(seed).shuffle(answers)
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not raw or TEMPLATES[template]['source_difficulty_present']:q[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:q[':question/worked-solution']=solution
    if raw:
        for value in [prompt,solution or '',*values]:guard(value)
    else:mf.validate_generated_record({'question':q})
    return {'knowledge_point':dict(KP),'question':q,'generation':{'version':VERSION,'template':template,'profile':profile,'bank_profile':profile,'seed':seed,'parameters':p,'source_id':TEMPLATES[template]['source_id'] if template in TEMPLATES else None,'source_basis':2275,'source_lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','eligible_for_learning':not raw,'evidence_only':raw,'authored':level=='hard' or profile=='method','target_variable':target,'held_variable':held,'domain':'h != 0 before limit; all supplied and incremented function arguments in real domain','mathematical_fingerprint':digest(mathkey),'content_fingerprint':digest(content),'dependencies':{'python':sys.version.split()[0],'sympy':S.__version__},'math_format':mf.FORMAT_VERSION}}

# Easy and moderate: symbolic function values, with no limit evaluation.
def generate_standard(level,seed=0,template=None,parameters=None,profile=None):
    rng=random.Random(seed);profile=profile or 'method'
    if profile not in ('method','observed'):raise ValueError('Unsupported bank profile')
    eligible=[k for k,v in TEMPLATES.items() if v['level']==level]
    template=template or rng.choice(eligible)
    if template not in eligible:raise ValueError('Family does not belong to supplied difficulty')
    p=parameters_for(template,rng,parameters)
    prompt,solution,values,t,u=standard_content(template,p,profile)
    expr,target=symbolic_parts(template,p)
    x,y=S.symbols('x y',real=True);canonical=expr.xreplace({(x if target=='x' else y):S.Symbol('T'),(y if target=='x' else x):S.Symbol('U')})
    return assemble(level,seed,template,p,profile,prompt,solution,values,TEMPLATES[template]['correct_index'],t,u,profile=='observed',{'task':'form-symbolic-quotient','function_up_to_additive_held_data':S.srepr(S.simplify(S.diff(canonical,S.Symbol('T'))))})

# Hard: authored point-specialized quotient. No analytic differentiation occurs.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio shape is supported')
    if profile not in (None,'method'):raise ValueError('Hard has no observed source profile')
    rng=random.Random(seed);template=template or rng.choice(['point_monomial','point_sine'])
    if template not in ('point_monomial','point_sine'):raise ValueError('Unknown hard family')
    allowed={'a','X','Y','swap'} if template=='point_monomial' else {'X','Y','swap'}
    if parameters is None:
        eligible=[{'X':X,'Y':Y,'swap':swap}|({'a':a} if template=='point_monomial' else {}) for X in [-3,-2,-1,1,2,3] for Y in [-3,-2,-1,1,2,3] for swap in [False,True] for a in ([-5,-4,-3,-2,-1,1,2,3,4,5] if template=='point_monomial' else [1]) if (abs(a*((Y if swap else X)**2)*(X if swap else Y))<=24 if template=='point_monomial' else X!=Y)]
        p=rng.choice(eligible)
    else:p=dict(parameters)
    p.setdefault('swap',False)
    if set(p)!=allowed or type(p['swap']) is not bool:raise ValueError('Hard parameter keys')
    for k in allowed-{'swap'}:
        if type(p[k]) is not int or p[k] not in ([-5,-4,-3,-2,-1,1,2,3,4,5] if k=='a' else [-3,-2,-1,1,2,3]):raise ValueError('Hard arithmetic cap')
    if template=='point_monomial' and abs(p['a']*((p['Y'] if p['swap'] else p['X'])**2)*(p['X'] if p['swap'] else p['Y']))>24:raise ValueError('Hard evaluated monomial arithmetic cap is 24')
    if template=='point_sine' and p['X']==p['Y']:raise ValueError('Whole sine bank collides at equal coordinates')
    X,Y=p['X'],p['Y'];t='y' if p['swap'] else 'x';u='x' if p['swap'] else 'y';base=Y if p['swap'] else X;held=X if p['swap'] else Y
    if template=='point_monomial':
        a=p['a'];function=fill(str(a)+r'{x}^{2}y',p);F=lambda A,B:str(a)+'('+A+r')^{2}('+B+')'
    else:
        function=fill(r'\operatorname{sin}(xy)',p);F=lambda A,B:r'\operatorname{sin}(('+A+')('+B+'))'
    f0=F(str(base),str(held));fc=F(str(base)+'+h',str(held));fo=F(str(base),str(held)+'+h');fb=F(str(base)+'+h',str(held)+'+h')
    Q=lambda A,B,sign='-':tex(r'\lim_{h\to 0}(\frac{('+A+')'+sign+'('+B+r')}{h})')
    values=[Q(fc,f0),Q(fo,f0),Q(fb,f0),Q(fc,f0,'+'),Q(f0,fc)]
    pair=(str(X)+', '+str(Y)+'+h') if t=='y' else (str(X)+'+h, '+str(Y))
    prompt=prose('Given that $f(x,y)='+function+',$ express $f_'+t+'('+str(X)+','+str(Y)+')$ as the limit of a difference quotient.')
    formal=tex(r'\lim_{h\to 0}(\frac{f('+pair+')-f('+str(X)+','+str(Y)+r')}{h})')
    solution=prose('The partial derivative of $f$ with respect to $'+t+'$ is given by the limit\n\n$$\nf_'+t+'('+str(X)+','+str(Y)+')='+formal+'.\n$$\n\nSince $f(x,y)='+function+',$ we have that\n\n$$\nf('+pair+')='+fc+r',\qquad f('+str(X)+','+str(Y)+')='+f0+'.\n$$\n\nTherefore,\n\n$$\nf_'+t+'('+str(X)+','+str(Y)+')='+values[0]+'.\n$$\n\nHere $h\\ne 0$ before taking the limit, and $'+u+'='+str(held)+'$ is held constant.')
    x,y=S.symbols('x y',real=True);fun=(p['a']*(y*y*x if p['swap'] else x*x*y)) if template=='point_monomial' else S.sin(x*y)
    h=S.Symbol('h',real=True);target=x if t=='x' else y
    assessed=((fun.subs(target,target+h)-fun)/h).subs({x:X,y:Y},simultaneous=True)
    return assemble('hard',seed,template,p,'method',prompt,solution,values,0,t,u,False,{'task':'form-point-quotient','increment_expression':S.srepr(S.expand(assessed))})

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio shape is supported')
    return generate_hard(seed,template,field_type,parameters,profile) if level=='hard' else generate_standard(level,seed,template,parameters,profile)

def markdown(record):
    q=record['question'];difficulty=q.get(':question/difficulty','unrated').split('/')[-1]
    rows=['### '+difficulty+' — '+record['generation']['template']+' — bank profile: '+record['generation']['bank_profile'],q[':question/problem']]
    for field in q.get(':question/answer-fields',[]):
        ref=field.get(':answer-field/correct',[None,None])[1]
        for i,a in enumerate(field[':answer-field/choices']):rows.append(str(i+1)+'. $'+a[':answer/value']+'$'+(' **Correct**' if a[':answer/id']==ref else ''))
        if ref is None:rows.append('Original correct designation absent; evidence only.')
    rows.extend(['Worked solution:',q.get(':question/worked-solution','Original worked solution absent.')]);return '\n\n'.join(rows)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=[*LEVELS,'all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile',choices=['method','observed'])
    args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (LEVELS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
