#!/usr/bin/env python3
"""Seeded coordinate-image questions. No service, database, or runtime asset writes."""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import random
import re
import uuid
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record
from source_replay import T, KP_ID, KP_UUID, TITLE, set_tex, paired_tex, parse_prompt, parse_sets

VERSION='coordinate-images-3'
FAMILIES={'easy':['affine_single'], 'moderate':['quadratic_single','quadratic_pair','affine_pair','root_single','root_pair','root_cubic','mixed','even_pair'], 'hard':['restricted_quadratics']}
SUPPORT={'affine_single':['808ba9b8-7fbd-5187-9780-5105c365918f','e3ca4cd3-a2f5-5cf2-84dd-64e7db9e1269'], 'quadratic_single':['97007632-9d2f-5a8a-900e-9e7bf33ec6d3','e0f124c2-4201-5bb3-865c-19b9f7b07595'], 'quadratic_pair':['2c5d5a76-6d19-5d2e-8ac8-15cac8c3ca23','2dc3a2b7-620d-5940-a1aa-2a26502f43cc'], 'affine_pair':['507bf285-e98e-529f-bfee-b764a50e3854','7a41944b-5b17-58c0-b340-9129937f3ee2'], 'root_single':['2de12943-54f8-500d-9e95-bde9a205cbca','a1475dc3-badf-5eaf-85a3-fd70878f8785'], 'root_pair':['48a3ec09-02a4-56d8-97ff-afaf8c99de7a','1f6727c7-1507-583d-a603-85c34e4d8ab3'], 'root_cubic':['8f5b7d05-a282-5021-9aa5-8966b1c2524c'], 'mixed':['5fc2dccb-24dd-5003-b2b4-73d21d258e08','d0d4a70a-5321-5bde-a4db-76e8b0c1223a'], 'even_pair':['a792fa16-e1fd-5f30-a128-bbc49a285429'], 'restricted_quadratics':['5fc2dccb-24dd-5003-b2b4-73d21d258e08','468940dc-fef5-52fb-97ca-09170efe4223']}
# Resolve exact capture identities from the bundled complete source.
from source_replay import SOURCE
SOURCE_IDS={q[':question/math-academy-id']:q[':question/id'] for q in SOURCE['record'][':knowledge-point/questions']}
SUPPORT['root_single']=[SOURCE_IDS['q-123763'],SOURCE_IDS['q-123768']]

def tex(x): return s.latex(x)
def coordinate_tex(c):
    # Preserve the selected root operator input, even when a CAS printer would
    # pull a perfect-square factor outside it. The learner argument uses these
    # same original operator roles.
    if c['kind']!='root':return tex(c['expr'])
    a=c['a'];prefix='' if a==1 else '-' if a==-1 else tex(a)
    result=prefix+r'\sqrt{'+tex(c['scale']*c['direction']*(T-c['origin']))+'}'
    if c['c']>0:result+='+'+tex(c['c'])
    elif c['c']<0:result+=tex(c['c'])
    return result

def half(bound,sign,closed):
    return s.Interval(bound,s.oo,left_open=not closed) if sign==1 else s.Interval(-s.oo,bound,right_open=not closed)
def edge(st):
    return (st.start,1,not st.left_open) if st.end==s.oo else (st.end,-1,not st.right_open)
def domain_text(d):
    if d==s.S.Reals:return r't\in(-\infty,\infty)'
    b,sign,closed=edge(d)
    return 't'+(r'\ge ' if sign==1 and closed else '>' if sign==1 else r'\le ' if closed else '<')+tex(b)
def coord(kind,expr,**kw):return {'kind':kind,'expr':expr,**kw}
def quadratic(a,h,k):return coord('quadratic',s.expand(a*(T-h)**2+k),a=a,h=h,k=k)
def affine(a,c):return coord('affine',a*T+c,a=a,c=c)
def root(a,scale,origin,c,direction):
    return coord('root',a*s.sqrt(scale*direction*(T-origin))+c,a=a,scale=scale,origin=origin,c=c,direction=direction)
