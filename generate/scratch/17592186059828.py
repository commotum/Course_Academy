#!/usr/bin/env python3
"""Half-open number-line to interval translation, frozen v1.

Observed unrated banks are parameterized raw replay profiles; they preserve absent
solutions, difficulty and keys. q-31762 actually has two open endpoints: raw replay
is retained, while its explicit repair closes the left endpoint. All ordinary
E/M/H catalogs assess one bounded half-open segment only. Difficulty is authored:
easy labels every integer; moderate reads signed integers on alternate labels;
hard reads signed halves between whole labels. No unions, unbounded assessed
intervals, solving or radical estimation. All explicit inputs obey the same finite
catalogs as sampling. Full banks are chosen before computing their five members.
Assets are rendered with Matplotlib, using a read-only cached Python fallback.
Unique render inputs and atomic PNG/sidecar publication support concurrent calls.
No DB operations. Source provenance is math basis 1356.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,subprocess,tempfile,uuid
from pathlib import Path
from fractions import Fraction

KP_ID=17592186059828
KP_UUID='c8c3e092-d9ff-5dc9-ad1e-f31aa2b226ba'
TITLE='Translating Between Half-Open Intervals and Number Lines'
VERSION='half-open-numberlines-v2'
HERE=Path(__file__).resolve().with_suffix('')
ROOT=HERE.parents[2]
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATE='numberline_interval_radio'
PROFILES=('authored_left_shift','observed_left_ray','observed_negate_left','raw_q28850','raw_q31762','repair_q28850','repair_q31762')
ASSETS={'raw_q28850':'images/a2/a2cc171a455a193deab3555b823b715d887d372c8c9b57933f525edcfc99e150.png', 'raw_q31762':'images/a2/a2e3d6a49f516b3037e0be9cb74312a59d2a924a6ec768a72660485951bb0302.png'}
PROMPT='Which of the following intervals corresponds to the segment shown above?'
CANON=json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/canonical-example'][':question/worked-solution']
# Shared prose is exact canonical source; each math block is constructed from complete components.
OPENING=CANON.split('The given interval')[0]

def stable(value): return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(value): return str(uuid.uuid5(uuid.UUID(KP_UUID),str(value)))
def frac(value):
    if isinstance(value,bool): raise ValueError('Boolean coordinate')
    return Fraction(str(value))
def num(value):
    f=frac(value)
    return str(f.numerator) if f.denominator==1 else str(f.numerator)+'/'+str(f.denominator)
def latex(value):
    f=frac(value)
    return str(f.numerator) if f.denominator==1 else ('-' if f<0 else '')+r'\frac{'+str(abs(f.numerator))+'}{'+str(f.denominator)+'}'
def parameters(a,b,left_closed,tick,label):
    return {'left':num(a),'right':num(b),'left_closed':left_closed,'tick_step':num(tick),'label_step':num(label)}

# EASY: fully labelled integer endpoints, either orientation, signed or unsigned.
def catalog(level):
    rows=[]
    if level=='easy':
        pairs=[(Fraction(a),Fraction(b)) for a in range(-4,5) for b in range(a+1,5) if b-a<=4]; tick,label=1,1
    elif level=='moderate':
        pairs=[(Fraction(a),Fraction(b)) for a in range(-6,0) for b in range(a+2,7) if b-a<=6 and (a%2 or b%2)];tick,label=1,2
    elif level=='hard':
        pairs=[(Fraction(a,2),Fraction(b,2)) for a in range(-8,0) for b in range(a+2,9) if b-a<=8 and (a%2 or b%2)];tick,label=Fraction(1,2),1
    else:raise ValueError('Unknown difficulty')
    for a,b in pairs:
        for lc in (False,True):rows.append(parameters(a,b,lc,tick,label))
    return rows

def parse_parameters(level,p,profile):
    if not isinstance(p,dict) or set(p)!={'left','right','left_closed','tick_step','label_step'}:raise ValueError('Exact five parameter keys required')
    if not isinstance(p['left_closed'],bool):raise ValueError('left_closed must be bool')
    q=parameters(frac(p['left']),frac(p['right']),p['left_closed'],frac(p['tick_step']),frac(p['label_step']))
    if profile.startswith('raw_'):
        a,b=frac(q['left']),frac(q['right'])
        if not(-6<=a<b<=6 and a.denominator==b.denominator==1 and 1<=b-a<=6 and q['tick_step']==q['label_step']=='1'):raise ValueError('Raw observed fully labelled integer bounds')
        if q['left_closed']:raise ValueError('Raw observed left endpoint is open')
    elif q not in catalog(level):raise ValueError('Parameters violate authored level catalog')
    return q

def interval_text(a,b,lc,rc,profile):
    left=num(a) if a is not None else '- ∞'
    if profile in ('raw_q28850','repair_q28850','observed_left_ray') and lc and frac(a)<0 and frac(a).denominator==1:left='- '+str(abs(frac(a).numerator))
    return 'x ∈ '+('[' if lc else '(')+left+', '+num(b)+(']' if rc else ')')

def bank(p,profile):
    a,b=frac(p['left']),frac(p['right'])
    family='ray' if profile in ('raw_q28850','repair_q28850','observed_left_ray') else 'negate' if profile in ('raw_q31762','repair_q31762','observed_negate_left') else 'shift'
    # Every observed bank contains all four closure combinations as a complete bank.
    parts=[('both_open',a,b,False,False),('both_closed',a,b,True,True),('open_closed',a,b,False,True),('closed_open',a,b,True,False)]
    if family=='ray':parts += [('left_ray',None,b,False,True)]
    elif family=='negate':parts += [('negate_left',-a,b,False,False)]
    else:parts += [('shift_left',a-frac(p['tick_step']),b,p['left_closed'],not p['left_closed'])]
    if any(x[1] is not None and x[1]>=x[2] for x in parts):raise ValueError('Whole bank invalid: unordered endpoints')
    values=[interval_text(x[1],x[2],x[3],x[4],profile) for x in parts]
    semantic=[tuple(x[1:]) for x in parts]
    if len(set(semantic))!=5:raise ValueError('Whole bank collision')
    return [(x[0],v) for x,v in zip(parts,values)]

def solution(p,right_closed=None):
    lc=p['left_closed'];rc=not lc if right_closed is None else right_closed
    def colored(value,closed):return r'{\color{'+('blue' if closed else 'red')+'}{'+value+'}}'
    ineq=latex(p['left'])+r'\,\, '+colored(r'\leq' if lc else r'\lt',lc)+r' \,\, x \,\, '+colored(r'\leq' if rc else r'\lt',rc)+r' \,\, '+latex(p['right'])
    result=r'x\in '+colored('[' if lc else '(',lc)+latex(p['left'])+','+latex(p['right'])+colored(']' if rc else ')',rc)
    return OPENING+'The given interval can be represented by the following inequality:\n\n$$\n'+ineq+'\n$$\n\nWe can express our inequality in interval notation as follows:\n\n$$\n'+result+'\n$$'

def geometry(p,profile):
    a,b=frac(p['left']),frac(p['right']);step=frac(p['label_step'])
    lo=(a//step-1)*step;hi=-((-b)//step)*step+step
    return {'left':float(a),'right':float(b),'left_closed':p['left_closed'],'right_closed':False if profile=='raw_q31762' else not p['left_closed'],'tick_step':float(frac(p['tick_step'])),'label_step':float(step),'lo':float(lo),'hi':float(hi)}

def render_plots(p,profile,output_dir=None):
    if profile in ASSETS:
        expected=parameters(-1,2,False,1,1) if profile=='raw_q28850' else parameters(1,4,False,1,1)
        if p==expected:return {'prompt':ASSETS[profile],'source_reused':True,'geometry':geometry(p,profile)}
    g=geometry(p,profile);out=Path(output_dir) if output_dir else HERE/'plots';out.mkdir(parents=True,exist_ok=True)
    name=stable({'renderer':VERSION,'renderer_hash':hashlib.sha256((HERE/'renderer.py').read_bytes()).hexdigest(),'geometry':g})[:24];png=out/(name+'.png');side=out/(name+'.json')
    if not(png.exists() and side.exists()):
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='render-input-',dir=out,delete=False) as f:
            json.dump({'geometry':g,'png':str(png),'sidecar':str(side)},f);inputpath=Path(f.name)
        try:subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE/'renderer.py'),str(inputpath)],check=True,capture_output=True,text=True)
        finally:inputpath.unlink(missing_ok=True)
    return {'prompt':str(png),'sidecar':str(side),'source_reused':False,'geometry':g}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
    if template not in (None,TEMPLATE):raise ValueError('Unknown template')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source radio layout')
    profile=profile or 'authored_left_shift'
    if profile not in PROFILES:raise ValueError('Unknown profile')
    rng=random.Random(seed)
    if parameters is None:
        if profile.startswith('raw_'):raise ValueError('Raw source replay requires explicit parameters')
        eligible=[]
        for row in catalog(level):
            try:bank(row,profile);eligible.append(row)
            except ValueError:pass
        if not eligible:raise ValueError('No eligible complete banks')
        p=rng.choice(eligible)
    else:p=parse_parameters(level,parameters,profile)
    values=bank(p,profile);plots=render_plots(p,profile)
    problem='![]('+plots['prompt']+')\n\n'+PROMPT
    raw=profile.startswith('raw_');worked=None if raw else solution(p)
    ident=stable({'version':VERSION,'prompt':problem,'solution':worked,'bank':sorted(v for _,v in values),'difficulty':None if raw else level})
    qid=uid(ident);fid=uid(qid+'/selection')
    choices=[{':answer/id':uid(fid+'/'+value),':answer/type':':answer.type/math',':answer/value':value} for _,value in values]
    rng.shuffle(choices)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
    question={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
    if not raw:
        correct=interval_text(frac(p['left']),frac(p['right']),p['left_closed'],not p['left_closed'],profile)
        field[':answer-field/correct']=[':answer/id',uid(fid+'/'+correct)]
        question.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':worked})
    fp=stable({'left':p['left'],'right':p['right'],'left_closed':p['left_closed'],'right_closed':plots['geometry']['right_closed'],'tick_step':p['tick_step'],'label_step':p['label_step']})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':TEMPLATE,'bank_profile':profile,'parameters':p,'mathematical_fingerprint':fp,'content_fingerprint':ident,'source':SOURCE,'raw_replay':raw,'evidence_only':raw,'difficulty_origin':'authored; originals unrated','recipes':[x for x,_ in values],'plots':plots,'catalog_count':len(catalog(level)),'scope_repair':'q-31762 closed-left half-open replacement' if profile=='repair_q31762' else None}}

# MODERATE: signed integer endpoints, unit ticks, alternate labels; at least one endpoint is unlabelled.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: signed half-integer endpoints, half-unit ticks and integer labels; at least one half is read.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Original solution, difficulty and key are absent.]')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
