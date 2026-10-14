"""Private full-band trig-composition draft; registered files remain immutable.

Source math basis 2275. Every captured MA source has exact observed_raw replay;
missing ratings/keys/solutions/fields remain missing in that evidence profile.
Normal moderate uses entire source banks and source ordered solution sentences.
Translations vary complete leaf trigonometric arguments without an additional
chain-rule factor. Source coefficients vary only where observed. Easy is an
explicit conservative sine-of-sine coefficient/translation band. Hard keeps the
cosine-of-sine tangent stages and adds documented special-angle phase slots.
No database operations. See adjacent extraction, independent parser, and native
application grading reports; five non-MA inventories never supply templates.
"""
import argparse,copy,hashlib,importlib.util,json,random,re,sys,uuid
from pathlib import Path
import sympy as s
KP_ID=17592186064284
KP_UUID='a483e892-90f2-51f4-80cd-2b1200cd0c37'
TITLE='Differentiating a Composition of Trigonometric Functions Using the Chain Rule'
VERSION='trig-composition-all-bands-2.0.0-draft'
HERE=Path(__file__).with_suffix('');ROOT=HERE.parents[2]
_spec=importlib.util.spec_from_file_location('math_format',ROOT/'scripts/question_capture/math_format.py');math_format=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(math_format)
SUPPORTED_LEVELS=('easy','moderate','hard');x=s.Symbol('x',real=True);u=s.Symbol('u',real=True)
SOURCE=json.loads((HERE/'source.json').read_text());SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
LEVELS={m:('hard' if m=='q-48644' else 'moderate') for m in SOURCES};LEVELS['authored-easy']='easy'
COEFF={'q-341223':4,'q-342443':4,'q-72173':3}
OPS={'q-31356':('cot','cos'),'q-48643':('sin','cos'),'q-72163':('sin','sec'),'q-72170':('csc','cos'),'q-341223':('cos','sin'),'q-342436':('tan','tan'),'q-342443':('sec','sin'),'q-342445':('sec','csc'),'q-72161':('cot','sin'),'q-72173':('sec','cos'),'authored-easy':('sin','sin'),'q-48644':('cos','sin')}
PHASES=('0','1/6','1/4','1/3','1/2','2/3','3/4','5/6','1','-1/6','-1/4','-1/3','-1/2')
DEFAULTS={m:({'a':1,'b':0,'phase':'0'} if m=='q-48644' else {'a':2,'b':0} if m=='authored-easy' else {'a':COEFF[m],'b':0} if m in COEFF else {'b':0}) for m in LEVELS}
TRIG={n:getattr(s,n) for n in ('sin','cos','tan','cot','sec','csc')}

def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def tex(v):return s.latex(v)
def normalize_prose(text):
    text=re.sub(r'\\\\\[[^\]]*pt\]',lambda m:r'\\',text)
    text=re.sub(r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}',lambda m:'\n$$\n'+r'\begin{aligned}'+m[1]+r'\end{aligned}'+'\n$$\n',text,flags=re.S)
    return math_format.normalize_prose(text)
def shifted(b):return 'x' if b==0 else 'x'+('+' if b>0 else '')+str(b)
def parameters_for(m):
    if m=='q-48644':return [{'a':a,'b':b,'phase':phase} for a in range(1,10) for b in (-3,0,3) for phase in PHASES]
    if m in COEFF or m=='authored-easy':return [{'a':a,'b':b} for a in range(1,10) for b in range(-8,9)]
    return [{'b':b} for b in range(-8,9)]
def model(m,p):
    a=p.get('a',1);z=x+p['b'];outer_name,inner_name=OPS[m];inner=TRIG[inner_name](z)
    if m=='q-48644':inner+=s.Rational(p['phase'])*s.pi
    outer=a*TRIG[outer_name](u);curve=outer.subs(u,inner);deriv=s.diff(curve,x)
    if m=='q-48644':
        curve=a*s.cos(inner,evaluate=False);deriv=-a*s.sin(inner,evaluate=False)*s.cos(z,evaluate=False)
    return inner,outer,curve,deriv

