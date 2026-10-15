"""Seeded, source-shaped parametric surface areas. See adjacent capabilities.json.

Only the domain-size slot varies. Surface coefficients, differential work, field
shape and source bank profile are fixed. Opaque distractors are transported as
complete banks by an explicitly authored common positive area-scale multiplier;
no psychological explanation is inferred. No new plots are required.
"""
import argparse, copy, hashlib, json, random, uuid
from pathlib import Path
import sympy as s
from functools import lru_cache
HERE=Path(__file__).with_suffix('')
KP_ID=17592186119888
KP_UUID='9361ad5a-b15c-507b-85d4-fe7ccb4d9fd8'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator:surface-area:domain-v1'))
VERSION='1.0.0'
SUPPORTED_LEVELS=('moderate','hard')
SOURCE=json.loads((HERE/'source.json').read_text())
CASES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
DEFAULTS={k:[1] for k in CASES}
LEVEL={k:q[':question/difficulty'][':db/ident'].split('/')[-1] for k,q in CASES.items()}
u,v=s.symbols('u v',nonnegative=True)
COORDS={
'q-105920':[2*u-v,3*u+2,u+2*v], 'q-109710':[u+v,2-3*u,1+u-v],
'q-109712':[u,v**2,s.Rational(2,3)*v**3], 'q-109761':[u**2,u*v,s.Rational(1,2)*v**2],
'q-105922':[-u+v,u-2*v,3*v], 'q-109779':[u,v,u-v],
'q-110252':[u,v,1-2*u+5*v], 'q-110551':[u-v,u+2*v,2*u-v]}
BASE_N={'q-105922':4,'q-109779':9,'q-110252':2,'q-110551':1}
BASE_CHOICES={
'q-105920':[2*s.sqrt(70),20,s.sqrt(30),10,s.sqrt(35)],
'q-109710':[5*s.sqrt(10),6*s.sqrt(2),4*s.sqrt(22),3*s.sqrt(14),8*s.sqrt(11)],
'q-109712':[s.Rational(14,3),s.Rational(5,3),s.Rational(7,2),s.Rational(19,6),s.Rational(9,2)],
'q-109761':[s.Rational(10,3),3,5,s.Rational(7,2),10],
'q-105922':[2*s.pi*s.sqrt(57),s.pi*s.sqrt(19),4*s.pi*s.sqrt(19),s.pi*s.sqrt(38),2*s.pi*s.sqrt(38)],
'q-109779':[2*s.sqrt(3),s.pi*s.sqrt(3),9*s.pi*s.sqrt(2),9*s.pi*s.sqrt(3),s.pi*s.sqrt(2)],
'q-110252':[s.pi*s.sqrt(20),2*s.pi*s.sqrt(10),3*s.pi*s.sqrt(5),s.pi*s.sqrt(15),2*s.pi*s.sqrt(30)],
'q-110551':[s.pi*s.sqrt(17),s.pi*s.sqrt(35),s.pi*s.sqrt(15),6*s.pi*s.sqrt(2),2*s.pi*s.sqrt(11)]}

def tex(x):return s.latex(s.sympify(x),mul_symbol=None)
def domain(template):return [[i] for i in range(1,7)]
@lru_cache(maxsize=None)
def math_data(template,t):
    r=s.Matrix(COORDS[template]);ru=r.diff(u);rv=r.diff(v);cross=ru.cross(rv);metric=s.simplify(s.sqrt(s.factor(cross.dot(cross))))
    if template in BASE_N:
        n=BASE_N[template]*t;bounds={'radius_squared':n};area=s.sqrt(s.factor(cross.dot(cross)))*s.pi*n;scale=s.Integer(t)
    else:
        if template=='q-105920':bounds={'u':[0,t],'v':[-1,1]};scale=s.Integer(t)
        elif template=='q-109710':bounds={'u':[0,2*t],'v':[-1,1]};scale=s.Integer(t)
        elif template=='q-109712':bounds={'u':[0,t],'v':[0,s.sqrt(3)]};scale=s.Integer(t)
        else:bounds={'u':[0,t],'v':[t,2*t]};scale=s.Integer(t)**4
        area=s.integrate(metric,(u,*bounds['u']),(v,*bounds['v']))
    return {'surface':r,'ru':ru,'rv':rv,'cross':cross,'metric':metric,'bounds':bounds,'area':s.simplify(area),'scale':scale}

