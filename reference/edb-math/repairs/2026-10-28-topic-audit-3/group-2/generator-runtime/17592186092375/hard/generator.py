"""Seeded parametric arc-length integral practice. No evaluation is assessed."""
import argparse, hashlib, json, math, os, random, uuid
from pathlib import Path
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

T=s.Symbol('t', real=True)
KP_ID=17592186092375
KP_UUID='4b03546f-6c79-53b9-b284-fb23ae4dba52'
TITLE='Finding an Integral Expression For the Arc Length of a Parametric Curve'
NAMESPACE=uuid.uuid5(uuid.UUID(KP_UUID),'arc-integral-generator-v2')
VERSION='2.0.1'

def tex(e):return s.latex(e, order='lex')
def display(z):return '$$\n'+z+'\n$$'
def integral(f,a,b):return r'\int_{'+str(a)+'}^{'+str(b)+'}'+f+r'\,\mathrm{d}t'
def root(p,expand=True):return r'\sqrt{'+tex(s.expand(p) if expand else p)+'}'
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True).encode()).hexdigest()
def factor_tex(u,kind):
    if kind=='absolute':return r'\left|'+tex(u)+r'\right|'
    if kind=='squared':return r'\left('+tex(u)+r'\right)^2'
    return r'\left('+tex(u if kind=='positive' else -u)+r'\right)'

def sample_parameters(band,rng,family,profile):
    A=rng.choice([1,2,3]);B=rng.choice([1,2,3,4])
    p={'family':family,'A':A,'B':B,'c':rng.randint(-3,3),'d':rng.randint(-3,3),'profile':profile}
    if family=='paired':
        h=0 if band=='easy' else rng.choice([-2,-1,0,1,2]);p['h']=h
        region='positive' if band=='easy' else ('crossing' if band=='hard' else rng.choice(['positive','negative']))
        l,r=rng.choice([1,2]),rng.choice([1,2,3]);p['region']=region
        if region=='positive':p.update(a=h+rng.choice([0,1]),b=h+3)
        elif region=='negative':p.update(a=h-3,b=h-rng.choice([0,1]))
        else:p.update(a=h-l,b=h+r)
        p['wrong_sign']=rng.choice(['positive','negative'])
    else:
        p['n']=rng.choice([2,3]) if family=='monomial' else rng.choice([2,3])
        p['m']=1 if family=='monomial' else (4 if p['n']==3 and rng.randrange(3)==0 else 2 if p['n']==3 else 3)
        p['C']=0 if family=='monomial' else rng.choice([-3,-2,-1,1,2,3])
        p['A']*=rng.choice([-1,1]);p['B']*=rng.choice([-1,1])
        p['a']=rng.choice([-2,-1,0]);p['b']=rng.choice([1,2,3])
    return p


