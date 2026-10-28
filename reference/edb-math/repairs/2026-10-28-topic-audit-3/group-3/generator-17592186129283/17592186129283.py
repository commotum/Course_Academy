#!/usr/bin/env python3
"""Orientation sign regions, steps 3–7 only; read-only math basis 1356.

Observed profiles preserve full source prose/banks at h=k=0. Templates use
translation of COMPLETE mathematical components: T_hk(u,v)=T(u-h,v-k).
The same substitution applies to derivatives, distributed determinant products,
inequalities, test points and plot geometry. No source answer lookup or literal
payload return occurs. Explicit observed plot profiles describe geometry, not an
unsupported claim about author intent. Authored defaults use whole operation
banks (reverse sign, negate boundary, double boundary and reverse its sign).
Easy/hard are authored missing-level design claims, documented in classification.
Matplotlib rendering uses the read-only cached Python3.10 fallback in render.py.
"""
from __future__ import annotations
import os
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
import argparse, hashlib, json, random, re, subprocess, uuid, tempfile, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().with_suffix('')

from math_format import normalize_prose, validate_generated_record
KP_ID=17592186129283
KP_UUID='091b8235-56d8-5a08-bc95-08c99772cfd8'
TITLE='Finding Regions Where a Transformation is Orientation-Preserving or Reversing'
VERSION='orientation-region-2-audit9837'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
u,v=sp.symbols('u v',real=True)
RAW=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in RAW['record'][':knowledge-point/questions']}
# Exact formulas independently transcribed from displayed source transformations.
FORMULAS={
'q-160341':(u**2-2*v**2,u-v), 'q-160601':(u**2-v,4*u-v**2),
'q-161838':(u+v,u**2+v**2), 'q-161842':(u**3-v**2/2,u-v/3),
'q-161843':(4*u+v**2,v-u**2), 'q-161855':(sp.exp(u*v),u**2+v),
'q-161835':(u*v,u+v), 'q-161837':(u**3/3+v,u*v),
'q-161839':(u**2-v,u*v+1), 'q-161840':(u**2+v**2,v-u),
'q-161841':(sp.exp(u+v),-u*v), 'q-161856':(u**2+2*v,-2*u-v**2)}
ASSETS=json.loads((HERE/'asset-index.json').read_text())
# degree, coefficient, shading. For degree -1, product comparisons preserve both
# branches; global above/below are observed wrong sign-division plots.
GEO_BY_INDEX={0:(-1,1,'below'),1:(1,'1/2','below'),2:(1,1,'below'),3:(2,2,'above'),4:(2,1,'below'),5:(1,1,'above'),6:(1,'1/2','above'),7:(2,-1,'above'),8:(2,1,'above'),9:(1,1,'above'),11:(-1,1,'above'),12:(2,2,'above'),13:(1,-1,'above'),14:(-1,'-1/2','above'),15:(1,1,'below'),16:(2,-2,'above'),17:(1,1,'above'),18:(2,-1,'below'),19:(-1,-1,'above'),20:(1,2,'below'),21:(-1,'1/3','product_lt'),22:(1,-1,'below'),23:(-1,-1,'product_gt'),24:(3,1,'above'),25:(-1,1,'product_gt'),26:(1,'1/3','below'),28:(-1,-1,'above'),29:(1,-1,'above'),30:(-1,1,'product_lt')}
GEOMETRY={ASSETS[i]:{'degree':n,'coefficient':str(c),'mode':m,'h':0,'k':0} for i,(n,c,m) in GEO_BY_INDEX.items()}
LEVELS={'easy':['axis_power','axis_power_horizontal'],'moderate':list(FORMULAS),'hard':['translated_hyperbola']}


def tex(e):return sp.latex(e)
def canonical(obj):return json.dumps(asset_payload(obj),sort_keys=True,separators=(',',':'))
def fingerprint(obj):return hashlib.sha256(canonical(obj).encode()).hexdigest()
def uid(text):return str(uuid.uuid5(uuid.UUID(KP_UUID),str(asset_payload(text))))
def translate_tex(s,h,k):
    """Only numeric mathematical components; no prose, labels or differential names."""
    slots={'u':tex(u-h),'v':tex(v-k)}
    # Protect whole TeX command names, then replace coordinate tokens, including uv.
    def f(m):
        t=m.group()
        if t.startswith('\\'):return t
        return ''.join(('('+slots[c]+')' if len(slots[c])>1 else slots[c]) if c in slots else c for c in t)
    return re.sub(r'\\[A-Za-z]+|[uv]+',f,s)

