#!/usr/bin/env python3
"""Seeded, relocatable determinant-unknown generator; no assets or database writes.

Current source: math basis 4662; 18 practice layouts plus canonical e-4436 replay.
Easy: linear. Moderate: repeated square. Hard: quadratic cancellation to linear.
Normal radio banks choose candidates and the correct role before coefficients.
Observed banks are restricted to exact source replay. See instructional-account.md.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from math_format import normalize_prose, normalize_tex, checked_math_content

KP_ID=17592186059750
KP_UUID='4ccdde46-a4ab-517e-910b-571a3a166b6a'
TITLE='Solving for an Unknown in an Expression Involving the Determinant of a 2x2 Matrix'
VERSION='determinant-unknown-v2-format-audit-9122-v1'
DIR=Path(__file__).resolve().parent
SOURCE=json.loads((DIR/'source-data.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['material']['kp'][':knowledge-point/questions']}
CANONICAL=SOURCE['material']['kp'][':knowledge-point/canonical-example']
QUESTIONS[CANONICAL[':question/math-academy-id']]=CANONICAL
Z=sp.Symbol('z',real=True)
# Layout-specific families preserve distinct solution sequences and response forms.
# c are complete integer coefficient components, never arbitrary expression replacements.
TEMPLATES={
'q-11651': dict(level='easy',family='diagonal',c=[2,3,5],root=9,var='k',name='C',kind='radio',equation=True),
'q-19801': dict(level='moderate',family='symmetric',c=[1,2,-3],root=3,var='t',name='A',kind='radio',equation=False),
'q-127614': dict(level='moderate',family='quad_bottom',c=[2,6,2,-2],root=4,var='x',name='D',kind='blank',equation=False),
'q-11653': dict(level='easy',family='offdiagonal',c=[2,4,3],root=1,var='w',name='M',kind='radio',equation=False),
'q-127604': dict(level='easy',family='bottom_linear',c=[3,-5,2,-1,2],root=-1,var='k',name='U',kind='radio',equation=True),
'q-127606': dict(level='moderate',family='quad_top',c=[1,2,2,8],root=-2,var='v',name='T',kind='radio',equation=True),
'q-127607': dict(level='moderate',family='quad_right',c=[1,-3,1,3],root=3,var='r',name='P',kind='radio',equation=False),
'q-127608': dict(level='moderate',family='quad_negative',c=[1,5,1,3],root=1,var='p',name='B',kind='radio',equation=True),
'q-127609': dict(level='moderate',family='quad_top',c=[3,1,3,-5],root=3,var='y',name='A',kind='radio',equation=True),
'q-275598': dict(level='easy',family='offdiagonal',c=[1,4,6],root=5,var='k',name='C',kind='blank',equation=False),
'q-275601': dict(level='hard',family='cancellation',c=[3,4,5],root=4,var='p',name='A',kind='blank',equation=False),
'q-317377': dict(level='easy',family='offdiagonal',c=[2,3,5],root=7,var='m',name='D',kind='blank',equation=False),
'q-317382': dict(level='easy',family='top_linear',c=[1,1,2,-1,-5,4],root=20,var='r',name='U',kind='blank',equation=False),
'q-317385': dict(level='moderate',family='symmetric',c=[3,2,-4],root=4,var='s',name='S',kind='blank',equation=False),
'q-69661': dict(level='easy',family='top_linear',c=[1,-1,1,1,-3,2],root=-3,var='p',name='S',kind='radio',equation=False),
'q-69658': dict(level='easy',family='signed_diagonal',c=[-1,5,4,3],root=-8,var='v',name='U',kind='radio',equation=False),
'q-11647': dict(level='easy',family='offdiagonal',c=[2,2,6],root=5,var='x',name='B',kind='radio',equation=True),
'q-275599': dict(level='moderate',family='symmetric',c=[3,4,-3],root=6,var='t',name='A',kind='blank',equation=False),
}
TEMPLATES['e-4436']=dict(level='easy',family='diagonal',c=[2,-1,-3],root=4,var='k',name='A',kind='blank',equation=False,replay_only=True)
SHORT_LINEAR={'e-4436','q-317377','q-317382','q-275601','q-11651'}
PROFILES={k:TEMPLATES[k] for k,q in QUESTIONS.items() if q.get(':question/answer-fields') and TEMPLATES[k]['kind']=='radio'}

def tex(e):
    return sp.latex(sp.sympify(e)).replace(' ', '')
def term(a,v=''):
    a=sp.sympify(a)
    if not v:return tex(a)
    if a==1:return v
    if a==-1:return '-'+v
    if a==0:return '0'
    return tex(a)+v

def add(parts):
    out=''
    for p in parts:
        if not out:out=p
        elif p.startswith('-'):out+=p
        else:out+='+'+p
    return out

def pair(c,v,constant_first=False):
    a,b=c
    return add([tex(b),term(a,v)]) if constant_first else add([term(a,v),tex(b)])
def grouped(s):return '('+s+')' if any(c in s[1:] for c in '+-') or s.startswith('-') else s

def objects(f,c):
    if f=='signed_diagonal':a,b,c0,d=c;return [a*Z,sp.Integer(b),sp.Integer(c0),sp.Integer(d)]
    if f=='diagonal':a,b,d=c;return [sp.Integer(a),sp.Integer(b),sp.Integer(d),Z]
    if f=='offdiagonal':a,b,d=c;return [sp.Integer(a),Z,sp.Integer(b),sp.Integer(d)]
    if f=='bottom_linear':a,b,c0,d,e=c;return [sp.Integer(a),sp.Integer(b),c0*Z,d*Z+e]
    if f=='top_linear':a,u,b,v,c0,d=c;return [a+u*Z,b+v*Z,sp.Integer(c0),sp.Integer(d)]
    if f=='symmetric':h,b,c0=c;return [h+Z,b*Z,sp.Integer(c0),h-Z]
    if f=='quad_bottom':a,b,c0,d=c;return [a*Z,sp.Integer(b),c0*Z,Z+d]
    if f=='quad_top':a,b,c0,d=c;return [a*Z,b*Z,sp.Integer(c0),Z+d]
    if f=='quad_right':a,d,b,c0=c;return [Z+d,b*Z,sp.Integer(c0),a*Z]
    if f=='quad_negative':a,d,b,c0=c;return [d-Z,b*Z,sp.Integer(c0),a*Z]
    if f=='cancellation':a,b,d=c;return [a+Z,b*Z-Z**2,sp.Integer(1),d-Z]
    raise ValueError(f)

def entries_tex(f,c,v):
    if f=='signed_diagonal':a,b,c0,d=c;return [term(a,v),tex(b),tex(c0),tex(d)]
    if f=='diagonal':a,b,d=c;return [tex(a),tex(b),tex(d),v]
    if f=='offdiagonal':a,b,d=c;return [tex(a),v,tex(b),tex(d)]
    if f=='bottom_linear':a,b,c0,d,e=c;return [tex(a),tex(b),term(c0,v),pair([d,e],v)]
    if f=='top_linear':a,u,b,w,c0,d=c;return [pair([u,a],v,True),pair([w,b],v,True),tex(c0),tex(d)]
    if f=='symmetric':h,b,c0=c;return [pair([1,h],v,True),term(b,v),tex(c0),pair([-1,h],v,True)]
    if f in ('quad_top','quad_bottom'):
        a,b,c0,d=c;return [term(a,v),tex(b) if f=='quad_bottom' else term(b,v),term(c0,v) if f=='quad_bottom' else tex(c0),pair([1,d],v)]
    if f=='quad_right':a,d,b,c0=c;return [pair([1,d],v),term(b,v),tex(c0),term(a,v)]
    if f=='quad_negative':a,d,b,c0=c;return [pair([-1,d],v,True),term(b,v),tex(c0),term(a,v)]
    if f=='cancellation':a,b,d=c;return [pair([1,a],v,True),add([term(b,v),'-{'+v+'}^{2}']),'1',pair([-1,d],v,True)]

def polynomial(Q,L,C,v,order='descending'):
    powers=[(Q,'{'+v+'}^{2}'),(L,v),(C,'')]
    if order=='constant_first':powers=list(reversed(powers))
    return add([term(a,x) for a,x in powers if a!=0]) or '0'

def align(rows):return '\\begin{aligned}'+r' \\ '.join(a+' & ='+b for a,b in rows)+r'\end{aligned}'

def math_stages(k,p):
    t=TEMPLATES[k];f=t['family'];c=p['c'];r=sp.Rational(p['root']);v=t['var'];M=t['name']
    E=objects(f,c);D=sp.expand(E[0]*E[3]-E[1]*E[2]);Q=D.coeff(Z,2);L=D.coeff(Z,1);C=D.subs(Z,0);N=D.subs(Z,r)
    ts=entries_tex(f,c,v);matrix=ts[0]+' & '+ts[1]+r' \\ '+ts[2]+' & '+ts[3]
    product=grouped(ts[0])+r'\cdot '+grouped(ts[3])+'-'+grouped(ts[1])+r'\cdot '+grouped(ts[2])
    # Symmetric and hard sources omit the first multiplication dot between binomials.
    if f in ('symmetric','cancellation'):product=grouped(ts[0])+grouped(ts[3])+'-'+grouped(ts[1])+r'\cdot '+grouped(ts[2])
    order='constant_first' if f in ('offdiagonal','cancellation') or k in ('q-317382','q-69661') else 'descending'
    P=polynomial(Q,L,C,v,order)
    detrows=[('det('+M+')','|'+r'\begin{aligned}'+matrix+r'\end{aligned}|'),('',product)]
    if f=='top_linear':
        a,u,b,w,c0,d=c
        detrows.append(('',add([tex(a*d),term(u*d,v),tex(-b*c0),term(-w*c0,v)])))
    if f=='symmetric':h,b,c0=c;detrows.append(('',add([tex(h*h),'-{'+v+'}^{2}',term(-b*c0,v)])))
    if f=='cancellation':
        a,b,d=c
        detrows.append(('',add([tex(a*d),term(-a,v),term(d,v),'-{'+v+'}^{2}',term(-b,v),'{'+v+'}^{2}'])))
        detrows.append(('',add([tex(a*d),term(L,v),r'-\cancel{{'+v+r'}^{2}}',r'\cancel{{'+v+r'}^{2}}'])))
    detrows.append(('',P))
    eqrows=[('det('+M+')',tex(N)),(P,tex(N))]
    if Q:
        eqrows.append((polynomial(Q,L,C-N,v),'0'))
        if Q!=1:eqrows.append((polynomial(1,L/Q,(C-N)/Q,v),'0'))
        factor='('+pair([1,-r],v)+')^{2}'
        eqrows.extend([(factor,'0'),(v,tex(r))])
    else:
        if k not in SHORT_LINEAR:
            lhs=term(L,v)
            eqrows.append((lhs,tex(N)+'-'+grouped(tex(C))))
        if not (k=='q-69661' and L==1):eqrows.append((term(L,v),tex(N-C)))
        eqrows.append((v,tex(r)))
    return dict(coefficients=c,matrix=matrix,determinant=D,target=N,Q=Q,L=L,C=C,root=r,detrows=detrows,eqrows=eqrows)

def validate_parameters(k,p):
    t=TEMPLATES[k]
    if set(p)!={'c','root'}:raise ValueError('Parameters require exactly c and root')
    c=p['c'];r=sp.sympify(p['root'])
    if len(c)!=len(t['c']) or any(type(a) is not int for a in c):raise ValueError('Complete integer coefficient components required')
    if r.is_Integer is not True:raise ValueError('Integer root required')
    limit=10 if t['level']=='easy' else 8
    if any(abs(a)>limit or a==0 for a in c):raise ValueError('Nonzero signed coefficients within level workload bounds required')
    if abs(r)>dict(easy=24,moderate=6,hard=12)[t['level']]:raise ValueError('Root outside level bounds')
    m=math_stages(k,p);Q,L,C,N=(m[a] for a in ['Q','L','C','target'])
    if abs(N)>200:raise ValueError('Target outside arithmetic bounds')
    if t['level']=='moderate':
        if Q==0 or L==0 or sp.expand(m['determinant']-N-Q*(Z-r)**2)!=0:raise ValueError('Moderate requires a nondegenerate repeated-root quadratic')
    elif Q!=0 or L==0:raise ValueError('Easy/hard determinant must reduce to nonconstant linear')
    if t['level']=='hard' and (c[0]==c[2] or c[1]==0):raise ValueError('Hard requires nonzero distribution terms')
    return m

def sample(k,rng,root,stats=None):
    t=TEMPLATES[k];f=t['family']
    for _ in range(2000):
        if stats is not None:stats['coefficient_attempts']=stats.get('coefficient_attempts',0)+1
        r=sp.Integer(root)
        if f=='symmetric':
            b=rng.choice([1,2,3,4]);c0=-2*r/b
            if c0.is_Integer is not True:continue
            c=[rng.randint(1,6),b,int(c0)]
        elif f.startswith('quad'):
            a=rng.choice([1,2,3]);b=rng.choice([-3,-2,-1,1,2,3]);c0=rng.choice([i for i in range(-6,7) if i])
            if f=='quad_negative':d=sp.Rational(2*a*r+b*c0,a);c=[a,d,b,c0]
            elif f=='quad_right':d=sp.Rational(-2*a*r+b*c0,a);c=[a,d,b,c0]
            else:d=sp.Rational(-2*a*r+b*c0,a);c=[a,b,c0,d]
            if d!=int(d):continue
            c=[int(a) for a in c]
        else:
            c=[rng.choice([i for i in range(-8,9) if i]) for _ in t['c']]
        if int(r)!=r:continue
        p={'c':c,'root':int(r)}
        try:validate_parameters(k,p);return p
        except ValueError as error:
            if stats is not None:
                reasons=stats.setdefault('rejections',{});key=str(error);reasons[key]=reasons.get(key,0)+1
    raise ValueError('No eligible complete instance')

def render_prompt(k,m):
    t=TEMPLATES[k];q=QUESTIONS[k];s=q[':question/problem']
    if k=='e-4436':s=normalize_prose(s)
    # Replace complete matrix content and determinant scalar, never global short substrings.
    pat=r'(\\begin\{(?:aligned|bmatrix)\})(.*?)(\\end\{(?:aligned|bmatrix)\})'
    matrix=m['matrix']
    if k=='q-19801':
        matrix=matrix.replace('+t',' + t').replace('-t',' - t')
    if k=='e-4436':
        # Retain the canonical prompt's cell whitespace as a presentation mask.
        def canonical_matrix(match):
            cells=iter(entries_tex(t['family'],m['coefficients'],t['var']))
            parts=re.split(r'(&|\\\\)',match[2])
            for i in range(0,len(parts),2):
                cell=re.fullmatch(r'(\s*)(.*?)(\s*)',parts[i],re.S)
                parts[i]=cell[1]+next(cells)+cell[3]
            return match[1]+''.join(parts)+match[3]
        s=re.sub(pat,canonical_matrix,s,flags=re.S)
    else:s=re.sub(pat,lambda a:a[1]+matrix+a[3],s,flags=re.S)
    s=re.sub(r'((?:det\}?|\\text\{det\}|\\det)\([^)]*\)\s*=\s*)(-?\d+)',lambda a:a[1]+tex(m['target']),s)
    if k in ('q-127614','e-4436'):s+='\n\n$'+t['var']+'=$\n{{field-1}}'
    return s

def style_display(original, rows):
    """Use the source's whitespace, labels and punctuation as a component mask.

    Every complete mathematical side comes from computation; no source payload
    return branch. Optional normalization rows use shared generic alignment.
    """
    original=re.sub(r'\\begin\{aligned\}', '<OUTER>',original,count=1)
    original=re.sub(r'\|\\begin\{aligned\}.*?\\end\{aligned\}\|','<MATRIX>',original,flags=re.S)
    original=re.sub(r'\\begin\{vmatrix\}.*?\\end\{vmatrix\}','<MATRIX>',original,flags=re.S)
    assert original.startswith('<OUTER>') and original.endswith(r'\end{aligned}')
    body=original[len('<OUTER>'):-len(r'\end{aligned}')]
    old=re.split(r'\\\\',body)
    if len(old)!=len(rows):return align(rows)
    rendered=[]
    for text,(lhs,rhs) in zip(old,rows):
        match=re.fullmatch(r'(\s*)(.*?)(\s*)&(\s*)=(\s*)(.*?)(\s*)',text,re.S)
        assert match,text
        lead,oldleft,before,after,eqgap,oldright,trail=match.groups()
        if 'det' in oldleft:lhs=oldleft
        if oldright.endswith('.'):rhs=rhs+'.'
        rendered.append(lead+lhs+before+'&'+after+'='+eqgap+rhs+trail)
    return r'\begin{aligned}'+r'\\'.join(rendered)+r'\end{aligned}'

def render_solution(k,m):
    q=QUESTIONS[k];s=q.get(':question/worked-solution')
    if s is None:
        s='For a $2\\times 2$ matrix, the determinant is given by the formula\n\n$$\n|\\begin{aligned}a & b \\\\ c & d\\end{aligned}|=ad-bc.\n$$\n\nUsing the formula, we have:\n\n$$\n{det}\n$$\n\nSince $det('+TEMPLATES[k]['name']+')={target}$, we obtain:\n\n$$\n{eq}\n$$'
        return s.replace('{det}',align(m['detrows'])).replace('{eq}',align(m['eqrows'])).replace('{target}',tex(m['target']))
    displays=list(re.finditer(r'\$\$\n(.*?)\n\$\$',s,re.S))
    assert len(displays)==3
    detrows=list(m['detrows'])
    if k in ('q-317385','q-275599'):
        left,right=detrows[1]
        ts=entries_tex(TEMPLATES[k]['family'],m['coefficients'],TEMPLATES[k]['var'])
        detrows[1]=(left,grouped(ts[0])+grouped(ts[3])+'-'+grouped(ts[1])+'('+ts[2]+')')
    values=[style_display(displays[1][1],detrows),style_display(displays[2][1],m['eqrows'])]
    for a,value in reversed(list(zip(displays[1:],values))):s=s[:a.start(1)]+value+s[a.end(1):]
    s=re.sub(r'(\$(?:\\det|det)\([^)]*\)=)(-?\d+)',lambda a:a[1]+tex(m['target']),s)
    return s

def choice_values(k,m,profile,bank=None):
    t=TEMPLATES[k];r=m['root'];v=t['var']
    if t['kind']=='blank':return [tex(r)],['solved_scalar']
    if profile=='authored:candidate-bank':
        if bank is None or len(bank)!=5 or r not in bank or len(set(bank))!=5:
            raise ValueError('Five distinct candidate scalars including the root required')
        return [(v+'=' if t['equation'] else '')+tex(a) for a in bank],['candidate_integer']*5
    if profile.startswith('observed:'):
        if profile!='observed:'+k:raise ValueError('Profile belongs to a different source layout')
        # Unknown intent: proportional observed expression pattern. Stored coefficients
        # are extracted expression/root ratios, not an answer lookup or default error fit.
        q=QUESTIONS[k];values=[];recipes=[]
        for a in q[':question/answer-fields'][0][':answer-field/choices']:
            raw=a[':answer/value'];frag=raw.split('=')[-1].strip();val=parse_math(frag)
            ratio=val/sp.Rational(t['root']);result=sp.cancel(ratio*r)
            # Preserve unreduced fractional expression spelling as a proportional mask.
            match=re.fullmatch(r'(-?)\\{1,2}frac\{(\d+)\}\{(\d+)\}',frag)
            if match:
                sign,n,d=match.groups();numer=sp.Rational(int(n)*(1 if not sign else -1),t['root'])*r
                if numer.is_Integer:rendered=('-' if numer<0 else '')+r'\frac{'+str(abs(numer))+'}{'+d+'}'
                else:rendered=tex(result)
            else:rendered=tex(result)
            # Source equation-prefix spacing is a mask; the parameterized formula
            # determines every scalar value.
            prefix=raw[:raw.index('=')+1] if '=' in raw else ''
            if prefix:
                gap=re.match(r'\s*',raw[len(prefix):]).group();rendered=prefix+gap+rendered
            values.append(rendered);recipes.append('observed_scalar_ratio:'+str(ratio)+' (intent unknown)')
        return values,recipes
    if profile!='authored:operations':raise ValueError('Unsupported profile')
    if t['level']=='moderate':vals=[r,-r,2*r,r*r,r/2];recipes=['correct','reverse_factored_sign','use_linear_coefficient_without_halving','use_constant_term','halve_root_again']
    else:
        L,C,N=m['L'],m['C'],m['target'];vals=[r,(N+C)/L,(C-N)/L,N/L,N-C];recipes=['correct','wrong_transposition_sign','reverse_numerator','omit_constant','omit_final_division']
    if len(set(vals))!=5:raise ValueError('Whole bank rejected: equivalent options')
    return [(v+'=' if t['equation'] else '')+tex(a) for a in vals],recipes

def parse_math(s):
    """Independent small LaTeX grammar used only for scalar/replay semantics."""
    from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
    s=s.replace('\\\\frac','\\frac').replace('\\cdot','*').replace('\\left','').replace('\\right','')
    # A cancelled term retains its value while checking the pre-reduction equality.
    s=s.replace('\\cancel','')
    while re.search(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',s):s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
    s=s.replace('{','(').replace('}',')').replace('^','**').rstrip('.')
    return parse_expr(s,local_dict={x:sp.Symbol(x,real=True) for x in 'xyztkvrpswm'},transformations=standard_transformations+(implicit_multiplication_application,))

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,bank=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    rng=random.Random(seed)
    if profile and profile.startswith('observed:'):
        pk=profile.split(':',1)[1]
        if template and template!=pk:raise ValueError('Profile/template mismatch')
        template=pk
        original=TEMPLATES[pk]
        replay={'c':original['c'],'root':original['root']}
        if parameters is None:parameters=replay
        elif parameters!=replay:raise ValueError('Observed bank profiles are source-replay only')
    eligible=[k for k,t in TEMPLATES.items() if (not t.get('replay_only') or template==k) and t['level']==level and (field_type is None or t['kind']==field_type.replace(':answer-field.type/',''))]
    k=template or rng.choice(eligible)
    if k not in eligible:raise ValueError('Template outside difficulty or field layout')
    t=TEMPLATES[k]
    if t.get('replay_only') and parameters is None:parameters={'c':t['c'],'root':t['root']}
    profile=profile or ('authored:blank_repair' if k in ('q-127614','e-4436') else 'none' if t['kind']=='blank' else 'authored:candidate-bank')
    if t['kind']=='blank' and profile not in ('none','authored:blank_repair'):raise ValueError('Blank has no distractor profile')
    if profile=='authored:operations':raise ValueError('Legacy bank disabled: recognizable answer pattern')
    root_domain=[i for i in range(-5,6) if i] if level=='moderate' else list(range(-10,11))
    if parameters is not None:
        selected_root=parameters['root']
        if profile=='authored:candidate-bank' and bank is None:
            bank=[selected_root]+rng.sample([i for i in root_domain if i!=selected_root],4)
    elif profile=='authored:candidate-bank':
        bank=rng.sample(root_domain,5) if bank is None else bank
        selected_root=rng.choice(bank)
    else:selected_root=rng.choice(root_domain)
    sampling_stats={}
    for _ in range(2000):
        p=parameters if parameters is not None else sample(k,rng,selected_root,sampling_stats)
        m=validate_parameters(k,p)
        try:values,recipes=choice_values(k,m,profile,bank);break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('Could not sample complete valid bank')
    prompt=normalize_prose(render_prompt(k,m));solution=normalize_prose(render_solution(k,m))
    values=[normalize_tex(a) for a in values]
    numeric=[parse_math(a.split('=')[-1]) for a in values]
    good=[i for i,x in enumerate(numeric) if sp.simplify(x-m['root'])==0]
    if len(good)!=1 or len(set(numeric))!=len(numeric):raise ValueError('Ambiguous complete bank')
    # mathematical task fingerprint includes the actual matrix coefficients and target;
    # canonical variable alias, layout and bank are excluded. Entries matter to assessed products.
    task={'matrix':[sp.srepr(a) for a in objects(t['family'],p['c'])],'target':str(m['target'])}
    fp=hashlib.sha256(json.dumps(task,sort_keys=True).encode()).hexdigest()
    identity={'version':VERSION,'prompt':prompt,'solution':solution,'kind':t['kind'],'values':sorted(values)}
    digest=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    qid=str(uuid.uuid5(uuid.NAMESPACE_URL,digest));fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+t['kind']))
    choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),a)),':answer/type':':answer.type/math',':answer/value':a} for a in values]
    correct=choices[good[0]][':answer/id'];rng.shuffle(choices)
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection' if t['kind']=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+t['kind'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'template':k,'profile':profile,'seed':seed,'parameters':p,'source':{a:SOURCE[a] for a in ('database','basis','lineage')},'source_refs':[k],'mathematical_fingerprint':fp,'content_digest':digest,'recipes':recipes,'domain':'real scalar, unique integer solution; moderate repeated root','authored_field_repair':k in ('q-127614','e-4436'),'authored_level_assignment':k in ('q-11651','q-19801','e-4436'),'canonical_replay_default':bool(t.get('replay_only')),'notation_normalization':'canonical source component masks; grouped signed factors','dependencies':{'sympy':sp.__version__},'plot_rating':'none','sampling':{'root_chosen_before_coefficients':True,'selected_root':selected_root,'bank':bank,**sampling_stats}}}

# EASY — determinant substitution, collection, two-step linear equation.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — quadratic determinant, zero form, GCF/sign normalization, perfect square.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — binomial distribution, subtracting a quadratic, cancellation to LINEAR.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    bank='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']) if f[':answer-field/type'].endswith('/radio') else ''
    return q[':question/problem']+'\n\n'+bank+'\n\n'+q[':question/worked-solution']

def main():
    a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='easy');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['json','markdown'],default='json');a.add_argument('--template');a.add_argument('--profile');ns=a.parse_args()
    if ns.count<1:a.error('--count must be positive')
    levels=['easy','moderate','hard'] if ns.difficulty=='all' else [ns.difficulty]
    rows=[generate(l,ns.seed+i,ns.template,profile=ns.profile) for l in levels for i in range(ns.count)]
    print(json.dumps(rows,indent=2) if ns.format=='json' else '\n\n---\n\n'.join(markdown(a) for a in rows))
if __name__=='__main__':main()
