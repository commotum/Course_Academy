#!/usr/bin/env python3
"""First-order IVP recognition, fixed basis 1356; steps 3–7 only.

Eleven observed easy recipes preserve complete three-checkbox banks and fixed
solution paragraphs. Source replay is public: profile='observed_raw', template
'source_q-...', and source-cases.json parameters. Recipes replace complete ODE
and initial-condition components, never arbitrary numerals throughout prose.
Raw evidence is explicitly ineligible for default learner sampling. Singularity
is not a classification test: a formal IVP need not have a solution. Normal
sampling simply chooses regular points; no existence theorem is assessed.

Authored easy: three simple prime-notation ODEs, orders 1/2. Moderate: orders
1/2/3, one lower-order term, chained initial conditions. Hard: same IVP
criterion with nested derivative groups and mixed prime/Leibniz notation, at
most third order. No integration, solution verification or domain quiz.
These missing-level distinctions are authored, not recovered difficulty labels.
All three levels use the original checkbox response layout and boolean banks.
Numerical coefficients/initial points are incidental to this categorical skill;
semantic fingerprints exclude them and variable-letter aliases.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID = 17592186166815
KP_UUID = '13e08fd0-4f41-56eb-8650-b72aa739b7a1'
TITLE = 'Initial Value Problems and Initial Conditions'
VERSION = 'ivp-recognition-v1'
HERE = Path(__file__).with_suffix('')
CAPTURE = json.loads((HERE/'source.json').read_text())
SOURCE = {k:CAPTURE[k] for k in ('database','basis','lineage')}
SOURCES = {q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
KEYS = ('I','II','III')
TYPES = {
 'easy':('ivp','missing','second','second_missing'),
 'moderate':('ivp','missing','second','third','second_missing'),
 'hard':('ivp','missing','second','third','second_missing'),
}
CATALOG = {level:[list(c) for c in itertools.product(types,repeat=3)
                 if 0<c.count('ivp')<3 and (level=='easy' or any(k in ('second','third','second_missing') for k in c))]
           for level,types in TYPES.items()}
OPENING = SOURCES['q-95985'][':question/worked-solution'].split('\n\n- System I')[0]

# Whole ODE components. Exponents are fixed structure; @a@ etc. are coefficient
# slots, not fitted wrong values. Every boolean follows order + condition type.
ODE_RECIPES = {
 'q-95985':(r'@a@x{y}^{′}=y',r'{y}^{′}-@b@xy={e}^{y}',r'@c@x{y}^{″}={y}^{′}'),
 'q-96986':(r'\frac{1}{@a@}{x}^{2}{y}^{″}=@b@{y}^{′}',r'@c@{x}^{2}{y}^{′}=y',r'@d@{y}^{′}-\frac{1}{@e@}xy=\operatorname{ln}⁡y'),
 'q-118786':(r'(1+{x}^{2}){y}^{′}=@a@y',r'@b@{y}^{′}-xy=@c@',r'@d@{y}^{″}=@e@y'),
 'q-96987':(r'{x}^{2}{y}^{\'\'}-y=@a@x',r'x{y}^{‴}-{e}^{x}{y}^{\'}=@b@y',r'@c@{y}^{\'}-\frac{1}{x}={e}^{y}'),
 'q-96992':(r'@a@{x}^{2}{y}^{′}={y}^{2}',r'\frac{{y}^{′}}{@b@}-{x}^{2}{y}^{2}=y',r'{y}^{′}-x\sqrt{y}={e}^{x}'),
 'q-118787':(r'{y}^{′}-x=-@a@y',r'{x}^{4}{y}^{‴}+@b@y={@c@}^{y}',r'x{y}^{″}-@d@y=@e@'),
 'q-118788':(r'{x}^{2}{y}^{‴}+@a@{x}^{3}{y}^{′}=-@b@y',r'x{y}^{′}+{e}^{x}y=@c@',r'@d@{y}^{″}+xy={e}^{x}'),
 'q-118790':(r'{y}^{′}=-@a@x',r'{y}^{′}-@b@{x}^{3}=-y',r'{y}^{″}+y=@c@'),
 'q-118791':(r'{y}^{‴}+{y}^{″}+{y}^{′}+y=0',r'{y}^{′}\operatorname{ln}⁡x+y={@a@}^{x}',r'\sqrt{x}{y}^{′}+{e}^{x}y=@b@'),
 'q-96988':(r'@a@x-{y}^{′}=\frac{1}{y}',r'@b@{y}^{′}-@c@{e}^{x}y={y}^{2}',r'@d@x{y}^{″}-\frac{1}{x}={y}^{′}'),
 'q-96990':(r'{x}^{3}{y}^{′}-\sqrt{x}=\operatorname{ln}⁡y',r'\sqrt{x}{y}^{‴}-x{y}^{′}=\frac{y}{@a@}',r'\sqrt{@b@}{y}^{′}-@c@x=@d@y'),
}
# Python raw strings above retain escaped quotes literally; the source uses
# ordinary ASCII prime bytes for q-96987. Normalize ONLY these recipe tokens.
ODE_RECIPES['q-96987'] = tuple(t.replace("\\'", "'") for t in ODE_RECIPES['q-96987'])
COEFFICIENTS = {
 'q-95985':dict(a=2,b=2,c=2), 'q-96986':dict(a=2,b=3,c=2,d=4,e=3),
 'q-118786':dict(a=8,b=8,c=3,d=3,e=4), 'q-96987':dict(a=2,b=9,c=2),
 'q-96992':dict(a=3,b=2), 'q-118787':dict(a=7,b=3,c=2,d=6,e=14),
 'q-118788':dict(a=9,b=7,c=6,d=6), 'q-118790':dict(a=9,b=8,c=3),
 'q-118791':dict(a=3,b=6), 'q-96988':dict(a=2,b=3,c=2,d=2),
 'q-96990':dict(a=4,b=3,c=3,d=2),
}

def source_components(q):
    systems = re.findall(r'- \*\*(?:I|II|III)\.\*\* \$(.*?)\$',q[':question/problem'])
    assert len(systems)==3
    return [s.split(r',\,',1) for s in systems]

def source_defaults(sid):
    """Extract initial-value slots within complete component boundaries."""
    p=dict(COEFFICIENTS[sid]);p['conditions']=[]
    for component in source_components(SOURCES[sid]):
        if len(component)==1:p['conditions'].append(None);continue
        c=component[1]
        parts=c.split(r',\,')
        point=re.search(r'\(([^()]*)\)',parts[0]).group(1)
        values=[part.rsplit('=',1)[1] for part in parts]
        p['conditions'].append({'point':point,'values':values})
    return p

DEFAULTS = {sid:source_defaults(sid) for sid in SOURCES}

def slots(template,p):
    return re.sub(r'@([a-z])@',lambda m:str(p[m[1]]),template)

def math_slots(text,mapping):
    """Simultaneous complete-component masks confined to math spans."""
    def replace(m):
        value=m[0]
        tokens={}
        for i,(old,new) in enumerate(sorted(mapping.items(),key=lambda kv:-len(kv[0]))):
            token=f'@@COMPONENT{i}@@';value=value.replace(old,token);tokens[token]=new
        for token,new in tokens.items():value=value.replace(token,new)
        return value
    return re.sub(r'\$\$.*?\$\$|\$[^$]*\$',replace,text,flags=re.S)

def render_observed(sid,p):
    original=SOURCES[sid];parts=source_components(original)
    prompt_lines=original[':question/problem'].split('\n- **')
    sol=original[':question/worked-solution'].split('\n\n- System ')
    for i,(component,ct) in enumerate(zip(parts,p['conditions'])):
        mapping={component[0]:slots(ODE_RECIPES[sid][i],p)}
        if len(component)>1:
            for j,fragment in enumerate(component[1].split(r',\,')):
                # One point slot per system; retain chains and derivative order.
                new=re.sub(r'\([^()]*\)',lambda _: '('+ct['point']+')',fragment)
                new=new.rsplit('=',1)[0]+'='+ct['values'][j]
                mapping[fragment]=new
                # Some source third-order solutions split the final condition
                # with prose "and". Each whole fragment remains a separate slot.
        prompt_lines[i+1]=math_slots(prompt_lines[i+1],mapping)
        sol[i+1]=math_slots(sol[i+1],mapping)
    return '\n- **'.join(prompt_lines),'\n\n- System '.join(sol)

def derivative_orders(tex):
    prime={'′':1,'″':2,'‴':3,"'":1,"''":2,"'''":3}
    orders=[prime[m] for m in re.findall(r'\{y\}\^\{(′|″|‴|\'{1,3})\}',tex)]
    orders += [int(k or 1) for k in re.findall(r'\\(?:dfrac|frac)\{d(?:\^\{?([23])\}?)?y\}\{dx(?:\^\{?[23]\}?)?\}',tex)]
    return orders

def classify_system(system):
    """Classification from rendered system, not stored source correct refs."""
    equation=system.split(r',\,',1)[0]
    equation=equation.split(r',\quad',1)[0]
    orders=derivative_orders(equation)
    if not orders:raise ValueError('No ordinary derivative in system')
    condition=system[len(equation):]
    has_function_value=re.search(r'(?<![A-Za-z])y\([^()]*\)\s*=',condition) is not None
    return max(orders)==1 and has_function_value

def prompt_systems(problem):
    return re.findall(r'- \*\*(?:I|II|III)\.\*\* \$(.*?)\$',problem)

def scalar_allowed(value):
    return isinstance(value,str) and bool(re.fullmatch(r'-?\d+|\\operatorname\{(?:ln|cos)\}⁡[2-4]',value))

def guard_observed(sid,p,raw):
    expected=set(DEFAULTS[sid]);
    if set(p)!=expected:raise ValueError('Exact source parameter keys required')
    for key in expected-{'conditions'}:
        if isinstance(p[key],bool) or not isinstance(p[key],int) or not 1<=p[key]<=14:raise ValueError('Observed coefficient bound 1..14')
    if not isinstance(p['conditions'],list) or len(p['conditions'])!=3:raise ValueError('Three condition layouts required')
    for i,(ct,original) in enumerate(zip(p['conditions'],DEFAULTS[sid]['conditions'])):
        if original is None:
            if ct is not None:raise ValueError('Do not add a source condition')
            continue
        if not isinstance(ct,dict) or set(ct)!={'point','values'}:raise ValueError('Condition slots required')
        if not scalar_allowed(ct['point']):raise ValueError('Point is a small constant expression')
        if ct['point'].lstrip('-').isdigit() and abs(int(ct['point']))>4:raise ValueError('Point magnitude <=4')
        if not isinstance(ct['values'],list) or len(ct['values'])!=len(original['values']):raise ValueError('Condition layout is fixed')
        if not all(isinstance(v,str) and re.fullmatch(r'-?\d+',v) and abs(int(v))<=6 for v in ct['values']):raise ValueError('Initial-value magnitude <=6')
        if ct['point'].lstrip('-').isdigit():point=sp.Integer(ct['point'])
        else:
            m=re.fullmatch(r'\\operatorname\{(ln|cos)\}⁡([2-4])',ct['point'])
            point=(sp.log if m[1]=='ln' else sp.cos)(int(m[2]))
        # Domain restrictions are generation guards, never extra quiz branches.
        # Permit captured sqrt(0) and singular-but-defined coefficients; reject
        # new undefined logarithm/radical inputs in either public profile.
        if (sid=='q-96990' and i in (0,1) or sid=='q-118791' and i==2) and point.is_negative:raise ValueError('Square-root input requires nonnegative initial point')
        if sid=='q-118791' and i==1 and point.is_positive is not True:raise ValueError('Logarithm requires positive initial point')
        if sid=='q-96990' and i==0 and int(ct['values'][0])<=0:raise ValueError('Logarithm requires positive initial function value')
        if not raw and (not ct['point'].isdigit() or int(ct['point'])<2):raise ValueError('Normal observed variants restrict all points to 2..4, without assessing regularity')

def authored_parameters(level,rng):
    return {'kinds':rng.choice(CATALOG[level]),'a':[rng.randint(2,5) for _ in KEYS],
            'b':[rng.randint(1,5) for _ in KEYS],'points':[rng.randint(2,4) for _ in KEYS],
            'values':[rng.randint(-5,5) for _ in KEYS]}

def guard_authored(level,p):
    if set(p)!={'kinds','a','b','points','values'}:raise ValueError('Exact authored parameter keys required')
    if p['kinds'] not in CATALOG[level]:raise ValueError('Unsupported categorical structure')
    for key,lo,hi in [('a',2,5),('b',1,5),('points',2,4),('values',-5,5)]:
        if not isinstance(p[key],list) or len(p[key])!=3 or any(isinstance(v,bool) or not isinstance(v,int) or not lo<=v<=hi for v in p[key]):raise ValueError(f'{level} {key} must be three integers {lo}..{hi}')

def prime(n):return '{y}^{'+('′','″','‴')[n-1]+'}'
def leibniz(n):return r'\dfrac{dy}{dx}' if n==1 else rf'\dfrac{{d^{n}y}}{{dx^{n}}}'

def conclusion(truth):
    selected=[key for key,t in zip(KEYS,truth) if t]
    return ' and '.join(selected)+' only.'

def render_authored(level,p):
    systems=[];paragraphs=[]
    for i,(key,kind) in enumerate(zip(KEYS,p['kinds'])):
        order={'second':2,'second_missing':2,'third':3}.get(kind,1)
        a,b,t,v=(p[k][i] for k in ('a','b','points','values'))
        if level=='easy':eq=f'{a}{prime(order)}={b}x+y'
        elif level=='moderate':eq=f'({a}+x^2){prime(order)}+{b}'+(prime(1) if order>1 else 'y')+'={e}^{x}'
        else:
            # Nested whole factors and two derivative appearances. All remain
            # linear in the highest derivative; nothing is solved or evaluated.
            eq=f'({a}+x^2)\\left({leibniz(order)}-{b}y\\right)+x'+prime(1)+'={e}^{x}'
        if kind in ('missing','second_missing'):condition=''
        elif order==1:condition=f'y({t})={v}'
        elif level=='easy':condition=f'y({t})={v}'+r',\,'+prime(1)+f'({t})={v+1}'
        elif level=='moderate':condition='='.join([f'y({t})']+[prime(k)+f'({t})' for k in range(1,order)])+f'={v}'
        else:condition=r',\,'.join([f'y({t})={v}']+[prime(k)+f'({t})={v+k}' for k in range(1,order)])
        system=eq+(r',\,'+condition if condition else '');systems.append(system)
        if kind=='ivp':description=f'is a first-order initial value problem. It consists of a first-order differential equation ${eq}$ together with the initial condition ${condition}.$'
        elif kind in ('missing',):description='is not a first-order initial value problem. We have a first-order ordinary differential equation, but there is no initial condition.'
        else:
            name=('second' if order==2 else 'third')
            if condition:description=f'is not a first-order initial value problem. It consists of a *{name}*-order differential equation ${eq}$ together with *'+('two' if order==2 else 'three')+f'* initial conditions ${condition}.$ This is a {name}-order initial value problem.'
            else:description='is not a first-order initial value problem. We have here a second-order ordinary differential equation.'
        paragraphs.append(f'- System {key} '+description)
    truth=[classify_system(s) for s in systems]
    prompt='Which of the following systems is a first-order initial value problem?\n\nSelect all that apply.\n\n'+'\n'.join(f'- **{k}.** ${s}$' for k,s in zip(KEYS,systems))
    solution=OPENING+'\n\n'+'\n\n'.join(paragraphs)+'\n\nTherefore, the correct answer is "'+conclusion(truth)+'"'
    return prompt,solution

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(value):return str(uuid.uuid5(uuid.NAMESPACE_URL,value))

def package(level,seed,template,profile,p,prompt,solution,source_ids,raw,semantic):
    truths=[classify_system(s) for s in prompt_systems(prompt)]
    assert len(truths)==3
    identity=digest([VERSION,level,prompt,solution,[[k,['false','true'],truth] for k,truth in zip(KEYS,truths)]])
    fields=[];rng=random.Random(seed)
    for key,truth in zip(KEYS,truths):
        fuid=uid(identity+'/field/'+key)
        choices=[{':answer/id':uid(fuid+'/'+v),':answer/type':':answer.type/text',':answer/value':v} for v in ('false','true')]
        rng.shuffle(choices)
        fields.append({':answer-field/id':fuid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fuid+'/'+str(truth).lower())]})
    q={':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
            'generation':{'version':VERSION,'source':SOURCE,'template':template,'profile':profile,'seed':seed,'parameters':p,'source_ids':source_ids,'evidence_only':raw,'eligible_for_learning':not raw,'authored':not raw,'content_fingerprint':identity,'mathematical_fingerprint':digest(semantic),'domain':'Structural IVP recognition, not existence/uniqueness; default initial points 2..4.','plots':[],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in TYPES:raise ValueError('Unknown difficulty')
    if field_type not in (None,'checkbox',':answer-field.type/checkbox'):raise ValueError('Only observed checkbox fields supported')
    rng=random.Random(seed)
    template=template or 'authored_'+level
    if template.startswith('source_'):
        sid=template[len('source_'):]
        if sid not in SOURCES or level!='easy':raise ValueError('Observed templates are easy only')
        if profile not in (None,'observed_raw','observed_regular','observed_domain_repair'):raise ValueError('Unsupported observed profile')
        repair=profile=='observed_domain_repair'
        if repair and sid!='q-96987':raise ValueError('Domain repair belongs only to q-96987')
        raw=profile=='observed_raw';profile=profile or 'observed_regular'
        if parameters is None:
            p=json.loads(json.dumps(DEFAULTS[sid]))
            if repair:p['conditions'][2]['point']='2'
            elif not raw:
                for key in sorted(set(p)-{'conditions'}):p[key]=rng.randint(2,9)
                for i,ct in enumerate(p['conditions']):
                    if ct:
                        ct['point']=str(rng.randint(2,4));ct['values']=[str(rng.randint(1,6)) for v in ct['values']]
        else:p=json.loads(json.dumps(parameters))
        guard_observed(sid,p,raw or repair)
        if repair and p['conditions'][2]['point'] not in ('1','2','3','4'):raise ValueError('Repair requires a nonzero small positive point for 1/x')
        prompt,solution=render_observed(sid,p)
        semantic=['recognize_first_order_ivp',sorted((max(derivative_orders(c[0])),len(c)>1) for c in source_components(SOURCES[sid]))]
        return package(level,seed,template,profile,p,prompt,solution,[sid],raw,semantic)
    if template!='authored_'+level or profile not in (None,'authored_boolean'):raise ValueError('Template/profile difficulty mismatch')
    p=authored_parameters(level,rng) if parameters is None else json.loads(json.dumps(parameters))
    guard_authored(level,p);prompt,solution=render_authored(level,p)
    semantic=['recognize_first_order_ivp',{'easy':'simple_prime','moderate':'prime_with_lower_derivative','hard':'nested_mixed_derivative_notation'}[level],sorted(p['kinds'])]
    return package(level,seed,template,'authored_boolean',p,prompt,solution,[],False,semantic)

# EASY: observed labels preserved; normal scope has only prime order 1 or 2,
# one derivative per ODE and <=5 coefficients. 9 semantic category multisets,
# rendered in 36 ordered layouts. Reordering systems does not add a task.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE (authored): third order, lower derivative term and condition chains;
# exactly three systems, <=5 coefficients, no algebraic operations required.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD (authored): nested factor containing a Leibniz derivative, another prime
# derivative outside the factor, and separately supplied derivative conditions.
# Order <=3 and the same <=5 coefficient ceiling; no solving or expansion quiz.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];gen=record['generation']
    level=q.get(':question/difficulty','').rsplit('/',1)[-1] or 'unrated'
    original=gen['evidence_only'] and gen['source_ids'] and gen['parameters']==DEFAULTS[gen['source_ids'][0]]
    kind='Original source replay' if original else ('Generated evidence variant' if gen['evidence_only'] else 'Generated')
    lines=[f'## {kind} — {level}',q[':question/problem'],'','Worked solution:',q.get(':question/worked-solution','')]
    for f in q.get(':question/answer-fields',[]):
        selected=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        lines.append(f"{f[':answer-field/key']}: {selected}; complete bank false / true")
    return '\n\n'.join(lines)

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile')
    args=a.parse_args()
    if args.count<1:a.error('count must be positive')
    levels=TYPES if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':main()
