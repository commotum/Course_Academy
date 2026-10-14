#!/usr/bin/env python3
"""Cosecant general-properties generator, steps 3–7 only, math basis 1356.

Observed moderate families retain their own complete source sentences and steps.
Unrated originals have explicit raw replay with missing attributes preserved.
Easy and hard are authored curriculum-grounded workloads; no transformed curves,
trig equations, derivatives, or given-value periodicity/oddness calculations.
The graph is always the same untransformed y=csc x, so original assets are reused.
Whole subset banks are chosen before finite mathematical parameters. See evidence.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186176053
ROOT=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((ROOT/'source.json').read_text())
KP=SNAPSHOT['record']; VERSION='cosecant-properties-1'
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
NAMESPACE=uuid.UUID(KP[':knowledge-point/id'])
SUBSETS=('None','I only','II only','III only','I and II only','I and III only','II and III only','I, II, and III')
TRUTHS={'q-42912':7,'q-65310':5,'q-103811':4,'q-103814':6,'q-65307':4,'q-65308':2,'q-103812':0}
ORIGINAL={'q-42912':{'point':1,'ordinate':-1,'range_value':2},'q-65310':{'zero':1},'q-103811':{'asymptote':9,'left':-4,'right':6},'q-103814':{'asymptote':9,'sign':1},'q-65307':{'asymptote':1},'q-65308':{'shift':2,'domain':5},'q-103812':{'domain':15}}


def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def ident(x): return str(uuid.uuid5(NAMESPACE,x))
def subset(mask): return SUBSETS[(0,1,2,4,3,5,6,7).index(mask)]
def pi(k,half=False):
    if half: return r'\frac{'+('' if k==1 else '-' if k==-1 else str(k))+r'\pi }{2}'
    return ('' if k==1 else '-' if k==-1 else str(k))+r'\pi '
def validate_parameters(t,p):
    if set(p)!=set(ORIGINAL[t] if t in ORIGINAL else {'trio','mask'} if t=='basic_properties' else {'point','ordinate','asymptote','domain'}): raise ValueError('exact parameter keys required')
    if any(type(v) is not int for v in p.values()): raise ValueError('integer parameters required')
    if t in ORIGINAL:
        for k,v in p.items():
            if k in ('asymptote','zero') and t!='q-103814' and (abs(v)>19 or v%2==0): raise ValueError('odd half-multiple required; |k|<=19')
            if k=='asymptote' and t=='q-103814' and (not v or abs(v)>19): raise ValueError('nonzero integer multiple; |k|<=19')
            if k in ('left','right','shift') and (not v or v%2 or abs(v)>12): raise ValueError('nonzero even multiple; |k|<=12')
            if k in ('point','domain') and (not v or abs(v)>15): raise ValueError('nonzero integer multiple; |k|<=15')
            if k=='ordinate' and v not in (-1,1): raise ValueError('ordinate ±1')
            if k=='range_value' and v not in (-4,-3,-2,2,3,4): raise ValueError('range test magnitude 2..4')
            if k=='sign' and v not in (-1,1): raise ValueError('extremal ordinate ±1')
        if t=='q-103811' and p['left']==p['right']: raise ValueError('distinct shifts required')
    elif t=='basic_properties':
        if not 0<=p['trio']<10 or not 0<=p['mask']<8: raise ValueError('finite easy catalog bounds')
    else:
        if p['point'] not in (-11,-9,-7,-5,5,7,9,11): raise ValueError('hard signed nonprincipal odd half-multiple')
        if p['ordinate'] not in (-1,1): raise ValueError('ordinate ±1')
        if not 2<=abs(p['asymptote'])<=15 or not 2<=abs(p['domain'])<=15: raise ValueError('hard nonprincipal integer/half-integer objects')


def sample(t,r):
    p=dict(ORIGINAL.get(t,{}))
    if t in ORIGINAL:
        for k in p:
            if k in ('asymptote','zero'): p[k]=r.choice([i for i in range(-19,20) if i%2] if t!='q-103814' else [i for i in range(-19,20) if i])
            elif k in ('left','right','shift'): p[k]=r.choice([i for i in range(-12,13,2) if i])
            elif k in ('point','domain'): p[k]=r.choice([i for i in range(-15,16) if i])
            elif k=='range_value': p[k]=r.choice([-4,-3,-2,2,3,4])
            else: p[k]=r.choice([-1,1])
        if t=='q-103811':
            while p['left']==p['right']: p['right']=r.choice([i for i in range(-12,13,2) if i])
    elif t=='basic_properties': p={'trio':r.randrange(10),'mask':r.randrange(8)}
    else: p={'point':r.choice([-11,-9,-7,-5,5,7,9,11]),'ordinate':r.choice([-1,1]),'asymptote':r.choice([i for i in range(-15,16) if abs(i)>=2]),'domain':r.choice([i for i in range(-15,16) if abs(i)>=2])}
    return p


def source_text(t,p):
    """Replace complete mathematical slots in source-specific prompt/solution masks."""
    q=SOURCES[t]; problem=q[':question/problem']; solution=q.get(':question/worked-solution')
    pairs=[]
    if t=='q-42912': pairs=[('(π,-1)',f"({p['point']}π,{p['ordinate']})"),('y = 2',f"y = {p['range_value']}")]
    if t=='q-65310': pairs=[(r'zero at $x = \frac{π}{2}',r'zero at $x = \frac{'+str(p['zero'])+r'π}{2}')]
    if t=='q-103811': pairs=[(r'\frac{9\pi }{2}',pi(p['asymptote'],True)),('x-4\\pi ',f"x{p['left']:+d}\\pi "),('x+6\\pi ',f"x{p['right']:+d}\\pi ")]
    if t=='q-103814':
        pairs=[('9\\pi ',pi(p['asymptote']))]
        if p['sign']==-1: pairs += [('value $1$','value $-1$'),('value $1$', 'value $-1$'),(r'x=\frac{\pi }{2}+2n\pi ',r'x=-\frac{\pi }{2}+2n\pi ')]
    if t=='q-65307': pairs=[(r'\frac{\pi }{2}',pi(p['asymptote'],True))]
    if t=='q-65308': pairs=[('5\\pi ',pi(p['domain'])),('x+2\\pi ',f"x{p['shift']:+d}\\pi "),('n=1,',f"n={p['shift']//2},")]
    if t=='q-103812': pairs=[('15\\pi ',pi(p['domain']))]
    # At the original parameter set masks preserve exact source notation.
    if p==ORIGINAL[t]: pairs=[]
    for old,new in pairs:
        problem=problem.replace(old,new)
        if solution is not None: solution=solution.replace(old,new)
    return problem,solution,TRUTHS[t]

PROPERTIES=(
 ('The domain is all real numbers except integer multiples of $\\pi$.','The domain is all real numbers.',"The function's domain is all real numbers except the integer multiples of $\\pi$."),
 ('The range is $(-\\infty,-1]\\cup[1,\\infty)$.','The range is all real numbers.','The range of the function is $(-\\infty,-1]\\cup[1,\\infty)$. '),
 ('The graph has no zeroes.','The graph has a zero at $x=0$.','The cosecant graph does not intersect the $x$-axis.'),
 ('The graph does not intersect the $y$-axis.','The graph intersects the $y$-axis.','The graph does not intersect the $y$-axis, as $x=0$ is not in the domain.'),
 ('The function has no global minimum or maximum.','$y=1$ is the global minimum.','The range is unbounded above and below, so the function has no global minimum or maximum.'))
TRIOS=list(itertools.combinations(range(5),3))

def authored_text(t,p):
    if t=='basic_properties':
        facts=[PROPERTIES[i] for i in TRIOS[p['trio']]]; mask=p['mask']
        claims=[f[0] if mask&(1<<i) else f[1] for i,f in enumerate(facts)]
        rows=[f'- {f[2]} Hence, statement {"I II III".split()[i]} is {"true" if mask&(1<<i) else "false"}.' for i,f in enumerate(facts)]
    else:
        k=p['point']; y=p['ordinate']; a=p['asymptote']; d=p['domain']
        actual=int(sp.sin(sp.pi*sp.Rational(k,2))); truths=[y==actual,True, d%2!=0]; mask=sum((1<<i) for i,v in enumerate(truths) if v)
        claims=[f'The point $({pi(k,True)},{y})$ is on the graph.',f'$x={pi(a)}$ is a vertical asymptote.',f'$x={pi(d,True)}$ is in the domain.']
        rows=[f'- The cosecant takes the value ${actual}$ at $x={pi(k,True)}$. Hence, statement I is {str(truths[0]).lower()}.', '- The lines $x=n\\pi$ for any integer $n$ are the vertical asymptotes of the function. Hence, statement II is true.',f'- The domain excludes exactly the integer multiples of $\\pi$. The number ${pi(d,True)}$ is {"not " if truths[2] else ""}an integer multiple of $\\pi$. Hence, statement III is {str(truths[2]).lower()}.']
    prompt='Which of the following statements are true regarding the function $y=\\csc x$?\n\n'+'\n'.join(f'{"I II III".split()[i]}. {v}' for i,v in enumerate(claims))
    solution="Let's plot the graph of $y=\\csc x.$\n\n![](images/f1/f1b80c29b8f9f4d33aae94fc287d95b97cc5865b36ecc98f4f41e625dfc842e1.png)\n\nNow, let's go through each statement.\n\n"+'\n\n'.join(rows)
    return prompt,solution,mask


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'): raise ValueError('difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('radio only')
    r=random.Random(seed)
    # Pick a complete family/profile before its mathematical parameters.
    if profile and profile.startswith(('observed:','method:')):
        inferred=profile.split(':',1)[1]
        if template and template!=inferred: raise ValueError('profile/template mismatch')
        template=inferred
    t=template or (r.choice(list(SOURCES)) if level=='moderate' else 'basic_properties' if level=='easy' else 'indexed_properties')
    allowed=list(SOURCES) if level=='moderate' else ['basic_properties'] if level=='easy' else ['indexed_properties']
    if t not in allowed: raise ValueError('template outside difficulty scope')
    selected=profile or ('method:'+t if t in SOURCES else 'subset-errors')
    raw=selected.startswith('observed:')
    if selected not in (['observed:'+t,'method:'+t] if t in SOURCES else ['subset-errors']): raise ValueError('profile')
    # Authored full five-option bank: correct mask and four fixed bit-error operations.
    # Error operations xor one bit or all bits; chosen as a whole before parameters.
    p=dict(parameters) if parameters is not None else sample(t,r); validate_parameters(t,p)
    prompt,solution,mask=source_text(t,p) if t in SOURCES else authored_text(t,p)
    if t in SOURCES:
        values=[a[':answer/value'] for a in SOURCES[t][':question/answer-fields'][0][':answer-field/choices']]
    else: values=[subset(mask^e) for e in (0,1,2,4,7)]
    correct=next((v for v in values if v==subset(mask) or (mask==0 and v=='None of the listed')),None)
    if correct is None or len(set(values))!=5: raise ValueError('whole-bank rejection')
    if not raw:
        if t=='q-103814': prompt=prompt.replace('function. $$','function.')
        if solution is None:
            # Inferred missing solution, explicitly authored; no recovered wording claim.
            if t=='q-42912':
                rows=[f'The number ${p["point"]}\\pi$ is outside the domain, so the stated point is not on the graph.', 'The vertical asymptotes are $x=n\\pi$ for integer $n$.',f'The value ${p["range_value"]}$ lies in $(-\\infty,-1]\\cup[1,\\infty)$.']
            else: rows=['The domain excludes exactly the integer multiples of $\\pi$.','The graph has no zeroes.','The cosecant takes the value $-1$ at $x=-\\frac{\\pi}{2}+2n\\pi$ for integer $n$.']
            solution="Now, let's go through each statement.\n\n"+'\n\n'.join(f'- {v} Hence, statement {"I II III".split()[i]} is {str(bool(mask&(1<<i))).lower()}.' for i,v in enumerate(rows))
    # Identity follows visible content, bank, difficulty, and presence; bank order/seed excluded.
    rated=not(raw and ':question/difficulty' not in SOURCES[t])
    content={'version':VERSION,'level':level if rated else None,'prompt':prompt,'solution':solution,'bank':sorted(values),'correct_presence':not raw or ':answer-field/correct' in SOURCES[t][':question/answer-fields'][0]}
    uid=ident(digest(content)); fid=ident(uid+'/selection')
    answers=[{':answer/id':ident(fid+'/'+v),':answer/type':':answer.type/text',':answer/value':v} for v in values]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if content['correct_presence']: field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]
    r.shuffle(answers)
    question={':question/id':uid,':question/problem':prompt,':question/answer-fields':[field]}
    if solution is not None: question[':question/worked-solution']=solution
    if rated: question[':question/difficulty']=':question.difficulty/'+level
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'template':t,'profile':selected,'parameters':p,'seed':seed,'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},'truth_mask':mask,'correct_value':correct,'evidence_only':raw,'eligible_for_learning':not raw,'authorship':'observed masks' if t in SOURCES else 'authored missing-level workload','mathematical_fingerprint':digest({'level':level,'template':t,'parameters':{k:v for k,v in p.items() if not(t=='q-42912' and k=='ordinate')}}),'content_fingerprint':digest(content),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# Easy: authored three direct global property recognitions, no indexed objects.
def generate_easy(seed=0,**kw): return generate('easy',seed,**kw)
# Moderate: seven observed masks, including two explicitly inferred unrated layouts.
def generate_moderate(seed=0,**kw): return generate('moderate',seed,**kw)
# Hard: authored signed nonprincipal indexed objects; still only ±1/domain/asymptotes.
def generate_hard(seed=0,**kw): return generate('hard',seed,**kw)

def markdown(record):
    q=record['question']; f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Worked solution absent in raw source.]')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
