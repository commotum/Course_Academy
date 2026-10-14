#!/usr/bin/env python3
"""Identifying homogeneous ODEs; math basis 2275, local review only.

Six complete observed families, seven complete observed radio banks. The source
texts are operative expression masks: simultaneous coordinate factors populate
all formula occurrences, including implicit xy, the distinct distributed/factored
scaling chains, and conclusions. There is no original-parameter payload branch.
Raw evidence retains both q-8739 fields and q-14322's erroneous witness/rule;
normal learning uses the supported field and a minimally repaired witness/rule.
See companion extraction, validation and review artifacts. No database access.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186087888
KP_UUID='e8c2a855-07a3-5855-9f6c-1a914953ac53'
TITLE='Identifying Homogeneous Differential Equations'
VERSION='homogeneous-recognition-2275-v1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
TEMPLATES={'quadratic_product':'q-8739','cubic_quotient':'q-14319','quadratic_difference':'q-8369',
           'linear_not':'q-8741','constant_offset_not':'q-14322','quadratic_not':'q-90597'}
LEVELS={'easy':['quadratic_product','cubic_quotient','quadratic_difference'],
        'moderate':['linear_not','constant_offset_not','quadratic_not'],
        'hard':['cubic_quotient','quadratic_difference']}
X,Y,T=sp.symbols('x y t',positive=True)
# Exact independent mathematical source expressions, all options, in captured order.
BANKS={
'q-8739':[[X**2*Y/(X**2+Y**2),2*X*Y/(X**2+Y**2),X**2*Y**2/(X**2+Y**2),X*Y**2/(X**2+Y**2),X*Y/(X+Y)],
 [X*Y**2/(X**2+Y**2),X*Y/(X+Y),X**2*Y**2/(X**2+Y**2),2*X*Y/(X**2+Y**2),X**2*Y/(X**2+Y**2)]],
'q-14319':[[(Y**2*X-X**2)/(Y**2+X**2),(X**3-3*X**2*Y+X*Y**2)/(Y**3+X**3),
 (X**3-3*X*Y+X*Y)/(Y**2-X**2),(Y**3-X**2*Y+X**3)/(Y**3+1),(X**2-X*Y**2+Y**2)/(1+X**2)]],
'q-8369':[[(Y**2-X**2)/(Y**2+X),(Y**2-X)/(Y**2+X**2),(Y**2-X**2)/(Y**2+X**2),(Y-X**2)/(Y**2+X**2),(Y**2-X**2)/(Y-X**2)]],
'q-8741':[[sp.Integer(1),sp.log(Y)-sp.log(X),X,sp.atan(X/Y),sp.Integer(2)]],
'q-14322':[[X*Y/(X**2+Y**2),sp.sin((X+Y)/Y),(X**2+1)/(Y**2+X*Y),sp.exp(sp.sin(X/Y)),4*X**2*Y/(X**3+X*Y**2)]],
'q-90597':[[Y**2/(X**2+X*Y),sp.cos(X/(2*Y)),Y**2/2,sp.sin(X**3/Y**3),sp.Integer(9)]]}


def uid(value):return str(uuid.uuid5(uuid.UUID(KP_UUID),value))
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

# Protect complete formal notation first, then substitute coordinate tokens in a
# single lexical pass. Commands consume their entire name; adjacent xy is two
# tokens. Newly inserted factors are never rescanned.
DERIVATIVE=re.compile(r'\\frac\{\\text\{d\}y\}\{\\text\{d\}x\}|\\frac\{dy\}\{dx\}')
FUNCTION=re.compile(r'f\([^()]*\)')
TOKEN=re.compile(r'\\[A-Za-z]+|[xy]')
def scale_math(text,sx,sy):
    protected=[]
    def shield(m):
        protected.append(m.group());return f'§{len(protected)-1}§'
    text=DERIVATIVE.sub(shield,text)
    text=FUNCTION.sub(shield,text)
    text=TOKEN.sub(lambda m: ('x' if sx==1 else f'({sx}x)') if m.group()=='x' else
                  ('y' if sy==1 else f'({sy}y)') if m.group()=='y' else m.group(),text)
    return re.sub(r'§(\d+)§',lambda m:protected[int(m.group(1))],text)

def scale_markdown(text,sx,sy):
    pieces=re.split(r'(\$\$[\s\S]*?\$\$|\$[^$]*?\$)',text)
    return ''.join(scale_math(v,sx,sy) if v.startswith('$') else v for v in pieces)

def witness(p):
    a,b,u,v,t=(p[k] for k in ('sx','sy','x0','y0','t'))
    def parts(xx,yy):return (a*xx)**2+1,(b*yy)**2+(a*xx)*(b*yy)
    ns,ds=parts(t*u,t*v);n,d=parts(u,v)
    scaled=sp.Rational(ns,ds);base=sp.Rational(n,d)
    first=(r'\begin{aligned}f(tx,ty) & =f('+str(t)+r'\cdot '+str(u)+','+str(t)+r'\cdot '+str(v)+r') \\  & =f('+str(t*u)+','+str(t*v)+r') \\  & =\frac{{'+str(a*t*u)+r'}^{2}+1}{{'+str(b*t*v)+r'}^{2}+'+str(a*t*u)+'('+str(b*t*v)+r')} \\  & =\frac{'+str(ns)+'}{'+str(ds)+r'} \\  & ='+sp.latex(scaled)+r'\end{aligned}')
    second=(r'\begin{aligned}f(x,y) & =f('+str(u)+','+str(v)+r') \\  & =\frac{{'+str(a*u)+r'}^{2}+1}{{'+str(b*v)+r'}^{2}+'+str(a*u)+'('+str(b*v)+r')} \\  & =\frac{'+str(n)+'}{'+str(d)+r'} \\  & ='+sp.latex(base)+r'.\end{aligned}')
    return f'For $x={u}$, $y={v}$ and $t={t}$, for instance, we have\n\n$$\n{first}\n$$\n\nand\n\n$$\n{second}\n$$\n\n',{'scaled':[ns,ds],'base':[n,d],'point':[u,v],'t':t}


def parameters_for(level,rng,template,explicit,raw):
    if explicit is None:
        if level=='hard':p={'sx':rng.randint(2,9),'sy':rng.randint(2,9)}
        elif level=='easy':
            axis=rng.choice(('sx','sy'));p={'sx':1,'sy':1};p[axis]=rng.randint(1,9)
        else:p={'sx':rng.randint(1,9),'sy':rng.randint(1,9)}
        if template=='constant_offset_not':p={'sx':rng.randint(1,3),'sy':rng.randint(1,3),'x0':1,'y0':2,'t':rng.randint(2,3)}
    else:p=dict(explicit)
    needed={'sx','sy'}|({'x0','y0','t'} if template=='constant_offset_not' else set())
    if set(p)!=needed:raise ValueError(f'parameters must be exactly {sorted(needed)}')
    if any(type(v) is not int for v in p.values()):raise ValueError('integer parameters required')
    if not all(1<=p[k]<=9 for k in ('sx','sy')):raise ValueError('coordinate factors must be 1..9')
    if level=='easy' and min(p['sx'],p['sy'])!=1:raise ValueError('easy allows at most one nonunit coordinate factor')
    if level=='hard' and not all(2<=p[k]<=9 for k in ('sx','sy')):raise ValueError('hard requires two nonunit factors 2..9')
    if template=='constant_offset_not':
        if not (p['sx']<=3 and p['sy']<=3 and p['x0']==1 and p['y0']==2 and 2<=p['t']<=3):raise ValueError('witness bounds: factors 1..3, x0=1, y0=2, t 2..3')
        if raw and p!={'sx':1,'sy':1,'x0':1,'y0':2,'t':3}:raise ValueError('malformed historical numeric witness is evidence-only at its original parameters')
    return p


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('unknown level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio fields only')
    rng=random.Random(seed)
    if template is None:template=rng.choice(LEVELS[level])
    if template not in LEVELS[level]:raise ValueError('template outside level scope')
    source_id=TEMPLATES[template];q=QUESTIONS[source_id]
    if profile not in (None,'normal','raw'):raise ValueError('profile must be normal or raw')
    raw=profile=='raw'
    if raw and level=='hard':raise ValueError('hard has no observed raw source')
    p=parameters_for(level,rng,template,parameters,raw)
    sx,sy=p['sx'],p['sy']
    original_fields=q[':question/answer-fields']
    indices=list(range(len(original_fields))) if raw else ([1] if source_id=='q-8739' else [0])
    body=q[':question/problem'];solution=scale_markdown(q[':question/worked-solution'],sx,sy)
    numerical=None
    if source_id=='q-14322' and not raw:
        start=solution.index('For $');end=solution.index('In other words,',start)
        numerical_text,numerical=witness(p)
        solution=solution[:start]+numerical_text+solution[end:]
        # The source's unrestricted implication is false if cancellation occurs.
        solution=solution.replace('We see that the numerator is NOT a homogeneous polynomial. Therefore, $f(x,y)$ is NOT a homogeneous function.',
           'We see that the numerator has terms of degrees $2$ and $0$, whereas the denominator is homogeneous of degree $2$. The nonzero constant term cannot cancel against this denominator, so the scaling factors cannot cancel. Therefore, $f(x,y)$ is NOT a homogeneous function of degree zero.')
    banks=[]
    for index in indices:
        f=original_fields[index]
        bank=[scale_math(c[':answer/value'],sx,sy) for c in f[':answer-field/choices']]
        correct_index=next((i for i,c in enumerate(f[':answer-field/choices']) if c[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')),None)
        banks.append({'source_field':index,'values':bank,'correct_index':correct_index})
    content={'version':VERSION,'level':level,'prompt':body,'solution':solution,'banks':[{'values':sorted(b['values']),'correct':b['values'][b['correct_index']] if b['correct_index'] is not None else None} for b in banks]}
    identity=digest(content);question_id=uid(identity)
    fields=[]
    for j,b in enumerate(banks):
        field_id=uid(identity+f'/field/{j}')
        choices=[{':answer/id':uid(field_id+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in b['values']]
        field={':answer-field/id':field_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
        if b['correct_index'] is not None:field[':answer-field/correct']=[':answer/id',choices[b['correct_index']][':answer/id']]
        fields.append(field)
    question={':question/id':question_id,':question/problem':body,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields}
    # Metadata excludes the key and source payload from learner-facing schema.
    math_banks=[[sp.simplify(e.subs({X:sx*X,Y:sy*Y},simultaneous=True)) for e in BANKS[source_id][i]] for i in indices]
    designated=math_banks[-1][banks[-1]['correct_index']]
    math_signature=digest({'criterion':'not-homogeneous' if level=='moderate' else 'homogeneous',
                           'assessed_rhs':sp.srepr(sp.simplify(sp.expand_log(designated,force=True))),
                           'coefficient_bookkeeping':2 if level=='hard' else (1 if level=='easy' else 'observed moderate')})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
      'generation':{'version':VERSION,'seed':seed,'template':template,'profile':'raw' if raw else 'normal','parameters':p,
        'source_ids':[source_id],'source':{k:SOURCE[k] for k in ('database','basis','lineage')},
        'content_identity':identity,'mathematical_identity':math_signature,'plot_rating':'none',
        'eligible_for_learning':not raw or source_id not in ('q-8739','q-14322'),
        'evidence_only':raw and source_id in ('q-8739','q-14322'),
        'authorship':'authored hard extension' if level=='hard' else 'observed masks with authored coefficient slots',
        'domains':['Every rational denominator must be nonzero.', 'Logarithms require x>0, y>0, t>0; the positive coordinate factors preserve this domain.', 'Ratio functions require their displayed denominator to be nonzero; all scaling checks use t>0.'],
        'numerical_witness':numerical,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=list(LEVELS),default='easy');parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--template');parser.add_argument('--profile',choices=['normal','raw']);parser.add_argument('--parameters',type=json.loads)
    parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='json')
    args=parser.parse_args();records=[generate(args.difficulty,args.seed+i,args.template,parameters=args.parameters,profile=args.profile) for i in range(args.count)]
    if args.format=='json':print(json.dumps(records[0] if args.count==1 else records,indent=2,ensure_ascii=False))
    else:
        for r in records:
            print(r['question'][':question/problem'])
            for f in r['question'][':question/answer-fields']:
                for a in f[':answer-field/choices']:print('\n- $'+a[':answer/value']+'$')
            print('\n'+r['question'][':question/worked-solution'])