def solution(template,t):
    """Retain all source prose, partial/cofactor/norm stages and integration order."""
    original=CASES[template][':question/worked-solution'];d=math_data(template,t)
    if t==1:return original  # Raw notation at the source anchor; same math stages below.
    head,final,tail=original.rsplit('$$',2)
    if template in BASE_N:
        n=d['bounds']['radius_squared'];old=BASE_N[template];rad=tex(s.sqrt(n))
        head=head.replace(r'{u}^{2}+{v}^{2}\le '+str(old),r'{u}^{2}+{v}^{2}\le '+str(n))
        oldrad=tex(s.sqrt(old));head=head.replace('of radius $'+oldrad+'.$','of radius $'+rad+'.$')
        # Source uses \sqrt{2}, not SymPy's spacing: the tokens coincide here.
        metric=tex(d['metric'])
        rows=[r'{∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A',r'{∬}_{D}'+metric+r'\,\text{d}A',metric+r'{∬}_{D}\text{d}A',metric+r'\cdot \text{Area}(D)',metric+r'\cdot (\pi \cdot ('+rad+r')^{2})',tex(d['area'])]
    elif template in ('q-105920','q-109710'):
        old=1 if template=='q-105920' else 2;hi=old*t
        head=head.replace(r'0\le u\le '+str(old),r'0\le u\le '+str(hi))
        metric=tex(d['metric'])
        rows=[r'{∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A',r'{∬}_{D}'+metric+r'\,\text{d}A',metric+r'{∬}_{D}\text{\u00a0}\,\text{d}A'.replace(r'\u00a0','\u00a0'),metric+r'\cdot \text{Area}(D)',metric+r'\cdot '+str(hi)+r'\cdot 2',tex(d['area'])]
    elif template=='q-109712':
        head=head.replace(r'0\le u\le 1',r'0\le u\le '+str(t))
        head=head.replace(r'{\int }_{0}^{1}',r'{\int }_{0}^{'+str(t)+'}')
        # Final evaluation of the u integral supplies the width to the remaining integral.
        oldlast=r' & ={\int }_{0}^{\sqrt{3}}2v\sqrt{{v}^{2}+1}\,\text{d}v\end{aligned}'
        newlast=r' & ='+str(t)+r'{\int }_{0}^{\sqrt{3}}2v\sqrt{{v}^{2}+1}\,\text{d}v\end{aligned}'
        assert oldlast in head;head=head.replace(oldlast,newlast)
        c=str(t)
        rows=[c+r'{\int }_{0}^{\sqrt{3}}2v\sqrt{{v}^{2}+1}\,\text{d}v',c+r'{\int }_{1}^{4}\sqrt{w}\,\text{d}w',c+r'{[\frac{2}{3}\sqrt{{w}^{3}}]}_{1}^{4}',c+r'\cdot \frac{2}{3}[\sqrt{{4}^{3}}-\sqrt{{1}^{3}}]',c+r'\cdot \frac{2}{3}(8-1)',tex(d['area'])]
    else:
        head=head.replace(r'0\le u\le 1',r'0\le u\le '+str(t)).replace(r'1\le v\le 2',str(t)+r'\le v\le '+str(2*t))
        a,b=str(t),str(2*t);c=tex(s.Rational(2,3)*t**3)
        rows=[r'{∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A',r'{∬}_{D}({v}^{2}+2{u}^{2})\,\text{d}A',r'{\int }_{'+a+'}^{'+b+r'}{\int }_{0}^{'+a+r'}({v}^{2}+2{u}^{2})\,\text{d}u\,\text{d}v',r'{\int }_{'+a+'}^{'+b+r'}{[u{v}^{2}+\frac{2}{3}{u}^{3}]}_{0}^{'+a+r'}\text{d}v',r'{\int }_{'+a+'}^{'+b+'}('+a+r'{v}^{2}+'+c+r')\text{d}v',r'{[\frac{'+a+r'}{3}{v}^{3}+'+c+r'v]}_{'+a+'}^{'+b+'}',r'\frac{'+a+r'}{3}[{'+b+r'}^{3}-{'+a+r'}^{3}]+('+c+')('+b+'-'+a+')',tex(3*s.Integer(t)**4),tex(d['area'])]
    return head+'$$\n'+r'\begin{aligned}{∬}_{S}\,\text{d}S & ='+r' \\  & ='.join(rows)+r'.\end{aligned}'+'\n$$'+tail

