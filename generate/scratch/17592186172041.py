#!/usr/bin/env python3
"""Rectangular slope-sign statements; local review records only (steps 3–7).

Source: math basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.
The seven observed five-choice banks are complete categorical subset banks,
not recovered misconception recipes. Normal generation uses a whole authored
bank: correct truth vector, each of three single-bit flips, and its complement.
All templates parameterize the full factored expression and three open regions.
No differential equations are solved; figures show only zero lines and signs.
Easy is an authored canonical-example subset with unit shifts and ordinary
factors. Moderate uses nonzero small integer shifts, at least one magnitude >=2,
and optionally reversed linear factors. Hard has exactly one squared factor.
No scalar magnitude is sampled or counted as substantive task variety.
Source q-96475 is unrated/missing its correct marker and worked solution:
it is assigned moderate, I only is independently derived, and its solution is
authored. Original source evidence and exact banks remain separately available.
Profiles affect full content identity, not the canonical mathematical task.
Source geometry assets are reused only for identical zero lines and region signs;
all other figures are rendered with Matplotlib through the cached renderer.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import re
import subprocess
import tempfile
import uuid
import sympy as sp

KP_ID=17592186172041
KP_UUID='75710e99-e13c-54ba-9401-486bfec15284'
TITLE='Identifying Rectangular Regions Where a Slope Field Is Positive or Negative'
VERSION='rectangular-sign-regions-1'
HERE=Path(__file__).resolve().with_suffix('')
PYTHON=Path(__file__).resolve().parents[2]/'.venv/bin/python'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
PROFILES=json.loads((HERE/'profiles.json').read_text())
SOURCE_GEOMETRIES=json.loads((HERE/'source-geometries.json').read_text())
TEMPLATES={'easy_bilinear':'easy','bilinear':'moderate','numbered_bilinear':'moderate','x_squared':'hard','y_squared':'hard'}
X,Y=sp.symbols('x y',real=True)
ROMAN=('I','II','III')

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL,'kp17592186172041:'+value))

def selection(bits):
    labels=[r for r,b in zip(ROMAN,bits) if b]
    return ('None of those listed' if not labels else 'I, II, and III' if len(labels)==3
            else labels[0]+' only' if len(labels)==1 else ' and '.join(labels)+' only')

def parse_selection(value):
    return tuple(bool(re.search(r'\b'+r+r'\b',value)) for r in ROMAN)

def factor(variable,root,orientation=1,power=1,numbered=False):
    if numbered:
        z=variable+(' + '+str(-root) if root<0 else ' - '+str(root))
    elif orientation==1:
        z=variable+('+'+str(-root) if root<0 else '-'+str(root))
    else:
        z=str(root)+'-'+variable
    return '('+z+')'+('^{2}' if power==2 else '')

def expression_tex(p,numbered=False):
    return factor('x',p['h'],p['ox'],p['px'],numbered)+factor('y',p['k'],p['oy'],p['py'],numbered)

def expression(p):
    return (p['ox']*(X-p['h']))**p['px']*(p['oy']*(Y-p['k']))**p['py']

def sign_at(p,sx,sy):
    return (p['ox']*sx)**p['px']*(p['oy']*sy)**p['py']

def validate_parameters(level,template,p):
    if set(p)!={'h','k','ox','oy','px','py','regions'}:raise ValueError('Exact parameter keys required')
    if any(type(p[k]) is not int for k in ('h','k','ox','oy','px','py')):raise ValueError('Integer components required')
    if not all(1<=abs(p[k])<=3 for k in ('h','k')):raise ValueError('Nonzero shifts of magnitude 1 through 3 required')
    if p['ox'] not in (-1,1) or p['oy'] not in (-1,1):raise ValueError('Factor orientations must be signed units')
    if level=='easy':
        if (p['px'],p['py'],p['ox'],p['oy'])!=(1,1,1,1) or max(abs(p['h']),abs(p['k']))!=1:raise ValueError('Easy requires ordinary factors and unit shifts')
    if level=='moderate':
        if (p['px'],p['py'])!=(1,1) or max(abs(p['h']),abs(p['k']))<2:raise ValueError('Moderate requires two linear factors and at least one shift magnitude >=2')
        if template=='numbered_bilinear' and (p['ox'],p['oy'])!=(1,1):raise ValueError('Numbered presentation uses ordinary factors')
    if level=='hard':
        pair=(2,1) if template=='x_squared' else (1,2)
        if (p['px'],p['py'])!=pair or (p['px']==2 and p['ox']!=1) or (p['py']==2 and p['oy']!=1):raise ValueError('Hard has the named squared factor, in ordinary orientation')
    regions=p['regions']
    if not isinstance(regions,list) or len(regions)!=3 or any(not isinstance(r,list) or len(r)!=3 or any(type(a) is not int or a not in (-1,1) for a in r) for r in regions):raise ValueError('Three signed open-region claims required')
    if len({tuple(r[:2]) for r in regions})!=3:raise ValueError('Distinct regions required')

def sample_parameters(level,template,rng):
    shifts=(-3,-2,-1,1,2,3)
    p={'h':rng.choice((-1,1) if level=='easy' else shifts),'k':rng.choice((-1,1) if level=='easy' else shifts),'ox':1,'oy':1,'px':1,'py':1}
    if level=='moderate' and max(abs(p['h']),abs(p['k']))<2:return sample_parameters(level,template,rng)
    if level=='moderate' and template!='numbered_bilinear':p['ox'],p['oy']=rng.choice((-1,1)),rng.choice((-1,1))
    if level=='hard':
        p['px'],p['py']=(2,1) if template=='x_squared' else (1,2)
        p['oy' if template=='x_squared' else 'ox']=rng.choice((-1,1))
    p['regions']=[[*r,rng.choice((-1,1))] for r in rng.sample(list(itertools.product((-1,1),repeat=2)),3)]
    return p

def render_plots(p,output_dir=None):
    """Full geometry/sign key; unique input and atomic asset writes permit concurrency."""
    geometry=[p[k] for k in ('h','k','ox','oy','px','py')]
    key=json.dumps(geometry,separators=(',',':'))
    if output_dir is None and key in SOURCE_GEOMETRIES:
        refs=SOURCE_GEOMETRIES[key]
        return {'partition':refs[0],'signs':refs[1],'reused_source_geometry':True}
    target=Path(output_dir) if output_dir else HERE/'plots';target.mkdir(parents=True,exist_ok=True)
    stem=digest(geometry)[:20]
    refs={role:str(target/(stem+'-'+role+'.png')) for role in ('partition','signs')}
    def complete_cache():
        for role,value in refs.items():
            path=Path(value);side=path.with_suffix('.json')
            if not path.exists() or not side.exists():return False
            try:info=json.loads(side.read_text())
            except (OSError,json.JSONDecodeError):return False
            if info.get('role')!=role or info.get('geometry_fingerprint')!=digest(geometry):return False
        return True
    if not complete_cache():
        data={'parameters':p,'paths':refs,'geometry_fingerprint':digest(geometry)}
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='rect-sign-',dir=HERE,delete=False) as f:
            json.dump(data,f);name=f.name
        try:subprocess.run([str(PYTHON),str(HERE/'render.py'),name],check=True,capture_output=True,text=True)
        finally:Path(name).unlink(missing_ok=True)
    if output_dir is None:refs={k:str(Path(v).relative_to(HERE)) for k,v in refs.items()}
    return {**refs,'reused_source_geometry':False}

def region_text(p,r,numbered=False):
    sx,sy,_=r;rx='>' if sx==1 else '<';ry='>' if sy==1 else '<'
    if numbered:
        n=lambda z:str(z) if z>0 else '- '+str(-z)
        return 'x '+rx+' '+n(p['h'])+'$ and $y '+ry+' '+n(p['k'])
    return 'x'+rx+str(p['h'])+'$ and $y'+ry+str(p['k'])+','

def prompt(p,numbered):
    eq=(r'\frac{dy}{dx} = ' if numbered else r'\frac{\text{d}y}{\text{d}x}=')+expression_tex(p,numbered)
    text='Consider the differential equation $'+eq+'$ and its slope field. Which of the following statements are true?\n\n'
    lines=[]
    for i,r in enumerate(p['regions']):
        word='positive' if r[2]==1 else 'negative'
        lines.append((str(i+1)+'. ' if numbered else '- ')+'At every point $('+('x, y' if numbered else 'x,y')+')$ where $'+region_text(p,r,numbered)+'$, the slope of the slope field is '+word if numbered else '- At every point $(x,y)$ where $'+region_text(p,r)+'$ the slope of the slope field is '+word)
    return text+'\n'.join(lines)

def worked_solution(p,plots,conclusion,correct):
    expr=expression_tex(p)
    text='First, we define $f(x,y)='+expr+'.$ Then, our differential equation is $'+r'\frac{\text{d}y}{\text{d}x}=f(x,y).$ '+'\n\n'
    text+='Notice that $f(x,y)=0$ when $x='+str(p['h'])+'$ or $y='+str(p['k'])+'.$ This divides the $xy$-plane into four regions, as shown below.\n\n'
    text+='![]('+plots['partition']+')\n\n'
    text+='If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:\n\n'
    text+='![]('+plots['signs']+')\n\n'
    text+="With that in mind, let's check each statement:\n\n"
    for i,r in enumerate(p['regions']):
        sg=sign_at(p,*r[:2]);truth=sg==r[2];word='positive' if sg==1 else 'negative'
        text+='- Statement '+ROMAN[i]+' is '+str(truth).lower()+'. If $'+region_text(p,r)+'$ then according to our diagram, we have\n\n'
        text+='$$\n'+r'{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)'+('>0.' if sg==1 else '<0.')+'\n$$\n\n'
        text+='This implies that the slope of the slope field is '+word+' for any point $(x,y)$ in this region.'
        if i<2:text+='\n\n'
    if conclusion:text+='\n\nTherefore, the correct answer is "'+correct+'."'
    return text

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio fields are supported')
    rng=random.Random(seed)
    if profile is not None and profile not in PROFILES and profile!='authored_truth_flips':raise ValueError('Unknown complete bank profile')
    if template is None:
        if profile in PROFILES:
            cases=json.loads((HERE/'source-cases.json').read_text());template=next(c['template'] for c in cases if c['bank_profile']==profile)
        else:template=rng.choice([t for t,l in TEMPLATES.items() if l==level and t!='numbered_bilinear'])
    if TEMPLATES.get(template)!=level:raise ValueError('Template/difficulty mismatch')
    profile=profile or 'authored_truth_flips'
    if profile in PROFILES:
        eligible=next(c for c in json.loads((HERE/'source-cases.json').read_text()) if c['bank_profile']==profile)
        if eligible['template']!=template:raise ValueError('Source bank profile must use its observed template')
    for _ in range(2000):
        p=json.loads(json.dumps(parameters)) if parameters is not None else sample_parameters(level,template,rng)
        validate_parameters(level,template,p)
        truths=tuple(sign_at(p,*r[:2])==r[2] for r in p['regions']);correct=selection(truths)
        if profile in PROFILES:
            bank=list(PROFILES[profile]['bank']);conclusion=PROFILES[profile]['conclusion']
        else:
            patterns=[truths]+[tuple(not b if j==i else b for j,b in enumerate(truths)) for i in range(3)]+[tuple(not b for b in truths)]
            bank=[selection(bits) for bits in patterns];conclusion=True
        if len(bank)==5 and len(set(bank))==5 and bank.count(correct)==1:break
        if parameters is not None:raise ValueError('Whole bank is ineligible: missing/ambiguous correct answer')
    else:raise ValueError('Could not sample an eligible whole bank')
    plots=render_plots(p)
    numbered=template=='numbered_bilinear'
    problem=prompt(p,numbered);solution=worked_solution(p,plots,conclusion,correct)
    # Mathematically assessed sign partition and ordered claims exclude factor
    # spelling, positive magnitudes, profiles and shuffled option order.
    canonical={'h':p['h'],'k':p['k'],'sign_grid':[sign_at(p,*r) for r in itertools.product((-1,1),repeat=2)],'regions':sorted(p['regions'])}
    fingerprint=digest(canonical)
    identity=digest({'version':VERSION,'level':level,'prompt':problem,'solution':solution,'bank':sorted(bank),'domain':'three distinct open rectangular regions'})
    qid=uid('question:'+identity);fid=uid('field:'+qid+':selection')
    choices=[{':answer/id':uid('answer:'+fid+':'+value),':answer/type':':answer.type/text',':answer/value':value} for value in bank]
    correct_id=next(a[':answer/id'] for a in choices if a[':answer/value']==correct)
    rng.shuffle(choices)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]},'generation':{'version':VERSION,'source':SOURCE,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,'domain':'Open regions x<h or x>h and y<k or y>k; zero lines excluded.','mathematical_fingerprint':fingerprint,'content_identity':identity,'plots':plots,'source_refs':PROFILES[profile]['sources'] if profile in PROFILES else [],'authored_bank':profile=='authored_truth_flips','sympy_version':sp.__version__}}

# Easy/moderate/hard entry points share the exact mathematical pipeline.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile')
    a=parser.parse_args();records=[generate(level,a.seed+i,template=a.template,profile=a.profile) for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
    if a.format=='json':print(json.dumps(records,indent=2))
    else:
        for r in records:
            q=r['question'];print('### '+q[':question/difficulty'].split('/')[-1]+'\n\n'+q[':question/problem']+'\n')
            print('\n'.join('- '+a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']))
            print('\n'+q[':question/worked-solution']+'\n')

if __name__=='__main__':main()
