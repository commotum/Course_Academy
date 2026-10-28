"""Seeded parametric arc-length integral questions. No repository or database access."""
import argparse, collections, hashlib, itertools, json, math, random, uuid
from pathlib import Path
import sympy as s
from math_format import normalize_prose, normalize_tex, checked_math_content
import legacy
T=legacy.T
HERE=Path(__file__).resolve().parent
KP=legacy.KP
LEVELS=('easy','moderate','hard')
FORMULA=r'L=\int_a^b\sqrt{\left(\frac{\mathrm{d}x}{\mathrm{d}t}\right)^2+\left(\frac{\mathrm{d}y}{\mathrm{d}t}\right)^2}\,\mathrm{d}t'

def tex(x):return s.latex(x)
def display(x):return '\n\n$$\n'+x+'\n$$\n\n'
def integ(body,a,b):return r'\int_{'+tex(a)+'}^{'+tex(b)+'}'+body+r'\,\mathrm{d}t'
def sqeq(a,b):return s.trigsimp(s.expand_trig(s.expand(a-b)))==0

def instance(family,p):
    """Ordered derivative inputs, then squared speed and lesson-supported final form."""
    a,b=map(s.sympify,p.get('bounds',[0,1]));A=s.Integer(p.get('A',2));B=s.Integer(p.get('B',3))
    m=s.Integer(p.get('m',2));n=s.Integer(p.get('n',3));sg=p.get('sign',1);k=p.get('k',1)
    fx=s.sin if p.get('fx','sin')=='sin' else s.cos
    fy=s.sin if p.get('fy','cos')=='sin' else s.cos
    note='Square the complete derivatives before adding, and retain the parameter limits.'
    if family=='exponential':
        x,y=A*T,B*s.exp(k*T)
        dx,dy=A,k*B*s.exp(k*T);rad=A*A+B*B*s.exp(2*k*T);speed=s.sqrt(rad)
        candidates=[(s.sqrt(i+j*s.exp(v*k*T)),f'linear/exponential coefficient error ({i}, {j}, exponent {v})')
                    for i,j,v in itertools.product(sorted(set([0,A,A*A,A**3,4*A*A])),sorted(set([B,B*B,B**3,4*B*B])),[1,2])]
    elif family=='trig':
        x,y=A*fx(m*T),B*fy(n*T);dx,dy=s.diff(x,T),s.diff(y,T)
        ux=s.cos(m*T) if fx==s.sin else s.sin(m*T)
        uy=s.cos(n*T) if fy==s.sin else s.sin(n*T)
        P,Q=A*m,B*n;rad=P*P*ux**2+Q*Q*uy**2;speed=s.sqrt(rad)
        # Complete error grid: missing, correct, or repeated chain/square factors.
        ps=sorted(set([A*A,A*A*m,P*P,P*P*m]+([P*P*m*m] if m==n else [])));qs=sorted(set([B*B,B*B*n,Q*Q,Q*Q*n]+([Q*Q*n*n] if m==n else [])))
        candidates=[(s.sqrt(i*ux**2+j*uy**2),f'chain/squaring errors ({i}, {j})') for i,j in itertools.product(ps,qs)]
        candidates += [(s.sqrt(P*P*(s.sin(m*T) if fx==s.sin else s.cos(m*T))**2+Q*Q*(s.sin(n*T) if fy==s.sin else s.cos(n*T))**2),'wrong trig derivatives')]
        if m!=n:
            note+=' The two trig arguments differ, so the Pythagorean identity cannot combine these terms.'
        elif fx!=fy and P==Q:
            rad=s.trigsimp(rad);speed=s.sqrt(rad)
            note+=r' The squared coefficients match. Use $\sin^2('+tex(m*T)+r')+\cos^2('+tex(m*T)+r')=1$ to simplify the speed.'
        else:
            note+=' The arguments match, but unequal squared coefficients prevent replacing the whole sum by a constant.'
        if m==n and fx!=fy:
            # Simplify every constant-speed alternative, not just the key.
            candidates=[(s.sqrt(s.trigsimp(v**2)) if not s.trigsimp(v**2).has(T) else v,recipe) for v,recipe in candidates]
    elif family=='sum':
        x,y=T+sg*A*s.sin(T),1+s.cos(B*T);dx,dy=s.diff(x,T),s.diff(y,T)
        rad=1+2*sg*A*s.cos(T)+A*A*s.cos(T)**2+B*B*s.sin(B*T)**2;speed=s.sqrt(rad)
        candidates=[]
        for c,h,j in [(0,1,1),(-2,1,1),(1,1,1),(4,4,4),(2,1,4),(2,4,1),(1,4,1),(2,0,1)]:
            r=1+c*sg*A*s.cos(T)+h*A*A*s.cos(T)**2+j*B*B*s.sin(B*T)**2
            # Conservative analytic lower bound for 1+c*A*cos+h*A²*cos².
            if h>0 and c*c<=4*h: candidates.append((s.sqrt(r),f'binomial/factor error ({c},{h},{j})'))
        note+=' Expand the binomial square, including its signed cross term.'
    elif family=='cosine_sum':
        x,y=A*s.cos(T),B*T+sg*s.cos(T);dx,dy=s.diff(x,T),s.diff(y,T)
        rad=(A*A+1)*s.sin(T)**2-2*sg*B*s.sin(T)+B*B;speed=s.sqrt(rad)
        candidates=[]
        for h,c,j in [(A*A,1,1),(1,2,1),(A*A+1,-2,1),(A*A+1,1,1),(A*A+1,2,2),(A*A+1,0,1),(2*(A*A+1),2,1)]:
            r=h*s.sin(T)**2-c*sg*B*s.sin(T)+j*B*B
            if j*B*B>=abs(c*B):candidates.append((s.sqrt(r),f'binomial/collection error ({h},{c},{j})'))
        note+=' Expand the binomial square, then collect the squared sine terms.'
    elif family=='product':
        x,y=A*s.exp(k*T),B*s.exp(k*T)*fx(T)
        dx,dy=s.diff(x,T),s.diff(y,T)
        cross=k if fx==s.sin else -k
        rad=A*A+B*B+cross*B*B*s.sin(2*T)
        speed=s.exp(k*T)*s.sqrt(rad)
        candidates=[]
        for j,h,l in [(0,1,1),(2,1,1),(1,2,1),(1,1,-1),(1,1,0),(1,1,2),(2,1,-1),(1,2,-1),(0,2,1)]:
            r=j*A*A+h*B*B+l*cross*B*B*s.sin(2*T)
            if j*A*A+h*B*B>=abs(l*B*B):
                candidates.append((s.exp(k*T)*s.sqrt(r),f'product/identity error ({j},{h},{l})'))
        note=(r'Apply the product rule to the exponential–trigonometric coordinate. Use $\sin^2t+\cos^2t=1$ and $2\sin t\cos t=\sin(2t)$. '
              +r'Since $e^{'+tex(k*T)+r'}>0$, its squared factor leaves the square root as $e^{'+tex(k*T)+r'}$.')
    else:raise ValueError(family)
    x+=p.get('hx',0);y+=p.get('hy',0)
    if p.get('swap'):x,y=y,x;dx,dy=dy,dx
    raw=s.Add(s.Pow(dx,2,evaluate=False),s.Pow(dy,2,evaluate=False),evaluate=False)
    return dict(x=x,y=y,a=a,b=b,dx=dx,dy=dy,raw=raw,rad=rad,speed=speed,candidates=candidates,note=note)