def signed(r,values=(1,2)):return r.choice([-1,1])*r.choice(values)

def instance(level,r,family=None):
    family=family or r.choice(FAMILIES[level])
    if family not in FAMILIES[level]:raise ValueError('Family/level mismatch')
    b=r.randint(-2,2);direction=r.choice([-1,1]);closed=r.choice([True,False]);d=half(b,direction,closed)
    a,c=signed(r),r.randint(-4,4)
    if family=='affine_single': cs=[affine(a,c),quadratic(1,0,1)]
    elif family=='affine_pair':cs=[affine(a,c),affine(signed(r),r.randint(-4,4))]
    elif family in ('quadratic_single','quadratic_pair','even_pair'):
        d=s.S.Reals;h=r.choice([-2,-1,1,2]);cs=[quadratic(a,h,c),quadratic(signed(r),0,r.randint(-4,4))]
        if family=='even_pair': cs[1]=coord('even',signed(r)*T**4+r.randint(-4,4));cs[1].update(a=cs[1]['expr'].coeff(T,4),c=cs[1]['expr'].subs(T,0))
    elif family in ('root_single','root_pair','root_cubic'):
        # Root's endpoint radicand is a small square; both signs are eligible.
        n=r.choice([0,1,2]);scale=r.choice([1,4]);origin=b-direction*n*n
        cs=[root(a,scale,origin,c,direction),affine(signed(r),r.randint(-3,3))]
        if family=='root_pair':cs[1]=root(signed(r),r.choice([1,4]),b-direction*r.choice([0,1,4]),r.randint(-3,3),direction)
        if family=='root_cubic':cs[1]=coord('cubic',signed(r,(1,))*T**3+r.randint(-3,3));cs[1].update(a=cs[1]['expr'].coeff(T,3),c=cs[1]['expr'].subs(T,0))
    elif family=='mixed':cs=[affine(a,c),quadratic(signed(r),0,r.randint(-4,4))]
    else:
        roles=r.choice([('inside','outside'),('outside','inside'),('outside','outside'),('boundary','inside'),('inside','boundary'),('boundary','outside'),('outside','boundary'),('boundary','boundary')])
        hs=[b+direction*r.choice([1,2]) if role=='inside' else b-direction*r.choice([1,2]) if role=='outside' else b for role in roles]
        # Keep both square completions nontrivial without increasing arithmetic.
        if 0 in hs:return instance(level,r,family)
        cs=[quadratic(signed(r),hs[0],r.randint(-4,4)),quadratic(signed(r),hs[1],r.randint(-4,4))]
    single=family.endswith('_single')
    # Assign eligible coordinate roles before formatting. The irrelevant companion
    # is polynomial and hence never silently restricts the parameter domain.
    if r.choice([True,False]):cs.reverse();assessed=['y'] if single else ['x','y']
    else:assessed=['x'] if single else ['x','y']
    kind='blank' if level=='moderate' and family not in ('root_single','root_cubic','even_pair') and r.choice([True,False]) else 'radio'
    return {'family':family,'domain':d,'coords':dict(zip(['x','y'],cs)),'assessed':assessed,'kind':kind}

