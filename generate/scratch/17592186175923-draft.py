#!/usr/bin/env python3
"""Private perpendicular-line generator and exact source replay, basis 2275.

No writes on import. Registered numeric script and its entire tree are immutable.
Every served instance uses three explicit points, exact rational arithmetic,
one complete chosen bank, and the source family's ordered solution stages.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
import argparse, copy, hashlib, importlib.util, json, random, re, uuid
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().with_suffix('')
def frozen(name):
    spec=importlib.util.spec_from_file_location('perp_points_private_'+name,HERE/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
fmt=frozen('math_format');parser=frozen('math_parser')
x,y=parser.SYMS['x'],parser.SYMS['y']
KP_ID=17592186175923
KP_UUID='44b9b212-27c4-5d6d-a221-cd85c25fc956'
TITLE='Finding the Equation of a Line Perpendicular to a Line Through Two Points'
VERSION='perpendicular-three-point-private-3'
LEVELS=('easy','moderate','hard')
SOURCE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
INCOMPLETE={'q-214038','q-22642'}
GRAPH='q-167797'
SIGN_ROWS={'q-103455','q-215768','q-237224','q-237225'}
DIFFERENCE_ROWS={'q-215768','q-23453','q-237036','q-72567','q-72568'}
POINT_SIGN_ROWS={'q-237036','q-72567','q-72568'}
FAMILIES={
    'easy-intercept-radio-three-slope-rows':['q-22642'],
    'easy-missing-diagram-text-repair':['q-167797'],
    'easy-intercept-blank-five-slope-rows':['q-215768'],
    'easy-intercept-radio-four-slope-rows':['q-23453'],
    'easy-intercept-blank-sign-stage':['q-237224','q-237225'],
    'translated-blank-three-slope-rows':['q-214038'],
    'translated-radio-three-slope-rows':['q-103440'],
    'translated-radio-sign-stage':['q-103455'],
    'translated-blank-difference-and-point-sign':['q-237036'],
    'translated-radio-difference-and-point-sign':['q-72567','q-72568'],
}
FAMILY={s:f for f,ss in FAMILIES.items() for s in ss}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def tex(v):return fmt.normalize_tex(sp.latex(sp.expand(v)))
def coord(p):return '('+','.join(map(str,p))+')'
def points(text):return [list(map(int,z)) for z in re.findall(r'\((-?\d+),\s*(-?\d+)\)',text)]
def original(s):
    pts=points(SOURCES[s][':question/problem'])
    if s==GRAPH:
        # Author-supplied repair, NOT recovered graph coordinates. Only -3 is evidenced.
        return {'P':pts[0],'A':[0,0],'B':[1,-3]}
    if len(pts)!=3:raise ValueError('unrecoverable supplied reference points')
    return dict(zip(('P','A','B'),pts))
def source_level(s):
    if s in INCOMPLETE:return 'moderate' if s=='q-214038' else 'easy'
    return SOURCES[s][':question/difficulty'][':db/ident'].split('/')[-1]
def field_type(s):return SOURCES[s][':question/answer-fields'][0][':answer-field/type'][':db/ident']
def values(p):
    h,k=p['P'];a,b=p['A'];c,d=p['B'];r=sp.Rational(d-b,c-a);m=-1/r
    return r,m,k-m*h
def line(t):
    left,right=t.split('=');poly=sp.Poly(sp.expand(parser.parse(left)-parser.parse(right)),x,y)
    if poly.total_degree()!=1:raise ValueError('not an entire straight-line equation')
    return poly.coeff_monomial(x),poly.coeff_monomial(y),poly.coeff_monomial(1)
def canonical_line(t):
    a,b,c=line(t);scale=a or b
    if not scale:raise ValueError('degenerate line')
    return tuple(str(sp.cancel(z/scale)) for z in (a,b,c))
def task_key(p,kind):
    a,b=p['A'];c,d=p['B'];dx=c-a;dy=d-b
    # Translations, endpoint separation, endpoint order, seed and bank order do not
    # create a new task. The reference direction and target point do.
    return digest(['perpendicular',str(sp.Rational(dy,dx)),p['P'],kind,'real plane'])
def raw_replay(s):
    missing=[]
    if s in INCOMPLETE:missing=['correct ref','worked solution']+(['answer value'] if s=='q-214038' else [])
    if s==GRAPH:missing=['reference diagram and its two coordinates absent from snapshot']
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':copy.deepcopy(SOURCES[s]),'generation':{'source_id':s,'source_basis':2275,'eligible':False,'origin':'immutable raw MA evidence','missing':missing}}

def profile(s,p):
    """Whole source profile: slope multiplier and exact incidence residual.

    Original option y=t*x+b0 -> new t=(t/m0)*m,
    new b=k-t*h+(b0-k0+t0*h0). Every original option is retained.
    This is an explicitly authored pattern extension, not inferred psychology.
    """
    _,m,b=values(p)
    if field_type(s).endswith('/blank'):return [tex(m*x+b)]
    old=original(s);_,m0,_=values(old);h0,k0=old['P'];h,k=p['P'];out=[]
    for answer in SOURCES[s][':question/answer-fields'][0][':answer-field/choices']:
        a,c,d=line(answer[':answer/value']);t=-a/c;intercept=-d/c
        slope=t/m0*m;residual=intercept-k0+t*h0
        out.append('y='+tex(slope*x+k-slope*h+residual))
    return out

def sub(a,b):return str(a)+'-'+('('+str(b)+')' if b<0 else str(b))
def simple_sub(a,b):return str(a)+('+'+str(-b) if b<0 else '-'+str(b))
def frac(a,b):return r'\frac{'+str(a)+'}{'+str(b)+'}'
def aligned(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def solution_blocks(s,p):
    h,k=p['P'];a,b=p['A'];c,d=p['B'];r,m,intercept=values(p)
    rows=[r'{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}}',' & ='+frac(sub(d,b),sub(c,a))]
    if s in SIGN_ROWS:rows.append(' & ='+frac(simple_sub(d,b),simple_sub(c,a)))
    if s in DIFFERENCE_ROWS:rows.append(' & ='+frac(d-b,c-a))
    rows.append(' & ='+tex(r)+('.' if s=='q-23453' else ''))
    first=aligned(rows)
    second='$$\n'+r'm\cdot ('+tex(r)+r')=-1\,⇒\,m='+tex(m)+'.\n$$'
    left=simple_sub('y',k);shift=simple_sub('x',h)
    rows=[r'y-{y}_{1} & =m(x-{x}_{1})',sub('y',k)+' & ='+tex(m)+'('+sub('x',h)+')']
    if s in POINT_SIGN_ROWS:rows.append(left+' & ='+tex(m)+'('+shift+')')
    rows.extend([left+' & ='+tex(m*(x-h)),'y & ='+tex(m*x+intercept)])
    return first,second,aligned(rows)
def solution(s,p):
    first,second,third=solution_blocks(s,p)
    if s in INCOMPLETE or s==GRAPH:
        a,b=p['A'],p['B'];target=p['P']
        return ('Perpendicular lines have slopes that are negative reciprocals of each other.\n\n'
            +f"First, let's find the slope ${{m}}_{{1}}$ of the line passing through the points ${coord(a)}$ and ${coord(b)}:$\n\n"+first
            +"\n\nSince we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy\n\n"+second
            +f'\n\nWe know that the line passes through the point ${coord(target)}.$ Using point-slope form and simplifying, we obtain the equation of the line'+(' in slope-intercept form:' if field_type(s).endswith('/blank') else ':')+'\n\n'+third)
    sol=SOURCES[s][':question/worked-solution'];it=iter([p['A'],p['B'],p['P']])
    sol=re.sub(r'\((-?\d+),\s*(-?\d+)\)',lambda _:coord(next(it)),sol)
    blocks=iter((first,second,third))
    return re.sub(r'\$\$\n.*?\n\$\$',lambda _:next(blocks),sol,flags=re.S)
def prompt(s,p):
    if s==GRAPH:
        return f'Write the equation of the line that passes through the point ${coord(p["P"])}$ and is perpendicular to the line passing through the points ${coord(p["A"])}$ and ${coord(p["B"])}.$\n\nThe slope-intercept form of the equation is $y=$\n{{{{field-1}}}}'
    it=iter([p['P'],p['A'],p['B']])
    return re.sub(r'\((-?\d+),\s*(-?\d+)\)',lambda _:coord(next(it)),SOURCES[s][':question/problem'])
def validate_parameters(s,p):
    if set(p)!={'P','A','B'} or any(len(pt)!=2 or any(type(v)!=int or abs(v)>100 for v in pt) for pt in p.values()):raise ValueError('bounded integer point triple required')
    if p['A'][0]==p['B'][0] or p['A'][1]==p['B'][1]:raise ValueError('source solution branch requires nonzero finite reference slope')
    # Easy explicit-point sources use a y-intercept target; the missing graph's
    # authored repair keeps its observed translated target workload separately.
    if source_level(s)=='easy' and s!=GRAPH and p['P'][0]!=0:raise ValueError('easy intercept-target family requires target x=0')
    if source_level(s)=='moderate' and p['P'][0]==0:raise ValueError('translated-target family requires target x nonzero')
def sample(s,rng):
    nonzero=[i for i in range(-8,9) if i]
    a,b=rng.randint(-6,6),rng.randint(-6,6);dx,dy=rng.choice(nonzero),rng.choice(nonzero)
    h=0 if source_level(s)=='easy' and s!=GRAPH else rng.choice(nonzero)
    return {'P':[h,rng.randint(-8,8)],'A':[a,b],'B':[a+dx,b+dy]}

@fmt.checked_math_content
def generate(level,seed=0,template=None,parameters=None,bank_profile=None):
    if level not in LEVELS:raise ValueError('invalid difficulty')
    rng=random.Random(seed);available=[s for s in SOURCES if source_level(s)==('moderate' if level=='hard' else level)]
    s=template or rng.choice(available)
    if s not in available:raise ValueError('template/level mismatch')
    selected=s if field_type(s).endswith('/radio') else None
    if bank_profile is not None and bank_profile!=selected:raise ValueError('profile must be the complete selected source profile')
    for _ in range(1000):
        p=copy.deepcopy(parameters) if parameters is not None else sample(s,rng);validate_parameters(s,p)
        vals=profile(s,p);_,m,b=values(p);kind=field_type(s)
        keys=[canonical_line(v) if kind.endswith('/radio') else str(parser.parse(v)) for v in vals]
        correct=[i for i,v in enumerate(vals) if canonical_line(v)==canonical_line('y='+tex(m*x+b))] if kind.endswith('/radio') else [0]
        if len(set(keys))==len(vals) and len(correct)==1:break
        if parameters is not None:raise ValueError('whole selected profile collides')
    else:raise ValueError('whole-bank sampler exhausted')
    old=SOURCES[s];of=old[':question/answer-fields'][0]
    replay=p==original(s) and s not in INCOMPLETE and s!=GRAPH
    problem=fmt.normalize_prose(old[':question/problem'] if replay else prompt(s,p))
    sol=fmt.normalize_prose(old[':question/worked-solution'] if replay else solution(s,p))
    if replay:vals=[fmt.normalize_tex(a[':answer/value']) for a in of[':answer-field/choices']]
    contract=[problem,sol,kind,of[':answer-field/key'],sorted(vals),vals[correct[0]]]
    content=digest(contract);qid=str(uuid.uuid5(uuid.UUID(KP_UUID),'content:'+content));fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+of[':answer-field/key']))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'value:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct[0]][':answer/id']]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':s,'family':FAMILY[s],'parameters':p,'bank_profile':selected,'source_id':s,'source_basis':2275,'eligible':True,'mathematical_fingerprint':task_key(p,kind),'content_hash':content,'plot_rating':'none','origin':'normalized source replay' if replay else 'authored missing-diagram textual repair' if s==GRAPH else 'authored completion of incomplete source' if s in INCOMPLETE else 'authored parameter variation','difficulty_origin':'authored hard; same moderate workload, no observed hard source' if level=='hard' else 'inferred for incomplete source' if s in INCOMPLETE else 'observed source level','domain':'real plane; finite nonzero reference slope; exact integer points','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def batch(level,count,seed=0,**kwargs):
    if type(count)!=int or not 1<=count<=1000:raise ValueError('count must be 1..1000')
    out=[];seen=set()
    for i in range(count*50):
        r=generate(level,seed+i,**kwargs);key=r['generation']['mathematical_fingerprint']
        if key not in seen:out.append(r);seen.add(key)
        if len(out)==count:return out
    raise ValueError('distinct-task sampler exhausted')
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--template');p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
    records=[r for l in (LEVELS if a.difficulty=='all' else (a.difficulty,)) for r in batch(l,a.count,a.seed,template=a.template)]
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n'.join(map(markdown,records)))
