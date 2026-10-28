#!/usr/bin/env python3
"""Seeded scalar line-integral setup. Runtime is self-contained and database-free."""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, sys, uuid
from pathlib import Path
import sympy as s
import mpmath as mp
from math_format import normalize_prose, normalize_tex, validate_generated_record

t,x,y,z=s.symbols('t x y z',real=True)
VERSION='scalar-setup-2.2'
KP={'db_id':17592186133829,'id':'28f7479a-a84c-59fa-a7ea-9377c7e65b19','title':'Writing the Line Integral of a Scalar Function as a Definite Integral'}
FAMILIES={'easy':('parabola','circle'),'moderate':('difference','squares','quadratic','helix'),'hard':('product',)}
SOURCES={'parabola':'1bb4ae8a-0b75-5e62-bc9b-0900b739960b','circle':'f07dd3d3-606f-520f-a95e-04303aa32f24','difference':'13f50e74-e351-581a-98f5-c8e27aa5380d','squares':'e477990a-d15e-595b-a078-39c7382f9c05','quadratic':'9dd51c2a-c921-500f-b456-d9efa51cbc02','helix':'cfad2296-6fbf-598f-a4ed-63e51e9c1622','product':'95a57adc-8e0c-4280-a31a-c4913344e995'}
def tex(v): return s.latex(v,fold_short_frac=False)
def vec(v):return r'\langle '+', '.join(tex(c) for c in v)+r'\rangle'
def integral(e,lo,hi):return r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}'+tex(e)+r'\,\mathrm{d}t'
def aligned(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+'|'+v))
def simple(v):return s.factor(s.trigsimp(s.expand(v))) if v.has(s.sin,s.cos) else s.factor(v)
def sample_parameters(family,rng,sign=None,interval_sign=None):
    p={'m':rng.choice([-2,-1,1,2]),'a':rng.choice([1,2]),'b':rng.choice([1,2]),'c':rng.choice([-2,-1,1,2]),'d':rng.choice([-2,-1,1,2]),'role':rng.randrange(2),'sign':rng.choice([-1,1]) if sign is None else sign}
    p['lo'],p['hi']=rng.choice([(0,1),(0,2),(1,2),(1,3)])
    if family in ('circle','helix'):
        p['lo'],p['hi']=rng.choice([(0,s.pi/3),(s.pi/6,s.pi/2),(0,s.pi/2),(s.pi/6,s.pi/3)])
    if family=='product':
        p['lo'],p['hi']=rng.choice([(1,2),(1,3),(2,3)])
        if interval_sign is None:interval_sign=rng.choice([-1,1])
        if interval_sign<0:p['lo'],p['hi']=-p['hi'],-p['lo']
    return p

