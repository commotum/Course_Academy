"""Seeded practice for described polar points; source replays retain legacy work."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import random
import uuid
from pathlib import Path
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id':17592186092218, 'id':'87f80908-037b-56ae-a2b5-59bdc49f0acb',
      'title':'Finding the Cartesian Coordinates of a Point Given a Description of the Radius and Angle'}
ANGLES = (0,30,45,60,90,120,135,150,180,210,225,240,270,300,315,330)
NONAXIS = tuple(d for d in ANGLES if d % 90)
RADII = tuple(map(s.Integer, range(2,13))) + (s.Rational(1,2),s.Rational(1,3),s.Rational(1,4),s.Rational(3,2),s.Rational(5,2))
VERSION = 'polar-description-2'

def tex(v):
    return normalize_tex(s.latex(s.simplify(v)))

def pair(v):
    return '(' + tex(v[0]) + ',' + tex(v[1]) + ')'

def uid(*v):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(v,sort_keys=True)))

def angle(d, unit):
    return str(d)+r'^{\circ}' if unit=='degrees' else tex(s.Rational(d,180)*s.pi)

def normalize_record(record):
    """Normalize all displayed content BEFORE content identity assignment."""
    q=record['question']
    for key in (':question/problem', ':question/worked-solution'):
        q[key]=normalize_prose(q[key])
    for f in q[':question/answer-fields']:
        old=f.get(':answer-field/correct')
        oldid=old[1] if isinstance(old,list) else old.get(':answer/id') if old else None
        for a in f[':answer-field/choices']:
            a[':answer/value']=normalize_tex(a[':answer/value'])
            a['_correct']=a[':answer/id']==oldid
    identity=[q[':question/problem'],q[':question/worked-solution'],q[':question/difficulty'],
              [[f[':answer-field/key'],f[':answer-field/type'],[(a[':answer/value'],a['_correct']) for a in f[':answer-field/choices']]] for f in q[':question/answer-fields']]]
    digest=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    q[':question/id']=uid(VERSION,digest)
    for f in q[':question/answer-fields']:
        f[':answer-field/id']=uid(q[':question/id'],f[':answer-field/key'])
        for a in f[':answer-field/choices']:
            a[':answer/id']=uid(f[':answer-field/id'],a[':answer/value'])
            if a.pop('_correct'):
                f[':answer-field/correct']=[':answer/id',a[':answer/id']]
    record['generation']['content_fingerprint']=digest
    return validate_generated_record(record)

def error_candidates(r,c,z,x,y):
    """Every candidate is a complete, interpretable wrong calculation."""
    return {
        'swap_coordinates':(y,x), 'reverse_x':(-x,y), 'reverse_y':(x,-y),
        'reverse_both':(-x,-y), 'omit_radius':(c,z),
        'reciprocal_radius':(c/r,z/r), 'omit_half':(2*x,2*y),
        'extra_half':(x/2,y/2), 'extra_half_x':(x/2,y),
        'extra_half_y':(x,y/2), 'omit_half_x':(2*x,y),
        'omit_half_y':(x,2*y),
    }

def bank(r,c,z,x,y,rng,profile):
    candidates=error_candidates(r,c,z,x,y)
    # Profile changes the *complete* set of likely mistakes, before order shuffle.
    profiles={
        'scale_order':['omit_radius','reciprocal_radius','swap_coordinates','extra_half','omit_half','reverse_x','reverse_y'],
        'sign_scale':['reverse_x','reverse_y','reverse_both','omit_radius','extra_half','omit_half','swap_coordinates'],
        'component_scale':['extra_half_x','extra_half_y','omit_half_x','omit_half_y','swap_coordinates','reverse_both','omit_radius'],
    }
    eligible={}
    for name in profiles[profile]:
        v=tuple(s.simplify(a) for a in candidates[name])
        if v!=(x,y) and v not in eligible.values():eligible[name]=v
    combinations=list(itertools.combinations(eligible,4));rng.shuffle(combinations)
    for names in combinations:
        selected=[(x,y)]+[eligible[name] for name in names]
        # Do not let a coordinate-frequency intersection supply the answer.
        freq=[{v[j]:sum(w[j]==v[j] for w in selected) for v in selected} for j in (0,1)]
        modal=[i for i,v in enumerate(selected) if all(freq[j][v[j]]==max(freq[j].values()) for j in (0,1))]
        if modal==[0]:continue
        # Angle signs alone must leave genuine scaling/order work in a radio task.
        signs=tuple(map(s.sign,(x,y)))
        if sum(tuple(map(s.sign,v))==signs for v in selected)<2:continue
        rng.shuffle(selected)
        return selected,list(names)
    raise ValueError('No complete distinct error bank without an incidental cue')

def make(level,d,r,unit,shape,rng,profile='sign_scale',point='P'):
    r=s.sympify(r)
    if level not in ('easy','moderate','hard') or d not in ANGLES or r<=0:
        raise ValueError('Invalid instance')
    a=angle(d,unit); rt=tex(r)
    theta=s.Rational(d,180)*s.pi
    c,z=s.cos(theta),s.sin(theta)
    x,y=s.simplify(r*c),s.simplify(r*z)
    # The ordered path is shared by key, solution, and choices.
    derivation=[('x',r'\cos',c,x),('y',r'\sin',z,y)]
    prompt=(f'The distance from ${point}$ to the origin is ${rt}$. '
            f'The ray from the origin through ${point}$ makes an angle of ${a}$ '
            'measured counterclockwise from the positive $x$-axis. '
            f'Find the exact Cartesian coordinates of ${point}$.')
    if level=='easy':
        prompt+=f'\n\nUse $x=r\\cos\\theta$ and $y=r\\sin\\theta$, with $\\cos({a})={tex(c)}$ and $\\sin({a})={tex(z)}$.'
    if shape=='blank':
        prompt+='\n\n$(x,y)=(${{field-1}}$,$ {{field-2}}$)$'
    solution=f'The description gives $r={rt}$ and $\\theta={a}$. '
    if d%90:
        quadrant=d//90+1
        ref=min(d%180,180-d%180)
        solution+=f'The angle is in quadrant ${quadrant}$ with reference angle ${angle(ref,unit)}$. '
    else:
        axis={0:'positive $x$',90:'positive $y$',180:'negative $x$',270:'negative $y$'}[d]
        solution+=f'The point is on the {axis}-axis. '
    solution+=f'Thus $\\cos({a})={tex(c)}$ and $\\sin({a})={tex(z)}$.\n\n'
    solution+='Use $x=r\\cos\\theta$ and $y=r\\sin\\theta$. Calculate the horizontal coordinate first, then the vertical coordinate:\n\n'
    for name,trig,t,v in derivation:
        solution+='$$\n\\begin{aligned}\n'+name+'&=r'+trig+r'\theta\\'+'\n'
        solution+='&=('+rt+')'+trig+'('+a+r')\\'+'\n'
        solution+='&=('+rt+')('+tex(t)+r')\\'+'\n'
        solution+='&='+tex(v)+'\n\\end{aligned}\n$$\n\n'
    if level=='hard':
        root=2 if d%90==45 else 3
        solution+=f'The radical product uses $\\sqrt{{{root}}}\\sqrt{{{root}}}={root}$.\n\n'
    solution+=f'Therefore the Cartesian coordinates are ${pair((x,y))}$. '
    solution+=f'As a check, $x^2+y^2={tex(x*x)}+{tex(y*y)}={tex(r*r)}=r^2$.'
    fields=[];used=[]
    if shape=='radio':
        vals,used=bank(r,c,z,x,y,rng,profile)
        spec=[('selection',[pair(v) for v in vals],pair((x,y)))]
    elif shape=='blank':
        spec=[('field-1',[tex(x)],tex(x)),('field-2',[tex(y)],tex(y))]
    else: raise ValueError('Unknown response shape')
    for key,values,correct in spec:
        choices=[{':answer/id':uid(key,i,v),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)]
        fields.append({':answer-field/key':key,':answer-field/type':':answer-field.type/'+shape,
                       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in choices if a[':answer/value']==correct)]})
    record={'knowledge_point':KP,'question':{':question/problem':prompt,':question/worked-solution':solution,
            ':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields},
            'generation':{'version':VERSION,'template':unit+'_'+shape,'parameters':{'radius':str(r),'degrees':d,'unit':unit},
                          'profile':profile if shape=='radio' else 'coordinate_blanks','error_recipes':used,
                          'source_ids':['3454059c-9847-5bb2-9732-e33885afa462'],
                          'path':[{'coordinate':n,'operator':t,'input':a,'unit_value':tex(v),'product':f'({rt})({tex(v)})','final':tex(out)} for n,t,v,out in derivation]}}
    return normalize_record(record)

def generate_batch(level,count,seed):
    rng=random.Random(seed);records=[];seen=set();work_seen=set();deck=[]
    last_position={};position_rng=random.Random(f'polar/positions/{seed}')
    if count<0:raise ValueError('count must be nonnegative')
    for i in range(count):
        # Stratify angle decisions through a shuffled deck without seed-specific rules.
        if not deck:
            deck=list(ANGLES if level=='moderate' else NONAXIS);rng.shuffle(deck)
        d=deck.pop()
        for attempt in range(1000):
            if level=='easy':r=s.Integer(rng.randint(2,6));unit='degrees';shape='radio'
            elif level=='moderate':r=rng.choice(RADII);unit=rng.choice(('degrees','radians'));shape=rng.choice(('radio','blank'))
            elif level=='hard':r=rng.randint(1,6)*s.sqrt(2 if d%90==45 else 3);unit='radians';shape='blank'
            else:raise ValueError('Unknown difficulty')
            ref=min(d%180,180-d%180)
            task=(str(r),d);work=(str(r),ref)
            # Do not recycle an essential scaling calculation within short batches.
            if task in seen or work in work_seen and count<=12:continue
            profile=rng.choice(('scale_order','sign_scale','component_scale'))
            record=make(level,d,r,unit,shape,rng,profile)
            if shape=='radio':
                # A short delivered family must not be answered by repeating a
                # position. Choose uniformly from positions other than the last
                # one in this visible angle family, without changing its bank.
                family='axis' if d%90==0 else '45' if d%90==45 else '30-60'
                field=record['question'][':question/answer-fields'][0]
                choices=field[':answer-field/choices']
                correct_id=field[':answer-field/correct'][1]
                current=next(j for j,a in enumerate(choices) if a[':answer/id']==correct_id)
                positions=[j for j in range(len(choices)) if j!=last_position.get(family)]
                target=position_rng.choice(positions)
                choices.insert(target,choices.pop(current))
                last_position[family]=target
                record=normalize_record(record)
            record['generation'].update(seed=seed,batch_index=i)
            records.append(record);seen.add(task);work_seen.add(work);break
        else:raise ValueError('Requested batch exceeds distinct supported instances')
    return records

def replay_source(source_id):
    import legacy
    if source_id=='q-276782':
        return make('moderate',180,s.Integer(5),'radians','blank',random.Random(0))
    case=next(c for c in json.loads((Path(__file__).parent/'replay_data/source-cases.json').read_text()) if c['source_id']==source_id)
    if source_id in ('q-17133','q-8522'):raise ValueError('Partial evidence is not served')
    record=legacy.generate(case['level'],0,case['template'],parameters=case['parameters'],profile=case['bank_profile'])
    return normalize_record(record)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--source-case')
    args=ap.parse_args()
    records=[replay_source(args.source_case)] if args.source_case else generate_batch('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
