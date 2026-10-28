#!/usr/bin/env python3
"""Seeded one-step definite integration-by-parts practice; no database or assets."""
import argparse
from collections import Counter
import itertools
import json
import random
import uuid
from pathlib import Path
import sympy as sp
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP_ID = 17592186064274
KP_UUID = 'd3aaba0a-3b86-58c3-bbc8-22ced09bc8a8'
VERSION = 'definite-ibp-3'
X = sp.Symbol('x', real=True)
PROFILES = json.loads((Path(__file__).parent / 'profiles.json').read_text())

def val(v):
    return sp.sympify(str(v), locals={'pi':sp.pi,'E':sp.E})

def clean(v):
    result=sp.simplify(v)
    # SymPy can turn paired exponential endpoint terms into hyperbolic functions.
    # They are not part of this lesson; retain the original exponential primitives.
    if result.has(sp.sinh,sp.cosh):
        result=sp.expand(result.xreplace({a:a.rewrite(sp.exp) for a in result.atoms(sp.sinh,sp.cosh)}))
    return result

def tex(v):
    # No trigonometric simplification or operator-argument rewriting.
    return normalize_tex(sp.latex(clean(v) if v.has(sp.sinh,sp.cosh) else v))

def aligned(rows):
    return '$$\n\\begin{aligned}\n' + '\\\\\n'.join(rows) + '\n\\end{aligned}\n$$'

def parts(p):
    c,b,lo,hi = (val(p[k]) for k in ('c','b','lo','hi'))
    f = {'sin':sp.sin,'cos':sp.cos,'exp':sp.exp}[p['kind']](b*X)
    v = {'sin':-sp.cos(b*X)/b,'cos':sp.sin(b*X)/b,'exp':sp.exp(b*X)/b}[p['kind']]
    w = {'sin':-sp.sin(b*X)/b**2,'cos':-sp.cos(b*X)/b**2,'exp':sp.exp(b*X)/b**2}[p['kind']]
    u=c*X
    F=sp.expand(u*v-c*w)
    top,bottom=(clean(F.subs(X,t)) for t in (hi,lo))
    boundary=clean((u*v).subs(X,hi)-(u*v).subs(X,lo))
    residual=clean(c*(w.subs(X,hi)-w.subs(X,lo)))
    return dict(c=c,b=b,lo=lo,hi=hi,u=u,f=f,v=v,w=w,F=F,top=top,bottom=bottom,
                boundary=boundary,residual=residual,answer=clean(top-bottom))

def rewrite(p,a=1,d=1):
    z=parts(p)
    h={'sin':sp.cos,'cos':sp.sin,'exp':sp.exp}[p['kind']](z['b']*X)
    sign=-1 if p['kind']=='sin' else 1
    B=clean(a*sign*z['c']/z['b'])
    R=clean(-d*sign*z['c']/z['b'])
    out=rf'\left[{tex(B*X*h)}\right]_{{{tex(z["lo"])}}}^{{{tex(z["hi"])}}}'
    if R:
        op='+' if R>0 else '-'
        coefficient=tex(abs(R)) if abs(R)!=1 else ''
        out+=op+coefficient+rf'\int_{{{tex(z["lo"])}}}^{{{tex(z["hi"])}}}{tex(h)}\,\mathrm{{d}}x'
    return normalize_tex(out)

def shortcut_bank(values):
    # A single sign pair or unique sign must not advertise the key in a bank.
    pairs=[(i,j) for i,a in enumerate(values) for j,b in enumerate(values) if j>i and clean(a+b)==0]
    if len(pairs)==1 and 0 in pairs[0]:return True
    # A sole rational, pi-bearing or exponential expression is a bank-only cue.
    shapes=[(v.has(sp.pi),v.has(sp.E,sp.exp),len(sp.Add.make_args(v))) for v in values]
    if shapes.count(shapes[0])==1:return True
    # A unique intersection of modal additive coefficients must not reveal the key.
    terms=[v.as_coefficients_dict() for v in values]
    basis=set().union(*(set(t) for t in terms))
    modes={}
    for term in basis:
        counts=Counter(t.get(term,sp.Integer(0)) for t in terms).most_common()
        if len(counts)==1 or counts[0][1]>counts[1][1]:modes[term]=counts[0][0]
    scores=[sum(t.get(term,sp.Integer(0))==v for term,v in modes.items()) for t in terms]
    if scores.count(max(scores))==1 and scores[0]==max(scores):return True
    signs=[int(sp.sign(v)) for v in values]
    if signs.count(signs[0])==1:return True
    return False