def prompt(template,t):
    text=CASES[template][':question/problem']
    if template in BASE_N:return text.replace(r'{u}^{2}+{v}^{2}\le '+str(BASE_N[template]),r'{u}^{2}+{v}^{2}\le '+str(BASE_N[template]*t))
    if template=='q-109761':return text.replace(r'0\le u\le 1',r'0\le u\le '+str(t)).replace(r'1\le v\le 2',str(t)+r'\le v\le '+str(2*t))
    old=2 if template=='q-109710' else 1
    return text.replace(r'0\le u\le '+str(old),r'0\le u\le '+str(old*t))

def fingerprint(q):
    # Prompt alone contains surface, domain and response demand. Ignore seed,
    # difficulty, solution spelling, field/answer UUIDs and choice ordering.
    return hashlib.sha256(' '.join(q[':question/problem'].split()).encode()).hexdigest()

def generate(difficulty,seed=0,template=None,parameters=None,profile=None):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed);eligible=[k for k in CASES if LEVEL[k]==difficulty]
    template=template or rng.choice(eligible)
    if template not in eligible:raise ValueError('Template/level mismatch')
    if profile not in (None,template):raise ValueError('Bank profile must remain complete')
    parameters=parameters or rng.choice(domain(template));t=parameters[0]
    if parameters not in domain(template):raise ValueError('Domain scale outside validated finite bounds')
    d=math_data(template,t);old=CASES[template];of=old[':question/answer-fields'][0]
    q={':question/problem':prompt(template,t),':question/worked-solution':solution(template,t),':question/difficulty':':question.difficulty/'+difficulty}
    # Identity ignores seed and order. Surface+domain determine the task; bank
    # profile/version determine authored representation within that task.
    identity=json.dumps([KP_UUID,VERSION,template,parameters],separators=(',',':'))
    qid=uuid.uuid5(uuid.UUID(GENERATOR_UUID),identity);fid=uuid.uuid5(qid,'field:selection')
    bank=[];correct=None
    for a,val in zip(of[':answer-field/choices'],BASE_CHOICES[template]):
        value=a[':answer/value'] if t==1 else tex(s.simplify(val*d['scale']))
        aid=str(uuid.uuid5(fid,'answer:'+s.srepr(s.simplify(val*d['scale']))))
        bank.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
        if a[':answer/id']==of[':answer-field/correct'][':answer/id']:correct=aid
    q[':question/id']=str(qid);q[':question/answer-fields']=[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/correct':[':answer/id',correct],':answer-field/choices':bank}]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Finding the Surface Area of a Parametric Surface'},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':template,'profile':template,'parameters':parameters,'parameter_role':'rectangle width, homogeneous rectangle scale, or disk squared-radius multiplier','domain':{k:([str(z) for z in val] if isinstance(val,list) else str(val)) for k,val in d['bounds'].items()},'source_question':old[':question/id'],'source_basis':2622,'source_lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','bank_policy':'exact source bank at t=1; explicitly authored complete-bank positive area-scale transport at t>1','bank_scale':str(d['scale']),'sympy':s.__version__,'mathematical_fingerprint':fingerprint(q)}}

def batch(difficulty,count,seed):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    slots=[(k,p) for k in CASES if LEVEL[k]==difficulty for p in domain(k)];random.Random(seed).shuffle(slots)
    if count>len(slots):raise ValueError(f'Finite limit: {len(slots)} distinct candidates for {difficulty}')
    return [generate(difficulty,seed,k,p) for k,p in slots[:count]]
def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join(('- [x] ' if a[':answer/id']==f[':answer-field/correct'][1] else '- [ ] ')+'$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=('json','markdown'),default='json');args=a.parse_args();out=batch(args.difficulty,args.count,args.seed)
    print(json.dumps(out,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
