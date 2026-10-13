#!/usr/bin/env python3
"""Unit vector parallel to an orthogonal vector sum, draft after steps 3–7.

Raw public profiles reproduce both complete captured banks and all missing
ratings/solutions/correct refs. Their scalar operations are evidence similarity
scalings, not inferred teaching errors. Inferred profiles add only a supported
correct reference; neither evidence profile is eligible for learning. Normal
method banks are authored. Level sections describe bounds below; the same
Pythagorean sum and normalization are used throughout, without component-form
questions, new diagrams, trig calculations, or progression within a level.
"""
import argparse
import hashlib
import json
import random
import uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186096815
KP_UUID='d44ac67b-5e3d-5b1e-bf2c-554b592ba29e'
TITLE='Finding a Unit Vector Parallel to a Vector Sum'
VERSION='orthogonal-sum-1'
ROOT=Path(__file__).with_suffix('')
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
CARDINAL=[('horizontally to the right','vertically down'),('horizontally to the right','vertically up'),('horizontally to the left','vertically down'),('horizontally to the left','vertically up')]
DIAGONAL=[('due north-east','due south-east'),('due north-east','due north-west'),('due south-east','due north-east'),('due south-east','due south-west'),('due south-west','due south-east'),('due south-west','due north-west'),('due north-west','due north-east'),('due north-west','due south-west')]
BANK_PROFILES={name:{'evidence_only':True,'eligible_for_learning':False,'kind':kind,'origin':'observed evidence, opaque wrong operations'} for name,kind in [('observed_cardinal_raw','cardinal'),('observed_cardinal_inferred','cardinal'),('observed_compass_raw','compass'),('observed_compass_inferred','compass')]}
BANK_PROFILES['authored_method']={'evidence_only':False,'eligible_for_learning':True,'origin':'authored method errors'}
TEMPLATES={'cardinal_sum':{'kind':'cardinal','sources':['q-12184']},'compass_sum':{'kind':'compass','sources':['q-12185']}}

def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x): return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def tex(x): return sp.latex(sp.sympify(x))
def fraction(d): return r'\frac{1}{'+d+r'}(a + b)'
def directions(kind): return CARDINAL if kind=='cardinal' else DIAGONAL

def prompt(kind,p):
    a,b=p['a'],p['b']; da,db=directions(kind)[p['orientation']]
    if kind=='cardinal':
        body=f'The vector $a$ is directed {da} and has magnitude ${a}$, while the vector $b$ is directed {db} and has magnitude ${b}$.'
    else:
        body=f'The vector $a$ is directed {da} and $\\mid a|= {a}$, while the vector $b$ is directed {db} and $\\mid b|= {b}$.'
    return body+' Which of the following is a unit vector that is parallel to $a + b$?\n\n> A scientific calculator is required to answer this question.'

def solution(p):
    a,b=p['a'],p['b']; n=a*a+b*b
    return (r'First, we have to find $a+b$. The given directions are perpendicular, so the triangle law of addition gives a right triangle.'+'\n\n'+
      r'To find the unit vector corresponding to $a+b$, we have to divide by the magnitude:'+'\n\n$$\n'+
      r'u=\frac{a+b}{|a+b|}'+'\n$$\n\n'+r'To find the magnitude, we can use the Pythagorean theorem:'+'\n\n$$\n'+
      r'\begin{aligned}|a+b|^2&=|a|^2+|b|^2\\'+ '\n'+f'&={a}^2+{b}^2'+r'\\'+'\n'+f'&={a*a}+{b*b}'+r'\\'+'\n'+f'&={n}'+r'\end{aligned}'+'\n$$\n\n'+
      'Therefore, the magnitude is\n\n$$\n'+r'|a+b|=\sqrt{'+str(n)+'}='+tex(sp.sqrt(n))+'\n$$\n\n'+
      'and the corresponding unit vector is\n\n$$\n'+r'\begin{aligned}u&=\frac{a+b}{|a+b|}\\'+'\n'+r'&=\frac{1}{'+tex(sp.sqrt(n))+r'}(a+b)\end{aligned}'+'\n$$')

def bank(profile,p):
    """Choose a COMPLETE profile. Opaque profiles scale all observed denominators.
    Expressions are structural parameterized similarity recipes, explicitly not
    recovered error intent. The raw original expression spelling is preserved.
    """
    a,b=p['a'],p['b']; N=a*a+b*b; norm=sp.sqrt(N)
    if profile.startswith('observed_cardinal'):
        # Denominators from the complete observed bank, scaled by norm/5.
        ds=[2*sp.sqrt(3)*norm/5,sp.sqrt(5)*norm/5,norm,3*sp.sqrt(3)*norm/5,2*norm]
        scale=sp.simplify(norm/5)
        bases=[r'2\sqrt{3}',r'\sqrt{5}','5',r'3\sqrt{3}','10']
        spell=[base if scale==1 else r'\left('+base+r'\right)\left('+tex(scale)+r'\right)' for base in bases]
        labels=['opaque_similarity_1','opaque_similarity_2','correct','opaque_similarity_4','opaque_similarity_5']
    elif profile.startswith('observed_compass'):
        # All five original denominators scaled by norm/sqrt569.
        ds=[norm,sp.sqrt(573)*norm/sp.sqrt(569),sp.sqrt(561)*norm/sp.sqrt(569),23*norm/sp.sqrt(569),25*norm/sp.sqrt(569)]
        scale=sp.simplify(norm/sp.sqrt(569))
        bases=[r'\sqrt{569}',r'\sqrt{573}',r'\sqrt{561}','23','25']
        spell=[base if scale==1 else r'\left('+base+r'\right)\left('+tex(scale)+r'\right)' for base in bases]
        labels=['correct','opaque_similarity_2','opaque_similarity_3','opaque_similarity_4','opaque_similarity_5']
    else:
        ds=[norm,a+b,N,a,b]
        spell=list(map(tex,ds)); labels=['correct','add_magnitudes','omit_square_root','normalize_by_a_only','normalize_by_b_only']
    coeffs=[sp.simplify(1/d) for d in ds]
    if len(set(coeffs))!=5 or sum(sp.simplify(c*c*N)==1 for c in coeffs)!=1:
        raise ValueError('Complete bank is ambiguous or collides')
    return [(label,fraction(s),str(c)) for label,s,c in zip(labels,spell,coeffs)]

