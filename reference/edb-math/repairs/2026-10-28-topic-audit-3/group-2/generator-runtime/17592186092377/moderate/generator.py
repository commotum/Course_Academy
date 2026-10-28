#!/usr/bin/env python3
"""Seeded, relocatable exact parametric arc-length practice. No database access."""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
from math_format import normalize_prose,normalize_tex,validate_generated_record
HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/'source-data.json').read_text())
KP=SOURCE['kp']; KP_ID=KP[':db/id']; PI=sp.pi; T=sp.symbols('t',real=True)
VERSION='arc-length-package-v4'
def group(text,start):
 assert text[start]=='{'
 depth=1;i=start+1
 while depth:
  if text[i]=='{':depth+=1
  if text[i]=='}':depth-=1
  i+=1
 return text[start+1:i-1],i

def parse_tex(text):
 """Small independent TeX subset parser for source stages and scalar options."""
 text=text.strip().rstrip('.,')
 text=text.replace('⁡','').replace('\\,','').replace('\\!','').replace('\\cdot','*').replace('\\left','').replace('\\right','')
 text=re.sub(r'\\operatorname\{(sin|cos)\}',r'\1',text)
 text=text.replace('{sin}','sin').replace('{cos}','cos').replace('{e}','e')
 text=text.replace('\\sin','sin').replace('\\cos','cos').replace('\\pi','pi')
 for command in ('frac','dfrac','sqrt'):
  while '\\'+command in text:
   start=text.index('\\'+command);pos=start+len(command)+1
   a,end=group(text,pos)
   if command!='sqrt':b,end=group(text,end);value='(('+str(parse_tex(a))+')/('+str(parse_tex(b))+'))'
   else:value='sqrt('+str(parse_tex(a))+')'
   text=text[:start]+value+text[end:]
 # Trig powers in source shorthand: sin^{2}(...) / sin^{2}t.
 text=re.sub(r'(sin|cos)\^\{(\d+)\}t',r'\1(t)^\2',text)
 text=re.sub(r'(sin|cos)t',r'\1(t)',text)
 while True:
  m=re.search(r'(sin|cos)\^\{(\d+)\}\(',text)
  if not m:break
  start=m.end()-1;depth=1;end=start+1
  while depth:
   if text[end]=='(':depth+=1
   if text[end]==')':depth-=1
   end+=1
  text=text[:m.start()]+m.group(1)+'('+text[start+1:end-1]+')^'+m.group(2)+text[end:]
 text=text.replace('{','(').replace('}',')').replace('|','')
 text=re.sub(r'([0-9a-z)])(sin|cos|sqrt)\(',r'\1*\2(',text)
 text=re.sub(r'(sin|cos)0',r'\1(0)',text)
 text=re.sub(r'(sin|cos)pi',r'\1(pi)',text)
 return parse_expr(text,local_dict={'t':T,'pi':PI,'e':sp.E,'sin':sp.sin,'cos':sp.cos,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor),evaluate=True)

def tex(value):return sp.latex(sp.simplify(value)).replace('e^{','{e}^{')
def equivalent(a,b):return sp.simplify(sp.trigsimp(a-b))==0

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'kp:'+str(KP_ID)+':'+v))