def derive(v,c,d):
    """Ordered learner argument, computed without function_range/CAS solving."""
    ex=c['expr'];rows=[v+' &='+coordinate_tex(c)];kind=c['kind']
    if d==s.S.Reals:
        if kind=='quadratic':b=c['k'];sg=1 if c['a']>0 else -1;rows.append('&='+tex(c['a']*(T-c['h'])**2+c['k']));where='The square takes every nonnegative value. Equality occurs at $t='+tex(c['h'])+'$.'
        elif kind=='even':b=c['c'];sg=1 if c['a']>0 else -1;where='The even power takes every nonnegative value and is zero at $t=0$.'
        else:raise ValueError('Unsupported all-real coordinate')
        st=half(b,sg,True)
    else:
        bd,ds,dc=edge(d);b=ex.subs(T,bd);sg=1 if c['a']*ds>0 else -1
        if kind=='quadratic':
            rows.append('&='+tex(c['a']*(T-c['h'])**2+c['k']))
            sg=1 if c['a']>0 else -1;h=c['h'];inside=(h-bd)*ds>0;at=h==bd
            if inside:b=c['k'];inc=True;where='The vertex parameter $t='+tex(h)+'$ is inside the domain, so its value $'+tex(b)+'$ is attained even if the parameter boundary is excluded.'
            elif at:b=c['k'];inc=dc;where='The vertex parameter $t='+tex(h)+'$ is the domain boundary, which is '+('included' if dc else 'excluded')+'.'
            else:inc=dc;where='The vertex parameter $t='+tex(h)+'$ is outside the domain. Moving along the allowed half-line increases the distance from this vertex. At the parameter boundary $t='+tex(bd)+'$, the coordinate value is $'+tex(b)+'$; this boundary is '+('included' if dc else 'excluded')+'.'
        else:
            inc=dc
            if kind=='root':sg=1 if c['a']>0 else -1;where='The radicand starts at $'+tex(s.simplify((b-c['c'])**2/c['a']**2))+'$ and increases without bound along the allowed half-line. The square root is increasing, and its exterior coefficient is $'+tex(c['a'])+'$.'
            else:where=('The cubic is strictly increasing before multiplication by its coefficient.' if kind=='cubic' else 'The affine coefficient is $'+tex(c['a'])+'$.')
            where+=' The boundary $t='+tex(bd)+'$ gives $'+v+'='+tex(b)+'$ and is '+('included' if dc else 'excluded')+'.'
        st=half(b,sg,inc)
    explanation='For $'+v+'$:\n\n$$\n'+r'\begin{aligned}'+'\n'+r' \\ '.join(rows)+'\n'+r'\end{aligned}'+'\n$$\n\n'+where+' The coordinate is continuous on the domain and unbounded '+('above' if edge(st)[1]==1 else 'below')+', so every value on the stated side of the bound occurs. Thus $'+set_tex(v,st)+'$.'
    return st,explanation

def options_for(c,d,correct):
    b,sg,cl=edge(correct);out=[]
    def add(st,reason):
        if st!=correct and all(st!=x[0] for x in out):out.append((st,reason))
    add(half(b,-sg,cl),'reversed bound direction')
    add(half(b,sg,not cl),'incorrect endpoint inclusion')
    ex=c['expr'];wrong=[]
    if c['kind']=='quadratic':
        wrong += [(ex.subs(T,0),'constant term mistaken for extremum'),(c['k'],'unrestricted vertex used without domain check')]
        if d!=s.S.Reals:wrong += [(ex.subs(T,edge(d)[0]),'boundary used instead of admissible vertex')]
        wrong += [(c['k']+2*c['a']*c['h']**2,'wrong sign when completing the square'),(-b,'sign of extremum reversed')]
    elif c['kind']=='root':
        bd=edge(d)[0];raw=s.sqrt(c['scale']*c['direction']*(bd-c['origin']))
        wrong += [(raw+c['c'],'exterior root scale omitted'),(c['c'],'radicand endpoint ignored'),(c['a']**2*raw+c['c'],'exterior scale squared'),(-b,'sign of boundary value reversed')]
    else:
        wrong += [(c.get('c',ex.subs(T,0)),'constant term used as endpoint'),(c['a'],'coefficient used as boundary value')]
        if d!=s.S.Reals:
            bd=edge(d)[0];wrong += [(c['a']*bd-c.get('c',0),'constant translation sign reversed'),(-c['a']*bd+c.get('c',0),'coefficient sign reversed')]
        wrong += [(-b,'sign of boundary value reversed')]
    for val,why in wrong:
        if val!=b:
            add(half(val,sg,cl),why);add(half(val,-sg,cl),why+' and reversed direction')
    return out