def model(family,p):
    m,a,b,c,d,role,sgn=(s.sympify(p[k]) for k in ('m','a','b','c','d','role','sign'))
    if family=='parabola':
        curve=(t,t*t); f=m*(x if role==0 else y)/(a*a*y+1)
        wrong=[('swap_numerator',m*(y if role==0 else x)/(a*a*y+1)),('wrong_denominator_coordinate',m*(x if role==0 else y)/(a*a*x+1))]
    elif family=='circle':
        curve=(s.cos(t),s.sin(t))
        f=m*x*y**(a+1) if role==0 else m*x**(a+1)*y
        wrong=[('lose_power',m*x*y**a if role==0 else m*x**a*y),('square_wrong_coordinate',m*x**(a+1)*y if role==0 else m*x*y**(a+1)),('omit_x',m*y**(a+1)),('omit_y',m*x)]
    elif family=='difference':
        curve=(t*t+a*t,t*t-a*t);f=m*s.sqrt(2)*(x+sgn*y)
        wrong=[('wrong_sign',m*s.sqrt(2)*(x-sgn*y)),('omit_y',m*s.sqrt(2)*x),('omit_x',m*s.sqrt(2)*sgn*y)]
    elif family=='squares':
        curve=(t*t,t-c,t+d);f=m*(2*x-y*y+sgn*z*z)
        wrong=[('wrong_z_sign',m*(2*x-y*y-sgn*z*z)),('wrong_y_sign',m*(2*x+y*y+sgn*z*z)),('omit_x',m*(-y*y+sgn*z*z)),('lose_square',m*(2*x-y+sgn*z))]
    elif family in ('quadratic','product'):
        curve=(t*t+c,t*t+d,t*t)
        if family=='quadratic':
            f=m*(x+y-z) if role==0 else m*(x-y+z)
            wrong=[('wrong_last_sign',f+2*m*z),('omit_coordinate',f-m*x),('wrong_first_sign',f-2*m*x)]
        else:
            f=m*(x*y+sgn*z) if role==0 else m*(x*z+sgn*y)
            wrong=[('wrong_sum_sign',m*(x*y-sgn*z) if role==0 else m*(x*z-sgn*y)),('product_as_sum',m*(x+y+sgn*z) if role==0 else m*(x+z+sgn*y)),('omit_addend',m*x*y if role==0 else m*x*z)]
    elif family=='helix':
        curve=(s.cos(t),s.sin(t),a*t);f=m*z*(x*x-y*y) if role==0 else m*z*(y*y-x*x)
        wrong=[('difference_as_sum',m*z*(x*x+y*y)),('lose_squares',m*z*(x-y) if role==0 else m*z*(y-x)),('square_difference',m*z*(x-y)**2),('omit_z',f/z)]
    else:raise ValueError(family)
    sub_raw=f.subs(dict(zip((x,y,z),curve)),simultaneous=True)
    sub=s.expand(sub_raw) if family not in ('circle','helix') else sub_raw
    derivative=tuple(s.diff(q,t) for q in curve)
    speed2=s.trigsimp(s.expand(sum(q*q for q in derivative)))
    speed=s.sqrt(speed2)
    if p['hi']<0:speed=s.refine(speed,s.Q.negative(t))
    elif p['lo']>=0:speed=s.refine(speed,s.Q.nonnegative(t))
    correct=s.factor(sub*speed) if family not in ('circle','helix') else sub*speed
    errors=[(name,s.factor(w.subs(dict(zip((x,y,z),curve)),simultaneous=True))*speed) for name,w in wrong]
    # Each error has a mathematical interpretation, not an arbitrary offset.
    errors += [('omit_speed',sub),('square_speed',sub*speed2),('reciprocal_speed',sub/speed),('reverse_arc_length_sign',-correct),('miss_factor_two',correct/2),('double_differential_factor',2*correct)]
    for j in range(len(curve)):
        partial=s.trigsimp(s.expand(speed2-derivative[j]**2))
        errors.append(('omit_derivative_component_'+str(j),sub*s.sqrt(partial)))
    return {'curve':curve,'f':f,'sub_raw':sub_raw,'sub':sub,'derivative':derivative,'speed2':speed2,'speed':speed,'correct':correct,'errors':errors}

def bank_values(expressions,lo,hi):
    """High precision integral-value collision guard; no evaluation is shown."""
    with mp.workdps(35):
        a,b=mp.mpf(str(s.N(lo,38))),mp.mpf(str(s.N(hi,38)))
        vals=[]
        for expr in expressions:
            fn=s.lambdify(t,expr,'mpmath')
            value=mp.quad(fn,[a,(a+b)/2,b])
            if abs(mp.im(value))>mp.mpf('1e-25') or not mp.isfinite(value):raise ValueError('nonreal bank')
            value=mp.re(value)
            if any(abs(value-v)<mp.mpf('1e-20')*(1+abs(v)) for v in vals):raise ValueError('colliding definite-integral values')
            vals.append(value)
        return [str(v) for v in vals]

def opposite_pair_cue(expressions):
    """Bank-only positive/negative counterpart cue; 0 means no correct prediction."""
    factored=[s.factor(e) for e in expressions]
    pairs=[(i,j) for i in range(5) for j in range(i)
           if s.factor(factored[i]+factored[j])==0]
    if len(pairs)!=1 or 0 not in pairs[0]:return 0
    coefficient=factored[0].as_independent(t,as_Add=False)[0]
    return 1 if coefficient.is_positive else -1 if coefficient.is_negative else 0