# EASY: constant speed, nonnegative linear speed, and an elementary power rule.
# MODERATE: cubic trig factoring, exponential product derivatives, and radical
# power integration. HARD: trig differences and half-angle speed simplification.
# Entries are source IDs, x(t), y(t), source lower/upper, positive speed, family.
SPECS={
'q-123039':(2*sp.sin(T)-2*T,-2*sp.cos(T),0,PI,4*sp.sin(T/2),'cycloid'),
'q-10255':(T-sp.sin(T),1-sp.cos(T),0,PI,2*sp.sin(T/2),'cycloid'),
'q-10260':(1+3*T,2*T**sp.Rational(3,2),0,1,3*sp.sqrt(1+T),'power'),
'q-10256':(sp.sin(T)**3,sp.cos(T)**3,0,PI/2,3*sp.sin(T)*sp.cos(T),'astroid'),
'q-10257':(2*sp.cos(T)**3,2*sp.sin(T)**3,0,PI/2,6*sp.sin(T)*sp.cos(T),'astroid'),
'q-10258':(2*(sp.sin(T)-T*sp.cos(T)),2*(sp.cos(T)+T*sp.sin(T)),0,PI,2*T,'involute'),
'q-10261':(2*sp.cos(T)-sp.cos(2*T),2*sp.sin(T)-sp.sin(2*T),0,PI,4*sp.sin(T/2),'epicycle'),
'q-20907':(4*sp.sin(T)+5,4*(sp.cos(T)+1),0,PI/2,sp.Integer(4),'circle'),
'q-348086':(sp.sin(T)-T*sp.cos(T),-sp.cos(T)-T*sp.sin(T),0,PI,T,'involute'),
'q-348088':(sp.cos(T)+T*sp.sin(T),sp.sin(T)-T*sp.cos(T),0,2*PI,T,'involute'),
'q-351427':(3*sp.sin(T)+2,3*sp.cos(T)-4,0,PI/3,sp.Integer(3),'circle'),
'q-351428':(5*sp.sin(T)-3,5*sp.cos(T)+1,PI/5,PI/2,sp.Integer(5),'circle'),
'q-351429':(T**2/2,(2*T+1)**sp.Rational(3,2)/3,0,2,T+1,'linear'),
'q-351438':(sp.exp(2*T)*sp.cos(T),sp.exp(2*T)*sp.sin(T),0,PI/2,sp.sqrt(5)*sp.exp(2*T),'spiral'),
'q-351439':(4*sp.cos(T)**3,4*sp.sin(T)**3,0,PI/4,12*sp.sin(T)*sp.cos(T),'astroid'),
'q-351471':(3*sp.cos(T)-sp.cos(3*T),3*sp.sin(T)-sp.sin(3*T),0,PI,6*sp.sin(T),'epicycle3'),
'q-351474':((6*T+1)**sp.Rational(3,2)/9,3*T**2/2,0,1,3*T+1,'linear'),
'q-351505':(T-T**3/3,T**2,0,3,1+T**2,'polynomial'),
'q-351508':(2+4*T,8*T**sp.Rational(3,2)/3,0,2,4*sp.sqrt(1+T),'power'),
}

TEMPLATES={}
for q in KP[':knowledge-point/questions']:
    key=q[':question/math-academy-id']
    x,y,a,b,v,family=SPECS[key]
    x,y,a,b,v=map(sp.sympify,(x,y,a,b,v))
    field=q[':question/answer-fields'][0]
    TEMPLATES[key]=dict(source=q,x=x,y=y,a=a,b=b,speed=v,family=family,
        level=q[':question/difficulty'][':db/ident'].split('/')[-1],
        kind=field[':answer-field/type'][':db/ident'].split('/')[-1])

# These intervals avoid sign crossings and use the source's familiar endpoint work.
def intervals(family):
    if family=='circle':
        return [(a,a+b) for a in (sp.Integer(0),PI/6,PI/4) for b in (PI/6,PI/4,PI/3,PI/2,PI)]
    if family=='involute':
        return [(a,b) for a in (sp.Integer(0),PI/6,PI/2) for b in (PI/2,PI,3*PI/2,2*PI) if a<b]
    if family=='astroid':
        return [(a,b) for a in (sp.Integer(0),PI/6,PI/4) for b in (PI/6,PI/4,PI/3,PI/2) if a<b]
    if family in ('cycloid','epicycle'):
        return [(a,b) for a in (sp.Integer(0),PI/3) for b in (PI/2,2*PI/3,PI) if a<b]
    if family=='epicycle3':
        return [(a,b) for a in (sp.Integer(0),PI/6,PI/2) for b in (PI/3,PI/2,2*PI/3,PI) if a<b]
    if family=='spiral':
        return [(sp.Integer(0),b) for b in (PI/6,PI/4,PI/3,PI/2)]
    return [(sp.Integer(a),sp.Integer(b)) for a,b in ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))]


def instance(key,a=None,b=None,scale=1):
    d=TEMPLATES[key].copy()
    a=d['a'] if a is None else sp.sympify(a)
    b=d['b'] if b is None else sp.sympify(b)
    scale=sp.sympify(scale)
    if scale not in (1,2,3,4): raise ValueError('Scale must be 1, 2, 3 or 4')
    limit=PI/2 if d['family']=='astroid' else PI if d['family'] in ('cycloid','epicycle','epicycle3') else 2*PI if d['family'] in ('circle','involute') else PI/2 if d['family']=='spiral' else 4
    if not (a>=0 and b>a and b<=limit): raise ValueError('Interval leaves the source sign domain')
    for k in ('x','y','speed'): d[k]=scale*d[k]
    d.update(key=key,a=a,b=b,scale=scale)
    d['dx'],d['dy']=[sp.diff(d[k],T) for k in ('x','y')]
    d['primitive']=primitive(d)
    d['length']=sp.simplify(d['primitive'].subs(T,b)-d['primitive'].subs(T,a))
    d['answer']=sp.exp(2*b)-sp.exp(2*a) if key=='q-351438' else d['length']
    return d