def bank(inst,correct,r):
    keys=inst['assessed'];pool={v:options_for(inst['coords'][v],inst['domain'],correct[v]) for v in keys}
    if len(keys)==1:
        v=keys[0];b,sg,cl=edge(correct[v]);numeric=[x for x in pool[v] if edge(x[0])[0]!=b]
        if not numeric:raise ValueError('Insufficient distinct error alternatives')
        # Two endpoint values, both directions. The fifth can repeat either
        # endpoint with the opposite inclusion. Modal endpoint is not a key.
        wrong=r.choice(numeric);e,_,_=edge(wrong[0]);fav=r.choice([b,e]);st=[correct,{v:half(b,-sg,cl)},{v:half(e,sg,cl)},{v:half(e,-sg,cl)},{v:half(fav,sg,not cl)}]
        return st,{'profile':'two-endpoints-two-directions','errors':[wrong[1],'direction','inclusion']}
    v,w=keys
    # Select a complete 2x2 misconception profile, then its fifth alternative.
    # Two single-coordinate errors ensure that each coordinate can be decisive.
    ev=r.choice(pool[v]);ew=r.choice(pool[w]);rows=[dict(correct),{**correct,v:ev[0]},{**correct,w:ew[0]},{v:ev[0],w:ew[0]}]
    extras=[({v:a[0],w:b[0]},a[1]+'; '+b[1]) for a in pool[v] for b in pool[w] if {v:a[0],w:b[0]} not in rows]
    ex,reason=r.choice(extras);rows.append(ex)
    return rows,{'profile':'cartesian-errors','errors':[ev[1],ew[1],reason]}

def finalize(level,problem,solution,fields,meta,feedback=None):
    problem=normalize_prose(problem);solution=normalize_prose(solution)
    normfields=[(key,ft,[(normalize_tex(value),right) for value,right in vals]) for key,ft,vals in fields]
    feedback={normalize_tex(k):normalize_prose(v) for k,v in (feedback or {}).items()}
    identity=json.dumps([VERSION,level,problem,solution,normfields]+([feedback] if feedback else []),sort_keys=True)
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),identity));fs=[]
    for key,kind,vals in normfields:
        fid=str(uuid.uuid5(uuid.UUID(qid),key));choices=[];correct=None
        for value,right in vals:
            aid=str(uuid.uuid5(uuid.UUID(fid),value));choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
            if value in feedback:choices[-1][':answer/feedback']=feedback[value]
            if right:correct=aid
        fs.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]})
    rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fs},'generation':meta}
    return validate_generated_record(rec)

def build(inst,level,seed=0):
    r=random.Random(seed);correct={};parts=[]
    for v in inst['assessed']:
        correct[v],path=derive(v,inst['coords'][v],inst['domain']);parts.append(path)
    problem='Given that a curve is defined parametrically as\n\n$$\nx='+coordinate_tex(inst['coords']['x'])+r',\quad y='+coordinate_tex(inst['coords']['y'])+r',\quad '+domain_text(inst['domain'])+' ,\n$$\n\n'
    problem+=('determine the range of $'+inst['assessed'][0]+'$.' if len(correct)==1 else 'determine the ranges of $x$ and $y$.')
    solution='Consider each coordinate separately.\n\n'+'\n\n'.join(parts)+'\n\nTherefore, $'+paired_tex(correct)+'$.'
    fields=[];bp={'profile':'split-inequality-bound'}
    if inst['kind']=='radio':
        vals,bp=bank(inst,correct,r);r.shuffle(vals);fields=[('selection','radio',[(paired_tex(x),x==correct) for x in vals])]
    else:
        for j,v in enumerate(inst['assessed']):
            st=correct[v];b,sg,cl=edge(st);op=(r'\ge' if cl else '>') if sg==1 else (r'\le' if cl else '<');n=2*j+1
            # Put each fragment next to the coordinate in visible prose; do not
            # reproduce the capture's unmatched dollar crossing placeholders.
            problem+='\n\n$'+v+'$ {{field-'+str(n)+'}}{{field-'+str(n+1)+'}}'
            fields += [('field-'+str(n),'blank',[(op,True)]),('field-'+str(n+1),'blank',[(tex(b),True)])]
    meta={'version':VERSION,'seed':seed,'template':inst['family'],'bank_profile':bp,'source_ids':SUPPORT[inst['family']],'domain':str(inst['domain']),'assessed':inst['assessed'],'coordinates':{v:{k:str(x) for k,x in c.items()} for v,c in inst['coords'].items()},'level_origin':'authored','plot_rating':'none'}
    return finalize(level,problem,solution,fields,meta)