def value_bank(p,rng,exclude_rank=None):
    z=parts(p);B,D,b,c,T,L=(z[k] for k in ('boundary','residual','b','c','top','bottom'))
    recipes={
        'residual sign':B+D,
        'boundary chain factor omitted':b*B-D,
        'residual second chain factor omitted':B-b*D,
        'both chain integrations omitted':b*B-b*b*D,
        'boundary extra chain factor':B/b-D,
        'residual extra chain factor':B-D/b,
        'linear constant applied twice':c*(B-D),
        'boundary only':B,
        'residual only':-D,
        'lower endpoint omitted':T,
        'upper endpoint omitted':-L,
        'endpoints added':T+L,
        'bounds reversed':L-T,
        'linear derivative taken as one':B-D/c,
        'first chain factor omitted throughout':b*(B-D),
    }
    candidates=[]
    for name,v in recipes.items():
        v=clean(v)
        if clean(v-z['answer'])==0:continue
        if any(clean(v-w)==0 for _,w in candidates):continue
        candidates.append((name,v))
    banks=list(itertools.combinations(candidates,4));rng.shuffle(banks)
    for bank in banks:
        values=[z['answer']]+[v for _,v in bank]
        if shortcut_bank(values):continue
        rank=sorted(range(len(values)),key=lambda i:float(values[i])).index(0)
        if rank==exclude_rank:continue
        return [tex(v) for v in values],['correct']+[name for name,_ in bank],rank
    raise ValueError('No distinct plausible value bank')

def make_record(p,difficulty,rng=None,response=None,source_id=None,source_replay=False,exclude_rank=None):
    rng=rng or random.Random(0);z=parts(p)
    response=response or ('blank' if difficulty=='hard' else 'radio')
    integral=rf'\int_{{{tex(z["lo"])}}}^{{{tex(z["hi"])}}} {tex(z["u"]*z["f"])}\,\mathrm{{d}}x'
    prompt='Evaluate the integral. Give an exact answer.\n\n$$\n'+integral+('.' if response=='radio' else '=')+'\n$$'
    if response=='blank':prompt+='\n\n{{field-1}}'
    choices,recipes,rank=([tex(z['answer'])],['exact value'],None) if response=='blank' or source_replay else value_bank(p,rng,exclude_rank)
    key='field-1'
    if source_replay:
        s=PROFILES[source_id];key=s['field_key'];response=s['field_type'].split('/')[-1]
        prompt=s['prefix']+'$$\n'+integral+('=' if s['equality'] else '.')+'\n$$'+s['suffix']
        # A wrong accepted alias in q-349241 is captured evidence, not a valid response.
        choices=[normalize_tex(a['tex']) for a in s['bank'] if response=='radio' or clean(val(a['expression'])-z['answer'])==0]
        correct_index=next(i for i,a in enumerate(s['bank']) if a['correct']) if response=='radio' else 0
        recipes=['observed source bank; see replay evidence']*len(choices)
    else:correct_index=0
    solution='Let $I$ denote the given integral. Choose the factors so that differentiating the linear factor simplifies the remaining integral.\n\n'
    solution+=aligned([rf'u&={tex(z["u"])}, & u^\prime&={tex(z["c"])},',rf'v^\prime&={tex(z["f"])}, & v&={tex(z["v"])}.'])
    solution+='\n\nApply the definite integration-by-parts formula:\n\n'
    solution+='$$\n'+r'\int_a^b uv^\prime\,\mathrm{d}x=[uv]_a^b-\int_a^b vu^\prime\,\mathrm{d}x.'+'\n$$\n\n'
    solution+=aligned([rf'I&=\left[{tex(z["u"]*z["v"])}\right]_{{{tex(z["lo"])}}}^{{{tex(z["hi"])}}}',rf'&\quad-\int_{{{tex(z["lo"])}}}^{{{tex(z["hi"])}}}\left({tex(z["v"])}\right)\left({tex(z["c"])}\right)\,\mathrm{{d}}x,',rf'&={rewrite(p)}.'])
    solution+='\n\nIntegrate the remaining function and combine the two primitive terms:\n\n'
    solution+=aligned([rf'I&=\left[{tex(z["F"])}\right]_{{{tex(z["lo"])}}}^{{{tex(z["hi"])}}}.'])
    solution+='\n\nLet $F(x)$ denote the primitive inside the brackets. Evaluate each endpoint, then subtract the entire lower value:\n\n'
    solution+=aligned([rf'F\left({tex(z["hi"])}\right)&={tex(z["F"].subs(X,z["hi"]))}={tex(z["top"] )},',rf'F\left({tex(z["lo"])}\right)&={tex(z["F"].subs(X,z["lo"]))}={tex(z["bottom"] )}.'])
    solution+='\n\n'+aligned([rf'I&=\left({tex(z["top"])}\right)-\left({tex(z["bottom"])}\right)',rf'&={choices[correct_index]}.'])
    prompt,solution=map(normalize_prose,(prompt,solution));choices=[normalize_tex(a) for a in choices]
    # Identity includes the complete visible normalized content, not seed or a source UUID.
    identity=json.dumps([VERSION,difficulty,prompt,solution,choices],sort_keys=True)
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),identity));fid=str(uuid.uuid5(uuid.UUID(qid),key))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(i))),':answer/type':':answer.type/math',':answer/value':s} for i,s in enumerate(choices)]
    correct=answers[correct_index][':answer/id'];rng.shuffle(answers) if response=='radio' else None
    record={'knowledge_point':{'id':KP_UUID,'db_id':KP_ID,'title':'Computing a Definite Integral Using Integration by Parts'},'question':{
        ':question/id':qid,':question/difficulty':':question.difficulty/'+difficulty,':question/problem':prompt,':question/worked-solution':solution,
        ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+response,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},
        'generation':{'version':VERSION,'template':p['kind']+'-'+response,'parameters':{k:str(v) for k,v in p.items()},'source_ids':[source_id] if source_id else {'sin':['q-49669','q-49676'],'cos':['q-49664','q-349299'],'exp':['q-49684','q-349348']}[p['kind']],
            'source_replay':source_replay,'correct_numeric_rank':rank,'error_profile':recipes,'dependencies':{'sympy':sp.__version__}}}
    return validate_generated_record(record)