def primitive(d):
    v=d['speed']; f=d['family']
    if f=='astroid': return -sp.simplify(v/(sp.sin(T)*sp.cos(T)))*sp.cos(2*T)/4
    if f in ('cycloid','epicycle'): return -2*sp.simplify(v/sp.sin(T/2))*sp.cos(T/2)
    if f=='epicycle3': return -sp.simplify(v/sp.sin(T))*sp.cos(T)
    if f=='spiral': return sp.simplify(v/sp.exp(2*T))*sp.exp(2*T)/2
    return sp.integrate(v,T)


def display(expr):
    # Do not use simplify here: retain the learner's operator inputs and final form.
    return normalize_tex(sp.latex(expr))


def block(rows): return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'


def solution(d):
    x,y,dx,dy,v,F,a,b=[d[k] for k in ('x','y','dx','dy','speed','primitive','a','b')]
    f=d['family']; c=d['scale']; lines=[]
    lines.append('The arc length is the integral of the nonnegative speed:\n\n'+
      '$$\n'+rf'L=\int_{{{display(a)}}}^{{{display(b)}}}\sqrt{{(x\prime(t))^2+(y\prime(t))^2}}\,\mathrm{{d}}t.'+'\n$$')
    # Differentiation is shown before any norm simplification.
    rows=[rf'x\prime(t)&=\frac{{\mathrm{{d}}}}{{\mathrm{{d}}t}}\left({display(x)}\right)',
          rf'&={display(dx)}',
          rf'y\prime(t)&=\frac{{\mathrm{{d}}}}{{\mathrm{{d}}t}}\left({display(y)}\right)',
          rf'&={display(dy)}']
    lines.append('Differentiate both coordinates'+(' using the product rule; the opposite cross terms cancel' if f=='involute' else ' using the product rule' if f=='spiral' else '')+':\n\n'+block(rows))
    raw=rf'\left({display(dx)}\right)^2+\left({display(dy)}\right)^2'
    rows=[rf'(x\prime)^2+(y\prime)^2&=\left({display(dx)}\right)^2',
          rf'&\quad+\left({display(dy)}\right)^2']
    if f=='circle':
        r=v;rows.extend([rf'&={display(r**2)}(\cos^2 t+\sin^2 t)',rf'&={display(r**2)}'])
    elif f=='involute':
        k=sp.simplify(v/T);rows.extend([rf'&={display(k**2)}t^2(\sin^2 t+\cos^2 t)',rf'&={display(v**2)}'])
    elif f=='astroid':
        k=sp.simplify(v/(sp.sin(T)*sp.cos(T)));rows.extend([
            rf'&={display(k**2)}\sin^2 t\cos^2 t(\sin^2 t+\cos^2 t)',
            rf'&={display(k**2)}\sin^2 t\cos^2 t'])
    elif f=='spiral':
        rows.extend([rf'&={display(c**2)}e^{{4t}}(2\cos t-\sin t)^2',
                     rf'&\quad+{display(c**2)}e^{{4t}}(2\sin t+\cos t)^2',
                     rf'&={display(5*c**2)}e^{{4t}}(\sin^2 t+\cos^2 t)',rf'&={display(v**2)}'])
    elif f in ('cycloid','epicycle','epicycle3'):
        k=sp.simplify(v/(sp.sin(T) if f=='epicycle3' else sp.sin(T/2)))
        freq=2 if f=='epicycle3' else 1
        if f.startswith('epicycle'):
            coeff=k**2/2
            rows.append(rf'&={display(coeff)}\left(1-\cos({freq+1}t)\cos t-\sin({freq+1}t)\sin t\right)')
        rows.extend([rf'&={display(k**2/2)}\left(1-\cos({display(freq*T)})\right)',
                     rf'&={display(k**2)}\sin^2\left({display(freq*T/2)}\right)'])
    else:
        rows.extend([rf'&={display(sp.expand(dx**2+dy**2))}',rf'&=\left({display(v)}\right)^2'])
    lines.append(('Use the cosine-difference identity, then '+r'$1-\cos(2z)=2\sin^2 z$' if f.startswith('epicycle') else 'Expand the squares and cancel the opposite cross terms' if f=='spiral' else 'Simplify the sum of squares')+':\n\n'+block(rows))
    if f in ('cycloid','epicycle','epicycle3'):
        z=T if f=='epicycle3' else T/2
        sign=rf'$\sin({display(z)})\geq0$'
    elif f=='astroid': sign=r'$\sin t\geq0$ and $\cos t\geq0$'
    else: sign=rf'${display(v)}\geq0$'
    lines.append('On the stated interval, '+sign+', so taking the square root gives\n\n'+
                 '$$\n'+rf'v(t)=\sqrt{{(x\prime)^2+(y\prime)^2}}={display(v)}.'+'\n$$')
    if f=='astroid':
        k=sp.simplify(v/(sp.sin(T)*sp.cos(T)))
        lines.append(r'Use $\sin t\cos t=\frac12\sin(2t)$ to integrate:'+'\n\n'+
            block([rf'\int {display(v)}\,\mathrm{{d}}t&={display(k/2)}\int\sin(2t)\,\mathrm{{d}}t',rf'&={display(F)}+C']))
    elif f in ('cycloid','epicycle','epicycle3','spiral'):
        lines.append('Integrating, including the constant chain-rule factor, gives\n\n'+
            '$$\n'+rf'\int {display(v)}\,\mathrm{{d}}t={display(F)}+C.'+'\n$$')
    else:
        lines.append('Integrating the speed gives\n\n'+'$$\n'+rf'\int {display(v)}\,\mathrm{{d}}t={display(F)}+C.'+'\n$$')
    rows=[rf'L&=\int_{{{display(a)}}}^{{{display(b)}}}{display(v)}\,\mathrm{{d}}t',
          rf'&=\left[{display(F)}\right]_{{{display(a)}}}^{{{display(b)}}}',
          rf'&=\left({display(F.subs(T,b))}\right)-\left({display(F.subs(T,a))}\right)',
          rf'&={display(d["length"])}']
    lines.append('Evaluate at both endpoints and subtract:\n\n'+block(rows))
    if d['key']=='q-351438':
        coeff=c*sp.sqrt(5)/2
        lines.append('In the supplied factored form,\n\n'+
            '$$\n'+rf'L={display(coeff)}\left({display(d["answer"])}\right),'+ '\n$$\n\n'+
            'so the requested entry is $'+display(d['answer'])+'$.')
    return normalize_prose('\n\n'.join(lines))