def build(family,p,rng,band=None,bank_guard=None):
    band=band or next(k for k,v in FAMILIES.items() if family in v)
    data=model(family,p);lo,hi=p['lo'],p['hi']
    # An authored mixed profile is an entire sampled quartet. If one member
    # collides, discard the entire profile rather than filling from a pool.
    finite_cache={}
    def complete_profiles():
        for _ in range(100):yield rng.sample(data['errors'],4)
        # Rare valid cases (including the canonical circle) have only a few
        # eligible full banks. Exhaust the finite profiles before resampling math.
        remaining=list(itertools.combinations(data['errors'],4));rng.shuffle(remaining)
        yield from remaining
    for selected in complete_profiles():
        expressions=[data['correct']]+[expr for _,expr in selected]
        # A unique intersection of modal constant coefficient and t-dependent
        # factor is an incidental choice-bank cue. Keep an ambiguous intersection.
        parts=[s.factor(e).as_independent(t,as_Add=False) for e in expressions]
        coefficients=[str(q[0]) for q in parts];cores=[str(q[1]) for q in parts]
        cm=max(coefficients.count(q) for q in coefficients);km=max(cores.count(q) for q in cores)
        intersection=[j for j in range(5) if coefficients.count(coefficients[j])==cm and cores.count(cores[j])==km]
        if len(intersection)==1:continue
        for e in expressions:
            if e not in finite_cache:
                finite_cache[e]=bool(s.limit(e,t,lo,dir='+').is_finite and s.limit(e,t,hi,dir='-').is_finite)
        if not all(finite_cache[e] for e in expressions):continue
        try:values=bank_values(expressions,lo,hi)
        except (ValueError,ZeroDivisionError):continue
        if bank_guard is not None and not bank_guard(expressions):continue
        break
    else:raise ValueError('not enough distinct plausible errors')
    # Preserve trig inputs: factor/expand polynomial arithmetic only.
    prompt=('Which of the following is equivalent to $\\int_C f\\,\\mathrm{d}s$, where $f('+','.join(('x','y','z')[:len(data['curve'])])+')='+tex(data['f'])+'$ and\n\n$$\n'+r'\mathbf r(t)='+vec(data['curve'])+r',\qquad '+tex(lo)+r'\le t\le '+tex(hi)+'.\n$$\n\nDo not evaluate the integral.')
    # The norm row shows the components, not just the CAS result.
    norm=r'\sqrt{'+ '+'.join('('+tex(q)+')^2' for q in data['derivative'])+'}'
    rows=[r"\mathbf r'(t)&="+vec(data['derivative']),r"\|\mathbf r'(t)\|&="+norm+'='+tex(s.sqrt(data['speed2']))]
    if family in ('quadratic','product'):
        rows[-1]+='='+tex(data['speed'])
        reason=('Since $t<0$ on this interval, $|t|=-t$.' if hi<0 else r'Since $t\ge0$ on this interval, $|t|=t$.')
    else:reason=''
    subrows=[r'f(\mathbf r(t))&='+tex(data['sub_raw'])]
    if data['sub_raw']!=data['sub']:subrows.append('&='+tex(data['sub']))
    solution=('Differentiate each coordinate and compute the speed:\n\n'+aligned(rows)+'\n\n'+reason+'\n\nSubstitute the coordinates into the scalar function:\n\n'+aligned(subrows)+'\n\nMultiply by speed and retain the parameter bounds:\n\n'+aligned([r'\int_C f\,\mathrm{d}s&=\int_{'+tex(lo)+'}^{'+tex(hi)+r"}f(\mathbf r(t))\,\|\mathbf r'(t)\|\,\mathrm{d}t",'&='+r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}('+tex(data['sub'])+')('+tex(data['speed'])+r')\,\mathrm{d}t','&='+integral(data['correct'],lo,hi)]))
    prompt,solution=normalize_prose(prompt),normalize_prose(solution)
    bank=[normalize_tex(integral(e,lo,hi)) for e in expressions]
    content=json.dumps([prompt,solution,sorted(bank),band],sort_keys=True)
    qid=uid(hashlib.sha256(content.encode()).hexdigest());fid=uid(qid+'|selection')
    answers=[{':answer/id':uid(fid+'|'+value),':answer/type':':answer.type/math',':answer/value':value} for value in bank]
    key=answers[0][':answer/id'];mapping={a[':answer/id']: {'error':label,'integrand':str(expr),'numeric_integral':value} for a,label,expr,value in zip(answers,['correct']+[e[0] for e in selected],expressions,values)}
    rng.shuffle(answers)
    record={'knowledge_point':KP,'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+band,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',key]}]},'generation':{'version':VERSION,'template':family,'parameters':{k:str(v) for k,v in p.items()},'source_question_ids':[SOURCES[family]],'authored_bank':True,'profile':[e[0] for e in selected],'choice_witnesses':mapping,'solution_path':{'substitution':str(data['sub']),'speed':str(data['speed']),'final':bank[0],'conversions': ['polynomial expansion and multiplication']+(['sqrt(t^2)=abs(t); interval resolves abs(t)'] if family in ('quadratic','product') else []),'support':['tutorial 35118cc3-1418-5f97-b94b-8c0c5b0c1f1d','prerequisite 17592186048418',SOURCES[family]]}}}
    return validate_generated_record(record)