def source_text(q,h,k):
    """Parameterized source skeleton; replaces complete display/inline components."""
    def render_block(m):
        text=m.group(1)
        if text.startswith('T:'):
            # Input basis stays u,v. Only output component slots vary.
            pivot=text.index('⟶');return '$$\n'+text[:pivot]+translate_tex(text[pivot:],h,k)+'\n$$'
        if r'\frac{∂(x,y)}{∂(u,v)}' in text:
            marker=r'\\  & =|'
            if marker in text:
                pivot=text.index(marker)+len(marker);return '$$\n'+text[:pivot]+translate_tex(text[pivot:],h,k)+'\n$$'
            return m.group()
        return '$$\n'+translate_tex(text,h,k)+'\n$$'
    def render(text):
        text=re.sub(r'\$\$\n(.*?)\n\$\$',render_block,text,flags=re.S)
        # Inline inequalities and actual coordinate tuples, never $uv$ plane labels.
        def inline(m):
            s=m.group(1)
            point=re.fullmatch(r'\((-?\d+),(-?\d+)\)',s)
            if point:return '$('+str(int(point[1])+h)+','+str(int(point[2])+k)+')$'
            if '<' in s or '>' in s:return '$'+translate_tex(s,h,k)+'$'
            return m.group()
        return re.sub(r'(?<!\$)\$(?!\$)([^\n$]+)\$(?!\$)',inline,text)
    return render(q[':question/problem']),render(q[':question/worked-solution'])


