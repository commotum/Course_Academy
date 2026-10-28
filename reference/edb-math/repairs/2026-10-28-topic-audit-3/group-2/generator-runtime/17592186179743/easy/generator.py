#!/usr/bin/env python3
"""Seeded, relocatable circulation practice. No database access or runtime repo imports."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import random
import uuid

os.environ.setdefault('MPLCONFIGDIR', '/tmp/course-academy-circulation-mpl')
import sympy as sp
from math_format import normalize_prose, validate_generated_record
from generator_policy import nonempty_checkbox

X, Y = sp.symbols('x y', real=True)
KP = {'db_id': 17592186179743, 'id': '1da220a9-2afc-5b63-a423-a4d2b3de9567', 'title': 'Circulation in Conservative Vector Fields'}
NS = uuid.UUID('8a029f2d-a612-55a0-bc35-c7647cdb25ce')
VERSION = 'circulation-1.0.0'
EASY = ['polynomial', 'rational', 'atan', 'exp_sin', 'exp_ratio', 'power']
MODERATE = ['poly2', 'poly1', 'exp', 'log', 'xexp', 'atan']


def tex(expr):
    return sp.latex(expr).replace(r'\operatorname{atan}', r'\arctan')


def math(expr):
    return '$' + expr + '$'


def display(expr):
    return '\n\n$$\n' + expr + '\n$$\n\n'


def identity(text):
    return str(uuid.uuid5(NS, text))


def pack(level, prompt, solution, statements, metadata):
    """Normalize the whole public surface before deriving any owned identity."""
    prompt, solution = normalize_prose(prompt), normalize_prose(solution)
    statements = [(normalize_prose(k), bool(v)) for k, v in statements]
    payload = json.dumps([level, prompt, solution, statements], ensure_ascii=False, sort_keys=True)
    qid = identity(payload)
    fields = []
    for i, (label, truth) in enumerate(statements):
        fid = identity(qid + '/field/' + str(i))
        choices = [{':answer/id': identity(fid + '/' + value), ':answer/type': ':answer.type/text', ':answer/value': value} for value in ('false', 'true')]
        fields.append({':answer-field/id': fid, ':answer-field/key': label, ':answer-field/type': ':answer-field.type/checkbox', ':answer-field/choices': choices, ':answer-field/correct': [':answer/id', choices[int(truth)][':answer/id']]})
    return validate_generated_record({'knowledge_point': KP.copy(), 'question': {':question/id': qid, ':question/difficulty': ':question.difficulty/' + level, ':question/problem': prompt, ':question/worked-solution': solution, ':question/answer-fields': fields}, 'generation': {'version': VERSION, **metadata}})


def potential(family, a, b, c):
    if family == 'polynomial': return a*X**2 + b*Y**2 + c*X*Y
    if family == 'rational': return a/(1 + X**2 + Y**2)
    if family == 'atan': return a*Y**2*sp.atan(b*X)
    if family == 'exp_sin': return a*sp.exp(Y) - sp.sin(b*X*Y)
    if family == 'exp_ratio': return a*sp.exp(b*X*Y)/(1+X**2)
    if family == 'power': return sp.Integer(abs(a)+2)**(-X-b*Y) + sp.sqrt(2)
    raise ValueError(family)


def components(family, a, b, c, conservative=True):
    if family == 'poly2':
        k = a if conservative else a + (1 if a != -1 else 2)
        return a*Y**2+b*X, 2*k*X*Y+c
    if family == 'poly1':
        k = a if conservative else a + (1 if a != -1 else 2)
        return b*X**2+a*Y, k*X+c
    if family == 'exp': return a*sp.exp(X+Y)+b*X, a*sp.exp(X+Y)+c*Y
    if family == 'log': return -2*a*X/(1+X**2+Y**2), -2*a*Y/(1+X**2+Y**2)
    if family == 'xexp': return a*X*sp.exp(Y)+b, a*X**2*sp.exp(Y)/2+c*Y
    if family == 'atan': return 2*a*X*sp.atan(b*Y), a*b*X**2/(1+b**2*Y**2)+c*Y
    raise ValueError(family)


def criterion(P, Q):
    py, qx = sp.diff(P,Y), sp.diff(Q,X)
    cons = sp.simplify(py-qx) == 0
    text = 'Write ' + math('P='+tex(P)) + ' and ' + math('Q='+tex(Q)) + '. The cross partials are' + display(r'\begin{aligned}P_y&='+tex(py)+r'\\Q_x&='+tex(qx)+r'.\end{aligned}')
    if cons:
        text += r'They agree everywhere. The components have continuous partial derivatives on the simply connected domain $\mathbb R^2$, so $\mathbf F$ is conservative.'
    else:
        text += r'They do not agree identically. Equality of the cross partials is necessary for a smooth field to be conservative, so $\mathbf F$ is not conservative. On this domain, if all closed-path integrals were zero, path independence would give a potential. Thus some closed path has nonzero circulation.'
    return cons, text


def theorem():
    return 'For a conservative field with potential '+math('f')+', the fundamental theorem gives'+display(r'\int_C\mathbf F\cdot\mathrm d\mathbf r=f(B)-f(A).')+'For such a conservative field, a closed path has the same endpoints, so its circulation is zero in either orientation. An open path can also have zero work when its endpoint potential values agree; zero work is not guaranteed for every open path.'


def general_bank(cons, profile, easy=False):
    """A complete three-statement profile; polarity is semantic, not a filler value."""
    p0,p1,p2 = profile
    first = (r'$\mathbf F$ is '+('conservative.' if p0 else '**not** conservative.'), cons if p0 else not cons)
    if p1 == 0:
        second = (r'$\oint_C\mathbf F\cdot\mathrm d\mathbf r=0$ for every closed path $C$.',cons)
    elif p1 == 1:
        second = (r'$\oint_C\mathbf F\cdot\mathrm d\mathbf r\ne0$ for some closed path $C$.',not cons)
    else:
        # Every nonconservative family here still has a retraced zero-work closed path.
        second = (r'$\oint_C\mathbf F\cdot\mathrm d\mathbf r\ne0$ for every closed path $C$.',False)
    if p2:
        third = (r'$\int_C\mathbf F\cdot\mathrm d\mathbf r\ne0$ for some open path $C$.',True)
    else:
        third = (r'$\int_C\mathbf F\cdot\mathrm d\mathbf r=0$ for every path $C$, including open paths.',False)
    return [first,second,third]


def finalize_bank(bank,rng):
    bank = list(bank)
    rng.shuffle(bank)
    bank.append(('None of the above',not any(v for _,v in bank)))
    return bank


def explain(bank, explanations=None):
    return '\n\n'+'\n'.join('- '+label+' This is **'+('true' if truth else 'false')+'**.'+((' '+explanations[label]) if explanations and label in explanations else '') for label,truth in bank)


def open_witness(P,Q):
    # Exact segment witness for the assertion that not all paths give zero work.
    t = sp.symbols('t', real=True)
    points = [(0,0),(1,0),(0,1),(1,1),(2,0),(0,2)]
    for A in points:
        for B in points:
            if A==B: continue
            x,y=A[0]+t*(B[0]-A[0]),A[1]+t*(B[1]-A[1])
            value = sp.integrate(P.subs({X:x,Y:y}, simultaneous=True)*(B[0]-A[0])+Q.subs({X:x,Y:y}, simultaneous=True)*(B[1]-A[1]),(t,0,1))
            if value.is_zero is False:
                return A,B,value
    raise ValueError('No nonzero open witness')


def ordinary(level, family, params, profile, rng):
    a,b,c=params
    if level=='easy':
        f=potential(family,a,b,c);P,Q=sp.diff(f,X),sp.diff(f,Y);cons=True
        prompt='Consider the scalar field '+math('f(x,y)='+tex(f))+r' and let $\mathbf F=\nabla f$ on $\mathbb R^2$.'
        solution=r'The field $\mathbf F=\nabla f$ is conservative by definition. '+theorem()
        # Avoid differentiating complicated supplied potentials in the learner solution.
        for A,B in [((0,0),(1,0)),((0,0),(0,1)),((0,1),(1,1))]:
            fa=f.subs({X:A[0],Y:A[1]});fb=f.subs({X:B[0],Y:B[1]});value=sp.simplify(fb-fa)
            if value.is_zero is False: break
    else:
        P,Q=components(family,a,b,c,profile[3]);cons,solution=criterion(P,Q)
        prompt='Consider the vector field'+display(r'\mathbf F(x,y)=\left('+tex(P)+r'\right)\mathbf i+\left('+tex(Q)+r'\right)\mathbf j')+r'on $\mathbb R^2$.'
        solution+=' '+theorem()
        A,B,value=open_witness(P,Q)
    solution+=' For example, the work along the segment from '+math(str(A))+' to '+math(str(B))+' is '+math(tex(value))+', which is nonzero. A path followed by its reverse always has zero total work, so a claim of nonzero work for every closed path is false.'
    bank=finalize_bank(general_bank(cons,profile[:3],level=='easy'),rng)
    prompt+=r' Which statements are true? Select all that apply. All paths mentioned are piecewise smooth and lie in $\mathbb R^2$.'
    solution+=explain(bank)
    return pack(level,prompt,solution,bank,{'family':family,'parameters':list(params),'profile':list(profile),'conservative':cons,'source_support':[17592186180721,17592186179605], 'operator_inputs':{'P':str(P),'Q':str(Q)}})


EDGES=[('A','B'),('B','C'),('A','C')]
LABELS=[r'\alpha',r'\beta',r'\gamma']


def cycle_tex(coeffs, labels):
    text=''
    for sign,label in zip(coeffs,labels):
        text+=('+' if sign>0 and text else '-' if sign<0 else '')+'W_{'+label+'}'
    return text


def diagram(signs,labels,output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    stem='paths-'+hashlib.sha256(json.dumps([signs,labels]).encode()).hexdigest()[:16]+'.png'
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    target=output/stem
    if not target.exists():
        xy={'A':(0,0),'B':(2,0),'C':(1,1.5)}
        fig,ax=plt.subplots(figsize=(5,3.3),dpi=140)
        offsets=[(0,-.17),(.17,.05),(-.18,.06)]
        for (u,v),sg,label,off in zip(EDGES,signs,labels,offsets):
            A,B=xy[u],xy[v]
            if sg<0:A,B=B,A
            ax.annotate('',xy=B,xytext=A,arrowprops={'arrowstyle':'-|>','lw':2,'color':'#235a80','shrinkA':8,'shrinkB':8,'mutation_scale':18})
            mid=((A[0]+B[0])/2+off[0],(A[1]+B[1])/2+off[1])
            ax.text(*mid,'$'+label+'$',ha='center',va='center',fontsize=16,bbox={'facecolor':'white','edgecolor':'none','pad':1})
        for name,(x,y) in xy.items():
            ax.plot(x,y,'o',color='#222222',ms=5)
            ax.text(x,y+(.15 if name=='C' else -.20),name,ha='center',fontsize=14)
        ax.set(xlim=(-.4,2.4),ylim=(-.4,1.9));ax.set_aspect('equal');ax.axis('off')
        fig.savefig(target,bbox_inches='tight',facecolor='white',metadata={'Software':VERSION});plt.close(fig)
    return stem


def hard(params,signs,labels,unknown,profile,rng,output):
    a,b,c,d=params
    P,Q=a+b*Y,b*X+2*c*Y+d
    cons,solution=criterion(P,Q)
    # Potential f=a*x+b*x*y+c*y^2+d*y at verification points A,B,C.
    fv=[0,a,a+b+c+d]
    base=[fv[1]-fv[0],fv[2]-fv[1],fv[2]-fv[0]]
    works=[sg*w for sg,w in zip(signs,base)]
    coeffs=[signs[0],signs[1],-signs[2]]
    routes=[]
    for (u,v),sg,label in zip(EDGES,signs,labels):
        if sg<0:u,v=v,u
        routes.append(math(label)+' goes from '+math(u)+' to '+math(v))
    image=diagram(signs,labels,output)
    alt='; '.join(label.replace('\\','')+' from '+(u if sg>0 else v)+' to '+(v if sg>0 else u) for (u,v),sg,label in zip(EDGES,signs,labels))
    prompt='Consider the vector field'+display(r'\mathbf F(x,y)=\left('+tex(P)+r'\right)\mathbf i+\left('+tex(Q)+r'\right)\mathbf j')+r'on $\mathbb R^2$. The diagram shows three piecewise-smooth directed paths: '+', '.join(routes)+'.\n\n!['+alt+']('+image+')\n\n'+r'For a directed path $\eta$, write $W_\eta=\int_\eta\mathbf F\cdot\mathrm d\mathbf r$. You are given '+ ' and '.join(math('W_{'+labels[i]+'}='+str(works[i])) for i in range(3) if i!=unknown)+'. Which statements are true? Select all that apply.'
    proposed_coeffs=list(coeffs)
    if not profile[0]:
        flip=(unknown+1)%3;proposed_coeffs[flip]*=-1
    proposed_value=works[unknown] if profile[1] else rng.choice([0,-works[unknown],sum(works[i] for i in range(3) if i!=unknown)])
    equation=cycle_tex(proposed_coeffs,labels)+'=0'
    bank=[(math(equation)+'.',sum(s*w for s,w in zip(proposed_coeffs,works))==0), (math('W_{'+labels[unknown]+'}='+str(proposed_value))+'.',proposed_value==works[unknown]), (r'$\oint_L\mathbf F\cdot\mathrm d\mathbf r'+('=0' if profile[2] else r'\ne0')+r'$ for '+('every' if profile[2] else 'some')+r' closed path $L$ in $\mathbb R^2$.',bool(profile[2])),(r'$\mathbf F$ is '+('conservative.' if profile[3] else '**not** conservative.'),bool(profile[3]))]
    bank=finalize_bank(bank,rng)
    known=[i for i in range(3) if i!=unknown]
    rhs=-sum(coeffs[i]*works[i] for i in known)
    solution+=' '+theorem()+r' Follow the route $A\to B\to C\to A$. Relative to the displayed arrows, its edge signs give'+display(r'\begin{aligned}'+cycle_tex(coeffs,labels)+r'&=0\\'+('' if coeffs[unknown]>0 else '-')+'W_{'+labels[unknown]+'}&='+str(rhs)+r'\\W_{'+labels[unknown]+'}&='+str(works[unknown])+r'.\end{aligned}')+'Reversing an edge changes its work sign. The proposed cycle sum evaluates to '+math(str(sum(s*w for s,w in zip(proposed_coeffs,works))))+'. Compare the proposed missing work with '+math(str(works[unknown]))+'.'+explain(bank)
    return pack('hard',prompt,solution,bank,{'family':'directed-cycle','parameters':list(params),'signs':list(signs),'labels':list(labels),'unknown':unknown,'profile':list(profile),'works':works,'source_support':[17592186708921,17592186180721,17592186049150],'operator_inputs':{'P':str(P),'Q':str(Q)}})


@nonempty_checkbox
def generate(difficulty='moderate',count=1,seed=0,output=None):
    if difficulty=='unclassified':difficulty='moderate'
    if difficulty not in ('easy','moderate','hard'):raise ValueError(difficulty)
    if count<0:raise ValueError('count must be nonnegative')
    output=output or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if difficulty=='hard' and not output:raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR for generated diagrams')
    rng=random.Random(seed);records=[];seen=set()
    families=list(EASY if difficulty=='easy' else MODERATE);rng.shuffle(families)
    if difficulty=='moderate':
        heads=['poly1','poly2'];rng.shuffle(heads)
        families=heads+[f for f in families if f not in heads]
    offset=rng.randrange(24)
    for i in range(count):
        # Decision schedule spans independent polarities and family assignments; no seed exceptions.
        role=(offset+i+7*(i//len(families)))%24
        profile=[bool(role&1), (role//2)%3, bool((role//6)%2), bool((role//12)%2)]
        family=families[i%len(families)]
        if difficulty=='moderate' and family in ('poly1','poly2'):
            profile[3]=bool((offset+(i//len(families))//2+families.index(family))%2)
        for attempt in range(100):
            params=[rng.choice([-3,-2,-1,1,2,3]) for _ in range(3)]
            if difficulty=='hard':
                signs=[rng.choice([-1,1]) for _ in range(3)];labels=LABELS.copy();rng.shuffle(labels)
                record=hard(params+[rng.choice([-2,-1,0,1,2])],signs,labels,(i+offset)%3,[bool(role&1),bool(role&2),bool(role&4),bool(role&8)],rng,output)
            else:
                record=ordinary(difficulty,family,params,profile,rng)
            # Semantic deduplication precedes field shuffling; two orders are not new instances.
            q=record['question'];fingerprint=json.dumps([q[':question/problem'],sorted((f[':answer-field/key'], next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])) for f in q[':question/answer-fields'])])
            if fingerprint not in seen:break
        else:raise RuntimeError('Cannot construct distinct batch')
        seen.add(fingerprint);record['generation'].update(seed=seed,index=i);records.append(record)
    return records


def replay_source():
    cases=json.loads(Path(__file__).with_name('source-cases.json').read_text())
    records=[]
    for case in cases:
        f=sp.sympify(case['potential'],locals={'x':X,'y':Y})
        P,Q=(sp.diff(f,X),sp.diff(f,Y)) if case['level']=='easy' else (sp.sympify(case['P'],locals={'x':X,'y':Y}),sp.sympify(case['Q'],locals={'x':X,'y':Y}))
        cons,solution=criterion(P,Q)
        if case['level']=='easy':solution=r'The supplied gradient is conservative by definition. '
        solution+=theorem()+r' This supplied field is nonzero, so some open paths have nonzero work. Every stated circle or ellipse is closed.'
        bank=[]
        for label,kind in case['bank']:
            truth={'conservative':cons,'not_conservative':not cons,'open_zero':False,'closed_zero':cons,'some_nonzero':not cons,'every_nonzero':False}.get(kind)
            if kind=='none':truth=not any(v for _,v in bank)
            bank.append((label,truth))
        # None may appear before other options in captured order.
        bank=[(k,not any(v for (k2,v),(_,kind) in zip(bank,case['bank']) if kind!='none')) if kind=='none' else (k,v) for (k,v),(_,kind) in zip(bank,case['bank'])]
        solution+=explain(bank)
        records.append(pack(case['level'],case['prompt'],solution,bank,{'source_replay':case['id'],'operator_inputs':{'P':str(P),'Q':str(Q)},'source_support':[case['id'],17592186180721]}))
    return records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['unclassified','easy','moderate','hard'],default='moderate');parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json'],default='json');parser.add_argument('--replay-source',action='store_true')
    args=parser.parse_args()
    records=replay_source() if args.replay_source else generate(args.difficulty,args.count,args.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