def mathematical_signature(z):
    # Main calculation, independent of shifts, orientation, bounds and banks.
    squares=[s.expand(v*v) for v in (z['dx'],z['dy'])]
    scale=s.gcd_list([c for v in squares for c in v.as_coefficients_dict().values()])
    return tuple(sorted(s.srepr(s.expand(v/scale)) for v in squares))

def numerical_integral(expr,a,b):
    # Composite Simpson is only a collision guard, never the answer engine.
    fn=s.lambdify(T,expr,'math');lo=float(a);hi=float(b);n=256;h=(hi-lo)/n
    return h/3*sum((1 if i in (0,n) else 4 if i%2 else 2)*fn(lo+i*h) for i in range(n+1))

def modal_winners(expressions):
    expanded=[s.expand(v**2).as_coefficients_dict() for v in expressions]
    terms=set().union(*(set(row) for row in expanded))
    modes={term:{v for v,n in collections.Counter(row.get(term,0) for row in expanded).items() if n==max(collections.Counter(row.get(term,0) for row in expanded).values())} for term in terms}
    return [i for i,row in enumerate(expanded) if all(row.get(term,0) in modes[term] for term in terms)]

def select_bank(z,rng):
    speed=z['speed'];pool=[];length=numerical_integral(speed,z['a'],z['b'])
    for value,recipe in z['candidates']:
        if sqeq(value**2,speed**2):continue
        try:
            if abs(numerical_integral(value,z['a'],z['b'])-length)<1e-5*max(1,abs(length)):continue
        except (ValueError,OverflowError):continue
        if any(sqeq(value**2,v**2) for v,_ in pool):continue
        pool.append((value,recipe))
    if len(pool)<4:raise ValueError('Insufficient distinct error alternatives')
    # Profile selected as a complete bank, never deterministic first-four pooling.
    for _ in range(96):
        selected=rng.sample(pool,4)+[(speed,'correct')]
        if not speed.has(T) and sum(not v.has(T) for v,_ in selected)<2:continue
        if speed.is_Integer and sum(v.is_Integer is True for v,_ in selected)<2:continue
        if len(modal_winners([v for v,_ in selected]))==1:continue
        rng.shuffle(selected)
        return selected
    raise ValueError('No bank without a unique modal-coefficient intersection')