def authored_bank(d,rng):
    """Choose a complete operation profile, then reject collisions as a whole."""
    L=d['length']; a,b=d['a'],d['b'];v=d['speed'];dx,dy=d['dx'],d['dy']
    sq=sp.integrate(sp.expand_trig(v*v),(T,a,b))
    chord=sp.sqrt((d['x'].subs(T,b)-d['x'].subs(T,a))**2+(d['y'].subs(T,b)-d['y'].subs(T,a))**2)
    # Each profile is an explicit set of four error operations, not a first-valid pool.
    # Halving/doubling arise from losing/duplicating the squared-component factor.
    operations={
      'half_factor':L/2,'double_factor':2*L,'square_root_omitted':sq,
      'upper_rectangle':v.subs(T,b)*(b-a),'lower_rectangle':v.subs(T,a)*(b-a),
      'chord_instead_of_arc':chord,'power_divisor_twice':L/3,
      'x_displacement':sp.Abs(d['x'].subs(T,b)-d['x'].subs(T,a)),
      'y_displacement':sp.Abs(d['y'].subs(T,b)-d['y'].subs(T,a)),
      'omit_common_scale':L/d['scale'],
      'endpoint_subtraction_reversed':-L,
    }
    profiles=[('half_factor','double_factor','square_root_omitted','upper_rectangle'),
              ('half_factor','chord_instead_of_arc','double_factor','square_root_omitted'),
              ('x_displacement','y_displacement','chord_instead_of_arc','square_root_omitted'),
              ('half_factor','double_factor','chord_instead_of_arc','omit_common_scale'),
              ('double_factor','square_root_omitted','upper_rectangle','chord_instead_of_arc'),
              ('half_factor','chord_instead_of_arc','x_displacement','y_displacement')]
    profile=rng.choice(profiles)
    values=[('correct',d['answer'])]+[(k,sp.simplify(operations[k])) for k in profile]
    if any(not val.is_real or val<0 for _,val in values): raise ValueError('Invalid bank value')
    if any(equivalent(x[1],y[1]) for i,x in enumerate(values) for y in values[i+1:]):
        raise ValueError('Complete bank collision')
    return values,'authored:'+','.join(profile)


