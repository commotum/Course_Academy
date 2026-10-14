#!/usr/bin/env python3
"""Bounded categorical recognition of vector fields on R^3; no EDB operations.

Source-backed easy families retain complete five-option banks and all prose/stages.
Moderate and hard are authored, missing-level designs, not observed labels.
Finite task identities use ordered (declared input dimension, output dimension)
pairs, excluding coefficient/function-letter/domain aliases. See evidence folder.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, re, sys, uuid
sys.dont_write_bytecode = True
from pathlib import Path
import sympy as sp

KP_ID = 17592186172087
KP_UUID = 'fb34fdb0-198e-507d-a944-9be782b4cfeb'
TITLE = 'Identifying Vector Fields on Three-Dimensions'
VERSION = 'vector-field-3d-2'
HERE = Path(__file__).with_suffix('')
SOURCE_WRAPPER = json.loads((HERE / 'source.json').read_text())
SOURCES = {q[':question/math-academy-id']: q for q in SOURCE_WRAPPER['record'][':knowledge-point/questions']}
PROVENANCE = {k:SOURCE_WRAPPER[k] for k in ('database','basis','lineage')}
LEVELS = ('easy','moderate','hard')
LABELS = ('None of the listed','I only','II only','I and II only','III only','I and III only','II and III only','I, II, and III')

# Each observed family has a complete mathematical-component slot, never a
# blind number/string substitution. a is positive, <=7, and incidental to the
# assessed classification. Domain slots are changed alongside their component.
SPECS = {
 'q-122467': (2,1, lambda a:rf'{{x}}^{{{a}}}\,i-{{y}}^{{{a}}}\,j', ((1,3),(2,2),(3,3))),
 'q-122697': (2,0, lambda a:rf'⟨x+{a},\sqrt{{x-y}},\operatorname{{ln}}⁡z⟩', ((3,3),(2,2),(1,3))),
 'q-122685': (2,1, lambda a:rf'{a}t\,i-{{t}}^{{2}}\,j-\sqrt{{t}}\,k', ((3,3),(1,3),(3,1))),
 'q-122688': (5,0, lambda a:rf'{a}\,i+{{z}}^{{2}}\,j+(y+x)\,k', ((3,3),(2,2),(3,3))),
 'q-122691': (5,1, lambda a:rf'⟨{a}{{e}}^{{-{{z}}^{{2}}}},{{x}}^{{3}}y,1-{{y}}^{{3}}⟩', ((3,1),(3,3),(2,2))),
 'q-122694': (3,1, lambda a:rf'⟨{{e}}^{{x-2y}},\sqrt{{{a}-x}},{a}{{z}}^{{3}}⟩', ((2,2),(3,3),(3,3))),
 'q-122696': (7,1, lambda a:rf'⟨{{y}}^{{3}}-3,\operatorname{{cos}}⁡(2x-y),{a}{{x}}^{{3}}⟩', ((3,1),(2,3),(3,3))),
 'q-122686': (3,2, lambda a:rf'\frac{{1}}{{t+1}}\,i-({a}t-1)\,j+\frac{{1}}{{{{t}}^{{2}}}}\,k', ((2,2),(3,3),(1,3))),
 'q-122695': (3,0, lambda a:rf'⟨z-{{x}}^{{2}},{a}x+{{z}}^{{2}},\frac{{1}}{{x+y}}⟩', ((3,3),(2,2),(1,2))),
}
TEMPLATES = {f'observed_{sid}':{'level':'easy','source_id':sid} for sid in SPECS}
TEMPLATES.update({f'authored_{level}':{'level':level,'source_id':None} for level in LEVELS})

def stable(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def digest(value):
    return hashlib.sha256(stable(value).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID),stable(value)))

def identity_components(level,prompt,solution,bank,correct,presence,correct_presence=True):
    return {'version':VERSION,'level':level if presence[':question/difficulty'] else None,
            'prompt':prompt,'solution':solution if presence[':question/worked-solution'] else None,
            'bank':sorted((value,':answer.type/text') for value in bank),
            'field':{'key':'selection','type':':answer-field.type/radio','correct_presence':correct_presence},
            'correct':correct if correct_presence else None,'presence':presence}

def selection(dims):
    return sum(1 << i for i,(n,m) in enumerate(dims) if n == m == 3)

def rename_names(text, old, new):
    # Match whole declared function applications; F and the set S in the
    # definition are not template letters.
    for i,name in enumerate(old):
        text = re.sub(r'\b'+re.escape(name)+r'(?=\()',f'@@NAME{i}@@',text)
    for i,name in enumerate(new):
        text = text.replace(f'@@NAME{i}@@',name)
    return text

def permute_label(label, order):
    bits = LABELS.index(label)
    return LABELS[sum(1<<i for i,j in enumerate(order) if bits & (1<<j))]

def observed_parts(sid, p, raw):
    """Extract fixed prose and component masks, then instantiate ordinary slots."""
    src = SOURCES[sid]
    lines = src[':question/problem'].splitlines()
    indices = [i for i,l in enumerate(lines) if l.startswith('- $')]
    apps, rhs = [], []
    for i in indices:
        app,expression = lines[i][3:-1].split('=',1)
        apps.append(app); rhs.append(expression)
    old_names = [a.split('(')[0] for a in apps]
    anchor,slot,recipe,dims = SPECS[sid]
    rhs[slot] = recipe(p['a'])
    displayed = [f'- ${apps[i]}={rhs[i]}$' for i in p['order']]
    prompt = '\n'.join(lines[:indices[0]]) + '\n' + '\n'.join(displayed)
    opening,body = src[':question/worked-solution'].split("With that in mind, let's examine each function.\n\n",1)
    examination,conclusion = body.rsplit('\n\nTherefore,',1)
    blocks = re.split(r'\n\n(?=- The function )',examination)
    assert len(blocks)==3
    if sid=='q-122694':
        blocks[1]=blocks[1].replace(r'3-x\ge 0',rf'{p["a"]}-x\ge 0')
    if not raw:
        blocks=[b.replace('to functions in $R$','to values in $R$').replace('S={',r'S=\{').replace('}\n$$',r'\}'+'\n$$') for b in blocks]
    dims = [dims[j] for j in p['order']]
    correct=LABELS[selection(dims)]
    solution=opening+"With that in mind, let's examine each function.\n\n"+'\n\n'.join(blocks[j] for j in p['order'])+f'\n\nTherefore, the correct answer is "{correct}."'
    prompt=rename_names(prompt,old_names,p['names'])
    solution=rename_names(solution,old_names,p['names'])
    field=src[':question/answer-fields'][0]
    bank=[permute_label(a[':answer/value'],p['order']) for a in field[':answer-field/choices']]
    return prompt,solution,bank,correct,dims

# Authored easy: signatures and vector components visibly distinguish 3->3,
# 2->2 and 1->3. The method is exactly the observed categorical recognition.
# Authored moderate: all inputs are triples; identify scalar/2/3-coordinate
# outputs instead of relying on the input signature alone (19 ordered tasks).
# Authored hard: all outputs are triples and depend on one displayed coordinate;
# attend to declared arguments even when coordinates are unused (18 tasks).
CATALOG = {'easy':((3,3),(2,2),(1,3)),
           'moderate':((3,3),(3,2),(3,1)),
           'hard':((3,3),(2,3),(1,3))}
def eligible_types(level):
    tasks=list(itertools.product(range(3),repeat=3))
    if level=='moderate': tasks=[t for t in tasks if 1 in t]
    if level=='hard': tasks=[t for t in tasks if 0 in t and any(i!=0 for i in t)]
    return tasks
INTRO = r'Suppose that $S$ is a subset of $\mathbb R^3.$ A vector field on $\mathbb R^3$ is a function $F$ that maps every point $(x,y,z)\in S$ to a vector $F(x,y,z)\in\mathbb R^3.$'

def authored_parts(level,p):
    dims=[CATALOG[level][t] for t in p['types']]
    prompt=r'Which of the following are vector fields on $\mathbb R^3?$'+'\n\n'
    blocks=[]
    for name,(n,m) in zip(p['names'],dims):
        args={1:'t',2:'x,y',3:'x,y,z'}[n]
        var='t' if n==1 else 'x'
        if level=='hard':
            # Unused coordinates are intentional, not grounds for reclassifying
            # an explicitly declared multivariable function as a curve.
            components=(rf'{p["a"]}{var}',rf'{var}^2','1')
        elif level=='moderate':
            components=(rf'{p["a"]}x','y^2','z')[:m]
        else:
            components={1:(rf'{p["a"]}t','t^2','1-t'),2:(rf'{p["a"]}x','y^2'),3:(rf'{p["a"]}x','y^2','z')}[n]
        expr=components[0] if m==1 else r'\langle '+', '.join(components)+r'\rangle'
        prompt+=f'- ${name}({args})={expr}$\n'
        app=f'{name}({args})'
        if n==m==3:
            block=f'- The function ${app}$ is a vector field on $\\mathbb R^3.$ It assigns every point $(x,y,z)\\in\\mathbb R^3$ to a vector in $\\mathbb R^3.$'
        else:
            inp=r'\mathbb R' if n==1 else rf'\mathbb R^{n}'
            out=r'\mathbb R' if m==1 else rf'\mathbb R^{m}'
            inp+=r' (not $\mathbb R^3$)' if n!=3 else ''
            # Keep every math delimiter explicit, including dimension remarks.
            inpdim=r'\mathbb R' if n==1 else rf'\mathbb R^{n}'
            outdim=r'\mathbb R' if m==1 else rf'\mathbb R^{m}'
            a=f'${inpdim}$'+(' (not $\\mathbb R^3$)' if n!=3 else '')
            b=f'${outdim}$'+(' (not $\\mathbb R^3$)' if m!=3 else '')
            block=f'- The function ${app}$ is *not* a vector field on $\\mathbb R^3.$ It assigns points in {a} to '+('values' if m==1 else 'vectors')+f' in {b}.'
        blocks.append(block)
    correct_mask=selection(dims)
    bank=[LABELS[correct_mask ^ error] for error in (0,1,2,4,7)]
    correct=LABELS[correct_mask]
    solution=INTRO+"\n\nWith that in mind, let's examine each function.\n\n"+'\n\n'.join(blocks)+f'\n\nTherefore, the correct answer is "{correct}."'
    return prompt.rstrip(),solution,bank,correct,dims

def validate_parameters(level,template,p):
    observed=TEMPLATES[template]['source_id'] is not None
    expected={'a','order','names'} if observed else {'a','types','names'}
    if set(p)!=expected: raise ValueError(f'parameters must have exactly {expected}')
    if type(p['a']) is not int or not 1<=p['a']<=7: raise ValueError('a must be an integer from 1 through 7')
    names=p['names']
    if not isinstance(names,(list,tuple)) or len(names)!=3 or any(not isinstance(s,str) for s in names) or len(set(names))!=3 or any(not re.fullmatch('[A-EG-Z]',s) for s in names):
        raise ValueError('three distinct uppercase function names, excluding F, are required')
    if observed:
        if not isinstance(p['order'],(tuple,list)) or sorted(p['order'])!=[0,1,2]: raise ValueError('order must permute 0,1,2')
    elif not isinstance(p['types'],(tuple,list)) or len(p['types'])!=3 or any(type(t)is not int or t not in range(3) for t in p['types']):
        raise ValueError('three categorical indices from 0 through 2 are required')
    elif tuple(p['types']) not in eligible_types(level):
        raise ValueError('categorical workload does not satisfy this authored level')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS: raise ValueError('invalid difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('only radio is supported')
    rng=random.Random(seed)
    eligible=[t for t,s in TEMPLATES.items() if s['level']==level]
    if profile and profile.startswith('observed_'):
        eligible=[t for t in eligible if t==profile]
    elif profile not in (None,'normal','authored_mask'): raise ValueError('unknown profile')
    if profile=='authored_mask': eligible=[t for t in eligible if t.startswith('authored_')]
    if template is not None: eligible=[t for t in eligible if t==template]
    if not eligible: raise ValueError('template/profile/difficulty do not identify an eligible family')
    template=rng.choice(eligible)
    sid=TEMPLATES[template]['source_id']
    raw=profile is not None and profile.startswith('observed_')
    if parameters is None:
        names=rng.sample(list('ABCDGHJKLMNPQRSTUVWXYZ'),3)
        parameters={'a':rng.randint(1,7),'names':names}
        if sid:
            parameters['order']=rng.sample(range(3),3)
        else:
            parameters['types']=list(rng.choice(eligible_types(level)))
    p=json.loads(json.dumps(parameters))
    validate_parameters(level,template,p)
    prompt,solution,bank,correct,dims=observed_parts(sid,p,raw) if sid else authored_parts(level,p)
    if len(bank)!=5 or len(set(bank))!=5 or bank.count(correct)!=1: raise ValueError('complete bank must contain one correct and four unique wrong subsets')
    profile=profile or ('normal' if sid else 'authored_mask')
    # All learner content, complete bank, actual correct value and presence are
    # identity-bearing. Presentation aliases and option order are not parameters
    # of identity; mathematical classification remains a separate fingerprint.
    presence={k:k in SOURCES[sid] for k in (':question/difficulty',':question/worked-solution',':question/answer-fields')} if raw else {k:True for k in (':question/difficulty',':question/worked-solution',':question/answer-fields')}
    identity=identity_components(level,prompt,solution,bank,correct,presence)
    content_id=digest(identity)
    field_id=uid([content_id,'selection'])
    answers=[{':answer/id':uid([field_id,value]),':answer/type':':answer.type/text',':answer/value':value} for value in bank]
    correct_ref=[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]
    rng.shuffle(answers)
    field={':answer-field/id':field_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':correct_ref}
    question={':question/id':uid(content_id),':question/problem':prompt}
    if presence[':question/difficulty']: question[':question/difficulty']=f':question.difficulty/{level}'
    if presence[':question/worked-solution']: question[':question/worked-solution']=solution
    if presence[':question/answer-fields']: question[':question/answer-fields']=[field]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
            'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source_id':sid,'provenance':PROVENANCE,'authored_level':not sid,'semantic_signature':dims,'mathematical_fingerprint':digest(dims),'content_id':content_id,'evidence_only':raw,'eligible_for_learning':not raw,'source_repairs':([] if raw or sid not in ('q-122685','q-122691','q-122696') else ['scalar output prose: functions → values']),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none'}}

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Observed + authored easy: visibly distinct input/output shapes."""
    return generate('easy',seed,template,field_type,parameters,profile)

def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Authored: three declared input coordinates; scalar/2-/3-vector outputs."""
    return generate('moderate',seed,template,field_type,parameters,profile)

def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Authored: triple outputs; declared input arity with unused coordinates."""
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question']; f=q.get(':question/answer-fields',[{}])[0]
    return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f.get(':answer-field/choices',[]))+'\n\n'+q.get(':question/worked-solution','')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile')
    args=ap.parse_args()
    levels=LEVELS if args.difficulty=='all' else (args.difficulty,)
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

if __name__=='__main__': main()
