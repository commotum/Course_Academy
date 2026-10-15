#!/usr/bin/env python3
"""Definite IBP, moderate only. CLI: --seed N --profile q-ID [--json FILE].

Conservative same-method dilation: c=s*c0, b=k*b0, [l,h]=[l0/k,h0/k].
Thus each complete source bank scales by s/k², with no pooled recipes. The
underlying misconception of an individual source distractor is not inferred.
Every recipe is the exact observed expression times the change-of-variable
factor. This preserves distinct banks, signs, domains, fields and IBP stages.
"""
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186064274
KP_UUID='d3aaba0a-3b86-58c3-bbc8-22ced09bc8a8'
VERSION='definite-ibp-1'
HERE=Path(__file__).with_suffix('')
PROFILES=json.loads((HERE/'profiles.json').read_text())
SNAPSHOT=json.loads((HERE/'reference/snapshot.json').read_text())
X=sp.Symbol('x',real=True)

def value(v):return sp.sympify(str(v),locals={'pi':sp.pi,'E':sp.E})
def latex(v):return sp.latex(sp.simplify(v)).replace(r'\left', '').replace(r'\right','')
def parameters(profile,scale=1,dilation=1):
    p=PROFILES[profile];s=sp.Integer(scale);k=sp.Integer(dilation)
    if not 1<=s<=12 or not 1<=k<=8:raise ValueError('bounded positive integer scale/dilation')
    return {'kind':p['kind'],'c':s*value(p['c']),'b':k*value(p['b']),
            'lo':value(p['lo'])/k,'hi':value(p['hi'])/k,'scale':int(s),'dilation':int(k)}

def mathematical_data(p):
    c,b=p['c'],p['b'];fn={'sin':sp.sin,'cos':sp.cos,'exp':sp.exp}[p['kind']]
    vp=fn(b*X)
    v={'sin':-sp.cos(b*X)/b,'cos':sp.sin(b*X)/b,'exp':sp.exp(b*X)/b}[p['kind']]
    w={'sin':-sp.sin(b*X)/b**2,'cos':-sp.cos(b*X)/b**2,'exp':sp.exp(b*X)/b**2}[p['kind']]
    u=c*X;F=sp.expand(u*v-c*w)
    answer=sp.simplify(F.subs(X,p['hi'])-F.subs(X,p['lo']))
    return u,vp,v,w,F,answer

def task_fingerprint(p):
    return '|'.join([p['kind']]+[str(sp.simplify(p[k])) for k in ('c','b','lo','hi')])

def generate(difficulty='moderate',seed=0,profile=None,scale=None,dilation=None,**_):
    if difficulty!='moderate':raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed);profile=profile or rng.choice(sorted(PROFILES));source=PROFILES[profile]
    scale=rng.randint(1,12) if scale is None else scale
    dilation=rng.randint(1,8) if dilation is None else dilation
    p=parameters(profile,scale,dilation);u,vp,v,w,F,correct=mathematical_data(p)
    factor=sp.Rational(scale,dilation*dilation)
    choices=[sp.simplify(value(a['expression'])*factor) for a in source['bank']]
    ci=next(i for i,a in enumerate(source['bank']) if a['correct'])
    assert sp.simplify(choices[ci]-correct)==0
    assert len({sp.srepr(a) for a in choices})==len(choices)
    integral=rf'\int_{{{latex(p["lo"])}}}^{{{latex(p["hi"])}}} {latex(u*vp)}\,\mathrm{{d}}x'
    prompt=source['prefix']+'$'+integral+('=' if source['equality'] else '.')+'$'+source['suffix']
    solution=("Let's use integration by parts. We set\n\n$$\n"
      +rf'\begin{{aligned}}u&={latex(u)} & u^\prime&={latex(p["c"])} \\ '
      +rf'v^\prime&={latex(vp)} & v&={latex(v)}.\end{{aligned}}'+'\n$$\n\n'
      +'Substituting the above into the integration by parts formula, we get\n\n$$\n'
      +rf'\begin{{aligned}}\int u v^\prime\,\mathrm{{d}}x&=uv-\int v u^\prime\,\mathrm{{d}}x \\ '
      +rf'\int {latex(u*vp)}\,\mathrm{{d}}x&={latex(u*v)}-\int {latex(v*p["c"])}\,\mathrm{{d}}x.\end{{aligned}}'+'\n$$\n\n'
      +'Finally, we evaluate the integral and get\n\n$$\n'
      +rf'\begin{{aligned}}{integral}&=\left[{latex(F)}\right]_{{{latex(p["lo"])}}}^{{{latex(p["hi"])}}} \\ '
      +rf'&=\left({latex(F.subs(X,p["hi"]))}\right)-\left({latex(F.subs(X,p["lo"]))}\right) \\ '
      +rf'&={latex(correct)}.\end{{aligned}}'+'\n$$')
    identity=VERSION+'|'+task_fingerprint(p)+'|'+profile
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),identity));fid=str(uuid.uuid5(uuid.UUID(qid),source['field_key']))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'option:'+str(i))),':answer/type':':answer.type/math',':answer/value':latex(a)} for i,a in enumerate(choices)]
    field={':answer-field/id':fid,':answer-field/key':source['field_key'],':answer-field/type':source['field_type'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[ci][':answer/id']]}
    return {'knowledge_point':{'id':KP_UUID,'db_id':KP_ID,'title':'Computing a Definite Integral Using Integration by Parts'},
       'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[field]},
       'generation':{'version':VERSION,'template':p['kind']+'-'+source['field_type'].split('/')[-1], 'profile':profile if 'radio' in source['field_type'] else None,'source_id':profile,'seed':seed,'scale':scale,'dilation':dilation,'parameters':{k:str(v) for k,v in p.items()},'task_fingerprint':task_fingerprint(p),'recipes':[{'source_value':a['tex'],'expression':a['expression'],'factor':str(factor),'interpretation':'observed expression transported by exact integral scaling; misconception unresolved' if not a['correct'] else 'exact definite integral'} for a in source['bank']], 'dependencies':{'sympy':sp.__version__},'evidence_only':False}}

def markdown(record):
    q=record['question'];return q[':question/problem']+'\n\n'+ '\n'.join(a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--difficulty',default='moderate');a.add_argument('--seed',type=int,default=0);a.add_argument('--profile',choices=sorted(PROFILES));a.add_argument('--json',type=Path);o=a.parse_args()
    r=generate(o.difficulty,o.seed,o.profile)
    if o.json:o.json.write_text(json.dumps(r,indent=2)+'\n')
    else:print(json.dumps(r,indent=2))