def derivation(band,p):
    A,B,c,d,a,b=[p[k] for k in ('A','B','c','d','a','b')]
    profile=p['profile'];pairs=[]
    if p['family']=='paired':
        u=T-p['h'];x=A*u**3+B*u**2+c;y=A*u**3-B*u**2+d
        dx=3*A*u**2+2*B*u;dy=3*A*u**2-2*B*u
        R=18*A*A*u**2+8*B*B
        region=p['region'];kind={'positive':'positive','negative':'negative','crossing':'absolute'}[region]
        wrong=p['wrong_sign'] if region=='crossing' else ('negative' if kind=='positive' else 'positive')
        # Complete paired banks: two coefficient families each expose a sign decision.
        errors=[(A,B),(4*A,3*B),(2*A,B),(6*A,4*B)]
        slots=[(0,1),(1,2),(3,1)][profile]
        D,E=errors[slots[0]];F,G=errors[slots[1]]
        R1=2*D*D*u**2+2*E*E;R2=2*F*F*u**2+2*G*G
        def add(rad,k,label):
            pre=factor_tex(u,k);f=s.Abs(u) if k=='absolute' else (u**2 if k=='squared' else (u if k=='positive' else -u))
            pairs.append((pre+root(rad,expand=False),f*s.sqrt(rad),label))
        # On symmetric crossing intervals all signed odd errors integrate to zero.
        # Give both coefficient families the same squared-factor alternative;
        # keeping only one signed error exposes its correct absolute counterpart.
        factor_error='squared' if region=='crossing' and a+b==2*p['h'] else wrong
        add(R,kind,'correct');add(R,factor_error,'invalid square-root extraction')
        add(R1,kind,'power-rule coefficients')
        second_error=factor_error
        add(R1,second_error,'power-rule coefficients and square-root extraction')
        add(R2,kind if profile!=1 or second_error=='squared' else wrong,'different power-rule coefficients')
        ss=18*A*A*u**4+8*B*B*u**2
        steps=[r"x'(t)="+tex(dx),r"y'(t)="+tex(dy),r"[x'(t)]^2+[y'(t)]^2="+tex(ss),r'=('+tex(u)+r')^2\bigl('+tex(R)+r'\bigr)']
        algebra=display(r'\begin{aligned}'+'\n'+r"x'(t)^2+y'(t)^2&="+tex(ss)+r'\\'+'\n'+r'&=('+tex(u)+r')^2\bigl('+tex(R)+r'\bigr).'+ '\n'+r'\end{aligned}')
        sign_text='The factor $'+tex(u)+'$ is nonnegative on this interval.' if region=='positive' else ('The factor $'+tex(u)+'$ is nonpositive on this interval.' if region=='negative' else 'The factor $'+tex(u)+'$ changes sign inside this interval, so its absolute value must remain.')
        conversion='Use $\\sqrt{('+tex(u)+')^2}=|'+tex(u)+'|$. '+sign_text
        if region!='crossing':conversion+=' Hence $|'+tex(u)+'|='+tex(u if region=='positive' else -u)+'$ here.'
        explanation='The cross terms cancel when the two derivative squares are added.\n\n'+algebra+'\n\n'+conversion
        sources=['dddf8a10-d360-5144-aae4-5bd6e2bd6915']
    else:
        n,m,C=[p[k] for k in ('n','m','C')]
        x=A*T**n+c;y=B*T**m+C*T+d
        dx=n*A*T**(n-1);dy=m*B*T**(m-1)+C
        correct=s.expand(dx*dx+dy*dy)
        # Multiplying by the degree incorrectly affects both coordinate derivatives.
        factors={'omit-degree':(1,1),'one-too-few':(n-1,m-1),'one-too-many':(n+1,m+1),'degree-squared':(n*n,m*m),'twice-degree':(2*n,2*m),'divide-degree':(s.Rational(1,n),s.Rational(1,m))}
        profiles=[['omit-degree','one-too-few','one-too-many','degree-squared'],['omit-degree','one-too-many','degree-squared','twice-degree'],['omit-degree','one-too-few','divide-degree','one-too-many']]
        pairs=[(root(correct),s.sqrt(correct),'correct')]
        for name in profiles[profile]:
            f,g=factors[name];ex=f*A*T**(n-1);ey=g*B*T**(m-1)+C;rad=s.expand(ex*ex+ey*ey)
            pairs.append((root(rad),s.sqrt(rad),name))
        ss=correct;steps=[r"x'(t)="+tex(dx),r"y'(t)="+tex(dy),r"[x'(t)]^2+[y'(t)]^2="+tex(ss)]
        explanation='Square both derivatives and add:\n\n'+display(r'\begin{aligned}'+'\n'+r"x'(t)^2+y'(t)^2&=\bigl("+tex(dx)+r'\bigr)^2+\bigl('+tex(dy)+r'\bigr)^2\\'+'\n'+r'&='+tex(ss)+r'.'+'\n'+r'\end{aligned}')
        sources=['a6c68291-2bb7-56b1-a306-1312ff237a63','0f078660-763f-536d-9faf-52311fdcfddf','ce632c36-0a89-59ca-a425-8c378bad7972'] if p['family']=='monomial' else ['1ac06717-3d6e-5cb8-bb53-88e2680a811e','a0cda492-f891-5b24-90a6-900da47a3f8d','77ecc403-c204-532a-a0f9-e871a850287a']
    if len({z[0] for z in pairs})!=5:raise ValueError('Bank notation collision')
    # Reject coincident integrals as well as duplicate integrands. Deterministic
    # composite midpoint quadrature is only a construction guard, not the proof.
    values=[]
    for _,expr,_ in pairs:
        f=s.lambdify(T,expr,'math');v=sum(f(a+(b-a)*(i+.5)/192) for i in range(192))*(b-a)/192
        if not math.isfinite(v):raise ValueError('Nonfinite choice')
        if any(abs(v-z)<1e-7*max(1,abs(v),abs(z)) for z in values):raise ValueError('Bank value collision')
        values.append(v)
    return x,y,dx,dy,ss,pairs,steps,explanation,sources


