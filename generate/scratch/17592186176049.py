#!/usr/bin/env python3
"""Tangent properties: current three-field checkbox format, finite catalogs.

Historical source evidence is preserved at basis 1356. Current source replay
uses migrated Boolean fields at basis 2242. Easy/moderate workload assignments
are authored; hard retains observed families and a two-identity extension.
Only normal supported records are eligible for replenishment. This script
performs no database reads or writes; scoped commit logic is in replenish.py.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186176049
KP_UUID='4241c7bd-4a2b-556f-be9f-8a884addebb9'
TITLE='Describing Properties of the Tangent Function'
VERSION='tangent-properties-2-checkbox'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
ROMAN=['I','II','III']
SUBSETS=['I only','II only','III only','I and II only','I and III only','II and III only']
NAMESPACE=uuid.UUID(KP_UUID)

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(NAMESPACE,v))
def label(truth):
    names=[ROMAN[i] for i,t in enumerate(truth) if t]
    if not names:return 'None of the statements'
    if len(names)==3:return 'I, II and III'
    return ' and '.join(names)+' only'

def graph(force=False):
    """Fixed y=tan x geometry: no transformation or independent sampling."""
    png=ROOT/'tangent.png'; side=ROOT/'tangent.json'
    if png.exists() and side.exists() and not force:return str(png)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from tempfile import NamedTemporaryFile
    fig,ax=plt.subplots(figsize=(4.8,4.0),dpi=160)
    for k in [-1,0,1]:
        x=np.linspace(k*np.pi-np.pi/2+.01,k*np.pi+np.pi/2-.01,1800)
        ax.plot(x,np.tan(x),color='#2877ba',lw=1.7)
    for h in [-1.5,-.5,.5,1.5]:ax.axvline(h*np.pi,color='#999999',ls=(0,(4,4)),lw=.8)
    ax.set(xlim=(-1.9*np.pi,1.9*np.pi),ylim=(-5,5))
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['bottom','left']].set_position('zero')
    ax.set_xticks([i*np.pi/2 for i in [-3,-2,-1,1,2,3]],
        [r'$-\frac{3\pi}{2}$',r'$-\pi$',r'$-\frac{\pi}{2}$',r'$\frac{\pi}{2}$',r'$\pi$',r'$\frac{3\pi}{2}$'])
    ax.set_yticks([-4,-2,2,4]);ax.text(1.84*np.pi,-.45,'$x$');ax.text(.2,4.65,'$y$')
    for xy,xytext in [((1.9*np.pi,0),(1.8*np.pi,0)),((0,5),(0,4.7))]:
        ax.annotate('',xy=xy,xytext=xytext,arrowprops={'arrowstyle':'->','lw':1})
    fig.tight_layout()
    with NamedTemporaryFile(dir=ROOT,suffix='.png',delete=False) as f:temp=Path(f.name)
    fig.savefig(temp,facecolor='white');plt.close(fig);temp.replace(png)
    data={'renderer':'Matplotlib','python':sys.version.split()[0],'matplotlib':matplotlib.__version__,
      'curve':'tan(x)','branches':[-1,0,1],'zeros_pi_units':[-1,0,1],
      'asymptotes_pi_units':[-1.5,-.5,.5,1.5],'bounds_pi_units':[-1.9,1.9],'y_bounds':[-5,5],
      'sha256':hashlib.sha256(png.read_bytes()).hexdigest()}
    with NamedTemporaryFile(dir=ROOT,suffix='.json',mode='w',delete=False) as f:json.dump(data,f,indent=2);tmp=Path(f.name)
    tmp.replace(side);return str(png)

# Observed masks change whole mathematical components, never short text globally.
# Each slot changes a false property or preserves an integer-period equality.
OBSERVED={
 'asym_sign_zero':('q-27638',{'false_set':'n\\pi '}),
 'asym_range_domain':('q-27660',{'range_half':r'\frac{π}{2}'}),
 'domain_zero_range':('q-103289',{'range_half':r'\frac{\pi }{4}'}),
 'asym_point_identity':('q-103295',{'false_set':r'2n\pi ', 'left_shift':r'-\frac{\pi }{6}','right_shift':r'+\frac{5\pi }{6}'}),
 'two_identities_asym':('q-28675',{'integer_shift':r'n\pi ', 'left_shift':r'-\frac{\pi }{2}','right_shift':r'+\frac{\pi }{2}'}),
 'asym_identity_range':('q-29608',{'integer_shift':r'2n\pi ', 'range':r'[-1,1]'})}
ANCHORS={name:dict(slots) for name,(_,slots) in OBSERVED.items()}
BOUNDS={
 'false_set':[r'n\pi ',r'2n\pi ',r'3n\pi '],
 'range_half':[r'\frac{\pi }{4}',r'\frac{\pi }{2}','1','2'],
 'range':[r'[-1,1]',r'[-2,2]',r'[-\pi,\pi]'],
 'integer_shift':[r'n\pi ',r'2n\pi ',r'3n\pi ']}

def observed_render(name,p,raw):
    qid,anchor=OBSERVED[name]; source=QUESTIONS[qid]
    if set(p)!=set(anchor):raise ValueError('Exact slot keys required')
    for k,v in p.items():
        if k in ['left_shift','right_shift']:continue
        allowed=BOUNDS[k]+[anchor[k]]
        if v not in allowed:raise ValueError(f'Invalid {k}: {v}')
    if 'left_shift' in p:
        valid=[(r'-\frac{\pi }{'+str(d)+'}',r'+\frac{'+('' if d==2 else str(d-1))+r'\pi }{'+str(d)+'}') for d in [2,3,4,6]]
        if (p['left_shift'],p['right_shift']) not in valid:raise ValueError('The two rational shifts must differ by pi')
    problem=source[':question/problem']; solution=source.get(':question/worked-solution')
    # Masks only affect prompt components except identity slots, which also occur
    # in each explicit source solution stage. The corrections of false properties
    # deliberately stay fixed because the underlying function remains tan x.
    for k,old in anchor.items():
        if k=='range_half':
            # Negative and positive bound occurrences are complete bound slots.
            problem='\n'.join(line.replace(old,p[k]) if 'range of the function' in line else line for line in problem.split('\n'))
        elif k=='integer_shift':
            # Restrict to tangent arguments; leave false asymptote claims unchanged.
            marker='x+'+old
            problem=problem.replace(marker,'x+'+p[k])
            if solution is not None:
                solution=solution.replace(marker,'x+'+p[k])
                if qid=='q-29608' and p[k]!=old:
                    coeff={'n\\pi ':1,'2n\\pi ':2,'3n\\pi ':3}[p[k]]
                    middle=r'x+n\pi +n\pi '
                    replacement=r'x+n\pi '+('' if coeff==1 else '+'+str(coeff-1)+r'n\pi ')
                    solution=solution.replace(middle,replacement)
        else:
            if k=='false_set':
                problem='\n'.join(line.replace(old,p[k]) if 'asymptote' in line else line for line in problem.split('\n'))
            else:problem=problem.replace(old,p[k])
            if k in ['left_shift','right_shift'] and solution is not None:solution=solution.replace(old,p[k])
    if not raw:
        if solution is None:
            solution="Let's plot the graph of $y=\\tan x.$\n\n![]("+graph()+")\n\nLet's go through each statement.\n\n- Statement I is true. The asymptotes occur at $x=\\frac{\\pi}{2}+n\\pi.$\n\n- Statement II is false. The range is $(-\\infty,\\infty).$\n\n- Statement III is false. The domain excludes $x=\\frac{\\pi}{2}+n\\pi.$\n\nSo, the correct answer is \"I only\"."
        else:
            import re
            solution=re.sub(r'!\[\]\(images/[^)]+\)',lambda m:'![]('+graph()+')',solution)
        # Semantic normalization of source Unicode function application only.
        problem=problem.replace(r'\operatorname{tan}⁡',r'\tan ').replace('tan⁡',r'\tan ')
        solution=solution.replace('tan⁡',r'\tan ')
        problem += '\n\nIn tangent equalities, consider values of $x$ where both sides are defined.' if 'shift' in str(anchor.keys()) else ''
    truths={'q-27638':[False,True,False],'q-27660':[True,False,False],
        'q-103289':[True,False,False],'q-103295':[False,True,True],
        'q-28675':[True,False,True],'q-29608':[False,True,False]}[qid]
    return problem,solution,truths,[a[':answer/value'] for a in source[':question/answer-fields'][0][':answer-field/choices']],qid

# Authored EASY: direct recognition of zeros, asymptotes, and range. Every item
# is a complete property, with no shifts, transformed curves, or evaluations.
# Authored MODERATE: domain exclusions + sign interval + period recognition.
# These require a global domain, one interval sign, and one repeat-distance fact.
FACTS={
 'zero':[
 ('The zeros of the function are exactly $x=n\\pi.$',True,'zero:npi'),
 ('The zeros of the function are exactly $x=\\frac{\\pi}{2}+n\\pi.$',False,'zero:half+n'),
 ('The zeros of the function are exactly $x=2n\\pi.$',False,'zero:2n'),
 ('The zeros of the function are exactly $x=\\frac{\\pi}{4}+n\\pi.$',False,'zero:quarter+n')],
 'asym':[
 ('The vertical asymptotes are exactly $x=\\frac{\\pi}{2}+n\\pi.$',True,'asym:half+n'),
 ('The vertical asymptotes are exactly $x=n\\pi.$',False,'asym:n'),
 ('The vertical asymptotes are exactly $x=2n\\pi.$',False,'asym:2n'),
 ('The vertical asymptotes are exactly $x=\\frac{\\pi}{2}+2n\\pi.$',False,'asym:half+2n')],
 'range':[
 ('The range of the function is $(-\\infty,\\infty).$',True,'range:R'),
 ('The range of the function is $[-1,1].$',False,'range:closed1'),
 ('The range of the function is $(-\\frac{\\pi}{2},\\frac{\\pi}{2}).$',False,'range:openhalfpi'),
 ('The range of the function is $(0,\\infty).$',False,'range:positive')],
 'domain':[
 ('The domain is all real numbers except $x=\\frac{\\pi}{2}+n\\pi.$',True,'domain:half+n'),
 ('The domain is all real numbers except $x=n\\pi.$',False,'domain:n'),
 ('The domain is all real numbers.',False,'domain:R'),
 ('The domain is $(-\\frac{\\pi}{2},\\frac{\\pi}{2}).$',False,'domain:onebranch')],
 'sign':[
 ('The function is positive throughout $(n\\pi,\\frac{\\pi}{2}+n\\pi).$',True,'sign:positive-right'),
 ('The function is negative throughout $(-\\frac{\\pi}{2}+n\\pi,n\\pi).$',True,'sign:negative-left'),
 ('The function is negative throughout $(n\\pi,\\frac{\\pi}{2}+n\\pi).$',False,'sign:negative-right'),
 ('The function is positive throughout $(-\\frac{\\pi}{2}+n\\pi,n\\pi).$',False,'sign:positive-left')],
 'period':[
 ('The least positive period is $\\pi.$',True,'period:pi'),
 ('The least positive period is $2\\pi.$',False,'period:2pi'),
 ('The least positive period is $\\frac{\\pi}{2}.$',False,'period:halfpi'),
 ('The function has no positive period.',False,'period:none')]
}
EXPLAIN={
 'zero':r'The zeros occur at $x=0,\pm\pi,\pm2\pi,\ldots,$ which can be written as $x=n\pi.$',
 'asym':r'The function has an asymptote at $x=\frac{\pi}{2}$ and the period is $\pi.$ Therefore, the asymptotes occur at $x=\frac{\pi}{2}+n\pi.$',
 'range':r'The function takes values on all the real numbers, hence the range is $(-\infty,\infty).$',
 'domain':r'The function is defined everywhere except where $x=\frac{\pi}{2}+n\pi.$',
 'sign':r'The function is positive on $(0,\frac{\pi}{2})$ and negative on $(-\frac{\pi}{2},0).$ The period is $\pi,$ so these signs repeat after each integer multiple of $\pi.$',
 'period':r'The graph repeats after a horizontal shift of $\pi,$ and no smaller positive shift repeats the whole graph. Therefore, the least positive period is $\pi.$'}

def catalogs(level):
    if level not in ['easy','moderate']:raise ValueError(level)
    cats=['zero','asym','range'] if level=='easy' else ['domain','sign','period']
    return [dict(indices=list(ix)) for ix in itertools.product(range(4),repeat=3)
            if 0<sum(FACTS[c][i][1] for c,i in zip(cats,ix))<3]

def authored_render(level,p):
    if set(p)!={'indices'} or len(p['indices'])!=3 or any(type(i)!=int or not 0<=i<4 for i in p['indices']):raise ValueError('indices must be three catalog indices')
    cats=['zero','asym','range'] if level=='easy' else ['domain','sign','period']
    facts=[FACTS[c][i] for c,i in zip(cats,p['indices'])];truth=[f[1] for f in facts]
    if sum(truth) not in [1,2]:raise ValueError('Exactly one or two statements must be true')
    problem="Which of the following statements are true regarding the function $y=\\tan x?$ Assume that $n$ is an integer.\n\n"+'\n\n'.join('- '+f[0] for f in facts)
    solution="Let's plot the graph of $y=\\tan x.$\n\n![]("+graph()+")\n\nLet's go through each statement.\n\n"+'\n\n'.join('- Statement '+ROMAN[i]+' is '+str(t).lower()+'. '+EXPLAIN[c] for i,(t,c) in enumerate(zip(truth,cats)))+'\n\nSo, the correct answer is "'+label(truth)+'".'
    correct=label(truth)
    # Eligible complete five-subset bank: correct subset plus four other
    # combinations. Choice operations are inclusion/omission of statements.
    bank=[s for s in SUBSETS if s!='II and III only']
    if correct not in bank:bank=[s for s in SUBSETS if s!='I and II only']
    return problem,solution,truth,bank,[f[2] for f in facts]

# Authored hard extension of q-28675: two identity judgements plus one
# direct property. Shift differences use familiar halves/quarters/sixths;
# noninteger period claims change truth, without numeric tangent evaluation.
def hard_catalog():
    result=[]
    for c,d,gap,k,i in itertools.product(['1','2','3','1/2'],[2,3,4,6],['1','2','1/2'],['asym','range','domain'],range(4)):
        ts=[sp.Rational(c).is_integer,sp.Rational(gap).is_integer,FACTS[k][i][1]]
        if sum(ts) in [1,2]:result.append({'integer_coefficient':c,'denominator':d,'gap':gap,'property':k,'index':i})
    return result

def shift_tex(coefficient):
    e=sp.Rational(coefficient)*sp.pi
    if e==0:return ''
    return ('+' if e>0 else '')+sp.latex(e)

def hard_render(p):
    if p not in hard_catalog():raise ValueError('Outside hard workload catalog')
    c=sp.Rational(p['integer_coefficient']);d=p['denominator'];gap=sp.Rational(p['gap']);k=p['property'];i=p['index']
    coefficient_tex='' if c==1 else sp.latex(c)
    first=r'\tan(x+\pi)=\tan(x+'+coefficient_tex+r'n\pi).'
    left=-sp.Rational(1,d);right=left+gap
    second=r'\tan(x'+shift_tex(left)+r')=\tan(x'+shift_tex(right)+r').'
    facts=[('$'+first+'$',bool(c.is_integer)),('$'+second+'$',bool(gap.is_integer)),FACTS[k][i][:2]]
    truths=[f[1] for f in facts]
    prompt="Which of the following statements are true regarding the function $y=\\tan x?$ Assume that $n$ represents any integer.\n\n"+'\n\n'.join('- '+f[0] for f in facts)+ '\n\nIn tangent equalities, consider values of $x$ where both sides are defined.'
    first_reason=(r'The function $y=\tan x$ has period $\pi.$ So, $\tan(x+\pi)=\tan(x)=\tan(x+'+coefficient_tex+r'n\pi)$ for any integer $n.$') if c.is_integer else r'The period is $\pi.$ A shift of $\frac{n\pi}{2}$ is not always an integer multiple of $\pi$ because $n$ may be odd. Thus, this identity does not hold for every integer $n.$'
    second_reason=r'The function $y=\tan x$ has period $\pi.$ The two arguments differ by $'+sp.latex(gap*sp.pi)+r',$ which is '+(r'an integer multiple of $\pi.$ Therefore, the equality holds wherever both sides are defined.' if gap.is_integer else r'not an integer multiple of $\pi.$ Therefore, the equality is false.')
    if gap.is_integer:
        second_reason += r' So, $\tan(x'+shift_tex(left)+r')=\tan(x'+shift_tex(left)+shift_tex(gap)+r')=\tan(x'+shift_tex(right)+r').$'
    solution="Let's recall the graph of $y=\\tan x.$\n\n![]("+graph()+")\n\nLet's examine each statement.\n\n"+'\n\n'.join('- Statement '+ROMAN[j]+' is '+str(f[1]).lower()+'. '+reason for j,(f,reason) in enumerate(zip(facts,[first_reason,second_reason,EXPLAIN[k]])))
    bank=[s for s in SUBSETS if s!='II and III only']
    if g_label:=label(truths):
        if g_label not in bank:bank=[s for s in SUBSETS if s!='I and II only']
    return prompt,solution,truths,bank,{'first_coefficient':str(c),'left':str(left),'right':str(right),'property':FACTS[k][i][2]}

def source_parameters(name,rng):
    p=dict(ANCHORS[name])
    for k in p:
        if k not in ['left_shift','right_shift']:p[k]=rng.choice(BOUNDS[k])
    if 'left_shift' in p:
        d=rng.choice([2,3,4,6]);p['left_shift']=r'-\frac{\pi }{'+str(d)+'}';p['right_shift']=r'+\frac{'+('' if d==2 else str(d-1))+r'\pi }{'+str(d)+'}'
    return p

# HARD: observed three-property classifications and one/two explicit periodic
# identities. Defaults serve all six source-shaped families, including the
# completed unrated family. No numeric tangent-value evaluation (sibling KP).
def generate_legacy(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError('Unknown difficulty')
    if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('Only radio is supported')
    rng=random.Random(seed)
    if profile and profile.startswith('observed:'):
        chosen=profile.split(':',1)[1]
        if chosen not in OBSERVED:raise ValueError('Unknown observed profile')
        if template not in [None,chosen]:raise ValueError('Profile/template mismatch')
        template=chosen
    template=template or (rng.choice(list(OBSERVED)+['two_identity_properties']) if level=='hard' else 'basic_properties' if level=='easy' else 'domain_sign_period')
    if template in OBSERVED:
        if level!='hard':raise ValueError('Observed templates have hard assignment')
        if profile not in [None,'completed','observed:'+template]:raise ValueError('Unknown profile')
        raw=profile=='observed:'+template
        p=dict(parameters) if parameters is not None else source_parameters(template,rng)
        prompt,solution,truth,bank,qid=observed_render(template,p,raw)
        observed=QUESTIONS[qid]; missing=qid=='q-27660' and raw
        semantic={'template':template,'slots':p,'truth':truth}
        refs=[qid]; origin='observed-template'; evidence_only=missing
    elif template=='two_identity_properties':
        if level!='hard' or profile not in [None,'authored-subsets']:raise ValueError('Hard identity template/profile required')
        raw=False;missing=False;p=dict(parameters) if parameters is not None else rng.choice(hard_catalog())
        prompt,solution,truth,bank,semantic=hard_render(p);refs=['q-28675'];origin='authored-observed-family-extension';evidence_only=False
    else:
        expected='basic_properties' if level=='easy' else 'domain_sign_period' if level=='moderate' else None
        if template!=expected:raise ValueError('Template outside this difficulty')
        if profile not in [None,'authored-subsets']:raise ValueError('Unknown profile')
        raw=False;missing=False;p=dict(parameters) if parameters is not None else rng.choice(catalogs(level))
        prompt,solution,truth,bank,semantic=authored_render(level,p);refs=[];origin='authored-missing-level';evidence_only=False
    actual_profile=profile or ('completed' if template in OBSERVED else 'authored-subsets')
    # Normalize equivalent TeX spellings/whitespace; retain actual asserted
    # property sets, identity arguments, and assessed response criterion.
    def normalized(value):
        if isinstance(value,dict):return {k:normalized(v) for k,v in value.items()}
        if isinstance(value,list):return [normalized(v) for v in value]
        if isinstance(value,str):return value.replace('π',r'\pi').replace(' ','')
        return value
    mathematical_fingerprint=digest(normalized(semantic))
    content=digest({'version':VERSION,'level':None if missing else level,'prompt':prompt,'solution':solution,'bank':sorted(bank),'correct':None if missing else label(truth)})
    q_uuid=uid(content);f_uuid=uid(content+':selection')
    answers=[{':answer/id':uid(f_uuid+':'+v),':answer/type':':answer.type/text',':answer/value':v} for v in bank]
    rng.shuffle(answers)
    field={':answer-field/id':f_uuid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if not missing:field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==label(truth))]
    q={':question/id':q_uuid,':question/problem':prompt,':question/answer-fields':[field]}
    if not missing:q[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:q[':question/worked-solution']=solution
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
      'generation':{'version':VERSION,'seed':seed,'level':level,'template':template,'profile':actual_profile,'parameters':p,
        'mathematical_fingerprint':mathematical_fingerprint,'content_identity':content,
        'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'source_questions':refs,
        'origin':origin,'evidence_only':evidence_only,'eligible_for_learning':not evidence_only,
        'domain':'Untransformed tangent; n is an integer. Equalities hold on their common domain.',
        'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Current three-field checkbox format; legacy radio profiles are evidence only."""
    if profile and profile.startswith('observed:'):
        return generate_legacy(level,seed,template,field_type,parameters,profile)
    if field_type not in [None,'checkbox',':answer-field.type/checkbox']:
        raise ValueError('Current format requires three Boolean checkbox fields')
    current_replay=bool(profile and profile.startswith('current:'))
    if current_replay:
        template=profile.split(':',1)[1]
        base=generate_legacy(level,seed,template,parameters=parameters,profile='observed:'+template)
    else:
        base=generate_legacy(level,seed,template,parameters=parameters,profile=profile)
    q=base['question'];meta=base['generation'];rows=[]
    import re
    for line in q[':question/problem'].splitlines():
        match=re.match(r'^(?:- |[123]\. |I{1,3}\. )(.*)$',line)
        if match:rows.append(match[1])
    if len(rows)!=3:raise ValueError('Three claims required')
    header=q[':question/problem'].split('\n\n',1)[0]
    # Current source migration puts the common-domain convention after the claims.
    convention='\n\nIn tangent equalities, consider values of $x$ where both sides are defined.' if 'In tangent equalities' in q[':question/problem'] else ''
    separator='\n\n' if meta['template'] in ('domain_zero_range','asym_identity_range') else '\n'
    q[':question/problem']=header+'\n\nSelect all that apply.\n\n'+separator.join('- **'+ROMAN[i]+'.** '+row for i,row in enumerate(rows))+convention
    radio=q[':question/answer-fields'][0]
    if current_replay:
        current=json.loads((ROOT/'current-source.json').read_text())['record']
        source=next(z for z in current[':knowledge-point/questions'] if z[':question/math-academy-id']==OBSERVED[template][0])
        truths=[next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][':answer/id'])=='true' for f in sorted(source[':question/answer-fields'],key=lambda f:ROMAN.index(f[':answer-field/key']))]
        if template=='asym_range_domain':q[':question/worked-solution']=source[':question/worked-solution']
        if ':question/difficulty' not in source:q.pop(':question/difficulty',None)
        meta['profile']='current:'+template
        meta['evidence_only']=':question/difficulty' not in source
        meta['eligible_for_learning']=not meta['evidence_only']
    else:
        correct=next(a[':answer/value'] for a in radio[':answer-field/choices'] if a[':answer/id']==radio[':answer-field/correct'][1])
        truths=[name in re.findall(r'\bI{1,3}\b',correct) for name in ROMAN]
    identity=digest({'version':VERSION,'question':q[':question/problem'],'solution':q.get(':question/worked-solution'),'level':q.get(':question/difficulty'),'truth':truths,'field_type':'checkbox'})
    q[':question/id']=uid(identity);fields=[]
    for name,t in zip(ROMAN,truths):
        field_id=uid(identity+':'+name)
        answers=[{':answer/id':uid(field_id+':'+value),':answer/type':':answer.type/text',':answer/value':value} for value in ['false','true']]
        fields.append({':answer-field/id':field_id,':answer-field/key':name,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==str(t).lower())]})
    q[':question/answer-fields']=fields;meta['content_identity']=identity;meta['truth_vector']=truths;meta['field_type']='checkbox'
    meta['current_source_basis']=json.loads((ROOT/'current-source.json').read_text())['basis']
    return base

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+q.get(':question/worked-solution','[Source worked solution absent.]')

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_legacy', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