def plot_spec(degree,coefficient,mode,h=0,k=0):return {'degree':degree,'coefficient':str(coefficient),'mode':mode,'h':h,'k':k}
def render_plots(specs, source_assets=None):
    """Matplotlib assets share exact instance geometry; no independent sampling."""
    radius=max(3,max(2*abs(float(sp.Rational(s['coefficient'])))**(1/(abs(s['degree'])+1)) for s in specs))
    bounds=[min(0,min(float(sp.Rational(s['h'])) for s in specs))-radius,max(0,max(float(sp.Rational(s['h'])) for s in specs))+radius,min(0,min(float(sp.Rational(s['k'])) for s in specs))-radius,max(0,max(float(sp.Rational(s['k'])) for s in specs))+radius]
    paths=[];pending=[]
    for i,spec in enumerate(specs):
        asset=(source_assets or [None]*len(specs))[i]
        # Reuse an unchanged source asset when exact source geometry is requested.
        if asset and GEOMETRY[asset]==spec:
            paths.append('/media/jake/SSD/EDB/math/'+asset);continue
        name='plot-'+fingerprint({'geometry':spec,'bounds':bounds})[:20]+'.png';path=Path(os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',str(HERE/'plots')))/name
        paths.append(str(path))
        if not path.exists():pending.append({'spec':spec,'path':str(path),'bounds':bounds})
    if pending:
        Path(os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',str(HERE/'plots'))).mkdir(parents=True,exist_ok=True)
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='render-call-',dir=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'),delete=False) as handle:
            json.dump(pending,handle);inp=Path(handle.name)
        try:subprocess.run([sys.executable,str(HERE/'render.py'),str(inp)],check=True,stdout=subprocess.DEVNULL)
        finally:inp.unlink(missing_ok=True)
    return paths

def eligible_bank(correct):
    n,c,m=correct['degree'],sp.Rational(correct['coefficient']),correct['mode']
    flip={'above':'below','below':'above','product_gt':'product_lt','product_lt':'product_gt','left':'right','right':'left','top':'bottom','bottom':'top'}
    # Complete authored bank: determinant sign reversal; sign error in boundary;
    # omitted factor 2 (implemented double boundary); factor+sign combined error.
    if n==0:
        key='k' if m in ('top','bottom') else 'h';h=correct[key];return [correct,{**correct,'mode':flip[m]},{**correct,key:-h},{**correct,key:2*h},{**correct,key:str(sp.Rational(h,2))}]
    return [correct,{**correct,'mode':flip[m]},{**correct,'coefficient':str(-c)},{**correct,'coefficient':str(2*c)},{**correct,'coefficient':str(2*c),'mode':flip[m]}]


def authored(level,p,template):
    h,k,a,b,orientation=p['h'],p['k'],p['a'],p['b'],p['orientation'];U=u-h;V=v-k
    op='>' if orientation=='preserving' else '<'
    if level=='easy':
        horizontal=template=='axis_power_horizontal'
        x=a*U if horizontal else a*U**2;y=b*V**2 if horizontal else b*V
        mode=('top' if orientation=='preserving' else 'bottom') if horizontal else ('right' if orientation=='preserving' else 'left')
        correct=plot_spec(0,1,mode,h,k)
        symbol,offset=(v,k) if horizontal else (u,h)
        region=tex(symbol)+' '+op+' '+str(offset);boundary=tex(sp.Eq(symbol,offset));kind='a horizontal line' if horizontal else 'a vertical line'
        extra=''
    else:
        x=U**2+a*V;y=-b*U-V**2;c=sp.Rational(a*b,4)
        correct=plot_spec(-1,c,'product_lt' if orientation=='preserving' else 'product_gt',h,k)
        relation='<' if orientation=='preserving' else '>'
        region=tex(U*V)+' '+relation+' '+tex(c);boundary=tex(sp.Eq(v,k+c/U));kind='a hyperbola'
        rel2='>' if relation=='<' else '<'
        extra=f'This gives the solution $v {relation} {tex(k+c/U)}$ for $u>{h}$ and $v {rel2} {tex(k+c/U)}$ for $u<{h}.$ At $u={h},$ the Jacobian is positive, so this line '+('belongs to' if orientation=='preserving' else 'is excluded from')+' the required region.\n\n'
    xu,xv,yu,yv=[sp.diff(z,w) for z,w in [(x,u),(x,v),(y,u),(y,v)]]
    J=sp.expand(xu*yv-xv*yu)
    T=r'T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}'+tex(x)+r' \\ '+tex(y)+r'\end{aligned}]'
    problem='Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by\n\n$$\n'+T+',\n$$\n\nis (locally) orientation-'+orientation+'?'
    solution=f'Recall that a transformation is (locally) orientation-{orientation} at the points where the Jacobian determinant is '+('positive' if op=='>' else 'negative')+':\n\n$$\n'+r'\frac{∂(x,y)}{∂(u,v)}'+op+'0\n$$\n\nWe have\n\n$$\n'+T+'.\n$$\n\nComputing the corresponding Jacobian determinant, we obtain\n\n$$\n'+r'\begin{aligned}\frac{∂(x,y)}{∂(u,v)} &=\begin{vmatrix}'+tex(xu)+' & '+tex(xv)+r' \\ '+tex(yu)+' & '+tex(yv)+r'\end{vmatrix} \\ &=('+tex(xu)+r')\cdot ('+tex(yv)+')-('+tex(xv)+r')\cdot ('+tex(yu)+r') \\ &='+tex(J)+r'.\end{aligned}'+'\n$$\n\nTo find the required regions, we solve the following inequality:\n\n$$\n'+r'\begin{aligned}'+tex(J)+' &'+op+r'0 \\ '+region+r'\end{aligned}'+'\n$$\n\n'+extra+'Notice that the equation\n\n$$\n'+boundary+'\n$$\n\ndefines '+kind+'.\n\nTherefore, the region where the transformation is (locally) orientation-'+orientation+' must be the following:\n\n{{plot}}'
    return problem,solution,correct,x,y


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed image radio layout supported')
    rng=random.Random(seed);template=template or rng.choice(LEVELS[level])
    if template not in LEVELS[level]:raise ValueError('Template outside level')
    observed=template in QUESTIONS
    if profile is None:profile='authored_operations'
    if profile not in ('authored_operations','observed','observed_legacy'):raise ValueError('Unknown complete bank')
    if not observed and profile!='authored_operations':raise ValueError('Authored template has no observed profile')
    p=dict(parameters) if parameters is not None else ({'h':rng.randint(-2,2),'k':rng.randint(-2,2)} if observed else {'h':rng.choice([-3,-2,-1,1,2,3]),'k':rng.choice([-3,-2,-1,1,2,3]),'a':rng.choice([1,2,3,4]),'b':rng.choice([1,2,3,4]),'orientation':rng.choice(['preserving','reversing'])})
    if parameters is None and level=='hard':
        p['a'],p['b']=rng.choice([(1,2),(2,1),(1,3),(3,1),(2,3),(3,2),(3,3)])
    required={'h','k'} if observed else {'h','k','a','b','orientation'}
    if set(p)!=required:raise ValueError('Exact required parameter set is '+str(sorted(required)))
    if any(type(p[z]) is not int or not -6<=p[z]<=6 for z in ('h','k')):raise ValueError('Bounded integer translation required')
    if not observed and (p['a'] not in (1,2,3,4) or p['b'] not in (1,2,3,4) or p['orientation'] not in ('preserving','reversing')):raise ValueError('Invalid authored parameters')
    if level=='hard' and (not p['h'] or not p['k'] or p['a']*p['b']<=1 or p['a']*p['b']%4==0):raise ValueError('Hard requires two nonzero shifts and a noninteger nonunit threshold')
    source_assets=None
    if observed:
        q=QUESTIONS[template];problem,solution=source_text(q,p['h'],p['k'])
        f=q[':question/answer-fields'][-1]
        if profile=='observed_legacy':
            if template!='q-160601':raise ValueError('Legacy profile only for q-160601')
            f=q[':question/answer-fields'][0]
        correct_asset=q[':question/answer-fields'][-1][':answer-field/correct'][':answer/value']
        correct={**GEOMETRY[correct_asset],**p}
        x,y=[z.subs({u:u-p['h'],v:v-p['k']},simultaneous=True) for z in FORMULAS[template]]
        if profile.startswith('observed'):
            source_assets=[a[':answer/value'] for a in f[':answer-field/choices']]
            specs=[{**GEOMETRY[a],**p} for a in source_assets]
            ci=source_assets.index(correct_asset)
        else:specs=eligible_bank(correct);ci=0
    else:
        problem,solution,correct,x,y=authored(level,p,template);specs=eligible_bank(correct);ci=0
    # Reject the whole bank, never replace an invalid member from a pooled list.
    if len(specs)!=5 or len({canonical(s) for s in specs})!=5:raise ValueError('Whole bank rejected: duplicate region')
    paths=render_plots(specs,source_assets)
    correct_path=paths[ci]
    if observed:
        solution=re.sub(r'!\[\]\(images/[^)]+\)',lambda m:'![]('+correct_path+')',solution)
    else:solution=solution.replace('{{plot}}','![]('+correct_path+')')
    problem=normalize_prose(problem);solution=normalize_prose(solution)
    transformation_fp=fingerprint({'x':sp.srepr(sp.expand(x)),'y':sp.srepr(sp.expand(y)),'orientation':('preserving' if 'orientation-preserving?' in problem else 'reversing'),'domain':'R2'})
    C=sp.Rational(correct['coefficient']);H=sp.Rational(correct['h']);K=sp.Rational(correct['k']);mode=correct['mode'];degree=correct['degree']
    if degree==0:region_expr=(v-K) if mode in ('top','bottom') else (u-H)
    elif degree==-1:region_expr=(u-H)*(v-K)-C
    else:region_expr=v-K-C*(u-H)**degree
    region_op='>' if mode in ('right','top','above','product_gt') else '<'
    mathfp=fingerprint({'strict_region_polynomial':sp.srepr(sp.expand(region_expr)),'op':region_op,'domain':'R2'})
    content=fingerprint({'version':VERSION,'problem':problem,'solution':solution,'bank':sorted(zip(paths,[canonical(s) for s in specs])),'math':mathfp})
    qid=uid(content);fid=uid(qid+'/selection')
    answers=[{':answer/id':uid(fid+'/'+canonical(s)+'/'+path),':answer/type':':answer.type/image',':answer/value':path} for s,path in zip(specs,paths)]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[ci][':answer/id']]}
    spec_map={a[':answer/id']:s for a,s in zip(answers,specs)}
    rng.shuffle(field[':answer-field/choices'])
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'source':SOURCE,'domain':'R2','mathematical_fingerprint':mathfp,'transformation_fingerprint':transformation_fp,'content_fingerprint':content,'plot_specs':spec_map,'formulas':[str(x),str(y)],'correct_spec':correct,'authored_level':not observed}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n\n'.join('![]('+a[':answer/value']+')' for a in f[':answer-field/choices'])+'\n\nWorked solution:\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    if args.count<1:ap.error('positive count required')
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (LEVELS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