def plot_curve(p,x,y,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    a,b=p['a'],p['b'];fx=s.lambdify(T,x,'math');fy=s.lambdify(T,y,'math')
    ts=[a+(b-a)*j/600 for j in range(601)]
    fig,ax=plt.subplots(figsize=(5.2,3.4),layout='constrained')
    ax.plot([fx(v) for v in ts],[fy(v) for v in ts],color='#1769aa',lw=2)
    marks=[(a,(8,8)),(b,(-38,-16))]
    if p['family']=='paired' and a<p['h']<b:marks.append((p['h'],(8,-17)))
    for v,offset in marks:
        ax.plot(fx(v),fy(v),'o',ms=4,color='#1769aa');ax.annotate(f'$t={v}$',(fx(v),fy(v)),xytext=offset,textcoords='offset points',fontsize=10)
    for f in [.25,.7]:
        v=a+f*(b-a);d=(b-a)*.02
        ax.annotate('',xy=(fx(v+d),fy(v+d)),xytext=(fx(v),fy(v)),arrowprops={'arrowstyle':'->','color':'#1769aa','lw':1.8})
    ax.axhline(0,color='#777',lw=.7);ax.axvline(0,color='#777',lw=.7);ax.set_xlabel('$x$');ax.set_ylabel('$y$',rotation=0)
    ax.spines[['top','right']].set_visible(False);ax.margins(.25)
    name='curve-'+digest(p)[:24]+'.png';out.mkdir(parents=True,exist_ok=True);fig.savefig(out/name,dpi=120);plt.close(fig)
    return name


def make_record(band,p,seed=0,assets=True):
    x,y,dx,dy,ss,pairs,steps,explanation,sources=derivation(band,p)
    a,b=p['a'],p['b']
    correct=integral(pairs[0][0],a,b)
    problem='Which of the following gives the length of the curve defined by\n\n'+display(r'\begin{aligned}'+'\n'+'x&='+tex(x)+r'\\'+'\n'+'y&='+tex(y)+'\n'+r'\end{aligned}')+ '\n\nfrom $t='+str(a)+'$ to $t='+str(b)+'$?\n\nChoose an integral expression valid on the entire interval. Do not evaluate it.'
    if assets:
        output=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
        if not output:raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR for generated diagrams')
        name=plot_curve(p,x,y,Path(output));problem+='\n\n![]('+name+')'
    formula=display(r'L=\int_a^b\sqrt{[x\prime(t)]^2+[y\prime(t)]^2}\,\mathrm{d}t.')
    solution='For parametric arc length, use\n\n'+formula+'\n\nDifferentiate each coordinate:\n\n'+display(r'\begin{aligned}'+'\n'+r"x'(t)&="+tex(dx)+r'\\'+'\n'+r"y'(t)&="+tex(dy)+r'.'+'\n'+r'\end{aligned}')+'\n\n'+explanation+'\n\nUse the given parameter bounds:\n\n'+display('L='+correct+'.')
    problem,solution=normalize_prose(problem),normalize_prose(solution)
    values=[normalize_tex(integral(z[0],a,b)) for z in pairs];correct=values[0]
    # Identity is based on normalized public content, before presentation order.
    identity=digest([band,problem,solution,sorted(values),correct]);qid=str(uuid.uuid5(NAMESPACE,identity));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct_id=answers[0][':answer/id'];random.Random(str(seed)+identity).shuffle(answers)
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+band,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]}
    r={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_version':VERSION,'seed':seed,'template':p['family'],'parameters':p,'source_question_ids':sources,'bank_profile':'authored-'+str(p['profile']),'normalization':'course-academy-tex-v1'}}
    validate_generated_record(r)
    return r


def batch(difficulty,count,seed):
    if difficulty not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if count<0:raise ValueError('Negative count')
    rng=random.Random(seed);result=[];seen=set();core_seen=set();attempts=0
    families=['monomial','binomial','paired'] if difficulty=='easy' else ['paired']
    family_order=families[:];rng.shuffle(family_order);profiles=[0,1,2];rng.shuffle(profiles)
    while len(result)<count:
        attempts+=1
        if attempts>max(1000,count*250):raise ValueError('Requested batch exceeds distinct supported instances')
        i=len(result);family=family_order[i%len(family_order)];profile=profiles[(i//len(family_order)+i%len(family_order))%3]
        p=sample_parameters(difficulty,rng,family,profile)
        core=(family,p['A'],p['B']) if family=='paired' else (family,p['A'],p['B'],p['n'],p['m'],p['C'])
        # Spread main calculations through a short batch, before reusing an
        # amplitude pair with a different interval-dependent sign calculation.
        if core in core_seen and (family!='paired' or sum(c[0]=='paired' for c in core_seen)<12):continue
        try:r=make_record(difficulty,p,seed,assets=False)
        except (ValueError,TypeError,ZeroDivisionError):continue
        qid=r['question'][':question/id']
        if qid in seen:continue
        seen.add(qid);core_seen.add(core)
        result.append(make_record(difficulty,p,seed,assets=True))
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='easy');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');args=ap.parse_args()
    print(json.dumps(batch(args.difficulty,args.count,args.seed),indent=2))