def plot(d,identity):
    source=d['source'][':question/problem']
    if '![](' not in source:return None
    output=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not output:raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR for generated assets')
    out=Path(output).resolve();out.mkdir(parents=True,exist_ok=True)
    path=out/(identity+'.png')
    if path.exists():return str(path)
    os.environ.setdefault('MPLCONFIGDIR',str(out/'mpl-cache'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    a,b=float(d['a']),float(d['b']);h=b-a
    fx=sp.lambdify(T,d['x'],'math');fy=sp.lambdify(T,d['y'],'math')
    ts=[a+h*i/400 for i in range(401)]
    context=[max(0,a-h/8)+(b+h/8-max(0,a-h/8))*i/450 for i in range(451)]
    xs,ys=[fx(t) for t in ts],[fy(t) for t in ts]
    fig,ax=plt.subplots(figsize=(5.4,4.2))
    ax.plot([fx(t) for t in context],[fy(t) for t in context],':',color='#8cb7df',lw=1)
    ax.plot(xs,ys,color='#2475c7',lw=2.2)
    ax.annotate('',xy=(xs[215],ys[215]),xytext=(xs[195],ys[195]),arrowprops=dict(arrowstyle='->',color='#2475c7',lw=1.5))
    ax.scatter([xs[0],xs[-1]],[ys[0],ys[-1]],s=22,color='#2475c7',zorder=3)
    for i,val in ((0,d['a']),(-1,d['b'])):
        ax.annotate('$t='+display(val)+'$',(xs[i],ys[i]),xytext=(8,12 if i==0 else -18),textcoords='offset points',fontsize=10)
    ax.axhline(0,color='black',lw=.6);ax.axvline(0,color='black',lw=.6)
    ax.set_xlabel('$x$');ax.set_ylabel('$y$',rotation=0);ax.margins(.22);ax.set_aspect('equal',adjustable='datalim')
    fig.tight_layout();fig.savefig(path,dpi=115);plt.close(fig)
    return str(path)


def generate(level,seed=0,template=None,parameters=None,replay=False):
    rng=random.Random(seed)
    eligible=[k for k,d in TEMPLATES.items() if d['level']==level]
    if template is None:
        template=rng.choice(eligible)
    if template not in eligible:raise ValueError('Template incompatible with level')
    d0=TEMPLATES[template]
    if replay:
        if parameters is not None:raise ValueError('Replay uses original parameters')
        d=instance(template)
        f0=d0['source'][':question/answer-fields'][0]
        values=[]
        for choice in f0[':answer-field/choices']:
            value=parse_tex(choice[':answer/value'].replace('\\\\','\\'))
            values.append(('correct' if choice[':answer/id']==f0[':answer-field/correct'][':answer/id'] else 'observed',value))
        assert equivalent(next(v for k,v in values if k=='correct'),d['answer'])
        profile='observed-original-parameters'
    else:
        for attempt in range(150):
            if parameters is None:
                a,b=rng.choice(intervals(d0['family']));scale=rng.choice((1,2,3,4))
            else:
                a=sp.sympify(parameters.get('lower',d0['a']),locals={'pi':PI})
                b=sp.sympify(parameters.get('upper',d0['b']),locals={'pi':PI});scale=parameters.get('scale',1)
            d=instance(template,a,b,scale)
            if d0['kind']=='blank':values=[('correct',d['answer'])];profile='source-blank-shape';break
            try:values,profile=authored_bank(d,rng);break
            except ValueError:
                # Explicit parameters are fixed; retry another complete bank.
                pass
        else:raise ValueError('No distinct plausible complete bank')
    f0=d0['source'][':question/answer-fields'][0];kind=d0['kind'];key=f0[':answer-field/key']
    prompt='Find the exact arc length of the curve defined parametrically as\n\n'+block([
        rf'x&={display(d["x"])}',rf'y&={display(d["y"])}',
        rf't&\in\left[{display(d["a"])},{display(d["b"])}\right].'])
    if replay:
        prompt=d0['source'][':question/problem']
    elif kind=='blank':
        prompt+='\n\n'+('$L='+display(d['scale']*sp.sqrt(5)/2)+'(${{'+key+'}}$)$' if template=='q-351438' else '$L=$\n{{'+key+'}}')
    prompt=normalize_prose(prompt);sol=solution(d)
    identity=digest(dict(prompt=re.sub(r'!\[\]\(.*?\)','[source-plot]',prompt),solution=sol,bank=sorted(display(v) for _,v in values)))
    asset=re.search(r'!\[\]\((.*?)\)',prompt).group(1) if replay and '![](' in prompt else None
    if not replay:asset=plot(d,identity)
    if asset and not replay:prompt='![]('+asset+')\n\n'+prompt
    qid=uid(identity);fid=uid(qid+':field')
    answers=[{':answer/id':uid(fid+':'+display(v)),':answer/type':':answer.type/math',':answer/value':display(v)} for _,v in values]
    correct=answers[0][':answer/id'] if values[0][0]=='correct' else next(a[':answer/id'] for a,(k,v) in zip(answers,values) if k=='correct')
    rng.shuffle(answers)
    record={'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':{
      ':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,
      ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,
      ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{
      'version':VERSION,'seed':seed,'template':template,'source_ids':[d0['source'][':db/id']],
      'basis':SOURCE['basis'],'family':d['family'],'parameters':{'lower':str(d['a']),'upper':str(d['b']),'scale':str(d['scale'])},
      'bank_profile':profile,'recipes':[{'recipe':k,'value':str(v)} for k,v in values],
      'math':{k:str(d[k]) for k in ('x','y','dx','dy','speed','primitive','length','answer')},
      'calculation':digest([d['family'],str(d['a']),str(d['b'])]),'plot':asset}}
    return validate_generated_record(record)


def choice_cues(record):
    f=record['question'][':question/answer-fields'][0]
    if not f[':answer-field/type'].endswith('/radio'):return None
    choices=f[':answer-field/choices'];cid=f[':answer-field/correct'][1]
    pos=next(i for i,a in enumerate(choices) if a[':answer/id']==cid)
    nums=[float(sp.N(parse_tex(a[':answer/value']))) for a in choices]
    return pos, sorted(nums).index(nums[pos])


def batch(level,count,seed):
    if count<0:raise ValueError('Count must be nonnegative')
    rng=random.Random(seed);records=[];seen=set();family_seen={};family_cues={}
    # Spread genuinely different calculations in a finite batch. Family choice
    # precedes coefficients and bank profile; no seed-specific policies.
    keys=[k for k,d in TEMPLATES.items() if d['level']==level]
    families=list(dict.fromkeys(TEMPLATES[k]['family'] for k in keys));queue=[]
    for i in range(count):
        if not queue:queue=families.copy();rng.shuffle(queue)
        family=queue.pop()
        candidates=[k for k in keys if TEMPLATES[k]['family']==family]
        for attempt in range(300):
            r=generate(level,rng.randrange(2**63),rng.choice(candidates))
            work=r['generation']['calculation']
            if work in family_seen.get(family,set()):continue
            cues=choice_cues(r);previous=family_cues.get(family,[])
            # A repeated visible family must not be solved throughout the batch
            # by one fixed position or numerical rank. Resample the whole item
            # and its plausible bank, without changing any keyed mathematics.
            if cues is not None and previous and any(
                len({p[j] for p in previous} | {cues[j]})==1 for j in (0,1)):
                continue
            break
        else:raise ValueError('Unable to spread main calculations')
        seen.add(work);family_seen.setdefault(family,set()).add(work)
        if len(family_seen[family])==len(intervals(family)):family_seen[family].clear()
        if cues is not None:family_cues.setdefault(family,[]).append(cues)
        records.append(r)
    return records

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='easy')
    p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=('json',),default='json')
    p.add_argument('--template');p.add_argument('--parameters');p.add_argument('--replay',action='store_true');a=p.parse_args()
    levels=('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)
    records=[]
    for level in levels:
        if a.template or a.replay:
            records.extend(generate(level,a.seed+i,a.template,json.loads(a.parameters) if a.parameters else None,a.replay) for i in range(a.count))
        else:records.extend(batch(level,a.count,a.seed))
    print(json.dumps(records,indent=2))