def components(text,m,p):
    """Mask every entire leaf trig-argument component, never differential x.

    The b=0 slot renders each captured mathematical component with its exact
    typography. Thus all parameters go through the same masks and template;
    there is no special source-anchor return. Coefficients replace complete
    coefficient-and-operator components, rather than free numeric substrings.
    """
    command=r'(?:\\operatorname\{(?:sin|cos|tan|cot|sec|csc)\}|\\(?:sin|cos|tan|cot|sec|csc)|\{(?:sin|cos|tan|cot|sec|csc)\})'
    pattern=command+r'(?:\^\{[23]\})?[⁡\s]*(?:\(\s*x\s*\)|\{\s*x\s*\}|x)(?![A-Za-z])'
    # Coefficient/operator components and leaf arguments overlap in source
    # strings. Render the enclosing coefficient before masking its argument.
    if m in COEFF:
        for op in ('sin','cos','tan','cot','sec','csc'):
            cmd=r'\operatorname{'+op+'}'
            text=text.replace(str(COEFF[m])+cmd,str(p['a'])+cmd)
    pairs=[]
    for match in re.finditer(pattern,text):
        old=match.group();prefix=old[:old.rfind('x')];suffix=old[old.rfind('x')+1:]
        if p['b']==0:new=old
        else:
            # Retain the operator and power; replace its complete argument.
            op=re.match(command+r'(?:\^\{[23]\})?',old).group();new=op+r'\left('+shifted(p['b'])+r'\right)'
        pairs.append((old,new))
    # Deduplicate masks; simultaneous replacement prevents cascading source
    # coefficient changes or an inner substitution touching its own output.
    pairs=list(dict(pairs).items())
    for i,(old,new) in enumerate(sorted(pairs,key=lambda v:len(v[0]),reverse=True)):
        text=text.replace(old,f'@@COMPONENT{i}@@')
    for i,(old,new) in enumerate(sorted(pairs,key=lambda v:len(v[0]),reverse=True)):
        text=text.replace(f'@@COMPONENT{i}@@',new)
    return text

def common_solution(inner,outer,curve,deriv):
    # Exact common instructional sentences of all observed derivative sources.
    return ('First, we express $y$ as the composite function\n\n$$\n'+f'y={tex(outer)},\\qquad u={tex(inner)}.\n'+'$$\n\nDifferentiating gives\n\n$$\n'
       +r'\frac{\text{d}y}{\text{d}u}='+tex(s.diff(outer,u))+r',\qquad \frac{\text{d}u}{\text{d}x}='+tex(s.diff(inner,x))+'.\n$$\n\nWe now apply the chain rule, and get\n\n$$\n'
       +r'\begin{aligned}\frac{\text{d}y}{\text{d}x} &=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &='+tex(s.diff(outer,u))+r'\cdot ('+tex(s.diff(inner,x))+r') \\ &='+tex(deriv)+r'.\end{aligned}'+'\n$$')