@checked_math_content
def build(level,family,p,seed=0):
    z=instance(family,p);rng=random.Random(seed);bank=select_bank(z,rng)
    prompt='Which integral gives the arc length of the curve defined by'+display('x='+tex(z['x'])+r',\qquad y='+tex(z['y']))
    prompt+='from $t='+tex(z['a'])+'$ to $t='+tex(z['b'])+'$? '
    if level=='easy':prompt+='Use the arc-length formula.'+display(FORMULA)
    prompt+='Choose an integral expression. Do not evaluate it.'
    vals=[normalize_tex(integ(tex(v),z['a'],z['b'])) for v,_ in bank]
    final=normalize_tex(integ(tex(z['speed']),z['a'],z['b']))
    rows=[r'L&='+integ(r'\sqrt{'+tex(z['raw'])+'}',z['a'],z['b'])]
    if family=='product':
        # Keep each derivation row within the actual learner UI column.
        A=s.Integer(p.get('A',2));B=s.Integer(p.get('B',3));k=p.get('k',1)
        trig=s.sin(T) if p.get('fx','sin')=='sin' else s.cos(T)
        dtrig=s.diff(trig,T);cross=k if trig==s.sin(T) else -k
        rrows=[r'R(t)&='+tex(A*A)+r'+'+tex(B*B)+r'\left('+tex(k*trig+dtrig)+r'\right)^2',
               r'&='+tex(A*A)+r'+'+tex(B*B)+r'\sin^2t+'+tex(B*B)+r'\cos^2t',
               r'&\quad'+('+'if cross>0 else '-')+tex(2*B*B)+r'\sin t\cos t',
               r'&='+tex(z['rad'])]
        expansion=display(r'\begin{aligned}'+r'\\'.join(rrows)+r'\end{aligned}')
        rows=[r'L&='+integ(tex(s.exp(k*T))+r'\sqrt{R(t)}',z['a'],z['b'])]
    rows.append('&='+final)
    solution='For a parametric curve, use'+display(FORMULA)+r'Differentiate with respect to $t$:'+display(r'\begin{aligned}\frac{\mathrm{d}x}{\mathrm{d}t}&='+tex(z['dx'])+r'\\\frac{\mathrm{d}y}{\mathrm{d}t}&='+tex(z['dy'])+r'\end{aligned}')
    solution+=z['note']
    if family=='product':
        solution+=' Write the speed as $e^{'+tex(p.get('k',1)*T)+r'}\sqrt{R(t)}$, where'+expansion
    solution+=' Substitute and simplify:'+display(r'\begin{aligned}'+r'\\'.join(rows)+r'\end{aligned}')
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    qid=str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),json.dumps([prompt,solution,sorted(vals)])))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v}for v in vals]
    ci=next(i for i,(_,r) in enumerate(bank)if r=='correct')
    return {'knowledge_point':{'db_id':17592186092376,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[ci][':answer/id']]}]},'generation':{'version':'2.0.1','seed':seed,'family':family,'parameters':p,'error_profile':[r for _,r in bank],'source_basis':8652,'support':{'exponential':['a60afb71-a1f2-5589-86e8-84aaf38f221a','cc3bd690-ca55-553c-a4e9-d792028b4a9b'],'trig':['c6e26edb-f404-57aa-9e8d-fef8eb7ecc78','c054bd74-1fa8-50dc-aa8f-bc5a2717fef5'],'sum':['b418c2bf-fd1a-57e4-845f-5c5fb4e1bb93'],'cosine_sum':['a37e6009-e864-56bc-93ae-b166a2b05514'],'product':['d674e5dc-8a57-5368-b53e-8363dba234a5','e0dd8f03-2b52-5c0f-998b-d1530a2830f4']}[family]}}

