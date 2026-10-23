#!/usr/bin/env python3
"""Finding a square-matrix entry; frozen math basis1356. No database writes.

Faithful public raw_q-* profiles reconstruct all six practice records from
parameterized matrix/index/presentation recipes, retaining missing attributes.
Raw replay is evidence-only. Normal output repairs R/E naming and completes the
unrated missing-ref example explicitly. Entire indexing banks are chosen before
matrix sampling; any value collision rejects the whole instance.
Easy retains observed2x2–4x4 and integer/radical entry forms. Authored moderate
uses5x5/max(i,j)>=4 and hard6x6/max(i,j)>=5: larger visual searches, the same
single lookup. No matrix arithmetic, symmetry or inverse-index questions.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186100989
KP_UUID='ecd07ea0-767d-55f0-a61c-da49dd320f89'
TITLE='Finding an Entry of a Square Matrix'
VERSION='square-entry-2'
ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/str(KP_ID)
PROVENANCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
VALUES=[str(x) for x in range(-13,14)]+[r'\sqrt{2}',r'\sqrt{3}']
TEMPLATES=('aligned_radio','aligned_blank','absent_radio','inline_radio')
# Profiles are whole banks. Historical q13490 scalars are opaque evidence slots;
# they are never used as default learner distractors or assigned invented intent.
BANKS={
 'q-13495':('aligned_radio',('target','left','transpose','transposed_first','missing')),
 'q-13490':('aligned_radio',('target','left','opaque0','opaque1','missing')),
 'q-279542':('aligned_blank',('target',)),
 'q-125593':('aligned_radio',('target','right','up','left','missing')),
 'q-125564':('absent_radio',('missing','cell11','cell12','cell21','cell22')),
 'q-13506':('inline_radio',('target','last_diagonal','previous_diagonal','cell23','missing')),
 'transpose_neighbors':('aligned_radio',('target','left','transpose','transposed_first','missing')),
 'right_up_left':('aligned_radio',('target','right','up','left','missing')),
 'local_neighbors':('aligned_radio',('target','left','up','down','missing')),
 'blank':('aligned_blank',('target',)),
 'all_four':('absent_radio',('missing','cell11','cell12','cell21','cell22')),
 'inline_diagonal':('inline_radio',('target','last_diagonal','previous_diagonal','cell23','missing')),
}
SOURCE_PRESENTATION={
 'q-13495': {'solution_period':False},
 'q-13490': {'solution_period':False},
 'q-279542':{'solution_period':True},
 'q-125593':{'solution_period':False,'solution_name':'E'},
 'q-125564':{}, 'q-13506':{'unrated':True,'missing_solution':True,'missing_correct':True},
}
class SampleRejected(ValueError): pass

def exact(s):
    if re.fullmatch(r'-?\d+',s): return sp.Integer(s)
    m=re.fullmatch(r'\\sqrt\{([23])\}',s)
    if m:return sp.sqrt(int(m[1]))
    raise ValueError('Only source-shaped integer or sqrt(2)/sqrt(3) entries are supported')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def ordinal(n):return str(n)+('th' if 10<=n%100<=20 else {1:'st',2:'nd',3:'rd'}.get(n%10,'th'))
def sub(p):return (p['name'].lower() if p.get('inline') else '{'+p['name'].lower()+'}')+'_{'+str(p['i'])+str(p['j'])+'}'
def matrix(p,inline=False,name=None,period=False):
    rows=r' \\ '.join(' & '.join(row) for row in p['matrix'])
    name=p['name'] if name is None else name
    if inline:return name+r' = \begin{bmatrix}'+rows+r'\end{bmatrix}'
    return name+r'=[\begin{aligned}'+rows+r'\end{aligned}]'+('.' if period else '')
def prompt(p,template):
    s=sub(p)
    if template=='inline_radio':return f'Find the entry ${s}$ of the matrix ${p["name"]}$, where\n$'+matrix(p,True)+'$.'
    text=f'Find the entry ${s}$ of the matrix ${p["name"]}$, where \n\n$$\n'+matrix(p,period=True)+'\n$$'
    if template=='aligned_blank':text+='\n\n \n\n$'+s+'=$\n{{field-1}}'
    return text

def correct(p):
    n=len(p['matrix']);i,j=p['i'],p['j']
    return p['matrix'][i-1][j-1] if i<=n and j<=n else 'No such entry'
def solution(p,template,raw=None):
    i,j=p['i'],p['j'];s=sub(p);n=len(p['matrix'])
    if correct(p)=='No such entry':
        axis='row' if i>n else 'column';index=i if i>n else j
        return f'The entry ${s}$ should lie at the intersection of the ${i}${ordinal(i)[len(str(i)):]} row and ${j}${ordinal(j)[len(str(j)):]} column. \nSince ${p["name"]}$ is a ${n}\\times {n}$ matrix, it does not have the ${index}${ordinal(index)[len(str(index)):]} {axis}. \n\nTherefore, ${p["name"]}$ does not have the entry ${s}.$'
    text=f'The entry ${s}$ lies at the intersection of the ${i}${ordinal(i)[len(str(i)):]} row and ${j}${ordinal(j)[len(str(j)):]} column. Therefore, ${s}={correct(p)}.$'
    if template=='inline_radio':return text+'\n\n$'+matrix(p,True)+'$.'
    traits=SOURCE_PRESENTATION.get(raw,{})
    return text+'\n\n$$\n'+matrix(p,name=traits.get('solution_name',p['name']),period=traits.get('solution_period',template=='aligned_blank'))+'\n$$'

def validate_parameters(level,p,template,raw=False):
    if set(p)-{'matrix','i','j','name','opaque','inline'}:raise ValueError('Unknown parameter')
    if not re.fullmatch('[A-Z]',p.get('name','')):raise ValueError('Single uppercase matrix name required')
    n=len(p['matrix'])
    if n<2 or any(len(row)!=n for row in p['matrix']):raise ValueError('Square matrix required')
    for row in p['matrix']:
        for x in row:
            v=exact(x)
            if v.is_Integer and abs(v)>13:raise ValueError('Entry magnitude exceeds13')
    if type(p['i']) is not int or type(p['j']) is not int or min(p['i'],p['j'])<1:raise ValueError('Positive integer indices required')
    if level=='easy':
        if n not in (2,3,4):raise ValueError('Easy must retain2–4 source sizes')
        if template=='absent_radio':
            if n!=2 or max(p['i'],p['j'])!=3 or min(p['i'],p['j'])>2:raise ValueError('Easy absent bank is2x2 with exactly one index3')
        elif max(p['i'],p['j'])>n:raise ValueError('Lookup requires existing entry')
    else:
        size,depth={'moderate':(5,4),'hard':(6,5)}[level]
        if n!=size or max(p['i'],p['j'])<depth or max(p['i'],p['j'])>n or template=='absent_radio':raise ValueError('Authored visual-search workload guard violated')
    if template=='aligned_blank' and correct(p)=='No such entry':raise ValueError('Numeric blank requires existing entry')

def coordinates(recipe,p):
    i,j=p['i'],p['j'];n=len(p['matrix'])
    return {'target':(i,j),'left':(i,j-1),'right':(i,j+1),'up':(i-1,j),'down':(i+1,j),'transpose':(j,i),'transposed_first':(j,1),'last_diagonal':(n,n),'previous_diagonal':(n-1,n-1),'cell11':(1,1),'cell12':(1,2),'cell21':(2,1),'cell22':(2,2),'cell23':(2,3)}.get(recipe)
def bank_values(p,bank):
    vals=[];n=len(p['matrix'])
    for recipe in BANKS[bank][1]:
        if recipe=='missing':val='No such entry'
        elif recipe.startswith('opaque'):
            try:val=p['opaque'][int(recipe[-1])];exact(val)
            except (KeyError,IndexError):raise ValueError('Opaque source bank requires two explicit scalar slots')
        else:
            row,col=coordinates(recipe,p)
            if not(1<=row<=n and 1<=col<=n):raise SampleRejected('Whole bank has out-of-range coordinate')
            val=p['matrix'][row-1][col-1]
        vals.append(val)
    canon=[str(exact(v)) if v!='No such entry' else v for v in vals]
    if len(set(canon))!=len(canon):raise SampleRejected('Whole bank rejected on equivalent displayed options')
    if canon.count(str(exact(correct(p))) if correct(p)!='No such entry' else correct(p))!=1:raise SampleRejected('Whole bank requires unique correct option')
    return vals

def eligible_banks(level,template):
    if template=='aligned_radio':return ['transpose_neighbors','right_up_left','local_neighbors']
    if template=='aligned_blank':return ['blank']
    if template=='absent_radio':return ['all_four'] if level=='easy' else []
    return ['inline_diagonal']
def sample(level,template,bank,rng):
    n=rng.choice([2,3,4]) if level=='easy' else {'moderate':5,'hard':6}[level]
    if bank in ('transpose_neighbors','right_up_left','local_neighbors'):n=max(3,n)
    if bank=='inline_diagonal':n=max(3,n)
    if template=='absent_radio':n=2
    p={'matrix':[[rng.choice(VALUES) for _ in range(n)] for _ in range(n)],'name':rng.choice('ABGPR'),'i':rng.randint(1,n),'j':rng.randint(1,n),'inline':template=='inline_radio'}
    if bank=='q-13490':p['opaque']=[rng.choice(VALUES),rng.choice(VALUES)]
    if template=='absent_radio':
        if rng.randrange(2):p['i']=3
        else:p['j']=3
    return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    rng=random.Random(seed);raw_source=None
    if profile and profile.startswith('raw_'):
        raw_source=profile[4:];bank=raw_source
    else:bank=profile
    if bank is not None:
        if bank not in BANKS:raise ValueError('Unknown profile')
        implied=BANKS[bank][0]
        if template and template!=implied:raise ValueError('Profile/template mismatch')
        template=implied
    choices=[x for x in TEMPLATES if (level=='easy' or x!='absent_radio') and (not field_type or ('blank' if x=='aligned_blank' else 'radio')==field_type)]
    if template and template not in choices:raise ValueError('Unsupported template/field/difficulty')
    if raw_source and level!='easy':raise ValueError('Raw observed profiles belong to easy replay route')
    template=template or rng.choice(choices)
    # Deterministic default bank for explicit parameters; seed only shuffles choices.
    bank=bank or (eligible_banks(level,template)[0] if parameters is not None else rng.choice(eligible_banks(level,template)))
    if bank=='q-13490' and not raw_source:raise ValueError('Opaque historical bank is evidence-only; choose local_neighbors')
    for _ in range(5000):
        p=json.loads(json.dumps(parameters)) if parameters is not None else sample(level,template,bank,rng)
        if 'inline' in p and p['inline'] != (template=='inline_radio'):raise ValueError('Explicit inline presentation contradicts template')
        p['inline']=template=='inline_radio'
        try:
            validate_parameters(level,p,template,raw_source is not None)
            vals=bank_values(p,bank)
        except (SampleRejected,ValueError):
            if parameters is not None:raise
            continue
        break
    else:raise SampleRejected('Could not sample complete eligible bank')
    traits=SOURCE_PRESENTATION.get(raw_source,{})
    q={':question/problem':prompt(p,template)}
    if not traits.get('unrated'):q[':question/difficulty']=':question.difficulty/'+level
    if not traits.get('missing_solution'):q[':question/worked-solution']=solution(p,template,raw_source)
    # Raw profiles retain the historical capture; learner output uses matrices.
    if raw_source is None:
        for attr in (':question/problem', ':question/worked-solution'):
            if attr in q:q[attr]=q[attr].replace(r'[\begin{aligned}',r'\begin{bmatrix}').replace(r'\end{aligned}]',r'\end{bmatrix}')
    kind='blank' if template=='aligned_blank' else 'radio';key='field-1' if kind=='blank' else 'selection'
    bank_content=sorted([('text' if v=='No such entry' else 'math',v) for v in vals])
    identity={'version':VERSION,'display':q,'field':(kind,key),'bank':bank_content,'correct':None if traits.get('missing_correct') else correct(p)}
    content=digest(identity);qid=uid(content);fid=uid(content+':field:'+key)
    answers=[{':answer/id':uid(fid+':'+typ+':'+val),':answer/type':':answer.type/'+typ,':answer/value':val} for typ,val in bank_content]
    field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
    if not traits.get('missing_correct'):field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct(p))]
    if kind=='radio':random.Random(seed).shuffle(answers)
    q[':question/id']=qid;q[':question/answer-fields']=[field]
    task={'n':len(p['matrix']),'i':p['i'],'j':p['j'],'target':str(exact(correct(p))) if correct(p)!='No such entry' else 'No such entry'}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,'bank_profile':profile or bank,'recipes':list(BANKS[bank][1]),'parameter_fingerprint':digest(task),'content_fingerprint':content,'source_analysis':PROVENANCE,'plot_rating':'none','evidence_only':raw_source is not None,'eligible_for_learning':raw_source is None,'authored_extension':level!='easy' or bank not in SOURCE_PRESENTATION or (bank=='q-13506' and raw_source is None),'source_repairs':(['solution matrix E renamed to requested '+p['name']] if bank=='q-125593' and raw_source is None else [])+(['authored easy level, independently inferred correct ref, authored solution'] if bank=='q-13506' and raw_source is None else [])}}

# EASY — source2x2–4x4, direct lookup or observed existence check.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — authored5x5, deep index>=4, exactly the same one-entry lookup.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored6x6, deep index>=5, exactly the same one-entry lookup.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    lines=[q[':question/problem'],'','Choices:']+[('- $'+a[':answer/value']+'$' if a[':answer/type'].endswith('/math') else '- '+a[':answer/value']) for a in f[':answer-field/choices']]
    if ':answer-field/correct' in f:lines+=['','Correct: '+next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])]
    else:lines+=['','Raw source omits correct designation.']
    lines+=['',q.get(':question/worked-solution','Raw source omits worked solution.')]
    return '\n'.join(lines)
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['all','easy','moderate','hard'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template',choices=TEMPLATES);parser.add_argument('--profile');args=parser.parse_args()
    if args.count<1:parser.error('Positive count required')
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