def hard_components(p):
    """Source q-48644 complete formal derivatives and each tangent equation."""
    inner,outer,curve,deriv=model('q-48644',p);z=x+p['b'];c=s.Rational(p['phase'])*s.pi;a=p['a'];point=-p['b'];height=s.simplify(a*s.cos(c));slope=s.simplify(-a*s.sin(c));rhs=s.expand(slope*(x-point)+height)
    # Source sentences and all seven math stages retain the same order. Whole
    # mathematical spans, not individual digits, are parameterized below.
    src=SOURCES['q-48644'];sol=src[':question/worked-solution']
    masks=[(r'$y = f(x)$',r'$y = f(x)$'),('$x = 0$',f'$x = {point}$'),("$f'(0).$",f"$f'({point}).$"),
      (r'f = \cos{u}, \qquad u = \sin x.',f'f = {tex(outer)}, \\qquad u = {tex(inner)}.'),
      (r'\dfrac{\textrm d f}{\textrm d u} = -\sin{u}, \qquad \dfrac{\textrm d u}{\textrm d x} =\cos x.',r'\dfrac{\textrm d f}{\textrm d u} = '+tex(s.diff(outer,u))+r', \qquad \dfrac{\textrm d u}{\textrm d x} ='+tex(s.diff(inner,x))+'.'),
      (r'&=-\sin u \cdot (\cos x)',r'&='+tex(s.diff(outer,u))+r' \cdot ('+tex(s.diff(inner,x))+')'),
      (r'&=-\cos x \sin (\sin x).',r'&='+tex(deriv)+'.'),
      ('$x=0,$',f'$x={point},$'),
      ("f'(0)&=-\\cos (0) \\sin (\\sin (0))",f"f'({point})&={tex(-a*s.sin(s.sin(s.Integer(0),evaluate=False)+c,evaluate=False)*s.cos(s.Integer(0),evaluate=False))}"),
      (r'&=-1 \cdot 0',r'&='+tex(-a*s.cos(0))+r' \cdot '+tex(s.sin(c))),
      ('        &=0.','        &='+tex(slope)+'.'),
      ('$(0,1)',f'$({point},{tex(height)})'),
      (r'y-1 &= (0)\cdot\left(x-0\right)',r'y-\left('+tex(height)+r'\right) &= ('+tex(slope)+r')\cdot\left(x-('+str(point)+r')\right)'),
      ('y&=1.','y&='+tex(rhs)+'.')]
    # Anchor forms are rendered from the same components with source notation;
    # each mask reconstructs its original whole formula when parameters agree.
    if p['a']==1 and p['phase']=='0':
        masks[3]=(masks[3][0],r'f = \cos{u}, \qquad u = '+components(r'\sin x','q-48644',p)+'.')
        masks[4]=(masks[4][0],r'\dfrac{\textrm d f}{\textrm d u} = -\sin{u}, \qquad \dfrac{\textrm d u}{\textrm d x} ='+components(r'\cos x','q-48644',p)+'.')
        masks[5]=(masks[5][0],r'&=-\sin u \cdot ('+components(r'\cos x','q-48644',p)+')')
        masks[6]=(masks[6][0],components(r'&=-\cos x \sin (\sin x).','q-48644',p))
    # Evaluation typography is fixed by the evaluated inner value zero, for
    # every translated source curve, rather than an anchor-return shortcut.
    if p['a']==1 and p['phase']=='0':
        masks[8]=(masks[8][0],f"f'({point})"+r'&=-\cos (0) \sin (\sin (0))')
        masks[9]=(masks[9][0],r'&=-1 \cdot 0')
    if height==1 and point==0:masks[12]=(masks[12][0],r'y-1 &= ('+tex(slope)+r')\cdot\left(x-0\right)')
    for i,(old,new) in enumerate(masks):
        assert old in sol,(i,old);sol=sol.replace(old,f'@@HARD{i}@@')
    for i,(old,new) in enumerate(masks):sol=sol.replace(f'@@HARD{i}@@',new)
    # Prompt entire curve and point slots, retaining source sentences.
    curve_tex=(components(r'\cos \left(\sin x \right)','q-48644',p) if a==1 and c==0 else tex(curve))
    prompt=src[':question/problem'].replace(r'\cos \left(\sin x \right)',curve_tex).replace(r'\left(0,1 \right)',r'\left('+str(point)+','+tex(height)+r' \right)')
    return prompt,sol,rhs,{'point_x':point,'point_y':tex(height),'slope':tex(slope)}

def domain(m,p):
    inn,out,curve,deriv=model(m,p)
    # Explicit nested pole restrictions retain both layers' differentiability.
    on,iname=OPS[m];z='('+shifted(p['b'])+')';inner=tex(inn);restr=[]
    if iname in ('tan','sec'):restr.append('cos'+z+' != 0')
    if iname in ('cot','csc'):restr.append('sin'+z+' != 0')
    if on in ('tan','sec'):restr.append('cos('+inner+') != 0')
    if on in ('cot','csc'):restr.append('sin('+inner+') != 0')
    return {'real_x':True,'restriction':'; '.join(restr) or 'all real x'}

