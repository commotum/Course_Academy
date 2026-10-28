#!/usr/bin/env python3
"""Portable half-open number-line generator adapted from the supplied v2 draft.
Source replay preserves original fields and complete banks; normal sampling supports
only the source-justified moderate integer band. No database or publication calls.
"""
from __future__ import annotations
import copy,sys,os
import argparse,hashlib,json,random,re,subprocess,tempfile,uuid
from pathlib import Path
from fractions import Fraction

KP_ID=17592186059828
KP_UUID='c8c3e092-d9ff-5dc9-ad1e-f31aa2b226ba'
TITLE='Translating Between Half-Open Intervals and Number Lines'
VERSION='half-open-numberlines-portable-v3'
HERE=Path(__file__).resolve().parent
SOURCE={'database':'math','basis':2275,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATE='numberline_interval_radio'
PROFILES=('authored_left_shift','observed_left_ray','observed_right_ray','observed_negate_left','raw_q28850','raw_q31762','repair_q28850','repair_q31762','source_q31779')
ASSETS={'raw_q28850':'images/a2/a2cc171a455a193deab3555b823b715d887d372c8c9b57933f525edcfc99e150.png', 'raw_q31762':'images/a2/a2e3d6a49f516b3037e0be9cb74312a59d2a924a6ec768a72660485951bb0302.png'}
from math_format import normalize_prose,normalize_tex,validate_generated_record
PROMPT='Which of the following intervals corresponds to the segment shown above?'
CONTEXT=json.loads((HERE/'source-context.json').read_text())
SOURCE=CONTEXT['source']
CANON=CONTEXT['canonical'][':question/worked-solution']
NORMAL_PROFILES=('observed_left_ray','observed_right_ray','observed_negate_left')
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

def catalog(level):
    if level != 'moderate':
        raise ValueError('Unsupported sampling band: '+level+'; only moderate has a supported half-open source')
    return [parameters(a,b,lc,1,1)
            for a in range(-4,6) for b in range(a+1,7) if b-a<=6
            for lc in (False,True)]

def parse_parameters(level,p,profile):
    if not isinstance(p,dict) or set(p)!={'left','right','left_closed','tick_step','label_step'}:raise ValueError('Exact five parameter keys required')
    if not isinstance(p['left_closed'],bool):raise ValueError('left_closed must be bool')
    q=parameters(frac(p['left']),frac(p['right']),p['left_closed'],frac(p['tick_step']),frac(p['label_step']))
    if profile.startswith('raw_'):
        a,b=frac(q['left']),frac(q['right'])
        if not(-6<=a<b<=6 and a.denominator==b.denominator==1 and 1<=b-a<=6 and q['tick_step']==q['label_step']=='1'):raise ValueError('Raw observed fully labelled integer bounds')
        if q['left_closed']:raise ValueError('Raw observed left endpoint is open')
    elif profile=='source_q31779' and level=='moderate' and q==parameters(2,4,True,1,1):pass
    elif q not in catalog(level):raise ValueError('Parameters violate authored level catalog')
    return q

def interval_text(a,b,lc,rc,profile):
    left=num(a) if a is not None else '- ∞'
    if profile in ('raw_q28850','repair_q28850','observed_left_ray') and lc and frac(a)<0 and frac(a).denominator==1:left='- '+str(abs(frac(a).numerator))
    return 'x ∈ '+('[' if lc else '(')+left+', '+num(b)+(']' if rc else ')')

def bank(p,profile):
    a,b=frac(p['left']),frac(p['right'])
    family='right_ray' if profile in ('observed_right_ray','source_q31779') else 'ray' if profile in ('raw_q28850','repair_q28850','observed_left_ray') else 'negate' if profile in ('raw_q31762','repair_q31762','observed_negate_left') else 'shift'
    # Every observed bank contains all four closure combinations as a complete bank.
    parts=[('both_open',a,b,False,False),('both_closed',a,b,True,True),('open_closed',a,b,False,True),('closed_open',a,b,True,False)]
    if family=='ray':parts += [('left_ray',None,b,False,True)]
    elif family=='right_ray':parts += [('right_ray',a,None,True,False)]
    elif family=='negate':parts += [('negate_left',-a,b,False,False)]
    else:parts += [('shift_left',a-frac(p['tick_step']),b,p['left_closed'],not p['left_closed'])]
    if any(x[1] is not None and x[2] is not None and x[1]>=x[2] for x in parts):raise ValueError('Whole bank invalid: unordered endpoints')
    values=[('x ∈ ['+num(x[1])+', ∞)') if x[2] is None else interval_text(x[1],x[2],x[3],x[4],profile) for x in parts]
    semantic=[tuple(x[1:]) for x in parts]
    if len(set(semantic))!=5:raise ValueError('Whole bank collision')
    return [(x[0],v) for x,v in zip(parts,values)]

def solution(p,right_closed=None,source_style=False):
    lc=p['left_closed'];rc=not lc if right_closed is None else right_closed
    if source_style:
        opening='Every inequality can be expressed as an interval. We use the following notations:\n\n- Parentheses $()$ if the endpoints are *not* included.\n\n- Brackets $[]$ if the endpoints *are* included.\n\n'
        inequality=latex(p['left'])+r'\,\,'+(r'\le ' if lc else '<')+r'\,\,x\,\,'+(r'\le ' if rc else '<')+r'\,\,'+latex(p['right'])
        final=r'x\in '+('[' if lc else '(')+latex(p['left'])+','+latex(p['right'])+(']' if rc else ')')
        return opening+'The given interval can be represented by the following inequality:\n\n$$\n'+inequality+'\n$$\n\nWe can express our inequality in interval notation as follows:\n\n$$\n'+final+'\n$$'
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
    g=geometry(p,profile);out=Path(output_dir or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',''))
    if not output_dir and not os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'):
        raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required for new diagrams')
    out=out.resolve();out.mkdir(parents=True,exist_ok=True)
    name=stable({'renderer':VERSION,'renderer_hash':hashlib.sha256((HERE/'renderer.py').read_bytes()).hexdigest(),'geometry':g})[:24];png=out/(name+'.png');side=out/(name+'.json')
    if not(png.exists() and side.exists()):
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='render-input-',dir=out,delete=False) as f:
            json.dump({'geometry':g,'png':str(png),'sidecar':str(side)},f);inputpath=Path(f.name)
        try:subprocess.run([sys.executable,str(HERE/'renderer.py'),str(inputpath)],check=True,capture_output=True,text=True)
        finally:inputpath.unlink(missing_ok=True)
    return {'prompt':str(png),'sidecar':str(side),'source_reused':False,'geometry':g}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level != 'moderate':raise ValueError('Only moderate sampling is supported')
    if template not in (None,TEMPLATE):raise ValueError('Unknown template')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source radio layout')
    if type(seed) is not int:raise ValueError('seed must be a built-in int')
    rng=random.Random(seed)
    profile=profile or rng.choice(NORMAL_PROFILES)
    if profile not in NORMAL_PROFILES:raise ValueError('Unsupported sampling profile')
    if type(seed) is not int:raise ValueError('seed must be a built-in int')
    if parameters is None:
        if profile.startswith('raw_'):raise ValueError('Raw source replay requires explicit parameters')
        lc=rng.choice((False,True))
        eligible=[]
        for row in catalog(level):
            if row['left_closed'] != lc:continue
            try:bank(row,profile);eligible.append(row)
            except ValueError:pass
        if not eligible:raise ValueError('No eligible complete banks')
        p=rng.choice(eligible)
    else:p=parse_parameters(level,parameters,profile)
    values=bank(p,profile);plots=render_plots(p,profile)
    problem='![]('+plots['prompt']+')\n\n'+PROMPT
    raw=profile.startswith('raw_');worked=None if raw else solution(p,source_style=profile=='source_q31779')
    problem=normalize_prose(problem)
    worked=normalize_prose(worked) if worked is not None else None
    values=[(recipe,normalize_tex(value)) for recipe,value in values]
    # Asset destination is not part of semantic identity.
    identity_problem=problem.replace(plots['prompt'],Path(plots['prompt']).name)
    ident=stable({'version':VERSION,'prompt':identity_problem,'solution':worked,'bank':sorted(v for _,v in values),'difficulty':None if raw else level})
    qid=uid(ident);fid=uid(qid+'/selection')
    choices=[{':answer/id':uid(fid+'/'+value),':answer/type':':answer.type/math',':answer/value':value} for _,value in values]
    rng.shuffle(choices)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
    question={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
    if not raw:
        correct=normalize_tex(interval_text(frac(p['left']),frac(p['right']),p['left_closed'],not p['left_closed'],profile))
        field[':answer-field/correct']=[':answer/id',uid(fid+'/'+correct)]
        question.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':worked})
    fp=stable({'left':p['left'],'right':p['right'],'left_closed':p['left_closed'],'right_closed':plots['geometry']['right_closed'],'tick_step':p['tick_step'],'label_step':p['label_step']})
    result={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
            'generation':{'version':VERSION,'seed':seed,'template':TEMPLATE,'bank_profile':profile,
                          'parameters':p,'mathematical_fingerprint':fp,'content_fingerprint':ident,
                          'source':SOURCE,'difficulty_origin':'moderate source q-31779; integer half-open variations',
                          'recipes':[x for x,_ in values],'plots':plots,'catalog_count':len(catalog(level)),
                          'solution_prose_origin':'supplied canonical e-10787'}}
    return result if raw else validate_generated_record(result)

# Moderate: fully labelled integer endpoints, matching the source graph workload.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Compatibility wrappers explicitly reject unsupported sampling bands.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Original solution, difficulty and key are absent.]')
def replay_source(source_id):
    """Reconstruct all source choices by their mathematical recipes and retain capture fields.

    Missing ratings, keys and worked solutions remain missing, including open-interval
    exceptions. Canonical image paths stay unchanged. No source records are published.
    """
    cases=json.loads((HERE/'source-cases.json').read_text())
    source=next(c['record'] for c in cases if c['source_id']==source_id)
    q=copy.deepcopy(source)
    a,b,lc,rc={'q-28850':(-1,2,False,True),'q-31762':(1,4,False,False),
               'q-154795':(-3,2,False,False),'q-31779':(2,4,True,False)}[source_id]
    values=[interval_text(a,b,l,r,'replay') for l,r in ((False,False),(True,True),(False,True),(True,False))]
    values += [{'q-28850':'x ∈ (- ∞, 2]', 'q-31762':'x ∈ (-1, 4)',
                'q-154795':r'x\in (-\infty,2)', 'q-31779':r'x\in [2,\infty)'}[source_id]]
    def equivalent(v):
        return normalize_tex(v).replace(' ','').replace('∈',r'\in').replace('∞',r'\infty')
    for c in q[':question/answer-fields'][0][':answer-field/choices']:
        match=[v for v in values if equivalent(v)==equivalent(c[':answer/value'])]
        if len(match)!=1:raise ValueError('Source choice not reproduced: '+c[':answer/value'])
        # Keep the captured spacing after mathematical reconstruction.
    if ':question/worked-solution' in q:
        q[':question/worked-solution']=solution(parameters(a,b,lc,1,1),right_closed=rc,source_style=True)
    image=re.search(r'!\[\]\((.*?)\)',source[':question/problem'])[1]
    q[':question/problem']='![]('+image+')\n\n'+PROMPT
    return q

def generate_batch(level,seed=0,count=1,profile=None,template=None):
    if type(seed) is not int or type(count) is not int:raise ValueError('seed/count must be integers')
    if level!='moderate':raise ValueError('Only moderate sampling is supported')
    if count<1:raise ValueError('count must be positive')
    if profile is not None and profile not in NORMAL_PROFILES:raise ValueError('Unsupported profile')
    # Assign the decision case and complete bank first, then compatible bounds.
    # Track semantic instances, so a new profile/order cannot disguise repetition.
    rng=random.Random(seed);records=[];seen=set()
    capacity=len(catalog(level))
    if count>capacity:raise ValueError('count exceeds semantic capacity '+str(capacity))
    for i in range(count):
        selected=profile or rng.choice(NORMAL_PROFILES)
        lc=rng.choice((False,True))
        def candidates(selected,lc):
            rows=[]
            for p in catalog(level):
                if p['left_closed']!=lc or (p['left'],p['right'],lc) in seen:continue
                try:bank(p,selected)
                except ValueError:continue
                rows.append(p)
            return rows
        rows=candidates(selected,lc)
        if not rows:
            # Finite-domain exhaustion only; all remaining decisions stay eligible.
            options=[(profile,cl,candidates(profile,cl)) for cl in (False,True)] if profile else [(pr,cl,candidates(pr,cl)) for pr in NORMAL_PROFILES for cl in (False,True)]
            options=[x for x in options if x[2]]
            if not options:raise ValueError('Selected profile capacity exhausted')
            selected,lc,rows=rng.choice(options)
        p=rng.choice(rows);seen.add((p['left'],p['right'],lc))
        records.append(generate(level,seed=seed+i,parameters=p,profile=selected,template=template))
    return records

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',default='moderate',choices=('easy','moderate','hard'))
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=('markdown','json'),default='json')
    args=parser.parse_args()
    try:records=generate_batch(args.difficulty,args.seed,args.count)
    except ValueError as error:parser.error(str(error))
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