def generate(level,seed=0,family=None):
    r=random.Random(seed)
    for _ in range(100):
        inst=instance(level,r,family)
        try:return build(inst,level,r.getrandbits(64))
        except ValueError as ex:
            if str(ex)!='Insufficient distinct error alternatives':raise
    raise RuntimeError('Unable to build a distinct plausible bank')

def replay_source(sid):
    import source_replay as legacy
    spec=legacy.TEMPLATES[sid]
    p,sol,correct=legacy.source_build(spec,{'sx':1,'sy':1})
    fields=[]
    if spec['kind']=='radio':
        for f in spec['fields']:
            fields.append((f[':answer-field/key'],'radio',[(a[':answer/value'],parse_sets(a[':answer/value'])==correct) for a in f[':answer-field/choices']]))
    else:
        # Rebuild only the malformed response line while preserving every field.
        p=p[:p.index('\n$x$')]
        for v in spec['assessed']:
            n=1 if v=='x' else 3
            p+='\n\n$'+v+'$ {{field-'+str(n)+'}}{{field-'+str(n+1)+'}}'
        for f in sorted(spec['fields'],key=lambda f:f[':answer-field/key']):
            fields.append((f[':answer-field/key'],'blank',[(f[':answer-field/correct'][':answer/value'],True)]))
    return finalize('moderate',p,sol,fields,{'version':VERSION,'source_id':SOURCE_IDS[sid],'template':'source-replay:'+sid,'fidelity':'original parameters and full bank; normalized presentation'})

def replay_exemplar(question_id):
    from pathlib import Path
    q=next(q for q in json.loads((Path(__file__).parent/'exemplars-source.json').read_text()) if q[':question/id']==question_id)
    fields=[]
    for f in q[':question/answer-fields']:
        correct=f[':answer-field/correct'][':answer/id']
        fields.append((f[':answer-field/key'],'radio',[(a[':answer/value'],a[':answer/id']==correct) for a in f[':answer-field/choices']]))
    level=q[':question/difficulty'][':db/ident'].split('/')[-1]
    return finalize(level,q[':question/problem'],q[':question/worked-solution'],fields,{'version':VERSION,'template':'source-replay:'+question_id,'source_id':question_id,'fidelity':'complete original-parameter bank; normalized presentation'},feedback={a[':answer/value']:a[':answer/feedback'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'] if a.get(':answer/feedback')})

def batch(level,count,seed):
    if level=='unclassified':level='moderate'
    r=random.Random(seed);result=[];seen=set()
    # A short practice batch must contrast included and excluded parameter
    # endpoints. IID sampling had served five strict easy ranges together,
    # removing the endpoint-attainment decision from the delivered pool.
    closure_schedule=[True,False]*(count//2)
    if count%2:closure_schedule.append(r.choice([True,False]))
    r.shuffle(closure_schedule)
    for slot in range(count):
        for attempt in range(100):
            rec=generate(level,r.getrandbits(64))
            qid=rec['question'][':question/id']
            if level in ('easy','hard') and count>=2:
                d=parse_prompt(rec['question'][':question/problem'])[2]
                closed=not (d.left_open and d.right_open)
                if closed!=closure_schedule[slot]:continue
            if qid not in seen:break
        else:raise RuntimeError('Unique batch exhausted')
        seen.add(qid);result.append(rec)
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');args=ap.parse_args()
    if args.count<0:ap.error('count must be nonnegative')
    print(json.dumps(batch(args.difficulty,args.count,args.seed),indent=2))