def complete_bank(m,p):
    """Every observed recipe is preserved together; no pooled choice search."""
    z=x+p['b'];S=s.sin(z);C=s.cos(z);a=p.get('a',1)
    if m=='q-31356':return (S*s.cot(C)**2,S*s.csc(C)**2,s.csc(z)*s.sin(C)**2,S*s.cos(s.csc(z))**2,s.csc(z)*s.cos(S)**2)
    if m=='q-48643':return (-C*s.sin(C),-S*s.cos(C),-S*s.cos(S),-C*s.cos(S),-S*s.sin(C))
    if m=='q-72161':return (-C*s.csc(C)**2,-C*s.csc(S)**2,-s.csc(S)**2,s.csc(C)**2,C*s.csc(C)**2)
    if m=='q-72173':return (a*s.sec(z)*s.tan(-S),a*S*s.sec(-S)*s.tan(-S),a*C*s.sec(C)*s.tan(C),a*S*s.sec(z)*s.tan(C),-a*S*s.sec(C)*s.tan(C))
    return ()

from functools import lru_cache
@lru_cache(None)
def _reject_bank(m,a):
    p={'a':a,'b':0}
    bank=complete_bank(m,p)
    for i,first in enumerate(bank):
        for second in bank[i+1:]:
            delta=first-second
            # Nonzero defined values prove nonidentity. Translate witnesses
            # with the same slot to avoid all source-function pole sets.
            witnesses=(s.Rational(1,5),s.Rational(2,5),s.Rational(4,5))
            if any(abs(complex(delta.subs(x,t-p['b']).evalf(16)))>1e-10 for t in witnesses):continue
            if s.trigsimp(delta)==0:raise ValueError('Entire selected source bank collides; reject instance')
def reject_bank_collisions(m,p):
    # Translation is an invertible substitution and common a is nonzero.
    # Collision proof may therefore be cached on each full profile/coefficient.
    return _reject_bank(m,p.get('a',1))