TRIG_MOD=[(0,sp.pi/2),(0,sp.pi),(0,2*sp.pi),(-sp.pi/2,sp.pi/2),(-sp.pi,0),(sp.pi/2,sp.pi),(sp.pi,3*sp.pi/2),(-sp.pi,sp.pi/2)]
TRIG_HARD=[(sp.pi/2,sp.pi),(sp.pi,3*sp.pi/2),(-sp.pi,sp.pi/2),(-sp.pi/2,sp.pi),(-sp.pi,sp.pi),(sp.pi/2,3*sp.pi/2)]
EXP_MOD=[(0,1),(0,2),(-1,0),(-2,0),(-1,1),(-2,-1)]
EXP_HARD=[(0,2),(-1,0),(-2,0),(-1,2),(-2,-1)]

def cases(difficulty):
    if difficulty=='easy':
        return [(kind,lo,hi) for kind in ('sin','cos','exp') for lo,hi in ([(0,1),(0,2)] if kind=='exp' else [(0,sp.pi/2),(0,sp.pi)])]
    return [(kind,lo,hi) for kind in ('sin','cos','exp') for lo,hi in ((EXP_HARD if difficulty=='hard' else EXP_MOD) if kind=='exp' else (TRIG_HARD if difficulty=='hard' else TRIG_MOD))]

def batch(difficulty,count,seed):
    if difficulty=='unclassified':difficulty='moderate'
    if difficulty not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if count<0:raise ValueError('Negative count')
    rng=random.Random(seed);deck=[];output=[];seen=set();attempts=0;pending=None;last_radio_rank={}
    while len(output)<count:
        attempts+=1
        if attempts>max(500,count*80):raise ValueError('Requested batch exceeds available unique practice')
        if not deck:
            # Function family first; interleave shuffled phase cases so finite batches vary method.
            groups=[]
            for kind in rng.sample(['sin','cos','exp'],3):
                group=[t for t in cases(difficulty) if t[0]==kind];rng.shuffle(group);groups.append(group)
            deck=[g[i] for i in range(max(map(len,groups))) for g in groups if i<len(g)]
            deck.reverse()
        if pending is None:
            kind,l,h=deck.pop()
        else:
            kind,l,h=rng.choice([t for t in cases(difficulty) if t[0]==pending])
        # Keep a rejected family slot until a valid distinct bank is found.
        # Advancing the deck on rejection systematically removed sine from short batches.
        pending=kind
        b=rng.choice([1,2,3])*(-1 if kind=='exp' and rng.randrange(2) else 1)
        b=rng.choice([1,2]) if difficulty=='easy' else b
        c=rng.choice([-3,-2,-1,1,2,3]);lo,hi=sorted([sp.sympify(l)/b,sp.sympify(h)/b])
        p=dict(kind=kind,c=c,b=b,lo=lo,hi=hi)
        z=parts(p)
        if difficulty=='hard' and (z['top']==0 or z['bottom']==0):continue
        semantic='|'.join(str(p[k]) for k in ('kind','c','b','lo','hi'))
        if semantic in seen:continue
        response='blank' if difficulty=='hard' or difficulty=='moderate' and rng.randrange(2) else 'radio'
        try:r=make_record(p,difficulty,rng,response,exclude_rank=last_radio_rank.get(kind))
        except ValueError:continue
        if response=='radio':last_radio_rank[kind]=r['generation']['correct_numeric_rank']
        r['generation']['seed']=seed;r['generation']['index']=len(output)
        seen.add(semantic);output.append(r);pending=None
    return output

def replay(source_id):
    s=PROFILES[source_id];p={k:s[k] for k in ('kind','c','b','lo','hi')}
    return make_record(p,'moderate',random.Random(0),source_id=source_id,source_replay=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='moderate',choices=['easy','moderate','hard','unclassified']);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',default='json',choices=['json']);ap.add_argument('--source-id',choices=sorted(PROFILES))
    a=ap.parse_args();print(json.dumps([replay(a.source_id)] if a.source_id else batch(a.difficulty,a.count,a.seed),ensure_ascii=False,indent=2))