# Easy: cardinal perpendicular directions and unequal integer legs 2..30 of
# an integer-hypotenuse triangle. Each task squares, adds, takes root, normalizes.
def generate_easy(seed=0,**kwargs): return generate('easy',seed,**kwargs)
# Moderate: cardinal perpendicular directions, unequal integer legs 2..12,
# nonsquare sum. Exact radical normalization is the only arithmetic extension.
def generate_moderate(seed=0,**kwargs): return generate('moderate',seed,**kwargs)
# Hard: perpendicular diagonal compass bearings, unequal integer legs 10..25,
# nonsquare sum. Recognize the 90-degree relationship; no angle/trig branch.
def generate_hard(seed=0,**kwargs): return generate('hard',seed,**kwargs)

def valid(level,kind,p,evidence=False):
    if set(p)!={'a','b','orientation'} or any(type(x)!=int for x in p.values()): raise ValueError('Exact integer a,b,orientation required')
    a,b,o=p['a'],p['b'],p['orientation']
    if not (1<=a<=50 and 1<=b<=50 and 0<=o<len(directions(kind))): raise ValueError('Invalid magnitudes or orientation')
    if evidence: return
    square=sp.sqrt(a*a+b*b).is_Integer
    if level=='easy' and not(kind=='cardinal' and 2<=a<=30 and 2<=b<=30 and a!=b and square): raise ValueError('Outside easy bounds')
    if level=='moderate' and not(kind=='cardinal' and 2<=a<=12 and 2<=b<=12 and a!=b and not square): raise ValueError('Outside moderate bounds')
    if level=='hard' and not(kind=='compass' and 10<=a<=25 and 10<=b<=25 and a!=b and not square): raise ValueError('Outside hard bounds')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']: raise ValueError('Unknown difficulty')
    profile=profile or 'authored_method'
    if profile not in BANK_PROFILES: raise ValueError('Unknown profile')
    evidence=BANK_PROFILES[profile]['evidence_only']; raw=profile.endswith('_raw')
    template=template or (('compass_sum' if BANK_PROFILES[profile]['kind']=='compass' else 'cardinal_sum') if evidence else ('compass_sum' if level=='hard' else 'cardinal_sum'))
    if template not in TEMPLATES or field_type not in [None,'radio',':answer-field.type/radio']: raise ValueError('Unsupported template/field')
    kind=TEMPLATES[template]['kind']
    if evidence and BANK_PROFILES[profile]['kind']!=kind: raise ValueError('Evidence bank/template mismatch')
    rng=random.Random(seed)
    if parameters is None:
        # Whole-instance rejection, never a first-valid option pool.
        for _ in range(2000):
            lo,hi=(2,30) if level=='easy' else ((2,12) if level=='moderate' else (10,25))
            p={'a':rng.randint(lo,hi),'b':rng.randint(lo,hi),'orientation':rng.randrange(len(directions(kind)))}
            try: valid(level,kind,p,evidence); values=bank(profile,p); break
            except ValueError: continue
        else: raise ValueError('No eligible whole instance')
    else:
        p=dict(parameters); valid(level,kind,p,evidence); values=bank(profile,p)
    text=prompt(kind,p); worked=None if evidence else solution(p)
    content=digest({'version':VERSION,'prompt':text,'solution':worked,'bank':sorted(v for _,v,_ in values)})
    task=digest({'method':kind,'unordered_magnitudes':sorted([p['a'],p['b']])})
    qid=uid('question:'+content); fid=uid(qid+':selection')
    answers=[]; correct=None; recipes={}
    for label,value,coefficient in values:
        aid=uid(fid+':'+value)
        answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
        recipes[aid]={'operation':label,'coefficient':coefficient}
        if label=='correct':correct=aid
    rng.shuffle(answers)
    f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    q={':question/id':qid,':question/problem':text,':question/answer-fields':[f]}
    if not raw:f[':answer-field/correct']=[':answer/id',correct]
    if not evidence:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':worked})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,**BANK_PROFILES[profile],'parameter_fingerprint':task,'content_fingerprint':content,'source_analysis':SOURCE,'source_ids':TEMPLATES[template]['sources'],'source_missing_correct_ref':evidence,'correct_ref_inferred':evidence and not raw,'correct_ref_origin':('missing in captured source' if raw else ('authored mathematical inference' if evidence else 'authored method bank')),'authored_level':level,'authored_extension':not evidence,'recipes':recipes,'plot_rating':'none','plot_assets':{},'sympy_version':sp.__version__}}

def markdown(r):
    q=r['question']; f=q[':question/answer-fields'][0]
    lines=[q[':question/problem'],'']+[f'{i+1}. ${a[":answer/value"]}$' for i,a in enumerate(f[':answer-field/choices'])]
    if ':question/worked-solution' in q:lines+=['',q[':question/worked-solution']]
    return '\n'.join(lines)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ns=ap.parse_args()
    levels=['easy','moderate','hard'] if ns.difficulty=='all' else [ns.difficulty]
    records=[generate(level,ns.seed+i,template=ns.template,profile=ns.profile) for level in levels for i in range(ns.count)]
    print(json.dumps(records,indent=2) if ns.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