def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
    rng=random.Random(seed);eligible=[m for m in LEVELS if LEVELS[m]==level];m=template or rng.choice(eligible)
    if m not in eligible:raise ValueError('Template/difficulty mismatch')
    raw=profile in ('observed_raw','raw-'+m)
    if profile not in (None,'default','observed_raw','raw-'+m,'source-bank','source-blank','authored-blank'):raise ValueError('Unknown profile')
    if raw and m not in SOURCES:raise ValueError('No source evidence for authored easy')
    p=copy.deepcopy(parameters) if parameters is not None else rng.choice(parameters_for(m))
    if p not in parameters_for(m) or any(type(v)!=int for k,v in p.items() if k!='phase'):raise ValueError('Parameters outside documented bounded domain')
    inner,outer,curve,deriv=model(m,p);extra={}
    if not raw:reject_bank_collisions(m,p)
    if m=='q-48644':prompt,worked,answer,extra=hard_components(p)
    elif m=='authored-easy':
        prompt=f'Given that $y={tex(curve)},$ we have\n\n'+r'$\frac{\text{d}y}{\text{d}x}=$'+'\n{{field-1}}'+r'$\cdot \cos($'+'\n{{field-2}} $).$'
        worked=common_solution(inner,outer,curve,deriv);answer=deriv
    else:prompt=components(SOURCES[m][':question/problem'],m,p);worked=components(SOURCES[m].get(':question/worked-solution',''),m,p);answer=deriv
    q={':question/problem':prompt}
    if raw:
        source=SOURCES[m]
        if ':question/difficulty' in source:q[':question/difficulty']=source[':question/difficulty'][':db/ident']
        if ':question/worked-solution' in source:q[':question/worked-solution']=worked
        fields=copy.deepcopy(source.get(':question/answer-fields',[]))
    else:
        q[':question/difficulty']=':question.difficulty/'+level
        if not worked:worked=common_solution(inner,outer,curve,deriv)
        q[':question/worked-solution']=worked
        fields=copy.deepcopy(SOURCES.get(m,{}).get(':question/answer-fields',[]))
        if not fields:
            fragments=[('field-1',p['a']*s.cos(x+p['b'])),('field-2',inner)] if m=='authored-easy' else [('field-1',answer)]
            fields=[{':answer-field/key':key,':answer-field/type':{':db/ident':':answer-field.type/blank'},':answer-field/choices':[{':answer/value':tex(val),':answer/type':{':db/ident':':answer.type/math'}}]} for key,val in fragments]
            if m!='authored-easy':prompt+='\n\n'+('$y=$ {{field-1}}' if m=='q-48644' else r'$\frac{\text{d}y}{\text{d}x}=$ {{field-1}}')
            q[':question/problem']=prompt
        for f in fields:
            if ':answer-field/correct' not in f:
                index=1 if m=='q-31356' else 0;f[':answer-field/correct']=copy.deepcopy(f[':answer-field/choices'][index])
    if raw and ':question/answer-fields' not in SOURCES[m]:fields=None
    # Parameterize the entire observed field content and preserve attributes.
    if fields is not None:
        for f in fields:
            if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
            for a in f[':answer-field/choices']:
                if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
                if m in SOURCES and m!='q-48644':a[':answer/value']=components(a[':answer/value'],m,p)
                if not raw:a[':answer/value']=math_format.normalize_tex(a[':answer/value'])
        types={f[':answer-field/type'] for f in fields}
        if field_type is not None and field_type not in types and ':answer-field.type/'+field_type not in types:raise ValueError('Field contract cannot change')
    elif field_type is not None:raise ValueError('Raw source has no field contract')
    if not raw:
        for k in (':question/problem',':question/worked-solution'):q[k]=normalize_prose(q[k])
    # Identity depends on content and whole bank; no seed/order aliases.
    normalized=[]
    for f in fields or []:
        correct=f.get(':answer-field/correct');cv=correct.get(':answer/value') if correct else None
        if cv is not None and m in SOURCES and m!='q-48644':cv=components(cv,m,p)
        if cv is not None and not raw:cv=math_format.normalize_tex(cv)
        normalized.append({'key':f[':answer-field/key'],'type':f[':answer-field/type'],'values':sorted(a[':answer/value'] for a in f[':answer-field/choices']),'correct':cv})
    cid=digest({'q':q,'fields':normalized,'domain':domain(m,p),'version':VERSION});uid=lambda t:str(uuid.uuid5(uuid.UUID(KP_UUID),t));qid=uid(cid);q[':question/id']=qid
    if fields is not None:
        for f,norm in zip(fields,normalized):
            fid=uid(qid+'|'+f[':answer-field/key']);f.pop(':db/id',None);f[':answer-field/id']=fid
            for a in f[':answer-field/choices']:
                a.pop(':db/id',None);a[':answer/id']=uid(fid+'|'+a[':answer/value'])
                if ':answer/feedback' in a:a[':answer/feedback']=components(a[':answer/feedback'],m,p)
            if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==norm['correct'])]
            if not raw and f[':answer-field/type'].endswith('/radio'):random.Random(seed).shuffle(f[':answer-field/choices'])
        q[':question/answer-fields']=fields
    fp=digest({'curve':s.srepr(curve),'task':'tangent' if m=='q-48644' else 'derivative','answer':s.srepr(answer),'field_shape':[(f[':answer-field/key'],f[':answer-field/type']) for f in fields or []]})
    r={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':uid(VERSION),'version':VERSION,'seed':seed,'level':level,'template':m,'parameters':p,'profile':'observed_raw' if raw else 'source-bank' if any(f[':answer-field/type'].endswith('/radio') for f in fields or []) else 'authored-blank' if m in ('q-48644','q-72163','q-72170','authored-easy') else 'source-blank','bank_profile':m if any(f[':answer-field/type'].endswith('/radio') for f in fields or []) else None,'mathematical_fingerprint':fp,'parameter_fingerprint':fp,'content_identity':cid,'domain':domain(m,p),'source_references':[m] if m in SOURCES else ['q-48643','e-735'],'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'evidence_only':raw,'eligible_for_learning':not raw,'difficulty_provenance':'authored conservative basic composition' if m=='authored-easy' else 'authored moderate completion of unrated source' if m=='q-31356' else 'observed MA level; documented same-backbone slot extension','origin':'captured MA template' if m in SOURCES else 'authored same-KP extension','dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'plots':[],'tangent':extra}}
    if raw:return r
    return math_format.validate_generated_record(r)

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
    q=r['question'];out=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):out.append('\n'.join(('* ' if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1] else '- ')+a[':answer/value'] for a in f[':answer-field/choices']))
    if ':question/worked-solution' in q:out.append(q[':question/worked-solution'])
    return '\n\n'.join(out)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=('json','markdown'),default='json');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
    if a.count<1:p.error('count must be positive')
    levels=SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty];rs=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)];print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