def parameters(family,rng):
    p={'A':rng.choice([1,2,3,4,5]),'B':rng.choice([1,2,3,4,5]),'swap':rng.choice([False,True]),'hx':rng.randint(-2,2),'hy':rng.randint(-2,2)}
    p['bounds']=rng.choice([[0,1],[-1,1],[-1,0],[1,2],[0,2]])
    if family=='exponential':p['k']=rng.choice([-1,1])
    elif family=='trig':
        p.update(m=rng.choice([2,3,4]),n=rng.choice([2,3,4]),fx=rng.choice(['sin','cos']),fy=rng.choice(['sin','cos']))
        if p['m']==p['n'] and p['fx']==p['fy']:p['n']=5-p['m'] if p['m']!=4 else 2
        p['bounds']=rng.choice([[0,'pi/3'],['pi/4','pi/2'],[0,'pi/2']])
    elif family=='sum':p.update(A=rng.choice([2,3]),B=rng.choice([2,3,4,5]),sign=rng.choice([-1,1]))
    elif family=='cosine_sum':p.update(A=rng.choice([2,3,4]),B=rng.choice([5,6,7,8]),sign=rng.choice([-1,1]))
    else:p.update(k=rng.choice([-1,1]),fx=rng.choice(['sin','cos']))
    return p

def batch(level,count,seed):
    if count<1:raise ValueError('count must be positive')
    rng=random.Random(seed);families={'easy':['exponential'],'moderate':['trig','sum','cosine_sum','exponential'],'hard':['product']}[level]
    records=[];seen=set();attempts=0
    # Cycle families with seeded order; reject repeated derivative calculations.
    while len(records)<count:
        if attempts>max(1000,100*count):raise ValueError('Requested batch exhausts distinct calculations')
        if len(records)%len(families)==0:rng.shuffle(families)
        f=families[len(records)%len(families)];p=parameters(f,rng);attempts+=1
        sig=mathematical_signature(instance(f,p))
        if sig in seen:continue
        try:r=build(level,f,p,rng.randrange(2**63))
        except ValueError:continue
        seen.add(sig);records.append(r)
    return records

def replay():
    out=[]
    for mid,q in legacy.SOURCES.items():
        if q.get(':question/worked-solution') and q.get(':question/answer-fields',[{}])[0].get(':answer-field/correct'):
            out.append(legacy.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],0,template=mid,profile='source-replay'))
    # Published ordinary examples are already complete captured records.
    for q in json.loads((HERE/'published-exemplars.json').read_text()):
        out.append({'knowledge_point':{'db_id':17592186092376,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'source_replay':True}})
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=LEVELS+('all','unclassified'),default='moderate');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--source-replay',action='store_true');args=ap.parse_args()
    levels=LEVELS if args.difficulty=='all'else ['moderate'if args.difficulty=='unclassified'else args.difficulty]
    records=replay()if args.source_replay else [r for level in levels for r in batch(level,args.count,args.seed)]
    print(json.dumps(records,indent=2))