def generate(band,count,seed):
    if band=='unclassified':band='moderate'
    rng=random.Random(seed);out=[];seen=set();cue_history={f:[] for f in FAMILIES[band]}
    # Cycle a shuffled family list; this keeps finite CLI batches representative.
    families=[]
    for i in range(count):
        if not families:families=list(FAMILIES[band]);rng.shuffle(families)
        family=families.pop()
        for attempt in range(100):
            p=sample_parameters(family,rng,interval_sign=(1 if i%2==0 else -1) if family=='product' else None)
            history=cue_history[family]
            def bank_guard(expressions):
                cue=opposite_pair_cue(expressions)
                return not history or not any(all(old==sign for old in history) and cue==sign for sign in (-1,1))
            try:rec=build(family,p,rng,band,bank_guard=bank_guard)
            except (ValueError,ZeroDivisionError):continue
            if rec['question'][':question/id'] not in seen:break
        else:raise ValueError('sampling exhausted')
        witnesses=rec['generation']['choice_witnesses'];key=rec['question'][':question/answer-fields'][0][':answer-field/correct'][1]
        expressions=[s.sympify(witnesses[key]['integrand'],locals={'t':t})]+[s.sympify(v['integrand'],locals={'t':t}) for k,v in witnesses.items() if k!=key]
        cue_history[family].append(opposite_pair_cue(expressions))
        seen.add(rec['question'][':question/id']);rec['generation'].update({'seed':seed,'batch_index':i});out.append(rec)
    return out

def replay_sources():
    """Evidence-only original-parameter banks; never used for normal practice."""
    profiles=json.loads(Path(__file__).with_name('source-profiles.json').read_text())
    recipes={
      'q-167608':(0,1,[4*t*t+1,t*t/s.sqrt(2*t+1),t/s.sqrt(4*t*t+1),t*(2*t+1),t*s.sqrt(4*t*t+1)],2),
      'q-40253':(0,s.sqrt(2),[4*t*s.sqrt(4*t*t+1),t*s.sqrt(2*t*t+1),s.sqrt(2)*t*s.sqrt(2*t*t-1),4*t*s.sqrt(8*t*t+1),2*t*s.sqrt(4*t*t+1)],0),
      'q-76377':(0,3,[-2*(t*t+2*t-1)*s.sqrt(t*t+1),-2*s.sqrt(2)*s.sqrt(2*t*t+1),-2*t*s.sqrt(t*t+1),s.sqrt(2)*(t*t-2*t)*s.sqrt(2*t*t+1),(t*t+2*t)*s.sqrt(2*t*t+1)],1),
      'q-76356':(0,2,[2*t*t*s.sqrt(t+1),2*s.sqrt(3)*t**3,s.sqrt(2)*(t*t-t)*s.sqrt(t+1),2*t*t*s.sqrt(t*t-t),s.sqrt(3)*t*t*s.sqrt(t*t+1)],1),
      'q-76379':(0,s.pi/2,[s.sqrt(2)*t*s.cos(t)*s.sqrt(2*s.cos(t)**2+1),s.sqrt(2)*t*s.cos(2*t),2*s.sqrt(2)*t*s.sin(t)*s.sqrt(2*s.cos(t)**2+3),2*t*(s.cos(t)-s.sin(t)),2*t*(s.cos(t)-s.sin(t))**2],1)}
    records=[]
    for source in profiles:
        lo,hi,expressions,idx=recipes[source['source_ma_id']]
        qid=uid('replay|'+source['source_id']);fid=uid(qid+'|selection')
        answers=[{':answer/id':uid(fid+'|'+str(j)),':answer/type':':answer.type/math',':answer/value':normalize_tex(integral(e,s.sympify(lo),s.sympify(hi)))} for j,e in enumerate(expressions)]
        rec={'knowledge_point':KP,'question':{':question/id':qid,':question/problem':source['problem'],':question/worked-solution':source['solution'],':question/difficulty':':question.difficulty/'+source['difficulty'],':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[idx][':answer/id']]}]},'generation':{'version':VERSION,'source_question_ids':[source['source_id']],'evidence_only':True,'eligible_for_learning':False,'profile':'historical source replay'}}
        records.append(validate_generated_record(rec))
    return records

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json'],default='json');parser.add_argument('--replay-source',action='store_true');args=parser.parse_args()
    if args.count<0:parser.error('count must be nonnegative')
    print(json.dumps(replay_sources() if args.replay_source else generate(args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
