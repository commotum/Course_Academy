#!/usr/bin/env python3
"""Seeded three-variable partial-derivative practice. No database or asset writes."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
import sympy as s
from batch_policy import shortcuts
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP=17592186192784
NS=uuid.UUID('b5cebc16-84c3-5ec8-b1f1-5f9c51a69d94')
X=s.symbols('x y z', real=True)
SOURCE={'easy':'c701d949-2d48-5058-b224-6149f2ad0e9c','moderate':'4f001fc3-1ece-55d3-b468-098ed948154d','hard':'a87ec839-cad9-515d-b29b-91381158b553'}
def tex(v): return s.latex(v,order='lex')
def uid(value): return str(uuid.uuid5(NS,value))
def aligned(rows): return '$$\n\\begin{aligned}\n'+r'\\'.join(rows)+'\n\\end{aligned}\n$$'
def pd(t): return r'\frac{\partial f}{\partial '+str(t)+'}'
def distinct_errors(key, errors):
    unique=[]
    for name,val in errors:
        if s.expand(val-key)==0 or any(s.expand(val-v)==0 for _,v in unique): continue
        unique.append((name,val))
    return unique

def record(difficulty,problem,solution,values,key_index,meta):
    problem=normalize_prose(problem);solution=normalize_prose(solution)
    vals=[normalize_tex(v) for v in values]
    identity=hashlib.sha256(json.dumps([problem,sorted(vals)],ensure_ascii=False).encode()).hexdigest()
    field_id=uid(identity+'/field')
    choices=[{':answer/id':uid(field_id+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
    q={':question/id':uid(identity),':question/problem':problem,':question/worked-solution':solution,
       ':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[
       {':answer-field/id':field_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
        ':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[key_index][':answer/id']]}]}
    return validate_generated_record({'knowledge_point':KP,'question':q,'assets':{},'generation':meta})

def construct(difficulty,rng,roles=None,role=0,outcome='positive',position=None,params=None):
    t,u,v=roles or rng.sample(list(X),3)
    a,b=rng.choice([-3,-2,-1,1,2,3]),rng.choice([-2,-1,1,2])
    n=rng.choice([2,3]);params=params or {}
    a=params.get('a',a);b=params.get('b',b);n=params.get('n',n)
    template={'easy':'power','moderate':'trig_sum','hard':'radical_at_point'}[difficulty]
    target=t if role==0 else u
    sub={};domain='All real coordinates.'
    if difficulty=='easy':
        m=params.get('m',rng.choice([2,3]))
        F=a*u*t**n+b*v**m;key=a*n*u*t**(n-1) if role==0 else a*t**n
        step=tex(a*u)+r'\cdot '+tex(n*t**(n-1))+'+0' if role==0 else tex(a*t**n)+r'\cdot 1+0'
        problem=f'Find ${pd(target)}$ for $f(x,y,z)={tex(F)}$. Treat ${", ".join(str(w) for w in X if w!=target)}$ as constants.'
        rows=[pd(target)+'&='+step,'&='+tex(key)]
        errors=[('differentiate '+str(w),s.diff(F,w)) for w in X if w!=target]
        errors += [('leave active term',a*u*t**n),('discard all',s.Integer(0)),('lose multiplier',n*t**(n-1) if role==0 else t**n),('retain inactive term',key+b*v**m),('negative power rule',-key),('omit power factor',a*u*t**(n-1) if role==0 else a*n*t**n)]
    elif difficulty=='moderate':
        # Both role cases have two contributions, while the constant/active factors swap.
        F=a*(u+v)*s.sin(t)+b*(t+v)*s.cos(u)
        if role==0:
            A=a*(u+v)*s.cos(t);B=b*s.cos(u)
            first=[A,a*(u+v)*s.sin(t),-A,(u+v)*s.cos(t),a*s.cos(t)]
            second=[B,-B,2*B,b*s.sin(u),b*(t+v)*s.cos(u)]
            step=r'\left('+tex(a*(u+v))+r'\right)\cos '+tex(t)+'+'+tex(b*s.cos(u))+r'\cdot 1'
        else:
            A=a*s.sin(t);B=-b*(t+v)*s.sin(u)
            first=[A,-A,2*A,a*s.cos(t),a*(u+v)*s.sin(t)]
            second=[B,-B,b*(t+v)*s.cos(u),-b*s.sin(u),-(t+v)*s.sin(u)]
            step=tex(a*s.sin(t))+r'\cdot 1+'+r'\left('+tex(b*(t+v))+r'\right)\left(-\sin '+tex(u)+r'\right)'
        key=A+B
        errors=[(f'factor-rule errors {i}/{j}',aa+bb) for i,aa in enumerate(first) for j,bb in enumerate(second) if i or j]
        problem=f'Find ${pd(target)}$ for $f(x,y,z)={tex(F)}$.'
        rows=[pd(target)+'&='+step,'&='+tex(key)]
    else:
        target=t if role==0 else u
        aa=params.get('aa',rng.choice([1,4]));bb=params.get('bb',rng.choice([1,4]))
        R=aa*t*t+bb*u*u;F=s.Mul(v,s.Pow(R,s.Rational(1,2),evaluate=False),evaluate=False)
        coefficient=aa if role==0 else bb
        derivative=coefficient*target*v/s.sqrt(R)
        # Choose signed Pythagorean coordinates BEFORE values; zero remains legitimate.
        pairs=[(3,4),(4,3),(0,3),(3,0)]
        pair=params.get('pair',rng.choice(pairs[:2] if outcome!='zero' else [pairs[2] if role==0 else pairs[3]]))
        tv=s.Rational(pair[0],s.sqrt(aa))*rng.choice([-1,1]);uv=s.Rational(pair[1],s.sqrt(bb))*rng.choice([-1,1]);vv=rng.choice([-2,-1,1,2])
        if outcome!='zero':
            coord=tv if role==0 else uv
            vv=abs(vv)*(1 if (coord>0)==(outcome=='positive') else -1)
        sub={t:tv,u:uv,v:s.Integer(vv)};sub=params.get('sub',sub)
        key=s.simplify(derivative.subs(sub));rr=s.simplify(R.subs(sub));cc=sub[target];ww=sub[v]
        if rr<=0: raise ValueError('Radical derivative requires a strictly positive radicand')
        errors=[('omit inner derivative',ww/(2*s.sqrt(rr))),('omit outside factor',coefficient*cc/s.sqrt(rr)),('omit inner coefficient',cc*ww/s.sqrt(rr)),('lose cancellation of two',key/2),('double cancellation',key*2),('wrong sign',-key),('differentiate other coordinate',s.diff(F,u if role==0 else t).subs(sub)),('differentiate outside multiplier',s.sqrt(rr)),('evaluate original',F.subs(sub)),('omit target coordinate',coefficient*ww/s.sqrt(rr)),('use radicand denominator',coefficient*cc*ww/rr)]
        point='('+','.join(tex(sub[w]) for w in X)+')'
        problem=f'For $f(x,y,z)={tex(F)}$, evaluate ${pd(target)}$ at the point ${point}$.'
        inner=2*coefficient*target
        rows=[pd(target)+'&='+tex(v)+r'\cdot\frac{1}{2\sqrt{'+tex(R)+r'}}\cdot '+tex(inner),
              '&='+r'\frac{'+tex(coefficient*target*v)+r'}{\sqrt{'+tex(R)+'}}',pd(target)+r'\big|_{'+point+'}&='+r'\frac{'+str(coefficient)+'('+tex(cc)+')('+tex(ww)+r')}{\sqrt{'+tex(rr)+'}}','&='+tex(key)]
        domain='Radicand strictly positive at the evaluation point; square root is the nonnegative real root.'
    intro=f'Differentiate with respect to ${target}$, holding ${"$ and $".join(str(w) for w in X if w!=target)}$ fixed. '
    if difficulty=='easy': intro+='The term involving only $'+str(v)+'$ differentiates to zero. Use the constant multiple and power rules.'
    elif difficulty=='moderate':intro+='Apply the sum rule. In each term, differentiate only the factors that depend on $'+str(target)+'$; all remaining factors stay fixed.'
    else:intro+='Use the constant multiple and chain rules, then substitute the coordinates. At this point the radicand is $'+tex(rr)+'>0$.'
    solution=intro+'\n\n'+aligned(rows)
    if params.get('source_profile'):
        # Exact complete exemplar banks, derived at their supplied parameters.
        # The ordinary sampler uses varied authored error profiles instead.
        if difficulty=='easy':
            source_values=[s.Integer(0),key,s.diff(F,u)+s.diff(F,v),a*u*t**n,a*n*t**(n-1)]
        elif difficulty=='moderate':
            source_values=[a*(u+v)*s.sin(t)+b*s.cos(u),key,a*(u+v)*s.cos(t)-b*(t+v)*s.sin(u),a*(u+v)*s.cos(t)+2*b*s.cos(u),a*(u+v)*s.cos(t)]
        else:source_values=[key/2,key,key/4,-key,F.subs(sub)]
        errors=[('exemplar error '+str(i),value) for i,value in enumerate(source_values) if s.expand(value-key)!=0]
    errors=distinct_errors(key,errors)
    if len(errors)<4: raise ValueError('Insufficient distinct meaningful errors')
    # One complete authored error profile: select four independent applicable recipes together.
    chosen=rng.sample(errors,4); rng.shuffle(chosen)
    pos=rng.randrange(5) if position is None else position
    bank=[tex(val) for _,val in chosen];bank.insert(pos,tex(key))
    bank_expressions=[s.sstr(val) for _,val in chosen];bank_expressions.insert(pos,s.sstr(key))
    meta={'bank_expressions':bank_expressions,'version':2,'template':template,'source_question_ids':[SOURCE[difficulty]],'target':str(target),
          'roles':[str(t),str(u),str(v)],'role':role,'error_profile':[name for name,_ in chosen],
          'expression':s.sstr(F),'derivative':s.sstr(s.diff(F,target)),'answer_expression':s.sstr(key),
          'substitution':{str(k):s.sstr(val) for k,val in sub.items()},'domain':domain,
          'parameters':{'a':a,'b':b,'n':n},'displayed_final':tex(key),'steps':rows,'conversions':[]}
    return record(difficulty,problem,solution,bank,pos,meta)

def _candidate_batch(difficulty,count,seed):
    rng=random.Random(seed); records=[];seen=set()
    # Coverage-oriented cycles are independent of parameter values and seed identity.
    permutations=list(itertools.permutations(X));rng.shuffle(permutations)
    positions=list(range(5));rng.shuffle(positions)
    cases=list(itertools.product([0,1],['positive','negative','zero']));rng.shuffle(cases)
    for i in range(count):
        role,outcome=cases[i%6]
        for attempt in range(200):
            try:r=construct(difficulty,rng,permutations[i%6],role,outcome,positions[i%5])
            except ValueError:continue
            qid=r['question'][':question/id']
            if qid in seen: continue
            r['generation'].update(seed=seed,index=i,attempt=attempt)
            seen.add(qid);records.append(r);break
        else:raise RuntimeError('Exhausted distinct valid instances')
    return records

def generate(difficulty,count,seed):
    # Stable seed stream, independent of inventory, preserves deterministic replay.
    # Reject complete candidate banks with a shared incidental cue, including
    # target/role/coefficient subgroups; option shuffling alone cannot repair it.
    stream=random.Random(seed)
    for attempt in range(512):
        candidate_seed=seed if attempt==0 else stream.getrandbits(64)
        records=_candidate_batch(difficulty,count,candidate_seed)
        if not shortcuts(records):
            for r in records:
                r['generation'].update(requested_seed=seed,batch_attempt=attempt)
            return records
    raise RuntimeError('Exhausted batches without a shared answer-bank shortcut')


def replay():
    result=[]
    for original in json.loads(Path(__file__).with_name('source-replay.json').read_text()):
        f=original[':question/answer-fields'][0];cs=f[':answer-field/choices'];key=f[':answer-field/correct'][':answer/id'];idx=next(i for i,a in enumerate(cs) if a[':answer/id']==key)
        result.append(record(original[':question/difficulty'][':db/ident'].split('/')[-1],original[':question/problem'],original[':question/worked-solution'],[a[':answer/value'] for a in cs],idx,{'template':'source-replay','source_question_ids':[original[':question/id']],'replay_only':True}))
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');p.add_argument('--replay-source',action='store_true');args=p.parse_args()
    if args.count<0:p.error('count must be nonnegative')
    output=replay() if args.replay_source else generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(output,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
