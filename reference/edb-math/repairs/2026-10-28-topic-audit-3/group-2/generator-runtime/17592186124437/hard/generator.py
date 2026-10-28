#!/usr/bin/env python3
"""Seeded coordinate-section slopes. No service or database access."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import uuid
import sympy as s
from easy_math import x,y,tex,val,math_data,source_rows,expression,sample,CONFIG
from math_format import normalize_prose,normalize_tex,validate_generated_record

VERSION='section-slopes-2'
KP={'db_id':17592186124437,'id':'049e8586-8348-50be-ac56-4ea79eba43cd','title':'Finding the Slope of the Tangent Line to a Curve at a Point'}
EASY=tuple(t for t in CONFIG if not t.startswith('canonical_'))+('exp_sin','translated_sin','exp_cancel')
BANDS=('easy','moderate','hard')

def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(text):
    return str(uuid.uuid5(uuid.NAMESPACE_URL,'ca:section-slopes:'+text))
def aligned(rows):
    return '$$\n'+r'\begin{aligned}'+'\n'+(' \\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'
def spec_tex(expr):
    return tex(expr)
def assemble(level,prompt,solution,key,meta,values=None):
    # Normalize BEFORE identities; values are bare TeX, never prose math blocks.
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    values=[normalize_tex(v) for v in (values or [key])];key=normalize_tex(key)
    ident=digest({'v':VERSION,'level':level,'prompt':prompt,'solution':solution,'values':values,'key':key})
    qid=uid(ident);fid=uid(qid+':slope')
    choices=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'slope' if len(values)==1 else 'selection',':answer-field/type':':answer-field.type/'+('blank' if len(values)==1 else 'radio'),':answer-field/choices':choices,':answer-field/correct':[':answer/id',next(c[':answer/id'] for c in choices if c[':answer/value']==key)]}]}
    rec={'knowledge_point':KP.copy(),'question':q,'generation':{'version':VERSION,**meta}}
    return validate_generated_record(rec)

def clean_tex(text):
    for name in ("sin","cos","ln"):
        text=text.replace(r"\operatorname{"+name+"}","\\"+name+" ")
    return text.replace("⁡", "").replace("π", r"\pi ")

def easy_data(t,p):
    if t in CONFIG:
        d,parts,ans,_,_=math_data(t,p)
        return d,[clean_tex(z) for z in source_rows(t,p)],ans,clean_tex(expression(t,p))
    X,Y=p['x'],p['y']
    if t=='exp_sin':
        d=y*s.exp(s.sin(x*y))*s.cos(x*y);angle=X*Y
        rows=[rf'({tex(Y)})e^{{\sin(({tex(X)})({tex(Y)}))}}\cos(({tex(X)})({tex(Y)}))',rf'({tex(Y)})e^{{{tex(s.sin(angle))}}}({tex(s.cos(angle))})']
        expr=r'y e^{\sin(xy)}\cos(xy)'
    elif t=='translated_sin':
        d=y*s.sin(x*y-s.pi/3);angle=X*Y-s.pi/3
        rows=[rf'({tex(Y)})\sin(({tex(X)})({tex(Y)})-\frac{{\pi}}{{3}})',rf'({tex(Y)})\sin({tex(angle)})',rf'({tex(Y)})({tex(s.sin(angle))})']
        expr=r'y\sin(xy-\frac{\pi}{3})'
    else:
        d=(s.exp(x)-s.exp(y))/(2*x)+2*y
        rows=[rf'\frac{{e^{{{tex(X)}}}-e^{{{tex(Y)}}}}}{{2({tex(X)})}}+2({tex(Y)})']
        expr=r'\frac{e^x-e^y}{2x}+2y'
    ans=s.simplify(d.subs({x:X,y:Y}));rows.append(tex(ans))
    return d,rows,ans,expr

def easy_sample(t,r):
    if t in CONFIG:
        p={k:val(v) for k,v in sample(t,r).items()}
        # cos_sum varies its free and fixed familiar angles, including nonzero
        # first terms. No template-to-constant-key shortcut.
        if t=='rational_radical':p.update(x=s.Integer(1),y=s.Integer(r.choice([-3,-2,-1,1,2,3])))
        if t=='cos_sum':p.update(x=r.choice([0,s.pi/2,s.pi,3*s.pi/2]),y=r.choice([0,s.pi,2*s.pi]))
        return p
    if t=='exp_sin':
        Y=r.choice([-2,-1,1,2]);return {'x':r.choice([-2,-1,0,1,2])*s.pi/Y,'y':s.Integer(Y)}
    if t=='translated_sin':return {'x':s.Integer(r.choice([-2,2])),'y':r.choice([-3,-1,1,3])*s.pi/4}
    X=r.choice([-2,-1,1,2]);Y=r.choice([-2,-1,1,2]);return {'x':s.Integer(X),'y':s.Integer(Y),'z':s.Integer(r.randint(-5,5))}

def easy_record(t,p,v,r,level='easy',surface=None):
    d,rows,ans,expr=easy_data(t,p)
    fixed='y' if v=='x' else 'x';X,Y=p['x'],p['y'];H=p[fixed]
    point=(rf'$P({tex(X)},{tex(Y)},{tex(p["z"])})$' if 'z' in p else rf'the point $P$ with ${v}$-coordinate ${tex(p[v])}$')
    prompt=rf'A surface $S$ is defined by $z=f(x,y)$. The curve $C$ is its intersection with the plane ${fixed}={tex(H)}$. Given that {point} lies on $C$ and that'+'\n\n$$\n'+rf'f_{v}(x,y)={expr}.'+'\n$$\n\n'+rf'Find the exact slope of the tangent to $C$ at $P$, measured with respect to ${v}$. $m=$ '+'{{slope}}'
    if surface is not None:
        prompt=rf'A surface is defined by $z=f(x,y)={tex(surface)}$. Its section in the plane ${fixed}={tex(H)}$ passes through $P$ with $(x,y)=({tex(X)},{tex(Y)})$. Given $f_{v}(x,y)={tex(d)}$, find the exact section slope at $P$. $m=$ '+'{{slope}}'
    deriv=[rf'm=f_{v}({tex(X)},{tex(Y)})&={rows[0]}']+['&='+row for row in rows[1:]]
    if rows[-1]!=tex(ans) and not rows[-1].endswith('='+tex(ans)):deriv+=['&='+tex(ans)]
    solution=rf'The plane ${fixed}={tex(H)}$ holds ${fixed}$ constant, so ${v}$ varies and the section slope is $dz/d{v}=f_{v}(x,y)$. Substitute the ordered coordinates of $P$:'+'\n\n'+aligned(deriv)
    if 'z' in p:solution+='\n\n'+rf'The height ${tex(p["z"])}$ is not an input to the supplied partial derivative.'
    # Store exact symbolic strings for replay, not as a substitute for checking
    # the actual prompt/key in validation.
    return assemble(level,prompt,solution,tex(ans),{'template':t,'orientation':v,'parameters':{k:str(vv) for k,vv in p.items()},'derivative':str(d),'answer':str(ans),'support':'supplied-partial','response_contract':'authored exact entry'})

def poly_data(p):
    a,b,c,d=[s.Integer(p[k]) for k in ('a','b','c','d')]
    f=c+a*x*x+b*x*y+d*y*y
    fx=2*a*x+b*y;fy=b*x+2*d*y
    return f,fx,fy

def render_section(p,v,f,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fixed='y' if v=='x' else 'x';symbol=x if v=='x' else y
    X,Y=s.Integer(p['x']),s.Integer(p['y']);U=float(X if v=='x' else Y)
    g=f.subs({y:Y} if v=='x' else {x:X});Z=float(g.subs(symbol,U))
    name='section-'+digest({'p':p,'v':v})[:20]+'.png';path=Path(out)/name;path.parent.mkdir(parents=True,exist_ok=True)
    ts=[U-2+4*i/200 for i in range(201)];zs=[float(g.subs(symbol,t)) for t in ts]
    fig,ax=plt.subplots(figsize=(5.6,3.6),dpi=120)
    ax.plot(ts,zs,color='#225ea8',linewidth=2);ax.scatter([U],[Z],color='#b2182b',zorder=3)
    ax.annotate('P',xy=(U,Z),xytext=(9,11),textcoords='offset points',fontsize=12)
    ax.set_xlabel(v,fontsize=12);ax.set_ylabel('z',rotation=0,fontsize=12,labelpad=10)
    ax.set_title(f'{fixed} = {p[fixed]}',fontsize=12);ax.grid(alpha=.2);ax.margins(y=.18);fig.tight_layout();fig.savefig(path);plt.close(fig)
    return name

def moderate_record(p,v,out,diagram=True):
    f,fx,fy=poly_data(p);X,Y=s.Integer(p['x']),s.Integer(p['y']);fixed='y' if v=='x' else 'x'
    d=fx if v=='x' else fy;ans=d.subs({x:X,y:Y});Z=f.subs({x:X,y:Y});coord=X if v=='x' else Y
    if v=='x':deriv=rf'2({p["a"]})x+({p["b"]})y';sub=rf'2({p["a"]})({X})+({p["b"]})({Y})'
    else:deriv=rf'({p["b"]})x+2({p["d"]})y';sub=rf'({p["b"]})({X})+2({p["d"]})({Y})'
    prompt=rf'A surface $S$ is defined by $z=f(x,y)={tex(f)}$. The curve $C$ is the intersection of $S$ with the plane ${fixed}={p[fixed]}$.'
    if diagram:
        asset=render_section(p,v,f,out);prompt+=rf' The diagram shows the section with ${v}$ horizontal and $z$ vertical.'+'\n\n![]('+asset+')'
    prompt+='\n\n'+rf'Find the exact slope of the tangent to $C$ at $P({X},{Y},{tex(Z)})$, measured with respect to ${v}$. $m=$ '+'{{slope}}'
    solution=rf'The plane fixes ${fixed}$; ${v}$ varies. Use $f_{v}$ and hold ${fixed}$ constant when differentiating:'+'\n\n'+aligned([rf'f_{v}(x,y)&={deriv}',rf'&={tex(d)}',rf'm=f_{v}({X},{Y})&={sub}',rf'&={tex(ans)}'])
    symbol=x if v=='x' else y;g=f.subs({y:Y} if v=='x' else {x:X})
    solution+='\n\n'+rf'As a check, the restricted curve is $g({v})={tex(g)}$. Differentiating it gives $g^{{\prime}}({tex(coord)})={tex(ans)}$.'
    return assemble('moderate',prompt,solution,tex(ans),{'template':'quadratic','orientation':v,'parameters':p,'surface':str(f),'derivative':str(d),'answer':str(ans),'support':'surface and section diagram' if diagram else 'surface','response_contract':'exact entry'})

def hard_record(p,v):
    fixed='y' if v=='x' else 'x';u=y if v=='x' else x;z=x if v=='x' else y
    a,b,k=[s.Integer(p[key]) for key in ('a','b','k')];U=s.Integer(p[fixed]);V=s.Integer(p[v]);X,Y=s.Integer(p['x']),s.Integer(p['y'])
    f=a*u*s.log(z)+b*s.exp(k*u*z)/z
    # Ordered logarithm + quotient/chain derivation, not CAS differentiation.
    deriv=a*u/z+b*s.exp(k*u*z)*(k*u*z-1)/z**2
    log_value=a*U/V;exp_coefficient=b*(k*U*V-1)/V**2
    ans=log_value+exp_coefficient*s.exp(k*U*V)
    # Preserve the operator input; simplify only rational coefficients.
    key=tex(log_value)
    if exp_coefficient:
        magnitude=abs(exp_coefficient)
        key+=('+' if exp_coefficient>0 else '-')+('' if magnitude==1 else tex(magnitude))+rf'e^{{{tex(k*U*V)}}}'
    inputtex=tex(k*u*z);exptex=tex(k*U*V)
    btext='' if abs(b)==1 else tex(abs(b))
    ftex=rf'{tex(a*u)}\ln {v}'+('+' if b>0 else '-')+rf'\frac{{{btext}e^{{{inputtex}}}}}{{{v}}}'
    prompt=rf'A surface $S$ is defined, for ${v}>0$, by'+'\n\n$$\n'+rf'z=f(x,y)={ftex}.'+'\n$$\n\n'+rf'The curve $C$ is the intersection of $S$ with the plane ${fixed}={tex(U)}$. Find the exact slope of its tangent at the point $P$ with ${v}$-coordinate ${tex(V)}$, measured with respect to ${v}$. $m=$ '+'{{slope}}'
    rows=[rf'f_{v}(x,y)&=\frac{{{tex(a*u)}}}{{{v}}}+{tex(b)}\frac{{{v}({tex(k*u)}e^{{{inputtex}}})-e^{{{inputtex}}}}}{{{v}^2}}',rf'&=\frac{{{tex(a*u)}}}{{{v}}}+\frac{{{tex(b)}e^{{{inputtex}}}({tex(k*u*z)}-1)}}{{{v}^2}}',rf'm=f_{v}({X},{Y})&=\frac{{{tex(a*U)}}}{{{tex(V)}}}+\frac{{{tex(b)}e^{{{exptex}}}({exptex}-1)}}{{({tex(V)})^2}}',rf'&={key}']
    solution=rf'The plane fixes ${fixed}$, so the section slope is $f_{v}({X},{Y})$. Hold ${fixed}$ constant. The logarithm contributes ${tex(a*u)}/{v}$. For the quotient, differentiate its exponential using the chain factor ${tex(k*u)}$, then subtract the numerator times the derivative of the denominator. Simplify the rational coefficients and keep the evaluated exponential input:'+'\n\n'+aligned(rows)
    return assemble('hard',prompt,solution,key,{'template':'log-exp-quotient','orientation':v,'parameters':p,'surface':str(f),'derivative':str(deriv),'answer':str(ans),'support':'surface only','response_contract':'authored exact entry','quotient_cancels':bool(k*U*V==1)})

def generate(level,seed=0,template=None,parameters=None,orientation=None,output_dir=None):
    r=random.Random(seed);v=orientation or r.choice(('x','y'))
    if level=='easy':
        t=template or r.choice(EASY);p={k:val(vv) for k,vv in parameters.items()} if parameters else easy_sample(t,r)
        return easy_record(t,p,v,r)
    if level=='moderate':
        p=parameters or {'a':r.choice([-3,-2,-1,1,2,3]),'b':r.choice([-2,-1,0,1,2]),'c':r.randint(6,15),'d':r.choice([-3,-2,-1,1,2,3]),'x':r.choice([-2,-1,0,1,2]),'y':r.choice([-2,-1,0,1,2])}
        out=output_dir or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
        if not out:raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR for generated section diagrams')
        return moderate_record(p,v,out)
    if level=='hard':
        p=parameters or {'a':r.choice([1,2]),'b':r.choice([-2,-1,1,2]),'k':r.choice([1,2]),('y' if v=='x' else 'x'):r.choice([-2,-1,1,2]),v:r.choice([1,2])}
        return hard_record(p,v)
    raise ValueError('unknown difficulty')

def generate_batch(level,count,seed,output_dir=None):
    """Cycle decision families before filling values; no favorable-seed search."""
    r=random.Random(seed);families=list(EASY) if level=='easy' else [None];r.shuffle(families)
    records=[];seen=set();attempt=0
    while len(records)<count:
        t=families[len(records)%len(families)];rec=generate(level,r.getrandbits(64),template=t,output_dir=output_dir)
        # Semantic dedup ignores bank order, IDs and ancillary heights.
        m=rec['generation'];finger=digest({'t':m['template'],'v':m['orientation'],'d':m['derivative'],'xy':{k:m['parameters'][k] for k in ('x','y')}})
        if finger not in seen:records.append(rec);seen.add(finger)
        attempt+=1
        if attempt>max(1000,count*100):raise ValueError('requested batch exceeds practical semantic support')
    return records

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=[*BANDS,'unclassified','all'],default='easy');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');args=ap.parse_args()
    if args.count<0:ap.error('count must be nonnegative')
    levels=BANDS if args.difficulty=='all' else ('easy' if args.difficulty=='unclassified' else args.difficulty,)
    records=[q for level in levels for q in generate_batch(level,args.count,args.seed)]
    print(json.dumps(records,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
